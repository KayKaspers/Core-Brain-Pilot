# Compliance Check – Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Letzte Prüfung | 2026-07-20, im Rahmen von CBP-WP-003 |
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
| Nova-REWORK der Phase A umgesetzt | erfüllt — Fragebogen ersetzt, nicht ergänzt |
| Ausschließlich Version v1.0.0 verwendet | erfüllt |
| Kein zweites Governance-System | erfüllt |
| Vorprüfung vor jeder Änderung | erfüllt |

## Scope-Compliance (CBP-WP-003)

| Prüfung | Ergebnis |
| --- | --- |
| Nur Markdown innerhalb `D:\Projects\Core-Brain-Pilot` | erfüllt |
| Keine weiteren Dateitypen | erfüllt |
| Nur erlaubte Dokumentdateien geändert | erfüllt |
| `PROJECT_DEFINITION.md` **nicht** geändert, obwohl D-016 es erfordert | erfüllt — außerhalb der Erlaubnisliste, als OD-31 erfasst |
| Kein Anwendungscode, kein Dockerfile, keine `compose.yaml` | erfüllt |
| Keine Skripte, CI/CD, GitHub Actions | erfüllt |
| Keine Datenbanken, Suchindex, Embeddings, Modelle | erfüllt |
| Kein Wiki-Ingest, Graph, MCP | erfüllt |
| Keine Softwareinstallation, keine Infrastrukturänderung | erfüllt |
| Keine `LICENSE`, kein Branch, keine Remote-Änderung | erfüllt |
| Kein Commit, kein Push, keine Issues, keine Releases | erfüllt |

## Intake-Compliance

| Prüfung | Ergebnis |
| --- | --- |
| Fragebogen deckt alle P0-Fragen ab | erfüllt — Fassung 1 deckte alle 38; Fassung 2 erhebt bewusst auf Profilebene |
| Keine unbeantwortete Frage ergänzt | erfüllt |
| Keine Antwort inhaltlich erweitert | erfüllt |
| Alle Antworten ihren IDs zugeordnet | erfüllt |
| `accepted` nur bei ausdrücklicher Entscheidung | erfüllt — 12 A0-Entscheidungen einzeln benannt |
| Infrastrukturangaben nicht pauschal als A0 | erfüllt — HDI trägt A2, nur einzelne Punkte A0 |
| Keine Entscheidung aus reinen Fakten abgeleitet | erfüllt |
| Keine Secrets erfragt oder gespeichert | erfüllt |
| Keine IP-Pläne oder Konfigurationsdetails erfragt | erfüllt |
| Keine Rechtsgrundlage ohne PII-Bezug erfragt | erfüllt — D-022 stellt PII außerhalb des Pilots |

## Gate-Compliance

| Prüfung | Ergebnis |
| --- | --- |
| **G0 bleibt NOT PASSED** | **erfüllt** |
| Kein neuer Gate-Name eingeführt | erfüllt — Deployment-Readiness-Gate nur als zu definierende Aufgabe benannt |
| Kriterienklassen gekennzeichnet | erfüllt — Core 25, Deployment 16, Conditional 6 |
| Deployment-Kriterien vertagt, nicht gestrichen | erfüllt — alle 16 bleiben `open` und erfasst |
| Fail-closed für fehlende Deploymentangaben dokumentiert | erfüllt |
| Offene P0-Fragen bleiben sichtbar | erfüllt |
| Blocker ausdrücklich markiert | erfüllt |
| Kein Scope Lock automatisch ausgesprochen | erfüllt |
| Keine Benchmarkfragen erfunden | erfüllt — G-1 bis G-6 bleiben `open` |

## Sicherheits-Compliance

| Prüfung | Ergebnis |
| --- | --- |
| Keine Secrets erzeugt, gelesen, gespeichert oder indexiert | erfüllt |
| Keine Zugangsdaten oder privaten Schlüssel | erfüllt |
| Standardwert „Übertragung an externe KI verweigert" dokumentiert | erfüllt |
| `excluded-from-ai` von Anfang an im Modell gefordert | erfüllt (D-021) |

## Dokumentations-Compliance

| Prüfung | Ergebnis |
| --- | --- |
| Alle Statusdokumente nennen Phase 0 | erfüllt |
| Aktuelles Work Package als CBP-WP-003 ausgewiesen | erfüllt |
| Keine Capability als `implemented` bezeichnet | erfüllt |
| Alle Capabilities besitzen eine Priorität | erfüllt |
| **Fehlerhafte Summen korrigiert** | **erfüllt** — 47/45/38/56 statt 41/39/35/55 |
| Korrektur transparent ausgewiesen | erfüllt — in vier Dokumenten und als R-33 |
| Keine offene Entscheidung als A0 ausgegeben | erfüllt |
| UTF-8 mit echten deutschen Umlauten | erfüllt |

## Offene Punkte

| Punkt | Bezug |
| --- | --- |
| Berechtigungsmodell nicht erhoben | OI-08, R-25, R-27 |
| Secret-Verfahren im Schadensfall offen | OI-09, R-01 |
| Benchmarkplan fehlt vollständig | OI-06, R-21 |
| 16 Deployment-Kriterien ohne zuständiges Gate | R-34, OD-33 |
| D-016 in `PROJECT_DEFINITION.md` nicht nachgeführt | OD-31 |
| Repository-Struktur nicht freigegeben | OI-07, OD-26 |

## Pflege

Diese Prüfung wird bei jedem Work Package erneuert. Sie ersetzt weder das
Review durch den Human Maintainer noch die NDF Quality Gates.
