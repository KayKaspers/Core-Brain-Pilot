# Source Registry MVP — Runbook (PowerShell)

| Feld | Wert |
| --- | --- |
| Erfasst in | **CBP-WP-014** |
| Autoritätsklasse | A2 (Betriebsleitfaden des Prototyps) |
| Stand | 2026-07-22 |

> **synthetic · non-operational · test-only.** Dieses Runbook ist **keine**
> produktive Betriebsanleitung. Es verwendet ausschließlich **synthetische**
> temporäre Metadaten und räumt vollständig in einem `finally`-Block auf. Alle
> Befehle sind **PowerShell**.

---

## Voraussetzungen

- Python 3.13 oder neuer, aufrufbar über `py -3.13`.
- Arbeitsverzeichnis `D:\Projects\Core-Brain-Pilot`.
- Keine Installation, keine Abhängigkeiten.

## Vollständiges, selbstaufräumendes Beispiel

BOM-freies UTF-8 über `System.Text.UTF8Encoding($false)`; vollständiges Cleanup
im `finally`-Block.

```powershell
$repo = "D:\Projects\Core-Brain-Pilot"
Set-Location $repo
$policy = "config\source_registry_policy.example.toml"

$tmp = Join-Path $env:TEMP ("cbp-wp014-" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $tmp | Out-Null
$utf8 = New-Object System.Text.UTF8Encoding($false)

try {
    # Synthetische Definition (nur Metadaten, kein Pfad, keine URL).
    $def = Join-Path $tmp "definition.toml"
    $lines = @(
        'schema_version = "1.0"',
        'namespace = "synthetic-demo"',
        'source_key = "notes-alpha"',
        'display_name = "Synthetische Notizsammlung Alpha"',
        'collection_key = "demo-collection"',
        'domain_key = "demo-domain"',
        'source_kind = "markdown"',
        'data_class = "internal"',
        'ai_eligibility = "restricted"',
        'owner_role = "operator"',
        'source_reference = "synthetic:demo-notes-alpha"',
        'synthetic_test_only = true',
        'activation_enabled = false',
        'content_access_enabled = false',
        'network_enabled = false'
    )
    [System.IO.File]::WriteAllText($def, ($lines -join "`n") + "`n", $utf8)

    $registry = Join-Path $tmp "registry"

    # 1 — Definition validieren (Exit 0).
    py -3.13 -m core.core_brain source-registry validate-definition `
        --definition $def --policy $policy
    Write-Output "validate_exit=$LASTEXITCODE"

    # 2 — Registrieren (Zustand REGISTERED_DISABLED).
    $regJson = py -3.13 -m core.core_brain source-registry register `
        --definition $def --policy $policy --registry $registry `
        --synthetic-test-only --json
    Write-Output "register_exit=$LASTEXITCODE"
    $id = ($regJson -join "`n" | ConvertFrom-Json).source_id

    # 3 — Katalog auflisten (minimiert).
    py -3.13 -m core.core_brain source-registry list --registry $registry
    Write-Output "list_exit=$LASTEXITCODE"

    # 4 — Record inspizieren (minimiert, kein Registry-Pfad).
    py -3.13 -m core.core_brain source-registry inspect --registry $registry --id $id
    Write-Output "inspect_exit=$LASTEXITCODE"

    # 5 — Retirement (append-only, keine Löschung).
    py -3.13 -m core.core_brain source-registry retire --registry $registry --id $id `
        --synthetic-test-only
    Write-Output "retire_exit=$LASTEXITCODE"

    # 6 — Aktivierung verweigert immer (Exit 11).
    py -3.13 -m core.core_brain source-registry activate --registry $registry --id $id
    Write-Output "activate_exit=$LASTEXITCODE"
}
finally {
    Remove-Item -Recurse -Force $tmp
    Write-Output ("temp_remains=" + (Test-Path $tmp))
}
```

## Erwartete Exitcodes

| Kommando | Exit | Bedeutung |
| --- | ---: | --- |
| `validate-definition` (gültig) | 0 | strukturell valide |
| `register` (gültig) | 0 | `REGISTERED_DISABLED` |
| `list` / `inspect` | 0 | minimierte Metadaten |
| `retire` (gültig) | 0 | `RETIRED`, append-only Event |
| Synthetic-Grenze verletzt / ungültige Definition | 8 | blockiert |
| abweichende Definition derselben Identität | 9 | Konflikt |
| unbekannte Source ID | 10 | nicht gefunden |
| `activate` | 11 | verweigert immer |

`$LASTEXITCODE` unmittelbar nach jedem nativen Aufruf lesen. Die tatsächlichen
Exitcodes entscheiden.

## Grenzen

- Ausschließlich synthetische Metadaten; keine realen Quellen, Pfade oder URLs.
- Der Registry-Root liegt **außerhalb** des Core-Repositorys und wird nur
  temporär verwendet.
- Kein Zustand bedeutet `approved`, `mapped`, `activated`, `ingestible`,
  `indexed` oder `retrievable`.
- `activate` erzeugt **kein** Source Mapping und **keine** Aktivierung.
