"""Abstrakte Grenzen zu noch nicht implementierten Subsystemen.

Dieses Modul definiert **Protokolle** und fail-closed Default-Implementierungen
für vier Grenzen aus ADR-0009. Es enthält:

- keinen realen Provider,
- keinen Dateizugriff auf Secret-Bereiche,
- keinen Netzwerkzugriff,
- keinen RT-2-Speicher.

Jede Default-Implementierung **verweigert**. Das ist beabsichtigt: Ein Port,
der im Skeleton etwas zurückgäbe, wäre eine stille Teilimplementierung.

Der Import dieses Moduls hat keine Nebenwirkungen.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from .errors import PortRefused, ReasonCode
from .models import GateStatus, RuntimeMode

__all__ = [
    "SecretResolver",
    "OperationalEvidenceWriter",
    "EgressDecisionPort",
    "RuntimeStatusProvider",
    "DenyingSecretResolver",
    "DenyingEvidenceWriter",
    "DenyingEgressPort",
    "SkeletonRuntimeStatusProvider",
]


@runtime_checkable
class SecretResolver(Protocol):
    """Löst eine Secret-Referenz zu einem Wert auf.

    Der Skeleton implementiert **keine** Auflösung.
    """

    def resolve(self, reference: str) -> str:
        """Löst eine Referenz auf.

        Args:
            reference: Opake Referenz nach ADR-0009, Form
                ``cbp-secret:v1:<provider>:<opaque-id>``.

        Returns:
            Den Secret-Wert.

        Raises:
            PortRefused: Immer, solange kein Provider angebunden ist.
        """
        ...


@runtime_checkable
class OperationalEvidenceWriter(Protocol):
    """Schreibt ein RT-2-Ereignis.

    Der Skeleton implementiert **keinen** Speicher.
    """

    def append(self, event_type: str, payload: dict[str, str]) -> str:
        """Fügt ein Ereignis an.

        Args:
            event_type: Ereignisart nach der Operational Evidence Policy.
            payload: Wertfreie Ereignisfelder. Enthält niemals Secrets.

        Returns:
            Die Ereignis-ID.

        Raises:
            PortRefused: Immer, solange kein Writer angebunden ist.
        """
        ...


@runtime_checkable
class EgressDecisionPort(Protocol):
    """Entscheidet über eine ausgehende Verbindung.

    Der Skeleton führt **keinen** Netzwerkzugriff aus.
    """

    def allow(self, target: str, purpose: str, identity: str) -> bool:
        """Entscheidet über einen Egress-Versuch.

        Args:
            target: Zielkennung, kein realer Host.
            purpose: Zweckbindung.
            identity: Anfragende Service-Identität.

        Returns:
            ``True``, wenn erlaubt.

        Raises:
            PortRefused: Immer — deny-by-default ohne Allowlist.
        """
        ...


@runtime_checkable
class RuntimeStatusProvider(Protocol):
    """Liefert den Betriebszustand der Runtime."""

    def is_production_ready(self) -> bool:
        """Gibt zurück, ob die Runtime produktiv betrieben werden darf."""
        ...

    def mode(self) -> RuntimeMode:
        """Gibt den Betriebsmodus zurück."""
        ...


class DenyingSecretResolver:
    """Default-Resolver: verweigert **jede** Auflösung.

    Er berührt keinen Secret-Bereich und liest keine Datei.
    """

    def resolve(self, reference: str) -> str:
        """Verweigert die Auflösung.

        Raises:
            PortRefused: Immer. Die Referenz wird **nicht** protokolliert.
        """
        raise PortRefused(
            ReasonCode.SECRET_RESOLUTION_NOT_IMPLEMENTED,
            "no secret provider is bound in skeleton mode",
        )


class DenyingEvidenceWriter:
    """Default-Writer: verweigert **jeden** Schreibversuch.

    Ein direkter RT-2-Schreibversuch scheitert. Es existiert kein Speicher.
    """

    def append(self, event_type: str, payload: dict[str, str]) -> str:
        """Verweigert das Anfügen.

        Raises:
            PortRefused: Immer.
        """
        raise PortRefused(
            ReasonCode.EVIDENCE_WRITER_NOT_IMPLEMENTED,
            "no operational evidence writer is bound in skeleton mode",
        )


class DenyingEgressPort:
    """Default-Port: verweigert **jede** ausgehende Verbindung."""

    def allow(self, target: str, purpose: str, identity: str) -> bool:
        """Verweigert den Egress.

        Raises:
            PortRefused: Immer. Es existiert keine Allowlist.
        """
        raise PortRefused(
            ReasonCode.EGRESS_PORT_DENY_BY_DEFAULT,
            "egress is deny-by-default and no allowlist is implemented",
        )


class SkeletonRuntimeStatusProvider:
    """Statusprovider des Skeletons.

    Meldet dauerhaft ``production_ready = False``.
    """

    def __init__(
        self,
        security_gate: GateStatus = GateStatus.NOT_EVALUATED,
        mapping_gate: GateStatus = GateStatus.NOT_EVALUATED,
    ) -> None:
        """Erzeugt den Provider mit den beiden Gate-Zuständen."""
        self.security_gate = security_gate
        self.mapping_gate = mapping_gate

    def is_production_ready(self) -> bool:
        """Gibt immer ``False`` zurück.

        Der Skeleton ist unabhängig vom Gate-Status nicht produktionsbereit.
        """
        return False

    def mode(self) -> RuntimeMode:
        """Gibt den Betriebsmodus zurück."""
        return RuntimeMode.SKELETON
