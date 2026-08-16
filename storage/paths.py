from __future__ import annotations

import os
from pathlib import Path
import sys


_APP_DIR_NAME = "ZenithInventory"


def default_data_directory() -> Path:
    if os.name == "nt":
        base = os.environ.get("LOCALAPPDATA") or os.environ.get("APPDATA")
        root = Path(base) if base else Path.home()
    elif sys.platform == "darwin":
        root = Path.home() / "Library" / "Application Support"
    else:
        root = Path(
            os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share")
        )

    path = root / _APP_DIR_NAME
    path.mkdir(parents=True, exist_ok=True)
    return path


def default_database_path() -> Path:
    return default_data_directory() / "inventory.db"
