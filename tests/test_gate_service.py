"""Tests der Gate-Orchestrierung und Bindung (CBP-WP-016/017/018)."""

from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from core.core_brain.errors import GateEvidenceError
from core.core_brain.gate import (
    DOCUMENTED_CONTROLS,
    RUNTIME_SCOPED_BINDINGS,
    run_activation_evaluate,
)
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


# ---------------------------------------------------------------------------
# CBP-WP-018 — Security-Control-Form-Bindungen (elf `(criterion, control_id)`)
# ---------------------------------------------------------------------------


def _all_eleven_specs() -> dict[int, list[dict]]:
    """Artefaktspezifikationen fuer genau die elf kanonischen Bindungen."""
    specs: dict[int, list[dict]] = {}
    for criterion, control in RUNTIME_SCOPED_BINDINGS:
        specs.setdefault(criterion, []).append({"control_id": control})
    return specs


def _partition(report) -> int:
    return (
        report.valid_form_binding_count
        + report.missing_form_binding_count
        + report.invalid_form_binding_count
        + report.stale_form_binding_count
        + report.conflicting_form_binding_count
    )


class TestSecurityBindingCounters(unittest.TestCase):
    """CBP-WP-018 §17/§22.10 — Contract-Felder, Zaehler und Summeninvariante."""

    def _eval_with(self, artifact_specs=None, *, evidence_overrides=None,
                   evidence_revision=1):
        with tempfile.TemporaryDirectory() as tmp:
            case = fx.build_case(
                tmp,
                artifact_specs=artifact_specs or {},
                evidence_overrides=evidence_overrides,
                evidence_revision=evidence_revision,
            )
            return _evaluate(case)

    def test_static_contract_counts(self) -> None:
        report = self._eval_with()
        self.assertEqual(report.security_contract_revision, "1.0")
        self.assertRegex(report.security_contract_sha256, r"\A[0-9a-f]{64}\Z")
        self.assertEqual(report.documented_control_count, 12)
        self.assertEqual(report.runtime_scoped_control_count, 7)
        self.assertEqual(report.runtime_scoped_binding_count, 11)
        self.assertEqual(report.operationally_unevaluated_binding_count, 11)

    def test_no_security_artifacts_yields_eleven_missing(self) -> None:
        report = self._eval_with()
        self.assertEqual(report.missing_form_binding_count, 11)
        self.assertEqual(report.valid_form_binding_count, 0)
        self.assertEqual(_partition(report), 11)

    def test_all_eleven_valid(self) -> None:
        report = self._eval_with(_all_eleven_specs())
        self.assertEqual(report.valid_form_binding_count, 11)
        self.assertEqual(report.missing_form_binding_count, 0)
        self.assertEqual(report.invalid_form_binding_count, 0)
        self.assertEqual(report.stale_form_binding_count, 0)
        self.assertEqual(report.conflicting_form_binding_count, 0)
        self.assertEqual(_partition(report), 11)

    def test_mixed_categories_partition_holds(self) -> None:
        specs = _all_eleven_specs()
        specs[4] = [{"control_id": "KB-08", "corrupt_hash": True}]      # invalid
        specs[10] = [{"control_id": "KB-11",
                      "binding_override": {"mapping_policy_sha256": "a" * 64}}]
        del specs[8]                                                    # 2x missing
        report = self._eval_with(specs)
        self.assertEqual(report.invalid_form_binding_count, 1)
        self.assertEqual(report.stale_form_binding_count, 1)
        self.assertEqual(report.missing_form_binding_count, 2)
        self.assertEqual(report.valid_form_binding_count, 7)
        self.assertEqual(_partition(report), 11)

    def test_stale_contract_makes_all_present_bindings_stale(self) -> None:
        report = self._eval_with(
            _all_eleven_specs(),
            evidence_overrides={"security_contract_revision": "0.9"},
        )
        self.assertEqual(report.stale_form_binding_count, 11)
        self.assertEqual(report.valid_form_binding_count, 0)
        self.assertEqual(_partition(report), 11)

    def test_extra_invalid_pair_does_not_break_partition(self) -> None:
        # Ein zusaetzliches, im Vertrag unzulaessiges Paar zaehlt nicht zur
        # Elf-Bindungs-Partition, erzeugt aber ein negatives Verdikt.
        specs = _all_eleven_specs()
        specs[4].append({"control_id": "KB-01", "artifact_id": fx.ART_ID_B})
        report = self._eval_with(specs)
        self.assertEqual(_partition(report), 11)
        self.assertEqual(report.valid_form_binding_count, 11)
        self.assertEqual(report.invalid_artifact_count, 1)


class TestSecurityBindingSemantics(unittest.TestCase):
    """CBP-WP-018 §22.7/§22.8/§22.9 — Invalid/Stale/Conflict und Mehrfachcontrols."""

    def _res(self, artifact_specs, *, evidence_overrides=None, evidence_revision=1):
        with tempfile.TemporaryDirectory() as tmp:
            case = fx.build_case(
                tmp,
                artifact_specs=artifact_specs,
                evidence_overrides=evidence_overrides,
                evidence_revision=evidence_revision,
            )
            return _by_id(_evaluate(case))

    # -- §22.7 Invalid/Stale-Abgrenzung ---------------------------------------
    def test_current_contract_plus_disallowed_pair_is_invalid(self) -> None:
        # KB-01 ist nicht runtime-scoped ⇒ unzulaessiges Paar bei aktuellem Vertrag.
        res = self._res({4: [{"control_id": "KB-01"}]})
        self.assertEqual(res[4], "INVALID_EVIDENCE")

    def test_wrong_criterion_for_valid_control_is_invalid(self) -> None:
        # KB-08 ist runtime-scoped, aber nur an Kriterium 4 gebunden.
        res = self._res({7: [{"control_id": "KB-08"}]})
        self.assertEqual(res[7], "INVALID_EVIDENCE")

    def test_stale_contract_revision_keeps_historic_pair_stale(self) -> None:
        res = self._res(
            {4: [{"control_id": "KB-08"}]},
            evidence_overrides={"security_contract_revision": "0.9"},
        )
        self.assertEqual(res[4], "STALE_EVIDENCE")

    def test_stale_contract_hash_is_stale(self) -> None:
        res = self._res(
            {6: [{"control_id": "KB-10"}]},
            evidence_overrides={"security_contract_sha256": "d" * 64},
        )
        self.assertEqual(res[6], "STALE_EVIDENCE")

    def test_integrity_error_outranks_stale_contract(self) -> None:
        # Falscher Artifact Hash bleibt INVALID, auch bei veraltetem Vertrag.
        res = self._res(
            {4: [{"control_id": "KB-08", "corrupt_hash": True}]},
            evidence_overrides={"security_contract_revision": "0.9"},
        )
        self.assertEqual(res[4], "INVALID_EVIDENCE")

    def test_security_form_on_criterion_nine_is_invalid(self) -> None:
        # Kriterium 9 ist non-security-structural und akzeptiert kein KB-Formular.
        res = self._res({9: [{"producer_class": "security-control-form",
                              "control_id": "KB-03"}]})
        self.assertEqual(res[9], "INVALID_EVIDENCE")

    def test_security_form_on_criterion_five_is_invalid(self) -> None:
        res = self._res({5: [{"producer_class": "security-control-form",
                              "control_id": "KB-03"}]})
        self.assertEqual(res[5], "INVALID_EVIDENCE")

    def test_foundation_form_on_security_criterion_is_invalid(self) -> None:
        res = self._res({8: [{"producer_class": "foundation-form"}]})
        self.assertEqual(res[8], "INVALID_EVIDENCE")

    # -- §22.8 Mehrfachcontrols je Kriterium ----------------------------------
    def test_multiple_controls_same_criterion_are_not_conflict(self) -> None:
        for criterion, controls in (
            (6, ("KB-10", "KB-11")),
            (7, ("KB-02", "KB-04", "KB-07")),
            (8, ("KB-03", "KB-04")),
            (11, ("KB-03", "KB-04")),
        ):
            with self.subTest(criterion=criterion):
                with tempfile.TemporaryDirectory() as tmp:
                    case = fx.build_case(tmp, artifact_specs={
                        criterion: [{"control_id": c} for c in controls]
                    })
                    report = _evaluate(case)
                results = _by_id(report)
                self.assertEqual(results[criterion], "DEPENDENCY_BLOCKED")
                self.assertEqual(report.conflicting_form_binding_count, 0)
                self.assertEqual(report.valid_form_binding_count, len(controls))
                self.assertEqual(_partition(report), 11)

    # -- §22.9 Konflikte -------------------------------------------------------
    def test_same_binding_two_artifacts_is_conflict(self) -> None:
        res = self._res({4: [{"control_id": "KB-08"},
                             {"control_id": "KB-08", "artifact_id": fx.ART_ID_B}]})
        self.assertEqual(res[4], "CONFLICTING_EVIDENCE")

    def test_same_artifact_id_different_hash_is_conflict(self) -> None:
        # Gleiche Artifact-ID, andere Bindung ⇒ anderer Artefakthash.
        with tempfile.TemporaryDirectory() as tmp:
            case = fx.build_case(tmp, artifact_specs={4: [
                {"control_id": "KB-08"},
                {"control_id": "KB-08", "art_rev": 1,
                 "binding_override": {"mapping_id": "MAP-OTHER"}},
            ]})
            report = _evaluate(case)
        self.assertEqual(_by_id(report)[4], "CONFLICTING_EVIDENCE")
        self.assertEqual(report.conflicting_form_binding_count, 1)

    def test_exact_duplicates_are_deduplicated(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            case = fx.build_case(tmp, artifact_specs={
                4: [{"control_id": "KB-08"}, {"control_id": "KB-08"},
                    {"control_id": "KB-08"}]
            })
            report = _evaluate(case)
        self.assertEqual(report.valid_form_binding_count, 1)
        self.assertEqual(report.conflicting_form_binding_count, 0)
        self.assertEqual(_by_id(report)[4], "DEPENDENCY_BLOCKED")

    def test_invalid_outranks_conflict(self) -> None:
        res = self._res({4: [{"control_id": "KB-08", "corrupt_hash": True},
                             {"control_id": "KB-08", "artifact_id": fx.ART_ID_B}]})
        self.assertEqual(res[4], "INVALID_EVIDENCE")

    def test_conflict_outranks_stale(self) -> None:
        # Zwei unterschiedliche stale Artefakte derselben Bindung ⇒ Conflict.
        res = self._res({4: [
            {"control_id": "KB-08",
             "binding_override": {"mapping_policy_sha256": "a" * 64}},
            {"control_id": "KB-08", "artifact_id": fx.ART_ID_B,
             "binding_override": {"mapping_policy_sha256": "b" * 64}},
        ]})
        self.assertEqual(res[4], "CONFLICTING_EVIDENCE")

    def test_binding_order_independent(self) -> None:
        controls = ["KB-02", "KB-04", "KB-07"]
        with tempfile.TemporaryDirectory() as tmp:
            case = fx.build_case(tmp, artifact_specs={
                7: [{"control_id": c} for c in controls]})
            first = canonical_json_bytes(_evaluate(case).to_dict())
        with tempfile.TemporaryDirectory() as tmp:
            case = fx.build_case(tmp, artifact_specs={
                7: [{"control_id": c} for c in reversed(controls)]})
            second = canonical_json_bytes(_evaluate(case).to_dict())
        self.assertEqual(first, second)

    # -- §22.6 Security-Binding-Hash je Komponente -----------------------------
    def test_security_binding_drift_each_component(self) -> None:
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
            {"security_contract_revision": "9.9"},
            {"security_contract_sha256": "6" * 64},
            {"evidence_revision": 99},
        ]
        for ov in overrides:
            with self.subTest(component=next(iter(ov))):
                res = self._res({4: [{"control_id": "KB-08",
                                      "binding_override": ov}]})
                self.assertEqual(res[4], "STALE_EVIDENCE")


class TestSecurityNegativeEvidenceOnly(unittest.TestCase):
    """CBP-WP-018 §22.11 — elf gueltige Formbindungen werten nichts positiv auf."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        case = fx.build_case(self._tmp.name, artifact_specs=_all_eleven_specs())
        self.report = _evaluate(case)
        self.results = _by_id(self.report)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_security_criteria_stay_dependency_blocked(self) -> None:
        for cid in (4, 6, 7, 8, 10, 11):
            with self.subTest(criterion=cid):
                self.assertEqual(self.results[cid], "DEPENDENCY_BLOCKED")

    def test_criterion_five_stays_human_decision_required(self) -> None:
        self.assertEqual(self.results[5], "HUMAN_DECISION_REQUIRED")

    def test_criterion_nine_stays_structural(self) -> None:
        # Leere Allowlist ⇒ strukturelles MISSING_EVIDENCE, unabhaengig von KB.
        self.assertEqual(self.results[9], "MISSING_EVIDENCE")

    def test_no_criterion_becomes_satisfied_by_security_forms(self) -> None:
        baseline_tmp = tempfile.TemporaryDirectory()
        try:
            base = _by_id(_evaluate(fx.build_case(baseline_tmp.name)))
        finally:
            baseline_tmp.cleanup()
        for cid in (4, 5, 6, 7, 8, 9, 10, 11):
            with self.subTest(criterion=cid):
                self.assertEqual(self.results[cid], base[cid])

    def test_gate_status_stays_blocked(self) -> None:
        self.assertEqual(self.report.evaluation_status, GateStatus.BLOCKED)
        self.assertGreater(self.report.blocker_count, 0)

    def test_report_leaks_no_control_or_artifact_identity(self) -> None:
        payload = canonical_json_bytes(self.report.to_dict()).decode("utf-8")
        for control in DOCUMENTED_CONTROLS:
            self.assertNotIn(control, payload)
        self.assertNotIn(fx.ART_ID_A, payload)
        self.assertNotIn(fx.ART_ID_B, payload)
        for token in ("control_id", "artifact_id", "producer_class",
                      "binding_sha256", "artifact_sha256"):
            self.assertNotIn(token, payload)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
