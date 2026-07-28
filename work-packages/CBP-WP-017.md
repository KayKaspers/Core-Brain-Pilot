# CBP-WP-017 — Synthetic Evidence Contract & Provenance Foundation

| Feld | Wert |
| --- | --- |
| **ID** | CBP-WP-017 |
| **Titel** | Synthetic Evidence Contract & Provenance Foundation |
| **Typ** | implementation |
| **NDF Prompt Mode** | Full |
| **Context Budget** | B2 – Standard |
| **Modell / Effort** | Claude Opus 4.8 (`claude-opus-4-8`) / ultracode |
| **Status** | **in-review** |
| **Grundlage** | D-051 (A0); ADR-0007 (RT-1/RT-2/RT-3), ADR-0009 (Evidence-Policy); WP-016-Gate-Evaluator |
| **Stand** | 2026-07-28 |

---

## Phase A — Architektur- und Governance-Review

Phase A war vollständig read-only. Sie rekonstruierte den WP-016-Evidenzvertrag
(Schema 1.0: `criterion_evidence` = 20 Einträge `{criterion, evidence_ref}`,
`evidence_ref` reine Provenienz, `INVALID_/STALE_/CONFLICTING_EVIDENCE` nie
erzeugt), verglich drei Architekturvarianten und empfahl **Variante B**
(eingebettete strukturierte Artefakte), **negative-evidence integration only**,
**Schema 2.0 mit 1.0 fail-closed**, minimal erweiterten Report und `ADR_UNCLEAR`
(A0 zu schließen).

## Human Authorization (D-051)

**APPROVE CBP-WP-017 IMPLEMENTATION WITH NOTES** (A0): **A2** Bundle mit
eingebetteten strukturierten Artefakten; **B1** negative-evidence integration
only; **C2** Evidence Schema 2.0, Schema 1.0 fail-closed; **D1**
`ADR_NOT_REQUIRED` unter Scope Lock; **E2** minimal erweiterter A6-Report.

## Ziel · Scope · Out of Scope

**Ziel:** ein geschlossener, deterministischer, **synthetic-only** Evidence-
Vertrag 2.0 mit eingebetteten Artefakten, Provenance-/Revisionsbindung und
deterministischer **Invalid-/Stale-/Conflict-Erkennung**, der über den
bestehenden `activation-evaluate --evidence`-Pfad **rein negativ** in den Gate-
Evaluator einfließt.

**Scope:** Evidence-Schema 2.0, Provenance-/Binding-/Artefakt-Hashes,
Verdiktlogik, negative Faltung, minimal erweiterter Report, Tests, Doku.

**Out of Scope:** reale/operative Evidenz, Evidence-Promotion, Aktivierung,
Gatefreigabe, Gate-Statusmutation, positive Gate-Erfüllung, Persistenz, RT-2,
Netzwerk, Secrets, DRC-/Security-Foundation-Evaluation, neuer CLI-Befehl,
separate Artefaktdateien, CBP-WP-018.

## Architektur

`core/core_brain/gate/`: **neues** `provenance.py` (reine kanonische Artefakt-/
Binding-Hashes + rein negatives Kriteriumsverdikt), erweitertes `evidence.py`
(Schema-2.0-Loader mit eingebetteten Artefakten, fail-closed), `evaluator.py`
(negative Faltung, Docstring-Korrektur, 6 Reportfelder), `service.py`
(Orchestrierung: erwartete Bindung je Kriterium, Verdikt, Zähler), `models.py`
(`EVIDENCE_SCHEMA_VERSION="2.0"`, `EVIDENCE_CONTRACT_REVISION="2.0"`,
Producer-Klassen, Kriterienzuordnung, Limits, `GATE-EVID-*`-Codes,
`evidence_contract_sha256()`, erweiterter Report). `evaluator.py` bleibt **pure
core**; Datei-I/O ausschließlich im Loader/Service. `errors.py` unverändert.

## Evidence-Schema 2.0

Geschlossenes Bundle (11 Top-Level-Felder). `criterion_evidence` = 20 Einträge
`{criterion, artifacts}` (feste Reihenfolge 1..20). Artefakt (6 geschlossene
Felder): `artifact_id` (`\Aart-[0-9a-f]{24}\Z`, opak, reportsicher),
`artifact_sha256` (Hash der kanonischen Artefaktbeschreibung **ohne**
`artifact_sha256`), `binding_sha256` (Hash der 11-teiligen Kriteriumsbindung),
`producer_class` (geschlossenes Enum), `evidence_revision` (int ≥ 1),
`synthetic_test_only` (true). Limits: **4** Artefakte je Kriterium, **80**
gesamt, **131072 B** Dateigröße. **Schema 1.0 fail-closed** (`GATE_EVIDENCE_
SCHEMA_UNSUPPORTED`); keine Migration (keine persistierte 1.0-Evidenz).

## Producer-Klassen · Autoritätsgrenzen

`structural-form` (1,2,3,12,13,14), `foundation-form` (4–11),
`operator-review-form` (15), `rt2-audit-form` (17), `backup-form` (18),
`rollback-form` (19), `human-decision-form` (16,20). **Note:**
`human-decision-form` schließt die von §8 offengelassene Zuordnung für die
reinen Human-Entscheidungen 16/20 (nur **Formvalidierung**, nie Erfüllung); 5
bleibt `foundation-form`. **Synthetische Artefakte erfüllen 5/16/20 nie**
(bleiben `HUMAN_DECISION_REQUIRED`); 15/18/19 bleiben operative
`MISSING_EVIDENCE`. Negative Faltung: `INVALID/CONFLICTING/STALE` überschreiben
negativ; `VALID_FORM`/kein Artefakt lassen das Basisergebnis unverändert; **kein
positives Upgrade**.

## Invalid · Conflict · Stale

**INVALID** (Integrität `artifact_sha256` falsch, oder Producer-Klasse nicht
zulässig). **CONFLICTING** (≥2 eindeutige Artefakte je Kriterium, oder gleiche
`artifact_id` mit anderem Hash; identische dedupliziert; **keine** automatische
Auflösung). **STALE** (wohlgeformt, aber `binding_sha256` ≠ aktueller Snapshot
oder `evidence_revision` ≠ Bundle — **ohne Uhr**). Priorität **INVALID >
CONFLICTING > STALE > Basisergebnis**. Reason-Codes `GATE-EVID-INVALID-HASH/
-PRODUCER-CLASS`, `-CONFLICT-ARTIFACT-ID/-HASH`, `-STALE-BINDING/
-EVIDENCE-REVISION` (stabil, sortiert, keine Rohdaten/IDs). `BIND_EVIDENCE_
REVISION_INVALID` bleibt als **Kompatibilitätskonstante**.

## Report · CLI · Exitcodes

Report minimal erweitert um `evidence_contract_revision`,
`evidence_contract_sha256` und `validated_/invalid_/stale_/conflicting_
artifact_count` (deduplizierte Zähler; **keine** Artefakt-ID/Rohartefakte/
Producer-Personen/Pfade/Zeitstempel; reine A6-Diagnose, keine Freigabewirkung).
CLI `source-mapping activation-evaluate --evidence` unverändert; Exitcode **14**;
`activation-check` bleibt **13**. GateStatus unverändert (`NOT_EVALUATED`/
`BLOCKED`).

## Tests · Evidenz

`tests/test_gate_provenance.py` (neu) + Erweiterungen in `test_gate_evidence/
models/service/cli.py`, `gate_fixtures.py`, `test_cli.py` (Netzwerk-Guard +
Import-Probe). **Ran 451 tests … OK** (Basislinie 398, +53), compileall grün.
Registry/Eingaben byte-identisch; nicht persistent; deterministisch; leak-frei;
Forbidden-Status abwesend.

## Akzeptanzkriterien

D-051 (A2/B1/C2/D1/E2) umgesetzt; Schema 2.0 geschlossen, 1.0 fail-closed;
deterministische Canonical-JSON/Hashes; Provenance-/Revisionsbindung;
Invalid-/Stale-/Conflict deterministisch belegt; keine stille Konfliktauflösung;
5/15/16/18/19/20 nie positiv erfüllt; keine reale Source/Persistenz/RT-2/
Gatefreigabe; GateStatus/Exitcodes/`activation-check` unverändert; Testsuite grün
(451 > 398). **Alle erfüllt.**

## Rückmeldung an Nova

Implementierung abgeschlossen, **in-review**. Kein Commit, kein Push (Commit-
Autorität beim Human Maintainer). Kein nächstes Work Package vorgeschlagen
(CBP-WP-018 ausdrücklich nicht Bestandteil).
