"""Fail-closed Orchestrierung der Ingest-Quarantäne (CBP-WP-013).

Die Pipeline behandelt **genau ein** ausdrücklich angegebenes Artefakt je
Intake. Sie setzt die **Synthetic-only-Grenze** technisch durch, validiert die
Eingabe strukturell **vor** dem Lesen, liest den Inhalt **einmal**, führt den
Baseline-Scan aus und erzeugt einen minimierten Record. Sie führt **keine**
Freigabe, Promotion, Indexierung oder Aufnahme aus.

Uhr und Leseoperation sind injizierbar, damit die Evidenz deterministisch
prüfbar bleibt. Der Import dieses Moduls hat keine Nebenwirkungen.
"""

from __future__ import annotations

import hashlib
import os
import stat
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from ..errors import QuarantineInputRejected, ReasonCode
from .models import (
    MEDIA_TYPE_BY_SUFFIX,
    RECORD_SCHEMA_VERSION,
    QuarantinePolicy,
    QuarantineRecord,
    ScanResult,
    ScanStatus,
)
from .scanner import content_findings, status_from_findings, structural_findings
from .store import QuarantineStore

__all__ = [
    "Clock",
    "StageOutcome",
    "SYNTHETIC_SOURCE_PREFIX",
    "run_scan",
    "run_stage",
    "default_clock",
]

Clock = Callable[[], datetime]
"""Signatur einer injizierbaren Uhr. Liefert einen ``datetime``."""

SYNTHETIC_SOURCE_PREFIX = "synthetic:"
"""Pflichtpräfix jeder opaken Source Reference im MVP."""

_SAFE_SOURCE_REF = set(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.:_-"
)
_O_NOFOLLOW = getattr(os, "O_NOFOLLOW", 0)


@dataclass(frozen=True, slots=True)
class StageOutcome:
    """Ergebnis von ``run_stage``.

    ``record`` ist ``None``, wenn der Scan ``BLOCKED`` ergab — in diesem Fall
    wird **kein** Payload und **kein** Manifest gespeichert (fail-closed).
    """

    scan: ScanResult
    record: QuarantineRecord | None


def default_clock() -> datetime:
    """Gibt die aktuelle UTC-Zeit zurück."""
    return datetime.now(UTC)


def run_scan(
    *,
    input_path: Path,
    policy: QuarantinePolicy,
    source_reference: str,
    synthetic_confirmed: bool,
) -> ScanResult:
    """Scannt genau ein Artefakt, ohne etwas zu speichern.

    Args:
        input_path: Ausdrücklicher Pfad zur einzelnen Eingabedatei.
        policy: Die validierte Policy.
        source_reference: Opake Referenz mit ``synthetic:``-Präfix.
        synthetic_confirmed: Ob ``--synthetic-test-only`` gesetzt wurde.

    Returns:
        Das minimierte :class:`ScanResult`.

    Raises:
        QuarantineInputRejected: Synthetic-Grenze verletzt, Datei fehlt oder
            Dateiidentität ändert sich zwischen Prüfung und Lesen.
    """
    scan, _ = _evaluate(
        input_path=input_path,
        policy=policy,
        source_reference=source_reference,
        synthetic_confirmed=synthetic_confirmed,
    )
    return scan


def run_stage(
    *,
    input_path: Path,
    policy: QuarantinePolicy,
    source_reference: str,
    synthetic_confirmed: bool,
    store: QuarantineStore,
    clock: Clock = default_clock,
) -> StageOutcome:
    """Scannt und speichert Payload und Record — **ohne** Promotion.

    Ein ``BLOCKED``-Scan speichert **nichts**. ``REVIEW_REQUIRED`` und
    ``READY_FOR_HUMAN_REVIEW`` speichern genau ein Objekt und genau einen
    Record.

    Args:
        input_path: Ausdrücklicher Pfad zur einzelnen Eingabedatei.
        policy: Die validierte Policy.
        source_reference: Opake Referenz mit ``synthetic:``-Präfix.
        synthetic_confirmed: Ob ``--synthetic-test-only`` gesetzt wurde.
        store: Der Zielspeicher.
        clock: Injizierbare Uhr für ``created_at``.

    Returns:
        Ein :class:`StageOutcome`. ``record`` ist ``None`` bei ``BLOCKED``.

    Raises:
        QuarantineInputRejected: Wie :func:`run_scan`.
        QuarantineStoreError: Bei Store-Kollision oder Root-Verstoß.
    """
    scan, payload = _evaluate(
        input_path=input_path,
        policy=policy,
        source_reference=source_reference,
        synthetic_confirmed=synthetic_confirmed,
    )

    if scan.status is ScanStatus.BLOCKED or payload is None:
        # fail-closed: blockierte Artefakte werden nicht persistiert.
        return StageOutcome(scan=scan, record=None)

    object_reference = store.write_object(scan.content_sha256, payload)
    record = _build_record(
        scan=scan,
        source_reference=source_reference,
        policy=policy,
        object_reference=object_reference,
        clock=clock,
    )
    store.write_record(record)
    return StageOutcome(scan=scan, record=record)


# -- interne Orchestrierung -----------------------------------------------


def _evaluate(
    *,
    input_path: Path,
    policy: QuarantinePolicy,
    source_reference: str,
    synthetic_confirmed: bool,
) -> tuple[ScanResult, bytes | None]:
    """Führt Synthetic-Gate, Strukturprüfung, Lesen und Scan aus."""
    _enforce_synthetic_gate(source_reference, synthetic_confirmed)

    pre = _lstat_or_reject(input_path)
    is_symlink = stat.S_ISLNK(pre.st_mode)
    is_regular = stat.S_ISREG(pre.st_mode) and not is_symlink
    suffix = input_path.suffix.lower()
    media_type = MEDIA_TYPE_BY_SUFFIX.get(suffix, "application/octet-stream")

    structural = structural_findings(
        is_symlink=is_symlink,
        is_regular_file=is_regular,
        suffix=suffix,
        size=pre.st_size,
        policy=policy,
    )
    if structural:
        # fail-closed: bei strukturellem Blocker wird nichts gelesen.
        result = ScanResult(
            status=status_from_findings(structural),
            findings=tuple(structural),
            content_sha256="",
            byte_size=max(pre.st_size, 0),
            media_type=media_type,
        )
        return result, None

    payload = _read_once(input_path, pre)
    findings = content_findings(payload, policy)
    digest = hashlib.sha256(payload).hexdigest()
    result = ScanResult(
        status=status_from_findings(findings),
        findings=tuple(findings),
        content_sha256=digest,
        byte_size=len(payload),
        media_type=media_type,
    )
    return result, payload


def _enforce_synthetic_gate(source_reference: str, synthetic_confirmed: bool) -> None:
    """Setzt die Synthetic-only-Grenze durch (raise on failure)."""
    if not synthetic_confirmed:
        raise QuarantineInputRejected(
            ReasonCode.QUARANTINE_SYNTHETIC_CONFIRMATION_MISSING,
            "synthetic-test-only confirmation is required",
        )
    if not source_reference or any(c not in _SAFE_SOURCE_REF for c in source_reference):
        raise QuarantineInputRejected(
            ReasonCode.QUARANTINE_SOURCE_REF_INVALID,
            "source reference contains unsafe characters",
        )
    if not source_reference.startswith(SYNTHETIC_SOURCE_PREFIX):
        raise QuarantineInputRejected(
            ReasonCode.QUARANTINE_SOURCE_REF_NOT_SYNTHETIC,
            "source reference must start with 'synthetic:'",
        )
    if len(source_reference) <= len(SYNTHETIC_SOURCE_PREFIX):
        raise QuarantineInputRejected(
            ReasonCode.QUARANTINE_SOURCE_REF_INVALID,
            "source reference has no opaque identifier",
        )


def _lstat_or_reject(path: Path) -> os.stat_result:
    """Ermittelt ``lstat`` oder weist einen fehlenden Pfad ab."""
    try:
        return path.lstat()
    except (OSError, ValueError) as exc:
        raise QuarantineInputRejected(
            ReasonCode.QUARANTINE_INPUT_NOT_FOUND, "input not found"
        ) from exc


def _read_once(path: Path, pre: os.stat_result) -> bytes:
    """Liest die Datei genau einmal und verweigert bei Identitätswechsel.

    Öffnet ``O_NOFOLLOW`` (wo verfügbar), vergleicht ``fstat`` gegen die
    Vorprüfung und liest anschließend den Inhalt. Der Inhalt wird von dieser
    Funktion **nicht** ausgegeben.
    """
    fd = os.open(path, os.O_RDONLY | _O_NOFOLLOW)
    try:
        post = os.fstat(fd)
        if (post.st_ino, post.st_dev, post.st_size, post.st_mtime_ns) != (
            pre.st_ino,
            pre.st_dev,
            pre.st_size,
            pre.st_mtime_ns,
        ):
            raise QuarantineInputRejected(
                ReasonCode.QUARANTINE_INPUT_CHANGED,
                "file identity changed between check and read",
            )
        if not stat.S_ISREG(post.st_mode):
            raise QuarantineInputRejected(
                ReasonCode.QUARANTINE_INPUT_CHANGED, "input is no longer a regular file"
            )
        with os.fdopen(fd, "rb", closefd=True) as handle:
            fd = -1
            return handle.read()
    finally:
        if fd != -1:
            os.close(fd)


def _build_record(
    *,
    scan: ScanResult,
    source_reference: str,
    policy: QuarantinePolicy,
    object_reference: str,
    clock: Clock,
) -> QuarantineRecord:
    """Baut den minimierten, kanonischen Record."""
    quarantine_id = _quarantine_id(
        source_reference, scan.content_sha256, policy.policy_sha256
    )
    return QuarantineRecord(
        record_schema_version=RECORD_SCHEMA_VERSION,
        quarantine_id=quarantine_id,
        source_reference=source_reference,
        content_sha256=scan.content_sha256,
        byte_size=scan.byte_size,
        media_type=scan.media_type,
        policy_schema_version=policy.schema_version,
        policy_sha256=policy.policy_sha256,
        scan_status=scan.status,
        finding_codes=scan.finding_codes,
        finding_count=len(scan.finding_codes),
        stored_object_reference=object_reference,
        created_at=_utc_iso(clock()),
    )


def _quarantine_id(source_reference: str, content_sha256: str, policy_sha256: str) -> str:
    """Leitet eine deterministische Quarantäne-ID aus nicht geheimen Werten ab."""
    material = f"{source_reference}\n{content_sha256}\n{policy_sha256}"
    return hashlib.sha256(material.encode("utf-8")).hexdigest()


def _utc_iso(moment: datetime) -> str:
    """Normalisiert einen ``datetime`` auf ISO-8601-UTC mit ``Z``."""
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=UTC)
    text = moment.astimezone(UTC).isoformat()
    return text.replace("+00:00", "Z")
