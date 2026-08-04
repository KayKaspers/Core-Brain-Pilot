"""Tests der read-only KB-04-Validierung (CBP-WP-022, Phase B2A).

Alle Zustaende sind injiziert. Kein Test veraendert eine Datei, ein Recht,
einen Mount oder eine Identitaet, und kein Test fuehrt NT-04 oder NT-05 aus.
"""

from __future__ import annotations

import pathlib
import unittest
from dataclasses import replace

from core.core_brain.enforcement import contract as c
from core.core_brain.enforcement import validator as v
from core.core_brain.enforcement.aggregate import Finding, FindingStatus
from core.core_brain.enforcement.binding import (
    CollisionState,
    ValidationState,
    ValueOrigin,
    validate_binding,
    validate_binding_set,
)
from core.core_brain.errors import ReasonCode
from tests.kb04_fixtures import (
    GROUP_A,
    GROUP_B,
    IDENTITY_A,
    IDENTITY_B,
    binding_for,
    conforming_observation,
    host_state,
    mount_state,
    runtime_identity_state,
    runtime_object_state,
)

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]


def codes(findings: tuple[Finding, ...]) -> set[ReasonCode | None]:
    """Gibt die Reason Codes einer Befundmenge zurueck."""
    return {f.reason for f in findings}


def status_of(findings: tuple[Finding, ...], dimension: c.Dimension) -> set:
    """Gibt die Status einer Dimension zurueck."""
    return {f.status for f in findings if str(f.dimension) == dimension.value}


class TestBindingForm(unittest.TestCase):
    def test_complete_binding_is_clean(self) -> None:
        self.assertEqual(validate_binding(binding_for(c.PathClass.PC_03)), ())

    def test_missing_binding_is_fail_closed(self) -> None:
        found = validate_binding(None)
        self.assertEqual(len(found), 1)
        self.assertIs(found[0].reason, ReasonCode.KB04_BINDING_MISSING)
        self.assertIs(found[0].status, FindingStatus.VIOLATION)

    def test_empty_identity_reference_is_rejected(self) -> None:
        binding = replace(
            binding_for(c.PathClass.PC_03), expected_effective_identity="  "
        )
        self.assertIn(ReasonCode.KB04_BINDING_MISSING, codes(validate_binding(binding)))

    def test_empty_primary_group_is_rejected(self) -> None:
        binding = replace(binding_for(c.PathClass.PC_03), primary_group_ref="")
        self.assertIn(ReasonCode.KB04_BINDING_MISSING, codes(validate_binding(binding)))

    def test_no_path_class_is_rejected(self) -> None:
        binding = replace(binding_for(c.PathClass.PC_03), path_class_refs=())
        self.assertIn(ReasonCode.KB04_BINDING_MISSING, codes(validate_binding(binding)))

    def test_unbindable_path_class_is_rejected(self) -> None:
        for member in (c.PathClass.PC_09, c.PathClass.PC_10, c.PathClass.PC_11):
            with self.subTest(path_class=member.value):
                binding = replace(
                    binding_for(c.PathClass.PC_03), path_class_refs=(member,)
                )
                self.assertIn(
                    ReasonCode.KB04_PATHCLASS_UNKNOWN,
                    codes(validate_binding(binding)),
                )

    def test_repository_origin_is_forbidden(self) -> None:
        for origin in (
            ValueOrigin.REPOSITORY,
            ValueOrigin.DERIVED,
            ValueOrigin.DEFAULT,
        ):
            with self.subTest(origin=origin.value):
                binding = replace(
                    binding_for(c.PathClass.PC_03), value_origin=origin
                )
                self.assertIn(
                    ReasonCode.KB04_BINDING_MISSING,
                    codes(validate_binding(binding)),
                )

    def test_collision_state_is_fail_closed(self) -> None:
        for state in (
            CollisionState.DUPLICATE_ROLE,
            CollisionState.DUPLICATE_IDENTITY,
            CollisionState.CROSS_BOUND,
        ):
            with self.subTest(state=state.value):
                binding = replace(
                    binding_for(c.PathClass.PC_03), collision_state=state
                )
                self.assertIn(
                    ReasonCode.KB04_BINDING_COLLISION,
                    codes(validate_binding(binding)),
                )

    def test_unvalidated_binding_is_indeterminate(self) -> None:
        binding = replace(
            binding_for(c.PathClass.PC_03),
            validation_state=ValidationState.UNVALIDATED,
        )
        found = validate_binding(binding)
        self.assertIn(FindingStatus.INDETERMINATE, {f.status for f in found})

    def test_rejected_binding_is_violation(self) -> None:
        binding = replace(
            binding_for(c.PathClass.PC_03),
            validation_state=ValidationState.REJECTED,
        )
        self.assertIn(ReasonCode.KB04_BINDING_MISSING, codes(validate_binding(binding)))

    def test_read_groups_forbidden_for_pp1(self) -> None:
        binding = replace(
            binding_for(c.PathClass.PC_02),
            profile_ref=c.PermissionProfile.PP_1,
            read_group_refs=(GROUP_B,),
        )
        self.assertIn(ReasonCode.KB04_GROUP_MISMATCH, codes(validate_binding(binding)))

    def test_read_groups_allowed_for_pp2(self) -> None:
        binding = replace(
            binding_for(c.PathClass.PC_03), read_group_refs=(GROUP_B,)
        )
        self.assertEqual(validate_binding(binding), ())

    def test_duplicate_role_collides(self) -> None:
        a = binding_for(c.PathClass.PC_03)
        b = binding_for(c.PathClass.PC_04, identity=IDENTITY_B)
        self.assertIn(
            ReasonCode.KB04_BINDING_COLLISION, codes(validate_binding_set([a, b]))
        )

    def test_shared_identity_collides(self) -> None:
        a = binding_for(c.PathClass.PC_03)
        b = binding_for(
            c.PathClass.PC_02, role=c.ServiceRole.DATA_WORKER, identity=IDENTITY_A
        )
        b = replace(b, profile_ref=c.PermissionProfile.PP_1)
        self.assertIn(
            ReasonCode.KB04_BINDING_COLLISION, codes(validate_binding_set([a, b]))
        )

    def test_distinct_bindings_are_clean(self) -> None:
        a = binding_for(c.PathClass.PC_03)
        b = replace(
            binding_for(c.PathClass.PC_02, identity=IDENTITY_B),
            role_id=c.ServiceRole.DATA_WORKER,
            profile_ref=c.PermissionProfile.PP_1,
            primary_group_ref=GROUP_B,
        )
        self.assertEqual(validate_binding_set([a, b]), ())

    def test_ten_required_fields_declared(self) -> None:
        from core.core_brain.enforcement.binding import REQUIRED_BINDING_FIELDS

        self.assertEqual(len(REQUIRED_BINDING_FIELDS), 10)


class TestObservationDimensions(unittest.TestCase):
    def setUp(self) -> None:
        self.binding = binding_for(c.PathClass.PC_03)
        self.observation = conforming_observation()

    def test_conforming_observation_has_no_violation(self) -> None:
        found = v.validate_observation(self.observation, self.binding)
        self.assertEqual(
            [f for f in found if f.status is not FindingStatus.CONFORM], []
        )

    def test_all_four_dimensions_present(self) -> None:
        found = v.validate_observation(self.observation, self.binding)
        dims = {str(f.dimension) for f in found}
        for dimension in ("D-I", "D-II", "D-III", "D-IV"):
            with self.subTest(dimension=dimension):
                self.assertIn(dimension, dims)

    def test_missing_host_is_indeterminate(self) -> None:
        found = v.validate_observation(
            replace(self.observation, host=None), self.binding
        )
        self.assertEqual(status_of(found, c.Dimension.D_I), {FindingStatus.INDETERMINATE})

    def test_missing_mount_is_indeterminate(self) -> None:
        found = v.validate_observation(
            replace(self.observation, mount=None), self.binding
        )
        self.assertEqual(
            status_of(found, c.Dimension.D_II), {FindingStatus.INDETERMINATE}
        )

    def test_missing_runtime_object_is_indeterminate(self) -> None:
        found = v.validate_observation(
            replace(self.observation, runtime_object=None), self.binding
        )
        self.assertEqual(
            status_of(found, c.Dimension.D_III), {FindingStatus.INDETERMINATE}
        )

    def test_missing_runtime_identity_is_indeterminate(self) -> None:
        found = v.validate_observation(
            replace(self.observation, runtime_identity=None), self.binding
        )
        self.assertEqual(
            status_of(found, c.Dimension.D_IV), {FindingStatus.INDETERMINATE}
        )

    def test_missing_dimension_is_never_conform(self) -> None:
        for field in ("host", "mount", "runtime_object", "runtime_identity"):
            with self.subTest(dimension=field):
                found = v.validate_observation(
                    replace(self.observation, **{field: None}), self.binding
                )
                indeterminate = [
                    f for f in found if f.status is FindingStatus.INDETERMINATE
                ]
                self.assertTrue(indeterminate)

    def test_host_state_does_not_prove_runtime_view(self) -> None:
        # D-I konform, D-III fehlt: das Gesamtbild bleibt unvollstaendig.
        found = v.validate_observation(
            replace(self.observation, runtime_object=None), self.binding
        )
        self.assertEqual(status_of(found, c.Dimension.D_I), {FindingStatus.CONFORM})
        self.assertEqual(
            status_of(found, c.Dimension.D_III), {FindingStatus.INDETERMINATE}
        )

    def test_mount_state_does_not_prove_host_rights(self) -> None:
        found = v.validate_observation(
            replace(self.observation, host=None), self.binding
        )
        self.assertEqual(status_of(found, c.Dimension.D_II), {FindingStatus.CONFORM})
        self.assertEqual(
            status_of(found, c.Dimension.D_I), {FindingStatus.INDETERMINATE}
        )


class TestOwnerGroupAndMode(unittest.TestCase):
    def setUp(self) -> None:
        self.binding = binding_for(c.PathClass.PC_03)
        self.observation = conforming_observation()

    def _host(self, **kwargs):
        return replace(self.observation, host=replace(self.observation.host, **kwargs))

    def test_correct_owner_is_conform(self) -> None:
        found = v.validate_observation(self.observation, self.binding)
        self.assertNotIn(ReasonCode.KB04_OWNER_MISMATCH, codes(found))

    def test_wrong_owner_is_violation(self) -> None:
        found = v.validate_observation(self._host(owner_ref="data-worker"), self.binding)
        self.assertIn(ReasonCode.KB04_OWNER_MISMATCH, codes(found))

    def test_correct_group_is_conform(self) -> None:
        found = v.validate_observation(self.observation, self.binding)
        self.assertNotIn(ReasonCode.KB04_GROUP_MISMATCH, codes(found))

    def test_wrong_group_is_violation(self) -> None:
        found = v.validate_observation(self._host(group_ref="service"), self.binding)
        self.assertIn(ReasonCode.KB04_GROUP_MISMATCH, codes(found))

    def test_correct_file_mode_is_conform(self) -> None:
        found = v.validate_observation(self.observation, self.binding)
        self.assertNotIn(ReasonCode.KB04_MODE_MISMATCH, codes(found))

    def test_wrong_file_mode_is_violation(self) -> None:
        found = v.validate_observation(self._host(mode=0o600), self.binding)
        self.assertIn(ReasonCode.KB04_MODE_MISMATCH, codes(found))

    def test_correct_directory_mode_is_conform(self) -> None:
        obs = self._host(mode=0o750, object_kind=c.ObjectKind.DIRECTORY)
        obs = replace(
            obs,
            runtime_object=runtime_object_state(
                mode=0o750, kind=c.ObjectKind.DIRECTORY, writable=True
            ),
        )
        found = v.validate_observation(obs, self.binding)
        self.assertNotIn(ReasonCode.KB04_MODE_MISMATCH, codes(found))

    def test_world_writable_file_is_violation(self) -> None:
        found = v.validate_observation(self._host(mode=0o642), self.binding)
        self.assertIn(ReasonCode.KB04_MODE_WORLD_BITS, codes(found))

    def test_world_writable_directory_is_violation(self) -> None:
        obs = self._host(mode=0o757, object_kind=c.ObjectKind.DIRECTORY)
        found = v.validate_observation(obs, self.binding)
        self.assertIn(ReasonCode.KB04_MODE_WORLD_BITS, codes(found))

    def test_world_readable_is_violation_outside_pp3b(self) -> None:
        found = v.validate_observation(self._host(mode=0o644), self.binding)
        self.assertIn(ReasonCode.KB04_MODE_WORLD_BITS, codes(found))

    def test_setuid_is_violation(self) -> None:
        found = v.validate_observation(self._host(mode=0o4640), self.binding)
        self.assertIn(ReasonCode.KB04_MODE_SPECIAL_BITS, codes(found))

    def test_sticky_bit_is_violation(self) -> None:
        found = v.validate_observation(self._host(mode=0o1640), self.binding)
        self.assertIn(ReasonCode.KB04_MODE_SPECIAL_BITS, codes(found))

    def test_setgid_directory_allowed_for_pp2(self) -> None:
        obs = self._host(mode=0o2750, object_kind=c.ObjectKind.DIRECTORY)
        found = v.validate_observation(obs, self.binding)
        self.assertNotIn(ReasonCode.KB04_MODE_SPECIAL_BITS, codes(found))

    def test_setgid_directory_forbidden_for_pp1(self) -> None:
        obs = replace(
            conforming_observation(),
            path_class=c.PathClass.PC_02,
            host=host_state(
                owner="data-worker",
                group="data-worker",
                mode=0o2700,
                kind=c.ObjectKind.DIRECTORY,
            ),
        )
        binding = replace(
            binding_for(c.PathClass.PC_02, role=c.ServiceRole.DATA_WORKER),
            profile_ref=c.PermissionProfile.PP_1,
        )
        found = v.validate_observation(obs, binding)
        self.assertIn(ReasonCode.KB04_MODE_SPECIAL_BITS, codes(found))

    def test_wrong_object_kind_is_violation(self) -> None:
        found = v.validate_observation(
            self._host(object_kind=c.ObjectKind.OTHER), self.binding
        )
        self.assertIn(ReasonCode.KB04_OBJECT_KIND_INVALID, codes(found))

    def test_host_symlink_is_violation(self) -> None:
        found = v.validate_observation(self._host(is_symlink=True), self.binding)
        self.assertIn(ReasonCode.KB04_LINK_SYMLINK_ESCAPE, codes(found))

    def test_host_hardlink_is_violation(self) -> None:
        found = v.validate_observation(self._host(is_hardlinked=True), self.binding)
        self.assertIn(ReasonCode.KB04_LINK_HARDLINK, codes(found))


class TestMountAndRuntimeObject(unittest.TestCase):
    def setUp(self) -> None:
        self.binding = binding_for(c.PathClass.PC_03)
        self.observation = conforming_observation()

    def test_expected_mount_mode_is_conform(self) -> None:
        found = v.validate_observation(self.observation, self.binding)
        self.assertEqual(status_of(found, c.Dimension.D_II), {FindingStatus.CONFORM})

    def test_wrong_mount_mode_is_violation(self) -> None:
        obs = replace(
            self.observation, mount=mount_state(mode=c.MountMode.READ_ONLY)
        )
        found = v.validate_observation(obs, self.binding)
        self.assertIn(ReasonCode.KB04_MOUNT_MODE_MISMATCH, codes(found))

    def test_unknown_mount_mode_is_indeterminate(self) -> None:
        obs = replace(self.observation, mount=mount_state(mode=c.MountMode.UNKNOWN))
        found = v.validate_observation(obs, self.binding)
        self.assertIn(
            FindingStatus.INDETERMINATE, status_of(found, c.Dimension.D_II)
        )

    def test_unexpected_additional_mount_is_violation(self) -> None:
        obs = replace(
            self.observation,
            mount=mount_state(
                mode=c.MountMode.READ_WRITE, unexpected=("<extra>",)
            ),
        )
        found = v.validate_observation(obs, self.binding)
        self.assertIn(ReasonCode.KB04_MOUNT_MODE_MISMATCH, codes(found))

    def test_mount_boundary_crossing_is_violation(self) -> None:
        obs = replace(
            self.observation,
            mount=mount_state(mode=c.MountMode.READ_WRITE, crosses_boundary=True),
        )
        found = v.validate_observation(obs, self.binding)
        self.assertIn(ReasonCode.KB04_PATH_OUTSIDE_ROOT, codes(found))

    def test_read_only_area_must_not_be_writable(self) -> None:
        obs = replace(
            conforming_observation(),
            path_class=c.PathClass.PC_01,
            host=host_state(
                owner="maintainer-owned", group="control-plane", mode=0o640
            ),
            mount=mount_state(mode=c.MountMode.READ_ONLY),
            runtime_object=runtime_object_state(mode=0o640, writable=True),
        )
        binding = replace(
            binding_for(c.PathClass.PC_01),
            profile_ref=c.PermissionProfile.PP_3A,
        )
        found = v.validate_observation(obs, binding)
        self.assertIn(ReasonCode.KB04_MOUNT_MODE_MISMATCH, codes(found))

    def test_unreadable_area_is_violation(self) -> None:
        obs = replace(
            self.observation,
            runtime_object=runtime_object_state(
                mode=0o640, readable=False, writable=True
            ),
        )
        found = v.validate_observation(obs, self.binding)
        self.assertIn(ReasonCode.KB04_MODE_MISMATCH, codes(found))

    def test_runtime_mode_mismatch_is_violation(self) -> None:
        obs = replace(
            self.observation,
            runtime_object=runtime_object_state(mode=0o666, writable=True),
        )
        found = v.validate_observation(obs, self.binding)
        self.assertIn(ReasonCode.KB04_MODE_WORLD_BITS, codes(found))

    def test_not_present_area_absent_is_conform(self) -> None:
        obs = v.Observation(
            path_class=c.PathClass.PC_09,
            relative_path="<not-mounted>",
            host=host_state(
                owner="human-maintainer",
                group="human-maintainer",
                mode=0,
                kind=c.ObjectKind.ABSENT,
            ),
            mount=mount_state(mode=c.MountMode.NOT_MOUNTED),
            runtime_object=runtime_object_state(
                mode=0, kind=c.ObjectKind.ABSENT, readable=False
            ),
            runtime_identity=runtime_identity_state(),
        )
        found = v.validate_observation(obs, binding_for(c.PathClass.PC_03))
        self.assertEqual(status_of(found, c.Dimension.D_I), {FindingStatus.CONFORM})

    def test_not_present_area_reachable_is_violation(self) -> None:
        obs = v.Observation(
            path_class=c.PathClass.PC_10,
            relative_path="<not-mounted>",
            host=host_state(owner="external", group="external", mode=0o700,
                            kind=c.ObjectKind.DIRECTORY),
            mount=mount_state(mode=c.MountMode.NOT_MOUNTED),
            runtime_object=runtime_object_state(
                mode=0o700, kind=c.ObjectKind.DIRECTORY
            ),
            runtime_identity=runtime_identity_state(),
        )
        found = v.validate_observation(obs, binding_for(c.PathClass.PC_03))
        self.assertIn(ReasonCode.KB04_OBJECT_KIND_INVALID, codes(found))


class TestRuntimeIdentity(unittest.TestCase):
    def setUp(self) -> None:
        self.binding = binding_for(c.PathClass.PC_03)
        self.observation = conforming_observation()

    def test_matching_identity_is_conform(self) -> None:
        found = v.validate_observation(self.observation, self.binding)
        self.assertEqual(status_of(found, c.Dimension.D_IV), {FindingStatus.CONFORM})

    def test_identity_mismatch_is_violation(self) -> None:
        obs = replace(
            self.observation, runtime_identity=runtime_identity_state(identity=IDENTITY_B)
        )
        found = v.validate_observation(obs, self.binding)
        self.assertIn(ReasonCode.KB04_IDENTITY_MISMATCH, codes(found))

    def test_role_mismatch_is_violation(self) -> None:
        obs = replace(
            self.observation,
            runtime_identity=runtime_identity_state(role=c.ServiceRole.DATA_WORKER),
        )
        found = v.validate_observation(obs, self.binding)
        self.assertIn(ReasonCode.KB04_ROLE_UNKNOWN, codes(found))

    def test_unexpected_supplementary_group_is_violation(self) -> None:
        obs = replace(
            self.observation,
            runtime_identity=runtime_identity_state(groups=(GROUP_A, "group-ref-x")),
        )
        found = v.validate_observation(obs, self.binding)
        self.assertIn(ReasonCode.KB04_GROUP_MISMATCH, codes(found))

    def test_declared_read_group_is_accepted(self) -> None:
        binding = replace(self.binding, read_group_refs=(GROUP_B,))
        obs = replace(
            self.observation,
            runtime_identity=runtime_identity_state(groups=(GROUP_A, GROUP_B)),
        )
        found = v.validate_observation(obs, binding)
        self.assertEqual(status_of(found, c.Dimension.D_IV), {FindingStatus.CONFORM})

    def test_identity_without_binding_is_violation(self) -> None:
        found = v.validate_observation(self.observation, None)
        self.assertIn(ReasonCode.KB04_BINDING_MISSING, codes(found))


class TestUnknownPathClass(unittest.TestCase):
    def test_pc_11_is_forbidden_not_neutral(self) -> None:
        obs = v.Observation(
            path_class=c.PathClass.PC_11, relative_path="<unclassified>"
        )
        found = v.validate_observation(obs, binding_for(c.PathClass.PC_03))
        self.assertEqual(len(found), 1)
        self.assertIs(found[0].reason, ReasonCode.KB04_PATHCLASS_UNKNOWN)
        self.assertIs(found[0].status, FindingStatus.VIOLATION)


class TestPP3bBoundary(unittest.TestCase):
    def _config_observation(
        self,
        classification: v.ContentClassification | None,
        *,
        content_origin: v.ObservationOrigin | None = v.ObservationOrigin.DECLARED,
    ) -> v.Observation:
        return v.Observation(
            path_class=c.PathClass.PC_07,
            relative_path="control-plane.toml",
            host=host_state(
                owner="deployment-owned", group="control-plane", mode=0o444
            ),
            mount=mount_state(mode=c.MountMode.READ_ONLY),
            runtime_object=runtime_object_state(mode=0o444),
            runtime_identity=runtime_identity_state(),
            content_classification=classification,
            content_origin=content_origin,
        )

    def test_non_secret_runtime_config_is_conform(self) -> None:
        obs = self._config_observation(
            v.ContentClassification.NON_SECRET_RUNTIME_CONFIG
        )
        found = v.validate_observation(obs, binding_for(c.PathClass.PC_07))
        self.assertNotIn(ReasonCode.KB04_CONTRACT_INVALID, codes(found))

    def test_sensitive_or_secret_is_violation(self) -> None:
        obs = self._config_observation(v.ContentClassification.SENSITIVE_OR_SECRET)
        found = v.validate_observation(obs, binding_for(c.PathClass.PC_07))
        self.assertIn(ReasonCode.KB04_CONTRACT_INVALID, codes(found))
        statuses = {f.status for f in found if f.reason is ReasonCode.KB04_CONTRACT_INVALID}
        self.assertEqual(statuses, {FindingStatus.VIOLATION})

    def test_unclassified_is_indeterminate(self) -> None:
        obs = self._config_observation(v.ContentClassification.UNCLASSIFIED)
        found = v.validate_observation(obs, binding_for(c.PathClass.PC_07))
        self.assertIn(ReasonCode.KB04_STATE_INDETERMINATE, codes(found))

    def test_missing_classification_defaults_to_unclassified(self) -> None:
        obs = self._config_observation(None)
        found = v.validate_observation(obs, binding_for(c.PathClass.PC_07))
        self.assertIn(ReasonCode.KB04_STATE_INDETERMINATE, codes(found))

    def test_missing_classification_is_never_conform(self) -> None:
        obs = self._config_observation(None)
        found = v.validate_observation(obs, binding_for(c.PathClass.PC_07))
        relevant = [
            f
            for f in found
            if f.reason is ReasonCode.KB04_STATE_INDETERMINATE
        ]
        self.assertTrue(relevant)
        self.assertNotIn(FindingStatus.CONFORM, {f.status for f in relevant})

    def test_classification_without_origin_is_indeterminate(self) -> None:
        obs = self._config_observation(
            v.ContentClassification.NON_SECRET_RUNTIME_CONFIG,
            content_origin=None,
        )
        found = v.validate_observation(obs, binding_for(c.PathClass.PC_07))
        self.assertIn(ReasonCode.KB04_STATE_INDETERMINATE, codes(found))

    def test_world_read_is_permitted_only_under_pp3b(self) -> None:
        obs = self._config_observation(
            v.ContentClassification.NON_SECRET_RUNTIME_CONFIG
        )
        found = v.validate_observation(obs, binding_for(c.PathClass.PC_07))
        self.assertNotIn(ReasonCode.KB04_MODE_WORLD_BITS, codes(found))

    def test_world_write_stays_forbidden_under_pp3b(self) -> None:
        obs = self._config_observation(
            v.ContentClassification.NON_SECRET_RUNTIME_CONFIG
        )
        obs = replace(obs, host=replace(obs.host, mode=0o446))
        found = v.validate_observation(obs, binding_for(c.PathClass.PC_07))
        self.assertIn(ReasonCode.KB04_MODE_WORLD_BITS, codes(found))

    def test_other_classes_do_not_require_classification(self) -> None:
        obs = conforming_observation()
        found = v.validate_observation(obs, binding_for(c.PathClass.PC_03))
        self.assertNotIn(ReasonCode.KB04_STATE_INDETERMINATE, codes(found))

    def test_pp3b_is_not_used_outside_pc_07(self) -> None:
        users = [
            m.value
            for m, s in c.PATH_CLASSES.items()
            if s.profile is c.PermissionProfile.PP_3B
        ]
        self.assertEqual(users, ["PC-07"])


class TestOriginHandling(unittest.TestCase):
    def test_synthetic_origin_is_carried_into_findings(self) -> None:
        found = v.validate_observation(
            conforming_observation(origin=v.ObservationOrigin.SYNTHETIC),
            binding_for(c.PathClass.PC_03),
        )
        origins = {f.origin for f in found if f.origin is not None}
        self.assertEqual(origins, {v.ObservationOrigin.SYNTHETIC})

    def test_declared_origin_is_carried_into_findings(self) -> None:
        found = v.validate_observation(
            conforming_observation(origin=v.ObservationOrigin.DECLARED),
            binding_for(c.PathClass.PC_03),
        )
        origins = {f.origin for f in found if f.origin is not None}
        self.assertEqual(origins, {v.ObservationOrigin.DECLARED})

    def test_observed_origin_is_carried_into_findings(self) -> None:
        found = v.validate_observation(
            conforming_observation(origin=v.ObservationOrigin.OBSERVED),
            binding_for(c.PathClass.PC_03),
        )
        origins = {f.origin for f in found if f.origin is not None}
        self.assertEqual(origins, {v.ObservationOrigin.OBSERVED})

    def test_three_origins_exist(self) -> None:
        self.assertEqual(
            [o.value for o in v.ObservationOrigin],
            ["SYNTHETIC", "DECLARED", "OBSERVED"],
        )


class TestDeterminismAndPurity(unittest.TestCase):
    def test_repeated_validation_is_identical(self) -> None:
        obs = conforming_observation()
        binding = binding_for(c.PathClass.PC_03)
        self.assertEqual(
            v.validate_observation(obs, binding),
            v.validate_observation(obs, binding),
        )

    def test_findings_are_sorted(self) -> None:
        obs = replace(
            conforming_observation(),
            host=host_state(owner="wrong", group="wrong", mode=0o646),
        )
        found = v.validate_observation(obs, binding_for(c.PathClass.PC_03))
        self.assertEqual(list(found), sorted(found))

    def test_observation_is_frozen(self) -> None:
        obs = conforming_observation()
        with self.assertRaises(Exception):
            obs.relative_path = "changed"  # type: ignore[misc]

    def test_host_state_is_frozen(self) -> None:
        obs = conforming_observation()
        with self.assertRaises(Exception):
            obs.host.mode = 0o777  # type: ignore[misc]

    def test_validator_source_has_no_mutation(self) -> None:
        source = (
            REPO_ROOT / "core" / "core_brain" / "enforcement" / "validator.py"
        ).read_text(encoding="utf-8")
        for token in (
            "chmod(",
            "chown(",
            "mkdir(",
            "unlink(",
            "rmdir(",
            "rename(",
            "write_text(",
            "write_bytes(",
            "touch(",
            "os.remove",
        ):
            with self.subTest(token=token):
                self.assertNotIn(token, source)

    def test_binding_source_has_no_identity_resolution(self) -> None:
        source = (
            REPO_ROOT / "core" / "core_brain" / "enforcement" / "binding.py"
        ).read_text(encoding="utf-8")
        for token in ("import pwd", "import grp", "getpwnam", "getgrnam", "geteuid"):
            with self.subTest(token=token):
                self.assertNotIn(token, source)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
