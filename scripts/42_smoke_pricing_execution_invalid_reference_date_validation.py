import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from services.pricing_execution_query_service import PricingExecutionQueryService


def main():
    service = PricingExecutionQueryService()

    try:
        service.list_execution_summaries(reference_date="10-05-2026")
    except ValueError as exc:
        print("EXPECTED ERROR:", exc)
        print("PRICING EXECUTION INVALID REFERENCE DATE VALIDATION SMOKE OK")
        return

    raise RuntimeError("expected ValueError for invalid reference_date")


if __name__ == "__main__":
    main()
