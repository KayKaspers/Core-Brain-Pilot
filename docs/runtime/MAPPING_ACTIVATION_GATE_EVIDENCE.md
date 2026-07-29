# Mapping Activation Gate Evaluator — Technische Evidenz (CBP-WP-016/017/018)

| Feld | Wert |
| --- | --- |
| **Status** | lokal ausgeführt · read-only · synthetic-only · nicht persistent |
| Grundlage | D-050, **D-051**, **D-052**, **D-053** (A0); **ADR-0013** (A1); PILOT_MAPPING_ACTIVATION_GATE.md (A3) |
| Python | **3.13.14** (nur Standardbibliothek) |
| Stand | 2026-07-29 (CBP-WP-018 Phase B1) |

Alle Nachweise stammen aus tatsächlichen lokalen Läufen mit **synthetischen,
temporären** Daten. Keine reale Quelle, kein Pfad, keine URL, kein
Source-Inhalt, keine Persistenz.

---

## PYTHON-TECHNICAL

| # | Prüfung | Ergebnis |
| --- | --- | --- |
| 1 | `py -3.13 --version` | **Python 3.13.14** |
| 2 | `py -3.13 -m compileall .` | **Exit 0** |
| 3 | `py -3.13 -m unittest discover -v` | **EXIT=0**, **Ran 558 tests**, **OK** |

Die **tatsächliche Testzahl** ist ausschließlich `Ran 558 tests` entnommen. Die
Basislinie von **451** (CBP-WP-017) bleibt grün; CBP-WP-018 fügt **+107**
additive Tests hinzu (558 > 451) — statischer Security Contract, Evidence-Schema
3.0, bedingtes `control_id`, Security-Artefakt-/Binding-Hash,
Invalid-/Stale-Abgrenzung, Mehrfachcontrols je Kriterium, Bindungskonflikte,
Binding-Zähler mit Summeninvariante, negative-evidence-only, Pure-Core-Faltung
sowie Report- und Leak-Schutz. Vorherige Basislinien: **398** (CBP-WP-016).

Der **Evidence-Vertrag 3.0** ist in
[SYNTHETIC_EVIDENCE_CONTRACT.md](SYNTHETIC_EVIDENCE_CONTRACT.md), der
**Security Contract 1.0** in
[SECURITY_FOUNDATION_READINESS_CONTRACT.md](SECURITY_FOUNDATION_READINESS_CONTRACT.md)
beschrieben.

## CLI-SMOKE (echte Subprozesse, erfasste Exitcodes)

Aufbau: synthetische temporäre Registry (`REGISTERED_DISABLED`), synthetischer
`VALID_DRAFT`, synthetisches Evidenz-Bundle **3.0** mit korrekt gebundenen
SHA-256-Hashes (ohne eingebettete Artefakte).

| Kommando | Exit | Beleg |
| --- | --- | --- |
| `source-mapping activation-evaluate` (menschenlesbar) | **14** | `evaluation_status: BLOCKED` |
| `source-mapping activation-evaluate --json` | **14** | kanonisches JSON, `"evaluation_status": "BLOCKED"` |
| `source-mapping activation-evaluate` (ohne `--synthetic-test-only`) | **14** | `GATE_SYNTHETIC_CONFIRMATION_MISSING` |
| `run --config config/runtime.example.toml` | **4** | unverändert |
| `source-mapping validate-draft --synthetic-test-only` | **0** | `validation_status: VALID_DRAFT`, unverändert (WP-015) |
| `source-mapping activation-check` | **13** | `MAPPING_ACTIVATION_ALWAYS_BLOCKED`, unverändert (WP-015) |

**Kein neuer CLI-Befehl, keine neue Option.** Der Exitcode-Vertrag ist
unverändert.

Belegte Kriterienverteilung im gültigen Fall: **16 Blocker** — 4 `SATISFIED`
(GATE-CRIT-02/03/13/14), 6 `DEPENDENCY_BLOCKED` (4/6/7/8/10/11), 3
`HUMAN_DECISION_REQUIRED` (5/16/20), 5 `MISSING_EVIDENCE` (9/15/17/18/19), 2
`OUT_OF_SYNTHETIC_SCOPE`. Der `gate_contract_sha256` ist über Läufe stabil und
gegenüber WP-017 **unverändert**; der `evidence_contract_sha256` ändert sich
mit dem 3.0-Deskriptor.

## Security-Contract-Bindungen im Report (belegt)

Im Bundle **ohne** Security-Control-Artefakte:

| Feld | Wert |
| --- | --- |
| `security_contract_revision` | `1.0` |
| `security_contract_sha256` | hex64, deterministisch |
| `documented_control_count` | **12** |
| `runtime_scoped_control_count` | **7** |
| `runtime_scoped_binding_count` | **11** |
| `missing_form_binding_count` | **11** |
| `valid`/`invalid`/`stale`/`conflicting_form_binding_count` | je **0** |
| `operationally_unevaluated_binding_count` | **11** |

Summeninvariante `valid + missing + invalid + stale + conflicting = 11`
eingehalten. Bei **elf gültigen** Formbindungen bleiben die Kriterien
4/6/7/8/10/11 `DEPENDENCY_BLOCKED`, Kriterium 5 `HUMAN_DECISION_REQUIRED` und
Kriterium 9 strukturell — **keine** positive Aufwertung.

## KONTROLLEN

| Prüfung | Ergebnis |
| --- | --- |
| Registry-Bytes vor/nach den Gate-Befehlen | **REGISTRY_BYTE_IDENTICAL = True** |
| Neue Dateien im Arbeitsbereich | **NO_NEW_FILE = True** (kein Report gespeichert) |
| Eingaben (Draft, Evidenz, Registry) nach der Auswertung | byte-/wertidentisch |
| Determinismus (zweifacher Lauf) | byte-identische Ausgabe |
| Report-/CLI-Leaks (Pfad, URL, `source_reference`, Inhalt) | keine |
| Forbidden-Status (`READY FOR`, `APPROVED FOR`, `REVOKED`) | im Report/JSON **nicht** vorhanden |

## Netzwerk-Guard

Der ausführbare Guard in `tests/test_cli.py` umfasst `source-mapping
activation-evaluate` (zusätzlich zu Kern-, Quarantäne-, Registry- und
Mapping-Pfaden) — seit CBP-WP-018 **einschließlich** des
Security-Control-Form-Pfads mit Mehrfachcontrols. Die Import-Probe deckt
`core.core_brain.gate.security_contract` mit ab.

> **Aussagegrenze (Wortlaut):** Während der ausgeführten Tests und lokalen
> CLI-Prüfungen wurde kein Netzwerkverbindungs- oder DNS-Versuch festgestellt.

Der Guard beweist **nicht** Deployment-Isolation, Firewallwirkung oder
Container-Netzgrenzen.

## Determinismus, Minimierung, Nichtpersistenz

Keine Uhr, kein Datum, kein Zufall; Code-Listen sortiert und dedupliziert;
Hashes über kanonische Darstellung; JSON mit sortierten Schlüsseln. Der Report
wird **nicht** gespeichert und besitzt ausschließlich **A6**-Autorität.

## Testgruppen

`tests/test_gate_models.py` (Vertrag/Status/Producer-Klassen),
`tests/test_gate_security_contract.py` (statischer Security Contract, Pure-Core,
Bindungen), `tests/test_gate_evidence.py` (fail-closed Bundle 3.0, bedingtes
`control_id`), `tests/test_gate_provenance.py` (Artefakt-/Binding-Hash,
per-Bindungs-Verdikte), `tests/test_gate_evaluator.py` (reine Kernlogik, rein
negative Faltung, Report), `tests/test_gate_service.py` (Bindung, elf
Formbindungen, Zähler/Invariante, read-only, Determinismus, `source_id`-
Leak-Schutz, `mapping_id`-Fail-Closed-Vertrag), `tests/test_gate_cli.py` (CLI,
`mapping_id`-Blockade ohne Echo, Nichtregression, Repo-unverändert); Erweiterung
von `tests/test_cli.py` (Netzwerk-Guard + Import-Probe). Fixtures:
`tests/gate_fixtures.py` (synthetisch, temporär).

## Verbleibende Blocker / Aussagegrenzen

**Nicht produktionsbereit.** Kein Gate ausgeführt, keine Aktivierung, kein
gespeichertes Ergebnis. **Keine reale Security-Evaluation** — die zwölf
KB-Kontrollen bleiben `DOCUMENTED ONLY`; die elf `(criterion, control_id)`-
Bindungen sind ausschließlich **synthetisch formgeprüft** und operativ
**unevaluiert**. **Mapping Activation Gate**, **Security Foundation Readiness
Gate** und **DRC** bleiben `NOT EVALUATED`; **0 von 29** Capabilities
`implemented`; Benchmark nicht ausgeführt.
