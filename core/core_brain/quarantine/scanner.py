"""Deterministischer, lokaler Baseline-Scanner (CBP-WP-013).

Der Scanner arbeitet ausschließlich mit der Python-Standardbibliothek und
liefert bei identischer Eingabe identische Befunde. Er erhebt **keinen**
Anspruch auf vollständige Secret-, PII-, Datenschutz- oder
Klassifikationserkennung — jeder Befund ist ein **Indikator**, keine
Tatsachenbehauptung über ein echtes Secret oder eine echte Person.

Befunde enthalten **niemals** einen Inhaltsauszug, einen Pfad, einen Wert
oder personenbezogene Daten — höchstens einen stabilen Code, die Schwere und
eine normalisierte Zeilennummer. Die Erkennungsmuster sind fest verdrahtet;
es gibt **keine** frei konfigurierbaren regulären Ausdrücke.

Der Import dieses Moduls hat keine Nebenwirkungen.
"""

from __future__ import annotations

import re
from typing import Final

from .models import (
    Finding,
    FindingCode,
    QuarantinePolicy,
    ScanStatus,
    severity_of,
)

__all__ = [
    "SYNTHETIC_MARKER",
    "structural_findings",
    "content_findings",
    "status_from_findings",
]

SYNTHETIC_MARKER: Final[str] = "<!-- synthetic-test-only -->"
"""Pflichtmarker jedes synthetischen Testartefakts."""

# Credential-Schlüsselwörter. Feste Liste, keine Konfiguration.
_CREDENTIAL_KEYWORDS: Final[frozenset[str]] = frozenset(
    {
        "password",
        "passwd",
        "pwd",
        "secret",
        "token",
        "apikey",
        "api_key",
        "accesskey",
        "access_key",
        "secretkey",
        "secret_key",
        "privatekey",
        "private_key",
        "client_secret",
        "auth_token",
        "bearer",
    }
)

# Private-Key-Marker aus sicheren Teilstrings zusammengesetzt. Es wird kein
# realistischer Schlüssel und kein Schlüsselkörper verwendet.
_PK_FRAGMENT_A: Final[str] = "PRIVATE"
_PK_FRAGMENT_B: Final[str] = "KEY"
_PK_NEEDLE: Final[str] = f"{_PK_FRAGMENT_A} {_PK_FRAGMENT_B}"

# Feste interne Erkennungsmuster (nicht konfigurierbar).
_TRAILING_IDENT: Final[re.Pattern[str]] = re.compile(r"([A-Za-z0-9_]+)\s*$")
_EMAIL_RE: Final[re.Pattern[str]] = re.compile(
    r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}"
)
_PHONE_CANDIDATE_RE: Final[re.Pattern[str]] = re.compile(r"\+?[\d][\d\s().\-]{5,}\d")

# Erlaubte Steuerzeichen im Text: Tab, Zeilenvorschub, Wagenrücklauf.
_ALLOWED_CONTROL: Final[frozenset[int]] = frozenset({0x09, 0x0A, 0x0D})


def structural_findings(
    *,
    is_symlink: bool,
    is_regular_file: bool,
    suffix: str,
    size: int,
    policy: QuarantinePolicy,
) -> list[Finding]:
    """Ermittelt strukturelle Blocking-Befunde aus Metadaten.

    Diese Prüfungen benötigen **keinen** Inhalt und werden vor dem Lesen
    ausgeführt. Ein Device, eine Named Pipe oder ein Verzeichnis ist kein
    ``regular file`` und erzeugt daher ``QF-STRUCTURE-NOT-REGULAR``.

    Args:
        is_symlink: Ob der Pfad ein Symlink ist (aus ``lstat``).
        is_regular_file: Ob der Pfad eine reguläre Datei ist.
        suffix: Kleingeschriebenes Dateisuffix inklusive Punkt.
        size: Dateigröße in Bytes.
        policy: Die geltende Policy.

    Returns:
        Eine Liste struktureller Befunde. Leer, wenn strukturell in Ordnung.
    """
    findings: list[Finding] = []

    if policy.reject_symlinks and is_symlink:
        findings.append(_blocking(FindingCode.STRUCTURE_SYMLINK))

    if policy.require_regular_file and not is_regular_file:
        findings.append(_blocking(FindingCode.STRUCTURE_NOT_REGULAR))

    if suffix.lower() not in policy.allowed_suffixes:
        findings.append(_blocking(FindingCode.STRUCTURE_SUFFIX))

    if size <= 0:
        findings.append(_blocking(FindingCode.STRUCTURE_EMPTY))
    elif size > policy.max_bytes:
        findings.append(_blocking(FindingCode.STRUCTURE_SIZE))

    return findings


def content_findings(raw: bytes, policy: QuarantinePolicy) -> list[Finding]:
    """Ermittelt Kodierungs-, Inhalts-, Credential- und PII-Befunde.

    Args:
        raw: Die gelesenen Rohbytes genau eines Artefakts.
        policy: Die geltende Policy.

    Returns:
        Eine Liste von Befunden. Der Rückgabewert enthält keinen Inhalt.
    """
    findings: list[Finding] = []

    # NUL-Prüfung auf Byteebene.
    if policy.reject_nul and b"\x00" in raw:
        findings.append(_blocking(FindingCode.CONTENT_NUL))

    # Striktes UTF-8. Schlägt die Dekodierung fehl, sind keine Textprüfungen
    # möglich — der Befund blockiert.
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        if policy.require_utf8:
            findings.append(_blocking(FindingCode.ENCODING_UTF8))
        return findings

    # Unerlaubte Steuerzeichen werden wie eine Kodierungsverletzung behandelt.
    if policy.require_utf8 and _has_disallowed_control(text):
        findings.append(_blocking(FindingCode.ENCODING_UTF8))

    # Synthetic-Marker ist Pflicht.
    if SYNTHETIC_MARKER not in text:
        findings.append(_blocking(FindingCode.SYNTHETIC_MARKER_MISSING))

    lines = text.splitlines()

    if policy.block_private_key_markers:
        for number, line in enumerate(lines, start=1):
            if _PK_NEEDLE in line.upper() and "BEGIN" in line.upper():
                findings.append(
                    _blocking(FindingCode.CREDENTIAL_PRIVATE_KEY_MARKER, line=number)
                )
                break

    if policy.block_credential_assignments:
        for number, line in enumerate(lines, start=1):
            if _is_credential_assignment(line):
                findings.append(
                    _blocking(FindingCode.CREDENTIAL_ASSIGNMENT, line=number)
                )
                break

    if policy.review_email_indicators:
        for number, line in enumerate(lines, start=1):
            if _EMAIL_RE.search(line):
                findings.append(
                    _review(FindingCode.PII_EMAIL_INDICATOR, line=number)
                )
                break

    if policy.review_phone_indicators:
        for number, line in enumerate(lines, start=1):
            if _looks_like_phone(line):
                findings.append(
                    _review(FindingCode.PII_PHONE_INDICATOR, line=number)
                )
                break

    return findings


def status_from_findings(findings: list[Finding]) -> ScanStatus:
    """Leitet den Ergebniszustand aus den Befunden ab.

    Ein einziger Blocking-Befund erzeugt ``BLOCKED``. Ausschließlich
    Review-Befunde erzeugen ``REVIEW_REQUIRED``. Keine Befunde erzeugen
    ``READY_FOR_HUMAN_REVIEW`` — niemals eine Freigabe.

    Args:
        findings: Alle strukturellen und inhaltlichen Befunde.

    Returns:
        Der abgeleitete :class:`ScanStatus`.
    """
    from .models import FindingSeverity

    if any(f.severity is FindingSeverity.BLOCKING for f in findings):
        return ScanStatus.BLOCKED
    if any(f.severity is FindingSeverity.REVIEW for f in findings):
        return ScanStatus.REVIEW_REQUIRED
    return ScanStatus.READY_FOR_HUMAN_REVIEW


def _blocking(code: FindingCode, *, line: int | None = None) -> Finding:
    """Baut einen Blocking-Befund."""
    return Finding(code=code, severity=severity_of(code), line=line)


def _review(code: FindingCode, *, line: int | None = None) -> Finding:
    """Baut einen Review-Befund."""
    return Finding(code=code, severity=severity_of(code), line=line)


def _has_disallowed_control(text: str) -> bool:
    """Prüft auf Steuerzeichen außerhalb von Tab, LF und CR."""
    for char in text:
        code = ord(char)
        if code < 0x20 and code not in _ALLOWED_CONTROL:
            return True
    return False


def _is_credential_assignment(line: str) -> bool:
    """Erkennt eine Credential-Zuweisung deterministisch.

    Sucht das erste ``=`` oder ``:``, prüft den letzten Bezeichner links davon
    gegen die feste Schlüsselwortliste und verlangt einen nicht leeren Wert.
    """
    position = _first_assignment_position(line)
    if position is None:
        return False
    left, right = line[:position], line[position + 1 :]
    if not right.strip():
        return False
    match = _TRAILING_IDENT.search(left)
    if match is None:
        return False
    return match.group(1).lower() in _CREDENTIAL_KEYWORDS


def _first_assignment_position(line: str) -> int | None:
    """Gibt die Position des ersten ``=`` oder ``:`` zurück."""
    positions = [line.find(char) for char in ("=", ":") if char in line]
    return min(positions) if positions else None


def _looks_like_phone(line: str) -> bool:
    """Erkennt eine telefonartige Ziffernfolge (7 bis 15 Ziffern)."""
    for candidate in _PHONE_CANDIDATE_RE.findall(line):
        digits = sum(1 for char in candidate if char.isdigit())
        if 7 <= digits <= 15:
            return True
    return False
