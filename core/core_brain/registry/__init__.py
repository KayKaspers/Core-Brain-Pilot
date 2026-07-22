"""Source Registry and Catalog — CBP-WP-014.

Ein lokaler, synthetisch testbarer, **deaktivierter** und fail-closed Registry-
und Catalog-Prototyp. Er implementiert **nicht**: reale Quellen, Source-Inhalte,
reale Pfade oder URLs, Source Mapping, Source Boundary, Aktivierung, Ingest,
Quarantäne-Promotion, Collection- oder Index-Erzeugung, Retrieval, Embeddings,
Netzwerkzugriff, Secret-Auflösung, RT-2-Speicherung, API oder Web UI.

Zulässige Lifecycle-Zustände sind ausschließlich ``REGISTERED_DISABLED`` und
``RETIRED``. Kein Zustand bedeutet ``approved``, ``mapped``, ``activated``,
``ingestible``, ``indexed`` oder ``retrievable``.

Der Import dieses Pakets hat keine Nebenwirkungen: Es wird keine Policy
gelesen, kein Speicher geöffnet und keine Verbindung aufgebaut.
"""

from __future__ import annotations

from .catalog import build_catalog
from .models import (
    Catalog,
    CatalogEntry,
    EventType,
    LifecycleState,
    RegistryPolicy,
    RegistryRecord,
    RetirementEvent,
    SourceDefinition,
)
from .policy import load_policy
from .service import (
    RetireOutcome,
    derive_source_id,
    inspect,
    load_definition,
    register,
    retire,
    validate_definition,
)
from .storage import RegistryStorage

__all__ = [
    "Catalog",
    "CatalogEntry",
    "EventType",
    "LifecycleState",
    "RegistryPolicy",
    "RegistryRecord",
    "RetirementEvent",
    "SourceDefinition",
    "RetireOutcome",
    "RegistryStorage",
    "build_catalog",
    "load_policy",
    "load_definition",
    "validate_definition",
    "derive_source_id",
    "register",
    "retire",
    "inspect",
]
