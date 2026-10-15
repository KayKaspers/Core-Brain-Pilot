# Compliance Check – Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | **Phase 0 COMPLETE** · Phase 1 AUTHORIZED FOR PLANNING |
| Letzte Prüfung | 2026-07-22, im Rahmen von **CBP-WP-014** |
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
| Aktuelles Work Package als **CBP-WP-012** ausgewiesen | erfüllt |
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

## Runtime-Compliance (CBP-WP-012)

| Prüfung | Ergebnis |
| --- | --- |
| Implementierung direkt vom Human Maintainer autorisiert | erfüllt — APPROVE WITH NOTES, A0 |
| Stack A1, CLI B1, additive Struktur C1 ausdrücklich gewählt | erfüllt |
| **Python ≥ 3.13 vor Phase B nachgewiesen** | erfüllt — 3.13.14; Blocker in Phase A gemeldet |
| Keine externe Runtime-Abhängigkeit, kein Paketdownload, keine globale Installation | erfüllt |
| Alle neuen Pfade in der Erlaubnisliste | erfüllt — `core/`, `config/`, `examples/`, `tests/`, `docs/runtime/`, `pyproject.toml` |
| **Keine bestehende Datei oder Ordner verschoben** | erfüllt — additiv |
| `compileall` erfolgreich | erfüllt — Exit 0 |
| **Unit-Testlauf erfolgreich** | erfüllt — **69/69**, Exit 0 |
| **Testzahl aus dem Lauf ausgezählt** | erfüllt — `Ran 69 tests ... OK` (67 + 2 Netzwerk-Guard) |
| Kein Test manuell zur Summe ergänzt | erfüllt |
| `version` Exit 0 · Beispielkonfiguration validiert | erfüllt |
| **`doctor` meldet nicht produktionsbereit** | erfüllt — `production_ready: false`, Exit 3 |
| **`doctor --json` gültiges JSON, BOM-frei** | erfüllt — erstes Byte `{`, über Datei belegt |
| Doctor-Ausgabe deterministisch, ohne Secret-Werte | erfüllt |
| **`run` verweigert fail-closed** | erfüllt — `RUNTIME_START_BLOCKED`, Exit 4 |
| `run` erzeugt keine Runtime-Daten | erfüllt — Tests belegen leeres Verzeichnis |
| Kein Netzwerkzugriff | erfüllt — keine Netzwerk-Imports |
| **Kein Secret gespeichert, keine Secret-Auflösung implementiert** | erfüllt — Resolver verweigert |
| Kein RT-2-Speicher, keine Egress-Allowlist | erfüllt — Writer und Egress-Port verweigern |
| Canonical Write bleibt verboten · Identitäten getrennt · Default-Ports verweigern | erfüllt |
| **Keine vollständige Security Control als `implemented`** | erfüllt — 12 Kontrollen bleiben `DOCUMENTED ONLY` |
| Alle drei Gates bleiben `NOT EVALUATED` | erfüllt |
| **Kein Risiko allein durch Skeleton geschlossen** | erfüllt |
| R-33 nicht geschlossen | erfüllt |
| CBP-WP-013 bleibt `proposed`, nicht autorisiert | erfüllt |
| Git-Diff enthält keine Secret-Werte | erfüllt |
| Kein Commit, kein Push | erfüllt |

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
| **CBP-WP-012** | **Ein Korrekturvorgang mit zwei Ausprägungen im ersten Report.** (1) **Git-Inventar** als „6 neue Pfade" angegeben statt tatsächlich **21 neue / 13 geänderte / 34 eindeutige** Pfade. (2) **Exitcode-Sequenz** als „alle sieben ausgeführt" beschrieben, aber nur **sechs** Exitcodes belegt — der siebte fehlte. Beide Male war die Aussage höher als der Beleg | **CBP-WP-012, Nova-REWORK-Korrekturlauf** |
| **CBP-WP-013** | **Dokumentübergreifender Mengen- und Terminologiekonsistenzfehler** (kein arithmetischer Zählfehler). Die Risikomengen A (6), B (5), C (11) waren **numerisch korrekt**; die Vereinigungsmenge **C** wurde jedoch fälschlich als „vollständige kritische Liste" bezeichnet, und Gruppe **B** als „offen/hoch", obwohl **R-33** die Kritikalität **mittel** hat. Betroffen: `work-packages/CBP-WP-013.md`, `docs/runtime/INGEST_QUARANTINE_EVIDENCE.md` | **CBP-WP-013, Nova-REWORK-Korrekturlauf** |
| **CBP-WP-015** | **Veraltete Feldzahlangabe in A3-Planungsartefakten** (kein arithmetischer Zählfehler). Die aktuellen Angaben nannten **19** Mapping-Felder, während der angenommene A1/A2-Vertrag **31 Felddefinitionen** (29 Pflicht + 2 optional) und **24 Validierungsregeln** hat. Betroffen: `docs/roadmap/PILOT_SOURCE_MAPPING_PLAN.md`, `docs/roadmap/PHASE_1_EVIDENCE_PLAN.md`. Die historische Queue-Aussage zu CBP-WP-008 wird **separat als historisch** behandelt | **CBP-WP-015** |
| **CBP-WP-015 (Post-Commit Reconciliation)** | **Git-/Register-Statusabweichung** (kein arithmetischer Zählfehler). Nach Commit und Push von CBP-WP-015 (`645ccb1`) blieb der A2-Status in mehreren Statusdokumenten auf `in-review`, obwohl Git CBP-WP-015 als `committed` und mit origin/main synchron auswies. Betroffen: `README.md`, `CLAUDE.md`, `project-system/WORK_PACKAGE_QUEUE.md`, `project-system/PROJECT_MANIFEST.md`, `project-brain/PROJECT_BRAIN.md` | **CBP-WP-015 Post-Commit Status Reconciliation** |
| **CBP-WP-014/015 (Queue Detail Block Reconciliation)** | **Git-/Register-Statusabweichung in Detailblöcken** (kein arithmetischer Zählfehler). In `WORK_PACKAGE_QUEUE.md` blieben die Detailblöcke CBP-WP-014 (`in-review`, „Commit nicht ausgeführt") und CBP-WP-015 (`vorgeschlagen, nicht freigegeben`, `proposed`) auf Vor-Commit-/Vor-Autorisierungsständen, obwohl beide `committed` (d0c0531 bzw. 645ccb1) sind. Betroffen: `project-system/WORK_PACKAGE_QUEUE.md` (Detailblöcke CBP-WP-014, CBP-WP-015) | **CBP-WP-014/015 Queue Detail Block Reconciliation** |
| **CBP-WP-016 (Post-Commit Reconciliation)** | **Git-/Register-Statusabweichung** (kein arithmetischer Zählfehler). Nach Commit und Push von CBP-WP-016 (`04c427c`) führten mehrere Statusdokumente CBP-WP-016 weiterhin als `in-review`/„nicht committet", obwohl Git CBP-WP-016 als `committed` und mit origin/main synchron auswies. Betroffen: `README.md`, `CLAUDE.md`, `project-system/WORK_PACKAGE_QUEUE.md`, `project-system/PROJECT_MANIFEST.md`, `project-system/PROJECT_PROFILE.md`, `project-system/HEALTH_SCORE.md`, `project-brain/PROJECT_BRAIN.md` | **CBP-WP-016 Post-Commit Status Reconciliation** |
| **CBP-WP-017 (Post-Commit Reconciliation)** | **Git-/Register-Statusabweichung** (kein arithmetischer Zählfehler). Nach Commit und Push von CBP-WP-017 (`d3168c4`) führten mehrere Statusdokumente CBP-WP-017 weiterhin als `in-review`/„nicht committet", obwohl Git CBP-WP-017 als `committed` und mit origin/main synchron auswies. Betroffen: `README.md`, `CLAUDE.md`, `project-system/WORK_PACKAGE_QUEUE.md`, `project-system/PROJECT_MANIFEST.md`, `project-system/PROJECT_PROFILE.md`, `project-system/HEALTH_SCORE.md`, `project-brain/PROJECT_BRAIN.md` | **CBP-WP-017 Post-Commit Status Reconciliation** |
| **CBP-WP-018 (ADR-Index-Zählkorrektur)** | **Vorbestehender Zählfehler in einem kanonischen Statusartefakt** (kein Post-Commit-Vorgang). Der ADR-Index `docs/decisions/README.md` wies „Angenommene ADRs" als **elf** aus, obwohl ADR-0001 bis ADR-0012 bereits existierten (korrekt: **zwölf**). Beim Hinzufügen von **ADR-0013** in Phase B0 auf den belegten Wert **13** korrigiert (11 → 12 vorbestehend + 12 → 13 Ergänzung). Betroffen: `docs/decisions/README.md` | **CBP-WP-018 Phase B0 Governance Foundation** |

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

**Der siebte Vorgang trat im ersten technischen Work Package auf** und zeigt
eine vierte Variante: **die Aussage lag höher als der Beleg**. Das Git-Inventar
wurde mit „6 neue Pfade" beziffert, obwohl `git status --porcelain=v1 -uall`
**21 neue, 13 geänderte, 34 eindeutige** Pfade auflistet; die Prüfmatrix wurde
als „alle sieben ausgeführt" beschrieben, während nur **sechs** Exitcodes
belegt waren. **Ergänzung zur Zählregel:** Jede genannte Anzahl von Artefakten
oder Kommandos muss gegen die **maschinell erzeugte** Quellliste
(`git status`, Befehlsmatrix) geprüft werden, bevor sie berichtet wird — die
Behauptung folgt dem Beleg, nicht umgekehrt. **Der Netzwerk-Guard, der in
diesem Korrekturlauf ergänzt wurde, ist eine lokale Testverbesserung und
schließt R-33 nicht** — R-33 ist eine Dokumentregel, keine technische
Kontrolle.

**Der achte Vorgang ist kein arithmetischer Zählfehler, sondern eine
Konsistenz- und Terminologieinkonsistenz.** In zwei Repository-Artefakten des
CBP-WP-013-Änderungssatzes (`work-packages/CBP-WP-013.md`,
`docs/runtime/INGEST_QUARANTINE_EVIDENCE.md`) waren die Risikomengen **A (6),
B (5) und C (11) numerisch korrekt**, aber die Vereinigungsmenge **C** wurde
fälschlich als „vollständige kritische Liste" bezeichnet und Gruppe **B** als
„offen/hoch", obwohl **R-33** die Kritikalität **mittel** hat. **Ergänzung zur
Zählregel:** Eine Vereinigungsmenge darf nicht unter dem Namen einer ihrer
Teilmengen geführt werden, und eine Kritikalität darf nicht heraufgestuft
benannt werden — die Benennung folgt der Quelltabelle. Korrigiert im
Nova-REWORK-Terminologiekorrekturlauf.

**R-33 bleibt `gemindert, nicht geschlossen`** — die Einträge ändern den Status
nicht. Die Zähl- und Statusregel ist weiterhin eine **Dokumentregel, keine
technische Kontrolle**. **Acht Konsistenzvorgänge in vierzehn Work Packages**
sind dokumentiert; jeder wurde durch Auszählung bzw. Terminologieprüfung
gefunden, keiner durch die Regel verhindert.

**CBP-WP-014 führte keinen neuen Konsistenzvorgang ein.** Testzahl (**212**) aus
`Ran N tests`, Git-Inventar aus `git status --porcelain=v1 -uall`, Entscheidungs-
(D-042…D-045) und ADR-Zahlen aus den Quelltabellen ausgezählt; die Risikomengen
A (6), B (5) und C (11) blieben kanonisch getrennt. **R-33 bleibt offen.**

**Der neunte Vorgang (CBP-WP-015) ist kein arithmetischer Zählfehler, sondern
eine veraltete Feldzahlangabe in Planungsartefakten.** Zwei aktuelle
A3-Dokumente (`docs/roadmap/PILOT_SOURCE_MAPPING_PLAN.md`,
`docs/roadmap/PHASE_1_EVIDENCE_PLAN.md`) führten „19 Felder" (bzw. „M1–M14")
als Planungsannahme aus CBP-WP-008 fort, obwohl der angenommene A1/A2-Vertrag
(ADR-0008, CBP-WP-010) **31 Felddefinitionen** — **29 Pflichtfelder** und **zwei
optionale Felder** — sowie **24 Validierungsregeln** umfasst. **Ergänzung zur
Zählregel:** Eine aktuelle Planungsangabe muss gegen den angenommenen
A1/A2-Vertrag geprüft werden; eine abgelöste Annahme wird als solche
gekennzeichnet, nicht stillschweigend fortgeführt. Korrigiert durch transparente
19/31-Korrekturhinweise; die historischen Angaben und die Queue-Aussage zu
CBP-WP-008 bleiben als **abgelöste Planungsannahme** erhalten und werden **nicht**
rückwirkend umgeschrieben. **Der akzeptierte 31-Feld-Vertrag wurde nicht
verändert.** Testzahl (**315**) aus `Ran N tests`, Git-Inventar, Entscheidungs-
(D-046…D-049) und ADR-Zahlen (ADR-0012) aus den Quelltabellen ausgezählt.

**R-33 bleibt `gemindert, nicht geschlossen`** — Kritikalität unverändert
**mittel**, kein Risiko geschlossen. **Neun Konsistenzvorgänge in fünfzehn Work
Packages** waren zu diesem Zeitpunkt dokumentiert; jeder wurde durch Auszählung
bzw. Quellenabgleich gefunden, keiner durch die Regel verhindert. Dieser Vorgang
ist mit dem Eintrag in [RISK_REGISTER.md](RISK_REGISTER.md) **identisch** und
zählt **nur einmal**.

**Der zehnte Vorgang (CBP-WP-015 Post-Commit Status Reconciliation) ist kein
arithmetischer Zählfehler, sondern eine Git-/Register-Statusabweichung.** Nach
Commit und Push von CBP-WP-015 (`645ccb1`) blieb der formale A2-Status in
mehreren Statusdokumenten (`README.md`, `CLAUDE.md`,
`project-system/WORK_PACKAGE_QUEUE.md`, `project-system/PROJECT_MANIFEST.md`,
`project-brain/PROJECT_BRAIN.md`) auf `in-review`, obwohl Git CBP-WP-015 bereits
als `committed` und mit origin/main synchron auswies. **Ursache:** Der
Implementation Commit trug den korrekten Vor-Commit-Reviewstatus `in-review`; es
fehlte danach eine Post-Commit-Status-Reconciliation. **Ergänzung zur
Zählregel:** Nach Commit und Push eines Work Packages ist der getrackte Status
gegen den Git-Verlauf zu synchronisieren; ein Vor-Commit-Reviewstatus darf nach
belegtem Commit nicht als aktueller Status fortbestehen. Korrigiert durch
Synchronisierung auf den `committed`-Zustand. **Wirkung:** kein Funktionsfehler,
keine Runtimeänderung, keine Gatefreigabe, keine Aktivierung, keine
Capability-Änderung; CBP-WP-016 bleibt `proposed`.

**R-33 bleibt `gemindert, nicht geschlossen`** — Kritikalität unverändert
**mittel**, kein Risiko geschlossen. **Zehn Konsistenzvorgänge in fünfzehn Work
Packages** waren zu diesem Zeitpunkt dokumentiert (*Stand nach dem zehnten
Vorgang; durch den elften Vorgang unten auf **elf** aktualisiert*; löst „neun"
ab); die Zahl der Work Packages bleibt **fünfzehn**, weil der Vorgang erneut
CBP-WP-015 betrifft und kein neues Work Package hinzukommt. Dieser Vorgang ist
mit dem Eintrag in [RISK_REGISTER.md](RISK_REGISTER.md) **identisch** und zählt
**nur einmal**.

**Der elfte Vorgang (CBP-WP-014/015 Queue Detail Block Reconciliation) ist kein
arithmetischer Zählfehler, sondern eine Git-/Register-Statusabweichung in
Detailblöcken.** In `project-system/WORK_PACKAGE_QUEUE.md` blieben die
Detailblöcke von CBP-WP-014 (`Status in-review`, „Commit nicht ausgeführt") und
CBP-WP-015 (`vorgeschlagen, nicht freigegeben`, `proposed`) auf Vor-Commit- bzw.
Vor-Autorisierungsständen, obwohl Git, Queue-Übersicht und zentrale Statusfelder
beide bereits als `committed` (d0c0531 bzw. 645ccb1) belegten. **Ursache:**
Frühere Status-Reconciliations prüften Header, Übersicht und zentrale
Statusfelder, erfassten jedoch nicht sämtliche **Detailblöcke** der Queue.
**Ergänzung zur Zählregel:** Eine Status-Reconciliation muss **alle** aktuellen
Statusaussagen eines Dokuments erfassen, auch Detailblöcke, nicht nur Header und
Übersicht. Korrigiert durch Synchronisierung beider Detailblöcke auf den
`committed`-Zustand; frühere Stände nur noch ausdrücklich historisch
gekennzeichnet. **Wirkung:** keine Codeänderung, keine Runtimeänderung, keine
Gatefreigabe, keine Aktivierung, keine Capability-Änderung; CBP-WP-016 bleibt
`proposed`.

**R-33 bleibt `gemindert, nicht geschlossen`** — Kritikalität unverändert
**mittel**, kein Risiko geschlossen. **Elf Konsistenzvorgänge in fünfzehn Work
Packages** waren zu diesem Zeitpunkt dokumentiert (*Stand nach dem elften
Vorgang; durch den zwölften Vorgang unten auf **zwölf** aktualisiert*; löst
„zehn" ab); die Zahl der Work Packages blieb **fünfzehn**, weil der Vorgang
CBP-WP-014 und CBP-WP-015 betrifft, die bereits Teil der Menge sind, und kein
neues Work Package hinzukommt. Dieser Vorgang ist mit dem Eintrag in
[RISK_REGISTER.md](RISK_REGISTER.md) **identisch** und zählt **nur einmal**.

**Der zwölfte Vorgang (CBP-WP-016 Post-Commit Status Reconciliation) ist kein
arithmetischer Zählfehler, sondern eine Git-/Register-Statusabweichung** derselben
Klasse wie der zehnte Vorgang. Nach Commit und Push von CBP-WP-016 (`04c427c`)
führten mehrere Statusdokumente (`README.md`, `CLAUDE.md`,
`project-system/WORK_PACKAGE_QUEUE.md`, `project-system/PROJECT_MANIFEST.md`,
`project-system/PROJECT_PROFILE.md`, `project-system/HEALTH_SCORE.md`,
`project-brain/PROJECT_BRAIN.md`) CBP-WP-016 weiterhin als `in-review`/„nicht
committet", obwohl Git CBP-WP-016 bereits als `committed` und mit origin/main
synchron auswies. **Ursache:** Der Implementation Commit trug den korrekten
Vor-Commit-Reviewstatus `in-review`; es fehlte danach die
Post-Commit-Status-Reconciliation. Korrigiert durch Synchronisierung auf den
`committed`-Zustand (`04c427c`); „aktuelles Work Package" auf **keines aktiv,
zuletzt abgeschlossen CBP-WP-016** gesetzt; kein Work Package `active`/`in-review`;
**CBP-WP-017 nicht autorisiert**. **Wirkung:** kein Funktionsfehler, keine
Runtimeänderung, keine Gatefreigabe, keine Aktivierung, keine Capability-Änderung.

**R-33 bleibt `gemindert, nicht geschlossen`** — Kritikalität unverändert
**mittel**, kein Risiko geschlossen. **Zwölf Konsistenzvorgänge in sechzehn Work
Packages** waren zu diesem Zeitpunkt dokumentiert (*Stand nach dem zwölften
Vorgang; durch den dreizehnten Vorgang unten auf **dreizehn** aktualisiert*; löst
„elf" ab); die Zahl der Work Packages stieg auf **sechzehn**, weil dieser Vorgang
**erstmals CBP-WP-016** betraf, das durch `04c427c` Teil der committeten Menge
wurde. Dieser Vorgang ist mit dem Eintrag in
[RISK_REGISTER.md](RISK_REGISTER.md) **identisch** und zählt **nur einmal**.

**Der dreizehnte Vorgang (CBP-WP-017 Post-Commit Status Reconciliation) ist kein
arithmetischer Zählfehler, sondern eine Git-/Register-Statusabweichung** derselben
Klasse wie der zehnte/zwölfte Vorgang. Nach Commit und Push von CBP-WP-017
(`d3168c4`) führten mehrere Statusdokumente (`README.md`, `CLAUDE.md`,
`project-system/WORK_PACKAGE_QUEUE.md`, `project-system/PROJECT_MANIFEST.md`,
`project-system/PROJECT_PROFILE.md`, `project-system/HEALTH_SCORE.md`,
`project-brain/PROJECT_BRAIN.md`) CBP-WP-017 weiterhin als `in-review`/„nicht
committet", obwohl Git CBP-WP-017 bereits als `committed` und mit origin/main
synchron auswies. **Ursache:** Der Implementation Commit trug den korrekten
Vor-Commit-Reviewstatus `in-review`; es fehlte danach die
Post-Commit-Status-Reconciliation. Korrigiert durch Synchronisierung auf den
`committed`-Zustand (`d3168c4`); „aktuelles Work Package" auf **keines aktiv,
zuletzt abgeschlossen CBP-WP-017** gesetzt; kein Work Package `active`/`in-review`;
**CBP-WP-018 nicht autorisiert**. **Wirkung:** kein Funktionsfehler, keine
Runtimeänderung, keine Gatefreigabe, keine Aktivierung, keine Capability-Änderung.

**R-33 bleibt `gemindert, nicht geschlossen`** — Kritikalität unverändert
**mittel**, kein Risiko geschlossen. **Dreizehn Konsistenzvorgänge in siebzehn Work
Packages** waren zu diesem Zeitpunkt dokumentiert (*Stand nach dem dreizehnten
Vorgang; durch den vierzehnten Vorgang unten auf **vierzehn** aktualisiert*; löst
„zwölf" ab); die Zahl der Work Packages stieg auf **siebzehn**, weil dieser Vorgang
**erstmals CBP-WP-017** betraf, das durch `d3168c4` Teil der committeten Menge
wurde. Dieser Vorgang ist mit dem Eintrag in
[RISK_REGISTER.md](RISK_REGISTER.md) **identisch** und zählt **nur einmal**.

**Der vierzehnte Vorgang (CBP-WP-018 Phase B0 — ADR-Index-Zählkorrektur) ist kein
Post-Commit-Vorgang und kein arithmetischer Summenfehler im Register, sondern die
Korrektur eines vorbestehenden Zählfehlers in einem kanonischen Statusartefakt.**
Der ADR-Index `docs/decisions/README.md` wies im Kopf-Feld „Angenommene ADRs"
**elf** aus, obwohl ADR-0001 bis ADR-0012 bereits existierten; der korrekte Wert
vor CBP-WP-018 war **zwölf**. **Ursache:** Der Index wurde nach der Aufnahme von
ADR-0012 (CBP-WP-015) nicht auf zwölf nachgeführt. Beim Hinzufügen von **ADR-0013**
in Phase B0 wurde der Index auf den durch Auszählung belegten Gesamtwert **13**
gesetzt (11 → 12 vorbestehend + 12 → 13 Ergänzung); kein ADR wurde inhaltlich
umgeschrieben. **Bestätigung der Zählregel:** R-33 zählt eigenständige Korrekturen
kanonischer Status-, Zähl- oder Konsistenzabweichungen und ist **nicht** auf
Post-Commit-Reconciliations beschränkt (vgl. den vierten bis neunten Vorgang).

**R-33 bleibt `gemindert, nicht geschlossen`** — Kritikalität unverändert
**mittel**, kein Risiko geschlossen. **Vierzehn Konsistenzvorgänge in achtzehn Work
Packages** waren zu diesem Zeitpunkt dokumentiert (*Stand nach dem vierzehnten
Vorgang; durch den fünfzehnten Vorgang unten auf **fünfzehn** aktualisiert*; löst
„dreizehn" ab); die Zahl der Work Packages stieg auf **achtzehn**, weil dieser
Vorgang **erstmals CBP-WP-018** betraf. Dieser Vorgang ist mit dem Eintrag in
[RISK_REGISTER.md](RISK_REGISTER.md) **identisch** und zählt **nur einmal**.

**Der fünfzehnte Vorgang (CBP-WP-018 Post-Commit Status Reconciliation) ist kein
arithmetischer Zählfehler, sondern eine Git-/Register-Statusabweichung** derselben
Klasse wie der zehnte/zwölfte/dreizehnte Vorgang. Nach Commit und Push der
technischen Implementation von CBP-WP-018 (`5ee2e83`) führten die
Statusdokumente (`README.md`, `CLAUDE.md`,
`project-system/WORK_PACKAGE_QUEUE.md`, `project-system/PROJECT_MANIFEST.md`,
`project-system/PROJECT_PROFILE.md`, `project-system/HEALTH_SCORE.md`,
`project-brain/PROJECT_BRAIN.md`) CBP-WP-018 weiterhin als `in-review` /
„Phase B1, uncommitted", obwohl Git CBP-WP-018 bereits als `committed` und mit
origin/main synchron auswies. **Ursache:** Der Implementation Commit trug den
korrekten Vor-Commit-Reviewstatus `in-review`; es fehlte danach die
Post-Commit-Status-Reconciliation. Korrigiert durch Synchronisierung auf den
`committed`-Zustand (Governance `4dec921`, Implementation `5ee2e83`);
„aktuelles Work Package" auf **keines aktiv, zuletzt abgeschlossen CBP-WP-018**
gesetzt; kein Work Package `active`/`in-review`; **kein nächstes Work Package
autorisiert**, **CBP-WP-019 nicht registriert, nicht begonnen, nicht
autorisiert**. **Wirkung:** kein Funktionsfehler, keine Runtimeänderung, keine
Gatefreigabe, keine Aktivierung, keine Capability-Änderung.

**R-33 bleibt `gemindert, nicht geschlossen`** — Kritikalität unverändert
**mittel**, kein Risiko geschlossen. **Fünfzehn Konsistenzvorgänge in achtzehn Work
Packages** waren zu diesem Zeitpunkt dokumentiert (*Stand nach dem fünfzehnten
Vorgang; durch den sechzehnten Vorgang unten auf **sechzehn** aktualisiert*; löst
„vierzehn" ab); die Zahl der Work Packages blieb **achtzehn**, weil CBP-WP-018
durch den vierzehnten Vorgang **bereits** Teil der betroffenen Menge war — ein
weiterer Vorgang im selben, bereits erfassten Work Package erhöht **nur** den
Vorgangszähler (**14/18 → 15/18**). Dieser Vorgang ist mit dem Eintrag in
[RISK_REGISTER.md](RISK_REGISTER.md) **identisch** und zählt **nur einmal**.

**Der sechzehnte Vorgang (CBP-WP-019 Post-Commit Status Reconciliation) ist kein
arithmetischer Zählfehler, sondern eine Git-/Register-Statusabweichung** derselben
Klasse wie der zehnte/zwölfte/dreizehnte/fünfzehnte Vorgang. Nach Commit und Push
von CBP-WP-019 (`3c437f2`) führten die Statusdokumente (`README.md`, `CLAUDE.md`,
`project-system/WORK_PACKAGE_QUEUE.md`, `project-system/PROJECT_MANIFEST.md`,
`project-system/PROJECT_PROFILE.md`, `project-system/HEALTH_SCORE.md`,
`project-brain/PROJECT_BRAIN.md`, `docs/roadmap/PHASE_1_WORK_PACKAGE_MAP.md`,
`work-packages/CBP-WP-019.md`) CBP-WP-019 weiterhin als `in-review` und als
**aktives** Work Package **ohne Commitbeleg**, obwohl Git es bereits als
`committed` und mit origin/main synchron auswies. **Ursache:** Der Implementation
Commit trug den korrekten Vor-Commit-Reviewstatus `in-review`; es fehlte danach
die Post-Commit-Status-Reconciliation. Korrigiert durch Synchronisierung auf den
`committed`-Zustand (`3c437f2`), Eintragung des Commitbelegs und Setzen von
„aktuelles Work Package" auf **keines aktiv, zuletzt abgeschlossen CBP-WP-019**;
kein Work Package `active`/`in-review`; **kein nächstes Work Package
autorisiert**, **CBP-WP-020 nicht registriert, nicht begonnen, nicht
autorisiert**. **Wirkung:** kein Funktionsfehler, keine Runtimeänderung, keine
Installation, keine Bereitstellung, keine Gatefreigabe, keine Aktivierung, keine
Capability-Änderung; **D-054 und der DRC-Vertrag unverändert**; **R-20 bleibt
offen**.

**R-33 blieb `gemindert, nicht geschlossen`** — Kritikalität unverändert
**mittel**, kein Risiko geschlossen. **Sechzehn Konsistenzvorgänge in neunzehn Work
Packages** waren dokumentiert (*Stand nach dem sechzehnten Vorgang; durch den
siebzehnten Vorgang unten auf **17/20** aktualisiert*; löst „fünfzehn" ab);
die Zahl der Work Packages stieg auf **neunzehn**, weil dieser Vorgang
**erstmals CBP-WP-019** betraf, das durch `3c437f2` Teil der committeten Menge
wurde (**15/18 → 16/19**). Dieser Vorgang ist mit dem Eintrag in
[RISK_REGISTER.md](RISK_REGISTER.md) **identisch** und zählt **nur einmal**.

### Siebzehnter Konsistenzvorgang — CBP-WP-020 Post-Commit Status Reconciliation (2026-07-29)

**Gefunden in CBP-WP-020 Phase C.** Nach Commit und Push der B1/B2-Implementation
von CBP-WP-020 (`9c6c0fb`, Parent `17057e2`) führten die Statusdokumente
(`README.md`, `CLAUDE.md`, `project-system/WORK_PACKAGE_QUEUE.md`,
`project-system/PROJECT_MANIFEST.md`, `project-system/PROJECT_PROFILE.md`,
`project-system/HEALTH_SCORE.md`, `project-brain/PROJECT_BRAIN.md`,
`docs/roadmap/PHASE_1_WORK_PACKAGE_MAP.md`, `work-packages/CBP-WP-020.md`)
CBP-WP-020 weiterhin als `in-review` in „Phase B1/B2, uncommitted" und als
**aktives** Work Package, obwohl Git es bereits als `committed` und mit
origin/main synchron auswies. **Ursache:** Der Implementation Commit trug den
korrekten Vor-Commit-Reviewstatus `in-review`; es fehlte danach die
Post-Commit-Status-Reconciliation.

**Zusätzlich bereinigte Zählabweichungen:** `project-brain/PROJECT_BRAIN.md`
führte **45/41** statt der kanonischen **55/51** getroffenen bzw.
A0-Entscheidungen; `project-system/HEALTH_SCORE.md` führte in der Zeile
„Entscheidungslage" **54** statt **55**; die Commitzähler in
`PROJECT_MANIFEST.md`, `PROJECT_BRAIN.md` und `HEALTH_SCORE.md` standen auf
**28** statt **29**. Kanonische Quelle ist `DECISION_REGISTER.md` (**55**, davon
**51** mit A0) beziehungsweise Git. **Alle durch Auszählung gefunden, keine durch
die Regel verhindert.**

**Korrigiert** durch Synchronisierung auf den `committed`-Zustand (B0
`17057e2`, B1/B2 `9c6c0fb`), Eintragung der Commitbelege, Setzen von CBP-WP-020
auf **`committed` und `complete`** und von „aktuelles Work Package" auf **keines
aktiv, zuletzt abgeschlossen CBP-WP-020**; kein Work Package `active`/`in-review`;
**kein nächstes Work Package autorisiert**, **CBP-WP-021 nicht registriert, nicht
begonnen, nicht autorisiert**.

**Wirkung:** kein Funktionsfehler, keine Runtimeänderung, keine Installation,
keine Bereitstellung, kein Containerstart, keine Gatefreigabe, keine Aktivierung,
keine Capability-Änderung; **D-055 unverändert**; das Profil-A-Bundle bleibt
*repository artifact implemented* und *offline validation passed* — **nicht
deployed, nicht operational, nicht production-ready**; die **166 Profile-A Bundle
Validation Tests sind keine** Security Foundation NT-01 bis NT-31 (**damals als
0 von 31 geführt** — siehe Nachtrag unten); Capabilities **0 von 29**; beide
Runtime-Gates `NOT EVALUATED`; die zwölf KB-Kontrollen `DOCUMENTED ONLY`;
**R-20 bleibt offen**.

> **Nachtrag aus CBP-WP-021 (D-056, 2026-08-03).** Die hier genannte Kennzahl
> „**0 von 31**" gibt den **damaligen** Stand wieder und war bereits zu diesem
> Zeitpunkt fehlerhaft. Kanonisch sind **32 Negativtests, 1 Positivtest, 33
> Testfälle** — ausgeführt **0 von 32** und **0 von 1**. Genau diese Abweichung
> ist Gegenstand des **achtzehnten** Konsistenzvorgangs unten. **Der historische
> Eintrag wird nicht umgeschrieben.**

**R-33 blieb `gemindert, nicht geschlossen`** — Kritikalität unverändert
**mittel**, kein Risiko geschlossen, **keine neue Risiko-ID**. **Siebzehn
Konsistenzvorgänge in zwanzig Work Packages** waren dokumentiert (*Stand nach
dem siebzehnten Vorgang; durch den achtzehnten Vorgang unten auf **18/21**
aktualisiert*; löste „sechzehn" ab); die Zahl der Work Packages stieg auf
**zwanzig**, weil jener Vorgang **erstmals CBP-WP-020** betraf, das durch
`9c6c0fb` Teil der committeten Menge wurde (**16/19 → 17/20**). Dieser Vorgang
ist mit dem Eintrag in [RISK_REGISTER.md](RISK_REGISTER.md) **identisch** und
zählt **nur einmal**.

### Achtzehnter Konsistenzvorgang — CBP-WP-021 Canonical Security Test Inventory Reconciliation (2026-08-03)

**Gefunden in CBP-WP-021 Phase A, behandelt in B0 bis B1/B2.2.** Der überholte
Wert **31** wurde als **aktive Security-Foundation-Negativtest-Gesamtzahl**
fortgeschrieben, obwohl die authoritative A2-Acceptance-Matrix **32**
Negativtests auszählt.

**Herkunft:** **31** war der von CBP-WP-011 auf **33** korrigierte
**Gesamtwert** (30 NT + 1 PT). Die Zusammenfassungszeile jenes Work Packages
wurde beim eigenen Zählaudit nicht mitgeführt und etikettierte den Gesamtwert
zusätzlich als „Negativtests". Von dort wanderte die Zahl über die Roadmap in
spätere Dokumente **und in ausführbare Artefakte**.

**Betroffen:** Status- und Roadmapdokumente (`CLAUDE.md`, `README.md`,
`project-brain/PROJECT_BRAIN.md`, `project-system/HEALTH_SCORE.md`,
`project-system/PROJECT_MANIFEST.md`, `project-system/PROJECT_PROFILE.md`,
`project-system/WORK_PACKAGE_QUEUE.md`,
`docs/roadmap/PHASE_1_WORK_PACKAGE_MAP.md`,
`docs/roadmap/PHASE_1_FOUNDATION_PLAN.md`), Profil-A-Dokumentation (beide
Runbooks, Runtime-Vertrag), Work Packages (`CBP-WP-011.md`, `CBP-WP-020.md`,
`CBP-WP-021.md`) sowie die **ausführbaren Artefakte**
`deployments/profile-a/bundle.json`, `deployments/profile-a/validate.py`,
`deployments/profile-a/README.md` und `tests/test_profile_a_deployment_bundle.py`.

**Besonderheit:** **Erstmals war ein Konsistenzfehler nicht rein redaktionell**,
sondern in **committetem, ausführbarem Code** verankert — Bundlevertrag,
fail-closed Validator und Bundle-Test erzwangen den falschen Wert. Die Korrektur
musste deshalb **atomar** erfolgen; eine Teiländerung hätte die
Bundlevalidierung sofort gebrochen.

**Autorität:** **D-056** (`accepted`, **A0**, 2026-08-03) stellt fest: **32**
aktive Negativtests (NT-01…NT-24, NT-26…NT-33), **1** Positivtest (**PT-01**),
**33** Testfälle; **NT-25** bleibt nach Regel **TT-5** frei; **NT-32** und
**NT-33** sind gültig; **31** ist ein überholter, falsch etikettierter
Ableitungswert.

**Korrigiert** in vier Teilschritten, die zu **genau einem** Konsistenzvorgang
gehören: **B0** (`0cb4ea9`) Registrierung und Authority · **B1/B2** (`271acc7`)
dokumentarische **und** ausführbare Angleichung auf **32 / 1 / 33** ·
**B1/B2.1** Schließung der Restfundstelle in der Profil-A-README · **B1/B2.2**
Bereinigung des erzeugten Repository-Bytecodes.

**Wirkung:** kein Funktionsfehler, keine Runtimeänderung, keine Installation,
keine Bereitstellung, kein Containerstart, keine Gatefreigabe, keine
Aktivierung, keine Capability-Änderung; **D-056 unverändert**; **die
Reconciliation einer Inventarzahl ist keine Testausführung** — ausgeführt
bleiben **0 von 32** Negativtests und **0 von 1** Positivtest; das Bundleschema
enthält **keinen** eigenen Positivtestzähler und wurde **nicht** erweitert;
Capabilities **0 von 29**; beide Runtime-Gates `NOT EVALUATED`; die zwölf
KB-Kontrollen `DOCUMENTED ONLY`; **R-20 bleibt offen**.

**R-33 bleibt `gemindert, nicht geschlossen`** — Kritikalität unverändert
**mittel**, kein Risiko geschlossen, **keine neue Risiko-ID**. **Achtzehn
Konsistenzvorgänge in einundzwanzig Work Packages** waren dokumentiert (*Stand
nach dem achtzehnten Vorgang; durch den neunzehnten Vorgang unten auf
**19/22** und durch die Vorgänge zwanzig bis zweiundzwanzig fortlaufend auf
**22/22** aktualisiert*; löste „siebzehn" ab); die Zahl der Work Packages steigt
auf **einundzwanzig**, weil dieser Vorgang **erstmals CBP-WP-021** betrifft, das
durch `271acc7` Teil der committeten Menge wurde (**17/20 → 18/21**). **Das
projektweite Konsistenzrisiko ist nicht beseitigt.** Dieser Vorgang ist mit dem
Eintrag in [RISK_REGISTER.md](RISK_REGISTER.md) **identisch** und zählt **nur
einmal**.

**Die Implementierung von CBP-WP-013 selbst führte keinen arithmetischen
Zählfehler ein.** Testzahl (**137**) aus `Ran N tests`, Git-Inventar aus
`git status --porcelain=v1 -uall`, Entscheidungs- und ADR-Zahlen aus den
Quelltabellen ausgezählt. Die **zwei** in CBP-WP-013 gefundenen Testdefekte
betrafen Testcode (Docstring-Prosa-Grep; Zeilenenden-Normalisierung), keine
Kennzahl. **Der achte Konsistenzvorgang entstand erst im ersten
Nova-Korrekturlauf** — in den beiden oben genannten Dokumenten — und ist als
solcher in der Tabelle geführt. **R-33 bleibt offen.**

### Neunzehnter Konsistenzvorgang — CBP-WP-022 D-066-Zählerspiegel-Reconciliation (2026-08-05)

**Gefunden in CBP-WP-022 Phase B2D-E-N07-GOV, behandelt im Retry
B2D-E-N07-GOV-N1-R1.** Zwei allgemeine Statusspiegel führten **veraltete
Decision- und A0-Zähler**: `CLAUDE.md` und `project-brain/PROJECT_BRAIN.md`
wiesen **61** Decisions und **57** mit **A0** aus, während das kanonische
Decision Register bereits **65** Decisions und **61** mit **A0** führte. Die
ADR-Zahl **14** war korrekt. Die Abweichung betrug **je vier fehlende
Fortschreibungen**.

**Herkunft:** Der Stand entstammt Commit **`38eb33f`**. Die Fortschreibung
unterblieb bei **D-062**, **D-063**, **D-064** und **D-065**. Betroffen waren
ausschließlich Zeilen allgemeiner Zustandstabellen; die **phasendatierten
Momentaufnahmen** in `project-system/WORK_PACKAGE_QUEUE.md` und
`work-packages/CBP-WP-022.md` waren **korrekt** und wiesen zuletzt
**65/61/14** aus.

**Betroffen:** **`CLAUDE.md`** und **`project-brain/PROJECT_BRAIN.md`** — je
genau eine Zeile des allgemeinen Projektzustands.

**Besonderheit:** **Rein dokumentarisch.** Im Gegensatz zum achtzehnten
Vorgang war **kein ausführbares Artefakt** betroffen — weder Bundlevertrag
noch fail-closed Validator noch Bundle-Test. Der Fehler wurde **innerhalb**
des D-066-Laufs durch die vorgeschriebene Zählerprüfung gefunden und **nicht**
durch die fünfteilige Zähl- und Statusregel verhindert.

**Autorität:** **D-066** (`accepted`, **A0**, 2026-08-05, Result
`PROFILE_A_RETRIEVAL_NOT_INSTANTIATED_N07_DEFERRED`, ADR-Gate
`ADR_NOT_REQUIRED`). Die Registrierung erfolgt im selben Kandidaten; **D-062
bis D-065 bleiben unverändert**.

**Korrigiert:** Im D-066-Arbeitsbaum wurden beide Spiegel auf den
Kandidatenstand **66** Decisions · **62** mit **A0** · **14** ADRs gebracht —
innerhalb des autorisierten D-066-Dateiscopes und im D-066-Ausführungsbericht
offengelegt, dessen Result deshalb **`COUNTER_INCONSISTENCY`** lautete. Die
Registrierung dieses Vorgangs erfolgte im Retry **B2D-E-N07-GOV-N1-R1**,
nachdem der erste Versuch mit **`ALLOWLIST_INSUFFICIENT`** angehalten hatte,
weil dieses Dokument außerhalb des damaligen Dateiscopes lag.

**Closure:** Die **aktiven** Decision- und A0-Spiegel stimmen im aktuellen
Arbeitsbaum wieder mit dem kanonischen Decision Register überein; der Vorgang
ist im Kandidaten **behoben**.

**Wirkung:** **keine Decision vor D-066 geändert**, **keine ADR geändert**,
**keine Risiko-ID ergänzt**, **keine Severity geändert**, **keine Tests
geändert**, **keine Traceability geändert**, **keine technische
Reifeaussage**; die **D-066-Semantik ist unverändert**; **KB-04 bleibt
`DOCUMENTED ONLY`**; Mapping Activation Gate und Security Foundation
Readiness Gate bleiben `NOT EVALUATED`; Capabilities **0 von 29**; **NT-04 und
NT-05 nicht ausgeführt**; **OD-37 offen**; **Contract §10.3 offen**;
**`KB04-T-N07` zurückgestellt**; **`KB04-T-N14` nicht autorisiert**; **R-20
bleibt offen**.

**R-33 bleibt `gemindert, nicht geschlossen`** — Kritikalität unverändert
**mittel**, kein Risiko geschlossen, **keine neue Risiko-ID**. **Neunzehn
Konsistenzvorgänge in zweiundzwanzig Work Packages** waren dokumentiert (*Stand
nach dem neunzehnten Vorgang; durch die Vorgänge zwanzig bis zweiundzwanzig
unten fortlaufend auf **20/22**, **21/22** und **22/22** aktualisiert*; löste
„achtzehn" ab); die Zahl der Work Packages steigt
auf **zweiundzwanzig**, weil dieser Vorgang **erstmals CBP-WP-022** betrifft,
das durch die Commits `e4caa14` bis `0cd21f5` Teil der committeten Menge ist
(**18/21 → 19/22**). **Das projektweite Konsistenzrisiko ist nicht
beseitigt** — dieser Vorgang belegt es erneut. Dieser Vorgang ist mit dem
Eintrag in [RISK_REGISTER.md](RISK_REGISTER.md) **identisch** und zählt **nur
einmal**. Die dortige Darstellung folgt der **Tabellenform** des Risk
Registers, während hier die **Prosaform** dieses Dokuments verwendet wird;
**Fakten, Zahlen, Closure-Grenze und R-33-Wirkung sind identisch**.

### Zwanzigster Konsistenzvorgang — CBP-WP-022 B2D-ENV-GOV Active Phase-status Mirrors Staleness (2026-08-06)

**Gefunden im read-only Bericht CBP-WP-022 Phase B2D-E-N14-HM-AUTH-PREP,
registriert in Phase B2D-E-N14-HM-AUTH-PREP-R33-N1 und in Phase
B2D-E-N14-HM-AUTH-PREP-R33-N2 auf alle bestätigten Fundstellen erweitert.**
**Mehrere aktive Statusspiegel** führten den Commitstatus **einer** Phase
falsch. In `CLAUDE.md` stand die falsche Angabe sogar **zweimal
widersprüchlich in einer Zelle**: die Phasenaufzählung wies **`B2D-ENV-GOV
uncommitted`** aus, während wenige Sätze später **in derselben Zelle** korrekt
**B2D-ENV-GOV ist `committed` (`0cd21f5`)** stand.

**Fehlerklasse:** **Unterbliebene Fortschreibung aktiver
Phasenstatusspiegel.** Alle Fundstellen entstanden im B2D-ENV-GOV-Lauf, als die
Phase tatsächlich noch nicht committet war; die Post-Commit-Fortschreibung
unterblieb, während spätere Läufe an anderer Stelle derselben Dokumente den
korrekten Zustand ergänzten — daher der Widerspruch.

**Betroffene aktive Artefakte — drei:**

| Artefakt | Falsche aktive Aussagen |
| --- | --- |
| **`CLAUDE.md`** | **`B2D-ENV-GOV uncommitted`** in der Zeile des aktiven Work Packages (*Aktueller Zustand*) |
| **`project-system/WORK_PACKAGE_QUEUE.md`** | **`B2D-ENV-GOV uncommitted`** in der Queue-Tabellenzeile · **`B2D-ENV-GOV nicht committed`** im Detailfeld *Commit* · **B2D-ENV-GOV als aktuelle Phase** in der Kopfzeile *Aktuelles Work Package*, im Feld *Stand* und im Detailfeld *Aktuelle Phase* |
| **`docs/roadmap/PHASE_1_WORK_PACKAGE_MAP.md`** | **„Phase B2D-ENV-GOV abgeschlossen und uncommitted"** in der aktiven Fortschrittsaussage |

**Warum genau ein Vorgang:** **eine** Phase · **ein** korrekter Commitstatus ·
**ein** gemeinsamer Root Cause — die unterbliebene Post-Commit-Fortschreibung
derselben Angabe · **eine** gemeinsame Reconciliation. Für einzelne
B2D-ENV-GOV-Zeilen wird deshalb **kein** zusätzlicher Konsistenzvorgang
angelegt.

**Abgrenzung:** Keine der Fundstellen ist eine **zitierte historische
Momentaufnahme** oder eine **bewusst markierte Darstellung eines früheren
Zustands**; alle stehen unmarkiert in aktiven Statusdarstellungen. Die
phasendatierten Momentaufnahmen — etwa die Phasenabsätze „(dieser Stand,
uncommitted)" in den Detailblöcken von `WORK_PACKAGE_QUEUE.md` und die
Abschnitte *Stand nach …* mit „complete (dieser Stand, uncommitted)" in
`work-packages/CBP-WP-022.md` — sind **ausdrücklich markiert**, damals
zutreffend und bleiben **unverändert**. *Präzisiert im R-33 Active-Status
Closure Fix:* Diese Ausnahme gilt **nur** für echte phasendatierte Abschnitte;
die **aktive Phasenmodelltabelle** in `work-packages/CBP-WP-022.md` ist ein
Live-Statusspiegel und keine Momentaufnahme — ihre Zeile B2D-E-N14-GOV ist im
**vierundzwanzigsten** Vorgang reconciliiert. Am committeten HEAD **`c662452`**
bestand eine **tatsächliche aktive Statusinkonsistenz**. Der Sachverhalt war in den bisherigen
**neunzehn** Vorgängen **nicht** als eigener Vorgang registriert.

**Korrigiert:** Alle bestätigten aktiven Fundstellen wurden auf **B2D-ENV-GOV
`committed` (`0cd21f5`)** und auf die tatsächliche aktuelle Phase
**B2D-E-N14-GOV** gebracht. **Keine phasendatierte historische Momentaufnahme
überschrieben.**

**Wirkung:** **keine technische Implementierungsänderung**, **keine
Decisionänderung**, **keine ADR-Änderung**, **keine Risikoänderung**, **keine
neue Risiko-ID**, **keine Teständerung**, **keine Traceabilityänderung**,
**keine Capabilityänderung**; **D-067 unverändert**; **KB-04 bleibt
`DOCUMENTED ONLY`**; Mapping Activation Gate und Security Foundation Readiness
Gate bleiben `NOT EVALUATED`; Capabilities **0 von 29**; **`KB04-T-N14` nicht
ausgeführt und nicht lokal autorisiert**; **NT-04 und NT-05 nicht ausgeführt**;
**OD-37 offen**; **Contract §10.3 offen**; **R-20 bleibt offen**.

**R-33 bleibt `gemindert, nicht geschlossen`** — Kritikalität unverändert
**mittel**, kein Risiko geschlossen, **keine neue Risiko-ID**. **Zwanzig
Konsistenzvorgänge in zweiundzwanzig Work Packages** waren dokumentiert (*Stand
nach dem zwanzigsten Vorgang; durch den einundzwanzigsten Vorgang unten auf
**21/22** und durch den zweiundzwanzigsten auf **22/22** aktualisiert*; löste
„neunzehn" ab); die Zahl der Work Packages bleibt **zweiundzwanzig**, weil
CBP-WP-022 durch den neunzehnten Vorgang **bereits** Teil der erfassten Menge
war — ein weiterer Vorgang im selben, bereits erfassten Work Package erhöht
**nur** den Vorgangszähler (**19/22 → 20/22**). **Das projektweite
Konsistenzrisiko ist nicht beseitigt** — der zwanzigste Vorgang belegt es
unmittelbar nach dem neunzehnten. Dieser Vorgang ist mit dem Eintrag in
[RISK_REGISTER.md](RISK_REGISTER.md) **identisch** und **zählt nur einmal**. Die
dortige Darstellung folgt der **Tabellenform** des Risk Registers, während hier
die **Prosaform** dieses Dokuments verwendet wird; **Fakten, Zahlen,
Closure-Grenze und R-33-Wirkung sind identisch**.

### Einundzwanzigster Konsistenzvorgang — CBP-WP-022 B2B-P Active Commit-status Mirror Staleness (2026-08-06)

**Gefunden im read-only Bericht CBP-WP-022 Phase B2D-E-N14-HM-AUTH-PREP und
dort als unregistrierte Nebenbeobachtung ausgewiesen; registriert in Phase
B2D-E-N14-HM-AUTH-PREP-R33-N2.** Die **aktive** Statusdarstellung in
`README.md` — die Zeile des aktuellen Work Packages im Abschnitt *Aktueller
Stand* — führte in der Phasen-Commit-Aufzählung **`B2B-P uncommitted`**.

**Fehlerklasse:** **Unterbliebene Fortschreibung eines aktiven
Commitstatusspiegels** — dieselbe Klasse wie der zwanzigste Vorgang, jedoch
**andere Phase**, **anderer Commit** und **anderes Artefakt**. Deshalb ein
**eigener** Vorgang.

**Betroffen — zwei aktive Artefakte:** **`README.md`** (eine aktive Statuszelle,
Aufzählung **`B2B-P uncommitted`**) und
**`docs/roadmap/PHASE_1_WORK_PACKAGE_MAP.md`** (aktive Fortschrittsaussage
**„Phase B2B-P ist abgeschlossen und uncommitted"**). Die zweite Fundstelle
wurde in Phase **B2D-E-N14-HM-AUTH-PREP-R33-N3** nachgetragen; **mehrere
Fundstellen derselben Fehlerursache bleiben genau ein Vorgang** und erhöhen den
Zähler **nicht** erneut.

**Korrekter Zustand:** **B2B-P ist `committed`**, Commit **`fff8227`** —
*„CBP-WP-022: add KB-04 initialization planning and safety guards"*.

**Abgrenzung:** **Keine zitierte historische Momentaufnahme**, **keine bewusst
markierte frühere Phase**; die Aussage steht unmarkiert in der aktiven
Statusdarstellung. Im Gegensatz zum zwanzigsten Vorgang enthält `README.md`
**keine** gegenläufige korrekte Angabe — der Fehler ist eine **reine
Fortschreibungslücke**. In den bisherigen **zwanzig** Vorgängen **nicht** als
eigener Vorgang registriert.

**Korrigiert:** Beide Fundstellen wurden auf **B2B-P `committed` `fff8227`**
gebracht. **Keine weitere Angabe dieser Dateien verändert** — insbesondere
bleibt die ausdrücklich markierte Momentaufnahme
`WORK_PACKAGE_QUEUE.md` „Phase B2B-P (dieser Stand, uncommitted)" und die
Phasenüberschrift in `work-packages/CBP-WP-022.md` unverändert.

**Erweiterung im R-33 Active-Status Closure Fix (2026-09-21):** Der
repositoryweite read-only Vollständigkeitsaudit bestätigte **zwei weitere
Fundstellen derselben Fehlerursache** in **`project-brain/PROJECT_BRAIN.md`** —
die Phasen-Commit-Aufzählung der Zeile *Aktuelles Work Package* und die Zeile
*Geplante Work Packages* führten jeweils **`B2B-P uncommitted`**. Beide wurden
auf **B2B-P `committed` `fff8227`** gebracht. **Zählneutral** — dieselbe Phase,
derselbe Commit, dieselbe Fehlerursache; **kein neuer Vorgang**, Zähler und
Nenner unverändert.

**Wirkung:** **keine technische Implementierungsänderung**, **keine
Decisionänderung**, **keine ADR-Änderung**, **keine Risikoänderung**, **keine
neue Risiko-ID**, **keine Teständerung**, **keine Traceabilityänderung**,
**keine Capabilityänderung**.

**R-33 bleibt `gemindert, nicht geschlossen`** — Kritikalität unverändert
**mittel**. **Einundzwanzig Konsistenzvorgänge in zweiundzwanzig Work
Packages** waren dokumentiert (*Stand nach dem einundzwanzigsten Vorgang; durch
den zweiundzwanzigsten Vorgang unten auf **22/22** aktualisiert*; löste
„zwanzig" ab); der Nenner bleibt **zweiundzwanzig** (**20/22 → 21/22**). Dieser
Vorgang ist mit dem Eintrag in [RISK_REGISTER.md](RISK_REGISTER.md)
**identisch** und **zählt nur einmal**; **Fakten, Zahlen, Closure-Grenze und
R-33-Wirkung sind identisch**.

### Zweiundzwanzigster Konsistenzvorgang — CBP-WP-022 B2D-E-N07-GOV Active Commit-status Mirror Staleness (2026-08-06)

**Gefunden im read-only Bericht CBP-WP-022 Phase B2D-E-N14-HM-AUTH-PREP und
dort als unregistrierte Nebenbeobachtung ausgewiesen; registriert in Phase
B2D-E-N14-HM-AUTH-PREP-R33-N2.** Die **aktive** Statusdarstellung in
`project-system/PROJECT_MANIFEST.md` — die Zeile des aktuellen Work Packages im
Abschnitt *Status* — führte in der Phasen-Commit-Aufzählung
**`B2D-E-N07-GOV uncommitted`**.

**Fehlerklasse:** **Unterbliebene Fortschreibung eines aktiven
Commitstatusspiegels** — dieselbe Klasse wie der zwanzigste und
einundzwanzigste Vorgang, jedoch **andere Phase**, **anderer Commit** und
**anderes Artefakt**. Deshalb ein **eigener** Vorgang.

**Betroffen:** **`project-system/PROJECT_MANIFEST.md`** — genau eine aktive
Statuszelle.

**Korrekter Zustand:** **B2D-E-N07-GOV ist `committed`**, Commit **`c4b0426`** —
*„CBP-WP-022: defer N07 retrieval and reconcile R-33"*.

**Abgrenzung:** **Keine zitierte historische Momentaufnahme**, **keine bewusst
markierte frühere Phase**. Die Zeile weist die aktuelle Phase
**B2D-E-N14-GOV** korrekt aus, führte den unmittelbar davorliegenden
Phasencommit aber weiter als offen; der Commit **`c4b0426`** war in dieser
Datei **an keiner Stelle** genannt — eine **reine Fortschreibungslücke**. In
den bisherigen **einundzwanzig** Vorgängen **nicht** als eigener Vorgang
registriert.

**Korrigiert:** **`B2D-E-N07-GOV uncommitted`** wurde durch **B2D-E-N07-GOV
`committed` `c4b0426`** ersetzt. **Keine weitere Angabe dieser Datei
verändert.**

**Wirkung:** **keine technische Implementierungsänderung**, **keine
Decisionänderung**, **keine ADR-Änderung**, **keine Risikoänderung**, **keine
neue Risiko-ID**, **keine Teständerung**, **keine Traceabilityänderung**,
**keine Capabilityänderung**; **D-067 unverändert**; **KB-04 bleibt
`DOCUMENTED ONLY`**; Mapping Activation Gate und Security Foundation Readiness
Gate bleiben `NOT EVALUATED`; Capabilities **0 von 29**; **`KB04-T-N14` nicht
ausgeführt und nicht lokal autorisiert**; **NT-04 und NT-05 nicht ausgeführt**;
**OD-37 offen**; **Contract §10.3 offen**; **R-20 bleibt offen**.

**R-33 bleibt `gemindert, nicht geschlossen`** — Kritikalität unverändert
**mittel**, kein Risiko geschlossen, **keine neue Risiko-ID**.
**Zweiundzwanzig Konsistenzvorgänge in zweiundzwanzig Work Packages** waren
dokumentiert (*Stand nach dem zweiundzwanzigsten Vorgang; durch den
dreiundzwanzigsten Vorgang unten auf **23/22** aktualisiert*; löste
„einundzwanzig" ab); die Zahl der Work Packages bleibt **zweiundzwanzig**, weil
die Vorgänge **20**, **21** und **22** dasselbe, seit dem neunzehnten Vorgang
bereits erfasste Work Package CBP-WP-022 betreffen und **ausschließlich** den
Vorgangszähler erhöhen (**19/22 → 20/22 → 21/22 → 22/22**). Nennerkonstanz ist
**kein Erstfall** — sie trat bereits beim **fünfzehnten** Vorgang auf
(`14/18 → 15/18`). **Das projektweite Konsistenzrisiko ist nicht beseitigt** —
drei Vorgänge derselben Klasse an einem Tag belegen es unmittelbar. Dieser
Vorgang ist mit dem Eintrag in [RISK_REGISTER.md](RISK_REGISTER.md)
**identisch** und **zählt nur einmal**. Die dortige Darstellung folgt der
**Tabellenform** des Risk Registers, während hier die **Prosaform** dieses
Dokuments verwendet wird; **Fakten, Zahlen, Closure-Grenze und R-33-Wirkung
sind identisch**.

### Dreiundzwanzigster Konsistenzvorgang — CBP-WP-022 Active Current-phase Mirrors Staleness (2026-08-06)

**Im Bericht CBP-WP-022 Phase B2D-E-N14-HM-AUTH-PREP-R33-N2 als verbleibende,
ausdrücklich nicht registrierte Beobachtung ausgewiesen; registriert in Phase
B2D-E-N14-HM-AUTH-PREP-R33-N3.** **Zwei** aktive Current-Phase-Spiegel
benannten eine **falsche aktuelle Phase**: `README.md` führte **`B2B-P`**, die
Roadmapkarte **`B2B-P`** im Kopffeld *Stand* und **`B2D-P`** in der
Work-Package-Tabellenzeile.

**Fehlerklasse:** **Unterbliebene Fortschreibung aktiver
Current-Phase-Spiegel.** Anders als bei den Vorgängen 20 bis 22 betrifft der
Fehler **nicht** den Commitstatus einer einzelnen Phase, sondern die Angabe,
**welche Phase gegenwärtig aktuell ist**. Beide Spiegel wurden über **mehrere**
Phasen hinweg nicht fortgeschrieben, während die Phasenkette bis
**B2D-E-N14-GOV** fortschritt.

**Betroffene aktive Artefakte — zwei:**

| Artefakt | Falscher aktiver Current-Phase-Wert |
| --- | --- |
| **`README.md`** | **`B2B-P`** in der Zeile *Aktuelles Work Package* (§ *Aktueller Stand*) |
| **`docs/roadmap/PHASE_1_WORK_PACKAGE_MAP.md`** | **`B2B-P`** im Kopffeld *Stand* · **`B2D-P`** in der Work-Package-Tabellenzeile CBP-WP-022 |

**Korrekter gemeinsamer Zustand:** Phase **`B2D-E-N14-GOV`** — *N14 Ephemeral
Observation Bridge Classification*; Decision **D-067** (`accepted`, **A0**);
Commit **`c662452`**.

**Aktiv, nicht historisch:** Beide Fundstellen sind **Top-Level-Current-Phase-
Spiegel** ihrer Dokumente, stehen **unmarkiert**, tragen **keine** Zitatform
und **keinen** Hinweis auf einen früheren Zustand. Beide Dateien nennen **an
anderer Stelle** bereits korrekt **B2D-E-N14-GOV** und **D-067** — der
Widerspruch ist dateiintern belegt. In den bisherigen **zweiundzwanzig**
Vorgängen **nicht** als eigener Vorgang registriert.

**Warum genau ein Vorgang:** **derselbe Spiegeltyp** — aktiver
Current-Phase-Spiegel · **derselbe Zielzustand** — `B2D-E-N14-GOV` / D-067 /
`c662452` · **dieselbe Fortschreibungsfehlerklasse** · **eine** gemeinsame
Reconciliation. Deshalb **keine** eigene Ereignisnummer je Datei.

**Korrigiert:** Beide aktiven Current-Phase-Spiegel wurden auf **Phase
`B2D-E-N14-GOV` – D-067, `committed` `c662452`** gebracht. **Keine historische
Phasenangabe ersetzt** — insbesondere bleiben **B2D-P ist `committed`
(`b409d25`)** und **B2B-P `committed` `fff8227`** unverändert, ebenso alle
früheren Work-Package-Planungen und accepted Governancegrenzen.

**Erweiterung im R-33 Active-Status Closure Fix (2026-09-21):** Der
repositoryweite read-only Vollständigkeitsaudit bestätigte **vier weitere aktive
Current-Phase-Spiegel desselben Spiegeltyps** mit **demselben Zielzustand**:
**`project-brain/PROJECT_BRAIN.md`** (Zeile *Geplante Work Packages*:
**`B2B-P`**) · **`project-system/HEALTH_SCORE.md`** (Zeile *Vorgeschlagene Work
Packages*: **`B2C.2`**) · **`project-system/PROJECT_PROFILE.md`** (Zeile
*Phase 1*: **`B2C.1 – Synthetic Evidence Scope Decision`**) ·
**`project-system/WORK_PACKAGE_QUEUE.md`** (Übersichtsabsatz CBP-WP-022:
**`Phase B0 – Registration and Authority Baseline`**). Alle wurden auf **Phase
`B2D-E-N14-GOV` – D-067**, `committed` **`c662452`**, gebracht; im Queue-Absatz
blieb die Registrierungsangabe als **Phase B0 `committed` `e4caa14`** erhalten.
**Aussagen zum Autorisierungsstand in denselben Zeilen blieben wörtlich
unverändert.** **Zählneutral** — derselbe Spiegeltyp, derselbe Zielzustand,
dieselbe Fortschreibungsfehlerklasse; **kein neuer Vorgang**, Zähler und Nenner
unverändert.

**Wirkung:** **keine technische Implementierungsänderung**, **keine neue
Decision**, **keine ADR**, **keine Risikoänderung**, **keine neue Risiko-ID**,
**keine Teständerung**, **keine Traceabilityänderung**, **keine
Capabilityänderung**; **D-067 unverändert**; **KB-04 bleibt `DOCUMENTED
ONLY`**; Mapping Activation Gate und Security Foundation Readiness Gate bleiben
`NOT EVALUATED`; Capabilities **0 von 29**; **`KB04-T-N14` nicht ausgeführt und
nicht lokal autorisiert**; **NT-04 und NT-05 nicht ausgeführt**; **OD-37
offen**; **Contract §10.3 offen**; **R-20 bleibt offen**.

**R-33 bleibt `gemindert, nicht geschlossen`** — Kritikalität unverändert
**mittel**, kein Risiko geschlossen, **keine neue Risiko-ID**.
**Dreiundzwanzig Konsistenzvorgänge in zweiundzwanzig Work Packages** waren
dokumentiert (*Stand nach dem dreiundzwanzigsten Vorgang; durch die Vorgänge
vierundzwanzig bis dreißig unten fortlaufend auf **30/22** aktualisiert, die
Erweiterung dieses Vorgangs ist zählneutral*; löste „zweiundzwanzig" ab); die Zahl
der Work Packages bleibt **zweiundzwanzig**, weil Vorgang **23** — wie die
Vorgänge 20 bis 22 — das seit dem neunzehnten Vorgang bereits erfasste Work
Package CBP-WP-022 betrifft und **ausschließlich** den Vorgangszähler erhöht.
Vollständige Progression: **19/22 → 20/22 → 21/22 → 22/22 → 23/22**.
**`23/22` ist kein Erfüllungsgrad und keine Prozentkennzahl** — der Zähler
zählt dokumentierte Vorgänge, der Nenner Work Packages mit mindestens einem
Vorgang, und der Zähler **darf** den Nenner überschreiten; **`23/23` ist
unzulässig**. **Das projektweite Konsistenzrisiko ist nicht beseitigt** — vier
Vorgänge derselben Grundklasse an einem Tag belegen es unmittelbar. Dieser
Vorgang ist mit dem Eintrag in [RISK_REGISTER.md](RISK_REGISTER.md)
**identisch** und **zählt nur einmal**. Die dortige Darstellung folgt der
**Tabellenform** des Risk Registers, während hier die **Prosaform** dieses
Dokuments verwendet wird; **Fakten, Zahlen, Closure-Grenze und R-33-Wirkung
sind identisch**.

### Vierundzwanzigster Konsistenzvorgang — CBP-WP-022 B2D-E-N14-GOV Active Commit-status Mirrors Staleness (2026-09-21)

**Nach mehreren read-only Reviews im repositoryweiten read-only
Vollständigkeitsaudit bestätigt; registriert im abschließenden Lauf R-33
Active-Status Closure Fix**, der die Vorgänge 21 und 23 zählneutral erweitert
und genau sieben neue Vorgänge registriert. **Vier** aktive Spiegel führten den
Commitstatus der Phase **B2D-E-N14-GOV** falsch.

**Fehlerklasse:** **Unterbliebene Fortschreibung aktiver
Commitstatusspiegel** — dieselbe Grundklasse wie die Vorgänge 20 bis 22, jedoch
**andere Phase** und **anderer Commit**. Alle Fundstellen entstanden im
B2D-E-N14-GOV-Lauf **vor** dem Commit `c662452`; die Post-Commit-Fortschreibung
unterblieb.

| Artefakt | Falsche aktive Aussage |
| --- | --- |
| **`project-system/HEALTH_SCORE.md`** | **`B2D-E-N14-GOV uncommitted`** in der Zeile *Vorgeschlagene Work Packages* |
| **`project-system/PROJECT_PROFILE.md`** | **`B2D-E-N14-GOV uncommitted`** in der Zeile *Phase 1* |
| **`docs/roadmap/PHASE_1_WORK_PACKAGE_MAP.md`** | **„B2D-E-N14-GOV registriert D-067 (…), uncommitted"** in der Work-Package-Tabellenzeile CBP-WP-022 |
| **`work-packages/CBP-WP-022.md`** | **„complete (dieser Stand, uncommitted)"** in der Zeile B2D-E-N14-GOV der Phasenmodelltabelle |

**Korrekter Zustand:** **B2D-E-N14-GOV ist `committed`**, Commit **`c662452`** —
*„CBP-WP-022: classify N14 observation bridge"*.

**Aktiv, nicht historisch:** Alle Fundstellen stehen in aktiven Statuszeilen
beziehungsweise in der **aktiven Phasenmodelltabelle**. Der Vermerk „(dieser
Stand, uncommitted)" macht die Zeile einer Live-Statustabelle **nicht** zu einer
historischen Momentaufnahme — die Nachbarzeilen **B2D-ENV-GOV** und
**B2D-E-N07-GOV** derselben Tabelle waren bereits auf `committed`
fortgeschrieben. In den bisherigen **dreiundzwanzig** Vorgängen **nicht** als
eigener Vorgang registriert.

**Korrigiert:** Alle vier Fundstellen wurden auf **B2D-E-N14-GOV `committed`
`c662452`** gebracht; die Phasenmodellzeile folgt der Form ihrer Nachbarzeilen.
**Eine** Phase, **ein** Commit, **eine** Fehlerursache, **eine** Reconciliation
— **genau ein** Vorgang trotz vier Fundstellen. **Zählwirkung: `23/22 → 24/22`**,
Nenner unverändert.

### Fünfundzwanzigster Konsistenzvorgang — CBP-WP-022 Active Commit-field Sequence Staleness (2026-09-21)

**Im repositoryweiten read-only Vollständigkeitsaudit bestätigt; registriert im
R-33 Active-Status Closure Fix.** Das Kopffeld *Commit* in
**`work-packages/CBP-WP-022.md`** endete bei **B2B-P `committed` `fff8227`** und
führte **„B2C.1 nicht committed"**; sämtliche Commits ab B2C.1 fehlten.

**Fehlerklasse:** **Unterbliebene Fortschreibung eines aktiven Commitfelds** über
**neun** Phasencommits hinweg. Der Eintrag entstand im B2C.1-Lauf **vor** dessen
Commit `38eb33f`; keiner der folgenden Läufe schrieb das Feld fort, obwohl die
Phasenmodelltabelle derselben Datei die Commits zeilenweise auswies. Ein
**aktives Kopffeld**, keine Momentaufnahme — die Abschnitte *Stand nach …*
derselben Datei bleiben unverändert. In den bisherigen **vierundzwanzig**
Vorgängen **nicht** als eigener Vorgang registriert.

**Korrigiert:** Die Folge wurde vervollständigt — **B2C.1 `38eb33f`** ·
**B2C.2 `117647f`** · **B2C-T-R `9cde9de`** · **B2D-P `b409d25`** ·
**B2D-GOV `7e8328a`** · **B2D-AUTH `1222ec0`** · **B2D-ENV-GOV `0cd21f5`** ·
**B2D-E-N07-GOV `c4b0426`** · **B2D-E-N14-GOV `c662452`**, sämtlich
`committed`; die Angaben B0 bis B2B-P und der Vermerk zur Commit-Autorität
blieben unverändert. **Ein** Feld, **eine** Fehlerursache — **genau ein**
Vorgang. **Zählwirkung: `24/22 → 25/22`**, Nenner unverändert.

### Sechsundzwanzigster Konsistenzvorgang — CBP-WP-022 B2C-T-R Active Commit-status Mirrors Staleness (2026-09-21)

**Im repositoryweiten read-only Vollständigkeitsaudit bestätigt; registriert im
R-33 Active-Status Closure Fix.** **Zwei** aktive Spiegel führten B2C-T-R als
nicht committet: **`docs/roadmap/PHASE_1_WORK_PACKAGE_MAP.md`** (**„Phase
B2C-T-R ist abgeschlossen und uncommitted"**) und
**`project-system/WORK_PACKAGE_QUEUE.md`** (Kopfzeile *Aktuelles Work Package*:
**`B2C-T-R uncommitted`**, zusätzlich mit unausgeglichener Fettmarkierung).

**Fehlerklasse:** **Unterbliebene Fortschreibung aktiver
Commitstatusspiegel** — dieselbe Grundklasse wie der vierundzwanzigste Vorgang,
jedoch **andere Phase** und **anderer Commit**. Beide Aussagen entstanden im
B2C-T-R-Lauf **vor** dem Commit `9cde9de`. Beide Dateien weisen **an anderer
Stelle** bereits korrekt **B2C-T-R `committed` `9cde9de`** aus — der Widerspruch
ist dateiintern belegt. In den bisherigen **fünfundzwanzig** Vorgängen **nicht**
als eigener Vorgang registriert.

**Korrekter Zustand und Korrektur:** **B2C-T-R ist `committed`**, Commit
**`9cde9de`** — *„CBP-WP-022: add KB-04 contract traceability and NT
preparation"*. Beide Fundstellen wurden entsprechend gebracht, die
Fettmarkierung der Queue-Aufzählung ist ausgeglichen; die Aussage zum
Autorisierungsstand am Ende derselben Queue-Zeile blieb **wörtlich
unverändert**. **Genau ein** Vorgang trotz zweier Artefakte. **Zählwirkung:
`25/22 → 26/22`**, Nenner unverändert.

### Siebenundzwanzigster Konsistenzvorgang — CBP-WP-022 B1C Active Commit-status Mirror Staleness (2026-09-21)

**Im repositoryweiten read-only Vollständigkeitsaudit bestätigt; registriert im
R-33 Active-Status Closure Fix.** Die aktive Fortschrittsaussage im Absatz zu
CBP-WP-022 in **`docs/roadmap/PHASE_1_WORK_PACKAGE_MAP.md`** führte **„Phase
B1C ist abgeschlossen und uncommitted"**.

**Fehlerklasse:** **Unterbliebene Fortschreibung eines aktiven
Commitstatusspiegels** — dieselbe Grundklasse, jedoch **andere Phase** und
**anderer Commit**. Die Aussage entstand im B1C-Lauf **vor** dessen Commit
`24de07e`; spätere Läufe ergänzten wenige Absätze darunter **„Phase B1C ist
`committed` (`24de07e`)"**, schrieben die ursprüngliche Aussage aber nicht fort
— der Widerspruch ist dateiintern belegt. In den bisherigen
**sechsundzwanzig** Vorgängen **nicht** als eigener Vorgang registriert.

**Korrekter Zustand und Korrektur:** **B1C ist `committed`**, Commit
**`24de07e`** — *„CBP-WP-022: define KB-04 enforcement contract and validation
plan"*; die Aussage lautet nun **„Phase B1C ist abgeschlossen und `committed`
(`24de07e`)"**, keine weitere Angabe verändert. **Zählwirkung:
`26/22 → 27/22`**, Nenner unverändert.

### Achtundzwanzigster Konsistenzvorgang — CBP-WP-021 Queue Detail Block Staleness (2026-09-21)

**Im repositoryweiten read-only Vollständigkeitsaudit bestätigt; registriert im
R-33 Active-Status Closure Fix, im Rahmen von CBP-WP-022.** Im Detailblock
CBP-WP-021 von **`project-system/WORK_PACKAGE_QUEUE.md`** standen *Status*
**`in-review`**, *Aktuelle Phase* **„Phase C – Post-Commit Reconciliation
(vorbereitet)"** und *Commit* **„nicht ausgeführt"**.

**Fehlerklasse:** **Git-/Register-Statusabweichung in einem Detailblock** —
dieselbe Klasse wie der **elfte** Vorgang. *Status* und *Commit* stammen aus der
Registrierung (`0cb4ea9`) und aus B1/B2 (`271acc7`); der Phase-C-Lauf
(`0344774`) setzte die Phase auf „vorbereitet", schrieb die drei Felder nach dem
Commit aber nicht fort. Queue-Tabelle, Kopfzeile und Übersichtsabsatz führten
CBP-WP-021 bereits korrekt als `committed`. Die Phasenabsätze **„Phase B1/B2
(dieser Stand, uncommitted)"** und **„Phase C (dieser Stand, uncommitted)"**
desselben Detailblocks sind echte phasendatierte Momentaufnahmen und bleiben
unverändert. In den bisherigen **siebenundzwanzig** Vorgängen **nicht** als
eigener Vorgang registriert.

**Korrekter Zustand und Korrektur:** **CBP-WP-021 ist `committed` und
`complete`**, Phase C abgeschlossen; die Felder lauten nun **`committed` ·
`complete`**, **„Phase C – Post-Commit Reconciliation (abgeschlossen)"** und
**B0 `committed` `0cb4ea9` · B1/B2 `committed` `271acc7` · C `committed`
`0344774`** — in der etablierten Form der Detailblöcke CBP-WP-020 und
CBP-WP-022. **Ein** Detailblock, **eine** Fehlerursache — **genau ein** Vorgang
trotz dreier Felder. **Der Nenner bleibt unverändert**, weil CBP-WP-021 seit dem
achtzehnten Vorgang bereits erfasst ist. **Zählwirkung: `27/22 → 28/22`.**

### Neunundzwanzigster Konsistenzvorgang — CBP-WP-019 Residual Queue Summary Status Staleness (2026-09-21)

**Im repositoryweiten read-only Vollständigkeitsaudit bestätigt, für diesen Lauf
verbindlich als eigener Vorgang festgelegt und im R-33 Active-Status Closure Fix
registriert, im Rahmen von CBP-WP-022.** Der Übersichtsabsatz unter der
Queue-Tabelle in **`project-system/WORK_PACKAGE_QUEUE.md`** führte
**„CBP-WP-019 (…) steht auf `in-review` in `committed` (`3c437f2`, …)"** — eine
widersprüchliche Kombination aus `in-review` und `committed`.

**Fehlerklasse:** **Residuum einer unvollständigen früheren Reconciliation.** Vor
dem Commit lautete der Satz **„steht auf `in-review` in Phase B1.2 – Human DRC
Approval Reconciliation"**; die Post-Commit-Reconciliation `387416b` ersetzte nur
die Phasenangabe durch **`committed`** und ließ **„steht auf `in-review` in"**
stehen. **Der sechzehnte Vorgang bleibt unverändert, wird nicht wiedereröffnet
und nicht rückwirkend neu gezählt.** In den bisherigen **achtundzwanzig**
Vorgängen **nicht** als eigener Vorgang registriert.

**Korrekter Zustand und Korrektur:** **CBP-WP-019 ist `committed`**, Commit
**`3c437f2`**; **„steht auf `in-review` in"** wurde durch **„ist"** ersetzt, alle
weiteren Angaben des Absatzes blieben unverändert. **Der Nenner bleibt
unverändert**, weil CBP-WP-019 seit dem sechzehnten Vorgang bereits erfasst ist.
**Zählwirkung: `28/22 → 29/22`.**

### Dreißigster Konsistenzvorgang — CBP-WP-022 Registration Lifecycle-state Mirrors Staleness (2026-09-21)

**Im repositoryweiten read-only Vollständigkeitsaudit bestätigt; registriert im
R-33 Active-Status Closure Fix.** Lebenszyklusaussagen, die nur bis zur
Registrierung von CBP-WP-022 zutrafen, wurden mit dem Registrierungscommit
**`e4caa14`** nicht fortgeschrieben.

**Betroffene aktive Artefakte — zwei:**

| Artefakt | Falsche aktive Aussage |
| --- | --- |
| **`docs/roadmap/PHASE_1_WORK_PACKAGE_MAP.md`** | **„Kein Work Package ist aktiv, kein Folge-Work-Package autorisiert."** im Absatz zu CBP-WP-021 · Block **„Aktueller Stand (nachgeführt in CBP-WP-020 Phase C …)"** mit **„Kein Work Package ist aktiv; kein Folge-Work-Package über CBP-WP-020 hinaus ist autorisiert."**, ohne CBP-WP-021 und CBP-WP-022 |
| **`project-brain/PROJECT_BRAIN.md`** | **„das KB-04-Paket ist lediglich als möglicher Kandidat vorgemerkt"** in der Zeile *Geplante Work Packages* |

**Fehlerklasse und Herkunft:** **Unterbliebene Fortschreibung von
Lebenszyklusaussagen bei der Registrierung eines Work Packages.** Der Absatz
entstand im Phase-C-Lauf von CBP-WP-021 (`0344774`), der Statusblock im
Phase-C-Lauf von CBP-WP-020 (`d6a1a3c`); beide trafen zu ihrem Zeitpunkt zu. In
`PROJECT_BRAIN.md` ersetzte der Registrierungslauf `e4caa14` in derselben Zeile
**„CBP-WP-022 nicht registriert …"** durch **„CBP-WP-023 nicht registriert …"**,
ließ den anschließenden Kandidatenhinweis aber stehen. Alle Fundstellen stehen
unmarkiert in aktiven Statusdarstellungen; der Statusblock bezeichnet sich
selbst als **Aktueller Stand**. In den bisherigen **neunundzwanzig** Vorgängen
**nicht** als eigener Vorgang registriert.

**Korrekter Zustand:** **CBP-WP-022 ist registriert** (D-057,
Registrierungscommit **`e4caa14`**) und das **aktuelle Work Package**,
`in-review`, Phase **B2D-E-N14-GOV – D-067**, `committed` **`c662452`**;
**CBP-WP-021 ist `committed` und `complete`**.

**Korrigiert:** Roadmapkarte: Absatz CBP-WP-021 und Statusblock auf den
aktuellen Lebenszyklus gebracht; die früheren Aussagen zum Aktivitäts- und
Autorisierungsstand blieben **inhaltlich erhalten** und sind ausdrücklich auf
ihren Abschlusszeitpunkt bezogen („Zum Abschluss von CBP-WP-020" bzw. „… von
CBP-WP-021"). `PROJECT_BRAIN.md`: Kandidatenhinweis durch die Registrierung als
**CBP-WP-022** (D-057, `e4caa14`) und den Status `in-review` ersetzt;
**„CBP-WP-023 nicht registriert, nicht begonnen, nicht autorisiert"** blieb
**wörtlich** erhalten. **Ein** Ereignis, **ein** korrekter Lebenszyklusstand,
**eine** Fehlerursache — **genau ein** Vorgang trotz dreier Fundstellen in zwei
Dateien. **Zählwirkung: `29/22 → 30/22`**, Nenner unverändert.

### Gemeinsame Wirkung der Vorgänge 24 bis 30 und Zurückstellung von AF-6

**Wirkung:** **keine technische Implementierungsänderung**, **keine neue
Decision**, **keine ADR**, **keine Risikoänderung**, **keine neue Risiko-ID**,
**keine Teständerung**, **keine Traceabilityänderung**, **keine
Capabilityänderung**, **keine Änderung einer Aussage zum Autorisierungsstand**;
**D-056** und **D-067** unverändert; **KB-04 bleibt `DOCUMENTED ONLY`**; Mapping
Activation Gate und Security Foundation Readiness Gate bleiben `NOT EVALUATED`;
Capabilities **0 von 29**; **`KB04-T-N14`**, **NT-04** und **NT-05** nicht
ausgeführt; **OD-37**, **Contract §10.3** und **R-20** bleiben offen.

**Bekannter, zurückgestellter Befund AF-6 — kein Konsistenzvorgang dieser
Chronologie:** Die Angaben zum Git-Gesamtzähler und zum HEAD in
`project-brain/PROJECT_BRAIN.md`, `project-system/HEALTH_SCORE.md` und
`project-system/PROJECT_MANIFEST.md` (**Commits 29**, HEAD **`9c6c0fb`**) sind
veraltet. **D-056 Teil T** nimmt die Commitzähler-Governance aus und verweist
sie in eine separate Governance-Note; CBP-WP-022 schließt sie ausdrücklich aus
(Non-Goal *keine Commitzähler-Governance*). Gemäß **A0-Festlegung** für diesen
Lauf (**keine neue Decision-ID**) ist AF-6 **bekannt und zurückgestellt**, **kein
einunddreißigster Vorgang** und **ohne Zählwirkung**; die drei Felder bleiben
**unverändert**.

**R-33 bleibt `gemindert, nicht geschlossen`** — Kritikalität unverändert
**mittel**, kein Risiko geschlossen, **keine neue Risiko-ID**. **Dreißig
Konsistenzvorgänge in zweiundzwanzig Work Packages** waren dokumentiert (*Stand
nach dem dreißigsten Vorgang; durch den einunddreißigsten Vorgang unten auf
**31/22** aktualisiert*; löste „dreiundzwanzig" ab); die Zahl der Work Packages
bleibt **zweiundzwanzig**, weil die Vorgänge 24 bis 27 und 30 das seit dem
neunzehnten Vorgang erfasste CBP-WP-022, Vorgang 28 das seit dem achtzehnten
Vorgang erfasste CBP-WP-021 und Vorgang 29 das seit dem sechzehnten Vorgang
erfasste CBP-WP-019 betreffen und **ausschließlich** den Vorgangszähler
erhöhen. Vollständige Progression seit dem neunzehnten Vorgang: **19/22 →
20/22 → 21/22 → 22/22 → 23/22 → 24/22 → 25/22 → 26/22 → 27/22 → 28/22 → 29/22
→ 30/22**. Die **Erweiterungen der Vorgänge 21 und 23 sind zählneutral**.
**`30/22` ist kein Erfüllungsgrad und keine Prozentkennzahl** — der Zähler zählt
dokumentierte Vorgänge, der Nenner Work Packages mit mindestens einem Vorgang,
und der Zähler **darf** den Nenner überschreiten; **`30/23` und `31/22` sind
unzulässig**. **Das projektweite Konsistenzrisiko ist nicht beseitigt** —
sieben weitere Vorgänge derselben Grundklasse, gefunden erst durch einen
repositoryweiten Vollständigkeitsaudit, belegen es unmittelbar. Diese Vorgänge
sind mit den Einträgen in [RISK_REGISTER.md](RISK_REGISTER.md) **identisch** und
**zählen je nur einmal**. Die dortige Darstellung folgt der **Tabellenform** des
Risk Registers, während hier die **Prosaform** dieses Dokuments verwendet wird;
**Fakten, Zahlen, Closure-Grenze und R-33-Wirkung sind identisch**.

### Einunddreißigster Konsistenzvorgang — CBP-WP-022 Active B2 Authorization Umbrella Staleness (2026-10-15)

**Im abgeschlossenen read-only Finding-A/B Classification Review als Finding B
klassifiziert (`VALID_ACTIVE_STALENESS`, Primärklasse R-33); gemäß
A0-Festlegung des Human Maintainers für diesen Lauf (2026-10-15, keine neue
Decision-ID) als eigener Vorgang registriert in der Finding-A/B-Reconciliation.**
Der Abschlussvermerk unmittelbar unter der Phasenmodelltabelle im Abschnitt
*Phasenmodell* von **`work-packages/CBP-WP-022.md`** führte **„B2 bleibt nicht
autorisiert."**

**Fehlerklasse:** **Unterbliebene Fortschreibung einer aktiven
Autorisierungs-Sammelaussage** — eine pauschale Aussage über die Gesamtphase B2
blieb stehen, nachdem B2 in granulare Teilphasen zerlegt und mehrere davon
autorisiert, abgeschlossen und committet worden waren. Die Aussage entstand im
**B1C**-Lauf (Commit **`24de07e`**, 2026-08-04), als B2 noch als **ungeteilte**
Phase geführt wurde und tatsächlich nicht autorisiert war. Mit der Zerlegung in
granulare Teilphasen ab **B2A** (`929d10b`) wurde sie **nicht fortgeschrieben**
und widersprach seitdem der unmittelbar darüberstehenden Phasenmodelltabelle —
der Widerspruch ist dateiintern belegt.

**Aktiv, nicht historisch:** Der Vermerk steht **unmarkiert** im aktiven
Abschnitt *Phasenmodell* direkt unter der Live-Statustabelle, nicht in einem
phasendatierten Abschnitt *Stand nach …*. Die phasengebundenen Aussagen
**„B2-Kandidat — nicht autorisiert"** und **„B2 nicht autorisiert"** im Abschnitt
*Phase B1C* (einschließlich *Stand nach B1C*) sind echte Momentaufnahmen und
bleiben **unverändert**. In den bisherigen **dreißig** Vorgängen **nicht** als
eigener Vorgang registriert.

**Korrekter Zustand:** Der Autorisierungsstand ist **je Teilphase** im
Phasenmodell geführt: mehrere B2-Teilphasen — **B2A `929d10b`** bis
**B2D-E-N14-GOV `c662452`** — sind abgeschlossen und `committed`; **B2D-H**,
**B2D-E**, **B2D-V**, **B2D-G**, **B2B-Apply** sowie die Aggregatzeilen **B2C**
und **B2D** bleiben **nicht autorisiert**.

**Korrigiert:** Die Sammelaussage wurde durch einen **nicht duplizierenden
Verweis** ersetzt: **„Maßgeblich für den Autorisierungsstand der B2-Teilphasen
ist ausschließlich das Phasenmodell; die dort als `nicht autorisiert` geführten
Teilphasen und Aggregate bleiben nicht autorisiert."** Es entsteht **kein**
weiterer manuell zu pflegender Sammelspiegel; **kein Phasenstatus verändert**,
**keine neue Autorisierung**. **Eine** Aussage, **eine** Fehlerursache, **eine**
Reconciliation — **genau ein** Vorgang. **Der Nenner bleibt unverändert**, weil
CBP-WP-022 seit dem neunzehnten Vorgang bereits erfasst ist. **Zählwirkung:
`30/22 → 31/22`.**

**Abgrenzung:** **Kein AF-6-Fall** und **keine zählneutrale Erweiterung** der
Vorgänge 20 bis 30. Die Fortschreibung der Zählerspiegel auf `31/22` in weiteren
Dateien ist **kein** eigener Befund und erzeugt **keinen** weiteren Vorgang. Der
im selben Lauf behobene **Finding A** — der veraltete feste ADR-Bereich in der
Quellentabelle von `CLAUDE.md` — ist ein **R-16**-Dokumentationspflegefall,
**zählt nicht** zu R-33 und ist **nicht** Teil dieses Vorgangs; R-16 bleibt
**offen**.

**Wirkung:** **keine technische Implementierungsänderung**, **keine neue
Decision**, **keine ADR**, **keine Risikoänderung**, **keine neue Risiko-ID**,
**keine Teständerung**, **keine Traceabilityänderung**, **keine
Capabilityänderung**, **kein Phasenstatus und keine Autorisierung verändert**;
**D-067** unverändert; **KB-04 bleibt `DOCUMENTED ONLY`**; Mapping Activation
Gate und Security Foundation Readiness Gate bleiben `NOT EVALUATED`;
Capabilities **0 von 29**; **`KB04-T-N14`**, **NT-04** und **NT-05** nicht
ausgeführt; **B2D-E**, **B2D-V**, **B2D-G** und **B2B-Apply** nicht autorisiert;
**OD-37**, **Contract §10.3** und **R-20** bleiben offen; **CBP-WP-023** nicht
registriert.

**R-33 bleibt `gemindert, nicht geschlossen`** — Kritikalität unverändert
**mittel**, kein Risiko geschlossen, **keine neue Risiko-ID**.
**Einunddreißig Konsistenzvorgänge in zweiundzwanzig Work Packages** sind
dokumentiert (**neue aktuelle Basislinie**; löst „dreißig" ab); die Zahl der
Work Packages bleibt **zweiundzwanzig**, weil Vorgang **31** das seit dem
neunzehnten Vorgang erfasste CBP-WP-022 betrifft und **ausschließlich** den
Vorgangszähler erhöht. Vollständige Progression seit dem neunzehnten Vorgang:
**19/22 → 20/22 → 21/22 → 22/22 → 23/22 → 24/22 → 25/22 → 26/22 → 27/22 → 28/22
→ 29/22 → 30/22 → 31/22**. **`31/22` ist kein Erfüllungsgrad und keine
Prozentkennzahl** — der Zähler zählt dokumentierte Vorgänge, der Nenner Work
Packages mit mindestens einem Vorgang, und der Zähler **darf** den Nenner
überschreiten; **`31/23` und `32/22` sind unzulässig**. **Das projektweite
Konsistenzrisiko ist nicht beseitigt** — eine seit B2A stehengebliebene
Sammelaussage, die im R-33 Active-Status Closure Fix nicht registriert wurde,
belegt es unmittelbar. Dieser Vorgang ist mit dem Eintrag in
[RISK_REGISTER.md](RISK_REGISTER.md) **identisch** und **zählt nur einmal**. Die
dortige Darstellung folgt der **Tabellenform** des Risk Registers, während hier
die **Prosaform** dieses Dokuments verwendet wird; **Fakten, Zahlen,
Closure-Grenze und R-33-Wirkung sind identisch**.

---

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
