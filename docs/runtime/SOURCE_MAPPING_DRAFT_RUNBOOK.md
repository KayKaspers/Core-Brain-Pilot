# Source Mapping Draft Validator — Runbook (CBP-WP-015)

| Feld | Wert |
| --- | --- |
| **Status** | lokaler Prototyp · read-only · synthetic-only · **nicht produktiv** |
| Grundlage | ADR-0012 (A1) |
| Shell | **ausschließlich PowerShell** |
| Stand | 2026-07-27 |

Dieser Runbook zeigt **ausschließlich** die lokale, synthetische Prüfung. Er ist
**keine** produktive Betriebsanleitung: er bindet keine reale Quelle an,
aktiviert nichts und speichert nichts. Alle Beispieldaten sind **synthetisch und
temporär**, werden **UTF-8 ohne BOM** geschrieben und im `finally`-Block wieder
entfernt.

> **Wichtig — UTF-8 ohne BOM:** Windows PowerShell 5.1 schreibt mit
> `Out-File -Encoding utf8` eine **BOM**. Der Registry- und der Mapping-Parser
> lehnen eine BOM fail-closed ab. Verwenden Sie daher
> `[System.IO.File]::WriteAllText($pfad, $text, (New-Object System.Text.UTF8Encoding($false)))`.

---

## Vollständiger Ablauf (PowerShell)

```powershell
$ErrorActionPreference = "Stop"
Set-Location "D:\Projects\Core-Brain-Pilot"
$utf8 = New-Object System.Text.UTF8Encoding($false)   # UTF-8 OHNE BOM
$base = Join-Path $env:TEMP "cbp-wp015-runbook"
try {
    if (Test-Path $base) { Remove-Item -Recurse -Force $base }
    New-Item -ItemType Directory -Path $base | Out-Null
    $reg   = Join-Path $base "registry"
    $def   = Join-Path $base "def.toml"
    $draft = Join-Path $base "draft.json"
    $mpol  = "config\source_mapping_validation_policy.example.toml"
    $rpol  = "config\source_registry_policy.example.toml"

    # 1 — synthetische Source-Definition (collection/data_class = Draft)
    $defText = @'
schema_version = "1.0"
namespace = "synthetic-ns"
source_key = "notes-alpha"
display_name = "Synthetic Notes"
collection_key = "example-domain-alpha"
domain_key = "example-domain"
source_kind = "markdown"
data_class = "internal"
ai_eligibility = "restricted"
owner_role = "operator"
source_reference = "synthetic:notes-alpha"
synthetic_test_only = true
activation_enabled = false
content_access_enabled = false
network_enabled = false
'@
    [System.IO.File]::WriteAllText($def, $defText, $utf8)

    # 2 — synthetischer, deaktivierter 31-Feld-Entwurf (PS-02)
    $draftText = @'
{
  "schema_version": "1.0",
  "mapping_id": "MAP-EXAMPLE-0001",
  "slot_id": "PS-02",
  "mapping_name": "Beispiel Markdown Root",
  "source_boundary_type": "markdown-root",
  "deployment_profile": "B",
  "operator_reference": "role-operator-placeholder",
  "location_reference": "synthetic-placeholder-markdown-root",
  "location_reference_type": "local-directory",
  "collection": "example-domain-alpha",
  "project": "example-project-alpha",
  "enabled": false,
  "read_only": true,
  "allowed_subpaths": [],
  "excluded_subpaths": [],
  "follow_symlinks": false,
  "data_class": "internal",
  "ai_transfer_policy": "forbidden",
  "local_search_policy": "forbidden",
  "indexing_policy": "none",
  "mobile_visibility": "forbidden",
  "revision_strategy": "content-hash",
  "deletion_behavior": "tombstone-and-cleanup",
  "verification_status": "unverified",
  "approval_status": "not-approved",
  "approved_by": null,
  "approved_at": null,
  "mapping_revision": 1,
  "previous_revision": null,
  "credential_reference": null,
  "notes": "Synthetisches Beispiel. Nicht aktivieren."
}
'@
    [System.IO.File]::WriteAllText($draft, $draftText, $utf8)

    # 3 — synthetische Registry anlegen; Source ID uebernehmen
    $sid = (python -m core.core_brain source-registry register --definition $def --policy $rpol --registry $reg --synthetic-test-only --json | ConvertFrom-Json).source_id
    Write-Host "register exit=$LASTEXITCODE source_id=$sid"

    # 4 — Registry-Bytes VOR den Mapping-Befehlen hashen
    $before = (Get-ChildItem -Recurse -File $reg | Sort-Object FullName | ForEach-Object { (Get-FileHash $_.FullName -Algorithm SHA256).Hash }) -join "|"

    # 5 — validate-draft (menschenlesbar) — erwartet Exit 0
    python -m core.core_brain source-mapping validate-draft --draft $draft --policy $mpol --registry $reg --source-id $sid --synthetic-test-only
    Write-Host "validate exit=$LASTEXITCODE"

    # 6 — validate-draft (JSON) — erwartet Exit 0
    python -m core.core_brain source-mapping validate-draft --draft $draft --policy $mpol --registry $reg --source-id $sid --synthetic-test-only --json
    Write-Host "validate-json exit=$LASTEXITCODE"

    # 7 — activation-check — erwartet Exit 13 (verweigert immer)
    python -m core.core_brain source-mapping activation-check --draft $draft --policy $mpol --registry $reg --source-id $sid --synthetic-test-only
    Write-Host "activation-check exit=$LASTEXITCODE"

    # 8 — Kontrolle: run bleibt Exit 4
    python -m core.core_brain run --config config\runtime.example.toml | Out-Null
    Write-Host "run exit=$LASTEXITCODE"

    # 9 — Registry-Bytes NACH den Mapping-Befehlen hashen und vergleichen
    $after = (Get-ChildItem -Recurse -File $reg | Sort-Object FullName | ForEach-Object { (Get-FileHash $_.FullName -Algorithm SHA256).Hash }) -join "|"
    if ($before -eq $after) { Write-Host "REGISTRY_BYTE_IDENTICAL=TRUE" } else { Write-Host "REGISTRY_BYTE_IDENTICAL=FALSE" }
}
finally {
    # 10 — Cleanup der synthetischen temporaeren Daten
    if (Test-Path $base) { Remove-Item -Recurse -Force $base }
    if (Test-Path $base) { Write-Host "CLEANUP=FALSE" } else { Write-Host "CLEANUP=TRUE" }
}
```

## Erwartete Ausgänge

| Schritt | Erwarteter `$LASTEXITCODE` |
| --- | --- |
| `source-registry register` | 0 |
| `validate-draft` (gültiger synthetischer Draft) | **0** (`VALID_DRAFT`) |
| `validate-draft --json` | **0** |
| `activation-check` | **13** (verweigert immer) |
| `run` | **4** (unverändert) |
| Registry-Bytevergleich | `REGISTRY_BYTE_IDENTICAL=TRUE` |
| Cleanup | `CLEANUP=TRUE` |

Ein blockierter Draft (z. B. `enabled=true`) liefert **Exit 12** und
`validation_status: BLOCKED` mit einem stabilen `MAP-*`-Reason-Code.

## Aussagegrenzen

**Exitcode 0 bedeutet ausschließlich** Vertragskonformität eines synthetischen
Entwurfs — **nicht** approved, mapped, activated, ingestible, indexed oder
retrievable. Dieser Ablauf ist **synthetic-only** und **nicht produktiv**;
**Mapping Activation Gate**, **Security Foundation Readiness Gate** und **DRC**
bleiben `NOT EVALUATED`.
