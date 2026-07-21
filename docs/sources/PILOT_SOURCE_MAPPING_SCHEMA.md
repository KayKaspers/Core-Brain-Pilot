# Pilot Source Mapping Schema — Feldmodell

| Feld | Wert |
| --- | --- |
| **Status** | **ACCEPTED FOR IMPLEMENTATION PLANNING** |
| **Nicht** | IMPLEMENTED · ACTIVE · DEPLOYED |
| Grundlage | **ADR-0008** (A1), ADR-0006, ADR-0007 |
| Erfasst in | CBP-WP-010 |
| Autoritätsklasse | A2 |
| Schema-Version | **`1.0`** |
| Stand | 2026-07-21 |

Dieses Dokument definiert **31 Felder**. Es enthält **keinen realen Pfad, keine
private Repository-URL, keine Hostangabe, keine reale Credential Reference und
kein Secret**. Es ist keine Konfigurationsdatei, kein JSON Schema und nicht
ausführbar.

---

## Feldübersicht

| # | Feld | Typ | Pflicht | Default |
| --- | --- | --- | --- | --- |
| 1 | `schema_version` | String | **ja** | — |
| 2 | `mapping_id` | String | **ja** | — |
| 3 | `slot_id` | Enum | **ja** | — |
| 4 | `mapping_name` | String | **ja** | — |
| 5 | `source_boundary_type` | Enum | **ja** | — |
| 6 | `deployment_profile` | Enum | **ja** | — |
| 7 | `operator_reference` | String | **ja** | — |
| 8 | `location_reference` | String | **ja** | — |
| 9 | `location_reference_type` | Enum | **ja** | — |
| 10 | `collection` | String | **ja** | — |
| 11 | `project` | String | **ja** | — |
| 12 | `enabled` | Boolean | **ja** | **`false`** |
| 13 | `read_only` | Boolean | **ja** | **`true`** |
| 14 | `allowed_subpaths` | Sequenz | **ja** | **`[]`** |
| 15 | `excluded_subpaths` | Sequenz | **ja** | `[]` |
| 16 | `follow_symlinks` | Boolean | **ja** | **`false`** |
| 17 | `data_class` | Enum | **ja** | **`unknown`** |
| 18 | `ai_transfer_policy` | Enum | **ja** | **`forbidden`** |
| 19 | `local_search_policy` | Enum | **ja** | `forbidden` |
| 20 | `indexing_policy` | Enum | **ja** | **`none`** |
| 21 | `mobile_visibility` | Enum | **ja** | **`forbidden`** |
| 22 | `revision_strategy` | Enum | **ja** | — |
| 23 | `deletion_behavior` | Enum | **ja** | `tombstone-and-cleanup` |
| 24 | `verification_status` | Enum | **ja** | **`unverified`** |
| 25 | `approval_status` | Enum | **ja** | **`not-approved`** |
| 26 | `approved_by` | String \| null | ja | `null` |
| 27 | `approved_at` | String \| null | ja | `null` |
| 28 | `mapping_revision` | Integer | **ja** | `1` |
| 29 | `previous_revision` | Integer \| null | ja | `null` |
| 30 | `credential_reference` | String \| null | nein | `null` |
| 31 | `notes` | String \| null | nein | `null` |

**Jedes Pflichtfeld muss vorhanden sein** — auch dann, wenn es seinen Default
trägt. Ein fehlendes Feld ist kein impliziter Default, sondern ein Fehler (V2).

---

## Felddefinitionen

### 1 · `schema_version`

| | |
| --- | --- |
| **Typ** | String |
| **Pflicht** | **ja** |
| **Default** | — |
| **Erlaubte Werte** | derzeit ausschließlich `"1.0"` |
| **Datenschutzwirkung** | keine |
| **Validierung** | **V1** — nicht unterstützte Version **blockiert** die Aktivierung. Kein Fallback auf eine ältere Version |

### 2 · `mapping_id`

| | |
| --- | --- |
| **Typ** | String |
| **Pflicht** | **ja** |
| **Default** | — |
| **Erlaubte Werte** | stabile, ortsunabhängige Kennung |
| **Datenschutzwirkung** | **hoch** — darf **keinen** privaten Pfad, Hostnamen, Repository-Namen oder Benutzernamen enthalten |
| **Validierung** | **V4** — eindeutig je Deployment; **nie wiederverwendet**, auch nach Löschung nicht (V21) |

Die ID überlebt Umbenennung und Ortswechsel. Ein geänderter Ort erzeugt eine
neue **Revision**, keine neue ID.

### 3 · `slot_id`

| | |
| --- | --- |
| **Typ** | Enum |
| **Pflicht** | **ja** |
| **Default** | — |
| **Erlaubte Werte** | **ausschließlich** `PS-02`, `PS-03`, `PS-04` |
| **Datenschutzwirkung** | keine |
| **Validierung** | **V5** — jeder andere Wert blockiert. PS-01 und PS-05 brauchen kein Mapping; PS-06 und PS-07 sind `deferred` |

**Verpflichtendes Metadatum** (ADR-0008 Teil B): Provenienz, Ingest-Regeln,
Berechtigungen, Löschung und Audit folgen dem Slot.

### 4 · `mapping_name`

| | |
| --- | --- |
| **Typ** | String |
| **Pflicht** | **ja** |
| **Default** | — |
| **Erlaubte Werte** | sprechender Name für Operatoren |
| **Datenschutzwirkung** | **mittel** — kein Pfad, kein Hostname, kein Personenname |
| **Validierung** | nicht leer; keine Pfadsyntax |

### 5 · `source_boundary_type`

| | |
| --- | --- |
| **Typ** | Enum |
| **Pflicht** | **ja** |
| **Default** | — |
| **Erlaubte Werte** | `markdown-root`, `git-repository`, `handoff-root` |
| **Datenschutzwirkung** | keine |
| **Validierung** | **V6** — muss zum Slot passen: PS-02 → `markdown-root`, PS-03 → `git-repository`, PS-04 → `handoff-root`. Jede andere Kombination blockiert |

### 6 · `deployment_profile`

| | |
| --- | --- |
| **Typ** | Enum |
| **Pflicht** | **ja** |
| **Default** | — |
| **Erlaubte Werte** | `A`, `B`, `C`, `D`, `E` |
| **Datenschutzwirkung** | keine |
| **Validierung** | unbekanntes Profil blockiert |

### 7 · `operator_reference`

| | |
| --- | --- |
| **Typ** | String |
| **Pflicht** | **ja** |
| **Default** | — |
| **Erlaubte Werte** | **Rollen- oder Pseudonymkennung**, kein Klarname |
| **Datenschutzwirkung** | **hoch** — kein Personenname, keine E-Mail-Adresse, keine Organisationskennung |
| **Validierung** | nicht leer; keine E-Mail-Syntax |

### 8 · `location_reference`

| | |
| --- | --- |
| **Typ** | String |
| **Pflicht** | **ja** |
| **Default** | — |
| **Erlaubte Werte** | Ortsangabe der Source Boundary |
| **Datenschutzwirkung** | **höchste im Schema** |
| **Validierung** | **V7** — **ausschließlich im privaten Operator-Workspace gespeichert.** Ein realer Wert im Core-Repository ist ein **Blocker** und löst Stop-Bedingung **SB-02** aus |

**Dieses Feld ist der Grund für ADR-0007.** Im Core-Repository erscheint es nur
mit **synthetischen Platzhaltern**.

### 9 · `location_reference_type`

| | |
| --- | --- |
| **Typ** | Enum |
| **Pflicht** | **ja** |
| **Default** | — |
| **Erlaubte Werte** | `local-directory`, `mounted-volume`, `git-remote`, `git-local-clone` |
| **Datenschutzwirkung** | gering — benennt die **Art**, nicht den Ort |
| **Validierung** | muss zu `source_boundary_type` passen: `markdown-root` und `handoff-root` → `local-directory` oder `mounted-volume`; `git-repository` → `git-remote` oder `git-local-clone` |

### 10 · `collection`

| | |
| --- | --- |
| **Typ** | String |
| **Pflicht** | **ja** |
| **Default** | — |
| **Erlaubte Werte** | fachliche Collection nach **Projekt oder Domäne** |
| **Datenschutzwirkung** | **mittel** — Name kann fachlichen Kontext preisgeben |
| **Validierung** | **V15** — nicht leer; **verleiht keine Autorität, keine Datenklasse und keine AI-Transfer-Freigabe** (Grundsatz M-B) |

### 11 · `project`

| | |
| --- | --- |
| **Typ** | String |
| **Pflicht** | **ja** |
| **Default** | — |
| **Erlaubte Werte** | fachliche Projektzuordnung |
| **Datenschutzwirkung** | mittel |
| **Validierung** | nicht leer |

### 12 · `enabled`

| | |
| --- | --- |
| **Typ** | Boolean |
| **Pflicht** | **ja** |
| **Default** | **`false`** |
| **Erlaubte Werte** | `true`, `false` |
| **Datenschutzwirkung** | **hoch** — `true` bedeutet aktive Anbindung |
| **Validierung** | **V24** — `true` **nur** nach vollständigem Aktivierungsgate. Jede Lücke setzt auf `false` zurück |

**Ein neues Mapping tut nichts.** Aktivierung ist ein getrennter, kontrollierter
Vorgang.

### 13 · `read_only`

| | |
| --- | --- |
| **Typ** | Boolean |
| **Pflicht** | **ja** |
| **Default** | **`true`** |
| **Erlaubte Werte** | `true`, `false` |
| **Datenschutzwirkung** | **hoch** |
| **Validierung** | **V11** — `false` erfordert eine **benennbare A0-Entscheidung**; ohne diese blockiert das Mapping |

### 14 · `allowed_subpaths`

| | |
| --- | --- |
| **Typ** | Sequenz von Strings |
| **Pflicht** | **ja** |
| **Default** | **`[]`** |
| **Erlaubte Werte** | relative Unterpfade innerhalb der Source Boundary |
| **Datenschutzwirkung** | **hoch** — Aufnahmeumfang |
| **Validierung** | **V12** — **leer nimmt nichts auf.** Eine leere Allowlist blockiert die **Aktivierung**, erlaubt aber nicht etwa alles |

**Die wichtigste Vorgabe des Schemas.** Ein leerer Filter, der „alles" bedeutet,
ist die häufigste Ursache für unbeabsichtigten Ingest.

### 15 · `excluded_subpaths`

| | |
| --- | --- |
| **Typ** | Sequenz von Strings |
| **Pflicht** | **ja** |
| **Default** | `[]` |
| **Erlaubte Werte** | relative Unterpfade |
| **Datenschutzwirkung** | **hoch** |
| **Validierung** | **V13** — **gewinnt immer gegen `allowed_subpaths`.** Bei Überschneidung wird ausgeschlossen |

### 16 · `follow_symlinks`

| | |
| --- | --- |
| **Typ** | Boolean |
| **Pflicht** | **ja** |
| **Default** | **`false`** |
| **Erlaubte Werte** | `true`, `false` |
| **Datenschutzwirkung** | **hoch** — ein Symlink kann aus der Source Boundary herausführen |
| **Validierung** | **V14** — `true` erfordert eine benennbare Begründung; Ziele außerhalb der Boundary blockieren stets |

### 17 · `data_class`

| | |
| --- | --- |
| **Typ** | Enum |
| **Pflicht** | **ja** |
| **Default** | **`unknown`** |
| **Erlaubte Werte** | `public`, `internal`, `confidential`, `excluded-from-ai`, `unknown` — **niemals `secret`** |
| **Datenschutzwirkung** | **höchste im Schema neben Feld 8** |
| **Validierung** | **V9** — `unknown` wird **fail-closed** behandelt: wie `excluded-from-ai`, **nicht** wie `internal`. `secret` ist unzulässig und ein **Blocker** |

**`unknown` blockiert die Aktivierung.** Es ist ein Ausgangszustand, kein
Betriebszustand.

### 18 · `ai_transfer_policy`

| | |
| --- | --- |
| **Typ** | Enum |
| **Pflicht** | **ja** |
| **Default** | **`forbidden`** |
| **Erlaubte Werte** | `allowed`, `restricted`, `forbidden` |
| **Datenschutzwirkung** | **höchste** |
| **Validierung** | **V10** — `data_class: excluded-from-ai` **erzwingt** `forbidden`. `data_class: unknown` erzwingt `forbidden`. Jede andere Kombination wird **abgelehnt, nicht korrigiert** |

Eine stille Korrektur würde verbergen, dass jemand die Regel nicht verstanden
hat.

### 19 · `local_search_policy`

| | |
| --- | --- |
| **Typ** | Enum |
| **Pflicht** | **ja** |
| **Default** | `forbidden` |
| **Erlaubte Werte** | `allowed`, `metadata-only`, `forbidden` |
| **Datenschutzwirkung** | mittel — lokale Suche verlässt das System nicht |
| **Validierung** | `data_class: unknown` erzwingt `forbidden` |

### 20 · `indexing_policy`

| | |
| --- | --- |
| **Typ** | Enum |
| **Pflicht** | **ja** |
| **Default** | **`none`** |
| **Erlaubte Werte** | `none`, `metadata-only`, `full` |
| **Datenschutzwirkung** | **hoch** |
| **Validierung** | `none` bei `enabled: false`; `unknown` oder `excluded-from-ai` erlauben höchstens `metadata-only` |

### 21 · `mobile_visibility`

| | |
| --- | --- |
| **Typ** | Enum |
| **Pflicht** | **ja** |
| **Default** | **`forbidden`** |
| **Erlaubte Werte** | `allowed`, `authorized-only`, `forbidden` |
| **Datenschutzwirkung** | **hoch** |
| **Validierung** | `unknown` oder `excluded-from-ai` erzwingen `forbidden` |

### 22 · `revision_strategy`

| | |
| --- | --- |
| **Typ** | Enum |
| **Pflicht** | **ja** |
| **Default** | — |
| **Erlaubte Werte** | `content-hash`, `git-commit`, `handoff-revision` |
| **Datenschutzwirkung** | keine |
| **Validierung** | **V16** — muss zum Slot passen: PS-02 → `content-hash`; PS-03 → `git-commit`; PS-04 → `content-hash` oder `handoff-revision` |

### 23 · `deletion_behavior`

| | |
| --- | --- |
| **Typ** | Enum |
| **Pflicht** | **ja** |
| **Default** | `tombstone-and-cleanup` |
| **Erlaubte Werte** | `tombstone-and-cleanup`, `tombstone-only` |
| **Datenschutzwirkung** | **hoch** |
| **Validierung** | `tombstone-only` erfordert eine benennbare Begründung; abgeleitete Daten bleiben sonst bestehen |

### 24 · `verification_status`

| | |
| --- | --- |
| **Typ** | Enum |
| **Pflicht** | **ja** |
| **Default** | **`unverified`** |
| **Erlaubte Werte** | `unverified`, `verified`, `failed` |
| **Datenschutzwirkung** | mittel |
| **Validierung** | **V18** — `verified` nur nach bestandener technischer Verifikation (V19, V20). **Maschinell gesetzt zulässig** — im Gegensatz zu Feld 25 |

### 25 · `approval_status`

| | |
| --- | --- |
| **Typ** | Enum |
| **Pflicht** | **ja** |
| **Default** | **`not-approved`** |
| **Erlaubte Werte** | `not-approved`, `review-required`, `approved`, `revoked` |
| **Datenschutzwirkung** | **hoch** |
| **Validierung** | **V17** — `approved` setzt **ausschließlich ein Mensch**. Maschinell gesetztes `approved` ist ungültig |

### 26 · `approved_by`

| | |
| --- | --- |
| **Typ** | String oder `null` |
| **Pflicht** | ja (darf `null` sein) |
| **Default** | `null` |
| **Erlaubte Werte** | Rollenkennung, **kein Klarname** |
| **Datenschutzwirkung** | **hoch** |
| **Validierung** | Pflicht bei `approval_status: approved`; `null` in jedem anderen Zustand |

### 27 · `approved_at`

| | |
| --- | --- |
| **Typ** | String oder `null` |
| **Pflicht** | ja (darf `null` sein) |
| **Default** | `null` |
| **Erlaubte Werte** | **explizit quotierter** Datums-String, `YYYY-MM-DD` |
| **Datenschutzwirkung** | gering |
| **Validierung** | Pflicht bei `approved`. **Muss quotiert sein** — implizite Datumswerte sind im YAML-Subset unzulässig |

### 28 · `mapping_revision`

| | |
| --- | --- |
| **Typ** | Integer |
| **Pflicht** | **ja** |
| **Default** | `1` |
| **Erlaubte Werte** | ganzzahlig, ≥ 1, **explizit dezimal** |
| **Datenschutzwirkung** | keine |
| **Validierung** | **V16, V22** — jede inhaltliche Änderung erhöht die Revision. Kein aktiver Vorgänger derselben Revision |

### 29 · `previous_revision`

| | |
| --- | --- |
| **Typ** | Integer oder `null` |
| **Pflicht** | ja (darf `null` sein) |
| **Default** | `null` |
| **Erlaubte Werte** | ganzzahlig, ≥ 1 |
| **Datenschutzwirkung** | keine |
| **Validierung** | `null` nur bei `mapping_revision: 1`; sonst lückenlose Kette |

### 30 · `credential_reference`

| | |
| --- | --- |
| **Typ** | String oder `null` |
| **Pflicht** | **nein** |
| **Default** | `null` |
| **Erlaubte Werte** | **vollständig opake** Kennung |
| **Datenschutzwirkung** | **höchste Missbrauchsgefahr** |
| **Validierung** | **V8, V23** — enthält **niemals** einen Secret-Wert, kein Fragment, kein Passwort, kein Token. Ein Fund ist ein **Blocker** und löst **SB-02** aus |

> **OD-34 bleibt offen.** Dieses Schema legt **kein** Provider-, URI- oder
> Namensschema für Secrets fest. Die Kennung ist opak: Sie verweist, ohne zu
> verraten, worauf.

### 31 · `notes`

| | |
| --- | --- |
| **Typ** | String oder `null` |
| **Pflicht** | **nein** |
| **Default** | `null` |
| **Erlaubte Werte** | Freitext für Operatoren |
| **Datenschutzwirkung** | **hoch — häufigster Leckagepfad** |
| **Validierung** | **V8** — darf **keine Secrets**, keine `excluded-from-ai`-Inhalte, keine realen Pfade und keine Personennamen enthalten |

**Freitextfelder sind der Ort, an dem Regeln umgangen werden.** `notes`
unterliegt derselben Secret-Prüfung wie jedes andere Feld.

---

## Fail-closed-Übersicht

| Feld | Default | Wirkung |
| --- | --- | --- |
| `enabled` | **`false`** | Ein neues Mapping tut nichts |
| `read_only` | **`true`** | Schreiben ist die Ausnahme |
| `allowed_subpaths` | **`[]`** | Nimmt **nichts** auf |
| `follow_symlinks` | **`false`** | Kein Ausbruch aus der Boundary |
| `data_class` | **`unknown`** | Erzwingt bewusste Zuweisung; blockiert Aktivierung |
| `ai_transfer_policy` | **`forbidden`** | Übertragung wird gewährt, nicht angenommen |
| `local_search_policy` | `forbidden` | Suche wird gewährt |
| `indexing_policy` | **`none`** | Nichts wird versehentlich indexiert |
| `mobile_visibility` | **`forbidden`** | Mobile Sichtbarkeit ist eine Entscheidung |
| `verification_status` | **`unverified`** | Ausgangszustand ist ungeprüft |
| `approval_status` | **`not-approved`** | Ausgangszustand ist nicht freigegeben |
| `credential_reference` | `null` | Kein Mapping bringt implizit Zugang mit |

### Was restriktive Defaults leisten — und was nicht

**Restriktive Defaults erzeugen keine operative Wirkung. Sie ersetzen aber
keine verpflichtenden Mappingwerte.**

| Aussage | Gilt |
| --- | --- |
| Ein Mapping ist **schema-valid** nur dann, wenn **alle** verpflichtenden Identitäts-, Boundary-, Location-, Collection-, Revisions- und sonstigen Pflichtwerte vorhanden **und gültig** sind | **ja** |
| Ein Dokument, in dem nur Defaults stehen und Pflichtwerte fehlen, ist schema-valid | **nein** — V2 verweigert |
| Ein schema-valides Mapping mit restriktiven Defaults ist wirkungslos | **ja** |
| Ein schema-valides Mapping ist damit security-checked, source-verified, approved, enabled oder ingestfähig | **nein** |

**Bleiben die steuernden Felder auf ihren restriktiven Defaults**, ist das
Mapping auch nach erreichter Schema-Validität weiterhin **nicht
security-checked, nicht source-verified, nicht approved, nicht enabled und
nicht ingestfähig**.

| Default | Zulässig als Schemawert | Blockiert |
| --- | --- | --- |
| `data_class: unknown` | **ja** — definierter Schemawert | **Security Check, Approval und Aktivierung** (V9); Behandlung fail-closed wie `excluded-from-ai` |
| `allowed_subpaths: []` | **ja** — zulässiger restriktiver Default | **nimmt keine Inhalte auf**; blockiert Source Verification und Aktivierung (V12) |
| `enabled: false` | ja | **erzeugt keine Aufnahme in Ingest oder Retrieval** |
| `approval_status: not-approved` | ja | **ist keine Freigabe** |
| `verification_status: unverified` | ja | **ist kein technischer Nachweis** |
| `ai_transfer_policy: forbidden` | ja | **erlaubt keine externe Übertragung** |
| `indexing_policy: none` | ja | **erlaubt keine Indexierung** |

> **Präzisierung gegenüber der Erstfassung (Nova-REWORK, 2026-07-21):** Die
> frühere Formulierung „ein vollständig mit Defaults ausgefülltes Mapping ist
> gültig und wirkungslos" trennte **Vorlage**, **Schema-Validität** und
> **operative Freigabe** nicht ausreichend. Sie hätte so gelesen werden können,
> als sei ein Dokument ohne Pflichtwerte bereits gültig. **Fehlende
> Pflichtwerte verhindern Schema-Validität.**

Vollständige Stufenfolge in
[PILOT_SOURCE_MAPPING_SPECIFICATION.md](PILOT_SOURCE_MAPPING_SPECIFICATION.md),
Abschnitt „Validitätsstufen".

---

## Formatregeln — YAML 1.2 Strict Subset

Verbindlich aus **ADR-0008 Teil A**.

### Erlaubt

| Konstrukt | Verwendung |
| --- | --- |
| Mappings | Feldstruktur |
| Sequenzen | `allowed_subpaths`, `excluded_subpaths` |
| Strings | Textfelder — Datumswerte **explizit quotiert** |
| Booleans | ausschließlich `true` und `false` |
| `null` | leere optionale Felder |
| Integer | **nur** `mapping_revision` und `previous_revision`, explizit dezimal |

### Nicht erlaubt

| Konstrukt | Grund |
| --- | --- |
| Benutzerdefinierte Tags | parserabhängige Semantik |
| Anchors | Wiederverwendung verschleiert den Inhalt |
| Aliases | dasselbe |
| Merge Keys | implizite Vererbung |
| Ausführbare Typen | Codeausführung beim Parsen |
| Implizite Datumswerte | parserabhängige Interpretation |
| Nicht eindeutige numerische Schreibweisen | Oktal, Hex, `1_000`, Sexagesimal |
| **Doppelte Schlüssel** | letzter gewinnt — je nach Parser |
| Mehrere Dokumente je Datei | Mehrdeutigkeit, welches gilt |

### Zusätzliche Regeln

| # | Regel |
| --- | --- |
| **F1** | **UTF-8** |
| **F2** | **Genau ein Mapping-Dokument je Datei** |
| **F3** | **Keine Tabulatoren** zur Einrückung |
| **F4** | Der Parser **muss doppelte Schlüssel ablehnen** — nicht überschreiben |
| **F5** | **Unbekannte Felder blockieren die Aktivierung** (V3) |
| **F6** | `schema_version` muss unterstützt sein (V1) |
| **F7** | Die Serialisierung muss **deterministisch normalisierbar** sein |

**Zu F7:** Zwei Läufe über dasselbe Mapping müssen dieselbe Normalform
erzeugen. Ohne diese Eigenschaft ist kein stabiler Hash und kein
reproduzierbarer Vergleich möglich.

**JSON Schema ist die maschinenprüfbare Vertragsgrenze.** YAML ist die
Eingabeform, JSON Schema der Vertrag.

> **In diesem Work Package wurde keine Schema-Datei erstellt** — weder JSON
> noch YAML. Es existiert nur diese Markdown-Spezifikation.

## Abgrenzung

| Dieses Dokument | Nicht dieses Dokument |
| --- | --- |
| Feldmodell und Wertebereiche | Ausführbares JSON Schema |
| Formatregeln | Parser oder Validator |
| Datenschutzwirkung je Feld | Konkrete Werte einer Installation |
| Validierungsverweise | Validierungscode |

## Status

**ACCEPTED FOR IMPLEMENTATION PLANNING.** **Es existiert kein Mapping.** Kein
Slot ist aktiviert, keine Quelle angebunden, kein Ingest ausgeführt, kein
Validator geschrieben.

**Implementierung erlaubt: nein.**
