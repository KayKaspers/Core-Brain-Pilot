# Project Manifest – Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Überarbeitet in | **CBP-WP-016** |
| Autoritätsklasse | A2 |
| Stand | 2026-07-21 |

> **Formatabweichung.** NDF v1.0.0 sieht `project-system/project-manifest.yaml`
> vor. Diese Markdown-Fassung ist **vorläufig für den Bootstrap** akzeptiert —
> AB-03, OD-13.

## Identität

| Feld | Wert |
| --- | --- |
| Interner Arbeitstitel | Core Brain Pilot |
| Kurzform | CBP |
| WP-Präfix | `CBP-WP-` |
| Art | KI-Wissens- und Arbeitssystem, serverzentriert und portabel |
| Sichtbarkeit | **PUBLIC** — Repository Visibility durch **D-069** (A0, 2026-10-17) bestätigt, **OD-11 beantwortet** · Development State **PRIVATE DEVELOPMENT**. Core-Repository ist `publication-capable by design` — **Product Publication NOT AUTHORIZED**; eine Produktveröffentlichung benötigt A0. ADR-0015 `accepted` (A1, 2026-10-17) |
| Sprache Dokumentation | Deutsch, UTF-8 mit echten Umlauten |
| Lizenz | **nicht festgelegt** (OD-23) |
| Öffentlicher Produktname | **nicht beschlossen** (OD-28) |

## Framework

| Feld | Wert |
| --- | --- |
| Framework | Nova Development Framework **v1.0.0**, verbindlich |
| v1.1-Planung | **nicht** übernommen |
| Zweites Governance-System | **ausgeschlossen** |
| Abweichungen | AB-01 bis AB-10; AB-03 bis AB-08 nur vorläufig |

## Status

| Feld | Wert |
| --- | --- |
| Phase | **Phase 0 – COMPLETE** · Phase 1 AUTHORIZED FOR PLANNING |
| Aktuelles Work Package | **CBP-WP-025** — *GitHub Repository Ownership Transfer & Rename Governance*, **P0** — registriert durch **D-071** (`accepted`, **A0**, 2026-10-26); **Phase X1** ausgeführt, `in-review`, **nicht committed**; **X2 bis X6 und X4b nicht autorisiert** — kein Transfer, keine Umbenennung, kein Remote-Wechsel; [CBP-WP-025.md](../work-packages/CBP-WP-025.md). Unabhängig davon **CBP-WP-024** — *Synthetic Brain-First Lexical Retrieval Slice (V1 Foundation)*, P1 — registriert durch **D-070** (`accepted`, **A0**, 2026-10-22); **Phase B0 – Registration & Governance Preparation** `committed` (`dd72c3f`, Human-Commit und -Push 2026-10-23), Gesamt-Work-Package `in-review`; **B1, B2, B3 und C nicht autorisiert** — keine technische Implementierung, keine Suchintegration (DO_NOT_START #4 unverändert), `KB04-T-N07` bleibt zurückgestellt (D-066); [CBP-WP-024.md](../work-packages/CBP-WP-024.md). Der vorherige Ruhezustand nach der dokumentarischen Closure von CBP-WP-022 (begrenzte Auslegung von Queue-Regel 4, Human-Maintainer-A0 vom 2026-10-19) endete mit dieser Registrierung. Zuletzt abgeschlossen: **CBP-WP-022** (`committed`, `complete`, 2026-10-20; dokumentarische Closure in **Phase C** an der **D-068**-Grenze; letzte Ausführungsphase **B2D-E-N14-GOV – D-067 N14 Ephemeral Observation Bridge Classification**) — **D-057** Registrierung, **D-058** ADR-Gate (**`ADR_REQUIRED`**), **D-059** Architekturannahme und **D-060** Enforcement Contract (alle `accepted`, **A0**, 2026-08-03); **ADR-0014 `accepted`, A1** — **Host-authoritative Enforcement mit deklarativem Zielmodell und read-only Runtime-Validierung**; Vertrag: [KB_04_STAGE_1_ENFORCEMENT_CONTRACT.md](../docs/security/KB_04_STAGE_1_ENFORCEMENT_CONTRACT.md); **KB-04 Enforcement Stage 1** = Stufe 1 der neunstufigen Durchsetzungsreihenfolge (**OS-Dateirechte**); B0 `committed` `e4caa14`, B1A `committed` `1a7696d`, B1B `committed` `b86a35f`, B1C `committed` `24de07e`, B2A `committed` `929d10b`, B2B-P `committed` `fff8227`, B2C.1 `committed` `38eb33f`, B2C.2 `committed` `117647f`, B2C-T-R `committed` `9cde9de`, B2D-P `committed` `b409d25`, B2D-GOV `committed` `7e8328a`, B2D-AUTH `committed` `1222ec0`, B2D-ENV-GOV `committed` `0cd21f5`, **B2D-E-N07-GOV `committed` `c4b0426`**; **D-061** (`accepted`, **A0**, `B2C_TRACEABILITY_AND_NT_PREPARATION_SELECTED`, `ADR_NOT_REQUIRED`) begrenzt **B2C** auf Traceability und NT-Vorbereitung; **D-062** (`accepted`, **A0**, `B2C_TRACEABILITY_COVERAGE_SPLIT_RECONCILED`, `ADR_NOT_REQUIRED`, 2026-08-04) setzt den kanonischen Abdeckungssplit über die **45** Contract-Testkennungen auf **37 `SYNTHETIC_COVERED` · 2 `SYNTHETIC_COVERAGE_GAP` (`KB04-T-P10`, `KB04-T-N25`, beide **Contract §10.3**) · 6 `B2D_REAL_ONLY`**; **B2C-T-R setzt die Traceability technisch um**: **drei neue Testdateien** (`tests/kb04_nt_fixtures.py`, `tests/test_kb04_contract_traceability.py`, `tests/test_kb04_nt_preparation.py`) mit den Traceability-Zählern **45 / 37 / 2 / 6**, **152 neuen Tests** und einer Testbasis von **1202 grün, 0 übersprungen**; **B2D-P ergänzt genau eine neue Plandatei** — [KB_04_PROFILE_A_INTEGRATION_PLAN.md](../docs/runtime/KB_04_PROFILE_A_INTEGRATION_PLAN.md), **plan-only**, ohne reale Infrastruktur; **B2D-GOV registriert D-063** (`accepted`, **A0**, `B2D_EXECUTION_PREREQUISITES_ESTABLISHED`, `ADR_NOT_REQUIRED`) sowie die beiden neuen kanonischen Risiken **R-35** und **R-36** (beide **hoch**, **offen**) und entscheidet die Harnessfrage mit **`NO_HARNESS_REQUIRED`**; **B2D-AUTH registriert D-064** (`accepted`, **A0**, `B2D_E_RUN_AUTHORIZATION_ARTIFACT_FORM_SELECTED`, `ADR_NOT_REQUIRED`, 2026-08-05) und legt **genau eine neue Datei** an — [KB_04_B2D_E_RUN_AUTHORIZATION_TEMPLATE.md](../docs/runtime/KB_04_B2D_E_RUN_AUTHORIZATION_TEMPLATE.md), ein **vollständig leeres** Pre-run-Autorisierungstemplate mit **20 Pflichtfeldern** `AUTH-01`…`AUTH-20`; **B2D-ENV-GOV registriert D-065** (`accepted`, **A0**, `B2D_REFERENCE_ENVIRONMENT_PREPARATION_MODEL_SELECTED`, `ADR_NOT_REQUIRED`, 2026-08-05) mit dem Modell **`DEDICATED_NON_PRODUCTION_PROFILE_A_VM_WITH_LOCAL_PER_TARGET_APPROVAL`** — **keine neue Datei**, keine konkrete Instanz; **B2D-E-N07-GOV registriert D-066** (`accepted`, **A0**, `PROFILE_A_RETRIEVAL_NOT_INSTANTIATED_N07_DEFERRED`, `ADR_NOT_REQUIRED`, 2026-08-05) — **Variante C**, **keine neue Datei**, **keine neue Risiko-ID**: die Rolle **`retrieval`** ist derzeit **nicht instanziiert**, **`KB04-T-N07` ist zurückgestellt** und bleibt **`B2D_REAL_ONLY`** mit unveränderter Traceability-Disposition, **`KB04-T-N14`** ist nur nächster Planungskandidat und **nicht autorisiert**; **B2D-E-N14-GOV registriert D-067** (`accepted`, **A0**, `N14_EPHEMERAL_LOCAL_OBSERVATION_BRIDGE_ALLOWED`, `ADR_NOT_REQUIRED`, 2026-08-05) — **Variante B**, **keine neue Datei**, **keine neue Risiko-ID**, **keine Produktionscodeänderung**: erlaubt ist ausschließlich eine **flüchtige, einmalige, run-spezifische und nicht versionierte lokale Observation Bridge** über **`os.lstat`** plus die **vorhandene exportierte** Funktion `validate_observation`; **kein H1-Testhelper, kein Harness, keine CLI, kein Adapterexport, keine Produktionsschnittstelle**, **kein `paths.check_path`**, **kein `Path.resolve()`**, **kein `realpath()`**; **zwölf Überschreitungsgrenzen** lösen eine erneute Decision- und ADR-Prüfung aus; **N14 bleibt nicht ausgeführt**, **NT-05 bleibt nicht ausgeführt**, der Befehlsentwurf trägt weiterhin **Platzhalter**, und **`B2D-E-N14-PREP-N1`** ist erst **nach Commit und Reconciliation** zulässig; Decision-/A0-/ADR-Zähler nach D-067 **67/63/14** (*phasengebunden; aktueller Stand in den Feldern* Getroffene Entscheidungen *und* Angenommene ADRs), **Risiken 35** mit Severity **20/14/1 unverändert**; Traceability **45/37/2/6 unverändert**, Tests **1202 unverändert**; **kein Produktionsmodul, keine §10.3-Implementierung, kein Evidence-Artefakt, kein Harness**; der **erste B2C-T-Lauf** endete `BLOCKED`; **B2C-T-R ist abgeschlossen und `committed` (`9cde9de`)** — **drei Testdateien**, **152 zusätzliche Tests**; **Implementierungspfad** `core/core_brain/enforcement/` — sechs B2A-Module plus die beiden **Plan-only-Module** `filesystem_adapter.py` und `initialization.py`, insgesamt **24 additive `KB04-*`-ReasonCodes** in `errors.py`, **206 + 120 neue Tests** aus B2A und B2B-P (damaliger Gesamtstand nach B2B-P **1050**; zuletzt dokumentierte Gesamtsuite **1202** seit B2C-T-R); **keine CLI, keine Config, kein Deployment, keine Mutation, kein Apply**; KB-04 bleibt **`DOCUMENTED ONLY`**. **B2B-P `committed` (`fff8227`); B2B-Apply, Aggregat B2C und Aggregat B2D nicht autorisiert.** **D-068** (`accepted`, **A0**, 2026-10-15, `WP022_CLOSURE_BOUNDARY_SELECTED_DEFERRED_EXECUTION_REBIND_REQUIRED`, `ADR_NOT_REQUIRED`) wählt die Closure-Grenze — die **dokumentarische Closure an dieser Grenze ist in Phase C vollzogen** (Human-Maintainer-A0 vom 2026-10-19; Abschluss 2026-10-20). Zuvor abgeschlossen **CBP-WP-023** (`committed`, `complete`, 2026-10-19; *Repository Visibility Governance Reconciliation*; **D-069** Teil P, A0; **ADR-0015 `accepted`**, A1; G1 bis G3 `ca63b0a`); davor **CBP-WP-021** (`committed`, `complete`; B0 `0cb4ea9`, B1/B2 `271acc7`, C `0344774`). **CBP-WP-024 ist `in-review` (Phase B0 `committed` `dd72c3f`; B1, B2, B3 und C nicht autorisiert); CBP-WP-025 ist `in-review` (Phase X1, nicht committed; X2 bis X6 und X4b nicht autorisiert); kein Work Package ist `active`** |
| Zuletzt abgeschlossen | **CBP-WP-022** (`committed`, `complete`, 2026-10-20; *KB-04 Enforcement Stage 1*; dokumentarische Closure in **Phase C** an der **D-068**-Grenze — **14** gelieferte Gegenstände; **keine reale Ausführung**, KB-04 **`DOCUMENTED ONLY`**). **Zum Abschluss von CBP-WP-022 war kein Folge-Work-Package registriert oder autorisiert** (Ruhezustand, begrenzte Auslegung von Queue-Regel 4); **seit 2026-10-22 ist CBP-WP-024 registriert** (D-070; Phase B0 `committed` `dd72c3f`, Work Package `in-review`). Zuvor abgeschlossen **CBP-WP-023** (`committed`, `complete`, 2026-10-19; *Repository Visibility Governance Reconciliation*; **D-069** Teil P, A0; **ADR-0015 `accepted`**, A1; G1 bis G3 `ca63b0a`). **Zum Abschluss von CBP-WP-023 war kein Folge-Work-Package autorisiert; CBP-WP-022 blieb bis zu seiner Closure `in-review`.** Davor abgeschlossen **CBP-WP-021** (`committed`, `complete`, 2026-08-03; **D-056**, `ADR_NOT_REQUIRED`; kanonisches Security-Testinventar **32 / 1 / 33**, **0 von 32** und **0 von 1** ausgeführt; B0 `0cb4ea9`, B1/B2 `271acc7`). **Zum Abschluss von CBP-WP-021 war kein Folge-Work-Package autorisiert; seitdem ist CBP-WP-022 registriert (D-057, `e4caa14`); es stand bis zu seiner Closure auf `in-review`.** Noch davor abgeschlossen **CBP-WP-020** (`committed`, `complete`; **D-055**; **Z1 erreicht / S2 abgeschlossen / P1 eingehalten**; B0 `17057e2`, B1/B2 `9c6c0fb`, C `d6a1a3c`) |
| **Kanonisches Security-Testinventar** | **32 Negativtests · 1 Positivtest · 33 Testfälle** (D-056) — **0 von 32** und **0 von 1** ausgeführt; **NT-25 nicht aktiv** (TT-5), **NT-32/NT-33 gültig**; die Zahl **31** ist überholt. **In B1/B2 reconciliiert** — Dokumente, `bundle.json`, `validate.py` und Bundle-Tests |
| **Gate-Status G0** | **PASSED WITH NOTES** — 2026-07-21, A0 |
| Nächstes Prüfmodell | **Deployment Readiness Check** — **`APPROVED BY HUMAN MAINTAINER`** (Profil A, 2026-07-29; 19 Prüfpunkte, **19 `ready` / 0 `blocked`**, D-054); **rein dokumentarisch, keine Installationsfreigabe** |
| Phase-1-Planung | Streams F1–F5; CBP-WP-016 **`committed`** (`04c427c`, D-050); CBP-WP-017 **`committed`** (`d3168c4`, D-051); CBP-WP-018 **`committed`** (ADR-0013/D-052/D-053; B0 `4dec921`, B1 `5ee2e83`); CBP-WP-019 **`committed`** (`3c437f2`, D-054, Deployment Readiness Intake, DRC für Profil A freigegeben); CBP-WP-020 **`committed`** und **`complete`** (D-055, Controlled Profile-A Deployment Foundation; B0 `17057e2`, B1/B2 `9c6c0fb`, C `d6a1a3c`); CBP-WP-021 **`committed`** und **`complete`** (D-056, Canonical Security Test Inventory Reconciliation; B0 `0cb4ea9`, B1/B2 `271acc7`) |
| **Runtime Skeleton** | **lokal implementiert** (CBP-WP-012) — `run` fail-closed; keine KB-Kontrolle durchgesetzt |
| **Ingest-Quarantäne MVP** | **lokaler Prototyp** (CBP-WP-013, ADR-0010) — synthetic-only, fail-closed, keine Promotion, **nicht produktiv** |
| **Source-Registry MVP** | **lokaler Prototyp** (CBP-WP-014, ADR-0011) — synthetic-only, fail-closed, **deaktiviert**, `activate` verweigert, **nicht produktiv** |
| **Source-Mapping-Draft-Validator MVP** | **lokaler Prototyp** (CBP-WP-015, ADR-0012) — synthetic-only, read-only, fail-closed, **31-Feld-Vertrag** (29+2), externe read-only Registry-Bindung, `mapping_id` nur validiert, `activation-check` verweigert, **nicht produktiv** |
| **Mapping-Activation-Gate-Evaluator MVP** | **lokaler Prototyp** (CBP-WP-016, D-050) — synthetic-only, read-only, nicht persistent, fail-closed; **20 Gate-Kriterien**, Ausgabestatus nur `NOT_EVALUATED`/`BLOCKED`, `activation-evaluate` endet immer `BLOCKED` (Exit 14); Security Foundation/DRC keine Kriterien 21/22; **nicht produktiv** |
| **Synthetic Evidence Contract 3.0 MVP** | **lokaler Prototyp** (CBP-WP-018, ADR-0013, D-052/D-053, `committed` `5ee2e83`) — Evidence-Schema 3.0 mit eingebetteten Artefakten, `security-control-form` + `control_id`, Provenance-/Binding-Hashes inkl. Security-Contract-Bindung, deterministische Invalid-/Stale-/Conflict-Erkennung, **negative-evidence-only**; Schema 1.0 **und 2.0** fail-closed; kein RT-2/Persistenz/Aktivierung; **558 Tests**, **nicht produktiv** |
| **Security Foundation Readiness Contract MVP** | **lokaler Prototyp** (CBP-WP-018, ADR-0013, D-053, `committed` `5ee2e83`) — statischer, reiner Vertrag 1.0 ohne I/O/Uhr/Zufall/Netz; **12 dokumentierte / 7 runtime-scoped Controls / 11 `(criterion, control_id)`-Bindungen**; ausschließlich synthetische Formprüfung, rein negative Faltung; **keine** Security-Evaluation, **kein** Enforcement, **keine** Readiness-Aussage; **nicht produktiv** |
| **Profile-A Deployment Bundle** | **Repository-Artefakt, `committed` `9c6c0fb`** (CBP-WP-020, D-055) — **genau sieben Dateien** unter `deployments/profile-a/`; zwei getrennte Service-Identitäten, fail-closed Compose- und Konfigurationsvorlagen, maschinenlesbare Mount-/Egress-/Secret-/Backup-/RT-2-Verträge; **deterministischer Offline-Validator** (`PROFILE-A-BUNDLE VALID`, `issues=0`, Exit 0, byte-identisch wiederholbar); **166 Bundle-Validation-Tests**, Gesamttestzahl **724** (0 übersprungen); Status ausschließlich *repository artifact implemented* / *offline validation passed* — **nicht deployed, nicht operational, nicht production-ready** |
| **Mappingkonvention** | **entschieden** — ADR-0008 (D-031, D-032, D-033); Draft-Validator ADR-0012 (D-046…D-049) |
| **Mapping Activation Gate** | **`NOT EVALUATED`** — 0 Mappings, 0 angebundene Quellen |
| **Repository-Zielstruktur** | **entschieden** — Monorepo, ADR-0007 (D-029); **Migration nicht autorisiert** |
| **Bereichsmodell** | **W-3** — Operator-Workspace außerhalb (D-030); **nicht angelegt** |
| **Veröffentlichung** | **Product Publication NOT AUTHORIZED** — Repository Visibility **PUBLIC** (D-069, A0) ist keine Produktveröffentlichung; eine Produktveröffentlichung benötigt eine separate A0-Entscheidung, Lizenz (OD-23) und Produktname (OD-28) bleiben offen |
| Technische Nachweise | **0** — alle Artefakte auf Stufe 1 `dokumentiert` |
| G0-Kriterien | **47** |
| davon blockierend (Core Required) | **25** |
| davon `accepted` | **25** — alle |
| Kriterienstand | 25 von 25 `accepted` |
| Capabilities implementiert | **0** von 29 — Capability 2/3/5/6/7 bleiben nicht vollständig `implemented` |
| Getroffene Entscheidungen | **71** (davon **67** mit A0) |
| Angenommene ADRs | **15** |
| Scope gelockt | **ja** — mit Auflagen |

## Repository

| Feld | Wert |
| --- | --- |
| Pfad | `D:\Projects\Core-Brain-Pilot` |
| Branch | `main` |
| Commits | **29** — aktueller Git-Gesamtzähler auf `main`, HEAD `9c6c0fb` |
| Remote | `origin` → `https://github.com/KayKaspers/Core-Brain-Pilot.git` |
| Commit-Autorität | ausschließlich Human Maintainer |

## Pilotumfang

Festgelegt im Human Discovery Intake, CBP-WP-003. Profilebene, keine
Installationswerte.

| Dimension | Festlegung |
| --- | --- |
| Betriebsprofil | Proxmox-VM mit dedizierter Linux-VM (D-015) |
| Anwendungslaufzeit | Docker Compose bevorzugt innerhalb der VM (D-016) |
| Portabilität | Linux-VM, Docker/OCI, Einzelplatz bleiben dokumentierbar (D-017) |
| Nutzung | Einzelperson; Multi-User kein Pflichtumfang (D-018) |
| Quellen im Pilot | Markdown, Git, Chat-Handoffs, Obsidian-Vault als Markdown |
| Datenklassen im Pilot | `public`, `internal` |
| Zugriff | privates VPN oder privates Netz, keine öffentliche Freigabe (D-023) |
| Im Pilot | Web-UI (nach Retrieval), mobile Nutzung (D-024) |
| Vertagt | native Obsidian-Nutzung, Wiki-Pilot, externe Connectoren, Graph (D-025) |

## Kriterienmodell

| Klasse | Anzahl | Blockiert G0 | Zuständiges Gate |
| --- | --- | --- | --- |
| **Core Required** | 25 | **ja** | G0 |
| Deployment Required | 16 | nein | [Deployment Readiness Check](../docs/operations/DEPLOYMENT_READINESS_CHECK.md) — **APPROVED BY HUMAN MAINTAINER** für Profil A, 19 Prüfpunkte (17 G0-abgeleitet + 2 ohne G0-Herkunft), alle 19 `ready` |
| Conditional | 6 | nur bei aktivierter Funktion | je nach Funktion |

## Sichere Standardwerte

Architekturdefaults, **keine Behauptungen über die reale Infrastruktur**:

1. Single-User-Betrieb als Einstieg
2. Privater Zugriff
3. Keine öffentliche Dienstfreigabe
4. Keine Secrets in Wissensbestand, Index oder Context Packs
5. **Übertragung an externe KI standardmäßig verweigert**, bis eine Datenklasse sie erlaubt
6. Trennung von canonical und derived; Runtime-Daten getrennt in **RT-1**
   (reproduzierbar), **RT-2 Operational Evidence** (**nicht** reproduzierbar,
   aufbewahrungs- und sicherungspflichtig) und **RT-3** (flüchtig)
7. Keine automatische Konfliktauflösung
8. Keine automatischen Commits oder Pushes
9. Keine Obsidian-Synchronisation als Standard
10. Backup muss vor produktivem Betrieb eingerichtet **und getestet** sein
11. Optionale Funktionen bleiben deaktiviert, bis sie bewusst gewählt werden

## Rollen

| Rolle | Träger | Verantwortung |
| --- | --- | --- |
| Planung | Nova (ChatGPT) | Architektur und Work Packages |
| Ausführung | Implementation Agent (Claude Desktop) | Genau ein freigegebenes Work Package |
| Freigabe | Human Maintainer | Review, GO / GO WITH NOTES / REWORK / SPLIT / STOP, Commit, Push, Veröffentlichung |

## Quellen

| Quelle | Klasse | Ort |
| --- | --- | --- |
| `Bauanleitung_Second-Brain.pdf` | **A4** | außerhalb des Repositorys, sechs Inhaltsseiten |
| `Second-Brain-Bauanleitung-Textfassung.md` | **A6** | außerhalb des Repositorys |
| `docs/discovery/Core-Brain-Project-Handoff.md` | **A5** | im Repository, getrackt |
| `docs/discovery/HUMAN_DISCOVERY_INPUT.md` | **A2** mit einzelnen A0-Entscheidungen | im Repository |
| Nova Development Framework v1.0.0 | **A1** | extern |

## Autoritätsmodell

`A0` Human-Maintainer-Beschluss · `A1` Release, Tag, ADR · `A2` Projektstatus,
WP-Queue · `A3` Roadmap, Gate-Doku · `A4` README, erläuternde Doku ·
`A5` Projektchat-Übergabe · `A6` abgeleitete Zusammenfassung

**A6 überschreibt A0–A5 niemals automatisch.**

## Datenklassen

`public` · `internal` · `confidential` · `secret` · `excluded-from-ai`

Secrets gelangen nicht in Repository, Wissensbestand, Index, Context Pack oder
Modellkontext. Das **Verfahren im Schadensfall ist definiert**
([SECRET_INCIDENT_RESPONSE.md](../docs/security/SECRET_INCIDENT_RESPONSE.md),
OD-10 geschlossen) — **automatische Erkennung fehlt weiterhin** (R-01).

## Context Budgets

`B0` Micro · `B1` Lean · `B2` Standard · `B3` Extended · `B4` Exceptional

**Nicht zu verwechseln mit den NDF Prompt Modes** Full, Standard, Short.
„Lean" ist ausschließlich der Name von B1 (D-009).

## Sperrliste Phase 0

25 gesperrte Gegenstände in
[../docs/product/DO_NOT_START.md](../docs/product/DO_NOT_START.md).
