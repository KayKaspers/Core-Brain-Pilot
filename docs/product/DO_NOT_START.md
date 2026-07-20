# Do Not Start — Verbindliche Sperrliste Phase 0

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Überarbeitet in | CBP-WP-002 |
| Autoritätsklasse | **A0** |
| Stand | 2026-07-20 |

Die folgenden Arbeiten sind **nicht begonnen** und dürfen **nicht begonnen
werden**. Die Liste hat A0-Rang: sie wird nicht durch Dokumentation,
Roadmap-Formulierungen oder abgeleitete Zusammenfassungen aufgeweicht.

## Gesperrt

Zusammenführung der Sperrliste aus CBP-WP-001 und Projektübergabe §17.
*Erweitert in CBP-WP-002 als F-10 und F-13.*

| # | Gegenstand | Quelle |
| --- | --- | --- |
| 1 | Produktive Implementierung | CBP-WP-001 |
| 2 | Docker Compose | CBP-WP-001 |
| 3 | Web-UI | CBP-WP-001 |
| 4 | Suchintegration | CBP-WP-001 |
| 5 | Wiki-Ingest — auch teilweise | CBP-WP-001, Übergabe §17 |
| 6 | Knowledge Graph / eigene Graph-Web-App | CBP-WP-001, Übergabe §17 |
| 7 | Obsidian-Synchronisation | CBP-WP-001 |
| 8 | MCP-Integration | CBP-WP-001 |
| 9 | Externe Connectoren | CBP-WP-001 |
| 10 | Automatisierte Commits und Pushes | CBP-WP-001, Übergabe §17 |
| 11 | Öffentliches Branding | CBP-WP-001, Übergabe §17 |
| 12 | **Öffentliche Produktveröffentlichung** | Übergabe §17 |
| 13 | **Endgültiges Branding** | Übergabe §17 |
| 14 | **Automatische Repository-Änderungen** | Übergabe §17 |
| 15 | **Automatische Konfliktentscheidung** | Übergabe §17 |
| 16 | **Produktive Mehrgeräte-Synchronisation ohne Test-Vault** | Übergabe §17 |
| 17 | **Kubernetes** | Übergabe §17 |
| 18 | **Multi-Tenant-Betrieb** | Übergabe §17 |
| 19 | **SaaS** | Übergabe §17 |
| 20 | **Proxmox-API-Integration** | Übergabe §10, §17 |
| 21 | **Neue NDF-Skills** | Übergabe §17 |
| 22 | **CDF-Integration** | Übergabe §17 |
| 23 | **CoreOps-Integration** | Übergabe §17 |
| 24 | **CDS-Komponenten** | Übergabe §17 |
| 25 | **Öffentliche Cloudinstanz** | Übergabe §17 |

## Bestätigte Nicht-Ziele — Beleg für G0-Kriterium A-8

Die folgenden Punkte sind **ausdrücklich bestätigte Nicht-Ziele** des ersten
Piloten. Sie belegen G0-Kriterium **A-8** (Explizite Nicht-Ziele), gemappt in
CBP-WP-004.

| # | Nicht-Ziel | Beleg |
| --- | --- | --- |
| 1 | Kein Kubernetes im Pilot | Übergabe §4, §17 · Sperrpunkt 17 |
| 2 | Kein Multi-Tenant-SaaS | Übergabe §4, §17 · D-018 · Sperrpunkte 18, 19 |
| 3 | Keine öffentliche Cloudinstanz | Übergabe §17 · Sperrpunkt 25 |
| 4 | Keine Proxmox-API-Integration | Übergabe §10, §17 · ADR-0001 · Sperrpunkt 20 |
| 5 | Kein vollständiger Wiki-Ingest | Übergabe §17 · D-025 · Sperrpunkt 5 |
| 6 | Kein Knowledge Graph im ersten Pilot | D-025 · Sperrpunkt 6 |
| 7 | Keine automatische Konfliktentscheidung | Übergabe §10, §17 · Sperrpunkt 15 |
| 8 | Keine automatischen Commits und Pushes | Übergabe §10, §17 · D-003 · Sperrpunkt 10 |
| 9 | Keine breite Connector-Integration | D-025 · Sperrpunkt 9 |
| 10 | Keine produktive Obsidian-Synchronisation ohne Test | Übergabe §9, §17 · D-025 · Sperrpunkt 16 |
| 11 | Kein öffentliches Branding oder Release | Übergabe §17 · Sperrpunkte 11, 12, 13 |

Alle elf sind durch A0-Quellen gedeckt und in der Sperrliste oben enthalten.

> **Nicht Teil von A-8:** Die Frage, ob das Repository **dauerhaft privat**
> bleibt, ist eine Sichtbarkeitsentscheidung und keine Nicht-Ziel-Festlegung.
> Sie wird gesondert als **OD-11** geführt und bleibt offen.

## Zweites Governance-System

Superpowers **darf als Referenz untersucht werden**, aber **nicht parallel als
zweites Governance-System eingeführt werden**. Verbindlich ist NDF v1.0.0.

*Quelle: Projektübergabe §14. Ergänzt in CBP-WP-002 als F-13; erfasst als
Risiko R-28.*

## Warum eine Sperrliste

Phase 0 dient dem **Scope Lock**. Jede vorgezogene Implementierung schafft
Fakten, die eine noch nicht getroffene Architekturentscheidung präjudiziert.
Ein Docker-Compose-File vor dem Scope Lock ist keine Vorarbeit, sondern eine
unbemerkt getroffene Entscheidung.

## Was das konkret ausschließt

Auch dann gesperrt, wenn es klein wirkt:

- „nur ein Gerüst" für Compose, UI oder Ingest
- ein Proof of Concept für die Suche
- ein Testskript, das eine Quelle abruft
- CI-Workflows
- eine `LICENSE`-Datei (Lizenzwahl ist eine offene A0-Entscheidung, OD-23)
- ein Git-Remote-Wechsel oder Push
- Logos, Wortmarken, öffentliche Beschreibungen

## Was erlaubt ist

Markdown-Dokumentation, `.gitignore` und Ordner für Projektdokumentation — im
Rahmen des jeweils freigegebenen Work Packages.

## Bedingte Sperren

Zwei Punkte sind nicht dauerhaft gesperrt, sondern an ein Gate gebunden:

| Gegenstand | Bedingung |
| --- | --- |
| Wiki, Graph, eigene Web-UI | **Nicht vor einem bestandenen Retrieval-Pilot-Gate** (D-014) |
| Produktive Synchronisation | Nicht vor Prüfung mit einem Test-Vault auf Konflikte, Datenverlust und Backupfähigkeit |

Projektübergabe §9 nennt als Bedingungen für eine Oberfläche: Index und Suche
funktionieren, Tokenersparnis ist belegt, Mehrgerätezugriff funktioniert, der
Alltagsnutzen ist bestätigt.

## Aufhebung

Ein Punkt dieser Liste wird ausschließlich durch einen **ausdrücklichen
Beschluss des Human Maintainers** (A0) aufgehoben, dokumentiert als ADR in
[../decisions/](../decisions/README.md) und nachgeführt in
[../../project-system/CAPABILITY_MATRIX.md](../../project-system/CAPABILITY_MATRIX.md).

Ein Implementation Agent hebt keinen Punkt selbst auf und leitet keine
Aufhebung aus dem Kontext ab. Im Zweifel: anhalten und melden.
