"""Reine Kernlogik des Mapping-Activation-Gate-Evaluators (CBP-WP-016).

Diese Schicht ist **rein**: sie öffnet **keine** Dateien, baut **keine**
Verbindungen auf, liest **keine** Uhr, erzeugt **keinen** Zufall und verändert
**nichts**. Sie bildet aus dem Draft-Validitätszustand, dem Allowlist-Zustand
und den Bindungs-Blockern die 20 Kriterienresultate und einen deterministischen
Report.

Der synthetische MVP endet **immer** ``BLOCKED``. ``NOT_EVALUATED`` beschreibt
ausschließlich den nicht ausgeführten Zustand und wird hier **nicht** erzeugt.
Human-only-Kriterien (5, 15, 16, 20) gelten **nie** als erfüllt; synthetische
Human-Evidenz hat keine A0-Autorität.

Der Import dieses Moduls hat keine Nebenwirkungen.
"""

from __future__ import annotations

from .models import (
    GATE_CONTRACT_REVISION,
    GATE_CRITERIA,
    REPORT_SCHEMA_VERSION,
    Criterion,
    CriterionOutcome,
    CriterionResult,
    GateEvaluationReport,
    GateReasonCode,
    GateStatus,
    gate_contract_sha256,
)

__all__ = ["evaluate_criteria", "build_report"]


def _result_for(
    criterion: Criterion, *, draft_valid: bool, allowed_subpaths_nonempty: bool
) -> CriterionResult:
    """Bestimmt das deterministische MVP-Resultat eines Kriteriums."""
    if criterion.mvp_result is not None:
        return criterion.mvp_result
    # Aus Draft/Bindung abgeleitete Kriterien.
    if criterion.criterion_id == 9:
        # V12: leere Allowlist nimmt nichts auf. Ein WP-015-VALID_DRAFT ist
        # deaktiviert und trägt eine leere Allowlist ⇒ MISSING_EVIDENCE.
        if draft_valid and allowed_subpaths_nonempty:
            return CriterionResult.SATISFIED
        return CriterionResult.MISSING_EVIDENCE
    # 2, 3, 13, 14 — technisch-dokumentarisch: nur bei gültigem WP-015-Draft.
    return (
        CriterionResult.SATISFIED
        if draft_valid
        else CriterionResult.DEPENDENCY_BLOCKED
    )


def evaluate_criteria(
    *, draft_valid: bool, allowed_subpaths_nonempty: bool
) -> tuple[CriterionOutcome, ...]:
    """Bewertet die 20 Kriterien in fester Reihenfolge 1..20."""
    return tuple(
        CriterionOutcome(
            criterion_id=c.criterion_id,
            code=c.code,
            nachweisstufe=c.nachweisstufe,
            result=_result_for(
                c,
                draft_valid=draft_valid,
                allowed_subpaths_nonempty=allowed_subpaths_nonempty,
            ),
        )
        for c in GATE_CRITERIA
    )


def build_report(
    *,
    source_id: str,
    mapping_id: str,
    mapping_draft_sha256: str,
    mapping_policy_sha256: str,
    registry_record_sha256: str | None,
    outcomes: tuple[CriterionOutcome, ...],
    binding_blockers: list[GateReasonCode],
    evidence_count: int,
) -> GateEvaluationReport:
    """Baut den deterministischen, minimierten A6-Report (immer ``BLOCKED``)."""
    criterion_blockers = [
        o.code for o in outcomes if o.result is not CriterionResult.SATISFIED
    ]
    missing = tuple(
        sorted(o.code for o in outcomes if o.result is CriterionResult.MISSING_EVIDENCE)
    )
    human = tuple(
        sorted(
            o.code
            for o in outcomes
            if o.result is CriterionResult.HUMAN_DECISION_REQUIRED
        )
    )
    binding_codes = [b.value for b in binding_blockers]
    blocker_codes = tuple(sorted(set(criterion_blockers) | set(binding_codes)))

    # Ausgeführte Evaluation: niemals NOT_EVALUATED, niemals READY/APPROVED.
    # Im MVP existiert stets mindestens ein blockierendes Kriterium.
    status = GateStatus.BLOCKED

    return GateEvaluationReport(
        report_schema_version=REPORT_SCHEMA_VERSION,
        source_id=source_id,
        mapping_id=mapping_id,
        mapping_draft_sha256=mapping_draft_sha256,
        mapping_policy_sha256=mapping_policy_sha256,
        registry_record_sha256=registry_record_sha256,
        gate_contract_revision=GATE_CONTRACT_REVISION,
        gate_contract_sha256=gate_contract_sha256(),
        evaluation_status=status,
        criterion_results=outcomes,
        blocker_codes=blocker_codes,
        blocker_count=len(blocker_codes),
        missing_evidence_codes=missing,
        missing_evidence_count=len(missing),
        human_decision_codes=human,
        human_decision_count=len(human),
        evidence_count=evidence_count,
    )
