"""Tests der lokalen CLI."""

from __future__ import annotations

import io
import json
import socket
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from core.core_brain.cli import VERSION, main
from core.core_brain.errors import EXIT_CODES, ExitCode

REPO_ROOT = Path(__file__).resolve().parent.parent
EXAMPLE_CONFIG = REPO_ROOT / "config" / "runtime.example.toml"
EXAMPLE_POLICY = REPO_ROOT / "config" / "quarantine_policy.example.toml"
REGISTRY_POLICY = REPO_ROOT / "config" / "source_registry_policy.example.toml"
MAPPING_POLICY = REPO_ROOT / "config" / "source_mapping_validation_policy.example.toml"
SYNTHETIC_MARKER = "<!-- synthetic-test-only -->"

# Synthetischer 31-Feld-Mapping-Entwurf, dessen collection/data_class zum
# _REGISTRY_DEF-Record (demo-collection / internal) passen.
_MAPPING_DRAFT = json.dumps(
    {
        "schema_version": "1.0",
        "mapping_id": "MAP-EXAMPLE-0001",
        "slot_id": "PS-02",
        "mapping_name": "Beispiel Markdown Root",
        "source_boundary_type": "markdown-root",
        "deployment_profile": "B",
        "operator_reference": "role-operator-placeholder",
        "location_reference": "synthetic-placeholder-markdown-root",
        "location_reference_type": "local-directory",
        "collection": "demo-collection",
        "project": "example-project-alpha",
        "enabled": False,
        "read_only": True,
        "allowed_subpaths": [],
        "excluded_subpaths": [],
        "follow_symlinks": False,
        "data_class": "internal",
        "ai_transfer_policy": "forbidden",
        "local_search_policy": "forbidden",
        "indexing_policy": "none",
        "mobile_visibility": "forbidden",
        "revision_strategy": "content-hash",
        "deletion_behavior": "tombstone-and-cleanup",
        "verification_status": "unverified",
        "approval_status": "not-approved",
        "approved_by": None,
        "approved_at": None,
        "mapping_revision": 1,
        "previous_revision": None,
        "credential_reference": None,
        "notes": "Synthetisches Beispiel. Nicht aktivieren.",
    }
)

_REGISTRY_DEF = """schema_version = "1.0"
namespace = "synthetic-guard"
source_key = "notes-alpha"
display_name = "Synthetic Guard Notes"
collection_key = "demo-collection"
domain_key = "demo-domain"
source_kind = "markdown"
data_class = "internal"
ai_eligibility = "restricted"
owner_role = "operator"
source_reference = "synthetic:guard"
synthetic_test_only = true
activation_enabled = false
content_access_enabled = false
network_enabled = false
"""


def run_cli(*argv: str) -> tuple[int, str, str]:
    """Führt die CLI in-process aus und gibt Code, stdout und stderr zurück."""
    out, err = io.StringIO(), io.StringIO()
    code = main(list(argv), out=out, err=err)
    return code, out.getvalue(), err.getvalue()


class TestVersion(unittest.TestCase):
    """Test 17 — ``version`` liefert Exitcode 0."""

    def test_version_exit_zero(self) -> None:
        code, out, _ = run_cli("version")
        self.assertEqual(code, EXIT_CODES[ExitCode.OK])
        self.assertEqual(out.strip(), VERSION)

    def test_version_matches_pyproject(self) -> None:
        import tomllib

        data = tomllib.loads(
            (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
        )
        self.assertEqual(data["project"]["version"], VERSION)


class TestValidateConfig(unittest.TestCase):
    """Test 18 — ``validate-config`` validiert die Beispielkonfiguration."""

    def test_valid_example_config(self) -> None:
        code, out, _ = run_cli("validate-config", "--config", str(EXAMPLE_CONFIG))
        self.assertEqual(code, EXIT_CODES[ExitCode.OK])
        self.assertIn("CONFIG_VALID", out)

    def test_invalid_config_returns_config_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.toml"
            bad.write_text(
                EXAMPLE_CONFIG.read_text(encoding="utf-8").replace(
                    'egress_default = "deny"', 'egress_default = "allow"'
                ),
                encoding="utf-8",
            )
            code, _, err = run_cli("validate-config", "--config", str(bad))
        self.assertEqual(code, EXIT_CODES[ExitCode.CONFIG_INVALID])
        self.assertIn("EGRESS_NOT_DENY", err)

    def test_missing_config_returns_config_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "nope.toml"
            code, _, err = run_cli("validate-config", "--config", str(missing))
        self.assertEqual(code, EXIT_CODES[ExitCode.CONFIG_INVALID])
        self.assertIn("CONFIG_FILE_MISSING", err)


class TestDoctor(unittest.TestCase):
    """Tests 19 bis 21 — Doctor ist deterministisch, JSON-fähig, secretfrei."""

    def test_doctor_is_deterministic(self) -> None:
        results = [
            run_cli("doctor", "--config", str(EXAMPLE_CONFIG)) for _ in range(5)
        ]
        first = results[0]
        for other in results[1:]:
            self.assertEqual(other, first)

    def test_doctor_reports_blocked(self) -> None:
        code, out, _ = run_cli("doctor", "--config", str(EXAMPLE_CONFIG))
        self.assertEqual(code, EXIT_CODES[ExitCode.POLICY_BLOCKED])
        self.assertIn("production_ready: false", out)
        self.assertIn("BLOCKED", out)

    def test_doctor_json_is_valid_json(self) -> None:
        code, out, _ = run_cli("doctor", "--config", str(EXAMPLE_CONFIG), "--json")
        self.assertEqual(code, EXIT_CODES[ExitCode.POLICY_BLOCKED])
        payload = json.loads(out)
        self.assertFalse(payload["production_ready"])
        self.assertEqual(payload["runtime_mode"], "skeleton")
        self.assertGreaterEqual(payload["summary"]["blocked"], 1)

    def test_doctor_json_is_deterministic(self) -> None:
        outputs = {
            run_cli("doctor", "--config", str(EXAMPLE_CONFIG), "--json")[1]
            for _ in range(5)
        }
        self.assertEqual(len(outputs), 1)

    def test_doctor_output_contains_no_secret_values(self) -> None:
        _, out, err = run_cli("doctor", "--config", str(EXAMPLE_CONFIG))
        _, jout, _ = run_cli("doctor", "--config", str(EXAMPLE_CONFIG), "--json")
        combined = (out + err + jout).lower()
        for marker in ("password", "token", "api_key", "cbp-secret:", "bearer "):
            with self.subTest(marker=marker):
                self.assertNotIn(marker, combined)

    def test_doctor_on_invalid_config_still_emits_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.toml"
            bad.write_text('schema_version = "9.9"', encoding="utf-8")
            code, out, _ = run_cli("doctor", "--config", str(bad), "--json")
        self.assertEqual(code, EXIT_CODES[ExitCode.CONFIG_INVALID])
        payload = json.loads(out)
        self.assertFalse(payload["production_ready"])


class TestRunFailsClosed(unittest.TestCase):
    """Tests 22 und 23 — ``run`` verweigert und erzeugt keine Dateien."""

    def test_run_refuses_with_documented_exit_code(self) -> None:
        code, out, err = run_cli("run", "--config", str(EXAMPLE_CONFIG))
        self.assertEqual(code, EXIT_CODES[ExitCode.RUNTIME_START_BLOCKED])
        self.assertNotEqual(code, 0)
        self.assertIn("RUNTIME_START_BLOCKED", err)
        self.assertEqual(out, "")

    def test_run_is_deterministic(self) -> None:
        results = [run_cli("run", "--config", str(EXAMPLE_CONFIG)) for _ in range(3)]
        self.assertEqual(len(set(results)), 1)

    def test_run_creates_no_runtime_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workdir = Path(tmp)
            config = workdir / "runtime.toml"
            config.write_text(
                EXAMPLE_CONFIG.read_text(encoding="utf-8"), encoding="utf-8"
            )
            before = {p.name for p in workdir.iterdir()}
            run_cli("run", "--config", str(config))
            after = {p.name for p in workdir.iterdir()}
        self.assertEqual(before, after)

    def test_run_creates_no_files_in_repository(self) -> None:
        before = {p.name for p in REPO_ROOT.iterdir()}
        run_cli("run", "--config", str(EXAMPLE_CONFIG))
        after = {p.name for p in REPO_ROOT.iterdir()}
        self.assertEqual(before, after)


class _NetworkAttempt(AssertionError):
    """Wird ausgelöst, sobald ein lokaler Pfad Netzwerk versucht."""


class TestNetworkGuard(unittest.TestCase):
    """Deterministischer Netzwerk-Guard über die lokalen CLI-Pfade.

    Der Guard ersetzt die zentralen Socket-Einstiegspunkte durch Funktionen,
    die den Test **sofort scheitern lassen**. Verläuft ein CLI-Pfad ohne
    Verbindungs- oder DNS-Versuch, ist der Guard nicht ausgelöst worden.

    **Aussagegrenze:** Der Test beweist ausschließlich, dass *diese lokalen
    CLI-Pfade in-process keinen Socket- oder DNS-Versuch unternehmen*. Er
    beweist **nicht** Deployment-Isolation, Firewallwirkung,
    Container-Netzgrenzen, VM-Egress-Kontrolle oder allgemeine
    Systemnetzwerkfreiheit.
    """

    _CLI_PATHS: tuple[tuple[str, ...], ...] = (
        ("version",),
        ("validate-config", "--config", str(EXAMPLE_CONFIG)),
        ("doctor", "--config", str(EXAMPLE_CONFIG)),
        ("doctor", "--config", str(EXAMPLE_CONFIG), "--json"),
        ("run", "--config", str(EXAMPLE_CONFIG)),
    )

    def _run_under_guard(self, argv: tuple[str, ...]) -> None:
        def _deny(*_args: object, **_kwargs: object) -> object:
            raise _NetworkAttempt(f"network attempt during: {' '.join(argv)}")

        out, err = io.StringIO(), io.StringIO()
        with (
            mock.patch.object(socket, "create_connection", _deny),
            mock.patch.object(socket, "getaddrinfo", _deny),
            mock.patch.object(socket.socket, "connect", _deny),
            mock.patch.object(socket.socket, "connect_ex", _deny),
        ):
            # Kein Netzwerkversuch darf auftreten; ein Aufruf würde
            # _NetworkAttempt auslösen und den Test scheitern lassen.
            main(list(argv), out=out, err=err)

    def test_no_network_attempt_on_any_cli_path(self) -> None:
        for argv in self._CLI_PATHS:
            with self.subTest(path=" ".join(argv)):
                # Wirft der Codepfad _NetworkAttempt, schlägt der Subtest fehl.
                self._run_under_guard(argv)

    def test_guard_itself_triggers_on_a_real_attempt(self) -> None:
        # Gegenprobe: der Guard erkennt einen tatsächlichen Versuch.
        def _deny(*_a: object, **_k: object) -> object:
            raise _NetworkAttempt("blocked")

        with mock.patch.object(socket, "create_connection", _deny):
            with self.assertRaises(_NetworkAttempt):
                socket.create_connection(("192.0.2.1", 9))

    def test_no_network_attempt_on_quarantine_cli_paths(self) -> None:
        # CBP-WP-013: der Guard umfasst scan, stage, inspect und release.
        with tempfile.TemporaryDirectory() as tmp:
            artifact = Path(tmp) / "artifact.md"
            artifact.write_text(
                f"{SYNTHETIC_MARKER}\n# synthetic\ntext\n", encoding="utf-8"
            )
            store = Path(tmp) / "store"
            # Staging außerhalb des Guards, um eine Record-ID zu erhalten.
            out, err = io.StringIO(), io.StringIO()
            main(
                [
                    "quarantine", "stage", "--input", str(artifact),
                    "--policy", str(EXAMPLE_POLICY), "--source-ref", "synthetic:guard",
                    "--store", str(store), "--synthetic-test-only", "--json",
                ],
                out=out,
                err=err,
            )
            record_id = json.loads(out.getvalue())["quarantine_id"]

            quarantine_paths: tuple[tuple[str, ...], ...] = (
                (
                    "quarantine", "scan", "--input", str(artifact),
                    "--policy", str(EXAMPLE_POLICY), "--source-ref", "synthetic:guard",
                    "--synthetic-test-only",
                ),
                (
                    "quarantine", "stage", "--input", str(artifact),
                    "--policy", str(EXAMPLE_POLICY), "--source-ref", "synthetic:guard",
                    "--store", str(store), "--synthetic-test-only",
                ),
                ("quarantine", "inspect", "--store", str(store), "--id", record_id),
                ("quarantine", "release", "--store", str(store), "--id", record_id),
            )
            for argv in quarantine_paths:
                with self.subTest(path=" ".join(argv[:2])):
                    self._run_under_guard(argv)

    def test_no_network_attempt_on_source_registry_cli_paths(self) -> None:
        # CBP-WP-014: der Guard umfasst alle sechs Registry-Pfade.
        with tempfile.TemporaryDirectory() as tmp:
            definition = Path(tmp) / "def.toml"
            definition.write_text(_REGISTRY_DEF, encoding="utf-8")
            registry = Path(tmp) / "registry"
            out, err = io.StringIO(), io.StringIO()
            main(
                [
                    "source-registry", "register", "--definition", str(definition),
                    "--policy", str(REGISTRY_POLICY), "--registry", str(registry),
                    "--synthetic-test-only", "--json",
                ],
                out=out,
                err=err,
            )
            source_id = json.loads(out.getvalue())["source_id"]

            registry_paths: tuple[tuple[str, ...], ...] = (
                ("source-registry", "validate-definition", "--definition",
                 str(definition), "--policy", str(REGISTRY_POLICY)),
                ("source-registry", "register", "--definition", str(definition),
                 "--policy", str(REGISTRY_POLICY), "--registry", str(registry),
                 "--synthetic-test-only"),
                ("source-registry", "list", "--registry", str(registry)),
                ("source-registry", "inspect", "--registry", str(registry),
                 "--id", source_id),
                ("source-registry", "retire", "--registry", str(registry),
                 "--id", source_id, "--synthetic-test-only"),
                ("source-registry", "activate", "--registry", str(registry),
                 "--id", source_id),
            )
            for argv in registry_paths:
                with self.subTest(path=" ".join(argv[:2])):
                    self._run_under_guard(argv)

    def test_no_network_attempt_on_source_mapping_cli_paths(self) -> None:
        # CBP-WP-015: der Guard umfasst validate-draft und activation-check.
        with tempfile.TemporaryDirectory() as tmp:
            definition = Path(tmp) / "def.toml"
            definition.write_text(_REGISTRY_DEF, encoding="utf-8")
            registry = Path(tmp) / "registry"
            out, err = io.StringIO(), io.StringIO()
            main(
                [
                    "source-registry", "register", "--definition", str(definition),
                    "--policy", str(REGISTRY_POLICY), "--registry", str(registry),
                    "--synthetic-test-only", "--json",
                ],
                out=out,
                err=err,
            )
            source_id = json.loads(out.getvalue())["source_id"]

            draft = Path(tmp) / "draft.json"
            draft.write_text(_MAPPING_DRAFT, encoding="utf-8")

            mapping_paths: tuple[tuple[str, ...], ...] = (
                ("source-mapping", "validate-draft", "--draft", str(draft),
                 "--policy", str(MAPPING_POLICY), "--registry", str(registry),
                 "--source-id", source_id, "--synthetic-test-only"),
                ("source-mapping", "validate-draft", "--draft", str(draft),
                 "--policy", str(MAPPING_POLICY), "--registry", str(registry),
                 "--source-id", source_id, "--synthetic-test-only", "--json"),
                ("source-mapping", "activation-check", "--draft", str(draft),
                 "--policy", str(MAPPING_POLICY), "--registry", str(registry),
                 "--source-id", source_id, "--synthetic-test-only"),
            )
            for argv in mapping_paths:
                with self.subTest(path=" ".join(argv[:2])):
                    self._run_under_guard(argv)

    def test_no_network_attempt_on_gate_evaluator_cli_path(self) -> None:
        # CBP-WP-016: der Guard umfasst source-mapping activation-evaluate.
        from tests import gate_fixtures as gfx

        with tempfile.TemporaryDirectory() as tmp:
            case = gfx.build_case(tmp)
            argv = (
                "source-mapping", "activation-evaluate",
                "--draft", str(case["draft_path"]),
                "--policy", str(case["policy_path"]),
                "--registry", str(case["root"]),
                "--source-id", case["source_id"],
                "--evidence", str(case["evidence_path"]),
                "--synthetic-test-only",
            )
            self._run_under_guard(argv)


class TestUsage(unittest.TestCase):
    """Unbekannte Kommandos liefern einen Usage-Fehler."""

    def test_unknown_command_is_usage_error(self) -> None:
        code, _, _ = run_cli("does-not-exist")
        self.assertEqual(code, EXIT_CODES[ExitCode.USAGE_ERROR])

    def test_missing_config_argument_is_usage_error(self) -> None:
        code, _, _ = run_cli("doctor")
        self.assertEqual(code, EXIT_CODES[ExitCode.USAGE_ERROR])


class TestNoImportSideEffects(unittest.TestCase):
    """Test 24 — der Modulimport erzeugt keine Nebenwirkungen."""

    def test_importing_package_produces_no_output_and_no_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            probe = (
                "import sys, pathlib;"
                "sys.path.insert(0, r'" + str(REPO_ROOT) + "');"
                "before = set(pathlib.Path(r'" + tmp + "').iterdir());"
                "import core.core_brain, core.core_brain.cli,"
                " core.core_brain.config, core.core_brain.policies,"
                " core.core_brain.ports, core.core_brain.models,"
                " core.core_brain.errors, core.core_brain.quarantine,"
                " core.core_brain.quarantine.models,"
                " core.core_brain.quarantine.policy,"
                " core.core_brain.quarantine.scanner,"
                " core.core_brain.quarantine.store,"
                " core.core_brain.quarantine.pipeline,"
                " core.core_brain.registry,"
                " core.core_brain.registry.models,"
                " core.core_brain.registry.policy,"
                " core.core_brain.registry.storage,"
                " core.core_brain.registry.catalog,"
                " core.core_brain.registry.service,"
                " core.core_brain.mapping,"
                " core.core_brain.mapping.models,"
                " core.core_brain.mapping.policy,"
                " core.core_brain.mapping.parser,"
                " core.core_brain.mapping.validator,"
                " core.core_brain.mapping.service,"
                " core.core_brain.gate,"
                " core.core_brain.gate.models,"
                " core.core_brain.gate.evidence,"
                " core.core_brain.gate.evaluator,"
                " core.core_brain.gate.service;"
                "after = set(pathlib.Path(r'" + tmp + "').iterdir());"
                "assert before == after;"
                "print('IMPORT_CLEAN')"
            )
            result = subprocess.run(
                [sys.executable, "-c", probe],
                capture_output=True,
                text=True,
                timeout=60,
            )
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertEqual(result.stdout.strip(), "IMPORT_CLEAN")
        self.assertEqual(result.stderr.strip(), "")

    def test_no_module_uses_dynamic_execution_or_shell(self) -> None:
        package = REPO_ROOT / "core" / "core_brain"
        for module in sorted(package.rglob("*.py")):
            source = module.read_text(encoding="utf-8")
            with self.subTest(module=module.name):
                self.assertNotIn("eval(", source)
                self.assertNotIn("exec(", source)
                self.assertNotIn("shell=True", source)
                self.assertNotIn("__import__(", source)


class TestQuarantineLeavesRepositoryUnchanged(unittest.TestCase):
    """Test 55 — Quarantäneoperationen schreiben nur in temporäre Verzeichnisse."""

    def test_quarantine_scan_and_stage_create_no_files_in_repository(self) -> None:
        def _snapshot() -> set[Path]:
            return set((REPO_ROOT / "core").rglob("*")) | set(
                (REPO_ROOT / "config").rglob("*")
            )

        before = _snapshot()
        with tempfile.TemporaryDirectory() as tmp:
            artifact = Path(tmp) / "artifact.md"
            artifact.write_text(
                f"{SYNTHETIC_MARKER}\n# synthetic\ntext\n", encoding="utf-8"
            )
            store = Path(tmp) / "store"
            run_cli(
                "quarantine", "scan", "--input", str(artifact),
                "--policy", str(EXAMPLE_POLICY), "--source-ref", "synthetic:repo",
                "--synthetic-test-only",
            )
            run_cli(
                "quarantine", "stage", "--input", str(artifact),
                "--policy", str(EXAMPLE_POLICY), "--source-ref", "synthetic:repo",
                "--store", str(store), "--synthetic-test-only",
            )
        after = _snapshot()
        self.assertEqual(before, after)


class TestRegistryLeavesRepositoryUnchanged(unittest.TestCase):
    """Test 81 — Registry-Operationen schreiben nur in temporäre Verzeichnisse."""

    def test_registry_register_and_retire_create_no_files_in_repository(self) -> None:
        def _snapshot() -> set[Path]:
            return set((REPO_ROOT / "core").rglob("*")) | set(
                (REPO_ROOT / "config").rglob("*")
            )

        before = _snapshot()
        with tempfile.TemporaryDirectory() as tmp:
            definition = Path(tmp) / "def.toml"
            definition.write_text(_REGISTRY_DEF, encoding="utf-8")
            registry = Path(tmp) / "registry"
            _, out, _ = run_cli(
                "source-registry", "register", "--definition", str(definition),
                "--policy", str(REGISTRY_POLICY), "--registry", str(registry),
                "--synthetic-test-only", "--json",
            )
            source_id = json.loads(out)["source_id"]
            run_cli("source-registry", "list", "--registry", str(registry))
            run_cli(
                "source-registry", "retire", "--registry", str(registry),
                "--id", source_id, "--synthetic-test-only",
            )
        after = _snapshot()
        self.assertEqual(before, after)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
