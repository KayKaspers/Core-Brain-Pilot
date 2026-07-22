"""Orchestrierung der Source Registry (CBP-WP-014).

Validiert synthetische Source-Definitionen, leitet deterministische Source IDs
ab, registriert unveränderliche Records im Zustand ``REGISTERED_DISABLED``,
dokumentiert Retirement als append-only Event und leitet den Katalog ab. Sie
**aktiviert nichts**, liest **keinen** Source-Inhalt und öffnet **keine**
Verbindung.

Uhr und Speicher sind injizierbar. Der Import hat keine Nebenwirkungen.
"""

from __future__ import annotations

import hashlib
import json
import re
import tomllib
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Final

from ..errors import (
    RegistryDefinitionRejected,
    RegistryNotFound,
    ReasonCode,
)
from .catalog import Clock, build_catalog, default_clock, effective_state
from .models import (
    DEFINITION_FIELDS,
    DEFINITION_SCHEMA_VERSION,
    EVENT_SCHEMA_VERSION,
    IDENTITY_SCHEMA_VERSION,
    RECORD_SCHEMA_VERSION,
    EventType,
    LifecycleState,
    RegistryPolicy,
    RegistryRecord,
    RetirementEvent,
    SourceDefinition,
)
from .storage import RegistryStorage

__all__ = [
    "SYNTHETIC_SOURCE_PREFIX",
    "RETIREMENT_REASON_CODE",
    "RetireOutcome",
    "load_definition",
    "validate_definition",
    "derive_source_id",
    "register",
    "retire",
    "inspect",
    "rebuild_catalog",
]

SYNTHETIC_SOURCE_PREFIX = "synthetic:"
RETIREMENT_REASON_CODE = "HUMAN_REQUESTED_SYNTHETIC_RETIREMENT"

_SLUG: Final[re.Pattern[str]] = re.compile(r"\A[a-z0-9]+(-[a-z0-9]+)*\Z")
_SAFE_REFERENCE: Final[frozenset[str]] = frozenset(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.:_-"
)
_SLUG_FIELDS: Final[tuple[str, ...]] = (
    "namespace",
    "source_key",
    "collection_key",
    "domain_key",
    "owner_role",
)
_URL_MARKERS: Final[tuple[str, ...]] = ("://", "http:", "https:", "ftp:", "file:", "www.")


@dataclass(frozen=True, slots=True)
class RetireOutcome:
    """Ergebnis von :func:`retire`.

    ``event`` ist ``None``, wenn die Source bereits stillgelegt war (idempotent).
    """

    record: RegistryRecord
    event: RetirementEvent | None
    lifecycle_state: LifecycleState


# -- Definition -----------------------------------------------------------


def load_definition(path: Path, policy: RegistryPolicy) -> SourceDefinition:
    """Lädt und validiert eine synthetische Source-Definition.

    Raises:
        RegistryDefinitionRejected: Datei fehlt, zu groß, nicht parsebar oder
            schemawidrig.
    """
    if not path.is_file():
        raise RegistryDefinitionRejected(
            ReasonCode.REGISTRY_DEFINITION_FILE_MISSING, "definition"
        )
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise RegistryDefinitionRejected(
            ReasonCode.REGISTRY_DEFINITION_NOT_READABLE, "definition"
        ) from exc
    if len(raw) > policy.max_definition_bytes:
        raise RegistryDefinitionRejected(
            ReasonCode.REGISTRY_DEFINITION_INVALID_VALUE, "definition too large"
        )
    try:
        data = tomllib.loads(raw.decode("utf-8"))
    except (tomllib.TOMLDecodeError, UnicodeDecodeError) as exc:
        raise RegistryDefinitionRejected(
            ReasonCode.REGISTRY_DEFINITION_PARSE_ERROR, "definition"
        ) from exc
    return validate_definition(data, policy)


def validate_definition(data: dict[str, Any], policy: RegistryPolicy) -> SourceDefinition:
    """Validiert ein geparstes Definition-Mapping fail-closed.

    Raises:
        RegistryDefinitionRejected: Bei jedem Verstoß. Prüfreihenfolge stabil.
    """
    raw_version = data.get("schema_version")
    if raw_version is None:
        raise RegistryDefinitionRejected(
            ReasonCode.REGISTRY_DEFINITION_MISSING_FIELD, "schema_version"
        )
    if not isinstance(raw_version, str) or raw_version != DEFINITION_SCHEMA_VERSION:
        raise RegistryDefinitionRejected(
            ReasonCode.REGISTRY_DEFINITION_SCHEMA_UNSUPPORTED,
            f"expected {DEFINITION_SCHEMA_VERSION}",
        )

    unknown = sorted(set(data) - DEFINITION_FIELDS)
    if unknown:
        raise RegistryDefinitionRejected(
            ReasonCode.REGISTRY_DEFINITION_UNKNOWN_FIELD, ", ".join(unknown)
        )
    missing = sorted(DEFINITION_FIELDS - set(data))
    if missing:
        raise RegistryDefinitionRejected(
            ReasonCode.REGISTRY_DEFINITION_MISSING_FIELD, ", ".join(missing)
        )

    strings = {
        key: _require_str(data, key)
        for key in (
            "namespace",
            "source_key",
            "display_name",
            "collection_key",
            "domain_key",
            "source_kind",
            "data_class",
            "ai_eligibility",
            "owner_role",
            "source_reference",
        )
    }
    for value in strings.values():
        _reject_unsafe(value)

    for field in _SLUG_FIELDS:
        _require_slug(strings[field], field, policy.max_key_chars)
    if len(strings["display_name"]) > policy.max_display_name_chars:
        raise RegistryDefinitionRejected(
            ReasonCode.REGISTRY_DEFINITION_INVALID_VALUE, "display_name too long"
        )
    if not strings["display_name"].strip():
        raise RegistryDefinitionRejected(
            ReasonCode.REGISTRY_DEFINITION_INVALID_VALUE, "display_name empty"
        )

    if strings["source_kind"] not in policy.allowed_source_kinds:
        raise RegistryDefinitionRejected(
            ReasonCode.REGISTRY_DEFINITION_KIND_NOT_ALLOWED, "source_kind"
        )
    if strings["data_class"] not in policy.allowed_data_classes:
        raise RegistryDefinitionRejected(
            ReasonCode.REGISTRY_DEFINITION_DATA_CLASS_NOT_ALLOWED, "data_class"
        )
    if strings["ai_eligibility"] not in policy.allowed_ai_eligibility:
        raise RegistryDefinitionRejected(
            ReasonCode.REGISTRY_DEFINITION_AI_ELIGIBILITY_NOT_ALLOWED, "ai_eligibility"
        )

    reference = strings["source_reference"]
    if any(c not in _SAFE_REFERENCE for c in reference):
        raise RegistryDefinitionRejected(
            ReasonCode.REGISTRY_DEFINITION_INVALID_VALUE, "source_reference charset"
        )
    if not reference.startswith(SYNTHETIC_SOURCE_PREFIX) or len(reference) <= len(
        SYNTHETIC_SOURCE_PREFIX
    ):
        raise RegistryDefinitionRejected(
            ReasonCode.REGISTRY_DEFINITION_SOURCE_REF_NOT_SYNTHETIC, "source_reference"
        )

    synthetic = _require_bool(data, "synthetic_test_only")
    activation = _require_bool(data, "activation_enabled")
    content_access = _require_bool(data, "content_access_enabled")
    network = _require_bool(data, "network_enabled")

    if policy.require_synthetic_reference and not synthetic:
        raise RegistryDefinitionRejected(
            ReasonCode.REGISTRY_DEFINITION_NOT_SYNTHETIC, "synthetic_test_only"
        )
    if activation:
        raise RegistryDefinitionRejected(
            ReasonCode.REGISTRY_DEFINITION_ACTIVATION_REQUESTED, "activation_enabled"
        )
    if content_access:
        raise RegistryDefinitionRejected(
            ReasonCode.REGISTRY_DEFINITION_CONTENT_ACCESS_REQUESTED,
            "content_access_enabled",
        )
    if network:
        raise RegistryDefinitionRejected(
            ReasonCode.REGISTRY_DEFINITION_NETWORK_REQUESTED, "network_enabled"
        )

    canonical = {
        "schema_version": raw_version,
        **strings,
        "synthetic_test_only": True,
        "activation_enabled": False,
        "content_access_enabled": False,
        "network_enabled": False,
    }
    definition_sha256 = hashlib.sha256(
        json.dumps(canonical, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()

    return SourceDefinition(
        schema_version=raw_version,
        namespace=strings["namespace"],
        source_key=strings["source_key"],
        display_name=strings["display_name"],
        collection_key=strings["collection_key"],
        domain_key=strings["domain_key"],
        source_kind=strings["source_kind"],
        data_class=strings["data_class"],
        ai_eligibility=strings["ai_eligibility"],
        owner_role=strings["owner_role"],
        source_reference=reference,
        synthetic_test_only=True,
        activation_enabled=False,
        content_access_enabled=False,
        network_enabled=False,
        definition_sha256=definition_sha256,
    )


def derive_source_id(namespace: str, source_key: str) -> str:
    """Leitet die deterministische Source ID aus der logischen Identität ab.

    Die Identität besteht ausschließlich aus Identitätsschema-Version,
    ``namespace`` und ``source_key`` — kein Display Name, kein Pfad, kein Inhalt.
    """
    material = f"{IDENTITY_SCHEMA_VERSION}\n{namespace}\n{source_key}"
    digest = hashlib.sha256(material.encode("utf-8")).hexdigest()
    return f"src-{digest[:24]}"


# -- Operationen ----------------------------------------------------------


def register(
    *,
    definition_path: Path,
    policy: RegistryPolicy,
    storage: RegistryStorage,
    synthetic_confirmed: bool,
    clock: Clock = default_clock,
) -> RegistryRecord:
    """Registriert eine synthetische Definition als deaktivierten Record.

    Raises:
        RegistryDefinitionRejected: Synthetic-Grenze verletzt oder Definition
            ungültig.
        RegistryStorageError: Bei Konflikt oder Root-Verstoß.
    """
    if not synthetic_confirmed:
        raise RegistryDefinitionRejected(
            ReasonCode.REGISTRY_SYNTHETIC_CONFIRMATION_MISSING,
            "synthetic-test-only confirmation is required",
        )
    definition = load_definition(definition_path, policy)
    source_id = derive_source_id(definition.namespace, definition.source_key)
    record = RegistryRecord(
        record_schema_version=RECORD_SCHEMA_VERSION,
        source_id=source_id,
        namespace=definition.namespace,
        source_key=definition.source_key,
        display_name=definition.display_name,
        collection_key=definition.collection_key,
        domain_key=definition.domain_key,
        source_kind=definition.source_kind,
        data_class=definition.data_class,
        ai_eligibility=definition.ai_eligibility,
        owner_role=definition.owner_role,
        source_reference=definition.source_reference,
        definition_sha256=definition.definition_sha256,
        policy_sha256=policy.policy_sha256,
        lifecycle_state=LifecycleState.REGISTERED_DISABLED,
        registered_at=_utc_iso(clock()),
    )
    stored = storage.write_record(record)
    rebuild_catalog(storage, clock=clock)
    return stored


def retire(
    *,
    storage: RegistryStorage,
    source_id: str,
    synthetic_confirmed: bool,
    clock: Clock = default_clock,
) -> RetireOutcome:
    """Legt eine synthetische Registry-Identität append-only still.

    Idempotent: ein zweites Retirement erzeugt kein neues Event.

    Raises:
        RegistryDefinitionRejected: Fehlende Synthetic-Bestätigung.
        RegistryNotFound: Unbekannte Source ID.
        RegistryStorageError: Bei Konflikt oder Root-Verstoß.
    """
    if not synthetic_confirmed:
        raise RegistryDefinitionRejected(
            ReasonCode.REGISTRY_SYNTHETIC_CONFIRMATION_MISSING,
            "synthetic-test-only confirmation is required",
        )
    if not storage.record_exists(source_id):
        raise RegistryNotFound(ReasonCode.REGISTRY_RECORD_NOT_FOUND, "record")

    record = storage.load_record(source_id)
    existing_events = storage.load_events(source_id)
    if existing_events:
        # bereits stillgelegt — idempotent, kein neues Event.
        return RetireOutcome(
            record=record, event=None, lifecycle_state=LifecycleState.RETIRED
        )

    event_id = _derive_event_id(source_id)
    event = RetirementEvent(
        event_schema_version=EVENT_SCHEMA_VERSION,
        event_id=event_id,
        source_id=source_id,
        event_type=EventType.RETIRED,
        reason_code=RETIREMENT_REASON_CODE,
        occurred_at=_utc_iso(clock()),
        previous_state=LifecycleState.REGISTERED_DISABLED,
        resulting_state=LifecycleState.RETIRED,
    )
    stored_event = storage.append_event(event)
    rebuild_catalog(storage, clock=clock)
    return RetireOutcome(
        record=record, event=stored_event, lifecycle_state=LifecycleState.RETIRED
    )


def inspect(
    storage: RegistryStorage, source_id: str
) -> tuple[RegistryRecord, LifecycleState]:
    """Lädt einen Record und den wirksamen Lifecycle-Zustand.

    Raises:
        RegistryNotFound: Unbekannte Source ID.
        RegistryStorageError: Ungültiger Record.
    """
    if not storage.record_exists(source_id):
        raise RegistryNotFound(ReasonCode.REGISTRY_RECORD_NOT_FOUND, "record")
    record = storage.load_record(source_id)
    has_retirement = len(storage.load_events(source_id)) > 0
    return record, effective_state(record.lifecycle_state, has_retirement)


def rebuild_catalog(storage: RegistryStorage, *, clock: Clock = default_clock) -> None:
    """Baut den Katalog neu und ersetzt ihn atomar."""
    catalog = build_catalog(storage, clock=clock)
    payload = (
        json.dumps(catalog.to_dict(), sort_keys=True, ensure_ascii=False, indent=2)
        + "\n"
    ).encode("utf-8")
    storage.write_catalog(payload)


# -- interne Helfer -------------------------------------------------------


def _require_str(data: dict[str, Any], key: str) -> str:
    value = data[key]
    if not isinstance(value, str):
        raise RegistryDefinitionRejected(
            ReasonCode.REGISTRY_DEFINITION_INVALID_VALUE, f"{key} must be a string"
        )
    return value


def _require_bool(data: dict[str, Any], key: str) -> bool:
    value = data[key]
    if not isinstance(value, bool):
        raise RegistryDefinitionRejected(
            ReasonCode.REGISTRY_DEFINITION_INVALID_VALUE, f"{key} must be a boolean"
        )
    return value


def _reject_unsafe(value: str) -> None:
    """Weist Pfadseparatoren, ``..`` und URL-Indikatoren fail-closed ab."""
    if "/" in value or "\\" in value:
        raise RegistryDefinitionRejected(
            ReasonCode.REGISTRY_DEFINITION_PATH_SEPARATOR, "path separator"
        )
    if ".." in value:
        raise RegistryDefinitionRejected(
            ReasonCode.REGISTRY_DEFINITION_DOTDOT, "dotdot"
        )
    lowered = value.lower()
    if any(marker in lowered for marker in _URL_MARKERS):
        raise RegistryDefinitionRejected(
            ReasonCode.REGISTRY_DEFINITION_URL_INDICATOR, "url indicator"
        )
    for char in value:
        if ord(char) < 0x20:
            raise RegistryDefinitionRejected(
                ReasonCode.REGISTRY_DEFINITION_INVALID_VALUE, "control character"
            )


def _require_slug(value: str, field: str, max_chars: int) -> None:
    if len(value) > max_chars:
        raise RegistryDefinitionRejected(
            ReasonCode.REGISTRY_DEFINITION_INVALID_VALUE, f"{field} too long"
        )
    if not _SLUG.match(value):
        raise RegistryDefinitionRejected(
            ReasonCode.REGISTRY_DEFINITION_INVALID_SLUG, field
        )


def _derive_event_id(source_id: str) -> str:
    """Leitet eine deterministische Event-ID aus nicht geheimen Eventdaten ab.

    ``occurred_at`` fließt **nicht** ein, damit ein idempotentes Retirement
    dieselbe Event-ID ergibt.
    """
    material = (
        f"{EVENT_SCHEMA_VERSION}\n{source_id}\n{EventType.RETIRED.value}\n"
        f"{RETIREMENT_REASON_CODE}\n{LifecycleState.REGISTERED_DISABLED.value}\n"
        f"{LifecycleState.RETIRED.value}"
    )
    digest = hashlib.sha256(material.encode("utf-8")).hexdigest()
    return f"evt-{digest[:24]}"


def _utc_iso(moment: datetime) -> str:
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=UTC)
    return moment.astimezone(UTC).isoformat().replace("+00:00", "Z")
