# Core Brain Pilot

> **Phase 0 abgeschlossen — G0 am 2026-07-21 mit Auflagen freigegeben.**
> Das Repository enthält Dokumentation und seit CBP-WP-012 einen **lokalen,
> fail-closed Foundation Runtime Skeleton** (Python, Standardbibliothek).
> Der Skeleton ist **nicht produktionsbereit**: Er bindet keine Quelle an,
> löst kein Secret auf, öffnet keine Verbindung und startet keine operative
> Runtime — `run` verweigert deterministisch.

Core Brain Pilot ist ein serverzentriertes und portables KI-Wissens- und
Arbeitssystem.

Ziel ist, Claude und anderen Implementation Agents nur die **kleinste
ausreichende Menge** relevanter, aktueller, autoritativer und
datenschutzrechtlich erlaubter Informationen bereitzustellen.

**Der Anlass:** zu hoher Token- und Kontextverbrauch. Das Claude-Nutzungslimit
kann bereits nach wenigen umfangreichen Prompts erreicht sein. Das System soll
Limits **nicht umgehen**, sondern den vorhandenen Kontext wesentlich
effizienter nutzen.

Proxmox ist die erste Referenzplattform, aber nicht die Produktgrenze. Der
Referenzbetrieb ist eine dedizierte Linux-VM; Docker Compose ist eine darin
vorgesehene, **noch nicht implementierte** Anwendungslaufzeit.

## Aktueller Stand

| Feld | Wert |
| --- | --- |
| Phase | **Phase 0 COMPLETE** · Phase 1 AUTHORIZED FOR PLANNING |
| Aktuelles Work Package | **keines** — zuletzt abgeschlossen **CBP-WP-021** (`committed`, `complete`, 2026-08-03; **D-056**, `ADR_NOT_REQUIRED`; B0 `0cb4ea9`, B1/B2 `271acc7`); zuvor abgeschlossen **CBP-WP-020** (`committed`, `complete`; **D-055**; B0 `17057e2`, B1/B2 `9c6c0fb`, C `d6a1a3c`) |
| Nächster Schritt | **Wird durch den Human Maintainer und Nova separat bestimmt.** Das kanonische Security-Foundation-Testinventar ist reconciliiert: **32 Negativtests, 1 Positivtest, 33 Testfälle**; **0 von 32** und **0 von 1** ausgeführt. **Weiterhin keine Installation und keine Bereitstellung.** **Kein Folge-Work-Package autorisiert; CBP-WP-022 ist nicht registriert** |
| **Gate G0** | **PASSED WITH NOTES** — 2026-07-21, A0 |
| Phase-1-Planung | **Streams F1–F5 geplant**, [Foundation Plan](docs/roadmap/PHASE_1_FOUNDATION_PLAN.md) |
| **Repository-Struktur** | **entschieden** — [ADR-0007](docs/decisions/ADR-0007-repository-und-workspace-grenze.md); **Migration nicht autorisiert** |
| **Mappingkonvention** | **entschieden** — [ADR-0008](docs/decisions/ADR-0008-pilot-source-mapping-konvention.md); **0 Mappings, 0 angebundene Quellen** |
| **Sicherheitsgrundlage** | **spezifiziert** — [ADR-0009](docs/decisions/ADR-0009-technische-sicherheitsgrundlage.md); **12 Kontrollen `DOCUMENTED ONLY`, 0 Tests ausgeführt** |
| **Runtime Skeleton** | **lokal implementiert** — [FOUNDATION_RUNTIME_SKELETON.md](docs/runtime/FOUNDATION_RUNTIME_SKELETON.md); `run` fail-closed, **nicht produktionsbereit** |
| **Ingest-Quarantäne MVP** | **lokaler Prototyp** — [INGEST_QUARANTINE_MVP.md](docs/runtime/INGEST_QUARANTINE_MVP.md), [ADR-0010](docs/decisions/ADR-0010-ingest-quarantaene-mvp.md); synthetic-only, fail-closed, **keine Promotion**; **nicht produktiv** |
| **Source-Registry MVP** | **lokaler Prototyp** — [SOURCE_REGISTRY_MVP.md](docs/runtime/SOURCE_REGISTRY_MVP.md), [ADR-0011](docs/decisions/ADR-0011-deterministische-source-registry.md); synthetic-only, fail-closed, **deaktiviert**, `activate` verweigert; **nicht produktiv** |
| **Source-Mapping-Draft-Validator MVP** | **lokaler Prototyp** — [SOURCE_MAPPING_DRAFT_VALIDATOR.md](docs/runtime/SOURCE_MAPPING_DRAFT_VALIDATOR.md), [ADR-0012](docs/decisions/ADR-0012-source-mapping-draft-validator.md); synthetic-only, read-only, fail-closed, 31-Feld-Vertrag, externe read-only Registry-Bindung, `activation-check` verweigert; **nicht produktiv** |
| **Mapping-Activation-Gate-Evaluator MVP** | **lokaler Prototyp** — [MAPPING_ACTIVATION_GATE_EVALUATOR.md](docs/runtime/MAPPING_ACTIVATION_GATE_EVALUATOR.md) (CBP-WP-016, D-050); synthetic-only, read-only, nicht persistent, fail-closed; **20 Gate-Kriterien**, Ausgabestatus nur `NOT_EVALUATED`/`BLOCKED`, `activation-evaluate` endet immer `BLOCKED` (Exit 14); **nicht produktiv** |
| **Synthetic Evidence Contract 3.0 MVP** | **lokaler Prototyp** — [SYNTHETIC_EVIDENCE_CONTRACT.md](docs/runtime/SYNTHETIC_EVIDENCE_CONTRACT.md) (CBP-WP-018, ADR-0013, D-052/D-053, `committed` `5ee2e83`); Schema 3.0 mit eingebetteten Artefakten, `security-control-form` + `control_id`, Provenance-/Binding-Hashes, deterministische Invalid-/Stale-/Conflict-Erkennung, **negative-evidence-only**; Schema 1.0 **und 2.0** fail-closed; **451 → 558 Tests**, **nicht produktiv** |
| **Security Foundation Readiness Contract MVP** | **lokaler Prototyp** — [SECURITY_FOUNDATION_READINESS_CONTRACT.md](docs/runtime/SECURITY_FOUNDATION_READINESS_CONTRACT.md) (CBP-WP-018, ADR-0013, D-053, `committed` `5ee2e83`); statischer Vertrag 1.0, **12 Controls / 7 runtime-scoped / 11 Bindungen**, ausschließlich synthetische Formprüfung, rein negativ; **keine** Security-Evaluation, **kein** Enforcement, **keine** Readiness-Aussage; **nicht produktiv** |
| **Profile-A Deployment Bundle** | **Repository-Artefakt, `committed` `9c6c0fb`** — [PROFILE_A_DEPLOYMENT_BUNDLE.md](docs/runtime/PROFILE_A_DEPLOYMENT_BUNDLE.md) (CBP-WP-020, D-055); sieben Dateien unter `deployments/profile-a/`, zwei getrennte Service-Identitäten, fail-closed Compose- und Konfigurationsvorlagen, maschinenlesbare Mount-/Egress-/Secret-/Backup-/RT-2-Verträge, **deterministischer Offline-Validator** (Exit 0, byte-identisch), **166 Bundle-Validation-Tests**; Runbooks: [Installation](docs/operations/PROFILE_A_INSTALLATION_RUNBOOK.md), [Validierung](docs/operations/PROFILE_A_VALIDATION_RUNBOOK.md), [Rollback](docs/operations/PROFILE_A_ROLLBACK_RUNBOOK.md). **Nicht deployed, nicht operational, nicht production-ready** |
| Implementierte Capabilities | **keine (0 von 29)** — Capability 2/3/5/6/7 bleiben nicht vollständig `implemented` |
| Angenommene ADRs | **13** |
| Framework | Nova Development Framework v1.0.0 |

## Pilotumfang

Im Human Discovery Intake auf **Profilebene** entschieden; konkrete
Infrastrukturwerte bewusst nicht erhoben.

| Dimension | Festlegung |
| --- | --- |
| Betriebsprofil | Proxmox-VM mit dedizierter Linux-VM |
| Anwendungslaufzeit | Docker Compose bevorzugt innerhalb der VM |
| Nutzung | Einzelperson; Multi-User kein Pflichtumfang |
| Quellen im Pilot | Markdown, Git-Repositories, Chat-Handoffs, Obsidian-Vault als Markdown |
| Datenklassen im Pilot | `public`, `internal` |
| Zugriff | privates VPN oder privates Netz, keine öffentliche Freigabe |
| Im Pilot | Web-UI (erst nach funktionierendem Retrieval), mobile Nutzung |
| Vertagt | native Obsidian-Nutzung, Wiki, externe Connectoren, Knowledge Graph |

Belege in [HUMAN_DISCOVERY_INPUT.md](docs/discovery/HUMAN_DISCOVERY_INPUT.md).

## Kriterienmodell

G0 sperrt den allgemeinen Produkt- und Architektur-Scope, nicht die Details
einer späteren Installation.

| Klasse | Anzahl | Blockiert G0 |
| --- | --- | --- |
| **Core Required** | 25 | **ja** |
| Deployment Required | 16 | nein — [Deployment Readiness Check](docs/operations/DEPLOYMENT_READINESS_CHECK.md), **APPROVED BY HUMAN MAINTAINER** für Profil A (19 Prüfpunkte, alle `ready`) |
| Conditional | 6 | nur bei aktivierter Funktion |

## Prozessmodell

Verbindlich nach
[Nova Development Framework v1.0.0](https://github.com/KayKaspers/Nova-Development-Framework/releases/tag/v1.0.0).

```
Nova (ChatGPT)  →  Implementation Agent  →  Human Maintainer
   plant              führt genau ein          prüft, entscheidet,
   Work Packages      Work Package aus         committet und pusht
```

Lifecycle jedes Work Packages:

```
Classify → Plan → Execute → Report to Nova → Review → Commit
```

Nur der Human Maintainer committet, tagged und pusht.

## Repository-Struktur

| Pfad | Inhalt |
| --- | --- |
| `docs/architecture/` | Projektdefinition, Systemarchitektur, Komponentenmodell, Deploymentprofile, Prinzipien, Vertrauensgrenzen, Context Budgets |
| `docs/operations/` | Deployment Readiness Check, Pilot Mapping Activation Gate, Operational-Evidence-Policy, Security Foundation Readiness Gate |
| `docs/benchmark/` | Quellenvertrag, Evaluationsplan, Metriken, Baseline-Protokoll, Governance |
| `docs/sources/` | Pilot Source Contract, Source-Slot-Modell, Mapping-Spezifikation, -Schema, -Validierung, synthetische Beispiele |
| `docs/roadmap/` | Phase-1-Backlog, Foundation Plan, Stream-Pläne F1–F5, Work-Package-Karte, Nachweisplan, Abbruchbedingungen |
| `benchmarks/` | Synthetischer Korpus (24 Quellen), 36 Fragen, erwartete Ergebnisse |
| `docs/security/` | Berechtigungsmodell, Secret-Incident-Response, Sicherheitsspezifikation, Identitätsmodell, Secret-Vertrag, Egress-Policy, Abnahmematrix |
| `docs/decisions/` | Architecture Decision Records — **9 angenommen** |
| `docs/discovery/` | Fragebogen, G0-Kriterien, Quellenabgleich, A5-Projektübergabe |
| `docs/ndf/` | NDF-Anwendung und dokumentierte Abweichungen |
| `docs/privacy/` | Datenklassen und technische Datenschutzregeln |
| `docs/product/` | Verbindliche Sperrliste der aktuellen Phase |
| `project-brain/` | Kuratiertes Projektgedächtnis |
| `project-system/` | Profil, Manifest, Capability Matrix, Register, WP-Queue |
| `work-packages/` | Wortlaut der freigegebenen Work Packages |
| `core/` | **Skeleton** (CBP-WP-012) + **Ingest-Quarantäne-MVP** (CBP-WP-013) + **Source-Registry-MVP** (CBP-WP-014) + **Source-Mapping-Draft-Validator** (CBP-WP-015) + **Mapping-Activation-Gate-Evaluator** (CBP-WP-016) — lokal, fail-closed |
| `config/` | Synthetische Beispielkonfiguration und -policies |
| `examples/` | Synthetische Quarantäne- und Registry-Beispiele (test-only) |
| `tests/` | Lokale Unit- und Negativtests (Standardbibliothek) |
| `docs/runtime/` | Skeleton- und Quarantäne-Doku, technische Evidenz, Runbooks |

> **Dies ist die aktuelle, nicht die Zielstruktur.** Am 2026-07-21 wurde als
> Ziel ein **Monorepo** mit `core/`, `adapters/`, `deployments/`, `config/`,
> `docs/`, `examples/`, `tests/` beschlossen, dazu ein **privater
> Operator-Workspace außerhalb dieses Repositorys** und ein getrennter
> Runtime-Datenbereich — **OD-26 geschlossen**,
> [ADR-0007](docs/decisions/ADR-0007-repository-und-workspace-grenze.md).
>
> **Die Migration ist nicht autorisiert.** Das aktuelle Layout bleibt bestehen,
> bis ein separates, ausdrücklich freigegebenes Work Package vorliegt.
>
> **Das Repository ist `publication-capable by design`, aber nicht
> veröffentlicht.** Privater Bestand, produktive Mappings und Secrets sind
> konstruktiv ausgeschlossen — das ist eine Bauweise, keine Freigabe. Das
> Repository bleibt **privat**; Veröffentlichung, Lizenz und Produktname
> benötigen jeweils eine eigene Human-Maintainer-Entscheidung (OD-11, OD-23,
> OD-28).

## Einstiegspunkte

| Frage | Dokument |
| --- | --- |
| Worum geht es? | [PROJECT_DEFINITION.md](docs/architecture/PROJECT_DEFINITION.md) |
| Wo steht das Projekt? | [PROJECT_BRAIN.md](project-brain/PROJECT_BRAIN.md) |
| Was muss vor G0 geklärt werden? | [G0_SCOPE_LOCK_CRITERIA.md](docs/discovery/G0_SCOPE_LOCK_CRITERIA.md) |
| **Worüber wird bei G0 entschieden?** | **[G0_SCOPE_LOCK_REVIEW.md](docs/discovery/G0_SCOPE_LOCK_REVIEW.md)** |
| Welche Nachweise liegen vor? | [G0_EVIDENCE_MATRIX.md](docs/discovery/G0_EVIDENCE_MATRIX.md) |
| Welche Quellen sind zulässig? | [PILOT_SOURCE_CONTRACT.md](docs/sources/PILOT_SOURCE_CONTRACT.md) |
| **Wie wird eine Quelle angebunden?** | **[PILOT_SOURCE_MAPPING_SPECIFICATION.md](docs/sources/PILOT_SOURCE_MAPPING_SPECIFICATION.md)** |
| Wann darf ein Mapping wirksam werden? | [PILOT_MAPPING_ACTIVATION_GATE.md](docs/operations/PILOT_MAPPING_ACTIVATION_GATE.md) — **NOT EVALUATED** |
| Was hat der Maintainer entschieden? | [HUMAN_DISCOVERY_INPUT.md](docs/discovery/HUMAN_DISCOVERY_INPUT.md) |
| Welche Fragen sind offen? | [DISCOVERY_QUESTIONS.md](docs/discovery/DISCOVERY_QUESTIONS.md) |
| **Wie geht Phase 1 weiter?** | **[PHASE_1_FOUNDATION_PLAN.md](docs/roadmap/PHASE_1_FOUNDATION_PLAN.md)** |
| Welche Work Packages sind vorgeschlagen? | [PHASE_1_WORK_PACKAGE_MAP.md](docs/roadmap/PHASE_1_WORK_PACKAGE_MAP.md) |
| Was zählt als Nachweis? | [PHASE_1_EVIDENCE_PLAN.md](docs/roadmap/PHASE_1_EVIDENCE_PLAN.md) |
| Wann ist anzuhalten? | [PHASE_1_STOP_CONDITIONS.md](docs/roadmap/PHASE_1_STOP_CONDITIONS.md) |
| Wie ist das System aufgebaut? | [SYSTEM_ARCHITECTURE.md](docs/architecture/SYSTEM_ARCHITECTURE.md) |
| Wer darf was? | [PERMISSION_MODEL.md](docs/security/PERMISSION_MODEL.md) |
| **Was muss technisch durchgesetzt werden?** | **[TECHNICAL_SECURITY_FOUNDATION_SPECIFICATION.md](docs/security/TECHNICAL_SECURITY_FOUNDATION_SPECIFICATION.md)** |
| Woran erkennt man, dass es wirkt? | [SECURITY_CONTROL_ACCEPTANCE_MATRIX.md](docs/security/SECURITY_CONTROL_ACCEPTANCE_MATRIX.md) — **DOCUMENTED ONLY** |
| Woher stammen die Aussagen? | [SOURCE_RECONCILIATION.md](docs/discovery/SOURCE_RECONCILIATION.md) |
| Was darf nicht begonnen werden? | [DO_NOT_START.md](docs/product/DO_NOT_START.md) |

## Kernprinzipien

Kanonischer Markdown-Wissensbestand · Git-Historie für kuratierte Inhalte ·
reproduzierbare abgeleitete Daten · deterministischer Quellenindex · lokale
Hybrid-Suche · Brain-First-Retrieval · A0–A6-Autoritätsmodell · Datenklassen
und technische Datenschutzregeln · Context Budgets B0–B4 · reproduzierbare
Context Packs · erklärbarer Retrieval-Trace · menschlich kontrollierte
Konfliktauflösung · private Mehrgeräte-Nutzung · deployment-neutrale
Architektur · austauschbare Suche und Web-UI · Backup-, Restore- und
Rebuild-Fähigkeit.

Ausführlich in
[ARCHITECTURE_PRINCIPLES.md](docs/architecture/ARCHITECTURE_PRINCIPLES.md).

## Datenschutz in zwei Sätzen

Index und Suche laufen lokal — die Sprachverarbeitung nicht. Weil ausgewählte
Inhalte an das Claude-Modell übertragen werden, regeln fünf Datenklassen, was
übertragen werden darf; **Secrets** gelangen nie in Repository, Wissensbestand,
Index, Context Pack oder Modellkontext.

Siehe [DATA_CLASSIFICATION.md](docs/privacy/DATA_CLASSIFICATION.md).

## Leitprinzip

> Proxmox ist die erste Referenzplattform, nicht die Produktgrenze. Der
> Wissensbestand bleibt portabel, der Index bleibt reproduzierbar, Claude liest
> nur das Nötige und der Mensch entscheidet, was gilt.

## Lizenz

Noch nicht festgelegt. Bewusst offen bis zu einer Entscheidung des Human
Maintainers — OD-23 in
[DECISION_REGISTER.md](project-system/DECISION_REGISTER.md).
