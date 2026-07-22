"""Tests der Source-Registry-Policy (CBP-WP-014).

Deckt die fail-closed Validierung ab (Fälle 1–14). Ausschließlich
Standardbibliothek, keine realen Quellen, keine realen Pfade.
"""

from __future__ import annotations

import copy
import os
import unittest
from pathlib import Path
from unittest import mock

from core.core_brain.errors import RegistryPolicyError, ReasonCode
from core.core_brain.registry.policy import load_policy, parse_policy_mapping

REPO_ROOT = Path(__file__).resolve().parent.parent
EXAMPLE_POLICY = REPO_ROOT / "config" / "source_registry_policy.example.toml"

_BASE: dict[str, object] = {
    "schema_version": "1.0",
    "max_definition_bytes": 65536,
    "max_key_chars": 64,
    "max_display_name_chars": 128,
    "allowed_source_kinds": ["markdown"],
    "allowed_data_classes": ["public", "internal"],
    "allowed_ai_eligibility": ["allowed", "restricted"],
    "require_synthetic_reference": True,
    "allow_activation": False,
    "allow_content_access": False,
    "allow_network": False,
    "allow_updates": False,
    "allow_deletion": False,
    "allow_retirement": True,
}


def _mapping(**overrides: object) -> dict[str, object]:
    data = copy.deepcopy(_BASE)
    data.update(overrides)
    return data


class TestRegistryPolicy(unittest.TestCase):
    """Fälle 1 bis 12."""

    def test_1_example_policy_valid(self) -> None:
        policy = load_policy(EXAMPLE_POLICY)
        self.assertEqual(policy.schema_version, "1.0")
        self.assertEqual(policy.allowed_source_kinds, ("markdown",))
        self.assertFalse(policy.allow_activation)
        self.assertTrue(policy.allow_retirement)
        self.assertEqual(len(policy.policy_sha256), 64)

    def test_2_unknown_field_blocks(self) -> None:
        with self.assertRaises(RegistryPolicyError) as ctx:
            parse_policy_mapping(_mapping(surprise=1), "0" * 64)
        self.assertEqual(ctx.exception.reason, ReasonCode.REGISTRY_POLICY_UNKNOWN_FIELD)

    def test_3_unknown_version_blocks(self) -> None:
        with self.assertRaises(RegistryPolicyError) as ctx:
            parse_policy_mapping(_mapping(schema_version="9.9"), "0" * 64)
        self.assertEqual(
            ctx.exception.reason, ReasonCode.REGISTRY_POLICY_SCHEMA_UNSUPPORTED
        )

    def test_4_missing_field_blocks(self) -> None:
        data = _mapping()
        del data["allow_network"]
        with self.assertRaises(RegistryPolicyError) as ctx:
            parse_policy_mapping(data, "0" * 64)
        self.assertEqual(ctx.exception.reason, ReasonCode.REGISTRY_POLICY_MISSING_FIELD)

    def test_5_invalid_max_values_block(self) -> None:
        for field, value in (
            ("max_definition_bytes", 0),
            ("max_key_chars", -1),
            ("max_display_name_chars", 10**9),
        ):
            with self.subTest(field=field, value=value):
                with self.assertRaises(RegistryPolicyError) as ctx:
                    parse_policy_mapping(_mapping(**{field: value}), "0" * 64)
                self.assertEqual(
                    ctx.exception.reason, ReasonCode.REGISTRY_POLICY_INVALID_VALUE
                )

    def test_6_empty_allowlist_blocks(self) -> None:
        for field in (
            "allowed_source_kinds",
            "allowed_data_classes",
            "allowed_ai_eligibility",
        ):
            with self.subTest(field=field):
                with self.assertRaises(RegistryPolicyError) as ctx:
                    parse_policy_mapping(_mapping(**{field: []}), "0" * 64)
                self.assertEqual(
                    ctx.exception.reason, ReasonCode.REGISTRY_POLICY_INVALID_VALUE
                )

    def test_7_allow_activation_blocks(self) -> None:
        with self.assertRaises(RegistryPolicyError) as ctx:
            parse_policy_mapping(_mapping(allow_activation=True), "0" * 64)
        self.assertEqual(
            ctx.exception.reason, ReasonCode.REGISTRY_POLICY_ACTIVATION_ENABLED
        )

    def test_8_allow_content_access_blocks(self) -> None:
        with self.assertRaises(RegistryPolicyError) as ctx:
            parse_policy_mapping(_mapping(allow_content_access=True), "0" * 64)
        self.assertEqual(
            ctx.exception.reason, ReasonCode.REGISTRY_POLICY_CONTENT_ACCESS_ENABLED
        )

    def test_9_allow_network_blocks(self) -> None:
        with self.assertRaises(RegistryPolicyError) as ctx:
            parse_policy_mapping(_mapping(allow_network=True), "0" * 64)
        self.assertEqual(
            ctx.exception.reason, ReasonCode.REGISTRY_POLICY_NETWORK_ENABLED
        )

    def test_10_allow_updates_blocks(self) -> None:
        with self.assertRaises(RegistryPolicyError) as ctx:
            parse_policy_mapping(_mapping(allow_updates=True), "0" * 64)
        self.assertEqual(
            ctx.exception.reason, ReasonCode.REGISTRY_POLICY_UPDATES_ENABLED
        )

    def test_11_allow_deletion_blocks(self) -> None:
        with self.assertRaises(RegistryPolicyError) as ctx:
            parse_policy_mapping(_mapping(allow_deletion=True), "0" * 64)
        self.assertEqual(
            ctx.exception.reason, ReasonCode.REGISTRY_POLICY_DELETION_ENABLED
        )

    def test_12_allow_retirement_false_blocks(self) -> None:
        with self.assertRaises(RegistryPolicyError) as ctx:
            parse_policy_mapping(_mapping(allow_retirement=False), "0" * 64)
        self.assertEqual(
            ctx.exception.reason, ReasonCode.REGISTRY_POLICY_RETIREMENT_DISABLED
        )


class TestPolicyNotOverridable(unittest.TestCase):
    """Fälle 13 und 14."""

    def test_13_environment_does_not_override_policy(self) -> None:
        with mock.patch.dict(
            os.environ,
            {
                "REGISTRY_ALLOW_ACTIVATION": "true",
                "REGISTRY_ALLOW_NETWORK": "true",
            },
        ):
            policy = load_policy(EXAMPLE_POLICY)
        self.assertFalse(policy.allow_activation)
        self.assertFalse(policy.allow_network)

    def test_14_policy_module_reads_neither_environ_nor_argv(self) -> None:
        source = (
            REPO_ROOT / "core" / "core_brain" / "registry" / "policy.py"
        ).read_text(encoding="utf-8")
        self.assertNotIn("import os", source)
        self.assertNotIn("import sys", source)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
