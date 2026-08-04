# CBP-WP-022 — KB-04 Enforcement Stage 1

| Feld | Wert |
| --- | --- |
| Titel | **KB-04 Enforcement Stage 1** |
| Typ | **security-foundation enforcement** (Stufe 1) |
| Prompt Mode | **Full** · Context Budget **B2 – Standard** |
| Status | **`in-review`** |
| Aktuelle Phase | **Phase B2A – Contract Model and Read-only Validator** |
| Registration Decision | **D-057** (konsolidiert, A–M) |
| ADR-Gate-Decision | **D-058** (konsolidiert, A–M) — Ergebnis **`ADR_REQUIRED`** |
| Architektur-Decision | **D-059** (konsolidiert, A–N) — Ergebnis **`ADR-0014_ACCEPTED`** |
| Contract-Decision | **D-060** (konsolidiert, A–S) — Ergebnis **`KB-04_STAGE_1_CONTRACT_ACCEPTED`**, **`ADR_NOT_REQUIRED`** |
| Decision Class | **A0** — für D-057, D-058, D-059 und D-060 |
| ADR | **ADR-0014** — *KB-04 Stage 1 Filesystem Enforcement Architecture*, `accepted`, **Autoritätsklasse A1**, 2026-08-03. `ADR_NOT_REQUIRED` galt für D-057 und gilt für **D-060**, **solange der Vertrag vollständig innerhalb ADR-0014 bleibt** |
| Enforcement Contract | [KB_04_STAGE_1_ENFORCEMENT_CONTRACT.md](../docs/security/KB_04_STAGE_1_ENFORCEMENT_CONTRACT.md) — **`accepted contract`**, 2026-08-03 |
| Registrierungsdatum | **2026-08-03** |
| Human-Maintainer-Freigabe | **B2A Contract Model and Read-only Validator authorized** |
| Technische Implementierung | **B2A implementiert** (intern, read-only) · **B2B, B2C und B2D nicht autorisiert** |
| KB-04-Status | **`DOCUMENTED ONLY`** — unverändert |
| Capabilities | **0 von 29** — unverändert |
| Gates | Mapping Activation `NOT EVALUATED` · Security Foundation Readiness `NOT EVALUATED` |
| Security Controls | **12 `DOCUMENTED ONLY`** |
| R-20 | **offen** |
| R-33 | **18/21** — in diesem Lauf **unverändert** |
| Commit | **B0 `committed` `e4caa14`** · **B1A `committed` `1a7696d`** · **B1B `committed` `b86a35f`** · **B1C `committed` `24de07e`** · **B2A nicht committed** — Commit-Autorität beim Human Maintainer |

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
| **B0** | **Registration and Authority Baseline** | **complete** — `committed` `e4caa14` |
| **B1A** | **Contract Boundary and ADR Gate** | **complete** — `committed` `1a7696d` |
| **B1B** | **ADR-0014 Authoring and Design Decision** | **complete** — `committed` `b86a35f` |
| **B1C** | **Enforcement Contract and Validation Plan** | **complete** — `committed` `24de07e` |
| **B2A** | **Contract Model and Read-only Validator** | **complete (dieser Stand, uncommitted)** |
| **B2B** | **New-target Initialization Boundary** | **nicht autorisiert** |
| **B2C** | **Synthetic Tests and Evidence** | **nicht autorisiert** |
| **B2D** | **Profile-A Deployment Integration** | **nicht autorisiert** |
| **C** | **Post-Commit Reconciliation** | **nicht autorisiert** |

**Die ADR-Erforderlichkeit wurde in B1A bewertet und in D-058 mit
`ADR_REQUIRED` beantwortet; ADR-0014 ist in B1B angenommen; der
implementierungsfähige Vertrag ist in B1C unter D-060 angenommen.
**B2 bleibt nicht autorisiert.**

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

## Phase B1A — Contract Boundary and ADR Gate

**B0-Commit:** `e4caa14` — „CBP-WP-022: register KB-04 enforcement stage 1“,
10 Pfade (1 neu, 9 modifiziert), 338 Einfügungen, 32 Löschungen.

### Technische Fundstellen

| Quelle | Aussage | Klasse | Bindung | Offene Designfrage | ADR-Relevanz |
| --- | --- | :---: | --- | --- | :---: |
| Spezifikation §KB-04 | Owner-/Gruppenregeln, keine world-writable Dateien, kein Canonical-Schreiben durch Retrieval/Ingest, Symlink-Escapes blockieren, sichere Erstellung, atomare Writes | **C** | **bindend** | — | Grundlage |
| Spezifikation §44, §468 | Unix-/Container-Identitäten, UID, GID — **Deployment Required** | **C** | **bindend** | Identitätsabbildung | **hoch** |
| Acceptance Matrix §KB-04 | Status `DOCUMENTED ONLY`, **NT-04**, **NT-05**, Nachweisstufe **4**, **SB-S04** | **C** | **bindend** | — | Nachweisziel |
| Identity Model :13, :225 | **keine konkreten Unix-Benutzer, keine Gruppen, keine UID-/GID-Werte**; UID/GID **Deployment Required** | **C** | **bindend** | **Owner-/Gruppenmodell** | **hoch** |
| Identity Model V-1, V-3, V-5, V-11, V-12 | kein root, kein privilegierter Container, kein Canonical-Schreiben ohne Freigabe, kein Backup-Schreiben, keine Impersonation | **C** | **bindend** | — | Randbedingung |
| Identity Model M-1…M-4 | keine unkontrollierten Host-Mounts · RT-2 nie direkt eingebunden · nicht benötigter Bereich **gar nicht** eingebunden · **Symlink-Escapes blockieren** | **C** | **bindend** | Mount-Modus je Bereich | mittel |
| Foundation Plan KB-04 | Voraussetzung **KB-01, KB-02**; Umsetzungsreihenfolge Schritt 1 | **E** | informativ | Reihenfolge | mittel |
| Foundation Plan :91, :306 | „Konkrete UIDs und GIDs werden hier nicht festgelegt“ · **„Konkrete UIDs, GIDs, Dateimodi — offen, Deployment“** | **E** | informativ | **Dateimodi** | **hoch** |
| ADR-0010 / Quarantine MVP | atomare Schreibweise (exklusive Temp-Datei, `fsync`, `os.replace`), **kein Schreiben außerhalb des Roots, keine Hard- oder Symlinks**, `QF-STRUCTURE-SYMLINK` | **B/C** | **bindend** | — | **Präzedenzfall** |
| ADR-0011 / Registry MVP | unveränderliche Records, atomar ersetzter Katalog, kein Schreiben außerhalb des Roots, keine Hard-/Symlinks | **B/C** | **bindend** | — | **Präzedenzfall** |
| `core/core_brain/quarantine/store.py`, `registry/storage.py` | `_atomic_write_bytes`: Temp-Datei, `fsync`, `os.replace`; Reason Codes `*_STORE_IS_SYMLINK`, `*_WRITE_OUTSIDE_ROOT` | **C** | **bindend** (implementiert) | — | **Präzedenzfall** |
| Profil-A-Bundle | `read_only: true`, `cap_drop: ALL`, `no-new-privileges`, kein `privileged`, UID/GID nur als fail-closed Operatorvariablen, Config `mode 0444`, `canonical-data` beidseitig read-only, Backup und RT-2 **nicht gemountet** | **C** | **bindend** | Host-/Container-Grenze | **hoch** |
| Readiness Gate 3, 5 | „OS-Rechte umgesetzt“ (Stufe 2) · „Canonical read-only nachgewiesen“ (**NT-04**, Stufe 4) | **C/E** | **bindend** | — | Nachweisziel |
| Mapping Gate 7, 8, 11 | KB-01…KB-04 Voraussetzung; **Symlink-Verhalten geprüft** | **C/E** | **bindend** | — | mittelbar |
| Stop Conditions :45–46 | Wiederaufnahme erst nach bestandenem KB-04-Negativtest | **E** | informativ | — | Nachweisziel |
| Quarantine Plan :141, :169 | Quarantänebereich für den Indexer über KB-03/KB-04 unzugänglich | **E** | informativ | Bereichsschnitt | mittel |
| **OD-37** | Produktive Isolation auf der Ziel-VM (KB-03, KB-04) — **offen**, Deployment Required | **A** | **bindend** | **Durchsetzungsort** | **hoch** |
| PERMISSION_MODEL :35 | „Nicht-privilegierte UIDs; kanonische Volumes lesend eingebunden, wo möglich“ | **C** | **bindend** | „wo möglich“ unbestimmt | mittel |

**Konflikte: keine.** Alle Quellen sind widerspruchsfrei; die Differenz zwischen
neun Durchsetzungsstufen (A2-Spezifikation) und sieben Ebenen (A3-Plan) betrifft
die Stufenzahl, nicht KB-04 — beide ordnen KB-04 der Stufe 1 zu.

### Designachsen

| # | Achse | Verbindlich festgelegt | Offen | Wirkung | ADR |
| --- | --- | --- | --- | --- | :---: |
| 5.1 | **Geschützte Datenbereiche** | Canonical (read-only beidseitig), Quarantine, Freigabebereich, Source-/Mapping-Registry, `tmpfs` als RT-3, Backup und RT-2 **nicht gemountet**; Bereichsschnitt aus der Mountmatrix | Zuordnung der Evidenz-/Metadatendateien innerhalb der Bereiche | lokal | nein |
| 5.2 | **Akteure und Rollen** | Zwei logische Identitäten (`svc-control-plane`, `svc-data-worker`) plus Operator; V-5 verbietet Canonical-Schreiben ohne Freigabe; Mountmatrix regelt ro/rw je Identität | Rolle des **Setup-/Deploymentprozesses** — nirgends definiert | **architekturweit** | **ja** |
| 5.3 | **Besitz- und Gruppenmodell** | **nichts** — Identity Model führt ausdrücklich keine Benutzer, Gruppen, UID- oder GID-Werte | Einzelbenutzer gegen gemeinsame Gruppe gegen getrennte Gruppen; Container-UID/GID-Abbildung; statisch oder konfigurierbar | **architekturweit** | **ja** |
| 5.4 | **Datei- und Verzeichnismodi** | Verbot world-writable; Config im Bundle `0444`; Deny-by-default | konkrete Modi — Foundation Plan: **offen, Deployment**; Execute-Bit, world-readable, group-writable, setgid, `umask` | **architekturweit** | **ja** |
| 5.5 | **Schreib- und Erstellungssemantik** | **weitgehend entschieden** — exklusive Temp-Datei, `fsync`, `os.replace`, kein Schreiben außerhalb des Roots (ADR-0010/0011, implementiert) | Übertragung des Musters auf Canonical und Freigabebereich | lokal | nein |
| 5.6 | **Link- und Pfadsicherheit** | Symlink-Escapes blockieren (KB-04, M-4); keine Hard-/Symlinks in den Stores; `*_WRITE_OUTSIDE_ROOT`; Bundle-Validator folgt keinen Symlinks | Hardlink-Behandlung außerhalb der Stores; **TOCTOU-Strategie**; Pfadauflösungsverfahren | mittel | teilweise |
| 5.7 | **Deployment- und Plattformgrenze** | Ubuntu Server 26.04 LTS amd64, Docker Compose in dedizierter VM; Container `read_only`, non-root über Operatorvariablen | **Host- gegen Container-Verantwortung** für Besitz und Modi; Verhalten auf Nicht-POSIX-Plattformen | **architekturweit** | **ja** |
| 5.8 | **Nachweis und Tests** | NT-04, NT-05, SB-S04, Nachweisstufe 4, Gate-Punkte 3 und 5 | Was offline prüfbar ist gegen was eine **reale Profil-A-Instanz** verlangt | lokal | nein |
| 5.9 | **Migration und Kompatibilität** | **nichts** | Umgang mit bestehenden Artefakten falscher Rechte; Reparaturmodus; Idempotenz; Rückwärtskompatibilität | **architekturweit** | **ja** |
| 5.10 | **Konfigurationsoberfläche** | Fail-closed-Prinzip; Bundle nutzt `${...:?...}` ohne Defaults | Welche Werte konfigurierbar sein dürfen; verbotene unsichere Werte; Validierungszeitpunkt | mittel | teilweise |

**Sechs der zehn Achsen enthalten eine offene, architekturweit wirkende Wahl.**

### Contract Boundary

**Verbindliche Sicherheitsinvarianten** (ausschließlich repository-gestützt):

| # | Invariante | Beleg |
| --- | --- | --- |
| **I-1** | **Deny-by-default auf Dateiebene** | Spezifikation §KB-04 |
| **I-2** | **Keine world-writable geschützten Artefakte** | Spezifikation §KB-04, Acceptance Matrix |
| **I-3** | **Retrieval besitzt keinen Schreibzugriff auf Canonical** | §KB-04, V-5, Mountmatrix |
| **I-4** | **Ingest besitzt keinen unkontrollierten Schreibzugriff auf Canonical** | §KB-04, V-5, TB-1/TB-2 |
| **I-5** | **Symlink-Escapes werden verhindert** | §KB-04, M-4, **NT-05** |
| **I-6** | **Schreibvorgänge erzeugen keinen unsicheren Zwischenzustand** | §KB-04 (sichere Erstellung, atomare Writes); ADR-0010/0011 |
| **I-7** | **Rechtefehler führen fail-closed, nicht zu stiller Abschwächung** | §KB-04, SB-S04, projektweites Fail-closed-Prinzip |

**Noch offene Designparameter:** Owner- und Gruppenmodell · UID-/GID-Abbildung
· konkrete Datei- und Verzeichnismodi · `umask` · Execute-Bit-Regel für
Verzeichnisse · setgid · Durchsetzungsakteur · Verifikations- gegen
Korrektursemantik · Validierungszeitpunkt · Migrations- und Reparaturverhalten
· Host-/Container-Verantwortungsgrenze · Plattformgrenze.

**Implementierungsneutrale Verantwortlichkeiten** — **keine** konkrete
Programmierschnittstelle:

| Verantwortung | Gegenstand |
| --- | --- |
| **Setup/Initialisierung** | Herstellung des dokumentierten Ausgangszustands eines Bereichs |
| **Validierung** | Feststellung, ob der Ist-Zustand die Invarianten I-1 bis I-7 erfüllt |
| **Runtime-Write** | Einhaltung von I-6 bei jedem Schreibvorgang |
| **Fehlerklassifikation** | Unterscheidung zwischen Vertragsverletzung, Umgebungsfehler und nicht anwendbarer Plattform |
| **Nachweis und Audit** | Rechteauflistung vor und nach dem Start; Ereignisart `incident` bei Verletzung |

**Fail-closed-Grenze** — eine spätere Implementierung **muss ablehnen**:
world-writable geschützte Artefakte · Schreibpfade auf Canonical für Retrieval
oder Ingest ohne dokumentierte Freigabe · Symlinks, deren Ziel den Bereich
verlässt · Schreibvorgänge ohne atomare Ersetzung · unbekannte oder nicht
zugeordnete Pfade · nicht feststellbare Rechte · jeden Zustand, der nicht
positiv als vertragskonform belegt ist. **Keine Exitcodes und keine Issue-Codes
festgelegt.**

**Nicht in Stage 1:** Application-Level-Autorisierung · Prozessisolation höherer
Stufen · Netzwerk-Enforcement · Secret-Management · Gate-Freigabe · reale
Testausführung · **KB-04 Stage 2** · **KB-01/KB-02-Implementierung** ·
**KB-03-Implementierung** · **KB-05 bis KB-12**.

### ADR-Gate — Ergebnis

| # | Prüffrage | Antwort |
| ---: | --- | --- |
| 1 | Neue Architektur oder neues Sicherheitsmuster? | **ja** — Durchsetzungsverantwortung ist nirgends festgelegt |
| 2 | Mehrere tragfähige Owner-/Gruppenmodelle? | **ja** — Identity Model führt bewusst keine Gruppen |
| 3 | Wahl root / rootless / gemischt? | **teilweise** — V-1/V-3 verbieten root im Dienst; die Privilegierung des **Setup-Akteurs** ist offen |
| 4 | Dauerhafte Host-/Container-Verantwortungsgrenze? | **ja** |
| 5 | Neue Verträge? | **ja** — ein Rechtevertrag entsteht |
| 6 | Migrations-, Kompatibilitäts- oder Deploymentwirkung? | **ja** |
| 7 | Schwer reversibel? | **ja** — persistente Besitz- und Modusverhältnisse |
| 8 | Mehrere Komponenten betroffen? | **ja** — Quarantine, Registry, Canonical, Freigabe, Bundle, Deployment |
| 9 | Ist ADR-0009 konkret genug? | **nein** — legt die Anforderung fest, verweist UID/GID/Modi auf Deployment |
| 10 | Decken bestehende ADRs die Lösungswahl ab? | **nein** |

> **Ergebnis: `ADR_REQUIRED`** — festgestellt in **D-058**. Vor jeder technischen
> Implementierung ist ein neuer ADR zu erstellen; voraussichtliche Kennung
> **ADR-0014**. **ADR-0014 wurde in diesem Lauf nicht angelegt.**

### Stand nach B1A

**B0 complete** (`e4caa14`) · **B1A complete** (dieser Stand, uncommitted) ·
**B1B — ADR-0014 Authoring and Design Decision: nicht autorisiert** · **B2 und C:
nicht autorisiert** · **technische Implementierung nicht autorisiert**.

**Unverändert:** KB-04 und alle zwölf Controls **`DOCUMENTED ONLY`** · beide
Gates **`NOT EVALUATED`** · Capabilities **0 von 29** · **NT-04 und NT-05 nicht
ausgeführt** (0 von 32 Negativtests, 0 von 1 Positivtest) · **R-20 offen** ·
**OD-37 offen** · **R-33 18/21** · keine neue Risiko-ID · keine reale
Bereitstellung · kein RT-2 · **CBP-WP-023 nicht registriert**.

---

## Phase B1B — ADR-0014 Authoring and Design Decision

**B0-Commit:** `e4caa14` — „CBP-WP-022: register KB-04 enforcement stage 1",
10 Pfade (1 neu, 9 modifiziert), 338 Einfügungen, 32 Löschungen.
**B1A-Commit:** `1a7696d` — „CBP-WP-022: determine KB-04 contract and ADR
boundary", **10 modifizierte Pfade**.

**Ausgangspunkt:** **D-058** (A0) stellte **`ADR_REQUIRED`** fest. Sechs der zehn
Designachsen enthielten eine offene, architekturweit wirkende Wahl.

### Optionenanalyse

| Option | Kern | Ergebnis |
| --- | --- | :---: |
| **A** | **Host-authoritative Deployment Enforcement** — Setup und Deployment besitzen die Authority, die Runtime validiert und scheitert fail-closed | **gewählt** |
| **B** | **Privileged Bootstrap, Unprivileged Runtime** — abgegrenzter Initialisierungsprozess innerhalb der Bereitstellungseinheit | **verortet** |
| **C** | **Runtime Self-Repair** — Langläufer korrigieren Besitz und Rechte selbst | **verworfen** |
| **D** | **ACL-centric Enforcement** — POSIX-ACLs als Hauptdurchsetzung | **verworfen** |
| **E** | **Zielmodell ohne Runtime-Validierung** — rein dokumentarisch *(ergänzt als Nullvergleich, weil `bundle.json` KB-04 bereits als `filesystem-permission-target-model` führt)* | **verworfen** |

**Ausschlusskriterien** waren die Invarianten **I-1 bis I-7**, **V-1** und
**V-3** (kein root, kein privilegierter Container), die Vereinbarkeit mit
`cap_drop: ALL`, `no-new-privileges` und `read_only` aus dem bereits
committeten Profil-A-Bundle sowie das Verbot realer UID-, GID-, Modus-,
Benutzer- und Gruppenwerte im Repository.

**Option C ist nicht die schwächere Wahl, sondern repository-widersprüchlich:**
sie verlangt Privilegien, die V-1 und V-3 verbieten und die das Bundle mit
`cap_drop: ALL` entzieht; sie verletzt **I-7**, weil sie eine Abweichung
**behebt statt sie abzulehnen**; und sie entwertet **NT-04** und **NT-05**,
deren Aussagekraft davon abhängt, dass ein falscher Zustand bestehen bleibt und
auffällt. **Option D** setzt Werkzeuge, Dateisystemoptionen und
Plattformzusagen voraus, die das Projekt nicht führt, während die
Spezifikation die Anforderung in Owner-, Gruppen- und
world-writable-Begriffen formuliert. **Option E** unterscheidet sich nicht vom
heutigen `DOCUMENTED ONLY`. **Option B ist nicht verworfen, sondern verortet:**
ihre Initialisierungsverantwortung ist Teil der gewählten Architektur und
liegt **vollständig auf der Deployment-Seite der Grenze**.

### Ausgewählte Architektur

> **Host-authoritative Enforcement mit deklarativem Zielmodell und read-only
> Runtime-Validierung.**

| Schicht | Ort | Befugnis |
| --- | --- | --- |
| **Zielmodell** | dieses Repository | beschreibt **abstrakt** Bereiche, Rollen, Zugriffsart, Rechteprofilklassen, Invarianten und Prüfregeln — **keine** realen Identitäten, UIDs, GIDs, Modi, Benutzer, Gruppen oder Hostpfade |
| **Durchsetzung** | Deployment und Operator, **außerhalb** von Runtime und Repository | bindet Rollen an Identitäten, **setzt** Besitz und Rechte **vor** dem Start, **repariert** nur ausdrücklich aufgerufen |
| **Validierung** | Runtime | **liest**, vergleicht, meldet, **scheitert fail-closed** — **setzt, ändert, repariert und mildert nichts** |

**Kategorisch:** **Keine lang laufende Runtime-Komponente verändert jemals
Besitz, Gruppe, Modus oder Identität** — unabhängig davon, ob die
Umgebung die nötigen Privilegien böte.

**Entschieden** sind Authority-Modell · Identitätsmodell mit explizit
erklärter und beim Start gegen die **effektive** Identität geprüfter
Host-/Container-Bindung · **Rechteprofil-Modell PP-1 bis PP-4** (owner-write ·
owner-write mit group-read · service-read-only · not-present) mit acht
kategorischen Klassenregeln · Initialisierung · Validierung an vier
Zeitpunkten · Migration und Reparatur nach dem Prinzip **Plan vor Wirkung**
· Link- und Pfadsicherheit einschließlich ausdrücklich anerkannter
**TOCTOU**-Grenze · Plattformgrenze · Nachweisgrenze.

**Die sieben Invarianten I-1 bis I-7 aus Phase B1A bleiben unverändert
bindend.** Die atomare Schreibsemantik aus **ADR-0010/ADR-0011** wird
**unverändert übernommen** und **nicht neu entschieden**.

### ADR-0014 und D-059

| Feld | Wert |
| --- | --- |
| Datei | [ADR-0014-kb-04-stage-1-filesystem-enforcement.md](../docs/decisions/ADR-0014-kb-04-stage-1-filesystem-enforcement.md) |
| Titel | **KB-04 Stage 1 Filesystem Enforcement Architecture** |
| Status | **`accepted`**, **Autoritätsklasse A1**, 2026-08-03 |
| Grundlage | **D-059** — `accepted`, **Decision Class A0**, ausdrücklicher Human-Maintainer-Beschluss |
| Verhältnis | konkretisiert **ADR-0009**; **löst nichts ab**; **OD-37 bleibt offen** |

**Das bestehende Autoritätsmodell bleibt unverändert:** A0 ist der
ausdrückliche Human-Maintainer-Beschluss, A1 der angenommene ADR. **Die
Decision trägt A0, der ADR trägt A1.**

### Konsequenzen

**Positiv:** Die Runtime benötigt **keinerlei** Rechteprivilegien · **keine
realen Werte im Repository** · eine Rechteabweichung wird **sichtbar** statt
überdeckt, **NT-04** und **NT-05** bleiben aussagekräftig · die konkreten
Werte bleiben außerhalb und damit neu bindbar · die Verantwortlichkeiten sind
disjunkt · der Nachweis entspricht wörtlich der Vorgabe „Rechteauflistung
vor und nach dem Start" · **OD-37** ist erstmals strukturiert.

**Negativ:** Die Sicherheit hängt an einem Vorgang **außerhalb** dieses
Repositorys · ein falsch vorbereiteter Bereich führt zu **Startverweigerung
statt Selbstheilung** · Bestandsdaten benötigen einen ausdrücklichen
Migrationsweg · der Reparaturweg ist an **RT-2** gebunden und deshalb bis auf
Weiteres **nicht freigegeben** · ein Teil der Zusage ist **nur real** prüfbar
· zwei Wahrheitsorte erfordern eine gepflegte Bindung · auf Nicht-POSIX-
Plattformen ist **keine** Durchsetzungsaussage möglich.

### Verbleibende Parameter

**Vierzehn Implementierungsparameter bleiben bewusst offen:** vollständige
Pfad-zu-Rolle-zu-Modus-Matrix · exakte symbolische oder numerische
Modusprofile · `umask` · Zuordnung der acht Bundle-Bereiche zu den
Profilklassen · Konfigurationsschema der Identitätsbindung ·
Identitätsvalidierungsvertrag · Initialisierungs- und Validierungsvertrag ·
Migrations- und Reparaturvertrag · Fehlerklassen · Bedarf an Issue- und
Exitcodes (**in ADR-0014 bewusst keine festgelegt**) · Testmatrix und
**NT-04-/NT-05**-Abbildung · Abgrenzung synthetischer gegen reale Nachweise ·
**B2-Implementierungs- und Dateiscope** · **sämtliche realen UID-, GID-,
Benutzer- und Gruppenwerte** (Deployment Required, **niemals im Repository**).

### Verbleibende Contract-Finalisierung

**B1C — Enforcement Contract and Validation Plan. Nicht autorisiert.**

B1C konkretisiert die vierzehn offenen Parameter zu einem prüfbaren Vertrag
und legt den Datei- und Implementierungsscope für B2 fest.

**B2 bleibt gesperrt. Ohne B1C ist keine technische Implementierung
zulässig.**

### Stand nach B1B

**B0 complete** (`e4caa14`) · **B1A complete** (`1a7696d`) · **B1B complete**
(dieser Stand, uncommitted) · **B1C nicht autorisiert** · **B2 und C nicht
autorisiert** · **technische Implementierung nicht autorisiert**.

**Unverändert:** **KB-04 bleibt `DOCUMENTED ONLY`**, alle zwölf Controls
`DOCUMENTED ONLY` — **keine Control-Hochstufung**; beide Gates
**`NOT EVALUATED`** — **keine Gateauswertung**; Capabilities **0 von 29**;
**NT-04 und NT-05 nicht ausgeführt** (0 von 32 Negativtests, 0 von 1
Positivtest); **SB-S04 nicht wirksam**; **R-20 offen**; **OD-37 offen** —
strukturiert, **nicht geschlossen**; **R-33 18/21**; keine neue Risiko-ID;
keine reale Bereitstellung; kein RT-2; **CBP-WP-023 nicht registriert**.

**Eine entschiedene Architektur ist keine Sicherheitswirkung.**

---

## Phase B1C — Enforcement Contract and Validation Plan

**B0-Commit:** `e4caa14` · **B1A-Commit:** `1a7696d` · **B1B-Commit:**
`b86a35f` — „CBP-WP-022: adopt KB-04 filesystem enforcement
architecture", **10 modifizierte Dateien und eine neue ADR-Datei**.

**D-060** (`accepted`, **A0**, 2026-08-03, Teile A–S) nimmt den
implementierungsfähigen Vertrag
[KB_04_STAGE_1_ENFORCEMENT_CONTRACT.md](../docs/security/KB_04_STAGE_1_ENFORCEMENT_CONTRACT.md)
an — Status **`accepted contract`**, Ergebnis
**`KB-04_STAGE_1_CONTRACT_ACCEPTED`**, ADR-Status **`ADR_NOT_REQUIRED`**.

> **D-060 konkretisiert ADR-0014. Es ändert ADR-0014 nicht und führt
> keine neue Architektur ein.** **ADR-0014 bleibt die bindende A1-Authority.**
> `ADR_NOT_REQUIRED` gilt **ausschließlich, solange der Vertrag
> vollständig innerhalb ADR-0014 bleibt**; **jede spätere Abweichung
> benötigt eine neue ADR-Erforderlichkeitsprüfung.**

### Contract-Zusammenfassung

| Vertragsbereich | Bindung |
| --- | --- |
| **Pfadklassen** | **elf** — **PC-01** Canonical · **PC-02** Quarantine · **PC-03** Source Registry · **PC-04** Mapping Registry · **PC-05** Released · **PC-06** Derived · **PC-07** Konfiguration · **PC-08** Transient · **PC-09** RT-2 · **PC-10** Backup · **PC-11** unbekannt (fail-closed). Verankert an den bereits committeten `container_paths` und `tmpfs_targets` des Bundles — **kein erfundener Rootpfad, kein Hostpfad** |
| **Akteure** | **zehn** mit zwölf Befugnisspalten; acht verbindliche Verbote |
| **Rechteprofile** | **PP-1** `0600`/`0700` · **PP-2** `0640`/`0750` (setgid `2750` nur bei zwingender Gruppenvererbung) · **PP-3a** `0640`/`0750` · **PP-3b** `0444`/`0555` — **eng begrenztes Kompatibilitätsprofil, nur PC-07, secretfrei** · **PP-4** *not-present*; `umask` **`0077`** beziehungsweise **`0027`**; acht kategorische Klassenregeln |
| **Mount- und POSIX-Trennung** | **MT-1 bis MT-8** — Schreibzugriff verlangt **gleichzeitig** Mountmodus, Rolle, PP-Profil und **positive** Identitätsbindung |
| **Vier Prüfdimensionen** | **MT-9 bis MT-14** — **D-I** Host-Quellobjekt · **D-II** Mountvertrag · **D-III** Runtime-sichtbares Objekt · **D-IV** Runtimeidentität; **der Bundlemodus ist kein Nachweis der Host-Quellrechte**, keine Dimension belegt eine andere, **eine nicht prüfbare Dimension gilt als nicht erfüllt** |
| **Identitätsbindung** | elf Felder, davon **zehn Pflichtfelder**; `value_origin` nur `operator-workspace`; acht fail-closed Fehlfälle |
| **Initialisierung** | Apply **nur** auf nachweislich neuer, leerer Struktur bei Erfüllung **aller sechs** Voraussetzungen; **Preflight → Plan → begrenztes Apply → Post-Validation**; **keine Rollback-Zusage** |
| **Validierung** | **vier** read-only Zeitpunkte; **nicht feststellbar = nicht erfüllt**; **kein periodischer Self-Repair** |
| **Link und Pfad** | **LP-1 bis LP-10**; interne Symlinks **abgelehnt statt aufgelöst**; Hardlinks verboten; **TOCTOU ausdrücklich anerkannt** |
| **Migration und Reparatur** | **plan-only**; ausführende Reparatur **an RT-2 gebunden und gesperrt** |
| **Fehlerklassen** | **24** mit Präfix **`KB04-`**, alle fail-closed |
| **Issue- und Exitcodes** | Wiederverwendung von `RUNTIME_START_BLOCKED` (4), `CONFIG_INVALID` (2), `USAGE_ERROR` (64) **ohne Überladung**; **zwei reservierte, nicht implementierte** Namen `FILESYSTEM_ENFORCEMENT_BLOCKED` (**15**) und `FILESYSTEM_MIGRATION_REQUIRED` (**16**). **RC-1 bis RC-10:** reine Contract-Reservierung, **kein Pfad emittiert sie**, **heutiges öffentliches Verhalten unverändert**, erneute Kollisionsprüfung vor B2, **keine stille Neunummerierung** |

**Ausdrücklich begründete Ausnahme — PP-3b:** Das committete
Profil-A-Bundle führt den Config-Bindmount mit `mode: 292`, also **`0444`**
(D-055). **Dieser Vertrag ändert das Bundle nicht** und schreibt keinen
abweichenden Wert vor, sondern **übernimmt und validiert** den vorgefundenen
Wert.

**PP-3b ist ein eng begrenztes Kompatibilitätsprofil** (Regeln 3b-1 bis
3b-16): es gilt **ausschließlich für PC-07**, ist **nicht auf andere
Pfadklassen übertragbar**, **kein allgemeines read-only Profil** und
**`0444`/`0555` ist kein sicherer Default** — der Grundzustand bleibt **kein
World-Zugriff**. Unter PP-3b sind **Secrets, Tokens, Passwörter, private
Schlüssel, Credential-Werte, konkrete lokale UID-/GID-Werte, konkrete lokale
Benutzer- oder Gruppennamen, vollständige Identitätsbindungen, sensible
Operator- und Deploymentwerte sowie private Hostpfade ausdrücklich
unzulässig**; ein solches Artefakt ist **nicht als PP-3b klassifizierbar**,
wird **nicht still in PC-07 übernommen** und endet ohne sichere
Alternativklassifikation **fail-closed**. **`world-writable` bleibt ausnahmslos
verboten**, und die Ausnahme **schwächt keine andere Profilklasse und keine
Invariante ab**. Eine spätere Verschärfung von PC-07 bleibt zulässig und
ist **kein Vertragsbruch**, sofern die erforderliche Runtime-Lesbarkeit erhalten
bleibt — sie wäre eine Bundle- und Deployment-Entscheidung in einem
**ausdrücklich autorisierten technischen Scope**.

### Validation Plan

**Zwölf positive** (`KB04-T-P01` bis `KB04-T-P12`) und **dreiunddreißig
negative** Testfälle (`KB04-T-N01` bis `KB04-T-N33`). Diese Kennungen sind
**vorläufige interne Testkennungen und ausdrücklich keine
Security-Test-IDs**; sie stehen in keinem Bezug zur NT-Nummerierung.

Enthalten ist die **vollständige PP-3b-Prüffolge** über alle vier
Dimensionen (`KB04-T-P12`) sowie **acht negative PP-3b-Fälle**
(`KB04-T-N26` bis `KB04-T-N33`): Secretmaterial im Artefakt · Verwendung
außerhalb PC-07 · nicht feststellbare Host-Quellrechte · read-only
Runtimesicht ohne positiv validierte Hostquelle · read-write Mount ·
veränderbares Artefakt · unerwartete Identität · Abweichung zwischen
Bundlemodus und tatsächlich sichtbarem Zustand. **Der Fixture-Fall zu
Secretmaterial verwendet einen synthetischen Marker, keinen Wert.**

**Synthetisch prüfbar:** Modell-, Zuordnungs-, Bindungs-, Ablehnungs- und
Fehlerklassenlogik. **Nur real prüfbar:** `KB04-T-N07` und `KB04-T-N08`
(**NT-04**), `KB04-T-N14` (**NT-05**), `KB04-T-N31`, `KB04-T-N33`, die
Dimension **D-I** in `KB04-T-P12` sowie jede Rechteauflistung vor und nach
dem Start — **Nachweisstufe 4, Profil-A-Instanz**.

**Kein Testfall wurde ausgeführt.** **NT-04 und NT-05 bleiben unausgeführt**
(0 von 32 Negativtests, 0 von 1 Positivtest). **SB-S04 bleibt nicht wirksam**,
**OD-37 bleibt offen** — der Vertrag **strukturiert** ihn, schließt ihn
aber nicht, weil OD-37 den Nachweis auf der Ziel-VM verlangt und ein Vertrag
kein Nachweis ist. **Beide Gates bleiben `NOT EVALUATED`.**

### B2-Kandidat — nicht autorisiert

| Teilphase | Möglicher Scope |
| --- | --- |
| **B2A** | Contract Model and Read-only Validator — **keine Deploymentmutation** |
| **B2B** | New-target Initialization Boundary — **kein Bestand, kein Reparaturmodus** |
| **B2C** | Synthetic Tests and Evidence — **keine reale Deploymentausführung** |
| **B2D** | Profile-A Deployment Integration — **späterer Kandidat** |

**Gesperrt:** produktive Reparatur · Migration bestehender Daten · RT-2
· reale Gatefreigabe · Control-Uplift · **Stage 2**.

**B2 darf PP-3b nur übernehmen**, wenn die vier Dimensionen **getrennt
validierbar** sind, die **Secretfreiheit vertraglich prüfbar** ist und **keine
Dimension still übersprungen** wird. Andernfalls gilt: **kein stiller
Fallback, kein bloßer Warnmodus, keine automatische Akzeptanz des
Bundlewerts** — **B2 stoppt mit einem klaren Blocker**, und eine Architektur-
oder Contract-Neubewertung wird erforderlich.

**B1C autorisiert keine dieser Teilphasen. B2 und C bleiben nicht autorisiert.**

### Stand nach B1C

**B0 complete** (`e4caa14`) · **B1A complete** (`1a7696d`) · **B1B
complete** (`b86a35f`) · **B1C complete** (dieser Stand, uncommitted) ·
**B2 nicht autorisiert** · **C nicht autorisiert** · **technische
Implementierung nicht autorisiert**.

**Unverändert:** **KB-04 bleibt `DOCUMENTED ONLY`**, alle zwölf Controls
`DOCUMENTED ONLY` — **keine Control-Hochstufung**; beide Gates
**`NOT EVALUATED`** — **keine Gateauswertung**; Capabilities **0 von 29**;
**NT-04 und NT-05 nicht ausgeführt**; **SB-S04 nicht wirksam**; **R-20
offen**; **OD-37 offen**; **R-33 18/21**; keine neue Risiko-ID; **RT-2 nicht
implementiert**; keine reale Bereitstellung; **CBP-WP-023 nicht registriert**.

**Ein implementierungsfähiger Vertrag ist keine Implementierung, und eine
geplante Prüfung ist kein Nachweis.**

---

## Phase B2A — Contract Model and Read-only Validator

**B1C-Commit:** `24de07e` — „CBP-WP-022: define KB-04 enforcement
contract and validation plan", **10 modifizierte Dateien und eine neue
Contract-Datei**.

B2A implementiert das interne, **read-only** Enforcement-Paket innerhalb von
**ADR-0014** und **D-060**. **Es entsteht keine neue öffentliche API, keine
CLI-Semantik, keine Config-Semantik und kein Deploymentmodell.**

### Exakte Dateien

| Pfad | Art | Verantwortung |
| --- | --- | --- |
| `core/core_brain/enforcement/__init__.py` | neu | Paketdoc, Negativabgrenzung, explizite Re-Exporte, vollständiges `__all__` |
| `core/core_brain/enforcement/contract.py` | neu | Teilmodell: PC-01…PC-11, PP-1…PP-4 mit PP-3a/PP-3b, zehn Akteure, D-I…D-IV, Selbstkonsistenz, Dokument- und Modellhash |
| `core/core_brain/enforcement/binding.py` | neu | Identitätsbindung, zehn Pflichtfelder, Kollisionsprüfung |
| `core/core_brain/enforcement/paths.py` | neu | Root-Boundary, Symlink, Hardlink, Objektart, TOCTOU-Grenze |
| `core/core_brain/enforcement/validator.py` | neu | Beobachtungsmodelle D-I…D-IV, read-only Prüfungen, PP-3b-Klassifikation |
| `core/core_brain/enforcement/aggregate.py` | neu | `FindingStatus`, `Finding`, `ValidationResult`, fail-closed Faltung |
| `core/core_brain/errors.py` | **additiv** | **21 `KB04-*`-ReasonCodes** + `FilesystemEnforcementError` — **keine ExitCode-Änderung** |
| `tests/kb04_fixtures.py` | neu | injizierbare Zustände, synthetischer Secretmarker |
| `tests/test_kb04_contract.py` | neu | Contract-Modell und Driftschutz |
| `tests/test_kb04_paths.py` | neu | Pfad-, Link- und Objektartprüfungen |
| `tests/test_kb04_validator.py` | neu | Bindung, vier Dimensionen, PP-3b, Herkunft |
| `tests/test_kb04_aggregate.py` | neu | Aggregation, operative Verifikation, Determinismus |

### API-Lock

**Enums:** `PathClass` (11) · `PermissionProfile` (5) · `ObjectKind` (5)
· `Actor` (10) · `Dimension` (4) · `MountMode` (5) ·
`ServiceRole` (7) · `ObservationOrigin` (3) · `ContentClassification`
(3) · `ValueOrigin` (4) · `ValidationState` (3) · `CollisionState`
(4) · `FindingStatus` (4).

**Dataclasses**, sämtlich `frozen=True, slots=True`, Mehrfachwerte nur als
Tupel: `ProfileSpec` · `PathClassSpec` · `IdentityBinding` ·
`PathResolution` · `HostObjectState` · `MountState` ·
`RuntimeObjectState` · `RuntimeIdentityState` · `Observation` ·
`Finding` (zusätzlich `order=True`) · `ValidationResult`.

**Funktionen:** `path_class_spec` · `profile_spec` · `validate_contract`
· `contract_model_sha256` · `normalize_document_bytes` ·
`validate_binding` · `validate_binding_set` · `resolve_within_root`
· `classify_object_kind` · `classify_link` · `detect_hardlink`
· `check_path` · `validate_observation` · `aggregate_findings`
· `canonical_json_bytes`.

**Keine Funktion mutiert.** Das Paket importiert ausschließlich aus der
Standardbibliothek, aus `core.core_brain.errors` und aus sich selbst; es wird
**nicht** in `core/core_brain/__init__.py` re-exportiert.

### Testumfang

**206 neue Tests** — Gesamtsuite **930 grün, 0 übersprungen**,
**ohne einen einzigen Plattformskip**. Symlinks, Hardlinks, FIFOs, Sockets und
Devices werden über **injizierte `stat`-Zustände** geprüft, nicht
über reale Objekte; damit laufen alle Fälle auch unter Windows ohne
Entwicklermodus und ohne Administratorrechte.

### Synthetische Grenze

Jede Beobachtung trägt eine **explizite Herkunft**: `SYNTHETIC`,
`DECLARED` oder `OBSERVED`. `ValidationResult.conform` bezeichnet die
**logische** Vertragskonformität; `operationally_verified` verlangt
zusätzlich, dass **alle vier Dimensionen** konform **und** durchgängig
`OBSERVED` sind. **Eine synthetische oder deklarierte Konformität erzeugt
sie niemals.**

### PP-3b-Grenze

PP-3b gilt **ausschließlich für PC-07** und ist im Modell als
`exclusive_path_class` verankert; `validate_contract()` weist jede
Verwendung außerhalb zurück. Die Inhaltsklassifikation ist
**deklarativ**: `SENSITIVE_OR_SECRET` ist eine **Verletzung**, `UNCLASSIFIED`
und eine **fehlende** Klassifikation sind **`INDETERMINATE`** — es gibt
**keinen Default auf secret-free**. **Keine Inhaltsanalyse, kein
Secret-Scanning, keine KB-08-Architektur.**

### Contract-Drift-Schutz

`CONTRACT_DOCUMENT_PATH` ist ein **relativer** Repositorypfad;
`CONTRACT_DOCUMENT_SHA256` ist der Hash der **zeilenendennormalisierten**
Dokumentfassung. Die Normalisierung ist zwingend, weil das Repository mit
`core.autocrlf` arbeitet und die Arbeitskopie unter Windows CRLF trägt,
der Commit-Blob aber LF — ohne sie wäre der Driftschutz
plattformabhängig. **Der Produktionscode liest das Dokument beim Import
nicht**; nur die Tests vergleichen. `contract_model_sha256()` sichert
zusätzlich das Teilmodell; ein geändertes Profil verändert den
Hash nachweislich.

### Keine operative Wirkung

**KB-04 bleibt `DOCUMENTED ONLY`.** Es ist kein Recht gesetzt, kein Besitz
zugewiesen, kein realer Mount geprüft, kein Test gegen eine Profil-A-Instanz
gelaufen. **NT-04 und NT-05 bleiben unausgeführt**, **SB-S04 nicht
wirksam**, **OD-37 offen**, beide Gates **`NOT EVALUATED`**, Capabilities
**0 von 29**, **RT-2 nicht implementiert**. Die Exitcodes **15** und **16**
bleiben **reine Vertragsreservierung** — **kein Pfad emittiert sie**, das
öffentliche CLI-Verhalten ist **unverändert**.

### Folgeschritte

**B2B** (New-target Initialization Boundary) · **B2C** (Synthetic Tests and
Evidence) · **B2D** (Profile-A Deployment Integration) — **sämtlich
nicht autorisiert**. **C** ist nicht autorisiert.

**Eine synthetisch festgestellte Konformität ist keine KB-04-Evidenz.**

---

## Aussageschutz

Dieses Work Package belegt auch nach Phase B2A **nicht**:

| Nicht belegt | Tatsächlicher Stand |
| --- | --- |
| KB-04 sei implementiert, getestet oder enforced | **`DOCUMENTED ONLY`** |
| Ein Security-Foundation-Test sei ausgeführt | **0 von 32** NT, **0 von 1** PT |
| Ein Gate sei ausgewertet | beide **`NOT EVALUATED`** |
| Eine Capability sei erreicht | **0 von 29** |
| Eine Bereitstellung existiere | **keine** |
| RT-2 existiere | **nicht implementiert** |
| Die spätere Umsetzung sei ADR-frei | **ADR-0014 angenommen** (D-059) — **keine Implementierungsfreigabe** |
| Eine Architekturentscheidung sei eine Sicherheitswirkung | **nein** — kein Recht gesetzt, kein Test gelaufen, kein Nachweis erbracht |
| Ein implementierungsfähiger Vertrag sei eine Implementierung | **nein** — D-060 autorisiert **B2B/B2C/B2D nicht**; die ausführende Reparatur bleibt an **RT-2** gebunden und gesperrt |
| Der implementierte Validator sei KB-04-Evidenz | **nein** — rein intern, read-only, **ausschließlich synthetisch nachgewiesen**; `operationally_verified` bleibt bei synthetischer oder deklarierter Herkunft **`False`** |

**Die Registrierung eines Work Packages ist keine Implementierungsfreigabe.**

**CBP-WP-023 ist nicht registriert und nicht autorisiert.**
