# Profile-A Rollback Runbook

| Feld | Wert |
| --- | --- |
| Gegenstand | späterer kontrollierter Rückbau einer Profil-A-Bereitstellung |
| Erfasst in | **CBP-WP-020** (D-055) |
| Autoritätsklasse | A3 |
| **Status** | **nicht ausgeführt** — kein Rollback in diesem Lauf |
| Stand | 2026-07-29 |

## Zweck und Aussagegrenze

Dieses Runbook beschreibt den **späteren** Rückbau. **Ein Rollback erfolgt erst
im separaten Deployment-Work-Package** — es gibt derzeit nichts
zurückzubauen, weil **keine Bereitstellung existiert**.

**In CBP-WP-020 wurde kein Rollback ausgeführt, kein Dienst gestoppt, kein
Volume entfernt und keine Referenz widerrufen.**

## Vorbedingung

**Jede destruktive Handlung erfordert eine ausdrückliche
Human-Maintainer-Bestätigung.** Ohne sie wird nichts gestoppt, gelöscht,
zurückgesetzt oder widerrufen.

## Ablauf eines späteren Rollbacks

### 1 — Ausgangspunkt bestimmen

- Den **vorherigen validierten Bundle-Commit** identifizieren.
- Der Zielstand muss den Offline-Validator mit Exitcode 0 bestehen.

### 2 — Human-Gate

- **Vor jeder destruktiven Handlung** ausdrückliche Bestätigung des Human
  Maintainers einholen.

### 3 — Dienste anhalten

- Dienste **kontrolliert** stoppen — kein erzwungenes Beenden, solange ein
  geordneter Halt möglich ist.

### 4 — Konfiguration zurücksetzen

- Konfiguration auf den vorherigen validierten Stand zurücksetzen.
- Erneut offline validieren, bevor etwas gestartet wird.

### 5 — Daten

| Regel |
| --- |
| **Kanonische Daten werden nicht gelöscht.** |
| **Volumes werden standardmäßig nicht entfernt.** |
| **Keine automatische `down -v`- oder `prune`-Aktion.** |
| Abgeleitete Daten (RT-1) dürfen später **neu aufgebaut** werden — Rebuild aus kanonisch und Registry. |

### 6 — Secret-Referenzen

- Secret-Referenzen werden **separat widerrufen und ersetzt** (alte Referenz
  sperren, neue setzen).
- **Aktuelle Referenzen dürfen nicht versehentlich in eine ältere Konfiguration
  übernommen werden** — ein Konfigurations-Rollback rollt Referenzen **nicht**
  automatisch zurück.
- **Keine Secret-Werte** in Repository, Environment, Compose oder Log.

## Backup- und Restore-Grenze

| Ebene | Behandlung |
| --- | --- |
| **VM-Backup** (wöchentlich) | getrennt behandeln — Betreiber-Backup-Regime |
| **Kanonische Datensicherung** (täglich) | getrennt behandeln — trägt das RPO |
| **CBP-/RT-2-Restore** | **nicht erbracht** — Readiness-Gate Punkt 18 und 19 offen |

**RPO 24 Stunden und RTO 8 Stunden gelten durch dieses Runbook nicht als
erfüllt.** Sie sind dokumentierte Zielwerte, keine gemessenen Ergebnisse.

**CBP-WP-020 erbringt keinen CBP- oder RT-2-Restore-Nachweis. R-20 bleibt
offen.**

## Abgrenzung

**Kein Rollback in diesem Lauf.** Dieses Dokument ist eine Vorbereitung für ein
separates, ausdrücklich autorisiertes Deployment-Work-Package.
