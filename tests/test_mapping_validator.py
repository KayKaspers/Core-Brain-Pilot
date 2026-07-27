"""Tests der Vertrags-, Sicherheits- und Reportlogik (CBP-WP-015).

Deckt die Faelle 29-39 (Vertrag und Sicherheit), 60-62 (mapping_id) und 74-90
(Report) ab. Der Validator berechnet ``mapping_id`` **nicht** und **speichert
nichts**.
"""

from __future__ import annotations

import hashlib
import json
import re
import tempfile
import unittest
from pathlib import Path

from core.core_brain.mapping import (
    load_policy,
    mapping_id_of,
    present_field_count,
    run_validate,
    validate_contract_and_state,
)
from core.core_brain.mapping.models import MappingReasonCode as R
from core.core_brain.mapping.models import ValidationStatus
from core.core_brain.registry.models import RECORD_FIELDS

REPO_ROOT = Path(__file__).resolve().parent.parent
POLICY = load_policy(
    REPO_ROOT / "config" / "source_mapping_validation_policy.example.toml"
)
REQUIRED_29 = [
    "schema_version", "mapping_id", "slot_id", "mapping_name",
    "source_boundary_type", "deployment_profile", "operator_reference",
    "location_reference", "location_reference_type", "collection", "project",
    "enabled", "read_only", "allowed_subpaths", "excluded_subpaths",
    "follow_symlinks", "data_class", "ai_transfer_policy", "local_search_policy",
    "indexing_policy", "mobile_visibility", "revision_strategy",
    "deletion_behavior", "verification_status", "approval_status",
    "approved_by", "approved_at", "mapping_revision", "previous_revision",
]


def valid_draft() -> dict[str, object]:
    """Ein gueltiger, synthetischer, deaktivierter 31-Feld-Entwurf (PS-02)."""
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


SOURCE_ID = "src-0123456789abcdef01234567"
SOURCE_REF = "synthetic:notes-ref-marker"


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


def _write_registry(root: Path, **record_over: object) -> None:
    (root / "records").mkdir(parents=True, exist_ok=True)
    payload = json.dumps(
        record_dict(**record_over), sort_keys=True, ensure_ascii=False, indent=2
    ) + "\n"
    (root / "records" / f"{SOURCE_ID}.json").write_text(payload, encoding="utf-8")


class TestContractAndSafety(unittest.TestCase):
    """Faelle 29-39 — Vertrag, Typen, Pfade, URLs, Traversal, Inhalt, Secrets."""

    def test_29_unknown_field_blocks(self) -> None:
        draft = valid_draft()
        draft["surprise_field"] = "x"
        self.assertIn(R.UNKNOWN_FIELD, validate_contract_and_state(draft, POLICY))

    def test_30_each_missing_required_field_blocks(self) -> None:
        for field in REQUIRED_29:
            with self.subTest(field=field):
                draft = valid_draft()
                del draft[field]
                reasons = validate_contract_and_state(draft, POLICY)
                self.assertIn(R.MISSING_FIELD, reasons)

    def test_31_wrong_type_blocks(self) -> None:
        draft = valid_draft()
        draft["allowed_subpaths"] = "notes"  # String statt Sequenz
        self.assertTrue(validate_contract_and_state(draft, POLICY))

    def test_32_wrong_schema_version_blocks(self) -> None:
        draft = valid_draft()
        draft["schema_version"] = "2.0"
        self.assertIn(R.SCHEMA_VERSION, validate_contract_and_state(draft, POLICY))

    def test_33_all_31_contract_fields_recognized(self) -> None:
        draft = valid_draft()
        self.assertEqual(present_field_count(draft), 31)
        self.assertNotIn(R.UNKNOWN_FIELD, validate_contract_and_state(draft, POLICY))

    def test_34_no_additional_fields_accepted(self) -> None:
        draft = valid_draft()
        draft["extra"] = "x"
        reasons = validate_contract_and_state(draft, POLICY)
        self.assertIn(R.UNKNOWN_FIELD, reasons)
        self.assertEqual(present_field_count(draft), 31)  # extra nicht mitgezaehlt

    def test_35_real_paths_block(self) -> None:
        draft = valid_draft()
        draft["mapping_name"] = "segment-a/segment-b"  # synthetisch, mit Separator
        self.assertIn(R.PATH_INDICATOR, validate_contract_and_state(draft, POLICY))

    def test_36_urls_block(self) -> None:
        draft = valid_draft()
        draft["mapping_name"] = "www.synthetic-host"
        self.assertIn(R.URL_INDICATOR, validate_contract_and_state(draft, POLICY))

    def test_37_parent_traversal_blocks(self) -> None:
        draft = valid_draft()
        draft["mapping_name"] = "segment..segment"
        self.assertIn(R.DOTDOT, validate_contract_and_state(draft, POLICY))

    def test_38_source_content_blocks(self) -> None:
        # Ein untergeschobenes Inhaltsfeld ist ein unbekanntes Feld und blockiert.
        draft = valid_draft()
        draft["source_content"] = "synthetic body"
        self.assertIn(R.UNKNOWN_FIELD, validate_contract_and_state(draft, POLICY))

    def test_39_secret_values_block(self) -> None:
        draft = valid_draft()
        draft["notes"] = "token = synthetic-placeholder-value"
        self.assertIn(R.SECRET_INDICATOR, validate_contract_and_state(draft, POLICY))


class TestMappingId(unittest.TestCase):
    """Faelle 60-62 — mapping_id wird geprueft, nicht berechnet."""

    def test_60_mapping_id_valid(self) -> None:
        draft = valid_draft()
        self.assertNotIn(
            R.MAPPING_ID_INVALID, validate_contract_and_state(draft, POLICY)
        )

    def test_61_invalid_mapping_id_blocks(self) -> None:
        draft = valid_draft()
        draft["mapping_id"] = "MAP WITH SPACE"
        self.assertIn(
            R.MAPPING_ID_INVALID, validate_contract_and_state(draft, POLICY)
        )

    def test_62_mapping_id_is_not_recomputed(self) -> None:
        draft = valid_draft()
        self.assertEqual(mapping_id_of(draft), "MAP-EXAMPLE-0001")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "registry"
            _write_registry(root)
            draft_path = Path(tmp) / "draft.json"
            draft_path.write_text(json.dumps(draft), encoding="utf-8")
            report = run_validate(
                draft_path=draft_path, policy=POLICY, registry_root=root,
                source_id=SOURCE_ID, synthetic_confirmed=True,
            )
        self.assertEqual(report.mapping_id, "MAP-EXAMPLE-0001")
        # Keine map-+SHA-256-Bildungsvorschrift.
        self.assertIsNone(re.fullmatch(r"map-[0-9a-f]{24,}", report.mapping_id or ""))


class TestReport(unittest.TestCase):
    """Faelle 74-90 — deterministischer, minimierter, nicht persistierter Report."""

    def _run(self, draft: dict[str, object], tmp: str):
        root = Path(tmp) / "registry"
        _write_registry(root)
        draft_path = Path(tmp) / "draft.json"
        raw = json.dumps(draft).encode("utf-8")
        draft_path.write_bytes(raw)
        report = run_validate(
            draft_path=draft_path, policy=POLICY, registry_root=root,
            source_id=SOURCE_ID, synthetic_confirmed=True,
        )
        return report, raw, root, draft_path

    def test_74_draft_sha256_correct(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report, raw, _, _ = self._run(valid_draft(), tmp)
        self.assertEqual(report.draft_sha256, hashlib.sha256(raw).hexdigest())

    def test_75_policy_sha256_correct(self) -> None:
        policy_bytes = (
            REPO_ROOT / "config" / "source_mapping_validation_policy.example.toml"
        ).read_bytes()
        self.assertEqual(POLICY.policy_sha256, hashlib.sha256(policy_bytes).hexdigest())
        with tempfile.TemporaryDirectory() as tmp:
            report, _, _, _ = self._run(valid_draft(), tmp)
        self.assertEqual(report.policy_sha256, POLICY.policy_sha256)

    def test_76_report_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            r1, _, _, _ = self._run(valid_draft(), tmp)
            r2, _, _, _ = self._run(valid_draft(), tmp)
        self.assertEqual(r1.to_dict(), r2.to_dict())

    def test_77_78_reason_codes_sorted_and_deduplicated(self) -> None:
        draft = valid_draft()
        draft["enabled"] = True
        draft["read_only"] = False
        draft["mapping_name"] = "segment-a/segment-b"
        with tempfile.TemporaryDirectory() as tmp:
            report, _, _, _ = self._run(draft, tmp)
        codes = list(report.reason_codes)
        self.assertEqual(codes, sorted(codes))
        self.assertEqual(len(codes), len(set(codes)))
        self.assertGreaterEqual(len(codes), 2)

    def test_79_80_field_counts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report, _, _, _ = self._run(valid_draft(), tmp)
        self.assertEqual(report.canonical_contract_field_count, 31)
        self.assertEqual(report.required_field_count, 29)

    def test_81_present_field_count_29(self) -> None:
        draft = valid_draft()
        del draft["credential_reference"]
        del draft["notes"]
        with tempfile.TemporaryDirectory() as tmp:
            report, _, _, _ = self._run(draft, tmp)
        self.assertEqual(report.present_field_count, 29)
        self.assertEqual(report.validation_status, ValidationStatus.VALID_DRAFT)

    def test_82_present_field_count_30(self) -> None:
        draft = valid_draft()
        del draft["notes"]
        with tempfile.TemporaryDirectory() as tmp:
            report, _, _, _ = self._run(draft, tmp)
        self.assertEqual(report.present_field_count, 30)
        self.assertEqual(report.validation_status, ValidationStatus.VALID_DRAFT)

    def test_83_present_field_count_31(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report, _, _, _ = self._run(valid_draft(), tmp)
        self.assertEqual(report.present_field_count, 31)
        self.assertEqual(report.validation_status, ValidationStatus.VALID_DRAFT)

    def test_84_to_88_report_has_no_leaks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report, _, root, draft_path = self._run(valid_draft(), tmp)
            serialized = json.dumps(report.to_dict(), ensure_ascii=False)
            self.assertNotIn(str(draft_path), serialized)  # 84 kein Eingabepfad
            self.assertNotIn(str(root), serialized)  # 85 kein Registry-Pfad
            self.assertNotIn(SOURCE_REF, serialized)  # 86 keine source_reference
            self.assertNotIn("synthetic-placeholder", serialized)  # 87 kein Inhalt
            for marker in ("://", "http:", "https:", "www."):  # 88 keine URL
                self.assertNotIn(marker, serialized)

    def test_89_valid_draft_is_not_approved(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report, _, _, _ = self._run(valid_draft(), tmp)
        self.assertEqual(report.validation_status, ValidationStatus.VALID_DRAFT)
        self.assertNotIn("approved", report.to_dict())
        self.assertNotIn("enabled", report.to_dict())

    def test_90_report_is_not_stored(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "registry"
            _write_registry(root)
            draft_path = Path(tmp) / "draft.json"
            draft_path.write_text(json.dumps(valid_draft()), encoding="utf-8")
            before = {p for p in Path(tmp).rglob("*")}
            run_validate(
                draft_path=draft_path, policy=POLICY, registry_root=root,
                source_id=SOURCE_ID, synthetic_confirmed=True,
            )
            after = {p for p in Path(tmp).rglob("*")}
        self.assertEqual(before, after)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
