# Phase 1 Evidence Plan — Nachweise und Abnahme

| Feld | Wert |
| --- | --- |
| **Status** | **PROPOSED** |
| Erfasst in | CBP-WP-008 |
| Autoritätsklasse | A3 |
| Gilt für | Streams **F1–F5**, Work Packages **CBP-WP-009 bis CBP-WP-014** |
| Stand | 2026-07-21 |

Dieses Dokument legt fest, **was als Nachweis zählt** und **wie weit ein
Nachweis trägt**. Es ist die Antwort auf ein wiederkehrendes Muster dieses
Projekts: dokumentierte Kontrollen wurden mit durchgesetzten Kontrollen
verwechselt.

> **Kein Status darf allein aus einer Absicht abgeleitet werden.** Eine
> geplante Kontrolle ist keine Kontrolle. Ein beschriebener Test ist kein
> Testergebnis.

---

## Sechs Statusstufen

Die Stufen sind **kumulativ**. Eine höhere Stufe setzt alle darunter voraus.

| Stufe | Name | Bedeutet | Bedeutet **nicht** |
| --- | --- | --- | --- |
| **1** | `dokumentiert` | Beschrieben und abgestimmt | dass es existiert |
| **2** | `implementiert` | Umgesetzt und lauffähig | dass es korrekt wirkt |
| **3** | `lokal getestet` | Der **Gutfall** funktioniert | dass der Schlechtfall scheitert |
| **4** | `negativ getestet` | Der **verbotene Fall scheitert tatsächlich** | dass es einen Ausfall übersteht |
| **5** | `wiederhergestellt` | Nach Verlust nachweislich wiederhergestellt | dass jemand es abgenommen hat |
| **6** | `vom Human Maintainer angenommen` | Ausdrücklich als ausreichend angenommen | — Endstufe |

### Regeln

| # | Regel |
| --- | --- |
| **E1** | Eine Stufe wird nur mit **Beleg** vergeben, nie aus Plausibilität |
| **E2** | Stufen werden **nicht übersprungen** |
| **E3** | **Stufe 1 schließt kein Risiko.** Ein Dokument ist keine Kontrolle |
| **E4** | Eine **Sicherheitskontrolle** braucht mindestens **Stufe 4**. Stufe 3 genügt nie |
| **E5** | Ein **Wiederherstellungsnachweis** braucht Stufe 5. Eine ungeprüfte Sicherung ist keine Sicherung |
| **E6** | **Stufe 6 vergibt ausschließlich der Human Maintainer** — nicht Nova, nicht der Implementation Agent |
| **E7** | Änderung am Gegenstand setzt die Stufe auf **höchstens 2** zurück |
| **E8** | Bei Zweifel gilt die **niedrigere** Stufe |

**E3 und E4 sind der Kern.** Der gesamte bisherige Projektstand steht auf
Stufe 1 — deshalb ist kein technisches Risiko geschlossen worden.

---

## Acht Nachweisarten

| Art | Kennung | Inhalt | Höchste Stufe **allein** |
| --- | --- | --- | --- |
| **Designnachweis** | NW-DES | Spezifikation, Modell, ADR | **1** |
| **Implementierungsnachweis** | NW-IMP | Konfigurations- und Ausführungsbeleg | 2 |
| **Negativtest** | **NW-NEG** | Der verbotene Fall scheitert | **4** |
| **Sicherheitsnachweis** | NW-SEC | Rechte, Identitäten, Grenzen wirksam | 4 |
| **Datenschutzbeleg** | NW-PRI | Klassifikation und Transfergrenze wirksam | 4 |
| **Rebuild-/Restore-Beleg** | **NW-RST** | Durchgeführter Rebuild oder Restore | **5** |
| **Human-Abnahme** | **NW-HUM** | Aufgezeichnete Entscheidung des Human Maintainers | **6** |
| **Statusquelle** | NW-SRC | Wo der Status geführt wird, nachprüfbar | — |

**Ein NW-DES erreicht nie Stufe 2.** Das ist keine Formalie: der Unterschied
zwischen „beschrieben" und „vorhanden" ist genau der Bereich, in dem R-25,
R-27, R-30, R-31 und R-32 liegen.

Ausnahme mit Grund: **Entscheidungen** werden nicht getestet. Ein NW-HUM
belegt nicht, dass etwas funktioniert, sondern dass jemand etwas entschieden
hat.

---

## Nachweise je Stream und Work Package

### F1 · CBP-WP-009 — Repository Boundary Decision

| Nachweisart | Inhalt | Zielstufe | Statusquelle |
| --- | --- | --- | --- |
| Designnachweis | REPOSITORY_AND_WORKSPACE_PLAN, REPOSITORY_LAYOUT_OPTIONS | 1 | `docs/roadmap/` |
| Implementierungsnachweis | **entfällt** — keine Umsetzung | — | — |
| Negativtest | **entfällt** | — | — |
| Sicherheitsnachweis | Bereichsgrenze schließt privaten Bestand aus dem Core Repository aus | 1 | ADR |
| Datenschutzbeleg | ADR-0006-Konformität begründet | 1 | ADR |
| Rebuild-/Restore-Beleg | **entfällt** | — | — |
| **Human-Abnahme** | **A0-Entscheidung zu OD-26 im Wortlaut** | **6** | DECISION_REGISTER |
| Statusquelle | DECISION_REGISTER, WORK_PACKAGE_QUEUE | — | `project-system/` |

### F2 · CBP-WP-010 — Pilot Source Mapping Specification

| Nachweisart | Inhalt | Zielstufe | Statusquelle |
| --- | --- | --- | --- |
| Designnachweis | Mappingschema, **31 Felddefinitionen** (29 Pflicht + 2 optional), **24 Validierungsregeln** V1–V24 *(19/31-Korrektur CBP-WP-015, R-33; frühere Angabe „19 Felder, M1–M14" war eine abgelöste Planungsannahme aus CBP-WP-008)* | 1 | PILOT_SOURCE_MAPPING_SCHEMA · PILOT_SOURCE_MAPPING_VALIDATION · ADR-0012 |
| Implementierungsnachweis | Mapping validiert; Quelle erreichbar; Rechte minimal | 2 | Operator Workspace |
| **Negativtest** | **Ausschlüsse wirksam**; Mapping ohne Freigabe aktiviert nicht (M6); Rechteerweiterung scheitert (M11) | **4** | Testprotokoll |
| Sicherheitsnachweis | **Keine Secrets** im gemappten Bereich | 4 | Scanprotokoll |
| **Datenschutzbeleg** | **Datenklasse bestätigt**; **AI-Transfer-Regel getestet** | **4** | Testprotokoll |
| Rebuild-/Restore-Beleg | **entfällt** in diesem Paket | — | — |
| Human-Abnahme | Freigabe der Quellenauswahl; OD-05, OD-06 | 6 | DECISION_REGISTER |
| Statusquelle | Registry, Operator Workspace | — | — |

### F3 · CBP-WP-011 — Technical Security Foundation Specification

| Nachweisart | Inhalt | Zielstufe | Statusquelle |
| --- | --- | --- | --- |
| Designnachweis | KB-01 bis KB-12 vollständig spezifiziert, mit Testdefinition | 1 | TECHNICAL_SECURITY_FOUNDATION_PLAN |
| Implementierungsnachweis | **entfällt** — noch keine Bereitstellung | — | — |
| Negativtest | **definiert**, nicht ausgeführt | 1 | Testdefinition |
| Sicherheitsnachweis | Jede Kontrolle hat eine tragende Ebene 1–6 (**SB-03**) | 1 | Zuordnungstabelle |
| Datenschutzbeleg | KB-11 spezifiziert | 1 | Plan |
| Rebuild-/Restore-Beleg | KB-12 spezifiziert | 1 | Plan |
| Human-Abnahme | Abnahme der Testdefinition | 6 | Review |
| Statusquelle | CAPABILITY_MATRIX, RISK_REGISTER | — | `project-system/` |

### F3 · CBP-WP-012 — Foundation Runtime Skeleton

| Nachweisart | Inhalt | Zielstufe | Statusquelle |
| --- | --- | --- | --- |
| Designnachweis | aus CBP-WP-011 übernommen | 1 | Plan |
| Implementierungsnachweis | Rechteauflistung (KB-04); Prozessidentitäten (KB-01, KB-02); Mountliste (KB-03) | 2 | Laufzeitbeleg |
| **Negativtest** | **Schreibversuch auf Canonical scheitert**; **Eskalation scheitert**; **`ro`-Verletzung scheitert**; **Pushversuch scheitert** (KB-07) | **4** | Testprotokoll |
| **Sicherheitsnachweis** | **Kein Secretfund** in Repository, Index, Context Pack (KB-08); Audit append-only (KB-09) | **4** | Scan- und Auditprotokoll |
| Datenschutzbeleg | Egress-Allowlist wirksam (KB-10) | 4 | Netztest |
| Rebuild-/Restore-Beleg | Backup-Isolation belegt (KB-12) | 4 | Rechtetest |
| Human-Abnahme | Abnahme der Sicherheitsgrundlage | 6 | Review |
| Statusquelle | RISK_REGISTER — **R-25, R-27** | — | `project-system/` |

**R-25 und R-27 schließen erst hier, bei Stufe 4** — nicht bei Stufe 2.

### F4 · CBP-WP-013 — Ingest Quarantine MVP

| Nachweisart | Inhalt | Zielstufe | Statusquelle |
| --- | --- | --- | --- |
| Designnachweis | 12 Schritte, 10 Status, Q1–Q5, S1–S9 | 1 | INGEST_QUARANTINE_PLAN |
| Implementierungsnachweis | Pipeline lauffähig; Statusübergänge protokolliert | 3 | Ausführungsprotokoll |
| **Negativtest** | **N-01 bis N-12**; **keine Quelle von `received` direkt nach indexiert** | **4** | Testprotokoll |
| **Sicherheitsnachweis** | **Secretfund blockiert jeden weiteren Ingest** (N-01, S5) | **4** | Testprotokoll |
| **Datenschutzbeleg** | **N-02, N-03, N-07** — `excluded-from-ai`, unbekannte Klasse, Sammelanfrage | **4** | Testprotokoll |
| Rebuild-/Restore-Beleg | **N-05, N-06** — Derived Cleanup und Tombstone wirksam | 4 | Testprotokoll |
| Human-Abnahme | Abnahme der Pipeline und der Freigabekette | 6 | Review |
| Statusquelle | RISK_REGISTER — **R-32, R-31, R-30** | — | `project-system/` |

**N-02 und N-07 sind die Nachweise zu KB-11** und damit zu R-31 und R-30. Kein
anderer Nachweis schließt diese beiden Risiken.

### F5 · CBP-WP-014 — Deterministic Source Registry and Catalog

| Nachweisart | Inhalt | Zielstufe | Statusquelle |
| --- | --- | --- | --- |
| Designnachweis | 24 Felder, ID-, Hash-, Revisions-, Tombstoneregeln | 1 | SOURCE_REGISTRY_PLAN |
| Implementierungsnachweis | Registry angelegt; Einträge erzeugt | 2 | Registry |
| **Negativtest** | **Tombstone überlebt Rebuild** (T-4); nur `approved` wird indexiert (C-6) | **4** | Testprotokoll |
| Sicherheitsnachweis | Registry nicht durch Dienstkonten schreibbar | 4 | Rechtetest |
| Datenschutzbeleg | `excluded-from-ai` erzwingt `forbidden` (C-3) | 4 | Testprotokoll |
| **Rebuild-/Restore-Beleg** | **Zwei Läufe, gleicher Indexzustand**; **Rebuild aus kanonisch + Registry** | **5** | Rebuildprotokoll |
| Human-Abnahme | Abnahme des Katalogs | 6 | Review |
| Statusquelle | RISK_REGISTER — **R-10, R-07** | — | `project-system/` |

**Der Rebuild-Vertrag aus ADR-0003 wird hier zum ersten Mal geprüft** — bis
dahin ist er eine Behauptung.

---

## Risikoschließung

| Risiko | Gegenstand | Schließt bei |
| --- | --- | --- |
| **R-25** | Berechtigungen nur als Promptregel | CBP-WP-012, **Stufe 4** |
| **R-27** | Git-/GitHub-Rechte nicht durchgesetzt | CBP-WP-012, **Stufe 4** |
| **R-26** | Root- oder Hostbetrieb | CBP-WP-012, **Stufe 4** |
| **R-32** | Keine Quarantäne | CBP-WP-013, **Stufe 4** |
| **R-31** | Sperrwirkung `excluded-from-ai` ungeprüft | CBP-WP-013, **Stufe 4** (N-02, N-07) |
| **R-30** | Klassifikation ohne technische Durchsetzung | CBP-WP-013, **Stufe 4** |
| **R-10** | Nichtdeterministische Indexierung | CBP-WP-014, **Stufe 4** |
| **R-07** | Indexverlust bedeutet Wissensverlust | CBP-WP-014, **Stufe 5** |
| **R-01** | Secret in der Git-Historie | **bleibt** — nur teilweise minderbar |
| **R-20** | Restore ungetestet | **außerhalb F1–F5** (P9) |
| **R-21** | Retrieval ungemessen | **außerhalb F1–F5** (P7) |
| **R-33** | Fehlerhafte Kennzahlen | **bleibt gemindert** — Dokumentregel, keine technische Kontrolle |

**Kein Risiko dieser Liste wird durch CBP-WP-008 geschlossen.** Dieses
Work Package erzeugt ausschließlich Designnachweise auf Stufe 1.

## Berichtsregel

Jeder Implementation Report eines Phase-1-Pakets nennt je Nachweis:
**Art · erreichte Stufe · Beleg · Statusquelle · was die Stufe *nicht*
bedeutet.**

Fehlt der Beleg, wird die Stufe **nicht vergeben** — sie wird als fehlend
berichtet. Eine nicht vergebene Stufe ist ein zulässiges Ergebnis. Eine
unbelegt vergebene Stufe ist ein Fehler.

## Status

**PROPOSED.** Alle bisherigen Artefakte des Projekts stehen auf **Stufe 1**.

**Implementierung erlaubt: nein.**
