"""Datenmodelle der Source Registry (CBP-WP-014).

Alle Modelle sind unveränderlich. Records, Events und Katalogeinträge enthalten
**niemals**:

- einen Source-Pfad oder Dateinamen,
- eine URL,
- Source-Inhalt,
- einen Mapping-Locator,
- einen Secret-Wert,
- personenbezogene Inhalte.

Der Import dieses Moduls hat keine Nebenwirkungen.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

__all__ = [
    "POLICY_SCHEMA_VERSION",
    "DEFINITION_SCHEMA_VERSION",
    "RECORD_SCHEMA_VERSION",
    "EVENT_SCHEMA_VERSION",
    "CATALOG_SCHEMA_VERSION",
    "IDENTITY_SCHEMA_VERSION",
    "IMPLEMENTATION_VERSION",
    "LifecycleState",
    "EventType",
    "RegistryPolicy",
    "SourceDefinition",
    "RegistryRecord",
    "RetirementEvent",
    "CatalogEntry",
    "Catalog",
    "DEFINITION_FIELDS",
    "RECORD_FIELDS",
    "EVENT_FIELDS",
]

POLICY_SCHEMA_VERSION = "1.0"
DEFINITION_SCHEMA_VERSION = "1.0"
RECORD_SCHEMA_VERSION = "1.0"
EVENT_SCHEMA_VERSION = "1.0"
CATALOG_SCHEMA_VERSION = "1.0"
IDENTITY_SCHEMA_VERSION = "1.0"
IMPLEMENTATION_VERSION = "0.1.0.dev0"


class LifecycleState(StrEnum):
    """Die einzigen zwei Registry-Zustände des MVP.

    Kein Zustand bedeutet ``approved``, ``mapped``, ``activated``,
    ``ingestible``, ``indexed`` oder ``retrievable``.
    """

    REGISTERED_DISABLED = "REGISTERED_DISABLED"
    RETIRED = "RETIRED"


class EventType(StrEnum):
    """Die einzige Lifecycle-Ereignisart des MVP."""

    RETIRED = "RETIRED"


@dataclass(frozen=True, slots=True)
class RegistryPolicy:
    """Validierte, fail-closed Registry-Policy."""

    schema_version: str
    max_definition_bytes: int
    max_key_chars: int
    max_display_name_chars: int
    allowed_source_kinds: tuple[str, ...]
    allowed_data_classes: tuple[str, ...]
    allowed_ai_eligibility: tuple[str, ...]
    require_synthetic_reference: bool
    allow_activation: bool
    allow_content_access: bool
    allow_network: bool
    allow_updates: bool
    allow_deletion: bool
    allow_retirement: bool
    policy_sha256: str

    def to_dict(self) -> dict[str, object]:
        """Gibt eine deterministische, JSON-taugliche Darstellung zurück."""
        return {
            "schema_version": self.schema_version,
            "max_definition_bytes": self.max_definition_bytes,
            "max_key_chars": self.max_key_chars,
            "max_display_name_chars": self.max_display_name_chars,
            "allowed_source_kinds": list(self.allowed_source_kinds),
            "allowed_data_classes": list(self.allowed_data_classes),
            "allowed_ai_eligibility": list(self.allowed_ai_eligibility),
            "require_synthetic_reference": self.require_synthetic_reference,
            "allow_activation": self.allow_activation,
            "allow_content_access": self.allow_content_access,
            "allow_network": self.allow_network,
            "allow_updates": self.allow_updates,
            "allow_deletion": self.allow_deletion,
            "allow_retirement": self.allow_retirement,
            "policy_sha256": self.policy_sha256,
        }


@dataclass(frozen=True, slots=True)
class SourceDefinition:
    """Validierte, synthetische Source-Definition.

    Enthält ausschließlich normalisierte Metadaten — **keinen** Pfad, keine
    URL, keinen Inhalt, keinen Mapping- oder Secret-Locator.
    """

    schema_version: str
    namespace: str
    source_key: str
    display_name: str
    collection_key: str
    domain_key: str
    source_kind: str
    data_class: str
    ai_eligibility: str
    owner_role: str
    source_reference: str
    synthetic_test_only: bool
    activation_enabled: bool
    content_access_enabled: bool
    network_enabled: bool
    definition_sha256: str


@dataclass(frozen=True, slots=True)
class RegistryRecord:
    """Unveränderlicher Registrierungsrecord. Initialzustand REGISTERED_DISABLED."""

    record_schema_version: str
    source_id: str
    namespace: str
    source_key: str
    display_name: str
    collection_key: str
    domain_key: str
    source_kind: str
    data_class: str
    ai_eligibility: str
    owner_role: str
    source_reference: str
    definition_sha256: str
    policy_sha256: str
    lifecycle_state: LifecycleState
    registered_at: str
    implementation_version: str = IMPLEMENTATION_VERSION

    def to_dict(self) -> dict[str, object]:
        """Gibt die kanonische Darstellung zurück (Serialisierung sortiert)."""
        return {
            "record_schema_version": self.record_schema_version,
            "source_id": self.source_id,
            "namespace": self.namespace,
            "source_key": self.source_key,
            "display_name": self.display_name,
            "collection_key": self.collection_key,
            "domain_key": self.domain_key,
            "source_kind": self.source_kind,
            "data_class": self.data_class,
            "ai_eligibility": self.ai_eligibility,
            "owner_role": self.owner_role,
            "source_reference": self.source_reference,
            "definition_sha256": self.definition_sha256,
            "policy_sha256": self.policy_sha256,
            "lifecycle_state": self.lifecycle_state.value,
            "registered_at": self.registered_at,
            "implementation_version": self.implementation_version,
        }


@dataclass(frozen=True, slots=True)
class RetirementEvent:
    """Unveränderliches, append-only Retirement-Event."""

    event_schema_version: str
    event_id: str
    source_id: str
    event_type: EventType
    reason_code: str
    occurred_at: str
    previous_state: LifecycleState
    resulting_state: LifecycleState
    implementation_version: str = IMPLEMENTATION_VERSION

    def to_dict(self) -> dict[str, object]:
        """Gibt die kanonische Darstellung zurück."""
        return {
            "event_schema_version": self.event_schema_version,
            "event_id": self.event_id,
            "source_id": self.source_id,
            "event_type": self.event_type.value,
            "reason_code": self.reason_code,
            "occurred_at": self.occurred_at,
            "previous_state": self.previous_state.value,
            "resulting_state": self.resulting_state.value,
            "implementation_version": self.implementation_version,
        }


@dataclass(frozen=True, slots=True, order=True)
class CatalogEntry:
    """Minimierter Katalogeintrag. Nach ``source_id`` sortierbar.

    Enthält **keine** Source Reference, keinen Pfad, keine URL, keinen Inhalt,
    keinen Definition Hash und keinen Mapping-Locator.
    """

    source_id: str
    namespace: str
    source_key: str
    display_name: str
    collection_key: str
    domain_key: str
    source_kind: str
    data_class: str
    ai_eligibility: str
    lifecycle_state: LifecycleState

    def to_dict(self) -> dict[str, object]:
        """Gibt die minimierte JSON-Darstellung zurück."""
        return {
            "source_id": self.source_id,
            "namespace": self.namespace,
            "source_key": self.source_key,
            "display_name": self.display_name,
            "collection_key": self.collection_key,
            "domain_key": self.domain_key,
            "source_kind": self.source_kind,
            "data_class": self.data_class,
            "ai_eligibility": self.ai_eligibility,
            "lifecycle_state": self.lifecycle_state.value,
        }


@dataclass(frozen=True, slots=True)
class Catalog:
    """Deterministisch abgeleiteter, minimierter Katalog."""

    catalog_schema_version: str
    generated_at: str
    record_count: int
    registered_disabled_count: int
    retired_count: int
    entries: tuple[CatalogEntry, ...]

    def to_dict(self) -> dict[str, object]:
        """Gibt die kanonische, minimierte JSON-Darstellung zurück."""
        return {
            "catalog_schema_version": self.catalog_schema_version,
            "generated_at": self.generated_at,
            "record_count": self.record_count,
            "registered_disabled_count": self.registered_disabled_count,
            "retired_count": self.retired_count,
            "entries": [e.to_dict() for e in self.entries],
        }


DEFINITION_FIELDS: frozenset[str] = frozenset(
    {
        "schema_version",
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
        "synthetic_test_only",
        "activation_enabled",
        "content_access_enabled",
        "network_enabled",
    }
)
"""Alle Pflichtfelder einer Source-Definition. Unbekannte Felder blockieren."""

RECORD_FIELDS: frozenset[str] = frozenset(
    {
        "record_schema_version",
        "source_id",
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
        "definition_sha256",
        "policy_sha256",
        "lifecycle_state",
        "registered_at",
        "implementation_version",
    }
)
"""Alle Pflichtfelder eines Records. Unbekannte Felder blockieren."""

EVENT_FIELDS: frozenset[str] = frozenset(
    {
        "event_schema_version",
        "event_id",
        "source_id",
        "event_type",
        "reason_code",
        "occurred_at",
        "previous_state",
        "resulting_state",
        "implementation_version",
    }
)
"""Alle Pflichtfelder eines Retirement-Events. Unbekannte Felder blockieren."""
