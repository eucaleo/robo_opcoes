import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from services.pricing_execution_query_service import PricingExecutionQueryService


def main():
    service = PricingExecutionQueryService()

    latest = service.get_latest_execution_summary()
    summaries = service.list_execution_summaries()

    if latest["id"] != summaries[0]["id"]:
        raise RuntimeError("latest summary should match first item from descending summaries")

    print("LATEST SUMMARY:", latest)
    print("PRICING EXECUTION LATEST SUMMARY SMOKE OK")


if __name__ == "__main__":
    main()
