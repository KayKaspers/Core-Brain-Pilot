"""Read-only Validierung eines beobachteten Zustands gegen den KB-04-Contract.

Dieses Modul enthält die **injizierbaren Beobachtungsmodelle** der vier
Prüfdimensionen (Contract §7.1) und die read-only Prüfungen darüber.

**Keine Funktion dieses Moduls schreibt, erstellt, löscht, ruft ``chmod`` oder
``chown``, verändert Mounts, löst Identitäten auf oder erfindet reale
Deploymentwerte.** Es gibt keine Mutationsfunktion und keinen Mutationspfad.

**Herkunft ist Pflicht.** Jeder Zustand trägt eine explizite
:class:`ObservationOrigin`. Ein ``SYNTHETIC``- oder ``DECLARED``-Zustand darf
die Vertragslogik durchlaufen, erzeugt aber **niemals allein** eine operative
Verifikation, erfüllt **niemals** NT-04 oder NT-05, schließt **OD-37 nicht**,
stellt **keine** Gate-Evidenz dar und stuft **KB-04 nicht** hoch.

**Dimensionsisolation (MT-9 bis MT-11).** Eine Dimension belegt keine andere:
ein im Bundle deklarierter Modus (D-II) ist kein Nachweis der Host-Quellrechte
(D-I); die Runtimesicht (D-III) belegt D-I nicht und umgekehrt. Eine fehlende
Dimension ist ``INDETERMINATE`` und **niemals** ``CONFORM`` (MT-13).

Der Import dieses Moduls hat keine Nebenwirkungen.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Final

from ..errors import ReasonCode
from .aggregate import Finding, FindingStatus
from .binding import IdentityBinding, validate_binding
from .contract import (
    SPECIAL_BITS,
    WORLD_WRITE_BITS,
    Dimension,
    MountMode,
    ObjectKind,
    PathClass,
    PermissionProfile,
    ServiceRole,
    path_class_spec,
    profile_spec,
)

__all__ = [
    "ObservationOrigin",
    "ContentClassification",
    "HostObjectState",
    "MountState",
    "RuntimeObjectState",
    "RuntimeIdentityState",
    "Observation",
    "validate_observation",
]

#: World-Read-Bit. Nur PP-3b darf es tragen (Regel G-2, 3b-10 bis 3b-16).
_WORLD_READ_BIT: Final[int] = 0o004

#: Permission-Bits ohne Sonderbits.
_PERM_MASK: Final[int] = 0o777


class ObservationOrigin(StrEnum):
    """Herkunft eines beobachteten Zustands. Wird niemals still angenommen.

    ``SYNTHETIC``
        Test- oder Fixturewert. **Keine** operative Evidenz.
    ``DECLARED``
        Explizite Operator- oder Contract-Angabe. **Nicht** technisch gemessen.
    ``OBSERVED``
        Technisch beobachteter Zustand. In B2A regelmäßig nur über injizierte
        Testdaten repräsentiert.
    """

    SYNTHETIC = "SYNTHETIC"
    DECLARED = "DECLARED"
    OBSERVED = "OBSERVED"


class ContentClassification(StrEnum):
    """Deklarative Inhaltsklassifikation für PP-3b (Regeln 3b-6 bis 3b-8).

    Es findet **keine Inhaltsanalyse** und **kein Secret-Scanning** statt. Die
    Klassifikation ist eine erklärte Zusage, kein Messergebnis; sie definiert
    **keine** Secret-Management-Architektur (das bleibt KB-08).
    """

    NON_SECRET_RUNTIME_CONFIG = "NON_SECRET_RUNTIME_CONFIG"
    SENSITIVE_OR_SECRET = "SENSITIVE_OR_SECRET"
    UNCLASSIFIED = "UNCLASSIFIED"


@dataclass(frozen=True, slots=True)
class HostObjectState:
    """D-I — Zustand des Host-Quellobjekts vor der Einbindung.

    ``owner_ref`` und ``group_ref`` sind **opake Referenzen**; sie werden
    verglichen, nicht aufgelöst.
    """

    owner_ref: str
    group_ref: str
    mode: int
    object_kind: ObjectKind
    is_symlink: bool
    is_hardlinked: bool
    origin: ObservationOrigin


@dataclass(frozen=True, slots=True)
class MountState:
    """D-II — Zustand des Mountvertrags."""

    mode: MountMode
    expected_target: str
    unexpected_mounts: tuple[str, ...]
    crosses_boundary: bool
    origin: ObservationOrigin


@dataclass(frozen=True, slots=True)
class RuntimeObjectState:
    """D-III — Zustand des Objekts, wie die Runtime es sieht."""

    visible_mode: int
    object_kind: ObjectKind
    relative_path: str
    readable: bool
    writable: bool
    origin: ObservationOrigin


@dataclass(frozen=True, slots=True)
class RuntimeIdentityState:
    """D-IV — Zustand der effektiven Runtimeidentität."""

    effective_identity_ref: str
    supplementary_group_refs: tuple[str, ...]
    role: ServiceRole | str
    origin: ObservationOrigin


@dataclass(frozen=True, slots=True)
class Observation:
    """Vollständige Beobachtung eines Artefakts über bis zu vier Dimensionen.

    Eine fehlende Dimension ist ``None`` und führt zu ``INDETERMINATE`` —
    niemals zu ``CONFORM`` (MT-13).
    """

    path_class: PathClass
    relative_path: str
    host: HostObjectState | None = None
    mount: MountState | None = None
    runtime_object: RuntimeObjectState | None = None
    runtime_identity: RuntimeIdentityState | None = None
    content_classification: ContentClassification | None = None
    content_origin: ObservationOrigin | None = None


def _finding(
    observation: Observation,
    dimension: Dimension | str,
    status: FindingStatus,
    reason: ReasonCode | None,
    detail: str,
    origin: ObservationOrigin | None,
) -> Finding:
    """Baut einen Befund ohne realen Wert im Detailtext."""
    return Finding(
        path_class=observation.path_class,
        relative_path=observation.relative_path,
        dimension=dimension,
        status=status,
        reason=reason,
        detail=detail,
        origin=origin,
    )


def _missing(observation: Observation, dimension: Dimension) -> Finding:
    """Baut den fail-closed Befund einer fehlenden Dimension (MT-13)."""
    return _finding(
        observation,
        dimension,
        FindingStatus.INDETERMINATE,
        ReasonCode.KB04_STATE_INDETERMINATE,
        f"dimension not observable: {dimension.value}",
        None,
    )


def _check_modes(
    observation: Observation,
    dimension: Dimension,
    mode: int,
    expected: int | None,
    profile: PermissionProfile,
    origin: ObservationOrigin,
) -> list[Finding]:
    """Prüft Modusbits gegen das Profil. Read-only, ohne Mutation."""
    findings: list[Finding] = []
    spec = profile_spec(profile)

    if mode & WORLD_WRITE_BITS:
        findings.append(
            _finding(
                observation,
                dimension,
                FindingStatus.VIOLATION,
                ReasonCode.KB04_MODE_WORLD_BITS,
                "world-writable is forbidden without exception",
                origin,
            )
        )
    if (mode & _WORLD_READ_BIT) and not spec.world_read_allowed:
        findings.append(
            _finding(
                observation,
                dimension,
                FindingStatus.VIOLATION,
                ReasonCode.KB04_MODE_WORLD_BITS,
                "world-readable not permitted for this profile",
                origin,
            )
        )
    if mode & SPECIAL_BITS:
        setgid_dir = (
            spec.setgid_dir_allowed
            and (mode & SPECIAL_BITS) == 0o2000
            and expected == spec.dir_mode
        )
        if not setgid_dir:
            findings.append(
                _finding(
                    observation,
                    dimension,
                    FindingStatus.VIOLATION,
                    ReasonCode.KB04_MODE_SPECIAL_BITS,
                    "forbidden special bits",
                    origin,
                )
            )
    if expected is not None and (mode & _PERM_MASK) != expected:
        findings.append(
            _finding(
                observation,
                dimension,
                FindingStatus.VIOLATION,
                ReasonCode.KB04_MODE_MISMATCH,
                "mode does not match the profile",
                origin,
            )
        )
    return findings


def _check_host(observation: Observation) -> list[Finding]:
    """Prüft D-I — Host-Quellobjekt. Belegt keine andere Dimension (MT-10)."""
    host = observation.host
    if host is None:
        return [_missing(observation, Dimension.D_I)]

    spec = path_class_spec(observation.path_class)
    findings: list[Finding] = []

    if spec.profile is None:
        return [
            _finding(
                observation,
                Dimension.D_I,
                FindingStatus.VIOLATION,
                ReasonCode.KB04_PATHCLASS_UNKNOWN,
                "path class carries no profile",
                host.origin,
            )
        ]

    profile = profile_spec(spec.profile)

    if not profile.present:
        # PP-4: der Bereich darf schlicht nicht existieren.
        if host.object_kind is not ObjectKind.ABSENT:
            findings.append(
                _finding(
                    observation,
                    Dimension.D_I,
                    FindingStatus.VIOLATION,
                    ReasonCode.KB04_OBJECT_KIND_INVALID,
                    "not-present area must not exist",
                    host.origin,
                )
            )
        else:
            findings.append(
                _finding(
                    observation,
                    Dimension.D_I,
                    FindingStatus.CONFORM,
                    None,
                    "not-present area absent as required",
                    host.origin,
                )
            )
        return findings

    if host.is_symlink:
        findings.append(
            _finding(
                observation,
                Dimension.D_I,
                FindingStatus.VIOLATION,
                ReasonCode.KB04_LINK_SYMLINK_ESCAPE,
                "symlink is rejected, not resolved",
                host.origin,
            )
        )
    if host.is_hardlinked:
        findings.append(
            _finding(
                observation,
                Dimension.D_I,
                FindingStatus.VIOLATION,
                ReasonCode.KB04_LINK_HARDLINK,
                "hardlink in protected area",
                host.origin,
            )
        )
    if host.object_kind not in spec.object_kinds:
        findings.append(
            _finding(
                observation,
                Dimension.D_I,
                FindingStatus.VIOLATION,
                ReasonCode.KB04_OBJECT_KIND_INVALID,
                f"object kind not permitted: {host.object_kind.value}",
                host.origin,
            )
        )

    if spec.owner_role is not None and host.owner_ref != spec.owner_role.value:
        findings.append(
            _finding(
                observation,
                Dimension.D_I,
                FindingStatus.VIOLATION,
                ReasonCode.KB04_OWNER_MISMATCH,
                "owner role does not match the contract",
                host.origin,
            )
        )

    allowed_groups = {r.value for r in spec.reader_roles}
    if spec.owner_role is not None:
        allowed_groups.add(spec.owner_role.value)
    if allowed_groups and host.group_ref not in allowed_groups:
        findings.append(
            _finding(
                observation,
                Dimension.D_I,
                FindingStatus.VIOLATION,
                ReasonCode.KB04_GROUP_MISMATCH,
                "group role does not match the contract",
                host.origin,
            )
        )

    expected = (
        profile.dir_mode
        if host.object_kind is ObjectKind.DIRECTORY
        else profile.file_mode
    )
    findings.extend(
        _check_modes(
            observation,
            Dimension.D_I,
            host.mode,
            expected,
            spec.profile,
            host.origin,
        )
    )

    if not findings:
        findings.append(
            _finding(
                observation,
                Dimension.D_I,
                FindingStatus.CONFORM,
                None,
                "host source object matches the contract",
                host.origin,
            )
        )
    return findings


def _check_mount(observation: Observation) -> list[Finding]:
    """Prüft D-II — Mountvertrag. Belegt D-I nicht (MT-9)."""
    mount = observation.mount
    if mount is None:
        return [_missing(observation, Dimension.D_II)]

    spec = path_class_spec(observation.path_class)
    findings: list[Finding] = []

    if mount.mode is MountMode.UNKNOWN:
        findings.append(
            _finding(
                observation,
                Dimension.D_II,
                FindingStatus.INDETERMINATE,
                ReasonCode.KB04_MOUNT_MODE_MISMATCH,
                "unknown mount status is fail-closed",
                mount.origin,
            )
        )
    elif mount.mode is not spec.mount_mode:
        findings.append(
            _finding(
                observation,
                Dimension.D_II,
                FindingStatus.VIOLATION,
                ReasonCode.KB04_MOUNT_MODE_MISMATCH,
                f"mount mode is not {spec.mount_mode.value}",
                mount.origin,
            )
        )
    if mount.unexpected_mounts:
        findings.append(
            _finding(
                observation,
                Dimension.D_II,
                FindingStatus.VIOLATION,
                ReasonCode.KB04_MOUNT_MODE_MISMATCH,
                "unexpected additional mount",
                mount.origin,
            )
        )
    if mount.crosses_boundary:
        findings.append(
            _finding(
                observation,
                Dimension.D_II,
                FindingStatus.VIOLATION,
                ReasonCode.KB04_PATH_OUTSIDE_ROOT,
                "path crosses a mount boundary",
                mount.origin,
            )
        )

    if not findings:
        findings.append(
            _finding(
                observation,
                Dimension.D_II,
                FindingStatus.CONFORM,
                None,
                "mount contract matches",
                mount.origin,
            )
        )
    return findings


def _check_runtime_object(observation: Observation) -> list[Finding]:
    """Prüft D-III — Runtime-sichtbares Objekt. Belegt D-I nicht (MT-11)."""
    runtime = observation.runtime_object
    if runtime is None:
        return [_missing(observation, Dimension.D_III)]

    spec = path_class_spec(observation.path_class)
    findings: list[Finding] = []

    if spec.profile is None:
        return [
            _finding(
                observation,
                Dimension.D_III,
                FindingStatus.VIOLATION,
                ReasonCode.KB04_PATHCLASS_UNKNOWN,
                "path class carries no profile",
                runtime.origin,
            )
        ]

    profile = profile_spec(spec.profile)

    if not profile.present:
        if runtime.object_kind is not ObjectKind.ABSENT:
            findings.append(
                _finding(
                    observation,
                    Dimension.D_III,
                    FindingStatus.VIOLATION,
                    ReasonCode.KB04_OBJECT_KIND_INVALID,
                    "not-present area is reachable",
                    runtime.origin,
                )
            )
        else:
            findings.append(
                _finding(
                    observation,
                    Dimension.D_III,
                    FindingStatus.CONFORM,
                    None,
                    "not-present area unreachable as required",
                    runtime.origin,
                )
            )
        return findings

    # Ein Bereich ohne Schreibrolle darf für die Runtime nicht schreibbar sein.
    if runtime.writable and not spec.writer_roles:
        findings.append(
            _finding(
                observation,
                Dimension.D_III,
                FindingStatus.VIOLATION,
                ReasonCode.KB04_MOUNT_MODE_MISMATCH,
                "runtime must not be able to write this area",
                runtime.origin,
            )
        )
    if not runtime.readable:
        findings.append(
            _finding(
                observation,
                Dimension.D_III,
                FindingStatus.VIOLATION,
                ReasonCode.KB04_MODE_MISMATCH,
                "area is not readable as required",
                runtime.origin,
            )
        )
    if runtime.object_kind not in spec.object_kinds:
        findings.append(
            _finding(
                observation,
                Dimension.D_III,
                FindingStatus.VIOLATION,
                ReasonCode.KB04_OBJECT_KIND_INVALID,
                f"object kind not permitted: {runtime.object_kind.value}",
                runtime.origin,
            )
        )

    expected = (
        profile.dir_mode
        if runtime.object_kind is ObjectKind.DIRECTORY
        else profile.file_mode
    )
    findings.extend(
        _check_modes(
            observation,
            Dimension.D_III,
            runtime.visible_mode,
            expected,
            spec.profile,
            runtime.origin,
        )
    )

    if not findings:
        findings.append(
            _finding(
                observation,
                Dimension.D_III,
                FindingStatus.CONFORM,
                None,
                "runtime view matches the contract",
                runtime.origin,
            )
        )
    return findings


def _check_runtime_identity(
    observation: Observation, binding: IdentityBinding | None
) -> list[Finding]:
    """Prüft D-IV — Runtimeidentität gegen die erklärte Bindung."""
    identity = observation.runtime_identity
    if identity is None:
        return [_missing(observation, Dimension.D_IV)]

    findings: list[Finding] = []
    if binding is None:
        findings.append(
            _finding(
                observation,
                Dimension.D_IV,
                FindingStatus.VIOLATION,
                ReasonCode.KB04_BINDING_MISSING,
                "no identity binding declared",
                identity.origin,
            )
        )
        return findings

    if identity.effective_identity_ref != binding.expected_effective_identity:
        findings.append(
            _finding(
                observation,
                Dimension.D_IV,
                FindingStatus.VIOLATION,
                ReasonCode.KB04_IDENTITY_MISMATCH,
                "effective identity differs from the declared binding",
                identity.origin,
            )
        )
    if str(identity.role) != str(binding.role_id):
        findings.append(
            _finding(
                observation,
                Dimension.D_IV,
                FindingStatus.VIOLATION,
                ReasonCode.KB04_ROLE_UNKNOWN,
                "role differs from the declared binding",
                identity.origin,
            )
        )

    declared_groups = set(binding.read_group_refs) | {binding.primary_group_ref}
    unexpected = tuple(
        sorted(set(identity.supplementary_group_refs) - declared_groups)
    )
    if unexpected:
        findings.append(
            _finding(
                observation,
                Dimension.D_IV,
                FindingStatus.VIOLATION,
                ReasonCode.KB04_GROUP_MISMATCH,
                "unexpected supplementary group",
                identity.origin,
            )
        )

    if not findings:
        findings.append(
            _finding(
                observation,
                Dimension.D_IV,
                FindingStatus.CONFORM,
                None,
                "runtime identity matches the declared binding",
                identity.origin,
            )
        )
    return findings


def _check_pp3b(observation: Observation) -> list[Finding]:
    """Prüft die PP-3b-Grenzen (Regeln 3b-1 bis 3b-16)."""
    spec = path_class_spec(observation.path_class)
    findings: list[Finding] = []

    profile = spec.profile
    if profile is PermissionProfile.PP_3B:
        exclusive = profile_spec(profile).exclusive_path_class
        if exclusive is not None and observation.path_class is not exclusive:
            findings.append(
                _finding(
                    observation,
                    Dimension.D_I,
                    FindingStatus.VIOLATION,
                    ReasonCode.KB04_CONTRACT_INVALID,
                    "PP-3b used outside its exclusive path class",
                    None,
                )
            )

    if not spec.secret_free_required:
        return findings

    classification = observation.content_classification
    origin = observation.content_origin

    if classification is None or classification is (
        ContentClassification.UNCLASSIFIED
    ):
        # Kein Default auf secret-free: unklassifiziert ist fail-closed.
        findings.append(
            _finding(
                observation,
                Dimension.D_I,
                FindingStatus.INDETERMINATE,
                ReasonCode.KB04_STATE_INDETERMINATE,
                "content classification missing or unclassified",
                origin,
            )
        )
    elif classification is ContentClassification.SENSITIVE_OR_SECRET:
        findings.append(
            _finding(
                observation,
                Dimension.D_I,
                FindingStatus.VIOLATION,
                ReasonCode.KB04_CONTRACT_INVALID,
                "sensitive or secret content is not classifiable as PP-3b",
                origin,
            )
        )
    elif origin is None:
        # Eine Zusage ohne erklärte Herkunft ist nicht feststellbar.
        findings.append(
            _finding(
                observation,
                Dimension.D_I,
                FindingStatus.INDETERMINATE,
                ReasonCode.KB04_STATE_INDETERMINATE,
                "content classification without declared origin",
                None,
            )
        )
    else:
        findings.append(
            _finding(
                observation,
                Dimension.D_I,
                FindingStatus.CONFORM,
                None,
                "declared non-secret runtime configuration",
                origin,
            )
        )
    return findings


def validate_observation(
    observation: Observation, binding: IdentityBinding | None
) -> tuple[Finding, ...]:
    """Validiert eine Beobachtung read-only gegen den Contract.

    Die vier Dimensionen werden **getrennt** geprüft; keine belegt eine andere
    (MT-9 bis MT-11). Eine fehlende Dimension ist ``INDETERMINATE`` (MT-13).

    Die Funktion **verändert nichts**: kein Schreibvorgang, keine
    Rechteänderung, keine Identitätsauflösung, keine Mountänderung.

    Args:
        observation: Der beobachtete Zustand.
        binding: Die erklärte Identitätsbindung oder ``None``.

    Returns:
        Die Befunde in deterministischer Reihenfolge.
    """
    if observation.path_class is PathClass.PC_11:
        return (
            _finding(
                observation,
                Dimension.D_I,
                FindingStatus.VIOLATION,
                ReasonCode.KB04_PATHCLASS_UNKNOWN,
                "unclassified path is forbidden, not neutral",
                None,
            ),
        )

    findings: list[Finding] = []
    findings.extend(validate_binding(binding))
    findings.extend(_check_host(observation))
    findings.extend(_check_mount(observation))
    findings.extend(_check_runtime_object(observation))
    findings.extend(_check_runtime_identity(observation, binding))
    findings.extend(_check_pp3b(observation))
    return tuple(sorted(findings))
