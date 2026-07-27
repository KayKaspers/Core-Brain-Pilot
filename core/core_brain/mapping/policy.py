"""Strikte, fail-closed Validierung der Mapping-Validierungspolicy (CBP-WP-015).

Grundsatz **fail-closed**: unbekanntes Feld, unbekannte Schema-Version,
fehlendes Feld, falsche Feldzahlen oder eine gelockerte Sicherheitsgrenze
blockieren. **Environment und CLI überschreiben keine Sicherheitswerte.**
Dieses Modul liest weder Environment noch CLI.

Der Import dieses Moduls hat keine Nebenwirkungen.
"""

from __future__ import annotations

import hashlib
import tomllib
from pathlib import Path
from typing import Any, Final

from ..errors import MappingPolicyError, ReasonCode
from .models import (
    CONTRACT_FIELD_COUNT,
    MAPPING_SCHEMA_VERSION,
    OPTIONAL_FIELD_COUNT,
    POLICY_SCHEMA_VERSION,
    REQUIRED_FIELD_COUNT,
    MappingPolicy,
)

__all__ = ["REQUIRED_POLICY_FIELDS", "load_policy", "parse_policy_mapping"]

_STR_FIELDS: Final[frozenset[str]] = frozenset(
    {"required_mapping_schema_version", "accepted_document_profile"}
)
_INT_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "max_draft_bytes",
        "canonical_contract_field_count",
        "required_field_count",
        "optional_field_count",
    }
)
_REQUIRE_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "require_synthetic_test_only",
        "require_registry_binding",
        "require_registered_disabled",
        "require_single_boundary",
        "require_collection_exact_match",
        "require_data_class_exact_match",
    }
)
_ALLOW_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "allow_activation",
        "allow_persistence",
        "allow_registry_write",
        "allow_network",
    }
)
_BOOL_FIELDS: Final[frozenset[str]] = _REQUIRE_FIELDS | _ALLOW_FIELDS
REQUIRED_POLICY_FIELDS: Final[frozenset[str]] = (
    frozenset({"schema_version"}) | _STR_FIELDS | _INT_FIELDS | _BOOL_FIELDS
)
_ACCEPTED_PROFILE: Final[str] = "canonical-json-yaml-subset"
_MAX_DRAFT_CEILING: Final[int] = 1024 * 1024


def _require_bool(data: dict[str, Any], key: str) -> bool:
    value = data[key]
    if not isinstance(value, bool):
        raise MappingPolicyError(
            ReasonCode.MAPPING_POLICY_INVALID_VALUE, f"{key} must be a boolean"
        )
    return value


def parse_policy_mapping(data: dict[str, Any], policy_sha256: str) -> MappingPolicy:
    """Validiert ein geparstes Policy-Mapping fail-closed.

    Raises:
        MappingPolicyError: Bei jedem Verstoß.
    """
    raw_version = data.get("schema_version")
    if raw_version is None:
        raise MappingPolicyError(
            ReasonCode.MAPPING_POLICY_MISSING_FIELD, "schema_version"
        )
    if not isinstance(raw_version, str) or raw_version != POLICY_SCHEMA_VERSION:
        raise MappingPolicyError(
            ReasonCode.MAPPING_POLICY_SCHEMA_UNSUPPORTED,
            f"expected {POLICY_SCHEMA_VERSION}",
        )

    unknown = sorted(set(data) - REQUIRED_POLICY_FIELDS)
    if unknown:
        raise MappingPolicyError(
            ReasonCode.MAPPING_POLICY_UNKNOWN_FIELD, ", ".join(unknown)
        )
    missing = sorted(REQUIRED_POLICY_FIELDS - set(data))
    if missing:
        raise MappingPolicyError(
            ReasonCode.MAPPING_POLICY_MISSING_FIELD, ", ".join(missing)
        )

    max_draft_bytes = data["max_draft_bytes"]
    if not isinstance(max_draft_bytes, int) or isinstance(max_draft_bytes, bool):
        raise MappingPolicyError(
            ReasonCode.MAPPING_POLICY_INVALID_VALUE, "max_draft_bytes must be int"
        )
    if not (0 < max_draft_bytes <= _MAX_DRAFT_CEILING):
        raise MappingPolicyError(
            ReasonCode.MAPPING_POLICY_INVALID_VALUE, "max_draft_bytes out of range"
        )

    required_mapping_schema_version = data["required_mapping_schema_version"]
    if (
        not isinstance(required_mapping_schema_version, str)
        or required_mapping_schema_version != MAPPING_SCHEMA_VERSION
    ):
        raise MappingPolicyError(
            ReasonCode.MAPPING_POLICY_INVALID_VALUE,
            "required_mapping_schema_version",
        )

    accepted_document_profile = data["accepted_document_profile"]
    if accepted_document_profile != _ACCEPTED_PROFILE:
        raise MappingPolicyError(
            ReasonCode.MAPPING_POLICY_INVALID_VALUE, "accepted_document_profile"
        )

    # Die Feldzahlen müssen exakt dem angenommenen Vertrag entsprechen.
    counts = {
        "canonical_contract_field_count": CONTRACT_FIELD_COUNT,
        "required_field_count": REQUIRED_FIELD_COUNT,
        "optional_field_count": OPTIONAL_FIELD_COUNT,
    }
    for key, expected in counts.items():
        value = data[key]
        if not isinstance(value, int) or isinstance(value, bool) or value != expected:
            raise MappingPolicyError(
                ReasonCode.MAPPING_POLICY_FIELD_COUNT_INVALID, key
            )

    bools = {key: _require_bool(data, key) for key in sorted(_BOOL_FIELDS)}

    # Fail-closed: jede require_*-Grenze muss gesetzt bleiben. Eine Lockerung
    # (false) blockiert — sie ist eine gelockerte Sicherheitsgrenze.
    for key in sorted(_REQUIRE_FIELDS):
        if not bools[key]:
            raise MappingPolicyError(
                ReasonCode.MAPPING_POLICY_INVALID_VALUE, f"{key} must be true"
            )

    if bools["allow_activation"]:
        raise MappingPolicyError(
            ReasonCode.MAPPING_POLICY_ACTIVATION_ENABLED, "allow_activation"
        )
    if bools["allow_persistence"]:
        raise MappingPolicyError(
            ReasonCode.MAPPING_POLICY_PERSISTENCE_ENABLED, "allow_persistence"
        )
    if bools["allow_registry_write"]:
        raise MappingPolicyError(
            ReasonCode.MAPPING_POLICY_REGISTRY_WRITE_ENABLED, "allow_registry_write"
        )
    if bools["allow_network"]:
        raise MappingPolicyError(
            ReasonCode.MAPPING_POLICY_NETWORK_ENABLED, "allow_network"
        )

    return MappingPolicy(
        schema_version=raw_version,
        max_draft_bytes=max_draft_bytes,
        required_mapping_schema_version=required_mapping_schema_version,
        accepted_document_profile=accepted_document_profile,
        canonical_contract_field_count=CONTRACT_FIELD_COUNT,
        required_field_count=REQUIRED_FIELD_COUNT,
        optional_field_count=OPTIONAL_FIELD_COUNT,
        require_synthetic_test_only=bools["require_synthetic_test_only"],
        require_registry_binding=bools["require_registry_binding"],
        require_registered_disabled=bools["require_registered_disabled"],
        require_single_boundary=bools["require_single_boundary"],
        require_collection_exact_match=bools["require_collection_exact_match"],
        require_data_class_exact_match=bools["require_data_class_exact_match"],
        allow_activation=False,
        allow_persistence=False,
        allow_registry_write=False,
        allow_network=False,
        policy_sha256=policy_sha256,
    )


def load_policy(path: Path) -> MappingPolicy:
    """Lädt und validiert eine Mapping-Validierungspolicy.

    Raises:
        MappingPolicyError: Datei fehlt, nicht lesbar, nicht parsebar oder
            schemawidrig.
    """
    if not path.is_file():
        raise MappingPolicyError(ReasonCode.MAPPING_POLICY_FILE_MISSING, path.name)
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise MappingPolicyError(
            ReasonCode.MAPPING_POLICY_NOT_READABLE, path.name
        ) from exc
    policy_sha256 = hashlib.sha256(raw).hexdigest()
    try:
        data = tomllib.loads(raw.decode("utf-8"))
    except (tomllib.TOMLDecodeError, UnicodeDecodeError) as exc:
        raise MappingPolicyError(
            ReasonCode.MAPPING_POLICY_PARSE_ERROR, path.name
        ) from exc
    return parse_policy_mapping(data, policy_sha256)
