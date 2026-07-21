# Compliance Check – Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | **Phase 0 COMPLETE** · Phase 1 AUTHORIZED FOR PLANNING |
| Letzte Prüfung | 2026-07-21, im Rahmen von **CBP-WP-011** |
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

## Scope-Compliance (CBP-WP-006)

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
| G0 zum Zeitpunkt der Prüfung NOT PASSED | erfüllt (historisch, CBP-WP-003) |
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
| Aktuelles Work Package als **CBP-WP-011** ausgewiesen | erfüllt |
| **Falsche WP-Titel in der Queue korrigiert** | erfüllt — Entwurfstitel aus CBP-WP-008 ersetzt, Korrektur sichtbar vermerkt |
| **Veraltete Gate-Angaben korrigiert** | erfüllt — CLAUDE.md, DISCOVERY_QUESTIONS.md, G0_EVIDENCE_MATRIX.md |
| Historische Berichte nicht stillschweigend umgeschrieben | erfüllt — frühere WP-Ergebnisse unverändert |
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

## Benchmark-Compliance (CBP-WP-005)

| Prüfung | Ergebnis |
| --- | --- |
| Korpus im Rahmen 15–24 Quellen | erfüllt — 24 |
| Alle Quellen als synthetische Fixtures gekennzeichnet | erfüllt — `test_fixture: true` durchgehend |
| Pflichtmetadaten vollständig | erfüllt — 15 Felder je Quelle |
| Keine realen Personen, Kunden oder Organisationen | erfüllt — drei erfundene Projekte, Rollen statt Namen |
| Keine echten oder realistischen Secrets | erfüllt — `data_class: secret` kommt nicht vor |
| A1 bis A6 im Korpus repräsentiert | erfüllt |
| Mindestens vier Konfliktpaare | erfüllt — K1 bis K4 |
| Mindestens vier veraltete oder superseded Quellen | erfüllt — 5 |
| Mindestens vier Datenschutzfälle | erfüllt — 4 Fixtures, 6 Fragen |
| Mindestens zwei `excluded-from-ai`-Fixtures | erfüllt — 2 |
| Mindestens drei Negativfälle | erfüllt — 6 Abstention-Fragen |
| Genau 36 Fragen, 6 Kategorien zu je 6 | erfüllt |
| Genau 24 Development und 12 Holdout | erfüllt |
| Kein Fall über drei Quellen | erfüllt — F-06 ist ausgewiesener Eskalationsfall |
| Kritische Fehler definiert | erfüllt — 7 |
| V0, V1, V2 provider-neutral | erfüllt — keine Suchsoftware benannt |
| Datenschutzverletzungen mit Zielwert 0 | erfüllt |
| Keine Suchsoftware ausgewählt oder installiert | erfüllt — qmd bleibt Kandidat (OD-25) |
| Keine ausführbaren Dateien | erfüllt — ausschließlich Markdown |
| Benchmark **dokumentiert, nicht ausgeführt** | erfüllt |

## G0-Compliance (CBP-WP-006)

| Prüfung | Ergebnis |
| --- | --- |
| Mindestens fünf aktive oder Test-Source-Slots | erfüllt — 4 `active` + 1 `test-only` |
| PDF/Office und externe Connectoren `deferred` | erfüllt — PS-06, PS-07 |
| Kein realer privater Pfad in einem Slot | erfüllt — nur `canonical_location_type`, kein Ort |
| Jeder Slot mit Owner, Datenklasse, AI-Transfer-Regel, Löschmodell | erfüllt — 7 von 7 |
| `excluded-from-ai` fail-closed | erfüllt — Slot-Regel 5 erzwingt `forbidden` |
| Benchmark-A0 ohne reale Projektgeltung | erfüllt — PS-05 `test-only`, kritischer Fehler 9 |
| Deployment Mapping bleibt separat | erfüllt — eigene Ebene, DRC zuständig |
| D-1 vollständig belegt | erfüllt — 5 Nachweisdokumente |
| D-1 bedeutet keine angebundene Quelle | erfüllt — dreifach vermerkt |
| Alle 25 Core-Kriterien in der Evidenzmatrix | erfüllt |
| Keine unbelegte `accepted`-Markierung | erfüllt — je Kriterium ein Dokumentverweis |
| Dokumentarische Erfüllung nicht als technische dargestellt | erfüllt — 16 Kriterien mit „technisch erforderlich: ja" |
| Benchmarkdesign nicht als Ausführung dargestellt | erfüllt — alle G-Kriterien mit „nicht ausgeführt" |
| **DRC bleibt NOT EVALUATED** | erfüllt |
| **G0 nicht eigenmächtig freigegeben** | **erfüllt** — Freigabe erfolgte durch den Human Maintainer am 2026-07-21 |
| Status READY FOR HUMAN DECISION eindeutig | erfüllt — in Kriterien, Matrix und Review |
| **Entscheidungsblock leer** | erfüllt |
| ADR-0006 bleibt `proposed` | erfüllt |
| OD-05, OD-06, OD-26 bleiben offen | erfüllt |
| Keine produktive Quelle eingebunden | erfüllt |

## Phase-1-Planungs-Compliance (CBP-WP-008)

| Prüfung | Ergebnis |
| --- | --- |
| Alle fünf Foundation-Streams geplant | erfüllt — F1 bis F5 |
| Jeder Stream mit Abhängigkeiten und Nachweisen | erfüllt — 14 Felder je Stream |
| Jeder Stream mit Abbruch- und Rücksetzbedingungen | erfüllt |
| Core Repository, privater Workspace und Runtime Data getrennt | erfüllt — drei Bereiche benannt |
| **Keine reale Repository-Reorganisation** | erfüllt — keine Datei verschoben |
| **Keine realen Source Mappings eingetragen** | erfüllt — nur Schema und Platzhalter |
| Mappingdefaults `enabled: false` und `read_only: true` | erfüllt |
| Security Plan enthält alle zwölf Kontrollbereiche | erfüllt — KB-01 bis KB-12 |
| **Promptregeln nicht als technische Kontrolle behandelt** | erfüllt — Rang 7, kein Bereich ruht allein darauf |
| Quarantäne fail-closed geplant | erfüllt — 12 Schritte, 10 Status |
| **Keine Quelle von `received` direkt nach indexiert** | erfüllt — Regel S1 |
| Secret-Fund blockiert den Ingest | erfüllt — Regel S5 |
| Source Registry und Suchindex getrennt | erfüllt — eigene Abgrenzungstabelle |
| Tombstone und Derived Cleanup geplant | erfüllt — T-1 bis T-6 |
| CBP-WP-009 bis CBP-WP-014 ausschließlich `proposed` | erfüllt |
| Kein Folge-Work-Package auf `active` | erfüllt |
| Keine Capability `implemented` | erfüllt — weiterhin 0 von 29 |
| **R-33 nicht geschlossen** | erfüllt — bleibt `gemindert` |
| Genau ein nächstes Work Package vorgeschlagen | erfüllt — CBP-WP-009 |
| Keine ausführbare Datei erstellt | erfüllt — ausschließlich Markdown |
| Kein Commit, kein Push, `origin` unverändert | erfüllt |

## Entscheidungs-Compliance (CBP-WP-009)

| Prüfung | Ergebnis |
| --- | --- |
| Beide Entscheidungen stammen direkt vom Human Maintainer | erfüllt — Entscheidungsblock im Wortlaut |
| Keine Entscheidung ergänzt oder erweitert | erfüllt — Notes nur normalisiert |
| Teil A und Teil B getrennt dokumentiert | erfüllt — D-029 und D-030, eigene ADR-Abschnitte |
| ADR-Status entspricht den Entscheidungen | erfüllt — zwei SELECT → `accepted` |
| **OD-26 nur bei zwei SELECT-Entscheidungen geschlossen** | erfüllt |
| **Keine Repository-Reorganisation** | erfüllt — Top-Level unverändert |
| **Kein privater Workspace angelegt** | erfüllt |
| **Keine Zielverzeichnisse angelegt** | erfüllt |
| Keine privaten Pfade oder URLs gespeichert | erfüllt |
| Core, Operator-Workspace und Runtime getrennt | erfüllt — drei Bereiche in ADR-0007 |
| **Registry-Schema und konkrete Registry-Metadaten getrennt** | erfüllt — Grenze G7 |
| **`.gitignore` nicht als Sicherheitsgrenze behandelt** | erfüllt — Grenze G3 ausdrücklich |
| ADR-0006 bleibt `accepted` | erfüllt |
| OD-05, OD-06, OD-34 bleiben offen | erfüllt |
| G0 bleibt PASSED WITH NOTES | erfüllt |
| Phase 1 bleibt AUTHORIZED FOR PLANNING | erfüllt |
| DRC bleibt NOT EVALUATED | erfüllt |
| Benchmark bleibt nicht ausgeführt | erfüllt |
| Keine Capability `implemented` | erfüllt — 0 von 29 |
| **Summen aus den Quelltabellen ausgezählt** | erfüllt — 30/26/21/5 |
| Genau ein Folge-Work-Package vorgeschlagen | erfüllt — CBP-WP-010 |
| Keine ausführbare Datei erstellt | erfüllt — ausschließlich Markdown |
| Kein Commit, kein Push, `origin` unverändert | erfüllt |

## Mapping-Compliance (CBP-WP-010)

| Prüfung | Ergebnis |
| --- | --- |
| Drei Entscheidungen direkt vom Human Maintainer | erfüllt — Entscheidungsblock im Wortlaut |
| Keine Human-Entscheidung ergänzt oder erweitert | erfüllt — Notes nur normalisiert |
| ADR-0008-Status entspricht den Entscheidungen | erfüllt — drei SELECT → `accepted` |
| **ADR-0006 nur durch sichtbaren Klarstellungsnachtrag ergänzt** | erfüllt — *non-substantive clarification*, datiert, A1 |
| **ADR-0006-Entscheidung unverändert** | erfüllt — Status `accepted`, Wortlaut nicht umgeschrieben |
| **Keine öffentliche Veröffentlichung freigegeben** | erfüllt — A0-Vorbehalt in ADR-0006 und ADR-0007 |
| Core-Repository bleibt privat | erfüllt |
| Alle neuen Dateien Markdown | erfüllt — 7 Dateien |
| **Keine reale Location Reference gespeichert** | erfüllt — nur `synthetic-placeholder-*` |
| **Keine private Repository-URL gespeichert** | erfüllt — nur `example.invalid` (RFC 2606) |
| **Kein Secret, kein realistisches Secret-Muster** | erfüllt — nur `<SYNTHETIC-SECRET-PLACEHOLDER-DO-NOT-USE>` |
| Mapping-Schema vollständig | erfüllt — 31 Felder mit Typ, Pflicht, Default, Werten, Datenschutzwirkung, Validierung |
| Defaults disabled, read-only, fail-closed | erfüllt — 12 Vorgabewerte |
| **`unknown` data_class blockiert** | erfüllt — V9, fail-closed wie `excluded-from-ai` |
| **`excluded-from-ai` blockiert externe Übertragung** | erfüllt — V10, **abgelehnt statt korrigiert** |
| Genau eine Source Boundary je Mapping | erfüllt — D-033, Beispiel 9 zeigt den Verstoß |
| PS-02-, PS-03-, PS-04-Regeln vollständig | erfüllt — 9 · 9 · 8 Regeln |
| Zustandsmodell verhindert `draft` → `enabled` | erfüllt — Z11 |
| **`approved` bedeutet nicht `enabled`** | erfüllt — Z5, Gate-Punkte 16 und 20 getrennt |
| `revoked` und `deleted` erzeugen Derived Cleanup | erfüllt — Z8, Z9, D3 |
| Mapping-ID nach Löschung nicht wiederverwendet | erfüllt — Z10, D5, V21 |
| Beispiele eindeutig `synthetic · non-operational · test-only` | erfüllt — 10 von 10 |
| Private Handoff-Vorlage ohne Werte | erfüllt — nur Defaults, fünf Hinweisregeln |
| **Activation Gate bleibt `NOT EVALUATED`** | erfüllt — nicht ausgeführt |
| **Kein Mapping `enabled`** | erfüllt — es existiert kein Mapping |
| OD-05, OD-06, OD-34 bleiben offen | erfüllt |
| Keine Dublette bei OD-35 angelegt | erfüllt — ein Eintrag statt drei, Verweis auf ADR-0007 |
| **Summen aus den Quelltabellen ausgezählt** | erfüllt — 33/29/23/5 |
| Genau ein Folge-Work-Package | erfüllt — CBP-WP-011 |
| Keine ausführbare Datei, kein JSON Schema, kein Validator | erfüllt |
| Kein Commit, kein Push, `origin` unverändert | erfüllt |

## Zähl- und Statusregel

*Ergänzt in CBP-WP-007, nach dem dritten Zählfehler des Projekts.*

| # | Regel |
| --- | --- |
| **1** | **Summen werden erst nach Auszählung der aktuellen Quelltabelle geschrieben.** |
| **2** | **Eine zuvor geschriebene Summenzeile ist keine gültige Quelle für eine spätere Summenzeile.** |
| **3** | **Berichtssummen müssen gegen die zugrunde liegenden Zeilen geprüft werden.** |
| **4** | **Bei Abweichung gilt die Tabelle**, bis die Ursache dokumentiert und korrigiert ist. |
| **5** | **Manuelle Summen sind als `derived status data` zu behandeln** — reproduzierbar, nie autoritativ. |

Regel 5 wendet das Kernprinzip des Projekts auf seine eigene Berichterstattung
an: eine Summe ist eine Ableitung. Sie steht in derselben Beziehung zur Tabelle
wie ein Index zum kanonischen Bestand — reproduzierbar, ersetzbar und der
Quelle nachgeordnet.

**Diese Regel schließt R-33 nicht.** Sie ist eine Dokumentregel, keine
technische Kontrolle; das Risiko bleibt bestehen, bis eine automatische Prüfung
existiert.

### Historie der Zählfehler

| Work Package | Fehler | Korrigiert in |
| --- | --- | --- |
| CBP-WP-002 | 41/39/35/55 statt 47/45/38/56 | CBP-WP-003 |
| CBP-WP-003 | 6 `accepted` / 15 `open` statt 8 / 13 | im selben Lauf |
| CBP-WP-006 | 15/6/4 statt 16/7/2 in der Evidenzmatrix | im selben Lauf |
| **CBP-WP-007** | **22 A0-Entscheidungen statt 24; 8 offene P0 statt 6** | **CBP-WP-008** |
| **CBP-WP-010** | **„neun Blocker" bei acht aufgezählten IDs** (V7, V8, V9, V10, V11, V14, V20, V23). Die Zahl war durch einen offenen Zusatz — „sowie jede Regel, deren Verletzung ein Secret sichtbar macht" — **unprüfbar** gemacht worden | **CBP-WP-010, Nova-REWORK-Korrekturlauf** |
| **CBP-WP-011** | **Drei Befunde in einem Korrekturvorgang.** (1) Readiness Gate: Stufenverteilung summierte sich auf **25** bei **24** Gate-Punkten — Stufe 4 war mit 10 angegeben, die ID-Liste enthielt 9. (2) **Testtaxonomie**: ein Positivtest trug die NT-ID `NT-25` und wurde zur Negativtestzahl gerechnet. (3) **Doppelt vergebene Test-IDs**: `NT-23` und `NT-24` bezeichneten in der Acceptance Matrix RT-1-/RT-3-Tests, in der Egress-Policy DNS-/Privatnetz-Tests | **CBP-WP-011, Nova-REWORK-Korrekturlauf** |

**Der vierte Fehler entstand, nachdem die Regel eingeführt war**, und wurde
erst ein Work Package später gefunden. Die Regel wirkt — aber nachlaufend. Das
ist der Grund, warum R-33 nicht geschlossen wird.

**Der fünfte Fehler zeigt eine neue Variante:** Die Zahl war nicht falsch
abgeschrieben, sondern durch einen unbestimmten Zusatz *plausibilisiert*
worden. Eine Aufzählung, die mit „sowie jede Regel, die …" endet, entzieht sich
Zählregel 3 — sie ist gegen die Quelltabelle nicht prüfbar. **Ergänzung zur
Zählregel:** Eine Summe darf **nicht** durch einen offenen Zusatz ergänzt
werden; jede gezählte Einheit muss einzeln benennbar sein.

**Der sechste Vorgang zeigt eine dritte Variante:** eine **Doppelvergabe von
IDs über Dokumentgrenzen hinweg**. Innerhalb jedes einzelnen Dokuments waren
`NT-23` und `NT-24` eindeutig; erst die dokumentübergreifende Auszählung machte
die Kollision sichtbar. **Ergänzung zur Zählregel:** Eine Kennung ist erst dann
eindeutig, wenn sie **über alle Dokumente hinweg** nur einmal vorkommt — die
kanonische Inventartabelle entscheidet.

**R-33 bleibt `gemindert, nicht geschlossen`** — die Einträge ändern den Status
nicht. Die Zähl- und Statusregel ist weiterhin eine **Dokumentregel, keine
technische Kontrolle**. Sechs Zählvorgänge in elf Work Packages sind
dokumentiert; jeder wurde durch Auszählung gefunden, keiner durch die Regel
verhindert.

## Offene Punkte

| Punkt | Bezug |
| --- | --- |
| Berechtigungsmodell dokumentiert, **technisch nicht durchgesetzt** | R-25, R-27 |
| Secret-Erkennung und technische Unterstützung fehlen | R-01 |
| Benchmark entworfen, **nicht ausgeführt** — keine Messung | R-21 |
| Konkreter produktiver Quellenbestand — Slot-Ebene entschieden, Mapping offen | OD-05, OD-06 |
| DRC definiert, aber **NOT EVALUATED** | R-34 |
| Repository-Zielstruktur entschieden, **Migration nicht geplant und nicht autorisiert** | D-029, ADR-0007 |
| Operator-Workspace beschlossen, **nicht angelegt** | D-030, ADR-0007 |
| Mappingkonvention entschieden, **kein Mapping, kein Validator** | D-031…D-033, ADR-0008 |
| **Mapping Activation Gate `NOT EVALUATED`** — ohne F3-Strang nicht durchlaufbar | PILOT_MAPPING_ACTIVATION_GATE |
| **Alle Nachweise stehen auf Stufe 1 `dokumentiert`** | PHASE_1_EVIDENCE_PLAN |
| Zwölf Stop-Bedingungen definiert, **keine erprobt** | PHASE_1_STOP_CONDITIONS |

> **Erledigt seit CBP-WP-007:** Die G0-Entscheidung des Human Maintainers liegt
> vor — **PASSED WITH NOTES**, 2026-07-21, A0.

## Pflege

Diese Prüfung wird bei jedem Work Package erneuert. Sie ersetzt weder das
Review durch den Human Maintainer noch die NDF Quality Gates.
