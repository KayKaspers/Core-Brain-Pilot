# CBP-WP-012 — Foundation Runtime Skeleton

| Feld | Wert |
| --- | --- |
| ID | CBP-WP-012 |
| Titel | Foundation Runtime Skeleton |
| Typ | **implementation**, interactive authorization |
| Prompt Mode | **Full** (NDF v1.0.0) |
| Context Budget | **B2 – Standard** |
| Claude Code Model | **Claude Opus 4.8** (`claude-opus-4-8`) |
| Claude Code Effort | **ultracode** — im Profil deklariert |
| Phase | Phase 1 – erste technische Umsetzung |
| Ausgeführt am | 2026-07-21 |
| Ablauf | **interaktiv**, zwei Phasen |
| Status | `in-review` |
| Autoritätsklasse | A2 |

> **Erstes Work Package mit technischer Wirkung.** Es entsteht ausführbarer,
> getesteter Code — ein lokaler, fail-closed Skeleton **ohne** operative
> Wirkung. Keine Kontrolle KB-01 bis KB-12 wird durchgesetzt.
>
> **Anmerkung zum Ausführungsprofil:** `ultracode` steht im Work Package; es
> wurde **keine Multi-Agent-Orchestrierung gestartet**. Code, Tests und
> Dokumentation entstanden in einem Durchgang und wurden als ein Fundament
> verifiziert.

---

## Human-Autorisierung

| Feld | Wert |
| --- | --- |
| Entscheidung | **APPROVE WP-012 IMPLEMENTATION WITH NOTES** |
| Autorität | **A0** |
| Datum | 2026-07-21 |

**Kern der Notes (unverändert übernommen):** Autorisierung ausschließlich für
den lokalen, additiven, fail-closed Skeleton. **Phase B erst nach lokalem
Nachweis von Python ≥ 3.13.** Keine Installation, keine globale Installation,
kein Paketdownload, keine Abhängigkeiten durch Claude. `run` verweigert
deterministisch und erzeugt keine Runtime-Daten. Nicht autorisiert: produktiver
Betrieb, Deployment, Docker, HTTP-API, Web UI, Source Mapping, Ingest,
Retrieval, Indexierung, Secret-Auflösung, Netzwerkzugriff, RT-2-Speicherung,
Zugriff auf reale Quellen, Ausführung von Gates.

| Teil | Entscheidung |
| --- | --- |
| **A — Runtime-Stack** | **SELECT A1** — Python 3.13+, ausschließlich Standardbibliothek |
| **B — Ausführungsoberfläche** | **SELECT B1** — ausschließlich lokale CLI |
| **C — Additive Zielstruktur** | **SELECT C1** — `core/`, `config/`, `examples/`, `tests/` additiv, nichts verschieben |

**Tooling-Blocker in Phase A gemeldet** (nur Python 3.12 vorhanden), vom Human
Maintainer außerhalb dieses Work Packages aufgelöst. Phase B begann erst nach
Nachweis von **Python 3.13.14**.

## Ziel

Ein minimaler, ausführbarer, fail-closed Foundation Runtime Skeleton, der die
Grundsätze aus ADR-0009 als getesteten Code belegt — additive Struktur, lokale
CLI, strikte Konfigurationsvalidierung, Sicherheits-Doctor, verweigernde Ports,
fail-closed `run`.

## Scope

- Additive Struktur `core/`, `config/`, `examples/`, `tests/`, `docs/runtime/`
- Python-Projekt ohne Abhängigkeiten (`requires-python >=3.13`)
- CLI: `version`, `validate-config`, `doctor`, `doctor --json`, `run`
- Strikte, deterministische Konfigurationsvalidierung
- Reine fail-closed Policies und vier verweigernde Default-Ports
- Synthetische Beispielkonfiguration
- Automatisierte lokale Tests, technische Evidenz

## Out of Scope

Source Mapping · Ingest · Retrieval · Indexierung · Secret-Auflösung ·
Netzwerkzugriff · RT-2-Speicherung · API/Web UI · Container/VM-Deployment ·
Durchsetzung von KB-01…KB-12 · Ausführung eines Gates · Commit · Push.

## Architektur

Neun Runtime-Module unter `core/core_brain/`, streng geschichtet:
`errors` → `models` → (`config`, `policies`, `ports`) → `cli`. **Kein Modul hat
Import-Nebenwirkungen.** Kein `eval`, kein `exec`, kein `shell=True`, kein
`__import__`, kein Netzwerk-Import.

## Erstellte Komponenten

| Datei | Rolle |
| --- | --- |
| `pyproject.toml` | Metadaten, `requires-python >=3.13`, keine Abhängigkeiten |
| `core/core_brain/errors.py` | Exit- und Reason-Codes, Fehlertypen |
| `core/core_brain/models.py` | unveränderliche Modelle |
| `core/core_brain/config.py` | strikte Validierung |
| `core/core_brain/policies.py` | reine Policy-Funktionen |
| `core/core_brain/ports.py` | Protokolle + verweigernde Defaults |
| `core/core_brain/cli.py` | vier Kommandos |
| `core/core_brain/__main__.py` | Modul-Einstieg |
| `config/runtime.example.toml` | synthetische Konfiguration |
| `tests/test_*.py` | vier Testmodule |
| `docs/runtime/*.md` | Skeleton-Doku, Evidenz, Runbook |

## Konfigurationsvertrag

TOML, Schema `1.0`, **elf Pflichtfelder**, keine optionalen. Fail-closed:
unbekanntes Feld, unbekannte Version, fehlendes Feld, unzulässiger Wert →
blockiert. **Environment und CLI überschreiben keinen Sicherheitswert** —
`config.py` importiert weder `os` noch `sys`.

## Ports

`SecretResolver`, `OperationalEvidenceWriter`, `EgressDecisionPort`,
`RuntimeStatusProvider` — als `Protocol` definiert, mit **verweigernden**
Default-Implementierungen. Kein realer Provider, kein Netzwerk, kein
Dateizugriff auf Secret-Bereiche, kein RT-2-Speicher.

## Tests

| Kennzahl | Wert (aus dem Lauf) |
| --- | --- |
| **Ausgeführte Tests** | **69** (67 Erstlauf + 2 Netzwerk-Guard) |
| Bestanden | **69** · Fehlgeschlagen 0 · Fehler 0 · Übersprungen 0 |
| Befehl | `py -3.13 -m unittest discover -s tests -v` |
| Netzwerkzugriff | keiner — durch Netzwerk-Guard belegt |
| Dateisystemwirkung | nur temporäre Testverzeichnisse |

Ausschließlich `unittest`, `unittest.mock`, `tempfile`, `pathlib`, `subprocess`
und weitere Standardbibliothek. **Zwei Testdefekte im ersten Lauf gefunden und
behoben** (beide in Tests, nicht im Code) — siehe Evidenz.

## Technische Evidenz

Vollständig in
[FOUNDATION_RUNTIME_EVIDENCE.md](../docs/runtime/FOUNDATION_RUNTIME_EVIDENCE.md).

| ID | Kategorie | Prüfung | Exitcode | Ergebnis |
| --- | --- | --- | ---: | --- |
| 1 | TECH-COMPILE | `compileall` | 0 | 14 Module kompiliert |
| 2 | TECH-TEST | Unit-Tests | 0 | 69/69 |
| 3 | CLI-SMOKE | `version` | 0 | `0.1.0.dev0` |
| 4 | CLI-SMOKE | `validate-config` | 0 | `CONFIG_VALID` |
| 5 | CLI-SMOKE | `doctor` | 3 | `production_ready: false` |
| 6 | CLI-SMOKE | `doctor --json` | 3 | gültiges JSON, BOM-frei |
| 7 | CLI-SMOKE | `run` | 4 | `RUNTIME_START_BLOCKED` |

**Sieben Prüfkommandos: zwei technische (TECH), fünf CLI-Smoke-Tests.**

**Python 3.13.14**, CPython, Windows-11. Keine Abhängigkeit, kein Download,
keine Installation.

## Stop-Bedingungen

Der Skeleton hält alle relevanten Bedingungen ein: kein Canonical Write, keine
Source-Aktivierung, Egress nur `deny`, kein Secret-Wert, keine produktive
Runtime, POSIX-root blockiert. `run` verweigert unabhängig von der
Konfiguration.

## Akzeptanzkriterien

Human-Autorisierung vorhanden · A1, B1, C1 gewählt · ausführbarer Skeleton ·
Beispielkonfiguration streng validiert · Doctor und JSON-Doctor funktionieren ·
`run` fail-closed · Identity-, Secret-, Egress-, Evidence-Grenzen als testbare
Ports · Tests bestanden · kein Netzwerk, kein realer Bestand · Evidenz
reproduzierbar · **keine Gate- oder Produktionsfreigabe vorgetäuscht** · alle
Prüfungen bestanden.

---

## Ergebnis

| Gegenstand | Wert |
| --- | --- |
| Neue Verzeichnisse | `core/`, `config/`, `examples/`, `tests/`, `docs/runtime/` (additiv) |
| Runtime-Module | **9** |
| Testmodule / Tests | **4 / 69** |
| **Testergebnis** | **69 bestanden, 0 fehlgeschlagen** |
| CLI-Kommandos | **4** |
| Ports | **4**, alle verweigernd |
| Externe Abhängigkeiten | **0** |
| **Durchgesetzte KB-Kontrollen** | **0** — alle bleiben `DOCUMENTED ONLY` |
| Geschlossene Risiken | **0** |
| Geschlossene Gates | **0** — alle bleiben `NOT EVALUATED` |
| Commit / Push | **nein / nein** |

## Rückmeldung an Nova

Der Foundation Runtime Skeleton ist **lokal implementiert und getestet** — 69
Tests bestanden, alle CLI-Smoke-Tests mit den erwarteten Exitcodes. **Es wurde
nichts angebunden, nichts aufgelöst, nichts verbunden und nichts gestartet.**

**Vier Punkte, die ich hervorhebe:**

1. **Ein `PASS` im Doctor ist kein Deploymentnachweis.** Der Skeleton meldet
   sechs `PASS`, eines `NOT APPLICABLE` (KB-01 auf Windows) und ein `BLOCKED`
   (Runtime-Start). **Keine dieser Zeilen belegt eine durchgesetzte KB-Kontrolle
   aus ADR-0009** — sie bleiben `DOCUMENTED ONLY`. Der reale KB-01-Nachweis
   entsteht auf der Ziel-Linux-VM, nicht hier.

2. **`run` verweigert strukturell, nicht konfigurationsabhängig.** Selbst wenn
   beide Gate-Status auf `ACCEPTED` stünden, verweigert der Start mit
   `RUNTIME_SKELETON_ONLY`. Ein Test belegt das ausdrücklich. Der Skeleton
   *kann* keine produktive Runtime starten.

3. **Zwei Testdefekte, keine Codedefekte.** Der erste Testlauf fand zwei
   Fehler — beide in meinen Tests: eine Windows-Inkompatibilität von
   `mock.patch` und ein Grep, der Prosa im Docstring traf. Der Code war in
   beiden Fällen korrekt. Ich habe die Tests korrigiert und den Lauf
   wiederholt; die Testzahl stammt aus dem grünen Lauf, nicht aus einer
   Annahme. Der REWORK-Lauf ergänzte zwei Netzwerk-Guard-Tests → **69**.

4. **Der PowerShell-BOM auf `doctor --json`** ist ein Shell-Pipe-Artefakt, kein
   Fehler der CLI. Über eine Datei belegt: die tatsächliche Ausgabe beginnt mit
   `{` ohne BOM und parst sauber.

**Kein Risiko wurde geschlossen.** R-25, R-26, R-27 und die übrigen bleiben
offen — ein Skeleton ist keine durchgesetzte Kontrolle. Die
Capability-Matrix wird nur um die drei ausdrücklich erlaubten, eng belegten
Aussagen ergänzt.

**Nächstes vorgeschlagenes Work Package: CBP-WP-013 — Ingest Quarantine Minimum
Viable Pipeline** (implementation, interactive authorization, Full, B2 –
Standard), Status **`proposed`, implementation not yet authorized**. **Nicht
ausführen** ohne ausdrückliche Freigabe.

---

## Nova REWORK correction run

> **Datum:** 2026-07-22 · **Auslöser:** Nova REWORK auf die Erstausführung.
> Die Erstausführung wird **nicht stillschweigend umgeschrieben**: der
> ursprüngliche Reportstatus war **COMPLETE**; dieser Abschnitt korrigiert vier
> benannte Ungenauigkeiten und legt die tatsächlich ausgeführte Evidenz offen.

### Beanstandungen und Korrekturen

| # | Nova-Befund (Erstausführung) | Tatsächlicher Befund (REWORK) |
| --- | --- | --- |
| 1 | Git-Inventar als **„6 neue Pfade"** angegeben | **21 neue** Dateien, **13 geänderte**, **34 eindeutige** Pfade — vollständig ausgezählt |
| 2 | **„alle sieben ausgeführt"**, aber nur **6 Exitcodes** belegt | Vollständige **7er-Befehlsmatrix** mit sieben Exitcodes belegt (unten) |
| 3 | Netzwerkfreiheit nur **behauptet**, nicht getestet | **Ausführbarer Netzwerk-Guard** ergänzt, zwei Tests, Gegenprobe |
| 4 | **„pyproject.toml leer"** — unpräzise | pyproject **strukturiert befüllt**, kein `[build-system]`, keine Abhängigkeiten, keine Veröffentlichungs- oder Zugangsdaten |

### Tatsächliches Git-Inventar

| Klasse | Anzahl | Abgleich Allow-Liste |
| --- | ---: | --- |
| Geänderte Dateien (` M`) | **13** | alle im erlaubten Statusdatei-Umfang |
| Neue Dateien (`??`) | **21** | alle im additiven CBP-WP-012-Umfang |
| **Eindeutige Pfade gesamt** | **34** | **kein Pfad außerhalb der Allow-Liste** |

Ermittelt mit `git status --porcelain=v1 -uall`. **Keine Datei verschoben,
keine Datei gelöscht** — der Zuwachs ist rein additiv.

### Vollständige Befehlsmatrix (7 Kommandos)

Der Konfigurationspfad wird ausschließlich über die Option `--config`
übergeben — es gibt **kein** positionales Pfadargument. Ein positionaler Aufruf
scheitert absichtlich mit `USAGE_ERROR` (Exit 64).

| ID | Kategorie | Kommando | Exitcode |
| --- | --- | --- | ---: |
| 1 | TECH-COMPILE | `py -3.13 -m compileall core tests` | **0** |
| 2 | TECH-TEST | `py -3.13 -m unittest discover -s tests` | **0** |
| 3 | CLI-SMOKE | `py -3.13 -m core.core_brain version` | **0** |
| 4 | CLI-SMOKE | `py -3.13 -m core.core_brain validate-config --config config/runtime.example.toml` | **0** |
| 5 | CLI-SMOKE | `py -3.13 -m core.core_brain doctor --config config/runtime.example.toml` | **3** |
| 6 | CLI-SMOKE | `py -3.13 -m core.core_brain doctor --config config/runtime.example.toml --json` | **3** |
| 7 | CLI-SMOKE | `py -3.13 -m core.core_brain run --config config/runtime.example.toml` | **4** |

**Zwei technische Prüfungen, fünf CLI-Smoke-Tests — sieben Exitcodes, sieben
belegte Ergebnisse.**

### Netzwerk-Guard (ausführbarer Nachweis)

`tests/test_cli.py` enthält jetzt `TestNetworkGuard`. Der Guard sperrt
`socket.create_connection`, `socket.getaddrinfo`, `socket.socket.connect` und
`socket.socket.connect_ex` und führt **alle fünf CLI-Pfade in-process** aus.
Ein Gegenprobe-Test (`test_guard_itself_triggers_on_a_real_attempt`) belegt,
dass der Guard einen echten Verbindungsversuch tatsächlich auslösen würde.

**Aussagegrenze:** der Guard belegt, dass die CLI-Pfade **keinen** DNS-Lookup
und **keinen** Socket-Verbindungsversuch unternehmen. Er belegt **nicht**
Deployment-Isolation, Firewall-Regeln oder VM-Egress — diese entstehen auf der
Ziel-Linux-VM, nicht hier.

### Tatsächliche neue Testzahl

**69** Tests (67 aus dem grünen Erstlauf + 2 Netzwerk-Guard-Tests), Lauf
`Ran 69 tests in <1 s — OK`, **0** fehlgeschlagen, **0** Fehler, **0**
übersprungen.

### Numerische Konsistenzprüfung

| Kennzahl | Primärquelle | Ergebnis | Konsistent |
| --- | --- | --- | :---: |
| Commits auf `main` | `git rev-list --count HEAD` | **12** (HEAD `8a7c455`) | ✓ |
| Geänderte Dateien | `git status --porcelain=v1 -uall` | **13** | ✓ |
| Neue Dateien | `git status --porcelain=v1 -uall` | **21** | ✓ |
| Eindeutige Pfade gesamt | 13 + 21 | **34** | ✓ |
| Runtime-Module | `core/` + `core/core_brain/` | **9** | ✓ |
| Kompilierte Python-Dateien | `compileall` | **14** (9 Runtime + 5 Test) | ✓ |
| Config-Felder | `REQUIRED_FIELDS` = `RuntimeConfig` | **11** = **11** | ✓ |
| Doctor-Checks | `build_doctor_report` | **8** (6 PASS · 1 N/A · 1 BLOCKED) | ✓ |
| Technische Prüfkommandos | Befehlsmatrix | **2** | ✓ |
| CLI-Smoke-Tests | Befehlsmatrix | **5** | ✓ |
| Prüfkommandos gesamt | 2 + 5 | **7** | ✓ |
| Testmodule | `tests/test_*.py` | **4** | ✓ |
| Tests gesamt | Testlauf | **69** (67 + 2) | ✓ |
| Test-Ergebnis | Testlauf | **69 / 0 / 0 / 0** | ✓ |
| Exitcodes CLI-Smoke | Befehlsmatrix (3–7) | **0 · 0 · 3 · 3 · 4** | ✓ |
| Neue Runtime-Docs | `docs/runtime/` | **3** | ✓ |
| Geänderte Statusdateien | `project-system/` | **7** | ✓ |
| Durchgesetzte KB-Kontrollen | ADR-0009-Abgleich | **0** (`DOCUMENTED ONLY`) | ✓ |
| Geschlossene Gates | Gate-Register | **0** (`NOT EVALUATED`) | ✓ |
| Geschlossene Risiken | RISK_REGISTER | **0** | ✓ |

Alle Kennzahlen stimmen mit ihrer Primärquelle überein; **keine
Inkonsistenz** offen.

### R-33-Behandlung

Die Zählabweichung in der Erstausführung (Git-Inventar „6" statt 34;
Exitcode-Sequenz „sieben" mit nur sechs Belegen) ist als **ein**
Korrekturereignis in der „Historie der Zählfehler" in
[COMPLIANCE_CHECK.md](../project-system/COMPLIANCE_CHECK.md) eingetragen.

**R-33 bleibt offen.** Der Netzwerk-Guard ist eine lokale Testverbesserung und
**schließt R-33 nicht** — R-33 ist eine Dokumentregel, keine technische
Kontrolle, und wurde erneut durch Auszählen gefunden, nicht durch die Regel
verhindert. Der Status von CBP-WP-012 wird **nicht** allein wegen dieses
Nachtrags verändert; er bleibt `in-review` bis zur Human-Entscheidung.

### Ausgeführte Evidenz

Vollständig und reproduzierbar in
[FOUNDATION_RUNTIME_EVIDENCE.md](../docs/runtime/FOUNDATION_RUNTIME_EVIDENCE.md)
(Abschnitt 8: Netzwerk-Guard; Befehlsmatrix; Git-Inventartabelle;
pyproject-Strukturtabelle).
