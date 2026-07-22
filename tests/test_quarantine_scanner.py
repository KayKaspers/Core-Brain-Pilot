"""Tests von Intake und Baseline-Scanner (CBP-WP-013).

Deckt die strukturelle Vorprüfung, die einmalige Leseoperation, die
Kodierungs-, Inhalts-, Credential- und PII-Indikatoren sowie die
Minimierungszusagen ab. Alle Testdaten sind synthetisch; Credential- und
Key-Muster werden zur Laufzeit aus sicheren Teilstücken zusammengesetzt.
"""

from __future__ import annotations

import dataclasses
import hashlib
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

from core.core_brain.errors import QuarantineInputRejected, ReasonCode
from core.core_brain.quarantine import ScanStatus, load_policy, run_scan
from core.core_brain.quarantine.models import FindingCode, QuarantinePolicy
from core.core_brain.quarantine.scanner import (
    SYNTHETIC_MARKER,
    structural_findings,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
EXAMPLE_POLICY = REPO_ROOT / "config" / "quarantine_policy.example.toml"
POLICY = load_policy(EXAMPLE_POLICY)

MARKER = SYNTHETIC_MARKER
SOURCE_REF = "synthetic:unit-test"


def _scan_bytes(raw: bytes, *, policy: QuarantinePolicy = POLICY) -> object:
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "artifact.md"
        target.write_bytes(raw)
        return run_scan(
            input_path=target,
            policy=policy,
            source_reference=SOURCE_REF,
            synthetic_confirmed=True,
        )


def _scan_text(text: str, *, policy: QuarantinePolicy = POLICY) -> object:
    return _scan_bytes(text.encode("utf-8"), policy=policy)


def _codes(result: object) -> tuple[str, ...]:
    return result.finding_codes  # type: ignore[attr-defined]


class TestIntakeAndScanner(unittest.TestCase):
    """Tests 10 bis 27."""

    def test_10_valid_synthetic_markdown_is_ready(self) -> None:
        result = _scan_text(f"{MARKER}\n# Notiz\nGewöhnlicher Text.\n")
        self.assertIs(result.status, ScanStatus.READY_FOR_HUMAN_REVIEW)
        self.assertEqual(_codes(result), ())

    def test_11_missing_file_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "nope.md"
            with self.assertRaises(QuarantineInputRejected) as ctx:
                run_scan(
                    input_path=missing,
                    policy=POLICY,
                    source_reference=SOURCE_REF,
                    synthetic_confirmed=True,
                )
        self.assertEqual(ctx.exception.reason, ReasonCode.QUARANTINE_INPUT_NOT_FOUND)

    def test_12_directory_is_not_regular(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = run_scan(
                input_path=Path(tmp),
                policy=POLICY,
                source_reference=SOURCE_REF,
                synthetic_confirmed=True,
            )
        self.assertIs(result.status, ScanStatus.BLOCKED)
        self.assertIn(FindingCode.STRUCTURE_NOT_REGULAR.value, _codes(result))

    def test_13_symlink_blocks_or_is_simulated(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            real = Path(tmp) / "real.md"
            real.write_text(f"{MARKER}\ntext\n", encoding="utf-8")
            link = Path(tmp) / "link.md"
            try:
                link.symlink_to(real)
            except (OSError, NotImplementedError):
                # Plattformneutrale Simulation der strukturellen Regel.
                findings = structural_findings(
                    is_symlink=True,
                    is_regular_file=False,
                    suffix=".md",
                    size=10,
                    policy=POLICY,
                )
                codes = {f.code for f in findings}
                self.assertIn(FindingCode.STRUCTURE_SYMLINK, codes)
                return
            result = run_scan(
                input_path=link,
                policy=POLICY,
                source_reference=SOURCE_REF,
                synthetic_confirmed=True,
            )
        self.assertIs(result.status, ScanStatus.BLOCKED)
        self.assertIn(FindingCode.STRUCTURE_SYMLINK.value, _codes(result))

    def test_14_wrong_suffix_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "artifact.txt"
            target.write_text(f"{MARKER}\ntext\n", encoding="utf-8")
            result = run_scan(
                input_path=target,
                policy=POLICY,
                source_reference=SOURCE_REF,
                synthetic_confirmed=True,
            )
        self.assertIs(result.status, ScanStatus.BLOCKED)
        self.assertIn(FindingCode.STRUCTURE_SUFFIX.value, _codes(result))

    def test_15_empty_file_blocks(self) -> None:
        result = _scan_bytes(b"")
        self.assertIs(result.status, ScanStatus.BLOCKED)
        self.assertIn(FindingCode.STRUCTURE_EMPTY.value, _codes(result))

    def test_16_file_too_large_blocks(self) -> None:
        small = dataclasses.replace(POLICY, max_bytes=8)
        result = _scan_text(f"{MARKER}\nmuch more than eight bytes\n", policy=small)
        self.assertIs(result.status, ScanStatus.BLOCKED)
        self.assertIn(FindingCode.STRUCTURE_SIZE.value, _codes(result))

    def test_17_invalid_utf8_blocks(self) -> None:
        result = _scan_bytes(b"\xff\xfe invalid bytes without marker")
        self.assertIs(result.status, ScanStatus.BLOCKED)
        self.assertIn(FindingCode.ENCODING_UTF8.value, _codes(result))

    def test_18_nul_byte_blocks(self) -> None:
        result = _scan_bytes(f"{MARKER}\nbefore".encode() + b"\x00" + b"after\n")
        self.assertIs(result.status, ScanStatus.BLOCKED)
        self.assertIn(FindingCode.CONTENT_NUL.value, _codes(result))

    def test_19_missing_synthetic_marker_blocks(self) -> None:
        result = _scan_text("# Notiz\nohne Marker\n")
        self.assertIs(result.status, ScanStatus.BLOCKED)
        self.assertIn(FindingCode.SYNTHETIC_MARKER_MISSING.value, _codes(result))

    def test_20_private_key_marker_blocks(self) -> None:
        needle = "-----" + "BEGIN" + " " + "PRIVATE" + " " + "KEY" + "-----"
        result = _scan_text(f"{MARKER}\n{needle}\n")
        self.assertIs(result.status, ScanStatus.BLOCKED)
        self.assertIn(
            FindingCode.CREDENTIAL_PRIVATE_KEY_MARKER.value, _codes(result)
        )

    def test_21_credential_assignment_blocks(self) -> None:
        line = "password" + " = " + "placeholder-not-a-real-secret"
        result = _scan_text(f"{MARKER}\n{line}\n")
        self.assertIs(result.status, ScanStatus.BLOCKED)
        self.assertIn(FindingCode.CREDENTIAL_ASSIGNMENT.value, _codes(result))

    def test_22_email_indicator_requires_review(self) -> None:
        result = _scan_text(f"{MARKER}\nKontakt: user@example.com\n")
        self.assertIs(result.status, ScanStatus.REVIEW_REQUIRED)
        self.assertIn(FindingCode.PII_EMAIL_INDICATOR.value, _codes(result))

    def test_23_phone_indicator_requires_review(self) -> None:
        # Reservierte fiktive Rufnummer (555-0100).
        result = _scan_text(f"{MARKER}\nRuf: +1-555-0100\n")
        self.assertIs(result.status, ScanStatus.REVIEW_REQUIRED)
        self.assertIn(FindingCode.PII_PHONE_INDICATOR.value, _codes(result))

    def test_24_findings_contain_no_content(self) -> None:
        token = "UNIQUE-CONTENT-TOKEN-24"
        line = "password" + " = " + token
        result = _scan_text(f"{MARKER}\n{line}\n")
        for finding in result.findings:  # type: ignore[attr-defined]
            self.assertNotIn(token, repr(finding))
            self.assertNotIn(token, str(finding.to_dict()))

    def test_25_findings_contain_no_input_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "unique-name-25.md"
            target.write_text("no marker here\n", encoding="utf-8")
            result = run_scan(
                input_path=target,
                policy=POLICY,
                source_reference=SOURCE_REF,
                synthetic_confirmed=True,
            )
            rendered = str(result.to_dict())
            self.assertNotIn("unique-name-25", rendered)
            self.assertNotIn(str(target), rendered)

    def test_26_sha256_is_correct(self) -> None:
        raw = f"{MARKER}\n# deterministic\ncontent\n".encode()
        result = _scan_bytes(raw)
        self.assertEqual(result.content_sha256, hashlib.sha256(raw).hexdigest())

    def test_27_identity_change_between_check_and_read_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "artifact.md"
            target.write_text(f"{MARKER}\ntext\n", encoding="utf-8")
            real = target.lstat()
            fake = types.SimpleNamespace(
                st_ino=real.st_ino,
                st_dev=real.st_dev,
                st_size=real.st_size + 1,
                st_mtime_ns=real.st_mtime_ns,
                st_mode=real.st_mode,
            )
            with mock.patch(
                "core.core_brain.quarantine.pipeline.os.fstat", return_value=fake
            ):
                with self.assertRaises(QuarantineInputRejected) as ctx:
                    run_scan(
                        input_path=target,
                        policy=POLICY,
                        source_reference=SOURCE_REF,
                        synthetic_confirmed=True,
                    )
        self.assertEqual(ctx.exception.reason, ReasonCode.QUARANTINE_INPUT_CHANGED)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
