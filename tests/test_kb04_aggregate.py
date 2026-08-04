"""Tests der fail-closed Befundaggregation (CBP-WP-022, Phase B2A).

Der Kern dieser Tests ist die Trennung von **logischer** Konformität und
**operativer** Verifikation: eine synthetische oder deklarierte Beobachtung
darf niemals ``operationally_verified`` erzeugen.
"""

from __future__ import annotations

import hashlib
import pathlib
import unittest
from dataclasses import replace

from core.core_brain.enforcement import contract as c
from core.core_brain.enforcement import validator as v
from core.core_brain.enforcement.aggregate import (
    REQUIRED_DIMENSIONS,
    Finding,
    FindingStatus,
    aggregate_findings,
    canonical_json_bytes,
)
from core.core_brain.errors import ReasonCode
from tests.kb04_fixtures import (
    binding_for,
    conforming_observation,
    host_state,
    observed_everything,
)

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]


def finding(
    dimension: str,
    status: FindingStatus,
    *,
    origin: str | None = "OBSERVED",
    required: bool = True,
    path: str = "a.json",
) -> Finding:
    """Baut einen minimalen Befund."""
    return Finding(
        path_class=c.PathClass.PC_03,
        relative_path=path,
        dimension=dimension,
        status=status,
        reason=None if status is FindingStatus.CONFORM else ReasonCode.KB04_MODE_MISMATCH,
        detail="",
        origin=origin,
        required=required,
    )


def all_conform(origin: str = "OBSERVED") -> list[Finding]:
    """Baut vier konforme Befunde, einen je Dimension."""
    return [finding(d, FindingStatus.CONFORM, origin=origin) for d in REQUIRED_DIMENSIONS]


class TestAggregationBasics(unittest.TestCase):
    def test_four_required_dimensions(self) -> None:
        self.assertEqual(REQUIRED_DIMENSIONS, ("D-I", "D-II", "D-III", "D-IV"))

    def test_all_conform_is_conform(self) -> None:
        result = aggregate_findings(all_conform())
        self.assertTrue(result.conform)
        self.assertEqual(result.violation_count, 0)
        self.assertEqual(result.indeterminate_count, 0)
        self.assertEqual(result.conform_count, 4)

    def test_empty_input_is_not_conform(self) -> None:
        result = aggregate_findings([])
        self.assertFalse(result.conform)
        self.assertFalse(result.operationally_verified)

    def test_single_violation_prevents_pass(self) -> None:
        findings = all_conform()
        findings[1] = finding("D-II", FindingStatus.VIOLATION)
        result = aggregate_findings(findings)
        self.assertFalse(result.conform)
        self.assertEqual(result.violation_count, 1)

    def test_single_indeterminate_prevents_pass(self) -> None:
        findings = all_conform()
        findings[2] = finding("D-III", FindingStatus.INDETERMINATE)
        result = aggregate_findings(findings)
        self.assertFalse(result.conform)
        self.assertEqual(result.indeterminate_count, 1)

    def test_required_not_applicable_prevents_pass(self) -> None:
        findings = all_conform()
        findings[3] = finding("D-IV", FindingStatus.NOT_APPLICABLE)
        result = aggregate_findings(findings)
        self.assertFalse(result.conform)
        self.assertEqual(result.not_applicable_count, 1)

    def test_optional_not_applicable_does_not_prevent_pass(self) -> None:
        findings = all_conform()
        findings.append(
            finding("D-I", FindingStatus.NOT_APPLICABLE, required=False)
        )
        result = aggregate_findings(findings)
        self.assertTrue(result.conform)

    def test_counts_are_exact(self) -> None:
        findings = [
            finding("D-I", FindingStatus.CONFORM),
            finding("D-II", FindingStatus.VIOLATION),
            finding("D-III", FindingStatus.INDETERMINATE),
            finding("D-IV", FindingStatus.NOT_APPLICABLE),
        ]
        result = aggregate_findings(findings)
        self.assertEqual(result.conform_count, 1)
        self.assertEqual(result.violation_count, 1)
        self.assertEqual(result.indeterminate_count, 1)
        self.assertEqual(result.not_applicable_count, 1)

    def test_not_applicable_is_not_a_pass(self) -> None:
        result = aggregate_findings(
            [finding(d, FindingStatus.NOT_APPLICABLE) for d in REQUIRED_DIMENSIONS]
        )
        self.assertFalse(result.conform)


class TestOperationalVerification(unittest.TestCase):
    def test_fully_observed_and_conform_is_verified(self) -> None:
        result = aggregate_findings(all_conform("OBSERVED"))
        self.assertTrue(result.conform)
        self.assertTrue(result.operationally_verified)
        self.assertEqual(result.observed_dimensions, REQUIRED_DIMENSIONS)

    def test_synthetic_conform_is_not_verified(self) -> None:
        result = aggregate_findings(all_conform("SYNTHETIC"))
        self.assertTrue(result.conform)
        self.assertFalse(result.operationally_verified)

    def test_declared_conform_is_not_verified(self) -> None:
        result = aggregate_findings(all_conform("DECLARED"))
        self.assertTrue(result.conform)
        self.assertFalse(result.operationally_verified)

    def test_one_declared_dimension_defeats_verification(self) -> None:
        findings = all_conform("OBSERVED")
        findings[0] = finding("D-I", FindingStatus.CONFORM, origin="DECLARED")
        result = aggregate_findings(findings)
        self.assertTrue(result.conform)
        self.assertFalse(result.operationally_verified)

    def test_missing_dimension_defeats_verification(self) -> None:
        findings = all_conform("OBSERVED")[:3]
        result = aggregate_findings(findings)
        self.assertFalse(result.operationally_verified)

    def test_no_origin_defeats_verification(self) -> None:
        result = aggregate_findings(all_conform(None))  # type: ignore[arg-type]
        self.assertTrue(result.conform)
        self.assertFalse(result.operationally_verified)

    def test_violation_defeats_verification(self) -> None:
        findings = all_conform("OBSERVED")
        findings[0] = finding("D-I", FindingStatus.VIOLATION)
        result = aggregate_findings(findings)
        self.assertFalse(result.operationally_verified)

    def test_observed_dimensions_are_sorted(self) -> None:
        result = aggregate_findings(all_conform("OBSERVED"))
        self.assertEqual(
            list(result.observed_dimensions), sorted(result.observed_dimensions)
        )


class TestEndToEndWithValidator(unittest.TestCase):
    def test_synthetic_conforming_observation_is_logically_conform(self) -> None:
        found = v.validate_observation(
            conforming_observation(), binding_for(c.PathClass.PC_03)
        )
        result = aggregate_findings(found)
        self.assertTrue(result.conform)

    def test_synthetic_conforming_observation_is_not_verified(self) -> None:
        found = v.validate_observation(
            conforming_observation(), binding_for(c.PathClass.PC_03)
        )
        result = aggregate_findings(found)
        self.assertFalse(result.operationally_verified)

    def test_declared_conforming_observation_is_not_verified(self) -> None:
        found = v.validate_observation(
            conforming_observation(origin=v.ObservationOrigin.DECLARED),
            binding_for(c.PathClass.PC_03),
        )
        self.assertFalse(aggregate_findings(found).operationally_verified)

    def test_fully_observed_fixture_can_be_verified(self) -> None:
        observation, binding = observed_everything()
        result = aggregate_findings(v.validate_observation(observation, binding))
        self.assertTrue(result.conform)
        self.assertTrue(result.operationally_verified)

    def test_broken_observation_is_not_conform(self) -> None:
        observation = replace(
            conforming_observation(),
            host=host_state(owner="wrong-role", group="wrong-role", mode=0o646),
        )
        result = aggregate_findings(
            v.validate_observation(observation, binding_for(c.PathClass.PC_03))
        )
        self.assertFalse(result.conform)
        self.assertFalse(result.operationally_verified)
        self.assertGreater(result.violation_count, 0)

    def test_missing_dimension_end_to_end_is_indeterminate(self) -> None:
        observation = replace(conforming_observation(), mount=None)
        result = aggregate_findings(
            v.validate_observation(observation, binding_for(c.PathClass.PC_03))
        )
        self.assertFalse(result.conform)
        self.assertGreater(result.indeterminate_count, 0)


class TestDeterminism(unittest.TestCase):
    def test_input_order_does_not_matter(self) -> None:
        findings = all_conform()
        forward = aggregate_findings(findings)
        backward = aggregate_findings(list(reversed(findings)))
        self.assertEqual(forward.findings, backward.findings)

    def test_findings_are_sorted(self) -> None:
        result = aggregate_findings(
            [
                finding("D-IV", FindingStatus.CONFORM, path="z.json"),
                finding("D-I", FindingStatus.CONFORM, path="a.json"),
            ]
        )
        self.assertEqual(list(result.findings), sorted(result.findings))

    def test_serialization_is_byte_identical(self) -> None:
        first = canonical_json_bytes(aggregate_findings(all_conform()).to_dict())
        second = canonical_json_bytes(aggregate_findings(all_conform()).to_dict())
        self.assertEqual(first, second)

    def test_serialization_hash_is_stable(self) -> None:
        payload = aggregate_findings(all_conform()).to_dict()
        digest = hashlib.sha256(canonical_json_bytes(payload)).hexdigest()
        self.assertEqual(
            digest, hashlib.sha256(canonical_json_bytes(payload)).hexdigest()
        )

    def test_same_input_produces_identical_result(self) -> None:
        observation = conforming_observation()
        binding = binding_for(c.PathClass.PC_03)
        first = aggregate_findings(v.validate_observation(observation, binding))
        second = aggregate_findings(v.validate_observation(observation, binding))
        self.assertEqual(
            canonical_json_bytes(first.to_dict()),
            canonical_json_bytes(second.to_dict()),
        )

    def test_canonical_json_is_compact_and_sorted(self) -> None:
        raw = canonical_json_bytes({"b": 1, "a": 2})
        self.assertEqual(raw, b'{"a":2,"b":1}')

    def test_to_dict_keys_are_stable(self) -> None:
        result = aggregate_findings(all_conform())
        self.assertEqual(
            sorted(result.to_dict()),
            [
                "conform",
                "conform_count",
                "findings",
                "indeterminate_count",
                "not_applicable_count",
                "observed_dimensions",
                "operationally_verified",
                "violation_count",
            ],
        )

    def test_finding_to_dict_keys_are_stable(self) -> None:
        item = finding("D-I", FindingStatus.CONFORM).to_dict()
        self.assertEqual(
            sorted(item),
            [
                "detail",
                "dimension",
                "origin",
                "path_class",
                "reason",
                "relative_path",
                "required",
                "status",
            ],
        )


class TestImmutability(unittest.TestCase):
    def test_finding_is_frozen(self) -> None:
        item = finding("D-I", FindingStatus.CONFORM)
        with self.assertRaises(Exception):
            item.status = FindingStatus.VIOLATION  # type: ignore[misc]

    def test_result_is_frozen(self) -> None:
        result = aggregate_findings(all_conform())
        with self.assertRaises(Exception):
            result.conform = False  # type: ignore[misc]

    def test_findings_are_a_tuple(self) -> None:
        result = aggregate_findings(all_conform())
        self.assertIsInstance(result.findings, tuple)

    def test_input_list_is_not_mutated(self) -> None:
        findings = list(reversed(all_conform()))
        snapshot = list(findings)
        aggregate_findings(findings)
        self.assertEqual(findings, snapshot)

    def test_aggregate_source_has_no_mutation(self) -> None:
        source = (
            REPO_ROOT / "core" / "core_brain" / "enforcement" / "aggregate.py"
        ).read_text(encoding="utf-8")
        for token in ("chmod(", "chown(", "mkdir(", "unlink(", "write_text("):
            with self.subTest(token=token):
                self.assertNotIn(token, source)


class TestStatusVocabulary(unittest.TestCase):
    def test_four_statuses(self) -> None:
        self.assertEqual(
            [s.value for s in FindingStatus],
            ["CONFORM", "VIOLATION", "INDETERMINATE", "NOT_APPLICABLE"],
        )

    def test_indeterminate_exists_as_distinct_status(self) -> None:
        self.assertIsNot(FindingStatus.INDETERMINATE, FindingStatus.NOT_APPLICABLE)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
