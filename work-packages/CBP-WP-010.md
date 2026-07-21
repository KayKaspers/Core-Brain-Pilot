# CBP-WP-010 — Pilot Source Mapping Specification

| Feld | Wert |
| --- | --- |
| ID | CBP-WP-010 |
| Titel | Pilot Source Mapping Specification |
| Typ | `docs-only`, **interactive** |
| Prompt Mode | **Full** (NDF v1.0.0) |
| Context Budget | **B1 – Lean** (Core Brain Pilot) |
| Claude Code Model | **Claude Opus 4.8** (`claude-opus-4-8`) |
| Claude Code Effort | **xhigh** |
| Phase | Phase 1 – Planung |
| Ausgeführt am | 2026-07-21 |
| Ablauf | **interaktiv**, zwei Phasen · **plus Nova-REWORK-Korrekturlauf** |
| Status | `in-review` |
| Autoritätsklasse | A2 |

> **Dieses Work Package enthält einen Nova-REWORK-Korrekturlauf.** Die
> Erstausführung wurde als COMPLETE berichtet; eine Kennzahl war widersprüchlich
> und eine Aussage zu Defaults unpräzise. Siehe
> [Nova REWORK correction run](#nova-rework-correction-run) am Ende. Die
> Erstausführung unten ist **nicht** umgeschrieben.

---

## Ziel

Die allgemeine, deploymentneutrale Spezifikation für Source Mappings der
Pilot-Slots **PS-02, PS-03 und PS-04** festlegen: Mappingformat,
Collection-Strategie und Granularität entscheiden, anschließend Schema,
Zustandsmodell, Validierung, Freigabekette, Lösch- und Tombstone-Verhalten,
slotspezifische Regeln, synthetische Beispiele, Aktivierungsgate und private
Operator-Vorlage spezifizieren.

**Keine realen oder produktiven Mappings.**

## Interaktiver Ablauf

| Phase | Inhalt | Ergebnis |
| --- | --- | --- |
| **A** | Repository read-only prüfen, **einen** Entscheidungsfragebogen ausgeben, keine Datei verändern | 22 Vorprüfungspunkte bestanden, **0 Dateiänderungen** |
| **B** | Drei Entscheidungen aufzeichnen, ADR-0008 erstellen, Spezifikation, Schema, Validierung, Beispiele und Gate erstellen, Register nachführen | 7 neue Dokumente, 3 A0-Entscheidungen |

## Human-Entscheidungen

Alle drei am **2026-07-21**, Autorität **A0**. Wortlaut unverändert übernommen,
keine Angabe ergänzt oder erweitert. Vollständig in
[ADR-0008](../docs/decisions/ADR-0008-pilot-source-mapping-konvention.md).

| Teil | Entscheidung | Kern der Notes |
| --- | --- | --- |
| **A** | **SELECT A1** — YAML 1.2 Strict Subset mit JSON-Schema-Validierung | Lesbar für Operatoren, deterministisch validierbar; JSON Schema ist die verbindliche Vertragsgrenze; keine Anchors, Aliases, Merge Keys, Tags, Duplicate Keys, Mehrfachdokumente |
| **B** | **SELECT B3** — hybride Collection-Strategie | Collections fachlich nach Projekt oder Domäne; **Slot bleibt verpflichtendes Metadatum**; **die Collection verleiht keine Autorität, Datenklasse oder AI-Transfer-Freigabe** |
| **C** | **SELECT C1** — genau eine Source Boundary je Mapping | Ein Markdown Root, ein Repository, ein Handoff Root; Rechte, Revision, Freigabe, Widerruf und Tombstone bleiben unabhängig prüfbar; **keine Kopplung mehrerer Quellen** |

Aufgezeichnet als **D-031**, **D-032**, **D-033**.

## Scope

- Klarstellung des Veröffentlichungsbegriffs in ADR-0006 und im Mapping-Plan
- Drei Entscheidungen erheben und im Wortlaut aufzeichnen
- ADR-0008 erstellen
- Mapping-Spezifikation, Schema, Validierung, Beispiele
- Aktivierungsgate definieren, **nicht** ausführen
- Private Operator-Vorlage
- Status- und Registerpflege

## Out of Scope

- Human-Entscheidung erfinden oder erweitern
- Dateiänderung vor der Human-Antwort
- **Reale Mappings, Hostpfade, private Repository-URLs, Credential References, Secrets**
- Secret-Store-Auswahl · Source-Aktivierung · Ingest · Indexierung
- Mapping-Gate ausführen
- Operator-Workspace oder Runtime-Bereich anlegen
- JSON-Schema-Datei, Parser, Validator, ausführbare Tests
- Commit, Push, Branch, Remote-Änderung, Issue, Release

## Inputs

NDF v1.0.0 · Repository-Stand auf `main` (Commit `1227aa5`) ·
`PILOT_SOURCE_CONTRACT.md` · `SOURCE_SLOT_MODEL.md` ·
`PILOT_SOURCE_MAPPING_PLAN.md` · `PHASE_1_FOUNDATION_PLAN.md` ·
`PHASE_1_WORK_PACKAGE_MAP.md` · `PHASE_1_EVIDENCE_PLAN.md` ·
`PHASE_1_STOP_CONDITIONS.md` · `ADR-0006` · `ADR-0007` ·
`DATA_CLASSIFICATION.md` · `PERMISSION_MODEL.md` · `SYSTEM_ARCHITECTURE.md` ·
`COMPONENT_MODEL.md` · `DEPLOYMENT_READINESS_CHECK.md` ·
`DECISION_REGISTER.md` · `RISK_REGISTER.md` · `WORK_PACKAGE_QUEUE.md` ·
`PROJECT_MANIFEST.md` · `PROJECT_PROFILE.md` · `CAPABILITY_MATRIX.md` ·
`COMPLIANCE_CHECK.md` · `PROJECT_BRAIN.md` · `CBP-WP-009.md` · `README.md` ·
`CLAUDE.md` · **Antworten des Human Maintainers**

## Aufgaben

| # | Aufgabe | Ergebnis |
| --- | --- | --- |
| 0 | Veröffentlichungsbegriff klarstellen | Nachtrag in ADR-0006 (*non-substantive clarification*, A1), Präzisierung im Mapping-Plan |
| A | Vorprüfung und Entscheidungsfragebogen | 22 Punkte, 0 Dateiänderungen |
| B | Entscheidungen prüfen und aufzeichnen | D-031, D-032, D-033 |
| 1 | ADR-0008 | `accepted`, A1 |
| 2 | Mapping-Spezifikation | 18 Abschnitte, Status ACCEPTED FOR IMPLEMENTATION PLANNING |
| 3 | Mapping-Schema | 31 Felder, Formatregeln F1–F7 |
| 4 | Validierung | 24 Regeln, 7 Fehlerklassen, 18 Negativtests |
| 5 | Synthetische Beispiele | 10 Beispiele, `synthetic · non-operational · test-only` |
| 6 | Aktivierungsgate | 20 Punkte, `NOT EVALUATED` |
| 7 | Status und Register | 15 Dokumente |

## Mappingfelder

**31 Felder.** Vollständig in
[PILOT_SOURCE_MAPPING_SCHEMA.md](../docs/sources/PILOT_SOURCE_MAPPING_SCHEMA.md).

`schema_version` · `mapping_id` · `slot_id` · `mapping_name` ·
`source_boundary_type` · `deployment_profile` · `operator_reference` ·
`location_reference` · `location_reference_type` · `collection` · `project` ·
`enabled` · `read_only` · `allowed_subpaths` · `excluded_subpaths` ·
`follow_symlinks` · `data_class` · `ai_transfer_policy` ·
`local_search_policy` · `indexing_policy` · `mobile_visibility` ·
`revision_strategy` · `deletion_behavior` · `verification_status` ·
`approval_status` · `approved_by` · `approved_at` · `mapping_revision` ·
`previous_revision` · `credential_reference` · `notes`

**Fail-closed-Defaults:** `enabled: false` · `read_only: true` ·
`allowed_subpaths: []` · `follow_symlinks: false` · `data_class: unknown` ·
`ai_transfer_policy: forbidden` · `indexing_policy: none` ·
`mobile_visibility: forbidden` · `verification_status: unverified` ·
`approval_status: not-approved` · `credential_reference: null`

> **Ein vollständig mit Defaults ausgefülltes Mapping ist gültig und
> wirkungslos.**

## Zustandsmodell

**10 Zustände:** `draft` → `schema-valid` → `security-checked` →
`source-verified` → `review-required` → `approved` → `enabled` ·
`suspended` · `revoked` · `deleted`

| Regel | Inhalt |
| --- | --- |
| **Z1** | `draft` darf nicht indexiert werden |
| **Z2–Z5** | `schema-valid` ist keine Sicherheitsfreigabe · `security-checked` keine Human-Freigabe · `source-verified` keine Aktivierung · **`approved` ist noch nicht `enabled`** |
| **Z8, Z9** | `revoked` und `deleted` erzwingen **Derived Cleanup** |
| **Z10** | Gelöschte `mapping_id` wird **nie wiederverwendet** |
| **Z11** | **Kein direkter Übergang von `draft` nach `enabled`** |
| **Z12** | **Kein automatischer Übergang nach `approved`** |
| **Z13** | Aktivierung erfordert einen **getrennten kontrollierten Vorgang** |

## Validierungsregeln

**24 Regeln V1–V24**, sämtlich fail-closed. **Genau acht tragen `blocker`:**
V7, V8, V9, V10, V11, V14, V20, V23 — sie halten die **Verarbeitung** an, nicht
nur die Aktivierung. Die übrigen 16 tragen `error`.

| Grundsatz | Regel |
| --- | --- |
| **FC-1** | Unbekannter Zustand blockiert |
| **FC-2** | Konflikt blockiert |
| **FC-3** | Fehlende Evidenz blockiert |
| **FC-4** | Die restriktivere Regel gewinnt |
| **FC-5** | **Eine Warnung hebt nie automatisch eine Blockade auf** |

**18 Negativtests NT-01 bis NT-18** für CBP-WP-013 definiert, **keiner
ausgeführt**.

## Aktivierungsgate

**20 Punkte**, Status **`NOT EVALUATED`**, definiert in
[PILOT_MAPPING_ACTIVATION_GATE.md](../docs/operations/PILOT_MAPPING_ACTIVATION_GATE.md).

| Ergebniswert | Wer stellt fest |
| --- | --- |
| `NOT EVALUATED` · `BLOCKED` · `READY FOR ACTIVATION DECISION` | Prüfung |
| **`APPROVED FOR ACTIVATION`** | **ausschließlich der Human Maintainer** |
| `REVOKED` | Human Maintainer oder Vorfall |

**Acht der zwanzig Punkte verlangen Nachweisstufe 4** — sie sind ohne
CBP-WP-012 nicht erfüllbar. **Das Gate wurde nicht ausgeführt.**

## Prüfungen

43 Prüfungen. Schwerpunkte: drei Entscheidungen direkt vom Human Maintainer ·
nichts ergänzt · ADR-0008-Status entspricht den Entscheidungen · ADR-0006 nur
durch sichtbaren Klarstellungsnachtrag ergänzt, Entscheidung unverändert ·
**keine öffentliche Veröffentlichung freigegeben** · Core bleibt privat ·
ausschließlich Markdown · **keine reale Location Reference, keine private URL,
kein Secret** · Schema vollständig · Defaults disabled, read-only, fail-closed ·
`unknown` blockiert · `excluded-from-ai` blockiert externe Übertragung · genau
eine Source Boundary · PS-02-, PS-03- und PS-04-Regeln vollständig ·
Zustandsmodell verhindert `draft` → `enabled` · `approved` ≠ `enabled` ·
`revoked`/`deleted` erzeugen Cleanup · ID nicht wiederverwendet · Beispiele
test-only · Vorlage ohne Werte · **Gate bleibt NOT EVALUATED** · kein Mapping
`enabled` · OD-05, OD-06, OD-34 offen · ADR-0007 `accepted` · OD-26 geschlossen
· G0, Phase, DRC, Benchmark unverändert · keine Capability `implemented` ·
**Summen ausgezählt** · genau ein Folge-Work-Package · kein Commit, kein Push.

## Akzeptanzkriterien

Drei Human-Entscheidungen eindeutig dokumentiert · ADR-0008 korrekt behandelt ·
Veröffentlichungsbegriff sichtbar klargestellt · Spezifikation und Schema
vollständig · Validierung und Zustandsmodell fail-closed · PS-02, PS-03, PS-04
vollständig abgedeckt · ausschließlich synthetische Beispiele ·
Aktivierungsgate definiert, **nicht ausgeführt** · **keine realen Mappingwerte
im Core** · **keine technische Implementierung begonnen** · alle Prüfungen
bestanden.

---

## Ergebnis

| Gegenstand | Wert |
| --- | --- |
| Neue A0-Entscheidungen | **D-031, D-032, D-033** |
| **ADR-0008** | **`accepted`** (A1) |
| Angenommene ADRs | 7 → **8** |
| Getroffene Entscheidungen | 30 → **33** (davon **29** mit A0) |
| Offene Entscheidungen | 21 → **23**, davon **5** mit P0 |
| Neue offene Entscheidungen | **OD-35** (RT-2), **OD-36** (ID-, Collection- und Versionsvorschriften) |
| Neue Dokumente | **7** |
| Mappingfelder | **31** |
| Validierungsregeln | **24** · Negativtests **18** |
| Zustände | **10** |
| Gate-Punkte | **20**, `NOT EVALUATED` |
| Synthetische Beispiele | **10** |
| **Erstellte Mappings** | **0** |
| **Angebundene Quellen** | **0** |
| **Capabilities `implemented`** | **0 von 29**, unverändert |
| Geschlossene Risiken | **0** |
| **Commit / Push** | **nein / nein** |

## Rückmeldung an Nova

Die drei Entscheidungen liegen eindeutig vor und decken sich mit den
Nova-Empfehlungen. **ADR-0008 ist `accepted`**, die Mappingkonvention steht.
**Es wurde kein Mapping erstellt, keine Quelle angebunden und nichts
aktiviert.**

**Vier Punkte, die ich hervorhebe:**

1. **Die Klarstellung aus Aufgabe 0 war überfällig und ist jetzt sichtbar
   verankert.** ADR-0006 trägt einen datierten Nachtrag als *non-substantive
   clarification* mit A1, abgeleitet aus ADR-0007 und den unveränderten
   A0-Entscheidungen D-029 und D-030. **Entscheidung und Status von ADR-0006
   sind unverändert**, der ursprüngliche Wortlaut ist nicht umgeschrieben. Ich
   hatte diese Fundstellen im REWORK-Lauf von CBP-WP-009 als außerhalb des
   Scopes gemeldet — sie sind damit geschlossen.

2. **Grundsatz M-B ist die schärfste Folge aus Teil B.** Die Entscheidung des
   Human Maintainers, dass eine Collection weder Autorität noch Datenklasse noch
   AI-Transfer-Freigabe verleiht, verhindert dieselbe Fehlerklasse wie
   Slot-Regel 8: **die Sortierordnung darf nicht zur Rechtequelle werden.** Ohne
   diesen Satz wäre B3 die riskanteste der drei Optionen gewesen.

3. **C1 kostet Betriebsaufwand und ist trotzdem richtig.** Je Quelle ein
   eigenes Mapping ist unbequemer als eine Sammeldatei. Der Gegenwert:
   Widerruf, Löschung und Tombstone treffen genau eine Quelle. Beispiel 9 in
   den synthetischen Beispielen zeigt den Fall, den C1 ausschließt.

4. **Das Aktivierungsgate ist heute nicht durchlaufbar** — und das ist kein
   Mangel dieses Work Packages. **Acht seiner zwanzig Punkte verlangen
   Nachweisstufe 4**, die ohne den F3-Strang (CBP-WP-011 → CBP-WP-012) nicht
   erreichbar ist. Ohne durchgesetzte Dateirechte und Mount-Grenzen gibt es
   keinen Read-only-Nachweis.

**Zu OD-35:** Die drei RT-2-Punkte aus ADR-0007 waren inhaltlich benannt, aber
in keinem Register geführt und damit nicht nachverfolgbar. Ich habe sie als
**einen** Registereintrag aufgenommen, nicht als drei — das ist keine Dublette,
sondern schließt eine Sichtbarkeitslücke.

**Kein Risiko wurde geschlossen.** Sämtliche Regeln dieser Spezifikation sind
dokumentarisch; es existiert kein Validator und keine technische Durchsetzung.
Alle Nachweise stehen weiterhin auf **Stufe 1 `dokumentiert`**.

**Nächstes vorgeschlagenes Work Package: CBP-WP-011 — Technical Security
Foundation Specification** (`docs-only`, Full, B2 – Standard). **Nicht
ausführen** ohne ausdrückliche Freigabe.

---

## Nova REWORK correction run

| Feld | Wert |
| --- | --- |
| Ausführung | **Nova REWORK correction run** |
| Datum | 2026-07-21 |
| Ursprünglicher Reportstatus | **COMPLETE** |
| Human-Entscheidungen | **unverändert** — D-031, D-032, D-033 nicht angetastet |
| ADR-0008 | bleibt **`accepted`** |
| Commit vor der Korrektur | **nicht erfolgt** |

**Die Erstausführung wird nicht stillschweigend umgeschrieben.** Der Bericht
oben bleibt im Wortlaut stehen; die beiden Befunde sind unten benannt und in
den Zieldokumenten korrigiert.

### Befund 1 — Blocker-Zählwiderspruch

**Ursprünglich:** „**Neun Regeln tragen `blocker`:** V7, V8, V9, V10, V11, V14,
V20, V23 — sowie jede Regel, deren Verletzung ein Secret sichtbar macht."

**Warum das falsch war:** Die Zahl **neun** stand acht aufgezählten IDs
gegenüber. Der Zusatz „sowie jede Regel, deren Verletzung ein Secret sichtbar
macht" füllte die Lücke rhetorisch auf und machte die Zahl **unprüfbar** — er
benennt keine ID und lässt sich nicht auszählen. Das verstößt gegen Zählregel 3:
Berichtssummen müssen gegen die zugrunde liegenden Zeilen prüfbar sein.

**Auszählung aus der Quelltabelle** (`Die 24 Regeln`, Spalte *Schweregrad*):

| # | Regel | Klasse | Blockadewirkung |
| --- | --- | --- | --- |
| 1 | **V7** | `SEC` | Location Reference im Core → Verarbeitung anhalten, SB-02 |
| 2 | **V8** | `SEC` | Secretfund in einem beliebigen Feld → Incident-Verfahren, SB-02 |
| 3 | **V9** | `PRI` | `data_class` `unknown` oder `secret` → Security Check, Approval und Aktivierung blockiert |
| 4 | **V10** | `PRI` | Unzulässige Kombination `data_class` × `ai_transfer_policy` → abgelehnt statt korrigiert |
| 5 | **V11** | `SEC` | `read_only: false` ohne A0-Entscheidung → Aktivierung blockiert |
| 6 | **V14** | `SEC` | Symlinkziel außerhalb der Boundary → Verarbeitung anhalten |
| 7 | **V20** | `SEC` | Rechte über das Nötige hinaus → Aktivierung blockiert |
| 8 | **V23** | `SEC` | `credential_reference` enthält einen Wert → SB-02 |

| Kennzahl | Ausgezählt |
| --- | --- |
| **Validierungsregeln gesamt** | **24** (V1–V24) |
| **Blocker** | **8** — sechs `SEC`, zwei `PRI` |
| **`error`** | **16** |
| **Negativtests** | **18** (NT-01–NT-18) |
| Duplikate in der Blockerliste | **0** |
| Blocker-IDs außerhalb V1–V24 | **0** |

**Korrektur:** „Genau acht der 24 Regeln tragen `blocker`" — mit vollständiger
ID-Tabelle und Blockadewirkung je Regel. Der unprüfbare Zusatz ist entfernt.

### Befund 2 — unpräzise Default- und Validitätsaussage

**Ursprünglich:** „Ein vollständig mit Defaults ausgefülltes Mapping ist gültig
und wirkungslos. Das ist beabsichtigt."

**Warum das falsch war:** Der Satz trennte **Vorlage**, **Schema-Validität** und
**operative Freigabe** nicht. Er hätte so gelesen werden können, als sei ein
Dokument, in dem nur Defaults stehen, bereits „gültig" — obwohl ihm sämtliche
Pflichtwerte fehlen und **V2** es verweigert. Restriktive Defaults machen ein
Mapping wirkungslos; sie machen es nicht vollständig.

**Korrektur — sieben Validitätsstufen**, kumulativ, keine impliziert die
nächste:

| Stufe | Bedeutet | Bedeutet **nicht** |
| --- | --- | --- |
| **1 Template** | Leere oder nur mit Defaults versehene Vorlage | **kein vollständiges Mapping**; fehlende Pflichtwerte verhindern Schema-Validität |
| **2 Parsed** | Syntaktisch lesbar | **nicht schema-valid** |
| **3 Schema-valid** | Alle Schema- und Formatregeln erfüllt | nicht security-checked, source-verified, approved, enabled, ingestfähig |
| **4 Security-checked** | Sicherheits- und Datenschutzblocker geprüft | **keine Human-Freigabe** |
| **5 Source-verified** | Boundary, Erreichbarkeit, minimale Rechte geprüft | **nicht enabled** |
| **6 Approved** | Ausdrückliche Human-Freigabe | **nicht automatisch enabled** |
| **7 Enabled** | Aktivierung im getrennten kontrollierten Vorgang nach bestandenem Gate | — |

**`parsed` wurde nicht als persistenter Zustand eingeführt.** Das
Zustandsmodell führt weiterhin **10** Zustände; `parsed` ist ausschließlich ein
Verarbeitungsbegriff vor `schema-valid` (Regel P1).

**Korrektur — restriktive Defaults:**

| Default | Zulässiger Schemawert | Blockiert |
| --- | --- | --- |
| `data_class: unknown` | **ja** | Security Check, Approval, Aktivierung; fail-closed wie `excluded-from-ai` |
| `allowed_subpaths: []` | **ja** | nimmt keine Inhalte auf; Source Verification und Aktivierung |
| `enabled: false` | ja | keine Aufnahme in Ingest oder Retrieval |
| `approval_status: not-approved` | ja | **keine Freigabe** |
| `verification_status: unverified` | ja | **kein technischer Nachweis** |
| `ai_transfer_policy: forbidden` | ja | keine externe Übertragung |
| `indexing_policy: none` | ja | keine Indexierung |

### Korrigierte Handoff-Bedeutung

Die Vorlage `# BEGIN PRIVATE OPERATOR MAPPING INPUT` trägt jetzt eine
ausdrückliche Kennzeichnung: **absichtlich unvollständig**, **kein
schema-valides Mapping**, **kein Aktivierungsartefakt**, nur außerhalb des
Core-Repositorys auszufüllen, restriktive Defaults bleiben nach der Ausfüllung
bestehen, und eine **ausgefüllte Fassung darf nicht in einen Implementation
Report kopiert werden**.

> **Ausfüllen ist nicht Validieren, Validieren ist nicht Freigeben, Freigeben
> ist nicht Aktivieren.**

### Ausgeführte Prüfevidenz

| Prüfung | Ergebnis |
| --- | --- |
| Blockerzahl aus der Quelltabelle ausgezählt | bestanden — **8** |
| Dokumentierte Zahl entspricht der ID-Liste | bestanden — 8 Zahl, 8 IDs |
| Jede Blocker-ID existiert in V1–V24 | bestanden |
| Keine ID doppelt gezählt | bestanden — 0 Duplikate |
| Regelzahl entspricht der Quelltabelle | bestanden — **24** |
| Negativtestzahl entspricht der Quelltabelle | bestanden — **18** |
| Keine widersprüchliche Blockerzahl mehr im Repository | bestanden — beide Fundstellen korrigiert |
| Leere Vorlage nicht als schema-valid bezeichnet | bestanden |
| Fehlende Pflichtfelder blockieren schema-valid | bestanden — V2 |
| `parsed` und `schema-valid` getrennt | bestanden — P1 |
| `schema-valid` und `security-checked` getrennt | bestanden — Z2, Stufe 3/4 |
| `security-checked` und `approved` getrennt | bestanden — Z3, Stufe 4/6 |
| `approved` und `enabled` getrennt | bestanden — Z5, Gate 16/20 |
| `parsed` **nicht** als persistenter Zustand eingeführt | bestanden — 10 Zustände unverändert |
| Human-Entscheidungen unverändert | bestanden — D-031, D-032, D-033 |

### Was ich daraus mitnehme

**Der erste Befund ist ein Zählfehler mit einer Besonderheit:** Die Zahl war
nicht falsch abgeschrieben, sondern durch einen unbestimmten Zusatz
*plausibilisiert* worden. Eine Aufzählung, die mit „sowie jede Regel, die …"
endet, entzieht sich der Auszählung — und genau darin lag der Fehler. Zählregel
3 verlangt Prüfbarkeit gegen die Quelltabelle; ein offener Zusatz macht das
unmöglich.

**Der zweite Befund ist derselbe Fehlertyp wie im REWORK von CBP-WP-009:** eine
zulässige Eigenschaft wurde zu einer stärkeren verallgemeinert. Dort wurde aus
„privater Bestand ist ausgeschlossen" ein „veröffentlichbar", hier aus
„restriktive Defaults sind zulässige Schemawerte" ein „gültig". Beide Male war
die kürzere Formulierung eingängiger — und beide Male hätte sie eine Lücke
gedeckt.
