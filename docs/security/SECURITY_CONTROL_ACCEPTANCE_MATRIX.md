# Security Control Acceptance Matrix

| Feld | Wert |
| --- | --- |
| **Status aller Kontrollen** | **DOCUMENTED ONLY** |
| **Nicht** | IMPLEMENTED · TESTED · PASSED |
| Grundlage | **ADR-0009** (A1), [Specification](TECHNICAL_SECURITY_FOUNDATION_SPECIFICATION.md) |
| Erfasst in | CBP-WP-011 |
| Autoritätsklasse | A2 |
| Kontrollbereiche | **12** — KB-01 bis KB-12 |
| Negativtests | **32** · Positivtests **1** · gesamt **33** |
| Stand | 2026-07-21 |

> **Kein Test wurde ausgeführt.** Sämtliche Kontrollen stehen auf
> **DOCUMENTED ONLY** — das entspricht Nachweisstufe **1 `dokumentiert`**.

---

## Statuswerte

| Status | Bedeutung |
| --- | --- |
| **`DOCUMENTED ONLY`** | Spezifiziert, **nicht umgesetzt** — aktueller Stand aller zwölf |
| `IMPLEMENTED` | Umgesetzt, nicht getestet |
| `TESTED` | Positivtest bestanden |
| `PASSED` | **Negativtest bestanden** — erst hier schließt ein Risiko |

---

## KB-01 — Nicht privilegierter Betrieb

| Feld | Inhalt |
| --- | --- |
| **Ziel** | Keine Ausführung als root, kein Hostbetrieb, kein privilegierter Container |
| **Bedrohung** | Übernahme von Host oder Nachbardiensten (BA-1) |
| **Designnachweis** | Spezifikation KB-01, Identity Model V-1…V-4 |
| **Implementierungsnachweis** | Effektive Identität je Prozess; Privilegienflags |
| **Positivtest** | Dienste starten unter nicht privilegierter Identität |
| **Negativtest** | **NT-01**, **NT-02** |
| **Datenschutzbeleg** | mittelbar — Privilegien ermöglichen Umgehung aller Datenklassen |
| **Evidence-Ereignis** | `authentication`, `incident` |
| **Stop-Bedingung** | **SB-S01**, **SB-S02** |
| **Rollback** | Dienst anhalten; nicht im Betrieb umkonfigurieren |
| **Nachweisstufe** | **4** |
| **Status** | **DOCUMENTED ONLY** |

## KB-02 — Getrennte Service-Identitäten

| Feld | Inhalt |
| --- | --- |
| **Ziel** | Control Plane und Data Worker getrennt, minimale unabhängige Rechte |
| **Bedrohung** | Ein übernommener Worker erbt Freigaberechte |
| **Designnachweis** | D-034, Identity Model, Ressourcenmatrix |
| **Implementierungsnachweis** | Zuordnung Identität ↔ Rolle ↔ Ressource |
| **Positivtest** | Jede Identität erreicht ihre zugewiesenen Ressourcen |
| **Negativtest** | **NT-07**, **NT-08** |
| **Datenschutzbeleg** | Control Plane erhält keine Secret-Werte |
| **Evidence-Ereignis** | `authorization` |
| **Stop-Bedingung** | **SB-S09** |
| **Rollback** | Identität deaktivieren |
| **Nachweisstufe** | **4** |
| **Status** | **DOCUMENTED ONLY** |

## KB-03 — Mount- und Speichergrenzen

| Feld | Inhalt |
| --- | --- |
| **Ziel** | Geringstmöglicher Modus je Bereich; keine unkontrollierten Host-Mounts |
| **Bedrohung** | Überschreiben kanonischen Wissens; Ausbruch aus dem Bereich |
| **Designnachweis** | Mount-Matrix M-1…M-4 |
| **Implementierungsnachweis** | Mountliste mit Modus je Identität |
| **Positivtest** | RT-1 beschreibbar, Canonical lesbar |
| **Negativtest** | **NT-03**, **NT-04** |
| **Datenschutzbeleg** | RT-2 von keiner Identität direkt eingebunden |
| **Evidence-Ereignis** | `incident` |
| **Stop-Bedingung** | **SB-S03**, **SB-S04** |
| **Rollback** | Mounts entfernen |
| **Nachweisstufe** | **4** |
| **Status** | **DOCUMENTED ONLY** |

## KB-04 — Dateisystemrechte

| Feld | Inhalt |
| --- | --- |
| **Ziel** | Deny-by-default auf Dateiebene; keine world-writable Dateien |
| **Bedrohung** | Direktzugriff unter Umgehung der Anwendung |
| **Designnachweis** | Spezifikation KB-04 |
| **Implementierungsnachweis** | Rechteauflistung vor und nach dem Start |
| **Positivtest** | Atomare Writes in RT-1 funktionieren |
| **Negativtest** | **NT-04**, **NT-05** |
| **Datenschutzbeleg** | Kein Lesezugriff über Bereichsgrenzen |
| **Evidence-Ereignis** | `incident` |
| **Stop-Bedingung** | **SB-S04** |
| **Rollback** | Rechte auf dokumentierten Ausgangszustand |
| **Nachweisstufe** | **4** |
| **Status** | **DOCUMENTED ONLY** |

## KB-05 — API-Authentisierung und Autorisierung

| Feld | Inhalt |
| --- | --- |
| **Ziel** | Serverseitige Autorisierung, deny-by-default |
| **Bedrohung** | Ein Client verlangt mehr als seine Rolle erlaubt |
| **Designnachweis** | Matrix 9 Rollen × 12 Ressourcen, DD-6 |
| **Implementierungsnachweis** | Prüfprotokoll je Rolle × Endpunkt |
| **Positivtest** | Berechtigte Rolle erreicht ihren Endpunkt |
| **Negativtest** | **NT-06**, **NT-07** |
| **Datenschutzbeleg** | Fehlerantworten enthalten keine Secrets |
| **Evidence-Ereignis** | `authentication`, `authorization` |
| **Stop-Bedingung** | **SB-S09** |
| **Rollback** | Endpunkt deaktivieren, **nicht** die Prüfung |
| **Nachweisstufe** | **4** |
| **Status** | **DOCUMENTED ONLY** |

## KB-06 — Approval-Zustände

| Feld | Inhalt |
| --- | --- |
| **Ziel** | Wirkung erst nach dokumentierter Freigabe; Aktivierung getrennt |
| **Bedrohung** | Unbeabsichtigte oder automatische Änderungen |
| **Designnachweis** | Validitätsstufen ADR-0008, KB-06 |
| **Implementierungsnachweis** | Zustandsverlauf mit Actor, Zeitpunkt, Grund, Revision |
| **Positivtest** | Freigegebene Aktion wirkt |
| **Negativtest** | **NT-08** |
| **Datenschutzbeleg** | Widerruf blockiert Folgeverarbeitung |
| **Evidence-Ereignis** | `approval`, `activation`, `suspension`, `revocation` |
| **Stop-Bedingung** | **SB-S09** |
| **Rollback** | Freigabezustände zurücksetzen |
| **Nachweisstufe** | **4** |
| **Status** | **DOCUMENTED ONLY** |

## KB-07 — Git- und GitHub-Rechte

| Feld | Inhalt |
| --- | --- |
| **Ziel** | Read-only als Standard; kein pauschaler Schreibzugriff |
| **Bedrohung** | Unkontrollierter Push; Veröffentlichung privaten Bestands |
| **Designnachweis** | KB-07, PERMISSION_MODEL |
| **Implementierungsnachweis** | Rechteauflistung der Zugänge; kein breit berechtigtes Token |
| **Positivtest** | Draft-Write im erlaubten Arbeitsbereich funktioniert |
| **Negativtest** | **NT-09** |
| **Datenschutzbeleg** | Publish nur nach separater Human-Freigabe |
| **Evidence-Ereignis** | `authorization`, `incident` |
| **Stop-Bedingung** | **SB-S10** |
| **Rollback** | Zugang entziehen; Token widerrufen |
| **Nachweisstufe** | **4** |
| **Status** | **DOCUMENTED ONLY** |

## KB-08 — Secret-Grenze

| Feld | Inhalt |
| --- | --- |
| **Ziel** | Werte verlassen den Store nur zur berechtigten Identität |
| **Bedrohung** | Secret in Git, Log, Report oder Modellkontext (BA-5) |
| **Designnachweis** | D-035, Secret Contract SR-1…SR-12 |
| **Implementierungsnachweis** | Resolver umgesetzt; Scan ohne Fund |
| **Positivtest** | Berechtigte Identität erhält den Wert read-only |
| **Negativtest** | **NT-10**, **NT-11**, **NT-12**, **NT-13** |
| **Datenschutzbeleg** | Kein Wert in Repository, Konfiguration, Logs, RT-2, Context Packs |
| **Evidence-Ereignis** | `secret-resolution-failure`, `incident` |
| **Stop-Bedingung** | **SB-S05**, **SB-S06** |
| **Rollback** | Zugriff sperren; **Rotation vor History Cleanup** |
| **Nachweisstufe** | **4** |
| **Status** | **DOCUMENTED ONLY** |

## KB-09 — Audit und Operational Evidence

| Feld | Inhalt |
| --- | --- |
| **Ziel** | Jede sicherheitsrelevante Entscheidung ist nachweisbar |
| **Bedrohung** | Vorfall bleibt unentdeckt oder wird verwischt (BA-7) |
| **Designnachweis** | D-037, Evidence Policy, 18 Felder, 17 Ereignisarten |
| **Implementierungsnachweis** | Ereignisse mit vollständiger Kette |
| **Positivtest** | Abgelehnter Zugriff erscheint im Protokoll |
| **Negativtest** | **NT-18**, **NT-19**, **NT-20**, **NT-28**, **NT-29**, **NT-30**, **NT-31** |
| **Datenschutzbeleg** | Kein Secret, kein vollständiger Quellinhalt im Ereignis |
| **Evidence-Ereignis** | alle 17 |
| **Stop-Bedingung** | **SB-S11**, **SB-S12** |
| **Rollback** | Protokollierung **nicht** abschalten; Dienst anhalten |
| **Nachweisstufe** | **4** |
| **Status** | **DOCUMENTED ONLY** |

## KB-10 — Netzwerk-Egress

| Feld | Inhalt |
| --- | --- |
| **Ziel** | Deny-by-default mit expliziter, vierfach gebundener Allowlist |
| **Bedrohung** | Datenabfluss an ein nicht vorgesehenes Ziel |
| **Designnachweis** | D-036, Egress Policy EG-1…EG-9, fünf Gates |
| **Implementierungsnachweis** | Wirksame Allowlist; Portauflistung von außen |
| **Positivtest** | **PT-01** — lokale Suche ohne externen Egress |
| **Negativtest** | **NT-14**, **NT-15**, **NT-23**, **NT-24**, **NT-26**, **NT-27** |
| **Datenschutzbeleg** | Datenklassen- und AI-Transfer-Gate vor jeder Übertragung |
| **Evidence-Ereignis** | `egress-decision` |
| **Stop-Bedingung** | **SB-S07** |
| **Rollback** | Egress vollständig sperren |
| **Nachweisstufe** | **4** |
| **Status** | **DOCUMENTED ONLY** |

## KB-11 — `excluded-from-ai`-Ausgabesperre

| Feld | Inhalt |
| --- | --- |
| **Ziel** | Kein gesperrter Inhalt überschreitet eine externe Modellgrenze |
| **Bedrohung** | Leakage über Retrieval, Context Pack, Sammelanfrage |
| **Designnachweis** | KB-11, zweifache Prüfung |
| **Implementierungsnachweis** | Filter vor Context Pack **und** vor Übertragung |
| **Positivtest** | Zulässiger Inhalt passiert |
| **Negativtest** | **NT-16**, **NT-17** |
| **Datenschutzbeleg** | **Zielwert null externe Leaks**, synthetische Fixtures (D-021) |
| **Evidence-Ereignis** | `excluded-from-ai-block` |
| **Stop-Bedingung** | **SB-S08** |
| **Rollback** | Retrieval anhalten; Context Packs verwerfen |
| **Nachweisstufe** | **4** |
| **Status** | **DOCUMENTED ONLY** |

## KB-12 — Backup-Storage-Isolation

| Feld | Inhalt |
| --- | --- |
| **Ziel** | Die Sicherung überlebt eine Kompromittierung der Anwendung |
| **Bedrohung** | Übernommene Komponente überschreibt Sicherungen |
| **Designnachweis** | KB-12, Backupwirkung B-1…B-4 |
| **Implementierungsnachweis** | Rechteauflistung; getrennte Klassifikation |
| **Positivtest** | Backup Service sichert erfolgreich |
| **Negativtest** | **NT-21**, **NT-22** |
| **Datenschutzbeleg** | Secret Store nie mit veröffentlichbarem Core-Inhalt gesichert |
| **Evidence-Ereignis** | `backup`, `restore` |
| **Stop-Bedingung** | **SB-S13**, **SB-S14** |
| **Rollback** | Schreibrechte entziehen; getrenntes Ziel |
| **Nachweisstufe** | **5** — durchgeführter Restore |
| **Status** | **DOCUMENTED ONLY** |

---

## Negativtests — 31

Ein Negativtest gilt nur als bestanden, wenn der verbotene Fall **tatsächlich
scheitert**. Eine Warnung genügt nicht.

| # | Test | Erwartung | KB |
| --- | --- | --- | --- |
| **NT-01** | Start als root | **verweigert** | KB-01 |
| **NT-02** | Privilegierter Container | **verweigert** | KB-01 |
| **NT-03** | Host-Mount außerhalb Allowlist | **verweigert** | KB-03 |
| **NT-04** | Schreibversuch auf Canonical | **scheitert** | KB-03, KB-04 |
| **NT-05** | Symlink Escape aus dem Bereich | **blockiert** | KB-04 |
| **NT-06** | API-Aufruf ohne Identität | **abgelehnt** | KB-05 |
| **NT-07** | Rollen-Selbstzuweisung durch den Client | **abgelehnt** | KB-02, KB-05 |
| **NT-08** | Approval-Bypass | **blockiert** | KB-02, KB-06 |
| **NT-09** | Automatischer Git-Push | **scheitert** | KB-07 |
| **NT-10** | Secret-Wert in Konfiguration | **Blocker** | KB-08 |
| **NT-11** | Secret-Wert in Log | **Blocker** | KB-08 |
| **NT-12** | Unbekannte Secret-Reference-Version | **blockiert**, kein Fallback | KB-08 |
| **NT-13** | Unbekannter Secret Provider | **blockiert** | KB-08 |
| **NT-14** | Egress zu nicht erlaubtem Ziel | **blockiert** | KB-10 |
| **NT-15** | Redirect zu nicht erlaubtem Ziel | **blockiert** | KB-10 |
| **NT-16** | Externe Übertragung von `excluded-from-ai` | **blockiert** | KB-11 |
| **NT-17** | Gemischtes Context Pack mit gesperrtem Inhalt | **blockiert** | KB-11 |
| **NT-18** | Audit-Event ohne Actor | **abgelehnt** | KB-09 |
| **NT-19** | Audit-Kettenbruch | **sichtbar**, nicht repariert | KB-09 |
| **NT-20** | Nachträgliche Event-Manipulation | **erkannt, abgelehnt** | KB-09 |
| **NT-21** | Backup durch Anwendungsprozess überschrieben | **scheitert** | KB-12 |
| **NT-22** | Restore ohne Integritätsnachweis | **abgelehnt** | KB-12 |
| **NT-23** | RT-1 als einzige Registry-Wahrheit | **abgelehnt** — Registry ist kanonisch | KB-03 |
| **NT-24** | RT-3 als dauerhafte Statuswahrheit nach Neustart | **abgelehnt** | KB-03 |
| **NT-26** | Egress-Erlaubnis der Control Plane vom Data Worker genutzt | **blockiert** | KB-02, KB-10 |
| **NT-27** | Externe Übertragung bei `data_class: unknown` | **blockiert** | KB-10, KB-11 |
| **NT-28** | Secret-Wert in einem Ereignisfeld | **abgelehnt** | KB-08, KB-09 |
| **NT-29** | Actor aus freiem Clienttext | **abgelehnt** | KB-09 |
| **NT-30** | Aufbewahrungsablauf bei aktiver Incident-Sperre | **Löschung unterbleibt** | KB-09 |
| **NT-31** | Schreibende Komponente löscht eigenen Auditeintrag | **scheitert** | KB-09 |
| **NT-32** | DNS löst auf ein nicht erlaubtes Ziel auf | **blockiert** | KB-10 |
| **NT-33** | Ziel im privaten Netz ohne Freigabe | **blockiert** | KB-10 |

### Positivtests

| # | Test | Erwartung | KB |
| --- | --- | --- | --- |
| **PT-01** | Lokale Suche bei vollständig gesperrtem Egress | **funktioniert** | KB-10 |

### Testtaxonomie

**Ein Test besitzt genau einen primären Testtyp.**

| Typ | Präfix | Prüft |
| --- | --- | --- |
| **Negativtest** | `NT-*` | Blockierung, Verweigerung, Erkennung oder sichere Abschaltung bei einer **unzulässigen** Situation |
| **Positivtest** | `PT-*` | Die **zulässige** Funktion bei erfüllten Voraussetzungen |

| # | Regel |
| --- | --- |
| **TT-1** | Eine **NT-ID bezeichnet ausschließlich einen Negativtest** |
| **TT-2** | Eine **PT-ID bezeichnet ausschließlich einen Positivtest** |
| **TT-3** | Ein **Positivtest wird nie zur Negativtestzahl gerechnet** |
| **TT-4** | Gesamtzahl = Negativtests **+** Positivtests |
| **TT-5** | Eine ID wird nach Umbenennung **nicht neu vergeben** — die Lücke bleibt |

### Testsummen — ausgezählt

| Kennzahl | Wert |
| --- | ---: |
| **Negativtests** (`NT-*`) | **32** |
| **Positivtests** (`PT-*`) | **1** |
| **Gesamtzahl der Testfälle** | **33** |

**NT-IDs:** NT-01 bis NT-24 (24) · NT-26 bis NT-33 (8) — **32 IDs**.
**PT-IDs:** PT-01 — **1 ID**.

> **NT-25 existiert nicht mehr.** Der Testfall war inhaltlich ein Positivtest
> und trägt seit dem Nova-REWORK-Lauf die ID **PT-01**. Nach Regel TT-5 bleibt
> die Nummer 25 in der NT-Reihe **frei** und wird nicht nachbesetzt.
>
> **NT-32 und NT-33 sind neu.** Die Egress-Policy führte zwei Tests unter den
> bereits vergebenen IDs NT-23 und NT-24, die in dieser Matrix RT-1- und
> RT-3-Tests des Bereichs KB-03 bezeichnen. Die Doppelvergabe ist mit den
> neuen IDs aufgelöst.

**Die geforderte Mindestzahl von 24 echten Negativtests ist erfüllt** — alle
32 NT-IDs bezeichnen Negativtests.

### Verteilung nach Kontrollbereich

| KB | Tests | Anzahl |
| --- | --- | ---: |
| KB-01 | NT-01, NT-02 | 2 |
| KB-02 | NT-07, NT-08, NT-26 | 3 |
| KB-03 | NT-03, NT-04, NT-23, NT-24 | 4 |
| KB-04 | NT-04, NT-05 | 2 |
| KB-05 | NT-06, NT-07 | 2 |
| KB-06 | NT-08 | 1 |
| KB-07 | NT-09 | 1 |
| KB-08 | NT-10, NT-11, NT-12, NT-13, NT-28 | 5 |
| KB-09 | NT-18, NT-19, NT-20, NT-28, NT-29, NT-30, NT-31 | 7 |
| KB-10 | NT-14, NT-15, NT-26, NT-27, NT-32, NT-33, **PT-01** | 7 |
| KB-11 | NT-16, NT-17, NT-27 | 3 |
| KB-12 | NT-21, NT-22 | 2 |

*Mehrfachnennungen entstehen, wo ein Test zwei Bereiche prüft. **Jeder Test
zählt in der Gesamtzahl nur einmal.***

| # | Regel |
| --- | --- |
| **NTR-1** | Bestanden nur, wenn der verbotene Fall **tatsächlich scheitert** |
| **NTR-2** | Eine Warnung genügt **nicht** |
| **NTR-3** | **Synthetische Daten**; **kein reales Secret wird erzeugt** |
| **NTR-4** | **Kein Test wurde ausgeführt** — Status aller **33**: **PLANNED / NOT EXECUTED** |

---

## Stop-Bedingungen im Detail

| ID | Erkennung | Sofortmaßnahme | Evidenz | Incident | Sichere Abschaltung | Wiederaufnahme | Autorität |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **SB-S01** | Prozess läuft als root | Dienst anhalten | Prozessliste | Prüfen, welche Ressourcen berührt wurden | Dienst gestoppt | KB-01 negativ getestet | **A0** |
| **SB-S02** | Privilegierter Container | Container anhalten | Runtime-Konfiguration | wie SB-S01 | Container gestoppt | KB-01 negativ getestet | **A0** |
| **SB-S03** | Zugriff auf den Hypervisor-Host | Sofort trennen | Auditspur | Hostintegrität prüfen | Netz und Dienst getrennt | Hostgrenze belegt | **A0** |
| **SB-S04** | Schreibzugriff auf Canonical | Schreibpfad sperren | Rechteauflistung, Auditeintrag | Bestand gegen Git und Backup abgleichen | Read-only erzwungen | KB-04 negativ getestet | **A0** |
| **SB-S05** | Secret in Git, Log, RT-2 oder Context Pack | **Jeden Ingest blockieren**; Wert **nicht** in den Bericht kopieren | Fundort ohne Wert | [SECRET_INCIDENT_RESPONSE](SECRET_INCIDENT_RESPONSE.md) — **Rotation vor Cleanup** | Verarbeitung gestoppt | Rotation **und** Bereinigung **und** Rebuild | **A0** |
| **SB-S06** | Unbekannte Secret Reference | Verarbeitung blockieren | `secret-resolution-failure` | Referenzherkunft prüfen | Resolver verweigert | Referenz gültig oder entfernt | A2 |
| **SB-S07** | Egress zu nicht erlaubtem Ziel | **Egress vollständig sperren** | `egress-decision` mit Grund | Ausbreitung prüfen — was wurde übertragen | Kein Netz | KB-10 negativ getestet | **A0** |
| **SB-S08** | `excluded-from-ai` überschreitet Modellgrenze | Retrieval stoppen; Context Packs verwerfen | `excluded-from-ai-block`, Auditspur | **Prüfen, ob externer Modellkontext erreicht wurde** | Retrieval gestoppt | KB-11 negativ getestet, **null Leaks** | **A0** |
| **SB-S09** | Approval-Bypass | Freigabepfad sperren | Zustandsverlauf | Betroffene Aktivierungen zurücknehmen | Aktivierung gesperrt | KB-06 negativ getestet | **A0** |
| **SB-S10** | Unkontrollierter Git-Push | Keine weitere Git-Operation; Zugang sperren | Remote-Stand | **Prüfen, ob privater Bestand veröffentlicht wurde** — falls ja zusätzlich SB-S05 | Zugang entzogen | Rechte korrigiert, KB-07 negativ getestet, Human bestätigt Remote | **A0** |
| **SB-S11** | RT-2-Manipulation oder Kettenbruch | Schreibpfad sperren | Kettenprüfung | Umfang bestimmen; **Bruch nicht reparieren** | Evidence Writer gestoppt | Integrität belegt | **A0** |
| **SB-S12** | Ereignis ohne Actor | Ereignis ablehnen | Ablehnungseintrag | Herkunft prüfen | Schnittstelle verweigert | KB-09 negativ getestet | A2 |
| **SB-S13** | Backupverlust oder Überschreibung | **Keine weitere Sicherung auf dasselbe Ziel** | Backupstände | Ältesten lesbaren Stand bestimmen | Sicherung eingefroren | Isolation negativ getestet **und** Restore durchgeführt | **A0** |
| **SB-S14** | Restore ohne Integritätsnachweis | Restore abbrechen | Prüfergebnis | Quelle des Backups prüfen | Restore gestoppt | Integritätsnachweis erbracht | A2 |
| **SB-S15** | Kontrolle ruht allein auf Promptregeln | Als **nicht durchgesetzt** kennzeichnen | Zuordnungstabelle | Tragende Stufe nachrüsten | — | Tragende Ebene umgesetzt und negativ getestet | A2 |
| **SB-S16** | Änderung außerhalb des Work-Package-Scopes | **Nicht raten**, nicht fortsetzen | Änderungsliste | Blocker melden | Arbeit angehalten | Ausdrückliche Autorisierung | **A0** |

**Zehn der sechzehn erfordern A0.**

## Zusammenfassung

| Kennzahl | Wert |
| --- | ---: |
| Kontrollbereiche | **12** |
| **Negativtests** (`NT-*`) | **32** |
| **Positivtests** (`PT-*`) | **1** |
| **Testfälle gesamt** | **33** |
| Bereiche mit Nachweisstufe 4 | **11** |
| Bereiche mit Nachweisstufe 5 | **1** — KB-12 |
| Stop-Bedingungen | **16** |
| **Kontrollen mit Status `IMPLEMENTED`** | **0** |
| **Ausgeführte Tests** | **0** |

## Status

**Alle zwölf Kontrollen: DOCUMENTED ONLY.** Keine ist umgesetzt, keine
getestet, keine bestanden.

**R-25, R-26, R-27, R-30, R-31, R-32 und R-20 bleiben offen.** Sie schließen
bei Nachweisstufe 4 beziehungsweise 5 — nicht durch dieses Dokument.

**Implementierung erlaubt: nein.**
