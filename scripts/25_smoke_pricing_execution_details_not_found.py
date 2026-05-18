import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from services.pricing_execution_query_service import PricingExecutionQueryService


def main():
    service = PricingExecutionQueryService()

    try:
        service.get_execution_details(999999)
    except ValueError as exc:
        if "not found" not in str(exc):
            raise RuntimeError("unexpected error message for missing execution") from exc

        print("EXPECTED ERROR:", str(exc))
        print("PRICING EXECUTION DETAILS NOT FOUND SMOKE OK")
        return

    raise RuntimeError("missing execution should have raised ValueError")


if __name__ == "__main__":
    main()
