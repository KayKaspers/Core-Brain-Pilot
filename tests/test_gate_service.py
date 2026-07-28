"""Tests der Gate-Orchestrierung und Bindung (CBP-WP-016)."""

from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from core.core_brain.errors import GateEvidenceError
from core.core_brain.gate import run_activation_evaluate
from core.core_brain.gate.models import GateStatus, canonical_json_bytes

from tests import gate_fixtures as fx


def _evaluate(case, *, synthetic: bool = True):
    return run_activation_evaluate(
        draft_path=case["draft_path"],
        policy=case["policy"],
        registry_root=case["root"],
        source_id=case["source_id"],
        evidence_path=case["evidence_path"],
        synthetic_confirmed=synthetic,
    )


class TestGateService(unittest.TestCase):
    def test_valid_case_blocked_without_binding_blockers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = _evaluate(fx.build_case(tmp))
        self.assertEqual(report.evaluation_status, GateStatus.BLOCKED)
        self.assertEqual(report.blocker_count, 16)  # nur Kriterien, keine Bindung
        self.assertFalse(
            [c for c in report.blocker_codes if c.startswith("GATE-BIND-")]
        )

    def test_synthetic_flag_required(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(GateEvidenceError):
                _evaluate(fx.build_case(tmp), synthetic=False)

    def test_retired_source_binding_blocker(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = _evaluate(fx.build_case(tmp, retired=True))
        self.assertIn(
            "GATE-BIND-SOURCE-NOT-REGISTERED-DISABLED", report.blocker_codes
        )

    def test_non_valid_draft_binding_blocker(self) -> None:
        draft = fx.valid_draft()
        draft["enabled"] = True  # WP-015 blockiert ⇒ nicht VALID_DRAFT
        with tempfile.TemporaryDirectory() as tmp:
            report = _evaluate(fx.build_case(tmp, draft=draft))
        self.assertIn("GATE-BIND-DRAFT-NOT-VALID", report.blocker_codes)

    def test_read_only_false_blocks(self) -> None:
        draft = fx.valid_draft()
        draft["read_only"] = False
        with tempfile.TemporaryDirectory() as tmp:
            report = _evaluate(fx.build_case(tmp, draft=draft))
        self.assertIn("GATE-BIND-DRAFT-NOT-VALID", report.blocker_codes)

    def test_follow_symlinks_true_blocks(self) -> None:
        draft = fx.valid_draft()
        draft["follow_symlinks"] = True
        with tempfile.TemporaryDirectory() as tmp:
            report = _evaluate(fx.build_case(tmp, draft=draft))
        self.assertIn("GATE-BIND-DRAFT-NOT-VALID", report.blocker_codes)

    def test_draft_hash_mismatch_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = _evaluate(
                fx.build_case(tmp, evidence_overrides={"mapping_draft_sha256": "0" * 64})
            )
        self.assertIn("GATE-BIND-DRAFT-HASH-MISMATCH", report.blocker_codes)

    def test_policy_hash_mismatch_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = _evaluate(
                fx.build_case(tmp, evidence_overrides={"mapping_policy_sha256": "0" * 64})
            )
        self.assertIn("GATE-BIND-POLICY-HASH-MISMATCH", report.blocker_codes)

    def test_record_hash_mismatch_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = _evaluate(
                fx.build_case(tmp, evidence_overrides={"registry_record_sha256": "0" * 64})
            )
        self.assertIn("GATE-BIND-RECORD-HASH-MISMATCH", report.blocker_codes)

    def test_source_id_mismatch_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = _evaluate(
                fx.build_case(
                    tmp, evidence_overrides={"source_id": "src-ffffffffffffffffffffffff"}
                )
            )
        self.assertIn("GATE-BIND-SOURCE-ID-MISMATCH", report.blocker_codes)

    def test_mapping_id_mismatch_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = _evaluate(
                fx.build_case(tmp, evidence_overrides={"mapping_id": "MAP-OTHER-0002"})
            )
        self.assertIn("GATE-BIND-MAPPING-ID-MISMATCH", report.blocker_codes)

    def test_contract_revision_mismatch_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = _evaluate(
                fx.build_case(tmp, evidence_overrides={"gate_contract_revision": "9.9"})
            )
        self.assertIn("GATE-BIND-CONTRACT-REVISION-MISMATCH", report.blocker_codes)

    def test_inputs_are_not_mutated(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            case = fx.build_case(tmp)
            before_draft = case["draft_path"].read_bytes()
            before_ev = case["evidence_path"].read_bytes()
            before_reg = _hash_tree(case["root"])
            _evaluate(case)
            _evaluate(case)
            self.assertEqual(case["draft_path"].read_bytes(), before_draft)
            self.assertEqual(case["evidence_path"].read_bytes(), before_ev)
            self.assertEqual(_hash_tree(case["root"]), before_reg)

    def test_no_new_files_created(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            case = fx.build_case(tmp)
            before = {p for p in Path(tmp).rglob("*")}
            _evaluate(case)
            self.assertEqual({p for p in Path(tmp).rglob("*")}, before)

    def test_report_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            case = fx.build_case(tmp)
            a = canonical_json_bytes(_evaluate(case).to_dict())
            b = canonical_json_bytes(_evaluate(case).to_dict())
        self.assertEqual(a, b)

    def test_report_has_no_leaks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            case = fx.build_case(tmp)
            blob = json.dumps(_evaluate(case).to_dict())
        self.assertNotIn("synthetic-placeholder", blob)
        self.assertNotIn("synthetic:notes-ref-marker", blob)
        self.assertNotIn(str(case["root"]), blob)
        self.assertNotIn(str(case["draft_path"]), blob)
        for marker in ("://", "http:", "www."):
            self.assertNotIn(marker, blob)


# Nicht report-sichere Werte: Pfade, Locator sowie Credential-/Secret-artige
# Eingaben. Jeder Wert muss die Evaluation fail-closed blockieren — als
# `source_id` und als `mapping_id`.
_LEAKY_IDS = (
    # Pfade und Locator
    "C:\\Users\\Example\\secret.txt",
    "/etc/shadow",
    "file:///etc/passwd",
    "https://example.invalid/private",
    "http://127.0.0.1/admin",
    "\\\\server\\share\\secret",
    "../secret",
    "..\\secret",
    "%2e%2e%2fsecret",
    "source/../../secret",
    # Credential- und Secret-artige Werte
    "user:password@example.invalid",
    "AKIA0000000000000000",
    "Bearer-example-secret-value",
    "token_example_secret_value",
    "password-example-secret",
)

# Weiterhin gueltige, opake mapping_id-Formen (Vertrag WP-015). Unveraendert
# in den Report zu uebernehmen, ohne Normalisierung.
_VALID_MAPPING_IDS = ("mapping-001", "map.synthetic_01", "MAPPING_TEST-01")


class TestIdentifierLeakProtection(unittest.TestCase):
    """N2 — `source_id` bleibt eine opake, validierte ID (fail-closed)."""

    def test_leaky_source_id_fails_closed(self) -> None:
        for leaky in _LEAKY_IDS:
            with self.subTest(source_id=leaky):
                with tempfile.TemporaryDirectory() as tmp:
                    case = fx.build_case(tmp)
                    with self.assertRaises(GateEvidenceError) as ctx:
                        run_activation_evaluate(
                            draft_path=case["draft_path"], policy=case["policy"],
                            registry_root=case["root"], source_id=leaky,
                            evidence_path=case["evidence_path"],
                            synthetic_confirmed=True,
                        )
                # Der abgewiesene Wert erscheint nicht in der Diagnose.
                self.assertNotIn(leaky, str(ctx.exception))

    def test_valid_ids_pass_through(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = _evaluate(fx.build_case(tmp))
        self.assertEqual(report.source_id, fx.SOURCE_ID)
        self.assertEqual(report.mapping_id, fx.MAPPING_ID)


class TestMappingIdContract(unittest.TestCase):
    """B.2 — mapping_id: Pflichtfeld, nur gelesen, nie redigiert; fail-closed.

    Eine ungueltige oder nicht report-sichere ``mapping_id`` blockiert **vor**
    der Reporterzeugung. Es gibt keinen ``null``-Fallback und keine Redaktion.
    """

    def _run_with_mapping_id(self, tmp: str, mapping_id: object):
        draft = fx.valid_draft()
        draft["mapping_id"] = mapping_id
        case = fx.build_case(
            tmp, draft=draft, evidence_overrides={"mapping_id": mapping_id}
        )
        return _evaluate(case)

    def test_leaky_mapping_id_blocks_before_report(self) -> None:
        for leaky in _LEAKY_IDS:
            with self.subTest(mapping_id=leaky):
                with tempfile.TemporaryDirectory() as tmp:
                    with self.assertRaises(GateEvidenceError) as ctx:
                        self._run_with_mapping_id(tmp, leaky)
                # Kein Echo des abgewiesenen Werts in der Diagnose.
                self.assertNotIn(leaky, str(ctx.exception))

    def test_missing_mapping_id_blocks(self) -> None:
        draft = fx.valid_draft()
        del draft["mapping_id"]
        with tempfile.TemporaryDirectory() as tmp:
            case = fx.build_case(tmp, draft=draft)
            with self.assertRaises(GateEvidenceError):
                _evaluate(case)

    def test_unparseable_draft_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            case = fx.build_case(tmp)
            case["draft_path"].write_bytes(b"{ not valid json ")
            with self.assertRaises(GateEvidenceError):
                _evaluate(case)

    def test_valid_mapping_ids_pass_unchanged(self) -> None:
        for mid in _VALID_MAPPING_IDS:
            with self.subTest(mapping_id=mid):
                with tempfile.TemporaryDirectory() as tmp:
                    report = self._run_with_mapping_id(tmp, mid)
                self.assertEqual(report.mapping_id, mid)  # byte-identisch uebernommen
                self.assertIsNotNone(report.mapping_id)

    def test_executed_report_mapping_id_never_null(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = _evaluate(fx.build_case(tmp))
        self.assertIsNotNone(report.mapping_id)
        self.assertNotIn('"mapping_id": null', json.dumps(report.to_dict()))
        self.assertNotIn('"mapping_id":null', canonical_json_bytes(report.to_dict()).decode())

    def test_valid_mapping_id_deterministic_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            case = fx.build_case(tmp)
            first = canonical_json_bytes(_evaluate(case).to_dict())
            second = canonical_json_bytes(_evaluate(case).to_dict())
        self.assertEqual(first, second)

    def test_draft_file_not_mutated(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            case = fx.build_case(tmp)
            before = case["draft_path"].read_bytes()
            _evaluate(case)
            self.assertEqual(case["draft_path"].read_bytes(), before)


def _by_id(report) -> dict[int, str]:
    return {o.criterion_id: o.result.value for o in report.criterion_results}


class TestArtifactEvidence(unittest.TestCase):
    """CBP-WP-017 — negative-evidence integration + Zähler + Mutationsschutz."""

    def _eval_with(self, artifact_specs, *, evidence_revision=1):
        with tempfile.TemporaryDirectory() as tmp:
            case = fx.build_case(
                tmp, artifact_specs=artifact_specs, evidence_revision=evidence_revision
            )
            return _evaluate(case)

    # -- §20.7 negative-only: gültige Artefakte werten nie positiv auf --------
    def test_valid_artifact_does_not_upgrade(self) -> None:
        # Basisergebnis je Kriterium ohne Artefakt.
        base = _by_id(self._eval_with({}))
        for cid in (2, 5, 15, 16, 18, 19, 20):
            with self.subTest(criterion=cid):
                res = _by_id(self._eval_with({cid: [{}]}))
                self.assertEqual(res[cid], base[cid])

    def test_missing_artifact_keeps_base(self) -> None:
        res = _by_id(self._eval_with({}))
        self.assertEqual(res[2], "SATISFIED")
        self.assertEqual(res[16], "HUMAN_DECISION_REQUIRED")
        self.assertEqual(res[18], "MISSING_EVIDENCE")

    # -- negative Überschreibung ---------------------------------------------
    def test_invalid_overrides_satisfied(self) -> None:
        res = _by_id(self._eval_with({2: [{"corrupt_hash": True}]}))
        self.assertEqual(res[2], "INVALID_EVIDENCE")

    def test_stale_overrides(self) -> None:
        res = _by_id(self._eval_with(
            {3: [{"binding_override": {"mapping_policy_sha256": "a" * 64}}]}))
        self.assertEqual(res[3], "STALE_EVIDENCE")

    def test_conflict_overrides(self) -> None:
        res = _by_id(self._eval_with(
            {6: [{}, {"artifact_id": fx.ART_ID_B}]}))
        self.assertEqual(res[6], "CONFLICTING_EVIDENCE")

    def test_producer_class_mismatch_is_invalid(self) -> None:
        res = _by_id(self._eval_with(
            {4: [{"producer_class": "operator-review-form"}]}))
        self.assertEqual(res[4], "INVALID_EVIDENCE")

    # -- §20.4 Stale je Bindungskomponente -----------------------------------
    def test_stale_binding_each_component(self) -> None:
        overrides = [
            {"source_id": "src-ffffffffffffffffffffffff"},
            {"mapping_id": "MAP-OTHER"},
            {"mapping_draft_sha256": "1" * 64},
            {"mapping_policy_sha256": "2" * 64},
            {"registry_record_sha256": "3" * 64},
            {"gate_contract_revision": "9.9"},
            {"gate_contract_sha256": "4" * 64},
            {"evidence_contract_revision": "9.9"},
            {"evidence_contract_sha256": "5" * 64},
            {"evidence_revision": 99},
        ]
        for ov in overrides:
            with self.subTest(component=next(iter(ov))):
                res = _by_id(self._eval_with({7: [{"binding_override": ov}]}))
                self.assertEqual(res[7], "STALE_EVIDENCE")

    def test_stale_evidence_revision(self) -> None:
        res = _by_id(self._eval_with({8: [{"art_rev": 2}]}, evidence_revision=1))
        self.assertEqual(res[8], "STALE_EVIDENCE")

    # -- §20.8 Zähler ---------------------------------------------------------
    def test_counts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            case = fx.build_case(tmp, artifact_specs={
                2: [{}],                                  # validated
                4: [{"corrupt_hash": True}],              # invalid
                3: [{"binding_override": {"mapping_policy_sha256": "a" * 64}}],  # stale
                6: [{}, {"artifact_id": fx.ART_ID_B}],    # conflict (2)
            })
            report = _evaluate(case)
        self.assertEqual(report.validated_artifact_count, 1)
        self.assertEqual(report.invalid_artifact_count, 1)
        self.assertEqual(report.stale_artifact_count, 1)
        self.assertEqual(report.conflicting_artifact_count, 2)
        self.assertEqual(report.evidence_count, 5)  # total geladen

    def test_identical_duplicates_counted_once(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            case = fx.build_case(tmp, artifact_specs={5: [{}, {}, {}]})
            report = _evaluate(case)
        self.assertEqual(report.validated_artifact_count, 1)
        self.assertEqual(report.conflicting_artifact_count, 0)

    # -- §20.9 Mutationsschutz ------------------------------------------------
    def test_inputs_not_mutated_and_no_new_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            case = fx.build_case(tmp, artifact_specs={2: [{}], 4: [{"corrupt_hash": True}]})
            ev_before = case["evidence_path"].read_bytes()
            draft_before = case["draft_path"].read_bytes()
            reg_before = _hash_tree(case["root"])
            tree_before = sorted(p.name for p in Path(tmp).iterdir())
            _evaluate(case)
            self.assertEqual(case["evidence_path"].read_bytes(), ev_before)
            self.assertEqual(case["draft_path"].read_bytes(), draft_before)
            self.assertEqual(_hash_tree(case["root"]), reg_before)
            self.assertEqual(sorted(p.name for p in Path(tmp).iterdir()), tree_before)

    # -- Determinismus / Reihenfolgeunabhängigkeit ---------------------------
    def test_deterministic_and_order_independent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            a = fx.build_case(tmp, artifact_specs={6: [{"artifact_id": fx.ART_ID_A},
                                                       {"artifact_id": fx.ART_ID_B}]})
            first = canonical_json_bytes(_evaluate(a).to_dict())
        with tempfile.TemporaryDirectory() as tmp:
            b = fx.build_case(tmp, artifact_specs={6: [{"artifact_id": fx.ART_ID_B},
                                                       {"artifact_id": fx.ART_ID_A}]})
            second = canonical_json_bytes(_evaluate(b).to_dict())
        self.assertEqual(first, second)


def _hash_tree(root: Path) -> list[tuple[str, str]]:
    result: list[tuple[str, str]] = []
    for path in sorted(root.rglob("*")):
        if path.is_file():
            result.append(
                (path.relative_to(root).as_posix(),
                 hashlib.sha256(path.read_bytes()).hexdigest())
            )
    return result


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
