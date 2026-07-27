"""Kanonischer JSON-Parser des MVP-Dokumentprofils (CBP-WP-015).

Akzeptiert **ausschließlich** kanonisch verarbeitbares JSON (das
JSON-kompatible MVP-Profil des beschlossenen strikten YAML-Teilumfangs). Es
wird **keine** allgemeine YAML-Unterstützung behauptet.

Fail-closed: BOM, ungültiges UTF-8, kein Objekt auf oberster Ebene, doppelte
Schlüssel, ``NaN`` und ``Infinity`` blockieren. Der Import hat keine
Nebenwirkungen.
"""

from __future__ import annotations

import json
from typing import Any

from .models import MappingReasonCode

__all__ = ["DraftRejected", "parse_draft"]

_BOM = b"\xef\xbb\xbf"


class DraftRejected(Exception):
    """Ein Entwurf wurde fail-closed abgewiesen. Trägt einen stabilen Grund.

    Enthält **keinen** Pfad, keine URL und keinen Inhaltsauszug.
    """

    def __init__(self, reason: MappingReasonCode) -> None:
        self.reason = reason
        super().__init__(reason.value)


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    seen: set[str] = set()
    for key, _ in pairs:
        if key in seen:
            raise DraftRejected(MappingReasonCode.PARSE_DUPLICATE_KEY)
        seen.add(key)
    return dict(pairs)


def _reject_constant(_token: str) -> Any:
    # json ruft parse_constant für NaN, Infinity und -Infinity auf.
    if "Infinity" in _token:
        raise DraftRejected(MappingReasonCode.PARSE_INFINITY)
    raise DraftRejected(MappingReasonCode.PARSE_NAN)


def parse_draft(raw: bytes, max_bytes: int) -> dict[str, Any]:
    """Parst einen Mapping-Entwurf aus Rohbytes fail-closed.

    Args:
        raw: Rohbytes des Entwurfs.
        max_bytes: Konservative Obergrenze aus der Policy.

    Returns:
        Das geparste JSON-Objekt (oberste Ebene ein Mapping).

    Raises:
        DraftRejected: Bei jedem Verstoß gegen das Dokumentprofil.
    """
    if len(raw) > max_bytes:
        raise DraftRejected(MappingReasonCode.DRAFT_TOO_LARGE)
    if raw[:3] == _BOM:
        raise DraftRejected(MappingReasonCode.PARSE_BOM)
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise DraftRejected(MappingReasonCode.PARSE_UTF8) from exc
    try:
        parsed = json.loads(
            text,
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=_reject_constant,
        )
    except DraftRejected:
        raise
    except (ValueError, RecursionError) as exc:
        raise DraftRejected(MappingReasonCode.PARSE_JSON) from exc
    if not isinstance(parsed, dict):
        raise DraftRejected(MappingReasonCode.PARSE_NOT_OBJECT)
    return parsed
