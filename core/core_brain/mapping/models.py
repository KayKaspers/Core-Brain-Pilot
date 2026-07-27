"""Datenmodelle des Source-Mapping-Draft-Validators (CBP-WP-015).

Der Validator wendet den **angenommenen 31-Feld-Vertrag** (ADR-0008) an. Er
fügt **kein** Feld hinzu, entfernt keines, benennt keines um und deutet keine
Semantik um. Report und Ausgaben enthalten **niemals** einen Pfad, eine URL,
Source-Inhalt, eine Source Reference oder einen Registry-Root.

Der Import dieses Moduls hat keine Nebenwirkungen.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Final

__all__ = [
    "POLICY_SCHEMA_VERSION",
    "MAPPING_SCHEMA_VERSION",
    "REPORT_SCHEMA_VERSION",
    "IMPLEMENTATION_VERSION",
    "CONTRACT_FIELD_COUNT",
    "REQUIRED_FIELD_COUNT",
    "OPTIONAL_FIELD_COUNT",
    "MAPPING_FIELDS",
    "REQUIRED_MAPPING_FIELDS",
    "OPTIONAL_MAPPING_FIELDS",
    "SLOT_IDS",
    "SLOT_BOUNDARY",
    "BOUNDARY_LOCATION_TYPES",
    "DATA_CLASSES",
    "AI_TRANSFER_POLICIES",
    "LOCATION_PLACEHOLDER_PREFIX",
    "MappingReasonCode",
    "ValidationStatus",
    "ValidationReport",
    "MappingPolicy",
]

POLICY_SCHEMA_VERSION = "1.0"
MAPPING_SCHEMA_VERSION = "1.0"
REPORT_SCHEMA_VERSION = "1.0"
IMPLEMENTATION_VERSION = "0.1.0.dev0"

CONTRACT_FIELD_COUNT = 31
REQUIRED_FIELD_COUNT = 29
OPTIONAL_FIELD_COUNT = 2

# Die 31 kanonischen Felder in kanonischer Reihenfolge (SCHEMA §1–§31).
MAPPING_FIELDS: Final[tuple[str, ...]] = (
    "schema_version",
    "mapping_id",
    "slot_id",
    "mapping_name",
    "source_boundary_type",
    "deployment_profile",
    "operator_reference",
    "location_reference",
    "location_reference_type",
    "collection",
    "project",
    "enabled",
    "read_only",
    "allowed_subpaths",
    "excluded_subpaths",
    "follow_symlinks",
    "data_class",
    "ai_transfer_policy",
    "local_search_policy",
    "indexing_policy",
    "mobile_visibility",
    "revision_strategy",
    "deletion_behavior",
    "verification_status",
    "approval_status",
    "approved_by",
    "approved_at",
    "mapping_revision",
    "previous_revision",
    "credential_reference",
    "notes",
)
OPTIONAL_MAPPING_FIELDS: Final[frozenset[str]] = frozenset(
    {"credential_reference", "notes"}
)
REQUIRED_MAPPING_FIELDS: Final[frozenset[str]] = (
    frozenset(MAPPING_FIELDS) - OPTIONAL_MAPPING_FIELDS
)

# Kanonische Enum-Werte und Cross-Field-Regeln (SCHEMA/VALIDATION).
SLOT_IDS: Final[frozenset[str]] = frozenset({"PS-02", "PS-03", "PS-04"})
SLOT_BOUNDARY: Final[dict[str, str]] = {
    "PS-02": "markdown-root",
    "PS-03": "git-repository",
    "PS-04": "handoff-root",
}
BOUNDARY_LOCATION_TYPES: Final[dict[str, frozenset[str]]] = {
    "markdown-root": frozenset({"local-directory", "mounted-volume"}),
    "handoff-root": frozenset({"local-directory", "mounted-volume"}),
    "git-repository": frozenset({"git-remote", "git-local-clone"}),
}
DATA_CLASSES: Final[frozenset[str]] = frozenset(
    {"public", "internal", "confidential", "excluded-from-ai", "unknown"}
)
AI_TRANSFER_POLICIES: Final[frozenset[str]] = frozenset(
    {"allowed", "restricted", "forbidden"}
)
DEPLOYMENT_PROFILES: Final[frozenset[str]] = frozenset({"A", "B", "C", "D", "E"})
REVISION_STRATEGIES: Final[dict[str, frozenset[str]]] = {
    "PS-02": frozenset({"content-hash"}),
    "PS-03": frozenset({"git-commit"}),
    "PS-04": frozenset({"content-hash", "handoff-revision"}),
}

# Kanonisches synthetisches V7-Platzhaltermarkerformat
# (PILOT_SOURCE_MAPPING_EXAMPLES.md: „Alle Platzhalter sind
# `synthetic-placeholder-*`"). Das MVP verlangt die URL- und pfadfreie Form.
LOCATION_PLACEHOLDER_PREFIX: Final[str] = "synthetic-placeholder-"


class MappingReasonCode(StrEnum):
    """Stabile, global eindeutige Validierungsgründe im ``MAP-``-Namensraum."""

    SYNTHETIC_CONFIRMATION_MISSING = "MAP-SYNTHETIC-CONFIRMATION-MISSING"
    # Parser / Dokumentprofil.
    DRAFT_FILE_MISSING = "MAP-DRAFT-FILE-MISSING"
    DRAFT_TOO_LARGE = "MAP-DRAFT-TOO-LARGE"
    PARSE_BOM = "MAP-PARSE-BOM"
    PARSE_UTF8 = "MAP-PARSE-UTF8"
    PARSE_JSON = "MAP-PARSE-JSON"
    PARSE_NOT_OBJECT = "MAP-PARSE-NOT-OBJECT"
    PARSE_DUPLICATE_KEY = "MAP-PARSE-DUPLICATE-KEY"
    PARSE_NAN = "MAP-PARSE-NAN"
    PARSE_INFINITY = "MAP-PARSE-INFINITY"
    # Vertrag.
    SCHEMA_VERSION = "MAP-SCHEMA-VERSION"
    UNKNOWN_FIELD = "MAP-UNKNOWN-FIELD"
    MISSING_FIELD = "MAP-MISSING-FIELD"
    FIELD_TYPE = "MAP-FIELD-TYPE"
    ENUM_VALUE = "MAP-ENUM-VALUE"
    # Feldsicherheit.
    PATH_INDICATOR = "MAP-PATH-INDICATOR"
    URL_INDICATOR = "MAP-URL-INDICATOR"
    DOTDOT = "MAP-DOTDOT"
    SECRET_INDICATOR = "MAP-SECRET-INDICATOR"
    # Slot / Boundary.
    SLOT_INVALID = "MAP-SLOT-INVALID"
    BOUNDARY_SLOT_MISMATCH = "MAP-BOUNDARY-SLOT-MISMATCH"
    LOCATION_TYPE_MISMATCH = "MAP-LOCATION-TYPE-MISMATCH"
    LOCATION_NOT_SYNTHETIC = "MAP-LOCATION-NOT-SYNTHETIC"
    REVISION_STRATEGY_MISMATCH = "MAP-REVISION-STRATEGY-MISMATCH"
    # Synthetischer Draft-Zustand (restriktivste Vertragswerte).
    ENABLED_TRUE = "MAP-ENABLED-TRUE"
    READ_ONLY_FALSE = "MAP-READ-ONLY-FALSE"
    FOLLOW_SYMLINKS_TRUE = "MAP-FOLLOW-SYMLINKS-TRUE"
    ALLOWED_SUBPATHS_NONEMPTY = "MAP-ALLOWED-SUBPATHS-NONEMPTY"
    EXCLUDED_SUBPATHS_NONEMPTY = "MAP-EXCLUDED-SUBPATHS-NONEMPTY"
    APPROVAL_NOT_DRAFT = "MAP-APPROVAL-NOT-DRAFT"
    VERIFICATION_NOT_DRAFT = "MAP-VERIFICATION-NOT-DRAFT"
    AI_TRANSFER_NOT_FORBIDDEN = "MAP-AI-TRANSFER-NOT-FORBIDDEN"
    INDEXING_NOT_NONE = "MAP-INDEXING-NOT-NONE"
    LOCAL_SEARCH_NOT_FORBIDDEN = "MAP-LOCAL-SEARCH-NOT-FORBIDDEN"
    MOBILE_NOT_FORBIDDEN = "MAP-MOBILE-NOT-FORBIDDEN"
    APPROVED_BY_NOT_NULL = "MAP-APPROVED-BY-NOT-NULL"
    APPROVED_AT_NOT_NULL = "MAP-APPROVED-AT-NOT-NULL"
    CREDENTIAL_REFERENCE_VALUE = "MAP-CREDENTIAL-REFERENCE-VALUE"
    DATA_CLASS_AI_INCOMPATIBLE = "MAP-DATA-CLASS-AI-INCOMPATIBLE"
    MAPPING_ID_INVALID = "MAP-MAPPING-ID-INVALID"
    # Registry-Bindung (read-only).
    SOURCE_ID_INVALID = "MAP-SOURCE-ID-INVALID"
    REGISTRY_NOT_FOUND = "MAP-REGISTRY-NOT-FOUND"
    REGISTRY_RECORD_INVALID = "MAP-REGISTRY-RECORD-INVALID"
    REGISTRY_RETIRED = "MAP-REGISTRY-RETIRED"
    SOURCE_REF_NOT_SYNTHETIC = "MAP-SOURCE-REF-NOT-SYNTHETIC"
    COLLECTION_MISMATCH = "MAP-COLLECTION-MISMATCH"
    DATA_CLASS_MISMATCH = "MAP-DATA-CLASS-MISMATCH"


class ValidationStatus(StrEnum):
    """Die einzigen zwei Ergebniszustände. Keiner bedeutet Freigabe."""

    VALID_DRAFT = "VALID_DRAFT"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True, slots=True)
class MappingPolicy:
    """Validierte, fail-closed Validierungspolicy (18 Felder)."""

    schema_version: str
    max_draft_bytes: int
    required_mapping_schema_version: str
    accepted_document_profile: str
    canonical_contract_field_count: int
    required_field_count: int
    optional_field_count: int
    require_synthetic_test_only: bool
    require_registry_binding: bool
    require_registered_disabled: bool
    require_single_boundary: bool
    require_collection_exact_match: bool
    require_data_class_exact_match: bool
    allow_activation: bool
    allow_persistence: bool
    allow_registry_write: bool
    allow_network: bool
    policy_sha256: str

    def to_dict(self) -> dict[str, object]:
        """Gibt eine deterministische, JSON-taugliche Darstellung zurück."""
        return {
            "schema_version": self.schema_version,
            "max_draft_bytes": self.max_draft_bytes,
            "required_mapping_schema_version": self.required_mapping_schema_version,
            "accepted_document_profile": self.accepted_document_profile,
            "canonical_contract_field_count": self.canonical_contract_field_count,
            "required_field_count": self.required_field_count,
            "optional_field_count": self.optional_field_count,
            "require_synthetic_test_only": self.require_synthetic_test_only,
            "require_registry_binding": self.require_registry_binding,
            "require_registered_disabled": self.require_registered_disabled,
            "require_single_boundary": self.require_single_boundary,
            "require_collection_exact_match": self.require_collection_exact_match,
            "require_data_class_exact_match": self.require_data_class_exact_match,
            "allow_activation": self.allow_activation,
            "allow_persistence": self.allow_persistence,
            "allow_registry_write": self.allow_registry_write,
            "allow_network": self.allow_network,
            "policy_sha256": self.policy_sha256,
        }


@dataclass(frozen=True, slots=True)
class ValidationReport:
    """Nicht persistierter, deterministischer, minimierter Validierungsreport.

    Enthält **keine** Pfade, URLs, Source-Inhalte, `source_reference`, keinen
    Registry-Root und keine Snippets. ``VALID_DRAFT`` bedeutet **keine**
    Freigabe und **keine** Aktivierung.
    """

    report_schema_version: str
    mapping_id: str | None
    source_id: str
    draft_sha256: str
    policy_sha256: str
    mapping_schema_version: str
    validation_status: ValidationStatus
    reason_codes: tuple[str, ...]
    reason_count: int
    canonical_contract_field_count: int
    required_field_count: int
    present_field_count: int
    boundary_count: int
    implementation_version: str = IMPLEMENTATION_VERSION

    def to_dict(self) -> dict[str, object]:
        """Gibt die kanonische, minimierte JSON-Darstellung zurück."""
        return {
            "report_schema_version": self.report_schema_version,
            "mapping_id": self.mapping_id,
            "source_id": self.source_id,
            "draft_sha256": self.draft_sha256,
            "policy_sha256": self.policy_sha256,
            "mapping_schema_version": self.mapping_schema_version,
            "validation_status": self.validation_status.value,
            "reason_codes": list(self.reason_codes),
            "reason_count": self.reason_count,
            "canonical_contract_field_count": self.canonical_contract_field_count,
            "required_field_count": self.required_field_count,
            "present_field_count": self.present_field_count,
            "boundary_count": self.boundary_count,
            "implementation_version": self.implementation_version,
        }
