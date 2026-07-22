# Ingest Quarantine MVP — Technische Evidenz

| Feld | Wert |
| --- | --- |
| Erfasst in | **CBP-WP-013** |
| Autoritätsklasse | A2 (technischer Nachweis) |
| Ausgeführt am | 2026-07-22 |
| Stand | 2026-07-22 |

> **Alle Zahlen stammen aus dem tatsächlichen Lauf**, nicht aus einer
> Spezifikation. Die Befehle sind reproduzierbar. Testzahlen stammen
> ausschließlich aus `Ran N tests`; Dateizahlen aus
> `git status --porcelain=v1 -uall`.

---

## Umgebung

| Feld | Wert |
| --- | --- |
| **Python-Version** | **3.13.14** (CPython) |
| **Launcher** | `py -3.13` (PowerShell-kompatibel) |
| **Plattform** | `Windows-11-10.0.26200-SP0` |
| Externe Runtime-Abhängigkeiten | **keine** |
| Paketdownloads | **keine** |
| Globale Installationen | **keine** |
| Modellprofil | Opus 4.8 (`claude-opus-4-8`), A0-Modellsubstitution |

## 1 — Compile

```powershell
py -3.13 -m compileall -q core tests config
```

Exitcode **0**. 15 Runtime-Module (davon 6 Quarantäne), 10 Testmodule.

## 2 — Unit-Tests

```powershell
py -3.13 -m unittest discover -s tests -v
```

`Ran 137 tests` · **OK** · **0** fehlgeschlagen · **0** Fehler · **0**
übersprungen. Exitcode **0**.

**Testbasislinie CBP-WP-012:** 69 Tests bleiben grün. Der Zuwachs entstand
durch fünf neue Quarantäne-Testmodule und die Erweiterung des Netzwerk-Guards.
**Zwei Testdefekte im ersten Lauf gefunden und behoben** (beide in Tests, nicht
im Code):

1. eine Prüfung suchte die Prosa `os.environ`/`sys.argv` in der Docstring des
   Policy-Moduls statt nur die Importzeilen — auf reine Importprüfung reduziert;
2. eine Payload-Prüfung verglich mit `\n`, während Windows `write_text` die
   Datei mit `\r\n` schrieb — auf exakte Bytes (`write_bytes`) umgestellt. Der
   Store hatte die Bytes korrekt unverändert gespeichert.

## Kanonische Prüfmatrix — drei Kategorien (Nova-REWORK-Präzisierung)

Ausgeführt in einem eindeutigen temporären PowerShell-Verzeichnis mit
BOM-freien UTF-8-Dateien (`System.Text.UTF8Encoding($false)`). Native Befehle
und PowerShell-Kontrollschritte werden **getrennt** gezählt: nur native Befehle
besitzen `$LASTEXITCODE`; Kontrollschritte erhalten ein Pass/Fail-Ergebnis.

| ID | Kategorie | Prüfschritt | Erwartung | Ergebnis |
| --- | --- | --- | --- | :---: |
| P01 | PYTHON-TECHNICAL | `compileall core tests` | Exit 0 | **0** |
| P02 | PYTHON-TECHNICAL | `unittest discover -s tests` | Exit 0, `Ran 137 tests`, OK | **0** |
| P03 | PYTHON-TECHNICAL | Policy-Check (`load_policy`, read-only) | Exit 0, 13 Felder | **0** |
| S04 | CLI-SMOKE | `version` | Exit 0 | **0** |
| S05 | CLI-SMOKE | `quarantine scan` (clean) | Exit 0 · `READY_FOR_HUMAN_REVIEW` | **0** |
| S06 | CLI-SMOKE | `quarantine scan` (E-Mail) | Exit 5 · `REVIEW_REQUIRED` | **5** |
| S07 | CLI-SMOKE | `quarantine scan` (kein Marker) | Exit 6 · `BLOCKED` | **6** |
| S08 | CLI-SMOKE | `quarantine scan --json` | Exit 0 · minimiertes JSON | **0** |
| S09 | CLI-SMOKE | `quarantine stage` (clean) | Exit 0 · 1 Objekt + 1 Record | **0** |
| S10 | CLI-SMOKE | `quarantine inspect` | Exit 0 · minimierte Metadaten | **0** |
| S11 | CLI-SMOKE | `quarantine release` | Exit 7 · `QUARANTINE_RELEASE_BLOCKED` | **7** |
| S12 | CLI-SMOKE | `run` | Exit 4 · `RUNTIME_START_BLOCKED` | **4** |
| C13 | POWERSHELL-CONTROL | temporäres Verzeichnis erzeugen | existiert | **PASS** |
| C14 | POWERSHELL-CONTROL | synthetische BOM-freie Testdatei | existiert, kein BOM | **PASS** |
| C15 | POWERSHELL-CONTROL | Store-Inventar prüfen | 1 Objekt, 1 Record | **PASS** |
| C16 | POWERSHELL-CONTROL | Manifest minimiert prüfen | kein Pfad, kein Dateiname | **PASS** |
| C17 | POWERSHELL-CONTROL | Cleanup ausführen | Store entfernt | **PASS** |
| C18 | POWERSHELL-CONTROL | Cleanup-Ergebnis prüfen | `Test-Path` = False | **PASS** |

**Zahlen je Kategorie:** PYTHON-TECHNICAL **3** · CLI-SMOKE **9** ·
POWERSHELL-CONTROL **6** · **Gesamt 18 Prüfschritte.** Native Befehle mit
`$LASTEXITCODE`: **12** · PowerShell-Kontrollschritte mit Pass/Fail: **6**.

> **Zur früheren Zahl „elf".** Die ursprüngliche Befehlsmatrix nannte **11**
> native Befehle. Diese Zahl bleibt gültig als **klar benannte Teilmenge** —
> die 12 nativen Befehle **ohne** den nun separat ausgewiesenen Policy-Check
> (12 − 1 = 11). Sie war kein falscher Zählwert, sondern eine unvollständige
> Klassifikation.

**Policy-Check (P03), reproduzierbar und read-only:** `py -3.13` lädt die
Beispielpolicy über `core.core_brain.quarantine.policy.load_policy` (temporäres
Skript außerhalb des Repos, danach gelöscht; keine Datei im Repo, kein Netzwerk,
keine Runtime-Daten). Bestätigt: `loaded=True`, `schema_version=1.0`, **13**
Pflichtfelder, `release_enabled=False`, `network_enabled=False`,
`allowed_suffixes=['.md']`, `policy_sha256`-Länge 64. Negativnachweis:
`quarantine scan` mit ungültiger Policy (`schema_version = "9.9"`) → Exit **2**
(`CONFIG_INVALID`); negative Policy-Tests `test_2/3/6/7` in
`test_quarantine_policy.py` bestätigen unbekanntes Feld, unbekannte Version,
`release_enabled = true`, `network_enabled = true`.

## Temporärer Store und Cleanup

- `quarantine stage` erzeugte genau **ein** Objekt (`objects=1`) und **einen**
  Record (`records=1`).
- Der Store lag ausschließlich in einem temporären Verzeichnis außerhalb des
  Core-Repositorys.
- Cleanup erfolgte in `finally { Remove-Item -Recurse -Force $tmp }`.
- `Test-Path $tmp` nach Cleanup: **False** — es verbleiben **keine**
  WP-013-Runtime-Daten.

## Pfad- und Inhaltsminimierung

Das `stage --json`-Manifest wurde geprüft:

- `contains_clean_md = False` — kein Dateiname,
- `contains_tmp_path = False` — kein Eingabepfad,
- `stored_object_reference` ist **store-relativ** (`objects/sha256/…`), kein
  absoluter Pfad,
- `source_reference` ist opak (`synthetic:…`).

In-process-Tests belegen zusätzlich, dass weder ein Inhaltstoken noch ein
Dateiname in `stdout`/`stderr` von `scan` und `stage` erscheint (Test 50) und
dass `json.loads` das CLI-JSON **ohne BOM** parst. Der beim PowerShell-Befehl
`Out-File -Encoding utf8` beobachtete BOM (`EF BB BF`) ist ein
**Shell-Artefakt**, kein Fehler der CLI — identisch zum Befund aus CBP-WP-012.

## Netzwerk-Guard

`tests/test_cli.py::TestNetworkGuard` sperrt `socket.create_connection`,
`socket.getaddrinfo`, `socket.socket.connect` und `socket.socket.connect_ex`
und führt **alle** CLI-Pfade in-process aus — inklusive der vier neuen
Quarantäne-Pfade `scan`, `stage`, `inspect`, `release`. Eine Gegenprobe belegt,
dass der Guard einen echten Verbindungsversuch auslösen würde.

**Aussagegrenze:** Der Guard belegt, dass **während der ausgeführten Tests und
lokalen CLI-Prüfungen kein Netzwerkverbindungs- oder DNS-Versuch festgestellt
wurde**. Er belegt **nicht** Deployment-Isolation, Firewallwirkung,
Container-Netzgrenzen oder VM-Egress-Kontrolle.

## Keine Promotion

- `quarantine release` verweigert unabhängig vom Recordstatus (Exit **7**) und
  öffnet den Store nicht.
- Es existiert **kein** erfolgreicher Promotion- oder Release-Pfad.
- Kein Mapping wird aktiviert, keine Collection und kein Index erzeugt.

## Verbleibende Blocker

**Von CBP-WP-013 berührt (nicht geschlossen):** R-01, R-32, R-33.

- **R-32** bleibt `offen` — die produktive Quarantäne existiert nicht.
- **R-01** bleibt offen — es gibt keine vollständige Secret-Erkennung.
- Alle drei Gates (Security Foundation Readiness, Mapping Activation, DRC)
  bleiben `NOT EVALUATED`.
- **OD-37** (produktive Isolation) und **OD-38** (produktive Erkennung) offen.

**Diese Aufzählung ist nicht die kritische Risikoliste.** Drei kanonisch
benannte Mengen, jede aus ihrer ID-Liste ausgezählt (Quelle:
[RISK_REGISTER.md](../../project-system/RISK_REGISTER.md)):

- **Weiterhin kritisch — kuratierte Registerliste (6):** R-21, R-25, R-27,
  R-31, R-32, R-34 (Abschnitt `## Weiterhin kritisch`, identisch in
  `PROJECT_BRAIN.md`). Nur diese IDs sind kanonisch „weiterhin kritisch".
- **Zusätzliche offene Beobachtungsrisiken (5):** R-01, R-20, R-26, R-30, R-33
  — offen, aber **nicht** in der kuratierten Liste; enthält mit R-33 ein
  Risiko der Kritikalität **mittel** und wird daher **nicht** als „hoch"
  bezeichnet.
- **Gesamte beobachtete Risikomenge (11):** die Vereinigung beider — **keine**
  kritische Liste.

> **R-33-Chronologie.** Ein früherer Korrekturlauf bezeichnete in diesem
> Dokument und in `work-packages/CBP-WP-013.md` die Vereinigungsmenge (11)
> fälschlich als „kritische Liste" und die zusätzliche Gruppe als „hoch",
> obwohl R-33 mittel ist. Da beide Dateien **Repository-Artefakte** des
> CBP-WP-013-Änderungssatzes sind, wurde entsprechend der Nova-Vorgabe **ein**
> R-33-Chronologieeintrag ergänzt (achter Konsistenzvorgang, 2026-07-22) —
> geführt in [RISK_REGISTER.md](../../project-system/RISK_REGISTER.md) und
> [COMPLIANCE_CHECK.md](../../project-system/COMPLIANCE_CHECK.md). Die Zahlen
> **6, 5 und 11 waren korrekt**; fehlerhaft war die Mengenbenennung und die
> Kritikalitätsterminologie. **R-33 bleibt `gemindert, nicht geschlossen`;**
> aktueller Stand: **acht Konsistenzvorgänge in dreizehn Work Packages**.

**CBP-WP-013 hat keines dieser Risiken geschlossen.**

## Git-Inventar

Ausgezählt mit `git status --porcelain=v1 -uall`:

| Klasse | Anzahl |
| --- | ---: |
| Geänderte Dateien (` M`) | **20** |
| Neue Dateien (`??`) | **18** |
| Gelöschte Dateien | **0** |
| Umbenannte Dateien | **0** |
| **Eindeutige Pfade gesamt** | **38** |

**Summenprüfung:** 20 + 18 + 0 + 0 = **38**. Alle Pfade liegen in der
Erlaubnisliste von CBP-WP-013; `__pycache__` und `*.pyc` sind ignoriert. Keine
Datei wurde verschoben oder gelöscht. Davon **13** Codeträger (6 Quarantäne-
Module, Beispiel-Policy, Beispiele, 5 Testmodule) und **2** geänderte
Codeträger (`cli.py`, `errors.py`) plus die Erweiterung `tests/test_cli.py`.
