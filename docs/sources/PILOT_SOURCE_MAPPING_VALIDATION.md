# Pilot Source Mapping Validation — 24 Regeln

| Feld | Wert |
| --- | --- |
| **Status** | **ACCEPTED FOR IMPLEMENTATION PLANNING** |
| **Nicht** | IMPLEMENTED · ACTIVE |
| Grundlage | **ADR-0008** (A1), [Schema](PILOT_SOURCE_MAPPING_SCHEMA.md), [Specification](PILOT_SOURCE_MAPPING_SPECIFICATION.md) |
| Erfasst in | CBP-WP-010 |
| Autoritätsklasse | A2 |
| Stand | 2026-07-21 |

Dieses Dokument beschreibt, **was ein Validator prüfen muss**. **Es existiert
kein Validator**, kein Parser und kein JSON Schema als Datei.

---

## Grundsatz — fail-closed

| # | Regel |
| --- | --- |
| **FC-1** | **Jeder unbekannte Zustand blockiert** |
| **FC-2** | **Jeder Konflikt blockiert** |
| **FC-3** | **Fehlende Evidenz blockiert** |
| **FC-4** | Bei Widerspruch gewinnt die **restriktivere** Regel |
| **FC-5** | **Eine Warnung hebt niemals automatisch eine Blockade auf** |

**Zu FC-5:** Eine Warnung, die sich selbst quittiert, ist keine Warnung. Nur ein
Mensch oder eine bestandene Prüfung hebt eine Blockade auf — nie der Zeitablauf,
nie ein Wiederholungsversuch, nie ein „force"-Schalter.

**Der Normalzustand ist Verweigerung.** Eine Lücke wird nie zugunsten der
Verfügbarkeit ausgelegt.

---

## Fehlerklassen und Schweregrade

| Klasse | Kennung | Bedeutung | Wirkung |
| --- | --- | --- | --- |
| **Format** | `FMT` | YAML-Subset verletzt | blockiert Parsing |
| **Schema** | `SCH` | Feld, Typ oder Wertebereich verletzt | blockiert Validierung |
| **Sicherheit** | `SEC` | Secret, Rechte, Symlink, Credential | **blockiert und eskaliert** |
| **Datenschutz** | `PRI` | Datenklasse, AI-Transfer, Sichtbarkeit | **blockiert und eskaliert** |
| **Konsistenz** | `CON` | Revision, Tombstone, Vorgänger | blockiert Aktivierung |
| **Freigabe** | `APP` | Verifikation, Approval, Gate | blockiert Aktivierung |
| **Erreichbarkeit** | `SRC` | Quelle nicht lesbar | blockiert Aktivierung |

| Schweregrad | Bedeutung | Verhalten |
| --- | --- | --- |
| **`blocker`** | Verstoß gegen eine Sicherheits- oder Datenschutzgrenze | Verarbeitung **anhalten**, Stop-Bedingung auslösen |
| **`error`** | Regelverstoß ohne unmittelbare Gefährdung | Aktivierung verweigert |
| **`warning`** | Auffälligkeit ohne Regelverstoß | **hebt keine Blockade auf** (FC-5) |
| **`info`** | Hinweis | keine Wirkung |

## Ergebniswerte

| Wert | Bedeutung |
| --- | --- |
| `not-evaluated` | Prüfung nicht durchgeführt |
| `pass` | Regel erfüllt |
| `fail` | Regel verletzt — Aktivierung ausgeschlossen |
| **`blocked`** | **Sicherheits- oder Datenschutzverstoß** — Verarbeitung anhalten |
| `human-review-required` | Nur ein Mensch kann entscheiden |

**Ein Mapping ist nur dann aktivierbar, wenn alle 24 Regeln `pass` tragen.** Ein
einziges `not-evaluated` genügt zur Verweigerung (FC-3).

---

## Die 24 Regeln

| # | Regel | Klasse | Schweregrad bei Verstoß | Ergebnis |
| --- | --- | --- | --- | --- |
| **V1** | **Schema-Version unterstützt** — `schema_version` ist ein bekannter Wert; **kein Fallback** auf eine ältere Version | `SCH` | `error` | `fail` |
| **V2** | **Alle Pflichtfelder vorhanden** — 29 Pflichtfelder, auch wenn sie ihren Default tragen | `SCH` | `error` | `fail` |
| **V3** | **Keine unbekannten Felder** — ein unbekanntes Feld blockiert die Aktivierung, es wird **nicht ignoriert** | `SCH` | `error` | `fail` |
| **V4** | **`mapping_id` gültig und stabil** — eindeutig je Deployment, ohne Pfad-, Host- oder Personenbestandteile | `SCH` | `error` | `fail` |
| **V5** | **Slot zulässig** — `slot_id` ist `PS-02`, `PS-03` oder `PS-04` | `SCH` | `error` | `fail` |
| **V6** | **Source Boundary entspricht dem Slot** — PS-02 → `markdown-root`, PS-03 → `git-repository`, PS-04 → `handoff-root` | `CON` | `error` | `fail` |
| **V7** | **Location Reference vorhanden, aber nicht im Core** — gesetzt, und der reale Wert liegt **ausschließlich** im privaten Operator-Workspace | `SEC` | **`blocker`** | **`blocked`** |
| **V8** | **Keine Secrets** — in keinem Feld, insbesondere nicht in `notes` und `credential_reference` | `SEC` | **`blocker`** | **`blocked`** |
| **V9** | **Datenklasse bekannt** — `data_class` ist nicht `unknown` und nicht `secret` | `PRI` | **`blocker`** | **`blocked`** |
| **V10** | **AI-Transfer-Regel kompatibel** — `excluded-from-ai` und `unknown` erzwingen `forbidden`; abweichende Kombination wird **abgelehnt, nicht korrigiert** | `PRI` | **`blocker`** | **`blocked`** |
| **V11** | **`read_only`-Grenze eingehalten** — `false` nur mit benennbarer A0-Entscheidung | `SEC` | **`blocker`** | **`blocked`** |
| **V12** | **Subpath-Allowlist nicht leer vor Aktivierung** — leere Allowlist nimmt **nichts** auf und blockiert `enabled` | `SEC` | `error` | `fail` |
| **V13** | **Ausschlüsse überschreiben Einschlüsse** — bei Überschneidung wird ausgeschlossen | `SEC` | `error` | `fail` |
| **V14** | **Symlink-Regel eingehalten** — `follow_symlinks: false` als Vorgabe; Ziele außerhalb der Boundary blockieren **immer** | `SEC` | **`blocker`** | **`blocked`** |
| **V15** | **Collection zulässig** — gesetzt und nicht leer; **verleiht keine Autorität, Datenklasse oder AI-Transfer-Freigabe** | `SCH` | `error` | `fail` |
| **V16** | **Revision vollständig** — `mapping_revision` ≥ 1, `previous_revision` lückenlos, `revision_strategy` slotkonform | `CON` | `error` | `fail` |
| **V17** | **Human Approval vorhanden** — `approval_status: approved` mit `approved_by` und `approved_at`; **maschinell gesetztes `approved` ist ungültig** | `APP` | `error` | `human-review-required` |
| **V18** | **Technische Verifikation bestanden** — `verification_status: verified` auf Basis von V19 und V20 | `APP` | `error` | `fail` |
| **V19** | **Quelle erreichbar** — die Source Boundary existiert und ist lesbar | `SRC` | `error` | `fail` |
| **V20** | **Minimale Rechte nachgewiesen** — kein Schreibrecht über das Nötige hinaus; bei PS-03 kein Push- oder Schreibrecht | `SEC` | **`blocker`** | **`blocked`** |
| **V21** | **Tombstone-Konflikt ausgeschlossen** — die `mapping_id` wurde nie gelöscht; eine getombsteinte ID ist **nie wiederverwendbar** | `CON` | `error` | `fail` |
| **V22** | **Kein aktiver Vorgänger derselben Revision** — höchstens eine aktive Fassung je `mapping_id` | `CON` | `error` | `fail` |
| **V23** | **Credential Reference enthält keinen Wert** — vollständig opak; kein Passwort, Token oder Fragment | `SEC` | **`blocker`** | **`blocked`** |
| **V24** | **Aktivierungsgate vollständig** — alle 20 Gate-Punkte erfüllt; jede Lücke setzt `enabled` auf `false` | `APP` | `error` | `fail` |

### Blockerregeln — ausgezählt

**Genau acht der 24 Regeln tragen `blocker`.** Die Zahl ist aus der Tabelle
oben ausgezählt, nicht fortgeschrieben (Zählregel 1).

| # | Regel | Klasse | Blockadewirkung |
| --- | --- | --- | --- |
| 1 | **V7** | `SEC` | Location Reference im Core → Verarbeitung anhalten, **SB-02** |
| 2 | **V8** | `SEC` | Secretfund in einem beliebigen Feld → Incident-Verfahren, **SB-02** |
| 3 | **V9** | `PRI` | Datenklasse `unknown` oder `secret` → Security Check, Approval und Aktivierung blockiert |
| 4 | **V10** | `PRI` | Unzulässige Kombination aus `data_class` und `ai_transfer_policy` → **abgelehnt statt korrigiert** |
| 5 | **V11** | `SEC` | `read_only: false` ohne benennbare A0-Entscheidung → Aktivierung blockiert |
| 6 | **V14** | `SEC` | Symlinkziel außerhalb der Source Boundary → Verarbeitung anhalten |
| 7 | **V20** | `SEC` | Rechte über das Nötige hinaus, bei PS-03 Push- oder Schreibrecht → Aktivierung blockiert |
| 8 | **V23** | `SEC` | `credential_reference` enthält einen Wert statt einer opaken Kennung → **SB-02** |

**Verteilung:** sechs `SEC`, zwei `PRI`. Die übrigen 16 Regeln tragen `error`
und verweigern die Aktivierung, halten aber nicht die Verarbeitung an.

**Blocker halten die Verarbeitung an, nicht nur die Aktivierung.** Das ist der
Unterschied zu `error`.

---

## Zuordnung zu Validitätsstufen und Zuständen

Die 24 Regeln verteilen sich auf die sieben **Validitätsstufen** aus der
[Spezifikation](PILOT_SOURCE_MAPPING_SPECIFICATION.md). Jede Stufe hat ihre
eigenen Regeln; **keine Stufe impliziert die nächste.**

| Stufe | Regeln | Persistierter Zustand |
| --- | --- | --- |
| **1 Template** | — | **keiner** — eine Vorlage ist kein Mapping |
| **2 Parsed** | Formatregeln F1–F7 | **keiner** — reiner Verarbeitungsbegriff |
| **3 Schema-valid** | V1–V6, V15, V16 | `schema-valid` |
| **4 Security-checked** | **V7, V8, V9, V10, V11, V14, V20, V23** — die acht Blocker — sowie V12, V13 | `security-checked` |
| **5 Source-verified** | V18, V19 | `source-verified` |
| **6 Approved** | **V17** | `review-required` → `approved` |
| **7 Enabled** | **V24** plus V21, V22 | `enabled` |

| # | Regel |
| --- | --- |
| **P1** | **`parsed` ist kein persistierter Zustand.** Er beschreibt einen Verarbeitungsschritt vor `schema-valid` und wird nicht gespeichert |
| **P2** | Eine **Template** erreicht ohne Pflichtwerte nicht einmal Stufe 3 — **V2** verweigert |
| **P3** | **Alle acht Blocker liegen auf Stufe 4.** Sie werden **vor** jeder Quellenberührung geprüft |
| **P4** | Stufe 6 setzt ausschließlich ein Mensch (V17) |
| **P5** | Stufe 7 erfordert einen **getrennten kontrollierten Vorgang** (V24, Z13) |

## Prüfreihenfolge

Die Reihenfolge ist bindend: Eine spätere Regel wird erst geprüft, wenn die
früheren `pass` tragen.

| Stufe | Regeln | Grund |
| --- | --- | --- |
| **1 · Format** | Parsing, F1–F7 | Ohne eindeutiges Parsing ist kein Feld verlässlich |
| **2 · Schema** | V1–V6, V15, V16 | Struktur vor Inhalt |
| **3 · Sicherheit** | **V7, V8, V11, V14, V20, V23** | **vor jeder Quellenberührung** |
| **4 · Datenschutz** | V9, V10, V12, V13 | vor jeder Indexierung |
| **5 · Quelle** | V19, V18 | erst jetzt wird die Quelle berührt |
| **6 · Konsistenz** | V21, V22 | Tombstones und Vorgänger |
| **7 · Freigabe** | V17, V24 | zuletzt, menschlich |

**Stufe 3 vor Stufe 5 ist die wichtigste Anordnung.** Ein Mapping mit einem
Secret oder einem Symlink aus der Boundary heraus darf die Quelle gar nicht
erst berühren.

---

## Operatorhinweise

Bei einem Fehler nennt der Validator: **Regel · Klasse · Schweregrad · Feld ·
was zu tun ist**. Er nennt **nicht** den beanstandeten Wert, wenn dieser ein
Secret oder eine Location Reference sein könnte.

| Situation | Hinweis an den Operator |
| --- | --- |
| V3 unbekanntes Feld | Feldname nennen; auf `schema_version` prüfen |
| V8 Secretverdacht | **Wert nicht ausgeben**; Incident-Verfahren |
| V9 `unknown` | Datenklasse bestimmen und menschlich bestätigen |
| V10 Konflikt | Kombination nennen; **keine automatische Korrektur anbieten** |
| V12 leere Allowlist | Erklären, dass leer **nichts** aufnimmt |
| V17 fehlende Freigabe | An den Human Maintainer verweisen |
| V19 nicht erreichbar | Erreichbarkeit prüfen; **keinen Pfad ausgeben** |

## Human-Review-Punkte

Vier Punkte sind **ausschließlich** menschlich zu entscheiden:

| # | Punkt | Regel |
| --- | --- | --- |
| 1 | **Freigabe des Mappings** | V17 |
| 2 | **Bestätigung der Datenklasse** | V9 |
| 3 | **Begründung für `read_only: false`** | V11 |
| 4 | **Aktivierungsentscheidung** | V24 |

Zusätzlich menschlich: eine Begründung für `follow_symlinks: true` (V14) und
für `deletion_behavior: tombstone-only`.

## Spätere Negativtests

Zu erbringen in **CBP-WP-013**. Ein Negativtest gilt nur als bestanden, wenn die
Aktivierung **tatsächlich scheitert** — nicht, wenn eine Warnung erscheint.

| # | Test | Erwartung | Regel |
| --- | --- | --- | --- |
| **NT-01** | Unbekanntes Feld | Aktivierung blockiert | V3 |
| **NT-02** | Nicht unterstützte `schema_version` | blockiert, **kein Fallback** | V1 |
| **NT-03** | Doppelter Schlüssel im YAML | Parser **lehnt ab** | F4 |
| **NT-04** | Anchor oder Alias | Parser lehnt ab | Formatregeln |
| **NT-05** | **Synthetisches Secret-Muster in `notes`** | **`blocked`**, Incident-Verfahren | V8 |
| **NT-06** | `credential_reference` mit Wert statt Kennung | **`blocked`** | V23 |
| **NT-07** | `data_class: unknown` bei Aktivierung | blockiert | V9 |
| **NT-08** | `excluded-from-ai` mit `ai_transfer_policy: allowed` | **abgelehnt**, nicht korrigiert | V10 |
| **NT-09** | Leere `allowed_subpaths` bei Aktivierung | blockiert | V12 |
| **NT-10** | Pfad in beiden Listen | **ausgeschlossen** | V13 |
| **NT-11** | Symlink aus der Boundary heraus | **`blocked`** | V14 |
| **NT-12** | `enabled: true` ohne Approval | auf `false` zurückgesetzt | V17, V24 |
| **NT-13** | Maschinell gesetztes `approved` | ungültig | V17 |
| **NT-14** | Wiederverwendete getombsteinte `mapping_id` | blockiert | V21 |
| **NT-15** | Zwei aktive Fassungen derselben ID | blockiert | V22 |
| **NT-16** | Mehrere Source Boundaries in einem Mapping | blockiert | V6, C1 |
| **NT-17** | Schreibversuch bei `read_only: true` | scheitert | V20 |
| **NT-18** | Warnung soll Blockade aufheben | **wirkungslos** | FC-5 |

**NT-05 ausdrücklich:** Der Test verwendet ein **erkennbares Muster ohne realen
Geheimwert**. Es wird kein Secret erzeugt, um eine Secret-Erkennung zu prüfen.

**NT-18 prüft die Regel selbst** — dass sich das System nicht durch eine
Quittierung freischalten lässt.

## Status

**Es existiert kein Validator.** Keine dieser 24 Regeln ist implementiert,
keiner der 18 Negativtests ausgeführt. Sämtliche Nachweise stehen auf **Stufe 1
`dokumentiert`**.

**Implementierung erlaubt: nein.**
