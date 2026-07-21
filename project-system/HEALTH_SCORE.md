# Health Score – Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | **Phase 0 COMPLETE** · Phase 1 AUTHORIZED FOR PLANNING |
| Letzte Bewertung | 2026-07-21, im Rahmen von CBP-WP-007 |
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
| Scope-Klarheit | **gut** | ↑ | **Alle 25 Core-Kriterien `accepted`**; Quellenraum über logische Slots definiert |
| Entscheidungslage | **gut** | ↑ | 28 Entscheidungen, **6 angenommene ADRs**; G0 und ADR-0006 entschieden |
| Antwortlage Discovery | **gut** | ↑ | Alle Core-Required-Fragen belegt; Entscheidung steht aus |
| Sicherheitslage | **ausreichend** | ↑ | Berechtigungsmodell und Incident-Response dokumentiert (ADR-0004); **technisch weiterhin nicht durchgesetzt** |
| Messbarkeit | **ausreichend** | ↑↑ | 36 Fragen, 4 Metrikgruppen, 7 kritische Fehler, Governance. **Nichts gemessen** |
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

| Kennzahl | CBP-WP-002 | **CBP-WP-007** |
| --- | --- | --- |
| G0-Kriterien gesamt | *41* → korrekt 47 | **47** |
| davon blockierend | *39* → korrekt 45 | **25** (dreistufiges Modell) |
| davon `accepted` | 0 | **25** |
| davon `answered` | 0 | **0** |
| davon `open` | 47 | **0** |
| davon `not-applicable` | 0 | 2 |
| Core Required | — | 25 |
| Deployment Required | — | 16 |
| Conditional | — | 6 |
| Discovery-Fragen | *55* → korrekt 56 | **56** |
| davon P0 | *35* → korrekt 38 | **38** |
| davon P0 offen und Core Required | 38 | **8** |
| Getroffene Entscheidungen | 14 | **28** |
| davon A0 | 8 | **22** |
| Offene Entscheidungen | 27 | **21** |
| davon P0 | 14 | **8** |
| Erfasste Risiken | 29 | **32** |
| davon gemindert | 5 | **14** |
| davon hoch | 14 | 17 |
| Capabilities `implemented` | **0** | **0** |
| Angenommene ADRs | 0 | **6** |
| Commits | 2 | 7 |

## Fortschritt in einem Bild

```text
Verbleibende G0-Blocker
CBP-WP-002:  ████████████████████████████████████████████  45
CBP-WP-003:  █████████████████                             17
CBP-WP-004:  ███████                                        7
CBP-WP-005:  █                                              1   ← D-1
CBP-WP-006:                                                 0   Kriterien vollständig
CBP-WP-007:                                                 —   ► GATE PASSED WITH NOTES
```

Die Reduktion von 45 auf 25 stammte aus dem **Kriterienmodell**. Von 25 auf 17
aus den **Intake-Antworten**. Von 17 auf 7 aus den **Architektur- und
Sicherheitsdokumenten**. Von 7 auf 1 aus dem **Benchmarkdesign**. Von 1 auf 0
aus dem **Quellenvertrag**.

> **Diese Kurve misst dokumentarische Vollständigkeit, nicht Systemreife.**
>
> **Sechzehn der 25 angenommenen Kriterien beschreiben Kontrollen, die nicht
> existieren.** Sie sind nachprüfbare Absichten, keine funktionierenden
> Mechanismen. Der Sprung von 45 auf 0 bedeutet: das Projekt weiß, was es bauen
> will, und kann es prüfen. **Gebaut ist nichts.**
>
> **Null Blocker war nicht gleich Gate bestanden.** Die Freigabe erfolgte
> gesondert am 2026-07-21 durch den Human Maintainer — **PASSED WITH NOTES**,
> mit fünf Nachweisauflagen vor produktivem Betrieb.

## Wichtigste Hebel

Nach der G0-Entscheidung verschiebt sich der Engpass von Dokumentation auf
Umsetzung. Reihenfolge nach dem [Phase-1-Backlog](../docs/roadmap/PHASE_1_BACKLOG.md):

| # | Hebel | Backlog | Wirkung |
| --- | --- | --- | --- |
| 1 | **Technische Sicherheitsgrundlage** | **P3** | Der breiteste Enabler — P4, P8 und P10 hängen daran. Schließt R-25 und R-27 |
| 2 | Repository-Entscheidung und Source Mapping | P1, P2 | Schließt OD-26, OD-05 und OD-06 |
| 3 | `excluded-from-ai`-Negativtests | P8 | Auflage 2; macht aus einer behaupteten Sperre eine geprüfte |
| 4 | Benchmarklauf V0/V1 | P7 | Auflage 3; kalibriert OD-02b, schließt R-21 |
| 5 | Restore-Test und DRC Profil A | P9, P10 | Auflagen 4 und 5; R-20 und R-34 |
## Bewertung in einem Satz

Phase 0 ist **abgeschlossen und freigegeben** — von hier an misst dieser Score
nicht mehr die Vollständigkeit von Dokumenten, sondern den Fortschritt von
**Nachweisen**, und der steht bei null.
## Pflege

Diese Bewertung wird bei jedem Work Package erneuert. Kennzahlen werden
ausgezählt, nicht aus dem Vorbericht übernommen (R-33).
