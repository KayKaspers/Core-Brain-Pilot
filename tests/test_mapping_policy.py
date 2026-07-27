"""Tests der Source-Mapping-Validierungspolicy (CBP-WP-015, Faelle 1-17)."""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from core.core_brain.errors import MappingPolicyError, ReasonCode
from core.core_brain.mapping import load_policy

REPO_ROOT = Path(__file__).resolve().parent.parent
EXAMPLE_POLICY = REPO_ROOT / "config" / "source_mapping_validation_policy.example.toml"

# Alle 18 Policy-Felder mit ihren verbindlichen Werten als TOML-Rohtext.
_BASE: dict[str, str] = {
    "schema_version": '"1.0"',
    "max_draft_bytes": "65536",
    "required_mapping_schema_version": '"1.0"',
    "accepted_document_profile": '"canonical-json-yaml-subset"',
    "canonical_contract_field_count": "31",
    "required_field_count": "29",
    "optional_field_count": "2",
    "require_synthetic_test_only": "true",
    "require_registry_binding": "true",
    "require_registered_disabled": "true",
    "require_single_boundary": "true",
    "require_collection_exact_match": "true",
    "require_data_class_exact_match": "true",
    "allow_activation": "false",
    "allow_persistence": "false",
    "allow_registry_write": "false",
    "allow_network": "false",
}


def _render(
    overrides: dict[str, str] | None = None,
    drop: tuple[str, ...] = (),
    extra: dict[str, str] | None = None,
) -> str:
    data = dict(_BASE)
    for key in drop:
        data.pop(key, None)
    if overrides:
        data.update(overrides)
    lines = [f"{key} = {value}" for key, value in data.items()]
    if extra:
        lines.extend(f"{key} = {value}" for key, value in extra.items())
    return "\n".join(lines) + "\n"


def _load_text(text: str):
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "policy.toml"
        path.write_text(text, encoding="utf-8")
        return load_policy(path)


class TestPolicy(unittest.TestCase):
    """Die Policy ist fail-closed: jede Lockerung blockiert."""

    def test_01_example_policy_valid(self) -> None:
        policy = load_policy(EXAMPLE_POLICY)
        self.assertEqual(policy.canonical_contract_field_count, 31)
        self.assertEqual(policy.required_field_count, 29)
        self.assertEqual(policy.optional_field_count, 2)
        self.assertFalse(policy.allow_activation)
        self.assertFalse(policy.allow_persistence)
        self.assertFalse(policy.allow_registry_write)
        self.assertFalse(policy.allow_network)

    def test_02_unknown_field_blocks(self) -> None:
        with self.assertRaises(MappingPolicyError) as ctx:
            _load_text(_render(extra={"surprise_field": "true"}))
        self.assertEqual(ctx.exception.reason, ReasonCode.MAPPING_POLICY_UNKNOWN_FIELD)

    def test_03_unknown_version_blocks(self) -> None:
        with self.assertRaises(MappingPolicyError) as ctx:
            _load_text(_render(overrides={"schema_version": '"9.9"'}))
        self.assertEqual(
            ctx.exception.reason, ReasonCode.MAPPING_POLICY_SCHEMA_UNSUPPORTED
        )

    def test_04_missing_field_blocks(self) -> None:
        with self.assertRaises(MappingPolicyError) as ctx:
            _load_text(_render(drop=("max_draft_bytes",)))
        self.assertEqual(ctx.exception.reason, ReasonCode.MAPPING_POLICY_MISSING_FIELD)

    def test_05_wrong_counts_block(self) -> None:
        for field in (
            "canonical_contract_field_count",
            "required_field_count",
            "optional_field_count",
        ):
            with self.subTest(field=field):
                with self.assertRaises(MappingPolicyError) as ctx:
                    _load_text(_render(overrides={field: "7"}))
                self.assertEqual(
                    ctx.exception.reason,
                    ReasonCode.MAPPING_POLICY_FIELD_COUNT_INVALID,
                )

    def test_06_wrong_document_profile_blocks(self) -> None:
        with self.assertRaises(MappingPolicyError) as ctx:
            _load_text(
                _render(overrides={"accepted_document_profile": '"yaml-general"'})
            )
        self.assertEqual(ctx.exception.reason, ReasonCode.MAPPING_POLICY_INVALID_VALUE)

    def test_07_registry_binding_false_blocks(self) -> None:
        with self.assertRaises(MappingPolicyError):
            _load_text(_render(overrides={"require_registry_binding": "false"}))

    def test_08_registered_disabled_false_blocks(self) -> None:
        with self.assertRaises(MappingPolicyError):
            _load_text(_render(overrides={"require_registered_disabled": "false"}))

    def test_09_single_boundary_false_blocks(self) -> None:
        with self.assertRaises(MappingPolicyError):
            _load_text(_render(overrides={"require_single_boundary": "false"}))

    def test_10_collection_exact_false_blocks(self) -> None:
        with self.assertRaises(MappingPolicyError):
            _load_text(_render(overrides={"require_collection_exact_match": "false"}))

    def test_11_data_class_exact_false_blocks(self) -> None:
        with self.assertRaises(MappingPolicyError):
            _load_text(_render(overrides={"require_data_class_exact_match": "false"}))

    def test_12_allow_activation_true_blocks(self) -> None:
        with self.assertRaises(MappingPolicyError) as ctx:
            _load_text(_render(overrides={"allow_activation": "true"}))
        self.assertEqual(
            ctx.exception.reason, ReasonCode.MAPPING_POLICY_ACTIVATION_ENABLED
        )

    def test_13_allow_persistence_true_blocks(self) -> None:
        with self.assertRaises(MappingPolicyError) as ctx:
            _load_text(_render(overrides={"allow_persistence": "true"}))
        self.assertEqual(
            ctx.exception.reason, ReasonCode.MAPPING_POLICY_PERSISTENCE_ENABLED
        )

    def test_14_allow_registry_write_true_blocks(self) -> None:
        with self.assertRaises(MappingPolicyError) as ctx:
            _load_text(_render(overrides={"allow_registry_write": "true"}))
        self.assertEqual(
            ctx.exception.reason, ReasonCode.MAPPING_POLICY_REGISTRY_WRITE_ENABLED
        )

    def test_15_allow_network_true_blocks(self) -> None:
        with self.assertRaises(MappingPolicyError) as ctx:
            _load_text(_render(overrides={"allow_network": "true"}))
        self.assertEqual(
            ctx.exception.reason, ReasonCode.MAPPING_POLICY_NETWORK_ENABLED
        )

    def test_16_environment_overrides_nothing(self) -> None:
        # Eine gesetzte Environment-Variable darf die geladenen Werte nicht
        # veraendern; der Loader liest kein Environment.
        marker = "CBP_MAPPING_ALLOW_ACTIVATION"
        previous = os.environ.get(marker)
        os.environ[marker] = "true"
        try:
            policy = load_policy(EXAMPLE_POLICY)
        finally:
            if previous is None:
                os.environ.pop(marker, None)
            else:
                os.environ[marker] = previous
        self.assertFalse(policy.allow_activation)
        self.assertFalse(policy.allow_network)

    def test_17_cli_overrides_nothing(self) -> None:
        # Es gibt keinen CLI-Override der Sicherheitswerte; der Loader-Quelltext
        # liest weder Environment noch argv.
        source = (
            REPO_ROOT / "core" / "core_brain" / "mapping" / "policy.py"
        ).read_text(encoding="utf-8")
        self.assertNotIn("os.environ", source)
        self.assertNotIn("getenv", source)
        self.assertNotIn("sys.argv", source)
        policy = load_policy(EXAMPLE_POLICY)
        self.assertTrue(policy.require_registry_binding)
        self.assertTrue(policy.require_collection_exact_match)
        self.assertTrue(policy.require_data_class_exact_match)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
