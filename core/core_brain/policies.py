"""Reine, testbare fail-closed Policy-Funktionen.

Jede Funktion ist seiteneffektfrei und liefert ein :class:`Check`. Keine
Funktion greift auf Netzwerk, Secrets, kanonische Quellen oder reale Source
Boundaries zu.

**Wichtig:** Ein ``PASS`` in diesem Modul ist ein Skeleton-Ergebnis, **kein
Deploymentnachweis**. Die Kontrollbereiche KB-01 bis KB-12 aus ADR-0009
bleiben `DOCUMENTED ONLY`.

Der Import dieses Moduls hat keine Nebenwirkungen.
"""

from __future__ import annotations

import os

from .errors import ReasonCode
from .models import (
    Check,
    CheckResult,
    ComponentStatus,
    DoctorReport,
    EgressDefault,
    GateStatus,
    RuntimeConfig,
)

__all__ = [
    "check_not_privileged",
    "check_identity_separation",
    "check_canonical_write_blocked",
    "check_source_activation_blocked",
    "check_egress_deny_by_default",
    "check_secret_provider_unconfigured",
    "check_evidence_writer_unconfigured",
    "check_runtime_start_blocked",
    "build_doctor_report",
]


def check_not_privileged() -> Check:
    """Prüft, dass der Prozess nicht privilegiert läuft.

    Auf POSIX wird ``os.geteuid()`` ausgewertet; ``0`` blockiert. Auf
    Plattformen ohne ``geteuid`` — insbesondere Windows — ist das Ergebnis
    ``NOT APPLICABLE``.

    Returns:
        Das Prüfergebnis.

    Note:
        ``NOT APPLICABLE`` ist **kein bestandener Deploymentnachweis**. Der
        Nachweis zu KB-01 wird auf der Ziel-Linux-VM erbracht, nicht hier.
    """
    geteuid = getattr(os, "geteuid", None)
    if geteuid is None:
        return Check(
            check_id="KB-01",
            title="Nicht privilegierter Betrieb",
            result=CheckResult.NOT_APPLICABLE,
            detail=(
                "Plattform ohne geteuid. Kein Deploymentnachweis — "
                "KB-01 wird auf der Ziel-VM geprüft."
            ),
        )
    if geteuid() == 0:
        return Check(
            check_id="KB-01",
            title="Nicht privilegierter Betrieb",
            result=CheckResult.BLOCKED,
            reason=ReasonCode.PRIVILEGED_PROCESS,
            detail="Prozess läuft mit effektiver UID 0.",
        )
    return Check(
        check_id="KB-01",
        title="Nicht privilegierter Betrieb",
        result=CheckResult.PASS,
        detail="Effektive UID ist nicht 0. Lokales Skeleton-Ergebnis.",
    )


def check_identity_separation(config: RuntimeConfig) -> Check:
    """Prüft, dass Control Plane und Data Worker getrennt sind."""
    if (
        config.control_plane_identity.strip().lower()
        == config.data_worker_identity.strip().lower()
    ):
        return Check(
            check_id="KB-02",
            title="Getrennte Service-Identitäten",
            result=CheckResult.BLOCKED,
            reason=ReasonCode.IDENTITIES_NOT_SEPARATED,
            detail="Control Plane und Data Worker sind identisch.",
        )
    return Check(
        check_id="KB-02",
        title="Getrennte Service-Identitäten",
        result=CheckResult.PASS,
        detail="Logisch getrennt. Keine OS-Identität angelegt.",
    )


def check_canonical_write_blocked(config: RuntimeConfig) -> Check:
    """Prüft, dass Schreibzugriff auf Canonical verboten bleibt."""
    if config.canonical_write_allowed:
        return Check(
            check_id="KB-03",
            title="Canonical Write verboten",
            result=CheckResult.BLOCKED,
            reason=ReasonCode.CANONICAL_WRITE_REQUESTED,
            detail="canonical_write_allowed ist true.",
        )
    return Check(
        check_id="KB-03",
        title="Canonical Write verboten",
        result=CheckResult.PASS,
        detail="Skeleton berührt keine kanonische Quelle.",
    )


def check_source_activation_blocked(config: RuntimeConfig) -> Check:
    """Prüft, dass keine Source-Aktivierung angefordert wird."""
    if config.source_activation_enabled:
        return Check(
            check_id="KB-06",
            title="Source-Aktivierung blockiert",
            result=CheckResult.BLOCKED,
            reason=ReasonCode.SOURCE_ACTIVATION_REQUESTED,
            detail="source_activation_enabled ist true.",
        )
    return Check(
        check_id="KB-06",
        title="Source-Aktivierung blockiert",
        result=CheckResult.PASS,
        detail="Kein Mapping wird aktiviert.",
    )


def check_egress_deny_by_default(config: RuntimeConfig) -> Check:
    """Prüft, dass der Egress-Default ``deny`` ist.

    Note:
        Es ist **keine Allowlist implementiert**. Der Skeleton führt keinen
        Netzwerkzugriff aus.
    """
    if config.egress_default is not EgressDefault.DENY:
        return Check(
            check_id="KB-10",
            title="Netzwerk-Egress deny-by-default",
            result=CheckResult.BLOCKED,
            reason=ReasonCode.EGRESS_NOT_DENY,
            detail="egress_default ist nicht 'deny'.",
        )
    return Check(
        check_id="KB-10",
        title="Netzwerk-Egress deny-by-default",
        result=CheckResult.PASS,
        detail="Deny. Keine Allowlist implementiert, kein Netzwerkzugriff.",
    )


def check_secret_provider_unconfigured(config: RuntimeConfig) -> Check:
    """Prüft, dass kein Secret-Provider angebunden ist."""
    if config.secret_provider_status is not ComponentStatus.UNCONFIGURED:
        return Check(
            check_id="KB-08",
            title="Secret-Provider nicht angebunden",
            result=CheckResult.BLOCKED,
            reason=ReasonCode.SECRET_PROVIDER_UNCONFIGURED,
            detail="Skeleton erlaubt keinen konfigurierten Secret-Provider.",
        )
    return Check(
        check_id="KB-08",
        title="Secret-Provider nicht angebunden",
        result=CheckResult.PASS,
        detail="Unconfigured. Keine Secret-Auflösung implementiert.",
    )


def check_evidence_writer_unconfigured(config: RuntimeConfig) -> Check:
    """Prüft, dass kein RT-2-Writer angebunden ist."""
    if config.evidence_writer_status is not ComponentStatus.UNCONFIGURED:
        return Check(
            check_id="KB-09",
            title="Operational Evidence nicht angebunden",
            result=CheckResult.BLOCKED,
            reason=ReasonCode.EVIDENCE_WRITER_UNCONFIGURED,
            detail="Skeleton erlaubt keinen konfigurierten Evidence Writer.",
        )
    return Check(
        check_id="KB-09",
        title="Operational Evidence nicht angebunden",
        result=CheckResult.PASS,
        detail="Unconfigured. Kein RT-2-Speicher implementiert.",
    )


def check_runtime_start_blocked(config: RuntimeConfig) -> Check:
    """Prüft den operativen Start — im Skeleton **immer blockiert**.

    Der Start bleibt verweigert, solange das Security Foundation Readiness
    Gate nicht außerhalb dieses Work Packages angenommen und technisch
    angebunden ist.
    """
    if config.security_gate_status is not GateStatus.ACCEPTED:
        reason = ReasonCode.SECURITY_GATE_NOT_ACCEPTED
    elif config.mapping_gate_status is not GateStatus.ACCEPTED:
        reason = ReasonCode.MAPPING_GATE_NOT_ACCEPTED
    else:
        reason = ReasonCode.RUNTIME_SKELETON_ONLY

    return Check(
        check_id="RUNTIME",
        title="Operativer Runtime-Start",
        result=CheckResult.BLOCKED,
        reason=reason,
        detail=(
            "Der Skeleton startet keine operative Runtime. "
            "Verweigerung ist unabhängig von der Konfiguration."
        ),
    )


def build_doctor_report(config: RuntimeConfig) -> DoctorReport:
    """Erstellt den vollständigen, deterministischen Doctor-Bericht.

    Die Reihenfolge der Prüfungen ist fest und hängt nicht von Mengen,
    Zeitpunkten oder Umgebungsvariablen ab.

    Returns:
        Den Bericht. ``production_ready`` ist **immer** ``False``.
    """
    checks = (
        check_not_privileged(),
        check_identity_separation(config),
        check_canonical_write_blocked(config),
        check_source_activation_blocked(config),
        check_secret_provider_unconfigured(config),
        check_evidence_writer_unconfigured(config),
        check_egress_deny_by_default(config),
        check_runtime_start_blocked(config),
    )
    return DoctorReport(
        runtime_mode=config.runtime_mode,
        production_ready=False,
        checks=checks,
    )
