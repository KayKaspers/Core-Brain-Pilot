"""Gemeinsame synthetische Fixtures fuer die CBP-WP-016/017-Gate-Tests.

Dieses Modul ist **kein** Testmodul (Muster ``test_*.py``) und wird nicht
gesammelt. Es liefert ausschliesslich synthetische, temporaere Daten: keine
realen Quellen, keine realen Pfade oder URLs, keine echten Secrets.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from core.core_brain.gate import (
    CRITERION_PRODUCER_CLASS,
    EVIDENCE_CONTRACT_REVISION,
    EVIDENCE_SCHEMA_VERSION,
    GATE_CONTRACT_REVISION,
    canonical_artifact_sha256,
    canonical_binding_sha256,
    evidence_contract_sha256,
    gate_contract_sha256,
)
from core.core_brain.gate.models import canonical_json_bytes
from core.core_brain.mapping import load_policy
from core.core_brain.registry.models import RECORD_FIELDS

REPO_ROOT = Path(__file__).resolve().parent.parent
POLICY_PATH = REPO_ROOT / "config" / "source_mapping_validation_policy.example.toml"
SOURCE_ID = "src-0123456789abcdef01234567"
MAPPING_ID = "MAP-EXAMPLE-0001"
ART_ID_A = "art-0123456789abcdef01234567"
ART_ID_B = "art-89abcdef0123456789abcdef"


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


def fresh_binding(
    criterion: int,
    *,
    draft_sha: str,
    policy_sha: str,
    record_sha: str | None,
    evidence_revision: int = 1,
    source_id: str = SOURCE_ID,
    mapping_id: str = MAPPING_ID,
    **override: object,
) -> str:
    """Berechnet die aktuelle kanonische Kriteriumsbindung (mit optionalem Drift)."""
    params: dict[str, object] = dict(
        source_id=source_id,
        mapping_id=mapping_id,
        criterion=criterion,
        mapping_draft_sha256=draft_sha,
        mapping_policy_sha256=policy_sha,
        registry_record_sha256=record_sha,
        gate_contract_revision=GATE_CONTRACT_REVISION,
        gate_contract_sha256=gate_contract_sha256(),
        evidence_contract_revision=EVIDENCE_CONTRACT_REVISION,
        evidence_contract_sha256=evidence_contract_sha256(),
        evidence_revision=evidence_revision,
    )
    params.update(override)
    return canonical_binding_sha256(**params)  # type: ignore[arg-type]


def make_artifact(
    criterion: int,
    *,
    draft_sha: str,
    policy_sha: str,
    record_sha: str | None,
    evidence_revision: int = 1,
    artifact_id: str = ART_ID_A,
    producer_class: str | None = None,
    binding_override: dict[str, object] | None = None,
    binding_sha256: str | None = None,
    art_rev: int | None = None,
    corrupt_hash: bool = False,
    synthetic: bool = True,
) -> dict[str, object]:
    """Baut ein synthetisches Artefakt (frisch oder gezielt fehlerhaft)."""
    pc = producer_class if producer_class is not None else CRITERION_PRODUCER_CLASS[criterion]
    bo = dict(binding_override or {})
    binding = binding_sha256 if binding_sha256 is not None else fresh_binding(
        criterion,
        draft_sha=draft_sha,
        policy_sha=policy_sha,
        record_sha=record_sha,
        evidence_revision=bo.pop("evidence_revision", evidence_revision),
        **bo,
    )
    rev = art_rev if art_rev is not None else evidence_revision
    sha = canonical_artifact_sha256(
        artifact_id=artifact_id,
        binding_sha256=binding,
        producer_class=pc,
        evidence_revision=rev,
        synthetic_test_only=synthetic,
    )
    if corrupt_hash:
        sha = "f" * 64 if sha != "f" * 64 else "e" * 64
    return {
        "artifact_id": artifact_id,
        "artifact_sha256": sha,
        "binding_sha256": binding,
        "producer_class": pc,
        "evidence_revision": rev,
        "synthetic_test_only": synthetic,
    }


def evidence_bundle(
    *,
    draft_sha256: str,
    policy_sha256: str,
    record_sha256: str | None,
    evidence_revision: int = 1,
    artifacts_by_criterion: dict[int, list] | None = None,
    **over: object,
) -> dict[str, object]:
    abc = artifacts_by_criterion or {}
    ce = [{"criterion": i, "artifacts": list(abc.get(i, []))} for i in range(1, 21)]
    bundle: dict[str, object] = {
        "evidence_schema_version": EVIDENCE_SCHEMA_VERSION,
        "synthetic_test_only": True,
        "source_id": SOURCE_ID,
        "mapping_id": MAPPING_ID,
        "gate_contract_revision": GATE_CONTRACT_REVISION,
        "evidence_contract_revision": EVIDENCE_CONTRACT_REVISION,
        "evidence_revision": evidence_revision,
        "mapping_draft_sha256": draft_sha256,
        "mapping_policy_sha256": policy_sha256,
        "registry_record_sha256": record_sha256,
        "criterion_evidence": ce,
    }
    bundle.update(over)
    return bundle


def build_case(tmp: str, *, draft: dict[str, object] | None = None,
               record: dict[str, object] | None = None,
               retired: bool = False,
               evidence_overrides: dict[str, object] | None = None,
               artifact_specs: dict[int, list[dict]] | None = None,
               evidence_revision: int = 1):
    """Legt eine vollstaendige synthetische Fixture an und gibt Pfade zurueck.

    ``artifact_specs`` bildet ``criterion -> Liste von make_artifact-kwargs`` ab;
    die tatsaechlichen Hashes (draft/policy/record) werden hier injiziert.
    """
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

    abc: dict[int, list] = {}
    for cid, specs in (artifact_specs or {}).items():
        abc[cid] = [
            make_artifact(
                cid,
                draft_sha=draft_sha,
                policy_sha=policy.policy_sha256,
                record_sha=record_sha,
                evidence_revision=evidence_revision,
                **spec,
            )
            for spec in specs
        ]

    bundle = evidence_bundle(
        draft_sha256=draft_sha,
        policy_sha256=policy.policy_sha256,
        record_sha256=record_sha,
        evidence_revision=evidence_revision,
        artifacts_by_criterion=abc,
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
