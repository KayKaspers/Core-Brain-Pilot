"""Tests des Gate-Vertrags und der Modelle (CBP-WP-016)."""

from __future__ import annotations

import unittest

from core.core_brain.gate.models import (
    CANONICAL_GATE_STATES,
    GATE_CRITERIA,
    GATE_CRITERION_COUNT,
    CriterionResult,
    GateStatus,
    gate_contract_sha256,
)


class TestGateContract(unittest.TestCase):
    def test_exactly_20_criteria_in_order(self) -> None:
        self.assertEqual(len(GATE_CRITERIA), 20)
        self.assertEqual(GATE_CRITERION_COUNT, 20)
        for index, criterion in enumerate(GATE_CRITERIA, start=1):
            self.assertEqual(criterion.criterion_id, index)
            self.assertEqual(criterion.code, f"GATE-CRIT-{index:02d}")

    def test_no_criterion_21_or_22(self) -> None:
        ids = {c.criterion_id for c in GATE_CRITERIA}
        self.assertNotIn(21, ids)
        self.assertNotIn(22, ids)
        self.assertEqual(max(ids), 20)

    def test_human_only_criteria_are_5_16_20(self) -> None:
        # N1: ausschließlich menschliche Entscheidungen sind 5, 16, 20.
        # Kriterium 15 (Operator Review) ist menschlich erzeugte operative
        # Evidenz, KEINE Gate-Entscheidung ⇒ nicht human_only.
        human = {c.criterion_id for c in GATE_CRITERIA if c.human_only}
        self.assertEqual(human, {5, 16, 20})
        self.assertFalse(next(c for c in GATE_CRITERIA if c.criterion_id == 15).human_only)

    def test_nachweisstufen_match_gate_doc(self) -> None:
        stufe = {c.criterion_id: c.nachweisstufe for c in GATE_CRITERIA}
        self.assertEqual(
            {i for i, s in stufe.items() if s == 4},
            {4, 5, 6, 7, 8, 9, 10, 11},
        )
        self.assertEqual({i for i, s in stufe.items() if s == 6}, {16, 20})

    def test_gate_contract_sha256_is_deterministic(self) -> None:
        self.assertEqual(gate_contract_sha256(), gate_contract_sha256())
        self.assertRegex(gate_contract_sha256(), r"\A[0-9a-f]{64}\Z")


class TestGateStatus(unittest.TestCase):
    def test_only_two_output_states(self) -> None:
        self.assertEqual(
            {s.value for s in GateStatus}, {"NOT_EVALUATED", "BLOCKED"}
        )

    def test_forbidden_states_not_in_gate_status(self) -> None:
        values = {s.value for s in GateStatus}
        for forbidden in (
            "READY FOR ACTIVATION DECISION",
            "READY_FOR_ACTIVATION_DECISION",
            "APPROVED FOR ACTIVATION",
            "REVOKED",
        ):
            self.assertNotIn(forbidden, values)

    def test_canonical_states_are_reference_only(self) -> None:
        # Die vollstaendige kanonische Menge ist dokumentiert, aber die drei
        # letzten sind vom MVP nicht als GateStatus modellierbar.
        self.assertEqual(len(CANONICAL_GATE_STATES), 5)
        self.assertIn("READY FOR ACTIVATION DECISION", CANONICAL_GATE_STATES)
        self.assertIn("APPROVED FOR ACTIVATION", CANONICAL_GATE_STATES)
        self.assertIn("REVOKED", CANONICAL_GATE_STATES)


class TestCriterionResult(unittest.TestCase):
    def test_closed_result_set(self) -> None:
        self.assertEqual(
            {r.value for r in CriterionResult},
            {
                "SATISFIED",
                "MISSING_EVIDENCE",
                "INVALID_EVIDENCE",
                "STALE_EVIDENCE",
                "CONFLICTING_EVIDENCE",
                "HUMAN_DECISION_REQUIRED",
                "OUT_OF_SYNTHETIC_SCOPE",
                "DEPENDENCY_BLOCKED",
            },
        )

    def test_result_values_are_not_gate_states(self) -> None:
        gate_values = {s.value for s in GateStatus}
        for result in CriterionResult:
            self.assertNotIn(result.value, gate_values)


class TestEvidenceContract20(unittest.TestCase):
    def test_versions(self) -> None:
        from core.core_brain.gate.models import (
            EVIDENCE_CONTRACT_REVISION,
            EVIDENCE_SCHEMA_VERSION,
            GATE_CONTRACT_REVISION,
        )
        self.assertEqual(EVIDENCE_SCHEMA_VERSION, "2.0")
        self.assertEqual(EVIDENCE_CONTRACT_REVISION, "2.0")
        self.assertEqual(GATE_CONTRACT_REVISION, "1.0")  # Gate-Vertrag unverändert

    def test_evidence_contract_sha256_deterministic(self) -> None:
        from core.core_brain.gate.models import (
            evidence_contract_sha256,
            gate_contract_sha256,
        )
        self.assertEqual(evidence_contract_sha256(), evidence_contract_sha256())
        self.assertRegex(evidence_contract_sha256(), r"\A[0-9a-f]{64}\Z")
        self.assertNotEqual(evidence_contract_sha256(), gate_contract_sha256())

    def test_limits(self) -> None:
        from core.core_brain.gate.models import (
            MAX_ARTIFACTS_PER_CRITERION,
            MAX_ARTIFACTS_TOTAL,
        )
        self.assertEqual(MAX_ARTIFACTS_PER_CRITERION, 4)
        self.assertEqual(MAX_ARTIFACTS_TOTAL, 80)

    def test_producer_classes_are_closed(self) -> None:
        from core.core_brain.gate.models import PRODUCER_CLASSES
        self.assertEqual(set(PRODUCER_CLASSES), {
            "structural-form", "foundation-form", "operator-review-form",
            "backup-form", "rollback-form", "rt2-audit-form", "human-decision-form",
        })

    def test_every_criterion_maps_to_valid_class(self) -> None:
        from core.core_brain.gate.models import (
            CRITERION_PRODUCER_CLASS,
            PRODUCER_CLASSES,
        )
        self.assertEqual(set(CRITERION_PRODUCER_CLASS), set(range(1, 21)))
        for cid, cls in CRITERION_PRODUCER_CLASS.items():
            self.assertIn(cls, PRODUCER_CLASSES)

    def test_human_decision_form_only_16_20_and_5_is_foundation(self) -> None:
        from core.core_brain.gate.models import CRITERION_PRODUCER_CLASS
        human_form = {c for c, cls in CRITERION_PRODUCER_CLASS.items()
                      if cls == "human-decision-form"}
        self.assertEqual(human_form, {16, 20})
        self.assertEqual(CRITERION_PRODUCER_CLASS[5], "foundation-form")
        self.assertEqual(CRITERION_PRODUCER_CLASS[15], "operator-review-form")

    def test_new_evid_reason_codes_exist(self) -> None:
        from core.core_brain.gate.models import GateReasonCode
        values = {c.value for c in GateReasonCode}
        for code in (
            "GATE-EVID-INVALID-HASH", "GATE-EVID-INVALID-PRODUCER-CLASS",
            "GATE-EVID-CONFLICT-ARTIFACT-ID", "GATE-EVID-CONFLICT-HASH",
            "GATE-EVID-STALE-BINDING", "GATE-EVID-STALE-EVIDENCE-REVISION",
        ):
            self.assertIn(code, values)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
