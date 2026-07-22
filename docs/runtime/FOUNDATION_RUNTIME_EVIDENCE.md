# Foundation Runtime — Technische Evidenz

| Feld | Wert |
| --- | --- |
| Erfasst in | CBP-WP-012 |
| Autoritätsklasse | A2 (technischer Nachweis) |
| Ausgeführt am | 2026-07-21 |
| Stand | 2026-07-22 (Nova-REWORK-Korrekturlauf: Netzwerk-Guard, 7er-Befehlsmatrix, Git-Inventar, 69 Tests) |

> **Alle Zahlen stammen aus dem tatsächlichen Lauf**, nicht aus einer früheren
> Zusammenfassung. Die Befehle sind reproduzierbar.

---

## Umgebung

| Feld | Wert |
| --- | --- |
| **Python-Version** | **3.13.14** (CPython) |
| **Interpreterpfad** | `C:\Users\KayKa\AppData\Local\Programs\Python\Python313\python.exe` |
| **Launcher** | `py -3.13` (PowerShell-kompatibel) |
| **Plattform** | `Windows-11-10.0.26200-SP0` |
| Externe Runtime-Abhängigkeiten | **keine** |
| Paketdownloads | **keine** |
| Globale Installationen | **keine** |

Ermittelt read-only:

```powershell
py -0p
py -3.13 -c "import sys, platform; print(sys.version.split()[0]); print(sys.executable); print(platform.platform())"
```

## 1 — Compile

```powershell
py -3.13 -m compileall core tests
```

**Ergebnis:** alle 14 Module kompiliert · `$LASTEXITCODE = 0`.

## 2 — Unit-Tests

```powershell
py -3.13 -m unittest discover -s tests -v
```

| Kennzahl | Wert |
| --- | --- |
| **Ausgeführte Tests** | **69** |
| **Bestanden** | **69** |
| **Fehlgeschlagen** | **0** |
| **Fehler** | **0** |
| **Übersprungen** | **0** |
| Laufzeit | ~0,19 s |
| `$LASTEXITCODE` | **0** |

> **Testzahl aus dem Lauf ausgezählt:** `Ran 69 tests ... OK`. Keine Zahl aus
> einer Spezifikation übernommen. Der Erstlauf hatte **67** Tests; der
> Nova-REWORK-Lauf ergänzte **2** Netzwerk-Guard-Tests (Abschnitt 8) →
> **69**. Das Work Package forderte mindestens die 24 nummerierten Fälle.

**Zwei Testdefekte im ersten Lauf gefunden und behoben** — beide in den Tests,
nicht im Code:

| Defekt | Ursache | Korrektur |
| --- | --- | --- |
| `test_missing_geteuid_is_not_applicable` | `mock.patch.object` ohne `create=True` scheitert auf Windows, wo `os.geteuid` fehlt | `create=True` ergänzt |
| `test_config_module_reads_neither_environ_nor_argv` | Grep fand die Wörter `os.environ`/`sys.argv` im **Docstring** | Prüfung auf `import os` / `import sys` umgestellt |

## Vollständige Befehlsmatrix

Alle **sieben** Prüfkommandos, Exitcode je Zeile über `$LASTEXITCODE` erfasst.
**Zwei technische Prüfkommandos** (TECH) und **fünf CLI-Smoke-Tests** (CLI).

| ID | Kategorie | Befehl | Erwartet | Tatsächlich | Ergebnis |
| --- | --- | --- | ---: | ---: | --- |
| 1 | **TECH-COMPILE** | `compileall core tests` | 0 | **0** | OK |
| 2 | **TECH-TEST** | `unittest discover -s tests` | 0 | **0** | OK |
| 3 | **CLI-SMOKE** | `version` | 0 | **0** | OK |
| 4 | **CLI-SMOKE** | `validate-config --config …example.toml` | 0 | **0** | OK |
| 5 | **CLI-SMOKE** | `doctor --config …` | 3 | **3** | OK |
| 6 | **CLI-SMOKE** | `doctor --config … --json` | 3 | **3** | OK |
| 7 | **CLI-SMOKE** | `run --config …` | 4 | **4** | OK |

> **Abgrenzung:** `compileall` und `unittest` sind **technische
> Prüfkommandos**, keine CLI-Smoke-Tests. Es gibt **genau fünf**
> CLI-Smoke-Tests (IDs 3–7). Alle sieben wurden ausgeführt; jeder Exitcode ist
> einzeln zugeordnet.

```powershell
py -3.13 -m core.core_brain version
py -3.13 -m core.core_brain validate-config --config config/runtime.example.toml
py -3.13 -m core.core_brain doctor --config config/runtime.example.toml
py -3.13 -m core.core_brain doctor --config config/runtime.example.toml --json
py -3.13 -m core.core_brain run --config config/runtime.example.toml
```

### Doctor-Ausgabe (menschenlesbar)

```text
runtime_mode:     skeleton
production_ready: false

checks:
  KB-01    NOT APPLICABLE  Nicht privilegierter Betrieb
  KB-02    PASS            Getrennte Service-Identitäten
  KB-03    PASS            Canonical Write verboten
  KB-06    PASS            Source-Aktivierung blockiert
  KB-08    PASS            Secret-Provider nicht angebunden
  KB-09    PASS            Operational Evidence nicht angebunden
  KB-10    PASS            Netzwerk-Egress deny-by-default
  RUNTIME  BLOCKED         Operativer Runtime-Start [SECURITY_GATE_NOT_ACCEPTED]

summary: pass=6 blocked=1 not_applicable=1
```

> **KB-01 `NOT APPLICABLE`** unter Windows ist **kein Deploymentnachweis**.
> **`PASS`** ist ein Skeleton-Ergebnis; keine KB-Kontrolle gilt als
> durchgesetzt.

## Determinismus

| Prüfung | Ergebnis |
| --- | --- |
| `doctor` fünffach ausgeführt | **identische** Ausgabe (`test_doctor_is_deterministic`) |
| `doctor --json` fünffach | **eine** eindeutige Ausgabe (`test_doctor_json_is_deterministic`) |
| `run` dreifach | identisch (`test_run_is_deterministic`) |
| Prüfreihenfolge | stabil: KB-01, KB-02, KB-03, KB-06, KB-08, KB-09, KB-10, RUNTIME |

## JSON-Validität

Die JSON-Ausgabe beginnt mit Byte **123** (`{`), **ohne BOM**. Über eine Datei
belegt (kein PowerShell-Pipe-Artefakt):

```powershell
$tmp = Join-Path $env:TEMP "cbp_doctor.json"
Start-Process py -ArgumentList "-3.13","-m","core.core_brain","doctor",`
  "--config","config/runtime.example.toml","--json" `
  -NoNewWindow -Wait -RedirectStandardOutput $tmp
py -3.13 -c "import json,pathlib; d=json.loads(pathlib.Path(r'$tmp').read_text(encoding='utf-8')); print(d['production_ready'], d['summary'])"
```

**Ergebnis:** `JSON OK: production_ready=False blocked=1 pass=6`. Erste 3 Bytes
`123 13 10` — kein `EF BB BF`.

> **Hinweis:** Ein direktes `| py …` in PowerShell fügt zwischen zwei nativen
> Prozessen einen UTF-8-BOM ein. Das ist ein Pipe-Artefakt der Shell, **kein**
> Fehler der CLI. Der In-Process-Test `test_doctor_json_is_valid_json` parst
> die Ausgabe erfolgreich mit `json.loads`.

## Erzeugte Runtime-Daten

**Keine.** Belegt durch:

- `test_run_creates_no_runtime_files` — `run` legt in einem temporären
  Arbeitsverzeichnis keine Datei an;
- `test_run_creates_no_files_in_repository` — kein neuer Repository-Eintrag;
- `test_importing_package_produces_no_output_and_no_files` — der Import in
  einem Subprozess erzeugt keine Datei und keine Ausgabe.

Die einzigen automatisch erzeugten Dateien sind `__pycache__/*.pyc` aus
`compileall` und dem Testlauf — durch `.gitignore` ausgeschlossen.

## 8 — Netzwerkfreiheit: statisch und ausführbar

### Statisch

| Prüfung | Ergebnis |
| --- | --- |
| Suche nach `import socket`/`urllib`/`http`/`requests` in `core/core_brain/*.py` | **kein Treffer** |
| `test_ports_module_has_no_network_or_file_access` | bestanden |
| Kein Egress-Port gibt `True` zurück | bestanden |

### Ausführbarer Netzwerk-Guard *(Nova-REWORK ergänzt)*

`tests/test_cli.py::TestNetworkGuard` (zwei Tests) ersetzt in-process die
zentralen Socket-Einstiegspunkte durch Funktionen, die den Test **sofort
scheitern lassen**, und führt darunter **jeden der fünf CLI-Pfade** aus.

| Gesperrte Funktion | Verhalten bei Aufruf |
| --- | --- |
| `socket.create_connection` | löst `_NetworkAttempt` aus → Test scheitert |
| `socket.socket.connect` | dito |
| `socket.socket.connect_ex` | dito |
| `socket.getaddrinfo` | dito (deckt DNS-Auflösung ab) |

| Geprüfter CLI-Pfad | Ergebnis |
| --- | --- |
| `version` | kein Netzwerk-/DNS-Versuch |
| `validate-config` | kein Netzwerk-/DNS-Versuch |
| `doctor` | kein Netzwerk-/DNS-Versuch |
| `doctor --json` | kein Netzwerk-/DNS-Versuch |
| `run` | kein Netzwerk-/DNS-Versuch |

Eine **Gegenprobe** (`test_guard_itself_triggers_on_a_real_attempt`) belegt,
dass der Guard einen tatsächlichen `create_connection`-Versuch erkennt — der
Nachweis ist also nicht durch einen wirkungslosen Patch erschlichen.

**Kein echter Netzwerkzugriff, kein Listener, kein DNS-Aufruf, kein
Testserver, keine externe Adresse, keine Firewalländerung, keine
Abhängigkeit.**

> **Aussagegrenze.** Der Guard beweist ausschließlich: *Während dieser fünf
> geprüften lokalen CLI-Pfade wurde in-process kein Netzwerkverbindungs- oder
> DNS-Versuch festgestellt.* Er beweist **nicht** Deployment-Isolation,
> Firewallwirkung, Container-Netzgrenzen, VM-Egress-Kontrolle oder allgemeine
> Systemnetzwerkfreiheit.

## Dateisystemprüfung — Git-Inventar

Kanonische Quelle: `git status --porcelain=v1 -uall`.

| Git-Status | Anzahl |
| --- | ---: |
| Modifizierte getrackte Dateien (` M`) | **13** |
| Neue ungetrackte Dateien (`??`) | **21** |
| Gelöschte Dateien | 0 |
| Umbenannte Dateien | 0 |
| **Gesamtzahl eindeutiger Dateipfade** | **34** |

**Summenprüfung:** 13 + 21 + 0 + 0 = **34** = eindeutige Pfade. Alle 21 neuen
Dateien decken sich **exakt** mit der Erlaubnisliste des Work Packages — keine
außerhalb, keine fehlend.

| Prüfung | Ergebnis |
| --- | --- |
| Neue Pfade nur in `core/`, `config/`, `examples/`, `tests/`, `docs/runtime/`, `pyproject.toml`, `work-packages/CBP-WP-012.md` | bestätigt |
| Kein bestehender Ordner verschoben | bestätigt |
| Kein Operator-Workspace angelegt | bestätigt |
| Kein Runtime-Datenbereich mit realen Daten | bestätigt |
| `docs/runtime/` **nicht** ignoriert (`git check-ignore` → kein Treffer) | bestätigt |
| `__pycache__` weiterhin ignoriert (`.gitignore:106`) | bestätigt |
| Wurzelbezogener `/runtime/`-Datenbereich weiterhin ignoriert | bestätigt |

> **`.gitignore` ist eine Vorsichtsmaßnahme, keine Sicherheitsgrenze** (ADR-0007,
> G3). Ein im REWORK entdeckter zu breiter Eintrag `runtime/` hätte
> `docs/runtime/` versehentlich ausgeblendet; er ist auf `/runtime/`
> wurzel-verankert.

## Pyproject — strukturelle Prüfung

`pyproject.toml` ist **nicht leer**; die Metadaten sind vorhanden. Über
`tomllib` ausgelesen:

| Feld | Wert |
| --- | --- |
| `project.name` | `core-brain-pilot` |
| `project.version` | `0.1.0.dev0` |
| `project.requires-python` | `>=3.13` |
| `project.dependencies` | `[]` — **keine Runtime-Abhängigkeit** |
| `project.optional-dependencies` | `{dev = []}` — **keine Development-Abhängigkeit** |
| `[build-system]` | **nicht vorhanden** — kein Build, kein Backend |
| `[project.urls]`, `[project.scripts]` | **nicht vorhanden** |
| Veröffentlichungskonfiguration | **keine** |
| Zugangsdaten, private Pfade | **keine** |
| `tool.core-brain-pilot` | `status = "internal prototype"`, `production_ready = false` |

**Kein Paketdownload, keine globale Installation, keine Paketinstallation für
die lokalen Tests.**

## Verbleibende Blocker

| Blocker | Zuständig |
| --- | --- |
| KB-01 bis KB-12 nicht durchgesetzt | CBP-WP-012+ auf der Ziel-VM |
| Security Foundation Readiness Gate `NOT EVALUATED` | nach Umsetzung von KB-01…KB-12 |
| Mapping Activation Gate `NOT EVALUATED` | nach CBP-WP-010-Aktivierung |
| DRC `NOT EVALUATED` | Deployment-Werte offen |
| Konkrete Deploymentwerte (UID/GID, Hostpfade, Ports) | Deployment Required |

## Reproduktion

Vollständige Befehlsfolge in
[DEVELOPER_RUNBOOK.md](DEVELOPER_RUNBOOK.md).
