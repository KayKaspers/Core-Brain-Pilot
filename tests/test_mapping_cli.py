"""Tests der ``source-mapping``-CLI (CBP-WP-015, Faelle 91-106).

Exitcode 0 ausschliesslich bei ``VALID_DRAFT``; ``activation-check`` verweigert
immer mit Exitcode 13. Kein CLI-Pfad leakt Pfade oder Inhalte, keiner veraendert
die Registry.
"""

from __future__ import annotations

import hashlib
import io
import json
import socket
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from core.core_brain.cli import main
from core.core_brain.errors import EXIT_CODES, ExitCode
from core.core_brain.registry.models import RECORD_FIELDS

REPO_ROOT = Path(__file__).resolve().parent.parent
POLICY = REPO_ROOT / "config" / "source_mapping_validation_policy.example.toml"
SOURCE_ID = "src-0123456789abcdef01234567"
CONTENT_MARKER = "synthetic-notes-content-marker"


def valid_draft() -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "mapping_id": "MAP-EXAMPLE-0001",
        "slot_id": "PS-02",
        "mapping_name": "Beispiel Markdown Root",
        "source_boundary_type": "markdown-root",
        "deployment_profile": "B",
        "operator_reference": "role-operator-placeholder",
        "location_reference": "synthetic-placeholder-markdown-root",
        "location_reference_type": "local-directory",
        "collection": "example-domain-alpha",
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
        "notes": CONTENT_MARKER,
    }


def record_dict() -> dict[str, object]:
    data = {key: "x" for key in RECORD_FIELDS}
    data.update(
        {
            "record_schema_version": "1.0",
            "source_id": SOURCE_ID,
            "namespace": "synthetic-ns",
            "source_key": "notes-alpha",
            "display_name": "Synthetic Notes",
            "collection_key": "example-domain-alpha",
            "domain_key": "example-domain",
            "source_kind": "markdown",
            "data_class": "internal",
            "ai_eligibility": "restricted",
            "owner_role": "operator",
            "source_reference": "synthetic:notes-ref-marker",
            "definition_sha256": "0" * 64,
            "policy_sha256": "0" * 64,
            "lifecycle_state": "REGISTERED_DISABLED",
            "registered_at": "2026-07-27T00:00:00Z",
            "implementation_version": "0.1.0.dev0",
        }
    )
    return data


def run_cli(*argv: str) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    code = main(list(argv), out=out, err=err)
    return code, out.getvalue(), err.getvalue()


def _hash_tree(root: Path) -> list[tuple[str, str]]:
    result: list[tuple[str, str]] = []
    for path in sorted(root.rglob("*")):
        if path.is_file():
            result.append(
                (
                    path.relative_to(root).as_posix(),
                    hashlib.sha256(path.read_bytes()).hexdigest(),
                )
            )
    return result


class _Fixture:
    """Erzeugt eine synthetische temporaere Registry und einen Draft."""

    def __init__(self, tmp: str, draft: dict[str, object]) -> None:
        self.root = Path(tmp) / "registry"
        (self.root / "records").mkdir(parents=True)
        (self.root / "records" / f"{SOURCE_ID}.json").write_text(
            json.dumps(record_dict(), sort_keys=True, ensure_ascii=False, indent=2)
            + "\n",
            encoding="utf-8",
        )
        self.draft = Path(tmp) / "draft.json"
        self.draft.write_text(json.dumps(draft), encoding="utf-8")

    def validate_args(self, *, synthetic: bool = True, as_json: bool = False):
        argv = [
            "source-mapping", "validate-draft", "--draft", str(self.draft),
            "--policy", str(POLICY), "--registry", str(self.root),
            "--source-id", SOURCE_ID,
        ]
        if synthetic:
            argv.append("--synthetic-test-only")
        if as_json:
            argv.append("--json")
        return argv

    def activation_args(self, *, synthetic: bool = True):
        argv = [
            "source-mapping", "activation-check", "--draft", str(self.draft),
            "--policy", str(POLICY), "--registry", str(self.root),
            "--source-id", SOURCE_ID, "--synthetic-test-only",
        ]
        if not synthetic:
            argv.remove("--synthetic-test-only")
        return argv


class TestMappingCli(unittest.TestCase):
    def test_91_validate_draft_success(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fx = _Fixture(tmp, valid_draft())
            code, out, _ = run_cli(*fx.validate_args())
        self.assertEqual(code, EXIT_CODES[ExitCode.OK])
        self.assertIn("VALID_DRAFT", out)

    def test_92_validate_draft_blocks_invalid_draft(self) -> None:
        draft = valid_draft()
        draft["enabled"] = True
        with tempfile.TemporaryDirectory() as tmp:
            fx = _Fixture(tmp, draft)
            code, out, _ = run_cli(*fx.validate_args())
        self.assertEqual(code, EXIT_CODES[ExitCode.SOURCE_MAPPING_DRAFT_BLOCKED])
        self.assertIn("BLOCKED", out)

    def test_93_validate_draft_without_synthetic_flag_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fx = _Fixture(tmp, valid_draft())
            code, out, _ = run_cli(*fx.validate_args(synthetic=False))
        self.assertEqual(code, EXIT_CODES[ExitCode.SOURCE_MAPPING_DRAFT_BLOCKED])
        self.assertIn("MAP-SYNTHETIC-CONFIRMATION-MISSING", out)

    def test_94_validate_draft_json_is_canonical(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fx = _Fixture(tmp, valid_draft())
            code, out, _ = run_cli(*fx.validate_args(as_json=True))
        self.assertEqual(code, EXIT_CODES[ExitCode.OK])
        parsed = json.loads(out)
        self.assertEqual(out.strip(), json.dumps(parsed, indent=2, sort_keys=True))
        self.assertEqual(parsed["validation_status"], "VALID_DRAFT")
        self.assertEqual(parsed["canonical_contract_field_count"], 31)

    def test_95_activation_check_always_refuses(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fx = _Fixture(tmp, valid_draft())  # ansonsten gueltiger Draft
            code, _, err = run_cli(*fx.activation_args())
        self.assertEqual(
            code, EXIT_CODES[ExitCode.SOURCE_MAPPING_ACTIVATION_BLOCKED]
        )
        self.assertIn("MAPPING_ACTIVATION_ALWAYS_BLOCKED", err)

    def test_96_activation_check_writes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fx = _Fixture(tmp, valid_draft())
            before_reg = _hash_tree(fx.root)
            before_tmp = {p for p in Path(tmp).rglob("*")}
            run_cli(*fx.activation_args())
            self.assertEqual(_hash_tree(fx.root), before_reg)
            self.assertEqual({p for p in Path(tmp).rglob("*")}, before_tmp)

    def test_97_98_no_cli_path_leaks_paths_or_content(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fx = _Fixture(tmp, valid_draft())
            combined = ""
            for argv in (
                fx.validate_args(),
                fx.validate_args(as_json=True),
                fx.activation_args(),
            ):
                _, out, err = run_cli(*argv)
                combined += out + err
        self.assertNotIn(str(fx.root), combined)  # 97 kein Registry-Pfad
        self.assertNotIn(str(fx.draft), combined)  # 97 kein Eingabepfad
        self.assertNotIn(CONTENT_MARKER, combined)  # 98 kein Inhalt
        self.assertNotIn("synthetic-placeholder", combined)  # 98 kein Locator
        self.assertNotIn("synthetic:notes-ref-marker", combined)  # keine Source Ref

    def test_99_no_cli_path_modifies_registry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fx = _Fixture(tmp, valid_draft())
            before = _hash_tree(fx.root)
            run_cli(*fx.validate_args())
            run_cli(*fx.validate_args(as_json=True))
            run_cli(*fx.activation_args())
            after = _hash_tree(fx.root)
        self.assertEqual(before, after)

    def test_100_unknown_registry_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            draft = Path(tmp) / "draft.json"
            draft.write_text(json.dumps(valid_draft()), encoding="utf-8")
            missing = Path(tmp) / "does-not-exist"
            code, out, _ = run_cli(
                "source-mapping", "validate-draft", "--draft", str(draft),
                "--policy", str(POLICY), "--registry", str(missing),
                "--source-id", SOURCE_ID, "--synthetic-test-only",
            )
        self.assertEqual(code, EXIT_CODES[ExitCode.SOURCE_MAPPING_DRAFT_BLOCKED])
        self.assertIn("MAP-REGISTRY-NOT-FOUND", out)

    def test_101_run_stays_exit_four(self) -> None:
        code, _, _ = run_cli(
            "run", "--config", str(REPO_ROOT / "config" / "runtime.example.toml")
        )
        self.assertEqual(code, EXIT_CODES[ExitCode.RUNTIME_START_BLOCKED])

    def test_102_quarantine_cli_unchanged(self) -> None:
        code, _, err = run_cli(
            "quarantine", "release", "--store", "unused", "--id", "q-unused"
        )
        self.assertEqual(code, EXIT_CODES[ExitCode.QUARANTINE_RELEASE_BLOCKED])
        self.assertIn("QUARANTINE_RELEASE_ALWAYS_BLOCKED", err)

    def test_103_source_registry_cli_unchanged(self) -> None:
        code, _, err = run_cli(
            "source-registry", "activate", "--registry", "unused", "--id", SOURCE_ID
        )
        self.assertEqual(
            code, EXIT_CODES[ExitCode.SOURCE_REGISTRY_ACTIVATION_BLOCKED]
        )
        self.assertIn("REGISTRY_ACTIVATION_ALWAYS_BLOCKED", err)

    def test_104_network_guard_covers_both_mapping_commands(self) -> None:
        def _deny(*_a: object, **_k: object) -> object:
            raise AssertionError("network attempt in mapping CLI")

        with tempfile.TemporaryDirectory() as tmp:
            fx = _Fixture(tmp, valid_draft())
            for argv in (fx.validate_args(), fx.activation_args()):
                with self.subTest(cmd=argv[1]):
                    out, err = io.StringIO(), io.StringIO()
                    with (
                        mock.patch.object(socket, "create_connection", _deny),
                        mock.patch.object(socket, "getaddrinfo", _deny),
                        mock.patch.object(socket.socket, "connect", _deny),
                        mock.patch.object(socket.socket, "connect_ex", _deny),
                    ):
                        main(list(argv), out=out, err=err)

    def test_106_no_file_outside_temp_directories(self) -> None:
        def _snapshot() -> set[Path]:
            return set((REPO_ROOT / "core").rglob("*")) | set(
                (REPO_ROOT / "config").rglob("*")
            )

        before = _snapshot()
        with tempfile.TemporaryDirectory() as tmp:
            fx = _Fixture(tmp, valid_draft())
            run_cli(*fx.validate_args())
            run_cli(*fx.activation_args())
        after = _snapshot()
        self.assertEqual(before, after)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
