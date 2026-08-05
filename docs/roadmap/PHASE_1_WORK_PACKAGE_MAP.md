# Phase 1 Work Package Map — CBP-WP-009 bis CBP-WP-014

| Feld | Wert |
| --- | --- |
| **Charakter** | **historisches Planungsartefakt** (Streamschnitt F1–F5, Stand 2026-07-21) |
| **Statusabgleich** | nachgeführt in **CBP-WP-019** (2026-07-29) |
| Stream-Grundlage | [PHASE_1_FOUNDATION_PLAN.md](PHASE_1_FOUNDATION_PLAN.md) (F1–F5) |
| Backlog-Grundlage | [PHASE_1_BACKLOG.md](PHASE_1_BACKLOG.md) (P1–P5) |
| Erfasst in | CBP-WP-008 |
| Autoritätsklasse | A3 |
| Stand | 2026-08-03 — CBP-WP-022 Phase B2B-P |

> **Diese Karte ist ein historisches Planungsartefakt.** Sie schnitt bewusst nur
> **F1 bis F5** (CBP-WP-009 bis CBP-WP-014). Die **ursprüngliche
> Stream-Planung wird nicht rückwirkend umgedeutet** — die Abhängigkeitsregeln
> A–E und die Streamzuordnung bleiben im Wortlaut erhalten. Nachgeführt wurden
> in CBP-WP-019 **ausschließlich die Statuswerte und Commit-Belege**, weil die
> Karte Pakete weiterhin als `proposed`/`in-review` führte, die längst
> `committed` sind.

**Der kanonische Work-Package-Status steht in
[WORK_PACKAGE_QUEUE.md](../../project-system/WORK_PACKAGE_QUEUE.md)** (A2), nicht
in dieser Karte. Ein Vorschlag wird erst durch eine ausdrückliche Freigabe des
Human Maintainers ausführbar — Regel 6 der Work Package Queue.

---

## Überblick

| ID | Titel | Typ | Stream | Status | Implementierung autorisiert |
| --- | --- | --- | --- | --- | --- |
| **CBP-WP-009** | Repository Boundary Decision | `docs-only`, interaktiv | F1 | **`committed`** | **nein** |
| **CBP-WP-010** | Pilot Source Mapping Specification | `docs-only`, interaktiv | F2 | **`committed`** | **nein** |
| **CBP-WP-011** | Technical Security Foundation Specification | `docs-only`, interaktiv | F3 | **`committed`** — `8a7c455` | **nein** |
| **CBP-WP-012** | Foundation Runtime Skeleton | implementation | F3 | **`committed`** — `1f55234` | **ausgeführt** |
| **CBP-WP-013** | Ingest Quarantine Minimum Viable Pipeline | implementation | F4 | **`committed`** — `4a35245` | **ausgeführt** |
| **CBP-WP-014** | Deterministic Source Registry and Catalog | implementation | F5 | **`committed`** — `d0c0531` | **ausgeführt** (A0 WITH NOTES) |
| **CBP-WP-015** | Deterministic Source Mapping Draft Validator | implementation | F5 | **`committed`** — `645ccb1` | **ausgeführt** |

### Nach dem Kartenschnitt ergänzte Work Packages

Diese Pakete lagen **außerhalb** des ursprünglichen F1–F5-Schnitts und sind hier
nur zur Statusvollständigkeit geführt:

| ID | Titel | Status |
| --- | --- | --- |
| **CBP-WP-016** | Deterministic Mapping Activation Gate Evaluator | **`committed`** — `04c427c` |
| **CBP-WP-017** | Synthetic Evidence Contract & Provenance Foundation | **`committed`** — `d3168c4` |
| **CBP-WP-018** | Security Foundation Readiness Contract & Synthetic Form-Validator | **`committed`** — `4dec921` (Governance), `5ee2e83` (Implementation) |
| **CBP-WP-019** | Deployment Readiness Intake and Profile-A Target Specification | **`committed`** — `3c437f2` |
| **CBP-WP-020** | Controlled Profile-A Deployment Foundation | **`committed`** — `17057e2` (B0), `9c6c0fb` (B1/B2), `d6a1a3c` (C) |
| **CBP-WP-021** | Canonical Security Test Inventory Reconciliation | **`committed`** — `0cb4ea9` (B0), `271acc7` (B1/B2), `0344774` (C) |
| **CBP-WP-022** | KB-04 Enforcement Stage 1 | **`in-review`** (Phase B2D-P) — B0…B2C.2 committed, **B2C-T-R `committed` `9cde9de`**; D-057…**D-062**, **ADR-0014 `accepted`/A1**, **Enforcement Contract `accepted contract`**; **read-only Validator- und Initialisierungsplanungspaket implementiert**; **vollständige 45er-Traceability** (Split **37/2/6**, Gesamtsuite **1202**); **B2D.0, B2D.1, B2D-E0 und B2D-E1 read-only complete** (je `PASS WITH NOTES`); **B2D-P `committed` `b409d25`**, **B2D-GOV `committed` `7e8328a`**, **B2D-AUTH `committed` `1222ec0`**; **B2D-ENV-GOV `committed` `0cd21f5`**; **B2D-PREP-PLAN, B2D-PREP-PLAN-N1 und B2D-E-N07-PREP read-only complete**, letzterer mit **`N07_IDENTITY_MAPPING_INSUFFICIENT`**; **B2D-E-N07-GOV `committed` `c4b0426`** (D-066, `PROFILE_A_RETRIEVAL_NOT_INSTANTIATED_N07_DEFERRED`, Variante C) und in **B2D-E-N07-GOV-PCR** post-commit reconciliiert; **`KB04-T-N07` zurückgestellt**; **B2D-E-N14-PREP** read-only complete mit **`N14_A0_DECISION_REQUIRED`**; **B2D-E-N14-GOV registriert D-067** (`N14_EPHEMERAL_LOCAL_OBSERVATION_BRIDGE_ALLOWED`, Variante B), **uncommitted** — **flüchtige lokale Observation Bridge klassifiziert**, **kein Testhelper, keine CLI, kein Adapterexport**, **N14 weiterhin nicht ausgeführt**; **kein Evidence-Artefakt**, Contract §10.3 offen; **reale Infrastruktur, B2D-H/E/V/G und B2B-Apply nicht autorisiert** |

**CBP-WP-020 ist `committed` und `complete`** (D-055): Phase B0 `17057e2`,
Phase B1/B2 `9c6c0fb`. Das **Profil-A-Bundle** liegt als Repository-Artefakt mit
**genau sieben Dateien** unter `deployments/profile-a/` vor und ist
**deterministisch offline validiert** (`PROFILE-A-BUNDLE VALID`, `issues=0`,
Exit 0), begleitet von drei Runbooks, einem Runtime-Vertrag und **166
Bundle-Validation-Tests** (Gesamtstand **724 Tests OK**, 0 übersprungen).
**Zielzustand Z1 erreicht, Scope S2 abgeschlossen, RT-2-Grenze P1 eingehalten.**

**Zulässige Statusaussage:** *repository artifact implemented* · *offline
validation implemented* · *offline validation passed*. **B3 (reale
Bereitstellung) ist ausgeschlossen** — es wurde nichts installiert, gestartet,
verbunden oder durchgesetzt.

**CBP-WP-021 ist `committed` und `complete`** (D-056), abgeschlossen am
**2026-08-03**: Phase B0 `0cb4ea9`, Phase B1/B2 `271acc7`. D-056 stellt das
kanonische Security-Foundation-Testinventar fest: **32 Negativtests**, **1
Positivtest**, **33 Testfälle**; **NT-25 bleibt nach Regel TT-5 frei**, **NT-32
und NT-33 sind gültig**, die Zahl **31** ist ein überholter, falsch
etikettierter Ableitungswert. **Ausgeführt sind 0 von 32 und 0 von 1.** Die
Reconciliation umfasste auch die **ausführbaren** Profil-A-Artefakte.
**Kein Work Package ist aktiv, kein Folge-Work-Package autorisiert.**

> **In CBP-WP-021 Phase B1 korrigiert.** Diese Karte führte zuvor „31
> Negativtests"; der Wert ist auf den kanonischen Stand **32** gebracht.

**CBP-WP-022 ist registriert** (D-057, `accepted`/A0, 2026-08-03) und steht auf
**`in-review`** in **Phase B2B-P – New-target Initialization Plan and Safety Guard**. Titel:
**KB-04 Enforcement Stage 1** — Stufe 1 der neunstufigen Durchsetzungsreihenfolge
(**OS-Dateirechte**). **Phase B0 ist `committed` (`e4caa14`), Phase B1A ist `committed`
(`1a7696d`), Phase B1B ist `committed` (`b86a35f`)**; **Phase B1C** ist abgeschlossen und
**uncommitted**.

**D-058** hatte **`ADR_REQUIRED`** festgestellt. **D-059** (`accepted`, **A0**) nimmt
daraufhin **ADR-0014** *KB-04 Stage 1 Filesystem Enforcement Architecture* an;
**ADR-0014 trägt nach Annahme Autoritätsklasse A1**. Gewählt ist **Host-authoritative Enforcement mit deklarativem Zielmodell und read-only Runtime-Validierung**:
das Repository hält ausschließlich das **abstrakte** Zielmodell, das Deployment setzt
Besitz und Rechte **vor** dem Start, die Runtime **prüft nur und scheitert
fail-closed**. Vierzehn Implementierungsparameter bleiben bewusst offen.

**D-060** (`accepted`, **A0**) nimmt den implementierungsfähigen Vertrag
[KB_04_STAGE_1_ENFORCEMENT_CONTRACT.md](../security/KB_04_STAGE_1_ENFORCEMENT_CONTRACT.md)
an — elf Pfadklassen, zehn Akteure, die Rechteprofile **PP-1** bis **PP-4**, der
Identitätsbindungsvertrag, vier read-only Validierungszeitpunkte, zehn Link- und
Pfadregeln, **24 Fehlerklassen** sowie zwei **reservierte, nicht implementierte**
Exitcodes. **`ADR_NOT_REQUIRED`** gilt nur, solange der Vertrag vollständig
innerhalb **ADR-0014** bleibt; die ausführende Reparatur bleibt an **RT-2**
gebunden und **gesperrt**.

**Phase B1C ist `committed` (`24de07e`), Phase B2A ist `committed`
(`929d10b`); Phase B2B-P** ist abgeschlossen und
**uncommitted**. B2A implementiert das interne, **read-only**
Enforcement-Paket `core/core_brain/enforcement/` — sechs Module, **21 additive
`KB04-*`-ReasonCodes**, **206 neue Tests**, Gesamtsuite **930 grün**.
**Keine CLI, keine Config-Datei, keine Deploymentänderung, kein neuer
Exitcode, keine Mutation.**

**B2B-P ist `committed` (`fff8227`).** **Phase B2C.0** wurde read-only
abgeschlossen und ergab **`DECISION REQUIRED`**; **Phase B2C.1** registriert
daraufhin **D-061** (`accepted`, **A0**,
`B2C_TRACEABILITY_AND_NT_PREPARATION_SELECTED`, `ADR_NOT_REQUIRED`) und ist
**`committed` (`38eb33f`)**. Gewählt ist **Variante T** — eine rein
synthetische Test-, Fixture- und Rückverfolgbarkeitsphase; **Variante E**
(Security-Control-Form- oder Gate-Evidence-Artefakt) ist **nicht autorisiert**.

**Der erste B2C-T-Lauf endete `BLOCKED` — vor jeder Dateiänderung, null
geänderte Dateien.** Der read-only Audit fand **zwei** als *synthetisch
abdeckbar* geführte Kennungen, die derzeit **nicht abgedeckt** sind.
**Phase B2C.2** registriert daraufhin **D-062** (`accepted`, **A0**,
`B2C_TRACEABILITY_COVERAGE_SPLIT_RECONCILED`, `ADR_NOT_REQUIRED`) und ist
**`committed` (`117647f`)**. Kanonische Aufteilung der **45** Kennungen:
**37 `SYNTHETIC_COVERED` · 2 `SYNTHETIC_COVERAGE_GAP` · 6 `B2D_REAL_ONLY`**.
Die zwei Lücken sind **`KB04-T-P10`** und **`KB04-T-N25`** — beide **Contract
§10.3 Schreibzeitvalidierung**, weder als Produktionslogik noch als
funktionaler Test vorhanden.

**Phase B2C-T-R ist abgeschlossen und uncommitted.** Sie setzt die
Traceability technisch um: drei neue Test- und Fixturedateien bilden **alle
45** Contractkennungen ab, belegen **37** Zuordnungen auf vorhandene
funktionale KB-04-Tests, dokumentieren die **zwei** Coverage Gaps
wahrheitsgemäß mit leerem `covered_by` und bereiten die **sechs**
real-only Fälle rein deklarativ vor. **152 neue Tests**, Gesamtsuite
**1202 grün, 0 übersprungen**. **Es entsteht kein Evidence-Artefakt**, keine
Gate-Eingabe und kein Produktionscode; **Contract §10.3 bleibt offen** und
verlangt für eine Umsetzung eine eigene Scopefreigabe.

**Phase B2D.0 ist read-only abgeschlossen** und ergab `PASS WITH NOTES` bei
**null Konflikten**: Contract §18 definiert B2D als *„lokale Identitätsbindung
· reale Profil-A-Instanz · reale Nachweise · OD-37 · Gate-Evidenz"*, und
**B2D hängt nicht von B2B-Apply ab**, weil ADR-0014 den Setup-Akteur
hostseitig und operatorgeführt außerhalb von Runtime und Repository verortet.

**Phase B2D-P ist `committed` (`b409d25`).** Sie legt
[KB_04_PROFILE_A_INTEGRATION_PLAN.md](../runtime/KB_04_PROFILE_A_INTEGRATION_PLAN.md)
vor — **plan-only**, zwanzig Kapitel, fünfstufiges Phasenmodell, verbindliches
**Snapshot-/Recovery-Gate**, dreizehnteilige Precondition-Checkliste, neun
Evidenzoptionen **ohne Auswahl** und sechs Risikokandidaten **ohne ID**.
**Es entsteht kein Evidence-Artefakt**, keine Gate-Eingabe, keine reale
Aktion.

**Phase B2D.1 ist read-only abgeschlossen** (`PASS WITH NOTES`) und
**Phase B2D-GOV `committed` (`7e8328a`)**: **D-063** (`accepted`,
**A0**, `B2D_EXECUTION_PREREQUISITES_ESTABLISHED`, `ADR_NOT_REQUIRED`)
kanonisiert die Ausführungsvoraussetzungen, registriert **R-35** und **R-36**
(beide **hoch**, **offen**), entscheidet die Harnessfrage mit
**`NO_HARNESS_REQUIRED`** und reconciliiert die Risk-Register-Aggregate auf
**hoch 20 · mittel 14 · niedrig 1 · Summe 35**. **D-063 autorisiert keinen
Lauf** — jeder spätere B2D-E-Lauf verlangt eine **einmalige, nicht
übertragbare** Freigabe. **Es entsteht kein Evidence-Artefakt und keine
Gate-Eingabe.**

**Phase B2D-E0 ist read-only abgeschlossen** (`PASS WITH NOTES`) und
**Phase B2D-AUTH `committed` (`1222ec0`)**: **D-064** (`accepted`,
**A0**, `B2D_E_RUN_AUTHORIZATION_ARTIFACT_FORM_SELECTED`,
`ADR_NOT_REQUIRED`) wählt **Variante A1** und legt ein **leeres versioniertes
Autorisierungstemplate** mit **20 Pre-run-Pflichtfeldern** `AUTH-01` bis
`AUTH-20` an (**10 repo-neutral · 4 lokal-only · 6 Definition mit lokalem
Wert**). **Ausgefüllte Kopien bleiben ausschließlich lokal**, eine Freigabe
ist **einmalig und nicht übertragbar**, und **Pre-run und Post-run bleiben
getrennt**. **Kein Evidence-Artefakt, keine Gate-Eingabe, keine
Ausführungsfreigabe.**

**Phase B2D-E1 ist read-only abgeschlossen** (`PASS WITH NOTES`) und
**Phase B2D-ENV-GOV abgeschlossen und uncommitted**: **D-065** (`accepted`,
**A0**, `B2D_REFERENCE_ENVIRONMENT_PREPARATION_MODEL_SELECTED`,
`ADR_NOT_REQUIRED`) wählt das Modell
**`DEDICATED_NON_PRODUCTION_PROFILE_A_VM_WITH_LOCAL_PER_TARGET_APPROVAL`** —
eine **dedizierte, nicht produktive Linux/POSIX-VM**, bestehend oder neu
zulässig, **Container nicht automatisch gleichwertig**, **keine konkrete
Instanz im Repository**. **Eine lokale Templatekopie darf erst nach dem
D-065-Commit entstehen**, weil `AUTH-03` an den Repository-HEAD bindet.
**Reale Vorbereitung und B2D-E bleiben nicht autorisiert.**

**Nächste mögliche Phasen: B2D-H, B2D-E, B2D-V, B2D-G und B2B-Apply —
sämtlich nicht begonnen und nicht autorisiert; reale Infrastruktur ist nicht
autorisiert.** **KB-04 bleibt `DOCUMENTED ONLY`; es gibt keine
Gate- und keine Control-Hochstufung.** **CBP-WP-023 ist nicht registriert und nicht
autorisiert.**

**Die ersten drei sind `docs-only`.** CBP-WP-012 bis CBP-WP-015 sind committed;
sie erzeugten lokale, synthetisch testbare, **deaktivierte** Prototypen —
**nicht produktiv**, keine angebundene Quelle, keine Aktivierung.

---

## CBP-WP-009 — Repository Boundary Decision

| Feld | Inhalt |
| --- | --- |
| **ID** | CBP-WP-009 |
| **Typ** | `docs-only`, **interaktiv** |
| **Ziel** | **OD-26 durch eine ausdrückliche Human-Entscheidung schließen** — Layoutoption und Bereichsmodell |
| **Voraussetzungen** | CBP-WP-008 committed |
| **Erlaubter Scope** | Entscheidungsfragebogen ausgeben; gegebene Entscheidung im Wortlaut aufzeichnen; ADR entwerfen; Register nachführen |
| **Verbotener Scope** | **Jede Reorganisation**; Datei oder Ordner verschieben; OD-26 ohne Human-Entscheidung schließen; OD-05, OD-06, OD-11 vorwegnehmen |
| **Nachweise** | Aufgezeichnete Entscheidung im Wortlaut; ADR mit Status; dokumentierte Bereichsgrenze |
| **Abbruchbedingungen** | Human Maintainer entscheidet nicht oder nur teilweise → anhalten, **nicht annehmen** (SB-12) |
| **Erwartete Risiken** | R-01, R-17 |
| **Review Gate** | Nova-Review, dann Human-Maintainer-Entscheidung |
| **Status** | **`committed`** — ausgeführt am 2026-07-21 |
| **Ergebnis** | **OD-26 geschlossen** — D-029 (Layout-Option B) und D-030 (Modell W-3), [ADR-0007](../decisions/ADR-0007-repository-und-workspace-grenze.md) `accepted` |
| **Implementierung autorisiert** | **nein** |

**Die Entscheidung geht der Verschiebung voraus.** Eine Reorganisation wäre ein
eigenes, späteres Paket — **und ist es geblieben**: D-029 hält ausdrücklich
fest, dass das aktuelle Layout bis zu einem separaten, freigegebenen
Migrations-Work-Package bestehen bleibt.

## CBP-WP-010 — Pilot Source Mapping Specification

| Feld | Inhalt |
| --- | --- |
| **ID** | CBP-WP-010 |
| **Typ** | `docs-only`, interaktiv |
| **Ziel** | Konkrete Mappings für PS-02, PS-03, PS-04 spezifizieren; **OD-05 und OD-06 vorbereiten** |
| **Voraussetzungen** | **CBP-WP-009 entschieden** — ohne Bereichsgrenze kein Mapping |
| **Erlaubter Scope** | Mappingspezifikation je Slot **nach Human-Eingabe**; Ausschlussregeln; Freigabeverfahren |
| **Verbotener Scope** | **Keine Aktivierung**; kein Ingest; keine realen Pfade oder privaten Repository-URLs im Core Repository; keine Secrets |
| **Nachweise** | Mapping validiert; Quelle erreichbar; Rechte minimal; Ausschlüsse wirksam; keine Secrets; Datenklasse bestätigt; AI-Transfer-Regel getestet |
| **Abbruchbedingungen** | Ein realer Pfad oder Secret soll ins Core Repository → **sofort anhalten** (SB-02, SB-01) |
| **Erwartete Risiken** | **R-01**, R-27, R-03 |
| **Review Gate** | Nova-Review; Freigabe der Quellenauswahl durch den Human Maintainer |
| **Status** | **`committed`** — ausgeführt am 2026-07-21 |
| **Ergebnis** | **D-031, D-032, D-033** (A0) · [ADR-0008](../decisions/ADR-0008-pilot-source-mapping-konvention.md) `accepted` · Spezifikation, Schema (31 Felder), Validierung (24 Regeln), Zustandsmodell (10 Zustände), 10 synthetische Beispiele, Aktivierungsgate (`NOT EVALUATED`) |
| **Implementierung autorisiert** | **nein** |

**Ausgefüllte Mappings gehören in den Operator Workspace**, nicht in dieses
Repository (ADR-0006). Jedes bleibt `enabled: false`.

**OD-05 und OD-06 blieben offen** — die Konvention steht, die konkreten Quellen
nicht. Das war beabsichtigt: Die Spezifikation ist unabhängig davon, welche
Quellen später angebunden werden.

## CBP-WP-011 — Technical Security Foundation Specification

| Feld | Inhalt |
| --- | --- |
| **ID** | CBP-WP-011 |
| **Typ** | `docs-only` |
| **Ziel** | Die zwölf Kontrollbereiche KB-01 bis KB-12 in prüfbare technische Kontrollen und **Abnahmetests** überführen |
| **Voraussetzungen** | CBP-WP-009; unabhängig von CBP-WP-010 |
| **Erlaubter Scope** | Kontrollspezifikation; Abnahmetestdefinition; Rollen- und Ressourcenzuordnung; Durchsetzungsreihenfolge |
| **Verbotener Scope** | **Noch keine Bereitstellung**; keine Installation; keine Portfestlegung; keine UID-Festlegung; keine Hostpfade |
| **Nachweise** | Je Kontrollbereich: Kontrolle, Nachweisform, **Negativtest**, Rollback — vollständig spezifiziert |
| **Abbruchbedingungen** | Eine Kontrolle ruht allein auf Promptregeln → als **nicht durchgesetzt** kennzeichnen (SB-03) |
| **Erwartete Risiken** | **R-25**, **R-27**, R-26 |
| **Review Gate** | Nova-Review; Abnahme der Testdefinition durch den Human Maintainer |
| **Status** | **`committed`** — ausgeführt am 2026-07-21, Commit `8a7c455` |
| **Ergebnis** | **D-034 bis D-037** (A0) · [ADR-0009](../decisions/ADR-0009-technische-sicherheitsgrundlage.md) `accepted` · Spezifikation (18 Abschnitte), Identitätsmodell, Secret-Vertrag, Egress-Policy, Evidence-Policy, Abnahmematrix (**32** Negativtests, 1 Positivtest, 33 Testfälle), Readiness Gate (24 Punkte, `NOT EVALUATED`). **OD-34 und OD-35 geschlossen** |
| **Implementierung autorisiert** | **nein** |

**Auflage 1 der G0-Entscheidung** beginnt hier — als Spezifikation, nicht als
Umsetzung. **Alle zwölf Kontrollen stehen auf `DOCUMENTED ONLY`.**

## CBP-WP-012 — Foundation Runtime Skeleton

| Feld | Inhalt |
| --- | --- |
| **ID** | CBP-WP-012 |
| **Typ** | **spätere Implementierung** |
| **Ziel** | Minimales, nicht privilegiertes Laufzeitgerüst mit durchgesetzten Kontrollen KB-01 bis KB-04 und KB-08 |
| **Voraussetzungen** | **CBP-WP-011 abgenommen**; ausdrückliche Freigabe des Human Maintainers |
| **Erlaubter Scope** | *Erst nach Autorisierung festzulegen* |
| **Verbotener Scope** | **Alles** — dieses Work Package ist **nicht autorisiert** |
| **Nachweise** | Rechte- und Identitätsauflistung; **bestandene Negativtests** zu KB-01 bis KB-04, KB-08 |
| **Abbruchbedingungen** | Root- oder Hostausführung; unerwarteter Schreibzugriff auf Canonical; Secretfund (SB-01, SB-04 der Stop-Bedingungen) |
| **Erwartete Risiken** | R-26, **R-25**, R-01 |
| **Review Gate** | Human-Maintainer-Freigabe **vor** Beginn, Nova-Review danach |
| **Status** | **`committed`** — ausgeführt am 2026-07-21, Commit `1f55234` |
| **Ergebnis** | Human-Autorisierung APPROVE WITH NOTES (A0); Stack A1, CLI B1, Struktur C1. Additiver Python-Skeleton, **9 Module**, lokale CLI, vier verweigernde Ports, **69 Tests bestanden**, `run` fail-closed (Exit 4). **Keine KB-Kontrolle durchgesetzt** — alle `DOCUMENTED ONLY` |
| **Implementierung autorisiert** | **ja, ausgeführt** — nur der lokale Skeleton, kein produktiver Betrieb |

**Erstes Work Package mit technischer Wirkung.** Bewusst als Gerüst
geschnitten: keine Suche, kein Retrieval, keine Oberfläche, keine angebundene
Quelle. **Die Umsetzung von KB-01…KB-12 auf der Ziel-VM steht aus** — der
Skeleton prüft lokal, er setzt nicht durch.

## CBP-WP-013 — Ingest Quarantine Minimum Viable Pipeline

| Feld | Inhalt |
| --- | --- |
| **ID** | CBP-WP-013 |
| **Typ** | **spätere Implementierung** |
| **Ziel** | Fail-closed-Pipeline mit zwölf Schritten und zehn Statuswerten, Markdown zuerst |
| **Voraussetzungen** | **CBP-WP-010 und CBP-WP-012**; ausdrückliche Freigabe |
| **Erlaubter Scope** | *Erst nach Autorisierung festzulegen* |
| **Verbotener Scope** | **Alles**; insbesondere produktiver Ingest, PDF-/Office-Parser, realistische Secrets |
| **Nachweise** | **Negativtests N-01 bis N-12 bestanden**; keine Quelle gelangt von `received` direkt nach indexiert |
| **Abbruchbedingungen** | Weg von Quarantäne nach kanonisch ohne Human Review; Secretfund; `excluded-from-ai` durchgebrochen |
| **Erwartete Risiken** | **R-32**, **R-31**, R-30, R-04, R-01 |
| **Review Gate** | Human-Maintainer-Freigabe vor Beginn; Abnahme der Negativtests danach |
| **Status** | **`committed`** — Commit `4a35245` |
| **Implementierung autorisiert** | **ja, ausgeführt** — lokaler synthetischer Quarantäne-Prototyp, kein produktiver Ingest |

**PDF und Office bleiben `deferred`.** Tests laufen mit **synthetischen** Daten.

## CBP-WP-014 — Deterministic Source Registry and Catalog

| Feld | Inhalt |
| --- | --- |
| **ID** | CBP-WP-014 |
| **Typ** | **spätere Implementierung** |
| **Ziel** | Registry mit stabilen IDs, Revisionen, Tombstones und reproduzierbarem INDEX |
| **Voraussetzungen** | **CBP-WP-013**; ausdrückliche Freigabe; OD-16 entschieden |
| **Erlaubter Scope** | *Erst nach Autorisierung festzulegen* |
| **Verbotener Scope** | **Alles**; insbesondere Suchintegration und Retrieval-Implementierung |
| **Nachweise** | **Zwei Läufe, gleicher Indexzustand**; **Tombstone überlebt Rebuild**; Derived Cleanup wirksam; Rebuild aus kanonisch + Registry |
| **Abbruchbedingungen** | Registry nicht reproduzierbar; Index enthält gelöschte Quelle; fehlender Rollback |
| **Erwartete Risiken** | **R-10**, R-07, R-06 |
| **Review Gate** | Human-Maintainer-Freigabe vor Beginn; Abnahme des Rebuild-Nachweises danach |
| **Status** | **`committed`** — Commit `d0c0531` |
| **Implementierung autorisiert** | **ja, ausgeführt** — lokaler, deaktivierter Registry-Prototyp, nicht produktiv |

---

## Abhängigkeiten als gerichtete Reihenfolge

```text
CBP-WP-009 ─┬─► CBP-WP-010 ─────────────┐
            │                           ├─► CBP-WP-013 ─► CBP-WP-014
            └─► CBP-WP-011 ─► CBP-WP-012┘
```

| Regel | Inhalt |
| --- | --- |
| **A** | **CBP-WP-009 geht allen voraus** — ohne Bereichsgrenze kein Mapping und keine Ablage |
| **B** | CBP-WP-010 und CBP-WP-011 sind **parallel** möglich |
| **C** | CBP-WP-012 setzt **CBP-WP-011** voraus — erst spezifizieren, dann bauen |
| **D** | CBP-WP-013 setzt **CBP-WP-010 und CBP-WP-012** voraus |
| **E** | CBP-WP-014 setzt **CBP-WP-013** voraus — nur `approved` wird indexiert |

**Der breiteste Enabler ist der F3-Strang** (CBP-WP-011 → CBP-WP-012). Er
sollte früh beginnen, weil CBP-WP-013 und CBP-WP-014 ohne ihn nicht
durchsetzbar sind.

## Was diese Karte nicht enthält

| Backlogpunkt | Grund |
| --- | --- |
| **P6** Retrieval-Pilot V1 | setzt P5 voraus |
| **P7** Benchmark V0/V1 | setzt P6 voraus |
| **P8** `excluded-from-ai`-Negativtests | setzt P3 **und** P6 voraus |
| **P9** Backup-/Restore-/Rebuild-Test | setzt P5 voraus |
| **P10** Deployment Readiness Profil A | setzt P3 und P9 voraus |
| **P11** Web-UI und Mobile | **erst nach gemessenem Retrieval** — ausdrückliche G0-Auflage |

Die Karte schneidet bewusst nur **F1 bis F5**. Sie weiterzuführen, bevor die
ersten Nachweise vorliegen, wäre Planung ohne Rückkopplung.

## Status

> **Historischer Stand nach CBP-WP-010 (unverändert erhalten):** CBP-WP-009 war
> committed, CBP-WP-010 ausgeführt; CBP-WP-011 bis CBP-WP-014 standen auf
> `proposed`. Dieser Absatz beschreibt den damaligen Planungszustand und wird
> **nicht rückwirkend umgedeutet**.

**Aktueller Stand (nachgeführt in CBP-WP-020 Phase C, 2026-07-29):** **Alle**
Work Packages dieser Karte — **CBP-WP-009 bis CBP-WP-015** — sind
**`committed`**. Ebenso committed sind die nach dem Kartenschnitt ergänzten
**CBP-WP-016**, **CBP-WP-017**, **CBP-WP-018**, **CBP-WP-019** (`3c437f2`) und
**CBP-WP-020** (`17057e2`, `9c6c0fb`). Die **Bundle-Artefakte existieren, sind
offline validiert und committed** — **aber es gibt weiterhin keine
Bereitstellung**. **Kein Work Package ist aktiv; kein Folge-Work-Package über
CBP-WP-020 hinaus ist autorisiert.**

**Regeln A und B sind erfüllt:** Die Bereichsgrenze steht (009), die
Mappingkonvention steht (010).

**Regel C und der F3-Strang:** Der F3-Strang (011 → 012) ist ausgeführt.
**Die damalige Feststellung bleibt sachlich gültig:** Das Aktivierungsgate ist
weiterhin **nicht durchlaufbar**, weil acht seiner zwanzig Punkte Nachweisstufe 4
verlangen — CBP-WP-012 hat einen lokalen Skeleton erstellt, der **prüft, aber
nicht durchsetzt**. **Keine der zwölf KB-Kontrollen ist durchgesetzt**; alle
bleiben `DOCUMENTED ONLY`.

**Aktueller Gatestand:** Mapping Activation Gate `NOT EVALUATED` · Security
Foundation Readiness Gate `NOT EVALUATED` · **DRC `APPROVED BY HUMAN MAINTAINER`**
(Profil A, 2026-07-29, **19 `ready` / 0 `blocked`**, CBP-WP-019/D-054) — **rein
dokumentarisch, keine Installations- oder Betriebsfreigabe**.
**Capabilities 0 von 29.**

**Produktive Implementierung autorisiert: nein.**

> **Ergänzung zu einem Migrations-Work-Package.** D-029 verlangt für die
> Überführung in die Zielstruktur ein **separates, ausdrücklich freigegebenes**
> Work Package mit nachvollziehbarer, schrittweiser, rücksetzbarer Planung ohne
> Verlust der Git-Historie. Ein solches Paket ist in dieser Karte **nicht**
> geschnitten und wäre von Nova zu spezifizieren.
