import sys
from pathlib import Path

from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from main import app
from services.pricing_execution_query_service import PricingExecutionQueryService


def main():
    service = PricingExecutionQueryService()
    summaries = service.list_execution_summaries()

    if not summaries:
        raise RuntimeError(
            "no execution summaries found for controller detail smoke test"
        )

    latest = summaries[0]

    client = TestClient(app)
    response = client.get(f"/pricing-executions/{latest['id']}")

    if response.status_code != 200:
        raise RuntimeError(
            f"controller detail returned status {response.status_code}: {response.text}"
        )

    data = response.json()

    if data["id"] != latest["id"]:
        raise RuntimeError("controller detail id does not match requested execution id")

    if "pricing_payload" not in data:
        raise RuntimeError("pricing_payload not found in controller detail response")

    if "result" not in data:
        raise RuntimeError("result not found in controller detail response")

    print("CONTROLLER EXECUTION DETAIL:", data)
    print("PRICING EXECUTION CONTROLLER DETAIL SMOKE OK")


if __name__ == "__main__":
    main()
