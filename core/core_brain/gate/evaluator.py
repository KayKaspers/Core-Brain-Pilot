"""Reine Kernlogik des Mapping-Activation-Gate-Evaluators (CBP-WP-016/017).

Diese Schicht ist **rein**: sie öffnet **keine** Dateien, baut **keine**
Verbindungen auf, liest **keine** Uhr, erzeugt **keinen** Zufall und verändert
**nichts**. Sie bildet aus dem Draft-Validitätszustand, dem Allowlist-Zustand,
den Bindungs-Blockern und den **ausschließlich negativen** Artefaktverdikten die
20 Kriterienresultate und einen deterministischen Report.

Human-only decisions: **5, 16, 20** (`HUMAN_DECISION_REQUIRED`).
Human-produced operational evidence: **15**.
Additional operational evidence: **18, 19**.
Diese Kriterien werden durch synthetische Artefakte **nie positiv** erfüllt;
ein Artefakt kann ein Ergebnis höchstens **negativ** überschreiben
(``INVALID_EVIDENCE``/``CONFLICTING_EVIDENCE``/``STALE_EVIDENCE``).

Der synthetische MVP endet **immer** ``BLOCKED``. ``NOT_EVALUATED`` beschreibt
ausschließlich den nicht ausgeführten Zustand und wird hier **nicht** erzeugt.

Der Import dieses Moduls hat keine Nebenwirkungen.
"""

from __future__ import annotations

from typing import Final

from .models import (
    EVIDENCE_CONTRACT_REVISION,
    GATE_CONTRACT_REVISION,
    GATE_CRITERIA,
    REPORT_SCHEMA_VERSION,
    Criterion,
    CriterionOutcome,
    CriterionResult,
    GateEvaluationReport,
    GateReasonCode,
    GateStatus,
    evidence_contract_sha256,
    gate_contract_sha256,
)

__all__ = ["evaluate_criteria", "build_report"]

# Rein negative Faltung: ausschließlich diese Ergebnisse dürfen ein bestehendes
# Kriterienergebnis überschreiben. Eine positive Aufwertung ist **ausgeschlossen**.
_NEGATIVE_OVERRIDES: Final[frozenset[CriterionResult]] = frozenset(
    {
        CriterionResult.INVALID_EVIDENCE,
        CriterionResult.CONFLICTING_EVIDENCE,
        CriterionResult.STALE_EVIDENCE,
    }
)


def _result_for(
    criterion: Criterion, *, draft_valid: bool, allowed_subpaths_nonempty: bool
) -> CriterionResult:
    """Bestimmt das deterministische Basis-MVP-Resultat eines Kriteriums."""
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
    *,
    draft_valid: bool,
    allowed_subpaths_nonempty: bool,
    evidence_overrides: dict[int, CriterionResult] | None = None,
) -> tuple[CriterionOutcome, ...]:
    """Bewertet die 20 Kriterien in fester Reihenfolge 1..20 (negativ gefaltet)."""
    overrides = evidence_overrides or {}
    outcomes: list[CriterionOutcome] = []
    for c in GATE_CRITERIA:
        base = _result_for(
            c,
            draft_valid=draft_valid,
            allowed_subpaths_nonempty=allowed_subpaths_nonempty,
        )
        override = overrides.get(c.criterion_id)
        result = override if override in _NEGATIVE_OVERRIDES else base
        outcomes.append(
            CriterionOutcome(
                criterion_id=c.criterion_id,
                code=c.code,
                nachweisstufe=c.nachweisstufe,
                result=result,
            )
        )
    return tuple(outcomes)


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
    evidence_blockers: list[GateReasonCode] | None = None,
    validated_artifact_count: int = 0,
    invalid_artifact_count: int = 0,
    stale_artifact_count: int = 0,
    conflicting_artifact_count: int = 0,
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
    evidence_codes = [b.value for b in (evidence_blockers or [])]
    blocker_codes = tuple(
        sorted(set(criterion_blockers) | set(binding_codes) | set(evidence_codes))
    )

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
        evidence_contract_revision=EVIDENCE_CONTRACT_REVISION,
        evidence_contract_sha256=evidence_contract_sha256(),
        evaluation_status=status,
        criterion_results=outcomes,
        blocker_codes=blocker_codes,
        blocker_count=len(blocker_codes),
        missing_evidence_codes=missing,
        missing_evidence_count=len(missing),
        human_decision_codes=human,
        human_decision_count=len(human),
        evidence_count=evidence_count,
        validated_artifact_count=validated_artifact_count,
        invalid_artifact_count=invalid_artifact_count,
        stale_artifact_count=stale_artifact_count,
        conflicting_artifact_count=conflicting_artifact_count,
    )
