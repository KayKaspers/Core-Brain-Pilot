# CLAUDE.md — Core Brain Pilot

Betriebsanweisung für Implementation Agents in diesem Repository.
Verbindlich nach **Nova Development Framework v1.0.0**.

## Rollenmodell

| Rolle | Verantwortung |
| --- | --- |
| Nova (ChatGPT) | Plant Architektur und Work Packages: Typ, Scope, Akzeptanzkriterien |
| Implementation Agent (Claude Desktop) | Führt **genau ein** freigegebenes Work Package aus und berichtet strukturiert |
| Human Maintainer | Prüft, entscheidet GO / GO WITH NOTES / REWORK / SPLIT / STOP, committet und pusht |

## Lifecycle

```
Classify → Plan → Execute → Report to Nova → Review → Commit
```

Kein Schritt wird ausgelassen.

## Harte Regeln

1. Arbeite ausschließlich innerhalb von `D:\Projects\Core-Brain-Pilot`.
2. Benachbarte Projekte werden weder gelesen noch verändert. Ausdrücklich
   benannte Quelldateien dürfen gelesen werden.
3. Führe nur das aktuell freigegebene Work Package aus.
4. Keine stillschweigenden Scope-Erweiterungen.
5. Keine Commits, Pushes, Remotes oder GitHub-Aktionen ohne ausdrückliche
   Freigabe. Commit-Autorität liegt beim Human Maintainer.
6. Keine Secrets, Zugangsdaten oder privaten Schlüssel erzeugen, lesen,
   speichern oder indexieren — auch keine Beispiel-Secrets.
7. Vor jeder Dateiänderung: Zielpfad prüfen, aktuellen Zustand lesen, Scope
   und erlaubte Dateien prüfen.
8. Bei Konflikten, unklaren Entscheidungen oder fehlender Autorisierung:
   nicht raten, Arbeit sicher anhalten, Blocker melden.
9. Befehle für den Human Maintainer ausschließlich als vollständige
   **PowerShell**-Befehle ausgeben.
10. Keine Bash-, CMD- oder WSL-Anweisungen für den Human Maintainer.
11. Nach jedem Work Package einen strukturierten NDF Implementation Report
    erzeugen.
12. Neue und geänderte Dokumente verwenden **UTF-8 mit echten deutschen
    Umlauten**.

## Autoritätsmodell A0–A6

| Klasse | Quelle |
| --- | --- |
| A0 | Ausdrücklicher Human-Maintainer-Beschluss |
| A1 | Release, Tag oder angenommener ADR |
| A2 | Formeller Projektstatus oder Work-Package-Queue |
| A3 | Freigegebene Roadmap oder Gate-Dokumentation |
| A4 | README und erläuternde Dokumentation |
| A5 | Freigegebene Projektchat-Übergabe |
| A6 | Automatisch abgeleitete Zusammenfassung oder Wiki-Inhalt |

**A6 darf A0 bis A5 niemals automatisch überschreiben.**

Bei Konflikt gewinnt die niedrigere Zahl. Ein Konflikt zwischen gleichrangigen
Quellen wird **nicht** automatisch aufgelöst, sondern dem Human Maintainer
vorgelegt.

### Quellen dieses Projekts

| Quelle | Klasse |
| --- | --- |
| `Bauanleitung_Second-Brain.pdf` | **A4** — Originalquelle, sechs Inhaltsseiten |
| `Second-Brain-Bauanleitung-Textfassung.md` | **A6** — abgeleitete Arbeitsrepräsentation |
| `docs/discovery/Core-Brain-Project-Handoff.md` | **A5** — kanonisch, getrackt |
| Nova Development Framework v1.0.0 | **A1** |

Die A6-Textfassung beansprucht keine höhere Autorität als die A4-PDF.

## Kanonisch vs. abgeleitet

- **Kanonisch** — kuratierter Markdown-Wissensbestand unter Git-Historie.
  Einzige Wahrheitsquelle.
- **Abgeleitet** — Index, Cache, Embeddings, Graph, Web-UI-Zustand.
  Jederzeit reproduzierbar, nie autoritativ, nie in Git.

Der Verlust von Index, Cache, Embeddings, Graph oder Web-UI darf **keinen
Wissensverlust** verursachen.

## Prompt Modes ≠ Context Budgets

Zwei getrennte Konzepte. Die Verwechslung ist als Risiko R-24 erfasst.

### NDF Prompt Modes (A1)

| Modus | Einsatz |
| --- | --- |
| **Full** | Governance-kritische Arbeit: Scope Lock, Architektur, Security, Release, destruktive Aktionen |
| **Standard** | Normale, begrenzte Work Packages und Dokumentationsreviews |
| **Short** | Standardisierte Folgearbeit mit vorhandenem Context Pack |

### Core-Brain Context Budgets (A2)

| Budget | Name | Quellen |
| --- | --- | --- |
| B0 | Micro | 1 Abschnitt |
| B1 | **Lean** | 1 Quelle |
| B2 | Standard | ≤ 3 Quellen |
| B3 | Extended | ≤ 3 Hauptquellen, begründet |
| B4 | Exceptional | begründet, Freigabe vorab |

> **„Lean" ist kein NDF Prompt Mode**, sondern ausschließlich der Name von B1
> (D-009). Vollständig in
> [docs/architecture/CONTEXT_BUDGETS.md](docs/architecture/CONTEXT_BUDGETS.md).

## Brain-First-Suchleiter

1. Index lesen → 2. Quellentyp und Autoritätsklasse bestimmen → 3. Status
prüfen → 4. Wiki nur als abgeleitete Orientierung → 5. Suche auf Collection
begrenzen → 6. Kandidaten über Metadaten prüfen → 7. kleinste ausreichende Zahl
von Quellen öffnen → 8. nur relevante Abschnitte lesen → 9. Fakten,
Ableitungen, Empfehlungen und Unsicherheit trennen → 10. Quellen und Revisionen
nennen.

**Keine blinden Vollscans.**

## Aktueller Zustand

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Aktuelles Work Package | CBP-WP-004 (`in-review`) |
| Nächstes Gate | G0 – Discovery and Scope Lock |
| **Gate-Status** | **NOT PASSED** — 18 von 25 Core-Kriterien `accepted`, 7 offen |
| Angenommene ADRs | 5 (A1) |
| Implementierte Capabilities | keine |

## Sperrliste Phase 0

25 gesperrte Gegenstände, verbindlich in
[docs/product/DO_NOT_START.md](docs/product/DO_NOT_START.md).

Kurzfassung: produktive Implementierung, Docker Compose, Web-UI,
Suchintegration, Wiki-Ingest, Knowledge Graph, Obsidian-Synchronisation,
MCP-Integration, externe Connectoren, automatisierte Commits, öffentliches
Branding, Kubernetes, Multi-Tenant, SaaS, Proxmox-API-Integration, neue
NDF-Skills, CDF-, CoreOps- und CDS-Integration, öffentliche Cloudinstanz.

Superpowers darf als Referenz untersucht, aber **nicht** als zweites
Governance-System eingeführt werden.
