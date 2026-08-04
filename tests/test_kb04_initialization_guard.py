"""Sicherheitsgrenzen der KB-04-Initialisierungsplanung (B2B-P).

Jeder Fall belegt, dass ein nicht eindeutig **neuer und leerer** Zielzustand
**fail-closed** endet und **niemals** einen anwendbaren Plan erzeugt.

Alle Zustaende sind virtuell injiziert — kein Test legt etwas an, veraendert
ein Recht oder benoetigt Administratorrechte. **Kein Plattformskip.**
"""

from __future__ import annotations

import ast
import pathlib
import unittest
from dataclasses import replace

from core.core_brain.enforcement import initialization as I
from core.core_brain.enforcement.contract import PathClass
from core.core_brain.errors import ReasonCode
from tests.kb04_init_fixtures import (
    BOUNDARY,
    DEFAULT_BINDINGS,
    FakeFilesystemAdapter,
    adapter_empty,
    adapter_initialized,
    device,
    directory,
    fifo,
    regular_file,
    request_for,
    socket_node,
    symlink,
)

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
ENFORCEMENT = REPO_ROOT / "core" / "core_brain" / "enforcement"
NEW_MODULES = ("initialization", "filesystem_adapter")


def reasons(plan: I.InitializationPlan) -> set[ReasonCode | None]:
    """Gibt die Reason Codes eines Plans zurueck."""
    return {f.reason for f in plan.findings}


def plan_with(adapter: FakeFilesystemAdapter, **kw: object) -> I.InitializationPlan:
    """Baut einen Plan mit dem angegebenen Adapter."""
    return I.build_initialization_plan(request_for(**kw), adapter)  # type: ignore[arg-type]


class TestNonEmptyTarget(unittest.TestCase):
    def _adapter(self, *entries: str, **nodes: object) -> FakeFilesystemAdapter:
        base = {
            "/vroot": directory("target"),
            "/vroot/target": directory(*entries),
        }
        base.update(nodes)  # type: ignore[arg-type]
        return FakeFilesystemAdapter(nodes=base)  # type: ignore[arg-type]

    def test_unknown_file_requires_migration(self) -> None:
        plan = plan_with(self._adapter("stray.txt"))
        self.assertIs(plan.status, I.InitializationStatus.MIGRATION_REQUIRED)
        self.assertIn(ReasonCode.KB04_MIGRATION_REQUIRED, reasons(plan))

    def test_hidden_file_requires_migration(self) -> None:
        plan = plan_with(self._adapter(".hidden"))
        self.assertIs(plan.status, I.InitializationStatus.MIGRATION_REQUIRED)

    def test_lock_artifact_requires_migration(self) -> None:
        plan = plan_with(self._adapter(".lock"))
        self.assertIs(plan.status, I.InitializationStatus.MIGRATION_REQUIRED)

    def test_metadata_artifact_requires_migration(self) -> None:
        plan = plan_with(self._adapter(".metadata"))
        self.assertIs(plan.status, I.InitializationStatus.MIGRATION_REQUIRED)

    def test_migration_plan_is_not_applicable(self) -> None:
        plan = plan_with(self._adapter("stray.txt"))
        self.assertFalse(plan.applicable)
        self.assertEqual(plan.operations, ())

    def test_partial_structure_is_reported(self) -> None:
        plan = plan_with(self._adapter("quarantine",
                                       **{"/vroot/target/quarantine": directory()}))
        self.assertIs(plan.status, I.InitializationStatus.PARTIAL)
        self.assertIn(ReasonCode.KB04_INIT_PARTIAL, reasons(plan))

    def test_partial_structure_is_not_applicable(self) -> None:
        plan = plan_with(self._adapter("quarantine",
                                       **{"/vroot/target/quarantine": directory()}))
        self.assertFalse(plan.applicable)

    def test_partial_plus_stray_is_migration_not_partial(self) -> None:
        plan = plan_with(
            self._adapter("quarantine", "stray",
                          **{"/vroot/target/quarantine": directory()})
        )
        self.assertIs(plan.status, I.InitializationStatus.MIGRATION_REQUIRED)

    def test_non_directory_entry_requires_repair(self) -> None:
        names = tuple(b.relative_path for b in DEFAULT_BINDINGS)
        nodes: dict[str, object] = {
            "/vroot": directory("target"),
            "/vroot/target": directory(*names),
        }
        for name in names:
            nodes[f"/vroot/target/{name}"] = directory()
        nodes["/vroot/target/derived"] = regular_file()
        plan = plan_with(FakeFilesystemAdapter(nodes=nodes))  # type: ignore[arg-type]
        self.assertIs(plan.status, I.InitializationStatus.REPAIR_REQUIRED)
        self.assertIn(ReasonCode.KB04_REPAIR_RT2_REQUIRED, reasons(plan))

    def test_repair_is_never_applicable(self) -> None:
        names = tuple(b.relative_path for b in DEFAULT_BINDINGS)
        nodes: dict[str, object] = {
            "/vroot": directory("target"),
            "/vroot/target": directory(*names),
        }
        for name in names:
            nodes[f"/vroot/target/{name}"] = directory()
        nodes["/vroot/target/derived"] = fifo()
        plan = plan_with(FakeFilesystemAdapter(nodes=nodes))  # type: ignore[arg-type]
        self.assertFalse(plan.applicable)


class TestObjectKindGuards(unittest.TestCase):
    def _target(self, node: object) -> FakeFilesystemAdapter:
        return FakeFilesystemAdapter(
            nodes={"/vroot": directory("target"), "/vroot/target": node}  # type: ignore[dict-item]
        )

    def test_symlink_root_is_blocked(self) -> None:
        plan = plan_with(self._target(symlink()))
        self.assertIs(plan.status, I.InitializationStatus.BLOCKED)
        self.assertIn(ReasonCode.KB04_LINK_SYMLINK_ESCAPE, reasons(plan))

    def test_regular_file_root_is_blocked(self) -> None:
        plan = plan_with(self._target(regular_file()))
        self.assertIn(ReasonCode.KB04_OBJECT_KIND_INVALID, reasons(plan))

    def test_fifo_root_is_blocked(self) -> None:
        plan = plan_with(self._target(fifo()))
        self.assertIn(ReasonCode.KB04_OBJECT_KIND_INVALID, reasons(plan))

    def test_socket_root_is_blocked(self) -> None:
        plan = plan_with(self._target(socket_node()))
        self.assertIn(ReasonCode.KB04_OBJECT_KIND_INVALID, reasons(plan))

    def test_device_root_is_blocked(self) -> None:
        plan = plan_with(self._target(device()))
        self.assertIn(ReasonCode.KB04_OBJECT_KIND_INVALID, reasons(plan))

    def test_hardlinked_regular_root_is_blocked(self) -> None:
        plan = plan_with(self._target(regular_file(nlink=2)))
        self.assertIs(plan.status, I.InitializationStatus.BLOCKED)

    def test_mountpoint_root_is_blocked(self) -> None:
        plan = plan_with(self._target(directory(is_mount=True)))
        self.assertIs(plan.status, I.InitializationStatus.BLOCKED)
        self.assertIn(ReasonCode.KB04_MOUNT_MODE_MISMATCH, reasons(plan))

    def test_none_of_these_is_applicable(self) -> None:
        for node in (symlink(), regular_file(), fifo(), socket_node(),
                     device(), directory(is_mount=True)):
            with self.subTest(kind=node.kind):
                self.assertFalse(plan_with(self._target(node)).applicable)


class TestBoundaryGuards(unittest.TestCase):
    def test_boundary_symlink_is_blocked(self) -> None:
        adapter = FakeFilesystemAdapter(
            nodes={"/vroot": symlink(), "/vroot/target": directory()}
        )
        plan = plan_with(adapter)
        self.assertIn(ReasonCode.KB04_LINK_SYMLINK_ESCAPE, reasons(plan))

    def test_boundary_is_not_a_directory(self) -> None:
        adapter = FakeFilesystemAdapter(
            nodes={"/vroot": regular_file(), "/vroot/target": directory()}
        )
        plan = plan_with(adapter)
        self.assertIn(ReasonCode.KB04_OBJECT_KIND_INVALID, reasons(plan))

    def test_missing_boundary_is_blocked(self) -> None:
        adapter = FakeFilesystemAdapter(nodes={"/vroot/target": directory()})
        plan = plan_with(adapter)
        self.assertIs(plan.status, I.InitializationStatus.BLOCKED)
        self.assertIn(ReasonCode.KB04_PATH_OUTSIDE_ROOT, reasons(plan))

    def test_target_outside_boundary_is_blocked(self) -> None:
        adapter = FakeFilesystemAdapter(
            nodes={"/vroot": directory(), "/elsewhere/target": directory()}
        )
        plan = plan_with(
            adapter, target_root=pathlib.Path("/elsewhere/target")
        )
        self.assertIs(plan.status, I.InitializationStatus.BLOCKED)
        self.assertIn(ReasonCode.KB04_PATH_OUTSIDE_ROOT, reasons(plan))

    def test_parent_symlink_is_blocked(self) -> None:
        adapter = FakeFilesystemAdapter(
            nodes={
                "/vroot": directory("mid"),
                "/vroot/mid": symlink(),
                "/vroot/mid/target": directory(),
            }
        )
        plan = plan_with(
            adapter, target_root=pathlib.Path("/vroot/mid/target")
        )
        self.assertIn(ReasonCode.KB04_LINK_SYMLINK_ESCAPE, reasons(plan))

    def test_target_inside_repository_is_blocked(self) -> None:
        inside = REPO_ROOT / "core"
        adapter = FakeFilesystemAdapter(
            nodes={REPO_ROOT.as_posix(): directory("core"),
                   inside.as_posix(): directory()}
        )
        plan = plan_with(
            adapter, boundary_root=REPO_ROOT, target_root=inside
        )
        self.assertIs(plan.status, I.InitializationStatus.BLOCKED)
        self.assertIn(ReasonCode.KB04_PATH_OUTSIDE_ROOT, reasons(plan))


class TestPathBindingGuards(unittest.TestCase):
    def test_parent_traversal_is_rejected(self) -> None:
        plan = plan_with(
            adapter_empty(),
            bindings=(I.TargetPathBinding(PathClass.PC_03, "../escape"),),
        )
        self.assertIs(plan.status, I.InitializationStatus.BLOCKED)
        self.assertIn(ReasonCode.KB04_PATH_OUTSIDE_ROOT, reasons(plan))

    def test_absolute_binding_path_is_rejected(self) -> None:
        plan = plan_with(
            adapter_empty(),
            bindings=(I.TargetPathBinding(PathClass.PC_03, "/absolute"),),
        )
        self.assertIn(ReasonCode.KB04_PATH_OUTSIDE_ROOT, reasons(plan))

    def test_drive_style_binding_path_is_rejected(self) -> None:
        plan = plan_with(
            adapter_empty(),
            bindings=(I.TargetPathBinding(PathClass.PC_03, "C:/data"),),
        )
        self.assertIn(ReasonCode.KB04_PATH_OUTSIDE_ROOT, reasons(plan))

    def test_empty_binding_path_is_rejected(self) -> None:
        plan = plan_with(
            adapter_empty(),
            bindings=(I.TargetPathBinding(PathClass.PC_03, "   "),),
        )
        self.assertIn(ReasonCode.KB04_CONTRACT_INVALID, reasons(plan))

    def test_duplicate_path_class_is_rejected(self) -> None:
        plan = plan_with(
            adapter_empty(),
            bindings=(
                I.TargetPathBinding(PathClass.PC_03, "a"),
                I.TargetPathBinding(PathClass.PC_03, "b"),
            ),
        )
        self.assertIs(plan.status, I.InitializationStatus.BLOCKED)
        self.assertIn(ReasonCode.KB04_CONTRACT_INVALID, reasons(plan))

    def test_duplicate_target_path_is_rejected(self) -> None:
        plan = plan_with(
            adapter_empty(),
            bindings=(
                I.TargetPathBinding(PathClass.PC_02, "same"),
                I.TargetPathBinding(PathClass.PC_03, "same"),
            ),
        )
        self.assertIn(ReasonCode.KB04_CONTRACT_INVALID, reasons(plan))

    def test_unclassified_path_class_is_rejected(self) -> None:
        plan = plan_with(
            adapter_empty(),
            bindings=(I.TargetPathBinding(PathClass.PC_11, "unknown"),),
        )
        self.assertIn(ReasonCode.KB04_PATHCLASS_UNKNOWN, reasons(plan))


class TestObservabilityGuards(unittest.TestCase):
    def test_permission_error_is_indeterminate(self) -> None:
        adapter = FakeFilesystemAdapter(
            nodes={"/vroot": directory("target")},
            errors={"/vroot/target": PermissionError("denied")},
        )
        plan = plan_with(adapter)
        self.assertIs(plan.status, I.InitializationStatus.INDETERMINATE)
        self.assertIn(ReasonCode.KB04_STATE_INDETERMINATE, reasons(plan))

    def test_permission_error_is_not_applicable(self) -> None:
        adapter = FakeFilesystemAdapter(
            nodes={"/vroot": directory("target")},
            errors={"/vroot/target": PermissionError("denied")},
        )
        self.assertFalse(plan_with(adapter).applicable)

    def test_boundary_permission_error_is_indeterminate(self) -> None:
        adapter = FakeFilesystemAdapter(
            nodes={"/vroot/target": directory()},
            errors={"/vroot": PermissionError("denied")},
        )
        self.assertIs(
            plan_with(adapter).status, I.InitializationStatus.INDETERMINATE
        )

    def test_unsupported_platform_is_indeterminate(self) -> None:
        adapter = adapter_empty(posix_semantics=False)
        plan = plan_with(adapter)
        self.assertIs(plan.status, I.InitializationStatus.INDETERMINATE)
        self.assertIn(ReasonCode.KB04_PLATFORM_UNSUPPORTED, reasons(plan))

    def test_unsupported_platform_is_never_applicable(self) -> None:
        for factory in (adapter_empty, adapter_initialized):
            with self.subTest(factory=factory.__name__):
                plan = plan_with(factory(posix_semantics=False))
                self.assertFalse(plan.applicable)

    def test_unsupported_platform_never_reports_success(self) -> None:
        assessment = I.verify_initialized(
            request_for(), adapter_initialized(posix_semantics=False)
        )
        self.assertFalse(assessment.conform)


class TestRaceGuards(unittest.TestCase):
    def test_artifact_appears_between_observations(self) -> None:
        # Ein Durchgang von assess_target beobachtet das Ziel dreimal
        # (lstat, is_mount, iterdir). Die ersten drei Werte bilden den ersten
        # Durchgang ab, die folgenden den zweiten.
        adapter = adapter_empty()
        adapter.race["/vroot/target"] = [
            directory(),
            directory(),
            directory(),
            directory("stray"),
            directory("stray"),
            directory("stray"),
        ]
        plan = plan_with(adapter)
        self.assertIs(plan.status, I.InitializationStatus.INDETERMINATE)
        self.assertIn(ReasonCode.KB04_STATE_INDETERMINATE, reasons(plan))

    def test_root_replaced_by_symlink_between_observations(self) -> None:
        adapter = adapter_empty()
        adapter.race["/vroot/target"] = [directory(), directory(), symlink()]
        plan = plan_with(adapter)
        self.assertIs(plan.status, I.InitializationStatus.INDETERMINATE)

    def test_root_becomes_mountpoint_between_observations(self) -> None:
        adapter = adapter_empty()
        adapter.race["/vroot/target"] = [
            directory(),
            directory(),
            directory(),
            directory(is_mount=True),
            directory(is_mount=True),
        ]
        self.assertIs(
            plan_with(adapter).status, I.InitializationStatus.INDETERMINATE
        )

    def test_object_kind_changes_between_observations(self) -> None:
        adapter = adapter_empty()
        adapter.race["/vroot/target"] = [
            directory(), directory(), regular_file()
        ]
        self.assertIs(
            plan_with(adapter).status, I.InitializationStatus.INDETERMINATE
        )

    def test_target_vanishes_between_observations(self) -> None:
        adapter = adapter_empty()
        adapter.race["/vroot/target"] = [directory(), directory(), None]
        self.assertIs(
            plan_with(adapter).status, I.InitializationStatus.INDETERMINATE
        )

    def test_race_result_is_never_applicable(self) -> None:
        adapter = adapter_empty()
        adapter.race["/vroot/target"] = [
            directory(), directory(), directory(),
            directory("stray"), directory("stray"), directory("stray"),
        ]
        self.assertFalse(plan_with(adapter).applicable)

    def test_stable_state_survives_revalidation(self) -> None:
        plan = plan_with(adapter_empty())
        self.assertIs(plan.status, I.InitializationStatus.PLANNED)

    def test_revalidation_observes_more_than_once(self) -> None:
        adapter = adapter_empty()
        I.build_initialization_plan(request_for(), adapter)
        self.assertGreater(adapter.observations, 2)


class TestNoMutationAnywhere(unittest.TestCase):
    def _sources(self) -> dict[str, str]:
        return {
            name: (ENFORCEMENT / f"{name}.py").read_text(encoding="utf-8")
            for name in NEW_MODULES
        }

    def test_no_mutating_call_in_new_modules(self) -> None:
        forbidden = {
            "mkdir", "makedirs", "open", "touch", "write", "write_text",
            "write_bytes", "chmod", "chown", "unlink", "remove", "rmdir",
            "rename", "replace", "fsync", "system", "run", "Popen",
            "symlink_to", "hardlink_to", "rmtree", "copy",
        }
        for name in NEW_MODULES:
            tree = ast.parse((ENFORCEMENT / f"{name}.py").read_text(encoding="utf-8"))
            calls = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    fn = node.func
                    called = (
                        fn.attr if isinstance(fn, ast.Attribute)
                        else fn.id if isinstance(fn, ast.Name) else None
                    )
                    if called in forbidden:
                        calls.append((name, node.lineno, called))
            with self.subTest(module=name):
                self.assertEqual(calls, [])

    def test_no_subprocess_or_os_system_import(self) -> None:
        for name, src in self._sources().items():
            with self.subTest(module=name):
                self.assertNotIn("import subprocess", src)
                self.assertNotIn("os.system", src)

    def test_adapter_protocol_has_no_mutating_method(self) -> None:
        from core.core_brain.enforcement.filesystem_adapter import (
            FilesystemAdapter,
            RealFilesystemAdapter,
        )

        forbidden = {
            "mkdir", "makedirs", "open", "open_exclusive", "touch", "write",
            "chmod", "chown", "unlink", "remove", "rmdir", "rename",
            "replace", "fsync",
        }
        for cls in (FilesystemAdapter, RealFilesystemAdapter):
            with self.subTest(cls=cls.__name__):
                self.assertEqual(forbidden & set(dir(cls)), set())

    def test_adapter_only_offers_read_operations(self) -> None:
        from core.core_brain.enforcement.filesystem_adapter import (
            RealFilesystemAdapter,
        )

        public = {n for n in dir(RealFilesystemAdapter) if not n.startswith("_")}
        self.assertEqual(
            public,
            {"exists", "lstat", "stat", "iterdir", "resolve", "is_mount",
             "posix_semantics"},
        )

    def test_no_apply_symbol_in_sources(self) -> None:
        for name, src in self._sources().items():
            for token in ("def apply_", "def execute_", "def initialize_target",
                          "def create_target"):
                with self.subTest(module=name, token=token):
                    self.assertNotIn(token, src)

    def test_planning_creates_nothing_on_disk(self) -> None:
        before = {p for p in REPO_ROOT.rglob("*") if p.is_file()}
        plan_with(adapter_empty())
        plan_with(adapter_initialized())
        after = {p for p in REPO_ROOT.rglob("*") if p.is_file()}
        self.assertEqual(before, after)


class TestImportIsolation(unittest.TestCase):
    def _imports(self, path: pathlib.Path) -> set[str]:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        found: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                found.add((node.module or "").split(".")[-1])
                for alias in node.names:
                    found.add(alias.name)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    found.add(alias.name.split(".")[-1])
        return found

    def test_no_existing_production_module_imports_the_new_ones(self) -> None:
        for path in sorted((REPO_ROOT / "core").rglob("*.py")):
            if path.stem in NEW_MODULES:
                continue
            with self.subTest(module=path.name):
                self.assertEqual(self._imports(path) & set(NEW_MODULES), set())

    def test_enforcement_init_is_unchanged_and_has_no_reexport(self) -> None:
        src = (ENFORCEMENT / "__init__.py").read_text(encoding="utf-8")
        for name in NEW_MODULES:
            with self.subTest(name=name):
                self.assertNotIn(name, src)

    def test_core_brain_init_has_no_reexport(self) -> None:
        src = (REPO_ROOT / "core" / "core_brain" / "__init__.py").read_text(
            encoding="utf-8"
        )
        for name in NEW_MODULES:
            with self.subTest(name=name):
                self.assertNotIn(name, src)

    def test_new_modules_import_only_permitted_sources(self) -> None:
        import sys

        allowed_local = {
            "errors", "aggregate", "contract", "binding", "paths",
            "validator", "filesystem_adapter", "initialization",
        }
        for name in NEW_MODULES:
            tree = ast.parse((ENFORCEMENT / f"{name}.py").read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom) and node.level:
                    base = (node.module or "").split(".")[-1]
                    with self.subTest(module=name, imported=base):
                        self.assertIn(base, allowed_local)
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        root = alias.name.split(".")[0]
                        with self.subTest(module=name, imported=root):
                            self.assertIn(root, sys.stdlib_module_names)

    def test_importing_new_modules_has_no_side_effect(self) -> None:
        import contextlib
        import importlib
        import io

        before = {p for p in REPO_ROOT.rglob("*") if p.is_file()}
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            for name in NEW_MODULES:
                importlib.import_module(
                    f"core.core_brain.enforcement.{name}"
                )
        after = {p for p in REPO_ROOT.rglob("*") if p.is_file()}
        self.assertEqual(out.getvalue(), "")
        self.assertEqual(err.getvalue(), "")
        self.assertEqual(before, after)


class TestReasonCodeActivation(unittest.TestCase):
    def test_all_twentyfour_contract_codes_exist(self) -> None:
        codes = {c.value for c in ReasonCode if c.value.startswith("KB04-")}
        self.assertEqual(len(codes), 24)

    def test_three_previously_reserved_codes_exist(self) -> None:
        for code in ("KB04-PLATFORM-UNSUPPORTED", "KB04-MIGRATION-REQUIRED",
                     "KB04-REPAIR-RT2-REQUIRED"):
            with self.subTest(code=code):
                self.assertIn(code, {c.value for c in ReasonCode})

    def test_exit_codes_fifteen_and_sixteen_stay_unimplemented(self) -> None:
        from core.core_brain.errors import EXIT_CODES, ExitCode

        self.assertNotIn(15, set(EXIT_CODES.values()))
        self.assertNotIn(16, set(EXIT_CODES.values()))
        names = {e.value for e in ExitCode}
        self.assertNotIn("FILESYSTEM_ENFORCEMENT_BLOCKED", names)
        self.assertNotIn("FILESYSTEM_MIGRATION_REQUIRED", names)

    def test_normal_deviations_are_findings_not_exceptions(self) -> None:
        adapter = FakeFilesystemAdapter(
            nodes={"/vroot": directory("target"),
                   "/vroot/target": directory("stray")}
        )
        plan = plan_with(adapter)  # darf nicht erheben
        self.assertGreater(len(plan.findings), 0)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
