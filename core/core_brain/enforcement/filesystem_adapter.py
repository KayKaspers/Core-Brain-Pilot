"""Read-only Dateisystemzugriff für die KB-04-Initialisierungsplanung.

Der Adapter existiert allein, um die Zielzustandsbeobachtung **injizierbar**
und damit plattformunabhängig testbar zu machen. Er ist **keine**
Deploymentabstraktion und **keine** öffentliche Schnittstelle.

**Er enthält ausschließlich lesende Operationen.** Es gibt bewusst kein
``mkdir``, ``makedirs``, ``open``, ``touch``, ``write``, ``chmod``, ``chown``,
``unlink``, ``remove``, ``rmdir``, ``rename``, ``replace`` und ``fsync`` —
weder im Protokoll noch in der realen Implementierung. Was hier nicht steht,
kann über diesen Weg auch nicht geschehen.

**Keine stillen Fallbacks.** Eine nicht durchführbare oder nicht eindeutig
feststellbare Beobachtung wird als ``OSError`` an den Planer weitergereicht;
eine auf der Plattform fehlende Semantik wird über
:attr:`FilesystemAdapter.posix_semantics` gemeldet. Der Adapter **emuliert
nichts** und liefert **keinen** Ersatzwert.

Der Import dieses Moduls hat keine Nebenwirkungen.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterator, Protocol, runtime_checkable

__all__ = [
    "FilesystemAdapter",
    "RealFilesystemAdapter",
    "posix_semantics_available",
]


def posix_semantics_available() -> bool:
    """Gibt zurück, ob die Plattform POSIX-Rechtesemantik trägt.

    Maßgeblich ist die Verfügbarkeit von ``os.chown``: fehlt sie, kann die
    Plattform Besitz- und Gruppenzuordnung nicht abbilden, und jede
    Rechteaussage wäre eine Behauptung ohne Grundlage.

    **Ein ``False`` ist kein Fehler, sondern eine Feststellung** — sie führt
    im Planer zu ``KB04-PLATFORM-UNSUPPORTED`` und damit fail-closed, niemals
    zu einem Erfolg.
    """
    return hasattr(os, "chown")


@runtime_checkable
class FilesystemAdapter(Protocol):
    """Minimale **read-only** Sicht auf das Dateisystem.

    Jede Methode darf ``OSError`` erheben. Der Planer behandelt das als
    ``KB04-STATE-INDETERMINATE`` — nicht feststellbar ist nicht erfüllt.
    """

    @property
    def posix_semantics(self) -> bool:
        """Ob die Plattform POSIX-Rechtesemantik trägt."""
        ...

    def exists(self, path: Path) -> bool:
        """Ob der Pfad existiert; folgt keinem Symlink."""
        ...

    def lstat(self, path: Path) -> os.stat_result:
        """``lstat`` des Pfades — folgt **keinem** Symlink."""
        ...

    def stat(self, path: Path) -> os.stat_result:
        """``stat`` des Pfades — folgt Symlinks."""
        ...

    def iterdir(self, path: Path) -> Iterator[Path]:
        """Alle Einträge eines Verzeichnisses, **einschließlich versteckter**."""
        ...

    def resolve(self, path: Path) -> Path:
        """Vollständig aufgelöster Pfad."""
        ...

    def is_mount(self, path: Path) -> bool:
        """Ob der Pfad ein Mountpoint ist."""
        ...


class RealFilesystemAdapter:
    """Reale, ausschließlich lesende Implementierung über die Standardbibliothek.

    Die Klasse hält keinen Zustand, öffnet keine Datei und verändert nichts.
    """

    __slots__ = ()

    @property
    def posix_semantics(self) -> bool:
        """Ob die Plattform POSIX-Rechtesemantik trägt."""
        return posix_semantics_available()

    def exists(self, path: Path) -> bool:
        """Ob der Pfad existiert; folgt keinem Symlink.

        Ein Symlink auf ein fehlendes Ziel gilt als **existierend**, weil das
        Linkobjekt selbst vorhanden und damit ein Befund ist.
        """
        try:
            path.lstat()
        except FileNotFoundError:
            return False
        return True

    def lstat(self, path: Path) -> os.stat_result:
        """``lstat`` des Pfades — folgt **keinem** Symlink."""
        return path.lstat()

    def stat(self, path: Path) -> os.stat_result:
        """``stat`` des Pfades — folgt Symlinks."""
        return path.stat()

    def iterdir(self, path: Path) -> Iterator[Path]:
        """Alle Einträge eines Verzeichnisses, **einschließlich versteckter**."""
        return path.iterdir()

    def resolve(self, path: Path) -> Path:
        """Vollständig aufgelöster Pfad."""
        return path.resolve()

    def is_mount(self, path: Path) -> bool:
        """Ob der Pfad ein Mountpoint ist."""
        return path.is_mount()
