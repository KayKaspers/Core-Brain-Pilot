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
| `docs/decisions/ADR-0001` bis `ADR-0009` | **A1** — angenommen und bindend |

Die A6-Textfassung beansprucht keine höhere Autorität als die A4-PDF.

## Kanonisch vs. abgeleitet

- **Kanonisch** — kuratierter Markdown-Wissensbestand unter Git-Historie.
  Einzige Wahrheitsquelle.
- **Abgeleitet** — Index, Cache, Embeddings, Graph, Web-UI-Zustand.
  Jederzeit reproduzierbar, nie autoritativ, nie in Git.

Der Verlust von Index, Cache, Embeddings, Graph oder Web-UI darf **keinen
Wissensverlust** verursachen.

**Runtime-Daten sind nicht durchgehend abgeleitet** (ADR-0007): **RT-1**
Rebuildable Derived Data ist reproduzierbar · **RT-2 Operational Evidence**
(Audit-, Approval-, Incident- und Restore-Nachweise) ist **nicht**
reproduzierbar und aufbewahrungs- sowie sicherungspflichtig · **RT-3**
Transient Runtime State ist flüchtig und nie alleinige Statuswahrheit.

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
| Phase | **Phase 0 – COMPLETE** |
| **Gate G0** | **PASSED WITH NOTES** — 2026-07-21, A0 |
| **Phase 1** | **AUTHORIZED FOR PLANNING** — keine Implementierung freigegeben |
| Aktuelles Work Package | CBP-WP-015 (`in-review`) |
| Core-Kriterien | 25 von 25 `accepted`, 0 `answered`, 0 `open`, 0 `blocked` |
| Angenommene ADRs | **12** (A1) |
| **Mappingkonvention** | **entschieden** — ADR-0008; **0 Mappings, 0 Quellen, Gate `NOT EVALUATED`** |
| **Sicherheitsgrundlage** | **spezifiziert** — ADR-0009; **12 Kontrollen `DOCUMENTED ONLY`**, Readiness Gate `NOT EVALUATED` |
| **Runtime Skeleton** | **lokal implementiert** (CBP-WP-012) — Python-Standardbibliothek, `run` fail-closed, **nicht produktionsbereit** |
| **Ingest-Quarantäne MVP** | **lokaler Prototyp** (CBP-WP-013, ADR-0010) — synthetic-only, fail-closed, content-addressed Store außerhalb Repo, **keine Promotion**; **nicht produktiv** |
| **Source-Registry MVP** | **lokaler Prototyp** (CBP-WP-014, ADR-0011) — synthetic-only, fail-closed, **deaktiviert**, deterministische Source IDs, unveränderliche Records, append-only Retirement, minimierter Katalog; `activate` verweigert; **nicht produktiv** |
| **Source-Mapping-Draft-Validator MVP** | **lokaler Prototyp** (CBP-WP-015, ADR-0012) — synthetic-only, read-only, fail-closed, **31-Feld-Vertrag** (29 Pflicht + 2 optional), externe read-only Registry-Bindung, `mapping_id` nur validiert, nicht persistierter Report; `activation-check` verweigert; **315 Tests**, **nicht produktiv** |
| **Repository-Zielstruktur** | **entschieden** — Ziel-Monorepo (D-029, ADR-0007); **Migration nicht autorisiert** |
| **Bereichsmodell** | **W-3** — privater Operator-Workspace außerhalb des Core-Repositorys (D-030); **nicht angelegt** |
| **Veröffentlichung** | Core-Repository `publication-capable by design`, **bleibt privat** — Freigabe benötigt A0 (OD-11) |
| DRC | **NOT EVALUATED** |
| Benchmark | **entworfen, nicht ausgeführt** (Dataset 2.0.0) |
| Technische Implementierung | **Skeleton + Quarantäne- + Registry- + Mapping-Draft-Validator-Prototyp lokal** (CBP-WP-012/013/014/015) — keine KB-Kontrolle durchgesetzt, keine Quelle angebunden, kein Mapping gespeichert, nichts aktiviert |
| Implementierte Capabilities | **keine (0 von 29)** — lokale Bausteine belegt; **Capability 2/3/5/6/7 bleiben nicht vollständig `implemented`** |

> **Criteria complete ≠ Technical implementation ≠ Deployment ready.**
> G0 sperrt den Produkt- und Pilot-Scope. **16 der 25 Kriterien beschreiben
> Kontrollen, die nicht existieren.** Die Freigabe autorisiert ausschließlich
> die **Planung** von Phase 1 — siehe
> [docs/roadmap/PHASE_1_BACKLOG.md](docs/roadmap/PHASE_1_BACKLOG.md).

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
