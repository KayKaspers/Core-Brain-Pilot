"""Read-only Pfad-, Link- und Objektartprüfungen (Contract §11, LP-1…LP-10).

Sämtliche Funktionen sind **lesend**. Dieses Modul erzeugt, verändert und
löscht **keine** Datei, kein Verzeichnis und keinen Link; es ruft weder
``chmod`` noch ``chown``.

Die Muster folgen dem bereits implementierten Bestand aus
``quarantine/store.py`` und ``registry/storage.py``: Auflösung über
``Path.resolve()``, Bereichsprüfung über ``Path.is_relative_to()`` — **kein
Vertrauen auf Zeichenkettenpräfixe** (LP-1, LP-8).

**TOCTOU-Grenze (LP-9):** Jedes Ergebnis dieses Moduls ist eine Aussage über
**einen Zeitpunkt**. Es gilt nicht über einen nachfolgenden Schreibvorgang
hinaus, und die Rechteprüfung ist **niemals** die einzige Absicherung —
Mountmodus (KB-03), Prozessidentität (KB-01/KB-02) und die atomare
Schreibsemantik (ADR-0010/ADR-0011) tragen unabhängig.

Der Import dieses Moduls hat keine Nebenwirkungen.
"""

from __future__ import annotations

import stat as stat_module
from dataclasses import dataclass
from pathlib import Path
from typing import Final, Protocol

from ..errors import ReasonCode
from .aggregate import Finding, FindingStatus
from .contract import Dimension, ObjectKind, PathClass

__all__ = [
    "StatLike",
    "PathResolution",
    "resolve_within_root",
    "classify_object_kind",
    "classify_link",
    "detect_hardlink",
    "check_path",
]


class StatLike(Protocol):
    """Minimale ``stat``-Schnittstelle.

    Erlaubt die Injektion von Zuständen in Tests und auf Plattformen, die
    POSIX-Metadaten nicht abbilden — ohne Plattformskip und ohne echte
    Dateisystemänderung.
    """

    st_mode: int
    st_nlink: int


#: Objektarten, die in geschützten Bereichen unzulässig sind (LP-6).
_FORBIDDEN_KINDS: Final[frozenset[ObjectKind]] = frozenset(
    {ObjectKind.SYMLINK, ObjectKind.OTHER}
)


@dataclass(frozen=True, slots=True)
class PathResolution:
    """Ergebnis einer Bereichsauflösung.

    ``resolved`` ist der aufgelöste Pfad. ``inside`` gibt an, ob er innerhalb
    der Bereichswurzel liegt. ``relative`` ist die repositorierelative bzw.
    bereichsrelative Darstellung — **niemals** ein absoluter Hostpfad.
    """

    resolved: Path
    root: Path
    inside: bool
    relative: str


def resolve_within_root(path: Path, root: Path) -> PathResolution:
    """Löst ``path`` auf und prüft ihn gegen die feste Bereichswurzel.

    Der Vergleich erfolgt ausschließlich auf **aufgelösten** Pfaden
    (LP-1, LP-2); Zeichenkettenpräfixe werden nicht ausgewertet (LP-8).
    Die Funktion liest ausschließlich — sie legt nichts an.

    Args:
        path: Der zu prüfende Pfad.
        root: Die Bereichswurzel.

    Returns:
        Die Auflösung samt Bereichszugehörigkeit.
    """
    resolved_root = root.resolve()
    resolved = path.resolve()
    inside = resolved == resolved_root or resolved.is_relative_to(resolved_root)
    if inside:
        relative = (
            "." if resolved == resolved_root
            else resolved.relative_to(resolved_root).as_posix()
        )
    else:
        relative = "<outside-root>"
    return PathResolution(
        resolved=resolved, root=resolved_root, inside=inside, relative=relative
    )


def classify_object_kind(st: StatLike | None) -> ObjectKind:
    """Bestimmt die Objektart aus einem ``lstat``-Ergebnis.

    Args:
        st: Das ``lstat``-Ergebnis oder ``None`` für einen fehlenden Pfad.

    Returns:
        Die Objektart. Device Files, FIFOs und Sockets werden zu
        :attr:`ObjectKind.OTHER` und sind damit unzulässig (LP-6).
    """
    if st is None:
        return ObjectKind.ABSENT
    mode = st.st_mode
    if stat_module.S_ISLNK(mode):
        return ObjectKind.SYMLINK
    if stat_module.S_ISDIR(mode):
        return ObjectKind.DIRECTORY
    if stat_module.S_ISREG(mode):
        return ObjectKind.REGULAR_FILE
    return ObjectKind.OTHER


def classify_link(st: StatLike | None) -> bool:
    """Gibt zurück, ob das Objekt ein Symlink ist.

    Interne Symlinks werden **nicht aufgelöst, sondern abgelehnt** (LP-4) —
    diese Funktion stellt lediglich fest, sie folgt keinem Ziel.
    """
    return classify_object_kind(st) is ObjectKind.SYMLINK


def detect_hardlink(st: StatLike | None) -> bool:
    """Gibt zurück, ob eine reguläre Datei mehrfach verlinkt ist (LP-5).

    Nur reguläre Dateien werden bewertet: Verzeichnisse tragen auf POSIX
    systembedingt mehrere Links. Ein ``True`` ist ein **Befund**, keine
    Gewissheit — auf manchen Dateisystemen ist ``st_nlink`` nicht aussagekräftig.
    """
    if st is None:
        return False
    if not stat_module.S_ISREG(st.st_mode):
        return False
    return st.st_nlink > 1


def check_path(
    *,
    path: Path,
    root: Path,
    path_class: PathClass,
    st: StatLike | None,
    allowed_kinds: tuple[ObjectKind, ...],
) -> tuple[Finding, ...]:
    """Prüft einen Pfad read-only gegen die Link- und Pfadregeln.

    Geprüft werden Bereichsgrenze (LP-1, LP-2, LP-8), Symlinkstatus (LP-3,
    LP-4), Hardlinks (LP-5), Objektart (LP-6) und die vertraglich zulässigen
    Objektarten der Pfadklasse.

    Args:
        path: Der zu prüfende Pfad.
        root: Die Bereichswurzel.
        path_class: Die zugeordnete Pfadklasse.
        st: Das ``lstat``-Ergebnis oder ``None``. Injizierbar.
        allowed_kinds: Die vertraglich zulässigen Objektarten.

    Returns:
        Die Befunde in deterministischer Reihenfolge; leer bedeutet konform.
    """
    resolution = resolve_within_root(path, root)
    rel = resolution.relative
    findings: list[Finding] = []

    def add(
        reason: ReasonCode | None, detail: str, status: FindingStatus
    ) -> None:
        findings.append(
            Finding(
                path_class=path_class,
                relative_path=rel,
                dimension=Dimension.D_I,
                status=status,
                reason=reason,
                detail=detail,
                origin=None,
            )
        )

    if not resolution.inside:
        add(
            ReasonCode.KB04_PATH_OUTSIDE_ROOT,
            "resolved path leaves the area root",
            FindingStatus.VIOLATION,
        )
        return tuple(sorted(findings))

    kind = classify_object_kind(st)

    if st is None:
        add(
            ReasonCode.KB04_STATE_INDETERMINATE,
            "object state not observable",
            FindingStatus.INDETERMINATE,
        )
        return tuple(sorted(findings))

    if kind is ObjectKind.SYMLINK:
        # LP-3 und LP-4: abgelehnt, nicht aufgelöst — unabhängig vom Ziel.
        add(
            ReasonCode.KB04_LINK_SYMLINK_ESCAPE,
            "symlink is rejected, not resolved",
            FindingStatus.VIOLATION,
        )
    elif kind in _FORBIDDEN_KINDS or kind not in allowed_kinds:
        add(
            ReasonCode.KB04_OBJECT_KIND_INVALID,
            f"object kind not permitted: {kind.value}",
            FindingStatus.VIOLATION,
        )

    if detect_hardlink(st):
        add(
            ReasonCode.KB04_LINK_HARDLINK,
            "hardlink in protected area",
            FindingStatus.VIOLATION,
        )

    if not findings:
        add(None, "path within root, permitted object kind", FindingStatus.CONFORM)

    return tuple(sorted(findings))
