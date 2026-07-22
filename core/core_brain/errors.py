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
    "QuarantinePolicyError",
    "QuarantineInputRejected",
    "QuarantineStoreError",
    "QuarantineReleaseBlocked",
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
    # CBP-WP-013 — Ingest-Quarantäne. Neue, stabile Prozessausgänge.
    QUARANTINE_REVIEW_REQUIRED = "QUARANTINE_REVIEW_REQUIRED"
    QUARANTINE_BLOCKED = "QUARANTINE_BLOCKED"
    QUARANTINE_RELEASE_BLOCKED = "QUARANTINE_RELEASE_BLOCKED"
    USAGE_ERROR = "USAGE_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"


EXIT_CODES: dict[ExitCode, int] = {
    ExitCode.OK: 0,
    ExitCode.CONFIG_INVALID: 2,
    ExitCode.POLICY_BLOCKED: 3,
    ExitCode.RUNTIME_START_BLOCKED: 4,
    ExitCode.QUARANTINE_REVIEW_REQUIRED: 5,
    ExitCode.QUARANTINE_BLOCKED: 6,
    ExitCode.QUARANTINE_RELEASE_BLOCKED: 7,
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

    # CBP-WP-013 — Ingest-Quarantäne. Policy.
    QUARANTINE_POLICY_FILE_MISSING = "QUARANTINE_POLICY_FILE_MISSING"
    QUARANTINE_POLICY_NOT_READABLE = "QUARANTINE_POLICY_NOT_READABLE"
    QUARANTINE_POLICY_PARSE_ERROR = "QUARANTINE_POLICY_PARSE_ERROR"
    QUARANTINE_POLICY_SCHEMA_UNSUPPORTED = "QUARANTINE_POLICY_SCHEMA_UNSUPPORTED"
    QUARANTINE_POLICY_UNKNOWN_FIELD = "QUARANTINE_POLICY_UNKNOWN_FIELD"
    QUARANTINE_POLICY_MISSING_FIELD = "QUARANTINE_POLICY_MISSING_FIELD"
    QUARANTINE_POLICY_INVALID_VALUE = "QUARANTINE_POLICY_INVALID_VALUE"
    QUARANTINE_POLICY_RELEASE_ENABLED = "QUARANTINE_POLICY_RELEASE_ENABLED"
    QUARANTINE_POLICY_NETWORK_ENABLED = "QUARANTINE_POLICY_NETWORK_ENABLED"

    # CBP-WP-013 — Ingest-Quarantäne. Synthetic-only-Grenze und Intake.
    QUARANTINE_SYNTHETIC_CONFIRMATION_MISSING = (
        "QUARANTINE_SYNTHETIC_CONFIRMATION_MISSING"
    )
    QUARANTINE_SOURCE_REF_NOT_SYNTHETIC = "QUARANTINE_SOURCE_REF_NOT_SYNTHETIC"
    QUARANTINE_SOURCE_REF_INVALID = "QUARANTINE_SOURCE_REF_INVALID"
    QUARANTINE_INPUT_NOT_FOUND = "QUARANTINE_INPUT_NOT_FOUND"
    QUARANTINE_INPUT_CHANGED = "QUARANTINE_INPUT_CHANGED"

    # CBP-WP-013 — Ingest-Quarantäne. Scanergebnis.
    QUARANTINE_SCAN_BLOCKED = "QUARANTINE_SCAN_BLOCKED"
    QUARANTINE_SCAN_REVIEW_REQUIRED = "QUARANTINE_SCAN_REVIEW_REQUIRED"

    # CBP-WP-013 — Ingest-Quarantäne. Store und Record.
    QUARANTINE_STORE_INSIDE_REPOSITORY = "QUARANTINE_STORE_INSIDE_REPOSITORY"
    QUARANTINE_STORE_IS_SYMLINK = "QUARANTINE_STORE_IS_SYMLINK"
    QUARANTINE_STORE_ROOT_INVALID = "QUARANTINE_STORE_ROOT_INVALID"
    QUARANTINE_STORE_WRITE_OUTSIDE_ROOT = "QUARANTINE_STORE_WRITE_OUTSIDE_ROOT"
    QUARANTINE_OBJECT_HASH_COLLISION = "QUARANTINE_OBJECT_HASH_COLLISION"
    QUARANTINE_RECORD_COLLISION = "QUARANTINE_RECORD_COLLISION"
    QUARANTINE_RECORD_NOT_FOUND = "QUARANTINE_RECORD_NOT_FOUND"
    QUARANTINE_RECORD_INVALID = "QUARANTINE_RECORD_INVALID"

    # CBP-WP-013 — Ingest-Quarantäne. Freigabe verweigert.
    QUARANTINE_RELEASE_ALWAYS_BLOCKED = "QUARANTINE_RELEASE_ALWAYS_BLOCKED"


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


class QuarantinePolicyError(CoreBrainError):
    """Die Quarantäne-Policy ist syntaktisch oder strukturell ungültig."""


class QuarantineInputRejected(CoreBrainError):
    """Ein Intake wurde vor oder während der Prüfung fail-closed abgewiesen.

    Die Ausnahme trägt **keinen** Eingabepfad, keinen Dateinamen und keinen
    Inhaltsauszug — ausschließlich einen stabilen Reason Code.
    """


class QuarantineStoreError(CoreBrainError):
    """Eine Store-Operation wurde fail-closed verweigert.

    Trägt keinen absoluten Pfad und keinen Payload — nur einen Reason Code.
    """


class QuarantineReleaseBlocked(CoreBrainError):
    """``quarantine release`` verweigert unabhängig vom Recordstatus."""
