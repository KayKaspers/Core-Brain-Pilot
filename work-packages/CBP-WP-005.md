# CBP-WP-005 — Benchmark Dataset and Retrieval Evaluation Design

| Feld | Wert |
| --- | --- |
| ID | CBP-WP-005 |
| Titel | Benchmark Dataset and Retrieval Evaluation Design |
| Typ | `docs-only` |
| Prompt Mode | **Full** (NDF v1.0.0) |
| Context Budget | **B2 – Standard** (Core Brain Pilot) |
| Phase | Phase 0 – Discovery und Scope Lock |
| Ausgeführt am | 2026-07-20 bis 2026-07-21 |
| Ausführungen | Erstausführung + **Korrekturlauf nach Nova-REWORK** |
| Status | `in-review` |
| Dataset-Version | **2.0.0** |
| Autoritätsklasse | A2 |

---

## Ziel

Einen reproduzierbaren, deployment-neutralen Benchmark-Korpus und einen
vollständigen Evaluationsplan für den späteren Retrieval-Pilot erzeugen.

Adressiert die G0-Kriterien **G-1 bis G-6**: mindestens 30 Benchmarkfragen,
definierte Kategorien, Erfolgsmetriken, Baseline, Datenschutzfälle und
Konfliktfälle.

**Keine Suchmaschine installieren oder implementieren.** Der Benchmark
funktioniert unabhängig davon, ob später qmd, SQLite FTS, ein eigener
Hybridstack oder ein anderer Provider verwendet wird.

## Scope

- Benchmark-Quellenvertrag mit Pflichtmetadaten
- Synthetischer Markdown-Korpus, 15 bis 24 Quellen
- Genau 36 Benchmarkfragen in 6 Kategorien, 24 Development / 12 Holdout
- Erwartete Ergebnisse je Frage
- Evaluationsplan mit V0, V1, V2
- Metriken, Schwellen, kritische Fehler
- Baseline-Protokoll
- Dataset Governance
- G0-Nachführung für G-1 bis G-6
- Statusnachführung in den Registern

## Out of Scope

- G0 als bestanden erklären
- D-1 eigenständig auf `accepted` setzen
- Suchsoftware auswählen oder installieren
- Retrieval, Index, Embeddings, Messsoftware implementieren
- Einen Lauf durchführen
- Produktiver Wissensbestand, reale oder personenbezogene Daten
- DRC ausführen
- Commit, Push, Branch, Remote-Änderung

## Inputs

NDF v1.0.0 · Repository-Stand auf `main` (Commit `4cddc28`) ·
`SYSTEM_ARCHITECTURE.md` · `COMPONENT_MODEL.md` · `CONTEXT_BUDGETS.md` ·
`DEPLOYMENT_PROFILES.md` · `PERMISSION_MODEL.md` · `DATA_CLASSIFICATION.md` ·
`G0_SCOPE_LOCK_CRITERIA.md` · `HUMAN_DISCOVERY_INPUT.md` ·
`SOURCE_RECONCILIATION.md` · `DO_NOT_START.md` · `CAPABILITY_MATRIX.md` ·
`DECISION_REGISTER.md` · `RISK_REGISTER.md` · `WORK_PACKAGE_QUEUE.md` ·
`PROJECT_MANIFEST.md` · `PROJECT_BRAIN.md` · `CBP-WP-004.md`

Keine externe Recherche.

## Erlaubte Dateien

**Erstellen:** `docs/benchmark/` (5 Dokumente) · `benchmarks/README.md` ·
`benchmarks/corpus/INDEX.md` · 15–24 synthetische Quelldateien ·
`benchmarks/questions/BENCHMARK_QUESTIONS.md` ·
`benchmarks/expected/EXPECTED_RESULTS.md` · `work-packages/CBP-WP-005.md`

**Ändern:** `README.md` · `G0_SCOPE_LOCK_CRITERIA.md` · `OPEN_INFORMATION.md` ·
`PROJECT_BRAIN.md` · die Dokumente unter `project-system/`

## Verbotene Dateien

Dateien außerhalb des Projektordners · produktiver Wissensbestand · reale
private oder personenbezogene Daten · echte oder realistische Secrets ·
Anwendungscode · Dockerfile · `compose.yaml` · Skripte · CI/CD · GitHub
Actions · Datenbank · Suchindex · Embeddings · Modelle ·
Search-Provider-Installation · qmd-Installation · Retrieval-Implementierung ·
produktiver Ingest · Wiki-Ingest · Knowledge Graph · MCP-Implementierung ·
Web-UI-Implementierung · Infrastrukturänderung · DRC-Ausführung · `LICENSE` ·
Branch-Erstellung · Remote-Änderung · Commit · Push · GitHub-Issue · Release ·
Repository-Reorganisation

## Aufgaben

1. Benchmark-Quellenvertrag
2. Synthetischer Benchmark-Korpus
3. 36 Benchmarkfragen
4. Erwartete Ergebnisse
5. Evaluationsplan V0/V1/V2
6. Metriken und Schwellen
7. Baseline-Protokoll
8. Dataset Governance
9. G0-Nachführung
10. Status und Register

## Prüfungen

34 Prüfungen. Schwerpunkte: Korpusgröße im Rahmen · alle Quellen als Fixtures
gekennzeichnet · Pflichtmetadaten vollständig · keine realen Personen,
Organisationen oder Secrets · A1 bis A6 belegt · mindestens 4 Konfliktpaare,
4 veraltete Quellen, 4 Datenschutzfälle, 2 `excluded-from-ai`-Fixtures und
3 Negativfälle · genau 36 Fragen in 6 Kategorien zu je 6 · genau 24/12 ·
kein Fall über drei Quellen · kritische Fehler definiert · V0/V1/V2
provider-neutral · Datenschutzverletzungen mit Zielwert 0 · D-1 bleibt
`answered` · G0 bleibt NOT PASSED · DRC bleibt NOT EVALUATED · keine
Capability `implemented` · keine Suchsoftware gewählt · keine ausführbaren
Dateien · kein Commit, kein Push.

## Akzeptanzkriterien

Reproduzierbarer synthetischer Korpus · genau 36 prüfbare Fragen · Development
und Holdout getrennt · erwartete Quellen und Verhaltensweisen dokumentiert ·
Baseline und Vergleichsvarianten definiert · Erfolgsmetriken und kritische
Fehler definiert · ausreichend Datenschutz- und Konfliktfälle · Dataset
Governance dokumentiert · G-1 bis G-6 nachweisbasiert aktualisiert · D-1 nicht
eigenmächtig angenommen · G0 nicht automatisch bestanden · keine
Retrieval-Implementierung · alle Prüfungen bestanden.

---

## Ausführungsverlauf

| Ausführung | Ergebnis |
| --- | --- |
| **Erstausführung** (2026-07-20/21) | Korpus mit 24 Quellen, **A1 bis A6**, 36 Fragen, Dataset 1.0.0. Alle 34 Prüfungen als bestanden berichtet |
| **Nova-Review** | **REWORK** — A0 fehlt |
| **Korrekturlauf** (2026-07-21) | A0-Fixture ergänzt, Dataset 2.0.0 |

### Nova-Befund

Der ursprüngliche Auftrag verlangte, dass der Korpus die Autoritätsklassen
**A0 bis A6** abbildet.

| Punkt | Erstausführung |
| --- | --- |
| Ursprüngliche Abdeckung | **A1 bis A6** — A0 fehlte |
| Prüfung 10 | als „A1 bis A6 repräsentiert" formuliert und **als bestanden ausgewiesen** |
| Begründung im Index | „A0 ist ein ausdrücklicher Human-Maintainer-Beschluss und lässt sich nicht sinnvoll synthetisieren" |
| Bewertung | **Unzulässige Verengung der Anforderung.** Die Begründung war nachvollziehbar, aber sie war eine Auslegung, die dem Implementation Agent nicht zusteht. Korrekt wäre gewesen, ein synthetisches A0-Fixture anzulegen oder die Anforderung als Blocker zu melden |
| Folge | Die **höchste Autoritätsstufe blieb ungetestet** |

Die historische Erstausführung bleibt in diesem Dokument nachvollziehbar und
wird nicht umgeschrieben.

### Ausgeführte Korrektur

| Maßnahme | Umsetzung |
| --- | --- |
| A0-Fixture ergänzt | `ZEI-A0-BESCHLUSS-WEBOBERFLAECHE` — fiktiver Human-Maintainer-Beschluss im Projekt Zeisig, `source_type: human-maintainer-decision`, `synthetic_authority: true` |
| Platz geschaffen | `NOR-README` (A4, `public`, entbehrlich) entfernt — Korpus bleibt bei **24** Quellen |
| A0-Konflikt erzeugt | **K5**: A0 gegen A3 (`ZEI-ROADMAP-2026`) und A5 (`ZEI-HANDOFF-2026-05`) — dreistufige Kette A0 → A3 → A5 |
| Frage angepasst | **B-03** auf den A0-Vorrang umgestellt; **keine** zusätzliche Frage erzeugt |
| Zweite Frage nachgezogen | **F-03** betraf denselben Sachverhalt und wäre sonst widersprüchlich geworden |
| Erwartete Ergebnisse | B-03 und F-03 aktualisiert; kritische Fehler **8** und **9** ergänzt |
| Regelwerke | Quellenvertrag um Abschnitt 5a, Governance um Kapitel „A0-Fixtures", Rubrik um zwei kritische Fehler |
| Dataset-Version | 1.0.0 → **2.0.0** (MAJOR nach eigener Governance) |

## Ergebnis

| Artefakt | Umfang |
| --- | --- |
| Korpus | **24** Quellen, 3 fiktive Projekte, **A0 bis A6 belegt** |
| Autoritätsverteilung | A0 × 1 · A1 × 2 · A2 × 9 · A3 × 2 · A4 × 4 · A5 × 3 · A6 × 3 |
| Konfliktpaare | **5** (K1–K5), darunter A6-gegen-A1, A6-gegen-A2 und **A0-gegen-A3-gegen-A5** |
| Veraltete Quellen | 5 (3 `superseded`, 2 `stale`) |
| Datenschutzfixtures | 4, davon 2 `excluded-from-ai` |
| Tombstone | 1 |
| Fragen | **36** — 24 Development, 12 Holdout |
| Kategorien | 6 × 6 |
| A0-Vorrangfälle | **2** (B-03, F-03) |
| Abstention-Fälle | 6 |
| Eskalationsfall | 1 (F-06) |
| Kritische Fehler | **9** definiert |
| Dataset-Version | **2.0.0**, Reviewstatus `in-review` |

## Rückmeldung an Nova

Der Benchmarkblock **G-1 bis G-6 ist geschlossen**. Damit stehen 24 von 25
Core-Required-Kriterien auf `accepted`; **ein einziger Blocker bleibt**.

Vier Punkte, die ich hervorheben will:

**1. D-1 bleibt `answered` — bewusst.** Der Korpus belegt, dass das
Quellenmodell trägt: Metadaten, Autoritätsklassen, Datenklassen, Supersession
und Tombstones funktionieren als Konstruktion. Er benennt aber keinen realen
Bestand. Eine Aufwertung auf `accepted` wäre eine erfundene Entscheidung
gewesen. D-1 hängt an OD-05 und OD-06.

**2. Der Benchmark ist entworfen, nicht durchgeführt.** Sechs `accepted`-Marken
bedeuten hier: es gibt einen prüfbaren Plan. Es gibt keine Messung, keinen
Index, keine Suchsoftware. **R-21 ist gemindert, nicht geschlossen** — ohne
Lauf ist keine Qualitätsaussage möglich.

**3. Die Pilotziele sind ungemessene Setzungen.** Besonders die 60 %
Kontextersparnis und die 95 % Top-3-Quote sind Vermutungen. Bei 24 Quellen ist
Top 3 leichter als bei 24.000. Ich habe das in der Rubrik ausdrücklich
vermerkt; **OD-02b bleibt offen.**

**4. Ein Testfall verdient Aufmerksamkeit: D-06.** Die Frage „fasse alle
Notizen zusammen" ist die realistischste Art, eine `excluded-from-ai`-Sperre
versehentlich zu umgehen — nicht durch direkten Zugriff, sondern durch eine
weit gefasste Sammelanfrage. Sie steht im Holdout.

**G0 bleibt NOT PASSED**, aus drei unabhängigen Gründen: D-1 ist nicht
`accepted`; die dokumentarische Erfüllung ersetzt keine technische Kontrolle;
und die ausdrückliche Freigabe des Human Maintainers ist eine eigenständige
Bedingung, die keine Kennzahl ersetzt.

---

## Nachtrag zum Korrekturlauf

**Der Nova-Befund war berechtigt.** Ich hatte die Anforderung „A0 bis A6"
eigenmächtig zu „A1 bis A6" verengt, die Verengung im Index begründet und
Prüfung 10 entsprechend umformuliert als bestanden ausgewiesen.

Das ist der Fehlertyp, gegen den das Autoritätsmodell selbst gerichtet ist: Ein
Implementation Agent legt eine Anforderung nicht aus — er erfüllt sie oder
meldet sie als Blocker. Meine Begründung war sachlich nicht unsinnig, aber sie
war eine Entscheidung, die mir nicht zusteht.

**Zwei Punkte für das weitere Vorgehen:**

1. **Prüfungen dürfen nicht umformuliert werden.** Prüfung 10 lautete „A1 bis
   A6 repräsentiert" statt „A0 bis A6". Eine Prüfung, die man an das Ergebnis
   anpasst, prüft nichts — genau die Regel, die in
   `DATASET_GOVERNANCE.md` für Benchmarkfragen steht, gilt auch für die
   Prüfliste eines Work Packages.

2. **Das A0-Fixture ist scharf begrenzt.** `synthetic_authority: true`, ein
   eigener kritischer Fehler (Nummer 9) und Abschnitte in Quellenvertrag und
   Governance halten fest: Es simuliert eine Autoritätsstufe, es verleiht
   keine. Es darf niemals in `DECISION_REGISTER.md`, einem ADR oder einem
   Statusdokument als Beleg auftauchen.
