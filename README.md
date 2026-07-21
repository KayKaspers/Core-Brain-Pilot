# Core Brain Pilot

> **Phase 0 – Discovery und Scope Lock.**
> Dieses Repository enthält derzeit **ausschließlich Dokumentation**.
> Es existiert **keine** Implementierung, keine Laufzeit und keine Installation.

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
| Phase | Phase 0 – Discovery und Scope Lock |
| Aktuelles Work Package | CBP-WP-006 (`in-review`) |
| Nächstes Gate | **G0 – Discovery and Scope Lock** |
| **Gate-Status** | **NOT PASSED** — alle 25 Core-Kriterien `accepted`; **READY FOR HUMAN DECISION** |
| Implementierte Capabilities | **keine (0 von 29)** |
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
| Deployment Required | 16 | nein — [Deployment Readiness Check](docs/operations/DEPLOYMENT_READINESS_CHECK.md), **NOT EVALUATED** |
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
| `docs/operations/` | Deployment Readiness Check |
| `docs/benchmark/` | Quellenvertrag, Evaluationsplan, Metriken, Baseline-Protokoll, Governance |
| `docs/sources/` | Pilot Source Contract, Source-Slot-Modell |
| `benchmarks/` | Synthetischer Korpus (24 Quellen), 36 Fragen, erwartete Ergebnisse |
| `docs/security/` | Berechtigungsmodell, Secret-Incident-Response |
| `docs/decisions/` | Architecture Decision Records — **5 angenommen** |
| `docs/discovery/` | Fragebogen, G0-Kriterien, Quellenabgleich, A5-Projektübergabe |
| `docs/ndf/` | NDF-Anwendung und dokumentierte Abweichungen |
| `docs/privacy/` | Datenklassen und technische Datenschutzregeln |
| `docs/product/` | Verbindliche Sperrliste der aktuellen Phase |
| `project-brain/` | Kuratiertes Projektgedächtnis |
| `project-system/` | Profil, Manifest, Capability Matrix, Register, WP-Queue |
| `work-packages/` | Wortlaut der freigegebenen Work Packages |

> Die Struktur ist **nicht freigegeben** und vor G0 zu entscheiden — OD-26.

## Einstiegspunkte

| Frage | Dokument |
| --- | --- |
| Worum geht es? | [PROJECT_DEFINITION.md](docs/architecture/PROJECT_DEFINITION.md) |
| Wo steht das Projekt? | [PROJECT_BRAIN.md](project-brain/PROJECT_BRAIN.md) |
| Was muss vor G0 geklärt werden? | [G0_SCOPE_LOCK_CRITERIA.md](docs/discovery/G0_SCOPE_LOCK_CRITERIA.md) |
| **Worüber wird bei G0 entschieden?** | **[G0_SCOPE_LOCK_REVIEW.md](docs/discovery/G0_SCOPE_LOCK_REVIEW.md)** |
| Welche Nachweise liegen vor? | [G0_EVIDENCE_MATRIX.md](docs/discovery/G0_EVIDENCE_MATRIX.md) |
| Welche Quellen sind zulässig? | [PILOT_SOURCE_CONTRACT.md](docs/sources/PILOT_SOURCE_CONTRACT.md) |
| Was hat der Maintainer entschieden? | [HUMAN_DISCOVERY_INPUT.md](docs/discovery/HUMAN_DISCOVERY_INPUT.md) |
| Welche Fragen sind offen? | [DISCOVERY_QUESTIONS.md](docs/discovery/DISCOVERY_QUESTIONS.md) |
| Wie ist das System aufgebaut? | [SYSTEM_ARCHITECTURE.md](docs/architecture/SYSTEM_ARCHITECTURE.md) |
| Wer darf was? | [PERMISSION_MODEL.md](docs/security/PERMISSION_MODEL.md) |
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
