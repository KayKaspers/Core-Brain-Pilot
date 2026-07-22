"""Strikte, deterministische Konfigurationsvalidierung.

Grundsatz: **fail-closed**. Ein unbekanntes Feld, eine unbekannte
Schema-Version, ein fehlendes Pflichtfeld oder ein unzulässiger Wert
blockieren — es gibt keine Vorgabe, die eine Lücke füllt.

**Environment-Variablen und CLI-Argumente überschreiben keine
Sicherheitswerte.** Diese Datei liest bewusst weder ``os.environ`` noch
``sys.argv``.

Der Import dieses Moduls hat keine Nebenwirkungen.
"""

from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any, Final

from .errors import ConfigError, ReasonCode
from .models import (
    SCHEMA_VERSION,
    ComponentStatus,
    EgressDefault,
    GateStatus,
    RuntimeConfig,
    RuntimeMode,
)

__all__ = [
    "REQUIRED_FIELDS",
    "SECURITY_FIELDS",
    "FORBIDDEN_IDENTITY_NAMES",
    "load_config",
    "parse_config_mapping",
]

REQUIRED_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "schema_version",
        "runtime_mode",
        "control_plane_identity",
        "data_worker_identity",
        "egress_default",
        "canonical_write_allowed",
        "source_activation_enabled",
        "mapping_gate_status",
        "security_gate_status",
        "secret_provider_status",
        "evidence_writer_status",
    }
)
"""Alle Pflichtfelder. Es gibt keine optionalen Felder im Skeleton."""

SECURITY_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "egress_default",
        "canonical_write_allowed",
        "source_activation_enabled",
        "mapping_gate_status",
        "security_gate_status",
        "control_plane_identity",
        "data_worker_identity",
    }
)
"""Felder, die weder über Environment noch über CLI überschrieben werden."""

FORBIDDEN_IDENTITY_NAMES: Final[frozenset[str]] = frozenset(
    {"root", "administrator", "system"}
)
"""Identitätsnamen, die im Skeleton unzulässig sind."""


def _require_str(data: dict[str, Any], key: str) -> str:
    """Liest ein Pflichtfeld vom Typ ``str``."""
    value = data[key]
    if not isinstance(value, str):
        raise ConfigError(ReasonCode.CONFIG_TYPE_MISMATCH, f"{key} must be a string")
    if not value.strip():
        raise ConfigError(ReasonCode.CONFIG_INVALID_VALUE, f"{key} must not be empty")
    return value


def _require_bool(data: dict[str, Any], key: str) -> bool:
    """Liest ein Pflichtfeld vom Typ ``bool``."""
    value = data[key]
    if not isinstance(value, bool):
        raise ConfigError(ReasonCode.CONFIG_TYPE_MISMATCH, f"{key} must be a boolean")
    return value


def parse_config_mapping(data: dict[str, Any]) -> RuntimeConfig:
    """Validiert ein bereits geparstes Mapping und baut eine Konfiguration.

    Args:
        data: Rohes Mapping aus einer TOML-Datei.

    Returns:
        Die validierte Konfiguration.

    Raises:
        ConfigError: Bei jedem Verstoß gegen das Schema. Die Prüfreihenfolge
            ist stabil: Schema-Version, unbekannte Felder, fehlende Felder,
            Werte.
    """
    # 1 — Schema-Version zuerst. Ohne bekannte Version wird nichts gedeutet.
    raw_version = data.get("schema_version")
    if raw_version is None:
        raise ConfigError(ReasonCode.CONFIG_MISSING_FIELD, "schema_version")
    if not isinstance(raw_version, str) or raw_version != SCHEMA_VERSION:
        raise ConfigError(
            ReasonCode.CONFIG_SCHEMA_VERSION_UNSUPPORTED,
            f"expected {SCHEMA_VERSION}",
        )

    # 2 — Unbekannte Felder blockieren; sie werden nicht ignoriert.
    unknown = sorted(set(data) - REQUIRED_FIELDS)
    if unknown:
        raise ConfigError(ReasonCode.CONFIG_UNKNOWN_FIELD, ", ".join(unknown))

    # 3 — Fehlende Pflichtfelder.
    missing = sorted(REQUIRED_FIELDS - set(data))
    if missing:
        raise ConfigError(ReasonCode.CONFIG_MISSING_FIELD, ", ".join(missing))

    # 4 — Werte.
    runtime_mode_raw = _require_str(data, "runtime_mode")
    if runtime_mode_raw != RuntimeMode.SKELETON.value:
        raise ConfigError(
            ReasonCode.CONFIG_INVALID_VALUE,
            "runtime_mode must be 'skeleton'",
        )

    control = _require_str(data, "control_plane_identity")
    worker = _require_str(data, "data_worker_identity")

    if control.strip().lower() in FORBIDDEN_IDENTITY_NAMES:
        raise ConfigError(ReasonCode.IDENTITY_IS_ROOT, "control_plane_identity")
    if worker.strip().lower() in FORBIDDEN_IDENTITY_NAMES:
        raise ConfigError(ReasonCode.IDENTITY_IS_ROOT, "data_worker_identity")
    if control.strip().lower() == worker.strip().lower():
        raise ConfigError(ReasonCode.IDENTITIES_NOT_SEPARATED, "identities are equal")

    egress_raw = _require_str(data, "egress_default")
    if egress_raw != EgressDefault.DENY.value:
        raise ConfigError(
            ReasonCode.EGRESS_NOT_DENY,
            "egress_default must be 'deny' in skeleton mode",
        )

    if _require_bool(data, "canonical_write_allowed"):
        raise ConfigError(
            ReasonCode.CANONICAL_WRITE_REQUESTED,
            "canonical_write_allowed must be false",
        )

    if _require_bool(data, "source_activation_enabled"):
        raise ConfigError(
            ReasonCode.SOURCE_ACTIVATION_REQUESTED,
            "source_activation_enabled must be false",
        )

    try:
        mapping_gate = GateStatus(_require_str(data, "mapping_gate_status"))
        security_gate = GateStatus(_require_str(data, "security_gate_status"))
    except ValueError as exc:
        raise ConfigError(
            ReasonCode.CONFIG_INVALID_VALUE, "unknown gate status"
        ) from exc

    try:
        secret_status = ComponentStatus(_require_str(data, "secret_provider_status"))
        evidence_status = ComponentStatus(
            _require_str(data, "evidence_writer_status")
        )
    except ValueError as exc:
        raise ConfigError(
            ReasonCode.CONFIG_INVALID_VALUE, "unknown component status"
        ) from exc

    return RuntimeConfig(
        schema_version=raw_version,
        runtime_mode=RuntimeMode.SKELETON,
        control_plane_identity=control,
        data_worker_identity=worker,
        egress_default=EgressDefault.DENY,
        canonical_write_allowed=False,
        source_activation_enabled=False,
        mapping_gate_status=mapping_gate,
        security_gate_status=security_gate,
        secret_provider_status=secret_status,
        evidence_writer_status=evidence_status,
    )


def load_config(path: Path) -> RuntimeConfig:
    """Lädt und validiert eine Skeleton-Konfiguration.

    Args:
        path: Ausdrücklicher Pfad zur TOML-Datei. Es gibt **keinen**
            impliziten Standardpfad.

    Returns:
        Die validierte Konfiguration.

    Raises:
        ConfigError: Datei fehlt, ist nicht lesbar, nicht parsebar oder
            verletzt das Schema.
    """
    if not path.is_file():
        raise ConfigError(ReasonCode.CONFIG_FILE_MISSING, path.name)

    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise ConfigError(ReasonCode.CONFIG_NOT_READABLE, path.name) from exc

    try:
        data = tomllib.loads(raw.decode("utf-8"))
    except (tomllib.TOMLDecodeError, UnicodeDecodeError) as exc:
        raise ConfigError(ReasonCode.CONFIG_PARSE_ERROR, path.name) from exc

    return parse_config_mapping(data)
