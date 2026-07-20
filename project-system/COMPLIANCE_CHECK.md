# Compliance Check – Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Letzte Pruefung | 2026-07-20, im Rahmen von CBP-WP-001 |
| Autoritaetsklasse | A2 |

> Diese Datei gehoert zur kanonischen NDF-v1.0.0-Ordnerstruktur, ist in der
> Zielstruktur von CBP-WP-001 aber nicht aufgefuehrt. Sie wurde als Geruest
> angelegt — offengelegt in **AB-08** in
> [../docs/ndf/ADOPTION_NOTES.md](../docs/ndf/ADOPTION_NOTES.md).

## Prozess-Compliance (NDF v1.0.0)

| Pruefung | Ergebnis |
| --- | --- |
| Rollenmodell Nova → Agent → Human Maintainer eingehalten | erfuellt |
| Lifecycle vollstaendig durchlaufen | erfuellt bis `Report to Nova` |
| Genau ein Work Package ausgefuehrt | erfuellt |
| Work-Package-Typ `docs-only` eingehalten | erfuellt |
| Keine autonomen Commits oder Pushes | erfuellt |
| Abweichungen vom Framework dokumentiert | erfuellt (AB-01 bis AB-10) |
| Ausschliesslich Version v1.0.0 verwendet | erfuellt |
| Keine v1.1-Planung uebernommen | erfuellt |

## Scope-Compliance (CBP-WP-001)

| Pruefung | Ergebnis |
| --- | --- |
| Nur innerhalb `D:\Projects\Core-Brain-Pilot` gearbeitet | erfuellt |
| Keine benachbarten Ordner geoeffnet oder durchsucht | erfuellt |
| Nur Markdown, `.gitignore` und Ordner erzeugt | erfuellt |
| Kein ausfuehrbarer Anwendungscode | erfuellt |
| Kein Dockerfile, keine `compose.yaml` | erfuellt |
| Keine Skripte, keine CI-Workflows | erfuellt |
| Keine Datenbanken, Binaerdateien, Modellartefakte | erfuellt |
| Keine `LICENSE`-Datei | erfuellt |
| Kein Git-Remote, kein Commit, kein Push | erfuellt |

## Sicherheits-Compliance

| Pruefung | Ergebnis |
| --- | --- |
| Keine Secrets erzeugt, gelesen, gespeichert oder indexiert | erfuellt |
| Keine Beispiel-Secrets, keine `.env.example` | erfuellt |
| Keine Zugangsdaten oder privaten Schluessel | erfuellt |
| `.gitignore` deckt Secrets, Schluessel und `.env` ab | erfuellt |
| `.gitignore` deckt abgeleitete Daten und Context Packs ab | erfuellt |
| Datenklassen dokumentiert | erfuellt |

## Dokumentations-Compliance

| Pruefung | Ergebnis |
| --- | --- |
| Alle Statusdokumente nennen Phase 0 | erfuellt |
| Aktuelles Work Package als CBP-WP-001 ausgewiesen | erfuellt |
| Naechstes Gate als G0 – Discovery and Scope Lock ausgewiesen | erfuellt |
| Keine Capability als `implemented` bezeichnet | erfuellt |
| Keine parallelen doppelten Strukturen | erfuellt |

## Offene Punkte

| Punkt | Bezug |
| --- | --- |
| Gate-G0-Kriterien fehlen; Scope-Lock-Compliance nicht pruefbar | OI-04, OD-01 |
| Zwei verbindliche Eingangsquellen lagen nicht vor | OI-01, R-15 |
| Technische Datenschutzkontrollen sind dokumentiert, nicht durchgesetzt | R-02, R-03 |

## Pflege

Diese Pruefung wird bei jedem Work Package erneuert. Sie ersetzt weder das
Review durch den Human Maintainer noch die NDF Quality Gates.
