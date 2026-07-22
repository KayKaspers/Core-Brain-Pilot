# Source Registry MVP — Technische Evidenz

| Feld | Wert |
| --- | --- |
| Erfasst in | **CBP-WP-014** |
| Autoritätsklasse | A2 (technischer Nachweis) |
| Ausgeführt am | 2026-07-22 |
| Stand | 2026-07-22 |

> **Alle Zahlen stammen aus dem tatsächlichen Lauf.** Testzahlen aus
> `Ran N tests`; Dateizahlen aus `git status --porcelain=v1 -uall`.

---

## Umgebung

| Feld | Wert |
| --- | --- |
| **Python-Version** | **3.13.14** (CPython) |
| **Launcher** | `py -3.13` |
| **Plattform** | `Windows-11-10.0.26200-SP0` |
| Externe Runtime-Abhängigkeiten | **keine** |
| Paketdownloads / globale Installationen | **keine** |
| Modellprofil | Opus 4.8 (`claude-opus-4-8`), Effort ultracode |

## Kanonische Prüfmatrix — drei Kategorien

Ausgeführt in einem eindeutigen temporären PowerShell-Verzeichnis mit
BOM-freien UTF-8-Dateien. Native Befehle und PowerShell-Kontrollschritte werden
**getrennt** gezählt: nur native Befehle besitzen `$LASTEXITCODE`.

| ID | Kategorie | Prüfschritt | Erwartung | Ergebnis |
| --- | --- | --- | --- | :---: |
| P01 | PYTHON-TECHNICAL | `compileall core tests` | Exit 0 | **0** |
| P02 | PYTHON-TECHNICAL | `unittest discover -s tests` | Exit 0, `Ran 212 tests`, OK | **0** |
| P03 | PYTHON-TECHNICAL | Policy-Check (`load_policy`, read-only) | Exit 0, 14 Felder | **0** |
| S04 | CLI-SMOKE | `version` | Exit 0 | **0** |
| S05 | CLI-SMOKE | `source-registry validate-definition` | Exit 0 | **0** |
| S06 | CLI-SMOKE | `source-registry register` | Exit 0 · `REGISTERED_DISABLED` | **0** |
| S07 | CLI-SMOKE | `source-registry list` | Exit 0 · minimiert | **0** |
| S08 | CLI-SMOKE | `source-registry inspect` | Exit 0 · minimiert | **0** |
| S09 | CLI-SMOKE | `source-registry retire` | Exit 0 · `RETIRED` | **0** |
| S10 | CLI-SMOKE | `source-registry list` (nach Retirement) | Exit 0 | **0** |
| S11 | CLI-SMOKE | `source-registry activate` | Exit 11 · verweigert | **11** |
| S12 | CLI-SMOKE | `run` | Exit 4 · verweigert | **4** |
| C13 | POWERSHELL-CONTROL | temporäres Verzeichnis erzeugen | existiert | **PASS** |
| C14 | POWERSHELL-CONTROL | synthetische BOM-freie Definition | existiert, kein BOM | **PASS** |
| C15 | POWERSHELL-CONTROL | Registry-Inventar prüfen | 1 Record, 1 Event, 1 Katalog | **PASS** |
| C16 | POWERSHELL-CONTROL | Katalog minimiert prüfen | keine Ref, kein Pfad, keine URL | **PASS** |
| C17 | POWERSHELL-CONTROL | Cleanup + Ergebnis prüfen | `Test-Path` = False | **PASS** |

**Zahlen je Kategorie:** PYTHON-TECHNICAL **3** · CLI-SMOKE **9** ·
POWERSHELL-CONTROL **5** · **Gesamt 17 Prüfschritte.** Native Befehle mit
`$LASTEXITCODE`: **12** · PowerShell-Kontrollschritte mit Pass/Fail: **5**.

**Policy-Check (P03), read-only:** `py -3.13` lädt die Beispielpolicy über
`core.core_brain.registry.policy.load_policy` (temporäres Skript außerhalb des
Repos, danach gelöscht; keine Datei im Repo, kein Netzwerk). Bestätigt:
`loaded=True`, `schema=1.0`, **14** Pflichtfelder, `allow_activation=False`,
`allow_network=False`, `allow_retirement=True`.

## Tests

`py -3.13 -m unittest discover -s tests -v` → `Ran 212 tests` · **OK** · **0**
fehlgeschlagen · **0** Fehler · **0** übersprungen.

**Testbasislinie CBP-WP-013:** 137 Tests bleiben grün. Der Zuwachs entstand
durch sechs neue Registry-Testmodule und die Erweiterung des Netzwerk-Guards.
**Ein Testdefekt im ersten Lauf gefunden und behoben** (im Test, nicht im
Code): eine URL-Indikator-Prüfung verwendete eine URL **mit** Schrägstrich, die
zuerst als Pfadseparator blockiert; auf einen schrägstrichfreien URL-Marker
(`www.`) umgestellt und eine zweite Prüfung für den Pfadseparator-Fall ergänzt.

## Registry-Inventar und Minimierung

- `register` erzeugte genau **einen** Record; `retire` genau **ein** Event;
  der Katalog wurde als genau **eine** `catalog.json` abgeleitet.
- Der Katalog enthält **keine** `source_reference`, **keinen** Pfad, **keine**
  URL, **keinen** Inhalt (geprüft: kein `synthetic:`, kein `://`, kein
  temporärer Pfad).
- Der Record enthält 17 kanonische Felder ohne Pfad/URL/Inhalt/Mapping-Locator;
  in-process-Tests belegen dies zusätzlich.

## Cleanup

Cleanup in `finally { Remove-Item -Recurse -Force $tmp }`; `Test-Path $tmp`
danach **False** — es verbleiben **keine** WP-014-Registry-Daten.

## Netzwerk-Guard

`tests/test_cli.py::TestNetworkGuard` sperrt `socket.create_connection`,
`socket.getaddrinfo`, `socket.socket.connect` und `socket.socket.connect_ex`
und führt **alle** CLI-Pfade in-process aus — inklusive der sechs neuen
Registry-Pfade `validate-definition`, `register`, `list`, `inspect`, `retire`,
`activate`. Eine Gegenprobe belegt, dass der Guard einen echten
Verbindungsversuch auslösen würde.

**Aussagegrenze:** Der Guard belegt, dass **während der ausgeführten Tests und
lokalen CLI-Prüfungen kein Netzwerkverbindungs- oder DNS-Versuch festgestellt
wurde**. Er belegt **nicht** Deployment-Isolation, Firewall- oder
VM-Isolationsgarantie.

## Keine Aktivierung

- `source-registry activate` verweigert unabhängig vom Zustand (Exit **11**)
  und öffnet den Speicher nicht.
- Kein Mapping wird erzeugt oder aktiviert, keine Source Boundary, keine
  Collection und kein Index.

## Verbleibende Blocker

- **R-33** bleibt `gemindert, nicht geschlossen`.
- Alle drei Gates (Security Foundation Readiness, Mapping Activation, DRC)
  bleiben `NOT EVALUATED`.
- **OD-05, OD-06, OD-37, OD-38** bleiben offen.
- Product Capabilities implemented bleibt **0 von 29**.

## Git-Inventar

Ausgezählt mit `git status --porcelain=v1 -uall`:

| Klasse | Anzahl |
| --- | ---: |
| Geänderte Dateien (` M`) | **19** |
| Neue Dateien (`??`) | **19** |
| Gelöschte Dateien | **0** |
| Umbenannte Dateien | **0** |
| **Eindeutige Pfade gesamt** | **38** |

**Summenprüfung:** 19 + 19 + 0 + 0 = **38**. Alle Pfade liegen in der
Erlaubnisliste von CBP-WP-014; `__pycache__` und `*.pyc` sind ignoriert. Keine
Datei wurde verschoben oder gelöscht. Davon **13** Codeträger (6 Registry-
Module, Beispiel-Policy, 6 Testmodule) und **3** geänderte Codeträger
(`cli.py`, `errors.py`, `tests/test_cli.py`).
