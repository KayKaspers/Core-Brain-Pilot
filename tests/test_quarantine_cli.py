"""Tests der Quarantäne-CLI (CBP-WP-013).

Deckt die Exitcodes der vier Unterkommandos, die minimierten Ausgaben, die
immer verweigernde Freigabe, die Fortführung des fail-closed ``run`` und die
Zusage ab, dass kein CLI-Pfad einen Eingabepfad oder Inhalt ausgibt.
"""

from __future__ import annotations

import io
import json
import tempfile
import unittest
from pathlib import Path

from core.core_brain.cli import main
from core.core_brain.errors import EXIT_CODES, ExitCode

REPO_ROOT = Path(__file__).resolve().parent.parent
EXAMPLE_POLICY = REPO_ROOT / "config" / "quarantine_policy.example.toml"
MARKER = "<!-- synthetic-test-only -->"


def run_cli(*argv: str) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    code = main(list(argv), out=out, err=err)
    return code, out.getvalue(), err.getvalue()


def _write(tmp: str, name: str, text: str) -> Path:
    target = Path(tmp) / name
    target.write_text(text, encoding="utf-8")
    return target


class TestQuarantineScanCli(unittest.TestCase):
    """Exitcodes von ``quarantine scan``."""

    def test_scan_ready_exit_zero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = _write(tmp, "a.md", f"{MARKER}\n# ok\ntext\n")
            code, _, _ = run_cli(
                "quarantine", "scan", "--input", str(path),
                "--policy", str(EXAMPLE_POLICY),
                "--source-ref", "synthetic:cli", "--synthetic-test-only",
            )
        self.assertEqual(code, EXIT_CODES[ExitCode.OK])

    def test_scan_review_exit_five(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = _write(tmp, "a.md", f"{MARKER}\nuser@example.com\n")
            code, _, _ = run_cli(
                "quarantine", "scan", "--input", str(path),
                "--policy", str(EXAMPLE_POLICY),
                "--source-ref", "synthetic:cli", "--synthetic-test-only",
            )
        self.assertEqual(code, EXIT_CODES[ExitCode.QUARANTINE_REVIEW_REQUIRED])

    def test_scan_blocked_exit_six(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = _write(tmp, "a.md", "no marker\n")
            code, _, _ = run_cli(
                "quarantine", "scan", "--input", str(path),
                "--policy", str(EXAMPLE_POLICY),
                "--source-ref", "synthetic:cli", "--synthetic-test-only",
            )
        self.assertEqual(code, EXIT_CODES[ExitCode.QUARANTINE_BLOCKED])

    def test_scan_missing_synthetic_flag_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = _write(tmp, "a.md", f"{MARKER}\ntext\n")
            code, _, err = run_cli(
                "quarantine", "scan", "--input", str(path),
                "--policy", str(EXAMPLE_POLICY),
                "--source-ref", "synthetic:cli",
            )
        self.assertEqual(code, EXIT_CODES[ExitCode.QUARANTINE_BLOCKED])
        self.assertIn("SYNTHETIC_CONFIRMATION_MISSING", err)

    def test_scan_bad_source_ref_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = _write(tmp, "a.md", f"{MARKER}\ntext\n")
            code, _, _ = run_cli(
                "quarantine", "scan", "--input", str(path),
                "--policy", str(EXAMPLE_POLICY),
                "--source-ref", "real-source", "--synthetic-test-only",
            )
        self.assertEqual(code, EXIT_CODES[ExitCode.QUARANTINE_BLOCKED])

    def test_scan_invalid_policy_exit_config_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = _write(tmp, "a.md", f"{MARKER}\ntext\n")
            bad = _write(tmp, "policy.toml", 'schema_version = "9.9"\n')
            code, _, _ = run_cli(
                "quarantine", "scan", "--input", str(path),
                "--policy", str(bad),
                "--source-ref", "synthetic:cli", "--synthetic-test-only",
            )
        self.assertEqual(code, EXIT_CODES[ExitCode.CONFIG_INVALID])


class TestQuarantineStageInspectCli(unittest.TestCase):
    """``quarantine stage`` und ``inspect`` (Test 46)."""

    def _stage(self, tmp: str, text: str) -> tuple[int, dict[str, object], Path]:
        path = _write(tmp, "a.md", text)
        store = Path(tmp) / "store"
        code, out, _ = run_cli(
            "quarantine", "stage", "--input", str(path),
            "--policy", str(EXAMPLE_POLICY),
            "--source-ref", "synthetic:cli", "--store", str(store),
            "--synthetic-test-only", "--json",
        )
        return code, json.loads(out), store

    def test_stage_ready_writes_object_and_record(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            code, record, store = self._stage(tmp, f"{MARKER}\ntext\n")
            objects = list((store / "objects").rglob("*.blob"))
            records = list((store / "records").glob("*.json"))
        self.assertEqual(code, EXIT_CODES[ExitCode.OK])
        self.assertEqual(len(objects), 1)
        self.assertEqual(len(records), 1)

    def test_stage_blocked_writes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = _write(tmp, "a.md", "no marker\n")
            store = Path(tmp) / "store"
            code, _, _ = run_cli(
                "quarantine", "stage", "--input", str(path),
                "--policy", str(EXAMPLE_POLICY),
                "--source-ref", "synthetic:cli", "--store", str(store),
                "--synthetic-test-only",
            )
            objects = list((store / "objects").rglob("*.blob"))
            records = list((store / "records").glob("*.json"))
        self.assertEqual(code, EXIT_CODES[ExitCode.QUARANTINE_BLOCKED])
        self.assertEqual(objects, [])
        self.assertEqual(records, [])

    def test_46_inspect_shows_minimized_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _, record, store = self._stage(tmp, f"{MARKER}\ntext\n")
            quarantine_id = str(record["quarantine_id"])
            code, out, _ = run_cli(
                "quarantine", "inspect", "--store", str(store),
                "--id", quarantine_id, "--json",
            )
            payload = json.loads(out)
        self.assertEqual(code, EXIT_CODES[ExitCode.OK])
        self.assertEqual(payload["quarantine_id"], quarantine_id)
        self.assertNotIn("a.md", out)
        self.assertNotIn(str(tmp), out)

    def test_inspect_missing_record_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            store.mkdir()
            code, _, err = run_cli(
                "quarantine", "inspect", "--store", str(store), "--id", "f" * 64
            )
        self.assertEqual(code, EXIT_CODES[ExitCode.QUARANTINE_BLOCKED])
        self.assertIn("RECORD_NOT_FOUND", err)


class TestQuarantineReleaseAndRun(unittest.TestCase):
    """Tests 47 und 51 — Freigabe verweigert, ``run`` bleibt fail-closed."""

    def test_47_release_always_refuses_and_changes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            store.mkdir()
            before = {p.name for p in store.iterdir()}
            code, out, err = run_cli(
                "quarantine", "release", "--store", str(store), "--id", "a" * 64
            )
            after = {p.name for p in store.iterdir()}
        self.assertEqual(code, EXIT_CODES[ExitCode.QUARANTINE_RELEASE_BLOCKED])
        self.assertIn("QUARANTINE_RELEASE_BLOCKED", err)
        self.assertEqual(out, "")
        self.assertEqual(before, after)

    def test_51_run_stays_fail_closed(self) -> None:
        config = REPO_ROOT / "config" / "runtime.example.toml"
        code, _, err = run_cli("run", "--config", str(config))
        self.assertEqual(code, EXIT_CODES[ExitCode.RUNTIME_START_BLOCKED])
        self.assertIn("RUNTIME_START_BLOCKED", err)


class TestNoPathOrContentLeak(unittest.TestCase):
    """Test 50 — kein CLI-Pfad gibt Eingabepfad oder Inhalt aus."""

    def test_50_scan_and_stage_leak_neither_path_nor_content(self) -> None:
        token = "SECRET-LOOKING-BODY-TOKEN-50"
        filename = "leak-probe-filename-50.md"
        with tempfile.TemporaryDirectory() as tmp:
            path = _write(tmp, filename, f"{MARKER}\npassword = {token}\n")
            store = Path(tmp) / "store"
            combined = ""
            for argv in (
                (
                    "quarantine", "scan", "--input", str(path),
                    "--policy", str(EXAMPLE_POLICY), "--source-ref", "synthetic:cli",
                    "--synthetic-test-only", "--json",
                ),
                (
                    "quarantine", "stage", "--input", str(path),
                    "--policy", str(EXAMPLE_POLICY), "--source-ref", "synthetic:cli",
                    "--store", str(store), "--synthetic-test-only", "--json",
                ),
            ):
                _, out, err = run_cli(*argv)
                combined += out + err
        self.assertNotIn(token, combined)
        self.assertNotIn(filename, combined)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
