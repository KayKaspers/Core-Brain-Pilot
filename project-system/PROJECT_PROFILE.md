# Project Profile – Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | **Phase 0 – COMPLETE** · Phase 1 AUTHORIZED FOR PLANNING |
| Überarbeitet in | **CBP-WP-016** |
| Autoritätsklasse | A2 |
| Stand | 2026-07-21 |

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

**Erster Pilot: eine Einzelperson, ein Nutzer** (D-018). Multi-User und
Multi-Tenant sind kein Pflichtumfang; die Architektur darf spätere Teamnutzung
nicht verhindern.

Sekundär: Implementation Agents als maschinelle Konsumenten des
Retrieval-Pfads.

Eine spätere öffentliche Zielgruppe bleibt offen — Phase 7 entscheidet.

## Kernfunktionen

Alle geplant, **keine implementiert**. Priorisiert in
[CAPABILITY_MATRIX.md](CAPABILITY_MATRIX.md).

**P0 — Voraussetzung für den Retrieval-Pilot** (17 Capabilities): kanonischer
Markdown-Bestand, Source Manifest, stabile Source-ID und Hash, Secret- und
PII-Prüfung, deterministischer Index, inkrementelle Indexierung mit Tombstones,
Volltext- und semantische Suche, Brain-First-Retrieval, Autoritäts- und
Datenschutzfilter, Retrieval-Trace, Context Budgets, Context Packs, Konflikt-
und Review-Queues, Berechtigungsmodell, Vault Doctor, Benchmarks,
Backup/Restore/Rebuild, Deployment-Neutralität.

**Durch den Intake vertagt** (D-025): native Obsidian-Nutzung, Wiki-Pilot,
externe Connectoren. **Nicht Pilotumfang:** Knowledge Graph.

**Im Pilot, aber sequenziert** (D-024): Web-UI erst nach funktionierendem
Index, Suche, Brain-First-Retrieval und Benchmark. Mobile Nutzung im Pilot.

## Technische Basis

| Aspekt | Festlegung |
| --- | --- |
| Kanonisches Format | Markdown |
| Versionierung | Git |
| Quellen im Pilot | Markdown-Verzeichnisse, Git-Repositories, Chat-Handoffs, Obsidian-Vault als Markdown |
| Nicht-Markdown-Quellen | PDF und Office **nur über kontrollierte Quarantäne** (D-019) |
| Index und Suche | lokal, selbst gehostet, austauschbar |
| Sprachverarbeitung | **nicht lokal** — ausgewählte Inhalte werden übertragen |
| Web-UI | austauschbar, erst nach funktionierendem Retrieval |
| Programmiersprache | offen (OD-20) |
| Suchmaschine | offen; qmd Kandidat mit Prüfvorbehalt (OD-25) |
| Embedding-Modell | offen |

## Deployment

| Aspekt | Festlegung | Beleg |
| --- | --- | --- |
| Betriebsprofil | **Proxmox-VM mit dedizierter Linux-VM** | D-015 |
| Anwendungslaufzeit | **Docker Compose bevorzugt** innerhalb der VM | D-016 |
| Portabilität | allgemeine Linux-VM, Docker/OCI, Einzelplatz bleiben dokumentierbar | D-017 |
| Zugriff | privates VPN oder privates Netz, **keine öffentliche Freigabe** | D-023 |
| Konkrete Werte | **bewusst nicht erhoben** — Deployment Required | — |

Fünf Referenzprofile A bis E in
[../docs/architecture/PROJECT_DEFINITION.md](../docs/architecture/PROJECT_DEFINITION.md).

Es existiert **keine** Installation.

## Risiken

32 erfasste Risiken, davon 17 hoch. Vollständig in
[RISK_REGISTER.md](RISK_REGISTER.md).

**Weiterhin kritisch:**

- Berechtigungsmodell dokumentiert, aber **technisch nicht durchgesetzt** (R-25, R-27)
- Sperrwirkung von `excluded-from-ai` ungeprüft (R-31)
- Keine Quarantäne für Nicht-Markdown-Quellen (R-32)
- 16 vertagte Deployment-Kriterien; DRC auf **19 Prüfpunkte** erweitert, für Profil A vollständig erhoben (**19 `ready` / 0 `blocked`**) und am 2026-07-29 freigegeben — **APPROVED BY HUMAN MAINTAINER**, rein dokumentarisch (D-054, R-34)
- Benchmark entworfen, nicht ausgeführt — keine Qualitätsaussage (R-21)
- Secret-Schadensverfahren definiert, aber ohne technische Erkennung (R-01)

## Bekannte Einschränkungen

- Kein lauffähiges System, kein Wissensbestand, kein Index
- **Scope gelockt** (G0 PASSED WITH NOTES). Fünf Auflagen sind vor produktivem Betrieb zu erbringen
- Sämtliche konkreten Infrastrukturwerte unbekannt und bewusst nicht erhoben
- Benchmark **entworfen, aber nicht durchgeführt** — keine Messung, keine Qualitätsaussage
- Repository-Struktur nicht freigegeben
- Keine Lizenz festgelegt
- PDF-Fließtext lokal nicht extrahierbar; Auswertung über A6-Textfassung

## Roadmap

| Phase | Inhalt | Status |
| --- | --- | --- |
| **Phase 0** | Discovery und Scope Lock | **COMPLETE** |
| **Gate G0** | Discovery and Scope Lock | **PASSED WITH NOTES** — 2026-07-21 |
| Deployment-Readiness | 16 vertagte Kriterien | [DRC](../docs/operations/DEPLOYMENT_READINESS_CHECK.md) **APPROVED BY HUMAN MAINTAINER** — Profil A, 2026-07-29; 19 Prüfpunkte, **19 `ready` / 0 `blocked`** (D-054); keine Installationsfreigabe |
| **Phase 1** | Proxmox-Referenzumgebung | **AUTHORIZED FOR PLANNING** — [Backlog](../docs/roadmap/PHASE_1_BACKLOG.md), [Foundation Plan](../docs/roadmap/PHASE_1_FOUNDATION_PLAN.md) F1–F5; **OD-26 geschlossen** (ADR-0007), Core-Repository `publication-capable by design` und **weiterhin privat**; **Mappingkonvention entschieden** (ADR-0008), Activation Gate `NOT EVALUATED`; **Sicherheitsgrundlage spezifiziert** (ADR-0009, 12 Kontrollen `DOCUMENTED ONLY`); **Runtime Skeleton lokal implementiert** (CBP-WP-012, `run` fail-closed, nicht produktionsbereit); **Ingest-Quarantäne-MVP lokal implementiert** (CBP-WP-013, ADR-0010, synthetic-only, keine Promotion, nicht produktiv); **Source-Registry-MVP lokal implementiert** (CBP-WP-014, ADR-0011, synthetic-only, deaktiviert, `activate` verweigert, nicht produktiv); **Source-Mapping-Draft-Validator-MVP lokal implementiert** (CBP-WP-015, ADR-0012, synthetic-only, read-only, 31-Feld-Vertrag, externe read-only Registry-Bindung, `activation-check` verweigert, nicht produktiv); **Mapping-Activation-Gate-Evaluator-MVP lokal implementiert** (CBP-WP-016, D-050, synthetic-only, read-only, nicht persistent, 20 Gate-Kriterien, Ausgabestatus nur `NOT_EVALUATED`/`BLOCKED`, `activation-evaluate` endet immer `BLOCKED`, nicht produktiv); **Synthetic-Evidence-Contract-3.0-MVP lokal implementiert** (CBP-WP-018, ADR-0013, D-052/D-053, synthetic-only, eingebettete Artefakte, `security-control-form` + `control_id`, Provenance-/Binding-Hashes inkl. Security-Contract-Bindung, deterministische Invalid-/Stale-/Conflict-Erkennung, negative-evidence-only, Schema 1.0 und 2.0 fail-closed, kein RT-2/Persistenz/Aktivierung, 558 Tests, nicht produktiv); **Security-Foundation-Readiness-Contract-MVP lokal implementiert** (CBP-WP-018, D-053, statischer reiner Vertrag 1.0, 12 dokumentierte / 7 runtime-scoped Controls / 11 `(criterion, control_id)`-Bindungen, nur synthetische Formprüfung, keine Security-Evaluation, kein Enforcement, keine Readiness-Aussage, nicht produktiv); CBP-WP-016 `committed` (`04c427c`, D-050), CBP-WP-017 `committed` (`d3168c4`, D-051); **CBP-WP-018 `committed`** (ADR-0013/D-052/D-053, Phase B0 `4dec921`, Phase B1 `5ee2e83`, Runtime-Stand Evidence Schema 3.0 mit Security Contract 1.0); **CBP-WP-019 `committed`** (`3c437f2`, D-054, Deployment Readiness Intake, DRC-Gesamtstatus **APPROVED BY HUMAN MAINTAINER** für Profil A seit 2026-07-29 bei 19 Prüfpunkten und **19 `ready` / 0 `blocked`**, rein dokumentarisch, Profil-A-Zielbild dokumentiert und **nicht bereitgestellt**); **CBP-WP-022 `in-review`** (D-057 Registrierung, D-058 ADR-Gate, **D-059** Architekturannahme und **D-060** Enforcement Contract (alle **A0**), KB-04 Enforcement Stage 1, **Phase B2A – Contract Model and Read-only Validator**; B0 `committed` `e4caa14`, B1A `committed` `1a7696d`, B1B `committed` `b86a35f`, B1C `committed` `24de07e`; **ADR-0014 `accepted`, Autoritätsklasse A1** — **Host-authoritative Enforcement mit deklarativem Zielmodell und read-only Runtime-Validierung**; **Enforcement Contract `accepted contract`** (`ADR_NOT_REQUIRED` innerhalb ADR-0014); **internes read-only Enforcement-Modul** `core/core_brain/enforcement/` implementiert (sechs Module, 21 additive ReasonCodes, 206 neue Tests) — **keine CLI, keine Config, kein Deployment, keine Mutation, keine operative KB-04-Evidenz**; KB-04 bleibt `DOCUMENTED ONLY`, B2B/B2C/B2D **nicht autorisiert**, **keine reale Bereitstellung**, **kein RT-2**; B2A uncommitted); **CBP-WP-021 `committed` und `complete`** (D-056, Canonical Security Test Inventory Reconciliation, abgeschlossen 2026-08-03; B0 `0cb4ea9`, B1/B2 `271acc7`; kanonisch **32 Negativtests / 1 Positivtest / 33 Testfälle**, **0 ausgeführt**; **NT-25 nicht aktiv** nach TT-5, **NT-32/NT-33 gültig**, die Zahl **31** überholt; Durchführung einschließlich der ausführbaren Profil-A-Artefakte abgeschlossen); **CBP-WP-020 `committed` und `complete`** (D-055, Controlled Profile-A Deployment Foundation; Zielzustand **Z1 erreicht** / Scope **S2 abgeschlossen** / RT-2-Grenze **P1 eingehalten**; B0 `17057e2`, B1/B2 `9c6c0fb`, C `d6a1a3c`; **Profil-A-Bundle als committetes Repository-Artefakt** — genau sieben Dateien unter `deployments/profile-a/`, zwei getrennte Service-Identitäten, fail-closed Compose- und Konfigurationsvorlagen, maschinenlesbare Mount-/Egress-/Secret-/Backup-/RT-2-Verträge, **deterministischer Offline-Validator** mit Exit 0 und `issues=0`, **166 Bundle-Validation-Tests**, Gesamtstand **724 Tests OK, 0 übersprungen**; Status ausschließlich *repository artifact implemented* / *offline validation passed* — **keine Bereitstellung, kein Containerstart, nicht operational**); **CBP-WP-023 nicht registriert, nicht autorisiert** |
| Phase 2 | Wissensfundament | nicht begonnen |
| Phase 3 | Retrieval-Pilot | nicht begonnen |
| Phase 4 | Mehrgeräte- und Mobile-Pilot | nicht begonnen |
| Phase 5 | Wiki-Pilot | nicht begonnen |
| Phase 6 | Portabilität | nicht begonnen |
| Phase 7 | Öffentliche Entscheidung | nicht begonnen |

## NDF-Notizen

Framework **v1.0.0**, verbindlich, keine v1.1-Planung, kein zweites
Governance-System.

Zehn Abweichungen AB-01 bis AB-10. AB-01, AB-02 und AB-09 entschieden, AB-10
aufgehoben, AB-03 bis AB-08 nur vorläufig für den Bootstrap akzeptiert und vor
G0 zu entscheiden (OD-29).
