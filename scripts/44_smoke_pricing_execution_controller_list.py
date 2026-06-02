import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi.testclient import TestClient

from main import app


def main():
    client = TestClient(app)

    response = client.get("/pricing-executions?page=1&page_size=2")
    if response.status_code != 200:
        raise RuntimeError(f"expected 200, got {response.status_code}: {response.text}")

    data = response.json()
    if "items" not in data:
        raise RuntimeError("response must include items")

    if data["page"] != 1:
        raise RuntimeError("page should be 1")

    if data["page_size"] != 2:
        raise RuntimeError("page_size should be 2")

    print("LIST RESPONSE:", data)
    print("PRICING EXECUTION CONTROLLER LIST SMOKE OK")


if __name__ == "__main__":
    main()
