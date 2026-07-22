"""Tests des content-addressed Quarantänespeichers (CBP-WP-013).

Deckt Root-Grenzen, digestbasierte Objektpfade, Payload-Unveränderlichkeit,
kanonische Manifeste ohne Pfad und Inhalt, Idempotenz, Kollision, atomare
Schreibweise, Record-Validierung und deterministische injizierte Uhr ab.
"""

from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path
from unittest import mock

from core.core_brain.errors import QuarantineStoreError, ReasonCode
from core.core_brain.quarantine import (
    ScanStatus,
    load_policy,
    run_stage,
)
from core.core_brain.quarantine.models import (
    IMPLEMENTATION_VERSION,
    RECORD_SCHEMA_VERSION,
    QuarantineRecord,
)
from core.core_brain.quarantine.store import QuarantineStore

REPO_ROOT = Path(__file__).resolve().parent.parent
EXAMPLE_POLICY = REPO_ROOT / "config" / "quarantine_policy.example.toml"
POLICY = load_policy(EXAMPLE_POLICY)
MARKER = "<!-- synthetic-test-only -->"
SOURCE_REF = "synthetic:store-test"
FIXED_CLOCK = lambda: datetime(2026, 7, 22, 12, 0, 0, tzinfo=UTC)  # noqa: E731


def _record(**overrides: object) -> QuarantineRecord:
    base: dict[str, object] = {
        "record_schema_version": RECORD_SCHEMA_VERSION,
        "quarantine_id": "a" * 64,
        "source_reference": SOURCE_REF,
        "content_sha256": "b" * 64,
        "byte_size": 3,
        "media_type": "text/markdown",
        "policy_schema_version": "1.0",
        "policy_sha256": "c" * 64,
        "scan_status": ScanStatus.READY_FOR_HUMAN_REVIEW,
        "finding_codes": (),
        "finding_count": 0,
        "stored_object_reference": "objects/sha256/bb/" + "b" * 64 + ".blob",
        "created_at": "2026-07-22T12:00:00Z",
        "implementation_version": IMPLEMENTATION_VERSION,
    }
    base.update(overrides)
    return QuarantineRecord(**base)  # type: ignore[arg-type]


def _stage(tmp: str, text: str, *, clock=None):  # type: ignore[no-untyped-def]
    target = Path(tmp) / "artifact.md"
    target.write_text(text, encoding="utf-8")
    store = QuarantineStore(Path(tmp) / "store")
    kwargs = {"clock": clock} if clock is not None else {}
    outcome = run_stage(
        input_path=target,
        policy=POLICY,
        source_reference=SOURCE_REF,
        synthetic_confirmed=True,
        store=store,
        **kwargs,
    )
    return store, outcome


class TestStoreRoot(unittest.TestCase):
    """Tests 28 und 29 — Root-Grenzen."""

    def test_28_store_inside_repository_blocks(self) -> None:
        with self.assertRaises(QuarantineStoreError) as ctx:
            QuarantineStore(REPO_ROOT / "tmp-store-should-not-exist")
        self.assertEqual(
            ctx.exception.reason, ReasonCode.QUARANTINE_STORE_INSIDE_REPOSITORY
        )

    def test_29_store_symlink_blocks(self) -> None:
        # Plattformneutral: die Symlink-Regel wird deterministisch geprüft,
        # indem die Symlink-Erkennung für den Root aktiviert wird.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "link-store"
            root.mkdir()
            with mock.patch("pathlib.Path.is_symlink", return_value=True):
                with self.assertRaises(QuarantineStoreError) as ctx:
                    QuarantineStore(root)
        self.assertEqual(
            ctx.exception.reason, ReasonCode.QUARANTINE_STORE_IS_SYMLINK
        )


class TestStoreObjectsAndRecords(unittest.TestCase):
    """Tests 30 bis 40."""

    def test_30_object_path_stays_in_store(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store, outcome = _stage(tmp, f"{MARKER}\n# ok\ntext\n")
            reference = outcome.record.stored_object_reference
            self.assertFalse(Path(reference).is_absolute())
            resolved = (store.root / reference).resolve()
            self.assertTrue(resolved.is_relative_to(store.root))
            self.assertTrue(resolved.is_file())

    def test_31_payload_is_unchanged(self) -> None:
        # Exakte Bytes ohne Zeilenendennormalisierung (write_bytes).
        raw = f"{MARKER}\n# payload\nunveraendert\n".encode()
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "artifact.md"
            target.write_bytes(raw)
            store = QuarantineStore(Path(tmp) / "store")
            outcome = run_stage(
                input_path=target,
                policy=POLICY,
                source_reference=SOURCE_REF,
                synthetic_confirmed=True,
                store=store,
            )
            blob = (store.root / outcome.record.stored_object_reference).read_bytes()
        self.assertEqual(blob, raw)
        self.assertEqual(hashlib.sha256(blob).hexdigest(), outcome.record.content_sha256)

    def test_32_manifest_is_canonical_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store, outcome = _stage(tmp, f"{MARKER}\ntext\n")
            path = store.root / "records" / f"{outcome.record.quarantine_id}.json"
            text = path.read_text(encoding="utf-8")
            parsed = json.loads(text)
            canonical = json.dumps(parsed, sort_keys=True, ensure_ascii=False, indent=2)
        self.assertEqual(text, canonical + "\n")

    def test_33_manifest_has_no_input_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "very-unique-filename-33.md"
            target.write_text(f"{MARKER}\ntext\n", encoding="utf-8")
            store = QuarantineStore(Path(tmp) / "store")
            outcome = run_stage(
                input_path=target,
                policy=POLICY,
                source_reference=SOURCE_REF,
                synthetic_confirmed=True,
                store=store,
            )
            text = (
                store.root / "records" / f"{outcome.record.quarantine_id}.json"
            ).read_text(encoding="utf-8")
        self.assertNotIn("very-unique-filename-33", text)
        self.assertNotIn(str(target), text)

    def test_34_manifest_has_no_payload(self) -> None:
        token = "UNIQUE-BODY-TOKEN-34"
        with tempfile.TemporaryDirectory() as tmp:
            store, outcome = _stage(tmp, f"{MARKER}\n{token}\n")
            text = (
                store.root / "records" / f"{outcome.record.quarantine_id}.json"
            ).read_text(encoding="utf-8")
        self.assertNotIn(token, text)

    def test_35_finding_codes_sorted_and_deduplicated(self) -> None:
        # Zwei E-Mail-Zeilen und eine Telefonzeile ergeben genau zwei Codes.
        with tempfile.TemporaryDirectory() as tmp:
            store, outcome = _stage(
                tmp,
                f"{MARKER}\na@example.com\nb@example.com\n+1-555-0100\n",
            )
        codes = outcome.record.finding_codes
        self.assertEqual(list(codes), sorted(set(codes)))
        self.assertEqual(outcome.record.finding_count, len(codes))

    def test_36_identical_repeat_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "artifact.md"
            target.write_text(f"{MARKER}\ntext\n", encoding="utf-8")
            store = QuarantineStore(Path(tmp) / "store")
            kwargs = dict(
                input_path=target,
                policy=POLICY,
                source_reference=SOURCE_REF,
                synthetic_confirmed=True,
                store=store,
                clock=FIXED_CLOCK,
            )
            first = run_stage(**kwargs)
            second = run_stage(**kwargs)
            records = list((store.root / "records").glob("*.json"))
            objects = list((store.root / "objects").rglob("*.blob"))
        self.assertEqual(first.record.to_dict(), second.record.to_dict())
        self.assertEqual(len(records), 1)
        self.assertEqual(len(objects), 1)

    def test_37_record_collision_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = QuarantineStore(Path(tmp) / "store")
            store.write_record(_record())
            with self.assertRaises(QuarantineStoreError) as ctx:
                store.write_record(_record(content_sha256="d" * 64))
        self.assertEqual(
            ctx.exception.reason, ReasonCode.QUARANTINE_RECORD_COLLISION
        )

    def test_37b_object_collision_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = QuarantineStore(Path(tmp) / "store")
            payload = b"synthetic-payload"
            digest = hashlib.sha256(payload).hexdigest()
            reference = store.object_reference(digest)
            target = store.root / reference
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(b"different-bytes")
            with self.assertRaises(QuarantineStoreError) as ctx:
                store.write_object(digest, payload)
        self.assertEqual(
            ctx.exception.reason, ReasonCode.QUARANTINE_OBJECT_HASH_COLLISION
        )

    def test_38_atomic_write_leaves_no_partial_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = QuarantineStore(Path(tmp) / "store")
            record = _record()
            with mock.patch(
                "core.core_brain.quarantine.store.os.replace",
                side_effect=OSError("boom"),
            ):
                with self.assertRaises(OSError):
                    store.write_record(record)
            records_dir = store.root / "records"
            self.assertFalse((records_dir / f"{record.quarantine_id}.json").exists())
            self.assertEqual(list(records_dir.glob("*.tmp-*")), [])

    def test_39_record_validation_blocks_unknown_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = QuarantineStore(Path(tmp) / "store")
            record = _record()
            payload = record.to_dict()
            payload["surprise"] = 1
            path = store.root / "records" / f"{record.quarantine_id}.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaises(QuarantineStoreError) as ctx:
                store.load_record(record.quarantine_id)
        self.assertEqual(ctx.exception.reason, ReasonCode.QUARANTINE_RECORD_INVALID)

    def test_39b_record_not_found_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = QuarantineStore(Path(tmp) / "store")
            with self.assertRaises(QuarantineStoreError) as ctx:
                store.load_record("f" * 64)
        self.assertEqual(ctx.exception.reason, ReasonCode.QUARANTINE_RECORD_NOT_FOUND)

    def test_40_injected_clock_is_deterministic(self) -> None:
        outcomes = []
        for _ in range(2):
            with tempfile.TemporaryDirectory() as tmp:
                _, outcome = _stage(tmp, f"{MARKER}\ntext\n", clock=FIXED_CLOCK)
                outcomes.append(outcome.record)
        self.assertEqual(outcomes[0].created_at, "2026-07-22T12:00:00Z")
        self.assertEqual(outcomes[0].to_dict(), outcomes[1].to_dict())


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
