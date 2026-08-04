"""Deterministische Fixtures der KB-04-Initialisierungsplanung (B2B-P).

Kein ``test_``-Praefix: das Modul wird von ``unittest discover`` nicht als
Testmodul entdeckt.

Der Fake-Adapter bildet ein **rein virtuelles** Dateisystem ab. Er legt nichts
an, veraendert nichts und beruehrt keinen realen Pfad. Dadurch laufen alle
Faelle — Symlink, Mountpoint, Hardlink, FIFO, Socket, Device, PermissionError,
Wettlauf, fehlende POSIX-Semantik — auf **jeder** Plattform ohne ``skipTest``,
ohne Entwicklermodus und ohne Administratorrechte.

Alle Werte sind synthetisch und abstrakt: keine realen UID- oder GID-Werte,
keine realen Benutzer- oder Gruppennamen, keine privaten Pfade, keine Secrets.
"""

from __future__ import annotations

import stat as stat_module
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Final, Iterator

from core.core_brain.enforcement.binding import (
    CollisionState,
    IdentityBinding,
    ValidationState,
    ValueOrigin,
)
from core.core_brain.enforcement.contract import (
    Actor,
    PathClass,
    PermissionProfile,
    ServiceRole,
)
from core.core_brain.enforcement.initialization import (
    InitializationRequest,
    TargetPathBinding,
)

__all__ = [
    "BOUNDARY",
    "TARGET",
    "TARGET_REF",
    "FakeNode",
    "FakeFilesystemAdapter",
    "directory",
    "regular_file",
    "symlink",
    "fifo",
    "socket_node",
    "device",
    "binding",
    "request_for",
    "adapter_absent",
    "adapter_empty",
    "adapter_initialized",
    "DEFAULT_BINDINGS",
    "replace",
]

#: Virtuelle, plattformneutrale Ankerpfade. Keine realen Hostpfade.
BOUNDARY: Final[Path] = Path("/vroot")
TARGET: Final[Path] = Path("/vroot/target")
TARGET_REF: Final[str] = "<synthetic-target>"

#: Die in den Tests verwendete Standardbindung dreier Pfadklassen.
DEFAULT_BINDINGS: Final[tuple[TargetPathBinding, ...]] = (
    TargetPathBinding(PathClass.PC_02, "quarantine"),
    TargetPathBinding(PathClass.PC_03, "source-registry"),
    TargetPathBinding(PathClass.PC_06, "derived"),
)


@dataclass(frozen=True, slots=True)
class FakeNode:
    """Ein Knoten des virtuellen Dateisystems."""

    kind: str = "dir"
    mode: int = 0o750
    nlink: int = 1
    is_mount: bool = False
    entries: tuple[str, ...] = ()

    @property
    def st_mode(self) -> int:
        """POSIX-Modus samt Typbits."""
        type_bits = {
            "dir": stat_module.S_IFDIR,
            "file": stat_module.S_IFREG,
            "symlink": stat_module.S_IFLNK,
            "fifo": stat_module.S_IFIFO,
            "socket": stat_module.S_IFSOCK,
            "device": stat_module.S_IFCHR,
        }[self.kind]
        return type_bits | self.mode


def directory(*entries: str, mode: int = 0o750, is_mount: bool = False) -> FakeNode:
    """Baut ein Verzeichnis mit den angegebenen Eintraegen."""
    return FakeNode(
        kind="dir", mode=mode, entries=tuple(entries), is_mount=is_mount
    )


def regular_file(mode: int = 0o640, nlink: int = 1) -> FakeNode:
    """Baut eine regulaere Datei."""
    return FakeNode(kind="file", mode=mode, nlink=nlink)


def symlink() -> FakeNode:
    """Baut einen Symlink."""
    return FakeNode(kind="symlink", mode=0o777)


def fifo() -> FakeNode:
    """Baut eine FIFO."""
    return FakeNode(kind="fifo", mode=0o600)


def socket_node() -> FakeNode:
    """Baut einen Socket."""
    return FakeNode(kind="socket", mode=0o600)


def device() -> FakeNode:
    """Baut ein Character Device."""
    return FakeNode(kind="device", mode=0o600)


class _FakeStat:
    """Minimales ``stat``-Ergebnis des virtuellen Dateisystems."""

    __slots__ = ("st_mode", "st_nlink")

    def __init__(self, st_mode: int, st_nlink: int) -> None:
        self.st_mode = st_mode
        self.st_nlink = st_nlink


@dataclass
class FakeFilesystemAdapter:
    """Injizierbarer, **rein lesender** Fake-Adapter.

    ``nodes`` bildet POSIX-Pfadzeichenketten auf Knoten ab. ``errors`` erhebt
    fuer die angegebenen Pfade den hinterlegten ``OSError``. ``race`` liefert
    fuer einen Pfad je Beobachtung den naechsten Zustand und simuliert damit
    eine Zustandsaenderung zwischen zwei Pruefungen.

    Der Adapter **legt nichts an und veraendert nichts** — er beantwortet
    ausschliesslich Fragen.
    """

    nodes: dict[str, FakeNode] = field(default_factory=dict)
    posix_semantics: bool = True
    errors: dict[str, OSError] = field(default_factory=dict)
    race: dict[str, list[FakeNode | None]] = field(default_factory=dict)
    observations: int = 0

    # ---------------------------------------------------------------- intern
    def _key(self, path: Path) -> str:
        return path.as_posix()

    def _node(self, path: Path) -> FakeNode:
        key = self._key(path)
        self.observations += 1
        if key in self.errors:
            raise self.errors[key]
        if key in self.race and self.race[key]:
            nxt = self.race[key].pop(0)
            if nxt is None:
                raise FileNotFoundError(key)
            self.nodes[key] = nxt
            return nxt
        if key not in self.nodes:
            raise FileNotFoundError(key)
        return self.nodes[key]

    # ------------------------------------------------------------ read-only
    def exists(self, path: Path) -> bool:
        """Ob der Pfad existiert; folgt keinem Symlink."""
        try:
            self._node(path)
        except FileNotFoundError:
            return False
        return True

    def lstat(self, path: Path) -> _FakeStat:
        """``lstat`` des Pfades — folgt keinem Symlink."""
        node = self._node(path)
        return _FakeStat(node.st_mode, node.nlink)

    def stat(self, path: Path) -> _FakeStat:
        """``stat`` des Pfades."""
        return self.lstat(path)

    def iterdir(self, path: Path) -> Iterator[Path]:
        """Alle Eintraege, **einschliesslich versteckter**."""
        node = self._node(path)
        return iter([path / name for name in node.entries])

    def resolve(self, path: Path) -> Path:
        """Gibt den Pfad unveraendert zurueck — virtuelle Aufloesung."""
        key = self._key(path)
        if key in self.errors:
            raise self.errors[key]
        return path

    def is_mount(self, path: Path) -> bool:
        """Ob der Pfad ein Mountpoint ist."""
        try:
            return self._node(path).is_mount
        except FileNotFoundError:
            return False


def binding(
    *,
    role: ServiceRole = ServiceRole.CONTROL_PLANE,
    profile: PermissionProfile = PermissionProfile.PP_2,
    path_classes: tuple[PathClass, ...] = (PathClass.PC_03,),
    value_origin: ValueOrigin = ValueOrigin.OPERATOR_WORKSPACE,
    validation_state: ValidationState = ValidationState.VALIDATED,
    collision_state: CollisionState = CollisionState.NONE,
) -> IdentityBinding:
    """Baut eine formal gueltige Identitaetsbindung mit opaken Referenzen."""
    return IdentityBinding(
        role_id=role,
        host_identity_ref="identity-ref-a",
        container_identity_ref="identity-ref-a",
        expected_effective_identity="identity-ref-a",
        primary_group_ref="group-ref-a",
        path_class_refs=path_classes,
        profile_ref=profile,
        value_origin=value_origin,
        validation_state=validation_state,
        collision_state=collision_state,
    )


def request_for(
    *,
    authority: Actor = Actor.DEPLOYMENT_SETUP,
    bindings: tuple[TargetPathBinding, ...] = DEFAULT_BINDINGS,
    identity: IdentityBinding | None = None,
    boundary_root: Path = BOUNDARY,
    target_root: Path = TARGET,
    target_ref: str = TARGET_REF,
) -> InitializationRequest:
    """Baut eine vollstaendige Planungsanfrage."""
    return InitializationRequest(
        authority=authority,
        boundary_root=boundary_root,
        target_root=target_root,
        target_ref=target_ref,
        path_bindings=bindings,
        identity_binding=binding() if identity is None else identity,
    )


def adapter_absent(**kwargs: object) -> FakeFilesystemAdapter:
    """N-1: Boundary vorhanden, Ziel fehlt."""
    return FakeFilesystemAdapter(
        nodes={"/vroot": directory("other")}, **kwargs  # type: ignore[arg-type]
    )


def adapter_empty(**kwargs: object) -> FakeFilesystemAdapter:
    """N-2: Ziel vorhanden und vollstaendig leer."""
    return FakeFilesystemAdapter(
        nodes={"/vroot": directory("target"), "/vroot/target": directory()},
        **kwargs,  # type: ignore[arg-type]
    )


def adapter_initialized(**kwargs: object) -> FakeFilesystemAdapter:
    """Bereits vollstaendig vorbereitete Struktur ohne Fremdinhalt."""
    names = tuple(b.relative_path for b in DEFAULT_BINDINGS)
    nodes: dict[str, FakeNode] = {
        "/vroot": directory("target"),
        "/vroot/target": directory(*names),
    }
    for name in names:
        nodes[f"/vroot/target/{name}"] = directory()
    return FakeFilesystemAdapter(nodes=nodes, **kwargs)  # type: ignore[arg-type]
