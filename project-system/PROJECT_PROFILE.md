# Project Profile – Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Überarbeitet in | CBP-WP-002 |
| Autoritätsklasse | A2 |
| Stand | 2026-07-20 |

Struktur nach `framework/project-system/templates/PROJECT_PROFILE_TEMPLATE.md`
(NDF v1.0.0).

## Ziel

Ein serverzentriertes und portables KI-Wissens- und Arbeitssystem, das Claude
und anderen Implementation Agents die kleinste ausreichende Menge relevanter,
aktueller, autoritativer und datenschutzrechtlich erlaubter Informationen
bereitstellt.

**Anlass:** zu hoher Token- und Kontextverbrauch. Das System soll keine
Nutzungslimits umgehen, sondern vorhandenen Kontext effizienter nutzen.

## Zielgruppe

Ein privater Human Maintainer mit mehreren Geräten einschließlich mobiler
Nutzung. Kein Mehrmandantenbetrieb in Phase 0.

Sekundär: Implementation Agents (Claude Desktop und andere) als maschinelle
Konsumenten des Retrieval-Pfads.

Eine spätere öffentliche Zielgruppe ist offen — Phase 7 entscheidet, ohne
Vorfestlegung zugunsten eines öffentlichen Produkts.

## Kernfunktionen

Alle geplant, **keine implementiert**. Priorisiert nach P0 bis Deferred in
[CAPABILITY_MATRIX.md](CAPABILITY_MATRIX.md).

**P0 — Voraussetzung für den Retrieval-Pilot** (17 Capabilities): kanonischer
Markdown-Bestand, Source Manifest, stabile Source-ID und Hash, Secret- und
PII-Prüfung, deterministischer Index, inkrementelle Indexierung mit Tombstones,
Volltext- und semantische Suche, Brain-First-Retrieval, Autoritäts- und
Datenschutzfilter, Retrieval-Trace, Context Budgets, Context Packs, Konflikt-
und Review-Queues, Berechtigungsmodell, Vault Doctor, Benchmarks,
Backup/Restore/Rebuild, Deployment-Neutralität.

**Deferred:** Graph-Web-App, vollständiger Wiki-Ingest, Multi-Tenant-SaaS,
Kubernetes, Proxmox-API-Integration, autonome Konfliktentscheidung, autonome
Commits und Pushes.

## Technische Basis

**Noch nicht festgelegt.** Feststehende Rahmenbedingungen:

| Aspekt | Festlegung |
| --- | --- |
| Kanonisches Format | Markdown |
| Versionierung | Git |
| Index und Suche | lokal, selbst gehostet, austauschbar |
| Sprachverarbeitung | **nicht lokal** — Claude Code überträgt ausgewählte Inhalte |
| Web-UI | austauschbar, nicht vor dem Retrieval-Pilot-Gate |
| Programmiersprache | offen (OD-20) |
| Suchmaschine | offen; qmd ist Kandidat mit Prüfvorbehalt (OD-25) |
| Embedding-Modell | offen (OD-20) |
| Datenhaltung abgeleitet | offen |

## Deployment

| Aspekt | Festlegung | Status |
| --- | --- | --- |
| Referenzplattform | Proxmox | erste Referenz, **nicht** Produktgrenze |
| Referenzbetrieb | dedizierte Linux-VM | Profile A und B |
| Anwendungslaufzeit | Docker Compose innerhalb der VM | Profil D, **kein Pflichtziel der ersten Phase**, gesperrt in Phase 0 |
| Architekturbindung | keine | deployment-neutral |

Fünf Referenzprofile A bis E in
[../docs/architecture/PROJECT_DEFINITION.md](../docs/architecture/PROJECT_DEFINITION.md).

Es existiert **keine** Installation.

## Risiken

29 erfasste Risiken, davon 14 mit Schweregrad hoch. Vollständig in
[RISK_REGISTER.md](RISK_REGISTER.md).

Die gravierendsten:

- Berechtigungen bestehen nur als Promptregel, nicht technisch (R-25)
- Datenschutzklassifikation ohne technische Durchsetzung (R-30)
- Restore wurde nie geprobt (R-20)
- Secret in der Git-Historie wäre praktisch irreversibel (R-01)
- Abgeleitete Inhalte (A6) überschreiben kuratierte (A0–A5) (R-06)

## Bekannte Einschränkungen

- Kein lauffähiges System, kein Wissensbestand, kein Index
- Scope **nicht** gelockt; G0 ist NOT PASSED, kein Kriterium beantwortet
- Sämtliche Infrastruktur- und Netzwerkangaben unbekannt
- Keine der mindestens 30 Benchmarkfragen formuliert (OI-06)
- Repository-Struktur nicht freigegeben (OI-07)
- Keine Lizenz festgelegt
- Kein Retrieval-Benchmark, damit keine Qualitätsaussage möglich
- PDF-Fließtext lokal nicht extrahierbar; Auswertung über A6-Textfassung
  (R-22, R-23)

## Roadmap

| Phase | Inhalt | Status |
| --- | --- | --- |
| **Phase 0** | Discovery und Scope Lock | **laufend** |
| **Gate G0** | Discovery and Scope Lock | **NOT PASSED** |
| Phase 1 | Proxmox-Referenzumgebung | nicht begonnen |
| Phase 2 | Wissensfundament | nicht begonnen |
| Phase 3 | Retrieval-Pilot | nicht begonnen |
| Phase 4 | Mehrgeräte- und Mobile-Pilot | nicht begonnen |
| Phase 5 | Wiki-Pilot | nicht begonnen |
| Phase 6 | Portabilität | nicht begonnen |
| Phase 7 | Öffentliche Entscheidung | nicht begonnen |

Vollständig in
[../docs/architecture/PROJECT_DEFINITION.md](../docs/architecture/PROJECT_DEFINITION.md).

## NDF-Notizen

Framework: **Nova Development Framework v1.0.0**, verbindlich, ausschließlich
freigegebene Version. Keine v1.1-Planung. Kein zweites Governance-System.

Zehn dokumentierte Abweichungen AB-01 bis AB-10 in
[../docs/ndf/ADOPTION_NOTES.md](../docs/ndf/ADOPTION_NOTES.md). AB-01, AB-02
und AB-09 sind entschieden, AB-10 ist aufgehoben, AB-03 bis AB-08 sind nur
vorläufig für den Bootstrap akzeptiert und vor G0 zu entscheiden.
