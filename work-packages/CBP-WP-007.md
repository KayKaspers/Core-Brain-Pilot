# CBP-WP-007 — G0 Decision Recording and Phase 1 Backlog

| Feld | Wert |
| --- | --- |
| ID | CBP-WP-007 |
| Titel | G0 Decision Recording and Phase 1 Backlog |
| Typ | `docs-only` |
| Prompt Mode | **Standard** (NDF v1.0.0) |
| Context Budget | **B0 – Micro** (Core Brain Pilot) |
| Phase | Phase 0 – Abschluss |
| Ausgeführt am | 2026-07-21 |
| Ablauf | **interaktiv**, zwei Phasen |
| Status | `in-review` |
| Autoritätsklasse | A2 |

---

## Ziel

Die ausdrückliche G0-Entscheidung und die separate ADR-0006-Entscheidung des
Human Maintainers erheben, dokumentieren und in Projektstatus sowie einen
priorisierten Phase-1-Backlog überführen.

## Interaktiver Ablauf

| Phase | Inhalt | Ergebnis |
| --- | --- | --- |
| **A** | Repository read-only prüfen, **einen** Entscheidungsfragebogen ausgeben, keine Datei verändern | Fragebogen ausgegeben, 14 Vorprüfungspunkte bestanden, **0 Dateiänderungen** |
| **B** | Nur die tatsächlich gegebenen Entscheidungen dokumentieren, Status und Register aktualisieren, Backlog erstellen | Beide Entscheidungen aufgezeichnet |

## Human-Entscheidungen

Beide am **2026-07-21**, Autorität **A0**, Quelle: direkte
Human-Maintainer-Entscheidung. Wortlaut unverändert übernommen, keine Auflage
ergänzt oder erweitert.

### G0

**APPROVE G0 WITH NOTES**

Kern der Notes: Die Freigabe autorisiert **ausschließlich die Planung von
Phase 1** — keine Freigabe für produktiven Betrieb, produktiven Ingest,
öffentliche Erreichbarkeit oder zusätzliche sensible Datenklassen. Fünf
Nachweise sind vor produktivem Betrieb zu erbringen; Web-UI und mobile Nutzung
erst nach einem funktionierenden und **gemessenen** Retrieval-Piloten.

### ADR-0006

**ACCEPT ADR-0006**

Produktive und private Wissensbestände bleiben außerhalb des allgemeinen
Core-Repositorys und werden über logische Source Slots und
deploymentspezifische, fail-closed Mappings angebunden. **Keine konkreten
Pfade, Repository-URLs oder Produktionsbestände** festgelegt; OD-05, OD-06 und
OD-26 bleiben offen.

Vollständiger Wortlaut in den beiden Entscheidungsblöcken in
[G0_SCOPE_LOCK_REVIEW.md](../docs/discovery/G0_SCOPE_LOCK_REVIEW.md).

## Scope

- Entscheidungsfragebogen ausgeben und auf Antwort warten
- Beide Entscheidungen in den vorhandenen Blöcken aufzeichnen
- G0-Status und Phasenstatus setzen
- ADR-0006 auf `accepted`
- Phase-1-Backlog erstellen
- Zähl- und Statusregel dokumentieren
- Register und Statusdokumente nachführen

## Out of Scope

- Entscheidungen erfinden, ergänzen oder erweitern
- Dateiänderung vor der Human-Antwort
- Technische Implementierung jeder Art
- DRC ausführen, Benchmark ausführen, Quellen anbinden
- OD-05, OD-06, OD-26 schließen
- Commit, Push, Branch, Remote-Änderung

## Inputs

NDF v1.0.0 · Repository-Stand auf `main` (Commit `f93f257`) ·
`G0_SCOPE_LOCK_REVIEW.md` · `G0_EVIDENCE_MATRIX.md` ·
`G0_SCOPE_LOCK_CRITERIA.md` · `PILOT_SOURCE_CONTRACT.md` ·
`SOURCE_SLOT_MODEL.md` · `ADR-0006` · `DEPLOYMENT_READINESS_CHECK.md` ·
`BENCHMARK_PLAN.md` · `PERMISSION_MODEL.md` · `PROJECT_MANIFEST.md` ·
`DECISION_REGISTER.md` · `RISK_REGISTER.md` · `WORK_PACKAGE_QUEUE.md` ·
`PROJECT_BRAIN.md` · `CBP-WP-006.md` · **Antworten des Human Maintainers**

## Aufgaben

1. Phase A — Vorprüfung und Entscheidungsfragebogen
2. Phase B — Entscheidungen prüfen und aufzeichnen
3. G0-Statusregeln anwenden
4. ADR-0006-Statusregeln anwenden
5. Entscheidungsdokumentation in den vorhandenen Blöcken
6. Phase-1-Backlog
7. Zähl- und Statusregel
8. Status und Register

## Prüfungen

21 Prüfungen. Schwerpunkte: Entscheidungen stammen direkt vom Human
Maintainer · nichts ergänzt oder erweitert · A0-Autorität auf konkrete
Entscheidungen begrenzt · Status entspricht exakt der Entscheidung · Criteria
complete und technische Implementierung bleiben getrennt · DRC bleibt
NOT EVALUATED · Benchmark bleibt nicht ausgeführt · jeder Backlogpunkt als
Planung markiert · R-33 nicht ohne technische Evidenz geschlossen · kein
Commit, kein Push.

## Akzeptanzkriterien

Beide Entscheidungen aufgezeichnet · Status exakt entsprechend · Phase-1-Backlog
bei bestandenem G0 vorhanden und als Planung markiert · Zählregel dokumentiert ·
keine Capability `implemented` · keine Implementierung begonnen · alle
Prüfungen bestanden.

---

## Ergebnis

| Gegenstand | Wert |
| --- | --- |
| **G0** | **PASSED WITH NOTES** |
| **Phase 0** | **COMPLETE** |
| **Phase 1** | **AUTHORIZED FOR PLANNING** |
| **ADR-0006** | `proposed` → **`accepted`** (A1) |
| Neue A0-Entscheidungen | D-027 (G0), D-028 (ADR-0006) |
| Phase-1-Backlog | 11 Punkte, **alle „Implementierung erlaubt: nein"** |
| Zählregel | 5 Regeln in `COMPLIANCE_CHECK.md` |
| DRC | **NOT EVALUATED**, unverändert |
| Benchmark | **nicht ausgeführt**, unverändert |

## Rückmeldung an Nova

**Phase 0 ist abgeschlossen.** G0 wurde am 2026-07-21 mit Auflagen freigegeben,
ADR-0006 angenommen. Beide Entscheidungen sind im Wortlaut aufgezeichnet; ich
habe nichts ergänzt und keine zusätzliche Auflage erfunden.

**Die fünf Auflagen sind im Backlog verankert**, nicht nur zitiert: jede ist
einem Punkt zugeordnet (P3, P8, P7, P10, P9), und die Sequenzierungsauflage für
Web-UI und mobile Nutzung steht als Abhängigkeit in P11.

**Vier Punkte, die ich hervorhebe:**

1. **Die Freigabe autorisiert Planung, nicht Implementierung.** Alle elf
   Backlogpunkte tragen „Implementierung erlaubt: nein". Auch das
   vorgeschlagene Folge-Work-Package ist `docs-only`.

2. **Der Statuswechsel ändert nichts an der technischen Lage.** 16 der 25
   Kriterien beschreiben weiterhin Kontrollen, die nicht existieren. DRC bleibt
   `NOT EVALUATED`, der Benchmark unausgeführt, `excluded-from-ai` ungeprüft,
   Restore ungetestet. **Kein Risiko wurde durch die Gate-Entscheidung
   geschlossen.**

3. **ADR-0006 ist die wirksamste Einzelentscheidung dieses Projekts.** Sie hält
   privaten Bestand konstruktiv aus der Git-Historie des Kern-Repositorys —
   der einzige Schutz gegen R-01, der nicht auf Disziplin beruht.

4. **Die Zählregel ist eine Dokumentregel, keine Kontrolle.** R-33 bleibt
   offen. Drei Zählfehler in sieben Work Packages sind dokumentiert; die Regel
   macht den vierten wahrscheinlich später sichtbar, aber nicht unmöglich.

**Ein Hinweis zur Reihenfolge:** P3 (technische Sicherheitsgrundlage) ist der
breiteste Enabler — P4, P8 und P10 hängen daran. Wenn Phase 1 irgendwo
beginnen soll, dann dort.
