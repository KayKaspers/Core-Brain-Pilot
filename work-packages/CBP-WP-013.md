# CBP-WP-013 — Ingest Quarantine Minimum Viable Pipeline

| Feld | Wert |
| --- | --- |
| ID | CBP-WP-013 |
| Titel | Ingest Quarantine Minimum Viable Pipeline |
| Typ | **implementation**, interactive authorization |
| Prompt Mode | **Full** (NDF v1.0.0) |
| Context Budget | **B2 – Standard** |
| Claude Code Model | **Claude Opus 4.8** (`claude-opus-4-8`) — A0-Modellsubstitution |
| Claude Code Effort | **ultracode** — im Profil deklariert |
| Phase | Phase 1 – zweite technische Umsetzung |
| Ausgeführt am | 2026-07-22 |
| Ablauf | **interaktiv**, zwei Phasen |
| Status | `in-review` |
| Autoritätsklasse | A2 |

> **Zweites Work Package mit technischer Wirkung.** Es entsteht ausführbarer,
> getesteter Code — ein lokaler, synthetisch testbarer, fail-closed
> Quarantäneprototyp **ohne** operative Wirkung. Keine reale Quelle, kein reales
> Mapping, kein produktiver Ingest, keine Indexierung.
>
> **Anmerkung zur Modellwahl:** Das Profil forderte Claude Fable 5. Da dieses
> Modell nicht verfügbar war, hat der Human Maintainer eine **A0-Substitution**
> auf Opus 4.8 (`claude-opus-4-8`) erteilt. Es wurde nicht stillschweigend
> gewechselt — die Ausführung stoppte zunächst mit `MODEL_UNAVAILABLE`.

---

## Human-Autorisierung

| Feld | Wert |
| --- | --- |
| Entscheidung | **APPROVE WP-013 IMPLEMENTATION WITH NOTES** |
| Autorität | **A0** |
| Datum | 2026-07-22 |

**Kern der Notes (eng normalisiert, nicht erweitert):** Autorisierung
ausschließlich für den lokalen, synthetisch testbaren, fail-closed
Quarantäneprototyp. Nur genau eine synthetische Markdown-Datei je Intake,
lokale strukturelle Prüfungen, deterministische Credential- und PII-Indikatoren,
ein content-addressed Store nur in temporären Testverzeichnissen außerhalb des
Core-Repositorys, minimierte Records, lokale CLI, Tests und Evidenz. **Nicht**
autorisiert: reale Quellen, reale Mappings, produktiver Ingest, Freigabe oder
Promotion, Collection-/Index-Erzeugung, Retrieval, Embeddings, externe
Übertragung, Netzwerkzugriff, Secret-Auflösung, RT-2-Speicherung, HTTP-API/Web
UI, Docker/Deployment, Gate-Ausführung. Jede Scan-/Stage-Operation muss die
Synthetic-only-Grenze technisch durchsetzen. Kein Status bedeutet `approved`,
`released`, `enabled`, `indexed` oder produktionsbereit. `quarantine release`
verweigert deterministisch. Kein Eingabepfad, Dateiname, Inhaltsauszug,
Secret-artiger Wert oder personenbezogener Testinhalt erscheint in Manifest,
CLI-Ausgabe oder Report.

## Vier Teilentscheidungen (A0)

| Teil | Entscheidung | Decision-ID |
| --- | --- | --- |
| A – Intake-Granularität | genau eine ausdrücklich angegebene Markdown-Datei je Intake | **D-038** |
| B – Quarantänespeicher | lokaler content-addressed Store, unveränderlicher Payload, atomares JSON-Manifest | **D-039** |
| C – Baseline-Scanner | strukturelle Prüfungen plus deterministische Credential- und PII-Indikatoren | **D-040** |
| D – Freigabemodell | drei Zustände, keine automatische Promotion | **D-041** |

Festgehalten in [ADR-0010](../docs/decisions/ADR-0010-ingest-quarantaene-mvp.md)
(`accepted`, A1). **OD-05 und OD-06 bleiben offen.** Neu geöffnet: **OD-37**
(produktive Isolation) und **OD-38** (produktive Erkennung).

## Ziel

Ein synthetisch testbarer, fail-closed Minimum-Viable-Prototyp der
Ingest-Quarantäne: strukturelle Validierung vor dem Lesen, deterministischer
Baseline-Scan, isolierte content-addressed Ablage, minimierte Records und
ausschließlich die Zustände `READY_FOR_HUMAN_REVIEW`, `REVIEW_REQUIRED`,
`BLOCKED` — **ohne** jede automatische Freigabe oder Promotion.

## Scope

- Quarantäne-Paket `core/core_brain/quarantine/` (6 Module).
- Beispiel-Policy, Beispiele, CLI-Kommandogruppe `quarantine`.
- Fünf neue Testmodule, erweiterter Netzwerk-Guard.
- Drei Runtime-Dokumente, ADR-0010, dieses Work-Package-Dokument.

## Out of Scope

Reale Quellen, reale Mappings, produktiver Ingest, Promotion, Indexierung,
Retrieval, Embeddings, externe Übertragung, Netzwerk-Egress, Secret-Auflösung,
RT-2-Speicherung, HTTP-API, Web UI, Docker, Deployment, Gate-Ausführung.

## Trust Boundary

Pre-Ingest (TB-1). Die **Synthetic-only-Grenze** ist technisch durchgesetzt:
Flag `--synthetic-test-only` **und** `synthetic:`-Präfix **und** Marker
`<!-- synthetic-test-only -->` sind Pflicht; fehlt eines, blockiert die
Operation ohne Speicherung.

## Module

| Modul | Inhalt |
| --- | --- |
| `quarantine/models.py` | Enums, Finding-Codes (`QF-*`), Policy-/Scan-/Record-Modelle |
| `quarantine/policy.py` | fail-closed Policy-Validierung |
| `quarantine/scanner.py` | strukturelle, Kodierungs-, Credential-, PII-Indikatoren |
| `quarantine/store.py` | content-addressed Store, atomar, idempotent, Kollision |
| `quarantine/pipeline.py` | Orchestrierung, Synthetic-Gate, einmaliges Lesen |
| `quarantine/__init__.py` | nebenwirkungsfreie Exporte |

## Policy

13 Pflichtfelder, fail-closed. Unbekanntes Feld, unbekannte Version, fehlendes
Feld, nicht positives/zu großes `max_bytes`, leere Suffixliste,
`release_enabled = true`, `network_enabled = true` → **blockiert**. Environment
und CLI überschreiben nichts. Keine frei konfigurierbaren regulären Ausdrücke.

## Scanner

Zehn blockierende und zwei Review-Befundcodes im `QF-`-Namensraum. Befunde
tragen Code, Schwere und optional eine Zeilennummer — **kein** Snippet,
**kein** Pfad, **kein** Wert. Credential- und Key-Muster werden in den Tests aus
sicheren Teilstücken zur Laufzeit zusammengesetzt.

## Store

`objects/sha256/<prefix>/<digest>.blob` und `records/<id>.json`. Objektpfade nur
aus validiertem SHA-256; Root außerhalb des Repositorys; atomare Schreibweise;
Idempotenz; Kollision blockiert; kein Schreiben außerhalb des Roots.

## Record

14 Felder, minimiert, ohne Pfad und ohne Inhalt. `source_reference` opak
(`synthetic:`). `quarantine_id` deterministisch abgeleitet. `created_at`
UTC-normalisiert und injizierbar.

## CLI

| Kommando | Wirkung | Exitcodes |
| --- | --- | --- |
| `quarantine scan` | liest und scannt, speichert nichts | 0 / 5 / 6 |
| `quarantine stage` | scannt und speichert, keine Promotion | 0 / 5 / 6 (BLOCKED speichert nichts) |
| `quarantine inspect` | minimierte Record-Metadaten | 0 / 6 |
| `quarantine release` | verweigert immer, ändert nichts | 7 |

Neue Exitcodes: **5** `QUARANTINE_REVIEW_REQUIRED`, **6** `QUARANTINE_BLOCKED`,
**7** `QUARANTINE_RELEASE_BLOCKED`. Exit 0 bedeutet ausschließlich: technisch
abgeschlossen, kein Baseline-Indikator — **nicht** `approved`, `released`,
`enabled`, `indexed` oder sicher für externe Übertragung.

## Zustände

`READY_FOR_HUMAN_REVIEW`, `REVIEW_REQUIRED`, `BLOCKED`. Kein Zustand erzeugt
automatisch Approval, Release, Mapping-Aktivierung, Registry-, Collection- oder
Index-Eintrag, Context Pack oder externen Transfer.

## Tests

| Kennzahl | Wert (aus dem Lauf) |
| --- | --- |
| **Ausgeführte Tests** | **137** |
| Bestanden | **137** · Fehlgeschlagen 0 · Fehler 0 · Übersprungen 0 |
| Befehl | `py -3.13 -m unittest discover -s tests -v` |
| Testbasislinie CBP-WP-012 | **69**, weiterhin grün |
| Neue Testmodule | 5 (policy, scanner, store, pipeline, cli) |
| Netzwerkzugriff | keiner — durch erweiterten Netzwerk-Guard belegt |
| Dateisystemwirkung | nur temporäre Testverzeichnisse |

**Zwei Testdefekte im ersten Lauf gefunden und behoben** (beide in Tests, nicht
im Code) — siehe Evidenz.

## Technische Evidenz

Vollständig in
[INGEST_QUARANTINE_EVIDENCE.md](../docs/runtime/INGEST_QUARANTINE_EVIDENCE.md).

| # | Kommando | Exitcode |
| --- | --- | ---: |
| 1 | `compileall core tests config` | 0 |
| 2 | `unittest discover -s tests` | 0 |
| 3 | `version` | 0 |
| 4 | `quarantine scan` (clean) | 0 |
| 5 | `quarantine scan` (E-Mail) | 5 |
| 6 | `quarantine scan` (kein Marker) | 6 |
| 7 | `quarantine scan --json` | 0 |
| 8 | `quarantine stage` (clean) | 0 |
| 9 | `quarantine inspect` | 0 |
| 10 | `quarantine release` | 7 |
| 11 | `run` | 4 |

Store: genau 1 Objekt + 1 Record; Cleanup vollständig (`temp_remains=False`).
Manifest ohne Pfad und Inhalt. Netzwerk-Guard über alle vier neuen CLI-Pfade.

## Stop-Bedingungen

Erfüllt: keine externe Abhängigkeit, kein Paketdownload, kein realer
Secret-Fund, keine realen personenbezogenen Daten, keine reale Source Boundary,
kein reales Mapping, kein Netzwerkversuch, keine Speicherung im Repository, kein
Schreiben außerhalb des temporären Stores, kein Symlink-Escape, kein Pfad- oder
Inhaltsleak, keine automatische Promotion, keine Index- oder Collection-Erzeugung,
kein fehlgeschlagener Test, keine unerwartete Datei, keine Änderung außerhalb der
Erlaubnisliste, keine Gate-Ausführung, kein Versuch CBP-WP-014 auszuführen.

## Akzeptanzkriterien

Alle erfüllt: Implementierung ausdrücklich autorisiert; A1/B1/C1/D1 gewählt;
ADR-0010 erstellt; ausführbarer synthetischer MVP; Policy strikt fail-closed;
Scanner/Store/Record/Pipeline testbar; Store content-addressed und außerhalb des
Repos; keine Pfade/Inhalte in Manifesten und Ausgaben; kein automatischer
Releasepfad; vollständige Testsuite grün; kein Netzwerk, keine reale Quelle;
keine Gate- oder Produktionsreife vorgetäuscht.

## Ergebnis

| Gegenstand | Wert |
| --- | --- |
| Neue Quarantäne-Module | **6** |
| Neue Testmodule / Gesamttests | **5 / 137** |
| **Testergebnis** | **137 bestanden, 0 fehlgeschlagen** |
| Neue CLI-Kommandos | **4** (`scan`, `stage`, `inspect`, `release`) |
| Neue Exitcodes | **3** (5, 6, 7) |
| Externe Abhängigkeiten | **0** |
| **Durchgesetzte KB-Kontrollen** | **0** — alle bleiben `DOCUMENTED ONLY` |
| Geschlossene Risiken | **0** — R-01, R-32, R-33 bleiben offen |
| Geschlossene Gates | **0** — alle bleiben `NOT EVALUATED` |
| Commit / Push | **nein / nein** |

## Rückmeldung an Nova

Der Quarantäne-MVP ist **lokal implementiert und getestet** — 137 Tests
bestanden, alle CLI-Smoke-Tests mit den erwarteten Exitcodes (0/5/6/7). **Es
wurde keine reale Quelle berührt, nichts aktiviert, nichts freigegeben und
nichts promotet.**

**Vier Punkte, die ich hervorhebe:**

1. **Ein `BLOCKED` oder `READY_FOR_HUMAN_REVIEW` ist keine Freigabe.** Die drei
   Zustände beschreiben ausschließlich das Ergebnis einer lokalen
   Baseline-Prüfung. `quarantine release` verweigert strukturell (Exit 7).

2. **Der Scanner ist ein Indikator, kein Kontrollsystem.** Er blockiert
   offensichtliche Credential- und Private-Key-Marker und kennzeichnet E-Mail-
   und Telefonindikatoren zur Human-Prüfung. **Keine** vollständige Secret- oder
   PII-Erkennung wird behauptet. **R-01 und R-32 bleiben offen.**

3. **Die Synthetic-only-Grenze ist technisch durchgesetzt**, nicht nur
   dokumentiert: Flag, `synthetic:`-Präfix und Marker sind Pflicht; fehlt eines,
   blockiert die Operation ohne Speicherung.

4. **Zwei Testdefekte, keine Codedefekte.** Beide betrafen meine Tests
   (Docstring-Prosa-Grep; Zeilenenden-Normalisierung von `write_text` auf
   Windows). Der Code war korrekt. Die Testzahl 137 stammt aus dem grünen Lauf.

**Kein Risiko wurde geschlossen. Kein Gate wurde bewertet. Capability 5 bleibt
nicht vollständig `implemented`.**

**Nächstes vorgeschlagenes Work Package: CBP-WP-014 — Deterministic Source
Registry and Catalog** (implementation, interactive authorization, Full, B2 –
Standard), Status **`proposed`, implementation not yet authorized**. **Nicht
ausführen** ohne ausdrückliche Freigabe.

---

## Nova REWORK correction run

> **Datum:** 2026-07-22 · **Auslöser:** Nova REWORK auf den Implementation
> Report. Modell Opus 4.8, Effort xhigh, Budget B1 – Lean. Die Erstausführung
> wird **nicht stillschweigend umgeschrieben**: der ursprüngliche Reportstatus
> war **COMPLETE**; dieser Abschnitt korrigiert zwei benannte Ungenauigkeiten im
> **Report** und legt die vollständige, aus den Quelltabellen abgeleitete
> Evidenz offen. **Keine Registerstatus, keine Entscheidung, kein Code, kein
> Store-/Record-/Scannerformat wurden verändert.**

### Beanstandungen

| # | Nova-Befund | Tatsächlicher Befund |
| --- | --- | --- |
| 1 | Der Report nannte nur **5** weiterhin kritische Risiken (R-01, R-25, R-27, R-31, R-32), obwohl CBP-WP-012 **11** führte und nur R-01/R-32/R-33 verändert wurden | **Report-Fehler, kein Registerfehler.** Die Repository-Artefakte sind korrekt und konsistent: `RISK_REGISTER.md` und `PROJECT_BRAIN.md` führen dieselbe kuratierte Liste **`## Weiterhin kritisch`** (6 Einträge). Kein Risiko ist aus einem Register verschwunden |
| 2 | Die technische Evidenz nannte **11 native Befehle**, aber keinen separat bezeichneten Quarantänepolicy-Check; Python-Aufrufe und PowerShell-Kontrollschritte waren nicht getrennt gezählt | **Klassifikationslücke, kein falscher Zählwert.** Die 11 waren korrekt als Teilmenge (native Befehle ohne separaten Policy-Check). Ergänzt: expliziter Policy-Check und kanonische Drei-Kategorien-Matrix |

### Risiko-Prüftabelle (aus den aktuellen Zeilen abgeleitet)

> **Terminologie (im zweiten Korrekturlauf präzisiert):** „Weiterhin kritisch"
> bezeichnet **ausschließlich** die IDs des kanonischen Registerabschnitts
> `## Weiterhin kritisch` (kuratierte Liste). Offene Risiken außerhalb dieser
> Liste sind **zusätzliche offene Beobachtungsrisiken**, nicht „weiterhin
> kritisch". Die Vereinigung beider ist die **gesamte beobachtete
> Risikomenge** — **keine** kritische Liste.

| Risk-ID | Status | Kritikalität | In kuratierter Liste | Zusätzliche Beobachtung | Menge | Quelle |
| --- | --- | --- | :---: | :---: | :---: | --- |
| R-21 | gemindert, nicht geschlossen | **mittel** | ja | nein | A | RISK_REGISTER Z.71, Z.229 |
| R-25 | verändert, offen | hoch | ja | nein | A | Z.31, Z.224 |
| R-27 | verändert, offen | hoch | ja | nein | A | Z.33, Z.225 |
| R-31 | gemindert | hoch | ja | nein | A | Z.34, Z.226 |
| R-32 | neu, offen | hoch | ja | nein | A | Z.48, Z.227 |
| R-34 | neu, offen | hoch | ja | nein | A | Z.63, Z.228 |
| R-01 | offen — Veröffentlichungspfad teilweise gemindert | hoch | nein | ja | B | Z.26 |
| R-20 | verändert, offen | hoch | nein | ja | B | Z.70 |
| R-26 | offen | hoch | nein | ja | B | Z.32 |
| R-30 | konkretisiert | hoch | nein | ja | B | Z.73 |
| R-33 | gemindert, nicht geschlossen | **mittel** | nein | ja | B | Z.62 |

**Alle elf bleiben offen; keines wurde geschlossen.** In CBP-WP-013 verändert
(nicht geschlossen): **R-01, R-32, R-33**. Die übrigen acht wurden **nicht**
berührt — sie bleiben unverändert offen.

### Drei kanonisch benannte Mengen

- **A — Weiterhin kritisch (kuratierte Registerliste), 6:** R-21, R-25, R-27,
  R-31, R-32, R-34 — ausschließlich die IDs des kanonischen Registerabschnitts
  `## Weiterhin kritisch`, identisch in `RISK_REGISTER.md` und
  `PROJECT_BRAIN.md`. Enthält mit **R-21** ein Risiko der Kritikalität
  **mittel** (die Kuratierung ist eine Registerentscheidung, keine
  Schwere-Ableitung).
- **B — Zusätzliche offene Beobachtungsrisiken, 5:** R-01, R-20, R-26, R-30,
  R-33 — offen, aber **nicht** in der kuratierten Liste. Enthält mit **R-33**
  ein Risiko der Kritikalität **mittel**; diese Gruppe wird daher **nicht** als
  „hoch" bezeichnet.
- **C — Gesamte beobachtete Risikomenge, 11:** die eindeutige Vereinigung von A
  und B (= die von CBP-WP-012 beobachtete Menge). **C ist keine kritische
  Liste** und wird nicht unter dem Namen der Teilmenge A geführt.

### Policy-Validierungsevidenz

| Frage | Antwort | Beleg |
| --- | --- | --- |
| Ladepfad | `core.core_brain.quarantine.policy.load_policy(path)` → `parse_policy_mapping` (fail-closed) | `policy.py` |
| `quarantine scan` validiert Policy **vor** Intake | ja — `load_policy(args.policy)` vor `run_scan(...)` | `cli.py::_cmd_quarantine_scan` |
| `quarantine stage` validiert Policy **vor** Scan/Speicherung | ja — `load_policy(args.policy)` vor `QuarantineStore(...)` und `run_stage(...)` | `cli.py::_cmd_quarantine_stage` |
| Unbekanntes Feld blockiert | `test_2_unknown_field_blocks` · ok | `test_quarantine_policy.py` |
| Unbekannte Schema-Version blockiert | `test_3_unknown_version_blocks` · ok | `test_quarantine_policy.py` |
| `release_enabled = true` blockiert | `test_6_release_enabled_blocks` · ok | `test_quarantine_policy.py` |
| `network_enabled = true` blockiert | `test_7_network_enabled_blocks` · ok | `test_quarantine_policy.py` |

**Reproduzierbarer read-only Policy-Check** (`py -3.13`, temporäres Skript
außerhalb des Repos, danach gelöscht; keine Datei im Repo, kein Netzwerk, keine
Runtime-Daten): `loaded=True`, `schema_version=1.0`, **13** Pflichtfelder,
`release_enabled=False`, `network_enabled=False`, `allowed_suffixes=['.md']`,
`policy_sha256`-Länge 64. Exit **0**. Es wurde **keine** neue CLI-Funktion
erzeugt.

### Kanonische Prüfmatrix (drei Kategorien)

| ID | Kategorie | Prüfschritt | Erwartung | Ergebnis | Evidenzquelle |
| --- | --- | --- | --- | --- | --- |
| P01 | PYTHON-TECHNICAL | `compileall core tests` | Exit 0 | **0** | Testlauf |
| P02 | PYTHON-TECHNICAL | `unittest discover -s tests` | Exit 0, `Ran 137 tests`, OK | **0** | Testlauf |
| P03 | PYTHON-TECHNICAL | Policy-Check (`load_policy`) | Exit 0, 13 Felder | **0** | Policy-Check |
| S04 | CLI-SMOKE | `version` | Exit 0 | **0** | Matrixlauf |
| S05 | CLI-SMOKE | `quarantine scan` clean | Exit 0 | **0** | Matrixlauf |
| S06 | CLI-SMOKE | `quarantine scan` review | Exit 5 | **5** | Matrixlauf |
| S07 | CLI-SMOKE | `quarantine scan` blocked | Exit 6 | **6** | Matrixlauf |
| S08 | CLI-SMOKE | `quarantine scan --json` | Exit 0 | **0** | Matrixlauf |
| S09 | CLI-SMOKE | `quarantine stage` | Exit 0 | **0** | Matrixlauf |
| S10 | CLI-SMOKE | `quarantine inspect` | Exit 0 | **0** | Matrixlauf |
| S11 | CLI-SMOKE | `quarantine release` | Exit 7 | **7** | Matrixlauf |
| S12 | CLI-SMOKE | `run` | Exit 4 | **4** | Matrixlauf |
| C13 | POWERSHELL-CONTROL | temporäres Verzeichnis erzeugen | Verzeichnis existiert | **PASS** | Matrixlauf |
| C14 | POWERSHELL-CONTROL | synthetische BOM-freie Testdatei | Datei existiert, kein BOM | **PASS** | Matrixlauf |
| C15 | POWERSHELL-CONTROL | Store-Inventar prüfen | 1 Objekt, 1 Record | **PASS** | Matrixlauf |
| C16 | POWERSHELL-CONTROL | Manifest minimiert prüfen | kein Pfad, kein Dateiname | **PASS** | Matrixlauf |
| C17 | POWERSHELL-CONTROL | Cleanup ausführen | Store entfernt | **PASS** | Matrixlauf |
| C18 | POWERSHELL-CONTROL | Cleanup-Ergebnis prüfen | `Test-Path` = False | **PASS** | Matrixlauf |

**Zahlen je Kategorie:** PYTHON-TECHNICAL **3** · CLI-SMOKE **9** ·
POWERSHELL-CONTROL **6** · **Gesamt 18 Prüfschritte.** Native Befehle mit
`$LASTEXITCODE`: **12** (P01–P03 + S04–S12). PowerShell-Kontrollschritte mit
Pass/Fail: **6**. **Die frühere Zahl 11** bezeichnet die native Teilmenge
**ohne** den nun separat ausgewiesenen Policy-Check (12 − 1 = 11).

### Bestätigte Testzahl

`Ran 137 tests` · **OK** · 0 fehlgeschlagen · 0 Fehler · 0 übersprungen.
Ausschließlich aus der tatsächlichen Ausgabe, nicht addiert.

### Git-Inventar

`git status --porcelain=v1 -uall`: **20 modifiziert + 18 neu + 0 gelöscht + 0
umbenannt = 38 eindeutige Pfade** — unverändert seit dem Erstlauf. HEAD
`1f55234`, 13 Commits, Branch `main`, origin unverändert. `__pycache__`/`*.pyc`
ignoriert.

### R-33-Behandlung

**Zwei getrennte Befunde.** Der Befund dieses ersten Korrekturlaufs — der
Implementation Report nannte nur 5 statt der vollständigen Risikoliste — lag
im **Report**; die kanonischen Register (`RISK_REGISTER.md`, `PROJECT_BRAIN.md`)
waren korrekt. **Der im Zuge dieser Korrektur in dieses Dokument und in
`INGEST_QUARANTINE_EVIDENCE.md` eingeführte Terminologiewiderspruch** (die
Vereinigungsmenge C mit 11 IDs fälschlich als „kritische Liste" bezeichnet) ist
hingegen ein **Repository-Artefaktbefund** und wird als **achter
Konsistenzvorgang** geführt — siehe die Abschnitte weiter unten sowie
[RISK_REGISTER.md](../project-system/RISK_REGISTER.md) und
[COMPLIANCE_CHECK.md](../project-system/COMPLIANCE_CHECK.md). **R-33 bleibt
`gemindert, nicht geschlossen`.**

### Verbleibende Widersprüche

**Keine.** Registerstatus unverändert; die kuratierte Liste „Weiterhin
kritisch" (Menge A, 6), die zusätzlichen offenen Beobachtungsrisiken (Menge B,
5) und die gesamte beobachtete Risikomenge (Menge C, 11) sind kanonisch benannt
und gegeneinander erklärt; Prüfmatrix, Testzahl und Git-Inventar sind gegen ihre
Primärquellen konsistent.

---

## Nova REWORK risk terminology correction run

> **Datum:** 2026-07-22 · **Auslöser:** Nova REWORK auf die Terminologie des
> ersten Korrekturlaufs. Modell Opus 4.8, Effort xhigh, Budget B1 – Lean.
> **docs-only Terminologiekorrektur.** Kein Code, kein Test, keine Policy, kein
> Scanner, kein Store, kein Record, keine CLI, keine neue Datei, kein
> Registerstatus verändert. Die früheren Abschnitte werden nicht stillschweigend
> umgeschrieben; die Terminologie oben ist auf die kanonischen Mengennamen
> präzisiert.

### Ursprünglicher Mengenwiderspruch

Der erste Korrekturlauf bezeichnete die **Vereinigung** aus sechs kuratierten
und fünf zusätzlichen offenen Risiken als „**vollständige aktuelle Liste
kritischer Risiken**" (11) und die zweite Gruppe als „zusätzlich offen/**hoch**",
obwohl sie mit **R-33** ein Risiko der Kritikalität **mittel** enthält. Beide
Formulierungen sind nicht kanonisch: Eine Vereinigungsmenge darf nicht unter
dem Namen ihrer Teilmenge („weiterhin kritisch") geführt werden, und „mittel"
darf nicht als „hoch" bezeichnet werden.

### Kanonische kuratierte Liste — Menge A (Zahl 6)

Ausgezählt aus dieser ID-Liste: **R-21, R-25, R-27, R-31, R-32, R-34** → **6**.
Quelle: kanonischer Registerabschnitt `## Weiterhin kritisch`
([RISK_REGISTER.md](../project-system/RISK_REGISTER.md) Z.220–229), identisch in
`PROJECT_BRAIN.md`.

| ID | Status | Kritikalität |
| --- | --- | --- |
| R-21 | gemindert, nicht geschlossen | **mittel** |
| R-25 | verändert, offen | hoch |
| R-27 | verändert, offen | hoch |
| R-31 | gemindert | hoch |
| R-32 | neu, offen | hoch |
| R-34 | neu, offen | hoch |

### Zusätzliche offene Beobachtungsrisiken — Menge B (Zahl 5)

Ausgezählt aus dieser ID-Liste: **R-01, R-20, R-26, R-30, R-33** → **5**.
Offen, aber **nicht** in der kuratierten Liste; **nicht** „weiterhin kritisch".

| ID | Status | Kritikalität |
| --- | --- | --- |
| R-01 | offen — Veröffentlichungspfad teilweise gemindert | hoch |
| R-20 | verändert, offen | hoch |
| R-26 | offen | hoch |
| R-30 | konkretisiert | hoch |
| R-33 | gemindert, nicht geschlossen | **mittel** |

### Gesamte beobachtete Risikomenge — Menge C (Zahl 11)

Ausgezählt aus dieser ID-Liste: **R-01, R-20, R-21, R-25, R-26, R-27, R-30,
R-31, R-32, R-33, R-34** → **11** (eindeutige Vereinigung von A und B).
**C ist keine kritische Liste.** In CBP-WP-013 verändert (nicht geschlossen):
R-01, R-32, R-33. Geschlossen: keines.

### Korrigierte Dateien

- `work-packages/CBP-WP-013.md` — Terminologie der Risikomengen präzisiert
  (Menge A/B/C), Prüftabelle nach kanonischem Schema, „hoch"-Fehlbezeichnung
  entfernt.
- `docs/runtime/INGEST_QUARANTINE_EVIDENCE.md` — dieselbe Terminologiekorrektur
  in „Verbleibende Blocker".

**Keine Statusdatei verändert.** Der Widerspruch bestand ausschließlich in
diesen beiden ungetrackten WP-013-Dokumenten; die kanonischen Register
(`RISK_REGISTER.md`, `PROJECT_BRAIN.md`) waren bereits korrekt.

### R-33-Behandlung (korrigiert im dritten Korrekturlauf)

> **Korrektur der vorherigen Schlussfolgerung.** Der zweite Korrekturlauf hatte
> festgestellt, „kein neuer R-33-Chronologieeintrag" sei nötig, weil der
> Widerspruch nur in den beiden ungetrackten WP-013-Dokumenten lag. **Diese
> Einschränkung auf ein „kanonisches Statusartefakt" war nicht autorisiert.**

**Genau ein neuer R-33-Chronologieeintrag wurde ergänzt.** Die beiden Dateien
`work-packages/CBP-WP-013.md` und `docs/runtime/INGEST_QUARANTINE_EVIDENCE.md`
sind **Repository-Artefakte** des CBP-WP-013-Änderungssatzes; dass sie noch
ungetrackt sind oder keine kanonischen Statusregister sind, hebt die Regel
nicht auf. Der Eintrag (achter Konsistenzvorgang, 2026-07-22) ist geführt in
[RISK_REGISTER.md](../project-system/RISK_REGISTER.md) unter R-33 und in der
Tabelle „Historie der Zählfehler" in
[COMPLIANCE_CHECK.md](../project-system/COMPLIANCE_CHECK.md).

- **Zahlen 6, 5 und 11 waren korrekt** — es war kein arithmetischer Zählfehler.
- **Der Fehler betraf die Mengenbenennung** (Vereinigungsmenge C als „kritische
  Liste") **und die Kritikalitätsterminologie** (Gruppe B als „hoch", obwohl
  R-33 mittel ist).
- **R-33 bleibt `gemindert, nicht geschlossen`** — der Eintrag ändert den Status
  nicht; frühere Chronologieeinträge sind unverändert.
- **Aktueller Stand: acht Konsistenzvorgänge in dreizehn Work Packages.**

### Verbleibende Widersprüche (dritter Korrekturlauf)

**Keine.** Menge A (6), Menge B (5) und Menge C (11) sind kanonisch benannt,
jede Zahl aus ihrer ID-Liste ausgezählt, keine Kritikalität fehlbezeichnet, kein
Registerstatus und keine Risikokritikalität verändert; der R-33-Chronologie-
eintrag ist ergänzt und die Chronologieanzahl auf acht nachgeführt.
