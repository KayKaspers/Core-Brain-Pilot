"""Tests der KB-04-Contract-Traceability (CBP-WP-022, Phase B2C-T-R).

Diese Tests sichern die Matrix gegen Contractdrift, falsche Zuordnung und
unbelegte Abdeckungsbehauptungen. Sie sind **Metatests** und zaehlen selbst
**niemals** als fachliche Abdeckung einer Contractkennung.

Kein Test fuehrt NT-04 oder NT-05 aus, keiner erzeugt Evidenz, keiner
veraendert eine Datei, ein Recht, einen Mount oder eine Identitaet.
"""

from __future__ import annotations

import json
import pathlib
import re
import unittest

from tests.kb04_nt_fixtures import (
    ALLOWED_TEST_MODULES,
    B2D_REAL_ONLY_CONTRACT_TEST_IDS,
    CONTRACT_TEST_TRACEABILITY,
    GAP_CONTRACT_SECTION,
    SYNTHETIC_COVERAGE_GAP_CONTRACT_TEST_IDS,
    SYNTHETIC_COVERED_CONTRACT_TEST_IDS,
    ContractTestTrace,
    TraceabilityDisposition,
    traceability_manifest_dict,
    traceability_manifest_sha256,
)

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTRACT_DOCUMENT = (
    REPO_ROOT / "docs" / "security" / "KB_04_STAGE_1_ENFORCEMENT_CONTRACT.md"
)

#: Die beiden neuen B2C-T-Testmodule duerfen niemals als Abdeckung dienen.
NEW_MODULES = (
    "tests.test_kb04_contract_traceability",
    "tests.test_kb04_nt_preparation",
)

_ID_PATTERN = re.compile(r"KB04-T-([PN])(\d{2})")


def contract_ids_from_document() -> set[str]:
    """Liest alle Testkennungen **read-only** aus dem Contractdokument."""
    text = CONTRACT_DOCUMENT.read_text(encoding="utf-8")
    return {f"KB04-T-{kind}{num}" for kind, num in _ID_PATTERN.findall(text)}


def trace(contract_test_id: str) -> ContractTestTrace:
    """Gibt den Matrixeintrag einer Kennung zurueck."""
    for entry in CONTRACT_TEST_TRACEABILITY:
        if entry.contract_test_id == contract_test_id:
            return entry
    raise AssertionError(f"unbekannte Kennung: {contract_test_id}")


#: Verneinungen, die einer Abdeckungs- oder Bestehensbehauptung ihren
#: behauptenden Charakter nehmen.
_NEGATIONS = ("nicht", "niemals", "weder", "noch", "keine", "kein", "ohne")


def affirmative_claims(text: str, token: str) -> list[str]:
    """Fundstellen von *token*, denen **keine** Verneinung vorausgeht.

    Eine Formulierung wie *„weder als abgedeckt noch als bestanden"* ist
    ausdruecklich **keine** Behauptung; nur eine unverneinte Fundstelle
    waere eine.
    """
    lowered = text.lower()
    hits: list[str] = []
    for match in re.finditer(re.escape(token), lowered):
        window = lowered[max(0, match.start() - 60) : match.start()]
        if not any(negation in window for negation in _NEGATIONS):
            hits.append(lowered[max(0, match.start() - 60) : match.end()])
    return hits


def existing_test_ids() -> set[str]:
    """Deterministische Gesamtmenge der Testkennungen der sechs Module."""
    loader = unittest.TestLoader()
    found: set[str] = set()

    def walk(suite: unittest.TestSuite) -> None:
        for item in suite:
            if isinstance(item, unittest.TestSuite):
                walk(item)
            else:
                found.add(item.id())

    for module in ALLOWED_TEST_MODULES:
        walk(loader.loadTestsFromName(module))
    return found


class TestContractIdDrift(unittest.TestCase):
    """Die Matrix muss exakt der Kennungsmenge aus Contract §15 entsprechen."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.document_ids = contract_ids_from_document()
        cls.matrix_ids = {t.contract_test_id for t in CONTRACT_TEST_TRACEABILITY}

    def test_contract_document_exists(self) -> None:
        self.assertTrue(CONTRACT_DOCUMENT.is_file())

    def test_document_declares_exactly_fortyfive_ids(self) -> None:
        self.assertEqual(len(self.document_ids), 45)

    def test_document_declares_twelve_positive_ids(self) -> None:
        positives = {i for i in self.document_ids if "-P" in i}
        self.assertEqual(len(positives), 12)

    def test_document_declares_thirtythree_negative_ids(self) -> None:
        negatives = {i for i in self.document_ids if "-N" in i}
        self.assertEqual(len(negatives), 33)

    def test_positive_range_is_gapless(self) -> None:
        expected = {f"KB04-T-P{n:02d}" for n in range(1, 13)}
        self.assertEqual({i for i in self.document_ids if "-P" in i}, expected)

    def test_negative_range_is_gapless(self) -> None:
        expected = {f"KB04-T-N{n:02d}" for n in range(1, 34)}
        self.assertEqual({i for i in self.document_ids if "-N" in i}, expected)

    def test_matrix_has_fortyfive_entries(self) -> None:
        self.assertEqual(len(CONTRACT_TEST_TRACEABILITY), 45)

    def test_matrix_has_no_duplicate_id(self) -> None:
        ids = [t.contract_test_id for t in CONTRACT_TEST_TRACEABILITY]
        self.assertEqual(len(ids), len(set(ids)))

    def test_matrix_equals_document(self) -> None:
        self.assertEqual(self.matrix_ids, self.document_ids)

    def test_matrix_has_no_additional_id(self) -> None:
        self.assertEqual(self.matrix_ids - self.document_ids, set())

    def test_matrix_misses_no_document_id(self) -> None:
        self.assertEqual(self.document_ids - self.matrix_ids, set())

    def test_no_invented_id_shape(self) -> None:
        for entry in CONTRACT_TEST_TRACEABILITY:
            with self.subTest(contract_test_id=entry.contract_test_id):
                self.assertRegex(entry.contract_test_id, r"^KB04-T-[PN]\d{2}$")


class TestDisposition(unittest.TestCase):
    """Die kanonische Aufteilung 37 / 2 / 6 nach D-062."""

    def test_three_dispositions_exist(self) -> None:
        self.assertEqual(
            [d.value for d in TraceabilityDisposition],
            ["SYNTHETIC_COVERED", "SYNTHETIC_COVERAGE_GAP", "B2D_REAL_ONLY"],
        )

    def test_exactly_thirtyseven_covered(self) -> None:
        self.assertEqual(len(SYNTHETIC_COVERED_CONTRACT_TEST_IDS), 37)

    def test_exactly_two_coverage_gaps(self) -> None:
        self.assertEqual(len(SYNTHETIC_COVERAGE_GAP_CONTRACT_TEST_IDS), 2)

    def test_exactly_six_real_only(self) -> None:
        self.assertEqual(len(B2D_REAL_ONLY_CONTRACT_TEST_IDS), 6)

    def test_counts_sum_to_fortyfive(self) -> None:
        self.assertEqual(
            len(SYNTHETIC_COVERED_CONTRACT_TEST_IDS)
            + len(SYNTHETIC_COVERAGE_GAP_CONTRACT_TEST_IDS)
            + len(B2D_REAL_ONLY_CONTRACT_TEST_IDS),
            45,
        )

    def test_gap_set_is_exactly_p10_and_n25(self) -> None:
        self.assertEqual(
            set(SYNTHETIC_COVERAGE_GAP_CONTRACT_TEST_IDS),
            {"KB04-T-P10", "KB04-T-N25"},
        )

    def test_real_only_set_is_exactly_six_named_ids(self) -> None:
        self.assertEqual(
            set(B2D_REAL_ONLY_CONTRACT_TEST_IDS),
            {
                "KB04-T-N07",
                "KB04-T-N08",
                "KB04-T-N14",
                "KB04-T-N31",
                "KB04-T-N33",
                "KB04-T-P12",
            },
        )

    def test_no_other_id_is_a_gap(self) -> None:
        for entry in CONTRACT_TEST_TRACEABILITY:
            if entry.contract_test_id in {"KB04-T-P10", "KB04-T-N25"}:
                continue
            with self.subTest(contract_test_id=entry.contract_test_id):
                self.assertIsNot(
                    entry.disposition,
                    TraceabilityDisposition.SYNTHETIC_COVERAGE_GAP,
                )

    def test_no_other_id_is_real_only(self) -> None:
        allowed = set(B2D_REAL_ONLY_CONTRACT_TEST_IDS)
        for entry in CONTRACT_TEST_TRACEABILITY:
            if entry.contract_test_id in allowed:
                continue
            with self.subTest(contract_test_id=entry.contract_test_id):
                self.assertIsNot(
                    entry.disposition, TraceabilityDisposition.B2D_REAL_ONLY
                )

    def test_the_three_sets_are_disjoint(self) -> None:
        covered = set(SYNTHETIC_COVERED_CONTRACT_TEST_IDS)
        gaps = set(SYNTHETIC_COVERAGE_GAP_CONTRACT_TEST_IDS)
        real = set(B2D_REAL_ONLY_CONTRACT_TEST_IDS)
        self.assertEqual(covered & gaps, set())
        self.assertEqual(covered & real, set())
        self.assertEqual(gaps & real, set())

    def test_every_entry_carries_a_known_disposition(self) -> None:
        for entry in CONTRACT_TEST_TRACEABILITY:
            with self.subTest(contract_test_id=entry.contract_test_id):
                self.assertIsInstance(entry.disposition, TraceabilityDisposition)


class TestCoverageGapSemantics(unittest.TestCase):
    """P10 und N25 duerfen niemals als abgedeckt oder bestanden gelten."""

    def setUp(self) -> None:
        self.p10 = trace("KB04-T-P10")
        self.n25 = trace("KB04-T-N25")
        self.gaps = (self.p10, self.n25)

    def test_p10_is_a_coverage_gap(self) -> None:
        self.assertIs(
            self.p10.disposition, TraceabilityDisposition.SYNTHETIC_COVERAGE_GAP
        )

    def test_n25_is_a_coverage_gap(self) -> None:
        self.assertIs(
            self.n25.disposition, TraceabilityDisposition.SYNTHETIC_COVERAGE_GAP
        )

    def test_p10_has_no_covered_by(self) -> None:
        self.assertEqual(self.p10.covered_by, ())

    def test_n25_has_no_covered_by(self) -> None:
        self.assertEqual(self.n25.covered_by, ())

    def test_gaps_have_no_synthetic_support_tests(self) -> None:
        for entry in self.gaps:
            with self.subTest(contract_test_id=entry.contract_test_id):
                self.assertEqual(entry.synthetic_support_tests, ())

    def test_gaps_carry_a_non_empty_gap_description(self) -> None:
        for entry in self.gaps:
            with self.subTest(contract_test_id=entry.contract_test_id):
                self.assertTrue(entry.coverage_gap.strip())

    def test_gaps_name_contract_section_ten_three(self) -> None:
        for entry in self.gaps:
            with self.subTest(contract_test_id=entry.contract_test_id):
                self.assertEqual(entry.gap_contract_section, GAP_CONTRACT_SECTION)
                self.assertEqual(entry.gap_contract_section, "10.3")

    def test_gap_description_names_missing_write_time_validation(self) -> None:
        for entry in self.gaps:
            with self.subTest(contract_test_id=entry.contract_test_id):
                self.assertIn("Schreibzeitvalidierung", entry.coverage_gap)

    def test_gap_description_names_missing_functional_test(self) -> None:
        for entry in self.gaps:
            with self.subTest(contract_test_id=entry.contract_test_id):
                self.assertIn("kein funktionaler Test", entry.coverage_gap)

    def test_gap_description_excludes_root_boundary_substitution(self) -> None:
        for entry in self.gaps:
            with self.subTest(contract_test_id=entry.contract_test_id):
                self.assertIn("Root-Boundary", entry.coverage_gap)
                self.assertIn("unzulaessig", entry.coverage_gap)

    def test_gap_description_states_future_scope_release(self) -> None:
        for entry in self.gaps:
            with self.subTest(contract_test_id=entry.contract_test_id):
                self.assertIn("Scopefreigabe", entry.coverage_gap)

    def test_gaps_stay_synthetically_testable(self) -> None:
        for entry in self.gaps:
            with self.subTest(contract_test_id=entry.contract_test_id):
                self.assertIn("synthetisch testbar", entry.coverage_gap)

    def test_gaps_are_not_real_only(self) -> None:
        for entry in self.gaps:
            with self.subTest(contract_test_id=entry.contract_test_id):
                self.assertEqual(entry.b2d_target, "")
                self.assertEqual(entry.real_scope, "")
                self.assertEqual(entry.required_execution_origin, "")

    def test_n25_names_the_write_contract_reason_code(self) -> None:
        self.assertEqual(self.n25.gap_reason_code, "KB04-WRITE-CONTRACT-VIOLATION")

    def test_p10_carries_no_invented_reason_code(self) -> None:
        self.assertEqual(self.p10.gap_reason_code, "")

    def test_gaps_make_no_affirmative_pass_claim(self) -> None:
        forbidden = ("bestanden", "abgedeckt", "erfuellt", "verified", "passed")
        for entry in self.gaps:
            text = f"{entry.coverage_note} {entry.coverage_gap}"
            for token in forbidden:
                with self.subTest(
                    contract_test_id=entry.contract_test_id, token=token
                ):
                    self.assertEqual(affirmative_claims(text, token), [])

    def test_gaps_explicitly_deny_coverage(self) -> None:
        for entry in self.gaps:
            with self.subTest(contract_test_id=entry.contract_test_id):
                self.assertIn("Nicht abgedeckt", entry.coverage_note)
                self.assertIn("noch als bestanden", entry.coverage_note)

    def test_gaps_stay_visible_in_the_matrix(self) -> None:
        ids = {t.contract_test_id for t in CONTRACT_TEST_TRACEABILITY}
        self.assertIn("KB04-T-P10", ids)
        self.assertIn("KB04-T-N25", ids)

    def test_only_gaps_carry_a_gap_section(self) -> None:
        for entry in CONTRACT_TEST_TRACEABILITY:
            if entry.disposition is TraceabilityDisposition.SYNTHETIC_COVERAGE_GAP:
                continue
            with self.subTest(contract_test_id=entry.contract_test_id):
                self.assertEqual(entry.gap_contract_section, "")
                self.assertEqual(entry.gap_reason_code, "")
                self.assertEqual(entry.coverage_gap, "")


class TestTestIdExistence(unittest.TestCase):
    """Jede referenzierte Testkennung muss tatsaechlich existieren."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.inventory = existing_test_ids()

    def test_inventory_is_not_empty(self) -> None:
        self.assertTrue(self.inventory)

    def test_every_covered_by_id_exists(self) -> None:
        for entry in CONTRACT_TEST_TRACEABILITY:
            for test_id in entry.covered_by:
                with self.subTest(
                    contract_test_id=entry.contract_test_id, test_id=test_id
                ):
                    self.assertIn(test_id, self.inventory)

    def test_every_support_test_id_exists(self) -> None:
        for entry in CONTRACT_TEST_TRACEABILITY:
            for test_id in entry.synthetic_support_tests:
                with self.subTest(
                    contract_test_id=entry.contract_test_id, test_id=test_id
                ):
                    self.assertIn(test_id, self.inventory)

    def test_every_reference_uses_an_allowed_module(self) -> None:
        for entry in CONTRACT_TEST_TRACEABILITY:
            for test_id in entry.covered_by + entry.synthetic_support_tests:
                with self.subTest(test_id=test_id):
                    self.assertTrue(
                        any(test_id.startswith(m + ".") for m in ALLOWED_TEST_MODULES)
                    )

    def test_no_reference_to_the_new_traceability_module(self) -> None:
        for entry in CONTRACT_TEST_TRACEABILITY:
            for test_id in entry.covered_by + entry.synthetic_support_tests:
                with self.subTest(test_id=test_id):
                    self.assertFalse(test_id.startswith(NEW_MODULES[0]))

    def test_no_reference_to_the_new_preparation_module(self) -> None:
        for entry in CONTRACT_TEST_TRACEABILITY:
            for test_id in entry.covered_by + entry.synthetic_support_tests:
                with self.subTest(test_id=test_id):
                    self.assertFalse(test_id.startswith(NEW_MODULES[1]))

    def test_references_are_fully_qualified(self) -> None:
        for entry in CONTRACT_TEST_TRACEABILITY:
            for test_id in entry.covered_by + entry.synthetic_support_tests:
                with self.subTest(test_id=test_id):
                    self.assertGreaterEqual(len(test_id.split(".")), 4)

    def test_no_reference_to_a_nonexistent_test(self) -> None:
        referenced: set[str] = set()
        for entry in CONTRACT_TEST_TRACEABILITY:
            referenced.update(entry.covered_by)
            referenced.update(entry.synthetic_support_tests)
        self.assertEqual(referenced - self.inventory, set())


class TestCoverageRules(unittest.TestCase):
    """Strukturelle Regeln je Disposition."""

    def test_every_covered_entry_has_at_least_one_test(self) -> None:
        for entry in CONTRACT_TEST_TRACEABILITY:
            if entry.disposition is not TraceabilityDisposition.SYNTHETIC_COVERED:
                continue
            with self.subTest(contract_test_id=entry.contract_test_id):
                self.assertGreaterEqual(len(entry.covered_by), 1)

    def test_covered_entries_have_no_support_tests(self) -> None:
        for entry in CONTRACT_TEST_TRACEABILITY:
            if entry.disposition is not TraceabilityDisposition.SYNTHETIC_COVERED:
                continue
            with self.subTest(contract_test_id=entry.contract_test_id):
                self.assertEqual(entry.synthetic_support_tests, ())

    def test_covered_entries_carry_no_b2d_fields(self) -> None:
        for entry in CONTRACT_TEST_TRACEABILITY:
            if entry.disposition is not TraceabilityDisposition.SYNTHETIC_COVERED:
                continue
            with self.subTest(contract_test_id=entry.contract_test_id):
                self.assertEqual(entry.b2d_target, "")
                self.assertEqual(entry.real_scope, "")

    def test_real_only_entries_have_no_covered_by(self) -> None:
        for entry in CONTRACT_TEST_TRACEABILITY:
            if entry.disposition is not TraceabilityDisposition.B2D_REAL_ONLY:
                continue
            with self.subTest(contract_test_id=entry.contract_test_id):
                self.assertEqual(entry.covered_by, ())

    def test_real_only_entries_carry_a_b2d_target(self) -> None:
        for entry in CONTRACT_TEST_TRACEABILITY:
            if entry.disposition is not TraceabilityDisposition.B2D_REAL_ONLY:
                continue
            with self.subTest(contract_test_id=entry.contract_test_id):
                self.assertTrue(entry.b2d_target.strip())

    def test_real_only_entries_carry_a_real_scope(self) -> None:
        for entry in CONTRACT_TEST_TRACEABILITY:
            if entry.disposition is not TraceabilityDisposition.B2D_REAL_ONLY:
                continue
            with self.subTest(contract_test_id=entry.contract_test_id):
                self.assertTrue(entry.real_scope.strip())

    def test_real_only_entries_require_observed_execution(self) -> None:
        for entry in CONTRACT_TEST_TRACEABILITY:
            if entry.disposition is not TraceabilityDisposition.B2D_REAL_ONLY:
                continue
            with self.subTest(contract_test_id=entry.contract_test_id):
                self.assertIn("OBSERVED", entry.required_execution_origin)

    def test_p12_names_dimension_d_one(self) -> None:
        p12 = trace("KB04-T-P12")
        self.assertIn("D-I", p12.real_scope)

    def test_p12_support_tests_are_not_coverage(self) -> None:
        p12 = trace("KB04-T-P12")
        self.assertEqual(p12.covered_by, ())
        self.assertTrue(p12.synthetic_support_tests)

    def test_no_real_only_entry_is_called_passed(self) -> None:
        forbidden = ("bestanden", "abgedeckt", "passed", "verified")
        for entry in CONTRACT_TEST_TRACEABILITY:
            if entry.disposition is not TraceabilityDisposition.B2D_REAL_ONLY:
                continue
            text = f"{entry.coverage_note} {entry.real_scope}"
            for token in forbidden:
                with self.subTest(
                    contract_test_id=entry.contract_test_id, token=token
                ):
                    self.assertEqual(affirmative_claims(text, token), [])

    def test_every_real_only_entry_denies_a_pass(self) -> None:
        for entry in CONTRACT_TEST_TRACEABILITY:
            if entry.disposition is not TraceabilityDisposition.B2D_REAL_ONLY:
                continue
            with self.subTest(contract_test_id=entry.contract_test_id):
                self.assertIn("bestanden", entry.coverage_note)
                self.assertEqual(
                    affirmative_claims(entry.coverage_note, "bestanden"), []
                )

    def test_every_entry_has_a_non_empty_coverage_note(self) -> None:
        for entry in CONTRACT_TEST_TRACEABILITY:
            with self.subTest(contract_test_id=entry.contract_test_id):
                self.assertTrue(entry.coverage_note.strip())

    def test_every_entry_has_a_non_empty_title(self) -> None:
        for entry in CONTRACT_TEST_TRACEABILITY:
            with self.subTest(contract_test_id=entry.contract_test_id):
                self.assertTrue(entry.contract_title.strip())

    def test_no_circular_self_evidence(self) -> None:
        own_module = "tests.kb04_nt_fixtures"
        for entry in CONTRACT_TEST_TRACEABILITY:
            for test_id in entry.covered_by + entry.synthetic_support_tests:
                with self.subTest(test_id=test_id):
                    self.assertFalse(test_id.startswith(own_module))

    def test_multi_assignment_is_justified(self) -> None:
        seen: dict[str, list[str]] = {}
        for entry in CONTRACT_TEST_TRACEABILITY:
            for test_id in entry.covered_by:
                seen.setdefault(test_id, []).append(entry.contract_test_id)
        for test_id, owners in seen.items():
            if len(owners) < 2:
                continue
            for owner in owners:
                with self.subTest(test_id=test_id, contract_test_id=owner):
                    note = trace(owner).coverage_note
                    self.assertGreaterEqual(len(note.strip()), 40)


class TestDeterminism(unittest.TestCase):
    """Die Serialisierung muss byte-stabil und umgebungsfrei sein."""

    def test_manifest_covers_all_fortyfive_entries(self) -> None:
        self.assertEqual(len(traceability_manifest_dict()["entries"]), 45)

    def test_manifest_entries_are_sorted(self) -> None:
        ids = [e["contract_test_id"] for e in traceability_manifest_dict()["entries"]]
        self.assertEqual(ids, sorted(ids))

    def test_manifest_ids_are_unique(self) -> None:
        ids = [e["contract_test_id"] for e in traceability_manifest_dict()["entries"]]
        self.assertEqual(len(ids), len(set(ids)))

    def test_manifest_counts_match_the_split(self) -> None:
        counts = traceability_manifest_dict()["counts"]
        self.assertEqual(counts["synthetic_covered"], 37)
        self.assertEqual(counts["synthetic_coverage_gap"], 2)
        self.assertEqual(counts["b2d_real_only"], 6)
        self.assertEqual(counts["total"], 45)

    def test_manifest_is_equal_across_calls(self) -> None:
        self.assertEqual(traceability_manifest_dict(), traceability_manifest_dict())

    def test_hash_is_stable_across_calls(self) -> None:
        self.assertEqual(traceability_manifest_sha256(), traceability_manifest_sha256())

    def test_hash_is_hex64(self) -> None:
        self.assertRegex(traceability_manifest_sha256(), r"^[0-9a-f]{64}$")

    def test_serialization_is_byte_identical(self) -> None:
        def blob() -> bytes:
            return json.dumps(
                traceability_manifest_dict(),
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
            ).encode("utf-8")

        self.assertEqual(blob(), blob())

    def test_serialization_has_no_absolute_posix_path(self) -> None:
        blob = json.dumps(traceability_manifest_dict(), ensure_ascii=False)
        self.assertNotIn("/home/", blob)
        self.assertNotIn("/root/", blob)
        self.assertNotIn("/Users/", blob)

    def test_serialization_has_no_drive_letter(self) -> None:
        blob = json.dumps(traceability_manifest_dict(), ensure_ascii=False)
        for letter in ("C:", "D:", "\\\\"):
            with self.subTest(token=letter):
                self.assertNotIn(letter, blob)

    def test_serialization_has_no_repository_path(self) -> None:
        blob = json.dumps(traceability_manifest_dict(), ensure_ascii=False)
        self.assertNotIn(str(REPO_ROOT), blob)
        self.assertNotIn(REPO_ROOT.name, blob)

    def test_serialization_has_no_temporary_path(self) -> None:
        blob = json.dumps(traceability_manifest_dict(), ensure_ascii=False).lower()
        for token in ("/tmp", "temp\\", "appdata", "pytest-"):
            with self.subTest(token=token):
                self.assertNotIn(token, blob)

    def test_entry_keys_are_stable(self) -> None:
        for entry in traceability_manifest_dict()["entries"]:
            with self.subTest(contract_test_id=entry["contract_test_id"]):
                self.assertEqual(
                    sorted(entry),
                    [
                        "b2d_target",
                        "contract_test_id",
                        "contract_title",
                        "coverage_gap",
                        "coverage_note",
                        "covered_by",
                        "disposition",
                        "gap_contract_section",
                        "gap_reason_code",
                        "real_scope",
                        "required_execution_origin",
                        "synthetic_support_tests",
                    ],
                )

    def test_matrix_entries_are_frozen(self) -> None:
        with self.assertRaises(Exception):
            CONTRACT_TEST_TRACEABILITY[0].disposition = None  # type: ignore[misc]

    def test_manifest_writes_no_file(self) -> None:
        before = sorted(p.name for p in (REPO_ROOT / "tests").iterdir())
        traceability_manifest_sha256()
        after = sorted(p.name for p in (REPO_ROOT / "tests").iterdir())
        self.assertEqual(before, after)


class TestExistingTestBase(unittest.TestCase):
    """Die vorhandene Testbasis bleibt unangetastet."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.inventory = existing_test_ids()

    def test_six_allowed_modules_are_declared(self) -> None:
        self.assertEqual(len(ALLOWED_TEST_MODULES), 6)

    def test_allowed_modules_hold_at_least_326_tests(self) -> None:
        self.assertGreaterEqual(len(self.inventory), 326)

    def test_matrix_does_not_claim_every_test_is_mapped(self) -> None:
        mapped: set[str] = set()
        for entry in CONTRACT_TEST_TRACEABILITY:
            mapped.update(entry.covered_by)
            mapped.update(entry.synthetic_support_tests)
        self.assertLess(len(mapped), len(self.inventory))

    def test_matrix_maps_a_meaningful_share(self) -> None:
        mapped: set[str] = set()
        for entry in CONTRACT_TEST_TRACEABILITY:
            mapped.update(entry.covered_by)
        self.assertGreaterEqual(len(mapped), 37)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
