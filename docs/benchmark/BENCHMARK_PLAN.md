# Benchmark Plan — Vergleichsvarianten und Versuchsablauf

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Erfasst in | CBP-WP-005 |
| Autoritätsklasse | A2 |
| Status | **Plan dokumentiert, kein Lauf durchgeführt** |
| Stand | 2026-07-21 (Korrekturlauf) |

Belegt G0-Kriterium **G-4**.

---

## Zweck

Drei Varianten desselben Ablaufs auf demselben Korpus mit denselben Fragen.
Verglichen wird, was sich zwischen ihnen ändert — nicht, ob eine bestimmte
Software funktioniert.

**Es wurde keine Suchsoftware ausgewählt.** Alle drei Varianten sind
provider-neutral beschrieben.

---

## V0 — Bisheriger beziehungsweise naiver Ablauf

**Rolle: Baseline. Nur zum Vergleich, nicht als Ziel.**

| Merkmal | Ausprägung |
| --- | --- |
| Suchleiter | **keine verpflichtende** |
| Quellensuche | manuell oder ungezielt; Verzeichnisdurchsicht, Dateinamenraten, Volltextlesen |
| Index | keiner |
| Metadatenfilter | keine |
| Context Budget | **keines** |
| Autoritätsprüfung | allenfalls implizit |
| Datenschutzprüfung | allenfalls implizit |

V0 bildet den Zustand ab, aus dem das Projekt entstanden ist: hoher
Kontextverbrauch durch wiederholte und ungezielte Suchvorgänge.

V0 ist **kein Strohmann**. Der Ablauf wird ernsthaft durchgeführt, mit dem
Ziel, die Fragen richtig zu beantworten. Ein künstlich schlechter Baseline-Lauf
macht jede spätere Verbesserung wertlos.

## V1 — Deterministischer Brain-First-Ablauf

**Rolle: erster Nachweis, dass Ordnung allein wirkt.**

| Merkmal | Ausprägung |
| --- | --- |
| Einstieg | **`corpus/INDEX.md` vollständig lesen** |
| Metadatenfilter | Autoritätsklasse, Datenklasse, Frischestatus, Projekt |
| Suche | **lexikalisch** — Stichwort, Titel, Pfad |
| Semantische Suche | **nicht erforderlich** |
| Context Budget | **verbindlich** je Frage (B0 bis B3) |
| Quellenbegrenzung | Normalfall 1, erweitert höchstens 3 |
| Policy Layer | vollständig — Autorität, Aktualität, Datenklasse, Trace |

V1 ist die wichtigste Variante des Piloten. Wenn V1 gegenüber V0 keinen
messbaren Vorteil bringt, ist die Grundannahme des Projekts falsch — und das
wäre ein wertvolles Ergebnis.

## V2 — Hybrider Retrieval-Ablauf

**Rolle: Prüfung, ob semantische Suche zusätzlichen Nutzen bringt.**

| Merkmal | Ausprägung |
| --- | --- |
| Einstieg | wie V1 |
| Suche | **Volltext + semantisch**, optional Reranking |
| Policy Layer | **identisch mit V1** |
| Korpus | **identisch mit V1** |
| Context Budget | **identisch mit V1** |
| Suchsoftware | **nicht festgelegt** |

> **Keine konkrete Suchsoftware für V2.** qmd bleibt Evaluationskandidat mit
> Prüfvorbehalt (OD-25); SQLite FTS, ein eigener Hybridstack oder ein anderer
> Anbieter sind gleichermaßen zulässig. Die Wahl fällt nicht hier.

V2 unterscheidet sich von V1 **ausschließlich** in der Retrieval-Technik. Alles
andere bleibt gleich — sonst misst der Vergleich nicht die Technik, sondern die
Änderung drumherum.

---

## Vergleichsmatrix

| Merkmal | V0 | V1 | V2 |
| --- | --- | --- | --- |
| Index als Einstieg | nein | **ja** | **ja** |
| Metadatenfilter | nein | ja | ja |
| Lexikalische Suche | ungezielt | **ja** | ja |
| Semantische Suche | nein | nein | **ja** |
| Reranking | nein | nein | optional |
| Context Budget | nein | **ja** | ja |
| Policy Layer | nein | **ja** | ja |
| Provider-Bindung | keine | keine | **keine** |

---

## Versuchsablauf

Zehn Regeln. Sie gelten für jeden Lauf jeder Variante.

### 1. Identischer versionierter Korpus

Alle Läufe verwenden dieselbe Dataset-Version. Ändert sich der Korpus, sind
frühere Ergebnisse nicht mehr vergleichbar.

**Aktuell: Dataset 2.0.0** mit vollständiger Autoritätsabdeckung A0 bis A6.
Version 1.0.0 enthielt kein A0-Fixture und ist damit nicht vergleichbar; auf
ihrer Grundlage wurde nie gemessen.

### 2. Identische Fragen

Wortgleich aus `BENCHMARK_QUESTIONS.md`. Keine Umformulierung, keine Zusätze,
keine Hinweise auf die erwartete Quelle.

### 3. Frische Sessions

Jeder Lauf beginnt in einer neuen Sitzung ohne Vorwissen aus vorherigen Läufen.
Wissen aus einem früheren Lauf verfälscht die Messung mehr als jede
Suchtechnik.

### 4. Möglichst identisches Modell

Gleiches Modell, gleiche Version. Ein Modellwechsel während einer Messreihe
macht sie ungültig — siehe Regel 10.

### 5. Identische Datenschutz- und Berechtigungsregeln

In allen Varianten gelten dieselben Regeln aus
[PERMISSION_MODEL.md](../security/PERMISSION_MODEL.md) und
[DATA_CLASSIFICATION.md](../privacy/DATA_CLASSIFICATION.md). **Auch V0** — die
Baseline darf keine Datenschutzvorteile durch Regellosigkeit haben.

### 6. Development-Set für Iteration

Die 24 Development-Fragen dienen der Kalibrierung: Gewichte, Filterreihenfolge,
Prompts, Budgets.

### 7. Holdout-Set für die Abschlussprüfung

Die 12 Holdout-Fragen werden **erst am Ende** vollständig ausgewertet und
**nie** zur Kalibrierung verwendet. Wer alle Fragen zur Optimierung nutzt,
misst am Ende nur noch sich selbst.

### 8. Rohdaten versioniert speichern

Je Lauf: Variante, Dataset-Version, Datum, Modell, Frage, geöffnete Quellen,
Rangfolge, Antwort, Messwerte, Fehler. Ohne Rohdaten ist ein Ergebnis nicht
nachprüfbar.

**Rohdaten enthalten keine gesperrten Inhalte** — bei `excluded-from-ai` wird
nur die Entscheidung protokolliert, nicht der Inhalt.

### 9. Keine manuelle Nachkorrektur während eines Laufs

Fällt ein Fehler auf, wird er **notiert, nicht behoben**. Eine Korrektur
mittendrin erzeugt eine Mischung aus zwei Konfigurationen, die nichts mehr
misst.

### 10. Abweichungen dokumentieren

Jede Abweichung vom Protokoll wird festgehalten: Modellwechsel, Toolwechsel,
Abbruch, Umgebungsänderung. Ein Lauf mit dokumentierter Abweichung ist
verwertbar; ein Lauf mit unbemerkter Abweichung ist wertlos.

---

## Auswertungsreihenfolge

```text
1. V0 vollständig (Development + Holdout)   → Baseline
2. V1 Development                            → Kalibrierung
3. V1 Holdout                                → Abschlussprüfung V1
4. V2 Development                            → Kalibrierung
5. V2 Holdout                                → Abschlussprüfung V2
6. Vergleich V0 / V1 / V2
```

V0 wird **zuerst und vollständig** gemessen, bevor an V1 kalibriert wird.
Sonst besteht die Versuchung, die Baseline nachträglich schlechter darzustellen.

## Was der Plan nicht festlegt

| Punkt | Status |
| --- | --- |
| Suchsoftware für V2 | offen (OD-25, OD-20) |
| Embedding-Modell | offen |
| Reranking-Verfahren | offen |
| Konkrete Token-Zählmethode | offen, siehe [BASELINE_PROTOCOL.md](BASELINE_PROTOCOL.md) |
| Kalibrierung der Budget-Richtwerte | **OD-02b bleibt offen** bis zur Messung |

## Status

**Kein Lauf durchgeführt.** Es existiert keine Suche, kein Index, keine
Messung. Dieser Plan beschreibt, wie gemessen werden soll.
