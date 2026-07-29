"""Tests der reinen Provenance-/Verdikt-Logik (CBP-WP-017/018)."""

from __future__ import annotations

import unittest

from core.core_brain.gate.models import (
    CRITERION_PRODUCER_CLASS,
    SECURITY_CONTROL_PRODUCER_CLASS,
    CriterionResult,
    GateReasonCode,
)
from core.core_brain.gate.provenance import (
    ArtifactDescriptor,
    BindingVerdict,
    canonical_artifact_sha256,
    canonical_binding_sha256,
    evaluate_criterion_artifacts,
    evaluate_security_binding,
)

EXPECTED = "e" * 64
AID_A = "art-" + "0" * 24
AID_B = "art-" + "1" * 24

# Generisches Nicht-Security-Kriterium (structural-form) für die reinen
# WP-017-Provenance-Tests. Ein structural-form-Deskriptor trägt kein control_id
# und ist damit unter Evidence Schema 3.0 ein zulässiger Deskriptor. Die
# Security-Control-Bindungslogik wird getrennt in den Test*Security*-Klassen mit
# gültigem control_id geprüft (CBP-WP-018).
GENERIC_CRITERION = 2

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
        good = desc(GENERIC_CRITERION)
        tampered = ArtifactDescriptor(
            artifact_id=good.artifact_id, artifact_sha256="0" * 64,
            binding_sha256=good.binding_sha256, producer_class=good.producer_class,
            evidence_revision=good.evidence_revision, synthetic_test_only=True,
        )
        self.assertIsNone(verdict(GENERIC_CRITERION, [good]).override)
        self.assertEqual(verdict(GENERIC_CRITERION, [tampered]).override,
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
        ce = verdict(GENERIC_CRITERION, [desc(GENERIC_CRITERION)])
        self.assertIsNone(ce.override)
        self.assertEqual((ce.validated_count, ce.invalid_count,
                          ce.stale_count, ce.conflicting_count), (1, 0, 0, 0))

    def test_invalid_hash(self) -> None:
        ce = verdict(GENERIC_CRITERION, [desc(GENERIC_CRITERION, corrupt=True)])
        self.assertEqual(ce.override, CriterionResult.INVALID_EVIDENCE)
        self.assertEqual(ce.invalid_count, 1)

    def test_invalid_producer_class(self) -> None:
        ce = verdict(GENERIC_CRITERION, [desc(GENERIC_CRITERION, producer_class="operator-review-form")])
        self.assertEqual(ce.override, CriterionResult.INVALID_EVIDENCE)

    def test_stale_binding(self) -> None:
        ce = verdict(GENERIC_CRITERION, [desc(GENERIC_CRITERION, binding="d" * 64)])
        self.assertEqual(ce.override, CriterionResult.STALE_EVIDENCE)
        self.assertEqual(ce.stale_count, 1)

    def test_stale_evidence_revision(self) -> None:
        ce = verdict(GENERIC_CRITERION, [desc(GENERIC_CRITERION, art_rev=2)], rev=1)
        self.assertEqual(ce.override, CriterionResult.STALE_EVIDENCE)

    def test_conflict_two_distinct(self) -> None:
        ce = verdict(GENERIC_CRITERION, [desc(GENERIC_CRITERION, artifact_id=AID_A), desc(GENERIC_CRITERION, artifact_id=AID_B)])
        self.assertEqual(ce.override, CriterionResult.CONFLICTING_EVIDENCE)
        self.assertEqual(ce.conflicting_count, 2)

    def test_conflict_same_id_different_hash(self) -> None:
        # Gleiche artifact_id, aber unterschiedliche Bindung ⇒ anderer Hash.
        a = desc(GENERIC_CRITERION, artifact_id=AID_A, binding=EXPECTED)
        b = desc(GENERIC_CRITERION, artifact_id=AID_A, binding="d" * 64)
        ce = verdict(GENERIC_CRITERION, [a, b])
        self.assertEqual(ce.override, CriterionResult.CONFLICTING_EVIDENCE)

    def test_identical_duplicates_dedup(self) -> None:
        a = desc(GENERIC_CRITERION)
        ce = verdict(GENERIC_CRITERION, [a, a, a])
        self.assertIsNone(ce.override)
        self.assertEqual(ce.validated_count, 1)  # nur einmal gezählt

    def test_invalid_priority_over_conflict(self) -> None:
        ce = verdict(GENERIC_CRITERION, [desc(GENERIC_CRITERION, artifact_id=AID_A, corrupt=True),
                         desc(GENERIC_CRITERION, artifact_id=AID_B)])
        self.assertEqual(ce.override, CriterionResult.INVALID_EVIDENCE)

    def test_conflict_priority_over_stale(self) -> None:
        ce = verdict(GENERIC_CRITERION, [desc(GENERIC_CRITERION, artifact_id=AID_A, binding="d" * 64),
                         desc(GENERIC_CRITERION, artifact_id=AID_B)])
        self.assertEqual(ce.override, CriterionResult.CONFLICTING_EVIDENCE)

    def test_order_independence(self) -> None:
        a = desc(GENERIC_CRITERION, artifact_id=AID_A)
        b = desc(GENERIC_CRITERION, artifact_id=AID_B)
        self.assertEqual(verdict(GENERIC_CRITERION, [a, b]).override, verdict(GENERIC_CRITERION, [b, a]).override)
        self.assertEqual(verdict(GENERIC_CRITERION, [a, b]).conflicting_count,
                         verdict(GENERIC_CRITERION, [b, a]).conflicting_count)

    def test_empty_is_none(self) -> None:
        self.assertIsNone(verdict(GENERIC_CRITERION, []).override)


# ---------------------------------------------------------------------------
# CBP-WP-018 — Security-Control-Hashing und per-Bindung-Verdikte
# ---------------------------------------------------------------------------

SEC_KWARGS = dict(
    _BINDING_KWARGS,
    evidence_contract_revision="3.0",
    control_id="KB-08",
    security_contract_revision="1.0",
    security_contract_sha256="7" * 64,
)


def sec_desc(*, control_id="KB-08", binding=EXPECTED, art_rev=1,
             artifact_id=AID_A, producer_class=SECURITY_CONTROL_PRODUCER_CLASS,
             corrupt=False):
    sha = canonical_artifact_sha256(
        artifact_id=artifact_id, binding_sha256=binding,
        producer_class=producer_class, evidence_revision=art_rev,
        synthetic_test_only=True, control_id=control_id,
    )
    if corrupt:
        sha = "9" * 64
    return ArtifactDescriptor(
        artifact_id=artifact_id, artifact_sha256=sha, binding_sha256=binding,
        producer_class=producer_class, evidence_revision=art_rev,
        synthetic_test_only=True, control_id=control_id,
    )


def sec_verdict(arts, *, is_security=True, expected_pair=True, rev=1,
                contract_stale=False, binding=EXPECTED):
    return evaluate_security_binding(
        tuple(arts),
        criterion_is_security=is_security,
        is_expected_pair=expected_pair,
        expected_binding_sha256=binding,
        bundle_evidence_revision=rev,
        contract_stale=contract_stale,
    )


class TestSecurityArtifactHash(unittest.TestCase):
    def test_control_id_is_part_of_hash(self) -> None:
        a = canonical_artifact_sha256(
            artifact_id=AID_A, binding_sha256=EXPECTED,
            producer_class=SECURITY_CONTROL_PRODUCER_CLASS,
            evidence_revision=1, synthetic_test_only=True, control_id="KB-08")
        b = canonical_artifact_sha256(
            artifact_id=AID_A, binding_sha256=EXPECTED,
            producer_class=SECURITY_CONTROL_PRODUCER_CLASS,
            evidence_revision=1, synthetic_test_only=True, control_id="KB-03")
        self.assertNotEqual(a, b)

    def test_absent_control_id_differs_from_present(self) -> None:
        without = canonical_artifact_sha256(
            artifact_id=AID_A, binding_sha256=EXPECTED,
            producer_class=SECURITY_CONTROL_PRODUCER_CLASS,
            evidence_revision=1, synthetic_test_only=True)
        with_id = canonical_artifact_sha256(
            artifact_id=AID_A, binding_sha256=EXPECTED,
            producer_class=SECURITY_CONTROL_PRODUCER_CLASS,
            evidence_revision=1, synthetic_test_only=True, control_id="KB-08")
        self.assertNotEqual(without, with_id)

    def test_non_security_hash_unchanged_by_wp018(self) -> None:
        # Ein control_id-freies Artefakt hasht wie zuvor (kein Feld hinzugefuegt).
        explicit_none = canonical_artifact_sha256(
            artifact_id=AID_A, binding_sha256=EXPECTED,
            producer_class="structural-form", evidence_revision=1,
            synthetic_test_only=True, control_id=None)
        implicit = canonical_artifact_sha256(
            artifact_id=AID_A, binding_sha256=EXPECTED,
            producer_class="structural-form", evidence_revision=1,
            synthetic_test_only=True)
        self.assertEqual(explicit_none, implicit)

    def test_deterministic_and_hex64(self) -> None:
        first = sec_desc().artifact_sha256
        self.assertEqual(first, sec_desc().artifact_sha256)
        self.assertRegex(first, r"\A[0-9a-f]{64}\Z")

    def test_security_hash_excludes_itself(self) -> None:
        good = sec_desc()
        tampered = ArtifactDescriptor(
            artifact_id=good.artifact_id, artifact_sha256="0" * 64,
            binding_sha256=good.binding_sha256, producer_class=good.producer_class,
            evidence_revision=good.evidence_revision, synthetic_test_only=True,
            control_id=good.control_id,
        )
        self.assertEqual(sec_verdict([good]).verdict, BindingVerdict.VALID)
        self.assertEqual(sec_verdict([tampered]).verdict, BindingVerdict.INVALID)

    def test_dedup_key_separates_control_ids(self) -> None:
        a = sec_desc(control_id="KB-08")
        b = sec_desc(control_id="KB-03")
        self.assertNotEqual(a.dedup_key(), b.dedup_key())


class TestSecurityBindingHash(unittest.TestCase):
    def test_each_component_drift_changes_hash(self) -> None:
        base = canonical_binding_sha256(**SEC_KWARGS)
        drifts = {
            "source_id": "src-ffffffffffffffffffffffff",
            "mapping_id": "MAP-OTHER",
            "criterion": 6,
            "control_id": "KB-03",
            "mapping_draft_sha256": "1" * 64,
            "mapping_policy_sha256": "2" * 64,
            "registry_record_sha256": "3" * 64,
            "gate_contract_revision": "9.9",
            "gate_contract_sha256": "4" * 64,
            "evidence_contract_revision": "9.9",
            "evidence_contract_sha256": "5" * 64,
            "security_contract_revision": "9.9",
            "security_contract_sha256": "6" * 64,
            "evidence_revision": 2,
        }
        for field, value in drifts.items():
            with self.subTest(field=field):
                kwargs = dict(SEC_KWARGS)
                kwargs[field] = value
                self.assertNotEqual(canonical_binding_sha256(**kwargs), base)

    def test_security_binding_differs_from_non_security(self) -> None:
        non_security = canonical_binding_sha256(
            **dict(_BINDING_KWARGS, evidence_contract_revision="3.0"))
        self.assertNotEqual(canonical_binding_sha256(**SEC_KWARGS), non_security)

    def test_deterministic(self) -> None:
        self.assertEqual(canonical_binding_sha256(**SEC_KWARGS),
                         canonical_binding_sha256(**SEC_KWARGS))


class TestSecurityBindingVerdict(unittest.TestCase):
    def test_missing_when_no_artifact(self) -> None:
        result = sec_verdict([])
        self.assertEqual(result.verdict, BindingVerdict.MISSING)
        self.assertIsNone(result.override)
        self.assertEqual(result.reason_codes, ())

    def test_valid_single_fresh_artifact(self) -> None:
        result = sec_verdict([sec_desc()])
        self.assertEqual(result.verdict, BindingVerdict.VALID)
        self.assertIsNone(result.override)      # keine positive Aufwertung
        self.assertEqual(result.validated_count, 1)

    def test_invalid_hash(self) -> None:
        result = sec_verdict([sec_desc(corrupt=True)])
        self.assertEqual(result.verdict, BindingVerdict.INVALID)
        self.assertEqual(result.override, CriterionResult.INVALID_EVIDENCE)
        self.assertIn(GateReasonCode.EVID_INVALID_HASH, result.reason_codes)

    def test_invalid_pair_on_current_contract(self) -> None:
        result = sec_verdict([sec_desc()], expected_pair=False)
        self.assertEqual(result.verdict, BindingVerdict.INVALID)
        self.assertIn(GateReasonCode.EVID_INVALID_CONTROL_BINDING,
                      result.reason_codes)

    def test_invalid_on_non_security_criterion(self) -> None:
        result = sec_verdict([sec_desc()], is_security=False)
        self.assertEqual(result.verdict, BindingVerdict.INVALID)
        self.assertIn(GateReasonCode.EVID_INVALID_PRODUCER_CLASS,
                      result.reason_codes)

    def test_stale_contract(self) -> None:
        result = sec_verdict([sec_desc()], contract_stale=True)
        self.assertEqual(result.verdict, BindingVerdict.STALE)
        self.assertEqual(result.override, CriterionResult.STALE_EVIDENCE)
        self.assertIn(GateReasonCode.EVID_STALE_SECURITY_CONTRACT,
                      result.reason_codes)

    def test_stale_contract_does_not_reclassify_historic_pair(self) -> None:
        # Alter Vertrag + im aktuellen Vertrag unzulaessiges Paar ⇒ STALE,
        # nicht INVALID (keine nachtraegliche Invalid-Behauptung).
        result = sec_verdict([sec_desc()], expected_pair=False, contract_stale=True)
        self.assertEqual(result.verdict, BindingVerdict.STALE)

    def test_integrity_error_outranks_stale_contract(self) -> None:
        result = sec_verdict([sec_desc(corrupt=True)], contract_stale=True)
        self.assertEqual(result.verdict, BindingVerdict.INVALID)

    def test_stale_binding_drift(self) -> None:
        result = sec_verdict([sec_desc(binding="d" * 64)])
        self.assertEqual(result.verdict, BindingVerdict.STALE)
        self.assertIn(GateReasonCode.EVID_STALE_BINDING, result.reason_codes)

    def test_stale_evidence_revision(self) -> None:
        result = sec_verdict([sec_desc(art_rev=2)], rev=1)
        self.assertEqual(result.verdict, BindingVerdict.STALE)
        self.assertIn(GateReasonCode.EVID_STALE_EVIDENCE_REVISION,
                      result.reason_codes)

    def test_conflict_two_distinct_artifacts(self) -> None:
        result = sec_verdict([sec_desc(artifact_id=AID_A),
                              sec_desc(artifact_id=AID_B)])
        self.assertEqual(result.verdict, BindingVerdict.CONFLICTING)
        self.assertEqual(result.override, CriterionResult.CONFLICTING_EVIDENCE)
        self.assertEqual(result.conflicting_count, 2)

    def test_conflict_same_id_different_hash(self) -> None:
        result = sec_verdict([sec_desc(binding=EXPECTED),
                              sec_desc(binding="d" * 64)])
        self.assertEqual(result.verdict, BindingVerdict.CONFLICTING)
        self.assertIn(GateReasonCode.EVID_CONFLICT_ARTIFACT_ID,
                      result.reason_codes)

    def test_identical_duplicates_dedup_to_valid(self) -> None:
        a = sec_desc()
        result = sec_verdict([a, a, a])
        self.assertEqual(result.verdict, BindingVerdict.VALID)
        self.assertEqual(result.validated_count, 1)

    def test_invalid_outranks_conflict(self) -> None:
        result = sec_verdict([sec_desc(artifact_id=AID_A, corrupt=True),
                              sec_desc(artifact_id=AID_B)])
        self.assertEqual(result.verdict, BindingVerdict.INVALID)

    def test_conflict_outranks_stale(self) -> None:
        result = sec_verdict([sec_desc(artifact_id=AID_A, binding="d" * 64),
                              sec_desc(artifact_id=AID_B)])
        self.assertEqual(result.verdict, BindingVerdict.CONFLICTING)

    def test_order_independence(self) -> None:
        a = sec_desc(artifact_id=AID_A)
        b = sec_desc(artifact_id=AID_B)
        self.assertEqual(sec_verdict([a, b]), sec_verdict([b, a]))

    def test_verdict_values_are_closed(self) -> None:
        self.assertEqual(
            {v.value for v in BindingVerdict},
            {"MISSING", "VALID", "INVALID", "STALE", "CONFLICTING"},
        )

    def test_valid_and_missing_never_override(self) -> None:
        self.assertIsNone(sec_verdict([]).override)
        self.assertIsNone(sec_verdict([sec_desc()]).override)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
