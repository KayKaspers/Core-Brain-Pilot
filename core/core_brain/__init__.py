"""Foundation Runtime Skeleton — CBP-WP-012.

Ein lokaler, fail-closed Skeleton ohne operative Wirkung. Er implementiert
**nicht**: Source Mapping, Ingest, Retrieval, Indexierung, Secret-Auflösung,
Netzwerkzugriff, RT-2-Speicherung, API oder Web UI.

Der Import dieses Pakets hat keine Nebenwirkungen: Es wird keine
Konfiguration gelesen, kein Parser gebaut, keine Datei angelegt und keine
Verbindung geöffnet.

Ausführung::

    py -3.13 -m core.core_brain version
"""

from __future__ import annotations

__all__ = ["__version__", "RUNTIME_MODE", "PRODUCTION_READY"]

__version__ = "0.1.0.dev0"
RUNTIME_MODE = "skeleton"
PRODUCTION_READY = False
