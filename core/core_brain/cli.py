"""Lokale CLI des Foundation Runtime Skeletons.

Vier Kommandos: ``version``, ``validate-config``, ``doctor``, ``run``.

Es gibt **keine** HTTP-API, keinen Webserver und keinen Netzwerklistener.
``run`` verweigert deterministisch fail-closed.

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

from .errors import EXIT_CODES, ConfigError, ExitCode, ReasonCode
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

    return parser


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
        case _:  # pragma: no cover — argparse erzwingt ein bekanntes Kommando
            print("USAGE_ERROR unknown command", file=err)
            return EXIT_CODES[ExitCode.USAGE_ERROR]
