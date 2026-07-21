# Benchmarks — Core Brain Pilot

| Feld | Wert |
| --- | --- |
| **Dataset-Version** | **2.0.0** |
| Erfasst in | CBP-WP-005 |
| Autoritätsklasse | A2 |
| Status | **Design dokumentiert, nicht ausgeführt** |
| Stand | 2026-07-21 (Korrekturlauf) |

> **Alles hier ist ein synthetisches Testartefakt.**
> Kein produktiver Wissensbestand. Keine realen Daten. Keine Suchimplementierung.

---

## Was hier liegt

| Pfad | Inhalt |
| --- | --- |
| `corpus/INDEX.md` | Quellenkatalog — **Einstiegspunkt der Suchleiter** |
| `corpus/*.md` | 24 synthetische Quelldateien, alle mit `test_fixture: true`; das A0-Fixture zusätzlich mit `synthetic_authority: true` |
| `questions/BENCHMARK_QUESTIONS.md` | 36 Benchmarkfragen, 24 Development + 12 Holdout |
| `expected/EXPECTED_RESULTS.md` | Erwartete Quellenauswahl und Verhalten je Frage |

Die zugehörigen Regelwerke liegen unter `docs/benchmark/`:

| Dokument | Zweck |
| --- | --- |
| [BENCHMARK_SOURCE_CONTRACT.md](../docs/benchmark/BENCHMARK_SOURCE_CONTRACT.md) | Was eine Benchmarkquelle sein darf |
| [BENCHMARK_PLAN.md](../docs/benchmark/BENCHMARK_PLAN.md) | Vergleichsvarianten V0, V1, V2 und Versuchsablauf |
| [EVALUATION_RUBRIC.md](../docs/benchmark/EVALUATION_RUBRIC.md) | Metriken, Schwellen, kritische Fehler |
| [BASELINE_PROTOCOL.md](../docs/benchmark/BASELINE_PROTOCOL.md) | Wie ein Lauf durchgeführt und erfasst wird |
| [DATASET_GOVERNANCE.md](../docs/benchmark/DATASET_GOVERNANCE.md) | Wie das Dataset gepflegt wird, ohne sich selbst zu betrügen |

## Zweck

Der Benchmark misst den späteren Retrieval-Pfad gegen eine **konstruierte
Grundwahrheit**. Auf produktiven Daten wäre das nicht möglich — dort weiß
niemand vorab, welche Quelle die richtige ist.

Geprüft werden vier Dinge:

1. **Findet das System die richtige Quelle?** (Retrieval)
2. **Beachtet es Autorität, Aktualität und Datenklasse?** (Policy)
3. **Erkennt es Widersprüche, ohne sie zu entscheiden?** (Konflikte)
4. **Schweigt es, wenn keine Evidenz vorliegt?** (Abstention)

## Provider-Neutralität

Der Benchmark ist **unabhängig von der Suchtechnologie**. Er funktioniert
gleichermaßen mit qmd, SQLite FTS, einem eigenen Hybridstack oder einem anderen
Anbieter — gemessen werden Ergebnis und Verhalten, nicht die Implementierung.

**Es wurde keine Suchsoftware ausgewählt.** qmd bleibt Evaluationskandidat mit
Prüfvorbehalt (OD-25).

Der Benchmark funktioniert außerdem **ohne Knowledge Graph** — dieser ist nicht
Teil des ersten Piloten (D-025).

## Was der Benchmark nicht ist

| Nicht | Warum |
| --- | --- |
| Produktiver Wissensbestand | Rein erfundene Inhalte |
| Beweis einer Suchimplementierung | Es existiert keine Suche |
| Ersatz für einen Realbestandstest | Synthetik hat andere Verteilungen |
| Trainingsmaterial | Ausdrücklich ausgeschlossen |
| Freigabe für vertrauliche Daten | `confidential` und `excluded-from-ai` sind hier Etiketten auf harmlosem Text |

## Kennzahlen des Datasets

| Kennzahl | Wert |
| --- | --- |
| Quellen | 24 |
| Projekte | 3 |
| Autoritätsklassen belegt | **A0 bis A6** (A0 als synthetisches Fixture) |
| Datenklassen belegt | `public`, `internal`, `confidential`, `excluded-from-ai` |
| `data_class: secret` | **0** — Secrets sind auch synthetisch verboten |
| Konfliktpaare | **5** (darunter A0 gegen A3 und A5) |
| Superseded oder stale | 5 |
| Datenschutzfixtures | 4 (davon 2 `excluded-from-ai`) |
| Tombstones | 1 |
| Fragen | 36 (24 Development, 12 Holdout) |

## Holdout

12 der 36 Fragen sind als **Holdout** markiert. Sie werden:

- **nicht** zur Auswahl von Suchgewichten oder Prompts verwendet,
- erst bei einer formalen Abschlussevaluation vollständig ausgewertet,
- weiterhin versioniert und prüfbar geführt.

Der Holdout ist **kein Sicherheitsgeheimnis** — er steht offen im Repository.
Er ist eine Selbstdisziplin gegen Überanpassung: wer alle Fragen zur
Optimierung nutzt, misst am Ende nur noch sich selbst.

## Status

**Nicht ausgeführt.** Es wurde kein Lauf durchgeführt, keine Metrik erhoben,
kein Index gebaut, keine Suchsoftware installiert. Dieses Dataset beschreibt,
**was** gemessen werden soll — nicht, was gemessen wurde.

Kein Ergebnis in `docs/benchmark/` ist eine Messung. Alle dort genannten
Zielwerte sind **vorläufig und benchmarkpflichtig**.
