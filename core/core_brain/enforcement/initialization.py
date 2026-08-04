"""Read-only Initialisierungs**planung** für KB-04-Zielstrukturen.

Umsetzung von Teilphase **B2B-P** aus CBP-WP-022 auf Grundlage von
**ADR-0014** (A1), **D-060** (A0) und Contract §9 und §12.

**Dieses Modul ist Plan-only.** Es beobachtet, klassifiziert und **beschreibt**
Operationen — es führt keine aus. Es gibt bewusst **kein** ``apply_plan``,
``execute_plan``, ``initialize`` oder ``create_target``, und es ruft weder
``mkdir`` noch ``chmod``, ``chown``, ``unlink``, ``rename`` oder ``replace``
auf. Sämtliche Dateisystemsicht läuft über den **read-only**
:class:`~core.core_brain.enforcement.filesystem_adapter.FilesystemAdapter`,
der mutierende Operationen gar nicht erst kennt.

**Ein Plan ist keine Initialisierung.** ``applicable=True`` bedeutet
ausschließlich: *nach Contract wäre dieser Plan ausführbar*. Es bedeutet
**nicht**, dass er ausgeführt wurde, und **nicht**, dass eine ausführende
Funktion existiert. ``operationally_verified`` ist in B2B-P **immer** ``False``.

**Eine spätere Apply-Phase ist nicht autorisiert** und verlangt eine erneute
ADR-Erforderlichkeitsprüfung sowie die Klärung, wo das Setup-Werkzeug lebt
(ADR-0014 verortet die Durchsetzungsschicht außerhalb der Runtime und
außerhalb des Repositorys).

**KB-04 bleibt `DOCUMENTED ONLY`.** Kein Ergebnis dieses Moduls ist operative
Evidenz, erfüllt NT-04 oder NT-05, schließt OD-37 oder stuft eine Control hoch.

Der Import dieses Moduls hat keine Nebenwirkungen.
"""

from __future__ import annotations

import hashlib
import stat as stat_module
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Final

from ..errors import ReasonCode
from .aggregate import Finding, FindingStatus, canonical_json_bytes
from .binding import IdentityBinding, validate_binding
from .contract import (
    Actor,
    Dimension,
    ObjectKind,
    PathClass,
    PermissionProfile,
    path_class_spec,
    profile_spec,
    validate_contract,
)
from .filesystem_adapter import FilesystemAdapter

__all__ = [
    "TargetState",
    "InitializationStatus",
    "OperationKind",
    "TargetPathBinding",
    "InitializationRequest",
    "PlannedOperation",
    "InitializationPlan",
    "TargetAssessment",
    "InitializationAssessment",
    "assess_target",
    "build_initialization_plan",
    "verify_initialized",
]

#: Repositorywurzel — ein Ziel darf niemals innerhalb liegen. Muster aus
#: ``quarantine/store.py`` und ``registry/storage.py``.
_REPO_ROOT: Final[Path] = Path(__file__).resolve().parents[3]


class TargetState(StrEnum):
    """Klassifikation des beobachteten Zielzustands (Contract §9.1, §9.2)."""

    NEW_ABSENT = "NEW_ABSENT"
    NEW_EMPTY = "NEW_EMPTY"
    ALREADY_INITIALIZED = "ALREADY_INITIALIZED"
    PARTIAL = "PARTIAL"
    MIGRATION_REQUIRED = "MIGRATION_REQUIRED"
    REPAIR_REQUIRED = "REPAIR_REQUIRED"
    INDETERMINATE = "INDETERMINATE"
    BLOCKED = "BLOCKED"


class InitializationStatus(StrEnum):
    """Ergebnisstatus einer Planung.

    Es gibt bewusst **kein** ``APPLIED``, ``APPLYING``, ``ROLLED_BACK`` und
    ``CLEANED_UP`` — diese Zustände sind in B2B-P nicht erreichbar und dürfen
    auch nicht behauptbar sein.
    """

    PLANNED = "PLANNED"
    ALREADY_INITIALIZED = "ALREADY_INITIALIZED"
    BLOCKED = "BLOCKED"
    PARTIAL = "PARTIAL"
    MIGRATION_REQUIRED = "MIGRATION_REQUIRED"
    REPAIR_REQUIRED = "REPAIR_REQUIRED"
    INDETERMINATE = "INDETERMINATE"


class OperationKind(StrEnum):
    """Deklarative Planoperation. **Keine ausführbare Aktion.**"""

    CREATE_ROOT = "CREATE_ROOT"
    CREATE_CLASS_DIRECTORY = "CREATE_CLASS_DIRECTORY"
    POST_VALIDATE = "POST_VALIDATE"


@dataclass(frozen=True, slots=True, order=True)
class TargetPathBinding:
    """Bindung einer Pfadklasse an einen **relativen** Zielpfad."""

    path_class: PathClass
    relative_path: str

    def to_dict(self) -> dict[str, str]:
        """Deterministische, JSON-taugliche Darstellung."""
        return {
            "path_class": self.path_class.value,
            "relative_path": self.relative_path,
        }


@dataclass(frozen=True, slots=True)
class InitializationRequest:
    """Anfrage einer Initialisierungsplanung.

    ``boundary_root`` und ``target_root`` sind reale Pfade und dienen
    ausschließlich der internen Prüfung; sie erscheinen **niemals** in einer
    kanonisch serialisierten Ausgabe. Nach außen steht der opake
    ``target_ref``.
    """

    authority: Actor
    boundary_root: Path
    target_root: Path
    target_ref: str
    path_bindings: tuple[TargetPathBinding, ...]
    identity_binding: IdentityBinding | None

    def stable_mapping(self) -> dict[str, object]:
        """Baut die pfadfreie, kanonische Darstellung der Anfrage."""
        return {
            "authority": self.authority.value,
            "identity_binding": (
                self.identity_binding.to_dict()
                if self.identity_binding is not None
                else None
            ),
            "path_bindings": [
                b.to_dict() for b in sorted(self.path_bindings)
            ],
            "target_ref": self.target_ref,
        }

    def digest(self) -> str:
        """Deterministischer SHA-256 der pfadfreien Anfragedarstellung."""
        return hashlib.sha256(
            canonical_json_bytes(self.stable_mapping())
        ).hexdigest()


@dataclass(frozen=True, slots=True, order=True)
class PlannedOperation:
    """Eine **beschriebene**, nicht ausgeführte Operation."""

    sequence: int
    kind: OperationKind
    path_class: PathClass | str
    relative_path: str
    object_kind: ObjectKind | str
    expected_mode: int | None
    owner_role: str | None
    group_role: str | None
    preconditions: tuple[str, ...]
    postconditions: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        """Deterministische, JSON-taugliche Darstellung ohne absolute Pfade."""
        return {
            "expected_mode": self.expected_mode,
            "group_role": self.group_role,
            "kind": self.kind.value,
            "object_kind": str(self.object_kind),
            "owner_role": self.owner_role,
            "path_class": str(self.path_class),
            "postconditions": list(self.postconditions),
            "preconditions": list(self.preconditions),
            "relative_path": self.relative_path,
            "sequence": self.sequence,
        }


@dataclass(frozen=True, slots=True)
class InitializationPlan:
    """Vollständiger, deterministischer und **wirkungsfreier** Plan."""

    request_digest: str
    target_ref: str
    status: InitializationStatus
    operations: tuple[PlannedOperation, ...]
    findings: tuple[Finding, ...]
    applicable: bool

    def to_dict(self) -> dict[str, object]:
        """Deterministische, JSON-taugliche Darstellung ohne absolute Pfade."""
        return {
            "applicable": self.applicable,
            "findings": [f.to_dict() for f in self.findings],
            "operations": [o.to_dict() for o in self.operations],
            "request_digest": self.request_digest,
            "status": self.status.value,
            "target_ref": self.target_ref,
        }


@dataclass(frozen=True, slots=True)
class TargetAssessment:
    """Read-only Klassifikation des Zielzustands."""

    state: TargetState
    findings: tuple[Finding, ...]

    def to_dict(self) -> dict[str, object]:
        """Deterministische, JSON-taugliche Darstellung."""
        return {
            "findings": [f.to_dict() for f in self.findings],
            "state": self.state.value,
        }


@dataclass(frozen=True, slots=True)
class InitializationAssessment:
    """Gesamtbeurteilung einer Zielstruktur.

    ``operationally_verified`` ist in B2B-P **immer** ``False``: das Modul
    beobachtet über einen injizierbaren Adapter und erbringt keine reale
    Deploymentevidenz.
    """

    status: InitializationStatus
    plan: InitializationPlan
    findings: tuple[Finding, ...]
    conform: bool
    operationally_verified: bool

    def to_dict(self) -> dict[str, object]:
        """Deterministische, JSON-taugliche Darstellung."""
        return {
            "conform": self.conform,
            "findings": [f.to_dict() for f in self.findings],
            "operationally_verified": self.operationally_verified,
            "plan": self.plan.to_dict(),
            "status": self.status.value,
        }


def _finding(
    path_class: PathClass | str,
    relative_path: str,
    status: FindingStatus,
    reason: ReasonCode | None,
    detail: str,
) -> Finding:
    """Baut einen Planbefund ohne absoluten Pfad und ohne realen Wert."""
    return Finding(
        path_class=path_class,
        relative_path=relative_path,
        dimension=Dimension.D_I,
        status=status,
        reason=reason,
        detail=detail,
        origin=None,
    )


def _violation(relative_path: str, reason: ReasonCode, detail: str) -> Finding:
    """Kurzform für einen blockierenden Befund."""
    return _finding(
        PathClass.PC_11, relative_path, FindingStatus.VIOLATION, reason, detail
    )


def _indeterminate(relative_path: str, detail: str) -> Finding:
    """Kurzform für einen nicht feststellbaren Zustand."""
    return _finding(
        PathClass.PC_11,
        relative_path,
        FindingStatus.INDETERMINATE,
        ReasonCode.KB04_STATE_INDETERMINATE,
        detail,
    )


def _is_symlink(adapter: FilesystemAdapter, path: Path) -> bool:
    """Ob der Pfad selbst ein Symlink ist. Folgt keinem Ziel."""
    return stat_module.S_ISLNK(adapter.lstat(path).st_mode)


def _object_kind(st_mode: int) -> ObjectKind:
    """Bestimmt die Objektart aus einem ``lstat``-Modus."""
    if stat_module.S_ISLNK(st_mode):
        return ObjectKind.SYMLINK
    if stat_module.S_ISDIR(st_mode):
        return ObjectKind.DIRECTORY
    if stat_module.S_ISREG(st_mode):
        return ObjectKind.REGULAR_FILE
    return ObjectKind.OTHER


def _check_parent_chain(
    adapter: FilesystemAdapter, boundary: Path, target: Path
) -> list[Finding]:
    """Prüft alle Pfadbestandteile zwischen Boundary und Ziel auf Links."""
    findings: list[Finding] = []
    try:
        relative = target.relative_to(boundary)
    except ValueError:
        return findings
    current = boundary
    for part in relative.parts[:-1] if relative.parts else ():
        current = current / part
        try:
            if _is_symlink(adapter, current):
                findings.append(
                    _violation(
                        "<parent>",
                        ReasonCode.KB04_LINK_SYMLINK_ESCAPE,
                        "parent component is a symlink",
                    )
                )
        except FileNotFoundError:
            continue
        except OSError:
            findings.append(
                _indeterminate("<parent>", "parent component not observable")
            )
    return findings


def _classify_entries(
    adapter: FilesystemAdapter,
    request: InitializationRequest,
    target: Path,
) -> tuple[TargetState, list[Finding]]:
    """Klassifiziert den Inhalt eines vorhandenen, nicht leeren Ziels."""
    findings: list[Finding] = []
    expected = {b.relative_path.split("/")[0] for b in request.path_bindings}
    try:
        names = sorted(p.name for p in adapter.iterdir(target))
    except OSError:
        return TargetState.INDETERMINATE, [
            _indeterminate(request.target_ref, "target content not observable")
        ]

    unexpected = sorted(set(names) - expected)
    present = sorted(set(names) & expected)

    if unexpected:
        findings.append(
            _violation(
                request.target_ref,
                ReasonCode.KB04_MIGRATION_REQUIRED,
                "target holds content outside the contract model",
            )
        )
        return TargetState.MIGRATION_REQUIRED, findings

    if set(present) != expected:
        findings.append(
            _violation(
                request.target_ref,
                ReasonCode.KB04_INIT_PARTIAL,
                "target is only partially prepared",
            )
        )
        return TargetState.PARTIAL, findings

    # Alle erwarteten Klassenverzeichnisse vorhanden und nichts sonst. Ob sie
    # auch vertragskonform sind, entscheidet verify_initialized.
    for binding in sorted(request.path_bindings):
        entry = target / binding.relative_path
        try:
            kind = _object_kind(adapter.lstat(entry).st_mode)
        except OSError:
            findings.append(
                _indeterminate(
                    binding.relative_path, "entry state not observable"
                )
            )
            return TargetState.INDETERMINATE, findings
        if kind is not ObjectKind.DIRECTORY:
            findings.append(
                _finding(
                    binding.path_class,
                    binding.relative_path,
                    FindingStatus.VIOLATION,
                    ReasonCode.KB04_REPAIR_RT2_REQUIRED,
                    f"initialized entry is not a directory: {kind.value}",
                )
            )
            return TargetState.REPAIR_REQUIRED, findings

    return TargetState.ALREADY_INITIALIZED, findings


def assess_target(
    request: InitializationRequest, adapter: FilesystemAdapter
) -> TargetAssessment:
    """Klassifiziert den Zielzustand **vollständig read-only**.

    Zulässig für eine spätere Initialisierung sind ausschließlich die beiden
    Zustände :attr:`TargetState.NEW_ABSENT` und
    :attr:`TargetState.NEW_EMPTY` (Contract §9.1). **Alles andere ist
    fail-closed** — es wird gemeldet, nicht eingeordnet und niemals repariert.

    Args:
        request: Die Planungsanfrage.
        adapter: Der read-only Dateisystemadapter.

    Returns:
        Zustand und Befunde in deterministischer Reihenfolge.
    """
    findings: list[Finding] = []

    if not adapter.posix_semantics:
        findings.append(
            _violation(
                request.target_ref,
                ReasonCode.KB04_PLATFORM_UNSUPPORTED,
                "platform carries no POSIX permission semantics",
            )
        )
        return TargetAssessment(
            TargetState.INDETERMINATE, tuple(sorted(findings))
        )

    # --- Boundary ---------------------------------------------------------
    try:
        boundary = adapter.resolve(request.boundary_root)
        target = adapter.resolve(request.target_root)
    except OSError:
        return TargetAssessment(
            TargetState.INDETERMINATE,
            (_indeterminate(request.target_ref, "path not resolvable"),),
        )

    if target != boundary and not target.is_relative_to(boundary):
        findings.append(
            _violation(
                request.target_ref,
                ReasonCode.KB04_PATH_OUTSIDE_ROOT,
                "target leaves the boundary root",
            )
        )
        return TargetAssessment(TargetState.BLOCKED, tuple(sorted(findings)))

    if target == _REPO_ROOT or target.is_relative_to(_REPO_ROOT):
        findings.append(
            _violation(
                request.target_ref,
                ReasonCode.KB04_PATH_OUTSIDE_ROOT,
                "target lies inside the repository",
            )
        )
        return TargetAssessment(TargetState.BLOCKED, tuple(sorted(findings)))

    try:
        boundary_kind = _object_kind(adapter.lstat(boundary).st_mode)
    except FileNotFoundError:
        findings.append(
            _violation(
                request.target_ref,
                ReasonCode.KB04_PATH_OUTSIDE_ROOT,
                "boundary root does not exist",
            )
        )
        return TargetAssessment(TargetState.BLOCKED, tuple(sorted(findings)))
    except OSError:
        return TargetAssessment(
            TargetState.INDETERMINATE,
            (_indeterminate(request.target_ref, "boundary not observable"),),
        )

    if boundary_kind is ObjectKind.SYMLINK:
        findings.append(
            _violation(
                request.target_ref,
                ReasonCode.KB04_LINK_SYMLINK_ESCAPE,
                "boundary root is a symlink",
            )
        )
        return TargetAssessment(TargetState.BLOCKED, tuple(sorted(findings)))
    if boundary_kind is not ObjectKind.DIRECTORY:
        findings.append(
            _violation(
                request.target_ref,
                ReasonCode.KB04_OBJECT_KIND_INVALID,
                "boundary root is not a directory",
            )
        )
        return TargetAssessment(TargetState.BLOCKED, tuple(sorted(findings)))

    findings.extend(_check_parent_chain(adapter, boundary, target))
    if findings:
        state = (
            TargetState.INDETERMINATE
            if any(f.status is FindingStatus.INDETERMINATE for f in findings)
            else TargetState.BLOCKED
        )
        return TargetAssessment(state, tuple(sorted(findings)))

    # --- Ziel -------------------------------------------------------------
    try:
        target_mode = adapter.lstat(target).st_mode
    except FileNotFoundError:
        return TargetAssessment(TargetState.NEW_ABSENT, ())
    except OSError:
        return TargetAssessment(
            TargetState.INDETERMINATE,
            (_indeterminate(request.target_ref, "target not observable"),),
        )

    kind = _object_kind(target_mode)
    if kind is ObjectKind.SYMLINK:
        findings.append(
            _violation(
                request.target_ref,
                ReasonCode.KB04_LINK_SYMLINK_ESCAPE,
                "target root is a symlink",
            )
        )
        return TargetAssessment(TargetState.BLOCKED, tuple(sorted(findings)))
    if kind is not ObjectKind.DIRECTORY:
        findings.append(
            _violation(
                request.target_ref,
                ReasonCode.KB04_OBJECT_KIND_INVALID,
                f"target root is not a directory: {kind.value}",
            )
        )
        return TargetAssessment(TargetState.BLOCKED, tuple(sorted(findings)))

    try:
        if adapter.is_mount(target):
            findings.append(
                _violation(
                    request.target_ref,
                    ReasonCode.KB04_MOUNT_MODE_MISMATCH,
                    "target root is a mount point",
                )
            )
            return TargetAssessment(
                TargetState.BLOCKED, tuple(sorted(findings))
            )
    except OSError:
        return TargetAssessment(
            TargetState.INDETERMINATE,
            (_indeterminate(request.target_ref, "mount state not observable"),),
        )

    try:
        entries = list(adapter.iterdir(target))
    except OSError:
        return TargetAssessment(
            TargetState.INDETERMINATE,
            (_indeterminate(request.target_ref, "target content not observable"),),
        )

    if not entries:
        return TargetAssessment(TargetState.NEW_EMPTY, ())

    state, more = _classify_entries(adapter, request, target)
    findings.extend(more)
    return TargetAssessment(state, tuple(sorted(findings)))


def _validate_bindings(
    request: InitializationRequest,
) -> list[Finding]:
    """Prüft die relativen Pfadbindungen. Read-only, ohne Auflösung."""
    findings: list[Finding] = []
    if not request.path_bindings:
        findings.append(
            _violation(
                request.target_ref,
                ReasonCode.KB04_CONTRACT_INVALID,
                "no path binding supplied",
            )
        )
        return findings

    seen_classes: set[PathClass] = set()
    seen_paths: set[str] = set()
    for binding in sorted(request.path_bindings):
        rel = binding.relative_path
        if not rel or not rel.strip():
            findings.append(
                _violation(
                    request.target_ref,
                    ReasonCode.KB04_CONTRACT_INVALID,
                    "empty relative path",
                )
            )
            continue
        if Path(rel).is_absolute() or rel.startswith("/") or ":" in rel:
            findings.append(
                _violation(
                    rel,
                    ReasonCode.KB04_PATH_OUTSIDE_ROOT,
                    "binding path is absolute",
                )
            )
            continue
        if ".." in Path(rel).parts:
            findings.append(
                _violation(
                    rel,
                    ReasonCode.KB04_PATH_OUTSIDE_ROOT,
                    "binding path escapes the target root",
                )
            )
            continue
        if binding.path_class in seen_classes:
            findings.append(
                _violation(
                    rel,
                    ReasonCode.KB04_CONTRACT_INVALID,
                    f"duplicate path class: {binding.path_class.value}",
                )
            )
        if rel in seen_paths:
            findings.append(
                _violation(
                    rel,
                    ReasonCode.KB04_CONTRACT_INVALID,
                    "duplicate target path",
                )
            )
        seen_classes.add(binding.path_class)
        seen_paths.add(rel)

        spec = path_class_spec(binding.path_class)
        if spec.profile is None:
            findings.append(
                _violation(
                    rel,
                    ReasonCode.KB04_PATHCLASS_UNKNOWN,
                    "path class carries no profile",
                )
            )
    return findings


def _plan_operations(
    request: InitializationRequest,
) -> tuple[PlannedOperation, ...]:
    """Baut die deterministische Operationsfolge. **Führt nichts aus.**

    Pfadklassen mit ``PP-4`` (*not-present*) erzeugen **keine**
    Anlageoperation — der Bereich darf gerade nicht existieren.
    """
    operations: list[PlannedOperation] = [
        PlannedOperation(
            sequence=0,
            kind=OperationKind.CREATE_ROOT,
            path_class="",
            relative_path=".",
            object_kind=ObjectKind.DIRECTORY,
            expected_mode=None,
            owner_role=None,
            group_role=None,
            preconditions=("target is NEW_ABSENT or NEW_EMPTY",),
            postconditions=("root exists as a directory",),
        )
    ]

    sequence = 1
    for binding in sorted(request.path_bindings):
        spec = path_class_spec(binding.path_class)
        if spec.profile is None:
            continue
        profile = profile_spec(spec.profile)
        if not profile.present:
            # PP-4: not-present. Der Bereich wird nicht angelegt.
            continue
        operations.append(
            PlannedOperation(
                sequence=sequence,
                kind=OperationKind.CREATE_CLASS_DIRECTORY,
                path_class=binding.path_class,
                relative_path=binding.relative_path,
                object_kind=ObjectKind.DIRECTORY,
                expected_mode=profile.dir_mode,
                owner_role=(
                    spec.owner_role.value if spec.owner_role is not None else None
                ),
                group_role=(
                    spec.reader_roles[0].value if spec.reader_roles else None
                ),
                preconditions=("root exists", "entry does not exist"),
                postconditions=(
                    "entry exists as a directory",
                    "mode set at creation, not afterwards",
                    "no world-writable bit",
                ),
            )
        )
        sequence += 1

    operations.append(
        PlannedOperation(
            sequence=sequence,
            kind=OperationKind.POST_VALIDATE,
            path_class="",
            relative_path=".",
            object_kind=ObjectKind.DIRECTORY,
            expected_mode=None,
            owner_role=None,
            group_role=None,
            preconditions=("all create operations described above",),
            postconditions=("read-only validation reports CONFORM",),
        )
    )
    return tuple(operations)


_STATE_TO_STATUS: Final[dict[TargetState, InitializationStatus]] = {
    TargetState.ALREADY_INITIALIZED: InitializationStatus.ALREADY_INITIALIZED,
    TargetState.PARTIAL: InitializationStatus.PARTIAL,
    TargetState.MIGRATION_REQUIRED: InitializationStatus.MIGRATION_REQUIRED,
    TargetState.REPAIR_REQUIRED: InitializationStatus.REPAIR_REQUIRED,
    TargetState.INDETERMINATE: InitializationStatus.INDETERMINATE,
    TargetState.BLOCKED: InitializationStatus.BLOCKED,
}


def build_initialization_plan(
    request: InitializationRequest, adapter: FilesystemAdapter
) -> InitializationPlan:
    """Erzeugt einen deterministischen, **wirkungsfreien** Plan.

    Ein anwendbarer Plan entsteht ausschließlich bei
    :attr:`TargetState.NEW_ABSENT` oder :attr:`TargetState.NEW_EMPTY` und nur,
    wenn Contract, Authority, Identitätsbindung und Pfadbindungen fehlerfrei
    sind. **In jedem anderen Fall ist ``applicable`` ``False``.**

    ``applicable=True`` heißt: *nach Contract wäre der Plan ausführbar*. Es
    heißt **nicht**, dass er ausgeführt wurde — eine ausführende Funktion
    existiert in B2B-P nicht.

    Args:
        request: Die Planungsanfrage.
        adapter: Der read-only Dateisystemadapter.

    Returns:
        Der Plan mit Status, Operationen und Befunden.
    """
    findings: list[Finding] = []

    findings.extend(validate_contract())

    if request.authority is not Actor.DEPLOYMENT_SETUP:
        findings.append(
            _violation(
                request.target_ref,
                ReasonCode.KB04_ROLE_UNKNOWN,
                "only the deployment/setup actor may plan an initialization",
            )
        )

    findings.extend(validate_binding(request.identity_binding))
    findings.extend(_validate_bindings(request))

    blocking = [
        f
        for f in findings
        if f.status in (FindingStatus.VIOLATION, FindingStatus.INDETERMINATE)
    ]
    if blocking:
        return InitializationPlan(
            request_digest=request.digest(),
            target_ref=request.target_ref,
            status=InitializationStatus.BLOCKED,
            operations=(),
            findings=tuple(sorted(findings)),
            applicable=False,
        )

    assessment = assess_target(request, adapter)
    findings.extend(assessment.findings)

    if assessment.state in (TargetState.NEW_ABSENT, TargetState.NEW_EMPTY):
        # Revalidierung (Contract §10.3, LP-9): der Zustand wird ein zweites
        # Mal beobachtet. Weicht er ab, liegt ein Wettlauf vor — das Ergebnis
        # ist fail-closed und **niemals** ein anwendbarer Plan. Das schließt
        # TOCTOU nicht; jede Beobachtung bleibt eine Zeitpunktaussage.
        revalidation = assess_target(request, adapter)
        if revalidation.state is not assessment.state:
            findings.append(
                _indeterminate(
                    request.target_ref,
                    "target state changed between observations",
                )
            )
            findings.extend(revalidation.findings)
            return InitializationPlan(
                request_digest=request.digest(),
                target_ref=request.target_ref,
                status=InitializationStatus.INDETERMINATE,
                operations=(),
                findings=tuple(sorted(findings)),
                applicable=False,
            )
        return InitializationPlan(
            request_digest=request.digest(),
            target_ref=request.target_ref,
            status=InitializationStatus.PLANNED,
            operations=_plan_operations(request),
            findings=tuple(sorted(findings)),
            applicable=True,
        )

    return InitializationPlan(
        request_digest=request.digest(),
        target_ref=request.target_ref,
        status=_STATE_TO_STATUS[assessment.state],
        operations=(),
        findings=tuple(sorted(findings)),
        applicable=False,
    )


def verify_initialized(
    request: InitializationRequest, adapter: FilesystemAdapter
) -> InitializationAssessment:
    """Prüft **read-only**, ob eine Zielstruktur bereits vollständig vorbereitet ist.

    Unterscheidet ``ALREADY_INITIALIZED``, ``PARTIAL``, ``MIGRATION_REQUIRED``,
    ``REPAIR_REQUIRED`` und ``INDETERMINATE``.

    ``operationally_verified`` ist **immer** ``False``: die Beobachtung läuft
    über einen injizierbaren Adapter und ist keine reale Deploymentevidenz.

    Args:
        request: Die Planungsanfrage.
        adapter: Der read-only Dateisystemadapter.

    Returns:
        Die Gesamtbeurteilung samt Plan.
    """
    plan = build_initialization_plan(request, adapter)
    conform = plan.status is InitializationStatus.ALREADY_INITIALIZED
    return InitializationAssessment(
        status=plan.status,
        plan=plan,
        findings=plan.findings,
        conform=conform,
        operationally_verified=False,
    )
