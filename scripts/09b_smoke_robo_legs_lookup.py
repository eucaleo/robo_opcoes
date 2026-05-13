from __future__ import annotations

import dataclasses
import sys
from pathlib import Path
from pprint import pprint

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from repositories.robo_legs_repository import RoboLegsRepository
from services.robo_legs_service import LegValidationError, RoboLegsService


def to_debug_dict(obj):
    if hasattr(obj, "model_dump") and callable(obj.model_dump):
        return obj.model_dump()
    if hasattr(obj, "dict") and callable(obj.dict):
        return obj.dict()
    if dataclasses.is_dataclass(obj):
        return dataclasses.asdict(obj)
    if hasattr(obj, "_asdict") and callable(obj._asdict):
        return obj._asdict()
    if hasattr(obj, "__dict__"):
        return vars(obj)
    return repr(obj)


def main() -> int:
    repo = RoboLegsRepository()
    service = RoboLegsService(repo=repo)

    cases = [
        ("BOVA11", "09/05/2026 21:04:53"),
        ("BOVA11", "14/04/2026 17:55:51"),
        ("EMBJ3", "14/04/2026 17:55:51"),
        ("PRIO3", "14/04/2026 17:55:51"),
        ("SMAL11", "14/04/2026 17:55:51"),
        ("SBSP3", "14/04/2026 17:55:51"),
    ]

    print("== SMOKE ROBO LEGS LOOKUP V2 ==")
    print(f"PROJECT_ROOT: {PROJECT_ROOT}")
    print()

    for aba, timestamp in cases:
        print("=" * 80)
        print(f"CASE: aba={aba} timestamp={timestamp}")

        has_manual = repo.has_manual(aba, timestamp)
        print(f"HAS_MANUAL: {has_manual}")

        try:
            legs = service.get_legs(aba=aba, timestamp=timestamp, validate=True)
        except LegValidationError as exc:
            print(f"[FAIL] validação semântica: {exc}")
            print()
            continue

        print(f"LEGS FOUND: {len(legs)}")
        for i, leg in enumerate(legs, start=1):
            print(f"-- LEG {i} --")
            pprint(to_debug_dict(leg))

        print()

    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
