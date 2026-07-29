"""Tests des statischen Security Readiness Contract (CBP-WP-018, ADR-0013).

Der Vertrag ist rein statisch: keine Datei-, Netz-, ENV-, Uhr- oder
Zufallszugriffe. Er beschreibt ausschliesslich, welche
``(criterion, control_id)``-Bindungen eine synthetische Formpruefung erwartet —
er bestaetigt **keine** Security Readiness, Wirksamkeit oder Aktivierung.
"""

from __future__ import annotations

import inspect
import unittest

from core.core_brain.gate import security_contract as sc


class TestContractShape(unittest.TestCase):
    def test_revision_is_stable(self) -> None:
        self.assertEqual(sc.SECURITY_CONTRACT_REVISION, "1.0")

    def test_hash_is_hex64_and_deterministic(self) -> None:
        first = sc.security_contract_sha256()
        self.assertRegex(first, r"\A[0-9a-f]{64}\Z")
        self.assertEqual(first, sc.security_contract_sha256())
        self.assertEqual(first, sc.security_contract_sha256())

    def test_twelve_documented_controls(self) -> None:
        self.assertEqual(len(sc.DOCUMENTED_CONTROLS), 12)
        self.assertEqual(
            list(sc.DOCUMENTED_CONTROLS),
            [f"KB-{i:02d}" for i in range(1, 13)],
        )

    def test_seven_runtime_scoped_controls(self) -> None:
        self.assertEqual(len(sc.RUNTIME_SCOPED_CONTROLS), 7)
        self.assertEqual(
            set(sc.RUNTIME_SCOPED_CONTROLS),
            {"KB-02", "KB-03", "KB-04", "KB-07", "KB-08", "KB-10", "KB-11"},
        )

    def test_runtime_scoped_controls_are_documented(self) -> None:
        for ctrl in sc.RUNTIME_SCOPED_CONTROLS:
            self.assertIn(ctrl, sc.DOCUMENTED_CONTROLS)

    def test_non_runtime_scoped_partition_is_complete(self) -> None:
        self.assertEqual(len(sc.NON_RUNTIME_SCOPED_CONTROLS), 5)
        self.assertEqual(
            set(sc.RUNTIME_SCOPED_CONTROLS) | set(sc.NON_RUNTIME_SCOPED_CONTROLS),
            set(sc.DOCUMENTED_CONTROLS),
        )
        self.assertEqual(
            set(sc.RUNTIME_SCOPED_CONTROLS) & set(sc.NON_RUNTIME_SCOPED_CONTROLS),
            set(),
        )

    def test_no_duplicate_controls(self) -> None:
        for group in (
            sc.DOCUMENTED_CONTROLS,
            sc.RUNTIME_SCOPED_CONTROLS,
            sc.NON_RUNTIME_SCOPED_CONTROLS,
        ):
            self.assertEqual(len(group), len(set(group)))


class TestBindings(unittest.TestCase):
    EXPECTED = (
        (4, "KB-08"),
        (6, "KB-10"), (6, "KB-11"),
        (7, "KB-02"), (7, "KB-04"), (7, "KB-07"),
        (8, "KB-03"), (8, "KB-04"),
        (10, "KB-11"),
        (11, "KB-03"), (11, "KB-04"),
    )

    def test_eleven_bindings_exact(self) -> None:
        self.assertEqual(len(sc.RUNTIME_SCOPED_BINDINGS), 11)
        self.assertEqual(sc.RUNTIME_SCOPED_BINDINGS, self.EXPECTED)

    def test_no_duplicate_bindings(self) -> None:
        self.assertEqual(
            len(sc.RUNTIME_SCOPED_BINDINGS), len(set(sc.RUNTIME_SCOPED_BINDINGS))
        )

    def test_stable_sort_criterion_then_control(self) -> None:
        self.assertEqual(
            list(sc.RUNTIME_SCOPED_BINDINGS),
            sorted(sc.RUNTIME_SCOPED_BINDINGS, key=lambda p: (p[0], p[1])),
        )

    def test_only_security_criteria_appear(self) -> None:
        self.assertEqual(sc.RUNTIME_SCOPED_CRITERIA, frozenset({4, 6, 7, 8, 10, 11}))

    def test_criterion_nine_is_excluded(self) -> None:
        # Kriterium 9 ist non-security-structural und traegt keine KB-Bindung.
        self.assertNotIn(9, sc.RUNTIME_SCOPED_CRITERIA)
        self.assertIn(9, sc.NON_SECURITY_STRUCTURAL_CRITERIA)
        for criterion, _ in sc.RUNTIME_SCOPED_BINDINGS:
            self.assertNotEqual(criterion, 9)

    def test_criterion_five_is_excluded(self) -> None:
        # Kriterium 5 bleibt Human-only und traegt keine KB-Bindung.
        self.assertNotIn(5, sc.RUNTIME_SCOPED_CRITERIA)

    def test_every_binding_control_is_runtime_scoped(self) -> None:
        for _, ctrl in sc.RUNTIME_SCOPED_BINDINGS:
            self.assertIn(ctrl, sc.RUNTIME_SCOPED_CONTROLS)

    def test_every_runtime_scoped_control_is_bound(self) -> None:
        bound = {ctrl for _, ctrl in sc.RUNTIME_SCOPED_BINDINGS}
        self.assertEqual(bound, set(sc.RUNTIME_SCOPED_CONTROLS))

    def test_is_runtime_scoped_binding_accepts_contract_pairs(self) -> None:
        for criterion, ctrl in sc.RUNTIME_SCOPED_BINDINGS:
            self.assertTrue(sc.is_runtime_scoped_binding(criterion, ctrl))

    def test_is_runtime_scoped_binding_rejects_other_pairs(self) -> None:
        for pair in ((9, "KB-03"), (5, "KB-08"), (4, "KB-01"), (7, "KB-08"),
                     (1, "KB-02"), (11, "KB-99"), (0, "KB-01")):
            with self.subTest(pair=pair):
                self.assertFalse(sc.is_runtime_scoped_binding(*pair))


class TestControlIdSyntax(unittest.TestCase):
    def test_all_twelve_documented_ids_match(self) -> None:
        for ctrl in sc.DOCUMENTED_CONTROLS:
            self.assertRegex(ctrl, sc.CONTROL_ID_RE)

    def test_out_of_range_and_malformed_ids_rejected(self) -> None:
        for bad in ("KB-00", "KB-13", "KB-99", "kb-01", "KB-1", "KB-001",
                    "KB-0a", "KB-", "KB01", "", " KB-01", "KB-01 ",
                    "KB-01\n", "../KB-01", "http://x/KB-01"):
            with self.subTest(control_id=bad):
                self.assertIsNone(sc.CONTROL_ID_RE.match(bad))


class TestPurity(unittest.TestCase):
    """Der Vertrag darf keine I/O-, Zeit-, Zufalls- oder Netzabhaengigkeit haben."""

    _FORBIDDEN = (
        "open(", "Path(", "read_text", "read_bytes", "write_text", "write_bytes",
        "os.environ", "getenv", "socket", "urllib", "requests", "http",
        "time.", "datetime", "random", "uuid", "subprocess", "input(",
    )

    def test_module_source_has_no_io_or_clock(self) -> None:
        source = inspect.getsource(sc)
        for token in self._FORBIDDEN:
            with self.subTest(token=token):
                self.assertNotIn(token, source)

    def test_module_imports_are_minimal(self) -> None:
        # Nur hashlib, re, typing und das eigene models-Modul.
        source = inspect.getsource(sc)
        for line in source.splitlines():
            stripped = line.strip()
            if stripped.startswith(("import ", "from ")) and "__future__" not in stripped:
                self.assertTrue(
                    stripped.startswith(("import hashlib", "import re",
                                         "from typing", "from .models")),
                    msg=f"unerwarteter Import: {stripped}",
                )

    def test_contract_descriptor_is_immutable(self) -> None:
        for name in ("DOCUMENTED_CONTROLS", "RUNTIME_SCOPED_CONTROLS",
                     "NON_RUNTIME_SCOPED_CONTROLS", "RUNTIME_SCOPED_BINDINGS"):
            with self.subTest(name=name):
                self.assertIsInstance(getattr(sc, name), tuple)
        self.assertIsInstance(sc.RUNTIME_SCOPED_CRITERIA, frozenset)
        self.assertIsInstance(sc.NON_SECURITY_STRUCTURAL_CRITERIA, frozenset)

    def test_hash_stable_across_repeated_calls_and_import(self) -> None:
        import importlib

        before = sc.security_contract_sha256()
        reloaded = importlib.reload(sc)
        self.assertEqual(reloaded.security_contract_sha256(), before)


class TestNoReadinessClaim(unittest.TestCase):
    """Der Vertrag darf keine Erfuellungs-/Freigabeaussage kodieren."""

    def test_module_has_no_readiness_vocabulary_symbols(self) -> None:
        for forbidden in ("SECURITY_READY", "READINESS_PASSED", "CONTROLS_ENFORCED",
                          "APPROVED_CONTROLS", "security_ready", "security_passed"):
            with self.subTest(symbol=forbidden):
                self.assertFalse(hasattr(sc, forbidden))

    def test_negative_evidence_only_marker_in_descriptor(self) -> None:
        # Der gehashte Deskriptor traegt die Negativ-/Synthetic-Marker; ein
        # Deskriptor ohne sie ergaebe einen anderen Hash.
        source = inspect.getsource(sc)
        self.assertIn('"negative_evidence_only": True', source)
        self.assertIn('"synthetic_form_only": True', source)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
