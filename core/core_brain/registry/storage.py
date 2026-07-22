"""Lokaler Source-Registry-Speicher (CBP-WP-014).

Speichert unveränderliche Records und append-only Retirement-Events sowie einen
atomar ersetzten, abgeleiteten Katalog. Pfade werden **ausschließlich** aus
validierten IDs abgeleitet — niemals aus Eingabepfaden.

Grenzen und Zusicherungen:

- Der Registry-Root wird **explizit** angegeben und liegt **außerhalb** des
  Core-Repositorys; ein Symlink-Root wird abgewiesen.
- Records und Events sind unveränderlich; keine stillschweigende Überschreibung.
- Identische Registrierung ist idempotent; abweichende Definition derselben
  Identität blockiert.
- Es wird **nichts außerhalb** des Registry-Roots geschrieben; keine Hardlinks
  oder Symlinks.

Der Speicher ist **weder Canonical Source noch RT-2** und **keine** produktive
Sicherheits- oder Isolationsgrenze. Der Import hat keine Nebenwirkungen.
"""

from __future__ import annotations

import itertools
import json
import os
import re
from pathlib import Path
from typing import Final

from ..errors import RegistryStorageError, ReasonCode
from .models import (
    EVENT_FIELDS,
    RECORD_FIELDS,
    EventType,
    LifecycleState,
    RegistryRecord,
    RetirementEvent,
)

__all__ = ["RegistryStorage"]

_REPO_ROOT: Final[Path] = Path(__file__).resolve().parents[3]
_SOURCE_ID: Final[re.Pattern[str]] = re.compile(r"\Asrc-[0-9a-f]{24}\Z")
_EVENT_ID: Final[re.Pattern[str]] = re.compile(r"\Aevt-[0-9a-f]{24}\Z")
_temp_counter = itertools.count()


class RegistryStorage:
    """Ein Registry-Speicher unter einem expliziten Root-Pfad."""

    def __init__(self, root: Path) -> None:
        """Öffnet oder legt den Registry-Root an und validiert ihn.

        Raises:
            RegistryStorageError: Root ist Symlink, liegt im Repository oder ist
                strukturell unzulässig.
        """
        if root.is_symlink():
            raise RegistryStorageError(ReasonCode.REGISTRY_STORE_IS_SYMLINK, "root")

        resolved = root.resolve()
        if resolved == _REPO_ROOT or resolved.is_relative_to(_REPO_ROOT):
            raise RegistryStorageError(
                ReasonCode.REGISTRY_STORE_INSIDE_REPOSITORY, "root"
            )
        if resolved.exists() and not resolved.is_dir():
            raise RegistryStorageError(
                ReasonCode.REGISTRY_STORE_ROOT_INVALID, "root is not a directory"
            )

        resolved.mkdir(parents=True, exist_ok=True)
        (resolved / "records").mkdir(parents=True, exist_ok=True)
        (resolved / "events").mkdir(parents=True, exist_ok=True)
        (resolved / "catalog").mkdir(parents=True, exist_ok=True)
        self._root = resolved

    @property
    def root(self) -> Path:
        """Der aufgelöste Registry-Root."""
        return self._root

    # -- Records ----------------------------------------------------------

    def write_record(self, record: RegistryRecord) -> RegistryRecord:
        """Schreibt einen Record idempotent und atomar.

        Returns:
            Den wirksamen Record (bestehend bei Idempotenz, sonst neu).

        Raises:
            RegistryStorageError: Bei abweichender Identität oder Definition
                unter derselben Source ID.
        """
        self._require_source_id(record.source_id)
        target = self._within_root(f"records/{record.source_id}.json")

        if target.exists():
            existing = self._read_record(target)
            if (
                existing.namespace != record.namespace
                or existing.source_key != record.source_key
                or existing.definition_sha256 != record.definition_sha256
            ):
                raise RegistryStorageError(
                    ReasonCode.REGISTRY_RECORD_CONFLICT, "record"
                )
            return existing  # idempotent

        _atomic_write_bytes(target, _canonical_json(record.to_dict()))
        return record

    def record_exists(self, source_id: str) -> bool:
        """Prüft, ob ein Record existiert."""
        self._require_source_id(source_id)
        return self._within_root(f"records/{source_id}.json").is_file()

    def load_record(self, source_id: str) -> RegistryRecord:
        """Lädt und validiert einen Record fail-closed.

        Raises:
            RegistryStorageError: Record fehlt, ist unlesbar oder ungültig.
        """
        self._require_source_id(source_id)
        target = self._within_root(f"records/{source_id}.json")
        if not target.is_file():
            raise RegistryStorageError(ReasonCode.REGISTRY_RECORD_NOT_FOUND, "record")
        return self._read_record(target)

    def list_source_ids(self) -> list[str]:
        """Gibt alle vorhandenen Source IDs sortiert zurück."""
        records_dir = self._root / "records"
        ids = [
            p.stem
            for p in records_dir.glob("*.json")
            if _SOURCE_ID.match(p.stem)
        ]
        return sorted(ids)

    # -- Events -----------------------------------------------------------

    def append_event(self, event: RetirementEvent) -> RetirementEvent:
        """Fügt ein Retirement-Event append-only und idempotent an.

        Raises:
            RegistryStorageError: Bei abweichendem Event unter derselben ID.
        """
        self._require_source_id(event.source_id)
        self._require_event_id(event.event_id)
        target = self._within_root(
            f"events/{event.source_id}/{event.event_id}.json"
        )
        payload = _canonical_json(event.to_dict())

        if target.exists():
            if target.read_bytes() != payload:
                raise RegistryStorageError(
                    ReasonCode.REGISTRY_RETIREMENT_CONFLICT, "event"
                )
            return event  # idempotent

        target.parent.mkdir(parents=True, exist_ok=True)
        _atomic_write_bytes(target, payload)
        return event

    def load_events(self, source_id: str) -> list[RetirementEvent]:
        """Lädt alle Events einer Source, sortiert nach Event-ID."""
        self._require_source_id(source_id)
        events_dir = self._root / "events" / source_id
        if not events_dir.is_dir():
            return []
        events = [
            self._read_event(p)
            for p in sorted(events_dir.glob("*.json"))
            if _EVENT_ID.match(p.stem)
        ]
        return events

    # -- Catalog ----------------------------------------------------------

    def write_catalog(self, payload: bytes) -> None:
        """Ersetzt den Katalog atomar."""
        target = self._within_root("catalog/catalog.json")
        _atomic_write_bytes(target, payload, overwrite=True)

    # -- interne Helfer ---------------------------------------------------

    def _within_root(self, reference: str) -> Path:
        candidate = (self._root / reference).resolve()
        if candidate != self._root and not candidate.is_relative_to(self._root):
            raise RegistryStorageError(
                ReasonCode.REGISTRY_STORE_WRITE_OUTSIDE_ROOT, "path"
            )
        return candidate

    def _read_record(self, path: Path) -> RegistryRecord:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise RegistryStorageError(
                ReasonCode.REGISTRY_RECORD_INVALID, "record"
            ) from exc
        return _record_from_dict(data)

    def _read_event(self, path: Path) -> RetirementEvent:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise RegistryStorageError(
                ReasonCode.REGISTRY_RECORD_INVALID, "event"
            ) from exc
        return _event_from_dict(data)

    @staticmethod
    def _require_source_id(value: str) -> str:
        if not _SOURCE_ID.match(value):
            raise RegistryStorageError(
                ReasonCode.REGISTRY_RECORD_INVALID, "invalid source id"
            )
        return value

    @staticmethod
    def _require_event_id(value: str) -> str:
        if not _EVENT_ID.match(value):
            raise RegistryStorageError(
                ReasonCode.REGISTRY_RECORD_INVALID, "invalid event id"
            )
        return value


def _canonical_json(data: dict[str, object]) -> bytes:
    text = json.dumps(data, sort_keys=True, ensure_ascii=False, indent=2)
    return (text + "\n").encode("utf-8")


def _atomic_write_bytes(path: Path, data: bytes, *, overwrite: bool = False) -> None:
    """Schreibt Bytes atomar: exklusive Temp-Datei, fsync, ``os.replace``."""
    if path.exists() and not overwrite:
        raise RegistryStorageError(
            ReasonCode.REGISTRY_RECORD_CONFLICT, "would overwrite"
        )
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


def _record_from_dict(data: object) -> RegistryRecord:
    if not isinstance(data, dict):
        raise RegistryStorageError(ReasonCode.REGISTRY_RECORD_INVALID, "record")
    keys = set(data)
    if keys - RECORD_FIELDS or RECORD_FIELDS - keys:
        raise RegistryStorageError(
            ReasonCode.REGISTRY_RECORD_INVALID, "record field mismatch"
        )
    try:
        state = LifecycleState(data["lifecycle_state"])
        return RegistryRecord(
            record_schema_version=str(data["record_schema_version"]),
            source_id=str(data["source_id"]),
            namespace=str(data["namespace"]),
            source_key=str(data["source_key"]),
            display_name=str(data["display_name"]),
            collection_key=str(data["collection_key"]),
            domain_key=str(data["domain_key"]),
            source_kind=str(data["source_kind"]),
            data_class=str(data["data_class"]),
            ai_eligibility=str(data["ai_eligibility"]),
            owner_role=str(data["owner_role"]),
            source_reference=str(data["source_reference"]),
            definition_sha256=str(data["definition_sha256"]),
            policy_sha256=str(data["policy_sha256"]),
            lifecycle_state=state,
            registered_at=str(data["registered_at"]),
            implementation_version=str(data["implementation_version"]),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise RegistryStorageError(
            ReasonCode.REGISTRY_RECORD_INVALID, "record"
        ) from exc


def _event_from_dict(data: object) -> RetirementEvent:
    if not isinstance(data, dict):
        raise RegistryStorageError(ReasonCode.REGISTRY_RECORD_INVALID, "event")
    keys = set(data)
    if keys - EVENT_FIELDS or EVENT_FIELDS - keys:
        raise RegistryStorageError(
            ReasonCode.REGISTRY_RECORD_INVALID, "event field mismatch"
        )
    try:
        return RetirementEvent(
            event_schema_version=str(data["event_schema_version"]),
            event_id=str(data["event_id"]),
            source_id=str(data["source_id"]),
            event_type=EventType(data["event_type"]),
            reason_code=str(data["reason_code"]),
            occurred_at=str(data["occurred_at"]),
            previous_state=LifecycleState(data["previous_state"]),
            resulting_state=LifecycleState(data["resulting_state"]),
            implementation_version=str(data["implementation_version"]),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise RegistryStorageError(
            ReasonCode.REGISTRY_RECORD_INVALID, "event"
        ) from exc
