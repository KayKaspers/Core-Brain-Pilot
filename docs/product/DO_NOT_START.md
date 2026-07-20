# Do Not Start — Verbindliche Sperrliste Phase 0

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Autoritaetsklasse | A0 (ausdruecklicher Human-Maintainer-Beschluss) |
| Stand | 2026-07-20 |

Die folgenden Arbeiten sind in Phase 0 **nicht begonnen** und duerfen **nicht
begonnen werden**. Die Liste hat A0-Rang: sie wird nicht durch Dokumentation,
Roadmap-Formulierungen oder abgeleitete Zusammenfassungen aufgeweicht.

## Gesperrt

| # | Gegenstand |
| --- | --- |
| 1 | Produktive Implementierung |
| 2 | Docker Compose |
| 3 | Web-UI |
| 4 | Suchintegration |
| 5 | Wiki-Ingest |
| 6 | Knowledge Graph |
| 7 | Obsidian-Synchronisation |
| 8 | MCP-Integration |
| 9 | Externe Connectoren |
| 10 | Automatisierte Commits |
| 11 | Oeffentliches Branding |

## Warum eine Sperrliste

Phase 0 dient dem **Scope Lock**. Jede vorgezogene Implementierung schafft
Fakten, die eine noch nicht getroffene Architekturentscheidung praejudizieren.
Ein Docker-Compose-File vor dem Scope Lock ist keine Vorarbeit, sondern eine
unbemerkt getroffene Entscheidung.

## Was das konkret ausschliesst

Auch dann gesperrt, wenn es klein wirkt:

- "nur ein Geruest" fuer Compose, UI oder Ingest,
- ein Proof of Concept fuer die Suche,
- ein Testskript, das eine Quelle abruft,
- CI-Workflows,
- eine `LICENSE`-Datei (Lizenzwahl ist eine offene A0-Entscheidung),
- ein Git-Remote oder Push,
- Logos, Wortmarken, oeffentliche Beschreibungen.

## Was erlaubt ist

Dokumentation. Genauer: Markdown-Dokumentation, `.gitignore` und Ordner fuer
Projektdokumentation — im Rahmen des jeweils freigegebenen Work Packages.

## Aufhebung

Ein Punkt dieser Liste wird ausschliesslich durch einen **ausdruecklichen
Beschluss des Human Maintainers** (A0) aufgehoben, dokumentiert als ADR in
[docs/decisions/](../decisions/README.md) und nachgefuehrt in
[project-system/CAPABILITY_MATRIX.md](../../project-system/CAPABILITY_MATRIX.md).

Ein Implementation Agent hebt keinen Punkt selbst auf und leitet keine
Aufhebung aus dem Kontext ab. Im Zweifel: anhalten und melden.
