"""Tests der KB-04-Initialisierungsplanung (CBP-WP-022, Teilphase B2B-P).

**Plan-only.** Kein Test fuehrt eine Operation aus, legt eine Datei an oder
veraendert ein Recht. Alle Zustaende sind virtuell und injiziert.
"""

from __future__ import annotations

import hashlib
import pathlib
import unittest
from dataclasses import replace

from core.core_brain.enforcement import contract as c
from core.core_brain.enforcement import initialization as I
from core.core_brain.enforcement.aggregate import canonical_json_bytes
from core.core_brain.enforcement.contract import Actor, PathClass
from core.core_brain.errors import ReasonCode
from tests.kb04_init_fixtures import (
    DEFAULT_BINDINGS,
    adapter_absent,
    adapter_empty,
    adapter_initialized,
    binding,
    directory,
    request_for,
)

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]


def reasons(plan: I.InitializationPlan) -> set[ReasonCode | None]:
    """Gibt die Reason Codes eines Plans zurueck."""
    return {f.reason for f in plan.findings}


class TestNewAbsent(unittest.TestCase):
    def test_absent_target_is_planned(self) -> None:
        plan = I.build_initialization_plan(request_for(), adapter_absent())
        self.assertIs(plan.status, I.InitializationStatus.PLANNED)

    def test_absent_target_is_applicable(self) -> None:
        plan = I.build_initialization_plan(request_for(), adapter_absent())
        self.assertTrue(plan.applicable)

    def test_absent_state_is_new_absent(self) -> None:
        assessment = I.assess_target(request_for(), adapter_absent())
        self.assertIs(assessment.state, I.TargetState.NEW_ABSENT)

    def test_absent_state_has_no_findings(self) -> None:
        assessment = I.assess_target(request_for(), adapter_absent())
        self.assertEqual(assessment.findings, ())


class TestNewEmpty(unittest.TestCase):
    def test_empty_target_is_planned(self) -> None:
        plan = I.build_initialization_plan(request_for(), adapter_empty())
        self.assertIs(plan.status, I.InitializationStatus.PLANNED)

    def test_empty_state_is_new_empty(self) -> None:
        assessment = I.assess_target(request_for(), adapter_empty())
        self.assertIs(assessment.state, I.TargetState.NEW_EMPTY)

    def test_empty_target_yields_operations(self) -> None:
        plan = I.build_initialization_plan(request_for(), adapter_empty())
        self.assertGreater(len(plan.operations), 0)


class TestPlanShape(unittest.TestCase):
    def setUp(self) -> None:
        self.plan = I.build_initialization_plan(request_for(), adapter_empty())

    def test_first_operation_creates_root(self) -> None:
        self.assertIs(self.plan.operations[0].kind, I.OperationKind.CREATE_ROOT)

    def test_last_operation_is_post_validate(self) -> None:
        self.assertIs(
            self.plan.operations[-1].kind, I.OperationKind.POST_VALIDATE
        )

    def test_only_three_operation_kinds_exist(self) -> None:
        self.assertEqual(
            [k.value for k in I.OperationKind],
            ["CREATE_ROOT", "CREATE_CLASS_DIRECTORY", "POST_VALIDATE"],
        )

    def test_plan_uses_only_declared_kinds(self) -> None:
        kinds = {o.kind for o in self.plan.operations}
        self.assertTrue(kinds <= set(I.OperationKind))

    def test_no_mutating_operation_kind_declared(self) -> None:
        forbidden = {"CHMOD", "CHOWN", "DELETE", "REPLACE", "CLEANUP",
                     "MIGRATE", "REPAIR", "ROLLBACK"}
        self.assertEqual(
            forbidden & {k.value for k in I.OperationKind}, set()
        )

    def test_sequence_is_gapless_and_ascending(self) -> None:
        seqs = [o.sequence for o in self.plan.operations]
        self.assertEqual(seqs, list(range(len(seqs))))

    def test_operations_are_sorted(self) -> None:
        self.assertEqual(list(self.plan.operations), sorted(self.plan.operations))

    def test_one_directory_operation_per_binding(self) -> None:
        creates = [
            o
            for o in self.plan.operations
            if o.kind is I.OperationKind.CREATE_CLASS_DIRECTORY
        ]
        self.assertEqual(len(creates), len(DEFAULT_BINDINGS))

    def test_modes_come_from_profile_spec(self) -> None:
        for op in self.plan.operations:
            if op.kind is not I.OperationKind.CREATE_CLASS_DIRECTORY:
                continue
            with self.subTest(path_class=str(op.path_class)):
                spec = c.path_class_spec(PathClass(str(op.path_class)))
                self.assertIsNotNone(spec.profile)
                self.assertEqual(
                    op.expected_mode, c.profile_spec(spec.profile).dir_mode
                )

    def test_no_planned_mode_is_world_writable(self) -> None:
        for op in self.plan.operations:
            with self.subTest(sequence=op.sequence):
                if op.expected_mode is not None:
                    self.assertEqual(op.expected_mode & 0o002, 0)

    def test_owner_roles_are_abstract(self) -> None:
        roles = {o.owner_role for o in self.plan.operations if o.owner_role}
        for role in roles:
            with self.subTest(role=role):
                self.assertIn(role, {r.value for r in c.ServiceRole})

    def test_group_roles_are_abstract_or_absent(self) -> None:
        for op in self.plan.operations:
            with self.subTest(sequence=op.sequence):
                if op.group_role is not None:
                    self.assertIn(
                        op.group_role, {r.value for r in c.ServiceRole}
                    )

    def test_relative_paths_only(self) -> None:
        for op in self.plan.operations:
            with self.subTest(sequence=op.sequence):
                self.assertFalse(op.relative_path.startswith("/"))
                self.assertNotIn(":", op.relative_path)
                self.assertNotIn("\\", op.relative_path)

    def test_operations_carry_pre_and_postconditions(self) -> None:
        for op in self.plan.operations:
            with self.subTest(sequence=op.sequence):
                self.assertIsInstance(op.preconditions, tuple)
                self.assertIsInstance(op.postconditions, tuple)
                self.assertTrue(op.preconditions)
                self.assertTrue(op.postconditions)

    def test_object_kind_is_directory(self) -> None:
        for op in self.plan.operations:
            with self.subTest(sequence=op.sequence):
                self.assertEqual(str(op.object_kind), "DIRECTORY")


class TestDeterminism(unittest.TestCase):
    def test_digest_is_hex64(self) -> None:
        self.assertRegex(request_for().digest(), r"\A[0-9a-f]{64}\Z")

    def test_digest_is_stable(self) -> None:
        first = request_for().digest()
        self.assertEqual(first, request_for().digest())

    def test_digest_ignores_absolute_paths(self) -> None:
        a = request_for()
        b = replace(
            a,
            boundary_root=pathlib.Path("/other"),
            target_root=pathlib.Path("/other/t"),
        )
        self.assertEqual(a.digest(), b.digest())

    def test_digest_changes_with_bindings(self) -> None:
        a = request_for()
        b = replace(a, path_bindings=DEFAULT_BINDINGS[:1])
        self.assertNotEqual(a.digest(), b.digest())

    def test_same_input_yields_byte_identical_plan(self) -> None:
        first = I.build_initialization_plan(request_for(), adapter_empty())
        second = I.build_initialization_plan(request_for(), adapter_empty())
        self.assertEqual(
            canonical_json_bytes(first.to_dict()),
            canonical_json_bytes(second.to_dict()),
        )

    def test_plan_hash_is_reproducible(self) -> None:
        plan = I.build_initialization_plan(request_for(), adapter_empty())
        digest = hashlib.sha256(canonical_json_bytes(plan.to_dict())).hexdigest()
        again = I.build_initialization_plan(request_for(), adapter_empty())
        self.assertEqual(
            digest, hashlib.sha256(canonical_json_bytes(again.to_dict())).hexdigest()
        )

    def test_binding_order_does_not_matter(self) -> None:
        forward = I.build_initialization_plan(request_for(), adapter_empty())
        reverse = I.build_initialization_plan(
            request_for(bindings=tuple(reversed(DEFAULT_BINDINGS))),
            adapter_empty(),
        )
        self.assertEqual(forward.to_dict(), reverse.to_dict())


class TestStableOutput(unittest.TestCase):
    def _payload(self) -> str:
        plan = I.build_initialization_plan(request_for(), adapter_empty())
        return canonical_json_bytes(plan.to_dict()).decode("utf-8")

    def test_no_absolute_posix_path_in_output(self) -> None:
        self.assertNotIn('"/vroot', self._payload())

    def test_no_drive_letter_in_output(self) -> None:
        payload = self._payload()
        for token in (":\\", ":/"):
            with self.subTest(token=token):
                self.assertNotIn(token, payload)

    def test_no_repository_path_in_output(self) -> None:
        self.assertNotIn(REPO_ROOT.name, self._payload())

    def test_target_ref_is_used(self) -> None:
        self.assertIn("<synthetic-target>", self._payload())

    def test_request_stable_mapping_has_no_paths(self) -> None:
        mapping = request_for().stable_mapping()
        self.assertNotIn("boundary_root", mapping)
        self.assertNotIn("target_root", mapping)

    def test_plan_to_dict_keys_are_stable(self) -> None:
        plan = I.build_initialization_plan(request_for(), adapter_empty())
        self.assertEqual(
            sorted(plan.to_dict()),
            [
                "applicable",
                "findings",
                "operations",
                "request_digest",
                "status",
                "target_ref",
            ],
        )

    def test_operation_to_dict_keys_are_stable(self) -> None:
        plan = I.build_initialization_plan(request_for(), adapter_empty())
        self.assertEqual(
            sorted(plan.operations[0].to_dict()),
            [
                "expected_mode",
                "group_role",
                "kind",
                "object_kind",
                "owner_role",
                "path_class",
                "postconditions",
                "preconditions",
                "relative_path",
                "sequence",
            ],
        )


class TestAuthority(unittest.TestCase):
    def test_deployment_setup_is_accepted(self) -> None:
        plan = I.build_initialization_plan(request_for(), adapter_empty())
        self.assertNotIn(ReasonCode.KB04_ROLE_UNKNOWN, reasons(plan))

    def test_every_other_actor_is_blocked(self) -> None:
        for actor in Actor:
            if actor is Actor.DEPLOYMENT_SETUP:
                continue
            with self.subTest(actor=actor.value):
                plan = I.build_initialization_plan(
                    request_for(authority=actor), adapter_empty()
                )
                self.assertIs(plan.status, I.InitializationStatus.BLOCKED)
                self.assertFalse(plan.applicable)
                self.assertIn(ReasonCode.KB04_ROLE_UNKNOWN, reasons(plan))

    def test_authority_has_no_default(self) -> None:
        fields = I.InitializationRequest.__dataclass_fields__
        self.assertIs(
            fields["authority"].default,
            fields["authority"].default_factory,  # both MISSING
        )


class TestBindingRequirement(unittest.TestCase):
    def test_missing_identity_binding_blocks(self) -> None:
        plan = I.build_initialization_plan(
            request_for(identity=None) if False else replace(
                request_for(), identity_binding=None
            ),
            adapter_empty(),
        )
        self.assertIs(plan.status, I.InitializationStatus.BLOCKED)
        self.assertIn(ReasonCode.KB04_BINDING_MISSING, reasons(plan))

    def test_unvalidated_binding_blocks(self) -> None:
        from core.core_brain.enforcement.binding import ValidationState

        plan = I.build_initialization_plan(
            request_for(identity=binding(validation_state=ValidationState.UNVALIDATED)),
            adapter_empty(),
        )
        self.assertIs(plan.status, I.InitializationStatus.BLOCKED)

    def test_repository_origin_blocks(self) -> None:
        from core.core_brain.enforcement.binding import ValueOrigin

        plan = I.build_initialization_plan(
            request_for(identity=binding(value_origin=ValueOrigin.REPOSITORY)),
            adapter_empty(),
        )
        self.assertIs(plan.status, I.InitializationStatus.BLOCKED)

    def test_empty_path_bindings_block(self) -> None:
        plan = I.build_initialization_plan(
            request_for(bindings=()), adapter_empty()
        )
        self.assertIs(plan.status, I.InitializationStatus.BLOCKED)
        self.assertIn(ReasonCode.KB04_CONTRACT_INVALID, reasons(plan))


class TestPP4AndAlreadyInitialized(unittest.TestCase):
    def test_pp4_binding_creates_no_directory_operation(self) -> None:
        from tests.kb04_init_fixtures import FakeFilesystemAdapter

        request = request_for(
            bindings=(
                I.TargetPathBinding(PathClass.PC_03, "source-registry"),
                I.TargetPathBinding(PathClass.PC_09, "rt2"),
            )
        )
        adapter = FakeFilesystemAdapter(
            nodes={"/vroot": directory("target"), "/vroot/target": directory()}
        )
        plan = I.build_initialization_plan(request, adapter)
        classes = {
            str(o.path_class)
            for o in plan.operations
            if o.kind is I.OperationKind.CREATE_CLASS_DIRECTORY
        }
        self.assertEqual(classes, {"PC-03"})

    def test_pp4_is_not_present(self) -> None:
        spec = c.path_class_spec(PathClass.PC_09)
        self.assertFalse(c.profile_spec(spec.profile).present)

    def test_already_initialized_status(self) -> None:
        plan = I.build_initialization_plan(request_for(), adapter_initialized())
        self.assertIs(plan.status, I.InitializationStatus.ALREADY_INITIALIZED)

    def test_already_initialized_has_zero_operations(self) -> None:
        plan = I.build_initialization_plan(request_for(), adapter_initialized())
        self.assertEqual(plan.operations, ())

    def test_already_initialized_is_not_applicable(self) -> None:
        plan = I.build_initialization_plan(request_for(), adapter_initialized())
        self.assertFalse(plan.applicable)

    def test_already_initialized_is_deterministic(self) -> None:
        first = I.build_initialization_plan(request_for(), adapter_initialized())
        second = I.build_initialization_plan(request_for(), adapter_initialized())
        self.assertEqual(first.to_dict(), second.to_dict())

    def test_verify_reports_conform_when_initialized(self) -> None:
        assessment = I.verify_initialized(request_for(), adapter_initialized())
        self.assertTrue(assessment.conform)

    def test_verify_is_not_conform_when_absent(self) -> None:
        assessment = I.verify_initialized(request_for(), adapter_absent())
        self.assertFalse(assessment.conform)


class TestNoExecutionSemantics(unittest.TestCase):
    def test_operationally_verified_is_always_false(self) -> None:
        for adapter in (adapter_absent(), adapter_empty(), adapter_initialized()):
            with self.subTest(adapter=type(adapter).__name__):
                assessment = I.verify_initialized(request_for(), adapter)
                self.assertFalse(assessment.operationally_verified)

    def test_no_mutated_field(self) -> None:
        for cls in (I.InitializationPlan, I.InitializationAssessment):
            with self.subTest(cls=cls.__name__):
                self.assertNotIn("mutated", cls.__dataclass_fields__)

    def test_status_has_no_execution_values(self) -> None:
        values = {s.value for s in I.InitializationStatus}
        for forbidden in ("APPLIED", "APPLYING", "ROLLED_BACK", "CLEANED_UP"):
            with self.subTest(value=forbidden):
                self.assertNotIn(forbidden, values)

    def test_module_exposes_no_apply_symbol(self) -> None:
        for name in ("apply_plan", "execute_plan", "initialize",
                     "initialize_target", "create_target"):
            with self.subTest(name=name):
                self.assertFalse(hasattr(I, name))

    def test_all_exports_are_plan_only(self) -> None:
        for name in I.__all__:
            with self.subTest(name=name):
                self.assertNotIn("apply", name.lower())
                self.assertNotIn("execute", name.lower())

    def test_plan_is_frozen(self) -> None:
        plan = I.build_initialization_plan(request_for(), adapter_empty())
        with self.assertRaises(Exception):
            plan.applicable = False  # type: ignore[misc]

    def test_operation_is_frozen(self) -> None:
        plan = I.build_initialization_plan(request_for(), adapter_empty())
        with self.assertRaises(Exception):
            plan.operations[0].sequence = 99  # type: ignore[misc]

    def test_request_is_frozen(self) -> None:
        request = request_for()
        with self.assertRaises(Exception):
            request.target_ref = "changed"  # type: ignore[misc]

    def test_planning_does_not_touch_the_repository(self) -> None:
        before = {p for p in REPO_ROOT.rglob("*") if p.is_file()}
        I.build_initialization_plan(request_for(), adapter_empty())
        after = {p for p in REPO_ROOT.rglob("*") if p.is_file()}
        self.assertEqual(before, after)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
