"""Strikte, fail-closed Validierung der Source-Registry-Policy (CBP-WP-014).

Grundsatz **fail-closed**: unbekanntes Feld, unbekannte Schema-Version,
fehlendes Feld, unzulässiger Maximalwert, leere Allowlist, ``allow_activation``,
``allow_content_access``, ``allow_network``, ``allow_updates`` oder
``allow_deletion`` gleich ``true`` sowie ``allow_retirement`` gleich ``false``
blockieren die Validierung.

**Environment-Variablen und CLI-Argumente überschreiben keine Policy-Werte.**
Dieses Modul liest weder Environment noch CLI. Es gibt **keine** frei
konfigurierbaren regulären Ausdrücke.

Der Import dieses Moduls hat keine Nebenwirkungen.
"""

from __future__ import annotations

import hashlib
import tomllib
from pathlib import Path
from typing import Any, Final

from ..errors import RegistryPolicyError, ReasonCode
from .models import POLICY_SCHEMA_VERSION, RegistryPolicy

__all__ = ["REQUIRED_POLICY_FIELDS", "load_policy", "parse_policy_mapping"]

_LIST_FIELDS: Final[frozenset[str]] = frozenset(
    {"allowed_source_kinds", "allowed_data_classes", "allowed_ai_eligibility"}
)
_INT_FIELDS: Final[frozenset[str]] = frozenset(
    {"max_definition_bytes", "max_key_chars", "max_display_name_chars"}
)
_BOOL_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "require_synthetic_reference",
        "allow_activation",
        "allow_content_access",
        "allow_network",
        "allow_updates",
        "allow_deletion",
        "allow_retirement",
    }
)

REQUIRED_POLICY_FIELDS: Final[frozenset[str]] = (
    frozenset({"schema_version"}) | _LIST_FIELDS | _INT_FIELDS | _BOOL_FIELDS
)
"""Alle 14 Pflichtfelder. Es gibt keine optionalen Felder."""

# Konservative Obergrenzen.
_CEILINGS: Final[dict[str, int]] = {
    "max_definition_bytes": 1024 * 1024,
    "max_key_chars": 256,
    "max_display_name_chars": 512,
}


def _require_bool(data: dict[str, Any], key: str) -> bool:
    value = data[key]
    if not isinstance(value, bool):
        raise RegistryPolicyError(
            ReasonCode.REGISTRY_POLICY_INVALID_VALUE, f"{key} must be a boolean"
        )
    return value


def _require_positive_int(data: dict[str, Any], key: str) -> int:
    value = data[key]
    if not isinstance(value, int) or isinstance(value, bool):
        raise RegistryPolicyError(
            ReasonCode.REGISTRY_POLICY_INVALID_VALUE, f"{key} must be an integer"
        )
    if value <= 0:
        raise RegistryPolicyError(
            ReasonCode.REGISTRY_POLICY_INVALID_VALUE, f"{key} must be positive"
        )
    if value > _CEILINGS[key]:
        raise RegistryPolicyError(
            ReasonCode.REGISTRY_POLICY_INVALID_VALUE, f"{key} exceeds the ceiling"
        )
    return value


def _require_slug_list(data: dict[str, Any], key: str) -> tuple[str, ...]:
    value = data[key]
    if not isinstance(value, list) or not value:
        raise RegistryPolicyError(
            ReasonCode.REGISTRY_POLICY_INVALID_VALUE,
            f"{key} must be a non-empty list",
        )
    out: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise RegistryPolicyError(
                ReasonCode.REGISTRY_POLICY_INVALID_VALUE,
                f"{key} entries must be non-empty strings",
            )
        out.append(item)
    return tuple(out)


def parse_policy_mapping(data: dict[str, Any], policy_sha256: str) -> RegistryPolicy:
    """Validiert ein bereits geparstes Mapping und baut eine Policy.

    Raises:
        RegistryPolicyError: Bei jedem Verstoß. Prüfreihenfolge stabil:
            Schema-Version, unbekannte Felder, fehlende Felder, Werte.
    """
    raw_version = data.get("schema_version")
    if raw_version is None:
        raise RegistryPolicyError(
            ReasonCode.REGISTRY_POLICY_MISSING_FIELD, "schema_version"
        )
    if not isinstance(raw_version, str) or raw_version != POLICY_SCHEMA_VERSION:
        raise RegistryPolicyError(
            ReasonCode.REGISTRY_POLICY_SCHEMA_UNSUPPORTED,
            f"expected {POLICY_SCHEMA_VERSION}",
        )

    unknown = sorted(set(data) - REQUIRED_POLICY_FIELDS)
    if unknown:
        raise RegistryPolicyError(
            ReasonCode.REGISTRY_POLICY_UNKNOWN_FIELD, ", ".join(unknown)
        )

    missing = sorted(REQUIRED_POLICY_FIELDS - set(data))
    if missing:
        raise RegistryPolicyError(
            ReasonCode.REGISTRY_POLICY_MISSING_FIELD, ", ".join(missing)
        )

    max_definition_bytes = _require_positive_int(data, "max_definition_bytes")
    max_key_chars = _require_positive_int(data, "max_key_chars")
    max_display_name_chars = _require_positive_int(data, "max_display_name_chars")

    kinds = _require_slug_list(data, "allowed_source_kinds")
    data_classes = _require_slug_list(data, "allowed_data_classes")
    ai_eligibility = _require_slug_list(data, "allowed_ai_eligibility")

    bools = {key: _require_bool(data, key) for key in sorted(_BOOL_FIELDS)}

    if bools["allow_activation"]:
        raise RegistryPolicyError(
            ReasonCode.REGISTRY_POLICY_ACTIVATION_ENABLED, "allow_activation"
        )
    if bools["allow_content_access"]:
        raise RegistryPolicyError(
            ReasonCode.REGISTRY_POLICY_CONTENT_ACCESS_ENABLED, "allow_content_access"
        )
    if bools["allow_network"]:
        raise RegistryPolicyError(
            ReasonCode.REGISTRY_POLICY_NETWORK_ENABLED, "allow_network"
        )
    if bools["allow_updates"]:
        raise RegistryPolicyError(
            ReasonCode.REGISTRY_POLICY_UPDATES_ENABLED, "allow_updates"
        )
    if bools["allow_deletion"]:
        raise RegistryPolicyError(
            ReasonCode.REGISTRY_POLICY_DELETION_ENABLED, "allow_deletion"
        )
    if not bools["allow_retirement"]:
        raise RegistryPolicyError(
            ReasonCode.REGISTRY_POLICY_RETIREMENT_DISABLED, "allow_retirement"
        )

    return RegistryPolicy(
        schema_version=raw_version,
        max_definition_bytes=max_definition_bytes,
        max_key_chars=max_key_chars,
        max_display_name_chars=max_display_name_chars,
        allowed_source_kinds=kinds,
        allowed_data_classes=data_classes,
        allowed_ai_eligibility=ai_eligibility,
        require_synthetic_reference=bools["require_synthetic_reference"],
        allow_activation=False,
        allow_content_access=False,
        allow_network=False,
        allow_updates=False,
        allow_deletion=False,
        allow_retirement=True,
        policy_sha256=policy_sha256,
    )


def load_policy(path: Path) -> RegistryPolicy:
    """Lädt und validiert eine Registry-Policy.

    Raises:
        RegistryPolicyError: Datei fehlt, nicht lesbar, nicht parsebar oder
            schemawidrig.
    """
    if not path.is_file():
        raise RegistryPolicyError(ReasonCode.REGISTRY_POLICY_FILE_MISSING, path.name)

    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise RegistryPolicyError(
            ReasonCode.REGISTRY_POLICY_NOT_READABLE, path.name
        ) from exc

    policy_sha256 = hashlib.sha256(raw).hexdigest()

    try:
        data = tomllib.loads(raw.decode("utf-8"))
    except (tomllib.TOMLDecodeError, UnicodeDecodeError) as exc:
        raise RegistryPolicyError(
            ReasonCode.REGISTRY_POLICY_PARSE_ERROR, path.name
        ) from exc

    return parse_policy_mapping(data, policy_sha256)
