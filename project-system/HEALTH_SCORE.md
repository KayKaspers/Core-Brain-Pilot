# Health Score – Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Letzte Bewertung | 2026-07-20, im Rahmen von CBP-WP-003 |
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
| Gate-Klarheit | **gut** | ↑ | Dreistufiges Kriterienmodell trennt Produkt-Scope von Installationsdetail |
| Scope-Klarheit | **ausreichend** | ↑↑ | Pilotumfang auf Profilebene entschieden; 12 A0-Entscheidungen |
| Entscheidungslage | **ausreichend** | ↑ | 26 getroffene Entscheidungen (zuvor 14); 10 P0 offen (zuvor 14) |
| Antwortlage Discovery | **ausreichend** | ↑↑ | 6 von 6 Intake-Fragen beantwortet; 8 Core-Required-Fragen offen |
| Sicherheitslage | **schwach** | ↓ | Berechtigungsmodell nicht erhoben; `excluded-from-ai` ungeprüft; Secret-Verfahren fehlt |
| Messbarkeit | **sehr schwach** | → | Keine der mindestens 30 Benchmarkfragen existiert |
| Kennzahlendisziplin | **ausreichend** | ↑ | Fehlerhafte Summen gefunden und korrigiert; Auszählung statt Fortschreibung |
| Implementierung | nicht bewertbar | | Kein Code |
| Testabdeckung | nicht bewertbar | | Kein Code |
| CI/CD | nicht bewertbar | | In Phase 0 verboten |
| Betriebsreife | nicht bewertbar | | Keine Installation |
| Retrieval-Qualität | nicht bewertbar | | Kein Index, kein Benchmark |
| Releasefähigkeit | nicht bewertbar | | Keine Lizenz, keine Implementierung |

**Zur Verschlechterung der Sicherheitslage:** Sie ist nicht eingetreten, sondern
**sichtbar geworden**. Der Intake hat gezeigt, dass das Berechtigungsmodell nie
erhoben wurde und das Secret-Verbot ohne Schadensverfahren dasteht. Bessere
Sicht auf denselben Zustand.

## Kennzahlen

> Sämtliche Werte **ausgezählt**, nicht fortgeschrieben. Die Spalte
> „CBP-WP-002" zeigt die damals berichteten Werte; kursive Angaben waren
> falsch addiert.

| Kennzahl | CBP-WP-002 | **CBP-WP-003** |
| --- | --- | --- |
| G0-Kriterien gesamt | *41* → korrekt 47 | **47** |
| davon blockierend | *39* → korrekt 45 | **25** (dreistufiges Modell) |
| davon `accepted` | 0 | **8** |
| davon `answered` | 0 | 4 |
| davon `open` | 47 | 13 |
| davon `not-applicable` | 0 | 2 |
| Core Required | — | 25 |
| Deployment Required | — | 16 |
| Conditional | — | 6 |
| Discovery-Fragen | *55* → korrekt 56 | **56** |
| davon P0 | *35* → korrekt 38 | **38** |
| davon P0 offen und Core Required | 38 | **8** |
| Getroffene Entscheidungen | 14 | **26** |
| davon A0 | 8 | **20** |
| Offene Entscheidungen | 27 | 25 |
| davon P0 | 14 | **10** |
| Erfasste Risiken | 29 | **32** |
| davon hoch | 14 | 17 |
| Capabilities `implemented` | **0** | **0** |
| Angenommene ADRs | 0 | 0 |
| Commits | 2 | 3 |

## Fortschritt in einem Bild

```text
G0-Blocker
CBP-WP-002:  ████████████████████████████████████████████  45
CBP-WP-003:  █████████████████████████                     25   (Modell)
             ████████                                       8   davon accepted
             █████████████████                             17   noch offen
```

Die Reduktion von 45 auf 25 stammt aus dem **Kriterienmodell**, nicht aus
beantworteten Fragen. Die Reduktion von 25 auf 19 stammt aus den Antworten.

## Wichtigste Hebel

| # | Hebel | Wirkung |
| --- | --- | --- |
| 1 | **Benchmarkfragen formulieren** | Sechs der 17 verbleibenden Blocker auf einen Schlag; ohne sie ist kein Erfolgskriterium messbar |
| 2 | **Berechtigungsmodell erheben** (OI-08) | Vier Blocker; entschärft R-25 und R-27, die schwersten offenen Sicherheitsrisiken |
| 3 | Secret-Verfahren festlegen (OI-09) | Ein Blocker; schließt die Lücke im ansonsten bestätigten Secret-Verbot |
| 4 | Repository-Sichtbarkeit und Nicht-Ziele (A-8) | Ein Blocker; hängt an OD-11 und OD-26 |
| 5 | Deployment-Readiness-Gate definieren (OD-33) | Verhindert, dass die 16 vertagten Kriterien vergessen werden (R-34) |

## Bewertung in einem Satz

Der Pilotumfang ist erstmals **entschieden** statt nur beschrieben; der Engpass
hat sich von „alles offen" zu drei klar benennbaren Blöcken verdichtet —
Benchmark, Berechtigungen, Secret-Verfahren.

## Pflege

Diese Bewertung wird bei jedem Work Package erneuert. Kennzahlen werden
ausgezählt, nicht aus dem Vorbericht übernommen (R-33).
