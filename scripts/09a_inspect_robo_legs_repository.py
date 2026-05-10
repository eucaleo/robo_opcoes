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
    print(f"PROJECT_ROOT: {PROJECT_ROOT}")
    print()

    print("CLASS:", RoboLegsRepository)
    print("INIT SIGNATURE:", inspect.signature(RoboLegsRepository.__init__))
    print("GET_LEGS SIGNATURE:", inspect.signature(RoboLegsRepository.get_legs))
    print()

    try:
        print("SOURCE FILE:", inspect.getsourcefile(RoboLegsRepository))
    except Exception as e:
        print("SOURCE FILE ERROR:", e)

    print()
    print("PUBLIC METHODS:")
    for name, member in inspect.getmembers(RoboLegsRepository, predicate=inspect.isfunction):
        if not name.startswith("_"):
            print(f"  - {name}{inspect.signature(member)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
