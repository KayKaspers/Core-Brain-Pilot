# CBP-WP-011 — Technical Security Foundation Specification

| Feld | Wert |
| --- | --- |
| ID | CBP-WP-011 |
| Titel | Technical Security Foundation Specification |
| Typ | `docs-only`, **interactive** |
| Prompt Mode | **Full** (NDF v1.0.0) |
| Context Budget | **B2 – Standard** (Core Brain Pilot) |
| Claude Code Model | **Claude Opus 4.8** (`claude-opus-4-8`) |
| Claude Code Effort | **ultracode** — im Ausführungsprofil deklariert |
| Phase | Phase 1 – Planung |
| Ausgeführt am | 2026-07-21 |
| Ablauf | **interaktiv**, zwei Phasen · **plus Nova-REWORK-Korrekturlauf** |
| Status | `in-review` |
| Autoritätsklasse | A2 |

> **Dieses Work Package enthält einen Nova-REWORK-Korrekturlauf.** Die
> Erstausführung wurde als COMPLETE berichtet; zwei Kennzahlen waren
> widersprüchlich, ein dritter Widerspruch kam bei der Auszählung hinzu. Siehe
> [Nova REWORK correction run](#nova-rework-correction-run) am Ende. Die
> Erstausführung unten ist **nicht** umgeschrieben.

> **Anmerkung zum Ausführungsprofil.** Die Effort-Stufe `ultracode` steht im
> Work Package. Es wurde **keine Multi-Agent-Orchestrierung gestartet**; die
> zwölf Kontrollbereiche wurden in einem Durchgang bearbeitet und anschließend
> als ein zusammenhängendes Modell verifiziert.

---

## Ziel

Eine **entscheidungsbasierte technische Sicherheitsspezifikation** für die
spätere Foundation Runtime erstellen: vier Architekturentscheidungen erheben
und die zwölf Kontrollbereiche **KB-01 bis KB-12** in technisch abnehmbare
Anforderungen, Negativtests, Nachweise, Stop-Bedingungen und sichere
Rücksetzwege überführen.

**Keine Kontrolle wird als implementiert, getestet oder betriebsbereit
dargestellt.**

## Interaktiver Ablauf

| Phase | Inhalt | Ergebnis |
| --- | --- | --- |
| **A** | Repository read-only prüfen, **einen** Entscheidungsfragebogen ausgeben, keine Datei verändern | 30 Vorprüfungspunkte bestanden, **0 Dateiänderungen** |
| **B** | Vier Entscheidungen aufzeichnen, ADR-0009, Spezifikation und sechs Fachdokumente erstellen, Register nachführen | 9 neue Dokumente, 4 A0-Entscheidungen, 2 geschlossene OD |

## Human-Entscheidungen

Alle vier am **2026-07-21**, Autorität **A0**. Wortlaut unverändert übernommen,
nichts ergänzt oder erweitert. Vollständig in
[ADR-0009](../docs/decisions/ADR-0009-technische-sicherheitsgrundlage.md).

| Teil | Entscheidung | Kern | Grundsatz |
| --- | --- | --- | --- |
| **A** | **SELECT A2** — getrennte logische Identitäten | Control Plane und Data Worker; **Worker ohne Approval-, Administrations- und Publish-Rechte** | **S-A** Verarbeitung erteilt keine Freigabe |
| **B** | **SELECT B1** — versionierter Referenzvertrag plus OS-geschützter Datei-Provider | Werte **nie** in Git, Konfiguration, **Umgebungsvariablen**, **Kommandozeilen**, Logs, RT-2, Context Packs, Fehlermeldungen, Reports | **S-B** Eine Referenz ist kein Secret |
| **C** | **SELECT C1** — Egress deny-by-default | Bindung an **Ziel, Provider, Zweck und Identität**; lokale Suche **ohne** externen Egress | **S-C** Eine Netzwerkerlaubnis ist keine Datenfreigabe |
| **D** | **SELECT D1** — RT-2 append-only und verkettet | Korrekturen als **Folgeereignis**; Ketten- und Integritätsbrüche **sichtbar** | **S-D** Ein überschreibbarer Nachweis ist kein Nachweis |

Aufgezeichnet als **D-034, D-035, D-036, D-037**.

## Scope

- Vier Human-Entscheidungen erheben und im Wortlaut aufzeichnen
- ADR-0009 erstellen
- Technische Sicherheitsspezifikation, 18 Abschnitte
- Identitäts- und Privilegienmodell, Secret-Vertrag, Egress-Policy,
  Operational-Evidence-Policy
- Abnahmematrix mit Negativtests
- Readiness Gate definieren, **nicht ausführen**
- R-33-Chronologie ergänzen
- Status- und Registerpflege

## Out of Scope

- Human-Entscheidung erfinden oder erweitern
- Dateiänderung vor der Human-Antwort
- **Runtime implementieren**, OS-Benutzer anlegen, UID/GID oder Hostpfade festlegen
- Secret Store anlegen, Secret-Werte speichern
- Netzwerkregeln ändern, Ports öffnen, Firewall anfassen
- API, Authentisierung, Autorisierung implementieren
- Auditdatenbank anlegen; Logging-, Backup- oder Speichertechnologie wählen
- DRC, Mapping Activation Gate oder Readiness Gate ausführen
- **CBP-WP-012 ausführen oder autorisieren**
- Commit, Push, Branch, Remote-Änderung, Issue, Release

## Inputs

NDF v1.0.0 · Repository-Stand auf `main` (Commit `43bb4e3`) ·
`PERMISSION_MODEL.md` · `SECRET_INCIDENT_RESPONSE.md` ·
`DATA_CLASSIFICATION.md` · `TECHNICAL_SECURITY_FOUNDATION_PLAN.md` ·
`PHASE_1_FOUNDATION_PLAN.md` · `PHASE_1_WORK_PACKAGE_MAP.md` ·
`PHASE_1_EVIDENCE_PLAN.md` · `PHASE_1_STOP_CONDITIONS.md` ·
`REPOSITORY_AND_WORKSPACE_PLAN.md` · `PILOT_SOURCE_CONTRACT.md` ·
`SOURCE_SLOT_MODEL.md` · `PILOT_SOURCE_MAPPING_SPECIFICATION.md` ·
`PILOT_SOURCE_MAPPING_SCHEMA.md` · `PILOT_SOURCE_MAPPING_VALIDATION.md` ·
`PILOT_MAPPING_ACTIVATION_GATE.md` · `DEPLOYMENT_READINESS_CHECK.md` ·
`ADR-0006` · `ADR-0007` · `ADR-0008` · `SYSTEM_ARCHITECTURE.md` ·
`COMPONENT_MODEL.md` · `DEPLOYMENT_PROFILES.md` · `PROJECT_MANIFEST.md` ·
`PROJECT_PROFILE.md` · `DECISION_REGISTER.md` · `RISK_REGISTER.md` ·
`CAPABILITY_MATRIX.md` · `WORK_PACKAGE_QUEUE.md` · `COMPLIANCE_CHECK.md` ·
`HEALTH_SCORE.md` · `PROJECT_BRAIN.md` · `CBP-WP-010.md` · `README.md` ·
`CLAUDE.md` · **Antworten des Human Maintainers**

## Zwölf Kontrollbereiche

| ID | Bereich | Tragende Stufe | Nachweisstufe | Status |
| --- | --- | --- | --- | --- |
| **KB-01** | Nicht privilegierter Betrieb | 2 | 4 | DOCUMENTED ONLY |
| **KB-02** | Getrennte Service-Identitäten | 2 | 4 | DOCUMENTED ONLY |
| **KB-03** | Mount- und Speichergrenzen | 3 | 4 | DOCUMENTED ONLY |
| **KB-04** | Dateisystemrechte | 1 | 4 | DOCUMENTED ONLY |
| **KB-05** | API-Authentisierung und Autorisierung | 5 | 4 | DOCUMENTED ONLY |
| **KB-06** | Approval-Zustände | 7 | 4 | DOCUMENTED ONLY |
| **KB-07** | Git- und GitHub-Rechte | 2, 5, 7 | 4 | DOCUMENTED ONLY |
| **KB-08** | Secret-Grenze | 1, 2, 4 | 4 | DOCUMENTED ONLY |
| **KB-09** | Audit und Operational Evidence | 1, 3, 8 | 4 | DOCUMENTED ONLY |
| **KB-10** | Netzwerk-Egress | 6 | 4 | DOCUMENTED ONLY |
| **KB-11** | `excluded-from-ai`-Ausgabesperre | 1, 3, 5, 6 | 4 | DOCUMENTED ONLY |
| **KB-12** | Backup-Storage-Isolation | 1, 5 | **5** | DOCUMENTED ONLY |

### Durchsetzungsreihenfolge

```text
1 OS-Dateirechte
  2 Prozess-/Containeridentität
    3 Mount-Modi und Speichergrenzen
      4 Secret-Bereitstellung
        5 API-Authentisierung und Autorisierung
          6 Netzwerkgrenzen
            7 Approval-Zustände
              8 Audit und Operational Evidence
                9 Promptregeln — NUR ergänzend
```

**Eine spätere Stufe darf eine frühere technische Kontrolle nicht ersetzen.**
**Kein Bereich ruht allein auf Stufe 9** — sonst greift SB-S15.

## Secret-Vertrag

**Format:** `cbp-secret:v1:<provider>:<opaque-id>`

| Regel | Inhalt |
| --- | --- |
| **SR-2** | **Unbekannte Version blockiert** — kein Fallback |
| **SR-3** | **Unbekannter Provider blockiert** |
| **SR-8** | **Keine Übergabe über Umgebungsvariablen** |
| **SR-9** | **Keine Übergabe über Kommandozeilen** |
| **SR-11** | **Rotation ändert nicht zwingend die Referenz** |

**Pilotprovider:** OS-geschützter Dateibereich **außerhalb** von
Core-Repository, Operator-Workspace **und** Runtime — der **vierte Bereich**.
**Schließt OD-34.**

## Egress-Grundsatz

**Deny-by-default**, vierfach gebunden an **Ziel, Provider, Zweck und
Service-Identität**. Fünf Gates vor jeder externen Übertragung: Zielgate,
Datenklassengate, AI-Transfer-Gate, Approval-Gate, Zweckgate.

**DNS und Redirect heben die Zielbindung nicht auf.** **Lokale Suche
funktioniert ohne externen Egress.** `excluded-from-ai` bleibt unabhängig vom
Ziel blockiert.

## Operational-Evidence-Modell

**RT-2**, logisch append-only, verkettet. **18 Ereignisfelder**, **17
Ereignisarten**.

| Regel | Inhalt |
| --- | --- |
| **AO-2** | Korrekturen als **Folgeereignis**, nie stilles Überschreiben |
| **F-3** | **Actor nie aus freiem Clienttext** |
| **F-4/F-5** | **Kein Secret, kein vollständiger Quellinhalt** im Ereignis |
| **INT-2** | **Kettenbruch wird sichtbar** — nicht repariert |
| **RET-3** | **Fristablauf übergeht keine aktive Incident-, Legal- oder Restore-Sperre** |

**Schließt OD-35** — die konkrete Aufbewahrungsdauer bleibt **Deployment
Required**.

## Negativtests

**33 Testfälle** — **32 Negativtests** (`NT-*`) und **1 Positivtest** (`PT-01`,
lokale Suche bei gesperrtem Egress). Die geforderte Mindestzahl von 24 echten
Negativtests ist erfüllt.

**Kein Test wurde ausgeführt.** Alle 33 stehen auf `PLANNED / NOT EXECUTED`.
Ein Negativtest gilt nur als bestanden, wenn der verbotene Fall **tatsächlich
scheitert** — eine Warnung genügt nicht. **Ein Positivtest wird nie zur
Negativtestzahl gerechnet.**

## Readiness Gate

**24 Punkte**, Status **`NOT EVALUATED`**. Verteilung der Nachweisstufen:
1 × Stufe 1 · 8 × Stufe 2 · 4 × Stufe 3 · **9 × Stufe 4** · 1 × Stufe 5 ·
1 × Stufe 6 = **24**.

**Nur der Human Maintainer darf `ACCEPTED BY HUMAN MAINTAINER` feststellen.**
Das Gate wurde **nicht ausgeführt** und ist ohne CBP-WP-012 nicht durchlaufbar.

## Stop-Bedingungen

**16 Bedingungen** SB-S01 bis SB-S16, je mit Erkennung, Sofortmaßnahme,
Evidenz, Incident-Prozess, sicherer Abschaltung, Wiederaufnahmebedingung und
Autorität. **Zehn erfordern A0.**

## Prüfungen

48 Prüfungen. Schwerpunkte: vier Entscheidungen direkt vom Human Maintainer ·
nichts ergänzt · ADR-0009-Status entspricht den Entscheidungen · ausschließlich
Markdown · **keine Implementierung, keine Identität, keine UID/GID, keine
Hostpfade, keine Secret-Werte** · Secret-Referenzen synthetisch · **kein Secret
über Environment oder CLI** · alle zwölf Bereiche vollständig ·
Durchsetzungsreihenfolge vollständig · **Promptregeln nur ergänzend** ·
Canonical read-only · Control Plane und Data Worker getrennt · Worker ohne
Approval- oder Publish-Rechte · Secret-Vertrag versioniert · unbekannte Version
und unbekannter Provider blockieren · Egress deny-by-default · **Netzwerk-
erlaubnis ist keine Datenfreigabe** · `excluded-from-ai` extern blockiert ·
RT-2 getrennt und **kein Cache** · **mindestens 24 Negativtests geplant, keiner
ausgeführt** · alle vier Gates bleiben `NOT EVALUATED` · keine Capability
`implemented` · **kein Risiko allein durch Dokumentation geschlossen** ·
**R-33 nicht geschlossen** · OD-34 und OD-35 nur regelkonform behandelt ·
**CBP-WP-012 bleibt proposed und nicht autorisiert** · Summen ausgezählt ·
genau ein Folge-Work-Package · kein Commit, kein Push.

## Akzeptanzkriterien

Vier eindeutige Human-Entscheidungen dokumentiert · ADR-0009 korrekt behandelt ·
alle zwölf Kontrollbereiche vollständig spezifiziert · Identity-, Secret-,
Egress- und RT-2-Modelle entscheidungsreif · **mindestens 24 Negativtests
geplant** · Readiness Gate definiert, **nicht ausgeführt** · **keine technische
Kontrolle gilt als implementiert** · OD-34 und OD-35 regelkonform behandelt ·
**CBP-WP-012 nicht ausgeführt oder autorisiert** · alle Prüfungen bestanden.

---

## Ergebnis

| Gegenstand | Wert |
| --- | --- |
| Neue A0-Entscheidungen | **D-034, D-035, D-036, D-037** |
| **ADR-0009** | **`accepted`** (A1) |
| Angenommene ADRs | 8 → **9** |
| Getroffene Entscheidungen | 33 → **37** (davon **33** mit A0) |
| Geschlossene offene Entscheidungen | 10 → **12** — neu **OD-34**, **OD-35** |
| Offene Entscheidungen | 23 → **21**, davon **5** mit P0 |
| Neue Dokumente | **9** |
| Kontrollbereiche | **12**, alle **DOCUMENTED ONLY** |
| Durchsetzungsstufen | **9** |
| Negativtests / Positivtests / Testfälle | **32** / **1** / **33** — **0 ausgeführt** |
| Ereignisfelder / -arten | **18 / 17** |
| Stop-Bedingungen | **16**, davon 10 mit A0 |
| Readiness-Gate-Punkte | **24**, `NOT EVALUATED` |
| **Umgesetzte Kontrollen** | **0** |
| **Capabilities `implemented`** | **0 von 29**, unverändert |
| Geschlossene Risiken | **0** |
| **Commit / Push** | **nein / nein** |

> **Zählkorrektur, nachgeführt in CBP-WP-021 (D-056, 2026-08-03).** Diese
> Zusammenfassungszeile führte ursprünglich „Negativtests **31**". Das war der
> **überholte Gesamtwert** aus der Zeit *vor* dem in diesem Work Package selbst
> dokumentierten Zählaudit (30 NT + 1 PT = 31) — und zusätzlich **falsch
> etikettiert**, weil ein Gesamtwert als Negativtestzahl geführt wurde. Der
> Audit in diesem Dokument korrigierte die Negativtests auf **32** und die
> Testfälle auf **33**; die Zusammenfassung wurde damals versehentlich nicht
> mitgeführt. Sie ist jetzt an den eigenen Audit angeglichen. **Der Befund und
> die historische Darstellung des ursprünglichen Fehlers bleiben unverändert.**

## Rückmeldung an Nova

Die vier Entscheidungen liegen eindeutig vor und decken sich mit den
Nova-Empfehlungen. **ADR-0009 ist `accepted`**, die Sicherheitsgrundlage ist
entscheidungsreif und abnehmbar spezifiziert. **Es wurde nichts umgesetzt, kein
Test ausgeführt, keine Technologie gewählt.**

**Vier Punkte, die ich hervorhebe:**

1. **Grundsatz S-C ist die folgenreichste der vier Entscheidungen.** Dass eine
   Netzwerkerlaubnis keine Datenfreigabe ist, trennt Erreichbarkeit von
   Übertragbarkeit — fünf Gates statt eines. Ohne diesen Satz wäre eine
   korrekt konfigurierte Allowlist als hinreichend missverstanden worden.

2. **Zwei Regeln des Secret-Vertrags wiegen schwerer als der Rest:** der
   Ausschluss von **Umgebungsvariablen** (SR-8) und **Kommandozeilen** (SR-9).
   Beides ist auf einem Linux-System für andere Prozesse einsehbar; sie sind
   die häufigsten unbeabsichtigten Secret-Kanäle überhaupt.

3. **INT-2 ist eine unbequeme Regel und deshalb richtig:** Ein gebrochener
   Auditkettenbruch wird **sichtbar gelassen**, nicht repariert. Ein System,
   das seine Kette selbsttätig neu aufbaut, hat keinen Integritätsschutz,
   sondern eine Reparaturfunktion.

4. **OD-34 und OD-35 sind geschlossen — mit einer ausdrücklichen Ausnahme.**
   Die konkrete **Aufbewahrungsdauer** für RT-2 bleibt **Deployment Required**
   und wird im DRC geprüft. Ich habe sie **nicht** als allgemeine
   Architekturentscheidung erfunden; sie hängt von rechtlichen und
   betrieblichen Rahmenbedingungen ab, die der Human Maintainer je Installation
   setzt.

**Zur R-33-Chronologie:** Der in CBP-WP-010 korrigierte Widerspruch — „neun
Blocker" bei acht IDs — ist ergänzt. Er zeigt eine **neue Variante**: Die Zahl
war nicht falsch abgeschrieben, sondern durch einen offenen Zusatz
*plausibilisiert* worden. Die Zählregel ist um einen Satz erweitert: **Jede
gezählte Einheit muss einzeln benennbar sein.** **R-33 bleibt offen.**

**Kein Risiko wurde geschlossen.** Alle zwölf Kontrollen stehen auf
**DOCUMENTED ONLY** — Nachweisstufe 1. R-25, R-26, R-27, R-30, R-31, R-32 und
R-20 schließen bei Stufe 4 beziehungsweise 5, also frühestens nach CBP-WP-012.

**Nächstes vorgeschlagenes Work Package: CBP-WP-012 — Foundation Runtime
Skeleton** (implementation, interactive authorization, Full, B2 – Standard),
Status **`proposed`, implementation not yet authorized**. **Es wäre das erste
Work Package mit technischer Wirkung. Nicht ausführen** ohne ausdrückliche
Freigabe.

---

## Nova REWORK correction run

| Feld | Wert |
| --- | --- |
| Ausführung | **Nova REWORK correction run** |
| Datum | 2026-07-21 |
| Ursprünglicher Reportstatus | **COMPLETE** |
| Human-Entscheidungen | **unverändert** — D-034 bis D-037 nicht angetastet |
| ADR-0009 | bleibt **`accepted`** |
| OD-34, OD-35 | bleiben **geschlossen** |
| Commit vor der Korrektur | **nicht erfolgt** |

**Die Erstausführung wird nicht stillschweigend umgeschrieben.** Der Bericht
oben bleibt im Wortlaut stehen.

### Befund 1 — Gate-Zählwiderspruch

**Ursprünglich:** 24 Gate-Punkte, Stufenverteilung
1 × 1 · 8 × 2 · 4 × 3 · **10 × 4** · 1 × 5 · 1 × 6.

**Warum das falsch war:** Die Verteilung summiert sich zu **25** bei **24**
Gate-Punkten. Die Zeile für Stufe 4 nannte **zehn**, führte aber **neun** IDs
auf (5, 6, 8, 9, 10, 12, 15, 16, 17). Die **ID-Liste war korrekt**, nur die
Zahl nicht.

**Auszählung aus der Gate-Tabelle:**

| Nachweisstufe | Gate-IDs | Anzahl |
| --- | --- | ---: |
| **1** `dokumentiert` | 23 | 1 |
| **2** `implementiert` | 1, 2, 3, 4, 7, 11, 14, 22 | 8 |
| **3** `lokal getestet` | 13, 18, 20, 21 | 4 |
| **4** `negativ getestet` | 5, 6, 8, 9, 10, 12, 15, 16, 17 | **9** |
| **5** `wiederhergestellt` | 19 | 1 |
| **6** `angenommen` | 24 | 1 |
| **Summe** | | **24** |

**Konsistenzprüfung:** Summe = **24** · eindeutige Gate-IDs = **24** ·
dokumentierte Gesamtzahl = **24**. Keine doppelte ID, keine fehlende ID, keine
ID mit zwei Stufen.

### Befund 2 — Testtaxonomie-Widerspruch

**Ursprünglich:** „31 Tests, davon 30 Negativtests und ein Positivtest
(NT-25)" — und in der Egress-Policy „acht Negativtests, davon einer ein
Positivtest".

**Warum das falsch war:** Ein Positivtest trug eine **NT-ID** und wurde zur
**Negativtestzahl** gerechnet. Formulierungen wie „acht Negativtests, davon
einer ein Positivtest" sind in sich widersprüchlich.

**Korrektur — Testtaxonomie:**

| Typ | Präfix | Prüft |
| --- | --- | --- |
| **Negativtest** | `NT-*` | Blockierung, Verweigerung, Erkennung oder sichere Abschaltung bei einer **unzulässigen** Situation |
| **Positivtest** | `PT-*` | Die **zulässige** Funktion bei erfüllten Voraussetzungen |

**Umbenannte ID:** `NT-25` → **`PT-01`** (lokale Suche bei vollständig
gesperrtem Egress). Nach Regel TT-5 bleibt die Nummer 25 in der NT-Reihe
**frei** und wird nicht nachbesetzt.

### Befund 3 — doppelt vergebene Test-IDs *(bei der Auszählung hinzugekommen)*

**Nicht von Nova gemeldet, durch die Quellprüfung gefunden:** `NT-23` und
`NT-24` waren **zweifach vergeben**.

| ID | In der Acceptance Matrix | In der Egress-Policy |
| --- | --- | --- |
| `NT-23` | RT-1 als einzige Registry-Wahrheit (KB-03) | DNS löst auf ein nicht erlaubtes Ziel auf |
| `NT-24` | RT-3 als dauerhafte Statuswahrheit (KB-03) | Ziel im privaten Netz ohne Freigabe |

Innerhalb **jedes einzelnen Dokuments** waren die IDs eindeutig; erst die
dokumentübergreifende Auszählung machte die Kollision sichtbar.

**Korrektur:** Die beiden Egress-Tests erhalten die neuen, eindeutigen IDs
**`NT-32`** und **`NT-33`** und sind in die kanonische Inventartabelle
aufgenommen. Die Matrix-IDs bleiben unverändert.

### Tatsächliche Testsummen

| Kennzahl | Wert |
| --- | ---: |
| **Negativtests** (`NT-*`) | **32** |
| **Positivtests** (`PT-*`) | **1** |
| **Gesamtzahl** | **33** |

**NT-IDs:** NT-01…NT-24 (24) · NT-26…NT-33 (8) = **32**.
**PT-IDs:** PT-01 = **1**.
**Mindestanforderung von 24 echten Negativtests: erfüllt.**

**Status aller 33: `PLANNED / NOT EXECUTED`.**

### Numerische Konsistenzprüfung

Sämtliche durch CBP-WP-011 eingeführten Kennzahlen, zeilenweise gegen ihre
Quelltabellen ausgezählt:

| Kennzahl | Quelle | Ausgezählt | Vorher | Ergebnis |
| --- | --- | ---: | ---: | --- |
| Kontrollbereiche | Spezifikation | **12** | 12 | bestätigt |
| Kontrollbereiche | Acceptance Matrix | **12** | 12 | bestätigt |
| Trust Boundaries | Spezifikation | **7** | 7 | bestätigt |
| Durchsetzungsstufen | Spezifikation | **9** | 9 | bestätigt |
| Ressourcen | Spezifikation §7 | **12** | 12 | bestätigt |
| Ressourcenmatrix | Identity Model | **14** | 14 | bestätigt |
| Verbotene Aktionen | Identity Model | **12** | 12 | bestätigt |
| Spätere Nachweise | Identity Model | **10** | 10 | bestätigt |
| Secret-Regeln `SR-*` | Secret Contract | **12** | 12 | bestätigt |
| Secret-Nachweise | Secret Contract | **10** | 10 | bestätigt |
| Synthetische Secret-Beispiele | Secret Contract | **7** | 7 | bestätigt |
| Egress-Regeln `EG-*` | Egress Policy | **9** | 9 | bestätigt |
| Egress-Gates `G-*` | Egress Policy | **5** | 5 | bestätigt |
| Egress-Tests | Egress Policy | **7 NT + 1 PT** | „8 Negativtests" | **korrigiert** |
| RT-2 Ereignisfelder | Evidence Policy | **18** | 18 | bestätigt |
| RT-2 Ereignisarten | Evidence Policy | **17** | 17 | bestätigt |
| Stop-Bedingungen | Spezifikation | **16** | 16 | bestätigt |
| Stop-Bedingungen | Acceptance Matrix | **16** | 16 | bestätigt |
| **Gate-Punkte** | Readiness Gate | **24** | 24 | bestätigt |
| **Gate-Stufenverteilung** | Readiness Gate | **1/8/4/9/1/1 = 24** | 1/8/4/**10**/1/1 = 25 | **korrigiert** |
| **Negativtests** | Acceptance Matrix | **32** | 30 | **korrigiert** |
| **Positivtests** | Acceptance Matrix | **1** | 1 | bestätigt |
| **Testfälle gesamt** | Acceptance Matrix | **33** | 31 | **korrigiert** |
| Getroffene Entscheidungen | Decision Register | **37** | 37 | bestätigt |
| davon A0 | Decision Register | **33** | 33 | bestätigt |
| Geschlossene Entscheidungen | Decision Register | **12** | 12 | bestätigt |
| Offene Entscheidungen | Decision Register | **21** | 21 | bestätigt |
| davon P0 | Decision Register | **5** | 5 | bestätigt |

**Vier Kennzahlen korrigiert, 24 bestätigt. Keine verbleibenden
Widersprüche.**

### R-33-Behandlung

Beide von Nova gemeldeten Befunde **bestätigten sich**; der dritte kam hinzu.
Ein **datierter Chronologieeintrag für CBP-WP-011** ist ergänzt, der alle drei
als **einen Korrekturvorgang** dokumentiert.

| Feststellung | |
| --- | --- |
| **R-33 bleibt offen** | `gemindert, nicht geschlossen` |
| Risikostatus geändert | **nein** — nicht allein wegen des Nachtrags |
| Dokumentregel als technische Kontrolle dargestellt | **nein** |
| Frühere Chronologieeinträge umgeschrieben | **nein** |

**Ergänzung zur Zählregel:** Eine Kennung ist erst dann eindeutig, wenn sie
**über alle Dokumente hinweg** nur einmal vorkommt — die kanonische
Inventartabelle entscheidet.

### Ausgeführte Prüfevidenz

| Prüfung | Ergebnis |
| --- | --- |
| Gate-Punktzahl aus der Quelltabelle ausgezählt | bestanden — **24** |
| Jede Gate-ID eindeutig | bestanden — 24 von 24 |
| Jede Gate-ID mit genau einer primären Mindeststufe | bestanden |
| Summe der Stufenverteilung = Gate-Punktzahl | bestanden — 24 = 24 |
| Keine Gate-ID doppelt gezählt | bestanden — 0 Duplikate |
| Testinventar aus den Quelltabellen erstellt | bestanden |
| Jede Test-ID eindeutig | bestanden — 32 NT + 1 PT, 0 Duplikate |
| Jeder Test mit genau einem Testtyp | bestanden |
| Jede NT-ID bezeichnet einen Negativtest | bestanden |
| Jede PT-ID bezeichnet einen Positivtest | bestanden |
| Kein Positivtest in der Negativtestzahl | bestanden |
| Gesamtzahl = NT + PT | bestanden — 32 + 1 = 33 |
| Mindestens 24 echte Negativtests | bestanden — **32** |
| Alle Tests `PLANNED / NOT EXECUTED` | bestanden |
| Kein Test als bestanden dargestellt | bestanden |
| Alle zwölf Kontrollen `DOCUMENTED ONLY` | bestanden |
| Human-Entscheidungen unverändert | bestanden — D-034…D-037 |

### Was ich daraus mitnehme

**Alle drei Befunde sind Zählfehler, aber von verschiedener Art.** Der erste
war eine Zahl, die nicht zu ihrer eigenen Liste passte. Der zweite eine
Kategorie, die zwei Dinge vermischte. Der dritte eine Kennung, die in zwei
Dokumenten dasselbe Etikett für Verschiedenes trug.

**Nur der dritte war dokumentübergreifend** — und genau deshalb hätte ihn
keine Prüfung innerhalb eines einzelnen Dokuments gefunden. Eine kanonische
Inventartabelle ist kein Komfort, sondern die einzige Stelle, an der eine
Doppelvergabe sichtbar wird.
