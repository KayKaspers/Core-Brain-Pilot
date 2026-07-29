"""Tests des fail-closed Gate-Evidenz-Bundles 3.0 (CBP-WP-016/017/018)."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from core.core_brain.errors import GateEvidenceError, ReasonCode
from core.core_brain.gate.evidence import load_evidence

HEX = "a" * 64
ART_ID = "art-" + "0" * 24
ART_ID_B = "art-" + "1" * 24


def artifact(**over: object) -> dict[str, object]:
    art: dict[str, object] = {
        "artifact_id": ART_ID,
        "artifact_sha256": "b" * 64,
        "binding_sha256": "c" * 64,
        "producer_class": "structural-form",
        "evidence_revision": 1,
        "synthetic_test_only": True,
    }
    art.update(over)
    return art


def security_artifact(**over: object) -> dict[str, object]:
    """Ein Security-Control-Form-Artefakt mit Pflicht-``control_id`` (CBP-WP-018)."""
    art: dict[str, object] = {
        "artifact_id": ART_ID,
        "artifact_sha256": "b" * 64,
        "binding_sha256": "c" * 64,
        "producer_class": "security-control-form",
        "control_id": "KB-08",
        "evidence_revision": 1,
        "synthetic_test_only": True,
    }
    art.update(over)
    return art


def base_bundle(**over: object) -> dict[str, object]:
    bundle: dict[str, object] = {
        "evidence_schema_version": "3.0",
        "synthetic_test_only": True,
        "source_id": "src-0123456789abcdef01234567",
        "mapping_id": "MAP-EXAMPLE-0001",
        "gate_contract_revision": "1.0",
        "evidence_contract_revision": "3.0",
        "evidence_revision": 1,
        "security_contract_revision": "1.0",
        "security_contract_sha256": HEX,
        "mapping_draft_sha256": HEX,
        "mapping_policy_sha256": HEX,
        "registry_record_sha256": HEX,
        "criterion_evidence": [
            {"criterion": i, "artifacts": []} for i in range(1, 21)
        ],
    }
    bundle.update(over)
    return bundle


def _ce_with(criterion_index: int, arts: list) -> list:
    ce = [{"criterion": i, "artifacts": []} for i in range(1, 21)]
    ce[criterion_index - 1]["artifacts"] = arts
    return ce


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


def _assert_reason(self, text_or_bytes, reason, *, as_bytes=False):
    with self.assertRaises(GateEvidenceError) as ctx:
        (_load_bytes if as_bytes else _load_text)(text_or_bytes)
    self.assertEqual(ctx.exception.reason, reason)


class TestSchema20(unittest.TestCase):
    def test_valid_minimal_bundle_loads(self) -> None:
        bundle = _load_text(json.dumps(base_bundle()))
        self.assertTrue(bundle.synthetic_test_only)
        self.assertEqual(bundle.total_artifact_count, 0)
        self.assertEqual(bundle.evidence_contract_revision, "3.0")
        self.assertEqual(bundle.evidence_schema_version, "3.0")
        self.assertEqual(bundle.security_contract_revision, "1.0")
        self.assertEqual(bundle.security_contract_sha256, HEX)

    def test_valid_with_artifact_counts(self) -> None:
        b = base_bundle(criterion_evidence=_ce_with(1, [artifact(), artifact()]))
        bundle = _load_text(json.dumps(b))
        self.assertEqual(bundle.total_artifact_count, 2)
        self.assertEqual(len(bundle.criterion_artifacts[1]), 2)

    def test_schema_1_0_fails_closed(self) -> None:
        # CBP-WP-017: das abgelöste 1.0-Bundle wird fail-closed abgewiesen.
        legacy = base_bundle(evidence_schema_version="1.0")
        _assert_reason(self, json.dumps(legacy),
                       ReasonCode.GATE_EVIDENCE_SCHEMA_UNSUPPORTED)

    def test_schema_2_0_fails_closed(self) -> None:
        # CBP-WP-018: auch das abgelöste 2.0-Bundle wird fail-closed abgewiesen.
        legacy = base_bundle(evidence_schema_version="2.0")
        _assert_reason(self, json.dumps(legacy),
                       ReasonCode.GATE_EVIDENCE_SCHEMA_UNSUPPORTED)

    def test_missing_security_contract_revision_blocks(self) -> None:
        data = base_bundle()
        del data["security_contract_revision"]
        _assert_reason(self, json.dumps(data),
                       ReasonCode.GATE_EVIDENCE_MISSING_FIELD)

    def test_missing_security_contract_sha256_blocks(self) -> None:
        data = base_bundle()
        del data["security_contract_sha256"]
        _assert_reason(self, json.dumps(data),
                       ReasonCode.GATE_EVIDENCE_MISSING_FIELD)

    def test_bad_security_contract_sha256_blocks(self) -> None:
        _assert_reason(self, json.dumps(base_bundle(security_contract_sha256="short")),
                       ReasonCode.GATE_EVIDENCE_INVALID_VALUE)

    def test_empty_security_contract_revision_blocks(self) -> None:
        _assert_reason(self, json.dumps(base_bundle(security_contract_revision="")),
                       ReasonCode.GATE_EVIDENCE_INVALID_VALUE)

    def test_stale_security_contract_values_load(self) -> None:
        # Strukturell wohlgeformte, aber (semantisch) veraltete Contract-Werte
        # sind KEIN Loader-Schemafehler — sie laden und werden erst im Service
        # als STALE_EVIDENCE ausgewertet.
        bundle = _load_text(json.dumps(base_bundle(
            security_contract_revision="0.9",
            security_contract_sha256="d" * 64,
        )))
        self.assertEqual(bundle.security_contract_revision, "0.9")
        self.assertEqual(bundle.security_contract_sha256, "d" * 64)

    def test_unknown_schema_version_blocks(self) -> None:
        _assert_reason(self, json.dumps(base_bundle(evidence_schema_version="9.9")),
                       ReasonCode.GATE_EVIDENCE_SCHEMA_UNSUPPORTED)

    def test_unknown_top_level_field_blocks(self) -> None:
        _assert_reason(self, json.dumps(base_bundle(surprise="x")),
                       ReasonCode.GATE_EVIDENCE_UNKNOWN_FIELD)

    def test_missing_field_blocks(self) -> None:
        data = base_bundle()
        del data["evidence_contract_revision"]
        _assert_reason(self, json.dumps(data),
                       ReasonCode.GATE_EVIDENCE_MISSING_FIELD)

    def test_missing_criterion_blocks(self) -> None:
        ce = [{"criterion": i, "artifacts": []} for i in range(1, 20)]  # 19
        _assert_reason(self, json.dumps(base_bundle(criterion_evidence=ce)),
                       ReasonCode.GATE_EVIDENCE_INVALID_VALUE)

    def test_duplicate_criterion_blocks(self) -> None:
        ce = [{"criterion": 1, "artifacts": []} for _ in range(20)]
        _assert_reason(self, json.dumps(base_bundle(criterion_evidence=ce)),
                       ReasonCode.GATE_EVIDENCE_INVALID_VALUE)

    def test_wrong_criterion_order_blocks(self) -> None:
        ce = [{"criterion": i, "artifacts": []} for i in range(1, 21)]
        ce[0], ce[1] = ce[1], ce[0]  # 2,1,3,...
        _assert_reason(self, json.dumps(base_bundle(criterion_evidence=ce)),
                       ReasonCode.GATE_EVIDENCE_INVALID_VALUE)

    def test_unknown_criterion_entry_field_blocks(self) -> None:
        ce = [{"criterion": i, "artifacts": []} for i in range(1, 21)]
        ce[0]["surprise"] = 1
        _assert_reason(self, json.dumps(base_bundle(criterion_evidence=ce)),
                       ReasonCode.GATE_EVIDENCE_INVALID_VALUE)

    def test_unknown_artifact_field_blocks(self) -> None:
        b = base_bundle(criterion_evidence=_ce_with(1, [artifact(extra="x")]))
        _assert_reason(self, json.dumps(b), ReasonCode.GATE_EVIDENCE_INVALID_VALUE)

    def test_bundle_synthetic_false_blocks(self) -> None:
        _assert_reason(self, json.dumps(base_bundle(synthetic_test_only=False)),
                       ReasonCode.GATE_EVIDENCE_NOT_SYNTHETIC)

    def test_artifact_synthetic_false_blocks(self) -> None:
        b = base_bundle(criterion_evidence=_ce_with(1, [artifact(synthetic_test_only=False)]))
        _assert_reason(self, json.dumps(b), ReasonCode.GATE_EVIDENCE_NOT_SYNTHETIC)

    def test_five_artifacts_per_criterion_blocks(self) -> None:
        b = base_bundle(criterion_evidence=_ce_with(1, [artifact() for _ in range(5)]))
        _assert_reason(self, json.dumps(b), ReasonCode.GATE_EVIDENCE_INVALID_VALUE)

    def test_eighty_artifacts_total_loads(self) -> None:
        # 20 Kriterien x 4 = 80 (Grenze; > 80 ist bei ≤4/Kriterium unerreichbar).
        ce = [{"criterion": i, "artifacts": [artifact() for _ in range(4)]}
              for i in range(1, 21)]
        bundle = _load_text(json.dumps(base_bundle(criterion_evidence=ce)))
        self.assertEqual(bundle.total_artifact_count, 80)

    def test_worst_case_security_bundle_fits_size_limit(self) -> None:
        # CBP-WP-018 §21: 80 Security-Control-Artefakte (das groesste Artefakt,
        # da es zusaetzlich control_id traegt) bleiben unter 131072 Byte —
        # eingerueckt serialisiert, also ueber dem realen kompakten Fall.
        ce = [
            {"criterion": i,
             "artifacts": [security_artifact(artifact_id=aid)
                           for aid in ("art-" + f"{n:024x}" for n in range(4))]}
            for i in range(1, 21)
        ]
        payload = json.dumps(base_bundle(criterion_evidence=ce), indent=2)
        self.assertLess(len(payload.encode("utf-8")), 131072)
        bundle = _load_text(payload)
        self.assertEqual(bundle.total_artifact_count, 80)
        self.assertEqual(bundle.criterion_artifacts[4][0].control_id, "KB-08")

    def test_too_large_blocks(self) -> None:
        big = base_bundle(mapping_id="M" + "a" * 200000)
        _assert_reason(self, json.dumps(big), ReasonCode.GATE_EVIDENCE_INVALID_VALUE)

    def test_bom_blocks(self) -> None:
        _assert_reason(self, b"\xef\xbb\xbf" + json.dumps(base_bundle()).encode("utf-8"),
                       ReasonCode.GATE_EVIDENCE_PARSE_ERROR, as_bytes=True)

    def test_invalid_utf8_blocks(self) -> None:
        _assert_reason(self, b'{"evidence_schema_version": "2.0\xff"}',
                       ReasonCode.GATE_EVIDENCE_PARSE_ERROR, as_bytes=True)

    def test_duplicate_key_blocks(self) -> None:
        raw = b'{"evidence_schema_version": "2.0", "evidence_schema_version": "2.0"}'
        _assert_reason(self, raw, ReasonCode.GATE_EVIDENCE_PARSE_ERROR, as_bytes=True)

    def test_nan_blocks(self) -> None:
        _assert_reason(self, b'{"evidence_revision": NaN}',
                       ReasonCode.GATE_EVIDENCE_PARSE_ERROR, as_bytes=True)

    def test_infinity_blocks(self) -> None:
        _assert_reason(self, b'{"evidence_revision": Infinity}',
                       ReasonCode.GATE_EVIDENCE_PARSE_ERROR, as_bytes=True)

    def test_not_object_blocks(self) -> None:
        _assert_reason(self, b"[1,2,3]",
                       ReasonCode.GATE_EVIDENCE_PARSE_ERROR, as_bytes=True)

    def test_file_missing_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(GateEvidenceError) as ctx:
                load_evidence(Path(tmp) / "nope.json")
        self.assertEqual(ctx.exception.reason, ReasonCode.GATE_EVIDENCE_FILE_MISSING)

    def test_bad_source_id_blocks(self) -> None:
        _assert_reason(self, json.dumps(base_bundle(source_id="not-a-source-id")),
                       ReasonCode.GATE_EVIDENCE_INVALID_VALUE)

    def test_bad_hash_blocks(self) -> None:
        _assert_reason(self, json.dumps(base_bundle(mapping_draft_sha256="short")),
                       ReasonCode.GATE_EVIDENCE_INVALID_VALUE)

    def test_evidence_revision_zero_blocks(self) -> None:
        _assert_reason(self, json.dumps(base_bundle(evidence_revision=0)),
                       ReasonCode.GATE_EVIDENCE_INVALID_VALUE)

    def test_empty_evidence_contract_revision_blocks(self) -> None:
        _assert_reason(self, json.dumps(base_bundle(evidence_contract_revision="")),
                       ReasonCode.GATE_EVIDENCE_INVALID_VALUE)


class TestArtifactIdAndProducer(unittest.TestCase):
    _LEAKY = (
        "C:\\Users\\Example\\secret.txt", "/etc/shadow", "\\\\server\\share\\x",
        "file:///etc/passwd", "http://127.0.0.1/admin", "https://x.invalid/p",
        "../secret", "%2e%2e%2fsecret", "user:password@example.invalid",
        "AKIA0000000000000000", "Bearer-secret", "token-secret", "password-secret",
        "art-XYZ", "art-tooshort",
    )

    def test_leaky_artifact_id_blocks_without_echo(self) -> None:
        for leaky in self._LEAKY:
            with self.subTest(artifact_id=leaky):
                b = base_bundle(criterion_evidence=_ce_with(1, [artifact(artifact_id=leaky)]))
                with self.assertRaises(GateEvidenceError) as ctx:
                    _load_text(json.dumps(b))
                self.assertEqual(ctx.exception.reason,
                                 ReasonCode.GATE_EVIDENCE_INVALID_VALUE)
                self.assertNotIn(leaky, str(ctx.exception))

    def test_valid_artifact_id_loads(self) -> None:
        for ok in ("art-" + "0" * 24, "art-" + "abcdef0123456789abcdef01"):
            with self.subTest(artifact_id=ok):
                b = base_bundle(criterion_evidence=_ce_with(1, [artifact(artifact_id=ok)]))
                bundle = _load_text(json.dumps(b))
                self.assertEqual(bundle.criterion_artifacts[1][0].artifact_id, ok)

    def test_unknown_producer_class_blocks(self) -> None:
        for bad in ("mystery", "role-operator@host", "/etc/x", "http://x", "free text"):
            with self.subTest(producer_class=bad):
                b = base_bundle(criterion_evidence=_ce_with(1, [artifact(producer_class=bad)]))
                _assert_reason(self, json.dumps(b),
                               ReasonCode.GATE_EVIDENCE_INVALID_VALUE)


class TestControlIdConditionalSchema(unittest.TestCase):
    """CBP-WP-018 — bedingtes `control_id` (security-control-form only)."""

    def test_security_control_with_control_id_loads(self) -> None:
        # Kriterium 4 trägt security-control-form; control_id ist Pflicht.
        b = base_bundle(criterion_evidence=_ce_with(4, [security_artifact()]))
        bundle = _load_text(json.dumps(b))
        art = bundle.criterion_artifacts[4][0]
        self.assertEqual(art.control_id, "KB-08")
        self.assertEqual(art.producer_class, "security-control-form")

    def test_security_control_without_control_id_blocks(self) -> None:
        art = security_artifact()
        del art["control_id"]
        b = base_bundle(criterion_evidence=_ce_with(4, [art]))
        _assert_reason(self, json.dumps(b), ReasonCode.GATE_EVIDENCE_INVALID_VALUE)

    def test_foundation_form_with_control_id_blocks(self) -> None:
        # foundation-form (z. B. Kriterium 5) darf kein control_id tragen.
        art = artifact(producer_class="foundation-form", control_id="KB-01")
        b = base_bundle(criterion_evidence=_ce_with(5, [art]))
        _assert_reason(self, json.dumps(b), ReasonCode.GATE_EVIDENCE_INVALID_VALUE)

    def test_every_non_security_class_forbids_control_id(self) -> None:
        for pc in (
            "structural-form", "foundation-form", "operator-review-form",
            "rt2-audit-form", "backup-form", "rollback-form", "human-decision-form",
        ):
            with self.subTest(producer_class=pc):
                art = artifact(producer_class=pc, control_id="KB-01")
                b = base_bundle(criterion_evidence=_ce_with(1, [art]))
                _assert_reason(self, json.dumps(b),
                               ReasonCode.GATE_EVIDENCE_INVALID_VALUE)

    def test_all_twelve_control_ids_load(self) -> None:
        for i in range(1, 13):
            kb = f"KB-{i:02d}"
            with self.subTest(control_id=kb):
                b = base_bundle(
                    criterion_evidence=_ce_with(4, [security_artifact(control_id=kb)])
                )
                bundle = _load_text(json.dumps(b))
                self.assertEqual(bundle.criterion_artifacts[4][0].control_id, kb)

    def test_invalid_control_ids_block(self) -> None:
        for bad in (
            "KB-00", "KB-13", "KB-99", "kb-01", "KB-1", "KB-001", "KB-0a",
            "../secret", "http://x", "AKIA0000000000000000", "token", "",
        ):
            with self.subTest(control_id=bad):
                b = base_bundle(
                    criterion_evidence=_ce_with(4, [security_artifact(control_id=bad)])
                )
                with self.assertRaises(GateEvidenceError) as ctx:
                    _load_text(json.dumps(b))
                self.assertEqual(ctx.exception.reason,
                                 ReasonCode.GATE_EVIDENCE_INVALID_VALUE)
                if bad:
                    self.assertNotIn(bad, str(ctx.exception))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
