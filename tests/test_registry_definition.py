"""Tests der Source-Definition-Validierung und Identität (CBP-WP-014).

Deckt die Fälle 15–31 ab: strikte Validierung, Slug-Grenzen, Pfad-/URL-Abwehr,
Synthetic-only-Grenze sowie deterministische Definition-Hashes und Source IDs.
Alle Testdaten sind synthetisch; keine realen Pfade oder URLs.
"""

from __future__ import annotations

import copy
import unittest
from pathlib import Path

from core.core_brain.errors import RegistryDefinitionRejected, ReasonCode
from core.core_brain.registry import derive_source_id, load_policy, validate_definition

REPO_ROOT = Path(__file__).resolve().parent.parent
POLICY = load_policy(REPO_ROOT / "config" / "source_registry_policy.example.toml")

_BASE: dict[str, object] = {
    "schema_version": "1.0",
    "namespace": "synthetic-demo",
    "source_key": "notes-alpha",
    "display_name": "Synthetische Notizsammlung",
    "collection_key": "demo-collection",
    "domain_key": "demo-domain",
    "source_kind": "markdown",
    "data_class": "internal",
    "ai_eligibility": "restricted",
    "owner_role": "operator",
    "source_reference": "synthetic:demo-notes-alpha",
    "synthetic_test_only": True,
    "activation_enabled": False,
    "content_access_enabled": False,
    "network_enabled": False,
}


def _defn(**overrides: object) -> dict[str, object]:
    data = copy.deepcopy(_BASE)
    data.update(overrides)
    return data


class TestDefinitionValidation(unittest.TestCase):
    """Fälle 15 bis 28."""

    def test_15_valid_definition(self) -> None:
        definition = validate_definition(_defn(), POLICY)
        self.assertEqual(definition.namespace, "synthetic-demo")
        self.assertTrue(definition.synthetic_test_only)
        self.assertFalse(definition.activation_enabled)
        self.assertEqual(len(definition.definition_sha256), 64)

    def test_16_unknown_field_blocks(self) -> None:
        with self.assertRaises(RegistryDefinitionRejected) as ctx:
            validate_definition(_defn(surprise="x"), POLICY)
        self.assertEqual(
            ctx.exception.reason, ReasonCode.REGISTRY_DEFINITION_UNKNOWN_FIELD
        )

    def test_17_missing_field_blocks(self) -> None:
        data = _defn()
        del data["domain_key"]
        with self.assertRaises(RegistryDefinitionRejected) as ctx:
            validate_definition(data, POLICY)
        self.assertEqual(
            ctx.exception.reason, ReasonCode.REGISTRY_DEFINITION_MISSING_FIELD
        )

    def test_18_invalid_namespace_blocks(self) -> None:
        with self.assertRaises(RegistryDefinitionRejected) as ctx:
            validate_definition(_defn(namespace="Bad_Namespace"), POLICY)
        self.assertEqual(
            ctx.exception.reason, ReasonCode.REGISTRY_DEFINITION_INVALID_SLUG
        )

    def test_19_invalid_source_key_blocks(self) -> None:
        with self.assertRaises(RegistryDefinitionRejected) as ctx:
            validate_definition(_defn(source_key="UPPER"), POLICY)
        self.assertEqual(
            ctx.exception.reason, ReasonCode.REGISTRY_DEFINITION_INVALID_SLUG
        )

    def test_20_path_separator_blocks(self) -> None:
        with self.assertRaises(RegistryDefinitionRejected) as ctx:
            validate_definition(_defn(namespace="ns/evil"), POLICY)
        self.assertEqual(
            ctx.exception.reason, ReasonCode.REGISTRY_DEFINITION_PATH_SEPARATOR
        )

    def test_21_dotdot_blocks(self) -> None:
        with self.assertRaises(RegistryDefinitionRejected) as ctx:
            validate_definition(_defn(source_key="a..b"), POLICY)
        self.assertEqual(ctx.exception.reason, ReasonCode.REGISTRY_DEFINITION_DOTDOT)

    def test_22_url_indicator_blocks(self) -> None:
        # URL-Marker ohne Schrägstrich (der sonst zuerst als Pfadseparator
        # blockiert würde) — belegt gezielt die URL-Indikatorregel.
        with self.assertRaises(RegistryDefinitionRejected) as ctx:
            validate_definition(_defn(display_name="Contact www.example.com"), POLICY)
        self.assertEqual(
            ctx.exception.reason, ReasonCode.REGISTRY_DEFINITION_URL_INDICATOR
        )

    def test_22b_url_with_slash_blocks_as_path_separator(self) -> None:
        with self.assertRaises(RegistryDefinitionRejected) as ctx:
            validate_definition(_defn(display_name="https://example.com"), POLICY)
        self.assertEqual(
            ctx.exception.reason, ReasonCode.REGISTRY_DEFINITION_PATH_SEPARATOR
        )

    def test_23_missing_synthetic_prefix_blocks(self) -> None:
        with self.assertRaises(RegistryDefinitionRejected) as ctx:
            validate_definition(_defn(source_reference="real-source-1"), POLICY)
        self.assertEqual(
            ctx.exception.reason,
            ReasonCode.REGISTRY_DEFINITION_SOURCE_REF_NOT_SYNTHETIC,
        )

    def test_24_synthetic_false_blocks(self) -> None:
        with self.assertRaises(RegistryDefinitionRejected) as ctx:
            validate_definition(_defn(synthetic_test_only=False), POLICY)
        self.assertEqual(
            ctx.exception.reason, ReasonCode.REGISTRY_DEFINITION_NOT_SYNTHETIC
        )

    def test_25_activation_enabled_blocks(self) -> None:
        with self.assertRaises(RegistryDefinitionRejected) as ctx:
            validate_definition(_defn(activation_enabled=True), POLICY)
        self.assertEqual(
            ctx.exception.reason, ReasonCode.REGISTRY_DEFINITION_ACTIVATION_REQUESTED
        )

    def test_26_content_access_enabled_blocks(self) -> None:
        with self.assertRaises(RegistryDefinitionRejected) as ctx:
            validate_definition(_defn(content_access_enabled=True), POLICY)
        self.assertEqual(
            ctx.exception.reason,
            ReasonCode.REGISTRY_DEFINITION_CONTENT_ACCESS_REQUESTED,
        )

    def test_27_network_enabled_blocks(self) -> None:
        with self.assertRaises(RegistryDefinitionRejected) as ctx:
            validate_definition(_defn(network_enabled=True), POLICY)
        self.assertEqual(
            ctx.exception.reason, ReasonCode.REGISTRY_DEFINITION_NETWORK_REQUESTED
        )

    def test_28_source_locator_field_blocks(self) -> None:
        # Ein zusätzliches Locator-/Inhaltsfeld ist ein unbekanntes Feld.
        with self.assertRaises(RegistryDefinitionRejected) as ctx:
            validate_definition(_defn(source_path="/etc/passwd"), POLICY)
        self.assertEqual(
            ctx.exception.reason, ReasonCode.REGISTRY_DEFINITION_UNKNOWN_FIELD
        )


class TestDeterministicIdentity(unittest.TestCase):
    """Fälle 29 bis 31."""

    def test_29_definition_hash_deterministic(self) -> None:
        a = validate_definition(_defn(), POLICY)
        b = validate_definition(_defn(), POLICY)
        self.assertEqual(a.definition_sha256, b.definition_sha256)

    def test_30_source_id_deterministic(self) -> None:
        first = derive_source_id("synthetic-demo", "notes-alpha")
        second = derive_source_id("synthetic-demo", "notes-alpha")
        self.assertEqual(first, second)
        self.assertTrue(first.startswith("src-"))
        self.assertEqual(len(first), 4 + 24)

    def test_31_different_identities_differ(self) -> None:
        a = derive_source_id("synthetic-demo", "notes-alpha")
        b = derive_source_id("synthetic-demo", "notes-beta")
        c = derive_source_id("other-namespace", "notes-alpha")
        self.assertNotEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertNotEqual(b, c)

    def test_source_id_excludes_display_name(self) -> None:
        a = validate_definition(_defn(display_name="First"), POLICY)
        b = validate_definition(_defn(display_name="Second"), POLICY)
        self.assertEqual(
            derive_source_id(a.namespace, a.source_key),
            derive_source_id(b.namespace, b.source_key),
        )
        self.assertNotEqual(a.definition_sha256, b.definition_sha256)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
