"""Tests der ``source-mapping activation-evaluate``-CLI (CBP-WP-016)."""

from __future__ import annotations

import io
import json
import tempfile
import unittest
from pathlib import Path

from core.core_brain.cli import main
from core.core_brain.errors import EXIT_CODES, ExitCode

from tests import gate_fixtures as fx

REPO_ROOT = Path(__file__).resolve().parent.parent


def run_cli(*argv: str) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    code = main(list(argv), out=out, err=err)
    return code, out.getvalue(), err.getvalue()


def _argv(case, *, synthetic: bool = True, as_json: bool = False) -> list[str]:
    argv = [
        "source-mapping", "activation-evaluate",
        "--draft", str(case["draft_path"]),
        "--policy", str(case["policy_path"]),
        "--registry", str(case["root"]),
        "--source-id", case["source_id"],
        "--evidence", str(case["evidence_path"]),
    ]
    if synthetic:
        argv.append("--synthetic-test-only")
    if as_json:
        argv.append("--json")
    return argv


class TestGateCli(unittest.TestCase):
    def test_help_exits_zero(self) -> None:
        import contextlib

        with contextlib.redirect_stdout(io.StringIO()):
            code = main(["source-mapping", "activation-evaluate", "--help"])
        self.assertEqual(code, EXIT_CODES[ExitCode.OK])

    def test_valid_call_blocks_exit_14(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            code, out, _ = run_cli(*_argv(fx.build_case(tmp)))
        self.assertEqual(code, EXIT_CODES[ExitCode.MAPPING_GATE_EVALUATION_BLOCKED])
        self.assertEqual(code, 14)
        self.assertIn("evaluation_status:      BLOCKED", out)

    def test_json_is_canonical(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            code, out, _ = run_cli(*_argv(fx.build_case(tmp), as_json=True))
        self.assertEqual(code, 14)
        parsed = json.loads(out)
        self.assertEqual(out.strip(), json.dumps(parsed, indent=2, sort_keys=True))
        self.assertEqual(parsed["evaluation_status"], "BLOCKED")
        self.assertEqual(len(parsed["criterion_results"]), 20)

    def test_no_synthetic_flag_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            code, _, err = run_cli(*_argv(fx.build_case(tmp), synthetic=False))
        self.assertEqual(code, 14)
        self.assertIn("GATE_SYNTHETIC_CONFIRMATION_MISSING", err)

    def test_bad_policy_exit_2(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            case = fx.build_case(tmp)
            bad = Path(tmp) / "bad.toml"
            bad.write_text('schema_version = "9.9"', encoding="utf-8")
            argv = _argv(case)
            argv[argv.index("--policy") + 1] = str(bad)
            code, _, _ = run_cli(*argv)
        self.assertEqual(code, EXIT_CODES[ExitCode.CONFIG_INVALID])

    def test_invalid_evidence_json_blocks_without_stacktrace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            case = fx.build_case(tmp)
            case["evidence_path"].write_text("{ not json ", encoding="utf-8")
            code, _, err = run_cli(*_argv(case))
        self.assertEqual(code, 14)
        self.assertIn("GATE_EVIDENCE_PARSE_ERROR", err)
        self.assertNotIn("Traceback", err)

    def test_unknown_evidence_field_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            code, _, err = run_cli(
                *_argv(fx.build_case(tmp, evidence_overrides={"surprise": "x"}))
            )
        self.assertEqual(code, 14)
        self.assertIn("GATE_EVIDENCE_UNKNOWN_FIELD", err)

    def test_output_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            case = fx.build_case(tmp)
            a = run_cli(*_argv(case, as_json=True))
            b = run_cli(*_argv(case, as_json=True))
        self.assertEqual(a, b)

    def test_no_leaks_in_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            case = fx.build_case(tmp)
            _, out, err = run_cli(*_argv(case))
            combined = out + err
        self.assertNotIn(str(case["root"]), combined)
        self.assertNotIn(str(case["draft_path"]), combined)
        self.assertNotIn("synthetic-placeholder", combined)
        self.assertNotIn("synthetic:notes-ref-marker", combined)

    def test_leaky_source_id_blocks_without_echo(self) -> None:
        # N2: eine nicht opake Source ID wird fail-closed abgewiesen und
        # erscheint nicht im Report oder in der Diagnostik.
        for leaky in ("C:\\Users\\secret.txt", "https://example.invalid/private",
                      "/etc/shadow", "../secret"):
            with self.subTest(source_id=leaky):
                with tempfile.TemporaryDirectory() as tmp:
                    case = fx.build_case(tmp)
                    argv = _argv(case)
                    argv[argv.index("--source-id") + 1] = leaky
                    code, out, err = run_cli(*argv)
                self.assertEqual(code, 14)
                self.assertIn("GATE_EVIDENCE_INVALID_VALUE", err)
                self.assertNotIn(leaky, out + err)
                self.assertNotIn("Traceback", err)

    def test_leaky_mapping_id_blocks_without_echo(self) -> None:
        # B.2: eine ungueltige oder unsichere mapping_id blockiert vor der
        # Reporterzeugung — Exit 14, kein Report, kein `mapping_id: null`,
        # kein Echo des Werts, kein Stacktrace.
        for leaky in ("C:\\Users\\secret.txt", "https://example.invalid/private",
                      "/etc/shadow", "../secret", "AKIA0000000000000000",
                      "Bearer-example-secret-value", "password-example-secret"):
            with self.subTest(mapping_id=leaky):
                draft = fx.valid_draft()
                draft["mapping_id"] = leaky
                with tempfile.TemporaryDirectory() as tmp:
                    case = fx.build_case(tmp, draft=draft)
                    code, out, err = run_cli(*_argv(case))
                self.assertEqual(code, 14)
                self.assertIn("GATE_EVIDENCE_INVALID_VALUE", err)
                self.assertNotIn(leaky, out + err)
                self.assertNotIn("mapping_id", out)  # kein Report, kein null-Fallback
                self.assertNotIn("Traceback", err)

    def test_exit_code_14_is_collision_free(self) -> None:
        codes = {
            EXIT_CODES[c]
            for c in ExitCode
            if c is not ExitCode.MAPPING_GATE_EVALUATION_BLOCKED
        }
        self.assertNotIn(14, codes)

    def test_repository_unchanged(self) -> None:
        def _snapshot() -> set[Path]:
            return set((REPO_ROOT / "core").rglob("*")) | set(
                (REPO_ROOT / "config").rglob("*")
            )

        before = _snapshot()
        with tempfile.TemporaryDirectory() as tmp:
            run_cli(*_argv(fx.build_case(tmp)))
        self.assertEqual(_snapshot(), before)

    def test_existing_commands_unchanged(self) -> None:
        # run bleibt 4; source-registry activate bleibt 11; quarantine release bleibt 7.
        code, _, _ = run_cli(
            "run", "--config", str(REPO_ROOT / "config" / "runtime.example.toml")
        )
        self.assertEqual(code, EXIT_CODES[ExitCode.RUNTIME_START_BLOCKED])
        code, _, _ = run_cli(
            "source-registry", "activate", "--registry", "unused",
            "--id", fx.SOURCE_ID,
        )
        self.assertEqual(code, EXIT_CODES[ExitCode.SOURCE_REGISTRY_ACTIVATION_BLOCKED])
        code, _, _ = run_cli(
            "quarantine", "release", "--store", "unused", "--id", "q-unused"
        )
        self.assertEqual(code, EXIT_CODES[ExitCode.QUARANTINE_RELEASE_BLOCKED])


class TestWP017Cli(unittest.TestCase):
    """CBP-WP-017 — Schema 2.0 über den bestehenden --evidence-Pfad."""

    def test_leaky_artifact_id_blocks_without_echo(self) -> None:
        for leaky in ("/etc/shadow-secret", "C:\\Users\\secret.txt",
                      "https://example.invalid/p", "art-XYZ"):
            with self.subTest(artifact_id=leaky):
                with tempfile.TemporaryDirectory() as tmp:
                    case = fx.build_case(tmp, artifact_specs={2: [{"artifact_id": leaky}]})
                    code, out, err = run_cli(*_argv(case))
                self.assertEqual(code, 14)
                self.assertIn("GATE_EVIDENCE_INVALID_VALUE", err)
                self.assertNotIn(leaky, out + err)
                self.assertNotIn("evaluation_status", out)  # kein Report
                self.assertNotIn("Traceback", err)

    def test_schema_1_0_rejected_via_cli(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            case = fx.build_case(
                tmp, evidence_overrides={"evidence_schema_version": "1.0"})
            code, out, err = run_cli(*_argv(case))
        self.assertEqual(code, 14)
        self.assertIn("GATE_EVIDENCE_SCHEMA_UNSUPPORTED", err)
        self.assertNotIn("evaluation_status", out)

    def test_report_has_new_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            code, out, _ = run_cli(*_argv(fx.build_case(tmp), as_json=True))
        self.assertEqual(code, 14)
        parsed = json.loads(out)
        for field in ("evidence_contract_revision", "evidence_contract_sha256",
                      "validated_artifact_count", "invalid_artifact_count",
                      "stale_artifact_count", "conflicting_artifact_count"):
            self.assertIn(field, parsed)
        self.assertRegex(parsed["evidence_contract_sha256"], r"\A[0-9a-f]{64}\Z")
        self.assertEqual(parsed["evidence_contract_revision"], "2.0")

    def test_report_counts_and_no_artifact_leak(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            case = fx.build_case(tmp, artifact_specs={
                2: [{}],
                4: [{"corrupt_hash": True}],
                6: [{}, {"artifact_id": fx.ART_ID_B}],
            })
            code, out, err = run_cli(*_argv(case, as_json=True))
        parsed = json.loads(out)
        self.assertEqual(parsed["validated_artifact_count"], 1)
        self.assertEqual(parsed["invalid_artifact_count"], 1)
        self.assertEqual(parsed["conflicting_artifact_count"], 2)
        combined = out + err
        # Keine Artefakt-IDs, keine Rohartefakt-Metadaten im Report.
        self.assertNotIn(fx.ART_ID_A, combined)
        self.assertNotIn(fx.ART_ID_B, combined)
        self.assertNotIn("producer_class", combined)
        self.assertNotIn("binding_sha256", combined)
        self.assertNotIn("artifact_sha256", combined)

    def test_json_still_canonical_with_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            case = fx.build_case(tmp, artifact_specs={3: [{}]})
            a = run_cli(*_argv(case, as_json=True))
            b = run_cli(*_argv(case, as_json=True))
        self.assertEqual(a, b)
        parsed = json.loads(a[1])
        self.assertEqual(a[1].strip(), json.dumps(parsed, indent=2, sort_keys=True))

    def test_activation_check_still_exit_13(self) -> None:
        # WP-015 unverändert: `activation-check` verweigert weiter (Exit 13).
        with tempfile.TemporaryDirectory() as tmp:
            case = fx.build_case(tmp)
            code, _, _ = run_cli(
                "source-mapping", "activation-check",
                "--draft", str(case["draft_path"]),
                "--policy", str(case["policy_path"]),
                "--registry", str(case["root"]),
                "--source-id", case["source_id"],
                "--synthetic-test-only",
            )
        self.assertEqual(code, EXIT_CODES[ExitCode.SOURCE_MAPPING_ACTIVATION_BLOCKED])
        self.assertEqual(code, 13)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
