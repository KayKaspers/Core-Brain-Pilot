# CBP-WP-016 — Deterministic Mapping Activation Gate Evaluator

| Feld | Wert |
| --- | --- |
| **ID** | CBP-WP-016 |
| **Titel** | Deterministic Mapping Activation Gate Evaluator |
| **Typ** | implementation, interactive authorization |
| **NDF Prompt Mode** | Full |
| **Context Budget** | B2 – Standard |
| **Modell / Effort** | Claude Opus 4.8 (`claude-opus-4-8`) / ultracode |
| **Status** | **in-review** |
| **Grundlage** | D-050 (A0); PILOT_MAPPING_ACTIVATION_GATE.md (A3); ADR-0007/0008/0009/0012 |
| **Stand** | 2026-07-27 |

---

## Phase A / A.1 — Reconciliation

Phase A wurde dreimal read-only ausgeführt und zweimal wegen behobener Git-/
Register-Statusabweichungen (R-33, zehnter und elfter Vorgang) angehalten. Die
gezielte **Phase A.1** klärte vier interne Widersprüche des ersten Laufs:
(1) Human-only-Taxonomie (Nachweisstufe-6-Punkte 16/20 vs. vier menschliche
Entscheidungen 5/16/20 sowie bedingt 8, plus Human-Evidenz 15); (2) READY-/
APPROVED-Semantik (der synthetische MVP kann `READY FOR ACTIVATION DECISION`
**nie** emittieren, da gültige A0-Approval-Evidenz fehlt); (3) Autoritätsklassen
(Gate-Doc A3, Human-Entscheidungen A0, Evaluatorreport A6); (4) vollständige
41-Precondition-Matrix. Feasibility: **PASS WITH NOTES**.

## Human Authorization (D-050)

**APPROVE WP-016 IMPLEMENTATION WITH NOTES** (A0), **A1** (synthetisches
Eingabe-/Evidenzmodell), **B1 – eng** (Ausgabestatus nur `NOT_EVALUATED`/
`BLOCKED`; `READY FOR ACTIVATION DECISION`/`APPROVED FOR ACTIVATION`/`REVOKED`
nicht emittierbar), **C1** (fehlende/veraltete/NOT-EVALUATED/widersprüchliche
Abhängigkeiten blockieren fail-closed; Human-only nie automatisch erfüllt),
**D1** (deterministischer, minimierter, nicht persistierter A6-Report).

## Ziel · Scope · Out of Scope

**Ziel:** lokaler, synthetisch testbarer, read-only, nicht persistenter,
fail-closed Evaluator der **Review-Bereitschaft** eines
Mapping-Activation-Gate-Kandidaten anhand der **20 kanonischen Gate-Kriterien**.

**Scope:** Kriterienvertrag (20, feste Ordnung), geschlossenes Evidenz-Bundle,
reine Kernbewertung, read-only Registry-/Draft-Bindung (Wiederverwendung
WP-014/WP-015), deterministischer A6-Report, CLI, Tests, Evidenz, Doku.

**Out of Scope:** Gate-Ausführung/-Freigabe/-Statusmutation, `APPROVED FOR
ACTIVATION`, `REVOKED`, Mapping-/Source-/Boundary-Aktivierung, reale Sources/
Locators, Source-Inhaltszugriff, Registry-/Mapping-Schreibzugriff, Persistenz,
Netzwerk, Secret-Auflösung, RT-2, DRC-Ausführung/-Freigabe,
Security-Foundation-Freigabe, CBP-WP-017.

## Architektur

`core/core_brain/gate/`: `models.py` (20-Kriterien-Vertrag, `GateStatus`,
`CriterionResult`, `GateReasonCode`, `GateEvaluationReport`,
`gate_contract_sha256`), `evidence.py` (geschlossenes Bundle, fail-closed
Loader), `evaluator.py` (**reine** Kernlogik: keine I/O, keine Uhr, kein
Zufall), `service.py` (read-only Orchestrierung), `__init__.py`. Wiederverwendet:
`mapping.run_validate`, `mapping.service._read_registry_record`,
`mapping.parser`/`validator`. `errors.py`: Exitcode **14**
(`MAPPING_GATE_EVALUATION_BLOCKED`), `GateEvidenceError`, `GateEvaluationBlocked`,
`GATE_EVIDENCE_*`-Reason-Codes.

## Gate-Kriterien, Status, Human-only, Abhängigkeiten

**20 Kriterien** in fester Reihenfolge 1..20; Security Foundation/DRC sind
**keine** Kriterien 21/22. Ausgabestatus **nur** `NOT_EVALUATED`/`BLOCKED`.
Ausschließlich menschliche Entscheidungen (nie synthetisch erfüllt): **5, 16,
20** (`HUMAN_DECISION_REQUIRED`); Kriterium **15** (Operator Review) ist
menschlich erzeugte operative Evidenz (`MISSING_EVIDENCE`), keine Gate-
Entscheidung. Foundation-abhängig
(Stufe 4): 4, 6, 7, 8, 10, 11. Details in
[MAPPING_ACTIVATION_GATE_EVALUATOR.md](../docs/runtime/MAPPING_ACTIVATION_GATE_EVALUATOR.md).

## Eingabemodell · mapping_id · Report

Geschlossenes, versioniertes Evidenz-Bundle mit Hash-Bindung (Draft, Policy,
Registry-Record), `source_id`/`mapping_id`/`gate_contract_revision`/
`evidence_revision`, geschlossene 20-Kriterien-Evidenzliste. `mapping_id` ist
**Pflichtfeld**, nur **gelesen und validiert**, nie berechnet/normalisiert/
ersetzt/auf `null` redigiert; eine fehlende, ungültige oder nicht
report-sichere `mapping_id` **blockiert fail-closed vor der Reporterzeugung**
(Exit 14, kein Report, kein Echo). Report deterministisch, minimiert, nicht
persistent, **A6**; feste Nichtautorisierungssemantik.

## CLI · Exitcodes

`source-mapping activation-evaluate` (neu). `activation-check` (WP-015) bleibt
unverändert. Exitcode **14** kollisionsfrei mit 0–13, 64, 70; Policyfehler **2**.
Der MVP-Evaluationspfad endet **immer** `BLOCKED` (Exit 14).

## Tests · Evidenz

Sechs neue Testdateien + `gate_fixtures.py`; Erweiterung `test_cli.py`
(Netzwerk-Guard, Import-Probe). **Ran 398 tests … OK** (Basislinie 315 bleibt
grün, +83; inkl. `mapping_id`-Fail-Closed-Vertrag B.2). Registry vor/nach
byte-identisch; keine neue Datei; deterministisch; leak-frei; Forbidden-Status
abwesend. Vollständige Evidenz:
[MAPPING_ACTIVATION_GATE_EVIDENCE.md](../docs/runtime/MAPPING_ACTIVATION_GATE_EVIDENCE.md);
PowerShell-Ablauf:
[MAPPING_ACTIVATION_GATE_RUNBOOK.md](../docs/runtime/MAPPING_ACTIVATION_GATE_RUNBOOK.md).

## Stop-Bedingungen (eingehalten)

Keine ausgelöst: HEAD `0b2360c` vor Beginn, sauberer Baum, exakt 20 Kriterien,
kein Kriterium 21/22, Ausgabestatus nur `NOT_EVALUATED`/`BLOCKED`, kein READY/
APPROVED/REVOKED emittiert, keine Aktivierung, keine Persistenz, kein Registry-/
Mapping-Schreibzugriff, keine reale Source/Pfad/URL, kein Source-Inhaltszugriff,
kein Netzwerk, kein Secret, kein RT-2, kein DRC, keine Security-Foundation-
Freigabe, keine externe Abhängigkeit, kein Testfehler, kein Commit/Push.

## Akzeptanzkriterien

D-050 (A1/B1-eng/C1/D1) umgesetzt; 20 Kriterien in fester Ordnung; Status nur
`NOT_EVALUATED`/`BLOCKED`; `READY`/`APPROVED`/`REVOKED` nicht emittierbar;
Human-only 5/16/20 nie erfüllt, 15 als operative Evidenz `MISSING_EVIDENCE`; Security/DRC keine Zusatzkriterien;
deterministischer, nicht persistenter A6-Report; read-only Bindung; Registry
byte-identisch; Testsuite grün (398 > 315); keine Gate-/Produktionsreife
vorgetäuscht. **Alle erfüllt.**

## Rückmeldung an Nova

Implementierung abgeschlossen, **in-review**. Kein Commit, kein Push
(Commit-Autorität beim Human Maintainer). Kein nächstes Work Package
vorgeschlagen (CBP-WP-017 ausdrücklich nicht Bestandteil).
