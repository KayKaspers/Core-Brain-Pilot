"""Tests der Quarantäne-Policy (CBP-WP-013).

Deckt die fail-closed Validierung ab: gültige Beispielpolicy, unbekanntes Feld,
unbekannte Version, unzulässiges ``max_bytes``, leere Suffixliste,
``release_enabled``/``network_enabled`` sowie die Nicht-Überschreibbarkeit
durch Environment und CLI. Ausschließlich Standardbibliothek, keine realen
Secrets, keine realen Pfade.
"""

from __future__ import annotations

import copy
import os
import unittest
from pathlib import Path
from unittest import mock

from core.core_brain.errors import QuarantinePolicyError, ReasonCode
from core.core_brain.quarantine.policy import load_policy, parse_policy_mapping

REPO_ROOT = Path(__file__).resolve().parent.parent
EXAMPLE_POLICY = REPO_ROOT / "config" / "quarantine_policy.example.toml"

_BASE: dict[str, object] = {
    "schema_version": "1.0",
    "max_bytes": 1048576,
    "allowed_suffixes": [".md"],
    "reject_symlinks": True,
    "require_regular_file": True,
    "require_utf8": True,
    "reject_nul": True,
    "block_private_key_markers": True,
    "block_credential_assignments": True,
    "review_email_indicators": True,
    "review_phone_indicators": True,
    "release_enabled": False,
    "network_enabled": False,
}


def _mapping(**overrides: object) -> dict[str, object]:
    data = copy.deepcopy(_BASE)
    data.update(overrides)
    return data


class TestPolicyValidation(unittest.TestCase):
    """Tests 1 bis 7 — strikte Policy-Validierung."""

    def test_1_example_policy_is_valid(self) -> None:
        policy = load_policy(EXAMPLE_POLICY)
        self.assertEqual(policy.schema_version, "1.0")
        self.assertEqual(policy.allowed_suffixes, (".md",))
        self.assertFalse(policy.release_enabled)
        self.assertFalse(policy.network_enabled)
        self.assertEqual(len(policy.policy_sha256), 64)

    def test_2_unknown_field_blocks(self) -> None:
        with self.assertRaises(QuarantinePolicyError) as ctx:
            parse_policy_mapping(_mapping(surprise=1), "0" * 64)
        self.assertEqual(
            ctx.exception.reason, ReasonCode.QUARANTINE_POLICY_UNKNOWN_FIELD
        )

    def test_3_unknown_version_blocks(self) -> None:
        with self.assertRaises(QuarantinePolicyError) as ctx:
            parse_policy_mapping(_mapping(schema_version="9.9"), "0" * 64)
        self.assertEqual(
            ctx.exception.reason, ReasonCode.QUARANTINE_POLICY_SCHEMA_UNSUPPORTED
        )

    def test_4_max_bytes_zero_or_negative_blocks(self) -> None:
        for value in (0, -1):
            with self.subTest(value=value):
                with self.assertRaises(QuarantinePolicyError) as ctx:
                    parse_policy_mapping(_mapping(max_bytes=value), "0" * 64)
                self.assertEqual(
                    ctx.exception.reason, ReasonCode.QUARANTINE_POLICY_INVALID_VALUE
                )

    def test_4b_max_bytes_above_ceiling_blocks(self) -> None:
        with self.assertRaises(QuarantinePolicyError) as ctx:
            parse_policy_mapping(_mapping(max_bytes=10 * 1024 * 1024), "0" * 64)
        self.assertEqual(
            ctx.exception.reason, ReasonCode.QUARANTINE_POLICY_INVALID_VALUE
        )

    def test_5_empty_suffix_list_blocks(self) -> None:
        with self.assertRaises(QuarantinePolicyError) as ctx:
            parse_policy_mapping(_mapping(allowed_suffixes=[]), "0" * 64)
        self.assertEqual(
            ctx.exception.reason, ReasonCode.QUARANTINE_POLICY_INVALID_VALUE
        )

    def test_6_release_enabled_blocks(self) -> None:
        with self.assertRaises(QuarantinePolicyError) as ctx:
            parse_policy_mapping(_mapping(release_enabled=True), "0" * 64)
        self.assertEqual(
            ctx.exception.reason, ReasonCode.QUARANTINE_POLICY_RELEASE_ENABLED
        )

    def test_7_network_enabled_blocks(self) -> None:
        with self.assertRaises(QuarantinePolicyError) as ctx:
            parse_policy_mapping(_mapping(network_enabled=True), "0" * 64)
        self.assertEqual(
            ctx.exception.reason, ReasonCode.QUARANTINE_POLICY_NETWORK_ENABLED
        )

    def test_missing_field_blocks(self) -> None:
        data = _mapping()
        del data["reject_nul"]
        with self.assertRaises(QuarantinePolicyError) as ctx:
            parse_policy_mapping(data, "0" * 64)
        self.assertEqual(
            ctx.exception.reason, ReasonCode.QUARANTINE_POLICY_MISSING_FIELD
        )


class TestPolicyNotOverridable(unittest.TestCase):
    """Tests 8 und 9 — weder Environment noch CLI überschreiben die Policy."""

    def test_8_environment_does_not_override_policy(self) -> None:
        # Ein gesetzter Umgebungswert bleibt wirkungslos: die geladene Policy
        # trägt ausschließlich die Dateiwerte.
        with mock.patch.dict(
            os.environ,
            {
                "QUARANTINE_MAX_BYTES": "1",
                "QUARANTINE_RELEASE_ENABLED": "true",
                "QUARANTINE_NETWORK_ENABLED": "true",
            },
        ):
            policy = load_policy(EXAMPLE_POLICY)
        self.assertEqual(policy.max_bytes, 1048576)
        self.assertFalse(policy.release_enabled)
        self.assertFalse(policy.network_enabled)

    def test_9_policy_module_reads_neither_environ_nor_argv(self) -> None:
        # Strukturprüfung: das Modul importiert weder os noch sys und kann
        # deshalb keine Umgebungs- oder CLI-Werte lesen. Die Wörter
        # "environ"/"argv" stehen nur in der erläuternden Docstring-Prosa,
        # daher wird ausschließlich auf die Importzeilen geprüft.
        source = (
            REPO_ROOT / "core" / "core_brain" / "quarantine" / "policy.py"
        ).read_text(encoding="utf-8")
        self.assertNotIn("import os", source)
        self.assertNotIn("import sys", source)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
