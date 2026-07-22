# Ingest Quarantine MVP — Runbook (PowerShell)

| Feld | Wert |
| --- | --- |
| Erfasst in | **CBP-WP-013** |
| Autoritätsklasse | A2 (Betriebsleitfaden des Prototyps) |
| Stand | 2026-07-22 |

> **synthetic · non-operational · test-only.** Dieses Runbook ist **keine**
> produktive Betriebsanleitung. Es verwendet ausschließlich **synthetische**
> temporäre Daten und räumt vollständig in einem `finally`-Block auf. Alle
> Befehle sind **PowerShell**.

---

## Voraussetzungen

- Python 3.13 oder neuer, aufrufbar über `py -3.13`.
- Arbeitsverzeichnis `D:\Projects\Core-Brain-Pilot`.
- Keine Installation, keine Abhängigkeiten.

## Vollständiges, selbstaufräumendes Beispiel

Der folgende Block erstellt synthetische Artefakte, führt Scan, Stage, Inspect
und Release aus und **entfernt** anschließend alle temporären Daten. BOM-freies
UTF-8 wird über `System.Text.UTF8Encoding($false)` erzeugt.

```powershell
$repo = "D:\Projects\Core-Brain-Pilot"
Set-Location $repo
$policy = "config\quarantine_policy.example.toml"

$tmp = Join-Path $env:TEMP ("cbp-wp013-" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $tmp | Out-Null
$utf8 = New-Object System.Text.UTF8Encoding($false)

try {
    # Synthetische Artefakte (Pflichtmarker in Zeile 1).
    $clean = Join-Path $tmp "clean.md"
    [System.IO.File]::WriteAllText(
        $clean,
        "<!-- synthetic-test-only -->`n# synthetische Notiz`nGewoehnlicher Text.`n",
        $utf8)

    $store = Join-Path $tmp "store"

    # 1 — Scan ohne Speicherung (Exit 0 = READY_FOR_HUMAN_REVIEW).
    py -3.13 -m core.core_brain quarantine scan `
        --input $clean --policy $policy `
        --source-ref synthetic:demo-1 --synthetic-test-only
    Write-Output "scan_exit=$LASTEXITCODE"

    # 2 — Stage (genau ein Objekt und ein Record).
    $stageJson = py -3.13 -m core.core_brain quarantine stage `
        --input $clean --policy $policy `
        --source-ref synthetic:demo-1 --store $store --synthetic-test-only --json
    Write-Output "stage_exit=$LASTEXITCODE"
    $id = ($stageJson -join "`n" | ConvertFrom-Json).quarantine_id

    # 3 — Inspect (minimierte Metadaten, kein Pfad, kein Inhalt).
    py -3.13 -m core.core_brain quarantine inspect --store $store --id $id
    Write-Output "inspect_exit=$LASTEXITCODE"

    # 4 — Release verweigert immer (Exit 7).
    py -3.13 -m core.core_brain quarantine release --store $store --id $id
    Write-Output "release_exit=$LASTEXITCODE"
}
finally {
    Remove-Item -Recurse -Force $tmp
    Write-Output ("temp_remains=" + (Test-Path $tmp))
}
```

## Erwartete Exitcodes

| Kommando | Exit | Bedeutung |
| --- | ---: | --- |
| `quarantine scan` (clean) | 0 | `READY_FOR_HUMAN_REVIEW` |
| `quarantine scan` (E-Mail/Telefon) | 5 | `REVIEW_REQUIRED` |
| `quarantine scan` (Struktur/Credential/kein Marker) | 6 | `BLOCKED` |
| `quarantine stage` (clean) | 0 | ein Objekt + ein Record |
| `quarantine inspect` | 0 | minimierte Metadaten |
| `quarantine release` | 7 | verweigert immer |

`$LASTEXITCODE` unmittelbar nach jedem nativen Aufruf lesen. Die tatsächlichen
Exitcodes entscheiden.

## Grenzen

- Genau **eine** synthetische Markdown-Datei je Intake.
- Der Store liegt **außerhalb** des Core-Repositorys und wird nur temporär
  verwendet.
- Kein Ergebnisstatus bedeutet `approved`, `released`, `enabled` oder
  `indexed`.
- `quarantine release` gibt **nichts** frei und promotet **nichts**.
- Keine reale Quelle, kein reales Mapping, kein produktiver Ingest.
