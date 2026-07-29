"""Orchestrierung des Mapping-Activation-Gate-Evaluators (CBP-WP-016/017/018).

Diese Schicht bindet **read-only** die vorhandenen WP-014-/WP-015-Dienste
(Registry-Record-Lesen, Draft-Validierung) an das synthetische Evidenz-Bundle
3.0 und die reine Kernlogik. Sie **schreibt nichts**, öffnet **keine**
Verbindung, liest **keinen** Source-Inhalt, **aktiviert nichts** und
**verändert keine** Eingabe.

Zusätzlich zum per-Kriterium-Artefaktverdikt (WP-017) prüft sie die elf
kanonischen ``(criterion, control_id)``-Bindungen des statischen Security
Contract (WP-018) rein synthetisch und **rein negativ**: sie bindet
Security-Control-Artefakte an Contract-Revision und -Hash, unterscheidet
mehrere Controls innerhalb eines Kriteriums und faltet ausschließlich negative
Formverdikte (Invalid/Stale/Conflict) in die Kriterienresultate. Sie bestätigt
**keine** Security Readiness, **keine** Wirksamkeit und **keine** Aktivierung.

Der Ausgang ist **immer** ``BLOCKED``. Der Report ist nicht persistent und
besitzt A6-Autorität.

Der Import dieses Moduls hat keine Nebenwirkungen.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any, Final

from ..errors import GateEvidenceError, ReasonCode
from ..mapping import (
    MappingPolicy,
    MappingReasonCode,
    ValidationStatus,
    run_validate,
)
from ..mapping.parser import DraftRejected, parse_draft
from ..mapping.service import _read_registry_record
from ..mapping.validator import _path_url_reason, mapping_id_of
from .evaluator import build_report, evaluate_criteria
from .evidence import EvidenceBundle, load_evidence
from .models import (
    EVIDENCE_CONTRACT_REVISION,
    GATE_CONTRACT_REVISION,
    GATE_CRITERIA,
    CriterionResult,
    GateEvaluationReport,
    GateReasonCode,
    canonical_json_bytes,
    evidence_contract_sha256,
    gate_contract_sha256,
)
from .provenance import (
    ArtifactDescriptor,
    BindingVerdict,
    canonical_binding_sha256,
    evaluate_criterion_artifacts,
    evaluate_security_binding,
)
from .security_contract import (
    DOCUMENTED_CONTROLS,
    RUNTIME_SCOPED_BINDINGS,
    RUNTIME_SCOPED_CONTROLS,
    RUNTIME_SCOPED_CRITERIA,
    SECURITY_CONTRACT_REVISION,
    is_runtime_scoped_binding,
    security_contract_sha256,
)

__all__ = ["run_activation_evaluate"]

# Opake, vertraglich validierte ID-Formen. Nur exakt passende Werte dürfen in
# den Report gelangen — so kann kein Pfad, keine URL, kein Locator und kein
# Secret über `source_id`/`mapping_id` geleakt werden.
_SOURCE_ID_RE: Final[re.Pattern[str]] = re.compile(r"\Asrc-[0-9a-f]{24}\Z")
_MAPPING_ID_RE: Final[re.Pattern[str]] = re.compile(r"\A[A-Za-z0-9][A-Za-z0-9._-]*\Z")

# Report-Sicherheit der opaken `mapping_id`: dieselbe Secret-Vokabel wie in
# `mapping.validator._SECRET_RE` (dort keyword+Zuweisung), hier als Substring-
# Prüfung auf die ID, ergänzt um den Credential-Präfix `akia`. **Keine** zweite,
# unabhängige Secret-Scanner-Architektur — nur dieselbe Vokabel und die
# vorhandene Pfad-/URL-Prüfung, angewandt auf Reportsicherheit.
_MAPPING_ID_SECRET_MARKERS: Final[tuple[str, ...]] = (
    "password",
    "passwd",
    "secret",
    "token",
    "api_key",
    "apikey",
    "access_key",
    "private_key",
    "client_secret",
    "bearer",
    "akia",
)


def _mapping_id_report_safe(value: str) -> bool:
    """True nur für eine opake, syntaxkonforme, leak-/secretfreie ``mapping_id``.

    Der Wert wird ausschließlich geprüft — nie erzeugt, normalisiert, ersetzt
    oder verändert. Wiederverwendet werden die kanonische Syntaxprüfung und die
    bestehende Pfad-/URL-Prüfung aus ``mapping.validator``.
    """
    if not _MAPPING_ID_RE.match(value):
        return False
    if _path_url_reason(value) is not None:
        return False
    lowered = value.lower()
    return not any(marker in lowered for marker in _MAPPING_ID_SECRET_MARKERS)


# Rein negative Faltungspriorität je Kriterium (INVALID vor CONFLICTING vor
# STALE). Mehrere Security-Bindungen und der Nicht-Security-Pfad desselben
# Kriteriums werden zum **schwersten** negativen Verdikt zusammengefasst. Eine
# positive Aufwertung ist ausgeschlossen.
_OVERRIDE_RANK: Final[dict[CriterionResult, int]] = {
    CriterionResult.INVALID_EVIDENCE: 3,
    CriterionResult.CONFLICTING_EVIDENCE: 2,
    CriterionResult.STALE_EVIDENCE: 1,
}


def _worse_override(
    current: CriterionResult | None, candidate: CriterionResult | None
) -> CriterionResult | None:
    """Kombiniert zwei Kriteriums-Overrides zum schwersten (fail-closed)."""
    if candidate is None:
        return current
    if current is None:
        return candidate
    return candidate if _OVERRIDE_RANK[candidate] >= _OVERRIDE_RANK[current] else current


def run_activation_evaluate(
    *,
    draft_path: Path,
    policy: MappingPolicy,
    registry_root: Path,
    source_id: str,
    evidence_path: Path,
    synthetic_confirmed: bool,
) -> GateEvaluationReport:
    """Wertet die 20 Gate-Kriterien read-only gegen synthetische Evidenz aus.

    Returns:
        Einen deterministischen, nicht persistierten :class:`GateEvaluationReport`
        mit ``evaluation_status = BLOCKED`` (fail-closed). **Keine** Freigabe,
        **keine** Aktivierung.

    Raises:
        GateEvidenceError: Bei fehlender Synthetic-Bestätigung oder strukturell
            ungültigem Evidenz-Bundle.
    """
    if not synthetic_confirmed:
        raise GateEvidenceError(ReasonCode.GATE_SYNTHETIC_CONFIRMATION_MISSING)

    # Leak-Schutz: eine nicht opake Source ID (Pfad, URL, Locator, Secret)
    # darf niemals in den Report gelangen — fail-closed abweisen.
    if not _SOURCE_ID_RE.match(source_id):
        raise GateEvidenceError(ReasonCode.GATE_EVIDENCE_INVALID_VALUE, "source_id")

    evidence = load_evidence(evidence_path)

    # Draft-Rohbytes (read-only) und deterministischer Hash.
    try:
        raw = draft_path.read_bytes()
    except OSError as exc:
        raise GateEvidenceError(
            ReasonCode.GATE_EVIDENCE_INVALID_VALUE, "draft not readable"
        ) from exc
    draft_sha256 = hashlib.sha256(raw).hexdigest()

    # WP-015-Validierung (liefert VALID_DRAFT oder BLOCKED).
    validation = run_validate(
        draft_path=draft_path,
        policy=policy,
        registry_root=registry_root,
        source_id=source_id,
        synthetic_confirmed=True,
    )
    draft_valid = validation.validation_status is ValidationStatus.VALID_DRAFT

    # Draft strukturell parsen (nur zum Lesen von mapping_id/allowed_subpaths).
    draft: dict[str, Any] | None = None
    try:
        draft = parse_draft(raw, policy.max_draft_bytes)
    except DraftRejected:
        draft = None
    # `mapping_id` ist ein Pflichtfeld. Der Wert wird nur gelesen — nie erzeugt,
    # normalisiert, ersetzt oder auf ``null`` redigiert. Ein fehlender,
    # syntaktisch ungültiger oder nicht report-sicherer (pfad-/URL-/
    # secretverdächtiger) Wert blockiert **fail-closed vor** der Reporterzeugung:
    # kein Report, kein Echo des Werts. Nur ein gültiger, report-sicherer Wert
    # gelangt unverändert in den Report.
    raw_mapping_id = mapping_id_of(draft) if draft is not None else None
    if raw_mapping_id is None or not _mapping_id_report_safe(raw_mapping_id):
        raise GateEvidenceError(ReasonCode.GATE_EVIDENCE_INVALID_VALUE, "mapping_id")
    mapping_id = raw_mapping_id
    allowed_nonempty = bool(
        draft is not None and isinstance(draft.get("allowed_subpaths"), list)
        and len(draft["allowed_subpaths"]) > 0
    )

    # Registry-Record read-only lesen und kanonisch hashen.
    record_reasons, record = _read_registry_record(registry_root, source_id)
    registry_record_sha256: str | None = None
    if record is not None:
        registry_record_sha256 = hashlib.sha256(
            canonical_json_bytes(record)
        ).hexdigest()

    binding = _binding_blockers(
        evidence=evidence,
        source_id=source_id,
        mapping_id=mapping_id,
        draft_valid=draft_valid,
        record=record,
        record_reasons=record_reasons,
        draft_sha256=draft_sha256,
        policy_sha256=policy.policy_sha256,
        registry_record_sha256=registry_record_sha256,
    )

    # CBP-WP-017/018 — je Kriterium: erwartete Bindung (aktueller Snapshot),
    # rein negatives Artefaktverdikt und Artefaktzählung. Security-Control-Form-
    # Artefakte werden zusätzlich je `(criterion, control_id)`-Bindung geprüft.
    # Kein Uhrbezug, keine positive Erfüllung, keine Persistenz.
    gate_sha = gate_contract_sha256()
    evidence_sha = evidence_contract_sha256()
    security_rev = SECURITY_CONTRACT_REVISION
    security_sha = security_contract_sha256()
    # Ein Bundle, dessen eingebettete Security-Contract-Bindung nicht dem
    # aktuellen statischen Vertrag entspricht, gilt als **stale**: alle
    # Security-Control-Artefakte werden STALE — historische Paare werden nicht
    # nachträglich als aktuelle Invalid-Behauptung umklassifiziert.
    contract_stale = (
        evidence.security_contract_revision != security_rev
        or evidence.security_contract_sha256 != security_sha
    )

    evidence_overrides: dict[int, CriterionResult | None] = {}
    evidence_blockers: list[GateReasonCode] = []
    validated = invalid = stale = conflicting = 0

    # Security-Control-Artefakte je `(criterion, control_id)` gruppieren; alle
    # übrigen Artefakte laufen über den bestehenden per-Kriterium-Pfad (WP-017).
    security_groups: dict[tuple[int, str], list[ArtifactDescriptor]] = {}
    for cid, arts in evidence.criterion_artifacts.items():
        for art in arts:
            if art.control_id is not None:
                security_groups.setdefault((cid, art.control_id), []).append(art)

    # Nicht-Security-Pfad (WP-017): per Kriterium, ausschließlich `control_id`-freie
    # Artefakte. Mehrere Security-Controls desselben Kriteriums werden dadurch
    # **nicht** fälschlich als CONFLICT verrechnet.
    for criterion in GATE_CRITERIA:
        cid = criterion.criterion_id
        non_security = tuple(
            a
            for a in evidence.criterion_artifacts.get(cid, ())
            if a.control_id is None
        )
        expected_binding = canonical_binding_sha256(
            source_id=source_id,
            mapping_id=mapping_id,
            criterion=cid,
            mapping_draft_sha256=draft_sha256,
            mapping_policy_sha256=policy.policy_sha256,
            registry_record_sha256=registry_record_sha256,
            gate_contract_revision=GATE_CONTRACT_REVISION,
            gate_contract_sha256=gate_sha,
            evidence_contract_revision=EVIDENCE_CONTRACT_REVISION,
            evidence_contract_sha256=evidence_sha,
            evidence_revision=evidence.evidence_revision,
        )
        ce = evaluate_criterion_artifacts(
            cid,
            non_security,
            expected_binding_sha256=expected_binding,
            bundle_evidence_revision=evidence.evidence_revision,
        )
        evidence_overrides[cid] = _worse_override(
            evidence_overrides.get(cid), ce.override
        )
        evidence_blockers.extend(ce.reason_codes)
        validated += ce.validated_count
        invalid += ce.invalid_count
        stale += ce.stale_count
        conflicting += ce.conflicting_count

    # Security-Pfad (WP-018): die elf kanonischen `(criterion, control_id)`-
    # Bindungen. Jede Bindung wird geprüft — auch ohne Artefakt (⇒ MISSING). Die
    # Fünf-Wege-Partition summiert sich exakt auf `runtime_scoped_binding_count`.
    verdict_counts: dict[BindingVerdict, int] = {v: 0 for v in BindingVerdict}
    for crit, ctrl in RUNTIME_SCOPED_BINDINGS:
        arts = tuple(security_groups.pop((crit, ctrl), ()))
        expected_binding = canonical_binding_sha256(
            source_id=source_id,
            mapping_id=mapping_id,
            criterion=crit,
            mapping_draft_sha256=draft_sha256,
            mapping_policy_sha256=policy.policy_sha256,
            registry_record_sha256=registry_record_sha256,
            gate_contract_revision=GATE_CONTRACT_REVISION,
            gate_contract_sha256=gate_sha,
            evidence_contract_revision=EVIDENCE_CONTRACT_REVISION,
            evidence_contract_sha256=evidence_sha,
            evidence_revision=evidence.evidence_revision,
            control_id=ctrl,
            security_contract_revision=security_rev,
            security_contract_sha256=security_sha,
        )
        result = evaluate_security_binding(
            arts,
            criterion_is_security=True,
            is_expected_pair=True,
            expected_binding_sha256=expected_binding,
            bundle_evidence_revision=evidence.evidence_revision,
            contract_stale=contract_stale,
        )
        verdict_counts[result.verdict] += 1
        evidence_overrides[crit] = _worse_override(
            evidence_overrides.get(crit), result.override
        )
        evidence_blockers.extend(result.reason_codes)
        validated += result.validated_count
        invalid += result.invalid_count
        stale += result.stale_count
        conflicting += result.conflicting_count

    # Unerwartete/zusätzliche Security-Control-Artefakte (kein kanonisches Paar
    # oder falsches Kriterium): sie erzeugen negative Verdikte (Override +
    # Artefaktzählung + Reason-Code), zählen aber **nicht** zur Elf-Bindungs-
    # Partition. Deterministische Reihenfolge über sortierte Schlüssel.
    for crit, ctrl in sorted(security_groups):
        result = evaluate_security_binding(
            tuple(security_groups[(crit, ctrl)]),
            criterion_is_security=crit in RUNTIME_SCOPED_CRITERIA,
            is_expected_pair=is_runtime_scoped_binding(crit, ctrl),
            expected_binding_sha256="",
            bundle_evidence_revision=evidence.evidence_revision,
            contract_stale=contract_stale,
        )
        evidence_overrides[crit] = _worse_override(
            evidence_overrides.get(crit), result.override
        )
        evidence_blockers.extend(result.reason_codes)
        validated += result.validated_count
        invalid += result.invalid_count
        stale += result.stale_count
        conflicting += result.conflicting_count

    # Nur negative Faltung an die Kernlogik geben (None-Overrides entfernen).
    effective_overrides = {
        cid: ov for cid, ov in evidence_overrides.items() if ov is not None
    }

    outcomes = evaluate_criteria(
        draft_valid=draft_valid,
        allowed_subpaths_nonempty=allowed_nonempty,
        evidence_overrides=effective_overrides,
    )

    return build_report(
        source_id=source_id,
        mapping_id=mapping_id,
        mapping_draft_sha256=draft_sha256,
        mapping_policy_sha256=policy.policy_sha256,
        registry_record_sha256=registry_record_sha256,
        outcomes=outcomes,
        binding_blockers=binding,
        evidence_count=evidence.total_artifact_count,
        evidence_blockers=evidence_blockers,
        validated_artifact_count=validated,
        invalid_artifact_count=invalid,
        stale_artifact_count=stale,
        conflicting_artifact_count=conflicting,
        security_contract_revision=security_rev,
        security_contract_sha256=security_sha,
        documented_control_count=len(DOCUMENTED_CONTROLS),
        runtime_scoped_control_count=len(RUNTIME_SCOPED_CONTROLS),
        runtime_scoped_binding_count=len(RUNTIME_SCOPED_BINDINGS),
        valid_form_binding_count=verdict_counts[BindingVerdict.VALID],
        missing_form_binding_count=verdict_counts[BindingVerdict.MISSING],
        invalid_form_binding_count=verdict_counts[BindingVerdict.INVALID],
        stale_form_binding_count=verdict_counts[BindingVerdict.STALE],
        conflicting_form_binding_count=verdict_counts[BindingVerdict.CONFLICTING],
        operationally_unevaluated_binding_count=len(RUNTIME_SCOPED_BINDINGS),
    )


def _binding_blockers(
    *,
    evidence: EvidenceBundle,
    source_id: str,
    mapping_id: str,
    draft_valid: bool,
    record: dict[str, Any] | None,
    record_reasons: list,
    draft_sha256: str,
    policy_sha256: str,
    registry_record_sha256: str | None,
) -> list[GateReasonCode]:
    """Ermittelt die deterministischen Bindungs-Blocker (fail-closed)."""
    blockers: list[GateReasonCode] = []

    if not draft_valid:
        blockers.append(GateReasonCode.BIND_DRAFT_NOT_VALID)

    if record is None:
        if MappingReasonCode.REGISTRY_RETIRED in record_reasons:
            blockers.append(GateReasonCode.BIND_SOURCE_NOT_REGISTERED_DISABLED)
        else:
            blockers.append(GateReasonCode.BIND_REGISTRY_NOT_BOUND)

    if evidence.source_id != source_id:
        blockers.append(GateReasonCode.BIND_SOURCE_ID_MISMATCH)
    if evidence.mapping_id != mapping_id:
        blockers.append(GateReasonCode.BIND_MAPPING_ID_MISMATCH)
    if evidence.gate_contract_revision != GATE_CONTRACT_REVISION:
        blockers.append(GateReasonCode.BIND_CONTRACT_REVISION_MISMATCH)

    if evidence.mapping_draft_sha256 != draft_sha256:
        blockers.append(GateReasonCode.BIND_DRAFT_HASH_MISMATCH)
    if evidence.mapping_policy_sha256 != policy_sha256:
        blockers.append(GateReasonCode.BIND_POLICY_HASH_MISMATCH)
    if (
        registry_record_sha256 is None
        or evidence.registry_record_sha256 != registry_record_sha256
    ):
        blockers.append(GateReasonCode.BIND_RECORD_HASH_MISMATCH)

    return blockers
