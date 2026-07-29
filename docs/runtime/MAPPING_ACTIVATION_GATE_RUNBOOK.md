# Mapping Activation Gate Evaluator — Runbook (CBP-WP-016)

| Feld | Wert |
| --- | --- |
| **Status** | lokaler Prototyp · read-only · synthetic-only · **nicht produktiv** |
| Grundlage | D-050 (A0), PILOT_MAPPING_ACTIVATION_GATE.md (A3) |
| Shell | **ausschließlich PowerShell** |
| Stand | 2026-07-27 |

Dieser Runbook zeigt **ausschließlich** die lokale, synthetische Prüfung. Er ist
**keine** produktive Betriebsanleitung: er bindet keine reale Quelle an,
aktiviert nichts, gibt kein Gate frei und speichert nichts. Alle Daten sind
**synthetisch und temporär**, werden **UTF-8 ohne BOM** geschrieben und im
`finally`-Block entfernt.

> **UTF-8 ohne BOM:** Windows PowerShell 5.1 schreibt mit `Out-File -Encoding
> utf8` eine BOM, die fail-closed abgewiesen wird. Verwenden Sie
> `[System.IO.File]::WriteAllText($pfad, $text, (New-Object
> System.Text.UTF8Encoding($false)))`.

Da die Bindungshashes (Draft, Policy, Registry-Record) deterministisch aus der
kanonischen Darstellung gebildet werden, erzeugt ein kleiner **Python-Helfer**
(read-only) das synthetische Bündel. Der Helfer ist selbst ein `py -3.13`-Aufruf.

---

## Vollständiger Ablauf (PowerShell)

```powershell
$ErrorActionPreference = "Stop"
Set-Location -LiteralPath "D:\Projects\Core-Brain-Pilot"
$utf8 = New-Object System.Text.UTF8Encoding($false)   # UTF-8 OHNE BOM
$base = Join-Path $env:TEMP "cbp-wp016-runbook"
try {
    if (Test-Path $base) { Remove-Item -Recurse -Force $base }
    New-Item -ItemType Directory -Path $base | Out-Null

    # 1 — Synthetischen Fall erzeugen (read-only Helfer; schreibt nur in $base).
    $builder = Join-Path $base "build_case.py"
    $builderSrc = @'
import json, hashlib, sys
from pathlib import Path
from core.core_brain.mapping import load_policy
from core.core_brain.registry.models import RECORD_FIELDS
from core.core_brain.gate.models import canonical_json_bytes
from core.core_brain.gate.security_contract import (
    SECURITY_CONTRACT_REVISION, security_contract_sha256)

base = Path(sys.argv[1])
sid = "src-000000000000000000000000"
draft = {
  "schema_version":"1.0","mapping_id":"MAP-EXAMPLE-0001","slot_id":"PS-02",
  "mapping_name":"Beispiel Markdown Root","source_boundary_type":"markdown-root",
  "deployment_profile":"B","operator_reference":"role-operator-placeholder",
  "location_reference":"synthetic-placeholder-markdown-root",
  "location_reference_type":"local-directory","collection":"example-domain-alpha",
  "project":"example-project-alpha","enabled":False,"read_only":True,
  "allowed_subpaths":[],"excluded_subpaths":[],"follow_symlinks":False,
  "data_class":"internal","ai_transfer_policy":"forbidden",
  "local_search_policy":"forbidden","indexing_policy":"none",
  "mobile_visibility":"forbidden","revision_strategy":"content-hash",
  "deletion_behavior":"tombstone-and-cleanup","verification_status":"unverified",
  "approval_status":"not-approved","approved_by":None,"approved_at":None,
  "mapping_revision":1,"previous_revision":None,"credential_reference":None,
  "notes":"Synthetisches Beispiel. Nicht aktivieren.",
}
rec = {k:"x" for k in RECORD_FIELDS}
rec.update({"record_schema_version":"1.0","source_id":sid,"namespace":"synthetic-ns",
  "source_key":"notes-alpha","display_name":"Synthetic Notes",
  "collection_key":"example-domain-alpha","domain_key":"example-domain",
  "source_kind":"markdown","data_class":"internal","ai_eligibility":"restricted",
  "owner_role":"operator","source_reference":"synthetic:notes",
  "definition_sha256":"0"*64,"policy_sha256":"0"*64,
  "lifecycle_state":"REGISTERED_DISABLED","registered_at":"2026-07-27T00:00:00Z",
  "implementation_version":"0.1.0.dev0"})
reg = base/"registry"; (reg/"records").mkdir(parents=True)
(reg/"records"/f"{sid}.json").write_text(
    json.dumps(rec,sort_keys=True,ensure_ascii=False,indent=2)+"\n", encoding="utf-8")
raw = json.dumps(draft).encode("utf-8")
(base/"draft.json").write_bytes(raw)
policy = load_policy(Path("config/source_mapping_validation_policy.example.toml"))
# Evidence-Bundle 3.0 (CBP-WP-018) — hier ohne eingebettete Artefakte
# (leere Listen zulaessig); der Ausgang bleibt BLOCKED (Exit 14). Ohne
# Security-Control-Artefakte sind alle elf Bindungen MISSING.
ev = {"evidence_schema_version":"3.0","synthetic_test_only":True,"source_id":sid,
  "mapping_id":"MAP-EXAMPLE-0001","gate_contract_revision":"1.0",
  "evidence_contract_revision":"3.0","evidence_revision":1,
  "security_contract_revision":SECURITY_CONTRACT_REVISION,
  "security_contract_sha256":security_contract_sha256(),
  "mapping_draft_sha256":hashlib.sha256(raw).hexdigest(),
  "mapping_policy_sha256":policy.policy_sha256,
  "registry_record_sha256":hashlib.sha256(canonical_json_bytes(rec)).hexdigest(),
  "criterion_evidence":[{"criterion":i,"artifacts":[]} for i in range(1,21)]}
(base/"evidence.json").write_text(json.dumps(ev), encoding="utf-8")
print(sid)
'@
    [System.IO.File]::WriteAllText($builder, $builderSrc, $utf8)
    $sid = (py -3.13 $builder $base).Trim()
    $reg   = Join-Path $base "registry"
    $draft = Join-Path $base "draft.json"
    $ev    = Join-Path $base "evidence.json"
    $mpol  = "config\source_mapping_validation_policy.example.toml"

    # 2 — Registry-Bytes VOR den Gate-Befehlen hashen
    $before = (Get-ChildItem -Recurse -File $reg | Sort-Object FullName | ForEach-Object { (Get-FileHash $_.FullName -Algorithm SHA256).Hash }) -join "|"

    # 3 — activation-evaluate (menschenlesbar) — erwartet Exit 14, BLOCKED
    py -3.13 -m core.core_brain source-mapping activation-evaluate --draft $draft --policy $mpol --registry $reg --source-id $sid --evidence $ev --synthetic-test-only
    Write-Host "evaluate exit=$LASTEXITCODE"

    # 4 — activation-evaluate (JSON) — erwartet Exit 14
    py -3.13 -m core.core_brain source-mapping activation-evaluate --draft $draft --policy $mpol --registry $reg --source-id $sid --evidence $ev --synthetic-test-only --json
    Write-Host "evaluate-json exit=$LASTEXITCODE"

    # 5 — Kontrolle: run bleibt Exit 4
    py -3.13 -m core.core_brain run --config config\runtime.example.toml | Out-Null
    Write-Host "run exit=$LASTEXITCODE"

    # 6 — Registry-Bytes NACH den Gate-Befehlen hashen und vergleichen
    $after = (Get-ChildItem -Recurse -File $reg | Sort-Object FullName | ForEach-Object { (Get-FileHash $_.FullName -Algorithm SHA256).Hash }) -join "|"
    if ($before -eq $after) { Write-Host "REGISTRY_BYTE_IDENTICAL=TRUE" } else { Write-Host "REGISTRY_BYTE_IDENTICAL=FALSE" }
}
finally {
    if (Test-Path $base) { Remove-Item -Recurse -Force $base }
    if (Test-Path $base) { Write-Host "CLEANUP=FALSE" } else { Write-Host "CLEANUP=TRUE" }
}
```

## Erwartete Ausgänge

| Schritt | Erwarteter `$LASTEXITCODE` |
| --- | --- |
| `activation-evaluate` (gültiger synthetischer Fall) | **14** (`BLOCKED`) |
| `activation-evaluate --json` | **14** |
| `run` | **4** (unverändert) |
| Registry-Bytevergleich | `REGISTRY_BYTE_IDENTICAL=TRUE` |
| Cleanup | `CLEANUP=TRUE` |

Der Report zeigt `evaluation_status: BLOCKED`, 20 Kriterienresultate (davon 16
blockierend) und den festen Nichtautorisierungshinweis.

## Aussagegrenzen

**Exitcode 14 bedeutet ausschließlich** eine ausgeführte, fail-closed
Review-Bereitschaftsprüfung mit Ergebnis `BLOCKED` — **nicht** approved,
activated, ingestible, indexed oder retrievable. Der Report ist **A6** und
**keine** Gatefreigabe. Dieser Ablauf ist **synthetic-only** und **nicht
produktiv**; **Mapping Activation Gate**, **Security Foundation Readiness Gate**
und **DRC** bleiben `NOT EVALUATED`.
