"""Datenmodelle der Ingest-Quarantäne (CBP-WP-013).

Alle Modelle sind unveränderlich. Sie enthalten **niemals**:

- einen Eingabepfad oder Dateinamen,
- einen Inhaltsauszug (Snippet),
- einen Secret-Wert,
- personenbezogene Inhalte.

Ein Finding trägt höchstens einen stabilen Code, eine Schwere und eine
normalisierte Zeilennummer. Der Import dieses Moduls hat keine
Nebenwirkungen.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

__all__ = [
    "POLICY_SCHEMA_VERSION",
    "RECORD_SCHEMA_VERSION",
    "IMPLEMENTATION_VERSION",
    "MEDIA_TYPE_BY_SUFFIX",
    "FindingSeverity",
    "FindingCode",
    "ScanStatus",
    "Finding",
    "QuarantinePolicy",
    "ScanResult",
    "QuarantineRecord",
    "RECORD_FIELDS",
    "severity_of",
]

POLICY_SCHEMA_VERSION = "1.0"
"""Einzige unterstützte Policy-Schema-Version. Jede andere blockiert."""

RECORD_SCHEMA_VERSION = "1.0"
"""Schema-Version des Quarantänerecords."""

IMPLEMENTATION_VERSION = "0.1.0.dev0"
"""Version des Quarantäneprototyps. Identisch mit dem Runtime Skeleton."""

MEDIA_TYPE_BY_SUFFIX: dict[str, str] = {".md": "text/markdown"}
"""Zulässige Suffixe des MVP und ihr abgeleiteter Medientyp."""


class FindingSeverity(StrEnum):
    """Schwere eines Scan-Befunds.

    ``BLOCKING`` erzeugt den Zustand ``BLOCKED``. ``REVIEW`` erzeugt für sich
    genommen ``REVIEW_REQUIRED`` — niemals eine Freigabe.
    """

    BLOCKING = "BLOCKING"
    REVIEW = "REVIEW"


class FindingCode(StrEnum):
    """Stabile, global eindeutige Befundcodes im ``QF-``-Namensraum.

    Ein Code wird nach seiner Dokumentation nicht mehr umbenannt. Die Codes
    kollidieren nicht mit den Reason Codes aus :mod:`core.core_brain.errors`,
    weil ausschließlich Befunde das Präfix ``QF-`` tragen.
    """

    # Blocking — Struktur.
    STRUCTURE_NOT_REGULAR = "QF-STRUCTURE-NOT-REGULAR"
    STRUCTURE_SYMLINK = "QF-STRUCTURE-SYMLINK"
    STRUCTURE_SUFFIX = "QF-STRUCTURE-SUFFIX"
    STRUCTURE_SIZE = "QF-STRUCTURE-SIZE"
    STRUCTURE_EMPTY = "QF-STRUCTURE-EMPTY"
    # Blocking — Kodierung und Inhalt.
    ENCODING_UTF8 = "QF-ENCODING-UTF8"
    CONTENT_NUL = "QF-CONTENT-NUL"
    SYNTHETIC_MARKER_MISSING = "QF-SYNTHETIC-MARKER-MISSING"
    # Blocking — Credential-Indikatoren.
    CREDENTIAL_PRIVATE_KEY_MARKER = "QF-CREDENTIAL-PRIVATE-KEY-MARKER"
    CREDENTIAL_ASSIGNMENT = "QF-CREDENTIAL-ASSIGNMENT"
    # Review — PII-Indikatoren.
    PII_EMAIL_INDICATOR = "QF-PII-EMAIL-INDICATOR"
    PII_PHONE_INDICATOR = "QF-PII-PHONE-INDICATOR"


_BLOCKING_CODES: frozenset[FindingCode] = frozenset(
    {
        FindingCode.STRUCTURE_NOT_REGULAR,
        FindingCode.STRUCTURE_SYMLINK,
        FindingCode.STRUCTURE_SUFFIX,
        FindingCode.STRUCTURE_SIZE,
        FindingCode.STRUCTURE_EMPTY,
        FindingCode.ENCODING_UTF8,
        FindingCode.CONTENT_NUL,
        FindingCode.SYNTHETIC_MARKER_MISSING,
        FindingCode.CREDENTIAL_PRIVATE_KEY_MARKER,
        FindingCode.CREDENTIAL_ASSIGNMENT,
    }
)


def severity_of(code: FindingCode) -> FindingSeverity:
    """Gibt die feste Schwere eines Befundcodes zurück.

    Args:
        code: Der Befundcode.

    Returns:
        ``BLOCKING`` für strukturelle, Kodierungs-, Inhalts- und
        Credential-Codes; ``REVIEW`` für PII-Indikatoren.
    """
    if code in _BLOCKING_CODES:
        return FindingSeverity.BLOCKING
    return FindingSeverity.REVIEW


class ScanStatus(StrEnum):
    """Die einzigen drei Ergebniszustände des MVP.

    Kein Zustand bedeutet ``approved``, ``released``, ``enabled`` oder
    ``indexed``. Ein erfolgreicher Scan ist keine Human-Freigabe.
    """

    READY_FOR_HUMAN_REVIEW = "READY_FOR_HUMAN_REVIEW"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True, slots=True, order=True)
class Finding:
    """Ein einzelner Scan-Befund.

    Trägt ausschließlich einen stabilen Code, die Schwere und optional eine
    normalisierte 1-basierte Zeilennummer. **Kein** Snippet, **kein** Pfad,
    **kein** Wert.
    """

    code: FindingCode
    severity: FindingSeverity
    line: int | None = None

    def to_dict(self) -> dict[str, str | int | None]:
        """Gibt eine JSON-taugliche, minimierte Darstellung zurück."""
        return {
            "code": self.code.value,
            "severity": self.severity.value,
            "line": self.line,
        }


@dataclass(frozen=True, slots=True)
class QuarantinePolicy:
    """Validierte, fail-closed Quarantäne-Policy.

    Eine Instanz entsteht ausschließlich über
    :func:`core.core_brain.quarantine.policy.load_policy`. Ihr Vorhandensein
    bedeutet strukturelle Gültigkeit, keine Betriebsfreigabe.
    """

    schema_version: str
    max_bytes: int
    allowed_suffixes: tuple[str, ...]
    reject_symlinks: bool
    require_regular_file: bool
    require_utf8: bool
    reject_nul: bool
    block_private_key_markers: bool
    block_credential_assignments: bool
    review_email_indicators: bool
    review_phone_indicators: bool
    release_enabled: bool
    network_enabled: bool
    policy_sha256: str

    def to_dict(self) -> dict[str, object]:
        """Gibt eine deterministische, JSON-taugliche Darstellung zurück."""
        return {
            "schema_version": self.schema_version,
            "max_bytes": self.max_bytes,
            "allowed_suffixes": list(self.allowed_suffixes),
            "reject_symlinks": self.reject_symlinks,
            "require_regular_file": self.require_regular_file,
            "require_utf8": self.require_utf8,
            "reject_nul": self.reject_nul,
            "block_private_key_markers": self.block_private_key_markers,
            "block_credential_assignments": self.block_credential_assignments,
            "review_email_indicators": self.review_email_indicators,
            "review_phone_indicators": self.review_phone_indicators,
            "release_enabled": self.release_enabled,
            "network_enabled": self.network_enabled,
            "policy_sha256": self.policy_sha256,
        }


@dataclass(frozen=True, slots=True)
class ScanResult:
    """Ergebnis eines Baseline-Scans über genau ein Artefakt.

    Enthält den Status, die sortierten und deduplizierten Befunde sowie
    minimierte, nicht sensible Metadaten. **Kein** Pfad, **kein** Inhalt.
    """

    status: ScanStatus
    findings: tuple[Finding, ...]
    content_sha256: str
    byte_size: int
    media_type: str

    @property
    def finding_codes(self) -> tuple[str, ...]:
        """Sortierte, deduplizierte Befundcodes."""
        return tuple(sorted({f.code.value for f in self.findings}))

    def to_dict(self) -> dict[str, object]:
        """Gibt eine minimierte, JSON-taugliche Darstellung zurück."""
        return {
            "status": self.status.value,
            "finding_codes": list(self.finding_codes),
            "finding_count": len(self.finding_codes),
            "findings": [f.to_dict() for f in sorted(self.findings)],
            "content_sha256": self.content_sha256,
            "byte_size": self.byte_size,
            "media_type": self.media_type,
        }


@dataclass(frozen=True, slots=True)
class QuarantineRecord:
    """Kanonischer, minimierter Quarantänerecord.

    Der Record enthält **niemals** einen Eingabepfad, einen Dateinamen, einen
    Inhaltsauszug oder einen Secret-Wert. ``source_reference`` ist opak und
    beginnt im MVP mit ``synthetic:``.
    """

    record_schema_version: str
    quarantine_id: str
    source_reference: str
    content_sha256: str
    byte_size: int
    media_type: str
    policy_schema_version: str
    policy_sha256: str
    scan_status: ScanStatus
    finding_codes: tuple[str, ...]
    finding_count: int
    stored_object_reference: str
    created_at: str
    implementation_version: str = IMPLEMENTATION_VERSION

    def to_dict(self) -> dict[str, object]:
        """Gibt die kanonische, deterministisch sortierbare Darstellung zurück.

        Die Schlüssel werden beim Serialisieren sortiert (siehe Store). Diese
        Methode liefert alle Felder ohne Pfad und ohne Inhalt.
        """
        return {
            "record_schema_version": self.record_schema_version,
            "quarantine_id": self.quarantine_id,
            "source_reference": self.source_reference,
            "content_sha256": self.content_sha256,
            "byte_size": self.byte_size,
            "media_type": self.media_type,
            "policy_schema_version": self.policy_schema_version,
            "policy_sha256": self.policy_sha256,
            "scan_status": self.scan_status.value,
            "finding_codes": list(self.finding_codes),
            "finding_count": self.finding_count,
            "stored_object_reference": self.stored_object_reference,
            "created_at": self.created_at,
            "implementation_version": self.implementation_version,
        }


RECORD_FIELDS: frozenset[str] = frozenset(
    {
        "record_schema_version",
        "quarantine_id",
        "source_reference",
        "content_sha256",
        "byte_size",
        "media_type",
        "policy_schema_version",
        "policy_sha256",
        "scan_status",
        "finding_codes",
        "finding_count",
        "stored_object_reference",
        "created_at",
        "implementation_version",
    }
)
"""Alle Pflichtfelder eines Records. Unbekannte Felder blockieren."""
