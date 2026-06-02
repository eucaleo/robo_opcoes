import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from services.pricing_execution_app_service import PricingExecutionAppService


def main():
    service = PricingExecutionAppService()

    summaries = service.list_execution_summaries()
    if not summaries:
        raise RuntimeError("no execution summaries found for app service detail smoke")

    latest = summaries[0]
    execution = service.get_execution(latest["id"])

    if execution["id"] != latest["id"]:
        raise RuntimeError("app service execution id does not match latest summary id")

    if "pricing_payload" not in execution:
        raise RuntimeError("pricing_payload not found in app service execution detail")

    if "result" not in execution:
        raise RuntimeError("result not found in app service execution detail")

    print("APP SERVICE EXECUTION DETAIL:", execution)
    print("PRICING EXECUTION APP SERVICE DETAIL SMOKE OK")


if __name__ == "__main__":
    main()
