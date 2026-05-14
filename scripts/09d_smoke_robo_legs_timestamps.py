from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from repositories.robo_legs_repository import RoboLegsRepository


def main() -> int:
    repo = RoboLegsRepository()

    abas = ["BOVA11", "EMBJ3", "PRIO3", "SMAL11", "SBSP3"]

    print("== SMOKE ROBO LEGS TIMESTAMPS ==")
    print(f"PROJECT_ROOT: {PROJECT_ROOT}")
    print()

    for aba in abas:
        print("=" * 80)
        print(f"ABA: {aba}")

        for prefer in ["manual_then_rtd", "manual_only", "rtd_only"]:
            try:
                timestamps = repo.list_timestamps(aba, prefer=prefer)
                print(f"PREFER={prefer} COUNT={len(timestamps)}")
                print("HEAD:", timestamps[:5])
                print("TAIL:", timestamps[-5:] if timestamps else [])
            except Exception as e:
                print(f"PREFER={prefer} ERROR={type(e).__name__}: {e}")

        print()

    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
