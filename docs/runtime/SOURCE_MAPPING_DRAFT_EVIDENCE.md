# Source Mapping Draft Validator — Technische Evidenz (CBP-WP-015)

| Feld | Wert |
| --- | --- |
| **Status** | lokal ausgeführt · read-only · synthetic-only |
| Grundlage | ADR-0012 (A1) |
| Python | **3.13.14** (nur Standardbibliothek) |
| Stand | 2026-07-27 |

Alle Nachweise stammen aus tatsächlichen lokalen Läufen mit **synthetischen,
temporären** Daten. Es wurde **keine** reale Quelle berührt, **kein** Pfad,
**keine** URL, **kein** Source-Inhalt verarbeitet und **nichts** gespeichert.

---

## PYTHON-TECHNICAL

| # | Prüfung | Ergebnis |
| --- | --- | --- |
| 1 | `python --version` | **Python 3.13.14**, Exit 0 |
| 2 | `python -m compileall core tests` | **COMPILEALL_OK**, Exit 0 |
| 3 | `python -m unittest discover -s tests -p "test_*.py"` | **Ran 315 tests … OK**, Exit 0 |

Die **tatsächliche Testzahl** ist ausschließlich `Ran 315 tests` entnommen —
**nicht** aus der Falltabelle des Work Packages summiert. Die Testbasislinie von
**212** Tests (CBP-WP-014) bleibt grün; CBP-WP-015 fügt die
Mapping-Testmodule additiv hinzu.

## CLI-SMOKE

Aufbau: eine **synthetische, temporäre** Registry wird per
`source-registry register` erzeugt (UTF-8 **ohne BOM**), danach werden die
Mapping-Kommandos gegen sie ausgeführt. `$LASTEXITCODE` wird unmittelbar nach
jedem nativen Befehl erfasst.

| # | Kommando | Exit | Beleg |
| --- | --- | --- | --- |
| 4 | `version` | 0 | `0.1.0.dev0` |
| 5 | Mapping-Policy read-only geladen | — | `config/source_mapping_validation_policy.example.toml` |
| 6 | `source-registry register` (synthetische Registry) | 0 | `source_id = src-b674ad09fc43569984e3991c` (ephemer) |
| 7 | synthetischer 31-Feld-Draft erzeugt | — | UTF-8 ohne BOM |
| 8 | `source-mapping validate-draft` (menschenlesbar) | **0** | `validation_status: VALID_DRAFT`, `present_field_count: 31`, `boundary_count: 1`, `reason_count: 0` |
| 9 | `source-mapping validate-draft --json` | **0** | kanonisches JSON (`sort_keys`), `"validation_status": "VALID_DRAFT"` |
| 10 | `source-mapping validate-draft` (blockierter Draft `enabled=true`) | **12** | `validation_status: BLOCKED`, `reason_codes: [MAP-ENABLED-TRUE]` |
| 11 | `source-mapping activation-check` | **13** | `SOURCE_MAPPING_ACTIVATION_BLOCKED MAPPING_ACTIVATION_ALWAYS_BLOCKED` (obwohl Validierung `VALID_DRAFT`) |
| 12 | `run --config config/runtime.example.toml` | **4** | `RUNTIME_START_BLOCKED` (unverändert) |

Belegte Hashes (deterministisch, kein Leak): gültiger Draft
`draft_sha256 = d37769e8b4aee608c3a19bd39b544e52540c251edb2c598f42accc9dc56e81d2`;
blockierter Draft
`draft_sha256 = aa5b91b9af237b880e9b49245466316b3527c6cfcc9fc4003b0b393b1962771c`;
`policy_sha256 = ff05d8abf79b88fd8b5aa6b3df3f14f323c1715db855ce43bd600232b14abc19`.

## POWERSHELL-CONTROL

| # | Prüfung | Ergebnis |
| --- | --- | --- |
| 13 | Registry-Bytes **vor** den Mapping-Befehlen gehasht (SHA-256 je Datei) | erfasst |
| 14 | Registry-Bytes **nach** den Mapping-Befehlen gehasht | erfasst |
| 15 | Byte-Gleichheit | **REGISTRY_BYTE_IDENTICAL=TRUE** |
| 16 | Keine Mapping- oder Reportdatei außerhalb der Registry erzeugt | **NO_MAPPING_OR_REPORT_FILE=TRUE** |
| 17/18 | Cleanup der temporären Daten in `finally` | **CLEANUP=TRUE** |
| 19 | Git-Inventar (`git status --porcelain`) | wie unten |
| 20 | Keine unerwarteten Dateien | bestätigt (nur Allow-List-Pfade) |

## Netzwerk-Guard

Der ausführbare Guard in `tests/test_cli.py` ersetzt
`socket.create_connection`, `socket.getaddrinfo`, `socket.socket.connect` und
`socket.socket.connect_ex` durch sofort scheiternde Funktionen und umfasst nun
auch **`source-mapping validate-draft`** und **`source-mapping
activation-check`** (zusätzlich zu den bestehenden Kern-, Quarantäne- und
Registry-Pfaden). Ein eigenständiger Guard-Test steht zusätzlich in
`tests/test_mapping_cli.py`.

> **Aussagegrenze (Wortlaut):** Während der ausgeführten Tests und lokalen
> CLI-Prüfungen wurde kein Netzwerkverbindungs- oder DNS-Versuch festgestellt.

Der Guard beweist **nicht** Deployment-Isolation, Firewallwirkung,
Container-Netzgrenzen oder allgemeine Systemnetzwerkfreiheit.

## Registry-Hash vor und nach · Cleanup

Vor und nach jedem Mapping-Smoke-Test wurden die Registry-Bytes gehasht; sie
waren **bytegenau identisch** (Kontrolle 15). Es entstand **keine** Mapping-,
Report-, Lock-, Record-, Event- oder Katalogdatei durch die Mapping-Kommandos
(Kontrolle 16). Alle temporären Daten wurden in `finally` entfernt
(Kontrolle 17/18).

## Pfad-, URL- und Inhaltsminimierung

Kein CLI-Pfad und kein Report gibt einen Eingabepfad, einen Registry-Pfad, eine
`source_reference`, einen Source-Inhalt oder eine URL aus. Getestet in
`tests/test_mapping_cli.py` (Fälle 97/98) und `tests/test_mapping_validator.py`
(Fälle 84–88).

## R-33-Korrektur

CBP-WP-015 dokumentiert **genau einen** neuen, datierten Konsistenzvorgang (den
neunten): die aktuellen A3-Planungsangaben nannten **19** Mapping-Felder,
während der angenommene A1/A2-Vertrag **31 Felddefinitionen** umfasst. Betroffen:
`docs/roadmap/PILOT_SOURCE_MAPPING_PLAN.md`,
`docs/roadmap/PHASE_1_EVIDENCE_PLAN.md`. Neue Basislinie: **neun
Konsistenzvorgänge in fünfzehn Work Packages**. **R-33 bleibt gemindert, nicht
geschlossen.**

## Verbleibende Blocker / Aussagegrenzen

**Nicht produktionsbereit.** Kein Mapping gespeichert, keine Source aktiviert,
keine Boundary aktiv, keine Collection, kein Index. **Mapping Activation Gate**,
**Security Foundation Readiness Gate** und **DRC** bleiben `NOT EVALUATED`;
Benchmark nicht ausgeführt; **0 von 29** Capabilities `implemented`.
