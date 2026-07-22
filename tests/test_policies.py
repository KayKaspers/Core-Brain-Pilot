"""Tests der fail-closed Policy-Funktionen."""

from __future__ import annotations

import unittest
from unittest import mock

from core.core_brain import policies
from core.core_brain.errors import ReasonCode
from core.core_brain.models import (
    CheckResult,
    ComponentStatus,
    EgressDefault,
    GateStatus,
    RuntimeConfig,
    RuntimeMode,
)


def make_config(**overrides: object) -> RuntimeConfig:
    """Baut eine Konfiguration unter Umgehung der Validierung.

    Nur für Policy-Tests: Die Validierung würde unzulässige Werte bereits
    beim Laden blockieren, hier sollen die Policies selbst geprüft werden.
    """
    base: dict[str, object] = {
        "schema_version": "1.0",
        "runtime_mode": RuntimeMode.SKELETON,
        "control_plane_identity": "control-plane",
        "data_worker_identity": "data-worker",
        "egress_default": EgressDefault.DENY,
        "canonical_write_allowed": False,
        "source_activation_enabled": False,
        "mapping_gate_status": GateStatus.NOT_EVALUATED,
        "security_gate_status": GateStatus.NOT_EVALUATED,
        "secret_provider_status": ComponentStatus.UNCONFIGURED,
        "evidence_writer_status": ComponentStatus.UNCONFIGURED,
    }
    base.update(overrides)
    return RuntimeConfig(**base)  # type: ignore[arg-type]


class TestRootGuard(unittest.TestCase):
    """Tests 12 und 13 — POSIX-root blockiert, Windows ist NOT APPLICABLE."""

    def test_posix_root_is_blocked(self) -> None:
        with mock.patch.object(policies.os, "geteuid", create=True, return_value=0):
            check = policies.check_not_privileged()
        self.assertIs(check.result, CheckResult.BLOCKED)
        self.assertIs(check.reason, ReasonCode.PRIVILEGED_PROCESS)

    def test_posix_non_root_passes(self) -> None:
        with mock.patch.object(policies.os, "geteuid", create=True, return_value=1000):
            check = policies.check_not_privileged()
        self.assertIs(check.result, CheckResult.PASS)

    def test_missing_geteuid_is_not_applicable(self) -> None:
        # create=True, damit der Test auch auf Plattformen ohne geteuid
        # (z. B. Windows) das Fehlen simulieren kann.
        with mock.patch.object(policies.os, "geteuid", None, create=True):
            check = policies.check_not_privileged()
        self.assertIs(check.result, CheckResult.NOT_APPLICABLE)
        self.assertIn("Kein Deploymentnachweis", check.detail)


class TestIdentitySeparation(unittest.TestCase):
    """Getrennte Identitäten."""

    def test_separated_identities_pass(self) -> None:
        check = policies.check_identity_separation(make_config())
        self.assertIs(check.result, CheckResult.PASS)

    def test_identical_identities_blocked(self) -> None:
        config = make_config(data_worker_identity="control-plane")
        check = policies.check_identity_separation(config)
        self.assertIs(check.result, CheckResult.BLOCKED)
        self.assertIs(check.reason, ReasonCode.IDENTITIES_NOT_SEPARATED)


class TestRestrictivePolicies(unittest.TestCase):
    """Canonical Write, Source Activation, Egress, Komponenten."""

    def test_canonical_write_blocked(self) -> None:
        check = policies.check_canonical_write_blocked(
            make_config(canonical_write_allowed=True)
        )
        self.assertIs(check.result, CheckResult.BLOCKED)
        self.assertIs(check.reason, ReasonCode.CANONICAL_WRITE_REQUESTED)

    def test_canonical_write_default_passes(self) -> None:
        check = policies.check_canonical_write_blocked(make_config())
        self.assertIs(check.result, CheckResult.PASS)

    def test_source_activation_blocked(self) -> None:
        check = policies.check_source_activation_blocked(
            make_config(source_activation_enabled=True)
        )
        self.assertIs(check.result, CheckResult.BLOCKED)
        self.assertIs(check.reason, ReasonCode.SOURCE_ACTIVATION_REQUESTED)

    def test_egress_allow_blocked(self) -> None:
        check = policies.check_egress_deny_by_default(
            make_config(egress_default=EgressDefault.ALLOW)
        )
        self.assertIs(check.result, CheckResult.BLOCKED)
        self.assertIs(check.reason, ReasonCode.EGRESS_NOT_DENY)

    def test_egress_deny_passes_without_allowlist(self) -> None:
        check = policies.check_egress_deny_by_default(make_config())
        self.assertIs(check.result, CheckResult.PASS)
        self.assertIn("Keine Allowlist", check.detail)

    def test_configured_secret_provider_blocked(self) -> None:
        check = policies.check_secret_provider_unconfigured(
            make_config(secret_provider_status=ComponentStatus.CONFIGURED)
        )
        self.assertIs(check.result, CheckResult.BLOCKED)

    def test_configured_evidence_writer_blocked(self) -> None:
        check = policies.check_evidence_writer_unconfigured(
            make_config(evidence_writer_status=ComponentStatus.CONFIGURED)
        )
        self.assertIs(check.result, CheckResult.BLOCKED)


class TestRuntimeStartAlwaysBlocked(unittest.TestCase):
    """Test 8 der Spezifikation — Runtime Start ist immer blockiert."""

    def test_blocked_with_gates_not_evaluated(self) -> None:
        check = policies.check_runtime_start_blocked(make_config())
        self.assertIs(check.result, CheckResult.BLOCKED)
        self.assertIs(check.reason, ReasonCode.SECURITY_GATE_NOT_ACCEPTED)

    def test_blocked_even_if_security_gate_claims_accepted(self) -> None:
        config = make_config(security_gate_status=GateStatus.ACCEPTED)
        check = policies.check_runtime_start_blocked(config)
        self.assertIs(check.result, CheckResult.BLOCKED)
        self.assertIs(check.reason, ReasonCode.MAPPING_GATE_NOT_ACCEPTED)

    def test_blocked_even_if_both_gates_claim_accepted(self) -> None:
        config = make_config(
            security_gate_status=GateStatus.ACCEPTED,
            mapping_gate_status=GateStatus.ACCEPTED,
        )
        check = policies.check_runtime_start_blocked(config)
        self.assertIs(check.result, CheckResult.BLOCKED)
        self.assertIs(check.reason, ReasonCode.RUNTIME_SKELETON_ONLY)


class TestDoctorReport(unittest.TestCase):
    """Test 19 — der Bericht ist deterministisch."""

    def test_report_is_never_production_ready(self) -> None:
        report = policies.build_doctor_report(make_config())
        self.assertFalse(report.production_ready)

    def test_report_is_deterministic(self) -> None:
        config = make_config()
        first = policies.build_doctor_report(config).to_dict()
        for _ in range(5):
            self.assertEqual(policies.build_doctor_report(config).to_dict(), first)

    def test_report_always_has_a_blocked_runtime_check(self) -> None:
        report = policies.build_doctor_report(make_config())
        runtime_checks = [c for c in report.checks if c.check_id == "RUNTIME"]
        self.assertEqual(len(runtime_checks), 1)
        self.assertIs(runtime_checks[0].result, CheckResult.BLOCKED)
        self.assertGreaterEqual(len(report.blocked), 1)

    def test_check_order_is_stable(self) -> None:
        report = policies.build_doctor_report(make_config())
        ids = [c.check_id for c in report.checks]
        self.assertEqual(
            ids,
            [
                "KB-01",
                "KB-02",
                "KB-03",
                "KB-06",
                "KB-08",
                "KB-09",
                "KB-10",
                "RUNTIME",
            ],
        )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
