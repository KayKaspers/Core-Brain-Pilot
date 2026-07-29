"""Statischer Security Readiness Contract (CBP-WP-018, ADR-0013, D-053).

Dieses Modul ist **rein statisch**: keine Datei-, Netz-, ENV-, Uhr- oder
Zufallszugriffe, keine Mutation, keine I/O. Es kodiert die Zuordnung der
dokumentierten KB-Controls (ADR-0009) zu den Mapping-Activation-Gate-Kriterien
als **statischen Vertrag** und liefert dessen deterministischen Hash.

Der Vertrag ist **synthetic-form-only** und **RT-1**: er beschreibt, welche
`(criterion, control_id)`-Bindungen eine synthetische Formprüfung erwartet — er
**bestätigt keine** technische Durchsetzung, Wirksamkeit, Security Readiness,
keinen bestandenen Negativtest, keine Human Approval und keine Aktivierung.

Der Import dieses Moduls hat keine Nebenwirkungen.
"""

from __future__ import annotations

import hashlib
import re
from typing import Final

from .models import (
    SECURITY_CONTROL_PRODUCER_CLASS,
    canonical_json_bytes,
)

__all__ = [
    "SECURITY_CONTRACT_REVISION",
    "CONTROL_ID_RE",
    "DOCUMENTED_CONTROLS",
    "RUNTIME_SCOPED_CONTROLS",
    "NON_RUNTIME_SCOPED_CONTROLS",
    "RUNTIME_SCOPED_BINDINGS",
    "RUNTIME_SCOPED_CRITERIA",
    "NON_SECURITY_STRUCTURAL_CRITERIA",
    "is_runtime_scoped_binding",
    "security_contract_sha256",
]

SECURITY_CONTRACT_REVISION: Final[str] = "1.0"

# Geschlossene KB-Control-ID-Syntax (opak, reportsicher; kein freier String).
CONTROL_ID_RE: Final[re.Pattern[str]] = re.compile(r"\AKB-(0[1-9]|1[0-2])\Z")

# Zwölf dokumentierte Controls (ADR-0009, TECHNICAL_SECURITY_FOUNDATION_SPEC).
DOCUMENTED_CONTROLS: Final[tuple[str, ...]] = tuple(
    f"KB-{i:02d}" for i in range(1, 13)
)

# Sieben runtime-scoped Controls (mit Mapping-Gate-Kriteriumsidentität).
RUNTIME_SCOPED_CONTROLS: Final[tuple[str, ...]] = (
    "KB-02", "KB-03", "KB-04", "KB-07", "KB-08", "KB-10", "KB-11",
)

# Fünf nicht runtime-scoped Controls (Teil des breiteren 24-Punkte-Readiness-
# Gates; **nicht** unwichtig/erfüllt/implementiert/evaluiert/durchgesetzt).
NON_RUNTIME_SCOPED_CONTROLS: Final[tuple[str, ...]] = (
    "KB-01", "KB-05", "KB-06", "KB-09", "KB-12",
)

# Elf kanonische `(criterion, control_id)`-Bindungen, sortiert nach Kriterium
# aufsteigend, dann control_id lexikografisch.
RUNTIME_SCOPED_BINDINGS: Final[tuple[tuple[int, str], ...]] = (
    (4, "KB-08"),
    (6, "KB-10"), (6, "KB-11"),
    (7, "KB-02"), (7, "KB-04"), (7, "KB-07"),
    (8, "KB-03"), (8, "KB-04"),
    (10, "KB-11"),
    (11, "KB-03"), (11, "KB-04"),
)

# Kriterien mit runtime-scoped Security-Control-Bindungen.
RUNTIME_SCOPED_CRITERIA: Final[frozenset[int]] = frozenset(
    c for c, _ in RUNTIME_SCOPED_BINDINGS
)

# Kriterium 9 ist ausdrücklich non-security-structural (keine KB-Control-Bindung).
NON_SECURITY_STRUCTURAL_CRITERIA: Final[frozenset[int]] = frozenset({9})

_BINDING_SET: Final[frozenset[tuple[int, str]]] = frozenset(RUNTIME_SCOPED_BINDINGS)


def is_runtime_scoped_binding(criterion: int, control_id: str) -> bool:
    """True nur, wenn ``(criterion, control_id)`` ein zulässiges Vertragspaar ist."""
    return (criterion, control_id) in _BINDING_SET


def security_contract_sha256() -> str:
    """SHA-256 über den **vollständigen statischen** Security-Contract-Deskriptor.

    Deterministisch, ohne Laufzeitdaten und ohne I/O; identischer Vertrag ⇒
    identischer Hash.
    """
    payload = {
        "security_contract_revision": SECURITY_CONTRACT_REVISION,
        "documented_controls": list(DOCUMENTED_CONTROLS),
        "runtime_scoped_controls": list(RUNTIME_SCOPED_CONTROLS),
        "runtime_scoped_bindings": [
            {"criterion": c, "control_id": k} for c, k in RUNTIME_SCOPED_BINDINGS
        ],
        "non_runtime_scoped_controls": list(NON_RUNTIME_SCOPED_CONTROLS),
        "non_security_structural_criteria": sorted(NON_SECURITY_STRUCTURAL_CRITERIA),
        "required_producer_class": SECURITY_CONTROL_PRODUCER_CLASS,
        "control_id_syntax": "KB-(0[1-9]|1[0-2])",
        "synthetic_form_only": True,
        "binding_identity": ["criterion", "control_id"],
        "negative_evidence_only": True,
        "canonical_json_rules": [
            "utf-8", "no-bom", "sorted-keys", "compact-separators",
            "no-nan-infinity", "no-clock", "no-runtime-data",
        ],
    }
    return hashlib.sha256(canonical_json_bytes(payload)).hexdigest()
