import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from services.pricing_execution_query_service import PricingExecutionQueryService


def main():
    service = PricingExecutionQueryService()

    try:
        service.get_latest_execution_summary(structure_id=0)
    except ValueError as exc:
        print("EXPECTED ERROR:", exc)
        print("PRICING EXECUTION INVALID STRUCTURE ID VALIDATION SMOKE OK")
        return

    raise RuntimeError("expected ValueError for invalid structure_id")


if __name__ == "__main__":
    main()
