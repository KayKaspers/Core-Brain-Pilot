"""Orchestrierung des Source-Mapping-Draft-Validators (CBP-WP-015).

Diese Schicht verbindet Parser, Vertragsvalidierung und die **externe,
read-only** Registry-Bindung zu einem **nicht persistierten**,
deterministischen :class:`ValidationReport`. Sie **schreibt nichts**, öffnet
**keine** Verbindung, liest **keinen** Source-Inhalt und **aktiviert nichts**.

Die Registry wird **direkt und read-only** gelesen (``records/<source-id>.json``
und ``events/<source-id>/``). Es wird **kein** :class:`RegistryStorage`
instanziiert — dessen Konstruktor würde Verzeichnisse anlegen. Kein Lock, kein
Record, kein Event und kein Katalog wird geschrieben.

Der Import dieses Moduls hat keine Nebenwirkungen.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Final

from ..registry.models import RECORD_FIELDS, LifecycleState
from .models import (
    CONTRACT_FIELD_COUNT,
    REPORT_SCHEMA_VERSION,
    REQUIRED_FIELD_COUNT,
    MappingPolicy,
    MappingReasonCode,
    ValidationReport,
    ValidationStatus,
)
from .parser import DraftRejected, parse_draft
from .validator import (
    boundary_count,
    compare_to_registry,
    mapping_id_of,
    present_field_count,
    validate_contract_and_state,
)

__all__ = ["run_validate", "run_activation_check"]

R = MappingReasonCode
_SOURCE_ID_RE: Final[re.Pattern[str]] = re.compile(r"\Asrc-[0-9a-f]{24}\Z")
_EVENT_ID_RE: Final[re.Pattern[str]] = re.compile(r"\Aevt-[0-9a-f]{24}\Z")
# Nur diese Registry-Felder werden für die Bindung gelesen. Keine
# source_reference, kein Registry-Root und kein anderer Wert verlässt den Report.
_BOUND_FIELDS: Final[tuple[str, ...]] = (
    "collection_key",
    "data_class",
    "source_reference",
)


def run_validate(
    *,
    draft_path: Path,
    policy: MappingPolicy,
    registry_root: Path,
    source_id: str,
    synthetic_confirmed: bool,
) -> ValidationReport:
    """Validiert einen Mapping-Entwurf read-only gegen Vertrag und Registry.

    Args:
        draft_path: Pfad zum synthetischen Mapping-Entwurf (nur gelesen).
        policy: Bereits validierte, fail-closed Policy.
        registry_root: Registry-Wurzel (nur gelesen, niemals angelegt).
        source_id: Externe Source ID; **kein** Mapping-Feld.
        synthetic_confirmed: Ob ``--synthetic-test-only`` gesetzt war.

    Returns:
        Einen deterministischen, nicht persistierten :class:`ValidationReport`.
        ``VALID_DRAFT`` bedeutet **keine** Freigabe und **keine** Aktivierung.
    """
    reasons: list[MappingReasonCode] = []

    try:
        raw = draft_path.read_bytes()
        file_missing = False
    except OSError:
        raw = b""
        file_missing = True
    draft_sha256 = hashlib.sha256(raw).hexdigest()

    if not synthetic_confirmed:
        reasons.append(R.SYNTHETIC_CONFIRMATION_MISSING)

    draft: dict[str, Any] | None = None
    if file_missing:
        reasons.append(R.DRAFT_FILE_MISSING)
    else:
        try:
            draft = parse_draft(raw, policy.max_draft_bytes)
        except DraftRejected as exc:
            reasons.append(exc.reason)

    mapping_id_value: str | None = None
    present = 0
    boundary = 0
    if draft is not None:
        mapping_id_value = mapping_id_of(draft)
        present = present_field_count(draft)
        boundary = boundary_count(draft)
        reasons.extend(validate_contract_and_state(draft, policy))

    if policy.require_registry_binding:
        record_reasons, record = _read_registry_record(registry_root, source_id)
        reasons.extend(record_reasons)
        if draft is not None and record is not None:
            reasons.extend(
                compare_to_registry(
                    draft,
                    collection_key=record["collection_key"],
                    data_class=record["data_class"],
                    source_reference=record["source_reference"],
                    policy=policy,
                )
            )

    return _build_report(
        mapping_id=mapping_id_value,
        source_id=source_id,
        draft_sha256=draft_sha256,
        policy=policy,
        reasons=reasons,
        present=present,
        boundary=boundary,
    )


def run_activation_check(
    *,
    draft_path: Path,
    policy: MappingPolicy,
    registry_root: Path,
    source_id: str,
    synthetic_confirmed: bool,
) -> ValidationReport:
    """Validiert zunächst fail-closed, verweigert danach jede Aktivierung.

    Diese Funktion **aktiviert nichts** und **schreibt nichts**. Sie liefert
    denselben read-only Report wie :func:`run_validate`; die tatsächliche
    Aktivierungsverweigerung (Exitcode 13) verantwortet die CLI **unabhängig**
    vom Validierungsergebnis.
    """
    return run_validate(
        draft_path=draft_path,
        policy=policy,
        registry_root=registry_root,
        source_id=source_id,
        synthetic_confirmed=synthetic_confirmed,
    )


def _read_registry_record(
    registry_root: Path, source_id: str
) -> tuple[list[MappingReasonCode], dict[str, Any] | None]:
    """Liest einen Registry-Record **read-only**; legt nichts an.

    Returns:
        Ein Paar ``(reasons, record)``. ``record`` ist ``None``, sobald ein
        blockierender Grund vorliegt.
    """
    if not _SOURCE_ID_RE.match(source_id):
        return [R.SOURCE_ID_INVALID], None

    record_path = registry_root / "records" / f"{source_id}.json"
    if not record_path.is_file():
        return [R.REGISTRY_NOT_FOUND], None
    try:
        data = json.loads(record_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return [R.REGISTRY_RECORD_INVALID], None

    if not isinstance(data, dict) or set(data) != set(RECORD_FIELDS):
        return [R.REGISTRY_RECORD_INVALID], None
    if any(not isinstance(data.get(field), str) for field in _BOUND_FIELDS):
        return [R.REGISTRY_RECORD_INVALID], None
    try:
        state = LifecycleState(data["lifecycle_state"])
    except (KeyError, ValueError):
        return [R.REGISTRY_RECORD_INVALID], None

    if _has_retirement_event(registry_root, source_id) or state is LifecycleState.RETIRED:
        return [R.REGISTRY_RETIRED], None
    if state is not LifecycleState.REGISTERED_DISABLED:
        return [R.REGISTRY_RECORD_INVALID], None

    return [], data


def _has_retirement_event(registry_root: Path, source_id: str) -> bool:
    """Prüft read-only, ob mindestens ein Retirement-Event vorliegt."""
    events_dir = registry_root / "events" / source_id
    if not events_dir.is_dir():
        return False
    return any(_EVENT_ID_RE.match(p.stem) for p in events_dir.glob("*.json"))


def _build_report(
    *,
    mapping_id: str | None,
    source_id: str,
    draft_sha256: str,
    policy: MappingPolicy,
    reasons: list[MappingReasonCode],
    present: int,
    boundary: int,
) -> ValidationReport:
    """Baut den deterministischen, minimierten Report (sortiert, dedupliziert)."""
    codes = tuple(sorted({reason.value for reason in reasons}))
    status = ValidationStatus.VALID_DRAFT if not codes else ValidationStatus.BLOCKED
    return ValidationReport(
        report_schema_version=REPORT_SCHEMA_VERSION,
        mapping_id=mapping_id,
        source_id=source_id,
        draft_sha256=draft_sha256,
        policy_sha256=policy.policy_sha256,
        mapping_schema_version=policy.required_mapping_schema_version,
        validation_status=status,
        reason_codes=codes,
        reason_count=len(codes),
        canonical_contract_field_count=CONTRACT_FIELD_COUNT,
        required_field_count=REQUIRED_FIELD_COUNT,
        present_field_count=present,
        boundary_count=boundary,
    )
