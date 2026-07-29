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

**R-33 bleibt `gemindert, nicht geschlossen`** — Kritikalität unverändert
**mittel**, kein Risiko geschlossen. **Sechzehn Konsistenzvorgänge in neunzehn Work
Packages** sind dokumentiert (**neue aktuelle Basislinie**; löst „fünfzehn" ab);
die Zahl der Work Packages steigt auf **neunzehn**, weil dieser Vorgang
**erstmals CBP-WP-019** betrifft, das durch `3c437f2` Teil der committeten Menge
wurde (**15/18 → 16/19**). Dieser Vorgang ist mit dem Eintrag in
[RISK_REGISTER.md](RISK_REGISTER.md) **identisch** und zählt **nur einmal**.

**Die Implementierung von CBP-WP-013 selbst führte keinen arithmetischen
Zählfehler ein.** Testzahl (**137**) aus `Ran N tests`, Git-Inventar aus
`git status --porcelain=v1 -uall`, Entscheidungs- und ADR-Zahlen aus den
Quelltabellen ausgezählt. Die **zwei** in CBP-WP-013 gefundenen Testdefekte
betrafen Testcode (Docstring-Prosa-Grep; Zeilenenden-Normalisierung), keine
Kennzahl. **Der achte Konsistenzvorgang entstand erst im ersten
Nova-Korrekturlauf** — in den beiden oben genannten Dokumenten — und ist als
solcher in der Tabelle geführt. **R-33 bleibt offen.**

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
