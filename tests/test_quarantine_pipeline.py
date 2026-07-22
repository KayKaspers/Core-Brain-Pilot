"""Tests der Quarantäne-Pipeline (CBP-WP-013).

Deckt die drei Ergebniszustände, das Staging von genau einem Objekt und einem
Record, die Verweigerung jeder Promotion und die technische Durchsetzung der
Synthetic-only-Grenze ab.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from core.core_brain.errors import QuarantineInputRejected, ReasonCode
from core.core_brain.quarantine import (
    QuarantineStore,
    ScanStatus,
    load_policy,
    run_scan,
    run_stage,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
EXAMPLE_POLICY = REPO_ROOT / "config" / "quarantine_policy.example.toml"
POLICY = load_policy(EXAMPLE_POLICY)
MARKER = "<!-- synthetic-test-only -->"
SOURCE_REF = "synthetic:pipeline-test"

_PROMOTION_TERMS = ("approved", "released", "enabled", "indexed")


def _write(tmp: str, text: str) -> Path:
    target = Path(tmp) / "artifact.md"
    target.write_text(text, encoding="utf-8")
    return target


def _scan(tmp: str, text: str):  # type: ignore[no-untyped-def]
    return run_scan(
        input_path=_write(tmp, text),
        policy=POLICY,
        source_reference=SOURCE_REF,
        synthetic_confirmed=True,
    )


class TestPipelineStates(unittest.TestCase):
    """Tests 41 bis 43 — die drei Ergebniszustände."""

    def test_41_scan_ready_for_human_review(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = _scan(tmp, f"{MARKER}\n# clean\nplain text\n")
        self.assertIs(result.status, ScanStatus.READY_FOR_HUMAN_REVIEW)

    def test_42_scan_review_required(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = _scan(tmp, f"{MARKER}\nKontakt user@example.com\n")
        self.assertIs(result.status, ScanStatus.REVIEW_REQUIRED)

    def test_43_scan_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = _scan(tmp, "no marker at all\n")
        self.assertIs(result.status, ScanStatus.BLOCKED)


class TestPipelineStaging(unittest.TestCase):
    """Tests 44 und 45 — Staging und keine Promotion."""

    def test_44_stage_creates_exactly_one_object_and_record(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = QuarantineStore(Path(tmp) / "store")
            run_stage(
                input_path=_write(tmp, f"{MARKER}\ntext\n"),
                policy=POLICY,
                source_reference=SOURCE_REF,
                synthetic_confirmed=True,
                store=store,
            )
            objects = list((store.root / "objects").rglob("*.blob"))
            records = list((store.root / "records").glob("*.json"))
        self.assertEqual(len(objects), 1)
        self.assertEqual(len(records), 1)

    def test_45_stage_performs_no_promotion(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = QuarantineStore(Path(tmp) / "store")
            outcome = run_stage(
                input_path=_write(tmp, f"{MARKER}\ntext\n"),
                policy=POLICY,
                source_reference=SOURCE_REF,
                synthetic_confirmed=True,
                store=store,
            )
            # Nur die beiden erwarteten Unterverzeichnisse existieren.
            subdirs = {p.name for p in store.root.iterdir() if p.is_dir()}
            self.assertEqual(subdirs, {"objects", "records"})
            rendered = str(outcome.record.to_dict()).lower()
        self.assertIn(outcome.record.scan_status.value, {s.value for s in ScanStatus})
        for term in _PROMOTION_TERMS:
            self.assertNotIn(term, rendered)

    def test_stage_blocked_stores_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = QuarantineStore(Path(tmp) / "store")
            outcome = run_stage(
                input_path=_write(tmp, "no marker\n"),
                policy=POLICY,
                source_reference=SOURCE_REF,
                synthetic_confirmed=True,
                store=store,
            )
            objects = list((store.root / "objects").rglob("*.blob"))
            records = list((store.root / "records").glob("*.json"))
        self.assertIs(outcome.scan.status, ScanStatus.BLOCKED)
        self.assertIsNone(outcome.record)
        self.assertEqual(objects, [])
        self.assertEqual(records, [])


class TestSyntheticGate(unittest.TestCase):
    """Tests 48 und 49 — Synthetic-only-Grenze."""

    def test_48_missing_synthetic_confirmation_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(QuarantineInputRejected) as ctx:
                run_scan(
                    input_path=_write(tmp, f"{MARKER}\ntext\n"),
                    policy=POLICY,
                    source_reference=SOURCE_REF,
                    synthetic_confirmed=False,
                )
        self.assertEqual(
            ctx.exception.reason,
            ReasonCode.QUARANTINE_SYNTHETIC_CONFIRMATION_MISSING,
        )

    def test_49_source_ref_without_synthetic_prefix_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(QuarantineInputRejected) as ctx:
                run_scan(
                    input_path=_write(tmp, f"{MARKER}\ntext\n"),
                    policy=POLICY,
                    source_reference="real-source-1",
                    synthetic_confirmed=True,
                )
        self.assertEqual(
            ctx.exception.reason, ReasonCode.QUARANTINE_SOURCE_REF_NOT_SYNTHETIC
        )

    def test_source_ref_with_unsafe_characters_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(QuarantineInputRejected) as ctx:
                run_scan(
                    input_path=_write(tmp, f"{MARKER}\ntext\n"),
                    policy=POLICY,
                    source_reference="synthetic:../escape",
                    synthetic_confirmed=True,
                )
        self.assertEqual(
            ctx.exception.reason, ReasonCode.QUARANTINE_SOURCE_REF_INVALID
        )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
