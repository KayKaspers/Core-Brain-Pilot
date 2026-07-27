"""Source Mapping Draft Validator — CBP-WP-015.

Ein lokaler, synthetisch testbarer, **read-only** und fail-closed Validator für
**Mapping-Entwürfe** nach dem angenommenen **31-Feld-Vertrag** (ADR-0008,
D-031 bis D-033). Er implementiert **nicht**: reale Quellen, Source-Inhalte,
reale Pfade oder URLs, Mapping-Speicherung, Report-Speicherung,
Registry-Veränderung, Mapping- oder Source-Aktivierung, Ingest, Indexierung,
Retrieval, Netzwerkzugriff, Secret-Auflösung, RT-2-Speicherung, API oder Web UI.

Der Vertrag umfasst **31 Felddefinitionen** — **29 Pflichtfelder** und **zwei
optionale Felder** (``credential_reference`` und ``notes``). Der Validator fügt
**kein** Feld hinzu, entfernt keines, benennt keines um und berechnet
``mapping_id`` **nicht** (Bildungsvorschrift offen).

Die einzigen zwei Ergebnisse sind ``VALID_DRAFT`` und ``BLOCKED``. Keiner
bedeutet ``approved``, ``mapped``, ``activated``, ``ingestible``, ``indexed``
oder ``retrievable``.

Der Import dieses Pakets hat keine Nebenwirkungen: Es wird keine Policy
gelesen, kein Entwurf geöffnet, keine Registry berührt und keine Verbindung
aufgebaut.
"""

from __future__ import annotations

from .models import (
    CONTRACT_FIELD_COUNT,
    MAPPING_FIELDS,
    OPTIONAL_FIELD_COUNT,
    OPTIONAL_MAPPING_FIELDS,
    REQUIRED_FIELD_COUNT,
    REQUIRED_MAPPING_FIELDS,
    MappingPolicy,
    MappingReasonCode,
    ValidationReport,
    ValidationStatus,
)
from .parser import DraftRejected, parse_draft
from .policy import load_policy, parse_policy_mapping
from .service import run_activation_check, run_validate
from .validator import (
    boundary_count,
    compare_to_registry,
    mapping_id_of,
    present_field_count,
    validate_contract_and_state,
)

__all__ = [
    "CONTRACT_FIELD_COUNT",
    "REQUIRED_FIELD_COUNT",
    "OPTIONAL_FIELD_COUNT",
    "MAPPING_FIELDS",
    "REQUIRED_MAPPING_FIELDS",
    "OPTIONAL_MAPPING_FIELDS",
    "MappingPolicy",
    "MappingReasonCode",
    "ValidationReport",
    "ValidationStatus",
    "DraftRejected",
    "parse_draft",
    "load_policy",
    "parse_policy_mapping",
    "validate_contract_and_state",
    "compare_to_registry",
    "present_field_count",
    "boundary_count",
    "mapping_id_of",
    "run_validate",
    "run_activation_check",
]
