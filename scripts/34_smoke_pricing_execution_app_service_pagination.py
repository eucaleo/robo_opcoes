import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from services.pricing_execution_app_service import PricingExecutionAppService


def main():
    service = PricingExecutionAppService()

    page_data = service.paginate_execution_summaries(page=1, page_size=5)

    if "items" not in page_data:
        raise RuntimeError("app service pagination must include items")

    if page_data["page"] != 1:
        raise RuntimeError("app service pagination page should be 1")

    if page_data["page_size"] != 5:
        raise RuntimeError("app service pagination page_size should be 5")

    print("APP SERVICE PAGINATION:", page_data)
    print("PRICING EXECUTION APP SERVICE PAGINATION SMOKE OK")


if __name__ == "__main__":
    main()
