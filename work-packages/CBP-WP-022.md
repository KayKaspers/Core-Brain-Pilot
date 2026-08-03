# CBP-WP-022 — KB-04 Enforcement Stage 1

| Feld | Wert |
| --- | --- |
| Titel | **KB-04 Enforcement Stage 1** |
| Typ | **security-foundation enforcement** (Stufe 1) |
| Prompt Mode | **Full** · Context Budget **B2 – Standard** |
| Status | **`in-review`** |
| Aktuelle Phase | **Phase B0 – Registration and Authority Baseline** |
| Registration Decision | **D-057** (konsolidiert, A–M) |
| Decision Class | **A0** |
| ADR | **`ADR_NOT_REQUIRED`** — **nur für die Registration-Decision** |
| Registrierungsdatum | **2026-08-03** |
| Human-Maintainer-Freigabe | **Registration B0 authorized** |
| Technische Implementierung | **nicht autorisiert** |
| KB-04-Status | **`DOCUMENTED ONLY`** — unverändert |
| Capabilities | **0 von 29** — unverändert |
| Gates | Mapping Activation `NOT EVALUATED` · Security Foundation Readiness `NOT EVALUATED` |
| Security Controls | **12 `DOCUMENTED ONLY`** |
| R-20 | **offen** |
| R-33 | **18/21** — in diesem Lauf **unverändert** |
| Commit | **noch nicht vorhanden** — Commit-Autorität beim Human Maintainer |

---

## Zweck

**KB-04 ist der Kontrollbereich „Dateisystemrechte".** Sein Zweck ist im
Repository normativ festgelegt und wird hier **nicht neu definiert**:

| Feld | Kanonischer Inhalt |
| --- | --- |
| **Ziel** | **Deny-by-default auf Dateiebene** |
| **Bedrohung** | **Direktzugriff unter Umgehung der Anwendung** |
| **Anforderung** | Explizite Owner- und Gruppenregeln · **keine world-writable Dateien** · **kein Schreibrecht auf Canonical durch Retrieval oder Ingest** · **Symlink-Escapes blockieren** · sichere Dateierstellung und **atomare Writes** |
| **Nachweis** | Rechteauflistung **vor und nach dem Start** |
| **Negativtests** | **NT-04** (Canonical Write scheitert) · **NT-05** (Symlink Escape blockiert) |
| **Positivtest** | Atomare Writes in RT-1 funktionieren |
| **Evidence-Ereignis** | `incident` |
| **Stop-Bedingung** | **SB-S04** |
| **Rücksetzung** | Rechte auf den dokumentierten Ausgangszustand |
| **Nachweisstufe** | **4** — negativ getestet |
| **Durchsetzungsstufe** | **1** |

> **KB-04 ist die unterste tragende Ebene. Versagt sie, sind KB-05 bis KB-07
> wirkungslos.** (Spezifikation §KB-04; wortgleich im Foundation Plan.)

## Problem Statement

Das Repository beschreibt genau ein Problem: **Berechtigungen bestehen als
Modell, aber nicht technisch.** KB-04 steht auf **`DOCUMENTED ONLY`** — die
Anforderung ist spezifiziert und abnehmbar beschrieben, aber **auf keinem
System durchgesetzt**. Solange das so bleibt, ist ein Direktzugriff unter
Umgehung der Anwendung **nicht technisch verhindert**, und die darauf
aufbauenden Kontrollen KB-05 bis KB-07 sind laut Spezifikation **wirkungslos**.

**Keine weitergehende Problembeschreibung wird ergänzt** — dies ist der im
Repository belegte Umfang.

## Authority

| Quelle | Klasse | Beitrag |
| --- | --- | --- |
| [docs/decisions/ADR-0009-technische-sicherheitsgrundlage.md](../docs/decisions/ADR-0009-technische-sicherheitsgrundlage.md) | **A1** `accepted` | Grundlage: zwölf Kontrollbereiche und **neunstufige** Durchsetzungsreihenfolge |
| [docs/security/TECHNICAL_SECURITY_FOUNDATION_SPECIFICATION.md](../docs/security/TECHNICAL_SECURITY_FOUNDATION_SPECIFICATION.md) | **A2** | **§KB-04** — Ziel, Bedrohung, Anforderung, Nachweis, Negativtests, Stop-Bedingung; **§11** neunstufige Durchsetzungsreihenfolge, **Stufe 1 = OS-Dateirechte** |
| [docs/security/SECURITY_CONTROL_ACCEPTANCE_MATRIX.md](../docs/security/SECURITY_CONTROL_ACCEPTANCE_MATRIX.md) | **A2** | **§KB-04** — Abnahmekriterien, Status **`DOCUMENTED ONLY`**, NT-04/NT-05, Nachweisstufe 4 |
| [docs/operations/SECURITY_FOUNDATION_READINESS_GATE.md](../docs/operations/SECURITY_FOUNDATION_READINESS_GATE.md) | **A3** | Gate-Punkt **3** (OS-Rechte umgesetzt, Stufe 2) und **5** (Canonical read-only, **NT-04**, Stufe 4); Gate **`NOT EVALUATED`** |
| [docs/operations/PILOT_MAPPING_ACTIVATION_GATE.md](../docs/operations/PILOT_MAPPING_ACTIVATION_GATE.md) | **A3** | KB-01 bis KB-04 sind Voraussetzung der Punkte **7, 8, 11** |
| [docs/roadmap/TECHNICAL_SECURITY_FOUNDATION_PLAN.md](../docs/roadmap/TECHNICAL_SECURITY_FOUNDATION_PLAN.md) | **A3** | KB-04-Planblatt; **Voraussetzung KB-01, KB-02**; Umsetzungsreihenfolge **Schritt 1 = KB-01, KB-02, KB-04** |
| [docs/roadmap/PHASE_1_EVIDENCE_PLAN.md](../docs/roadmap/PHASE_1_EVIDENCE_PLAN.md) | **A3** | Implementierungsnachweis: **Rechteauflistung (KB-04)** |
| [docs/roadmap/PHASE_1_STOP_CONDITIONS.md](../docs/roadmap/PHASE_1_STOP_CONDITIONS.md) | **A3** | Wiederaufnahme erst nach **bestandenem KB-04-Negativtest** |
| [docs/roadmap/INGEST_QUARANTINE_PLAN.md](../docs/roadmap/INGEST_QUARANTINE_PLAN.md) | **A3** | Quarantänebereich muss über KB-03/KB-04 für den Indexer unzugänglich sein |
| [project-system/DECISION_REGISTER.md](../project-system/DECISION_REGISTER.md) — **OD-37** | **A2**, `offen` | Produktive Quarantäne-Isolation auf der Ziel-VM (**KB-03, KB-04**): OS-Rechte, getrennte Identität, Unzugänglichkeit für den Indexer — **Deployment Required** |
| [work-packages/CBP-WP-011.md](CBP-WP-011.md) | **A2** | Registriert KB-04: Durchsetzungsstufe **1**, Nachweisstufe **4**, Status **`DOCUMENTED ONLY`** |
| [core/core_brain/gate/security_contract.py](../core/core_brain/gate/security_contract.py) · [docs/runtime/SECURITY_FOUNDATION_READINESS_CONTRACT.md](../docs/runtime/SECURITY_FOUNDATION_READINESS_CONTRACT.md) | **A2** | KB-04 ist **runtime-scoped** und in den Bindungen **(7, KB-04)**, **(8, KB-04)**, **(11, KB-04)** geführt |
| [deployments/profile-a/bundle.json](../deployments/profile-a/bundle.json) | **A2** | Führt KB-04 mit Status **`DOCUMENTED ONLY`** |

**Kein Widerspruch festgestellt.** Alle Quellen beschreiben KB-04 übereinstimmend
als Dateisystemrechte-Kontrolle auf Durchsetzungsstufe 1 mit Nachweisstufe 4 und
Status `DOCUMENTED ONLY`.

## Stage-1-Grenze

**„Enforcement Stage 1" bezeichnet Stufe 1 der neunstufigen technischen
Durchsetzungsreihenfolge** aus Spezifikation §11:

| Stufe | Ebene | Gilt noch, wenn … |
| --- | --- | --- |
| **1** | **OS-Dateirechte** | … die Anwendung kompromittiert ist |

**KB-04 ist der Kontrollbereich, dessen tragende Ebene Stufe 1 ist.**

> **Der englische Begriff „Enforcement Stage 1" ist eine Benennung dieser
> bestehenden Stufe, keine neue Definition.** Er kommt im Repository sonst
> nirgends vor.

**Bindende Regel:** *„Eine spätere Stufe darf eine frühere technische Kontrolle
nicht ersetzen."*

### Was ausdrücklich nicht zu Stage 1 gehört

Stufe **2** Prozess- oder Containeridentität · **3** Mount-Modi und
Speichergrenzen · **4** Secret-Bereitstellung · **5** API-Authentisierung und
-Autorisierung · **6** Netzwerkgrenzen · **7** Approval-Zustände · **8** Audit
und Operational Evidence · **9** Promptregeln (nur ergänzend). Damit gehören
**KB-01, KB-02, KB-03, KB-05 bis KB-12** nicht zum Stage-1-Gegenstand.

### Offene Konkretisierung

Die vorhandene Authority liefert die **Anforderung** an KB-04 vollständig,
**aber keine technische Stage-1-Lösungsdefinition** — kein Rechtevertrag, kein
Prüfverfahren, keine Werkzeugwahl, keine Ablageentscheidung.

**Stage 1 wird in B0 daher ausschließlich als zu konkretisierende
Implementierungsstufe registriert.** Es wird **keine technische Lösung
vorweggenommen**. Design und ADR-Bewertung sind **Voraussetzung einer späteren
B1-Freigabe**.

## Voraussetzungen

| Voraussetzung | Beleg | Stand |
| --- | --- | --- |
| **KB-01** und **KB-02** | Foundation Plan: KB-04 „Voraussetzung KB-01, KB-02"; Umsetzungsreihenfolge Schritt 1 | beide **`DOCUMENTED ONLY`** |
| Reale Profil-A-Instanz für Nachweisstufe 4 | NT-04 und NT-05 verlangen ein reales POSIX-Dateisystem | **existiert nicht** — keine Bereitstellung |
| **OD-37** | Produktive Isolation auf der Ziel-VM (KB-03, KB-04), Deployment Required | **offen** |
| Separate Human-Freigabe für B1/B2 | D-057 K | **nicht erteilt** |

## Abhängigkeiten

**Decisions:** D-034 bis D-037 (Sicherheitsgrundlage), **D-057** (diese
Registrierung), **OD-37** (offen).
**ADRs:** **ADR-0009** (A1, Grundlage), ADR-0010 (Quarantäne-Bezug),
ADR-0013 (KB-04 als runtime-scoped Control im Evidence-/Security-Contract).
**Controls:** **KB-04** primär; KB-01, KB-02 als Voraussetzung; KB-05 bis KB-07
bauen darauf auf.
**Gates:** Security Foundation Readiness Gate Punkte **3** und **5**; Mapping
Activation Gate Punkte **7, 8, 11**. **Beide Gates bleiben `NOT EVALUATED`.**
**Tests:** **NT-04**, **NT-05** — **nicht ausgeführt** (0 von 32 Negativtests).
**Stop-Bedingung:** **SB-S04**.
**Risiken:** **R-06**, **R-25**, **R-26**; **R-20 offen**; **R-33 18/21**.
**Contracts:** Security Foundation Readiness Contract (Bindungen 7, 8, 11);
Profil-A-Bundle (`bundle.json` führt KB-04 `DOCUMENTED ONLY`).
**Work Packages:** CBP-WP-011 (Registrierung von KB-04), CBP-WP-012 (Skeleton
ohne Durchsetzung), CBP-WP-020 (Profil-A-Bundle), CBP-WP-021 (Testinventar).

## Non-Goals

| Ausgeschlossen |
| --- |
| **keine technische Implementierung in B0** |
| kein Runtime-Code |
| kein Deployment · keine reale Infrastruktur |
| keine operative Security-Testausführung (NT-04, NT-05 bleiben unausgeführt) |
| **keine Control-Hochstufung** — KB-04 bleibt `DOCUMENTED ONLY` |
| keine Gateauswertung · keine Gatefreigabe |
| keine Capability-Änderung |
| **kein KB-04-Stage-2-Scope** und keine andere Durchsetzungsstufe |
| kein RT-2 · keine Persistenz |
| kein Source- oder Mapping-Aktivierungsschritt |
| keine Commitzähler-Governance |
| kein Folge-Work-Package (**CBP-WP-023 nicht registriert**) |
| keine neue Control-ID · keine neue Test-ID · keine Wiederverwendung von NT-25 |
| keine neue Risiko-ID · keine R-33-Fortschreibung · keine R-20-Änderung |
| keine neue ADR-Datei |

## Phasenmodell

| Phase | Gegenstand | Stand |
| --- | --- | --- |
| **B0** | **Registration and Authority Baseline** | **aktuell autorisiert (dieser Stand, uncommitted)** |
| **B1** | **Contract and Design Boundary** | **nicht autorisiert** |
| **B2** | **Implementation and Validation** | **nicht autorisiert** |
| **C** | **Post-Commit Reconciliation** | **nicht autorisiert** |

**Vor einer B1-Freigabe ist die ADR-Erforderlichkeit anhand des dann
konkretisierten Designs erneut zu bewerten.**

## Acceptance Criteria für B0

B0 ist **nur** erfüllt, wenn:

1. die KB-04-Authority **vollständig auditiert** wurde,
2. **keine Authority-Widersprüche** bestehen,
3. **D-057** als `accepted`/**A0** registriert ist,
4. **CBP-WP-022** als `in-review` registriert ist,
5. die **Implementierung ausdrücklich nicht autorisiert** ist,
6. **keine technische Datei** verändert wurde,
7. **keine Capability, kein Gate und kein Control** verändert wurde,
8. **kein Folge-Work-Package** registriert wurde.

## Stop Conditions

| Bedingung | Wirkung |
| --- | --- |
| widersprüchliche KB-04-Definition | anhalten, Blocker melden |
| fehlende Authority für eine geforderte Aussage | anhalten, **nichts ergänzen** |
| ungeklärte ADR-Erforderlichkeit für die spätere Umsetzung | **B1 nicht freigeben** |
| Scope außerhalb Stufe 1 | anhalten |
| notwendige Änderung einer verbotenen Datei | anhalten |
| technische Implementierung wäre zur bloßen Registrierung erforderlich | anhalten |

---

## Aussageschutz

Dieses Work Package belegt in Phase B0 **nicht**:

| Nicht belegt | Tatsächlicher Stand |
| --- | --- |
| KB-04 sei implementiert, getestet oder enforced | **`DOCUMENTED ONLY`** |
| Ein Security-Foundation-Test sei ausgeführt | **0 von 32** NT, **0 von 1** PT |
| Ein Gate sei ausgewertet | beide **`NOT EVALUATED`** |
| Eine Capability sei erreicht | **0 von 29** |
| Eine Bereitstellung existiere | **keine** |
| RT-2 existiere | **nicht implementiert** |
| Die spätere Umsetzung sei ADR-frei | **erneut zu bewerten vor B1** |

**Die Registrierung eines Work Packages ist keine Implementierungsfreigabe.**

**CBP-WP-023 ist nicht registriert und nicht autorisiert.**
