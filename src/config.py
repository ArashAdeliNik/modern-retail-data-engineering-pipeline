from __future__ import annotations

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LANDING_DIR = Path(os.getenv("LANDING_DIR", PROJECT_ROOT / "data" / "landing"))
REJECTED_DIR = Path(os.getenv("REJECTED_DIR", PROJECT_ROOT / "data" / "rejected"))
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{PROJECT_ROOT / 'local_warehouse.db'}")

