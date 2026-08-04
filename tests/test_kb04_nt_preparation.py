"""Tests der KB-04-NT-Vorbereitungsfixtures (CBP-WP-022, Phase B2C-T-R).

Die sechs Fixtures sind **deklarative Vorbereitungen** der ausschliesslich
real pruefbaren Faelle. Sie werden **niemals ausgefuehrt** und **niemals als
bestanden** ausgegeben.

**Es wird weder NT-04 noch NT-05 ausgefuehrt.** Kein Test erzeugt Evidenz,
oeffnet einen Mount, ruft ``chmod`` oder ``chown`` auf, startet einen
Subprozess oder schreibt in das Dateisystem.
"""

from __future__ import annotations

import pathlib
import unittest

from core.core_brain.errors import ReasonCode
from tests.kb04_nt_fixtures import (
    B2D_REAL_ONLY_CONTRACT_TEST_IDS,
    B2D_TARGET,
    CONTRACT_DOES_NOT_SPECIFY,
    CONTRACT_TEST_TRACEABILITY,
    REAL_ONLY_PREPARATIONS,
    ExecutionStatus,
    PreparationStatus,
    RealOnlyPreparation,
)

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE_SOURCE = REPO_ROOT / "tests" / "kb04_nt_fixtures.py"

#: Alle 24 registrierten KB04-ReasonCode-Werte.
KB04_CODES = {c.value for c in ReasonCode if c.value.startswith("KB04-")}


def prep(contract_test_id: str) -> RealOnlyPreparation:
    """Gibt die Vorbereitung einer Kennung zurueck."""
    for item in REAL_ONLY_PREPARATIONS:
        if item.contract_test_id == contract_test_id:
            return item
    raise AssertionError(f"keine Vorbereitung fuer {contract_test_id}")


class TestFixtureCompleteness(unittest.TestCase):
    """Genau sechs Vorbereitungen fuer genau die sechs real-only Faelle."""

    def test_exactly_six_preparations(self) -> None:
        self.assertEqual(len(REAL_ONLY_PREPARATIONS), 6)

    def test_preparations_match_the_real_only_set(self) -> None:
        self.assertEqual(
            {p.contract_test_id for p in REAL_ONLY_PREPARATIONS},
            set(B2D_REAL_ONLY_CONTRACT_TEST_IDS),
        )

    def test_no_duplicate_preparation(self) -> None:
        ids = [p.contract_test_id for p in REAL_ONLY_PREPARATIONS]
        self.assertEqual(len(ids), len(set(ids)))

    def test_no_additional_contract_id(self) -> None:
        allowed = set(B2D_REAL_ONLY_CONTRACT_TEST_IDS)
        for item in REAL_ONLY_PREPARATIONS:
            with self.subTest(contract_test_id=item.contract_test_id):
                self.assertIn(item.contract_test_id, allowed)

    def test_every_real_only_case_has_a_preparation(self) -> None:
        prepared = {p.contract_test_id for p in REAL_ONLY_PREPARATIONS}
        for contract_test_id in B2D_REAL_ONLY_CONTRACT_TEST_IDS:
            with self.subTest(contract_test_id=contract_test_id):
                self.assertIn(contract_test_id, prepared)

    def test_no_gap_case_has_a_preparation(self) -> None:
        prepared = {p.contract_test_id for p in REAL_ONLY_PREPARATIONS}
        self.assertNotIn("KB04-T-P10", prepared)
        self.assertNotIn("KB04-T-N25", prepared)

    def test_preparations_are_frozen(self) -> None:
        with self.assertRaises(Exception):
            REAL_ONLY_PREPARATIONS[0].related_nt = "changed"  # type: ignore[misc]


class TestStatementBoundaries(unittest.TestCase):
    """Aussagegrenzen jedes einzelnen Fixtures."""

    def test_status_enums_have_exactly_one_value(self) -> None:
        self.assertEqual([s.value for s in PreparationStatus], ["PREPARED_ONLY"])
        self.assertEqual([s.value for s in ExecutionStatus], ["NOT_EXECUTED"])

    def test_every_preparation_is_prepared_only(self) -> None:
        for item in REAL_ONLY_PREPARATIONS:
            with self.subTest(contract_test_id=item.contract_test_id):
                self.assertIs(
                    item.preparation_status, PreparationStatus.PREPARED_ONLY
                )

    def test_every_preparation_is_not_executed(self) -> None:
        for item in REAL_ONLY_PREPARATIONS:
            with self.subTest(contract_test_id=item.contract_test_id):
                self.assertIs(item.execution_status, ExecutionStatus.NOT_EXECUTED)

    def test_preparation_origin_is_synthetic(self) -> None:
        for item in REAL_ONLY_PREPARATIONS:
            with self.subTest(contract_test_id=item.contract_test_id):
                self.assertEqual(item.preparation_origin, "SYNTHETIC")

    def test_required_execution_origin_is_observed(self) -> None:
        for item in REAL_ONLY_PREPARATIONS:
            with self.subTest(contract_test_id=item.contract_test_id):
                self.assertIn("OBSERVED", item.required_execution_origin)

    def test_required_execution_needs_a_real_instance(self) -> None:
        for item in REAL_ONLY_PREPARATIONS:
            with self.subTest(contract_test_id=item.contract_test_id):
                self.assertIn("Profil-A", item.required_execution_origin)

    def test_no_passed_field_exists(self) -> None:
        for name in ("passed", "conform", "operationally_verified", "verified"):
            with self.subTest(field=name):
                self.assertNotIn(name, RealOnlyPreparation.__slots__)

    def test_no_field_claims_operational_success(self) -> None:
        for item in REAL_ONLY_PREPARATIONS:
            blob = " ".join(item.to_dict().get(k, "") for k in ("real_scope",))
            with self.subTest(contract_test_id=item.contract_test_id):
                self.assertNotIn("bestanden", blob.lower())

    def test_forbidden_claims_reject_gate_fulfilment(self) -> None:
        for item in REAL_ONLY_PREPARATIONS:
            with self.subTest(contract_test_id=item.contract_test_id):
                self.assertIn("dass ein Gate erfuellt ist", item.forbidden_claims)

    def test_forbidden_claims_reject_control_uplift(self) -> None:
        for item in REAL_ONLY_PREPARATIONS:
            with self.subTest(contract_test_id=item.contract_test_id):
                self.assertIn(
                    "dass eine Control hochgestuft werden darf",
                    item.forbidden_claims,
                )

    def test_forbidden_claims_keep_kb04_documented_only(self) -> None:
        for item in REAL_ONLY_PREPARATIONS:
            with self.subTest(contract_test_id=item.contract_test_id):
                self.assertIn(
                    "dass KB-04 den Status DOCUMENTED ONLY verlaesst",
                    item.forbidden_claims,
                )

    def test_forbidden_claims_reject_preparation_as_evidence(self) -> None:
        for item in REAL_ONLY_PREPARATIONS:
            with self.subTest(contract_test_id=item.contract_test_id):
                self.assertIn(
                    "dass eine Vorbereitung ein Nachweis ist",
                    item.forbidden_claims,
                )

    def test_every_preparation_carries_preconditions(self) -> None:
        for item in REAL_ONLY_PREPARATIONS:
            with self.subTest(contract_test_id=item.contract_test_id):
                self.assertGreaterEqual(len(item.preconditions), 2)

    def test_every_preparation_carries_execution_steps(self) -> None:
        for item in REAL_ONLY_PREPARATIONS:
            with self.subTest(contract_test_id=item.contract_test_id):
                self.assertGreaterEqual(len(item.execution_steps_summary), 2)

    def test_every_preparation_carries_a_success_condition(self) -> None:
        for item in REAL_ONLY_PREPARATIONS:
            with self.subTest(contract_test_id=item.contract_test_id):
                self.assertTrue(item.success_condition.strip())

    def test_every_preparation_targets_b2d(self) -> None:
        for item in REAL_ONLY_PREPARATIONS:
            with self.subTest(contract_test_id=item.contract_test_id):
                self.assertEqual(item.b2d_target, B2D_TARGET)


class TestNtAssignment(unittest.TestCase):
    """NT-Zuordnung strikt nach Contract §15 und §16."""

    def test_n07_belongs_to_nt_04(self) -> None:
        self.assertEqual(prep("KB04-T-N07").related_nt, "NT-04")

    def test_n08_belongs_to_nt_04(self) -> None:
        self.assertEqual(prep("KB04-T-N08").related_nt, "NT-04")

    def test_n14_belongs_to_nt_05(self) -> None:
        self.assertEqual(prep("KB04-T-N14").related_nt, "NT-05")

    def test_n31_declares_no_nt_reference(self) -> None:
        self.assertEqual(
            prep("KB04-T-N31").related_nt, "CONTRACT_DECLARES_NO_NT_REFERENCE"
        )

    def test_n33_declares_no_nt_reference(self) -> None:
        self.assertEqual(
            prep("KB04-T-N33").related_nt, "CONTRACT_DECLARES_NO_NT_REFERENCE"
        )

    def test_p12_declares_no_nt_reference(self) -> None:
        self.assertEqual(
            prep("KB04-T-P12").related_nt, "CONTRACT_DECLARES_NO_NT_REFERENCE"
        )

    def test_only_three_cases_carry_an_nt(self) -> None:
        with_nt = {
            p.contract_test_id
            for p in REAL_ONLY_PREPARATIONS
            if p.related_nt.startswith("NT-")
        }
        self.assertEqual(with_nt, {"KB04-T-N07", "KB04-T-N08", "KB04-T-N14"})

    def test_no_nt_execution_is_claimed(self) -> None:
        for item in REAL_ONLY_PREPARATIONS:
            with self.subTest(contract_test_id=item.contract_test_id):
                self.assertIs(item.execution_status, ExecutionStatus.NOT_EXECUTED)

    def test_no_nt_beyond_04_and_05_is_referenced(self) -> None:
        for item in REAL_ONLY_PREPARATIONS:
            if not item.related_nt.startswith("NT-"):
                continue
            with self.subTest(contract_test_id=item.contract_test_id):
                self.assertIn(item.related_nt, {"NT-04", "NT-05"})


class TestRealityBoundary(unittest.TestCase):
    """Kein Fixture nennt oder beruehrt reale Infrastruktur."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.blob = " ".join(
            str(value)
            for item in REAL_ONLY_PREPARATIONS
            for value in item.to_dict().values()
        )
        cls.source = FIXTURE_SOURCE.read_text(encoding="utf-8")

    def test_no_absolute_host_path(self) -> None:
        for token in ("/home/", "/root/", "/Users/", "/mnt/", "/media/"):
            with self.subTest(token=token):
                self.assertNotIn(token, self.blob)

    def test_no_drive_letter_or_unc_path(self) -> None:
        self.assertNotRegex(self.blob, r"[A-Za-z]:[\\/]{1,2}[A-Za-z]")
        self.assertNotIn("\\\\", self.blob)

    def test_no_numeric_uid_or_gid(self) -> None:
        self.assertNotRegex(self.blob, r"(?i)\b(uid|gid)\s*[=:]\s*\d+")

    def test_no_user_or_group_account_name(self) -> None:
        for token in (" root ", "administrator", "sudo", "wheel"):
            with self.subTest(token=token):
                self.assertNotIn(token, self.blob.lower())

    def test_no_host_or_node_name(self) -> None:
        for token in ("pve", "proxmox", "synology", "unifi", "nas"):
            with self.subTest(token=token):
                self.assertNotIn(token, self.blob.lower())

    def test_no_ip_address(self) -> None:
        self.assertNotRegex(self.blob, r"\b(\d{1,3}\.){3}\d{1,3}\b")

    def test_no_url_or_domain(self) -> None:
        self.assertNotIn("http://", self.blob)
        self.assertNotIn("https://", self.blob)

    def test_no_secret_or_token(self) -> None:
        for token in ("password", "api_key", "private key", "bearer "):
            with self.subTest(token=token):
                self.assertNotIn(token, self.blob.lower())

    def test_source_has_no_mount_or_permission_call(self) -> None:
        for token in ("chmod(", "chown(", "mount(", "umask("):
            with self.subTest(token=token):
                self.assertNotIn(token, self.source)

    def test_source_has_no_subprocess_or_shell(self) -> None:
        for token in ("subprocess", "os.system", "popen", "shutil"):
            with self.subTest(token=token):
                self.assertNotIn(token, self.source.lower())

    def test_source_has_no_filesystem_write(self) -> None:
        for token in (
            "write_text(",
            "write_bytes(",
            "mkdir(",
            "touch(",
            "unlink(",
            "open(",
        ):
            with self.subTest(token=token):
                self.assertNotIn(token, self.source)

    def test_source_imports_no_production_enforcement_module(self) -> None:
        self.assertNotIn("core.core_brain", self.source)

    def test_importing_the_fixtures_creates_nothing(self) -> None:
        before = sorted(p.name for p in (REPO_ROOT / "tests").iterdir())
        import tests.kb04_nt_fixtures as reimported  # noqa: F401

        after = sorted(p.name for p in (REPO_ROOT / "tests").iterdir())
        self.assertEqual(before, after)


class TestContractFidelity(unittest.TestCase):
    """Inhalte stammen aus dem Contract, nichts wird erfunden."""

    def test_expected_reason_codes_are_registered(self) -> None:
        for item in REAL_ONLY_PREPARATIONS:
            for code in item.expected_reason_codes:
                with self.subTest(
                    contract_test_id=item.contract_test_id, code=code
                ):
                    self.assertIn(code, KB04_CODES)

    def test_exactly_twentyfour_kb04_codes_exist(self) -> None:
        self.assertEqual(len(KB04_CODES), 24)

    def test_no_new_reason_code_is_introduced(self) -> None:
        used = {
            code
            for item in REAL_ONLY_PREPARATIONS
            for code in item.expected_reason_codes
        }
        self.assertEqual(used - KB04_CODES, set())

    def test_every_preparation_expects_at_least_one_code(self) -> None:
        for item in REAL_ONLY_PREPARATIONS:
            with self.subTest(contract_test_id=item.contract_test_id):
                self.assertGreaterEqual(len(item.expected_reason_codes), 1)

    def test_n14_expects_the_symlink_escape_code(self) -> None:
        self.assertEqual(
            prep("KB04-T-N14").expected_reason_codes,
            ("KB04-LINK-SYMLINK-ESCAPE",),
        )

    def test_n33_expects_the_mode_mismatch_code(self) -> None:
        self.assertEqual(
            prep("KB04-T-N33").expected_reason_codes, ("KB04-MODE-MISMATCH",)
        )

    def test_n08_mirrors_n07_reason_codes(self) -> None:
        self.assertEqual(
            prep("KB04-T-N08").expected_reason_codes,
            prep("KB04-T-N07").expected_reason_codes,
        )

    def test_required_profiles_come_from_the_contract(self) -> None:
        expected = {
            "KB04-T-N07": "PP-3a",
            "KB04-T-N08": "PP-3a",
            "KB04-T-N14": "PP-1",
            "KB04-T-N31": "PP-3b",
            "KB04-T-N33": "PP-3b",
            "KB04-T-P12": "PP-3b",
        }
        for contract_test_id, profile in expected.items():
            with self.subTest(contract_test_id=contract_test_id):
                self.assertEqual(prep(contract_test_id).required_profile, profile)

    def test_titles_match_the_traceability_matrix(self) -> None:
        titles = {
            t.contract_test_id: t.contract_title for t in CONTRACT_TEST_TRACEABILITY
        }
        for item in REAL_ONLY_PREPARATIONS:
            with self.subTest(contract_test_id=item.contract_test_id):
                self.assertIn(
                    item.contract_title.split(" — ")[0],
                    titles[item.contract_test_id],
                )

    def test_unspecified_dimensions_use_the_neutral_marker(self) -> None:
        for contract_test_id in ("KB04-T-N07", "KB04-T-N08", "KB04-T-N14"):
            with self.subTest(contract_test_id=contract_test_id):
                self.assertEqual(
                    prep(contract_test_id).required_dimensions,
                    (CONTRACT_DOES_NOT_SPECIFY,),
                )

    def test_specified_dimensions_are_contract_grounded(self) -> None:
        self.assertEqual(prep("KB04-T-N31").required_dimensions, ("D-III",))
        self.assertEqual(prep("KB04-T-N33").required_dimensions, ("D-II", "D-III"))
        self.assertEqual(prep("KB04-T-P12").required_dimensions, ("D-I",))

    def test_declared_dimensions_are_valid_names(self) -> None:
        valid = {"D-I", "D-II", "D-III", "D-IV", CONTRACT_DOES_NOT_SPECIFY}
        for item in REAL_ONLY_PREPARATIONS:
            for dimension in item.required_dimensions:
                with self.subTest(
                    contract_test_id=item.contract_test_id, dimension=dimension
                ):
                    self.assertIn(dimension, valid)

    def test_no_invented_nt_identifier(self) -> None:
        allowed = {"NT-04", "NT-05", "CONTRACT_DECLARES_NO_NT_REFERENCE"}
        for item in REAL_ONLY_PREPARATIONS:
            with self.subTest(contract_test_id=item.contract_test_id):
                self.assertIn(item.related_nt, allowed)
                if item.related_nt.startswith("NT-"):
                    self.assertRegex(item.related_nt, r"^NT-0[45]$")


class TestSingleRealOnlyCases(unittest.TestCase):
    """Eigenstaendige Pruefung jedes der sechs real-only Faelle."""

    def test_n07_write_attempt_fails_on_os_level(self) -> None:
        item = prep("KB04-T-N07")
        self.assertIn("Betriebssystemebene", item.success_condition)
        self.assertIn("dass KB-03 vollstaendig ist", item.forbidden_claims)
        self.assertIs(item.execution_status, ExecutionStatus.NOT_EXECUTED)

    def test_n08_uncontrolled_ingest_write_fails(self) -> None:
        item = prep("KB04-T-N08")
        self.assertIn("Betriebssystemebene", item.success_condition)
        self.assertIn("dass andere Bereiche geschuetzt sind", item.forbidden_claims)
        self.assertIs(item.execution_status, ExecutionStatus.NOT_EXECUTED)

    def test_n14_resolution_is_refused_not_followed(self) -> None:
        item = prep("KB04-T-N14")
        self.assertIn("verweigert", item.success_condition)
        self.assertIn("dass Hardlinks abgedeckt sind", item.forbidden_claims)
        self.assertIn("dass TOCTOU geloest ist", item.forbidden_claims)

    def test_n31_runtime_write_capability_is_proven_negatively(self) -> None:
        item = prep("KB04-T-N31")
        self.assertIn("negativ zu belegen", item.success_condition)
        self.assertEqual(item.required_dimensions, ("D-III",))

    def test_n33_bundle_mode_is_not_accepted_automatically(self) -> None:
        item = prep("KB04-T-N33")
        self.assertIn("MT-9", item.success_condition)
        self.assertIn(
            "dass der Bundlemodus allein den sichtbaren Zustand belegt",
            item.forbidden_claims,
        )

    def test_p12_keeps_dimension_d_one_open(self) -> None:
        item = prep("KB04-T-P12")
        self.assertEqual(item.required_dimensions, ("D-I",))
        self.assertIn("offen auszuweisen", item.success_condition)

    def test_p12_is_never_declared_passed(self) -> None:
        item = prep("KB04-T-P12")
        self.assertIn("dass KB04-T-P12 bestanden ist", item.forbidden_claims)

    def test_p12_support_tests_are_not_a_full_proof(self) -> None:
        item = prep("KB04-T-P12")
        self.assertTrue(item.synthetic_support_tests)
        self.assertIn("dass D-III den Zustand von D-I belegt", item.forbidden_claims)

    def test_p12_stays_real_only_in_the_matrix(self) -> None:
        self.assertIn("KB04-T-P12", B2D_REAL_ONLY_CONTRACT_TEST_IDS)

    def test_only_p12_carries_support_tests(self) -> None:
        with_support = {
            p.contract_test_id
            for p in REAL_ONLY_PREPARATIONS
            if p.synthetic_support_tests
        }
        self.assertEqual(with_support, {"KB04-T-P12"})


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
