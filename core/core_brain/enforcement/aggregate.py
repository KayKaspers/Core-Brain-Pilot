"""Befunde, Aggregation und Gesamtergebnis der KB-04-Validierung.

Dieses Modul definiert das **Ergebnisvokabular** der Stufe-1-Durchsetzung
(CBP-WP-022, ADR-0014, D-060) und faltet Befunde **fail-closed** zusammen.

Es ist die unterste Schicht des Pakets: es importiert zur Laufzeit **nichts**
aus den übrigen Enforcement-Modulen und erzeugt dadurch keinen Importzyklus.

Zwei Aussagen werden strikt getrennt:

* ``conform`` — die **logische** Vertragskonformität der vorgelegten Befunde.
* ``operationally_verified`` — die **operative** Verifikation. Sie verlangt
  zusätzlich, dass jede erforderliche Beobachtung tatsächlich **beobachtet**
  wurde. Synthetische und deklarierte Beobachtungen erfüllen sie **nie**.

**Ein synthetisch konformes Ergebnis ist keine KB-04-Evidenz.** Es belegt
weder NT-04 noch NT-05, schließt OD-37 nicht, stellt keine Gate-Evidenz dar
und stuft keine Control hoch.

Der Import dieses Moduls hat keine Nebenwirkungen.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING, Final, Iterable

from ..errors import ReasonCode

if TYPE_CHECKING:  # pragma: no cover - nur für die Typprüfung
    from .contract import Dimension, PathClass
    from .validator import ObservationOrigin

__all__ = [
    "FindingStatus",
    "Finding",
    "ValidationResult",
    "REQUIRED_DIMENSIONS",
    "aggregate_findings",
    "canonical_json_bytes",
]


class FindingStatus(StrEnum):
    """Status eines einzelnen Befundes.

    ``NOT_APPLICABLE`` ist **kein bestandener Sicherheitsnachweis**. Für eine
    erforderliche Prüfung verhindert es die Konformität ebenso wie
    ``INDETERMINATE``.
    """

    CONFORM = "CONFORM"
    VIOLATION = "VIOLATION"
    INDETERMINATE = "INDETERMINATE"
    NOT_APPLICABLE = "NOT_APPLICABLE"


#: Die vier Prüfdimensionen, die für eine operative Verifikation erforderlich
#: sind (Contract §7.1, MT-9 bis MT-14). Als Zeichenketten geführt, damit
#: dieses Modul zur Laufzeit unabhängig von ``contract`` bleibt.
REQUIRED_DIMENSIONS: Final[tuple[str, ...]] = ("D-I", "D-II", "D-III", "D-IV")


@dataclass(frozen=True, slots=True, order=True)
class Finding:
    """Ein einzelner, unveränderlicher Prüfbefund.

    Die Feldreihenfolge bestimmt die deterministische Sortierung: erst
    Pfadklasse, dann relativer Pfad, dann Dimension, dann Status. ``order=True``
    macht die Reihenfolge reproduzierbar, ohne einen Sortierschlüssel zu
    erfinden.

    Der Befund trägt **niemals** einen realen Hostpfad, eine reale Identität
    oder einen Inhaltswert — ``relative_path`` ist repositorierelativ oder ein
    abstrakter Bereichsanker, ``detail`` ist wertfrei.
    """

    path_class: PathClass | str
    relative_path: str
    dimension: Dimension | str
    status: FindingStatus
    reason: ReasonCode | None = None
    detail: str = ""
    origin: ObservationOrigin | str | None = None
    required: bool = True

    def to_dict(self) -> dict[str, object]:
        """Gibt eine deterministische, JSON-taugliche Darstellung zurück."""
        return {
            "path_class": str(self.path_class),
            "relative_path": self.relative_path,
            "dimension": str(self.dimension),
            "status": self.status.value,
            "reason": self.reason.value if self.reason is not None else None,
            "detail": self.detail,
            "origin": str(self.origin) if self.origin is not None else None,
            "required": self.required,
        }


@dataclass(frozen=True, slots=True)
class ValidationResult:
    """Aggregiertes, unveränderliches Gesamtergebnis einer Validierung."""

    findings: tuple[Finding, ...]
    conform: bool
    operationally_verified: bool
    violation_count: int
    indeterminate_count: int
    not_applicable_count: int
    conform_count: int
    observed_dimensions: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        """Gibt eine deterministische, JSON-taugliche Darstellung zurück."""
        return {
            "conform": self.conform,
            "conform_count": self.conform_count,
            "findings": [f.to_dict() for f in self.findings],
            "indeterminate_count": self.indeterminate_count,
            "not_applicable_count": self.not_applicable_count,
            "observed_dimensions": list(self.observed_dimensions),
            "operationally_verified": self.operationally_verified,
            "violation_count": self.violation_count,
        }


def canonical_json_bytes(data: object) -> bytes:
    """Serialisiert ``data`` deterministisch und byte-stabil.

    Sortierte Schlüssel, kompakte Trennzeichen, UTF-8, keine Zeitstempel.
    """
    text = json.dumps(
        data, sort_keys=True, ensure_ascii=False, separators=(",", ":")
    )
    return text.encode("utf-8")


def aggregate_findings(findings: Iterable[Finding]) -> ValidationResult:
    """Faltet Befunde fail-closed zu einem Gesamtergebnis zusammen.

    ``conform`` ist nur dann ``True``, wenn **jeder erforderliche** Befund
    ``CONFORM`` ist: keine ``VIOLATION``, kein ``INDETERMINATE`` und kein
    erforderliches ``NOT_APPLICABLE``. Eine leere Befundmenge ist **nicht**
    konform — ein nicht geprüfter Zustand ist kein geprüfter Zustand.

    ``operationally_verified`` verlangt zusätzlich, dass **alle vier**
    Dimensionen aus :data:`REQUIRED_DIMENSIONS` mit ``CONFORM`` und der
    Herkunft ``OBSERVED`` belegt sind. Eine synthetische oder deklarierte
    Beobachtung erfüllt diese Aussage **niemals**.

    Args:
        findings: Die zu faltenden Befunde. Die Eingabereihenfolge ist
            unerheblich; das Ergebnis ist stets sortiert.

    Returns:
        Das aggregierte, unveränderliche Ergebnis.
    """
    ordered = tuple(sorted(findings))

    violations = sum(1 for f in ordered if f.status is FindingStatus.VIOLATION)
    indeterminate = sum(
        1 for f in ordered if f.status is FindingStatus.INDETERMINATE
    )
    not_applicable = sum(
        1 for f in ordered if f.status is FindingStatus.NOT_APPLICABLE
    )
    conform_count = sum(1 for f in ordered if f.status is FindingStatus.CONFORM)

    required = tuple(f for f in ordered if f.required)
    conform = bool(required) and all(
        f.status is FindingStatus.CONFORM for f in required
    )

    # Operative Verifikation: nur echte Beobachtungen zählen. ``str`` deckt
    # sowohl ``ObservationOrigin.OBSERVED`` als auch dessen Wert ab.
    observed = tuple(
        sorted(
            {
                str(f.dimension)
                for f in required
                if f.status is FindingStatus.CONFORM
                and f.origin is not None
                and str(f.origin) == "OBSERVED"
            }
        )
    )
    operationally_verified = conform and all(
        dimension in observed for dimension in REQUIRED_DIMENSIONS
    )

    return ValidationResult(
        findings=ordered,
        conform=conform,
        operationally_verified=operationally_verified,
        violation_count=violations,
        indeterminate_count=indeterminate,
        not_applicable_count=not_applicable,
        conform_count=conform_count,
        observed_dimensions=observed,
    )
