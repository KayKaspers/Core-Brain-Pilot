"""Tests der read-only Pfad-, Link- und Objektartpruefungen (CBP-WP-022, B2A).

Alle Faelle laufen auf jeder Plattform **ohne** ``skipTest``. Objektarten, die
sich unter Windows nicht erzeugen lassen — Symlink, FIFO, Socket, Device,
Hardlink — werden ueber injizierte ``stat``-Zustaende geprueft, nicht ueber
reale Dateisystemobjekte.
"""

from __future__ import annotations

import pathlib
import tempfile
import unittest
from pathlib import Path

from core.core_brain.enforcement import contract as c
from core.core_brain.enforcement import paths as p
from core.core_brain.enforcement.aggregate import FindingStatus
from core.core_brain.errors import ReasonCode
from tests.kb04_fixtures import (
    chardev_stat,
    dir_stat,
    fifo_stat,
    file_stat,
    socket_stat,
    symlink_stat,
)

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
FILE_AND_DIR = (c.ObjectKind.DIRECTORY, c.ObjectKind.REGULAR_FILE)


def codes(findings: tuple) -> set[ReasonCode | None]:
    """Gibt die Reason Codes einer Befundmenge zurueck."""
    return {f.reason for f in findings}


class TestRootBoundary(unittest.TestCase):
    def test_root_itself_is_inside(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            res = p.resolve_within_root(root, root)
            self.assertTrue(res.inside)
            self.assertEqual(res.relative, ".")

    def test_child_is_inside(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            res = p.resolve_within_root(root / "a" / "b.json", root)
            self.assertTrue(res.inside)
            self.assertEqual(res.relative, "a/b.json")

    def test_parent_is_outside(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "area"
            root.mkdir()
            res = p.resolve_within_root(root.parent, root)
            self.assertFalse(res.inside)
            self.assertEqual(res.relative, "<outside-root>")

    def test_traversal_is_resolved_not_string_matched(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "area"
            root.mkdir()
            res = p.resolve_within_root(root / ".." / "escape.json", root)
            self.assertFalse(res.inside)

    def test_traversal_back_into_root_is_inside(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "area"
            root.mkdir()
            res = p.resolve_within_root(root / "sub" / ".." / "ok.json", root)
            self.assertTrue(res.inside)
            self.assertEqual(res.relative, "ok.json")

    def test_sibling_with_shared_prefix_is_outside(self) -> None:
        # Reiner Zeichenkettenvergleich wuerde hier faelschlich "inside" sagen.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "area"
            root.mkdir()
            sibling = Path(tmp) / "area-other"
            sibling.mkdir()
            res = p.resolve_within_root(sibling / "x.json", root)
            self.assertFalse(res.inside)

    def test_relative_path_never_absolute(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            res = p.resolve_within_root(root / "deep" / "x", root)
            self.assertFalse(res.relative.startswith("/"))
            self.assertNotIn(":", res.relative)


class TestObjectKindClassification(unittest.TestCase):
    def test_absent(self) -> None:
        self.assertIs(p.classify_object_kind(None), c.ObjectKind.ABSENT)

    def test_directory(self) -> None:
        self.assertIs(
            p.classify_object_kind(dir_stat()), c.ObjectKind.DIRECTORY
        )

    def test_regular_file(self) -> None:
        self.assertIs(
            p.classify_object_kind(file_stat()), c.ObjectKind.REGULAR_FILE
        )

    def test_symlink(self) -> None:
        self.assertIs(
            p.classify_object_kind(symlink_stat()), c.ObjectKind.SYMLINK
        )

    def test_fifo_is_other(self) -> None:
        self.assertIs(p.classify_object_kind(fifo_stat()), c.ObjectKind.OTHER)

    def test_socket_is_other(self) -> None:
        self.assertIs(p.classify_object_kind(socket_stat()), c.ObjectKind.OTHER)

    def test_character_device_is_other(self) -> None:
        self.assertIs(
            p.classify_object_kind(chardev_stat()), c.ObjectKind.OTHER
        )

    def test_real_directory_on_disk(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            st = Path(tmp).lstat()
            self.assertIs(p.classify_object_kind(st), c.ObjectKind.DIRECTORY)

    def test_real_file_on_disk(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "a.txt"
            target.write_text("synthetic", encoding="utf-8")
            self.assertIs(
                p.classify_object_kind(target.lstat()),
                c.ObjectKind.REGULAR_FILE,
            )


class TestLinkClassification(unittest.TestCase):
    def test_classify_link_true_for_symlink(self) -> None:
        self.assertTrue(p.classify_link(symlink_stat()))

    def test_classify_link_false_for_file(self) -> None:
        self.assertFalse(p.classify_link(file_stat()))

    def test_classify_link_false_for_absent(self) -> None:
        self.assertFalse(p.classify_link(None))

    def test_hardlink_detected_on_regular_file(self) -> None:
        self.assertTrue(p.detect_hardlink(file_stat(nlink=2)))

    def test_single_link_file_is_not_hardlinked(self) -> None:
        self.assertFalse(p.detect_hardlink(file_stat(nlink=1)))

    def test_directory_link_count_is_not_a_hardlink_finding(self) -> None:
        self.assertFalse(p.detect_hardlink(dir_stat(nlink=5)))

    def test_absent_is_not_hardlinked(self) -> None:
        self.assertFalse(p.detect_hardlink(None))


class TestCheckPath(unittest.TestCase):
    def _check(self, path: Path, root: Path, st):
        return p.check_path(
            path=path,
            root=root,
            path_class=c.PathClass.PC_03,
            st=st,
            allowed_kinds=FILE_AND_DIR,
        )

    def test_conforming_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            found = self._check(root / "records" / "a.json", root, file_stat())
            self.assertEqual(len(found), 1)
            self.assertIs(found[0].status, FindingStatus.CONFORM)
            self.assertIsNone(found[0].reason)

    def test_conforming_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            found = self._check(root / "records", root, dir_stat())
            self.assertIs(found[0].status, FindingStatus.CONFORM)

    def test_outside_root_is_violation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "area"
            root.mkdir()
            found = self._check(root / ".." / "x.json", root, file_stat())
            self.assertIn(ReasonCode.KB04_PATH_OUTSIDE_ROOT, codes(found))
            self.assertIs(found[0].status, FindingStatus.VIOLATION)

    def test_missing_state_is_indeterminate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            found = self._check(root / "gone.json", root, None)
            self.assertIn(ReasonCode.KB04_STATE_INDETERMINATE, codes(found))
            self.assertIs(found[0].status, FindingStatus.INDETERMINATE)

    def test_symlink_is_rejected_not_resolved(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            found = self._check(root / "link", root, symlink_stat())
            self.assertIn(ReasonCode.KB04_LINK_SYMLINK_ESCAPE, codes(found))

    def test_internal_symlink_is_also_rejected(self) -> None:
        # Auch ein Symlink, dessen Ziel im Bereich laege, wird abgelehnt.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "target.json").write_text("x", encoding="utf-8")
            found = self._check(root / "inner-link", root, symlink_stat())
            self.assertIn(ReasonCode.KB04_LINK_SYMLINK_ESCAPE, codes(found))

    def test_hardlink_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            found = self._check(root / "a.json", root, file_stat(nlink=2))
            self.assertIn(ReasonCode.KB04_LINK_HARDLINK, codes(found))

    def test_fifo_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            found = self._check(root / "pipe", root, fifo_stat())
            self.assertIn(ReasonCode.KB04_OBJECT_KIND_INVALID, codes(found))

    def test_socket_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            found = self._check(root / "sock", root, socket_stat())
            self.assertIn(ReasonCode.KB04_OBJECT_KIND_INVALID, codes(found))

    def test_device_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            found = self._check(root / "dev", root, chardev_stat())
            self.assertIn(ReasonCode.KB04_OBJECT_KIND_INVALID, codes(found))

    def test_kind_outside_allowed_set_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            found = p.check_path(
                path=root / "d",
                root=root,
                path_class=c.PathClass.PC_03,
                st=dir_stat(),
                allowed_kinds=(c.ObjectKind.REGULAR_FILE,),
            )
            self.assertIn(ReasonCode.KB04_OBJECT_KIND_INVALID, codes(found))

    def test_findings_are_sorted_deterministically(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = self._check(root / "a.json", root, file_stat(nlink=2))
            second = self._check(root / "a.json", root, file_stat(nlink=2))
            self.assertEqual(first, second)
            self.assertEqual(list(first), sorted(first))

    def test_finding_carries_relative_path_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            found = self._check(root / "records" / "a.json", root, file_stat())
            self.assertEqual(found[0].relative_path, "records/a.json")

    def test_check_path_creates_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            before = sorted(x.name for x in root.iterdir())
            self._check(root / "never-created.json", root, file_stat())
            after = sorted(x.name for x in root.iterdir())
            self.assertEqual(before, after)


class TestModuleIsReadOnly(unittest.TestCase):
    def test_no_mutating_call_in_source(self) -> None:
        source = (
            REPO_ROOT / "core" / "core_brain" / "enforcement" / "paths.py"
        ).read_text(encoding="utf-8")
        for token in (
            "chmod(",
            "chown(",
            "mkdir(",
            "unlink(",
            "rmdir(",
            "rename(",
            "replace(",
            "write_text(",
            "write_bytes(",
            "touch(",
        ):
            with self.subTest(token=token):
                self.assertNotIn(token, source)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
