"""Deterministische Fixturehelfer der KB-04-Tests (CBP-WP-022, Phase B2A).

Kein ``test_``-Praefix: das Modul wird von ``unittest discover`` nicht als
Testmodul entdeckt.

Alle Werte sind **synthetisch und abstrakt**. Es gibt keine realen UID- oder
GID-Werte, keine realen Benutzer- oder Gruppennamen, keine realen Hostpfade
und keine private Infrastruktur. Fuer den Secretfall wird ausschliesslich ein
**synthetischer Marker** verwendet — niemals ein echter Wert.

Zustaende werden **injiziert**, nicht gemessen. Dadurch laufen alle Tests auf
jeder Plattform ohne ``skipTest`` und ohne Abhaengigkeit von
Windows-Entwicklermodus oder Administratorrechten.
"""

from __future__ import annotations

import stat as stat_module
from dataclasses import dataclass, replace
from typing import Final

from core.core_brain.enforcement import (
    ContentClassification,
    HostObjectState,
    IdentityBinding,
    MountMode,
    MountState,
    ObjectKind,
    Observation,
    ObservationOrigin,
    PathClass,
    PermissionProfile,
    RuntimeIdentityState,
    RuntimeObjectState,
    ServiceRole,
)
from core.core_brain.enforcement.binding import (
    CollisionState,
    ValidationState,
    ValueOrigin,
)

__all__ = [
    "FakeStat",
    "SECRET_MARKER",
    "IDENTITY_A",
    "IDENTITY_B",
    "GROUP_A",
    "GROUP_B",
    "dir_stat",
    "file_stat",
    "symlink_stat",
    "fifo_stat",
    "socket_stat",
    "chardev_stat",
    "binding_for",
    "host_state",
    "mount_state",
    "runtime_object_state",
    "runtime_identity_state",
    "conforming_observation",
    "observed_everything",
    "replace",
]

#: Synthetischer Marker fuer den PP-3b-Secretfall. **Kein echter Wert.**
SECRET_MARKER: Final[str] = "<synthetic-secret-marker>"

#: Opake, abstrakte Identitaets- und Gruppenreferenzen. Keine OS-Namen.
IDENTITY_A: Final[str] = "identity-ref-a"
IDENTITY_B: Final[str] = "identity-ref-b"
GROUP_A: Final[str] = "group-ref-a"
GROUP_B: Final[str] = "group-ref-b"


@dataclass(frozen=True, slots=True)
class FakeStat:
    """Injizierbarer ``stat``-Zustand.

    Erfuellt das ``StatLike``-Protokoll des Enforcement-Pakets, ohne eine
    reale Datei mit den entsprechenden Eigenschaften zu benoetigen.
    """

    st_mode: int
    st_nlink: int = 1


def dir_stat(mode: int = 0o750, nlink: int = 2) -> FakeStat:
    """Baut den Zustand eines Verzeichnisses."""
    return FakeStat(st_mode=stat_module.S_IFDIR | mode, st_nlink=nlink)


def file_stat(mode: int = 0o640, nlink: int = 1) -> FakeStat:
    """Baut den Zustand einer regulaeren Datei."""
    return FakeStat(st_mode=stat_module.S_IFREG | mode, st_nlink=nlink)


def symlink_stat(mode: int = 0o777) -> FakeStat:
    """Baut den Zustand eines Symlinks."""
    return FakeStat(st_mode=stat_module.S_IFLNK | mode, st_nlink=1)


def fifo_stat(mode: int = 0o600) -> FakeStat:
    """Baut den Zustand einer FIFO."""
    return FakeStat(st_mode=stat_module.S_IFIFO | mode, st_nlink=1)


def socket_stat(mode: int = 0o600) -> FakeStat:
    """Baut den Zustand eines Sockets."""
    return FakeStat(st_mode=stat_module.S_IFSOCK | mode, st_nlink=1)


def chardev_stat(mode: int = 0o600) -> FakeStat:
    """Baut den Zustand eines Character Device."""
    return FakeStat(st_mode=stat_module.S_IFCHR | mode, st_nlink=1)


def binding_for(
    path_class: PathClass,
    *,
    role: ServiceRole = ServiceRole.CONTROL_PLANE,
    profile: PermissionProfile = PermissionProfile.PP_2,
    identity: str = IDENTITY_A,
    primary_group: str = GROUP_A,
    read_groups: tuple[str, ...] = (),
    value_origin: ValueOrigin = ValueOrigin.OPERATOR_WORKSPACE,
    validation_state: ValidationState = ValidationState.VALIDATED,
    collision_state: CollisionState = CollisionState.NONE,
) -> IdentityBinding:
    """Baut eine vollstaendige, formal gueltige Bindung."""
    return IdentityBinding(
        role_id=role,
        host_identity_ref=identity,
        container_identity_ref=identity,
        expected_effective_identity=identity,
        primary_group_ref=primary_group,
        path_class_refs=(path_class,),
        profile_ref=profile,
        value_origin=value_origin,
        validation_state=validation_state,
        collision_state=collision_state,
        read_group_refs=read_groups,
    )


def host_state(
    *,
    owner: str,
    group: str,
    mode: int,
    kind: ObjectKind = ObjectKind.REGULAR_FILE,
    is_symlink: bool = False,
    is_hardlinked: bool = False,
    origin: ObservationOrigin = ObservationOrigin.SYNTHETIC,
) -> HostObjectState:
    """Baut einen D-I-Zustand."""
    return HostObjectState(
        owner_ref=owner,
        group_ref=group,
        mode=mode,
        object_kind=kind,
        is_symlink=is_symlink,
        is_hardlinked=is_hardlinked,
        origin=origin,
    )


def mount_state(
    *,
    mode: MountMode,
    target: str = "<area-anchor>",
    unexpected: tuple[str, ...] = (),
    crosses_boundary: bool = False,
    origin: ObservationOrigin = ObservationOrigin.SYNTHETIC,
) -> MountState:
    """Baut einen D-II-Zustand."""
    return MountState(
        mode=mode,
        expected_target=target,
        unexpected_mounts=unexpected,
        crosses_boundary=crosses_boundary,
        origin=origin,
    )


def runtime_object_state(
    *,
    mode: int,
    kind: ObjectKind = ObjectKind.REGULAR_FILE,
    relative_path: str = "artifact.json",
    readable: bool = True,
    writable: bool = False,
    origin: ObservationOrigin = ObservationOrigin.SYNTHETIC,
) -> RuntimeObjectState:
    """Baut einen D-III-Zustand."""
    return RuntimeObjectState(
        visible_mode=mode,
        object_kind=kind,
        relative_path=relative_path,
        readable=readable,
        writable=writable,
        origin=origin,
    )


def runtime_identity_state(
    *,
    identity: str = IDENTITY_A,
    groups: tuple[str, ...] = (GROUP_A,),
    role: ServiceRole = ServiceRole.CONTROL_PLANE,
    origin: ObservationOrigin = ObservationOrigin.SYNTHETIC,
) -> RuntimeIdentityState:
    """Baut einen D-IV-Zustand."""
    return RuntimeIdentityState(
        effective_identity_ref=identity,
        supplementary_group_refs=groups,
        role=role,
        origin=origin,
    )


def conforming_observation(
    *,
    origin: ObservationOrigin = ObservationOrigin.SYNTHETIC,
) -> Observation:
    """Baut eine in allen vier Dimensionen vertragskonforme PC-03-Beobachtung.

    PC-03 traegt PP-2 (`0640`/`0750`), gehoert ``control-plane`` und wird von
    ``data-worker`` gelesen.
    """
    return Observation(
        path_class=PathClass.PC_03,
        relative_path="records/synthetic.json",
        host=host_state(
            owner=ServiceRole.CONTROL_PLANE.value,
            group=ServiceRole.DATA_WORKER.value,
            mode=0o640,
            origin=origin,
        ),
        mount=mount_state(mode=MountMode.READ_WRITE, origin=origin),
        runtime_object=runtime_object_state(
            mode=0o640, writable=True, origin=origin
        ),
        runtime_identity=runtime_identity_state(origin=origin),
    )


def observed_everything() -> tuple[Observation, IdentityBinding]:
    """Baut eine vollstaendig ``OBSERVED`` markierte, konforme Beobachtung.

    Nur mit dieser Herkunft kann ``operationally_verified`` ueberhaupt ``True``
    werden. In B2A ist auch dieser Zustand injiziert und damit **keine reale
    Deploymentevidenz**.
    """
    observation = conforming_observation(origin=ObservationOrigin.OBSERVED)
    binding = binding_for(PathClass.PC_03)
    return observation, binding
