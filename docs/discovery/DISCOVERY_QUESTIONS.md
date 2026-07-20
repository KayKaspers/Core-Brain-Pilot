# Discovery Questions — Gate G0

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Naechstes Gate | G0 – Discovery and Scope Lock |
| Stand | 2026-07-20 |

Diese Fragen muessen vor dem Scope Lock beantwortet sein. Sie sind an den
**Human Maintainer** und an **Nova** gerichtet, nicht an den Implementation
Agent. Ein Agent beantwortet sie nicht durch Annahme.

Legende Prioritaet: **P1** blockiert G0 · **P2** vor Implementierung · **P3**
spaeter entscheidbar.

## Scope und Ziel

| # | Frage | Prio |
| --- | --- | --- |
| Q-01 | Was ist die kleinste Version, die im Alltag echten Nutzen bringt? | P1 |
| Q-02 | Woran wird "kleinste ausreichende Menge" gemessen — gibt es eine Zielmetrik? | P1 |
| Q-03 | Ist der Pilot fuer genau einen Nutzer gedacht, oder spaeter mehrere? | P1 |
| Q-04 | Welche Wissensquellen gehoeren in den ersten Scope, welche ausdruecklich nicht? | P1 |

## Wissensbestand

| # | Frage | Prio |
| --- | --- | --- |
| Q-05 | Wo liegt der kanonische Markdown-Bestand — im selben Repository oder getrennt? | P1 |
| Q-06 | Ist der Wissensbestand oeffentlich, privat oder gemischt? | P1 |
| Q-07 | Wie ist eine Wissenseinheit geschnitten — Datei, Abschnitt, Block? | P2 |
| Q-08 | Wie wird eine stabile Source-ID gebildet, sodass sie Umbenennung ueberlebt? | P2 |
| Q-09 | Welche Frontmatter-Felder sind verpflichtend? | P2 |

## Autoritaet und Konflikte

| # | Frage | Prio |
| --- | --- | --- |
| Q-10 | Wie wird eine Autoritaetsklasse vergeben — manuell, aus Pfad, aus Frontmatter? | P1 |
| Q-11 | Was passiert bei zwei widersprechenden Quellen gleicher Klasse? | P2 |
| Q-12 | Wann gilt Wissen als veraltet — feste Frist oder pro Quelle? | P2 |
| Q-13 | Wie wird Supersession ausgedrueckt und geprueft? | P2 |

## Datenschutz

| # | Frage | Prio |
| --- | --- | --- |
| Q-14 | Wer vergibt Datenklassen, und wann? | P1 |
| Q-15 | Welche Rechtsgrundlage gilt fuer personenbezogene Daten im Bestand? | P1 |
| Q-16 | Welches Verfahren gilt, wenn doch ein Secret in die Historie gelangt? | P1 |
| Q-17 | Erfolgt PII-Erkennung automatisch, manuell oder beides? | P2 |

## Retrieval

| # | Frage | Prio |
| --- | --- | --- |
| Q-18 | Was bedeuten B0 bis B4 konkret — Token, Dokumente, Zeichen? | P1 |
| Q-19 | Was genau ist "Brain-First" — welche Ebene wird zuerst befragt? | P2 |
| Q-20 | Welche Reihenfolge haben Autoritaets-, Datenschutz- und Aktualitaetsfilter? | P2 |
| Q-21 | Welchen Umfang und welches Format hat der Retrieval-Trace? | P2 |
| Q-22 | Wie wird Retrieval-Qualitaet gemessen — welche Benchmarks? | P2 |

## Betrieb

| # | Frage | Prio |
| --- | --- | --- |
| Q-23 | Wie kommen mehrere Geraete an den Bestand — Sync, Server, VPN? | P2 |
| Q-24 | Welche Ausfallzeit ist akzeptabel? | P3 |
| Q-25 | Wie oft wird gesichert, und wohin? | P2 |
| Q-26 | Wie wird ein Rebuild ausgeloest und verifiziert? | P2 |
| Q-27 | Wie wird Mehrschreiberzugriff verhindert oder aufgeloest? | P2 |

## Projektorganisation

| # | Frage | Prio |
| --- | --- | --- |
| Q-28 | Welche Lizenz gilt? (Bis dahin keine `LICENSE`-Datei.) | P2 |
| Q-29 | Bleibt das Repository dauerhaft privat? | P1 |
| Q-30 | Wird das NDF-`project-system`-Namensschema uebernommen oder abgewichen? | P2 |
| Q-31 | Welche Kriterien schliessen G0 ab? | P1 |

## Bearbeitung

Beantwortete Fragen werden **nicht geloescht**. Die Antwort wird ergaenzt, und
bei bindender Wirkung entsteht ein ADR in
[docs/decisions/](../decisions/README.md).
