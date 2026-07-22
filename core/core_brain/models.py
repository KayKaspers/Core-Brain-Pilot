"""Datenmodelle des Runtime Skeletons.

Alle Modelle sind unveränderlich. Sie enthalten keine Secrets, keine realen
Pfade und keine privaten Werte.

Der Import dieses Moduls hat keine Nebenwirkungen.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from .errors import ReasonCode

__all__ = [
    "SCHEMA_VERSION",
    "RuntimeMode",
    "EgressDefault",
    "GateStatus",
    "ComponentStatus",
    "CheckResult",
    "RuntimeConfig",
    "Check",
    "DoctorReport",
]

SCHEMA_VERSION = "1.0"
"""Einzige unterstützte Schema-Version. Jede andere blockiert."""


class RuntimeMode(StrEnum):
    """Betriebsmodus des Skeletons. Nur ``skeleton`` ist zulässig."""

    SKELETON = "skeleton"


class EgressDefault(StrEnum):
    """Netzwerk-Egress-Vorgabe. Im Skeleton nur ``deny``."""

    DENY = "deny"
    ALLOW = "allow"


class GateStatus(StrEnum):
    """Statuswerte eines Prüfmodells."""

    NOT_EVALUATED = "NOT EVALUATED"
    BLOCKED = "BLOCKED"
    ACCEPTED = "ACCEPTED"


class ComponentStatus(StrEnum):
    """Statuswerte einer noch nicht angebundenen Komponente."""

    UNCONFIGURED = "unconfigured"
    CONFIGURED = "configured"


class CheckResult(StrEnum):
    """Ergebnis einer einzelnen Doctor-Prüfung."""

    PASS = "PASS"
    BLOCKED = "BLOCKED"
    NOT_APPLICABLE = "NOT APPLICABLE"


@dataclass(frozen=True, slots=True)
class RuntimeConfig:
    """Validierte Skeleton-Konfiguration.

    Eine Instanz entsteht ausschließlich über
    :func:`core.core_brain.config.load_config`. Das Vorhandensein einer
    Instanz bedeutet **strukturelle** Gültigkeit — keine Betriebsfreigabe.
    """

    schema_version: str
    runtime_mode: RuntimeMode
    control_plane_identity: str
    data_worker_identity: str
    egress_default: EgressDefault
    canonical_write_allowed: bool
    source_activation_enabled: bool
    mapping_gate_status: GateStatus
    security_gate_status: GateStatus
    secret_provider_status: ComponentStatus
    evidence_writer_status: ComponentStatus


@dataclass(frozen=True, slots=True)
class Check:
    """Ergebnis einer einzelnen Prüfung im Doctor-Bericht."""

    check_id: str
    title: str
    result: CheckResult
    reason: ReasonCode | None = None
    detail: str = ""

    def to_dict(self) -> dict[str, str | None]:
        """Gibt eine JSON-taugliche Darstellung zurück."""
        return {
            "check_id": self.check_id,
            "title": self.title,
            "result": self.result.value,
            "reason": self.reason.value if self.reason is not None else None,
            "detail": self.detail,
        }


@dataclass(frozen=True, slots=True)
class DoctorReport:
    """Vollständiger, deterministischer Doctor-Bericht."""

    runtime_mode: RuntimeMode
    production_ready: bool
    checks: tuple[Check, ...] = field(default_factory=tuple)

    @property
    def blocked(self) -> tuple[Check, ...]:
        """Alle Prüfungen mit Ergebnis ``BLOCKED``."""
        return tuple(c for c in self.checks if c.result is CheckResult.BLOCKED)

    @property
    def summary(self) -> dict[str, int]:
        """Zählt die Ergebnisse je Kategorie."""
        return {
            "pass": sum(1 for c in self.checks if c.result is CheckResult.PASS),
            "blocked": sum(
                1 for c in self.checks if c.result is CheckResult.BLOCKED
            ),
            "not_applicable": sum(
                1 for c in self.checks if c.result is CheckResult.NOT_APPLICABLE
            ),
        }

    def to_dict(self) -> dict[str, object]:
        """Gibt eine JSON-taugliche Darstellung zurück.

        Die Reihenfolge der Prüfungen ist stabil.
        """
        return {
            "runtime_mode": self.runtime_mode.value,
            "production_ready": self.production_ready,
            "summary": self.summary,
            "checks": [c.to_dict() for c in self.checks],
        }
