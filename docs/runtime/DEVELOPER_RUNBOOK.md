# Developer Runbook — Foundation Runtime Skeleton

| Feld | Wert |
| --- | --- |
| Erfasst in | CBP-WP-012 |
| Autoritätsklasse | A2 |
| Shell | **PowerShell** — alle Befehle sind PowerShell-Befehle |
| Stand | 2026-07-21 |

> **Dies ist keine produktive Betriebsanleitung.** Der Skeleton ist lokal und
> fail-closed. Er startet keine Runtime, bindet keine Quelle an und öffnet
> keine Verbindung.
>
> **Für die Ingest-Quarantäne (CBP-WP-013)** siehe das eigene
> [INGEST_QUARANTINE_RUNBOOK.md](INGEST_QUARANTINE_RUNBOOK.md) — ausschließlich
> synthetische, temporäre Daten.

---

## Voraussetzung

**Python 3.13 oder neuer.** Prüfen:

```powershell
py -0p
py -3.13 --version
```

Ist `python` bereits 3.13+, kann `python` statt `py -3.13` verwendet werden.
Andernfalls gilt durchgehend `py -3.13`.

**Keine Installation nötig:** Der Skeleton verwendet ausschließlich die
Standardbibliothek. Es werden keine Pakete geladen und nichts global
installiert.

## Ausführungsverzeichnis

Alle Befehle laufen aus dem Repository-Wurzelverzeichnis:

```powershell
Set-Location "D:\Projects\Core-Brain-Pilot"
```

## Compile

```powershell
py -3.13 -m compileall core tests
```

## Tests

```powershell
py -3.13 -m unittest discover -s tests -v
```

Erwartung: alle Tests bestehen, `$LASTEXITCODE` ist `0`.

## CLI-Kommandos

### version

```powershell
py -3.13 -m core.core_brain version
$LASTEXITCODE   # 0
```

### validate-config

```powershell
py -3.13 -m core.core_brain validate-config --config config/runtime.example.toml
$LASTEXITCODE   # 0 bei struktureller Gültigkeit, 2 bei Verstoß
```

### doctor

```powershell
py -3.13 -m core.core_brain doctor --config config/runtime.example.toml
$LASTEXITCODE   # 3 (mindestens ein BLOCKED)
```

### doctor --json

```powershell
py -3.13 -m core.core_brain doctor --config config/runtime.example.toml --json
```

> **BOM-Hinweis:** Ein direktes `| ConvertFrom-Json` oder `| py …` fügt in
> PowerShell zwischen zwei nativen Prozessen einen UTF-8-BOM ein. Um die
> JSON-Ausgabe weiterzuverarbeiten, in eine Datei umleiten:
>
> ```powershell
> $tmp = Join-Path $env:TEMP "cbp_doctor.json"
> Start-Process py -ArgumentList "-3.13","-m","core.core_brain","doctor",`
>   "--config","config/runtime.example.toml","--json" `
>   -NoNewWindow -Wait -RedirectStandardOutput $tmp
> Get-Content $tmp -Raw | ConvertFrom-Json
> Remove-Item $tmp
> ```

### run

```powershell
py -3.13 -m core.core_brain run --config config/runtime.example.toml
$LASTEXITCODE   # 4 (RUNTIME_START_BLOCKED)
```

`run` verweigert **immer**. Das ist beabsichtigt: Der Skeleton startet keine
operative Runtime.

## Exitcodes

| Wert | Name | Bedeutung |
| --- | --- | --- |
| `0` | OK | erfolgreich |
| `2` | CONFIG_INVALID | Konfiguration ungültig |
| `3` | POLICY_BLOCKED | Doctor meldet BLOCKED |
| `4` | RUNTIME_START_BLOCKED | `run` verweigert |
| `64` | USAGE_ERROR | falsche Kommandozeile |
| `70` | INTERNAL_ERROR | unerwarteter Fehler |

## Was dieser Runbook nicht abdeckt

- **kein** produktiver Start,
- **keine** Quellenanbindung,
- **keine** Secret-Auflösung,
- **keine** Netzwerkkonfiguration,
- **kein** Deployment.

Diese Schritte sind Gegenstand späterer, ausdrücklich freigegebener Work
Packages.
