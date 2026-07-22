"""Tests der Source-Registry-CLI (CBP-WP-014).

Deckt die Fälle 65–78 ab: Exitcodes, minimierte Ausgaben, immer verweigernde
Aktivierung, unveränderte Grundkommandos und die Zusage, dass kein CLI-Pfad
einen Eingabepfad oder Definitioninhalt ausgibt.
"""

from __future__ import annotations

import io
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from core.core_brain.cli import main
from core.core_brain.errors import EXIT_CODES, ExitCode

REPO_ROOT = Path(__file__).resolve().parent.parent
POLICY = REPO_ROOT / "config" / "source_registry_policy.example.toml"

_DEF = """schema_version = "1.0"
namespace = "synthetic-demo"
source_key = "{key}"
display_name = "{dn}"
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


def run_cli(*argv: str) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    code = main(list(argv), out=out, err=err)
    return code, out.getvalue(), err.getvalue()


def _def_file(tmp: str, name: str, *, key="notes-alpha", dn="Name") -> Path:
    path = Path(tmp) / name
    path.write_text(_DEF.format(key=key, dn=dn), encoding="utf-8")
    return path


class TestValidateAndRegister(unittest.TestCase):
    """Fälle 65 bis 68."""

    def test_65_validate_definition_success(self) -> None:
        with TemporaryDirectory() as tmp:
            d = _def_file(tmp, "d.toml")
            code, out, _ = run_cli(
                "source-registry", "validate-definition",
                "--definition", str(d), "--policy", str(POLICY),
            )
        self.assertEqual(code, EXIT_CODES[ExitCode.OK])
        self.assertIn("DEFINITION_VALID", out)

    def test_66_validate_definition_blocks_invalid(self) -> None:
        with TemporaryDirectory() as tmp:
            d = Path(tmp) / "bad.toml"
            d.write_text(_DEF.format(key="k", dn="N").replace(
                "synthetic_test_only = true", "synthetic_test_only = false"
            ), encoding="utf-8")
            code, _, err = run_cli(
                "source-registry", "validate-definition",
                "--definition", str(d), "--policy", str(POLICY),
            )
        self.assertEqual(code, EXIT_CODES[ExitCode.SOURCE_REGISTRY_BLOCKED])
        self.assertIn("REGISTRY_DEFINITION_NOT_SYNTHETIC", err)

    def test_67_register_success_and_disabled(self) -> None:
        with TemporaryDirectory() as tmp:
            d = _def_file(tmp, "d.toml")
            reg = str(Path(tmp) / "reg")
            code, out, _ = run_cli(
                "source-registry", "register", "--definition", str(d),
                "--policy", str(POLICY), "--registry", reg,
                "--synthetic-test-only", "--json",
            )
            record = json.loads(out)
        self.assertEqual(code, EXIT_CODES[ExitCode.OK])
        self.assertEqual(record["lifecycle_state"], "REGISTERED_DISABLED")

    def test_68_register_without_synthetic_flag_blocks(self) -> None:
        with TemporaryDirectory() as tmp:
            d = _def_file(tmp, "d.toml")
            reg = str(Path(tmp) / "reg")
            code, _, err = run_cli(
                "source-registry", "register", "--definition", str(d),
                "--policy", str(POLICY), "--registry", reg,
            )
        self.assertEqual(code, EXIT_CODES[ExitCode.SOURCE_REGISTRY_BLOCKED])
        self.assertIn("REGISTRY_SYNTHETIC_CONFIRMATION_MISSING", err)


class TestListInspectRetireActivate(unittest.TestCase):
    """Fälle 69 bis 74."""

    def _register(self, tmp: str) -> tuple[str, str]:
        d = _def_file(tmp, "d.toml")
        reg = str(Path(tmp) / "reg")
        _, out, _ = run_cli(
            "source-registry", "register", "--definition", str(d),
            "--policy", str(POLICY), "--registry", reg,
            "--synthetic-test-only", "--json",
        )
        return reg, json.loads(out)["source_id"]

    def test_69_list_minimized(self) -> None:
        with TemporaryDirectory() as tmp:
            reg, _ = self._register(tmp)
            code, out, _ = run_cli(
                "source-registry", "list", "--registry", reg, "--json"
            )
            catalog = json.loads(out)
        self.assertEqual(code, EXIT_CODES[ExitCode.OK])
        self.assertEqual(catalog["record_count"], 1)
        self.assertNotIn("source_reference", out)

    def test_70_inspect_minimized(self) -> None:
        with TemporaryDirectory() as tmp:
            reg, sid = self._register(tmp)
            code, out, _ = run_cli(
                "source-registry", "inspect", "--registry", reg, "--id", sid, "--json"
            )
            data = json.loads(out)
        self.assertEqual(code, EXIT_CODES[ExitCode.OK])
        self.assertEqual(data["source_id"], sid)
        self.assertNotIn(str(reg), out)

    def test_71_retire_success(self) -> None:
        with TemporaryDirectory() as tmp:
            reg, sid = self._register(tmp)
            code, out, _ = run_cli(
                "source-registry", "retire", "--registry", reg, "--id", sid,
                "--synthetic-test-only", "--json",
            )
            data = json.loads(out)
        self.assertEqual(code, EXIT_CODES[ExitCode.OK])
        self.assertEqual(data["lifecycle_state"], "RETIRED")

    def test_72_activate_always_refuses(self) -> None:
        with TemporaryDirectory() as tmp:
            reg, sid = self._register(tmp)
            before = {p.name for p in (Path(reg) / "records").iterdir()}
            code, out, err = run_cli(
                "source-registry", "activate", "--registry", reg, "--id", sid
            )
            after = {p.name for p in (Path(reg) / "records").iterdir()}
        self.assertEqual(code, EXIT_CODES[ExitCode.SOURCE_REGISTRY_ACTIVATION_BLOCKED])
        self.assertIn("SOURCE_REGISTRY_ACTIVATION_BLOCKED", err)
        self.assertEqual(out, "")
        self.assertEqual(before, after)

    def test_73_unknown_id_stable_exit(self) -> None:
        with TemporaryDirectory() as tmp:
            reg, _ = self._register(tmp)
            code, _, err = run_cli(
                "source-registry", "inspect", "--registry", reg, "--id", "src-" + "0" * 24
            )
        self.assertEqual(code, EXIT_CODES[ExitCode.SOURCE_REGISTRY_NOT_FOUND])
        self.assertIn("SOURCE_REGISTRY_NOT_FOUND", err)

    def test_74_conflict_stable_exit(self) -> None:
        with TemporaryDirectory() as tmp:
            reg = str(Path(tmp) / "reg")
            d1 = _def_file(tmp, "d1.toml", dn="First")
            d2 = _def_file(tmp, "d2.toml", dn="Second")  # same identity, diff def
            run_cli(
                "source-registry", "register", "--definition", str(d1),
                "--policy", str(POLICY), "--registry", reg, "--synthetic-test-only",
            )
            code, _, err = run_cli(
                "source-registry", "register", "--definition", str(d2),
                "--policy", str(POLICY), "--registry", reg, "--synthetic-test-only",
            )
        self.assertEqual(code, EXIT_CODES[ExitCode.SOURCE_REGISTRY_CONFLICT])
        self.assertIn("SOURCE_REGISTRY_CONFLICT", err)


class TestNoLeakAndUnchanged(unittest.TestCase):
    """Fälle 75 bis 78."""

    def test_75_76_no_path_or_definition_content_leak(self) -> None:
        raw_marker = "activation_enabled = false"
        filename = "leak-probe-def-75.toml"
        with TemporaryDirectory() as tmp:
            d = _def_file(tmp, filename)
            reg = str(Path(tmp) / "reg")
            combined = ""
            for argv in (
                ("source-registry", "validate-definition", "--definition", str(d),
                 "--policy", str(POLICY), "--json"),
                ("source-registry", "register", "--definition", str(d), "--policy",
                 str(POLICY), "--registry", reg, "--synthetic-test-only", "--json"),
            ):
                _, out, err = run_cli(*argv)
                combined += out + err
        self.assertNotIn(filename, combined)  # kein Eingabepfad
        self.assertNotIn(raw_marker, combined)  # kein roher Definitioninhalt

    def test_77_run_stays_fail_closed(self) -> None:
        config = REPO_ROOT / "config" / "runtime.example.toml"
        code, _, err = run_cli("run", "--config", str(config))
        self.assertEqual(code, EXIT_CODES[ExitCode.RUNTIME_START_BLOCKED])
        self.assertIn("RUNTIME_START_BLOCKED", err)

    def test_78_quarantine_cli_unchanged(self) -> None:
        with TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            store.mkdir()
            code, _, err = run_cli(
                "quarantine", "release", "--store", str(store), "--id", "a" * 64
            )
        self.assertEqual(code, EXIT_CODES[ExitCode.QUARANTINE_RELEASE_BLOCKED])
        self.assertIn("QUARANTINE_RELEASE_BLOCKED", err)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
