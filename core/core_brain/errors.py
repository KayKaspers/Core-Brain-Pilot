"""Fehlertypen und stabile Reason Codes des Runtime Skeletons.

Reason Codes sind Teil der CLI-Schnittstelle. Sie werden nicht umbenannt,
sobald sie in der technischen Evidenz dokumentiert sind.

Der Import dieses Moduls hat keine Nebenwirkungen.
"""

from __future__ import annotations

from enum import StrEnum

__all__ = [
    "ExitCode",
    "ReasonCode",
    "CoreBrainError",
    "ConfigError",
    "PolicyBlocked",
    "PortRefused",
    "RuntimeStartBlocked",
]


class ExitCode(StrEnum):
    """Namen der stabilen Exitcodes.

    Die numerischen Werte stehen in :data:`EXIT_CODES`. Ein Exitcode wird
    nach seiner Dokumentation nicht mehr verändert.
    """

    OK = "OK"
    CONFIG_INVALID = "CONFIG_INVALID"
    POLICY_BLOCKED = "POLICY_BLOCKED"
    RUNTIME_START_BLOCKED = "RUNTIME_START_BLOCKED"
    USAGE_ERROR = "USAGE_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"


EXIT_CODES: dict[ExitCode, int] = {
    ExitCode.OK: 0,
    ExitCode.CONFIG_INVALID: 2,
    ExitCode.POLICY_BLOCKED: 3,
    ExitCode.RUNTIME_START_BLOCKED: 4,
    ExitCode.USAGE_ERROR: 64,
    ExitCode.INTERNAL_ERROR: 70,
}
"""Zuordnung von Exitcode-Namen zu numerischen Prozess-Exitcodes."""


class ReasonCode(StrEnum):
    """Stabile, maschinenlesbare Begründungen.

    Ein Reason Code benennt **warum** etwas verweigert wurde, ohne private
    Werte preiszugeben.
    """

    # Konfiguration
    CONFIG_FILE_MISSING = "CONFIG_FILE_MISSING"
    CONFIG_NOT_READABLE = "CONFIG_NOT_READABLE"
    CONFIG_PARSE_ERROR = "CONFIG_PARSE_ERROR"
    CONFIG_SCHEMA_VERSION_UNSUPPORTED = "CONFIG_SCHEMA_VERSION_UNSUPPORTED"
    CONFIG_UNKNOWN_FIELD = "CONFIG_UNKNOWN_FIELD"
    CONFIG_MISSING_FIELD = "CONFIG_MISSING_FIELD"
    CONFIG_INVALID_VALUE = "CONFIG_INVALID_VALUE"
    CONFIG_TYPE_MISMATCH = "CONFIG_TYPE_MISMATCH"

    # Policies
    IDENTITIES_NOT_SEPARATED = "IDENTITIES_NOT_SEPARATED"
    IDENTITY_IS_ROOT = "IDENTITY_IS_ROOT"
    PRIVILEGED_PROCESS = "PRIVILEGED_PROCESS"
    EGRESS_NOT_DENY = "EGRESS_NOT_DENY"
    CANONICAL_WRITE_REQUESTED = "CANONICAL_WRITE_REQUESTED"
    SOURCE_ACTIVATION_REQUESTED = "SOURCE_ACTIVATION_REQUESTED"

    # Ports
    SECRET_RESOLUTION_NOT_IMPLEMENTED = "SECRET_RESOLUTION_NOT_IMPLEMENTED"
    EVIDENCE_WRITER_NOT_IMPLEMENTED = "EVIDENCE_WRITER_NOT_IMPLEMENTED"
    EGRESS_PORT_DENY_BY_DEFAULT = "EGRESS_PORT_DENY_BY_DEFAULT"

    # Runtime
    RUNTIME_SKELETON_ONLY = "RUNTIME_SKELETON_ONLY"
    SECURITY_GATE_NOT_ACCEPTED = "SECURITY_GATE_NOT_ACCEPTED"
    MAPPING_GATE_NOT_ACCEPTED = "MAPPING_GATE_NOT_ACCEPTED"
    SECRET_PROVIDER_UNCONFIGURED = "SECRET_PROVIDER_UNCONFIGURED"
    EVIDENCE_WRITER_UNCONFIGURED = "EVIDENCE_WRITER_UNCONFIGURED"


class CoreBrainError(Exception):
    """Basisklasse aller Skeleton-Fehler."""

    def __init__(self, reason: ReasonCode, detail: str = "") -> None:
        """Erzeugt einen Fehler mit stabilem Reason Code.

        Args:
            reason: Maschinenlesbare Begründung.
            detail: Kurze, wertfreie Ergänzung. Enthält niemals private Werte.
        """
        self.reason = reason
        self.detail = detail
        super().__init__(f"{reason.value}: {detail}" if detail else reason.value)


class ConfigError(CoreBrainError):
    """Die Konfiguration ist syntaktisch oder strukturell ungültig."""


class PolicyBlocked(CoreBrainError):
    """Eine fail-closed Policy hat die Ausführung verweigert."""


class PortRefused(CoreBrainError):
    """Ein Default-Port hat den Zugriff verweigert."""


class RuntimeStartBlocked(CoreBrainError):
    """Der Start der operativen Runtime ist verweigert."""
