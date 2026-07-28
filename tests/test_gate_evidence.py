"""Tests des fail-closed Gate-Evidenz-Bundles (CBP-WP-016)."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from core.core_brain.errors import GateEvidenceError, ReasonCode
from core.core_brain.gate.evidence import load_evidence

HEX = "a" * 64


def base_bundle(**over: object) -> dict[str, object]:
    bundle: dict[str, object] = {
        "evidence_schema_version": "1.0",
        "synthetic_test_only": True,
        "source_id": "src-0123456789abcdef01234567",
        "mapping_id": "MAP-EXAMPLE-0001",
        "gate_contract_revision": "1.0",
        "evidence_revision": 1,
        "mapping_draft_sha256": HEX,
        "mapping_policy_sha256": HEX,
        "registry_record_sha256": HEX,
        "criterion_evidence": [
            {"criterion": i, "evidence_ref": None} for i in range(1, 21)
        ],
    }
    bundle.update(over)
    return bundle


def _load_text(text: str):
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "evidence.json"
        path.write_text(text, encoding="utf-8")
        return load_evidence(path)


def _load_bytes(raw: bytes):
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "evidence.json"
        path.write_bytes(raw)
        return load_evidence(path)


class TestEvidence(unittest.TestCase):
    def test_valid_bundle_loads(self) -> None:
        bundle = _load_text(json.dumps(base_bundle()))
        self.assertTrue(bundle.synthetic_test_only)
        self.assertEqual(bundle.provided_evidence_count, 0)

    def test_valid_synthetic_ref_counts(self) -> None:
        ce = [{"criterion": i, "evidence_ref": None} for i in range(1, 21)]
        ce[0]["evidence_ref"] = "synthetic-evidence-01"
        bundle = _load_text(json.dumps(base_bundle(criterion_evidence=ce)))
        self.assertEqual(bundle.provided_evidence_count, 1)

    def test_file_missing_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(GateEvidenceError) as ctx:
                load_evidence(Path(tmp) / "nope.json")
        self.assertEqual(ctx.exception.reason, ReasonCode.GATE_EVIDENCE_FILE_MISSING)

    def test_unknown_field_blocks(self) -> None:
        with self.assertRaises(GateEvidenceError) as ctx:
            _load_text(json.dumps(base_bundle(surprise="x")))
        self.assertEqual(ctx.exception.reason, ReasonCode.GATE_EVIDENCE_UNKNOWN_FIELD)

    def test_missing_field_blocks(self) -> None:
        data = base_bundle()
        del data["evidence_revision"]
        with self.assertRaises(GateEvidenceError) as ctx:
            _load_text(json.dumps(data))
        self.assertEqual(ctx.exception.reason, ReasonCode.GATE_EVIDENCE_MISSING_FIELD)

    def test_unknown_schema_version_blocks(self) -> None:
        with self.assertRaises(GateEvidenceError) as ctx:
            _load_text(json.dumps(base_bundle(evidence_schema_version="9.9")))
        self.assertEqual(
            ctx.exception.reason, ReasonCode.GATE_EVIDENCE_SCHEMA_UNSUPPORTED
        )

    def test_bom_blocks(self) -> None:
        with self.assertRaises(GateEvidenceError) as ctx:
            _load_bytes(b"\xef\xbb\xbf" + json.dumps(base_bundle()).encode("utf-8"))
        self.assertEqual(ctx.exception.reason, ReasonCode.GATE_EVIDENCE_PARSE_ERROR)

    def test_invalid_utf8_blocks(self) -> None:
        with self.assertRaises(GateEvidenceError) as ctx:
            _load_bytes(b'{"evidence_schema_version": "1.0\xff"}')
        self.assertEqual(ctx.exception.reason, ReasonCode.GATE_EVIDENCE_PARSE_ERROR)

    def test_duplicate_key_blocks(self) -> None:
        raw = b'{"evidence_schema_version": "1.0", "evidence_schema_version": "1.0"}'
        with self.assertRaises(GateEvidenceError) as ctx:
            _load_bytes(raw)
        self.assertEqual(ctx.exception.reason, ReasonCode.GATE_EVIDENCE_PARSE_ERROR)

    def test_nan_blocks(self) -> None:
        with self.assertRaises(GateEvidenceError) as ctx:
            _load_bytes(b'{"evidence_revision": NaN}')
        self.assertEqual(ctx.exception.reason, ReasonCode.GATE_EVIDENCE_PARSE_ERROR)

    def test_infinity_blocks(self) -> None:
        with self.assertRaises(GateEvidenceError) as ctx:
            _load_bytes(b'{"evidence_revision": Infinity}')
        self.assertEqual(ctx.exception.reason, ReasonCode.GATE_EVIDENCE_PARSE_ERROR)

    def test_top_level_not_object_blocks(self) -> None:
        with self.assertRaises(GateEvidenceError) as ctx:
            _load_bytes(b"[1, 2, 3]")
        self.assertEqual(ctx.exception.reason, ReasonCode.GATE_EVIDENCE_PARSE_ERROR)

    def test_not_synthetic_blocks(self) -> None:
        with self.assertRaises(GateEvidenceError) as ctx:
            _load_text(json.dumps(base_bundle(synthetic_test_only=False)))
        self.assertEqual(ctx.exception.reason, ReasonCode.GATE_EVIDENCE_NOT_SYNTHETIC)

    def test_bad_source_id_blocks(self) -> None:
        with self.assertRaises(GateEvidenceError) as ctx:
            _load_text(json.dumps(base_bundle(source_id="not-a-source-id")))
        self.assertEqual(ctx.exception.reason, ReasonCode.GATE_EVIDENCE_INVALID_VALUE)

    def test_bad_hash_blocks(self) -> None:
        with self.assertRaises(GateEvidenceError) as ctx:
            _load_text(json.dumps(base_bundle(mapping_draft_sha256="short")))
        self.assertEqual(ctx.exception.reason, ReasonCode.GATE_EVIDENCE_INVALID_VALUE)

    def test_evidence_revision_zero_blocks(self) -> None:
        with self.assertRaises(GateEvidenceError) as ctx:
            _load_text(json.dumps(base_bundle(evidence_revision=0)))
        self.assertEqual(ctx.exception.reason, ReasonCode.GATE_EVIDENCE_INVALID_VALUE)

    def test_criterion_evidence_wrong_length_blocks(self) -> None:
        with self.assertRaises(GateEvidenceError) as ctx:
            _load_text(json.dumps(base_bundle(criterion_evidence=[])))
        self.assertEqual(ctx.exception.reason, ReasonCode.GATE_EVIDENCE_INVALID_VALUE)

    def test_criterion_evidence_duplicate_id_blocks(self) -> None:
        ce = [{"criterion": 1, "evidence_ref": None} for _ in range(20)]
        with self.assertRaises(GateEvidenceError) as ctx:
            _load_text(json.dumps(base_bundle(criterion_evidence=ce)))
        self.assertEqual(ctx.exception.reason, ReasonCode.GATE_EVIDENCE_INVALID_VALUE)

    def test_criterion_evidence_leaky_ref_blocks(self) -> None:
        for leak in ("/etc/passwd", "C:\\secret", "http://host/x", "token-abc"):
            with self.subTest(leak=leak):
                ce = [{"criterion": i, "evidence_ref": None} for i in range(1, 21)]
                ce[0]["evidence_ref"] = leak
                with self.assertRaises(GateEvidenceError) as ctx:
                    _load_text(json.dumps(base_bundle(criterion_evidence=ce)))
                self.assertEqual(
                    ctx.exception.reason, ReasonCode.GATE_EVIDENCE_INVALID_VALUE
                )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
