"""Profile-A Bundle Validation Tests (CBP-WP-020, Phase B2).

These tests validate the **repository deployment bundle** only. They are
explicitly **not** Security Foundation NT-01 to NT-31, not real container
checks, not infrastructure or deployment tests, not enforcement evidence and
not operational evidence. The canonical figure stays: security negative tests
executed 0/31.

Standard library only. No Docker, no network, no host inspection.
Forbidden test values are assembled at runtime from fragments so that no
complete forbidden literal ever appears in the repository.
"""

from __future__ import annotations

import ast
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parent.parent
BUNDLE = REPO_ROOT / "deployments" / "profile-a"
VALIDATOR = BUNDLE / "validate.py"

EXPECTED_FILES = (
    "README.md",
    "bundle.json",
    "compose.yaml",
    "config/control-plane.example.toml",
    "config/data-worker.example.toml",
    "operator.env.example",
    "validate.py",
)


def _load_validator():
    name = "cbp_profile_a_validate"
    spec = importlib.util.spec_from_file_location(name, VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    # dataclasses resolves annotations via sys.modules during class creation.
    sys.modules[name] = module
    # A __pycache__ directory inside the bundle would violate its own file set.
    previous = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = previous
    return module


V = _load_validator()


# --- runtime-assembled forbidden values ------------------------------------


def forbidden_ipv4() -> str:
    return ".".join([str(10), str(1), str(2), str(3)])


def forbidden_url() -> str:
    return "htt" + "ps" + ":" + "//" + "reg" + "istry" + "." + "exa" + "mple" + ".com/x"


def forbidden_domain() -> str:
    return "no" + "de01" + "." + "inter" + "nal"


def forbidden_token_line() -> str:
    return "api" + "_key" + "=" + "AAAA" + "BBBB" + "CCCC"


def forbidden_unc() -> str:
    return "\\" + "\\" + "nas" + "\\" + "share"


def forbidden_win_path() -> str:
    return "C" + ":" + "\\" + "Users" + "\\" + "x"


def forbidden_mac() -> str:
    return ":".join(["de", "ad", "be", "ef", "00", "11"])


def forbidden_uuid() -> str:
    return "-".join(["a" * 8, "b" * 4, "c" * 4, "d" * 4, "e" * 12])


class _BundleFixture(unittest.TestCase):
    """Provides a writable copy of the canonical bundle."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name) / "profile-a"
        shutil.copytree(BUNDLE, self.root)
        self.addCleanup(self._tmp.cleanup)

    # helpers -------------------------------------------------------------
    def compose(self) -> dict:
        return json.loads((self.root / "compose.yaml").read_text(encoding="utf-8"))

    def write_compose(self, doc: dict) -> None:
        (self.root / "compose.yaml").write_text(
            json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8", newline=""
        )

    def contract(self) -> dict:
        return json.loads((self.root / "bundle.json").read_text(encoding="utf-8"))

    def write_contract(self, doc: dict) -> None:
        text = json.dumps(doc, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        (self.root / "bundle.json").write_text(text, encoding="utf-8", newline="")

    def validate(self):
        return V.validate_bundle(self.root)

    def codes(self) -> set[str]:
        return {i.code for i in self.validate().issues}

    def assert_invalid(self, prefix: str | None = None) -> None:
        report = self.validate()
        self.assertFalse(report.valid)
        self.assertTrue(report.issues)
        if prefix:
            self.assertTrue(
                any(i.code.startswith(prefix) for i in report.issues),
                msg=f"expected an issue with prefix {prefix}, got {sorted(self.codes())}",
            )


# ===========================================================================
# Positive tests
# ===========================================================================


class TestBundleValid(_BundleFixture):
    def test_canonical_bundle_is_valid(self) -> None:
        report = self.validate()
        self.assertTrue(report.valid, msg=str(sorted(self.codes())))
        self.assertEqual(report.issues, ())

    def test_public_api_returns_validation_report(self) -> None:
        report = V.validate_bundle(BUNDLE)
        self.assertIsInstance(report, V.ValidationReport)
        self.assertTrue(report.valid)
        self.assertIsInstance(report.issues, tuple)

    def test_repeated_api_runs_are_identical(self) -> None:
        a = V.validate_bundle(BUNDLE)
        b = V.validate_bundle(BUNDLE)
        self.assertEqual(a.issues, b.issues)
        self.assertEqual(a.valid, b.valid)

    def test_file_set_has_exactly_seven_files(self) -> None:
        files = {p.relative_to(BUNDLE).as_posix() for p in BUNDLE.rglob("*") if p.is_file()}
        self.assertEqual(files, set(EXPECTED_FILES))
        self.assertEqual(len(files), 7)

    def test_bundle_contains_no_symlink(self) -> None:
        self.assertFalse(any(p.is_symlink() for p in BUNDLE.rglob("*")))

    def test_bundle_json_is_canonically_formatted(self) -> None:
        text = (BUNDLE / "bundle.json").read_text(encoding="utf-8")
        doc = json.loads(text)
        canonical = json.dumps(doc, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        self.assertEqual(text, canonical)

    def test_bundle_json_parses(self) -> None:
        self.assertIsInstance(self.contract(), dict)

    def test_both_toml_templates_parse(self) -> None:
        for name in ("control-plane", "data-worker"):
            with self.subTest(name=name):
                raw = (BUNDLE / "config" / f"{name}.example.toml").read_bytes()
                self.assertIsInstance(tomllib.loads(raw.decode("utf-8")), dict)

    def test_compose_parses_as_json(self) -> None:
        self.assertIsInstance(self.compose(), dict)

    def test_compose_has_exactly_two_services(self) -> None:
        self.assertEqual(set(self.compose()["services"]), {"control-plane", "data-worker"})

    def test_service_identities_are_separate(self) -> None:
        services = self.contract()["services"]
        self.assertEqual(services["control-plane"]["service_identity"], "svc-control-plane")
        self.assertEqual(services["data-worker"]["service_identity"], "svc-data-worker")
        self.assertNotEqual(
            services["control-plane"]["service_identity"],
            services["data-worker"]["service_identity"],
        )

    def test_mount_matrix_matches_contract(self) -> None:
        doc = self.compose()
        cp = {v["source"]: bool(v.get("read_only"))
              for v in doc["services"]["control-plane"]["volumes"]}
        dw = {v["source"]: bool(v.get("read_only"))
              for v in doc["services"]["data-worker"]["volumes"]}
        self.assertTrue(cp["canonical-data"])
        self.assertFalse(cp["source-registry"])
        self.assertNotIn("quarantine", cp)
        self.assertTrue(dw["canonical-data"])
        self.assertTrue(dw["source-registry"])
        self.assertFalse(dw["quarantine"])
        self.assertNotIn("released-artifacts", dw)

    def test_exactly_one_internal_network(self) -> None:
        nets = self.compose()["networks"]
        self.assertEqual(len(nets), 1)
        self.assertTrue(next(iter(nets.values()))["internal"])

    def test_both_configs_are_mounted_read_only(self) -> None:
        for name in ("control-plane", "data-worker"):
            with self.subTest(name=name):
                cfg = self.compose()["services"][name]["configs"][0]
                self.assertEqual(cfg["source"], f"{name}-config")
                self.assertEqual(cfg["target"], f"/etc/cbp/{name}.toml")
                self.assertEqual(cfg["mode"] & 0o222, 0)

    def test_operator_env_is_complete_and_fail_closed(self) -> None:
        text = (BUNDLE / "operator.env.example").read_text(encoding="utf-8")
        pairs = [ln.split("=", 1) for ln in text.splitlines()
                 if ln.strip() and not ln.startswith("#")]
        keys = [k for k, _ in pairs]
        self.assertEqual(len(keys), 7)
        for key, value in pairs:
            if key != "CBP_DEPLOYMENT_PROFILE":
                self.assertEqual(value, "", msg=key)
        self.assertEqual(dict(pairs)["CBP_DEPLOYMENT_PROFILE"], "A")

    def test_leakage_scan_is_clean(self) -> None:
        self.assertFalse({c for c in self.codes() if c.startswith("BND-LEAK-")})

    def test_all_twelve_controls_are_documented_only(self) -> None:
        controls = self.contract()["security_controls"]
        self.assertEqual(len(controls), 12)
        for cid, spec in controls.items():
            with self.subTest(cid=cid):
                self.assertEqual(spec["status"], "DOCUMENTED ONLY")

    def test_capabilities_are_zero_of_29(self) -> None:
        caps = self.contract()["capabilities"]
        self.assertEqual((caps["implemented"], caps["total"]), (0, 29))

    def test_both_gates_are_not_evaluated(self) -> None:
        gates = self.contract()["gates"]
        self.assertEqual(gates["mapping_activation_gate"], "NOT EVALUATED")
        self.assertEqual(gates["security_foundation_readiness_gate"], "NOT EVALUATED")

    def test_r20_remains_open(self) -> None:
        self.assertEqual(self.contract()["risks"]["R-20"], "open")

    def test_rt2_is_contract_only(self) -> None:
        rt2 = self.contract()["rt2"]
        self.assertEqual(rt2["boundary"], "P1")
        self.assertEqual(rt2["mode"], "contract-only")
        for key in ("storage", "events", "hash_chaining", "retention_engine",
                    "backup", "restore"):
            with self.subTest(key=key):
                self.assertFalse(rt2[key])

    def test_security_negative_tests_are_zero_of_31(self) -> None:
        nt = self.contract()["security_negative_tests"]
        self.assertEqual((nt["executed"], nt["total"]), (0, 31))

    def test_validation_issue_is_sortable(self) -> None:
        a = V.ValidationIssue("A", "p", "m")
        b = V.ValidationIssue("B", "p", "m")
        self.assertLess(a, b)
        self.assertEqual(sorted([b, a]), [a, b])


class TestValidatorCli(unittest.TestCase):
    def _run(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(VALIDATOR), *args],
            capture_output=True, text=True, cwd=str(REPO_ROOT),
        )

    def test_cli_default_call_returns_zero(self) -> None:
        self.assertEqual(self._run().returncode, 0)

    def test_cli_valid_output_matches_contract(self) -> None:
        self.assertEqual(self._run().stdout, "PROFILE-A-BUNDLE VALID\nissues=0\n")

    def test_cli_output_is_byte_identical_on_repeat(self) -> None:
        self.assertEqual(self._run().stdout, self._run().stdout)

    def test_cli_output_contains_no_absolute_path(self) -> None:
        out = self._run().stdout
        self.assertNotIn(str(REPO_ROOT), out)
        self.assertNotIn(":\\", out)

    def test_cli_accepts_explicit_root(self) -> None:
        self.assertEqual(self._run(str(BUNDLE)).returncode, 0)

    def test_cli_too_many_arguments_returns_two(self) -> None:
        self.assertEqual(self._run(str(BUNDLE), str(BUNDLE)).returncode, 2)

    def test_cli_missing_root_returns_one(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = self._run(str(Path(tmp) / "absent"))
        self.assertEqual(result.returncode, 1)

    def test_cli_error_output_has_no_traceback(self) -> None:
        result = self._run(str(BUNDLE), str(BUNDLE))
        self.assertNotIn("Traceback", result.stderr)


# ===========================================================================
# Negative tests — file set
# ===========================================================================


class TestFileSetNegative(_BundleFixture):
    def test_missing_root_is_invalid(self) -> None:
        shutil.rmtree(self.root)
        report = self.validate()
        self.assertFalse(report.valid)
        self.assertIn("BND-FILE-ROOT-MISSING", {i.code for i in report.issues})

    def test_root_is_not_a_directory(self) -> None:
        shutil.rmtree(self.root)
        self.root.write_text("x", encoding="utf-8")
        self.assertIn("BND-FILE-ROOT-NOT-DIR", self.codes())

    def test_missing_expected_file(self) -> None:
        (self.root / "README.md").unlink()
        self.assertIn("BND-FILE-MISSING", self.codes())

    def test_additional_file(self) -> None:
        (self.root / "extra.md").write_text("x", encoding="utf-8")
        self.assertIn("BND-FILE-UNEXPECTED", self.codes())

    def test_additional_directory(self) -> None:
        (self.root / "extra").mkdir()
        (self.root / "extra" / "f.md").write_text("x", encoding="utf-8")
        self.assertIn("BND-FILE-UNEXPECTED-DIR", self.codes())

    # --- symlink negative case --------------------------------------------
    #
    # The bundle must reject symlinked entries fail-closed. Creating a real
    # symlink needs a privilege this environment does not grant, so the
    # condition is simulated deterministically: one existing entry reports
    # itself as a symlink through ``Path.is_symlink`` while the full
    # ``validate_bundle`` pipeline runs unchanged. The control assertion in
    # ``test_symlink_is_rejected`` proves the simulation flips exactly the
    # branch under test and nothing else.

    @staticmethod
    def _reported_as_symlink(target: Path):
        """Report exactly ``target`` as a symlink; every other path honestly."""
        original = Path.is_symlink

        def fake(self: Path) -> bool:
            return True if self == target else original(self)

        return mock.patch.object(Path, "is_symlink", fake)

    def test_symlink_is_rejected(self) -> None:
        link = self.root / "link.md"
        link.write_text("placeholder", encoding="utf-8")

        # Control: as a plain file the entry is merely unexpected.
        before = self.codes()
        self.assertNotIn("BND-FILE-SYMLINK", before)
        self.assertIn("BND-FILE-UNEXPECTED", before)

        with self._reported_as_symlink(link):
            after = self.codes()
        self.assertIn("BND-FILE-SYMLINK", after)

    def test_symlinked_expected_file_fails_closed(self) -> None:
        readme = self.root / "README.md"
        with self._reported_as_symlink(readme):
            report = self.validate()
        codes = {i.code for i in report.issues}
        self.assertFalse(report.valid)
        self.assertIn("BND-FILE-SYMLINK", codes)
        # The entry is skipped, so the expected file also counts as missing.
        self.assertIn("BND-FILE-MISSING", codes)

    def test_utf8_bom_is_rejected(self) -> None:
        p = self.root / "bundle.json"
        p.write_bytes(b"\xef\xbb\xbf" + p.read_bytes())
        self.assertIn("BND-FILE-BOM", self.codes())

    def test_nul_byte_is_rejected(self) -> None:
        p = self.root / "operator.env.example"
        p.write_bytes(p.read_bytes() + b"\x00")
        self.assertIn("BND-FILE-NUL", self.codes())

    def test_non_utf8_file_is_rejected(self) -> None:
        # Invalid UTF-8 without a NUL byte, so the encoding check is reached.
        (self.root / "compose.yaml").write_bytes(b"\xff\xfe\xfd not utf-8")
        self.assertIn("BND-FILE-ENCODING", self.codes())

    def test_empty_contract_file_is_rejected(self) -> None:
        (self.root / "bundle.json").write_text("   \n", encoding="utf-8")
        self.assertIn("BND-FILE-EMPTY", self.codes())

    def test_file_outside_root_is_not_read(self) -> None:
        outside = self.root.parent / "outside.md"
        outside.write_text(forbidden_url(), encoding="utf-8")
        report = self.validate()
        self.assertTrue(report.valid)
        self.assertFalse(any("outside" in i.path for i in report.issues))

    def test_reported_paths_are_relative(self) -> None:
        (self.root / "extra.md").write_text("x", encoding="utf-8")
        for issue in self.validate().issues:
            with self.subTest(code=issue.code):
                self.assertFalse(issue.path.startswith("/"))
                self.assertNotIn(":\\", issue.path)


# ===========================================================================
# Negative tests — compose
# ===========================================================================


class TestComposeNegative(_BundleFixture):
    def test_invalid_json(self) -> None:
        (self.root / "compose.yaml").write_text("{not json", encoding="utf-8")
        self.assertIn("BND-COMPOSE-PARSE", self.codes())

    def test_services_missing(self) -> None:
        doc = self.compose()
        del doc["services"]
        self.write_compose(doc)
        self.assertIn("BND-COMPOSE-SERVICES-MISSING", self.codes())

    def test_control_plane_missing(self) -> None:
        doc = self.compose()
        del doc["services"]["control-plane"]
        self.write_compose(doc)
        self.assertIn("BND-COMPOSE-SERVICE-MISSING", self.codes())

    def test_data_worker_missing(self) -> None:
        doc = self.compose()
        del doc["services"]["data-worker"]
        self.write_compose(doc)
        self.assertIn("BND-COMPOSE-SERVICE-MISSING", self.codes())

    def test_additional_service(self) -> None:
        doc = self.compose()
        doc["services"]["extra"] = {}
        self.write_compose(doc)
        self.assertIn("BND-COMPOSE-SERVICE-UNEXPECTED", self.codes())

    def test_unknown_top_level_section(self) -> None:
        doc = self.compose()
        doc["x-extra"] = {}
        self.write_compose(doc)
        self.assertIn("BND-COMPOSE-TOPLEVEL", self.codes())

    def test_concrete_image_literal(self) -> None:
        doc = self.compose()
        doc["services"]["control-plane"]["image"] = "img" + ":" + "latest"
        self.write_compose(doc)
        self.assertIn("BND-COMPOSE-IMAGE-LITERAL", self.codes())

    def test_image_variable_with_default(self) -> None:
        doc = self.compose()
        doc["services"]["control-plane"]["image"] = "${CBP_CONTROL_PLANE_IMAGE:-fallback}"
        self.write_compose(doc)
        self.assertIn("BND-COMPOSE-IMAGE-DEFAULT", self.codes())

    def test_root_user_literal(self) -> None:
        doc = self.compose()
        doc["services"]["data-worker"]["user"] = "root"
        self.write_compose(doc)
        self.assertIn("BND-COMPOSE-USER-ROOT", self.codes())

    def test_numeric_root_identity(self) -> None:
        doc = self.compose()
        doc["services"]["data-worker"]["user"] = "0:0"
        self.write_compose(doc)
        self.assertIn("BND-COMPOSE-USER-ROOT", self.codes())

    def test_concrete_numeric_identity(self) -> None:
        doc = self.compose()
        doc["services"]["data-worker"]["user"] = "1234:1234"
        self.write_compose(doc)
        self.assertIn("BND-COMPOSE-USER-NUMERIC", self.codes())

    def test_missing_fail_closed_identity(self) -> None:
        doc = self.compose()
        doc["services"]["control-plane"]["user"] = "${CBP_CONTROL_PLANE_UID}"
        self.write_compose(doc)
        self.assertIn("BND-COMPOSE-USER-NOT-REQUIRED", self.codes())

    def test_read_only_false(self) -> None:
        doc = self.compose()
        doc["services"]["control-plane"]["read_only"] = False
        self.write_compose(doc)
        self.assertIn("BND-COMPOSE-READONLY", self.codes())

    def test_no_new_privileges_missing(self) -> None:
        doc = self.compose()
        doc["services"]["control-plane"]["security_opt"] = []
        self.write_compose(doc)
        self.assertIn("BND-COMPOSE-NONEWPRIV", self.codes())

    def test_cap_drop_all_missing(self) -> None:
        doc = self.compose()
        doc["services"]["data-worker"]["cap_drop"] = ["NET_RAW"]
        self.write_compose(doc)
        self.assertIn("BND-COMPOSE-CAPDROP", self.codes())

    def test_privileged_true(self) -> None:
        doc = self.compose()
        doc["services"]["data-worker"]["privileged"] = True
        self.write_compose(doc)
        self.assertIn("BND-COMPOSE-PRIVILEGED", self.codes())

    def test_restart_not_no(self) -> None:
        doc = self.compose()
        doc["services"]["control-plane"]["restart"] = "always"
        self.write_compose(doc)
        self.assertIn("BND-COMPOSE-RESTART", self.codes())

    def test_host_network(self) -> None:
        doc = self.compose()
        doc["services"]["control-plane"]["network_mode"] = "host"
        self.write_compose(doc)
        self.assertIn("BND-COMPOSE-HOST-NETWORK", self.codes())

    def test_host_pid(self) -> None:
        doc = self.compose()
        doc["services"]["control-plane"]["pid"] = "host"
        self.write_compose(doc)
        self.assertIn("BND-COMPOSE-HOST-PID", self.codes())

    def test_host_ipc(self) -> None:
        doc = self.compose()
        doc["services"]["control-plane"]["ipc"] = "host"
        self.write_compose(doc)
        self.assertIn("BND-COMPOSE-HOST-IPC", self.codes())

    def test_published_port(self) -> None:
        doc = self.compose()
        doc["services"]["control-plane"]["ports"] = ["8080:8080"]
        self.write_compose(doc)
        self.assertIn("BND-COMPOSE-PORTS", self.codes())

    def test_device_access(self) -> None:
        doc = self.compose()
        doc["services"]["data-worker"]["devices"] = ["/dev/null:/dev/null"]
        self.write_compose(doc)
        self.assertIn("BND-COMPOSE-DEVICES", self.codes())

    def test_docker_socket_mount(self) -> None:
        doc = self.compose()
        doc["services"]["control-plane"]["volumes"].append(
            {"type": "volume", "source": "sock",
             "target": "/var/run/docker.sock", "read_only": True}
        )
        self.write_compose(doc)
        self.assertIn("BND-COMPOSE-DOCKER-SOCKET", self.codes())

    def test_host_bind_mount(self) -> None:
        doc = self.compose()
        doc["services"]["control-plane"]["volumes"].append(
            {"type": "bind", "source": "/srv/data",
             "target": "/var/lib/cbp/canonical", "read_only": True}
        )
        self.write_compose(doc)
        self.assertIn("BND-COMPOSE-BIND-MOUNT", self.codes())

    def test_canonical_data_writable(self) -> None:
        doc = self.compose()
        for v in doc["services"]["data-worker"]["volumes"]:
            if v["source"] == "canonical-data":
                v["read_only"] = False
        self.write_compose(doc)
        self.assertIn("BND-COMPOSE-MOUNT-MODE", self.codes())

    def test_control_plane_quarantine_write(self) -> None:
        doc = self.compose()
        doc["services"]["control-plane"]["volumes"].append(
            {"type": "volume", "source": "quarantine",
             "target": "/var/lib/cbp/quarantine", "read_only": False}
        )
        self.write_compose(doc)
        self.assertIn("BND-COMPOSE-MOUNT-UNEXPECTED", self.codes())

    def test_data_worker_released_artifacts_write(self) -> None:
        doc = self.compose()
        doc["services"]["data-worker"]["volumes"].append(
            {"type": "volume", "source": "released-artifacts",
             "target": "/var/lib/cbp/released", "read_only": False}
        )
        self.write_compose(doc)
        self.assertIn("BND-COMPOSE-MOUNT-UNEXPECTED", self.codes())

    def test_backup_storage_mounted(self) -> None:
        doc = self.compose()
        doc["services"]["control-plane"]["volumes"].append(
            {"type": "volume", "source": "backup-storage",
             "target": "/var/lib/cbp/released", "read_only": False}
        )
        self.write_compose(doc)
        self.assertIn("BND-COMPOSE-FORBIDDEN-AREA", self.codes())

    def test_rt2_mounted_directly(self) -> None:
        doc = self.compose()
        doc["services"]["data-worker"]["volumes"].append(
            {"type": "volume", "source": "rt2-operational-evidence",
             "target": "/var/lib/cbp/derived", "read_only": False}
        )
        self.write_compose(doc)
        self.assertIn("BND-COMPOSE-FORBIDDEN-AREA", self.codes())

    def test_tmpfs_missing(self) -> None:
        doc = self.compose()
        doc["services"]["control-plane"]["tmpfs"] = []
        self.write_compose(doc)
        self.assertIn("BND-COMPOSE-TMPFS", self.codes())

    def test_network_not_internal(self) -> None:
        doc = self.compose()
        doc["networks"]["cbp-profile-a-internal"]["internal"] = False
        self.write_compose(doc)
        self.assertIn("BND-COMPOSE-NETWORK-NOT-INTERNAL", self.codes())

    def test_additional_network(self) -> None:
        doc = self.compose()
        doc["networks"]["public"] = {}
        self.write_compose(doc)
        self.assertIn("BND-COMPOSE-NETWORK-COUNT", self.codes())

    def test_external_network_name(self) -> None:
        doc = self.compose()
        doc["networks"]["cbp-profile-a-internal"]["external"] = True
        self.write_compose(doc)
        self.assertIn("BND-COMPOSE-NETWORK-FORBIDDEN", self.codes())

    def test_subnet_definition(self) -> None:
        doc = self.compose()
        doc["networks"]["cbp-profile-a-internal"]["ipam"] = {"config": []}
        self.write_compose(doc)
        self.assertIn("BND-COMPOSE-NETWORK-FORBIDDEN", self.codes())

    def test_gateway_definition(self) -> None:
        doc = self.compose()
        doc["networks"]["cbp-profile-a-internal"]["driver_opts"] = {"gateway": "x"}
        self.write_compose(doc)
        self.assertIn("BND-COMPOSE-NETWORK-FORBIDDEN", self.codes())

    def test_config_not_read_only(self) -> None:
        doc = self.compose()
        doc["services"]["control-plane"]["configs"][0]["mode"] = 0o644
        self.write_compose(doc)
        self.assertIn("BND-COMPOSE-CONFIG-WRITABLE", self.codes())

    def test_config_wrong_target(self) -> None:
        doc = self.compose()
        doc["services"]["data-worker"]["configs"][0]["target"] = "/etc/cbp/other.toml"
        self.write_compose(doc)
        self.assertIn("BND-COMPOSE-CONFIG-TARGET", self.codes())

    def test_disallowed_target_path(self) -> None:
        doc = self.compose()
        doc["services"]["data-worker"]["volumes"][0]["target"] = "/opt/other"
        self.write_compose(doc)
        self.assertIn("BND-COMPOSE-TARGET-PATH", self.codes())

    def test_service_on_foreign_network(self) -> None:
        doc = self.compose()
        doc["services"]["data-worker"]["networks"] = ["other"]
        self.write_compose(doc)
        self.assertIn("BND-COMPOSE-SERVICE-NETWORK", self.codes())


# ===========================================================================
# Negative tests — bundle contract
# ===========================================================================


class TestContractNegative(_BundleFixture):
    def test_non_canonical_formatting(self) -> None:
        doc = self.contract()
        (self.root / "bundle.json").write_text(
            json.dumps(doc, ensure_ascii=False), encoding="utf-8", newline=""
        )
        self.assertIn("BND-DETERMINISM-CANONICAL", self.codes())

    def test_file_list_incomplete(self) -> None:
        doc = self.contract()
        doc["files"] = doc["files"][:-1]
        self.write_contract(doc)
        self.assertIn("BND-CONTRACT-FILES", self.codes())

    def test_file_list_has_extra_path(self) -> None:
        doc = self.contract()
        doc["files"] = sorted(doc["files"] + ["extra.md"])
        self.write_contract(doc)
        self.assertIn("BND-CONTRACT-FILES", self.codes())

    def test_identity_mismatch_between_layers(self) -> None:
        doc = self.contract()
        doc["services"]["data-worker"]["service_identity"] = "svc-control-plane"
        self.write_contract(doc)
        self.assertIn("BND-CONTRACT-IDENTITY-MISMATCH", self.codes())

    def test_wrong_target_state(self) -> None:
        doc = self.contract()
        doc["target_state"] = "Z2"
        self.write_contract(doc)
        self.assertIn("BND-CONTRACT-IDENTITY", self.codes())

    def test_deployed_true(self) -> None:
        doc = self.contract()
        doc["deployed"] = True
        self.write_contract(doc)
        self.assertIn("BND-CONTRACT-IDENTITY", self.codes())

    def test_runtime_started_true(self) -> None:
        doc = self.contract()
        doc["runtime_started"] = True
        self.write_contract(doc)
        self.assertIn("BND-CONTRACT-IDENTITY", self.codes())

    def test_egress_default_not_deny(self) -> None:
        doc = self.contract()
        doc["egress"]["default"] = "allow"
        self.write_contract(doc)
        self.assertIn("BND-CONTRACT-EGRESS-DEFAULT", self.codes())

    def test_egress_wildcard(self) -> None:
        doc = self.contract()
        doc["egress"]["target_classes"][0] = "*"
        self.write_contract(doc)
        self.assertIn("BND-CONTRACT-EGRESS-WILDCARD", self.codes())

    def test_egress_concrete_endpoint_flag(self) -> None:
        doc = self.contract()
        doc["egress"]["concrete_endpoints"] = True
        self.write_contract(doc)
        self.assertIn("BND-CONTRACT-EGRESS-ENDPOINT", self.codes())

    def test_egress_class_count_wrong(self) -> None:
        doc = self.contract()
        doc["egress"]["target_classes"] = doc["egress"]["target_classes"][:5]
        self.write_contract(doc)
        self.assertIn("BND-CONTRACT-EGRESS-COUNT", self.codes())

    def test_unknown_secret_provider(self) -> None:
        doc = self.contract()
        doc["secret_provider"]["provider_type"] = "vault"
        self.write_contract(doc)
        self.assertIn("BND-CONTRACT-SECRET-PROVIDER", self.codes())

    def test_invalid_secret_reference_syntax(self) -> None:
        doc = self.contract()
        doc["secret_provider"]["reference_syntax"] = "cbp-secret:v9:file:x"
        self.write_contract(doc)
        self.assertIn("BND-CONTRACT-SECRET-SYNTAX", self.codes())

    def test_missing_reference_does_not_block(self) -> None:
        doc = self.contract()
        doc["secret_provider"]["missing_reference_blocks"] = False
        self.write_contract(doc)
        self.assertIn("BND-CONTRACT-SECRET", self.codes())

    def test_secret_values_declared_in_bundle(self) -> None:
        doc = self.contract()
        doc["secret_provider"]["values_in_bundle"] = True
        self.write_contract(doc)
        self.assertIn("BND-CONTRACT-SECRET", self.codes())

    def test_capability_greater_than_zero(self) -> None:
        doc = self.contract()
        doc["capabilities"]["implemented"] = 1
        self.write_contract(doc)
        self.assertIn("BND-CONTRACT-CAPABILITIES", self.codes())

    def test_mapping_gate_released(self) -> None:
        doc = self.contract()
        doc["gates"]["mapping_activation_gate"] = "APPROVED FOR ACTIVATION"
        self.write_contract(doc)
        self.assertIn("BND-CONTRACT-GATE-STATUS", self.codes())

    def test_security_gate_released(self) -> None:
        doc = self.contract()
        doc["gates"]["security_foundation_readiness_gate"] = "ACCEPTED BY HUMAN MAINTAINER"
        self.write_contract(doc)
        self.assertIn("BND-CONTRACT-GATE-STATUS", self.codes())

    def test_control_marked_implemented(self) -> None:
        doc = self.contract()
        doc["security_controls"]["KB-01"]["status"] = "implemented"
        self.write_contract(doc)
        codes = self.codes()
        self.assertIn("BND-CONTRACT-CONTROL-STATUS", codes)
        self.assertIn("BND-CONTRACT-CONTROL-FORBIDDEN", codes)

    def test_control_marked_tested(self) -> None:
        doc = self.contract()
        doc["security_controls"]["KB-05"]["status"] = "tested"
        self.write_contract(doc)
        self.assertIn("BND-CONTRACT-CONTROL-FORBIDDEN", self.codes())

    def test_control_marked_enforced(self) -> None:
        doc = self.contract()
        doc["security_controls"]["KB-10"]["status"] = "ENFORCED"
        self.write_contract(doc)
        self.assertIn("BND-CONTRACT-CONTROL-FORBIDDEN", self.codes())

    def test_control_list_incomplete(self) -> None:
        doc = self.contract()
        del doc["security_controls"]["KB-12"]
        self.write_contract(doc)
        self.assertIn("BND-CONTRACT-CONTROLS", self.codes())

    def test_rt2_marked_implemented(self) -> None:
        doc = self.contract()
        doc["rt2"]["storage"] = True
        self.write_contract(doc)
        self.assertIn("BND-CONTRACT-RT2-IMPLEMENTED", self.codes())

    def test_rt2_boundary_changed(self) -> None:
        doc = self.contract()
        doc["rt2"]["boundary"] = "P2"
        self.write_contract(doc)
        self.assertIn("BND-CONTRACT-RT2-BOUNDARY", self.codes())

    def test_backup_job_claimed(self) -> None:
        doc = self.contract()
        doc["backup"]["job_implemented"] = True
        self.write_contract(doc)
        self.assertIn("BND-CONTRACT-BACKUP", self.codes())

    def test_restore_evidence_claimed(self) -> None:
        doc = self.contract()
        doc["backup"]["rt2_restore_evidence"] = True
        self.write_contract(doc)
        self.assertIn("BND-CONTRACT-BACKUP", self.codes())

    def test_r20_closed(self) -> None:
        doc = self.contract()
        doc["risks"]["R-20"] = "closed"
        self.write_contract(doc)
        self.assertIn("BND-CONTRACT-RISK", self.codes())

    def test_negative_tests_claimed_executed(self) -> None:
        doc = self.contract()
        doc["security_negative_tests"]["executed"] = 31
        self.write_contract(doc)
        self.assertIn("BND-CONTRACT-NEGATIVE-TESTS", self.codes())

    def test_service_privilege_escalation(self) -> None:
        doc = self.contract()
        doc["services"]["data-worker"]["publish_rights"] = True
        self.write_contract(doc)
        self.assertIn("BND-CONTRACT-PRIVILEGE", self.codes())

    def test_service_backup_access(self) -> None:
        doc = self.contract()
        doc["services"]["control-plane"]["backup_storage_access"] = True
        self.write_contract(doc)
        self.assertIn("BND-CONTRACT-PRIVILEGE", self.codes())

    def test_data_area_missing(self) -> None:
        doc = self.contract()
        del doc["data_areas"]["quarantine"]
        self.write_contract(doc)
        self.assertIn("BND-CONTRACT-DATA-AREAS", self.codes())

    def test_data_area_field_missing(self) -> None:
        doc = self.contract()
        del doc["data_areas"]["canonical-data"]["backup_required"]
        self.write_contract(doc)
        self.assertIn("BND-CONTRACT-DATA-AREAS", self.codes())

    def test_rt2_area_not_contract_only(self) -> None:
        doc = self.contract()
        doc["data_areas"]["rt2-operational-evidence"]["mode"] = "read-write"
        self.write_contract(doc)
        self.assertIn("BND-CONTRACT-DATA-AREAS", self.codes())

    def test_areas_inconsistent_with_mounts(self) -> None:
        doc = self.contract()
        doc["services"]["control-plane"]["allowed_areas"]["canonical-data"] = "read-write"
        self.write_contract(doc)
        self.assertIn("BND-CONTRACT-AREAS", self.codes())

    def test_contract_not_an_object(self) -> None:
        (self.root / "bundle.json").write_text("[1]\n", encoding="utf-8")
        self.assertIn("BND-CONTRACT-STRUCTURE", self.codes())

    def test_contract_invalid_json(self) -> None:
        (self.root / "bundle.json").write_text("{oops\n", encoding="utf-8")
        self.assertIn("BND-CONTRACT-PARSE", self.codes())


# ===========================================================================
# Negative tests — TOML, environment, leakage, determinism
# ===========================================================================


class TestConfigNegative(_BundleFixture):
    def _write(self, name: str, text: str) -> None:
        (self.root / "config" / f"{name}.example.toml").write_text(text, encoding="utf-8")

    def _patch(self, name: str, old: str, new: str) -> None:
        p = self.root / "config" / f"{name}.example.toml"
        text = p.read_text(encoding="utf-8")
        self.assertIn(old, text)
        p.write_text(text.replace(old, new, 1), encoding="utf-8")

    def test_invalid_toml(self) -> None:
        self._write("control-plane", "not = = toml\n")
        self.assertIn("BND-CONFIG-PARSE", self.codes())

    def test_profile_not_a(self) -> None:
        self._patch("control-plane", 'deployment_profile = "A"', 'deployment_profile = "B"')
        self.assertIn("BND-CONFIG-PROFILE", self.codes())

    def test_mode_not_offline_template(self) -> None:
        self._patch("data-worker", 'mode = "offline-template"', 'mode = "production"')
        self.assertIn("BND-CONFIG-MODE", self.codes())

    def test_identity_wrong(self) -> None:
        self._patch("data-worker", 'service_identity = "svc-data-worker"',
                    'service_identity = "svc-control-plane"')
        self.assertIn("BND-CONFIG-IDENTITY", self.codes())

    def test_real_source_activated(self) -> None:
        self._patch("data-worker", "real_source_bound = false", "real_source_bound = true")
        self.assertIn("BND-CONFIG-ACTIVATION", self.codes())

    def test_productive_mapping_activated(self) -> None:
        self._patch("control-plane", "productive_mapping = false", "productive_mapping = true")
        self.assertIn("BND-CONFIG-ACTIVATION", self.codes())

    def test_automatic_activation_enabled(self) -> None:
        self._patch("control-plane", "automatic_activation = false",
                    "automatic_activation = true")
        self.assertIn("BND-CONFIG-ACTIVATION", self.codes())

    def test_rt2_not_contract_only(self) -> None:
        self._patch("data-worker", 'mode = "contract-only"', 'mode = "append-only"')
        self.assertIn("BND-CONFIG-RT2", self.codes())

    def test_rt2_marked_implemented(self) -> None:
        self._patch("data-worker", "implemented = false", "implemented = true")
        self.assertIn("BND-CONFIG-RT2-IMPLEMENTED", self.codes())

    def test_secret_provider_unknown(self) -> None:
        self._patch("control-plane", 'provider_type = "file"', 'provider_type = "vault"')
        self.assertIn("BND-CONFIG-SECRET-PROVIDER", self.codes())

    def test_secret_reference_invalid(self) -> None:
        self._patch("control-plane", 'example_reference = "cbp-secret:v1:file:<opaque-id>"',
                    'example_reference = "cbp-secret:v0:file:x"')
        self.assertIn("BND-CONFIG-SECRET-SYNTAX", self.codes())

    def test_egress_not_deny_by_default(self) -> None:
        self._patch("data-worker", 'mode = "deny-by-default"', 'mode = "allow-all"')
        self.assertIn("BND-CONFIG-EGRESS", self.codes())

    def test_access_role_inconsistent(self) -> None:
        self._patch("data-worker", 'canonical_data = "read-only"',
                    'canonical_data = "read-write"')
        self.assertIn("BND-CONFIG-ACCESS", self.codes())

    def test_backup_access_granted(self) -> None:
        self._patch("control-plane", 'backup_storage = "none"',
                    'backup_storage = "read-write"')
        self.assertIn("BND-CONFIG-ACCESS", self.codes())

    def test_rt2_direct_access_granted(self) -> None:
        self._patch("data-worker", 'rt2_direct = "none"', 'rt2_direct = "read-write"')
        self.assertIn("BND-CONFIG-ACCESS", self.codes())

    def test_publish_rights_granted(self) -> None:
        self._patch("data-worker", "publish_rights = false", "publish_rights = true")
        self.assertIn("BND-CONFIG-PRIVILEGE", self.codes())

    def test_unknown_contract_section(self) -> None:
        p = self.root / "config" / "control-plane.example.toml"
        p.write_text(p.read_text(encoding="utf-8") + '\n[surprise]\nx = 1\n', encoding="utf-8")
        self.assertIn("BND-CONFIG-TOPLEVEL", self.codes())


class TestEnvNegative(_BundleFixture):
    def _env(self) -> Path:
        return self.root / "operator.env.example"

    def test_prefilled_required_value(self) -> None:
        p = self._env()
        p.write_text(p.read_text(encoding="utf-8").replace(
            "CBP_CONTROL_PLANE_IMAGE=", "CBP_CONTROL_PLANE_IMAGE=someimage"), encoding="utf-8")
        self.assertIn("BND-ENV-PREFILLED", self.codes())

    def test_concrete_uid_value(self) -> None:
        p = self._env()
        p.write_text(p.read_text(encoding="utf-8").replace(
            "CBP_CONTROL_PLANE_UID=", "CBP_CONTROL_PLANE_UID=1000"), encoding="utf-8")
        codes = self.codes()
        self.assertTrue({"BND-ENV-NUMERIC-IDENTITY", "BND-ENV-PREFILLED"} & codes)

    def test_additional_variable(self) -> None:
        p = self._env()
        p.write_text(p.read_text(encoding="utf-8") + "CBP_EXTRA=1\n", encoding="utf-8")
        self.assertIn("BND-ENV-UNEXPECTED", self.codes())

    def test_missing_required_variable(self) -> None:
        p = self._env()
        lines = [ln for ln in p.read_text(encoding="utf-8").splitlines()
                 if not ln.startswith("CBP_DATA_WORKER_GID")]
        p.write_text("\n".join(lines) + "\n", encoding="utf-8")
        self.assertIn("BND-ENV-MISSING", self.codes())

    def test_wrong_profile_value(self) -> None:
        p = self._env()
        p.write_text(p.read_text(encoding="utf-8").replace(
            "CBP_DEPLOYMENT_PROFILE=A", "CBP_DEPLOYMENT_PROFILE=D"), encoding="utf-8")
        self.assertIn("BND-ENV-PROFILE", self.codes())

    def test_duplicate_variable(self) -> None:
        p = self._env()
        p.write_text(p.read_text(encoding="utf-8") + "CBP_DEPLOYMENT_PROFILE=A\n",
                     encoding="utf-8")
        self.assertIn("BND-ENV-DUPLICATE", self.codes())


class TestLeakageNegative(_BundleFixture):
    def _append_readme(self, payload: str) -> None:
        p = self.root / "README.md"
        p.write_text(p.read_text(encoding="utf-8") + "\n" + payload + "\n", encoding="utf-8")

    def test_ipv4_address_is_detected(self) -> None:
        self._append_readme(forbidden_ipv4())
        self.assertIn("BND-LEAK-IPV4", self.codes())

    def test_url_is_detected(self) -> None:
        self._append_readme(forbidden_url())
        self.assertTrue({"BND-LEAK-URL", "BND-LEAK-DOMAIN"} & self.codes())

    def test_domain_is_detected(self) -> None:
        self._append_readme(forbidden_domain())
        self.assertIn("BND-LEAK-DOMAIN", self.codes())

    def test_mac_address_is_detected(self) -> None:
        self._append_readme(forbidden_mac())
        self.assertIn("BND-LEAK-MAC", self.codes())

    def test_uuid_is_detected(self) -> None:
        self._append_readme(forbidden_uuid())
        self.assertIn("BND-LEAK-UUID", self.codes())

    def test_windows_path_is_detected(self) -> None:
        self._append_readme(forbidden_win_path())
        self.assertIn("BND-LEAK-WINDOWS-PATH", self.codes())

    def test_unc_path_is_detected(self) -> None:
        self._append_readme(forbidden_unc())
        self.assertIn("BND-LEAK-UNC-PATH", self.codes())

    def test_token_assignment_is_detected(self) -> None:
        self._append_readme(forbidden_token_line())
        self.assertIn("BND-LEAK-TOKEN-ASSIGNMENT", self.codes())

    def test_password_assignment_is_detected(self) -> None:
        self._append_readme("pass" + "word" + "=" + "hunter")
        self.assertIn("BND-LEAK-PASSWORD-ASSIGNMENT", self.codes())

    def test_private_key_marker_is_detected(self) -> None:
        self._append_readme("BEGIN" + " " + "PRIVATE" + " " + "KEY")
        self.assertIn("BND-LEAK-PRIVATE-KEY", self.codes())

    def test_numeric_identity_is_detected(self) -> None:
        self._append_readme("u" + "id" + ": " + "1000")
        self.assertIn("BND-LEAK-NUMERIC-IDENTITY", self.codes())

    def test_validator_is_exempt_from_own_content_scan(self) -> None:
        report = self.validate()
        self.assertTrue(report.valid)
        self.assertFalse(any(i.path == "validate.py" and i.code.startswith("BND-LEAK-")
                             for i in report.issues))


class TestDeterminism(_BundleFixture):
    def test_issues_are_stably_sorted(self) -> None:
        (self.root / "extra.md").write_text("x", encoding="utf-8")
        (self.root / "README.md").unlink()
        issues = self.validate().issues
        self.assertEqual(list(issues), sorted(issues))

    def test_invalid_bundle_output_is_repeatable(self) -> None:
        (self.root / "extra.md").write_text("x", encoding="utf-8")
        self.assertEqual(self.validate().issues, self.validate().issues)

    def test_no_absolute_path_in_any_issue(self) -> None:
        (self.root / "extra.md").write_text("x", encoding="utf-8")
        for issue in self.validate().issues:
            with self.subTest(code=issue.code):
                self.assertFalse(issue.path.startswith("/"))

    def test_every_issue_carries_a_code(self) -> None:
        (self.root / "extra.md").write_text("x", encoding="utf-8")
        for issue in self.validate().issues:
            with self.subTest(path=issue.path):
                self.assertTrue(issue.code.startswith("BND-"))
                self.assertTrue(issue.message)


class TestNoForbiddenLiterals(unittest.TestCase):
    """The repository must not contain complete forbidden literals."""

    def test_test_file_contains_no_complete_forbidden_literal(self) -> None:
        text = Path(__file__).read_text(encoding="utf-8")
        for value in (forbidden_ipv4(), forbidden_url(), forbidden_domain(),
                      forbidden_token_line(), forbidden_unc(), forbidden_win_path(),
                      forbidden_mac(), forbidden_uuid()):
            with self.subTest(value=value[:6]):
                self.assertNotIn(value, text)

    def test_bundle_files_contain_no_forbidden_literal(self) -> None:
        for rel in EXPECTED_FILES:
            if rel == "validate.py":
                continue
            text = (BUNDLE / rel).read_text(encoding="utf-8")
            for value in (forbidden_ipv4(), forbidden_url(), forbidden_domain(),
                          forbidden_unc(), forbidden_win_path(), forbidden_mac()):
                with self.subTest(rel=rel, value=value[:6]):
                    self.assertNotIn(value, text)


class TestScopeBoundaries(unittest.TestCase):
    """The bundle must not claim anything beyond its authorised scope."""

    def setUp(self) -> None:
        self.doc = json.loads((BUNDLE / "bundle.json").read_text(encoding="utf-8"))

    def _imports(self) -> set[str]:
        tree = ast.parse(VALIDATOR.read_text(encoding="utf-8"))
        names: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names.update(a.name.split(".")[0] for a in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                names.add(node.module.split(".")[0])
        return names

    def test_validator_imports_no_external_dependency(self) -> None:
        self.assertTrue(self._imports() <= set(sys.stdlib_module_names))

    def test_validator_has_no_process_or_network_import(self) -> None:
        for banned in ("subprocess", "socket", "urllib", "http", "os", "shutil"):
            with self.subTest(banned=banned):
                self.assertNotIn(banned, self._imports())

    def test_bundle_declares_not_deployed(self) -> None:
        self.assertFalse(self.doc["deployed"])
        self.assertFalse(self.doc["runtime_started"])

    def test_bundle_scope_is_z1_s2_p1(self) -> None:
        self.assertEqual(self.doc["target_state"], "Z1")
        self.assertEqual(self.doc["scope"], "S2")
        self.assertEqual(self.doc["rt2_boundary"], "P1")

    def test_runbooks_exist_outside_the_bundle(self) -> None:
        for name in ("INSTALLATION", "VALIDATION", "ROLLBACK"):
            with self.subTest(name=name):
                p = REPO_ROOT / "docs" / "operations" / f"PROFILE_A_{name}_RUNBOOK.md"
                self.assertTrue(p.is_file())
                self.assertFalse((BUNDLE / p.name).exists())

    def test_runtime_contract_document_exists(self) -> None:
        self.assertTrue((REPO_ROOT / "docs" / "runtime"
                         / "PROFILE_A_DEPLOYMENT_BUNDLE.md").is_file())


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
