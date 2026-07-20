# Health Score – Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Letzte Bewertung | 2026-07-20, im Rahmen von CBP-WP-001 |
| Autoritaetsklasse | A2 |

> Diese Datei gehoert zur kanonischen NDF-v1.0.0-Ordnerstruktur, ist in der
> Zielstruktur von CBP-WP-001 aber nicht aufgefuehrt. Sie wurde als Geruest
> angelegt — offengelegt in **AB-08** in
> [../docs/ndf/ADOPTION_NOTES.md](../docs/ndf/ADOPTION_NOTES.md).

## Vorbemerkung

Ein Health Score misst die Gesundheit eines **laufenden** Projekts. Core Brain
Pilot hat keine Implementierung, keine Tests und keine Historie. Die meisten
Dimensionen sind daher **nicht bewertbar** — das ist der erwartete Zustand in
Phase 0 und kein Mangel.

Es wird bewusst **keine** Gesamtpunktzahl gebildet. Eine Zahl aus ueberwiegend
nicht bewertbaren Dimensionen waere irrefuehrend.

## Dimensionen

| Dimension | Bewertung | Begruendung |
| --- | --- | --- |
| Dokumentation | **gut** | Fundament vollstaendig, Struktur an NDF ausgerichtet, Abweichungen begruendet |
| Prozesstreue | **gut** | NDF-Lifecycle eingehalten, keine autonomen Commits, Scope respektiert |
| Entscheidungslage | **schwach** | 0 angenommene ADRs, 24 offene Entscheidungen, davon 11 mit P1 |
| Scope-Klarheit | **schwach** | Scope nicht gelockt, 29 Capabilities unpriorisiert, G0-Kriterien fehlen |
| Sicherheitslage | **teilweise** | Regelwerk dokumentiert, `.gitignore` wirksam, technische Kontrollen fehlen |
| Eingangsinformation | **luecken** | Zwei von vier verbindlichen Quellen lagen nicht vor (OI-01) |
| Implementierung | nicht bewertbar | Kein Code vorhanden |
| Testabdeckung | nicht bewertbar | Kein Code vorhanden |
| CI/CD | nicht bewertbar | In Phase 0 verboten |
| Betriebsreife | nicht bewertbar | Keine Installation |
| Retrieval-Qualitaet | nicht bewertbar | Kein Index, kein Benchmark |
| Releasefaehigkeit | nicht bewertbar | Keine Lizenz, keine Implementierung |

## Kennzahlen

| Kennzahl | Wert |
| --- | --- |
| Capabilities gesamt | 29 |
| davon `implemented` | **0** |
| davon `planned` | 20 |
| davon `discovery` | 6 |
| davon `not-started` | 3 |
| Angenommene ADRs | 0 |
| Offene Entscheidungen | 24 (davon 11 mit P1) |
| Offene Discovery-Fragen | 31 (davon 11 mit P1) |
| Erfasste Risiken | 21 (davon 8 hoch) |
| Dokumentierte NDF-Abweichungen | 10 |
| Work Packages abgeschlossen | 0 (CBP-WP-001 im Review) |
| Commits | 0 |

## Wichtigste Hebel

| # | Hebel | Wirkung |
| --- | --- | --- |
| 1 | Gate-G0-Kriterien definieren (OD-01) | Macht den Scope Lock ueberhaupt pruefbar |
| 2 | Minimal nuetzlichen Umfang festlegen (OD-04) | Entschaerft R-13, die Scope-Ueberdehnung |
| 3 | Fehlende Eingangsquellen nachreichen (OI-01) | Schliesst die groesste Wissensluecke |
| 4 | Kernprinzipien als ADR ausfertigen (OD-03) | Hebt sie von A2 auf A1 und macht sie bindend |

## Pflege

Diese Bewertung wird bei jedem Work Package erneuert. Dimensionen wechseln von
"nicht bewertbar" auf eine Bewertung, sobald der zugehoerige Gegenstand
existiert.
