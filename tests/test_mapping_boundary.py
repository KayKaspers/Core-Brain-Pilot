"""Tests der Boundary- und Draft-Zustandsregeln (CBP-WP-015, Faelle 40-59).

Genau eine deaktivierte synthetische Boundary mit bestehenden kanonischen
Feldern und ausschliesslich bereits erlaubten Vertragswerten (C1). Kein neues
Slot-Praefix, keine neuen Enum-Werte.
"""

from __future__ import annotations

import unittest

from core.core_brain.mapping import load_policy, validate_contract_and_state
from core.core_brain.mapping.models import MappingReasonCode as R
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
POLICY = load_policy(
    REPO_ROOT / "config" / "source_mapping_validation_policy.example.toml"
)


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


def reasons(**over: object) -> list[R]:
    draft = valid_draft()
    draft.update(over)
    return validate_contract_and_state(draft, POLICY)


class TestBoundary(unittest.TestCase):
    """Faelle 40-45 — Slot, Boundary, Location-Type und Platzhalter."""

    def test_40_slot_id_valid(self) -> None:
        self.assertNotIn(R.SLOT_INVALID, reasons())

    def test_41_invalid_slot_blocks(self) -> None:
        self.assertIn(R.SLOT_INVALID, reasons(slot_id="PS-99"))

    def test_42_boundary_slot_mismatch_blocks(self) -> None:
        self.assertIn(
            R.BOUNDARY_SLOT_MISMATCH, reasons(source_boundary_type="git-repository")
        )

    def test_43_location_reference_type_mismatch_blocks(self) -> None:
        self.assertIn(
            R.LOCATION_TYPE_MISMATCH, reasons(location_reference_type="git-remote")
        )

    def test_44_real_location_reference_blocks(self) -> None:
        # Ein Nicht-Platzhalter (kein synthetic-placeholder-*) blockiert.
        self.assertIn(
            R.LOCATION_NOT_SYNTHETIC, reasons(location_reference="local-notes-dir")
        )

    def test_45_canonical_synthetic_placeholder_accepted(self) -> None:
        self.assertNotIn(R.LOCATION_NOT_SYNTHETIC, reasons())
        # Auch der PS-04-Platzhalter ist zulaessig.
        self.assertNotIn(
            R.LOCATION_NOT_SYNTHETIC,
            reasons(
                slot_id="PS-04",
                source_boundary_type="handoff-root",
                location_reference="synthetic-placeholder-handoff-root",
                location_reference_type="local-directory",
                revision_strategy="handoff-revision",
            ),
        )


class TestDraftState(unittest.TestCase):
    """Faelle 46-59 — die deaktivierte synthetische Boundary ist restriktiv."""

    def test_46_enabled_true_blocks(self) -> None:
        self.assertIn(R.ENABLED_TRUE, reasons(enabled=True))

    def test_47_read_only_false_blocks(self) -> None:
        self.assertIn(R.READ_ONLY_FALSE, reasons(read_only=False))

    def test_48_follow_symlinks_true_blocks(self) -> None:
        self.assertIn(R.FOLLOW_SYMLINKS_TRUE, reasons(follow_symlinks=True))

    def test_49_allowed_subpaths_nonempty_blocks(self) -> None:
        self.assertIn(R.ALLOWED_SUBPATHS_NONEMPTY, reasons(allowed_subpaths=["notes"]))

    def test_50_excluded_subpaths_nonempty_blocks(self) -> None:
        self.assertIn(
            R.EXCLUDED_SUBPATHS_NONEMPTY, reasons(excluded_subpaths=["notes/private"])
        )

    def test_51_approval_status_not_draft_blocks(self) -> None:
        self.assertIn(R.APPROVAL_NOT_DRAFT, reasons(approval_status="approved"))

    def test_52_verification_status_not_draft_blocks(self) -> None:
        self.assertIn(R.VERIFICATION_NOT_DRAFT, reasons(verification_status="verified"))

    def test_53_ai_transfer_not_forbidden_blocks(self) -> None:
        self.assertIn(
            R.AI_TRANSFER_NOT_FORBIDDEN, reasons(ai_transfer_policy="allowed")
        )

    def test_54_indexing_not_none_blocks(self) -> None:
        self.assertIn(R.INDEXING_NOT_NONE, reasons(indexing_policy="full"))

    def test_55_local_search_not_forbidden_blocks(self) -> None:
        self.assertIn(
            R.LOCAL_SEARCH_NOT_FORBIDDEN, reasons(local_search_policy="allowed")
        )

    def test_56_mobile_visibility_not_forbidden_blocks(self) -> None:
        self.assertIn(R.MOBILE_NOT_FORBIDDEN, reasons(mobile_visibility="allowed"))

    def test_57_approved_by_not_null_blocks(self) -> None:
        self.assertIn(R.APPROVED_BY_NOT_NULL, reasons(approved_by="role-x"))

    def test_58_approved_at_not_null_blocks(self) -> None:
        self.assertIn(R.APPROVED_AT_NOT_NULL, reasons(approved_at="2026-01-01"))

    def test_59_credential_reference_with_value_blocks(self) -> None:
        self.assertIn(
            R.CREDENTIAL_REFERENCE_VALUE, reasons(credential_reference="cred-opaque-01")
        )

    def test_valid_draft_has_no_reasons(self) -> None:
        self.assertEqual(reasons(), [])


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
