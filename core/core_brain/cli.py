"""Lokale CLI des Foundation Runtime Skeletons.

Grundkommandos: ``version``, ``validate-config``, ``doctor``, ``run``.
Kommandogruppe ``quarantine`` (CBP-WP-013): ``scan``, ``stage``, ``inspect``,
``release``. Kommandogruppe ``source-registry`` (CBP-WP-014):
``validate-definition``, ``register``, ``list``, ``inspect``, ``retire``,
``activate``. Kommandogruppe ``source-mapping`` (CBP-WP-015/016):
``validate-draft``, ``activation-check`` und ``activation-evaluate`` — lokale,
synthetisch testbare, read-only und fail-closed Prototypen.

Es gibt **keine** HTTP-API, keinen Webserver und keinen Netzwerklistener.
``run`` verweigert deterministisch fail-closed. ``quarantine release`` und
``source-registry activate`` verweigern unabhängig vom Zustand.
``source-mapping activation-check`` verweigert jede Aktivierung unabhängig vom
Validierungsergebnis. Kein CLI-Pfad gibt einen Eingabepfad oder einen
Inhaltsauszug aus.

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
    GateEvidenceError,
    MappingPolicyError,
    QuarantineInputRejected,
    QuarantinePolicyError,
    QuarantineStoreError,
    ReasonCode,
    RegistryCatalogError,
    RegistryConflict,
    RegistryDefinitionRejected,
    RegistryNotFound,
    RegistryPolicyError,
    RegistryStorageError,
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
    _add_source_registry_parser(sub)
    _add_source_mapping_parser(sub)

    return parser


def _add_source_mapping_parser(
    sub: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    """Ergänzt die Kommandogruppe ``source-mapping`` (CBP-WP-015)."""
    mapping = sub.add_parser(
        "source-mapping",
        help=(
            "Lokaler, synthetischer, read-only Mapping-Draft-Validator "
            "(fail-closed)."
        ),
    )
    msub = mapping.add_subparsers(dest="mapping_command", required=True)

    validate = msub.add_parser(
        "validate-draft",
        help="Validiert einen synthetischen Mapping-Entwurf; schreibt nichts.",
    )
    activation = msub.add_parser(
        "activation-check",
        help="Validiert read-only und verweigert danach jede Aktivierung.",
    )
    evaluate = msub.add_parser(
        "activation-evaluate",
        help=(
            "Read-only Mapping-Activation-Gate-Evaluator (CBP-WP-016); "
            "fail-closed BLOCKED, keine Aktivierung."
        ),
    )
    for parser_ in (validate, activation, evaluate):
        parser_.add_argument("--draft", required=True, type=Path)
        parser_.add_argument("--policy", required=True, type=Path)
        parser_.add_argument("--registry", required=True, type=Path)
        parser_.add_argument("--source-id", required=True, dest="source_id")
        parser_.add_argument(
            "--synthetic-test-only", action="store_true", dest="synthetic_test_only"
        )
        parser_.add_argument("--json", action="store_true")
    # Der Evaluator bindet zusätzlich ein synthetisches Evidenz-Bundle.
    evaluate.add_argument("--evidence", required=True, type=Path)


def _add_source_registry_parser(
    sub: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    """Ergänzt die Kommandogruppe ``source-registry`` (CBP-WP-014)."""
    registry = sub.add_parser(
        "source-registry",
        help="Lokale, synthetische, deaktivierte Source Registry (fail-closed).",
    )
    rsub = registry.add_subparsers(dest="registry_command", required=True)

    validate = rsub.add_parser(
        "validate-definition",
        help="Validiert Definition und Policy; schreibt nichts.",
    )
    validate.add_argument("--definition", required=True, type=Path)
    validate.add_argument("--policy", required=True, type=Path)
    validate.add_argument("--json", action="store_true")

    register = rsub.add_parser(
        "register",
        help="Registriert eine synthetische Definition als REGISTERED_DISABLED.",
    )
    register.add_argument("--definition", required=True, type=Path)
    register.add_argument("--policy", required=True, type=Path)
    register.add_argument("--registry", required=True, type=Path)
    register.add_argument(
        "--synthetic-test-only", action="store_true", dest="synthetic_test_only"
    )
    register.add_argument("--json", action="store_true")

    listing = rsub.add_parser(
        "list", help="Zeigt minimierte Katalogeinträge; keine Pfade, keine Refs."
    )
    listing.add_argument("--registry", required=True, type=Path)
    listing.add_argument("--json", action="store_true")

    inspect = rsub.add_parser(
        "inspect", help="Zeigt minimierte Record-Metadaten; kein Registry-Pfad."
    )
    inspect.add_argument("--registry", required=True, type=Path)
    inspect.add_argument("--id", required=True, dest="source_id")
    inspect.add_argument("--json", action="store_true")

    retire = rsub.add_parser(
        "retire", help="Append-only Retirement-Event; löscht keinen Record."
    )
    retire.add_argument("--registry", required=True, type=Path)
    retire.add_argument("--id", required=True, dest="source_id")
    retire.add_argument(
        "--synthetic-test-only", action="store_true", dest="synthetic_test_only"
    )
    retire.add_argument("--json", action="store_true")

    activate = rsub.add_parser(
        "activate", help="Verweigert immer fail-closed; verändert keine Datei."
    )
    activate.add_argument("--registry", required=True, type=Path)
    activate.add_argument("--id", required=True, dest="source_id")


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


# -- Kommandogruppe source-registry (CBP-WP-014) --------------------------

_REGISTRY_DISCLAIMER = (
    "Kein Zustand bedeutet approved, mapped, activated, ingestible, indexed "
    "oder retrievable. Eine Registrierung ist keine Aktivierung."
)
_CONFLICT_REASONS = frozenset(
    {
        ReasonCode.REGISTRY_RECORD_CONFLICT,
        ReasonCode.REGISTRY_RETIREMENT_CONFLICT,
    }
)


def _cmd_source_registry(
    args: argparse.Namespace, out: TextIO, err: TextIO
) -> int:
    """Verteilt die Unterkommandos der Source Registry."""
    match args.registry_command:
        case "validate-definition":
            return _cmd_registry_validate(args, out, err)
        case "register":
            return _cmd_registry_register(args, out, err)
        case "list":
            return _cmd_registry_list(args, out, err)
        case "inspect":
            return _cmd_registry_inspect(args, out, err)
        case "retire":
            return _cmd_registry_retire(args, out, err)
        case "activate":
            return _cmd_registry_activate(out, err)
        case _:  # pragma: no cover — argparse erzwingt ein bekanntes Kommando
            print("USAGE_ERROR unknown source-registry command", file=err)
            return EXIT_CODES[ExitCode.USAGE_ERROR]


def _registry_error_exit(exc: object, err: TextIO) -> int:
    """Bildet eine Registry-Ausnahme auf einen stabilen Exitcode ab."""
    reason = exc.reason.value  # type: ignore[attr-defined]
    if isinstance(exc, RegistryPolicyError):
        print(f"REGISTRY_POLICY_INVALID {reason}", file=err)
        return EXIT_CODES[ExitCode.CONFIG_INVALID]
    if isinstance(exc, RegistryNotFound):
        print(f"SOURCE_REGISTRY_NOT_FOUND {reason}", file=err)
        return EXIT_CODES[ExitCode.SOURCE_REGISTRY_NOT_FOUND]
    if isinstance(exc, RegistryConflict) or (
        isinstance(exc, RegistryStorageError) and exc.reason in _CONFLICT_REASONS
    ):
        print(f"SOURCE_REGISTRY_CONFLICT {reason}", file=err)
        return EXIT_CODES[ExitCode.SOURCE_REGISTRY_CONFLICT]
    print(f"SOURCE_REGISTRY_BLOCKED {reason}", file=err)
    return EXIT_CODES[ExitCode.SOURCE_REGISTRY_BLOCKED]


def _render_registry_record(data: dict[str, object]) -> str:
    """Rendert Record-Metadaten minimiert — ohne Registry-Pfad."""
    order = (
        "source_id",
        "namespace",
        "source_key",
        "display_name",
        "collection_key",
        "domain_key",
        "source_kind",
        "data_class",
        "ai_eligibility",
        "owner_role",
        "source_reference",
        "lifecycle_state",
    )
    lines = [f"{key}: {data[key]}" for key in order if key in data]
    lines.extend(["", _REGISTRY_DISCLAIMER])
    return "\n".join(lines)


def _cmd_registry_validate(
    args: argparse.Namespace, out: TextIO, err: TextIO
) -> int:
    """``source-registry validate-definition`` — validiert, schreibt nichts."""
    from .registry import derive_source_id, load_definition, load_policy

    try:
        policy = load_policy(args.policy)
        definition = load_definition(args.definition, policy)
    except (RegistryPolicyError, RegistryDefinitionRejected) as exc:
        return _registry_error_exit(exc, err)

    source_id = derive_source_id(definition.namespace, definition.source_key)
    payload = {
        "definition_valid": True,
        "source_id": source_id,
        "namespace": definition.namespace,
        "source_key": definition.source_key,
        "display_name": definition.display_name,
        "collection_key": definition.collection_key,
        "domain_key": definition.domain_key,
        "source_kind": definition.source_kind,
        "data_class": definition.data_class,
        "ai_eligibility": definition.ai_eligibility,
        "owner_role": definition.owner_role,
        "source_reference": definition.source_reference,
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True), file=out)
    else:
        print("DEFINITION_VALID", file=out)
        print(_render_registry_record(payload), file=out)
    return EXIT_CODES[ExitCode.OK]


def _cmd_registry_register(
    args: argparse.Namespace, out: TextIO, err: TextIO
) -> int:
    """``source-registry register`` — registriert deaktiviert; aktiviert nichts."""
    from .registry import RegistryStorage, load_policy, register

    try:
        policy = load_policy(args.policy)
        storage = RegistryStorage(args.registry)
        record = register(
            definition_path=args.definition,
            policy=policy,
            storage=storage,
            synthetic_confirmed=args.synthetic_test_only,
        )
    except (
        RegistryPolicyError,
        RegistryDefinitionRejected,
        RegistryStorageError,
        RegistryConflict,
        RegistryCatalogError,
    ) as exc:
        return _registry_error_exit(exc, err)

    if args.json:
        print(json.dumps(record.to_dict(), indent=2, sort_keys=True), file=out)
    else:
        print(_render_registry_record(record.to_dict()), file=out)
    return EXIT_CODES[ExitCode.OK]


def _cmd_registry_list(
    args: argparse.Namespace, out: TextIO, err: TextIO
) -> int:
    """``source-registry list`` — zeigt minimierte Katalogeinträge."""
    from .registry import RegistryStorage, build_catalog

    try:
        storage = RegistryStorage(args.registry)
        catalog = build_catalog(storage)
    except (RegistryStorageError, RegistryCatalogError) as exc:
        return _registry_error_exit(exc, err)

    if args.json:
        print(json.dumps(catalog.to_dict(), indent=2, sort_keys=True), file=out)
    else:
        lines = [
            f"record_count:             {catalog.record_count}",
            f"registered_disabled_count: {catalog.registered_disabled_count}",
            f"retired_count:            {catalog.retired_count}",
            "entries:",
        ]
        for entry in catalog.entries:
            lines.append(
                f"  {entry.source_id}  {entry.lifecycle_state.value}  "
                f"{entry.namespace}/{entry.source_key}"
            )
        lines.extend(["", _REGISTRY_DISCLAIMER])
        print("\n".join(lines), file=out)
    return EXIT_CODES[ExitCode.OK]


def _cmd_registry_inspect(
    args: argparse.Namespace, out: TextIO, err: TextIO
) -> int:
    """``source-registry inspect`` — minimierte Record-Metadaten."""
    from .registry import RegistryStorage, inspect

    try:
        storage = RegistryStorage(args.registry)
        record, state = inspect(storage, args.source_id)
    except (RegistryStorageError, RegistryNotFound) as exc:
        return _registry_error_exit(exc, err)

    data = record.to_dict()
    data["lifecycle_state"] = state.value  # effektiver Zustand
    if args.json:
        print(json.dumps(data, indent=2, sort_keys=True), file=out)
    else:
        print(_render_registry_record(data), file=out)
    return EXIT_CODES[ExitCode.OK]


def _cmd_registry_retire(
    args: argparse.Namespace, out: TextIO, err: TextIO
) -> int:
    """``source-registry retire`` — append-only Retirement; keine Löschung."""
    from .registry import RegistryStorage, retire

    try:
        storage = RegistryStorage(args.registry)
        outcome = retire(
            storage=storage,
            source_id=args.source_id,
            synthetic_confirmed=args.synthetic_test_only,
        )
    except (
        RegistryDefinitionRejected,
        RegistryStorageError,
        RegistryNotFound,
        RegistryCatalogError,
    ) as exc:
        return _registry_error_exit(exc, err)

    payload = {
        "source_id": outcome.record.source_id,
        "lifecycle_state": outcome.lifecycle_state.value,
        "retirement_event_created": outcome.event is not None,
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True), file=out)
    else:
        print(f"source_id:      {payload['source_id']}", file=out)
        print(f"lifecycle_state: {payload['lifecycle_state']}", file=out)
        print(
            f"event_created:  {str(payload['retirement_event_created']).lower()}",
            file=out,
        )
        print("", file=out)
        print(_REGISTRY_DISCLAIMER, file=out)
    return EXIT_CODES[ExitCode.OK]


def _cmd_registry_activate(out: TextIO, err: TextIO) -> int:
    """``source-registry activate`` — verweigert immer, ändert nichts.

    Öffnet den Registry-Speicher **nicht** und liest keinen Record.
    """
    print(
        f"SOURCE_REGISTRY_ACTIVATION_BLOCKED "
        f"{ReasonCode.REGISTRY_ACTIVATION_ALWAYS_BLOCKED.value}",
        file=err,
    )
    print(
        "Der Source-Registry-Prototyp aktiviert nichts und erzeugt kein "
        "Source Mapping.",
        file=err,
    )
    print(
        "Eine Aktivierung erfordert eine menschliche Entscheidung und ein "
        "Mapping Activation Gate außerhalb dieses MVP.",
        file=err,
    )
    return EXIT_CODES[ExitCode.SOURCE_REGISTRY_ACTIVATION_BLOCKED]


# -- Kommandogruppe source-mapping (CBP-WP-015) ---------------------------

_MAPPING_DISCLAIMER = (
    "VALID_DRAFT bedeutet keine Freigabe, kein gespeichertes Mapping, keine "
    "Aktivierung, keinen Ingest, keine Indexierung und kein Retrieval. Der "
    "Report wird nicht gespeichert."
)


def _cmd_source_mapping(args: argparse.Namespace, out: TextIO, err: TextIO) -> int:
    """Verteilt die Unterkommandos des Source-Mapping-Draft-Validators."""
    match args.mapping_command:
        case "validate-draft":
            return _cmd_mapping_validate_draft(args, out, err)
        case "activation-check":
            return _cmd_mapping_activation_check(args, out, err)
        case "activation-evaluate":
            return _cmd_mapping_activation_evaluate(args, out, err)
        case _:  # pragma: no cover — argparse erzwingt ein bekanntes Kommando
            print("USAGE_ERROR unknown source-mapping command", file=err)
            return EXIT_CODES[ExitCode.USAGE_ERROR]


def _render_mapping_report(report: object) -> str:
    """Rendert den Report minimiert — ohne Pfad, URL, Inhalt oder Source Ref."""
    from .mapping import ValidationReport

    assert isinstance(report, ValidationReport)
    lines = [
        f"validation_status:              {report.validation_status.value}",
        f"mapping_id:                     {report.mapping_id}",
        f"source_id:                      {report.source_id}",
        f"draft_sha256:                   {report.draft_sha256}",
        f"policy_sha256:                  {report.policy_sha256}",
        f"mapping_schema_version:         {report.mapping_schema_version}",
        f"report_schema_version:          {report.report_schema_version}",
        f"canonical_contract_field_count: {report.canonical_contract_field_count}",
        f"required_field_count:           {report.required_field_count}",
        f"present_field_count:            {report.present_field_count}",
        f"boundary_count:                 {report.boundary_count}",
        f"reason_count:                   {report.reason_count}",
        f"implementation_version:         {report.implementation_version}",
        "reason_codes:",
    ]
    lines.extend(f"  {code}" for code in report.reason_codes)
    lines.extend(["", _MAPPING_DISCLAIMER])
    return "\n".join(lines)


def _emit_mapping_report(report: object, as_json: bool, out: TextIO) -> None:
    """Gibt den Report aus (kanonisches JSON bei ``--json``); speichert nichts."""
    from .mapping import ValidationReport

    assert isinstance(report, ValidationReport)
    if as_json:
        print(json.dumps(report.to_dict(), indent=2, sort_keys=True), file=out)
    else:
        print(_render_mapping_report(report), file=out)


def _cmd_mapping_validate_draft(
    args: argparse.Namespace, out: TextIO, err: TextIO
) -> int:
    """``source-mapping validate-draft`` — validiert read-only; schreibt nichts.

    Exitcode 0 ausschließlich bei ``VALID_DRAFT``. Andernfalls Exitcode 12. Eine
    ungültige Policy liefert Exitcode 2.
    """
    from .mapping import ValidationStatus, load_policy, run_validate

    try:
        policy = load_policy(args.policy)
    except MappingPolicyError as exc:
        print(f"MAPPING_POLICY_INVALID {exc.reason.value}".rstrip(), file=err)
        return EXIT_CODES[ExitCode.CONFIG_INVALID]

    report = run_validate(
        draft_path=args.draft,
        policy=policy,
        registry_root=args.registry,
        source_id=args.source_id,
        synthetic_confirmed=args.synthetic_test_only,
    )
    _emit_mapping_report(report, args.json, out)

    if report.validation_status is ValidationStatus.VALID_DRAFT:
        return EXIT_CODES[ExitCode.OK]
    return EXIT_CODES[ExitCode.SOURCE_MAPPING_DRAFT_BLOCKED]


def _cmd_mapping_activation_check(
    args: argparse.Namespace, out: TextIO, err: TextIO
) -> int:
    """``source-mapping activation-check`` — validiert, verweigert dann immer.

    Verändert **keine** Datei. Verweigert die Aktivierung **unabhängig** vom
    Validierungsergebnis mit Exitcode 13. Eine ungültige Policy liefert
    Exitcode 2.
    """
    from .mapping import load_policy, run_activation_check

    try:
        policy = load_policy(args.policy)
    except MappingPolicyError as exc:
        print(f"MAPPING_POLICY_INVALID {exc.reason.value}".rstrip(), file=err)
        return EXIT_CODES[ExitCode.CONFIG_INVALID]

    report = run_activation_check(
        draft_path=args.draft,
        policy=policy,
        registry_root=args.registry,
        source_id=args.source_id,
        synthetic_confirmed=args.synthetic_test_only,
    )
    _emit_mapping_report(report, args.json, out)

    print(
        f"SOURCE_MAPPING_ACTIVATION_BLOCKED "
        f"{ReasonCode.MAPPING_ACTIVATION_ALWAYS_BLOCKED.value}",
        file=err,
    )
    print(
        "Der Draft-Validator aktiviert kein Mapping und keine Source.", file=err
    )
    print(
        "Eine Aktivierung erfordert eine menschliche Entscheidung und ein "
        "Mapping Activation Gate außerhalb dieses MVP.",
        file=err,
    )
    return EXIT_CODES[ExitCode.SOURCE_MAPPING_ACTIVATION_BLOCKED]


# -- source-mapping activation-evaluate (CBP-WP-016) ----------------------

_GATE_DISCLAIMER = (
    "Der Report ist keine Gatefreigabe und keine Aktivierungsautorisierung "
    "(A6). evaluation_status ist ausschliesslich NOT_EVALUATED oder BLOCKED und "
    "bedeutet keine Freigabe. READY FOR ACTIVATION DECISION, APPROVED FOR "
    "ACTIVATION und REVOKED sind im synthetischen MVP nicht erreichbar."
)


def _render_gate_report(report: object) -> str:
    """Rendert den Gate-Report minimiert — ohne Pfad, URL, Inhalt oder Ref."""
    from .gate import GateEvaluationReport

    assert isinstance(report, GateEvaluationReport)
    lines = [
        f"evaluation_status:      {report.evaluation_status.value}",
        f"source_id:              {report.source_id}",
        f"mapping_id:             {report.mapping_id}",
        f"mapping_draft_sha256:   {report.mapping_draft_sha256}",
        f"mapping_policy_sha256:  {report.mapping_policy_sha256}",
        f"registry_record_sha256: {report.registry_record_sha256}",
        f"gate_contract_revision: {report.gate_contract_revision}",
        f"gate_contract_sha256:   {report.gate_contract_sha256}",
        f"evidence_contract_revision: {report.evidence_contract_revision}",
        f"evidence_contract_sha256:   {report.evidence_contract_sha256}",
        f"report_schema_version:  {report.report_schema_version}",
        f"blocker_count:          {report.blocker_count}",
        f"missing_evidence_count: {report.missing_evidence_count}",
        f"human_decision_count:   {report.human_decision_count}",
        f"evidence_count:         {report.evidence_count}",
        f"validated_artifact_count:    {report.validated_artifact_count}",
        f"invalid_artifact_count:      {report.invalid_artifact_count}",
        f"stale_artifact_count:        {report.stale_artifact_count}",
        f"conflicting_artifact_count:  {report.conflicting_artifact_count}",
        f"security_contract_revision:  {report.security_contract_revision}",
        f"security_contract_sha256:    {report.security_contract_sha256}",
        f"documented_control_count:        {report.documented_control_count}",
        f"runtime_scoped_control_count:    {report.runtime_scoped_control_count}",
        f"runtime_scoped_binding_count:    {report.runtime_scoped_binding_count}",
        f"valid_form_binding_count:        {report.valid_form_binding_count}",
        f"missing_form_binding_count:      {report.missing_form_binding_count}",
        f"invalid_form_binding_count:      {report.invalid_form_binding_count}",
        f"stale_form_binding_count:        {report.stale_form_binding_count}",
        f"conflicting_form_binding_count:  {report.conflicting_form_binding_count}",
        f"operationally_unevaluated_binding_count: "
        f"{report.operationally_unevaluated_binding_count}",
        f"implementation_version: {report.implementation_version}",
        "criterion_results:",
    ]
    lines.extend(
        f"  {c.code} stufe={c.nachweisstufe} {c.result.value}"
        for c in report.criterion_results
    )
    lines.append("blocker_codes:")
    lines.extend(f"  {code}" for code in report.blocker_codes)
    lines.extend(["", _GATE_DISCLAIMER])
    return "\n".join(lines)


def _emit_gate_report(report: object, as_json: bool, out: TextIO) -> None:
    """Gibt den Gate-Report aus (kanonisches JSON bei ``--json``); speichert nichts."""
    from .gate import GateEvaluationReport

    assert isinstance(report, GateEvaluationReport)
    if as_json:
        print(json.dumps(report.to_dict(), indent=2, sort_keys=True), file=out)
    else:
        print(_render_gate_report(report), file=out)


def _cmd_mapping_activation_evaluate(
    args: argparse.Namespace, out: TextIO, err: TextIO
) -> int:
    """``source-mapping activation-evaluate`` — read-only Gate-Evaluator.

    Bewertet die 20 kanonischen Gate-Kriterien gegen ein synthetisches
    Evidenz-Bundle und endet **immer** fail-closed ``BLOCKED`` (Exitcode 14).
    Schreibt **nichts**, aktiviert **nichts**. Eine ungültige Policy liefert
    Exitcode 2.
    """
    from .gate import run_activation_evaluate
    from .mapping import load_policy

    try:
        policy = load_policy(args.policy)
    except MappingPolicyError as exc:
        print(f"MAPPING_POLICY_INVALID {exc.reason.value}".rstrip(), file=err)
        return EXIT_CODES[ExitCode.CONFIG_INVALID]

    try:
        report = run_activation_evaluate(
            draft_path=args.draft,
            policy=policy,
            registry_root=args.registry,
            source_id=args.source_id,
            evidence_path=args.evidence,
            synthetic_confirmed=args.synthetic_test_only,
        )
    except GateEvidenceError as exc:
        print(f"MAPPING_GATE_BLOCKED {exc.reason.value}".rstrip(), file=err)
        return EXIT_CODES[ExitCode.MAPPING_GATE_EVALUATION_BLOCKED]

    _emit_gate_report(report, args.json, out)
    # Der synthetische MVP endet immer BLOCKED — keine Freigabe, keine Aktivierung.
    return EXIT_CODES[ExitCode.MAPPING_GATE_EVALUATION_BLOCKED]


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
        case "source-registry":
            return _cmd_source_registry(args, out, err)
        case "source-mapping":
            return _cmd_source_mapping(args, out, err)
        case _:  # pragma: no cover — argparse erzwingt ein bekanntes Kommando
            print("USAGE_ERROR unknown command", file=err)
            return EXIT_CODES[ExitCode.USAGE_ERROR]
