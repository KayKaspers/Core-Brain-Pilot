"""Lokale CLI des Foundation Runtime Skeletons.

Grundkommandos: ``version``, ``validate-config``, ``doctor``, ``run``.
Kommandogruppe ``quarantine`` (CBP-WP-013): ``scan``, ``stage``, ``inspect``,
``release`` — ein lokaler, synthetisch testbarer, fail-closed Prototyp.

Es gibt **keine** HTTP-API, keinen Webserver und keinen Netzwerklistener.
``run`` verweigert deterministisch fail-closed. ``quarantine release``
verweigert unabhängig vom Recordstatus. Kein CLI-Pfad gibt einen Eingabepfad
oder einen Inhaltsauszug aus.

Der Import dieses Moduls hat keine Nebenwirkungen — insbesondere wird beim
Import kein Parser gebaut und kein Argument gelesen.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import TextIO

from .errors import (
    EXIT_CODES,
    ConfigError,
    ExitCode,
    QuarantineInputRejected,
    QuarantinePolicyError,
    QuarantineStoreError,
    ReasonCode,
)
from .models import CheckResult, DoctorReport
from .policies import build_doctor_report, check_runtime_start_blocked

__all__ = ["VERSION", "build_parser", "main", "render_report"]

VERSION = "0.1.0.dev0"
"""Version des Runtime Skeletons. Identisch mit ``pyproject.toml``."""

_PROG = "core-brain-pilot"


def build_parser() -> argparse.ArgumentParser:
    """Baut den Argumentparser.

    Returns:
        Den Parser mit den vier Unterkommandos.
    """
    parser = argparse.ArgumentParser(
        prog=_PROG,
        description=(
            "Foundation Runtime Skeleton — lokal, fail-closed, "
            "nicht produktionsbereit."
        ),
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("version", help="Zeigt die Skeleton-Version.")

    validate = sub.add_parser(
        "validate-config", help="Validiert eine Skeleton-Konfiguration."
    )
    validate.add_argument(
        "--config",
        required=True,
        type=Path,
        help="Ausdrücklicher Pfad zur TOML-Konfiguration.",
    )

    doctor = sub.add_parser("doctor", help="Prüft die lokale Skeleton-Konfiguration.")
    doctor.add_argument("--config", required=True, type=Path)
    doctor.add_argument(
        "--json", action="store_true", help="Gibt den Bericht als JSON aus."
    )

    run = sub.add_parser("run", help="Verweigert den operativen Start (fail-closed).")
    run.add_argument("--config", required=True, type=Path)

    _add_quarantine_parser(sub)

    return parser


def _add_quarantine_parser(
    sub: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    """Ergänzt die Kommandogruppe ``quarantine`` (CBP-WP-013)."""
    quarantine = sub.add_parser(
        "quarantine",
        help="Lokale, synthetische Ingest-Quarantäne (fail-closed).",
    )
    qsub = quarantine.add_subparsers(dest="quarantine_command", required=True)

    scan = qsub.add_parser(
        "scan", help="Scannt genau ein synthetisches Artefakt; speichert nichts."
    )
    scan.add_argument("--input", required=True, type=Path)
    scan.add_argument("--policy", required=True, type=Path)
    scan.add_argument("--source-ref", required=True, dest="source_ref")
    scan.add_argument(
        "--synthetic-test-only", action="store_true", dest="synthetic_test_only"
    )
    scan.add_argument("--json", action="store_true")

    stage = qsub.add_parser(
        "stage",
        help="Scannt und legt Payload und Record ab; keine Promotion.",
    )
    stage.add_argument("--input", required=True, type=Path)
    stage.add_argument("--policy", required=True, type=Path)
    stage.add_argument("--source-ref", required=True, dest="source_ref")
    stage.add_argument("--store", required=True, type=Path)
    stage.add_argument(
        "--synthetic-test-only", action="store_true", dest="synthetic_test_only"
    )
    stage.add_argument("--json", action="store_true")

    inspect = qsub.add_parser(
        "inspect", help="Zeigt minimierte Record-Metadaten; kein Payload, kein Pfad."
    )
    inspect.add_argument("--store", required=True, type=Path)
    inspect.add_argument("--id", required=True, dest="quarantine_id")
    inspect.add_argument("--json", action="store_true")

    release = qsub.add_parser(
        "release", help="Verweigert immer fail-closed; verändert keine Datei."
    )
    release.add_argument("--store", required=True, type=Path)
    release.add_argument("--id", required=True, dest="quarantine_id")


def render_report(report: DoctorReport) -> str:
    """Rendert einen Doctor-Bericht menschenlesbar und deterministisch.

    Args:
        report: Der Bericht.

    Returns:
        Den mehrzeiligen Text. Die Zeilenfolge ist stabil.
    """
    lines: list[str] = [
        f"runtime_mode:     {report.runtime_mode.value}",
        f"production_ready: {str(report.production_ready).lower()}",
        "",
        "checks:",
    ]
    for check in report.checks:
        reason = f" [{check.reason.value}]" if check.reason is not None else ""
        lines.append(
            f"  {check.check_id:<8} {check.result.value:<15} "
            f"{check.title}{reason}"
        )
    summary = report.summary
    lines.extend(
        [
            "",
            (
                f"summary: pass={summary['pass']} "
                f"blocked={summary['blocked']} "
                f"not_applicable={summary['not_applicable']}"
            ),
            "",
            "Dieser Skeleton ist nicht produktionsbereit.",
            "Security Foundation Readiness Gate, Mapping Activation Gate "
            "und DRC bleiben NOT EVALUATED.",
        ]
    )
    return "\n".join(lines)


def _cmd_version(out: TextIO) -> int:
    """Führt ``version`` aus."""
    print(VERSION, file=out)
    return EXIT_CODES[ExitCode.OK]


def _cmd_validate_config(path: Path, out: TextIO, err: TextIO) -> int:
    """Führt ``validate-config`` aus.

    Gibt niemals private Werte vollständig aus — nur Feldnamen und
    Reason Codes.
    """
    from .config import load_config

    try:
        config = load_config(path)
    except ConfigError as exc:
        print(f"CONFIG_INVALID {exc.reason.value} {exc.detail}".rstrip(), file=err)
        return EXIT_CODES[ExitCode.CONFIG_INVALID]

    print("CONFIG_VALID", file=out)
    print(f"schema_version: {config.schema_version}", file=out)
    print(f"runtime_mode:   {config.runtime_mode.value}", file=out)
    print("Strukturell gültig. Keine Betriebsfreigabe.", file=out)
    return EXIT_CODES[ExitCode.OK]


def _cmd_doctor(path: Path, as_json: bool, out: TextIO, err: TextIO) -> int:
    """Führt ``doctor`` aus."""
    from .config import load_config

    try:
        config = load_config(path)
    except ConfigError as exc:
        if as_json:
            payload = {
                "runtime_mode": None,
                "production_ready": False,
                "error": {"reason": exc.reason.value, "detail": exc.detail},
            }
            print(json.dumps(payload, indent=2, sort_keys=True), file=out)
        else:
            print(f"CONFIG_INVALID {exc.reason.value} {exc.detail}".rstrip(), file=err)
        return EXIT_CODES[ExitCode.CONFIG_INVALID]

    report = build_doctor_report(config)

    if as_json:
        print(json.dumps(report.to_dict(), indent=2, sort_keys=True), file=out)
    else:
        print(render_report(report), file=out)

    has_blocked = any(c.result is CheckResult.BLOCKED for c in report.checks)
    return (
        EXIT_CODES[ExitCode.POLICY_BLOCKED]
        if has_blocked
        else EXIT_CODES[ExitCode.OK]
    )


def _cmd_run(path: Path, out: TextIO, err: TextIO) -> int:
    """Führt ``run`` aus — verweigert immer.

    Es wird keine Runtime gestartet, keine Datei geschrieben und kein
    Verzeichnis angelegt.
    """
    from .config import load_config

    try:
        config = load_config(path)
    except ConfigError as exc:
        print(f"CONFIG_INVALID {exc.reason.value} {exc.detail}".rstrip(), file=err)
        return EXIT_CODES[ExitCode.CONFIG_INVALID]

    check = check_runtime_start_blocked(config)
    reason = check.reason or ReasonCode.RUNTIME_SKELETON_ONLY

    print(f"RUNTIME_START_BLOCKED {reason.value}", file=err)
    print("Der Foundation Runtime Skeleton startet keine operative Runtime.", file=err)
    print(
        "Offen: Security Foundation Readiness Gate NOT EVALUATED · "
        "Mapping Activation Gate NOT EVALUATED · DRC NOT EVALUATED.",
        file=err,
    )
    print(
        "Die Umsetzung von KB-01 bis KB-12 ist nicht Bestandteil dieses "
        "Work Packages.",
        file=err,
    )
    return EXIT_CODES[ExitCode.RUNTIME_START_BLOCKED]


# -- Kommandogruppe quarantine (CBP-WP-013) -------------------------------

_QUARANTINE_DISCLAIMER = (
    "Kein Zustand bedeutet approved, released, enabled oder indexed. "
    "Ein technischer Scan ersetzt keine Human-Freigabe."
)


def _cmd_quarantine(
    args: argparse.Namespace, out: TextIO, err: TextIO
) -> int:
    """Verteilt die Unterkommandos der Quarantäne."""
    match args.quarantine_command:
        case "scan":
            return _cmd_quarantine_scan(args, out, err)
        case "stage":
            return _cmd_quarantine_stage(args, out, err)
        case "inspect":
            return _cmd_quarantine_inspect(args, out, err)
        case "release":
            return _cmd_quarantine_release(out, err)
        case _:  # pragma: no cover — argparse erzwingt ein bekanntes Kommando
            print("USAGE_ERROR unknown quarantine command", file=err)
            return EXIT_CODES[ExitCode.USAGE_ERROR]


def _exit_for_status(status: object) -> int:
    """Bildet einen Scan-Status auf einen Exitcode ab."""
    from .quarantine import ScanStatus

    if status is ScanStatus.READY_FOR_HUMAN_REVIEW:
        return EXIT_CODES[ExitCode.OK]
    if status is ScanStatus.REVIEW_REQUIRED:
        return EXIT_CODES[ExitCode.QUARANTINE_REVIEW_REQUIRED]
    return EXIT_CODES[ExitCode.QUARANTINE_BLOCKED]


def _render_scan(scan: object) -> str:
    """Rendert ein ScanResult minimiert — ohne Pfad und ohne Inhalt."""
    from .quarantine import ScanResult

    assert isinstance(scan, ScanResult)
    lines = [
        f"scan_status:    {scan.status.value}",
        f"finding_count:  {len(scan.finding_codes)}",
        "finding_codes:",
    ]
    lines.extend(f"  {code}" for code in scan.finding_codes)
    lines.extend(
        [
            "",
            f"content_sha256: {scan.content_sha256 or '(not read)'}",
            f"byte_size:      {scan.byte_size}",
            f"media_type:     {scan.media_type}",
            "",
            _QUARANTINE_DISCLAIMER,
        ]
    )
    return "\n".join(lines)


def _render_record(record: object) -> str:
    """Rendert einen Record minimiert — ohne Pfad und ohne Inhalt."""
    from .quarantine import QuarantineRecord

    assert isinstance(record, QuarantineRecord)
    data = record.to_dict()
    order = (
        "record_schema_version",
        "quarantine_id",
        "source_reference",
        "content_sha256",
        "byte_size",
        "media_type",
        "policy_schema_version",
        "policy_sha256",
        "scan_status",
        "finding_codes",
        "finding_count",
        "stored_object_reference",
        "created_at",
        "implementation_version",
    )
    lines = [f"{key}: {data[key]}" for key in order]
    lines.extend(["", _QUARANTINE_DISCLAIMER])
    return "\n".join(lines)


def _cmd_quarantine_scan(
    args: argparse.Namespace, out: TextIO, err: TextIO
) -> int:
    """Führt ``quarantine scan`` aus — liest, scannt, speichert nichts."""
    from .quarantine import load_policy, run_scan

    try:
        policy = load_policy(args.policy)
        scan = run_scan(
            input_path=args.input,
            policy=policy,
            source_reference=args.source_ref,
            synthetic_confirmed=args.synthetic_test_only,
        )
    except QuarantinePolicyError as exc:
        print(f"QUARANTINE_POLICY_INVALID {exc.reason.value}".rstrip(), file=err)
        return EXIT_CODES[ExitCode.CONFIG_INVALID]
    except QuarantineInputRejected as exc:
        print(f"QUARANTINE_BLOCKED {exc.reason.value}", file=err)
        return EXIT_CODES[ExitCode.QUARANTINE_BLOCKED]

    if args.json:
        print(json.dumps(scan.to_dict(), indent=2, sort_keys=True), file=out)
    else:
        print(_render_scan(scan), file=out)
    return _exit_for_status(scan.status)


def _cmd_quarantine_stage(
    args: argparse.Namespace, out: TextIO, err: TextIO
) -> int:
    """Führt ``quarantine stage`` aus — scannt und speichert; keine Promotion."""
    from .quarantine import QuarantineStore, load_policy, run_stage

    try:
        policy = load_policy(args.policy)
        store = QuarantineStore(args.store)
        outcome = run_stage(
            input_path=args.input,
            policy=policy,
            source_reference=args.source_ref,
            synthetic_confirmed=args.synthetic_test_only,
            store=store,
        )
    except QuarantinePolicyError as exc:
        print(f"QUARANTINE_POLICY_INVALID {exc.reason.value}".rstrip(), file=err)
        return EXIT_CODES[ExitCode.CONFIG_INVALID]
    except QuarantineInputRejected as exc:
        print(f"QUARANTINE_BLOCKED {exc.reason.value}", file=err)
        return EXIT_CODES[ExitCode.QUARANTINE_BLOCKED]
    except QuarantineStoreError as exc:
        print(f"QUARANTINE_BLOCKED {exc.reason.value}", file=err)
        return EXIT_CODES[ExitCode.QUARANTINE_BLOCKED]

    if outcome.record is None:
        # BLOCKED — es wurde nichts gespeichert.
        if args.json:
            print(json.dumps(outcome.scan.to_dict(), indent=2, sort_keys=True), file=out)
        else:
            print(_render_scan(outcome.scan), file=out)
        return EXIT_CODES[ExitCode.QUARANTINE_BLOCKED]

    if args.json:
        print(
            json.dumps(outcome.record.to_dict(), indent=2, sort_keys=True), file=out
        )
    else:
        print(_render_record(outcome.record), file=out)
    return _exit_for_status(outcome.scan.status)


def _cmd_quarantine_inspect(
    args: argparse.Namespace, out: TextIO, err: TextIO
) -> int:
    """Führt ``quarantine inspect`` aus — zeigt minimierte Metadaten."""
    from .quarantine import QuarantineStore

    try:
        store = QuarantineStore(args.store)
        record = store.load_record(args.quarantine_id)
    except QuarantineStoreError as exc:
        print(f"QUARANTINE_BLOCKED {exc.reason.value}", file=err)
        return EXIT_CODES[ExitCode.QUARANTINE_BLOCKED]

    if args.json:
        print(json.dumps(record.to_dict(), indent=2, sort_keys=True), file=out)
    else:
        print(_render_record(record), file=out)
    return EXIT_CODES[ExitCode.OK]


def _cmd_quarantine_release(out: TextIO, err: TextIO) -> int:
    """Führt ``quarantine release`` aus — verweigert immer, ändert nichts.

    Diese Funktion öffnet den Store **nicht** und liest keinen Record. Sie
    verändert keine Datei und gibt einen stabilen Reason Code aus.
    """
    print(
        f"QUARANTINE_RELEASE_BLOCKED {ReasonCode.QUARANTINE_RELEASE_ALWAYS_BLOCKED.value}",
        file=err,
    )
    print(
        "Der Quarantäneprototyp gibt nichts frei und promotet nichts.", file=err
    )
    print(
        "Eine Freigabe erfordert eine menschliche Entscheidung außerhalb "
        "dieses MVP.",
        file=err,
    )
    return EXIT_CODES[ExitCode.QUARANTINE_RELEASE_BLOCKED]


def main(
    argv: Sequence[str] | None = None,
    out: TextIO | None = None,
    err: TextIO | None = None,
) -> int:
    """Einstiegspunkt der CLI.

    Args:
        argv: Argumente ohne Programmnamen. ``None`` liest ``sys.argv``.
        out: Zielstrom für die reguläre Ausgabe.
        err: Zielstrom für Fehler und Verweigerungen.

    Returns:
        Den numerischen Exitcode.
    """
    out = out if out is not None else sys.stdout
    err = err if err is not None else sys.stderr

    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        code = exc.code
        if code in (0, None):
            return EXIT_CODES[ExitCode.OK]
        return EXIT_CODES[ExitCode.USAGE_ERROR]

    match args.command:
        case "version":
            return _cmd_version(out)
        case "validate-config":
            return _cmd_validate_config(args.config, out, err)
        case "doctor":
            return _cmd_doctor(args.config, args.json, out, err)
        case "run":
            return _cmd_run(args.config, out, err)
        case "quarantine":
            return _cmd_quarantine(args, out, err)
        case _:  # pragma: no cover — argparse erzwingt ein bekanntes Kommando
            print("USAGE_ERROR unknown command", file=err)
            return EXIT_CODES[ExitCode.USAGE_ERROR]
