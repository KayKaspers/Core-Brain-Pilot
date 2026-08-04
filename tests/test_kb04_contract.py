"""Tests des maschinenlesbaren KB-04-Contract-Teilmodells (CBP-WP-022, B2A).

Das Markdown-Dokument bleibt normative Authority. Diese Tests sichern das
abgeleitete Modell gegen Drift und pruefen seine Selbstkonsistenz.
"""

from __future__ import annotations

import hashlib
import pathlib
import unittest

from core.core_brain.enforcement import contract as c
from core.core_brain.errors import FilesystemEnforcementError, ReasonCode

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]


class TestPathClasses(unittest.TestCase):
    def test_eleven_path_classes(self) -> None:
        self.assertEqual(len(c.PathClass), 11)
        self.assertEqual(len(c.PATH_CLASSES), 11)

    def test_path_class_values_are_canonical(self) -> None:
        expected = [f"PC-{n:02d}" for n in range(1, 12)]
        self.assertEqual([m.value for m in c.PathClass], expected)

    def test_every_path_class_is_modelled(self) -> None:
        for member in c.PathClass:
            with self.subTest(path_class=member.value):
                self.assertIn(member, c.PATH_CLASSES)

    def test_spec_key_matches_member(self) -> None:
        for member, spec in c.PATH_CLASSES.items():
            with self.subTest(path_class=member.value):
                self.assertIs(spec.path_class, member)

    def test_classified_classes_carry_a_profile(self) -> None:
        for member, spec in c.PATH_CLASSES.items():
            with self.subTest(path_class=member.value):
                if spec.classified:
                    self.assertIsNotNone(spec.profile)

    def test_pc_11_is_unclassified_and_profileless(self) -> None:
        spec = c.PATH_CLASSES[c.PathClass.PC_11]
        self.assertFalse(spec.classified)
        self.assertIsNone(spec.profile)
        self.assertIs(spec.mount_mode, c.MountMode.UNKNOWN)
        self.assertEqual(spec.container_anchors, ())

    def test_pp4_classes_are_not_mounted(self) -> None:
        for member in (c.PathClass.PC_09, c.PathClass.PC_10):
            with self.subTest(path_class=member.value):
                spec = c.PATH_CLASSES[member]
                self.assertIs(spec.profile, c.PermissionProfile.PP_4)
                self.assertIs(spec.mount_mode, c.MountMode.NOT_MOUNTED)
                self.assertEqual(spec.container_anchors, ())

    def test_canonical_store_has_no_writer(self) -> None:
        spec = c.PATH_CLASSES[c.PathClass.PC_01]
        self.assertEqual(spec.writer_roles, ())
        self.assertIs(spec.profile, c.PermissionProfile.PP_3A)

    def test_configuration_class_has_no_writer_and_is_secret_free(self) -> None:
        spec = c.PATH_CLASSES[c.PathClass.PC_07]
        self.assertEqual(spec.writer_roles, ())
        self.assertTrue(spec.secret_free_required)
        self.assertIs(spec.profile, c.PermissionProfile.PP_3B)

    def test_only_pc_07_requires_secret_freedom(self) -> None:
        required = {
            m.value for m, s in c.PATH_CLASSES.items() if s.secret_free_required
        }
        self.assertEqual(required, {"PC-07"})

    def test_anchors_are_container_paths_without_host_reference(self) -> None:
        for member, spec in c.PATH_CLASSES.items():
            for anchor in spec.container_anchors:
                with self.subTest(path_class=member.value, anchor=anchor):
                    self.assertTrue(anchor.startswith("/"))
                    self.assertNotIn("\\", anchor)
                    self.assertNotIn(":", anchor)

    def test_multiple_values_are_tuples(self) -> None:
        for member, spec in c.PATH_CLASSES.items():
            with self.subTest(path_class=member.value):
                self.assertIsInstance(spec.container_anchors, tuple)
                self.assertIsInstance(spec.object_kinds, tuple)
                self.assertIsInstance(spec.reader_roles, tuple)
                self.assertIsInstance(spec.writer_roles, tuple)

    def test_spec_is_frozen(self) -> None:
        spec = c.PATH_CLASSES[c.PathClass.PC_01]
        with self.assertRaises(Exception):
            spec.area = "changed"  # type: ignore[misc]

    def test_path_class_spec_accessor(self) -> None:
        spec = c.path_class_spec(c.PathClass.PC_02)
        self.assertEqual(spec.area, "quarantine-store")


class TestPermissionProfiles(unittest.TestCase):
    def test_five_profile_variants(self) -> None:
        self.assertEqual(len(c.PermissionProfile), 5)
        self.assertEqual(len(c.PROFILES), 5)

    def test_profile_values_are_canonical(self) -> None:
        self.assertEqual(
            [m.value for m in c.PermissionProfile],
            ["PP-1", "PP-2", "PP-3a", "PP-3b", "PP-4"],
        )

    def test_pp1_modes(self) -> None:
        spec = c.profile_spec(c.PermissionProfile.PP_1)
        self.assertEqual(spec.file_mode, 0o600)
        self.assertEqual(spec.dir_mode, 0o700)
        self.assertEqual(spec.umask, 0o077)
        self.assertFalse(spec.world_read_allowed)
        self.assertFalse(spec.setgid_dir_allowed)

    def test_pp2_modes(self) -> None:
        spec = c.profile_spec(c.PermissionProfile.PP_2)
        self.assertEqual(spec.file_mode, 0o640)
        self.assertEqual(spec.dir_mode, 0o750)
        self.assertEqual(spec.umask, 0o027)
        self.assertFalse(spec.world_read_allowed)
        self.assertTrue(spec.setgid_dir_allowed)

    def test_pp3a_modes_and_no_world_read(self) -> None:
        spec = c.profile_spec(c.PermissionProfile.PP_3A)
        self.assertEqual(spec.file_mode, 0o640)
        self.assertEqual(spec.dir_mode, 0o750)
        self.assertFalse(spec.world_read_allowed)
        self.assertIsNone(spec.exclusive_path_class)

    def test_pp3b_modes(self) -> None:
        spec = c.profile_spec(c.PermissionProfile.PP_3B)
        self.assertEqual(spec.file_mode, 0o444)
        self.assertEqual(spec.dir_mode, 0o555)

    def test_pp3b_is_the_only_world_readable_profile(self) -> None:
        readable = {
            p.value for p, s in c.PROFILES.items() if s.world_read_allowed
        }
        self.assertEqual(readable, {"PP-3b"})

    def test_pp3b_is_exclusive_to_pc_07(self) -> None:
        spec = c.profile_spec(c.PermissionProfile.PP_3B)
        self.assertIs(spec.exclusive_path_class, c.PathClass.PC_07)

    def test_pp3b_is_used_by_exactly_one_path_class(self) -> None:
        users = [
            m.value
            for m, s in c.PATH_CLASSES.items()
            if s.profile is c.PermissionProfile.PP_3B
        ]
        self.assertEqual(users, ["PC-07"])

    def test_pp3a_and_pp3b_are_distinct(self) -> None:
        a = c.profile_spec(c.PermissionProfile.PP_3A)
        b = c.profile_spec(c.PermissionProfile.PP_3B)
        self.assertNotEqual(a.file_mode, b.file_mode)
        self.assertNotEqual(a.world_read_allowed, b.world_read_allowed)

    def test_pp4_is_not_present(self) -> None:
        spec = c.profile_spec(c.PermissionProfile.PP_4)
        self.assertFalse(spec.present)
        self.assertIsNone(spec.file_mode)
        self.assertIsNone(spec.dir_mode)
        self.assertIsNone(spec.umask)

    def test_no_profile_is_world_writable(self) -> None:
        for profile, spec in c.PROFILES.items():
            for mode in (spec.file_mode, spec.dir_mode):
                with self.subTest(profile=profile.value, mode=mode):
                    if mode is not None:
                        self.assertEqual(mode & c.WORLD_WRITE_BITS, 0)

    def test_no_profile_carries_special_bits_on_files(self) -> None:
        for profile, spec in c.PROFILES.items():
            with self.subTest(profile=profile.value):
                if spec.file_mode is not None:
                    self.assertEqual(spec.file_mode & c.SPECIAL_BITS, 0)

    def test_only_pp2_allows_setgid_directories(self) -> None:
        allowed = {
            p.value for p, s in c.PROFILES.items() if s.setgid_dir_allowed
        }
        self.assertEqual(allowed, {"PP-2"})

    def test_umask_never_grants_group_write_or_world_bits(self) -> None:
        for profile, spec in c.PROFILES.items():
            with self.subTest(profile=profile.value):
                if spec.umask is None:
                    continue
                self.assertEqual(spec.umask & 0o020, 0o020)
                self.assertEqual(spec.umask & 0o007, 0o007)


class TestActorsAndDimensions(unittest.TestCase):
    def test_ten_actors(self) -> None:
        self.assertEqual(len(c.Actor), 10)

    def test_actor_values(self) -> None:
        self.assertEqual(
            [a.value for a in c.Actor],
            [
                "deployment/setup",
                "operator",
                "ingest",
                "retrieval",
                "registry",
                "mapping",
                "release",
                "validation",
                "gate",
                "evidence",
            ],
        )

    def test_four_dimensions(self) -> None:
        self.assertEqual([d.value for d in c.Dimension], ["D-I", "D-II", "D-III", "D-IV"])

    def test_object_kinds(self) -> None:
        self.assertEqual(
            [k.value for k in c.ObjectKind],
            ["DIRECTORY", "REGULAR_FILE", "SYMLINK", "OTHER", "ABSENT"],
        )

    def test_mount_modes_include_unknown(self) -> None:
        self.assertIn(c.MountMode.UNKNOWN, list(c.MountMode))

    def test_service_roles_are_abstract(self) -> None:
        for role in c.ServiceRole:
            with self.subTest(role=role.value):
                self.assertRegex(role.value, r"\A[a-z][a-z-]*\Z")


class TestContractSelfConsistency(unittest.TestCase):
    def test_validate_contract_is_clean(self) -> None:
        self.assertEqual(c.validate_contract(), ())

    def test_validate_contract_is_deterministic(self) -> None:
        self.assertEqual(c.validate_contract(), c.validate_contract())

    def test_validate_contract_returns_tuple(self) -> None:
        self.assertIsInstance(c.validate_contract(), tuple)

    def test_accessor_rejects_unknown_profile(self) -> None:
        with self.assertRaises(FilesystemEnforcementError) as ctx:
            c.profile_spec("PP-99")  # type: ignore[arg-type]
        self.assertIs(ctx.exception.reason, ReasonCode.KB04_CONTRACT_INVALID)

    def test_accessor_rejects_unknown_path_class(self) -> None:
        with self.assertRaises(FilesystemEnforcementError) as ctx:
            c.path_class_spec("PC-99")  # type: ignore[arg-type]
        self.assertIs(ctx.exception.reason, ReasonCode.KB04_CONTRACT_INVALID)


class TestContractDriftProtection(unittest.TestCase):
    def _document_bytes(self) -> bytes:
        return (REPO_ROOT / c.CONTRACT_DOCUMENT_PATH).read_bytes()

    def test_document_path_is_relative(self) -> None:
        self.assertFalse(c.CONTRACT_DOCUMENT_PATH.startswith("/"))
        self.assertNotIn(":", c.CONTRACT_DOCUMENT_PATH)
        self.assertNotIn("\\", c.CONTRACT_DOCUMENT_PATH)

    def test_document_exists(self) -> None:
        self.assertTrue((REPO_ROOT / c.CONTRACT_DOCUMENT_PATH).is_file())

    def test_document_hash_matches_recorded_value(self) -> None:
        normalized = c.normalize_document_bytes(self._document_bytes())
        actual = hashlib.sha256(normalized).hexdigest()
        self.assertEqual(actual, c.CONTRACT_DOCUMENT_SHA256)

    def test_normalization_is_line_ending_independent(self) -> None:
        raw = self._document_bytes()
        crlf = raw.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
        lf = crlf.replace(b"\r\n", b"\n")
        self.assertEqual(
            hashlib.sha256(c.normalize_document_bytes(crlf)).hexdigest(),
            hashlib.sha256(c.normalize_document_bytes(lf)).hexdigest(),
        )

    def test_recorded_hash_is_hex64(self) -> None:
        self.assertRegex(c.CONTRACT_DOCUMENT_SHA256, r"\A[0-9a-f]{64}\Z")

    def test_model_hash_is_hex64(self) -> None:
        self.assertRegex(c.contract_model_sha256(), r"\A[0-9a-f]{64}\Z")

    def test_model_hash_is_stable_across_calls(self) -> None:
        first = c.contract_model_sha256()
        self.assertEqual(first, c.contract_model_sha256())
        self.assertEqual(first, c.contract_model_sha256())

    def test_model_hash_covers_profiles_and_path_classes(self) -> None:
        # Ein veraendertes Profil muss den Modellhash veraendern. Der Test
        # arbeitet auf einer Kopie und mutiert das Modell nicht dauerhaft.
        from dataclasses import replace as dc_replace

        original = c.PROFILES[c.PermissionProfile.PP_1]
        baseline = c.contract_model_sha256()
        c._PROFILES[c.PermissionProfile.PP_1] = dc_replace(
            original, file_mode=0o644
        )
        try:
            self.assertNotEqual(baseline, c.contract_model_sha256())
        finally:
            c._PROFILES[c.PermissionProfile.PP_1] = original
        self.assertEqual(baseline, c.contract_model_sha256())

    def test_revision_is_stable(self) -> None:
        self.assertEqual(c.CONTRACT_REVISION, "1.0")


class TestNoSideEffects(unittest.TestCase):
    def test_module_defines_no_mutating_helper(self) -> None:
        source = (
            REPO_ROOT / "core" / "core_brain" / "enforcement" / "contract.py"
        ).read_text(encoding="utf-8")
        for forbidden in ("chmod", "chown", "mkdir", "unlink", "rmdir"):
            with self.subTest(token=forbidden):
                self.assertNotIn(forbidden, source)

    def test_module_reads_no_file_on_import(self) -> None:
        source = (
            REPO_ROOT / "core" / "core_brain" / "enforcement" / "contract.py"
        ).read_text(encoding="utf-8")
        self.assertNotIn("read_bytes(", source)
        self.assertNotIn("read_text(", source)
        self.assertNotIn("open(", source)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
