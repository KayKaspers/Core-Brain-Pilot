"""Tests des kanonischen JSON-Parsers des MVP-Profils (CBP-WP-015, Faelle 18-28)."""

from __future__ import annotations

import json
import unittest

from core.core_brain.mapping import DraftRejected, parse_draft
from core.core_brain.mapping.models import MappingReasonCode

MAX = 65536


def full_draft() -> dict[str, object]:
    """Ein vollstaendiger synthetischer 31-Feld-Entwurf (deaktiviert)."""
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


def _encode(draft: dict[str, object]) -> bytes:
    return json.dumps(draft).encode("utf-8")


class TestParser(unittest.TestCase):
    """Der Parser akzeptiert ausschliesslich das kanonische JSON-MVP-Profil."""

    def test_18_valid_json_29_required_fields(self) -> None:
        draft = full_draft()
        del draft["credential_reference"]
        del draft["notes"]
        parsed = parse_draft(_encode(draft), MAX)
        self.assertEqual(len(parsed), 29)

    def test_19_valid_json_30_fields(self) -> None:
        draft = full_draft()
        del draft["notes"]
        parsed = parse_draft(_encode(draft), MAX)
        self.assertEqual(len(parsed), 30)

    def test_20_valid_json_31_fields(self) -> None:
        parsed = parse_draft(_encode(full_draft()), MAX)
        self.assertEqual(len(parsed), 31)

    def test_21_credential_reference_may_be_absent(self) -> None:
        draft = full_draft()
        del draft["credential_reference"]
        parsed = parse_draft(_encode(draft), MAX)
        self.assertNotIn("credential_reference", parsed)

    def test_22_notes_may_be_absent(self) -> None:
        draft = full_draft()
        del draft["notes"]
        parsed = parse_draft(_encode(draft), MAX)
        self.assertNotIn("notes", parsed)

    def test_23_bom_blocks(self) -> None:
        raw = b"\xef\xbb\xbf" + _encode(full_draft())
        with self.assertRaises(DraftRejected) as ctx:
            parse_draft(raw, MAX)
        self.assertEqual(ctx.exception.reason, MappingReasonCode.PARSE_BOM)

    def test_24_invalid_utf8_blocks(self) -> None:
        raw = b'{"schema_version": "1.0\xff"}'
        with self.assertRaises(DraftRejected) as ctx:
            parse_draft(raw, MAX)
        self.assertEqual(ctx.exception.reason, MappingReasonCode.PARSE_UTF8)

    def test_25_top_level_not_object_blocks(self) -> None:
        with self.assertRaises(DraftRejected) as ctx:
            parse_draft(b"[1, 2, 3]", MAX)
        self.assertEqual(ctx.exception.reason, MappingReasonCode.PARSE_NOT_OBJECT)

    def test_26_duplicate_key_blocks(self) -> None:
        raw = b'{"schema_version": "1.0", "schema_version": "1.0"}'
        with self.assertRaises(DraftRejected) as ctx:
            parse_draft(raw, MAX)
        self.assertEqual(ctx.exception.reason, MappingReasonCode.PARSE_DUPLICATE_KEY)

    def test_27_nan_blocks(self) -> None:
        raw = b'{"mapping_revision": NaN}'
        with self.assertRaises(DraftRejected) as ctx:
            parse_draft(raw, MAX)
        self.assertEqual(ctx.exception.reason, MappingReasonCode.PARSE_NAN)

    def test_28_infinity_blocks(self) -> None:
        raw = b'{"mapping_revision": Infinity}'
        with self.assertRaises(DraftRejected) as ctx:
            parse_draft(raw, MAX)
        self.assertEqual(ctx.exception.reason, MappingReasonCode.PARSE_INFINITY)

    def test_oversize_blocks(self) -> None:
        with self.assertRaises(DraftRejected) as ctx:
            parse_draft(_encode(full_draft()), 8)
        self.assertEqual(ctx.exception.reason, MappingReasonCode.DRAFT_TOO_LARGE)

    def test_malformed_json_blocks(self) -> None:
        with self.assertRaises(DraftRejected) as ctx:
            parse_draft(b'{"schema_version": ', MAX)
        self.assertEqual(ctx.exception.reason, MappingReasonCode.PARSE_JSON)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
