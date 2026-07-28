# Mapping Activation Gate Evaluator — Technische Evidenz (CBP-WP-016)

| Feld | Wert |
| --- | --- |
| **Status** | lokal ausgeführt · read-only · synthetic-only · nicht persistent |
| Grundlage | D-050 (A0), PILOT_MAPPING_ACTIVATION_GATE.md (A3) |
| Python | **3.13.14** (nur Standardbibliothek) |
| Stand | 2026-07-27 |

Alle Nachweise stammen aus tatsächlichen lokalen Läufen mit **synthetischen,
temporären** Daten. Keine reale Quelle, kein Pfad, keine URL, kein
Source-Inhalt, keine Persistenz.

---

## PYTHON-TECHNICAL

| # | Prüfung | Ergebnis |
| --- | --- | --- |
| 1 | `py -3.13 --version` | **Python 3.13.14** |
| 2 | `py -3.13 -m compileall core tests` | Exit 0 |
| 3 | `py -3.13 -m unittest discover -v` | **EXIT=0**, **Ran 398 tests**, **OK** |

Die **tatsächliche Testzahl** ist ausschließlich `Ran 398 tests` entnommen. Die
Basislinie von **315** (CBP-WP-015) bleibt grün; CBP-WP-016 fügt **+83**
additive Gate-Tests hinzu (398 > 315), davon der `mapping_id`-Fail-Closed-
Vertrag (B.2) als eigene Regressionsklasse.

## CLI-SMOKE (echte Subprozesse, erfasste Exitcodes)

Aufbau: synthetische temporäre Registry (`REGISTERED_DISABLED`), synthetischer
`VALID_DRAFT`, synthetisches Evidenz-Bundle mit korrekt gebundenen SHA-256-Hashes.

| Kommando | Exit | Beleg |
| --- | --- | --- |
| `source-mapping activation-evaluate` (menschenlesbar) | **14** | `evaluation_status: BLOCKED` |
| `source-mapping activation-evaluate --json` | **14** | kanonisches JSON, `"evaluation_status": "BLOCKED"` |
| `source-mapping activation-evaluate` (ohne `--synthetic-test-only`) | **14** | `GATE_SYNTHETIC_CONFIRMATION_MISSING` |
| `run --config config/runtime.example.toml` | **4** | unverändert |
| `source-mapping validate-draft` | 0 | unverändert (WP-015) |
| `source-mapping activation-check` | 13 | unverändert (WP-015) |

Belegte Kriterienverteilung im gültigen Fall: **16 Blocker** — 4 `SATISFIED`
(GATE-CRIT-02/03/13/14), 6 `DEPENDENCY_BLOCKED`, 3 `HUMAN_DECISION_REQUIRED`
(5/16/20), 5 `MISSING_EVIDENCE` (9/15/17/18/19), 2 `OUT_OF_SYNTHETIC_SCOPE`. Der
`gate_contract_sha256` ist
über Läufe stabil.

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

Der ausführbare Guard in `tests/test_cli.py` umfasst nun auch
`source-mapping activation-evaluate` (zusätzlich zu Kern-, Quarantäne-, Registry-
und Mapping-Pfaden).

> **Aussagegrenze (Wortlaut):** Während der ausgeführten Tests und lokalen
> CLI-Prüfungen wurde kein Netzwerkverbindungs- oder DNS-Versuch festgestellt.

Der Guard beweist **nicht** Deployment-Isolation, Firewallwirkung oder
Container-Netzgrenzen.

## Determinismus, Minimierung, Nichtpersistenz

Keine Uhr, kein Datum, kein Zufall; Code-Listen sortiert und dedupliziert;
Hashes über kanonische Darstellung; JSON mit sortierten Schlüsseln. Der Report
wird **nicht** gespeichert und besitzt ausschließlich **A6**-Autorität.

## Testgruppen

`tests/test_gate_models.py` (Vertrag/Status), `tests/test_gate_evidence.py`
(fail-closed Bundle), `tests/test_gate_evaluator.py` (reine Kernlogik + Report),
`tests/test_gate_service.py` (Bindung, read-only, Determinismus, `source_id`-
Leak-Schutz, `mapping_id`-Fail-Closed-Vertrag), `tests/test_gate_cli.py` (CLI,
`mapping_id`-Blockade ohne Echo, Nichtregression, Repo-unverändert); Erweiterung
von `tests/test_cli.py` (Netzwerk-Guard + Import-Probe). Fixtures:
`tests/gate_fixtures.py` (synthetisch, temporär).

## Verbleibende Blocker / Aussagegrenzen

**Nicht produktionsbereit.** Kein Gate ausgeführt, keine Aktivierung, kein
gespeichertes Ergebnis. **Mapping Activation Gate**, **Security Foundation
Readiness Gate** und **DRC** bleiben `NOT EVALUATED`; **0 von 29** Capabilities
`implemented`; Benchmark nicht ausgeführt.
