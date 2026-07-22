"""Ingest-Quarantäne — CBP-WP-013.

Ein lokaler, synthetisch testbarer und **fail-closed** Quarantäneprototyp. Er
implementiert **nicht**: reale Quellen, reale Source Mappings, produktiven
Ingest, Freigabe, Promotion, Collection- oder Index-Erzeugung, Retrieval,
Embeddings, externe Übertragung, Netzwerkzugriff, Secret-Auflösung,
RT-2-Speicherung, API oder Web UI.

Zulässige Ergebniszustände sind ausschließlich ``READY_FOR_HUMAN_REVIEW``,
``REVIEW_REQUIRED`` und ``BLOCKED``. Kein Zustand bedeutet ``approved``,
``released``, ``enabled`` oder ``indexed``.

Der Import dieses Pakets hat keine Nebenwirkungen: Es wird keine Policy
gelesen, keine Datei angelegt, kein Store geöffnet und keine Verbindung
aufgebaut.
"""

from __future__ import annotations

from .models import (
    Finding,
    FindingCode,
    FindingSeverity,
    QuarantinePolicy,
    QuarantineRecord,
    ScanResult,
    ScanStatus,
)
from .pipeline import StageOutcome, run_scan, run_stage
from .policy import load_policy
from .store import QuarantineStore

__all__ = [
    "Finding",
    "FindingCode",
    "FindingSeverity",
    "QuarantinePolicy",
    "QuarantineRecord",
    "ScanResult",
    "ScanStatus",
    "StageOutcome",
    "QuarantineStore",
    "load_policy",
    "run_scan",
    "run_stage",
]
