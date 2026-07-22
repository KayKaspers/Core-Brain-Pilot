"""Tests der fail-closed Default-Ports."""

from __future__ import annotations

import unittest

from core.core_brain.errors import PortRefused, ReasonCode
from core.core_brain.models import RuntimeMode
from core.core_brain.ports import (
    DenyingEgressPort,
    DenyingEvidenceWriter,
    DenyingSecretResolver,
    EgressDecisionPort,
    OperationalEvidenceWriter,
    RuntimeStatusProvider,
    SecretResolver,
    SkeletonRuntimeStatusProvider,
)


class TestDenyingSecretResolver(unittest.TestCase):
    """Test 14 — der Default-Resolver verweigert."""

    def test_resolve_refuses(self) -> None:
        resolver = DenyingSecretResolver()
        with self.assertRaises(PortRefused) as ctx:
            resolver.resolve("cbp-secret:v1:example-file-provider:placeholder-0001")
        self.assertIs(
            ctx.exception.reason, ReasonCode.SECRET_RESOLUTION_NOT_IMPLEMENTED
        )

    def test_refusal_does_not_echo_the_reference(self) -> None:
        resolver = DenyingSecretResolver()
        reference = "cbp-secret:v1:example-file-provider:placeholder-0002"
        with self.assertRaises(PortRefused) as ctx:
            resolver.resolve(reference)
        self.assertNotIn(reference, str(ctx.exception))

    def test_satisfies_protocol(self) -> None:
        self.assertIsInstance(DenyingSecretResolver(), SecretResolver)


class TestDenyingEvidenceWriter(unittest.TestCase):
    """Test 15 — der Default-Writer verweigert."""

    def test_append_refuses(self) -> None:
        writer = DenyingEvidenceWriter()
        with self.assertRaises(PortRefused) as ctx:
            writer.append("authorization", {"result": "blocked"})
        self.assertIs(
            ctx.exception.reason, ReasonCode.EVIDENCE_WRITER_NOT_IMPLEMENTED
        )

    def test_satisfies_protocol(self) -> None:
        self.assertIsInstance(DenyingEvidenceWriter(), OperationalEvidenceWriter)


class TestDenyingEgressPort(unittest.TestCase):
    """Test 16 — der Default-Egress-Port verweigert."""

    def test_allow_refuses(self) -> None:
        port = DenyingEgressPort()
        with self.assertRaises(PortRefused) as ctx:
            port.allow("example-target", "retrieval", "data-worker")
        self.assertIs(ctx.exception.reason, ReasonCode.EGRESS_PORT_DENY_BY_DEFAULT)

    def test_refuses_for_every_identity(self) -> None:
        port = DenyingEgressPort()
        for identity in ("control-plane", "data-worker", "unknown"):
            with self.subTest(identity=identity):
                with self.assertRaises(PortRefused):
                    port.allow("example-target", "any", identity)

    def test_satisfies_protocol(self) -> None:
        self.assertIsInstance(DenyingEgressPort(), EgressDecisionPort)


class TestRuntimeStatusProvider(unittest.TestCase):
    """Der Statusprovider meldet dauerhaft ``not production ready``."""

    def test_never_production_ready(self) -> None:
        self.assertFalse(SkeletonRuntimeStatusProvider().is_production_ready())

    def test_mode_is_skeleton(self) -> None:
        self.assertIs(SkeletonRuntimeStatusProvider().mode(), RuntimeMode.SKELETON)

    def test_satisfies_protocol(self) -> None:
        self.assertIsInstance(
            SkeletonRuntimeStatusProvider(), RuntimeStatusProvider
        )


class TestNoRealImplementations(unittest.TestCase):
    """Das Ports-Modul enthält keinen realen Provider."""

    def test_ports_module_has_no_network_or_file_access(self) -> None:
        from pathlib import Path

        source = (
            Path(__file__).resolve().parent.parent
            / "core"
            / "core_brain"
            / "ports.py"
        ).read_text(encoding="utf-8")
        for forbidden in (
            "import socket",
            "import urllib",
            "import http",
            "import requests",
            "open(",
            "subprocess",
        ):
            with self.subTest(token=forbidden):
                self.assertNotIn(forbidden, source)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
