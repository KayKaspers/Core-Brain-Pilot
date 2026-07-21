# Pilot Source Mapping Specification

| Feld | Wert |
| --- | --- |
| **Status** | **ACCEPTED FOR IMPLEMENTATION PLANNING** |
| **Nicht** | IMPLEMENTED · ACTIVE · DEPLOYED |
| Grundlage | **ADR-0008** (A1), ADR-0006, ADR-0007 |
| Entschieden in | **CBP-WP-010** — D-031, D-032, D-033 (A0) |
| Autoritätsklasse | A2 |
| Gilt für | **PS-02, PS-03, PS-04** |
| Stand | 2026-07-21 |

---

## 1 — Zweck

Diese Spezifikation legt fest, **wie ein Deployment Mapping aussieht, welchen
Lebenszyklus es durchläuft und unter welchen Bedingungen es wirksam werden
darf**.

Sie ist die verbindliche Fassung. Der Planungsstand
[PILOT_SOURCE_MAPPING_PLAN.md](../roadmap/PILOT_SOURCE_MAPPING_PLAN.md) aus
CBP-WP-008 bleibt als Historie erhalten; bei Abweichungen gilt dieses Dokument.

## 2 — Scope

| Gegenstand | Enthalten |
| --- | --- |
| Mappingformat, Collection-Strategie, Granularität | ja — ADR-0008 |
| Feldschema, 31 Felder | ja — [Schema](PILOT_SOURCE_MAPPING_SCHEMA.md) |
| Zustandsmodell, 10 Zustände | ja |
| Validierungsregeln V1–V24 | ja — [Validation](PILOT_SOURCE_MAPPING_VALIDATION.md) |
| Freigabekette, Lösch- und Tombstone-Verhalten | ja |
| Slotspezifische Regeln PS-02, PS-03, PS-04 | ja |
| Synthetische Beispiele | ja — [Examples](PILOT_SOURCE_MAPPING_EXAMPLES.md) |
| Aktivierungsgate | ja — [Gate](../operations/PILOT_MAPPING_ACTIVATION_GATE.md), `NOT EVALUATED` |

## 3 — Non-Goals

| Nicht Gegenstand | Zuständig |
| --- | --- |
| Konkrete Mappings, reale Location References | **OD-05, OD-06** — offen |
| Secret-Store-Technologie, Credential-Format | **OD-34** — offen |
| PS-01, PS-05 (kein Mapping nötig) · PS-06, PS-07 (`deferred`) | Quarantäne, CBP-WP-013 |
| JSON-Schema-Datei, Parser, Validator | spätere Implementierung |
| Aktivierung, Ingest, Indexierung, Retrieval | Gate; P6, CBP-WP-013 |
| Suchprovider | OD-25 |

**Diese Spezifikation aktiviert nichts.**

## 4 — Core-, Operator- und Runtime-Grenze

Verbindlich aus **ADR-0007**.

| Bereich | Enthält bezüglich Mappings | Klasse |
| --- | --- | --- |
| **Core Repository** | Schema, Validierungsregeln, Zustandsmodell, **synthetische** Beispiele, Dokumentation, später der Validator-Code | `publication-capable by design` — **nicht freigegeben** |
| **Privater Operator-Workspace** | **Ausgefüllte Mappings**, reale Location References, operatorbezogene kanonische Registry-Metadaten, Verweise auf den Secret Store | **kanonisch**, sicherungspflichtig |
| **Runtime-Datenbereich** | **Mapping-Projektionen** für Suche und Betrieb (RT-1), Auditnachweise zu Freigaben (RT-2) | abgeleitet bzw. Operational Evidence |

| # | Grenze |
| --- | --- |
| **MG-1** | Ein **ausgefülltes** Mapping liegt nie im Core-Repository |
| **MG-2** | Core-Beispiele verwenden **ausschließlich synthetische Platzhalter** |
| **MG-3** | Die **Runtime-Projektion ist nicht die kanonische Mapping-Quelle** |
| **MG-4** | Verlust der Runtime-Projektion ist über Rebuild behebbar; Verlust der kanonischen Mappings ist **Datenverlust** |
| **MG-5** | Secrets liegen in **keinem** der drei Bereiche im Klartext |

## 5 — Ausgewähltes Mappingformat

**YAML 1.2 Strict Subset mit JSON-Schema-Validierung** — D-031 (A0).

Vollständige Format- und Verbotsregeln F1–F7 im
[Schema](PILOT_SOURCE_MAPPING_SCHEMA.md). Kern:

- genau ein Mapping-Dokument je Datei, UTF-8, keine Tabulatoren
- **keine** Anchors, Aliases, Merge Keys, benutzerdefinierten Tags
- **doppelte Schlüssel werden abgelehnt**, nicht überschrieben
- unbekannte Felder **blockieren die Aktivierung**
- Serialisierung deterministisch normalisierbar
- **JSON Schema ist die maschinenprüfbare Vertragsgrenze**

## 6 — Ausgewählte Collection-Strategie

**Hybrid: fachliche Collection plus verpflichtende Slot-Kennzeichnung** —
D-032 (A0).

| Achse | Feld | Zweck |
| --- | --- | --- |
| **Fachlich** | `collection`, `project` | Retrieval, Berechtigungen, Gruppierung |
| **Provenienz** | `slot_id` | Herkunftsart, Ingest-Regeln, Löschung, Audit |

> **Grundsatz M-B:** **Eine Collection verleiht nichts.** Autoritätsklasse,
> Datenklasse und AI-Transfer-Freigabe stammen aus Slot, Mapping und Dokument —
> **niemals** aus der Zugehörigkeit zu einer Collection.

Das ist dieselbe Fehlerklasse wie Slot-Regel 8: Die Ablage darf nicht zur
Autoritätsquelle werden, sonst wäre Verschieben eine Beförderung.

## 7 — Ausgewählte Granularität

**Genau eine Source Boundary je Mapping** — D-033 (A0).

| Slot | Eine Boundary bedeutet |
| --- | --- |
| **PS-02** | genau **ein** freigegebener Markdown Root |
| **PS-03** | genau **ein** freigegebenes Git Repository |
| **PS-04** | genau **ein** freigegebener Handoff Root |

**Mehrere Quellen dürfen nicht durch ein gemeinsames Mapping gekoppelt werden.**

> **Grundsatz M-C:** Was gemeinsam gemappt ist, wird gemeinsam widerrufen.
> Deshalb wird nichts gemeinsam gemappt.

## 8 — Mapping-Lebenszyklus

### Validitätsstufen

Sieben Stufen, **kumulativ**. Jede höhere setzt alle darunter voraus. Keine
Stufe impliziert die nächste.

| # | Stufe | Bedeutet | Bedeutet **nicht** |
| --- | --- | --- | --- |
| **1** | **Template** | Eine leere oder nur mit Defaults versehene Handoff-Vorlage | **kein vollständiges Mapping.** Fehlende verpflichtende Identitäts-, Boundary-, Location- oder Revisionswerte **verhindern** Schema-Validität |
| **2** | **Parsed** | Das Dokument ist syntaktisch lesbar | **nicht schema-valid** |
| **3** | **Schema-valid** | Alle Schema- und Formatregeln erfüllt | **nicht** security-checked, source-verified, approved, enabled oder ingestfähig |
| **4** | **Security-checked** | Sicherheits- und Datenschutzblocker geprüft | **keine Human-Freigabe** |
| **5** | **Source-verified** | Boundary, Erreichbarkeit und minimale Rechte geprüft | **nicht enabled** |
| **6** | **Approved** | Ausdrückliche Human-Freigabe liegt vor | **nicht automatisch enabled** |
| **7** | **Enabled** | Aktivierung in einem **getrennten kontrollierten Vorgang** nach bestandenem Activation Gate | — |

> **`parsed` ist ein Verarbeitungsbegriff, kein persistierter Zustand.** Er
> beschreibt einen Zwischenschritt vor `schema-valid` und erscheint deshalb
> **nicht** im Zustandsmodell unten. Ein Dokument wird nicht mit dem Zustand
> „parsed" gespeichert.

**Stufe 1 ist die wichtigste Abgrenzung.** Eine Vorlage sieht aus wie ein
Mapping, ist aber keines: Ohne `mapping_id`, `slot_id`,
`source_boundary_type`, `location_reference`, `collection`, `project` und
`revision_strategy` verweigert bereits **V2**.

### Zehn Zustände

| # | Zustand | Bedeutung | Erreichbar aus |
| --- | --- | --- | --- |
| 1 | `draft` | Angelegt, nichts geprüft | — |
| 2 | `schema-valid` | Format und Schema geprüft | `draft` |
| 3 | `security-checked` | Secret-, Datenklassen- und Rechteprüfung bestanden | `schema-valid` |
| 4 | `source-verified` | Quelle erreichbar, Rechte minimal nachgewiesen | `security-checked` |
| 5 | `review-required` | Bereit zur menschlichen Prüfung | `source-verified` |
| 6 | `approved` | Menschlich freigegeben | `review-required` |
| 7 | `enabled` | Aktiv angebunden | `approved` — **nur über das Gate** |
| 8 | `suspended` | Vorübergehend ausgesetzt | `enabled` |
| 9 | `revoked` | Freigabe zurückgenommen | `approved`, `enabled`, `suspended` |
| 10 | `deleted` | Entfernt; Tombstone bleibt | jeder Zustand |

```text
draft ─► schema-valid ─► security-checked ─► source-verified ─► review-required
                                                                       │
                                                                       ▼
                                        suspended ◄───── enabled ◄── approved
                                            │               │           │
                                            └───────────────┴───► revoked
                                                                       │
                                        (jeder Zustand) ─────────► deleted
```

### Zustandsregeln

| # | Regel |
| --- | --- |
| **Z1** | **`draft` darf nicht indexiert werden** |
| **Z2** | **`schema-valid` ist keine Sicherheitsfreigabe** |
| **Z3** | **`security-checked` ist keine Human-Freigabe** |
| **Z4** | **`source-verified` ist keine Aktivierung** |
| **Z5** | **`approved` ist noch nicht `enabled`** |
| **Z6** | `enabled` benötigt **alle** vorherigen Nachweise |
| **Z7** | `suspended` blockiert neuen Ingest **und** Retrieval-Aufnahme |
| **Z8** | `revoked` erzwingt **Deaktivierung und Derived Cleanup** |
| **Z9** | `deleted` erzeugt **Tombstone und Derived Cleanup** |
| **Z10** | Eine gelöschte `mapping_id` wird **nie wiederverwendet** |
| **Z11** | **Kein direkter Übergang von `draft` nach `enabled`** |
| **Z12** | **Kein automatischer Übergang nach `approved`** — nur ein Mensch |
| **Z13** | **Aktivierung erfordert einen getrennten kontrollierten Vorgang** |
| **Z14** | Ein unbekannter Zustand wird wie `draft` behandelt — ohne jede Wirkung |

**Z2 bis Z5 sind die vier Verwechslungen, die dieses Modell verhindert.** Jede
von ihnen ist ein plausibler Kurzschluss: „validiert" klingt wie „sicher",
„geprüft" wie „freigegeben", „freigegeben" wie „aktiv". Sie sind es nicht.

## 9 — Autoritätsgrenzen

| # | Regel |
| --- | --- |
| **A1** | Ein Mapping **verleiht keine Autoritätsklasse.** Autorität stammt aus dem Dokument, nicht aus der Anbindung |
| **A2** | Eine Collection verleiht keine Autorität (M-B) |
| **A3** | Ein Mapping kann Slot-Rechte nur **einschränken**, nie erweitern |
| **A4** | Bei Widerspruch zwischen Slot und Mapping gewinnt die **restriktivere** Angabe |
| **A5** | **A0-Zuweisungen** müssen auf eine benennbare menschliche Entscheidung zurückführbar sein |

## 10 — Datenklassengrenzen

| Datenklasse | Zulässig im Mapping | Wirkung |
| --- | --- | --- |
| `public` | ja | keine Sonderregel |
| `internal` | ja | Pilotumfang |
| `confidential` | **nicht im Pilot** (D-020) | Modell trägt die Klasse, Pilot nutzt sie nicht |
| `excluded-from-ai` | ja | **erzwingt `ai_transfer_policy: forbidden`** |
| `unknown` | nur als **Ausgangszustand** | **fail-closed** — Behandlung wie `excluded-from-ai`; blockiert Aktivierung |
| `secret` | **niemals** | Fund ist Blocker, löst SB-02 aus |

## 11 — AI-Transfer-Grenzen

| # | Regel |
| --- | --- |
| **T1** | Vorgabe ist **`forbidden`** |
| **T2** | `excluded-from-ai` **erzwingt** `forbidden` — jede andere Kombination wird **abgelehnt, nicht korrigiert** |
| **T3** | `unknown` erzwingt `forbidden` |
| **T4** | `restricted` erfordert eine dokumentierte Einschränkung |
| **T5** | Die Regel gilt für **Suchergebnis, Context Pack und Antwort** gleichermaßen |
| **T6** | Auch **Sammelanfragen** und Zusammenfassungen unterliegen T2 |

**T6 ist der Weg, der in Benchmarkfrage D-06 geprüft wird** — breit gefasste
Anfragen, die gesperrten Inhalt indirekt einsammeln.

## 12 — Aktivierungsbedingungen

Ein Mapping erreicht `enabled` **nur**, wenn **alle 20 Gate-Punkte** aus
[PILOT_MAPPING_ACTIVATION_GATE.md](../operations/PILOT_MAPPING_ACTIVATION_GATE.md)
erfüllt sind.

| # | Kernbedingung |
| --- | --- |
| 1 | Mapping liegt **außerhalb** des Core-Repositorys |
| 2 | Schema validiert, keine unbekannten Felder |
| 3 | Secret-Prüfung bestanden |
| 4 | Datenklasse **bestätigt**, nicht `unknown` |
| 5 | `allowed_subpaths` **nicht leer** |
| 6 | Ausschlüsse **negativ getestet** |
| 7 | Quelle erreichbar, Rechte minimal |
| 8 | **Human Approval erfolgt** |
| 9 | **Aktivierung separat autorisiert** |

**Das Gate steht auf `NOT EVALUATED`.** Es wurde nicht ausgeführt.

## 13 — Änderungs- und Revisionsregeln

| # | Regel |
| --- | --- |
| **R1** | Jede inhaltliche Änderung erhöht `mapping_revision` |
| **R2** | `previous_revision` bildet eine **lückenlose Kette** |
| **R3** | Eine Änderung setzt `verification_status` auf `unverified` zurück |
| **R4** | Eine **sicherheitsrelevante** Änderung setzt zusätzlich `approval_status` auf `not-approved` und `enabled` auf `false` |
| **R5** | Kein aktiver Vorgänger derselben Revision (V22) |
| **R6** | `mapping_id` ändert sich **nie** durch eine Revision |

**Sicherheitsrelevant im Sinne von R4:** `location_reference`, `read_only`,
`allowed_subpaths`, `excluded_subpaths`, `follow_symlinks`, `data_class`,
`ai_transfer_policy`, `indexing_policy`, `mobile_visibility`,
`credential_reference`.

## 14 — Lösch- und Tombstone-Regeln

| # | Regel |
| --- | --- |
| **D1** | Löschen erzeugt einen **Tombstone**, nie eine leere Lücke |
| **D2** | Ein Tombstone trägt eine **Pflichtbegründung** |
| **D3** | `revoked` und `deleted` erzwingen **Derived Cleanup** — Index, Cache, Context Packs zur betroffenen Quelle |
| **D4** | Ein **Rebuild belebt einen getombsteinten Eintrag nie wieder** |
| **D5** | Die `mapping_id` wird **nie wiederverwendet** |
| **D6** | Der Tombstone ist **kanonisch** und wird gesichert |
| **D7** | Ein Secret-Fund erzwingt Tombstone **plus** Incident-Verfahren |

**D4 verhindert stille Wiederauferstehung:** Ein Rebuild, der die Quelle erneut
liest und den Tombstone ignoriert, macht die Löschung rückgängig. Das Registry
entscheidet über Zugehörigkeit, nicht die Quelle.

## 15 — Slotspezifische Regeln

### PS-02 — Operator Markdown Knowledge Root

| # | Regel |
| --- | --- |
| 1 | **Genau ein freigegebener Root** je Mapping (C1) |
| 2 | **Nur Markdown** im ersten Piloten |
| 3 | **Read-only** für Index und Retrieval |
| 4 | Schreibvorschläge **ausschließlich über den Review-Workflow** |
| 5 | **Symlinks werden standardmäßig nicht verfolgt** |
| 6 | Unterpfade **ausschließlich per Allowlist** |
| 7 | **Ausgeschlossene Unterpfade gewinnen** |
| 8 | **Keine Secrets** |
| 9 | **Keine unkontrollierten Dateibäume** — ein Root ohne Allowlist wird nicht aktiviert |

### PS-03 — Selected Git Repositories

| # | Regel |
| --- | --- |
| 1 | **Genau ein Repository** je Mapping (C1) |
| 2 | Repository muss **separat allowlisted** sein |
| 3 | URL oder lokaler Clone-Pfad **ausschließlich im privaten Workspace** |
| 4 | Standardzugriff **read-only** |
| 5 | **Keine automatischen Commits** |
| 6 | **Keine automatischen Pushes** |
| 7 | **Kein pauschaler GitHub-Schreibzugriff** |
| 8 | **Revision oder Commit muss für Evidenz erfassbar** sein |
| 9 | Draft-Änderungen **nur in getrennten, ausdrücklich erlaubten Arbeitsbereichen** |

Regeln 5 bis 7 sind Wiederholungen aus `PERMISSION_MODEL.md`: Claude ist
`forbidden` auf `github remote` und hat nur `draft` auf `git repository`.

### PS-04 — Approved Chat Handoffs

| # | Regel |
| --- | --- |
| 1 | **Genau ein freigegebener Handoff Root** je Mapping (C1) |
| 2 | **Keine vollständigen unkontrollierten Chatarchive** |
| 3 | Nur **klar begrenzte und freigegebene** Handoff-Artefakte |
| 4 | **A5 nur nach Human-Freigabe** |
| 5 | **Automatische Zusammenfassungen bleiben A6** |
| 6 | **Provenienz zum Ursprung muss erhalten bleiben** |
| 7 | **Keine Secrets** |
| 8 | **Widerruf erzeugt Derived Cleanup** |

Regeln 4 und 5 halten das Autoritätsmodell stabil: Ein Handoff wird nicht
dadurch A5, dass er in einem Handoff-Verzeichnis liegt.

## 16 — Audit- und Operational-Evidence-Anforderungen

Mappingbezogene Nachweise sind **RT-2 Operational Evidence** (ADR-0007) — **kein
Cache**, nicht reproduzierbar, aufbewahrungs- und sicherungspflichtig.

| Ereignis | Nachweis |
| --- | --- |
| Anlage, Revisionswechsel | Zeitpunkt, Revision, auslösende Rolle |
| Zustandswechsel | Vorher-, Nachherzustand, Grund |
| **Human Approval** | Rollenkennung, Zeitpunkt, Bezug auf Revision |
| **Aktivierung und Deaktivierung** | Gate-Ergebnis, Autorisierung |
| Widerruf, Löschung | Grund, Tombstone, Cleanup-Beleg |
| **Abgelehnter Versuch** | ebenfalls protokolliert |

| # | Regel |
| --- | --- |
| **AE-1** | Auditeinträge sind für die protokollierte Komponente **nicht löschbar** |
| **AE-2** | Sie gehören **nicht** ins Core-Repository |
| **AE-3** | Sie sind in Backup- und Aufbewahrungsregeln einzubeziehen (**OD-35**) |
| **AE-4** | Ein verlorener Auditnachweis ist **verloren** — kein Rebuild stellt ihn her |

## 17 — Fehler- und Stop-Bedingungen

| Auslöser | Wirkung | Stop-Bedingung |
| --- | --- | --- |
| Secret in Mapping, `notes` oder `credential_reference` | **Blocker**, Incident-Verfahren | **SB-02** |
| Realer Pfad oder private URL im Core-Repository | **Blocker** | **SB-02** |
| `enabled: true` ohne vollständiges Gate | Rücksetzung auf `false` | SB-12 |
| `data_class: unknown` bei Aktivierung | **Blockade** | **SB-07** |
| `excluded-from-ai` erreicht Modellkontext | Retrieval stoppen, Context Packs verwerfen | **SB-03** |
| Getombsteinte Quelle nach Rebuild auffindbar | Index sperren, Cleanup | **SB-08** |
| Unbekannter Zustand oder unbekanntes Feld | **Blockade** | SB-12 |
| Schreibzugriff trotz `read_only: true` | Sofort anhalten | **SB-01** |

Vollständig in
[PHASE_1_STOP_CONDITIONS.md](../roadmap/PHASE_1_STOP_CONDITIONS.md).

## 18 — Spätere Implementierungsnachweise

Zu erbringen in **CBP-WP-013** und folgenden. **Keiner existiert heute.**

| # | Nachweis | Art | Zielstufe |
| --- | --- | --- | --- |
| 1 | Mapping validiert gegen JSON Schema | NW-IMP | 2 |
| 2 | Quelle erreichbar | NW-IMP | 2 |
| 3 | Rechte minimal | NW-SEC | 4 |
| 4 | **Ausschlüsse wirksam** — negativ getestet | **NW-NEG** | **4** |
| 5 | **Keine Secrets** — Scan ohne Fund | **NW-SEC** | **4** |
| 6 | **Datenklasse bestätigt** | NW-PRI | 4 |
| 7 | **AI-Transfer-Regel getestet** — kein Modellkontext bei `forbidden` | **NW-NEG** | **4** |
| 8 | Symlink-Verhalten geprüft | NW-NEG | 4 |
| 9 | Unbekanntes Feld blockiert | NW-NEG | 4 |
| 10 | Tombstone überlebt Rebuild | NW-NEG | 4 |
| 11 | Derived Cleanup nach Widerruf wirksam | NW-NEG | 4 |
| 12 | Human Approval aufgezeichnet | NW-HUM | 6 |

Stufen nach
[PHASE_1_EVIDENCE_PLAN.md](../roadmap/PHASE_1_EVIDENCE_PLAN.md). **Alles steht
derzeit auf Stufe 1 `dokumentiert`.**

---

## Private Operator Handoff

> **Diese Vorlage ist absichtlich unvollständig.**
>
> | Feststellung | |
> | --- | --- |
> | Sie ist **kein schema-valides Mapping** | Verpflichtende Identitäts-, Boundary-, Location-, Collection- und Revisionswerte fehlen; **V2** verweigert |
> | Sie ist **kein Aktivierungsartefakt** | Sie erzeugt keinerlei Wirkung |
> | Sie darf **nur außerhalb des Core-Repositorys** ausgefüllt werden | MG-1, V7 |
> | **Erst** die vollständige private Ausfüllung **und** eine spätere Validierung können zu **schema-valid** führen | Stufe 3 der Validitätsstufen |
> | **Restriktive Defaults bleiben auch nach der Ausfüllung bestehen**, bis sie kontrolliert und zulässig geändert werden | siehe Tabelle unten |
> | Eine **ausgefüllte** Vorlage darf **nicht in einen Implementation Report** kopiert werden | Regel 4 unten |
>
> **Ausfüllen ist nicht Validieren, Validieren ist nicht Freigeben, Freigeben
> ist nicht Aktivieren.**

Der folgende Block wird **ausschließlich außerhalb des Core-Repositorys**
ausgefüllt.

# BEGIN PRIVATE OPERATOR MAPPING INPUT

schema_version:
mapping_id:
slot_id:
mapping_name:
source_boundary_type:
deployment_profile:
operator_reference:
location_reference:
location_reference_type:
collection:
project:
enabled: false
read_only: true
allowed_subpaths: []
excluded_subpaths: []
follow_symlinks: false
data_class: unknown
ai_transfer_policy: forbidden
local_search_policy:
indexing_policy: none
mobile_visibility: forbidden
revision_strategy:
deletion_behavior:
verification_status: unverified
approval_status: not-approved
approved_by:
approved_at:
mapping_revision:
previous_revision:
credential_reference:
notes:

# END PRIVATE OPERATOR MAPPING INPUT

### Verbindlicher Hinweis

| # | Regel |
| --- | --- |
| 1 | **Den Block nur außerhalb des Core-Repositorys ausfüllen.** |
| 2 | **Keine ausgefüllte Fassung** in Chat, Core-Repository oder unkontrolliertem Ticket speichern. |
| 3 | **Secrets nie eintragen** — auch nicht in `notes`. |
| 4 | **Location Reference und private Werte nicht in einen Implementation Report übernehmen.** |
| 5 | **Die leere Vorlage ist keine Aktivierung.** |

### Was die Vorgabewerte bedeuten

Die Defaults im Block sind bewusst restriktiv. **Sie erzeugen keine operative
Wirkung — und sie ersetzen keine Pflichtwerte.**

| Default | Zulässiger Schemawert | Blockiert |
| --- | --- | --- |
| `data_class: unknown` | **ja** | **Security Check, Approval und Aktivierung** (V9); fail-closed wie `excluded-from-ai` |
| `allowed_subpaths: []` | **ja** | **nimmt keine Inhalte auf**; blockiert Source Verification und Aktivierung (V12) |
| `enabled: false` | ja | **keine Aufnahme in Ingest oder Retrieval** |
| `approval_status: not-approved` | ja | **keine Freigabe** |
| `verification_status: unverified` | ja | **kein technischer Nachweis** |
| `ai_transfer_policy: forbidden` | ja | **keine externe Übertragung** |
| `indexing_policy: none` | ja | **keine Indexierung** |

**Ein Dokument mit diesen Defaults, aber ohne Pflichtwerte, ist nicht
schema-valid.** Sind alle Pflichtwerte gesetzt, kann es Stufe 3 erreichen —
bleibt aber, solange die steuernden Felder auf ihren Defaults stehen, **nicht
security-checked, nicht source-verified, nicht approved, nicht enabled und
nicht ingestfähig**.

Der Weg nach oben führt über sieben Stufen und ein Gate, nicht über das
Überschreiben eines Defaults.

## Status

**ACCEPTED FOR IMPLEMENTATION PLANNING.**

**Es existiert kein Mapping.** Kein Slot ist aktiviert, keine Quelle
angebunden, kein Ingest ausgeführt, kein Index gebaut, kein Validator
geschrieben. **Das Aktivierungsgate steht auf `NOT EVALUATED`.**

**OD-05, OD-06 und OD-34 bleiben offen.**

**Implementierung erlaubt: nein.**
