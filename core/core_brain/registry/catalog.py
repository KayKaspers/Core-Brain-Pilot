"""Ableitung des deterministischen Registry-Katalogs (CBP-WP-014).

Der Katalog wird **ausschließlich** aus validierten Records und
Retirement-Events abgeleitet, deterministisch nach ``source_id`` sortiert und
enthält nur minimierte Metadaten. Ein unbekannter oder beschädigter Record
blockiert die **gesamte** Katalogerzeugung — es entsteht **kein** Teilkatalog.

Der Import dieses Moduls hat keine Nebenwirkungen.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime

from ..errors import RegistryCatalogError, RegistryStorageError, ReasonCode
from .models import (
    CATALOG_SCHEMA_VERSION,
    Catalog,
    CatalogEntry,
    LifecycleState,
)
from .storage import RegistryStorage

__all__ = ["Clock", "build_catalog", "default_clock", "effective_state"]

Clock = Callable[[], datetime]


def default_clock() -> datetime:
    """Gibt die aktuelle UTC-Zeit zurück."""
    return datetime.now(UTC)


def effective_state(record_state: LifecycleState, has_retirement: bool) -> LifecycleState:
    """Leitet den wirksamen Lifecycle-Zustand ab.

    Ein vorhandenes Retirement-Event ergibt ``RETIRED``; andernfalls bleibt der
    Record-Zustand (``REGISTERED_DISABLED``).
    """
    if has_retirement:
        return LifecycleState.RETIRED
    return record_state


def build_catalog(storage: RegistryStorage, *, clock: Clock = default_clock) -> Catalog:
    """Baut den vollständigen, deterministisch sortierten Katalog.

    Args:
        storage: Der Registry-Speicher.
        clock: Injizierbare Uhr für ``generated_at``.

    Returns:
        Den vollständigen :class:`Catalog`.

    Raises:
        RegistryCatalogError: Bei einem unbekannten oder beschädigten Record;
            es wird **kein** Teilkatalog erzeugt.
    """
    entries: list[CatalogEntry] = []
    registered_disabled = 0
    retired = 0

    try:
        for source_id in storage.list_source_ids():
            record = storage.load_record(source_id)
            has_retirement = len(storage.load_events(source_id)) > 0
            state = effective_state(record.lifecycle_state, has_retirement)
            entries.append(
                CatalogEntry(
                    source_id=record.source_id,
                    namespace=record.namespace,
                    source_key=record.source_key,
                    display_name=record.display_name,
                    collection_key=record.collection_key,
                    domain_key=record.domain_key,
                    source_kind=record.source_kind,
                    data_class=record.data_class,
                    ai_eligibility=record.ai_eligibility,
                    lifecycle_state=state,
                )
            )
            if state is LifecycleState.RETIRED:
                retired += 1
            else:
                registered_disabled += 1
    except RegistryStorageError as exc:
        # fail-closed: kein Teilkatalog bei Integritätsfehler.
        raise RegistryCatalogError(
            ReasonCode.REGISTRY_CATALOG_INTEGRITY_ERROR, exc.reason.value
        ) from exc

    entries.sort()  # deterministisch nach source_id (CatalogEntry.order)

    return Catalog(
        catalog_schema_version=CATALOG_SCHEMA_VERSION,
        generated_at=_utc_iso(clock()),
        record_count=len(entries),
        registered_disabled_count=registered_disabled,
        retired_count=retired,
        entries=tuple(entries),
    )


def _utc_iso(moment: datetime) -> str:
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=UTC)
    return moment.astimezone(UTC).isoformat().replace("+00:00", "Z")
