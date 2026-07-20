# Core Brain Pilot

> **Phase 0 – Discovery und Scope Lock.**
> Dieses Repository enthaelt derzeit **ausschliesslich Dokumentation**.
> Es existiert **keine** Implementierung, keine Laufzeit und keine Installation.

Core Brain Pilot ist ein serverzentriertes und portables KI-Wissens- und
Arbeitssystem.

Ziel ist, Claude und anderen Implementation Agents nur die **kleinste
ausreichende Menge** relevanter, aktueller, autoritativer und
datenschutzrechtlich erlaubter Informationen bereitzustellen.

Proxmox ist die erste Referenzplattform, aber nicht die Produktgrenze.
Docker Compose ist als bevorzugte spaetere Anwendungslaufzeit innerhalb einer
dedizierten Linux-VM vorgesehen — noch nicht begonnen.

## Aktueller Stand

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Aktuelles Work Package | CBP-WP-001 |
| Naechstes Gate | G0 – Discovery and Scope Lock |
| Implementierte Capabilities | keine |
| Framework | Nova Development Framework v1.0.0 |

## Prozessmodell

Das Projekt arbeitet verbindlich nach dem
[Nova Development Framework v1.0.0](https://github.com/KayKaspers/Nova-Development-Framework/releases/tag/v1.0.0).

Rollen und Ablauf:

```
Nova (ChatGPT)  →  Implementation Agent  →  Human Maintainer
   plant              fuehrt genau ein          prueft, entscheidet,
   Work Packages      Work Package aus          committet und pusht
```

Lifecycle jedes Work Packages:

```
Classify → Plan → Execute → Report to Nova → Review → Commit
```

Nur der Human Maintainer committet, tagged und pusht.

## Repository-Struktur

| Pfad | Inhalt |
| --- | --- |
| `docs/architecture/` | Projektdefinition, Architekturprinzipien, Vertrauensgrenzen |
| `docs/decisions/` | Architecture Decision Records (ADR) |
| `docs/discovery/` | Offene Fragen und fehlende Information fuer Gate G0 |
| `docs/ndf/` | NDF-Anwendung und dokumentierte Abweichungen |
| `docs/privacy/` | Datenklassen und technische Datenschutzregeln |
| `docs/product/` | Explizite Nicht-Ziele der aktuellen Phase |
| `project-brain/` | Kuratiertes Projektgedaechtnis |
| `project-system/` | Profil, Manifest, Capability Matrix, Register, WP-Queue |
| `work-packages/` | Wortlaut der freigegebenen Work Packages |

## Kernprinzipien

- Kanonischer Markdown-Wissensbestand
- Git-Historie fuer kuratierte Inhalte
- Reproduzierbare abgeleitete Daten
- Deterministischer Quellenindex
- Lokale Hybrid-Suche
- Brain-First-Retrieval
- A0–A6-Autoritaetsmodell
- Datenklassen und technische Datenschutzregeln
- Context Budgets B0–B4
- Reproduzierbare Context Packs
- Erklaerbarer Retrieval-Trace
- Menschlich kontrollierte Konfliktaufloesung
- Private Mehrgeraete-Nutzung
- Deployment-neutrale Architektur
- Austauschbare Suche und Web-UI
- Backup-, Restore- und Rebuild-Faehigkeit

Ausfuehrlich in [docs/architecture/ARCHITECTURE_PRINCIPLES.md](docs/architecture/ARCHITECTURE_PRINCIPLES.md).

## Datenschutz in einem Satz

Secrets duerfen **nicht** in Repository, Wissensbestand, Index, Context Pack
oder Modellkontext gelangen. Siehe
[docs/privacy/DATA_CLASSIFICATION.md](docs/privacy/DATA_CLASSIFICATION.md).

## Was jetzt **nicht** begonnen wird

Siehe [docs/product/DO_NOT_START.md](docs/product/DO_NOT_START.md) — verbindliche
Sperrliste fuer Phase 0.

## Lizenz

Noch nicht festgelegt. Bewusst offen bis zu einer Entscheidung des Human
Maintainers; siehe [project-system/DECISION_REGISTER.md](project-system/DECISION_REGISTER.md).
