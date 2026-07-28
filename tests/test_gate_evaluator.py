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


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
