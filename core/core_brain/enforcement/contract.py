"""Maschinenlesbares Teilmodell des KB-04-Stage-1-Enforcement-Contract.

Normative Authority bleibt das Markdown-Dokument
``docs/security/KB_04_STAGE_1_ENFORCEMENT_CONTRACT.md`` (accepted contract,
D-060/A0, ADR-0014/A1). Dieses Modul bildet **ausschließlich** die
maschinell prüfbaren Größen ab — Pfadklassen, Rechteprofile, Rollen und
Dimensionen — und ist damit **abgeleitet, nicht normativ**.

Das Modul ist rein statisch: keine Datei-, Netz-, ENV-, Uhr- oder
Zufallszugriffe, keine Mutation, keine I/O. Insbesondere wird das
Markdown-Dokument beim Import **nicht** gelesen; der hinterlegte Dokumenthash
dient allein dem Driftschutz durch Tests.

Es enthält **keine** realen Hostpfade, UID- oder GID-Werte, Benutzer- oder
Gruppennamen. Die Containeranker stammen unverändert aus ``container_paths``
und ``tmpfs_targets`` des bereits committeten Profil-A-Bundles.

Der Import dieses Moduls hat keine Nebenwirkungen.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from enum import StrEnum
from typing import Final, Mapping

from ..errors import ReasonCode
from .aggregate import Finding, FindingStatus, canonical_json_bytes

__all__ = [
    "CONTRACT_REVISION",
    "CONTRACT_DOCUMENT_PATH",
    "CONTRACT_DOCUMENT_SHA256",
    "PathClass",
    "PermissionProfile",
    "ObjectKind",
    "Actor",
    "Dimension",
    "MountMode",
    "ServiceRole",
    "ProfileSpec",
    "PathClassSpec",
    "PROFILES",
    "PATH_CLASSES",
    "WORLD_WRITE_BITS",
    "SPECIAL_BITS",
    "path_class_spec",
    "profile_spec",
    "validate_contract",
    "contract_model_sha256",
    "normalize_document_bytes",
]

#: Revision des hier abgebildeten Teilmodells.
CONTRACT_REVISION: Final[str] = "1.0"

#: Relativer Repositorypfad des normativen Dokuments. Kein Hostpfad.
CONTRACT_DOCUMENT_PATH: Final[str] = (
    "docs/security/KB_04_STAGE_1_ENFORCEMENT_CONTRACT.md"
)

#: SHA-256 des in Commit ``24de07e`` enthaltenen Dokuments, berechnet über die
#: **zeilenendennormalisierte** Fassung (LF). Die Normalisierung ist zwingend:
#: das Repository arbeitet mit ``core.autocrlf``, sodass die Arbeitskopie unter
#: Windows CRLF trägt, der Commit-Blob aber LF. Ohne Normalisierung wäre der
#: Driftschutz plattformabhängig und damit wertlos.
CONTRACT_DOCUMENT_SHA256: Final[str] = (
    "c3a1b85fad359a19fe3b266aac7a09c7b95f90e2f5ca1f270507343d4df5492c"
)


class PathClass(StrEnum):
    """Die elf Pfadklassen des Contract (§4)."""

    PC_01 = "PC-01"
    PC_02 = "PC-02"
    PC_03 = "PC-03"
    PC_04 = "PC-04"
    PC_05 = "PC-05"
    PC_06 = "PC-06"
    PC_07 = "PC-07"
    PC_08 = "PC-08"
    PC_09 = "PC-09"
    PC_10 = "PC-10"
    PC_11 = "PC-11"


class PermissionProfile(StrEnum):
    """Die Rechteprofile des Contract (§6), PP-3 mit genau zwei Varianten."""

    PP_1 = "PP-1"
    PP_2 = "PP-2"
    PP_3A = "PP-3a"
    PP_3B = "PP-3b"
    PP_4 = "PP-4"


class ObjectKind(StrEnum):
    """Zulässige und unzulässige Objektarten (§11, LP-6)."""

    DIRECTORY = "DIRECTORY"
    REGULAR_FILE = "REGULAR_FILE"
    SYMLINK = "SYMLINK"
    OTHER = "OTHER"
    ABSENT = "ABSENT"


class Actor(StrEnum):
    """Die zehn Akteure der Rollenmatrix (§5)."""

    DEPLOYMENT_SETUP = "deployment/setup"
    OPERATOR = "operator"
    INGEST = "ingest"
    RETRIEVAL = "retrieval"
    REGISTRY = "registry"
    MAPPING = "mapping"
    RELEASE = "release"
    VALIDATION = "validation"
    GATE = "gate"
    EVIDENCE = "evidence"


class Dimension(StrEnum):
    """Die vier getrennten Prüfdimensionen (§7.1)."""

    D_I = "D-I"
    D_II = "D-II"
    D_III = "D-III"
    D_IV = "D-IV"


class MountMode(StrEnum):
    """Mountmodi der Bereiche. ``UNKNOWN`` ist fail-closed (MT-7)."""

    READ_ONLY = "ro"
    READ_WRITE = "rw"
    TMPFS = "tmpfs"
    NOT_MOUNTED = "not-mounted"
    UNKNOWN = "unknown"


class ServiceRole(StrEnum):
    """Abstrakte Besitz- und Zugriffsrollen. Keine Betriebssystemnamen."""

    CONTROL_PLANE = "control-plane"
    DATA_WORKER = "data-worker"
    SERVICE = "service"
    HUMAN_MAINTAINER = "human-maintainer"
    MAINTAINER_OWNED = "maintainer-owned"
    DEPLOYMENT_OWNED = "deployment-owned"
    EXTERNAL = "external"


#: Verbotene World-Write-Bits (I-2, Regel G-1). Ausnahmslos.
WORLD_WRITE_BITS: Final[int] = 0o002

#: setuid, setgid und sticky. Regel G-3, G-4, G-6.
SPECIAL_BITS: Final[int] = 0o7000


@dataclass(frozen=True, slots=True)
class ProfileSpec:
    """Vertragliche Festlegung eines Rechteprofils (§6)."""

    profile: PermissionProfile
    file_mode: int | None
    dir_mode: int | None
    umask: int | None
    world_read_allowed: bool
    setgid_dir_allowed: bool
    present: bool
    exclusive_path_class: PathClass | None = None


@dataclass(frozen=True, slots=True)
class PathClassSpec:
    """Vertragliche Festlegung einer Pfadklasse (§4)."""

    path_class: PathClass
    area: str
    container_anchors: tuple[str, ...]
    object_kinds: tuple[ObjectKind, ...]
    owner_role: ServiceRole | None
    reader_roles: tuple[ServiceRole, ...]
    writer_roles: tuple[ServiceRole, ...]
    profile: PermissionProfile | None
    mount_mode: MountMode
    secret_free_required: bool
    classified: bool


_PROFILES: Final[dict[PermissionProfile, ProfileSpec]] = {
    PermissionProfile.PP_1: ProfileSpec(
        profile=PermissionProfile.PP_1,
        file_mode=0o600,
        dir_mode=0o700,
        umask=0o077,
        world_read_allowed=False,
        setgid_dir_allowed=False,
        present=True,
    ),
    PermissionProfile.PP_2: ProfileSpec(
        profile=PermissionProfile.PP_2,
        file_mode=0o640,
        dir_mode=0o750,
        umask=0o027,
        world_read_allowed=False,
        setgid_dir_allowed=True,
        present=True,
    ),
    PermissionProfile.PP_3A: ProfileSpec(
        profile=PermissionProfile.PP_3A,
        file_mode=0o640,
        dir_mode=0o750,
        umask=0o027,
        world_read_allowed=False,
        setgid_dir_allowed=False,
        present=True,
    ),
    # Eng begrenztes Kompatibilitätsprofil (Regeln 3b-1 bis 3b-16).
    # Ausschließlich PC-07; kein allgemeines read-only Profil; kein Default.
    PermissionProfile.PP_3B: ProfileSpec(
        profile=PermissionProfile.PP_3B,
        file_mode=0o444,
        dir_mode=0o555,
        umask=None,
        world_read_allowed=True,
        setgid_dir_allowed=False,
        present=True,
        exclusive_path_class=PathClass.PC_07,
    ),
    PermissionProfile.PP_4: ProfileSpec(
        profile=PermissionProfile.PP_4,
        file_mode=None,
        dir_mode=None,
        umask=None,
        world_read_allowed=False,
        setgid_dir_allowed=False,
        present=False,
    ),
}

PROFILES: Final[Mapping[PermissionProfile, ProfileSpec]] = _PROFILES

_FILE_AND_DIR: Final[tuple[ObjectKind, ...]] = (
    ObjectKind.DIRECTORY,
    ObjectKind.REGULAR_FILE,
)

_PATH_CLASSES: Final[dict[PathClass, PathClassSpec]] = {
    PathClass.PC_01: PathClassSpec(
        path_class=PathClass.PC_01,
        area="canonical-store",
        container_anchors=("/var/lib/cbp/canonical",),
        object_kinds=_FILE_AND_DIR,
        owner_role=ServiceRole.MAINTAINER_OWNED,
        reader_roles=(ServiceRole.CONTROL_PLANE, ServiceRole.DATA_WORKER),
        writer_roles=(),
        profile=PermissionProfile.PP_3A,
        mount_mode=MountMode.READ_ONLY,
        secret_free_required=False,
        classified=True,
    ),
    PathClass.PC_02: PathClassSpec(
        path_class=PathClass.PC_02,
        area="quarantine-store",
        container_anchors=("/var/lib/cbp/quarantine",),
        object_kinds=_FILE_AND_DIR,
        owner_role=ServiceRole.DATA_WORKER,
        reader_roles=(),
        writer_roles=(ServiceRole.DATA_WORKER,),
        profile=PermissionProfile.PP_1,
        mount_mode=MountMode.READ_WRITE,
        secret_free_required=False,
        classified=True,
    ),
    PathClass.PC_03: PathClassSpec(
        path_class=PathClass.PC_03,
        area="source-registry",
        container_anchors=("/var/lib/cbp/source-registry",),
        object_kinds=_FILE_AND_DIR,
        owner_role=ServiceRole.CONTROL_PLANE,
        reader_roles=(ServiceRole.DATA_WORKER,),
        writer_roles=(ServiceRole.CONTROL_PLANE,),
        profile=PermissionProfile.PP_2,
        mount_mode=MountMode.READ_WRITE,
        secret_free_required=False,
        classified=True,
    ),
    PathClass.PC_04: PathClassSpec(
        path_class=PathClass.PC_04,
        area="mapping-registry",
        container_anchors=("/var/lib/cbp/mapping-registry",),
        object_kinds=_FILE_AND_DIR,
        owner_role=ServiceRole.CONTROL_PLANE,
        reader_roles=(ServiceRole.DATA_WORKER,),
        writer_roles=(ServiceRole.CONTROL_PLANE,),
        profile=PermissionProfile.PP_2,
        mount_mode=MountMode.READ_WRITE,
        secret_free_required=False,
        classified=True,
    ),
    PathClass.PC_05: PathClassSpec(
        path_class=PathClass.PC_05,
        area="released-artifacts",
        container_anchors=("/var/lib/cbp/released",),
        object_kinds=_FILE_AND_DIR,
        owner_role=ServiceRole.CONTROL_PLANE,
        reader_roles=(),
        writer_roles=(ServiceRole.CONTROL_PLANE,),
        profile=PermissionProfile.PP_1,
        mount_mode=MountMode.READ_WRITE,
        secret_free_required=False,
        classified=True,
    ),
    PathClass.PC_06: PathClassSpec(
        path_class=PathClass.PC_06,
        area="derived-indices",
        container_anchors=("/var/lib/cbp/derived",),
        object_kinds=_FILE_AND_DIR,
        owner_role=ServiceRole.DATA_WORKER,
        reader_roles=(),
        writer_roles=(ServiceRole.DATA_WORKER,),
        profile=PermissionProfile.PP_1,
        mount_mode=MountMode.READ_WRITE,
        secret_free_required=False,
        classified=True,
    ),
    PathClass.PC_07: PathClassSpec(
        path_class=PathClass.PC_07,
        area="configuration-artifacts",
        container_anchors=("/etc/cbp",),
        object_kinds=_FILE_AND_DIR,
        owner_role=ServiceRole.DEPLOYMENT_OWNED,
        reader_roles=(ServiceRole.CONTROL_PLANE, ServiceRole.DATA_WORKER),
        writer_roles=(),
        profile=PermissionProfile.PP_3B,
        mount_mode=MountMode.READ_ONLY,
        secret_free_required=True,
        classified=True,
    ),
    PathClass.PC_08: PathClassSpec(
        path_class=PathClass.PC_08,
        area="runtime-transient",
        container_anchors=("/run/cbp", "/tmp"),
        object_kinds=_FILE_AND_DIR,
        owner_role=ServiceRole.SERVICE,
        reader_roles=(),
        writer_roles=(ServiceRole.CONTROL_PLANE, ServiceRole.DATA_WORKER),
        profile=PermissionProfile.PP_1,
        mount_mode=MountMode.TMPFS,
        secret_free_required=False,
        classified=True,
    ),
    PathClass.PC_09: PathClassSpec(
        path_class=PathClass.PC_09,
        area="rt2-operational-evidence",
        container_anchors=(),
        object_kinds=(ObjectKind.ABSENT,),
        owner_role=ServiceRole.HUMAN_MAINTAINER,
        reader_roles=(),
        writer_roles=(),
        profile=PermissionProfile.PP_4,
        mount_mode=MountMode.NOT_MOUNTED,
        secret_free_required=False,
        classified=True,
    ),
    PathClass.PC_10: PathClassSpec(
        path_class=PathClass.PC_10,
        area="backup-storage",
        container_anchors=(),
        object_kinds=(ObjectKind.ABSENT,),
        owner_role=ServiceRole.EXTERNAL,
        reader_roles=(),
        writer_roles=(),
        profile=PermissionProfile.PP_4,
        mount_mode=MountMode.NOT_MOUNTED,
        secret_free_required=False,
        classified=True,
    ),
    # Sammelklasse für jeden nicht zugeordneten Pfad. Ohne Profil, ohne
    # Mountzusage, ohne Owner — sie ist ausschließlich fail-closed.
    PathClass.PC_11: PathClassSpec(
        path_class=PathClass.PC_11,
        area="unclassified",
        container_anchors=(),
        object_kinds=(),
        owner_role=None,
        reader_roles=(),
        writer_roles=(),
        profile=None,
        mount_mode=MountMode.UNKNOWN,
        secret_free_required=False,
        classified=False,
    ),
}

PATH_CLASSES: Final[Mapping[PathClass, PathClassSpec]] = _PATH_CLASSES


def path_class_spec(path_class: PathClass) -> PathClassSpec:
    """Gibt die Festlegung einer Pfadklasse zurück.

    Args:
        path_class: Die Pfadklasse.

    Returns:
        Die vertragliche Festlegung.

    Raises:
        FilesystemEnforcementError: Wenn die Klasse dem Modell fehlt. Das ist
            eine interne Inkonsistenz, keine Vertragsabweichung.
    """
    spec = _PATH_CLASSES.get(path_class)
    if spec is None:  # pragma: no cover - durch validate_contract abgedeckt
        from ..errors import FilesystemEnforcementError

        raise FilesystemEnforcementError(
            ReasonCode.KB04_CONTRACT_INVALID, "path class missing from model"
        )
    return spec


def profile_spec(profile: PermissionProfile) -> ProfileSpec:
    """Gibt die Festlegung eines Rechteprofils zurück.

    Args:
        profile: Das Rechteprofil.

    Returns:
        Die vertragliche Festlegung.

    Raises:
        FilesystemEnforcementError: Wenn das Profil dem Modell fehlt.
    """
    spec = _PROFILES.get(profile)
    if spec is None:  # pragma: no cover - durch validate_contract abgedeckt
        from ..errors import FilesystemEnforcementError

        raise FilesystemEnforcementError(
            ReasonCode.KB04_CONTRACT_INVALID, "profile missing from model"
        )
    return spec


def _model_mapping() -> dict[str, object]:
    """Baut die kanonische Darstellung des Teilmodells."""
    return {
        "revision": CONTRACT_REVISION,
        "document": CONTRACT_DOCUMENT_PATH,
        "actors": [a.value for a in Actor],
        "dimensions": [d.value for d in Dimension],
        "object_kinds": [o.value for o in ObjectKind],
        "profiles": {
            p.value: {
                "dir_mode": s.dir_mode,
                "exclusive_path_class": (
                    s.exclusive_path_class.value
                    if s.exclusive_path_class is not None
                    else None
                ),
                "file_mode": s.file_mode,
                "present": s.present,
                "setgid_dir_allowed": s.setgid_dir_allowed,
                "umask": s.umask,
                "world_read_allowed": s.world_read_allowed,
            }
            for p, s in sorted(_PROFILES.items(), key=lambda kv: kv[0].value)
        },
        "path_classes": {
            c.value: {
                "area": s.area,
                "classified": s.classified,
                "container_anchors": list(s.container_anchors),
                "mount_mode": s.mount_mode.value,
                "object_kinds": [k.value for k in s.object_kinds],
                "owner_role": (
                    s.owner_role.value if s.owner_role is not None else None
                ),
                "profile": s.profile.value if s.profile is not None else None,
                "reader_roles": [r.value for r in s.reader_roles],
                "secret_free_required": s.secret_free_required,
                "writer_roles": [r.value for r in s.writer_roles],
            }
            for c, s in sorted(_PATH_CLASSES.items(), key=lambda kv: kv[0].value)
        },
    }


def contract_model_sha256() -> str:
    """Gibt den deterministischen SHA-256 des Teilmodells zurück.

    Der Hash ist stabil über Prozessläufe und Plattformen: sortierte
    Schlüssel, stabile Tupelreihenfolge, UTF-8, kompakte Serialisierung, keine
    Zeitstempel, keine absoluten Pfade.

    Returns:
        64 Hexzeichen.
    """
    return hashlib.sha256(canonical_json_bytes(_model_mapping())).hexdigest()


def normalize_document_bytes(raw: bytes) -> bytes:
    """Normalisiert Zeilenenden auf LF.

    Notwendig, weil das Repository mit ``core.autocrlf`` arbeitet: die
    Arbeitskopie trägt unter Windows CRLF, der Commit-Blob LF. Ohne
    Normalisierung wäre :data:`CONTRACT_DOCUMENT_SHA256` plattformabhängig.

    Args:
        raw: Rohbytes des Dokuments.

    Returns:
        Die normalisierte Fassung.
    """
    return raw.replace(b"\r\n", b"\n")


def _finding(reason: ReasonCode, detail: str) -> Finding:
    """Baut einen Contract-Befund ohne Dimension und ohne Pfad."""
    return Finding(
        path_class=PathClass.PC_11,
        relative_path=CONTRACT_DOCUMENT_PATH,
        dimension="",
        status=FindingStatus.VIOLATION,
        reason=reason,
        detail=detail,
        origin=None,
    )


def validate_contract() -> tuple[Finding, ...]:
    """Prüft das Teilmodell auf Selbstkonsistenz.

    Read-only, deterministisch, ohne Mutation. Geprüft werden Vollständigkeit
    der Pfadklassen und Profile, die PC-zu-PP-Zuordnung, die Exklusivität von
    PP-3b (Regel 3b-1), das ausnahmslose Verbot von World-Write-Bits (I-2) und
    die Konsistenz von PP-4 mit ``not-mounted``.

    Returns:
        Die Befunde in deterministischer Reihenfolge. Ein leeres Tupel
        bedeutet: das Modell ist in sich schlüssig.
    """
    findings: list[Finding] = []

    for member in PathClass:
        if member not in _PATH_CLASSES:
            findings.append(
                _finding(
                    ReasonCode.KB04_CONTRACT_INVALID,
                    f"path class not modelled: {member.value}",
                )
            )
    for profile in PermissionProfile:
        if profile not in _PROFILES:
            findings.append(
                _finding(
                    ReasonCode.KB04_CONTRACT_INVALID,
                    f"profile not modelled: {profile.value}",
                )
            )

    for path_class, spec in _PATH_CLASSES.items():
        if spec.path_class is not path_class:
            findings.append(
                _finding(
                    ReasonCode.KB04_CONTRACT_INVALID,
                    f"path class key mismatch: {path_class.value}",
                )
            )
        if spec.classified and spec.profile is None:
            findings.append(
                _finding(
                    ReasonCode.KB04_CONTRACT_INVALID,
                    f"classified path class without profile: {path_class.value}",
                )
            )
        if not spec.classified and spec.profile is not None:
            findings.append(
                _finding(
                    ReasonCode.KB04_CONTRACT_INVALID,
                    f"unclassified path class with profile: {path_class.value}",
                )
            )
        if spec.profile is PermissionProfile.PP_4:
            if spec.mount_mode is not MountMode.NOT_MOUNTED:
                findings.append(
                    _finding(
                        ReasonCode.KB04_CONTRACT_INVALID,
                        f"PP-4 must be not-mounted: {path_class.value}",
                    )
                )
            if spec.container_anchors:
                findings.append(
                    _finding(
                        ReasonCode.KB04_CONTRACT_INVALID,
                        f"PP-4 must have no anchor: {path_class.value}",
                    )
                )

    # Regel 3b-1 und 3b-3: PP-3b gilt ausschließlich für seine exklusive
    # Pfadklasse und darf nirgends sonst auftreten.
    for profile, spec in _PROFILES.items():
        exclusive = spec.exclusive_path_class
        if exclusive is None:
            continue
        wrong = tuple(
            c.value
            for c, pc in _PATH_CLASSES.items()
            if pc.profile is profile and c is not exclusive
        )
        for name in sorted(wrong):
            findings.append(
                _finding(
                    ReasonCode.KB04_CONTRACT_INVALID,
                    f"{profile.value} outside {exclusive.value}: {name}",
                )
            )
        if _PATH_CLASSES[exclusive].profile is not profile:
            findings.append(
                _finding(
                    ReasonCode.KB04_CONTRACT_INVALID,
                    f"{exclusive.value} must carry {profile.value}",
                )
            )

    # I-2 und Regel G-1: kein Profil darf ein World-Write-Bit tragen.
    for profile, spec in _PROFILES.items():
        for mode in (spec.file_mode, spec.dir_mode):
            if mode is not None and mode & WORLD_WRITE_BITS:
                findings.append(
                    _finding(
                        ReasonCode.KB04_MODE_WORLD_BITS,
                        f"world-writable profile: {profile.value}",
                    )
                )
        if spec.file_mode is not None and spec.file_mode & SPECIAL_BITS:
            findings.append(
                _finding(
                    ReasonCode.KB04_MODE_SPECIAL_BITS,
                    f"special bits on file mode: {profile.value}",
                )
            )

    return tuple(sorted(findings))
