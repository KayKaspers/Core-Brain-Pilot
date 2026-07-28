"""Gemeinsame synthetische Fixtures fuer die CBP-WP-016-Gate-Tests.

Dieses Modul ist **kein** Testmodul (Muster ``test_*.py``) und wird nicht
gesammelt. Es liefert ausschliesslich synthetische, temporaere Daten: keine
realen Quellen, keine realen Pfade oder URLs, keine echten Secrets.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from core.core_brain.gate.models import canonical_json_bytes
from core.core_brain.mapping import load_policy
from core.core_brain.registry.models import RECORD_FIELDS

REPO_ROOT = Path(__file__).resolve().parent.parent
POLICY_PATH = REPO_ROOT / "config" / "source_mapping_validation_policy.example.toml"
SOURCE_ID = "src-0123456789abcdef01234567"
MAPPING_ID = "MAP-EXAMPLE-0001"


def valid_draft() -> dict[str, object]:
    """Ein gueltiger, synthetischer, deaktivierter 31-Feld-Entwurf (PS-02)."""
    return {
        "schema_version": "1.0",
        "mapping_id": MAPPING_ID,
        "slot_id": "PS-02",
        "mapping_name": "Beispiel Markdown Root",
        "source_boundary_type": "markdown-root",
        "deployment_profile": "B",
        "operator_reference": "role-operator-placeholder",
        "location_reference": "synthetic-placeholder-markdown-root",
        "location_reference_type": "local-directory",
        "collection": "example-domain-alpha",
        "project": "example-project-alpha",
        "enabled": False,
        "read_only": True,
        "allowed_subpaths": [],
        "excluded_subpaths": [],
        "follow_symlinks": False,
        "data_class": "internal",
        "ai_transfer_policy": "forbidden",
        "local_search_policy": "forbidden",
        "indexing_policy": "none",
        "mobile_visibility": "forbidden",
        "revision_strategy": "content-hash",
        "deletion_behavior": "tombstone-and-cleanup",
        "verification_status": "unverified",
        "approval_status": "not-approved",
        "approved_by": None,
        "approved_at": None,
        "mapping_revision": 1,
        "previous_revision": None,
        "credential_reference": None,
        "notes": "Synthetisches Beispiel. Nicht aktivieren.",
    }


def record_dict(**over: object) -> dict[str, object]:
    data = {key: "x" for key in RECORD_FIELDS}
    data.update(
        {
            "record_schema_version": "1.0",
            "source_id": SOURCE_ID,
            "namespace": "synthetic-ns",
            "source_key": "notes-alpha",
            "display_name": "Synthetic Notes",
            "collection_key": "example-domain-alpha",
            "domain_key": "example-domain",
            "source_kind": "markdown",
            "data_class": "internal",
            "ai_eligibility": "restricted",
            "owner_role": "operator",
            "source_reference": "synthetic:notes-ref-marker",
            "definition_sha256": "0" * 64,
            "policy_sha256": "0" * 64,
            "lifecycle_state": "REGISTERED_DISABLED",
            "registered_at": "2026-07-27T00:00:00Z",
            "implementation_version": "0.1.0.dev0",
        }
    )
    data.update(over)
    return data


def write_registry(root: Path, record: dict[str, object], *, retired: bool = False) -> None:
    (root / "records").mkdir(parents=True, exist_ok=True)
    (root / "records" / f"{SOURCE_ID}.json").write_text(
        json.dumps(record, sort_keys=True, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    if retired:
        events = root / "events" / SOURCE_ID
        events.mkdir(parents=True, exist_ok=True)
        (events / f"evt-{'a' * 24}.json").write_text('{"e":"RETIRED"}', encoding="utf-8")


def evidence_bundle(*, draft_sha256: str, policy_sha256: str, record_sha256: str,
                    **over: object) -> dict[str, object]:
    bundle: dict[str, object] = {
        "evidence_schema_version": "1.0",
        "synthetic_test_only": True,
        "source_id": SOURCE_ID,
        "mapping_id": MAPPING_ID,
        "gate_contract_revision": "1.0",
        "evidence_revision": 1,
        "mapping_draft_sha256": draft_sha256,
        "mapping_policy_sha256": policy_sha256,
        "registry_record_sha256": record_sha256,
        "criterion_evidence": [
            {"criterion": i, "evidence_ref": None} for i in range(1, 21)
        ],
    }
    bundle.update(over)
    return bundle


def build_case(tmp: str, *, draft: dict[str, object] | None = None,
               record: dict[str, object] | None = None,
               retired: bool = False,
               evidence_overrides: dict[str, object] | None = None):
    """Legt eine vollstaendige synthetische Fixture an und gibt Pfade zurueck."""
    root = Path(tmp) / "registry"
    rec = record if record is not None else record_dict()
    write_registry(root, rec, retired=retired)

    draft_obj = draft if draft is not None else valid_draft()
    draft_path = Path(tmp) / "draft.json"
    raw = json.dumps(draft_obj).encode("utf-8")
    draft_path.write_bytes(raw)

    policy = load_policy(POLICY_PATH)
    draft_sha = hashlib.sha256(raw).hexdigest()
    record_sha = hashlib.sha256(canonical_json_bytes(rec)).hexdigest()

    bundle = evidence_bundle(
        draft_sha256=draft_sha,
        policy_sha256=policy.policy_sha256,
        record_sha256=record_sha,
        **(evidence_overrides or {}),
    )
    evidence_path = Path(tmp) / "evidence.json"
    evidence_path.write_text(json.dumps(bundle), encoding="utf-8")

    return {
        "root": root,
        "draft_path": draft_path,
        "evidence_path": evidence_path,
        "policy": policy,
        "policy_path": POLICY_PATH,
        "draft_sha256": draft_sha,
        "record_sha256": record_sha,
        "source_id": SOURCE_ID,
    }
