# Ingest Quarantine Plan — fail-closed Aufnahmepipeline

| Feld | Wert |
| --- | --- |
| **Status** | **PROPOSED** — Plan, keine Implementierung |
| Stream | F4 · Backlogpunkt P4 |
| Erfasst in | CBP-WP-008 |
| Autoritätsklasse | A3 |
| Grundlage | **D-019**, **D-021**, ADR-0003 |
| Betrifft | **R-32** (bleibt offen) |
| Abhängig von | **F3** — KB-01 bis KB-04, KB-08 |
| Stand | 2026-07-21 |

Dieses Dokument beschreibt die Pipeline. Es **installiert keinen Scanner**,
wählt keine Software und verwendet **keine realistischen Secrets** — auch nicht
als Beispiel.

**Die Quarantäne existiert nicht.** PS-06 und PS-07 sind genau deshalb
`deferred` (R-32).

---

## Grundsatz

**D-019:** PDF- und Office-Dokumente gelangen **nicht ungeprüft** in den
kanonischen Bestand.

Die Pipeline ist **fail-closed**: Der Normalzustand jedes Schrittes ist
Ablehnung. Ein Fehler, ein Zeitüberlauf, ein nicht erreichbarer Prüfer oder ein
unbekanntes Format führen zu **Blockade**, nie zur Aufnahme.

> Ein übersprungener Prüfschritt ist keine bestandene Prüfung.

---

## Zwölf Schritte

| # | Schritt | Fail-closed-Verhalten |
| --- | --- | --- |
| **1** | **Quelle registrieren** — Zuordnung zu genau einem Slot und Mapping | Ohne gültiges, freigegebenes Mapping: `rejected` |
| **2** | **In Quarantäne aufnehmen** — isolierter Bereich außerhalb des kanonischen Bestands | Kein Zugriff durch Indexer oder Retrieval, auch nicht lesend |
| **3** | **Format prüfen** gegen `allowed_formats` des Slots | Unbekanntes oder nicht erlaubtes Format: `rejected` |
| **4** | **Secret-Scan** | Fund: **`rejected`** und **Blockade jedes weiteren Ingest** |
| **5** | **Datenklasse prüfen** | Nicht bestimmbar: `classification-required`, **nie** eine Vorgabe |
| **6** | **Metadaten prüfen** | Pflichtfelder fehlen: `classification-required` |
| **7** | **Autoritätsklasse bestimmen oder offen lassen** | Nicht bestimmbar: **offen lassen**, nie A0–A2 vergeben |
| **8** | **Ausschlussregeln anwenden** (`excluded_subpaths`) | Bei Überschneidung wird ausgeschlossen |
| **9** | **Human Review** | Ohne menschliche Prüfung bleibt der Eintrag `review-required` |
| **10** | **Freigabe** | Nur ein Mensch setzt `approved` |
| **11** | **Erst danach Indexierung** | Es gibt keinen Index über Quarantäneinhalt |
| **12** | **Auditnachweis erzeugen** | Jeder Schritt und jede Ablehnung wird protokolliert (KB-09) |

### Reihenfolgeregeln

| Regel | Inhalt |
| --- | --- |
| **Q1** | **Schritt 4 vor Schritt 11.** Ein Secret im Index ist nur durch Rotation und Rebuild zu beheben |
| **Q2** | **Schritt 9 und 10 vor Schritt 11.** Maschinelle Prüfung ersetzt kein Human Review |
| **Q3** | **Keine Quelle gelangt direkt von `received` nach indexiert.** Alle zwölf Schritte werden durchlaufen |
| **Q4** | Kein Schritt wird übersprungen, auch nicht bei erneuter Aufnahme desselben Inhalts |
| **Q5** | **Scannerentscheidungen ersetzen kein Human Review.** Ein `scan-passed` ist eine Voraussetzung, keine Freigabe |

**Q1 ist die wichtigste.** Die Reihenfolge Rotation-vor-Cleanup im
Secret-Incident-Verfahren existiert, weil Q1 verletzt wurde.

---

## Zehn Statuswerte

| # | Status | Bedeutung | Erreichbar aus |
| --- | --- | --- | --- |
| 1 | `received` | Angenommen, nichts geprüft | — (Eingang) |
| 2 | `quarantined` | Isoliert, Prüfung ausstehend | `received` |
| 3 | `scan-passed` | Secret- und Formatprüfung bestanden | `quarantined` |
| 4 | `scan-failed` | Prüfung nicht bestanden oder nicht abgeschlossen | `quarantined` |
| 5 | `classification-required` | Datenklasse oder Metadaten unbestimmt | `scan-passed` |
| 6 | `review-required` | Bereit zur menschlichen Prüfung | `scan-passed`, `classification-required` |
| 7 | `approved` | Menschlich freigegeben; Indexierung zulässig | `review-required` |
| 8 | `rejected` | Abgelehnt; Eintrag bleibt zur Nachvollziehbarkeit | jeder Status außer `approved` |
| 9 | `revoked` | Freigabe nachträglich zurückgenommen | `approved` |
| 10 | `deleted` | Entfernt; Tombstone bleibt | `rejected`, `revoked`, `approved` |

```text
received ─► quarantined ─┬─► scan-passed ─┬─► classification-required ─┐
                         │                │                            │
                         │                └────────────────────────────┴─► review-required
                         │                                                        │
                         └─► scan-failed ─────────► rejected ◄───────────────────┘
                                                        │                          │
                                                        │                    approved ─► revoked
                                                        │                          │        │
                                                        └────► deleted ◄───────────┴────────┘
```

### Zustandsregeln

| # | Regel |
| --- | --- |
| **S1** | **Keine Quelle gelangt von `received` direkt nach indexiert** |
| **S2** | Nur `approved` wird indexiert |
| **S3** | **`approved` setzt ausschließlich ein Mensch** |
| **S4** | `scan-failed` **blockiert**; kein automatischer Übergang nach `approved` |
| **S5** | **Ein Secret-Fund blockiert jeden weiteren Ingest**, nicht nur den betroffenen Eintrag |
| **S6** | `revoked` und `deleted` **erzeugen Derived Cleanup** — alle abgeleiteten Daten werden entfernt |
| **S7** | `deleted` löscht den **Inhalt**, nicht den Eintrag — der Tombstone bleibt |
| **S8** | Ein unbekannter Status wird wie `rejected` behandelt |
| **S9** | **PDF und Office bleiben `deferred`**, bis eine Parserfreigabe erteilt ist |

**Zu S5:** Ein Secret-Fund ist kein Einzelfall, sondern ein Hinweis auf eine
Quelle, deren Klassifikation nicht stimmt. Die Blockade gilt, bis das
[Incident-Verfahren](../security/SECRET_INCIDENT_RESPONSE.md) abgeschlossen
ist — **Rotation vor History Cleanup**.

---

## Negativtests

Ein Negativtest gilt nur als bestanden, wenn die Aufnahme **tatsächlich
scheitert** — nicht, wenn eine Warnung erscheint.

| # | Test | Erwartung |
| --- | --- | --- |
| **N-01** | **Synthetisches Secret-Muster** ohne realen Wert | `rejected` in Schritt 4; **jeder weitere Ingest blockiert** (S5) |
| **N-02** | Inhalt mit Klasse **`excluded-from-ai`** | Keine externe Übertragung; **weder in Suchergebnis noch in Context Pack noch in einer Antwort** |
| **N-03** | **Unbekannte Datenklasse** | `classification-required`; **keine** externe Übertragung |
| **N-04** | **Nicht erlaubtes Format** | `rejected` in Schritt 3 |
| **N-05** | **Widerrufene Quelle** (`revoked`) | Derived Cleanup ausgeführt; nicht mehr auffindbar |
| **N-06** | **Tombstone** | Überlebt einen Rebuild; Eintrag kehrt **nicht** zurück |
| **N-07** | **Sammelanfrage über gesperrte Quellen** | Kein gesperrter Inhalt in der Antwort — **auch nicht in Auszügen oder Zusammenfassungen** |
| **N-08** | Scanner nicht erreichbar oder Zeitüberlauf | `scan-failed`, **nicht** `approved` |
| **N-09** | Freigabe maschinell gesetzt | Wird nicht als `approved` akzeptiert (S3) |
| **N-10** | Indexer greift auf Quarantäne zu | Scheitert auf Ebene 1 oder 3 (KB-03, KB-04) |
| **N-11** | Erneute Aufnahme desselben Inhalts | Vollständiger Durchlauf, kein Überspringen (Q4) |
| **N-12** | PDF- oder Office-Datei | Bleibt `deferred`; keine Aufnahme ohne Parserfreigabe |

**N-01 ausdrücklich:** Der Test verwendet ein **erkennbares Muster ohne realen
Geheimwert**. Es wird kein Secret erzeugt, um eine Secret-Erkennung zu prüfen —
das wäre genau der Vorgang, den die Kontrolle verhindern soll.

**N-02 und N-07 sind die Nachweise zu KB-11** und damit zu **R-31**
(Sperrwirkung ungeprüft) und **R-30** (Klassifikation ohne Durchsetzung). Der
Weg über **weit gefasste Sammelanfragen** ist besonders zu prüfen —
Benchmarkfrage D-06.

---

## Abgrenzung

| Dieses Dokument | Nicht dieses Dokument |
| --- | --- |
| Schritte, Zustände, Regeln | Scannerauswahl oder -installation |
| Negativtestbeschreibungen | Ausgeführte Tests |
| Fail-closed-Verhalten | Implementierung dieses Verhaltens |
| Statusmodell | Datenbankschema |

## Abhängigkeiten

| Voraussetzung | Aus | Grund |
| --- | --- | --- |
| KB-03, KB-04 | F3 | Quarantänebereich muss für den Indexer unzugänglich sein |
| KB-01, KB-02 | F3 | Prüfprozess braucht eine eigene, nicht privilegierte Identität |
| **KB-08** | F3 | Schritt 4 setzt die Secret-Store-Grenze voraus |
| KB-09 | F3 | Schritt 12 setzt Audit-Logging voraus |
| Mappingschema | F2 | Schritt 1 braucht `slot_id` und `mapping_id` |

**Ohne F3 ist diese Pipeline nicht durchsetzbar** — sie wäre eine Konvention.

## Status

**PROPOSED.** Es existiert **keine** Quarantäne, kein Scanner, kein Ingest, kein
Statusspeicher. **R-32 bleibt `offen`** und schließt durch bestandene
Negativtests, nicht durch diesen Plan.

**Implementierung erlaubt: nein.**
