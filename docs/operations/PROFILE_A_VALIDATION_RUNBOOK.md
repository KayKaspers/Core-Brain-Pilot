# Profile-A Validation Runbook

| Feld | Wert |
| --- | --- |
| Gegenstand | deterministische Offline-Validierung des Profil-A-Bundles |
| Erfasst in | **CBP-WP-020** (D-055) |
| Autoritätsklasse | A3 |
| Status | **ausführbar** — reine Repository-Prüfung ohne Infrastruktur |
| Stand | 2026-07-29 |

## Zweck und Aussagegrenze

Der Validator prüft **Artefakte und Verträge** des Bundles. Er prüft **keine
reale Durchsetzung**.

| Prüft | Prüft **nicht** |
| --- | --- |
| Dateisatz, Kodierung, Symlinks | reale Hostrechte |
| Compose-Struktur und Härtungsvorlagen | reale UID- oder GID-Werte |
| Mountmatrix und Zielpfade | tatsächlich gemountete Volumes |
| Netzwerk- und Egress-**Vertrag** | echte Netzwerkdurchsetzung |
| Secret-**Referenzsyntax** | aufgelöste Secrets |
| Vertragskonsistenz zwischen Compose, TOML und `bundle.json` | laufende Container |
| Public-Neutrality und Leakage | Security-Foundation-Wirksamkeit |

**Ein grüner Validatorlauf belegt keine Sicherheitsdurchsetzung.**

## Abgrenzung zu NT-01 bis NT-33 und PT-01

Die Prüfungen dieses Runbooks und die zugehörigen Unit Tests heißen und gelten
ausschließlich als **Profile-A Bundle Validation**.

Sie sind **ausdrücklich nicht**: Security Foundation NT-01 bis NT-33 oder PT-01, reale
Containerprüfungen, Infrastruktur- oder Deploymenttests,
Security-Control-Enforcement-Nachweise oder operative Evidenz.

**Kanonische Kennzahl (D-056): 32 Negativtests, 1 Positivtest, 33 Testfälle —
ausgeführt 0 von 32 Negativtests und 0 von 1 Positivtest.**

## Standardaufruf

```bash
py.exe -3.13 deployments/profile-a/validate.py
```

Optional mit explizitem Bundle-Root:

```bash
py.exe -3.13 deployments/profile-a/validate.py <bundle-root>
```

## Exitcodes

| Code | Bedeutung |
| --- | --- |
| **0** | Bundle gültig |
| **1** | Bundle fachlich ungültig |
| **2** | ungültiger Aufruf oder unerwarteter Lesefehler |

Diese Exitcodes gelten **nur für dieses Offline-Werkzeug** und sind nicht mit
dem CLI-Exitcode-Vertrag des Produkt-Runtime zu verwechseln.

## Erwartete Ausgabe

Gültig:

```text
PROFILE-A-BUNDLE VALID
issues=0
```

Ungültig:

```text
PROFILE-A-BUNDLE INVALID
issues=<Anzahl>
<CODE> | <relativer Pfad> | <Meldung>
```

Die Ausgabe endet mit **genau einem** Zeilenumbruch, enthält **keine** Farben,
Terminalsteuerzeichen, Zeitangaben oder absoluten Pfade.

## Deterministische Wiederholungsprüfung

```bash
py.exe -3.13 deployments/profile-a/validate.py > out1.txt
py.exe -3.13 deployments/profile-a/validate.py > out2.txt
```

Beide Ausgaben müssen **byte-identisch** sein. Issues sind stabil sortiert nach
**Code, Pfad, Meldung**. Temporäre Vergleichsdateien gehören **nicht** ins
Repository.

## Getrennte Prüfobjekte

| Objekt | Ort | Prüfung |
| --- | --- | --- |
| **Repository-Bundle** | `deployments/profile-a/` | dieser Validator |
| **Operator-Workspace** | lokal, außerhalb des Repositorys | **separat**, nie mit dem Repository vermischt |

Der Validator liest **keine Datei außerhalb des übergebenen Bundle-Roots** und
folgt **keinen Symlinks**.

## Optionaler späterer Compose-Schritt

Ein `docker compose config`-Schritt ist **ausschließlich nach dem Human Gate**
des separaten Deployment-Work-Packages zulässig. **In CBP-WP-020 wurde kein
Docker-Kommando ausgeführt.**

## Abbruchbedingungen

**Bei jedem Validatorfehler anhalten.** Exitcode 1 oder 2 bedeutet: keine
weitere Compose-Auswertung, keine Bereitstellung, kein Commit ohne Klärung.

**Keine Ausführung einer realen Bereitstellung durch dieses Runbook.**
