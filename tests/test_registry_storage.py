"""Tests des Source-Registry-Speichers (CBP-WP-014).

Deckt die Fälle 32–47 ab: Root-Grenzen, ID-basierte Pfade, kanonische Records
ohne Pfad/URL/Inhalt, Idempotenz, Konflikt, atomare Schreibweise, Record-
Validierung und deterministische injizierte Uhr.
"""

from __future__ import annotations

import json
import unittest
from datetime import UTC, datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock

from core.core_brain.errors import RegistryStorageError, ReasonCode
from core.core_brain.registry import (
    LifecycleState,
    RegistryStorage,
    load_policy,
    register,
)
from core.core_brain.registry.models import RECORD_FIELDS, RegistryRecord

REPO_ROOT = Path(__file__).resolve().parent.parent
POLICY = load_policy(REPO_ROOT / "config" / "source_registry_policy.example.toml")
FIXED_CLOCK = lambda: datetime(2026, 7, 22, 12, 0, 0, tzinfo=UTC)  # noqa: E731

_DEF = """schema_version = "1.0"
namespace = "{ns}"
source_key = "{key}"
display_name = "{dn}"
collection_key = "demo-collection"
domain_key = "demo-domain"
source_kind = "markdown"
data_class = "internal"
ai_eligibility = "restricted"
owner_role = "operator"
source_reference = "synthetic:{ref}"
synthetic_test_only = true
activation_enabled = false
content_access_enabled = false
network_enabled = false
"""


def _write_def(tmp: str, *, ns="synthetic-demo", key="notes-alpha", dn="Name", ref="demo"):
    path = Path(tmp) / f"{ns}-{key}.toml"
    path.write_text(_DEF.format(ns=ns, key=key, dn=dn, ref=ref), encoding="utf-8")
    return path


def _record(**overrides: object) -> RegistryRecord:
    base: dict[str, object] = {
        "record_schema_version": "1.0",
        "source_id": "src-" + "a" * 24,
        "namespace": "ns-a",
        "source_key": "key-a",
        "display_name": "Name",
        "collection_key": "col-a",
        "domain_key": "dom-a",
        "source_kind": "markdown",
        "data_class": "internal",
        "ai_eligibility": "restricted",
        "owner_role": "operator",
        "source_reference": "synthetic:demo",
        "definition_sha256": "b" * 64,
        "policy_sha256": "c" * 64,
        "lifecycle_state": LifecycleState.REGISTERED_DISABLED,
        "registered_at": "2026-07-22T12:00:00Z",
        "implementation_version": "0.1.0.dev0",
    }
    base.update(overrides)
    return RegistryRecord(**base)  # type: ignore[arg-type]


class TestStorageRoot(unittest.TestCase):
    """Fälle 32 und 33."""

    def test_32_registry_in_repository_blocks(self) -> None:
        with self.assertRaises(RegistryStorageError) as ctx:
            RegistryStorage(REPO_ROOT / "tmp-registry-should-not-exist")
        self.assertEqual(
            ctx.exception.reason, ReasonCode.REGISTRY_STORE_INSIDE_REPOSITORY
        )

    def test_33_registry_symlink_blocks(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp) / "link-registry"
            root.mkdir()
            with mock.patch("pathlib.Path.is_symlink", return_value=True):
                with self.assertRaises(RegistryStorageError) as ctx:
                    RegistryStorage(root)
        self.assertEqual(ctx.exception.reason, ReasonCode.REGISTRY_STORE_IS_SYMLINK)


class TestRecordStorage(unittest.TestCase):
    """Fälle 34 bis 47."""

    def test_34_record_path_stays_in_registry(self) -> None:
        with TemporaryDirectory() as tmp:
            storage = RegistryStorage(Path(tmp) / "reg")
            record = register(
                definition_path=_write_def(tmp),
                policy=POLICY,
                storage=storage,
                synthetic_confirmed=True,
            )
            target = storage.root / "records" / f"{record.source_id}.json"
            self.assertTrue(target.resolve().is_relative_to(storage.root))
            self.assertTrue(target.is_file())

    def test_35_record_is_canonical_json(self) -> None:
        with TemporaryDirectory() as tmp:
            storage = RegistryStorage(Path(tmp) / "reg")
            record = register(
                definition_path=_write_def(tmp),
                policy=POLICY,
                storage=storage,
                synthetic_confirmed=True,
            )
            path = storage.root / "records" / f"{record.source_id}.json"
            text = path.read_text(encoding="utf-8")
            parsed = json.loads(text)
            canonical = json.dumps(parsed, sort_keys=True, ensure_ascii=False, indent=2)
        self.assertEqual(text, canonical + "\n")

    def test_36_to_39_record_has_no_path_url_content_or_locator(self) -> None:
        with TemporaryDirectory() as tmp:
            storage = RegistryStorage(Path(tmp) / "reg")
            record = register(
                definition_path=_write_def(tmp, dn="UNIQUE-DISPLAY-TOKEN"),
                policy=POLICY,
                storage=storage,
                synthetic_confirmed=True,
            )
            text = (
                storage.root / "records" / f"{record.source_id}.json"
            ).read_text(encoding="utf-8")
            data = json.loads(text)
        self.assertEqual(set(data), RECORD_FIELDS)  # keine Zusatzfelder
        self.assertNotIn("://", text)
        self.assertNotIn(str(tmp), text)
        self.assertNotIn("mapping", text.lower())
        self.assertNotIn("\\", text)

    def test_40_initial_state_registered_disabled(self) -> None:
        with TemporaryDirectory() as tmp:
            storage = RegistryStorage(Path(tmp) / "reg")
            record = register(
                definition_path=_write_def(tmp),
                policy=POLICY,
                storage=storage,
                synthetic_confirmed=True,
            )
        self.assertIs(record.lifecycle_state, LifecycleState.REGISTERED_DISABLED)

    def test_41_identical_registration_idempotent(self) -> None:
        with TemporaryDirectory() as tmp:
            storage = RegistryStorage(Path(tmp) / "reg")
            definition = _write_def(tmp)
            first = register(
                definition_path=definition,
                policy=POLICY,
                storage=storage,
                synthetic_confirmed=True,
                clock=FIXED_CLOCK,
            )
            second = register(
                definition_path=definition,
                policy=POLICY,
                storage=storage,
                synthetic_confirmed=True,
                clock=lambda: datetime(2030, 1, 1, tzinfo=UTC),
            )
            records = list((storage.root / "records").glob("*.json"))
        self.assertEqual(first.to_dict(), second.to_dict())
        self.assertEqual(len(records), 1)

    def test_42_differing_definition_same_identity_blocks(self) -> None:
        with TemporaryDirectory() as tmp:
            storage = RegistryStorage(Path(tmp) / "reg")
            register(
                definition_path=_write_def(tmp, dn="First"),
                policy=POLICY,
                storage=storage,
                synthetic_confirmed=True,
            )
            with self.assertRaises(RegistryStorageError) as ctx:
                register(
                    definition_path=_write_def(tmp, dn="Second"),
                    policy=POLICY,
                    storage=storage,
                    synthetic_confirmed=True,
                )
        self.assertEqual(ctx.exception.reason, ReasonCode.REGISTRY_RECORD_CONFLICT)

    def test_43_artificial_source_id_collision_blocks(self) -> None:
        with TemporaryDirectory() as tmp:
            storage = RegistryStorage(Path(tmp) / "reg")
            record = _record(source_id="src-" + "1" * 24, namespace="foreign")
            storage.write_record(record)
            # Zweiter Record mit derselben ID, aber abweichender Identität.
            with self.assertRaises(RegistryStorageError) as ctx:
                storage.write_record(_record(source_id="src-" + "1" * 24))
        self.assertEqual(ctx.exception.reason, ReasonCode.REGISTRY_RECORD_CONFLICT)

    def test_44_atomic_failure_leaves_no_partial_record(self) -> None:
        with TemporaryDirectory() as tmp:
            storage = RegistryStorage(Path(tmp) / "reg")
            record = _record()
            with mock.patch(
                "core.core_brain.registry.storage.os.replace",
                side_effect=OSError("boom"),
            ):
                with self.assertRaises(OSError):
                    storage.write_record(record)
            records_dir = storage.root / "records"
            self.assertFalse((records_dir / f"{record.source_id}.json").exists())
            self.assertEqual(list(records_dir.glob("*.tmp-*")), [])

    def test_45_unknown_record_field_blocks(self) -> None:
        with TemporaryDirectory() as tmp:
            storage = RegistryStorage(Path(tmp) / "reg")
            record = _record()
            payload = record.to_dict()
            payload["surprise"] = 1
            path = storage.root / "records" / f"{record.source_id}.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaises(RegistryStorageError) as ctx:
                storage.load_record(record.source_id)
        self.assertEqual(ctx.exception.reason, ReasonCode.REGISTRY_RECORD_INVALID)

    def test_46_corrupt_record_blocks(self) -> None:
        with TemporaryDirectory() as tmp:
            storage = RegistryStorage(Path(tmp) / "reg")
            source_id = "src-" + "a" * 24
            path = storage.root / "records" / f"{source_id}.json"
            path.write_text("{ not valid json", encoding="utf-8")
            with self.assertRaises(RegistryStorageError) as ctx:
                storage.load_record(source_id)
        self.assertEqual(ctx.exception.reason, ReasonCode.REGISTRY_RECORD_INVALID)

    def test_47_injected_clock_is_deterministic(self) -> None:
        records = []
        for _ in range(2):
            with TemporaryDirectory() as tmp:
                storage = RegistryStorage(Path(tmp) / "reg")
                record = register(
                    definition_path=_write_def(tmp),
                    policy=POLICY,
                    storage=storage,
                    synthetic_confirmed=True,
                    clock=FIXED_CLOCK,
                )
                records.append(record)
        self.assertEqual(records[0].registered_at, "2026-07-22T12:00:00Z")
        self.assertEqual(records[0].to_dict(), records[1].to_dict())

    def test_record_not_found_blocks(self) -> None:
        with TemporaryDirectory() as tmp:
            storage = RegistryStorage(Path(tmp) / "reg")
            with self.assertRaises(RegistryStorageError) as ctx:
                storage.load_record("src-" + "f" * 24)
        self.assertEqual(ctx.exception.reason, ReasonCode.REGISTRY_RECORD_NOT_FOUND)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
