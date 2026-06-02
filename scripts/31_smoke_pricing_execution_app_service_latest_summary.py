import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from services.pricing_execution_app_service import PricingExecutionAppService


def main():
    service = PricingExecutionAppService()

    latest = service.get_latest_execution_summary()

    if "id" not in latest:
        raise RuntimeError("latest summary id not found via app service")

    if "execution_status" not in latest:
        raise RuntimeError("latest summary execution_status not found via app service")

    print("APP SERVICE LATEST SUMMARY:", latest)
    print("PRICING EXECUTION APP SERVICE LATEST SUMMARY SMOKE OK")


if __name__ == "__main__":
    main()
