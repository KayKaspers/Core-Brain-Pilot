"""Orchestrierung des Mapping-Activation-Gate-Evaluators (CBP-WP-016).

Diese Schicht bindet **read-only** die vorhandenen WP-014-/WP-015-Dienste
(Registry-Record-Lesen, Draft-Validierung) an das synthetische Evidenz-Bundle
und die reine Kernlogik. Sie **schreibt nichts**, öffnet **keine** Verbindung,
liest **keinen** Source-Inhalt, **aktiviert nichts** und **verändert keine**
Eingabe.

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
from .provenance import canonical_binding_sha256, evaluate_criterion_artifacts

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

    # CBP-WP-017 — je Kriterium: erwartete Bindung (aktueller Snapshot),
    # rein negatives Artefaktverdikt und Artefaktzählung. Kein Uhrbezug,
    # keine positive Erfüllung, keine Persistenz.
    gate_sha = gate_contract_sha256()
    evidence_sha = evidence_contract_sha256()
    evidence_overrides: dict[int, CriterionResult] = {}
    evidence_blockers: list[GateReasonCode] = []
    validated = invalid = stale = conflicting = 0
    for criterion in GATE_CRITERIA:
        cid = criterion.criterion_id
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
            evidence.criterion_artifacts.get(cid, ()),
            expected_binding_sha256=expected_binding,
            bundle_evidence_revision=evidence.evidence_revision,
        )
        if ce.override is not None:
            evidence_overrides[cid] = ce.override
        evidence_blockers.extend(ce.reason_codes)
        validated += ce.validated_count
        invalid += ce.invalid_count
        stale += ce.stale_count
        conflicting += ce.conflicting_count

    outcomes = evaluate_criteria(
        draft_valid=draft_valid,
        allowed_subpaths_nonempty=allowed_nonempty,
        evidence_overrides=evidence_overrides,
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
