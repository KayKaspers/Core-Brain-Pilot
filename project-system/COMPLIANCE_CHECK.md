# Compliance Check – Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Letzte Prüfung | 2026-07-20, im Rahmen von CBP-WP-004 |
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

## Scope-Compliance (CBP-WP-004)

| Prüfung | Ergebnis |
| --- | --- |
| Nur Markdown innerhalb `D:\Projects\Core-Brain-Pilot` | erfüllt |
| Keine weiteren Dateitypen | erfüllt |
| Nur erlaubte Dokumentdateien geändert | erfüllt |
| `PROJECT_DEFINITION.md` nach D-016 nachgeführt | erfüllt — in CBP-WP-004 erlaubt; OD-31 geschlossen |
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
| Kein neuer Gate-Name eingeführt | erfüllt — DRC ist ein Prüfmodell, kein Gate (ADR-0005) |
| Kriterienklassen gekennzeichnet | erfüllt — Core 25, Deployment 16, Conditional 6 |
| Deployment-Kriterien vertagt, nicht gestrichen | erfüllt — alle 16 im DRC erfasst, Status `not-evaluated` |
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
| Aktuelles Work Package als CBP-WP-004 ausgewiesen | erfüllt |
| Keine Capability als `implemented` bezeichnet | erfüllt |
| Alle Capabilities besitzen eine Priorität | erfüllt |
| **Fehlerhafte Summen korrigiert** | **erfüllt** — 47/45/38/56 statt 41/39/35/55 |
| Korrektur transparent ausgewiesen | erfüllt — in vier Dokumenten und als R-33 |
| Keine offene Entscheidung als A0 ausgegeben | erfüllt |
| UTF-8 mit echten deutschen Umlauten | erfüllt |

## Architektur-Compliance (CBP-WP-004)

| Prüfung | Ergebnis |
| --- | --- |
| Architektur ohne Proxmox funktionsfähig beschrieben | erfüllt — Profil B als Neutralitätsnachweis |
| Proxmox bleibt Referenz, nicht Produktgrenze | erfüllt (ADR-0001) |
| Keine Proxmox-API-Abhängigkeit eingeführt | erfüllt |
| Alle fünf Deploymentprofile dokumentiert | erfüllt (A–E) |
| Docker Compose bevorzugt, aber keine Produktabhängigkeit | erfüllt (ADR-0002) |
| Canonical und Derived eindeutig getrennt | erfüllt (ADR-0003, Rebuild-Vertrag) |
| Jede logische Komponente mit klaren Schreibrechten | erfüllt — 14 Komponenten |
| Nur ein autorisierter Pfad verändert Canonical | erfüllt — Review/Approval |
| Alle fünf Aktionsklassen im Permission Model | erfüllt |
| Technische Durchsetzungsebenen benannt | erfüllt — fünf Ebenen |
| `excluded-from-ai` fail-closed gegenüber externer KI | erfüllt |
| Rotation vor History Cleanup | erfüllt — ausdrücklich als Grundsatz |
| Derived nach Secret-Vorfall gelöscht und neu aufgebaut | erfüllt — Schritte 8 und 9 |
| DRC mappt alle 16 Deployment-Required-Kriterien | erfüllt — 16 von 16 auf 18 Prüfpunkte |
| DRC steht auf NOT EVALUATED | erfüllt |
| Deployment Required blockiert G0 nicht | erfüllt |
| Keine Compose-Datei erzeugt | erfüllt |
| Keine Repository-Datei verschoben | erfüllt |
| Keine Infrastruktur bewertet oder bereitgestellt | erfüllt |
| ADRs nach bestehender Konvention | erfüllt — ADR-NNNN-titel.md, 5 Stück |

## Offene Punkte

| Punkt | Bezug |
| --- | --- |
| Berechtigungsmodell dokumentiert, **technisch nicht durchgesetzt** | R-25, R-27 |
| Secret-Erkennung und technische Unterstützung fehlen | R-01 |
| Benchmarkplan fehlt vollständig | OI-06, R-21 |
| DRC definiert, aber **NOT EVALUATED** | R-34 |
| Repository-Layout nur vorgeschlagen, nicht entschieden | OD-26 |

## Pflege

Diese Prüfung wird bei jedem Work Package erneuert. Sie ersetzt weder das
Review durch den Human Maintainer noch die NDF Quality Gates.
