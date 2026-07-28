# Health Score – Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | **Phase 0 COMPLETE** · Phase 1 AUTHORIZED FOR PLANNING |
| Letzte Bewertung | 2026-07-27, im Rahmen von **CBP-WP-016** |
| Autoritätsklasse | A2 |

> Diese Datei gehört zur kanonischen NDF-Ordnerstruktur, war aber in der
> Zielstruktur von CBP-WP-001 nicht aufgeführt — **AB-08**, vorläufig
> akzeptiert.

## Vorbemerkung

Ein Health Score misst die Gesundheit eines **laufenden** Projekts. Core Brain
Pilot hat seit CBP-WP-012 einen lokalen Runtime Skeleton mit Tests, aber keine
operative Implementierung. Die meisten Dimensionen bleiben **nicht bewertbar** —
der erwartete Zustand am Beginn von Phase 1.

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
| Entscheidungslage | **gut** | ↑ | **50 Entscheidungen, 12 angenommene ADRs**; G0, OD-26, Mappingkonvention, Sicherheitsgrundlage, Quarantäne-, Registry-, Mapping-Draft-Validator- und Gate-Evaluator-MVP (D-050) entschieden |
| Quellenanbindung | **nicht bewertbar** | | Konvention entschieden, **0 Mappings, 0 angebundene Quellen** |
| Strukturklarheit | **gut** | ↑↑ | Zielstruktur und Bereichsgrenze festgelegt (ADR-0007); zuvor drei konkurrierende Vorstellungen |
| Antwortlage Discovery | **gut** | ↑ | Alle Core-Required-Fragen belegt; Entscheidung steht aus |
| Sicherheitslage | **ausreichend** | → | Berechtigungsmodell, Incident-Response und **zwölf abnehmbare Kontrollbereiche** dokumentiert (ADR-0004, ADR-0009); **technisch weiterhin nicht durchgesetzt** — alle auf `DOCUMENTED ONLY` |
| Messbarkeit | **ausreichend** | ↑↑ | 36 Fragen, 4 Metrikgruppen, 7 kritische Fehler, Governance. **Nichts gemessen** |
| Kennzahlendisziplin | **ausreichend** | ↑ | Fehlerhafte Summen gefunden und korrigiert; Auszählung statt Fortschreibung |
| Planungsklarheit Phase 1 | **gut** | ↑↑ | Fünf Streams, sechs geschnittene Work Packages, Nachweisstufen und zwölf Stop-Bedingungen; zuvor nur ein Backlog |
| **Nachweislage** | **schwach** | → | **Alle Artefakte stehen auf Stufe 1 `dokumentiert`.** Kein Negativtest, kein Restore, kein Messwert |
| Implementierung | **schwach** | ↑ | **Lokaler Runtime Skeleton** (CBP-WP-012), **Quarantäneprototyp** (CBP-WP-013), **Registry-Prototyp** (CBP-WP-014), **Mapping-Draft-Validator** (CBP-WP-015) **und Gate-Evaluator** (CBP-WP-016); keine operative Wirkung, keine KB-Kontrolle durchgesetzt, keine Promotion, kein gespeichertes Mapping, kein Gate ausgeführt, keine Aktivierung |
| Testabdeckung | **ausreichend** | ↑↑ | **398 lokale Tests bestanden** (Skeleton 69 + Quarantäne + Registry + Mapping-Draft-Validator + Gate-Evaluator inkl. `mapping_id`-Fail-Closed-Vertrag, inkl. Netzwerk-Guard); kein Retrieval-, Ingest- oder Integrationstest |
| CI/CD | nicht bewertbar | | In Phase 0 verboten; lokale Tests manuell |
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

| Kennzahl | CBP-WP-002 | **CBP-WP-016** |
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
| davon P0 offen und Core Required | 38 | **0** |
| Getroffene Entscheidungen | 14 | **50** |
| davon A0 | 8 | **46** |
| Offene Entscheidungen | 27 | **23** |
| davon P0 | 14 | **5** |
| Erfasste Risiken | 29 | **32** |
| davon gemindert | 5 | **14** |
| davon hoch | 14 | 17 |
| Capabilities `implemented` | **0** | **0** |
| Angenommene ADRs | 0 | **12** |
| Vorgeschlagene Work Packages | 0 | **0** — CBP-WP-016 ist `committed` (`04c427c`, D-050) |
| **Erstellte Source Mappings** | 0 | **0** |
| **Angebundene Quellen** | 0 | **0** |
| **Umgesetzte Sicherheitskontrollen** | 0 | **0 von 12** |
| **Ausgeführte Sicherheits-Negativtests** | 0 | **0 von 32** |
| **Nachweise oberhalb Stufe 1** | 0 | **0** |
| **Runtime-Module (Skeleton)** | 0 | **9** |
| **Bestandene lokale Tests** | 0 | **69** |
| Commits | 2 | **12** |

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
| 1 | **Technische Sicherheitsgrundlage — Durchsetzung** | **P3** | Der breiteste Enabler. Spezifikation liegt vor (ADR-0009), **Runtime Skeleton lokal** (CBP-WP-012). Es fehlt die **Durchsetzung von KB-01…KB-12 auf der Ziel-VM**. Schließt R-25, R-26, R-27 erst bei Nachweisstufe 4 |
| 2 | Konkrete Quellenauswahl | P2 | OD-26 geschlossen, **Mappingkonvention entschieden** (CBP-WP-010). Verbleibend: **OD-05 und OD-06** — brauchen eine Human-Eingabe |
| 3 | `excluded-from-ai`-Negativtests | P8 | Auflage 2; macht aus einer behaupteten Sperre eine geprüfte |
| 4 | Benchmarklauf V0/V1 | P7 | Auflage 3; kalibriert OD-02b, schließt R-21 |
| 5 | Restore-Test und DRC Profil A | P9, P10 | Auflagen 4 und 5; R-20 und R-34 |
## Bewertung in einem Satz

Phase 0 ist abgeschlossen, Phase 1 geplant, alle Architekturentscheidungen
getroffen, und mit CBP-WP-012 existiert **erstmals lauffähiger, getesteter
Code** — ein fail-closed Skeleton. Der Score misst von hier an den Fortschritt
von **Nachweisen**: Der Skeleton belegt drei lokale Bausteine, aber **keine der
zwölf Sicherheitskontrollen ist auf der Ziel-VM durchgesetzt**, und kein Gate
ist bestanden.

**Alles Entscheidbare ist entschieden.** Was bleibt, ist zu bauen und zu
beweisen — und das beginnt frühestens mit CBP-WP-012.
## Pflege

Diese Bewertung wird bei jedem Work Package erneuert. Kennzahlen werden
ausgezählt, nicht aus dem Vorbericht übernommen (R-33).
