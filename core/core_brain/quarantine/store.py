"""Lokaler content-addressed Quarantänespeicher (CBP-WP-013).

Der Store legt genau ein unveränderliches Payload-Objekt und ein kanonisches
JSON-Manifest ab. Objektpfade werden **ausschließlich** aus einem validierten
SHA-256-Digest abgeleitet — niemals aus einem Eingabepfad.

Grenzen und Zusicherungen:

- Der Store-Root wird **explizit** angegeben und liegt **außerhalb** des
  Core-Repositorys.
- Ein Symlink als Root wird abgewiesen.
- Es wird **nichts außerhalb** des Store-Roots geschrieben.
- Schreibvorgänge sind atomar (Temp-Datei plus ``os.replace``).
- Ein identisches Objekt macht die Operation idempotent.
- Ein abweichender Inhalt unter derselben Identität blockiert.
- Es werden keine Hardlinks oder Symlinks erzeugt.

Der Store ist **weder Canonical Source noch RT-2** und **keine** produktive
Sicherheitsgrenze. ``.gitignore`` und OS-Rechte sind hier nicht durchgesetzt.

Der Import dieses Moduls hat keine Nebenwirkungen.
"""

from __future__ import annotations

import itertools
import json
import os
import re
from pathlib import Path
from typing import Final

from ..errors import QuarantineStoreError, ReasonCode
from .models import RECORD_FIELDS, QuarantineRecord, ScanStatus

__all__ = ["QuarantineStore"]

_REPO_ROOT: Final[Path] = Path(__file__).resolve().parents[3]
_HEX_DIGEST: Final[re.Pattern[str]] = re.compile(r"\A[0-9a-f]{64}\Z")
_HEX_ID: Final[re.Pattern[str]] = re.compile(r"\A[0-9a-f]{16,64}\Z")
_temp_counter = itertools.count()


class QuarantineStore:
    """Ein content-addressed Store unter einem expliziten Root-Pfad."""

    def __init__(self, root: Path) -> None:
        """Öffnet oder legt den Store an und validiert den Root.

        Args:
            root: Ausdrücklicher Store-Root. Liegt außerhalb des Repositorys.

        Raises:
            QuarantineStoreError: Root ist ein Symlink, liegt im Repository
                oder ist strukturell unzulässig.
        """
        if root.is_symlink():
            raise QuarantineStoreError(ReasonCode.QUARANTINE_STORE_IS_SYMLINK, "root")

        resolved = root.resolve()
        if resolved == _REPO_ROOT or resolved.is_relative_to(_REPO_ROOT):
            raise QuarantineStoreError(
                ReasonCode.QUARANTINE_STORE_INSIDE_REPOSITORY, "root"
            )

        if resolved.exists() and not resolved.is_dir():
            raise QuarantineStoreError(
                ReasonCode.QUARANTINE_STORE_ROOT_INVALID, "root is not a directory"
            )

        resolved.mkdir(parents=True, exist_ok=True)
        (resolved / "objects" / "sha256").mkdir(parents=True, exist_ok=True)
        (resolved / "records").mkdir(parents=True, exist_ok=True)
        self._root = resolved

    @property
    def root(self) -> Path:
        """Der aufgelöste Store-Root."""
        return self._root

    def object_reference(self, content_sha256: str) -> str:
        """Gibt die store-relative Objektreferenz zurück (kein absoluter Pfad).

        Args:
            content_sha256: Validierter Hexdigest.

        Returns:
            Referenz der Form ``objects/sha256/<prefix>/<digest>.blob``.
        """
        digest = self._require_digest(content_sha256)
        return f"objects/sha256/{digest[:2]}/{digest}.blob"

    def write_object(self, content_sha256: str, payload: bytes) -> str:
        """Schreibt das Payload-Objekt idempotent und atomar.

        Args:
            content_sha256: Validierter Hexdigest des Payloads.
            payload: Die unveränderten Rohbytes.

        Returns:
            Die store-relative Objektreferenz.

        Raises:
            QuarantineStoreError: Bei Digest-Mismatch oder Kollision.
        """
        digest = self._require_digest(content_sha256)
        reference = self.object_reference(digest)
        target = self._within_root(reference)

        if target.exists():
            if target.read_bytes() != payload:
                raise QuarantineStoreError(
                    ReasonCode.QUARANTINE_OBJECT_HASH_COLLISION, "object"
                )
            return reference  # idempotent

        target.parent.mkdir(parents=True, exist_ok=True)
        _atomic_write_bytes(target, payload)
        return reference

    def write_record(self, record: QuarantineRecord) -> None:
        """Schreibt das Manifest kanonisch, idempotent und atomar.

        Args:
            record: Der zu schreibende Record.

        Raises:
            QuarantineStoreError: Bei abweichender Kollision unter derselben
                ``quarantine_id``.
        """
        self._require_id(record.quarantine_id)
        target = self._record_path(record.quarantine_id)
        payload = _canonical_json(record)

        if target.exists():
            if target.read_bytes() != payload:
                raise QuarantineStoreError(
                    ReasonCode.QUARANTINE_RECORD_COLLISION, "record"
                )
            return  # idempotent

        target.parent.mkdir(parents=True, exist_ok=True)
        _atomic_write_bytes(target, payload)

    def load_record(self, quarantine_id: str) -> QuarantineRecord:
        """Lädt und validiert ein Manifest fail-closed.

        Args:
            quarantine_id: Die validierte Quarantäne-ID.

        Returns:
            Der validierte Record.

        Raises:
            QuarantineStoreError: Record fehlt, ist unlesbar, kein gültiges
                JSON oder verletzt das Record-Schema.
        """
        self._require_id(quarantine_id)
        target = self._record_path(quarantine_id)
        if not target.is_file():
            raise QuarantineStoreError(
                ReasonCode.QUARANTINE_RECORD_NOT_FOUND, "record"
            )

        try:
            data = json.loads(target.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise QuarantineStoreError(
                ReasonCode.QUARANTINE_RECORD_INVALID, "record"
            ) from exc

        return _record_from_dict(data)

    # -- interne Helfer ---------------------------------------------------

    def _record_path(self, quarantine_id: str) -> Path:
        return self._within_root(f"records/{quarantine_id}.json")

    def _within_root(self, reference: str) -> Path:
        """Baut einen Pfad im Store und verweigert jeden Ausbruch."""
        candidate = (self._root / reference).resolve()
        if candidate != self._root and not candidate.is_relative_to(self._root):
            raise QuarantineStoreError(
                ReasonCode.QUARANTINE_STORE_WRITE_OUTSIDE_ROOT, "path"
            )
        return candidate

    @staticmethod
    def _require_digest(value: str) -> str:
        if not _HEX_DIGEST.match(value):
            raise QuarantineStoreError(
                ReasonCode.QUARANTINE_STORE_ROOT_INVALID, "invalid content digest"
            )
        return value

    @staticmethod
    def _require_id(value: str) -> str:
        if not _HEX_ID.match(value):
            raise QuarantineStoreError(
                ReasonCode.QUARANTINE_RECORD_INVALID, "invalid quarantine id"
            )
        return value


def _canonical_json(record: QuarantineRecord) -> bytes:
    """Serialisiert einen Record deterministisch (sortierte Schlüssel)."""
    text = json.dumps(
        record.to_dict(), sort_keys=True, ensure_ascii=False, indent=2
    )
    return (text + "\n").encode("utf-8")


def _atomic_write_bytes(path: Path, data: bytes) -> None:
    """Schreibt Bytes atomar: exklusive Temp-Datei, fsync, ``os.replace``.

    Bei jedem Fehler wird die Temp-Datei entfernt; es entsteht **kein**
    freigegebenes Teilartefakt.
    """
    tmp = path.with_name(f"{path.name}.tmp-{os.getpid()}-{next(_temp_counter)}")
    fd = os.open(tmp, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def _record_from_dict(data: object) -> QuarantineRecord:
    """Baut einen Record fail-closed aus einem geparsten Mapping."""
    if not isinstance(data, dict):
        raise QuarantineStoreError(ReasonCode.QUARANTINE_RECORD_INVALID, "record")

    keys = set(data)
    if keys - RECORD_FIELDS:
        raise QuarantineStoreError(
            ReasonCode.QUARANTINE_RECORD_INVALID, "unknown record field"
        )
    if RECORD_FIELDS - keys:
        raise QuarantineStoreError(
            ReasonCode.QUARANTINE_RECORD_INVALID, "missing record field"
        )

    try:
        status = ScanStatus(data["scan_status"])
        codes = tuple(str(code) for code in data["finding_codes"])
        record = QuarantineRecord(
            record_schema_version=str(data["record_schema_version"]),
            quarantine_id=str(data["quarantine_id"]),
            source_reference=str(data["source_reference"]),
            content_sha256=str(data["content_sha256"]),
            byte_size=int(data["byte_size"]),
            media_type=str(data["media_type"]),
            policy_schema_version=str(data["policy_schema_version"]),
            policy_sha256=str(data["policy_sha256"]),
            scan_status=status,
            finding_codes=codes,
            finding_count=int(data["finding_count"]),
            stored_object_reference=str(data["stored_object_reference"]),
            created_at=str(data["created_at"]),
            implementation_version=str(data["implementation_version"]),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise QuarantineStoreError(
            ReasonCode.QUARANTINE_RECORD_INVALID, "record"
        ) from exc

    if record.finding_count != len(record.finding_codes):
        raise QuarantineStoreError(
            ReasonCode.QUARANTINE_RECORD_INVALID, "finding_count mismatch"
        )
    return record
