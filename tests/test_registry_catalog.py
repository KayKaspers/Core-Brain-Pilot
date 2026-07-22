"""Tests des abgeleiteten Registry-Katalogs (CBP-WP-014).

Deckt die Fälle 55–64 ab: deterministische Sortierung, korrekte Zählungen,
minimierte Einträge, Rekonstruierbarkeit und fail-closed Integritätsschutz
ohne Teilkatalog.
"""

from __future__ import annotations

import json
import unittest
from datetime import UTC, datetime
from pathlib import Path
from tempfile import TemporaryDirectory

from core.core_brain.errors import RegistryCatalogError, ReasonCode
from core.core_brain.registry import (
    LifecycleState,
    RegistryStorage,
    build_catalog,
    load_policy,
    register,
    retire,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
POLICY = load_policy(REPO_ROOT / "config" / "source_registry_policy.example.toml")
CLOCK = lambda: datetime(2026, 7, 22, 12, 0, 0, tzinfo=UTC)  # noqa: E731

_DEF = """schema_version = "1.0"
namespace = "{ns}"
source_key = "{key}"
display_name = "Display {key}"
collection_key = "demo-collection"
domain_key = "demo-domain"
source_kind = "markdown"
data_class = "internal"
ai_eligibility = "restricted"
owner_role = "operator"
source_reference = "synthetic:{key}"
synthetic_test_only = true
activation_enabled = false
content_access_enabled = false
network_enabled = false
"""


def _register(tmp: str, storage: RegistryStorage, ns: str, key: str):
    path = Path(tmp) / f"{ns}-{key}.toml"
    path.write_text(_DEF.format(ns=ns, key=key), encoding="utf-8")
    return register(
        definition_path=path,
        policy=POLICY,
        storage=storage,
        synthetic_confirmed=True,
        clock=CLOCK,
    )


class TestCatalog(unittest.TestCase):
    """Fälle 55 bis 64."""

    def test_55_to_57_sorted_counts(self) -> None:
        with TemporaryDirectory() as tmp:
            storage = RegistryStorage(Path(tmp) / "reg")
            _register(tmp, storage, "ns", "gamma")
            _register(tmp, storage, "ns", "alpha")
            r_beta = _register(tmp, storage, "ns", "beta")
            retire(
                storage=storage,
                source_id=r_beta.source_id,
                synthetic_confirmed=True,
                clock=CLOCK,
            )
            catalog = build_catalog(storage, clock=CLOCK)
        ids = [e.source_id for e in catalog.entries]
        self.assertEqual(ids, sorted(ids))
        self.assertEqual(catalog.record_count, 3)
        self.assertEqual(catalog.retired_count, 1)
        self.assertEqual(catalog.registered_disabled_count, 2)

    def test_58_entry_is_minimized(self) -> None:
        with TemporaryDirectory() as tmp:
            storage = RegistryStorage(Path(tmp) / "reg")
            _register(tmp, storage, "ns", "alpha")
            catalog = build_catalog(storage, clock=CLOCK)
            entry = catalog.entries[0].to_dict()
        self.assertEqual(
            set(entry),
            {
                "source_id",
                "namespace",
                "source_key",
                "display_name",
                "collection_key",
                "domain_key",
                "source_kind",
                "data_class",
                "ai_eligibility",
                "lifecycle_state",
            },
        )
        self.assertNotIn("source_reference", entry)
        self.assertNotIn("definition_sha256", entry)

    def test_59_60_no_reference_path_or_url(self) -> None:
        with TemporaryDirectory() as tmp:
            storage = RegistryStorage(Path(tmp) / "reg")
            _register(tmp, storage, "ns", "alpha")
            text = json.dumps(build_catalog(storage, clock=CLOCK).to_dict())
        self.assertNotIn("synthetic:", text)
        self.assertNotIn("source_reference", text)
        self.assertNotIn("://", text)
        self.assertNotIn(str(tmp), text)

    def test_61_reconstructable_from_records_and_events(self) -> None:
        with TemporaryDirectory() as tmp:
            storage = RegistryStorage(Path(tmp) / "reg")
            r = _register(tmp, storage, "ns", "alpha")
            retire(
                storage=storage,
                source_id=r.source_id,
                synthetic_confirmed=True,
                clock=CLOCK,
            )
            first = build_catalog(storage, clock=CLOCK).to_dict()
            # Katalogdatei löschen und neu ableiten.
            (storage.root / "catalog" / "catalog.json").unlink()
            second = build_catalog(storage, clock=CLOCK).to_dict()
        self.assertEqual(first, second)
        self.assertEqual(second["entries"][0]["lifecycle_state"], "RETIRED")

    def test_62_63_corrupt_record_blocks_whole_catalog(self) -> None:
        with TemporaryDirectory() as tmp:
            storage = RegistryStorage(Path(tmp) / "reg")
            _register(tmp, storage, "ns", "alpha")
            good = _register(tmp, storage, "ns", "beta")
            # einen Record beschädigen.
            (storage.root / "records" / f"{good.source_id}.json").write_text(
                "{ corrupt", encoding="utf-8"
            )
            catalog_path = storage.root / "catalog" / "catalog.json"
            before = catalog_path.read_bytes()
            with self.assertRaises(RegistryCatalogError) as ctx:
                build_catalog(storage, clock=CLOCK)
            after = catalog_path.read_bytes()
        self.assertEqual(
            ctx.exception.reason, ReasonCode.REGISTRY_CATALOG_INTEGRITY_ERROR
        )
        # kein Teilkatalog: die bestehende Katalogdatei ist unverändert.
        self.assertEqual(before, after)

    def test_64_atomic_catalog_replacement(self) -> None:
        with TemporaryDirectory() as tmp:
            storage = RegistryStorage(Path(tmp) / "reg")
            _register(tmp, storage, "ns", "alpha")
            _register(tmp, storage, "ns", "beta")  # ersetzt den Katalog atomar
            text = (storage.root / "catalog" / "catalog.json").read_text(
                encoding="utf-8"
            )
            parsed = json.loads(text)  # gültiges JSON nach Ersetzung
        self.assertEqual(parsed["record_count"], 2)
        self.assertEqual(len(list((storage.root / "catalog").glob("*.tmp-*"))), 0)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
