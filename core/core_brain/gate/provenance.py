"""Deterministische Provenance- und Artefaktsemantik (CBP-WP-017).

Diese Schicht ist **rein**: keine Datei-, Netz-, Uhr- oder Zufallszugriffe,
keine Mutation. Sie berechnet die kanonischen Artefakt- und Bindungs-Hashes und
leitet je Kriterium ein **ausschließlich negatives** Evidenzverdikt ab
(``INVALID`` / ``CONFLICTING`` / ``STALE`` / ``NONE``). Ein formal gültiges,
aktuelles synthetisches Artefakt erzeugt **nie** eine positive Erfüllung.

Prioritätsreihenfolge je Kriterium: ``INVALID`` vor ``CONFLICTING`` vor
``STALE`` vor dem bestehenden Kriterienergebnis. Staleness ist rein revisions-
und bindungsbasiert (**keine** Uhr). Konflikte werden **nie** automatisch
aufgelöst (kein „letzter Wert gewinnt").

Der Import dieses Moduls hat keine Nebenwirkungen.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from enum import Enum
from typing import Final

from .models import (
    CRITERION_PRODUCER_CLASS,
    CriterionResult,
    GateReasonCode,
    canonical_json_bytes,
)

__all__ = [
    "ArtifactDescriptor",
    "ArtifactStatus",
    "CriterionEvidence",
    "canonical_artifact_sha256",
    "canonical_binding_sha256",
    "evaluate_criterion_artifacts",
]


@dataclass(frozen=True, slots=True)
class ArtifactDescriptor:
    """Ein validiertes, synthetisches Evidenzartefakt (read-only, opak)."""

    artifact_id: str
    artifact_sha256: str
    binding_sha256: str
    producer_class: str
    evidence_revision: int
    synthetic_test_only: bool

    def dedup_key(self) -> tuple[str, str, str, str, int, bool]:
        """Vollständige kanonische Identität für die Deduplizierung."""
        return (
            self.artifact_id,
            self.artifact_sha256,
            self.binding_sha256,
            self.producer_class,
            self.evidence_revision,
            self.synthetic_test_only,
        )


class ArtifactStatus(str, Enum):
    """Intrinsischer Einzelstatus eines Artefakts (vor Konfliktbildung)."""

    FRESH = "FRESH"
    STALE = "STALE"
    INVALID = "INVALID"


@dataclass(frozen=True, slots=True)
class CriterionEvidence:
    """Aggregiertes negatives Verdikt eines Kriteriums mit Artefaktzählung."""

    #: Negatives Überschreibungsergebnis oder ``None`` (keine Herabstufung).
    override: CriterionResult | None
    reason_codes: tuple[GateReasonCode, ...]
    validated_count: int
    invalid_count: int
    stale_count: int
    conflicting_count: int


def canonical_artifact_sha256(
    *,
    artifact_id: str,
    binding_sha256: str,
    producer_class: str,
    evidence_revision: int,
    synthetic_test_only: bool,
) -> str:
    """SHA-256 der kanonischen Artefaktbeschreibung **ohne** ``artifact_sha256``."""
    payload = {
        "artifact_id": artifact_id,
        "binding_sha256": binding_sha256,
        "producer_class": producer_class,
        "evidence_revision": evidence_revision,
        "synthetic_test_only": synthetic_test_only,
    }
    return hashlib.sha256(canonical_json_bytes(payload)).hexdigest()


def canonical_binding_sha256(
    *,
    source_id: str,
    mapping_id: str,
    criterion: int,
    mapping_draft_sha256: str,
    mapping_policy_sha256: str,
    registry_record_sha256: str | None,
    gate_contract_revision: str,
    gate_contract_sha256: str,
    evidence_contract_revision: str,
    evidence_contract_sha256: str,
    evidence_revision: int,
) -> str:
    """SHA-256 der kanonischen Kriteriumsbindung (aktueller Snapshot)."""
    payload = {
        "source_id": source_id,
        "mapping_id": mapping_id,
        "criterion": criterion,
        "mapping_draft_sha256": mapping_draft_sha256,
        "mapping_policy_sha256": mapping_policy_sha256,
        "registry_record_sha256": registry_record_sha256,
        "gate_contract_revision": gate_contract_revision,
        "gate_contract_sha256": gate_contract_sha256,
        "evidence_contract_revision": evidence_contract_revision,
        "evidence_contract_sha256": evidence_contract_sha256,
        "evidence_revision": evidence_revision,
    }
    return hashlib.sha256(canonical_json_bytes(payload)).hexdigest()


def _intrinsic_status(
    artifact: ArtifactDescriptor,
    *,
    criterion: int,
    expected_binding_sha256: str,
    bundle_evidence_revision: int,
) -> tuple[ArtifactStatus, tuple[GateReasonCode, ...]]:
    """Bestimmt Einzelstatus + Gründe eines Artefakts (fail-closed, negativ)."""
    codes: list[GateReasonCode] = []

    # 1 — Integrität: der gespeicherte Hash muss die kanonische Beschreibung decken.
    recomputed = canonical_artifact_sha256(
        artifact_id=artifact.artifact_id,
        binding_sha256=artifact.binding_sha256,
        producer_class=artifact.producer_class,
        evidence_revision=artifact.evidence_revision,
        synthetic_test_only=artifact.synthetic_test_only,
    )
    if recomputed != artifact.artifact_sha256:
        codes.append(GateReasonCode.EVID_INVALID_HASH)

    # 2 — Kriterienklassenzuordnung: die Producer-Klasse muss für das Kriterium
    #     zulässig sein (formale Zuordnung; erfüllt nie ein Kriterium).
    if CRITERION_PRODUCER_CLASS.get(criterion) != artifact.producer_class:
        codes.append(GateReasonCode.EVID_INVALID_PRODUCER_CLASS)

    if codes:
        return ArtifactStatus.INVALID, tuple(codes)

    # 3 — Staleness (rein revisions-/bindungsbasiert, keine Uhr).
    stale_codes: list[GateReasonCode] = []
    if artifact.evidence_revision != bundle_evidence_revision:
        stale_codes.append(GateReasonCode.EVID_STALE_EVIDENCE_REVISION)
    if artifact.binding_sha256 != expected_binding_sha256:
        stale_codes.append(GateReasonCode.EVID_STALE_BINDING)
    if stale_codes:
        return ArtifactStatus.STALE, tuple(stale_codes)

    return ArtifactStatus.FRESH, ()


def evaluate_criterion_artifacts(
    criterion: int,
    artifacts: tuple[ArtifactDescriptor, ...],
    *,
    expected_binding_sha256: str,
    bundle_evidence_revision: int,
) -> CriterionEvidence:
    """Leitet das rein negative Kriteriumsverdikt aus seinen Artefakten ab.

    Deterministisch, fail-closed, ohne Uhr. Identische Artefakte werden
    dedupliziert; Konflikte werden **nie** automatisch aufgelöst.
    """
    # Deterministische Deduplizierung nach vollständiger kanonischer Beschreibung.
    unique: list[ArtifactDescriptor] = []
    seen: set[tuple[str, str, str, str, int, bool]] = set()
    for art in artifacts:
        key = art.dedup_key()
        if key not in seen:
            seen.add(key)
            unique.append(art)

    # Stabile Sortierung: criterion (fix) → artifact_id → artifact_sha256.
    unique.sort(key=lambda a: (a.artifact_id, a.artifact_sha256))

    statuses: list[tuple[ArtifactDescriptor, ArtifactStatus, tuple[GateReasonCode, ...]]] = []
    for art in unique:
        status, codes = _intrinsic_status(
            art,
            criterion=criterion,
            expected_binding_sha256=expected_binding_sha256,
            bundle_evidence_revision=bundle_evidence_revision,
        )
        statuses.append((art, status, codes))

    invalid = [s for s in statuses if s[1] is ArtifactStatus.INVALID]
    stale = [s for s in statuses if s[1] is ArtifactStatus.STALE]

    # Konflikterkennung (nur unter nicht-invaliden, eindeutigen Artefakten).
    non_invalid = [s for s in statuses if s[1] is not ArtifactStatus.INVALID]
    conflict_codes: list[GateReasonCode] = []
    by_id: dict[str, set[str]] = {}
    for art, _status, _codes in non_invalid:
        by_id.setdefault(art.artifact_id, set()).add(art.artifact_sha256)
    if any(len(hashes) > 1 for hashes in by_id.values()):
        conflict_codes.append(GateReasonCode.EVID_CONFLICT_ARTIFACT_ID)
    if len(non_invalid) > 1:
        conflict_codes.append(GateReasonCode.EVID_CONFLICT_HASH)
    is_conflict = bool(conflict_codes)

    # Priorität: INVALID → CONFLICTING → STALE → NONE.
    if invalid:
        override: CriterionResult | None = CriterionResult.INVALID_EVIDENCE
        codes = _dedup_sorted(c for _a, _s, cs in invalid for c in cs)
    elif is_conflict:
        override = CriterionResult.CONFLICTING_EVIDENCE
        codes = _dedup_sorted(conflict_codes)
    elif stale:
        override = CriterionResult.STALE_EVIDENCE
        codes = _dedup_sorted(c for _a, _s, cs in stale for c in cs)
    else:
        override = None
        codes = ()

    # Per-Artefakt-Klassifikation für die Zähler (eindeutige Artefakte).
    invalid_count = len(invalid)
    conflicting_count = len(non_invalid) if is_conflict else 0
    stale_count = 0 if is_conflict else len(stale)
    validated_count = (
        0 if is_conflict else sum(1 for _a, st, _c in statuses if st is ArtifactStatus.FRESH)
    )

    return CriterionEvidence(
        override=override,
        reason_codes=codes,
        validated_count=validated_count,
        invalid_count=invalid_count,
        stale_count=stale_count,
        conflicting_count=conflicting_count,
    )


def _dedup_sorted(codes) -> tuple[GateReasonCode, ...]:
    """Sortiert und dedupliziert Reason-Codes deterministisch (nach Wert)."""
    return tuple(sorted(set(codes), key=lambda c: c.value))
