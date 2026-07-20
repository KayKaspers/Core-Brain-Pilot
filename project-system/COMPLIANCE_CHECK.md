# Compliance Check – Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Letzte Prüfung | 2026-07-20, im Rahmen von CBP-WP-002 |
| Autoritätsklasse | A2 |

> Diese Datei gehört zur kanonischen NDF-Ordnerstruktur, war aber in der
> Zielstruktur von CBP-WP-001 nicht aufgeführt — **AB-08**, vorläufig
> akzeptiert.

## Prozess-Compliance (NDF v1.0.0)

| Prüfung | Ergebnis |
| --- | --- |
| Rollenmodell Nova → Agent → Human Maintainer eingehalten | erfüllt |
| Lifecycle vollständig durchlaufen | erfüllt bis `Report to Nova` |
| Genau ein Work Package ausgeführt | erfüllt |
| Work-Package-Typ `docs-only` eingehalten | erfüllt |
| Keine autonomen Commits oder Pushes | erfüllt |
| Abweichungen dokumentiert | erfüllt (AB-01 bis AB-10) |
| Ausschließlich Version v1.0.0 verwendet | erfüllt |
| Keine v1.1-Planung übernommen | erfüllt |
| Kein zweites Governance-System eingeführt | erfüllt |
| Vorprüfung vor jeder Änderung durchgeführt | erfüllt — zwei Versuche endeten korrekt mit BLOCKED |

## Scope-Compliance (CBP-WP-002)

| Prüfung | Ergebnis |
| --- | --- |
| Nur innerhalb `D:\Projects\Core-Brain-Pilot` geschrieben | erfüllt |
| Quelldateien außerhalb nur lesend geöffnet | erfüllt |
| Keine benachbarten Projekte durchsucht | erfüllt |
| Nur Markdown erzeugt und geändert | erfüllt |
| Kein ausführbarer Anwendungscode | erfüllt |
| Kein Dockerfile, keine `compose.yaml` | erfüllt |
| Keine Skripte, keine CI-Workflows | erfüllt |
| Keine Datenbanken, Suchindizes, Embeddings | erfüllt |
| Kein Wiki-Ingest, kein Graph | erfüllt |
| Keine `LICENSE`-Datei | erfüllt |
| Kein Remote-Wechsel, kein neuer Branch | erfüllt |
| Kein Commit, kein Push | erfüllt |
| Keine Softwareinstallation | erfüllt |

## Quellen-Compliance

| Prüfung | Ergebnis |
| --- | --- |
| A5-Übergabe als getrackte Quelle vorhanden | erfüllt |
| Fachlicher Inhalt der A5-Übergabe nicht umgeschrieben | erfüllt — nur Metadatenkopf vorangestellt |
| PDF als Originalquelle (A4) geführt | erfüllt |
| Textfassung ausdrücklich als A6 geführt | erfüllt |
| A6 beansprucht keine höhere Autorität als A4 | erfüllt |
| Seitenreferenzen ausschließlich Seite 1 bis 6 | erfüllt |
| Keine visuelle PDF-Prüfung behauptet | erfüllt — ausdrücklich verneint |
| Keine langen Volltextkopien der Quellen | erfüllt |
| OI-01 nur nach dokumentierter Provenienz geschlossen | erfüllt |
| Originalquellen nicht automatisch verändert | erfüllt |

## Sicherheits-Compliance

| Prüfung | Ergebnis |
| --- | --- |
| Keine Secrets erzeugt, gelesen, gespeichert oder indexiert | erfüllt |
| Keine Beispiel-Secrets, keine `.env.example` | erfüllt |
| Keine Zugangsdaten oder privaten Schlüssel | erfüllt |
| `.gitignore` deckt Secrets, Schlüssel und `.env` ab | erfüllt |
| `.gitignore` deckt abgeleitete Daten und Context Packs ab | erfüllt |
| Datenklassen mit Flussmatrix dokumentiert | erfüllt |
| Sicherheitsmodell mit Berechtigungsstufen dokumentiert | erfüllt |

## Dokumentations-Compliance

| Prüfung | Ergebnis |
| --- | --- |
| Alle Statusdokumente nennen Phase 0 | erfüllt |
| Aktuelles Work Package als CBP-WP-002 ausgewiesen | erfüllt |
| Nächstes Gate als G0 – Discovery and Scope Lock ausgewiesen | erfüllt |
| **G0 als NOT PASSED ausgewiesen** | **erfüllt** |
| Keine Capability als `implemented` bezeichnet | erfüllt |
| Alle Capabilities besitzen eine Priorität | erfüllt |
| Keine parallelen doppelten Strukturen | erfüllt |
| AB-03 bis AB-08 nicht stillschweigend dauerhaft akzeptiert | erfüllt |
| Keine offene Entscheidung als A0 ausgegeben | erfüllt |
| Keine Discovery-Frage durch Annahme beantwortet | erfüllt |
| UTF-8 mit echten deutschen Umlauten | erfüllt |

## Offene Punkte

| Punkt | Bezug |
| --- | --- |
| Technische Datenschutzkontrollen dokumentiert, nicht durchgesetzt | R-02, R-03, R-30 |
| Berechtigungen nur als Regel, nicht technisch | R-25 |
| Kein Kriterium von G0 beantwortet | G0_SCOPE_LOCK_CRITERIA |
| Repository-Struktur nicht freigegeben | OI-07, OD-26 |
| PDF nur über A6-Repräsentation ausgewertet | R-22, R-23 |

## Pflege

Diese Prüfung wird bei jedem Work Package erneuert. Sie ersetzt weder das
Review durch den Human Maintainer noch die NDF Quality Gates.
