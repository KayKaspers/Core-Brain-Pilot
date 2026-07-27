"""Tests der externen, read-only Registry-Bindung (CBP-WP-015, Faelle 63-73).

Die Registry wird ausschliesslich gelesen. Verglichen werden nur ``collection``
gegen ``collection_key`` (exakt) und ``data_class`` gegen ``data_class``
(exakt). Es gibt **keinen** project/domain- und **keinen**
ai_transfer/ai_eligibility-Crosswalk.
"""

from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from core.core_brain.mapping import load_policy, run_validate
from core.core_brain.mapping.models import MappingReasonCode as R
from core.core_brain.mapping.models import ValidationStatus
from core.core_brain.registry.models import RECORD_FIELDS

REPO_ROOT = Path(__file__).resolve().parent.parent
POLICY = load_policy(
    REPO_ROOT / "config" / "source_mapping_validation_policy.example.toml"
)
SOURCE_ID = "src-0123456789abcdef01234567"
EVENT_ID = "evt-fedcba9876543210fedcba98"
SOURCE_REF = "synthetic:notes-ref-marker"


def valid_draft() -> dict[str, object]:
    return {
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
            "source_reference": SOURCE_REF,
            "definition_sha256": "0" * 64,
            "policy_sha256": "0" * 64,
            "lifecycle_state": "REGISTERED_DISABLED",
            "registered_at": "2026-07-27T00:00:00Z",
            "implementation_version": "0.1.0.dev0",
        }
    )
    data.update(over)
    return data


def write_registry(root: Path, *, record: dict[str, object] | str | None,
                   retired: bool = False) -> None:
    (root / "records").mkdir(parents=True, exist_ok=True)
    if record is not None:
        target = root / "records" / f"{SOURCE_ID}.json"
        if isinstance(record, str):
            target.write_text(record, encoding="utf-8")  # bewusst korrupt
        else:
            target.write_text(
                json.dumps(record, sort_keys=True, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
    if retired:
        events = root / "events" / SOURCE_ID
        events.mkdir(parents=True, exist_ok=True)
        (events / f"{EVENT_ID}.json").write_text('{"event": "RETIRED"}', encoding="utf-8")


def _run(root: Path, draft: dict[str, object], source_id: str = SOURCE_ID):
    with tempfile.TemporaryDirectory() as tmp:
        draft_path = Path(tmp) / "draft.json"
        draft_path.write_text(json.dumps(draft), encoding="utf-8")
        return run_validate(
            draft_path=draft_path, policy=POLICY, registry_root=root,
            source_id=source_id, synthetic_confirmed=True,
        )


def _hash_tree(root: Path) -> list[tuple[str, str]]:
    result: list[tuple[str, str]] = []
    for path in sorted(root.rglob("*")):
        if path.is_file():
            rel = path.relative_to(root).as_posix()
            result.append((rel, hashlib.sha256(path.read_bytes()).hexdigest()))
    return result


class TestRegistryBinding(unittest.TestCase):
    def test_63_registered_disabled_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "reg"
            write_registry(root, record=record_dict())
            report = _run(root, valid_draft())
        self.assertEqual(report.validation_status, ValidationStatus.VALID_DRAFT)

    def test_64_unknown_source_id_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "reg"
            (root / "records").mkdir(parents=True)
            report = _run(root, valid_draft())
        self.assertIn(R.REGISTRY_NOT_FOUND.value, report.reason_codes)

    def test_65_invalid_source_id_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "reg"
            write_registry(root, record=record_dict())
            report = _run(root, valid_draft(), source_id="not-a-valid-source-id")
        self.assertIn(R.SOURCE_ID_INVALID.value, report.reason_codes)

    def test_66_corrupted_record_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "reg"
            write_registry(root, record="{ this is not valid json ")
            report = _run(root, valid_draft())
        self.assertIn(R.REGISTRY_RECORD_INVALID.value, report.reason_codes)

    def test_66b_record_field_mismatch_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "reg"
            bad = record_dict()
            del bad["owner_role"]
            write_registry(root, record=bad)
            report = _run(root, valid_draft())
        self.assertIn(R.REGISTRY_RECORD_INVALID.value, report.reason_codes)

    def test_67_retired_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "reg"
            write_registry(root, record=record_dict(), retired=True)
            report = _run(root, valid_draft())
        self.assertIn(R.REGISTRY_RETIRED.value, report.reason_codes)

    def test_68_non_synthetic_source_reference_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "reg"
            write_registry(root, record=record_dict(source_reference="real-source-x"))
            report = _run(root, valid_draft())
        self.assertIn(R.SOURCE_REF_NOT_SYNTHETIC.value, report.reason_codes)

    def test_69_collection_mismatch_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "reg"
            write_registry(root, record=record_dict(collection_key="other-collection"))
            report = _run(root, valid_draft())
        self.assertIn(R.COLLECTION_MISMATCH.value, report.reason_codes)

    def test_70_data_class_mismatch_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "reg"
            write_registry(root, record=record_dict(data_class="public"))
            report = _run(root, valid_draft())
        self.assertIn(R.DATA_CLASS_MISMATCH.value, report.reason_codes)

    def test_71_project_not_compared_with_domain(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "reg"
            # Abweichende domain_key/namespace duerfen NICHT blockieren.
            write_registry(
                root,
                record=record_dict(domain_key="totally-different", namespace="other-ns"),
            )
            report = _run(root, valid_draft())
        self.assertEqual(report.validation_status, ValidationStatus.VALID_DRAFT)

    def test_72_ai_transfer_not_compared_with_ai_eligibility(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "reg"
            # ai_eligibility abweichend; ai_transfer_policy bleibt forbidden.
            write_registry(root, record=record_dict(ai_eligibility="allowed"))
            report = _run(root, valid_draft())
        self.assertEqual(report.validation_status, ValidationStatus.VALID_DRAFT)

    def test_73_registry_stays_byte_identical(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "reg"
            write_registry(root, record=record_dict(), retired=False)
            before = _hash_tree(root)
            _run(root, valid_draft())
            _run(root, valid_draft())
            after = _hash_tree(root)
        self.assertEqual(before, after)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
