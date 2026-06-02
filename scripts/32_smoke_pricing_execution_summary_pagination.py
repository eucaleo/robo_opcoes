import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from services.pricing_execution_query_service import PricingExecutionQueryService


def main():
    service = PricingExecutionQueryService()

    page_data = service.paginate_execution_summaries(page=1, page_size=3)

    if "items" not in page_data:
        raise RuntimeError("pagination result must include items")

    if "total_items" not in page_data:
        raise RuntimeError("pagination result must include total_items")

    if "total_pages" not in page_data:
        raise RuntimeError("pagination result must include total_pages")

    if len(page_data["items"]) > 3:
        raise RuntimeError("page size exceeded in pagination result")

    print("PAGINATION PAGE 1:", page_data)
    print("PRICING EXECUTION SUMMARY PAGINATION SMOKE OK")


if __name__ == "__main__":
    main()
