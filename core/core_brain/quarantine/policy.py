"""Strikte, fail-closed Validierung der Quarantäne-Policy (CBP-WP-013).

Grundsatz: **fail-closed**. Ein unbekanntes Feld, eine unbekannte
Schema-Version, ein fehlendes Pflichtfeld, ein unzulässiger Wert, eine leere
Suffixliste, ``release_enabled = true`` oder ``network_enabled = true``
blockieren die Validierung.

**Environment-Variablen und CLI-Argumente überschreiben keine Policy-Werte.**
Dieses Modul liest weder ``os.environ`` noch ``sys.argv``. Es gibt **keine**
frei konfigurierbaren regulären Ausdrücke.

Der Import dieses Moduls hat keine Nebenwirkungen.
"""

from __future__ import annotations

import hashlib
import tomllib
from pathlib import Path
from typing import Any, Final

from ..errors import QuarantinePolicyError, ReasonCode
from .models import POLICY_SCHEMA_VERSION, QuarantinePolicy

__all__ = [
    "REQUIRED_POLICY_FIELDS",
    "load_policy",
    "parse_policy_mapping",
]

_STR_LIST_FIELDS: Final[frozenset[str]] = frozenset({"allowed_suffixes"})
_INT_FIELDS: Final[frozenset[str]] = frozenset({"max_bytes"})
_BOOL_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "reject_symlinks",
        "require_regular_file",
        "require_utf8",
        "reject_nul",
        "block_private_key_markers",
        "block_credential_assignments",
        "review_email_indicators",
        "review_phone_indicators",
        "release_enabled",
        "network_enabled",
    }
)

REQUIRED_POLICY_FIELDS: Final[frozenset[str]] = (
    frozenset({"schema_version"}) | _STR_LIST_FIELDS | _INT_FIELDS | _BOOL_FIELDS
)
"""Alle Pflichtfelder. Es gibt keine optionalen Felder in der MVP-Policy."""

# Konservative Obergrenze. max_bytes darf diese Schranke nicht überschreiten.
_MAX_BYTES_CEILING: Final[int] = 8 * 1024 * 1024


def _require_bool(data: dict[str, Any], key: str) -> bool:
    """Liest ein Pflichtfeld vom Typ ``bool``."""
    value = data[key]
    if not isinstance(value, bool):
        raise QuarantinePolicyError(
            ReasonCode.QUARANTINE_POLICY_INVALID_VALUE, f"{key} must be a boolean"
        )
    return value


def parse_policy_mapping(data: dict[str, Any], policy_sha256: str) -> QuarantinePolicy:
    """Validiert ein bereits geparstes Mapping und baut eine Policy.

    Args:
        data: Rohes Mapping aus einer TOML-Datei.
        policy_sha256: Hexdigest der kanonischen Policy-Bytes.

    Returns:
        Die validierte Policy.

    Raises:
        QuarantinePolicyError: Bei jedem Verstoß. Die Prüfreihenfolge ist
            stabil: Schema-Version, unbekannte Felder, fehlende Felder, Werte.
    """
    # 1 — Schema-Version zuerst.
    raw_version = data.get("schema_version")
    if raw_version is None:
        raise QuarantinePolicyError(
            ReasonCode.QUARANTINE_POLICY_MISSING_FIELD, "schema_version"
        )
    if not isinstance(raw_version, str) or raw_version != POLICY_SCHEMA_VERSION:
        raise QuarantinePolicyError(
            ReasonCode.QUARANTINE_POLICY_SCHEMA_UNSUPPORTED,
            f"expected {POLICY_SCHEMA_VERSION}",
        )

    # 2 — Unbekannte Felder blockieren.
    unknown = sorted(set(data) - REQUIRED_POLICY_FIELDS)
    if unknown:
        raise QuarantinePolicyError(
            ReasonCode.QUARANTINE_POLICY_UNKNOWN_FIELD, ", ".join(unknown)
        )

    # 3 — Fehlende Pflichtfelder.
    missing = sorted(REQUIRED_POLICY_FIELDS - set(data))
    if missing:
        raise QuarantinePolicyError(
            ReasonCode.QUARANTINE_POLICY_MISSING_FIELD, ", ".join(missing)
        )

    # 4 — Werte. max_bytes positiv und konservativ begrenzt.
    max_bytes = data["max_bytes"]
    if not isinstance(max_bytes, int) or isinstance(max_bytes, bool):
        raise QuarantinePolicyError(
            ReasonCode.QUARANTINE_POLICY_INVALID_VALUE, "max_bytes must be an integer"
        )
    if max_bytes <= 0:
        raise QuarantinePolicyError(
            ReasonCode.QUARANTINE_POLICY_INVALID_VALUE, "max_bytes must be positive"
        )
    if max_bytes > _MAX_BYTES_CEILING:
        raise QuarantinePolicyError(
            ReasonCode.QUARANTINE_POLICY_INVALID_VALUE,
            "max_bytes exceeds the conservative ceiling",
        )

    # 5 — allowed_suffixes: nicht leer, nur Strings, mit führendem Punkt.
    suffixes = data["allowed_suffixes"]
    if not isinstance(suffixes, list) or not suffixes:
        raise QuarantinePolicyError(
            ReasonCode.QUARANTINE_POLICY_INVALID_VALUE,
            "allowed_suffixes must be a non-empty list",
        )
    normalized: list[str] = []
    for item in suffixes:
        if not isinstance(item, str) or not item.startswith(".") or len(item) < 2:
            raise QuarantinePolicyError(
                ReasonCode.QUARANTINE_POLICY_INVALID_VALUE,
                "allowed_suffixes entries must be dotted suffixes",
            )
        normalized.append(item.lower())

    # 6 — Boolesche Sicherheitswerte. release/network dürfen nicht aktiv sein.
    bools = {key: _require_bool(data, key) for key in sorted(_BOOL_FIELDS)}

    if bools["release_enabled"]:
        raise QuarantinePolicyError(
            ReasonCode.QUARANTINE_POLICY_RELEASE_ENABLED,
            "release_enabled must be false",
        )
    if bools["network_enabled"]:
        raise QuarantinePolicyError(
            ReasonCode.QUARANTINE_POLICY_NETWORK_ENABLED,
            "network_enabled must be false",
        )

    return QuarantinePolicy(
        schema_version=raw_version,
        max_bytes=max_bytes,
        allowed_suffixes=tuple(normalized),
        reject_symlinks=bools["reject_symlinks"],
        require_regular_file=bools["require_regular_file"],
        require_utf8=bools["require_utf8"],
        reject_nul=bools["reject_nul"],
        block_private_key_markers=bools["block_private_key_markers"],
        block_credential_assignments=bools["block_credential_assignments"],
        review_email_indicators=bools["review_email_indicators"],
        review_phone_indicators=bools["review_phone_indicators"],
        release_enabled=False,
        network_enabled=False,
        policy_sha256=policy_sha256,
    )


def load_policy(path: Path) -> QuarantinePolicy:
    """Lädt und validiert eine Quarantäne-Policy.

    Args:
        path: Ausdrücklicher Pfad zur TOML-Datei. Es gibt **keinen**
            impliziten Standardpfad.

    Returns:
        Die validierte Policy inklusive ``policy_sha256`` der Rohbytes.

    Raises:
        QuarantinePolicyError: Datei fehlt, ist nicht lesbar, nicht parsebar
            oder verletzt das Schema.
    """
    if not path.is_file():
        raise QuarantinePolicyError(
            ReasonCode.QUARANTINE_POLICY_FILE_MISSING, path.name
        )

    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise QuarantinePolicyError(
            ReasonCode.QUARANTINE_POLICY_NOT_READABLE, path.name
        ) from exc

    policy_sha256 = hashlib.sha256(raw).hexdigest()

    try:
        data = tomllib.loads(raw.decode("utf-8"))
    except (tomllib.TOMLDecodeError, UnicodeDecodeError) as exc:
        raise QuarantinePolicyError(
            ReasonCode.QUARANTINE_POLICY_PARSE_ERROR, path.name
        ) from exc

    return parse_policy_mapping(data, policy_sha256)
