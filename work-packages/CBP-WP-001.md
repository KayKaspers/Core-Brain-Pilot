# CBP-WP-001 — Repository Bootstrap und dokumentarisches Projektfundament

| Feld | Wert |
| --- | --- |
| ID | CBP-WP-001 |
| Typ | `docs-only` |
| Prompt Mode | deklariert "Lean" → ausgefuehrt als **Standard** (AB-01) |
| Context Budget | B2 – Standard |
| Phase | Phase 0 – Discovery und Scope Lock |
| Ausgefuehrt am | 2026-07-20 |
| Status | `in-review` |
| Autoritaetsklasse | A2 |

Dieses Dokument haelt den **Wortlaut** des freigegebenen Work Packages fest.
Es wird nach der Ausfuehrung nicht mehr inhaltlich veraendert; das Ergebnis
steht im Implementation Report an Nova.

---

## Ziel

Erzeuge innerhalb des bereits initialisierten lokalen Repositorys
`D:\Projects\Core-Brain-Pilot` das minimale dokumentarische Projektfundament
fuer Core Brain Pilot. Noch keine Anwendung implementieren.

Verbindliche Grundlagen:

1. die Projektanweisungen dieses Claude-Projekts,
2. die als Projektwissen hinterlegte Core-Brain-Uebergabe,
3. die als Projektwissen hinterlegte Second-Brain-Bauanleitung,
4. Nova Development Framework v1.0.0.

Bei NDF insbesondere zu pruefen: `README.md`, Work-Package-Typen,
Work-Package-Lifecycle, Context Economy, Prompt Modes, Nova-Rollenmodell,
Vorlagen fuer neue Projekte.

Ausschliesslich die freigegebene Version v1.0.0 verwenden. Keine noch nicht
veroeffentlichte v1.1-Planung uebernehmen.

## Vorpruefung

Zunaechst read-only pruefen: Erreichbarkeit, Git-Repository, kein Commit, kein
Remote, keine unerwarteten Dateien. Bei Nichterfuellung: nichts veraendern,
Problem beschreiben, Status BLOCKED melden, STOP.

## Erlaubter Arbeitsbereich

Ausschliesslich `D:\Projects\Core-Brain-Pilot`. Keine benachbarten Ordner
oeffnen oder durchsuchen.

## Erlaubte Aenderungen

Markdown-Dokumentation, `.gitignore`, Ordner fuer Projektdokumentation.

## Verbotene Aenderungen

Ausfuehrbarer Anwendungscode, Dockerfile, `compose.yaml`, Skripte,
CI-Workflows, Datenbanken, Binaerdateien, Modellartefakte, Secrets,
Zugangsdaten, `LICENSE`-Datei, Git-Remote, Commit, Push, Dateien ausserhalb
des Projektordners.

## Projektstatus

Phase 0 – Discovery und Scope Lock. Noch keine produktive Installation oder
Implementierung.

## Projektdefinition

Core Brain Pilot ist ein serverzentriertes und portables KI-Wissens- und
Arbeitssystem. Ziel ist, Claude und anderen Implementation Agents nur die
kleinste ausreichende Menge relevanter, aktueller, autoritativer und
datenschutzrechtlich erlaubter Informationen bereitzustellen.

Proxmox ist die erste Referenzplattform, aber nicht die Produktgrenze. Docker
Compose ist als bevorzugte spaetere Anwendungslaufzeit innerhalb einer
dedizierten Linux-VM vorgesehen.

## Verbindliche Kernprinzipien

Kanonischer Markdown-Wissensbestand · Git-Historie fuer kuratierte Inhalte ·
reproduzierbare abgeleitete Daten · deterministischer Quellenindex · lokale
Hybrid-Suche · Brain-First-Retrieval · A0–A6-Autoritaetsmodell · Datenklassen
und technische Datenschutzregeln · Context Budgets B0–B4 · reproduzierbare
Context Packs · erklaerbarer Retrieval-Trace · menschlich kontrollierte
Konfliktaufloesung · private Mehrgeraete-Nutzung · deployment-neutrale
Architektur · austauschbare Suche und Web-UI · Backup-, Restore- und
Rebuild-Faehigkeit.

## Datenklassen

`public` · `internal` · `confidential` · `secret` · `excluded-from-ai`

Secrets duerfen nicht in Repository, Wissensbestand, Index, Context Pack oder
Modellkontext gelangen.

## Geplante Capabilities

Als `planned`, `discovery` oder `not-started` zu erfassen. Keine darf als
`implemented` bezeichnet werden:

1. kanonischer Markdown-Wissensbestand · 2. Source Manifest · 3. stabile
Source-ID und Content Hash · 4. Owner- und Verifikationsmodell ·
5. Ingest-Quarantaene · 6. Secret- und PII-Pruefung · 7. deterministischer
Quellenindex · 8. inkrementelle Indexierung mit Tombstones · 9. Volltext-,
semantische und hybride Suche · 10. Brain-First-Retrieval ·
11. Autoritaetsfilter · 12. Datenschutzfilter · 13. Aktualitaetsfilter ·
14. zeitliche Gueltigkeit und Supersession · 15. erklaerbarer Retrieval-Trace ·
16. Context Budgets B0–B4 · 17. reproduzierbare Context Packs · 18. Konflikt-
und Review-Queues · 19. Verifikations-Queues · 20. Quellen- und
Collection-Berechtigungen · 21. Vault Doctor · 22. Retrieval-Benchmarks und
Regressionstests · 23. atomare Aenderungen und Mehrschreiberschutz ·
24. private Mehrgeraete- und Mobile-Nutzung · 25. Docker-Compose-Betrieb ·
26. austauschbare Web-UI · 27. read-only MCP/API · 28. Backup, Restore und
Rebuild · 29. deployment-neutrale Architektur.

## Zielstruktur

```
D:\Projects\Core-Brain-Pilot
├── .gitignore
├── CLAUDE.md
├── README.md
├── docs
│   ├── architecture
│   │   ├── PROJECT_DEFINITION.md
│   │   ├── ARCHITECTURE_PRINCIPLES.md
│   │   └── TRUST_BOUNDARIES.md
│   ├── decisions
│   │   └── README.md
│   ├── discovery
│   │   ├── DISCOVERY_QUESTIONS.md
│   │   └── OPEN_INFORMATION.md
│   ├── ndf
│   │   ├── README.md
│   │   └── ADOPTION_NOTES.md
│   ├── privacy
│   │   └── DATA_CLASSIFICATION.md
│   └── product
│       └── DO_NOT_START.md
├── project-brain
│   └── PROJECT_BRAIN.md
├── project-system
│   ├── PROJECT_PROFILE.md
│   ├── PROJECT_MANIFEST.md
│   ├── CAPABILITY_MATRIX.md
│   ├── DECISION_REGISTER.md
│   ├── RISK_REGISTER.md
│   └── WORK_PACKAGE_QUEUE.md
└── work-packages
    └── CBP-WP-001.md
```

Falls NDF v1.0.0 andere kanonische Pfade verlangt: NDF folgen, Abweichung in
`docs/ndf/ADOPTION_NOTES.md` erklaeren, keine parallelen doppelten Strukturen
erzeugen.

## .gitignore

Mindestens auszuschliessen: `.env`, Secret-Dateien, private Schluessel,
IDE-Zustaende, temporaere Dateien, Logs, Caches, Suchindizes, Embeddings,
lokale Datenbanken, Context Packs mit Nutzdaten, Backup-Artefakte,
Betriebssystemdateien. Keine Beispiel-Secrets anlegen.

## Dokumentarische Pruefungen

1. Alle erwarteten Dokumente sind vorhanden.
2. Keine Datei ausserhalb des Zielordners wurde veraendert.
3. Keine Capability wird als implementiert bezeichnet.
4. Alle Statusdokumente nennen Phase 0.
5. Das aktuelle Work Package ist CBP-WP-001.
6. Das naechste Gate ist G0 – Discovery and Scope Lock.
7. Es existiert kein Git-Remote.
8. Es existiert kein Commit.
9. Es wurden keine Secrets erzeugt.
10. Es wurde kein Anwendungscode erzeugt.

Keinen Commit ausfuehren.

## Abschluss

Strukturierter NDF Implementation Report an Nova, danach STOP und auf Review
warten.
