"""Tests der reinen Gate-Kernlogik und des Reports (CBP-WP-016)."""

from __future__ import annotations

import json
import unittest

from core.core_brain.gate.evaluator import build_report, evaluate_criteria
from core.core_brain.gate.models import (
    CriterionResult,
    GateReasonCode,
    GateStatus,
)


def _results(*, draft_valid: bool, allowed_nonempty: bool) -> dict[int, CriterionResult]:
    outcomes = evaluate_criteria(
        draft_valid=draft_valid, allowed_subpaths_nonempty=allowed_nonempty
    )
    return {o.criterion_id: o.result for o in outcomes}


def _report(*, draft_valid: bool = True, allowed_nonempty: bool = False,
            binding=None):
    outcomes = evaluate_criteria(
        draft_valid=draft_valid, allowed_subpaths_nonempty=allowed_nonempty
    )
    return build_report(
        source_id="src-0123456789abcdef01234567",
        mapping_id="MAP-EXAMPLE-0001",
        mapping_draft_sha256="a" * 64,
        mapping_policy_sha256="b" * 64,
        registry_record_sha256="c" * 64,
        outcomes=outcomes,
        binding_blockers=binding or [],
        evidence_count=0,
    )


class TestEvaluateCriteria(unittest.TestCase):
    def test_twenty_outcomes_in_order(self) -> None:
        outcomes = evaluate_criteria(draft_valid=True, allowed_subpaths_nonempty=False)
        self.assertEqual([o.criterion_id for o in outcomes], list(range(1, 21)))

    def test_human_only_always_human_required(self) -> None:
        # N1: nur 5, 16, 20 sind HUMAN_DECISION_REQUIRED.
        for draft_valid in (True, False):
            res = _results(draft_valid=draft_valid, allowed_nonempty=True)
            for cid in (5, 16, 20):
                self.assertEqual(res[cid], CriterionResult.HUMAN_DECISION_REQUIRED)

    def test_criterion_15_is_operational_evidence_not_decision(self) -> None:
        # N1: Kriterium 15 (Operator Review) ist menschlich erzeugte operative
        # Evidenz ⇒ MISSING_EVIDENCE, NICHT HUMAN_DECISION_REQUIRED. Ein
        # synthetischer Review-Record erfüllt es nie.
        for draft_valid in (True, False):
            res = _results(draft_valid=draft_valid, allowed_nonempty=True)
            self.assertEqual(res[15], CriterionResult.MISSING_EVIDENCE)
            self.assertNotEqual(res[15], CriterionResult.HUMAN_DECISION_REQUIRED)

    def test_foundation_always_dependency_blocked(self) -> None:
        res = _results(draft_valid=True, allowed_nonempty=True)
        for cid in (4, 6, 7, 8, 10, 11):
            self.assertEqual(res[cid], CriterionResult.DEPENDENCY_BLOCKED)

    def test_technical_document_criteria_track_draft_valid(self) -> None:
        ok = _results(draft_valid=True, allowed_nonempty=False)
        bad = _results(draft_valid=False, allowed_nonempty=False)
        for cid in (2, 3, 13, 14):
            self.assertEqual(ok[cid], CriterionResult.SATISFIED)
            self.assertEqual(bad[cid], CriterionResult.DEPENDENCY_BLOCKED)

    def test_criterion_9_allowlist(self) -> None:
        empty = _results(draft_valid=True, allowed_nonempty=False)
        nonempty = _results(draft_valid=True, allowed_nonempty=True)
        self.assertEqual(empty[9], CriterionResult.MISSING_EVIDENCE)
        self.assertEqual(nonempty[9], CriterionResult.SATISFIED)

    def test_scope_and_missing_criteria(self) -> None:
        res = _results(draft_valid=True, allowed_nonempty=False)
        self.assertEqual(res[1], CriterionResult.OUT_OF_SYNTHETIC_SCOPE)
        self.assertEqual(res[12], CriterionResult.OUT_OF_SYNTHETIC_SCOPE)
        for cid in (17, 18, 19):
            self.assertEqual(res[cid], CriterionResult.MISSING_EVIDENCE)


class TestReport(unittest.TestCase):
    def test_status_always_blocked(self) -> None:
        self.assertEqual(_report().evaluation_status, GateStatus.BLOCKED)

    def test_valid_case_has_16_blockers(self) -> None:
        # N1: 16 Blocker; davon 3 HUMAN_DECISION_REQUIRED (5,16,20) und
        # 5 MISSING_EVIDENCE (9,15,17,18,19).
        report = _report(draft_valid=True, allowed_nonempty=False)
        self.assertEqual(report.blocker_count, 16)
        self.assertEqual(report.missing_evidence_count, 5)
        self.assertEqual(report.human_decision_count, 3)

    def test_blocker_codes_sorted_and_deduplicated(self) -> None:
        report = _report(
            binding=[
                GateReasonCode.BIND_DRAFT_NOT_VALID,
                GateReasonCode.BIND_DRAFT_NOT_VALID,
            ]
        )
        codes = list(report.blocker_codes)
        self.assertEqual(codes, sorted(codes))
        self.assertEqual(len(codes), len(set(codes)))
        self.assertIn("GATE-BIND-DRAFT-NOT-VALID", codes)

    def test_report_is_deterministic(self) -> None:
        a = json.dumps(_report().to_dict(), sort_keys=True)
        b = json.dumps(_report().to_dict(), sort_keys=True)
        self.assertEqual(a, b)

    def test_report_has_no_forbidden_states(self) -> None:
        blob = json.dumps(_report().to_dict())
        for forbidden in ("READY FOR", "APPROVED FOR", "REVOKED"):
            self.assertNotIn(forbidden, blob)

    def test_report_has_no_timestamp_fields(self) -> None:
        keys = set(_report().to_dict())
        for banned in ("timestamp", "generated_at", "created_at", "date", "time"):
            self.assertNotIn(banned, keys)

    def test_criterion_results_carry_id_code_stufe_result(self) -> None:
        entry = _report().to_dict()["criterion_results"][0]
        self.assertEqual(set(entry), {"criterion_id", "code", "nachweisstufe", "result"})


class TestPureNegativeFolding(unittest.TestCase):
    """CBP-WP-018 §22.15 — reine Faltung: nur negativ, deterministisch, ohne I/O."""

    _NEGATIVE = (
        CriterionResult.INVALID_EVIDENCE,
        CriterionResult.CONFLICTING_EVIDENCE,
        CriterionResult.STALE_EVIDENCE,
    )

    def _fold(self, overrides):
        outcomes = evaluate_criteria(
            draft_valid=True, allowed_subpaths_nonempty=False,
            evidence_overrides=overrides,
        )
        return {o.criterion_id: o.result for o in outcomes}

    def test_negative_overrides_apply(self) -> None:
        for negative in self._NEGATIVE:
            with self.subTest(result=negative.value):
                self.assertEqual(self._fold({4: negative})[4], negative)

    def test_positive_override_is_ignored(self) -> None:
        # Eine positive "Aufwertung" darf niemals durchschlagen.
        base = self._fold({})
        for positive in (CriterionResult.SATISFIED,
                         CriterionResult.HUMAN_DECISION_REQUIRED,
                         CriterionResult.MISSING_EVIDENCE,
                         CriterionResult.OUT_OF_SYNTHETIC_SCOPE,
                         CriterionResult.DEPENDENCY_BLOCKED):
            with self.subTest(result=positive.value):
                self.assertEqual(self._fold({4: positive})[4], base[4])

    def test_human_only_criteria_cannot_be_upgraded(self) -> None:
        for cid in (5, 16, 20):
            with self.subTest(criterion=cid):
                folded = self._fold({cid: CriterionResult.SATISFIED})
                self.assertEqual(folded[cid], CriterionResult.HUMAN_DECISION_REQUIRED)

    def test_satisfied_criterion_can_be_downgraded_only(self) -> None:
        base = self._fold({})
        self.assertEqual(base[2], CriterionResult.SATISFIED)
        self.assertEqual(self._fold({2: CriterionResult.INVALID_EVIDENCE})[2],
                         CriterionResult.INVALID_EVIDENCE)

    def test_override_mapping_is_not_mutated(self) -> None:
        overrides = {4: CriterionResult.INVALID_EVIDENCE}
        snapshot = dict(overrides)
        self._fold(overrides)
        self.assertEqual(overrides, snapshot)

    def test_folding_is_deterministic(self) -> None:
        overrides = {4: CriterionResult.INVALID_EVIDENCE,
                     7: CriterionResult.STALE_EVIDENCE}
        self.assertEqual(self._fold(overrides), self._fold(overrides))

    def test_unaffected_criteria_keep_base_result(self) -> None:
        base = self._fold({})
        folded = self._fold({4: CriterionResult.INVALID_EVIDENCE})
        for cid in range(1, 21):
            if cid != 4:
                with self.subTest(criterion=cid):
                    self.assertEqual(folded[cid], base[cid])


class TestReportSecurityFields(unittest.TestCase):
    """CBP-WP-018 §17 — Security-Contract-Felder im reinen Report-Builder."""

    def test_defaults_are_neutral(self) -> None:
        # Ohne uebergebene Werte bleibt der Report neutral (keine Erfindung).
        data = _report().to_dict()
        self.assertEqual(data["security_contract_revision"], "")
        self.assertEqual(data["security_contract_sha256"], "")
        self.assertEqual(data["documented_control_count"], 0)
        self.assertEqual(data["runtime_scoped_binding_count"], 0)

    def test_counts_are_passed_through_unchanged(self) -> None:
        outcomes = evaluate_criteria(draft_valid=True, allowed_subpaths_nonempty=False)
        report = build_report(
            source_id="src-0123456789abcdef01234567",
            mapping_id="MAP-EXAMPLE-0001",
            mapping_draft_sha256="a" * 64,
            mapping_policy_sha256="b" * 64,
            registry_record_sha256="c" * 64,
            outcomes=outcomes,
            binding_blockers=[],
            evidence_count=0,
            security_contract_revision="1.0",
            security_contract_sha256="e" * 64,
            documented_control_count=12,
            runtime_scoped_control_count=7,
            runtime_scoped_binding_count=11,
            valid_form_binding_count=3,
            missing_form_binding_count=5,
            invalid_form_binding_count=1,
            stale_form_binding_count=1,
            conflicting_form_binding_count=1,
            operationally_unevaluated_binding_count=11,
        )
        data = report.to_dict()
        self.assertEqual(data["security_contract_revision"], "1.0")
        self.assertEqual(data["documented_control_count"], 12)
        self.assertEqual(
            data["valid_form_binding_count"] + data["missing_form_binding_count"]
            + data["invalid_form_binding_count"] + data["stale_form_binding_count"]
            + data["conflicting_form_binding_count"],
            data["runtime_scoped_binding_count"],
        )
        # Der reine Builder trifft keine Security-Aussage.
        self.assertEqual(report.evaluation_status, GateStatus.BLOCKED)

    def test_no_readiness_vocabulary_in_report_keys(self) -> None:
        keys = set(_report().to_dict())
        for banned in ("ready_control_count", "passed_control_count",
                       "enforced_control_count", "approved_control_count",
                       "human_decision_control_count", "security_ready",
                       "security_passed"):
            self.assertNotIn(banned, keys)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
