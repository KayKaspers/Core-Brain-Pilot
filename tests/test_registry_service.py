"""Tests der Registry-Orchestrierung und des Retirements (CBP-WP-014).

Deckt die Fälle 48–54 ab: append-only Retirement-Event, Idempotenz, keine
Reaktivierung und stabile, minimierte Events.
"""

from __future__ import annotations

import json
import unittest
from datetime import UTC, datetime
from pathlib import Path
from tempfile import TemporaryDirectory

from core.core_brain.errors import RegistryNotFound, ReasonCode
from core.core_brain.registry import (
    LifecycleState,
    RegistryStorage,
    inspect,
    load_policy,
    register,
    retire,
)
from core.core_brain.registry.models import EVENT_FIELDS
from core.core_brain.registry.service import RETIREMENT_REASON_CODE

REPO_ROOT = Path(__file__).resolve().parent.parent
POLICY = load_policy(REPO_ROOT / "config" / "source_registry_policy.example.toml")
CLOCK = lambda: datetime(2026, 7, 22, 12, 0, 0, tzinfo=UTC)  # noqa: E731

_DEF = """schema_version = "1.0"
namespace = "synthetic-demo"
source_key = "notes-alpha"
display_name = "Synthetische Notiz"
collection_key = "demo-collection"
domain_key = "demo-domain"
source_kind = "markdown"
data_class = "internal"
ai_eligibility = "restricted"
owner_role = "operator"
source_reference = "synthetic:demo"
synthetic_test_only = true
activation_enabled = false
content_access_enabled = false
network_enabled = false
"""


def _register(tmp: str, storage: RegistryStorage):
    path = Path(tmp) / "def.toml"
    path.write_text(_DEF, encoding="utf-8")
    return register(
        definition_path=path,
        policy=POLICY,
        storage=storage,
        synthetic_confirmed=True,
        clock=CLOCK,
    )


class TestRetirement(unittest.TestCase):
    """Fälle 48 bis 54."""

    def test_48_51_retirement_creates_one_event_and_retires(self) -> None:
        with TemporaryDirectory() as tmp:
            storage = RegistryStorage(Path(tmp) / "reg")
            record = _register(tmp, storage)
            outcome = retire(
                storage=storage,
                source_id=record.source_id,
                synthetic_confirmed=True,
                clock=CLOCK,
            )
            events = list((storage.root / "events").rglob("*.json"))
        self.assertIsNotNone(outcome.event)
        self.assertEqual(len(events), 1)
        self.assertIs(outcome.lifecycle_state, LifecycleState.RETIRED)

    def test_49_event_is_append_only(self) -> None:
        with TemporaryDirectory() as tmp:
            storage = RegistryStorage(Path(tmp) / "reg")
            record = _register(tmp, storage)
            retire(
                storage=storage,
                source_id=record.source_id,
                synthetic_confirmed=True,
                clock=CLOCK,
            )
            event_path = next((storage.root / "events").rglob("*.json"))
            first = event_path.read_bytes()
            # zweites Retirement erzeugt kein neues und ändert kein Event.
            retire(
                storage=storage,
                source_id=record.source_id,
                synthetic_confirmed=True,
                clock=lambda: datetime(2030, 1, 1, tzinfo=UTC),
            )
            second = event_path.read_bytes()
        self.assertEqual(first, second)

    def test_50_event_has_no_free_text_or_paths(self) -> None:
        with TemporaryDirectory() as tmp:
            storage = RegistryStorage(Path(tmp) / "reg")
            record = _register(tmp, storage)
            retire(
                storage=storage,
                source_id=record.source_id,
                synthetic_confirmed=True,
                clock=CLOCK,
            )
            text = next((storage.root / "events").rglob("*.json")).read_text(
                encoding="utf-8"
            )
            data = json.loads(text)
        self.assertEqual(set(data), EVENT_FIELDS)
        self.assertEqual(data["reason_code"], RETIREMENT_REASON_CODE)
        self.assertNotIn("://", text)
        self.assertNotIn(str(tmp), text)

    def test_52_identical_repetition_idempotent(self) -> None:
        with TemporaryDirectory() as tmp:
            storage = RegistryStorage(Path(tmp) / "reg")
            record = _register(tmp, storage)
            kwargs = dict(
                storage=storage, source_id=record.source_id, synthetic_confirmed=True
            )
            first = retire(clock=CLOCK, **kwargs)
            second = retire(clock=CLOCK, **kwargs)
            events = list((storage.root / "events").rglob("*.json"))
        self.assertIsNotNone(first.event)
        self.assertIsNone(second.event)
        self.assertEqual(len(events), 1)

    def test_53_retire_unknown_id_blocks(self) -> None:
        with TemporaryDirectory() as tmp:
            storage = RegistryStorage(Path(tmp) / "reg")
            with self.assertRaises(RegistryNotFound) as ctx:
                retire(
                    storage=storage,
                    source_id="src-" + "f" * 24,
                    synthetic_confirmed=True,
                )
        self.assertEqual(ctx.exception.reason, ReasonCode.REGISTRY_RECORD_NOT_FOUND)

    def test_54_no_reactivation_exists(self) -> None:
        # Nach Retirement bleibt der wirksame Zustand RETIRED; es gibt keine
        # Service-Funktion, die REGISTERED_DISABLED wiederherstellt.
        from core.core_brain.registry import service

        self.assertNotIn("activate", service.__all__)
        self.assertNotIn("reactivate", service.__all__)
        with TemporaryDirectory() as tmp:
            storage = RegistryStorage(Path(tmp) / "reg")
            record = _register(tmp, storage)
            retire(
                storage=storage,
                source_id=record.source_id,
                synthetic_confirmed=True,
                clock=CLOCK,
            )
            _, state = inspect(storage, record.source_id)
        self.assertIs(state, LifecycleState.RETIRED)

    def test_synthetic_confirmation_required_for_retire(self) -> None:
        with TemporaryDirectory() as tmp:
            storage = RegistryStorage(Path(tmp) / "reg")
            record = _register(tmp, storage)
            from core.core_brain.errors import RegistryDefinitionRejected

            with self.assertRaises(RegistryDefinitionRejected) as ctx:
                retire(
                    storage=storage,
                    source_id=record.source_id,
                    synthetic_confirmed=False,
                )
        self.assertEqual(
            ctx.exception.reason, ReasonCode.REGISTRY_SYNTHETIC_CONFIRMATION_MISSING
        )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
