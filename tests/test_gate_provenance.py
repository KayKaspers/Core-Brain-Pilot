"""Tests der reinen Provenance-/Verdikt-Logik (CBP-WP-017)."""

from __future__ import annotations

import unittest

from core.core_brain.gate.models import CRITERION_PRODUCER_CLASS, CriterionResult
from core.core_brain.gate.provenance import (
    ArtifactDescriptor,
    canonical_artifact_sha256,
    canonical_binding_sha256,
    evaluate_criterion_artifacts,
)

EXPECTED = "e" * 64
AID_A = "art-" + "0" * 24
AID_B = "art-" + "1" * 24

_BINDING_KWARGS = dict(
    source_id="src-0123456789abcdef01234567",
    mapping_id="MAP-EXAMPLE-0001",
    criterion=4,
    mapping_draft_sha256="a" * 64,
    mapping_policy_sha256="b" * 64,
    registry_record_sha256="c" * 64,
    gate_contract_revision="1.0",
    gate_contract_sha256="d" * 64,
    evidence_contract_revision="2.0",
    evidence_contract_sha256="f" * 64,
    evidence_revision=1,
)


def desc(criterion, *, binding=EXPECTED, art_rev=1, artifact_id=AID_A,
         producer_class=None, corrupt=False):
    pc = producer_class if producer_class is not None else CRITERION_PRODUCER_CLASS[criterion]
    sha = canonical_artifact_sha256(
        artifact_id=artifact_id, binding_sha256=binding, producer_class=pc,
        evidence_revision=art_rev, synthetic_test_only=True,
    )
    if corrupt:
        sha = "9" * 64
    return ArtifactDescriptor(
        artifact_id=artifact_id, artifact_sha256=sha, binding_sha256=binding,
        producer_class=pc, evidence_revision=art_rev, synthetic_test_only=True,
    )


def verdict(criterion, arts, *, rev=1):
    return evaluate_criterion_artifacts(
        criterion, tuple(arts),
        expected_binding_sha256=EXPECTED, bundle_evidence_revision=rev,
    )


class TestArtifactHash(unittest.TestCase):
    def test_deterministic(self) -> None:
        a = canonical_artifact_sha256(artifact_id=AID_A, binding_sha256=EXPECTED,
                                      producer_class="foundation-form",
                                      evidence_revision=1, synthetic_test_only=True)
        b = canonical_artifact_sha256(artifact_id=AID_A, binding_sha256=EXPECTED,
                                      producer_class="foundation-form",
                                      evidence_revision=1, synthetic_test_only=True)
        self.assertEqual(a, b)
        self.assertRegex(a, r"\A[0-9a-f]{64}\Z")

    def test_hash_excludes_itself(self) -> None:
        # Zwei Deskriptoren, identisch bis auf artifact_sha256: die Integritäts-
        # prüfung akzeptiert nur den korrekten; der Hash ist nicht Teil seiner
        # eigenen Berechnung.
        good = desc(4)
        tampered = ArtifactDescriptor(
            artifact_id=good.artifact_id, artifact_sha256="0" * 64,
            binding_sha256=good.binding_sha256, producer_class=good.producer_class,
            evidence_revision=good.evidence_revision, synthetic_test_only=True,
        )
        self.assertIsNone(verdict(4, [good]).override)
        self.assertEqual(verdict(4, [tampered]).override,
                         CriterionResult.INVALID_EVIDENCE)

    def test_field_change_changes_hash(self) -> None:
        base = canonical_artifact_sha256(artifact_id=AID_A, binding_sha256=EXPECTED,
                                         producer_class="foundation-form",
                                         evidence_revision=1, synthetic_test_only=True)
        other = canonical_artifact_sha256(artifact_id=AID_B, binding_sha256=EXPECTED,
                                          producer_class="foundation-form",
                                          evidence_revision=1, synthetic_test_only=True)
        self.assertNotEqual(base, other)


class TestBindingHash(unittest.TestCase):
    def test_each_component_drift_changes_hash(self) -> None:
        base = canonical_binding_sha256(**_BINDING_KWARGS)
        drifts = {
            "source_id": "src-ffffffffffffffffffffffff",
            "mapping_id": "MAP-OTHER",
            "criterion": 5,
            "mapping_draft_sha256": "1" * 64,
            "mapping_policy_sha256": "2" * 64,
            "registry_record_sha256": "3" * 64,
            "gate_contract_revision": "9.9",
            "gate_contract_sha256": "4" * 64,
            "evidence_contract_revision": "9.9",
            "evidence_contract_sha256": "5" * 64,
            "evidence_revision": 2,
        }
        for field, value in drifts.items():
            with self.subTest(field=field):
                kwargs = dict(_BINDING_KWARGS)
                kwargs[field] = value
                self.assertNotEqual(canonical_binding_sha256(**kwargs), base)

    def test_record_sha_none_is_deterministic(self) -> None:
        kwargs = dict(_BINDING_KWARGS)
        kwargs["registry_record_sha256"] = None
        self.assertEqual(canonical_binding_sha256(**kwargs),
                         canonical_binding_sha256(**kwargs))


class TestVerdict(unittest.TestCase):
    def test_fresh_is_none_and_validated(self) -> None:
        ce = verdict(4, [desc(4)])
        self.assertIsNone(ce.override)
        self.assertEqual((ce.validated_count, ce.invalid_count,
                          ce.stale_count, ce.conflicting_count), (1, 0, 0, 0))

    def test_invalid_hash(self) -> None:
        ce = verdict(4, [desc(4, corrupt=True)])
        self.assertEqual(ce.override, CriterionResult.INVALID_EVIDENCE)
        self.assertEqual(ce.invalid_count, 1)

    def test_invalid_producer_class(self) -> None:
        ce = verdict(4, [desc(4, producer_class="operator-review-form")])
        self.assertEqual(ce.override, CriterionResult.INVALID_EVIDENCE)

    def test_stale_binding(self) -> None:
        ce = verdict(4, [desc(4, binding="d" * 64)])
        self.assertEqual(ce.override, CriterionResult.STALE_EVIDENCE)
        self.assertEqual(ce.stale_count, 1)

    def test_stale_evidence_revision(self) -> None:
        ce = verdict(4, [desc(4, art_rev=2)], rev=1)
        self.assertEqual(ce.override, CriterionResult.STALE_EVIDENCE)

    def test_conflict_two_distinct(self) -> None:
        ce = verdict(4, [desc(4, artifact_id=AID_A), desc(4, artifact_id=AID_B)])
        self.assertEqual(ce.override, CriterionResult.CONFLICTING_EVIDENCE)
        self.assertEqual(ce.conflicting_count, 2)

    def test_conflict_same_id_different_hash(self) -> None:
        # Gleiche artifact_id, aber unterschiedliche Bindung ⇒ anderer Hash.
        a = desc(4, artifact_id=AID_A, binding=EXPECTED)
        b = desc(4, artifact_id=AID_A, binding="d" * 64)
        ce = verdict(4, [a, b])
        self.assertEqual(ce.override, CriterionResult.CONFLICTING_EVIDENCE)

    def test_identical_duplicates_dedup(self) -> None:
        a = desc(4)
        ce = verdict(4, [a, a, a])
        self.assertIsNone(ce.override)
        self.assertEqual(ce.validated_count, 1)  # nur einmal gezählt

    def test_invalid_priority_over_conflict(self) -> None:
        ce = verdict(4, [desc(4, artifact_id=AID_A, corrupt=True),
                         desc(4, artifact_id=AID_B)])
        self.assertEqual(ce.override, CriterionResult.INVALID_EVIDENCE)

    def test_conflict_priority_over_stale(self) -> None:
        ce = verdict(4, [desc(4, artifact_id=AID_A, binding="d" * 64),
                         desc(4, artifact_id=AID_B)])
        self.assertEqual(ce.override, CriterionResult.CONFLICTING_EVIDENCE)

    def test_order_independence(self) -> None:
        a = desc(4, artifact_id=AID_A)
        b = desc(4, artifact_id=AID_B)
        self.assertEqual(verdict(4, [a, b]).override, verdict(4, [b, a]).override)
        self.assertEqual(verdict(4, [a, b]).conflicting_count,
                         verdict(4, [b, a]).conflicting_count)

    def test_empty_is_none(self) -> None:
        self.assertIsNone(verdict(4, []).override)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
