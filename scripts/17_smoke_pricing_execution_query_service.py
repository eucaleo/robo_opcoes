import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from services.pricing_execution_query_service import PricingExecutionQueryService


def main():
    service = PricingExecutionQueryService()

    summaries = service.list_execution_summaries()

    if not isinstance(summaries, list):
        raise RuntimeError("list_execution_summaries must return a list")

    print("EXECUTION SUMMARIES:", summaries)
    print("PRICING EXECUTION QUERY SERVICE SMOKE OK")


if __name__ == "__main__":
    main()
