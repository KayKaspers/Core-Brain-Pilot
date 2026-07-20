# Health Score – Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Letzte Bewertung | 2026-07-20, im Rahmen von CBP-WP-002 |
| Autoritätsklasse | A2 |

> Diese Datei gehört zur kanonischen NDF-Ordnerstruktur, war aber in der
> Zielstruktur von CBP-WP-001 nicht aufgeführt — **AB-08**, vorläufig
> akzeptiert.

## Vorbemerkung

Ein Health Score misst die Gesundheit eines **laufenden** Projekts. Core Brain
Pilot hat keine Implementierung, keine Tests und kaum Historie. Die meisten
Dimensionen bleiben **nicht bewertbar** — das ist der erwartete Zustand in
Phase 0 und kein Mangel.

Es wird bewusst **keine** Gesamtpunktzahl gebildet.

## Dimensionen

| Dimension | Bewertung | Veränderung | Begründung |
| --- | --- | --- | --- |
| Dokumentation | **gut** | ↑ | Fundament gegen beide Originalquellen abgeglichen; 16 Ergänzungen, 5 Korrekturen |
| Prozesstreue | **gut** | → | NDF-Lifecycle eingehalten; zwei Vorprüfungen korrekt mit BLOCKED beendet, ohne Schaden |
| Quellenlage | **gut** | ↑↑ | Beide Originalquellen gelesen und abgeglichen; OI-01 geschlossen. Zuvor: Lücken |
| Gate-Klarheit | **ausreichend** | ↑↑ | 41 objektiv prüfbare Kriterien liegen vor. Zuvor: keine Kriterien |
| Entscheidungslage | **schwach** | → | 0 angenommene ADRs, 27 offene Entscheidungen, davon 14 mit P0 |
| Scope-Klarheit | **schwach** | ↑ | Capabilities priorisiert, Scope weiterhin nicht gelockt |
| Sicherheitslage | **teilweise** | ↑ | Sicherheitsmodell und Berechtigungsstufen dokumentiert; technische Kontrollen fehlen |
| Antwortlage Discovery | **sehr schwach** | → | 0 von 55 Fragen beantwortet |
| Implementierung | nicht bewertbar | | Kein Code vorhanden |
| Testabdeckung | nicht bewertbar | | Kein Code vorhanden |
| CI/CD | nicht bewertbar | | In Phase 0 verboten |
| Betriebsreife | nicht bewertbar | | Keine Installation |
| Retrieval-Qualität | nicht bewertbar | | Kein Index, kein Benchmark |
| Releasefähigkeit | nicht bewertbar | | Keine Lizenz, keine Implementierung |

## Kennzahlen

| Kennzahl | Wert | Vorher (CBP-WP-001) |
| --- | --- | --- |
| Capabilities gesamt | 29 | 29 |
| davon `implemented` | **0** | **0** |
| davon mit Priorität | **29** | 0 |
| davon **P0** | 17 | — |
| Angenommene ADRs | 0 | 0 |
| Getroffene Entscheidungen | 14 | 8 |
| Offene Entscheidungen | 27 | 24 |
| davon **P0** | 14 | — |
| G0-Kriterien | **41** | 0 |
| davon blockierend | 39 | — |
| davon beantwortet | **0** | — |
| Discovery-Fragen | 55 | 31 |
| davon **P0** | 35 | — |
| Erfasste Risiken | 29 | 21 |
| davon hoch | 14 | 8 |
| davon geschlossen | 2 | 0 |
| NDF-Abweichungen | 10 | 10 |
| davon entschieden | 3 (+1 aufgehoben) | 0 |
| Work Packages `committed` | 1 | 0 |
| Commits | 2 | 0 |

## Wichtigste Hebel

| # | Hebel | Wirkung |
| --- | --- | --- |
| 1 | **Die 35 P0-Fragen beantworten** (CBP-WP-003) | Der einzige Weg zu G0. Ohne Antworten bewegt sich nichts |
| 2 | Repository-Struktur entscheiden (OD-26) | Löst AB-03 bis AB-08 gemeinsam auf |
| 3 | Kernprinzipien als ADR ausfertigen (OD-03) | Hebt sie von A2 auf A1 und macht sie bindend |
| 4 | Benchmarkfragen formulieren (OI-06) | Ohne sie ist kein Erfolgskriterium messbar |
| 5 | Technische Durchsetzung der Datenklassen planen | Entschärft R-25 und R-30, die beiden schwersten offenen Risiken |

## Bewertung in einem Satz

Das **Fundament** ist in gutem Zustand und jetzt quellengestützt; die
**Entscheidungs- und Antwortlage** ist der Engpass, und sie lässt sich nur
durch den Human Maintainer auflösen.

## Pflege

Diese Bewertung wird bei jedem Work Package erneuert. Dimensionen wechseln von
„nicht bewertbar" auf eine Bewertung, sobald der zugehörige Gegenstand
existiert.
