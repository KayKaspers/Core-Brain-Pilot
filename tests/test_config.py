"""Tests der strikten Konfigurationsvalidierung."""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from core.core_brain.config import (
    REQUIRED_FIELDS,
    SECURITY_FIELDS,
    load_config,
    parse_config_mapping,
)
from core.core_brain.errors import ConfigError, ReasonCode
from core.core_brain.models import ComponentStatus, GateStatus, RuntimeMode

REPO_ROOT = Path(__file__).resolve().parent.parent
EXAMPLE_CONFIG = REPO_ROOT / "config" / "runtime.example.toml"


def valid_mapping() -> dict[str, object]:
    """Gibt ein gültiges Rohmapping zurück."""
    return {
        "schema_version": "1.0",
        "runtime_mode": "skeleton",
        "control_plane_identity": "control-plane",
        "data_worker_identity": "data-worker",
        "egress_default": "deny",
        "canonical_write_allowed": False,
        "source_activation_enabled": False,
        "mapping_gate_status": "NOT EVALUATED",
        "security_gate_status": "NOT EVALUATED",
        "secret_provider_status": "unconfigured",
        "evidence_writer_status": "unconfigured",
    }


class TestExampleConfig(unittest.TestCase):
    """Test 1 — die Beispielkonfiguration ist strukturell gültig."""

    def test_example_config_is_valid(self) -> None:
        config = load_config(EXAMPLE_CONFIG)
        self.assertEqual(config.schema_version, "1.0")
        self.assertIs(config.runtime_mode, RuntimeMode.SKELETON)
        self.assertFalse(config.canonical_write_allowed)
        self.assertFalse(config.source_activation_enabled)
        self.assertIs(config.mapping_gate_status, GateStatus.NOT_EVALUATED)
        self.assertIs(config.security_gate_status, GateStatus.NOT_EVALUATED)
        self.assertIs(config.secret_provider_status, ComponentStatus.UNCONFIGURED)
        self.assertIs(config.evidence_writer_status, ComponentStatus.UNCONFIGURED)

    def test_example_config_contains_no_secret_markers(self) -> None:
        text = EXAMPLE_CONFIG.read_text(encoding="utf-8").lower()
        for marker in ("password", "token", "api_key", "cbp-secret:", "secret ="):
            self.assertNotIn(marker, text)


class TestUnknownAndMissingFields(unittest.TestCase):
    """Tests 2, 3 und 9 — unbekannte Felder, Version, Pflichtfelder."""

    def test_unknown_field_blocks(self) -> None:
        data = valid_mapping()
        data["unexpected_field"] = "x"
        with self.assertRaises(ConfigError) as ctx:
            parse_config_mapping(data)
        self.assertIs(ctx.exception.reason, ReasonCode.CONFIG_UNKNOWN_FIELD)

    def test_unknown_schema_version_blocks(self) -> None:
        data = valid_mapping()
        data["schema_version"] = "2.0"
        with self.assertRaises(ConfigError) as ctx:
            parse_config_mapping(data)
        self.assertIs(
            ctx.exception.reason, ReasonCode.CONFIG_SCHEMA_VERSION_UNSUPPORTED
        )

    def test_every_missing_required_field_blocks(self) -> None:
        for field_name in sorted(REQUIRED_FIELDS):
            with self.subTest(field=field_name):
                data = valid_mapping()
                del data[field_name]
                with self.assertRaises(ConfigError):
                    parse_config_mapping(data)


class TestSecurityValues(unittest.TestCase):
    """Tests 4 bis 8 — Sicherheitswerte blockieren fail-closed."""

    def test_identical_identities_block(self) -> None:
        data = valid_mapping()
        data["data_worker_identity"] = "control-plane"
        with self.assertRaises(ConfigError) as ctx:
            parse_config_mapping(data)
        self.assertIs(ctx.exception.reason, ReasonCode.IDENTITIES_NOT_SEPARATED)

    def test_identical_identities_block_case_insensitively(self) -> None:
        data = valid_mapping()
        data["data_worker_identity"] = "Control-Plane"
        with self.assertRaises(ConfigError) as ctx:
            parse_config_mapping(data)
        self.assertIs(ctx.exception.reason, ReasonCode.IDENTITIES_NOT_SEPARATED)

    def test_root_identity_blocks(self) -> None:
        for field_name in ("control_plane_identity", "data_worker_identity"):
            with self.subTest(field=field_name):
                data = valid_mapping()
                data[field_name] = "root"
                with self.assertRaises(ConfigError) as ctx:
                    parse_config_mapping(data)
                self.assertIs(ctx.exception.reason, ReasonCode.IDENTITY_IS_ROOT)

    def test_egress_not_deny_blocks(self) -> None:
        data = valid_mapping()
        data["egress_default"] = "allow"
        with self.assertRaises(ConfigError) as ctx:
            parse_config_mapping(data)
        self.assertIs(ctx.exception.reason, ReasonCode.EGRESS_NOT_DENY)

    def test_canonical_write_true_blocks(self) -> None:
        data = valid_mapping()
        data["canonical_write_allowed"] = True
        with self.assertRaises(ConfigError) as ctx:
            parse_config_mapping(data)
        self.assertIs(ctx.exception.reason, ReasonCode.CANONICAL_WRITE_REQUESTED)

    def test_source_activation_true_blocks(self) -> None:
        data = valid_mapping()
        data["source_activation_enabled"] = True
        with self.assertRaises(ConfigError) as ctx:
            parse_config_mapping(data)
        self.assertIs(ctx.exception.reason, ReasonCode.SOURCE_ACTIVATION_REQUESTED)

    def test_wrong_type_blocks(self) -> None:
        data = valid_mapping()
        data["canonical_write_allowed"] = "false"
        with self.assertRaises(ConfigError) as ctx:
            parse_config_mapping(data)
        self.assertIs(ctx.exception.reason, ReasonCode.CONFIG_TYPE_MISMATCH)


class TestNoOverrides(unittest.TestCase):
    """Tests 10 und 11 — Environment und CLI überschreiben nichts."""

    def test_environment_does_not_override_security_values(self) -> None:
        overrides = {
            "CORE_BRAIN_EGRESS_DEFAULT": "allow",
            "CORE_BRAIN_CANONICAL_WRITE_ALLOWED": "true",
            "CORE_BRAIN_SOURCE_ACTIVATION_ENABLED": "true",
            "CORE_BRAIN_SECURITY_GATE_STATUS": "ACCEPTED",
            "EGRESS_DEFAULT": "allow",
        }
        saved = {k: os.environ.get(k) for k in overrides}
        try:
            os.environ.update(overrides)
            config = load_config(EXAMPLE_CONFIG)
            self.assertEqual(config.egress_default.value, "deny")
            self.assertFalse(config.canonical_write_allowed)
            self.assertFalse(config.source_activation_enabled)
            self.assertIs(config.security_gate_status, GateStatus.NOT_EVALUATED)
        finally:
            for key, old in saved.items():
                if old is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = old

    def test_config_module_reads_neither_environ_nor_argv(self) -> None:
        # Robuste Prüfung auf tatsächliche Nutzung statt auf Prosa im
        # Docstring: config.py importiert weder os noch sys und kann sie
        # daher nicht lesen.
        source = (
            REPO_ROOT / "core" / "core_brain" / "config.py"
        ).read_text(encoding="utf-8")
        self.assertNotIn("import os", source)
        self.assertNotIn("import sys", source)
        self.assertNotIn("getenv", source)

    def test_security_fields_are_declared(self) -> None:
        self.assertTrue(SECURITY_FIELDS.issubset(REQUIRED_FIELDS))
        self.assertIn("egress_default", SECURITY_FIELDS)
        self.assertIn("canonical_write_allowed", SECURITY_FIELDS)


class TestFileHandling(unittest.TestCase):
    """Fehlende, unlesbare und fehlerhafte Dateien blockieren."""

    def test_missing_file_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "does-not-exist.toml"
            with self.assertRaises(ConfigError) as ctx:
                load_config(missing)
            self.assertIs(ctx.exception.reason, ReasonCode.CONFIG_FILE_MISSING)

    def test_broken_toml_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            broken = Path(tmp) / "broken.toml"
            broken.write_text("this is = = not toml", encoding="utf-8")
            with self.assertRaises(ConfigError) as ctx:
                load_config(broken)
            self.assertIs(ctx.exception.reason, ReasonCode.CONFIG_PARSE_ERROR)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
