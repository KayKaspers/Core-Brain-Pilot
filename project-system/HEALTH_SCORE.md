# Health Score – Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Letzte Bewertung | 2026-07-20, im Rahmen von CBP-WP-004 |
| Autoritätsklasse | A2 |

> Diese Datei gehört zur kanonischen NDF-Ordnerstruktur, war aber in der
> Zielstruktur von CBP-WP-001 nicht aufgeführt — **AB-08**, vorläufig
> akzeptiert.

## Vorbemerkung

Ein Health Score misst die Gesundheit eines **laufenden** Projekts. Core Brain
Pilot hat keine Implementierung und keine Tests. Die meisten Dimensionen
bleiben **nicht bewertbar** — der erwartete Zustand in Phase 0.

Keine Gesamtpunktzahl.

## Dimensionen

| Dimension | Bewertung | Veränderung | Begründung |
| --- | --- | --- | --- |
| Dokumentation | **gut** | → | Fundament quellengestützt, Intake dokumentiert |
| Prozesstreue | **gut** | → | Nova-REWORK sauber umgesetzt; keine Datei vor der Antwort verändert |
| Quellenlage | **gut** | → | Beide Originalquellen abgeglichen; Human-Evidenz ergänzt |
| Gate-Klarheit | **gut** | → | Dreistufiges Modell plus DRC als eigener Prüfort für die 16 vertagten Kriterien |
| Architekturklarheit | **gut** | ↑↑ | 9 Schichten, 14 Komponenten, 5 Profile, Rebuild-Vertrag; zuvor kein Komponentenschnitt |
| Scope-Klarheit | **ausreichend** | ↑↑ | Pilotumfang auf Profilebene entschieden; 12 A0-Entscheidungen |
| Entscheidungslage | **gut** | ↑↑ | 26 Entscheidungen und **5 angenommene ADRs** (A1); 8 P0 offen (zuvor 10) |
| Antwortlage Discovery | **ausreichend** | ↑↑ | 6 von 6 Intake-Fragen beantwortet; 8 Core-Required-Fragen offen |
| Sicherheitslage | **ausreichend** | ↑ | Berechtigungsmodell und Incident-Response dokumentiert (ADR-0004); **technisch weiterhin nicht durchgesetzt** |
| Messbarkeit | **sehr schwach** | → | Keine der mindestens 30 Benchmarkfragen existiert |
| Kennzahlendisziplin | **ausreichend** | ↑ | Fehlerhafte Summen gefunden und korrigiert; Auszählung statt Fortschreibung |
| Implementierung | nicht bewertbar | | Kein Code |
| Testabdeckung | nicht bewertbar | | Kein Code |
| CI/CD | nicht bewertbar | | In Phase 0 verboten |
| Betriebsreife | nicht bewertbar | | Keine Installation |
| Retrieval-Qualität | nicht bewertbar | | Kein Index, kein Benchmark |
| Releasefähigkeit | nicht bewertbar | | Keine Lizenz, keine Implementierung |

**Zur Sicherheitslage:** In CBP-WP-003 auf `schwach` gefallen, weil der Intake
sichtbar machte, dass das Berechtigungsmodell nie erhoben war. In CBP-WP-004
auf `ausreichend` gestiegen, weil das Modell nun vollständig dokumentiert ist —
**nicht**, weil es wirkt. Von `ausreichend` auf `gut` führt nur technische
Durchsetzung, nicht ein weiteres Dokument.

## Kennzahlen

> Sämtliche Werte **ausgezählt**, nicht fortgeschrieben. Die Spalte
> „CBP-WP-002" zeigt die damals berichteten Werte; kursive Angaben waren
> falsch addiert.

| Kennzahl | CBP-WP-002 | **CBP-WP-004** |
| --- | --- | --- |
| G0-Kriterien gesamt | *41* → korrekt 47 | **47** |
| davon blockierend | *39* → korrekt 45 | **25** (dreistufiges Modell) |
| davon `accepted` | 0 | **18** |
| davon `answered` | 0 | **1** |
| davon `open` | 47 | **6** |
| davon `not-applicable` | 0 | 2 |
| Core Required | — | 25 |
| Deployment Required | — | 16 |
| Conditional | — | 6 |
| Discovery-Fragen | *55* → korrekt 56 | **56** |
| davon P0 | *35* → korrekt 38 | **38** |
| davon P0 offen und Core Required | 38 | **8** |
| Getroffene Entscheidungen | 14 | **26** |
| davon A0 | 8 | **20** |
| Offene Entscheidungen | 27 | **21** |
| davon P0 | 14 | **8** |
| Erfasste Risiken | 29 | **32** |
| davon hoch | 14 | 17 |
| Capabilities `implemented` | **0** | **0** |
| Angenommene ADRs | 0 | **5** |
| Commits | 2 | 4 |

## Fortschritt in einem Bild

```text
Verbleibende G0-Blocker
CBP-WP-002:  ████████████████████████████████████████████  45
CBP-WP-003:  █████████████████                             17
CBP-WP-004:  ███████                                        7
             ██████ Benchmark (G-1…G-6)
             █ D-1 konkreter Quellenbestand
```

Die Reduktion von 45 auf 25 stammte aus dem **Kriterienmodell**. Von 25 auf 17
aus den **Intake-Antworten**. Von 17 auf 7 aus den **Architektur- und
Sicherheitsdokumenten** dieses Work Packages.

## Wichtigste Hebel

| # | Hebel | Wirkung |
| --- | --- | --- |
| 1 | **Benchmarkfragen formulieren** | **Sechs der sieben** verbleibenden Blocker auf einen Schlag. Der einzige noch geschlossene Bereich |
| 2 | Quellenbestand festlegen (OD-05, OD-06) | Der siebte Blocker D-1; Voraussetzung für sinnvolle Benchmarkfragen |
| 3 | Berechtigungen **technisch** umsetzen | Kein G0-Blocker mehr, aber R-25 und R-27 bleiben die schwersten offenen Risiken |
| 4 | Repository-Layout entscheiden (OD-26) | Löst AB-03 bis AB-08 gemeinsam auf; Vorlage liegt vor |
| 5 | DRC durchführen | Von NOT EVALUATED zu einer belastbaren Aussage über die Installierbarkeit |

## Bewertung in einem Satz

Die Architektur ist von „Prinzipien ohne Komponentenschnitt" auf ein
belastbares logisches Modell gesprungen, und der G0-Rest ist auf **einen
einzigen Block** zusammengeschrumpft — den Benchmark.

## Pflege

Diese Bewertung wird bei jedem Work Package erneuert. Kennzahlen werden
ausgezählt, nicht aus dem Vorbericht übernommen (R-33).
