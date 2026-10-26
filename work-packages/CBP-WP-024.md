# CBP-WP-024 — Synthetic Brain-First Lexical Retrieval Slice (V1 Foundation)

| Feld | Wert |
| --- | --- |
| Titel | **Synthetic Brain-First Lexical Retrieval Slice (V1 Foundation)** |
| Typ | **Mehrphasiges Work Package** — Governance (B0, B1) und gegebenenfalls synthetische Implementierung und Nachweise (B2, B3); **derzeit ausschließlich Governance** |
| Priorität | **P1** |
| Prompt Mode | **Full** · Context Budget **B2 – Standard** (begründet höchstens **B3**) |
| Status | **`in-review`** (Gesamt-Work-Package) — Phase **B0** **`committed`** (`dd72c3f`, Human-Commit und -Push 2026-10-23); **B1, B2, B3 und C nicht autorisiert** |
| Aktuelle Phase | **B0 – Registration & Governance Preparation** |
| Registration Decision | **D-070** — `accepted`, **A0**, 2026-10-22 — Ergebnis **`CBP_WP_024_REGISTERED_B0_GOVERNANCE_ONLY`** |
| Human-Maintainer-Authority | **A0** vom **2026-10-22**: „GO CBP-WP-024 B0 – Registration & Governance Preparation Only“ |
| Review Authority | **Nova** |
| ADR-Gate | **Registrierung: `ADR_NOT_REQUIRED`** · spätere Phasen: **offen** — vor jeder B1-Freigabe zu prüfen; B0-Vorbewertung siehe *B0-G1* und *B0-G4* |
| ADR | **keiner** |
| Registrierungsdatum | **2026-10-22** |
| Planungsgrundlage | read-only Intake **CBP-WP-024-PRE** vom 2026-10-22 (`READY_WITH_NOTES`); **kein** registriertes Work Package, **keine** Authority |
| Commit | **B0 `committed`** — `dd72c3f` (Parent `61e2f3a`; Commit und Push am 2026-10-23 ausschließlich durch den Human Maintainer, D-003); B1 bis C nicht autorisiert; keine Selbstreferenz auf einen künftigen Commit |
| KB-04-Status | **`DOCUMENTED ONLY`** — unverändert |
| Capabilities | **0 von 29** — unverändert |
| Gates | Mapping Activation `NOT EVALUATED` · Security Foundation Readiness `NOT EVALUATED` |
| R-33 | **`42/24`** — Vorgang **42** (`B0-R1-F01`, Active A0 Counter Mirror Staleness), registriert in **B0-R2** durch Human-Maintainer-A0 vom 2026-10-22 (HD-8, **Z-1**) |
| Retrieval-Integration | **keine** — weder real noch synthetisch implementiert |

## Anlass

Nach der dokumentarischen Closure von CBP-WP-022 (2026-10-20) und CBP-WP-023
(2026-10-19) war **kein** Work Package `active` oder `in-review`. Der read-only
Intake **CBP-WP-024-PRE** hat den Bestand bewertet. Ergebnis: Das Repository
enthält fünf synthetische, fail-closed Bausteine (Registry, Quarantäne,
Mapping-Draft-Validator, Gate-Evaluator, KB-04-Validator), aber **keinen**
Index, **keine** Suche, **kein** Retrieval Policy Gateway, **keinen** Trace und
**kein** Context Pack. Damit fehlt jeder Nutzpfad. Der Intake hat als
kleinsten kontrolliert testbaren nächsten Schritt einen **synthetischen
V1-Slice** über den vorhandenen Benchmark-Korpus empfohlen. Der Weg dorthin
führt über vorgeschaltete Governance-Phasen, weil Sperrliste, offene
Entscheidungen und ein Reopen-Trigger aus D-066 berührt sind.

Der Human Maintainer hat am **2026-10-22** ausschließlich **B0** freigegeben.

## Phasenmodell

Die Phasen sind **Schritte innerhalb desselben Work Packages**. Aus einer
Phase folgt **keine** Freigabe der nächsten.

| Phase | Gegenstand | Autorisierung | Status |
| --- | --- | --- | --- |
| **B0** | Registrierung, Governance, Scope Lock, Entscheidungsvorbereitung | **autorisiert** — Human-Maintainer-A0 vom 2026-10-22 | ausgeführt, **`committed`** (`dd72c3f`) |
| **B1** | Architektur- und ADR-Entscheidung | **nicht autorisiert** | — |
| **B2** | Synthetische Retrieval-Implementierung | **nicht autorisiert** | — |
| **B3** | Tests und technische Nachweise | **nicht autorisiert** | — |
| **C** | Closure | **nicht autorisiert** | — |

Jede Phase ab B1 verlangt eine **eigene ausdrückliche Human-Maintainer-A0**.
Vor einer B1-Freigabe sind die **Entscheidungsvorlagen dieses Dokuments**
(*B0-G1* bis *B0-G5*) durch den Human Maintainer beziehungsweise Nova zu
entscheiden; ohne diese Entscheidungen gilt der jeweils genannte fail-closed-
oder STOP-Zustand.

## Autorisierter B0-Scope

1. Registrierung von CBP-WP-024 (Titel, Priorität **P1**, Phasenmodell).
2. Dokumentation der Registrierungsentscheidung **D-070** — ausschließlich im
   Registrierungsumfang.
3. Scope Lock und Abgrenzung (*Non-Goals und Non-Claims*).
4. Entscheidungsvorlagen *B0-G1* bis *B0-G5* — **vorbereitet, nicht entschieden**.
5. Klassifikation der sechs Driftkandidaten aus CBP-WP-024-PRE — **nur in
   diesem Dokument**, ohne Änderung der Fundstellen.
6. Minimal notwendige Aktualisierung aktiver Registrierungs- und
   Zählerspiegel.

**Allowlist (Obergrenze, elf Dateien):** dieses Work Package (neu),
`WORK_PACKAGE_QUEUE.md`, `DECISION_REGISTER.md`, `README.md`, `CLAUDE.md`,
`PROJECT_BRAIN.md`, `PROJECT_MANIFEST.md`, `PROJECT_PROFILE.md`,
`HEALTH_SCORE.md`, `PHASE_1_WORK_PACKAGE_MAP.md`, `COMPLIANCE_CHECK.md`.
**Nicht verändert** werden insbesondere `DO_NOT_START.md`, `RISK_REGISTER.md`,
`CAPABILITY_MATRIX.md`, sämtliche ADRs, `benchmarks/`, `docs/benchmark/`,
`core/`, `tests/`, `config/` und `deployments/`.

## Abhängigkeiten

- Human-Maintainer-A0 vom 2026-10-22 (B0 only)
- NDF v1.0.0 · **D-003** (Commit- und Push-Autorität) · Zählregel (R-33)
- **D-068** (Closure-Grenze und Rebinding von CBP-WP-022) — **unverändert**
- **D-066** (Rückstellung `KB04-T-N07`, fünf Reopen-Trigger) — **unverändert**
- [DO_NOT_START.md](../docs/product/DO_NOT_START.md) — **unverändert, in Kraft**
- **ADR-0001** (deployment-neutral), **ADR-0003** (kanonisch vs. abgeleitet),
  **ADR-0014**, **ADR-0015** (öffentliches Repository)
- [DATASET_GOVERNANCE.md](../docs/benchmark/DATASET_GOVERNANCE.md) (Dataset
  2.0.0, `in-review`, Holdout-Schutz)

## Non-Goals und Non-Claims

B0 autorisiert **nicht**:

| Ausgeschlossen |
| --- |
| technische Implementierung · Python-, Test-, Konfigurations- oder Deploymentdateien |
| Suchintegration · Proof of Concept für die Suche · Aufhebung oder Auslegung von **DO_NOT_START #4** |
| Annahme oder Anlage eines ADR (insbesondere kein neuer ADR in B0) |
| Entscheidung über OD-04, OD-15, OD-18 oder OD-19 · Schließung irgendeiner offenen Entscheidung |
| N07-Ausführung · Änderung an D-066 · Identitätsbindung · Runtime-Instanziierung · reale Testvorbereitung |
| B2B-Apply · B2D-H/E/V/G · reale N14-Ausführung · Contract-§10.3-Implementierung |
| neue Sicherheitskontrolle · Control-Uplift · Evidence-Producer · Gateauswertung |
| Benchmarkmessung · Holdout-Nutzung · Datasetänderung · Übergang auf `released` |
| neue Risiko-ID · R-33-Vorgang (einzige Ausnahme: Vorgang **42** durch gesonderte Human-Maintainer-A0 HD-8/Z-1 in B0-R2) · Bereinigung von D-1 bis D-10 oder der Driftkandidaten |
| Lizenz, Branding, Produktveröffentlichung, Transfer |
| Commit, Push, Tag oder Release durch einen Implementation Agent |

## D-070 — Entscheidungsblock

| Feld | Wert |
| --- | --- |
| ID | **D-070** |
| Titel | **REGISTER CBP-WP-024 — SYNTHETIC BRAIN-FIRST LEXICAL RETRIEVAL SLICE (V1 FOUNDATION), B0 ONLY** |
| Status | `accepted` |
| Autorität | **A0** — Human Maintainer |
| Datum | **2026-10-22** |
| Work Package | **CBP-WP-024** |
| Ergebnis | **`CBP_WP_024_REGISTERED_B0_GOVERNANCE_ONLY`** |
| ADR-Gate | **`ADR_NOT_REQUIRED`** — ausschließlich für die Registrierung |

| Teil | Inhalt |
| --- | --- |
| **A — Gegenstand** | CBP-WP-024 wird als Work Package registriert: Titel **„Synthetic Brain-First Lexical Retrieval Slice (V1 Foundation)“**, Priorität **P1**, Typ **mehrphasiges Work Package** mit Governance- und gegebenenfalls späteren Implementierungsabschnitten. |
| **B — Grundlage** | Ausdrückliche Human-Maintainer-A0 vom **2026-10-22** („GO CBP-WP-024 B0 – Registration & Governance Preparation Only“). Der read-only Intake CBP-WP-024-PRE ist Planungsgrundlage, **keine** Authority. |
| **C — Autorisierte Phase** | **Ausschließlich B0 – Registration & Governance Preparation.** |
| **D — B0-Scope** | Registrierung · Scope Lock · **Vorbereitung** (nicht Entscheidung) der Vorlagen zu DO_NOT_START #4, zum D-066-Reopen-Trigger (1), zu OD-04, OD-15, OD-18, OD-19 und ihren Abhängigkeiten (OD-07, OD-08, OD-16, OD-17), zur Architekturgrenze und zur Dataset-Governance · Driftklassifikation · minimal notwendige Statusspiegel. |
| **E — Spätere Phasen** | **B1** (Architektur/ADR), **B2** (synthetische Implementierung), **B3** (Tests und technische Nachweise) und **C** (Closure) sind **je gesondert freigabepflichtig** (Human-Maintainer-A0). |
| **F — Suchsperre** | **Keine Suchintegration.** DO_NOT_START **#4** wird **weder aufgehoben noch ausgelegt**. |
| **G — N07** | **Keine N07-Ausführung.** D-066 bleibt unverändert; `KB04-T-N07` bleibt zurückgestellt. |
| **H — ADR** | **Kein ADR.** `ADR_NOT_REQUIRED` gilt ausschließlich für diese Registrierung; die ADR-Frage späterer Phasen ist vor einer B1-Freigabe zu prüfen. |
| **I — Implementierung** | **Keine technische Implementierung** — kein Code, keine Tests, keine Konfiguration, kein Deployment. |
| **J — Reife** | **Keine neue Security- oder Capability-Reifeaussage.** KB-04 `DOCUMENTED ONLY`, beide Gates `NOT EVALUATED`, Capabilities **0 von 29**. |
| **K — Keine Vorwegnahme** | D-070 trifft **keine** fachliche Entscheidung zu B1 oder B2; alle offenen Entscheidungen bleiben offen. |
| **L — Lifecycle** | Nach Ausführung von B0 steht CBP-WP-024 auf **`in-review`**; `committed` erst nach Bestätigung durch einen tatsächlichen Human-Commit. Der Ruhezustand nach der Closure von CBP-WP-022 (begrenzte Auslegung von Queue-Regel 4) **endet mit dieser Registrierung**; **kein** weiteres Work Package wird registriert. |
| **M — Commit-Autorität** | Commit und Push verbleiben **ausschließlich beim Human Maintainer** (D-003) |

Dieser Block ist mit der Zeile **D-070** im
[Decision Register](../project-system/DECISION_REGISTER.md) **inhaltlich
identisch**.

## Governance-Baseline vor B0

Am Ausgangscommit `61e2f3a` ausgezählt, nicht fortgeschrieben:

| Gegenstand | Wert |
| --- | --- |
| CBP-WP-022 / CBP-WP-023 | `committed` · `complete` / `committed` · `complete` |
| Work Packages `active` / `in-review` | **0 / 0** (Ruhezustand) |
| Decisions / A0 / höchste ID | **69 / 65 / D-069** |
| ADRs | **15** `accepted`, **0** `proposed` |
| Risiken | **35** (Severity **20/14/1**) |
| R-33 | **`41/23`** |
| Capabilities | **0 von 29** |
| KB-04 / Gates | `DOCUMENTED ONLY` / beide `NOT EVALUATED` |
| Tests | **1202** zuletzt dokumentiert bestanden; 1202 Testmethoden statisch gezählt — **nicht neu ausgeführt** |
| Retrieval-Integration | keine |
| Dataset | **2.0.0**, Reviewstatus **`in-review`** |

Nach B0: Decisions / A0 **70 / 66**, höchste **D-070**; nach B0-R2 R-33
**`42/24`** (Vorgang 42); alle übrigen Werte **unverändert**.

## B0-G1 — Sperrliste: DO_NOT_START #4 „Suchintegration“

**Entscheidungsvorlage für den Human Maintainer. Nicht entschieden.**

**Befund.**

- [DO_NOT_START.md](../docs/product/DO_NOT_START.md) trägt die
  **Autoritätsklasse A0** und führt **#4 „Suchintegration“**.
- Der Abschnitt *Was das konkret ausschließt* nennt ausdrücklich „**ein Proof
  of Concept für die Suche**“ als „auch dann gesperrt, wenn es klein wirkt“.
- Die Aufhebung eines Punkts erfolgt **ausschließlich** durch A0, dokumentiert
  **als ADR**, nachgeführt in der Capability Matrix (Abschnitt *Aufhebung*).
- Der Titel lautet „Sperrliste Phase 0“, ihre Begründung ist der Scope Lock
  von Phase 0. Eine Aufhebung **für Phase 1** ist **nicht** beschlossen.
- `CLAUDE.md` führt die Liste weiterhin als verbindlich.

**Geltungsbereich (Einschätzung).** Ein synthetischer lexikalischer
Retrieval-Slice ist ein **Proof of Concept für die Suche** und fällt damit
unter #4 — auch ohne externen Suchdienst und ohne reale Daten.

**Verhältnis zu früheren Work Packages.** Spätere technische Work Packages
haben Prototypen in angrenzenden Bereichen unter **eigener A0 und eigenem ADR**
gebaut:

- Quarantäne: ADR-0010, D-038 bis D-041
- Compose-Vorlagen: ADR-0002/D-016, D-055

Sie taten das, **ohne** den Wortlaut der Liste zu ändern. Das ist ein gelebtes,
aber **nicht ausdrücklich geregeltes** Muster. Es ersetzt die Aufhebungsregel
nicht und kann sie für #4 nicht stillschweigend ersetzen (R-12).

| Variante | Inhalt | Bewertung |
| --- | --- | --- |
| **V-1** | **Eng begrenzte Teilaufhebung von #4** durch A0, dokumentiert als ADR: ausschließlich ein **synthetischer, prozessinterner, nicht produktiver** lexikalischer Retrieval-Slice über `benchmarks/corpus/`; ohne externen Suchdienst, ohne Netz, ohne Modellaufruf, ohne reale Daten, ohne Persistenz im Repository | **empfohlen** — erfüllt die Aufhebungsregel, hält den Rest der Sperre intakt |
| **V-2** | Allgemeine Feststellung, dass die „Sperrliste Phase 0“ in Phase 1 nicht mehr gilt | **nicht empfohlen** — zu breit (R-12, R-13), hebt 24 weitere Punkte auf |
| **V-3** | Auslegung, #4 sei nicht einschlägig, weil keine Suchmaschine integriert wird | **nicht empfohlen** — widerspricht dem ausdrücklichen „Proof of Concept für die Suche“ |
| **V-4** | #4 bleibt vollständig in Kraft | zulässig; Folge: **B2 und B3 entfallen**, CBP-WP-024 endet nach B0/B1 als reine Planungseinheit oder wird neu geschnitten |

**Voraussetzungen einer Teilaufhebung (V-1).**

- ausdrückliche Human-Maintainer-A0
- ein **ADR** (Anlage frühestens in B1, nur `proposed` bis zur Annahme), der die
  Teilaufhebung und die Architekturgrenze aus *B0-G4* trägt
- dokumentierte Abgrenzung im Wortlaut der Sperrliste (Änderung von
  `DO_NOT_START.md` frühestens in B1, nicht in B0)
- Nachführung in der Capability Matrix **ohne** Reifehochstufung

**Fortbestehen.** Alle **übrigen 24 Punkte** bleiben unverändert in Kraft,
ebenso die *bedingten Sperren* (Wiki, Graph, Web-UI erst nach einem bestandenen
Retrieval-Pilot-Gate, D-014). Ausdrücklich weiter gesperrt bleiben:

- Suchmaschinen und externe Suchdienste
- semantische Suche und Embeddings
- produktive Suche
- MCP und externe Connectoren

**Entscheidungspunkte.** (1) Variante V-1 bis V-4 · (2) bei V-1: Zeitpunkt der
ADR-Anlage (B1) und Umfang der Abgrenzung · (3) Bestätigung, dass B0 keine
Wirkung auf #4 hat.

**Fehlt die Entscheidung:** **STOP** für B1 und B2 — keine Implementierung,
keine ADR-Anlage, #4 bleibt vollständig in Kraft.

## B0-G2 — D-066 Reopen Assessment

**Prüfgegenstand.** D-066 Teil I nennt **fünf Reopen-Trigger**. Bei jedem
dürfte `KB04-T-N07` *erneut bewertet* werden:

1. Die **Retrieval-Phase ist offiziell autorisiert**.
2. Das **Retrieval Policy Gateway ist als reale Profile-A-Komponente
   autorisiert**.
3. Die **Profile-A-Runtime erhält eine ausdrücklich akzeptierte
   Retrieval-Instanziierung**.
4. Eine **spätere A0-Entscheidung legt eine actor-specific
   Identitätsbindung fest**.
5. Eine **Contract-Klarstellung verändert die N07-Akteurs- oder
   Dimensionsanforderungen**.

Ein Trigger **erlaubt** eine Neubewertung; er **verlangt** sie nicht und
ändert die Rückstellung **nicht** von selbst.

| Trigger | Wirkung der B0-Autorisierung | Wirkung einer späteren B2-Freigabe (synthetischer Slice) |
| --- | --- | --- |
| (1) Retrieval-Phase autorisiert | **keine** — B0 autorisiert ausschließlich Governance-Vorbereitung, keine Retrieval-Arbeit | **auslegungsbedürftig** (siehe unten) |
| (2) Gateway als reale Profile-A-Komponente | keine | keine — der Slice ist keine Profile-A-Komponente |
| (3) Runtime-Instanziierung | keine | keine — keine Runtime, kein Dienst |
| (4) actor-specific Identitätsbindung | keine | keine — keine Identität |
| (5) Contract-Klarstellung | keine | keine — der Enforcement Contract bleibt unverändert |

**Feststellungsvorschlag für B0 (`INFERRED`, zur Bestätigung):** Die
B0-Autorisierung erfüllt **keinen** der fünf Trigger.

**Auslegungsfrage zu Trigger (1) für eine spätere B2-Freigabe:**

| Variante | Lesart | Folge |
| --- | --- | --- |
| **R-A** | „Retrieval-Phase“ meint eine **Retrieval-Ausbaustufe von Profile A** (Runtime-Bezug, wie bei Trigger 2 und 3). Ein synthetischer Bibliotheks-Slice erfüllt (1) **nicht**. | N07 bleibt ohne Neubewertung zurückgestellt |
| **R-B** | Jede offizielle Autorisierung von Retrieval-Arbeit erfüllt (1) | N07 **darf** neu bewertet werden. Die Neubewertung fände weiterhin **keine** instanziierte Rolle und **keine** Identität vor und würde mit hoher Wahrscheinlichkeit zur unveränderten Rückstellung führen |

**Empfehlung:** **R-A**. Die Lesart ist ausdrücklich in der Entscheidung zur
B2-Freigabe festzuhalten. Unter beiden Lesarten folgt aus einer B2-Freigabe
**keine** N07-Aktivität, **keine** Identitätsbindung, **keine**
Runtime-Instanziierung und **keine** reale Testvorbereitung.

**Entscheidungspunkte.** (1) Bestätigung: B0 erfüllt keinen Trigger ·
(2) Lesart R-A oder R-B für eine spätere B2-Freigabe.

**Fehlt die Entscheidung:** **fail-closed**. Der Trigger gilt als **nicht**
erfüllt, eine Neubewertung von N07 findet **nicht** statt, und eine
B2-Freigabe ohne ausdrückliche Lesart ist **unvollständig (STOP)**.

## B0-G3 — Offene Entscheidungen

**Vorlagen, nicht Entscheidungen.** Alle genannten offenen Entscheidungen
bleiben im [Decision Register](../project-system/DECISION_REGISTER.md) **offen**.

### OD-04 — Minimal nützlicher Funktionsumfang des Piloten (P0, Adressat Nova)

| Punkt | Inhalt |
| --- | --- |
| 1 Entscheidungsbedarf | Seit Phase 0 offen (P0). Ohne Festlegung fehlt CBP-WP-024 ein Maßstab für „nützlich“ und damit für die Abnahmekriterien. |
| 2 Bindungen | G0-Kriterium **A-8**; **D-014** (Retrieval-Pilot-Gate vor UI); **D-025** (Scope-Schnitte); Phase-1-Backlog **P6** (V1, lexikalisch, Brain-First); [BENCHMARK_PLAN.md](../docs/benchmark/BENCHMARK_PLAN.md) V1; Architekturprinzipien §6, §10, §11 (A2); DO_NOT_START #4 (A0). |
| 3 Varianten | **(a)** Quellenauswahl-Slice: zu einer Anfrage die kleinste zulässige Quellenmenge innerhalb des Budgets plus Trace, **ohne** Antworterzeugung · **(b)** End-to-end-V1 mit Context Pack **und** Modellantwort · **(c)** V1 über einen realen kanonischen Bestand |
| 4 Sicherheit/Datenschutz | (a) keine Übertragung, nur synthetische Daten · (b) Übertragung an ein externes Modell (TB-4), Benchmarkprotokoll erforderlich · (c) reale Daten — setzt P3, P8, OD-05, OD-06, OD-07, OD-08 voraus |
| 5 Technische Auswirkungen | (a) Python-Standardbibliothek genügt · (b) Modellanbindung — außerhalb der heutigen Sperrgrenzen · (c) Registry-Aktivierung, Quarantäne-Promotion, reale Ablage |
| 6 Empfehlung | **(a)** als Zielumfang von CBP-WP-024 — ausdrücklich als **Teilantwort**; OD-04 bleibt für den Gesamtpiloten offen |
| 7 Entscheidungspunkte | Annahme von (a) als Zielumfang · OD-04 bleibt offen (empfohlen) oder wird teilweise präzisiert |
| 8 Ohne Entscheidung | **STOP** für B1/B2 — Abnahmekriterien nicht bestimmbar |

### OD-15 — Schnitt einer Wissenseinheit (P1, Adressat Nova)

| Punkt | Inhalt |
| --- | --- |
| 1 Entscheidungsbedarf | Index, Abschnittsreferenzen und Budget hängen davon ab, was eine Einheit ist. |
| 2 Bindungen | Suchleiter Schritte 7 und 8 (kleinste Quellenzahl, nur relevante Abschnitte); Context Layer: *Abschnittsreferenzen* (A2); Rebuild-Vertrag: versionierte Segmentierung; Budget **B0 = 1 Abschnitt**; Dataset-Governance: Chunking-Änderung verlangt Regression |
| 3 Varianten | **(a)** Datei = Einheit · **(b)** Markdown-Abschnitt als Einheit, Datei als **Quelle**; Metadaten werden aus dem Frontmatter der Datei geerbt · **(c)** feste Token-Chunks |
| 4 Sicherheit/Datenschutz | (b) und (c) dürfen die Dateiklassifikation nicht verlieren. Abschnittsweise abweichende Klassen sind **nicht** zulässig; fehlende Metadaten → verweigern |
| 5 Technische Auswirkungen | (a) einfach, aber gröber als B0 erlaubt · (b) deterministisch über Überschriften, passt zur Quellenzahlregel · (c) tokenizerabhängig, nicht stdlib-neutral |
| 6 Empfehlung | **(b)** vorläufig **nur für den Slice**; OD-15 bleibt für den realen Bestand offen |
| 7 Entscheidungspunkte | Einheit für den Slice · Erbregel für Metadaten · Versionierung der Segmentierungsregel |
| 8 Ohne Entscheidung | **STOP** für B2 — Indexformat nicht bestimmbar |

### OD-18 — Filterreihenfolge im Retrieval-Pfad (P1, Adressat Nova)

| Punkt | Inhalt |
| --- | --- |
| 1 Entscheidungsbedarf | System Architecture (Schicht 4) und TB-4 lassen die Reihenfolge ausdrücklich offen. |
| 2 Bindungen | Schicht 4: Datenklasse, Berechtigung, Autorität und Aktualität → bei Unklarheit **verweigern**; Verifikation → kennzeichnen; Budget → kürzen, nie überschreiten; Trace → immer. TB-4: `secret` und `excluded-from-ai` passieren **nie**. Rebuild-Verifikation: keine solche Quelle im Index |
| 3 Varianten | **(a)** sicherheitsorientierte Anfragereihenfolge: Datenklasse/AI-Transfer → Collection/Projekt → Autorität → Aktualität → Verifikation (kennzeichnen) → Budget · **(b)** relevanzorientiert: erst Matching, dann Filter · **(c)** **(a)** plus Ausschluss bereits beim Indexieren: `secret`, `excluded-from-ai` und unbekannte Klasse werden **nicht indexiert**, nur als Metadateneintrag ohne Inhalt geführt |
| 4 Sicherheit/Datenschutz | (b) bewertet gesperrte Inhalte und kann sie in Ranking oder Trace sichtbar machen — **unzulässig** · (c) minimiert die Angriffsfläche |
| 5 Technische Auswirkungen | (c) verlangt ein Manifest ausgeschlossener Quellen (IDs und Grund, ohne Inhalt), damit Abstention begründbar bleibt |
| 6 Empfehlung | **(c)** vorläufig für den Slice; OD-18 bleibt für den realen Pfad offen |
| 7 Entscheidungspunkte | Reihenfolge · Indexzeit-Ausschluss · Behandlung von `restricted` |
| 8 Ohne Entscheidung | **STOP** für B2; jede Default-Implementierung müsste ohnehin fail-closed (c) entsprechen |

### OD-19 — Umfang und Format des Retrieval-Trace (P1, Adressat Nova)

| Punkt | Inhalt |
| --- | --- |
| 1 Entscheidungsbedarf | Der Trace ist Pflicht (Architekturprinzip §11), sein Format ist offen. |
| 2 Bindungen | §11: betrachtete Quellen, angewandte Filter, verworfene Treffer und Grund; Context Layer: Manifest, Abschnittsreferenzen, Pack-Hash, Ablaufzeit, Ausschlussgründe; RT-Klassen (ADR-0007): ein persistierter Audit-Trace wäre **RT-2**, und RT-2 ist **nicht** implementiert |
| 3 Varianten | **(a)** minimaler strukturierter, deterministischer Trace (JSON) **ohne Inhalte**: Anfrage, Index-Hash, Budget, Kandidaten mit Abschnittsreferenz, Filterentscheidungen mit ReasonCode, Auswahl, Ausschlussliste (nur IDs), Pack-Hash · **(b)** ausführlicher Trace mit Textauszügen · **(c)** persistentes Audit-Log |
| 4 Sicherheit/Datenschutz | (b) kann gesperrte Inhalte in den Trace tragen — **unzulässig** · (c) berührt RT-2 — **gesperrt** |
| 5 Technische Auswirkungen | (a) nutzt den vorhandenen ReasonCode-Rahmen und Hashmuster; Trace flüchtig (RT-3) |
| 6 Empfehlung | **(a)**, versioniertes Schema, keine Persistenz; vorläufig für den Slice |
| 7 Entscheidungspunkte | Pflichtfelder · Ausschluss von Inhalten · Schema-Versionierung · keine Persistenz |
| 8 Ohne Entscheidung | **STOP** für B2 — Abnahmekriterium „vollständiger Trace“ nicht bestimmbar |

### Abhängigkeiten zu OD-07, OD-08, OD-16 und OD-17

| OD | Bezug | Wirkung auf den Slice | Wirkung auf realen Bestand |
| --- | --- | --- | --- |
| **OD-07** (P0) Vergabe A0–A6 | Autoritätsfilter | **kein Blocker** — Autorität ist im synthetischen Frontmatter deklariert; Fixture-Autorität ist **keine** reale Autorität | **Blocker** |
| **OD-08** (P0) Vergabe Datenklassen | Datenschutzfilter | **kein Blocker** — Klasse deklariert; unbekannt oder fehlend → verweigern | **Blocker** |
| **OD-16** Bildungsvorschrift der Source-ID | Quellenidentität | **kein Blocker** — Fixture-IDs genügen; eine Brücke zum Registry-Schema (D-042) ist **nicht** Scope | offen |
| **OD-17** Pflicht-Frontmatter | Metadatenvertrag | **kein Blocker** — es gelten die Mindestmetadaten des [Benchmark-Quellenvertrags](../docs/benchmark/BENCHMARK_SOURCE_CONTRACT.md); fehlendes Feld → verweigern | offen |

**Der Scope wird dadurch nicht erweitert.** Keine dieser Entscheidungen wird
durch CBP-WP-024 vorweggenommen.

## B0-G4 — Architekturgrenze des synthetischen Retrieval-Scopes

**Planung, keine Umsetzung.** Kleinster verantwortbarer Scope — nur nach
positiver Entscheidung zu *B0-G1* (V-1), *B0-G2* und *B0-G3*:

| Element | Grenze |
| --- | --- |
| Eingabe | ausschließlich `benchmarks/corpus/` (read-only), Dataset **2.0.0** |
| Deterministische Quellenauswahl | gleicher Korpus und gleiche Konfiguration ergeben denselben Index-Hash; stabile Sortierung |
| Lexikalisches Matching | Titel, Pfad, Überschriften, Abschnittstext; **keine** Embeddings, **keine** Suchmaschine, **kein** Netz |
| Autoritäts- und Aktualitätsfilter | aus dem Frontmatter (`authority_class`, `freshness_status`, `valid_from`/`valid_until`); A6 nur als abgeleitete Orientierung, nie vorrangig vor A0–A5 (ADR-0003, Suchleiter Schritt 4) |
| Datenklassenfilter | `excluded-from-ai`, `secret`, unbekannt → nie im Inhalt von Index, Trace oder Pack; `ai_transfer` beachtet |
| Fail-closed | fehlendes oder unbekanntes Pflichtfeld → Quelle verweigert, Grund im Trace |
| Quellenzahl | Normalfall 1, erweitert höchstens 3 (B0–B3); Tokenwerte nur weich (OD-02b offen) |
| Retrieval-Trace | Format nach OD-19-Vorlage (a) |
| Context-Pack-Identität | Manifest (Quellen, Revisionen, Abschnittsreferenzen) mit deterministischem Hash; **Packs nie im Repository** |
| Abgeleitete Daten | im Speicher oder außerhalb des Repositorys; nie autoritativ (ADR-0003) |

**Vorgeschlagene Zerlegung von B2** (jede Teilphase eigene A0):

| Teilphase | Inhalt |
| --- | --- |
| **B2A** | Deterministischer Korpus-Index: Frontmatter-Prüfung, Segmentierung nach OD-15, Ausschlussmanifest, Index-Hash |
| **B2B** | Lexikalisches Matching und Policy-Filter in der Reihenfolge nach OD-18, Quellenzahlregel |
| **B2C** | Trace und Context-Pack-Manifest mit Hash; additiver read-only CLI-Unterbefehl |

Komponententests gehören zur jeweiligen Teilphase. **B3** bündelt die
technischen Nachweise: doppelte Determinismusläufe, Negativfälle und —
nur nach Entscheidung zu *B0-G5* — die Quellenauswahl gegen das Orakel des
Development-Sets.

**ADR-Vorbewertung:** voraussichtlich **`ADR_REQUIRED`**. Gründe sind neue
Komponenten- und Formatgrenzen (Indexer, Retrieval Policy Gateway, Context
Pack Compiler, Trace) nach dem Muster ADR-0010 bis ADR-0013 und die
Aufhebungsregel der Sperrliste bei V-1. Die Feststellung erfolgt erst in B1.

## B0-G5 — Dataset-Governance

| Gegenstand | Befund |
| --- | --- |
| Version | **2.0.0** in Korpusindex, Fragen, Erwartungen und `benchmarks/README.md` |
| Reviewstatus | **`in-review`** ([DATASET_GOVERNANCE.md](../docs/benchmark/DATASET_GOVERNANCE.md), Kopf und Abschnitt *Reviewstatus*); **für Messungen erst nach Human-Maintainer-Freigabe verwendbar** |
| Interne Abweichung | Der Abschnitt *Status* derselben Datei nennt noch **„Dataset-Version 1.0.0“** — siehe *Driftklassifikation*, DK-7 |
| Development / Holdout | **24 / 12** (Verhältnis 2:1); Holdout nicht zur Kalibrierung, nicht zur Fehlersuche; versehentliche Nutzung → `burned` |
| A0-Fixture | genau **ein** synthetisches A0-Fixture mit `test_fixture: true` und `synthetic_authority: true`; A0 bis A6 vertreten. Fixture-Autorität ist **keine** reale Projektautorität und wird hier **nicht** zitiert |
| Orakel | `EXPECTED_RESULTS.md`: erwartete Quelle, zulässige Alternativen, unzulässige Quellen, Form, kritische Fehler je Frage |

| Variante | Nutzung in B2/B3 | Bewertung |
| --- | --- | --- |
| **DS-A** | Orakelabgleich gilt als **Messung** → setzt eine **Freigabe von 2.0.0** (`released`) durch den Human Maintainer voraus | sauber, verlangt eine zusätzliche Entscheidung |
| **DS-B** | Orakelabgleich ausschließlich am **Development-Set** als **Komponentenkonformitätsprüfung** (keine Metriken, keine Schwellen, kein V0/V1-Vergleich) während `in-review`, per ausdrücklicher A0 | möglich, Abgrenzung zur Messung muss dokumentiert sein |
| **DS-C** | Komponententests nur mit **eigenen synthetischen Testfixtures**; der Benchmark bleibt bis P7 unberührt | geringstes Risiko; der Orakelabgleich entfällt |

**Empfehlung:** **DS-C** für B2. **DS-B** für B3 nur nach ausdrücklicher
Human-Maintainer-A0. Der Holdout wird in jedem Fall technisch
ausgeschlossen. Es gibt **keine** Benchmarkmessung, **keinen** automatischen
Übergang auf `released` und **keine** Datasetänderung.

**Entscheidungspunkte.** Variante · gegebenenfalls Freigabe von 2.0.0 als
eigene Entscheidung · Behandlung eines versehentlich berührten Holdouts.

**Fehlt die Entscheidung:** **fail-closed** — es gilt DS-C, ein Orakelabgleich
unterbleibt.

## Driftklassifikation

Klassifikation der Kandidaten aus CBP-WP-024-PRE — **ausschließlich hier**. Die
Fundstellen bleiben **unverändert**. Für die Driftkandidaten wird **kein** R-33-Vorgang registriert; der
in B0-R2 registrierte Vorgang **42** betrifft ausschließlich `B0-R1-F01` und ist mit keinem
Driftkandidaten zusammengefasst.

| Nr. | Fundstelle | Aussage | Klassifikation |
| --- | --- | --- | --- |
| **DK-1** | `docs/architecture/SYSTEM_ARCHITECTURE.md:317` | „Nicht implementiert. Keine Komponente dieser Architektur existiert. Phase 0 erlaubt ausschließlich Dokumentation.“ | **historisch korrekt, aber unzureichend qualifiziert**. Das Dokument ist auf Phase 0 und den Stand 2026-07-20 datiert; die logische Zielarchitektur ist weiterhin nicht produktiv umgesetzt, synthetische Prototypen existieren inzwischen → **R-16-Kandidat**; **kein** R-33-Kandidat |
| **DK-2** | `docs/roadmap/PHASE_1_BACKLOG.md:230` | „Es wurde nichts gebaut, nichts installiert, nichts angebunden und nichts gemessen.“ | **historisch korrekt (Stand 2026-07-21), aber unzureichend qualifiziert**. **Veraltet ist nur die pauschale Aussage, nichts sei gebaut worden.** Die einzelnen Backlog-Vermerke „Implementierung erlaubt: nein“ **bleiben bindend**; die WP-spezifischen A0-Freigaben sind Ausnahmen, keine Aufhebung → **R-16-Kandidat** |
| **DK-3** | `docs/operations/SECURITY_FOUNDATION_READINESS_GATE.md:36` | Abgrenzungstabelle: DRC `NOT EVALUATED` | **aktiver Statusspiegel veraltet**. Der DRC ist seit 2026-07-29 **APPROVED BY HUMAN MAINTAINER** (D-054, rein dokumentarisch). Gleiche Fehlerursache wie R-33-Vorgang **39** (DRC-Genehmigung nicht nachgeführt), der nur `COMPLIANCE_CHECK.md` erfasste → **R-33-Kandidat**. Nach der Regel „mehrere Fundstellen derselben Fehlerursache zählen als genau ein Vorgang“ wäre eine **zählneutrale Erweiterung von Vorgang 39** naheliegend — **Entscheidung des Human Maintainers erforderlich** |
| **DK-4** | `project-system/CAPABILITY_MATRIX.md:226` | „Dataset 1.0.0“ bei Capability 22 | **aktiver Statusspiegel veraltet** (Version statt Kennzahl). Gültig ist 2.0.0 seit dem Korrekturlauf zu CBP-WP-005 → **R-16-Kandidat**, Umfeld **D-7**; **kein** R-33-Kandidat (keine Kennzahl) |
| **DK-5** | `project-brain/PROJECT_BRAIN.md:412–511` | Abschnitt *Nächste Arbeitspakete* | **historisch korrekt** — der Abschnitt endet **nicht** bei CBP-WP-019, sondern reicht bis CBP-WP-021 und verweist auf die Registrierung von CBP-WP-022. Die Absätze „(dieser Stand, uncommitted)“ sind nach der Präzedenz der Human-Maintainer-A0 vom 2026-10-16 **phasendatierte Momentaufnahmen**. Unvollständig ist nur die Fortschreibung (WP-022-Closure, WP-023, WP-024) → **D-10-Klasse**, **R-16-Kandidat**; **kein** R-33-Kandidat |
| **DK-6** | `project-system/HEALTH_SCORE.md:147` | „… beginnt frühestens mit CBP-WP-012.“ | **historisch korrekt** — die Umsetzung begann mit CBP-WP-012 —, **aber unzureichend qualifiziert** im Abschnitt *Bewertung in einem Satz* → **R-16-Kandidat**, Umfeld **D-5**; **kein** R-33-Kandidat |
| **DK-7** | `docs/benchmark/DATASET_GOVERNANCE.md:250` (in B0 neu gefunden) | Abschnitt *Status*: „Dataset-Version 1.0.0, Reviewstatus `in-review`.“ | **aktiver Statusspiegel veraltet**, innerhalb derselben Datei widersprüchlich zum Kopf (2.0.0) → **R-16-Kandidat**; **nicht bestätigt**, ob ein R-33-Bezug besteht |

**Keine dieser Fundstellen ist ein aktueller Registrierungsstatusspiegel von
CBP-WP-024.** Daher bleibt jede unverändert. Eine Bereinigung verlangt eine
eigene Human-Maintainer-A0 — entweder zusammen mit D-1 bis D-10 oder als eigenes
Dokumentations-Work-Package.

## Offene Human-Maintainer-Entscheidungen

| Nr. | Entscheidung | Vorlage | Ohne Entscheidung |
| --- | --- | --- | --- |
| HD-1 | DO_NOT_START #4: Variante V-1 bis V-4 | *B0-G1* | STOP für B1/B2 |
| HD-2 | D-066 Trigger (1): Bestätigung „B0 erfüllt keinen Trigger“; Lesart R-A oder R-B für B2 | *B0-G2* | fail-closed; B2-Freigabe ohne Lesart unvollständig |
| HD-3 | OD-04 Teilantwort (a) | *B0-G3* | STOP für B1/B2 |
| HD-4 | OD-15, OD-18, OD-19 vorläufig für den Slice | *B0-G3* | STOP für B2 |
| HD-5 | Dataset-Nutzung DS-A, DS-B oder DS-C | *B0-G5* | fail-closed (DS-C) |
| HD-6 | Umgang mit DK-1 bis DK-7, insbesondere DK-3 (zählneutrale Erweiterung von Vorgang 39?) | *Driftklassifikation* | unverändert, keine Zählwirkung |
| HD-7 | Freigabe von B1 | *Phasenmodell* | B1 nicht autorisiert |
| HD-8 | Klassifikation von `B0-R1-F01` | *Stand B0-R1 und B0-R2* | **entschieden** — Human-Maintainer-A0 vom 2026-10-22: **Z-1**, R-33-Vorgang 42, `42/24` |

## Stand B0

B0 wurde am **2026-10-22** im uncommitteten Review-Diff ausgeführt:

- Registrierung und **D-070**
- Scope Lock
- Entscheidungsvorlagen *B0-G1* bis *B0-G5*
- Driftklassifikation
- minimal notwendige Statusspiegel

Es gibt keine technische Datei, keinen ADR, keine Änderung an der Sperrliste,
am Dataset, am Risk Register oder an der Capability Matrix. Zähler nach B0:
Decisions/A0 **70/66**, ADRs **15** angenommen und **0** vorgeschlagen, Risiken
**35** (**20/14/1**), R-33 **`41/23`** (*Stand vor B0-R2; durch Vorgang 42 auf `42/24`
fortgeschrieben, siehe unten*).

## Stand B0-R1 und B0-R2

**B0-R1 (Nova-REWORK, 2026-10-22).** Die unabhängige Nova-Prüfung des
B0-Reviewarchivs fand den Befund **`B0-R1-F01`**: In `HEALTH_SCORE.md`, Tabelle
*Kennzahlen*, war die Zeile *davon A0* nach der Registrierung von D-070 nicht von
**65** auf **66** fortgeschrieben, während die Nachbarzeile bereits **70**
Decisions auswies. Korrigiert durch genau eine Zeichenfolge (ein Byte); ein
anschließender wertbasierter Scan aller A0- und Decision-Zähler ergab keinen
weiteren Befund.

**B0-R2 (R-33-Reconciliation, 2026-10-22).** Durch Human-Maintainer-A0 vom 2026-10-22 (HD-8, Klassifikation **Z-1**) ist
`B0-R1-F01` als **R-33-Vorgang 42** registriert — **Active A0 Counter Mirror Staleness** (`B0-R1-F01`), zugeordnet
**CBP-WP-024** (erstes R-33-Erfassen): **`41/23 → 42/24`**. Identisch in
[RISK_REGISTER.md](../project-system/RISK_REGISTER.md) und
[COMPLIANCE_CHECK.md](../project-system/COMPLIANCE_CHECK.md), **genau einmal
gezählt**. **Kein** Bestandteil von Vorgang 39, **keine** zählneutrale
Erweiterung, **keine** Zusammenfassung mit DK-3 oder einem anderen
Driftkandidaten. HD-8 ist eine Klassifikationsentscheidung **ohne** neue
Decision-ID.

Zähler nach B0-R2: Decisions/A0 **70/66**, höchste **D-070**, ADRs **15**
angenommen und **0** vorgeschlagen, Risiken **35** (**20/14/1**), R-33
**`42/24`** (`gemindert, nicht geschlossen`). **B1, B2, B3 und C bleiben nicht
autorisiert.**

## Stand B0 committed – 2026-10-23

Phase **B0** ist **`committed`**: Commit
`dd72c3f92563082d628de93cab6ee6820ff82357` (Parent
`61e2f3a0d5d86a629b62ce4563fe7ca7c25fb153`, *docs(cbp): register WP-024 B0 and
reconcile R-33 event 42*). Commit und Push hat am **2026-10-23** ausschließlich
der Human Maintainer ausgeführt (D-003).

- Nova hat **B0-C3** und **B0-C4** abgenommen; die Remote-Baseline `dd72c3f`
  ist nach Human-Commit und Human-Push unabhängig bestätigt.
- **B0-C5** — read-only Post-Commit Reconciliation Intake
  (`READ_ONLY_COMPLETE_WITH_NOTES`), von Nova geprüft.
- Human-Maintainer-A0 vom 2026-10-23: **L-1** bestätigt — Phase B0
  `committed`, Gesamt-Work-Package `in-review`, **keine** separate
  B0-Closure-Decision — sowie **R-1 Option N** (kein zusätzlicher
  R-33-Vorgang).
- **B0-C6** — minimale Post-Commit-Status-Reconciliation der aktiven
  Statusspiegel; liegt als uncommitteter Review-Diff vor. Nova-Review, Commit
  und Push stehen aus.

Das Gesamt-Work-Package bleibt **`in-review`**; **B1, B2, B3 und C** bleiben
**nicht autorisiert**; **kein** Work Package ist `active`. Der
Post-Commit-Nachlauf der Statusspiegel — ein Commit kann seinen eigenen Hash
nicht vorwegnehmen — begründet **keinen** R-33-Vorgang: R-33 bleibt
**`42/24`**. Zähler unverändert: Decisions/A0 **70/66**, höchste **D-070**,
ADRs **15** angenommen und **0** vorgeschlagen, Risiken **35**. Die
historischen Abschnitte *Stand B0* und *Stand B0-R1 und B0-R2* sowie D-070
bleiben unverändert.

## Aussageschutz

| Behauptung | Zutreffend? |
| --- | --- |
| Die Registrierung sei eine Implementierungsfreigabe | **nein** — ausschließlich B0 |
| DO_NOT_START #4 sei aufgehoben oder ausgelegt | **nein** — unverändert in Kraft |
| D-070 entscheide OD-04, OD-15, OD-18 oder OD-19 | **nein** — alle offen; nur Vorlagen |
| B0 löse einen D-066-Reopen-Trigger aus | **nein** — Feststellungsvorschlag: kein Trigger erfüllt; Bestätigung durch den Human Maintainer offen |
| Es existiere ein ADR für CBP-WP-024 | **nein** |
| Ein Retrieval-Pfad, Index oder Suchdienst existiere | **nein** |
| Der Benchmark sei gemessen oder Dataset 2.0.0 freigegeben | **nein** — `in-review`, keine Messung |
| Eine Capability sei hochgestuft, eine Control wirksam oder ein Gate ausgewertet | **nein** — 0 von 29, `DOCUMENTED ONLY`, `NOT EVALUATED` |
| Die Driftklassifikation registriere einen R-33-Vorgang | **nein** — die Driftkandidaten bleiben ohne Zählwirkung; der einzige neue Vorgang **42** betrifft `B0-R1-F01` (`42/24`) |
| Vorgang 42 sei mit DK-3 oder Vorgang 39 zusammengefasst | **nein** — getrennt; DK-3 ohne Zählwirkung, Vorgang 39 unverändert |
| CBP-WP-024 sei insgesamt `committed` oder `complete` | **nein** — Gesamt-Work-Package `in-review`; B1, B2, B3 und C nicht autorisiert |
| Phase B0 sei `committed` | **ja** — `dd72c3f`, Human-Commit und -Push 2026-10-23 |

**Die Registrierung eines Work Packages ist keine Implementierungsfreigabe.**
