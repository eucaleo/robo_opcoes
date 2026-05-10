from __future__ import annotations

import sys
from pathlib import Path
from pprint import pprint

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from repositories.robo_legs_repository import RoboLegsRepository


APP_DB = "./dados/app.db"


def main() -> int:
    repo = RoboLegsRepository(APP_DB)

    cases = [
        ("manual", "BOVA11", "09/05/2026 21:04:53"),
        ("rtd", "BOVA11", "14/04/2026 17:55:51"),
        ("rtd", "EMBJ3", "14/04/2026 17:55:51"),
        ("rtd", "PRIO3", "14/04/2026 17:55:51"),
        ("rtd", "SMAL11", "14/04/2026 17:55:51"),
        ("rtd", "SBSP3", "14/04/2026 17:55:51"),
    ]

    print("== SMOKE ROBO LEGS LOOKUP ==")
    print(f"PROJECT_ROOT: {PROJECT_ROOT}")
    print(f"DB: {APP_DB}")
    print()

    for source, aba, timestamp in cases:
        print("=" * 80)
        print(f"CASE: source={source} aba={aba} timestamp={timestamp}")

        legs = repo.get_legs(source=source, aba=aba, timestamp=timestamp)

        print(f"LEGS FOUND: {len(legs)}")
        for i, leg in enumerate(legs, start=1):
            print(f"-- LEG {i} --")
            pprint(leg.model_dump())

        print()

    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
