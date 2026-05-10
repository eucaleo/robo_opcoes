from __future__ import annotations

import inspect
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from repositories.robo_legs_repository import RoboLegsRepository


def main() -> int:
    print("== INSPECT ROBO LEGS REPOSITORY ==")
    print()

    print("--- list_timestamps ---")
    print(inspect.getsource(RoboLegsRepository.list_timestamps))
    print()

    if hasattr(RoboLegsRepository, "_list_manual_timestamps"):
        print("--- _list_manual_timestamps ---")
        print(inspect.getsource(RoboLegsRepository._list_manual_timestamps))
        print()

    if hasattr(RoboLegsRepository, "_list_rtd_timestamps"):
        print("--- _list_rtd_timestamps ---")
        print(inspect.getsource(RoboLegsRepository._list_rtd_timestamps))
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
