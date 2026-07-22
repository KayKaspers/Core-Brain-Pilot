"""Modul-Einstiegspunkt: ``py -3.13 -m core.core_brain``.

Der Aufruf von :func:`core.core_brain.cli.main` erfolgt ausschließlich
innerhalb des ``__main__``-Guards. Ein Import dieses Moduls führt nichts aus.
"""

from __future__ import annotations

import sys

from .cli import main

if __name__ == "__main__":
    sys.exit(main())
