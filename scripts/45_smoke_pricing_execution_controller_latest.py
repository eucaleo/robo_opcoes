import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi.testclient import TestClient

from main import app


def main():
    client = TestClient(app)

    response = client.get("/pricing-executions/latest?status=ok")
    if response.status_code != 200:
        raise RuntimeError(f"expected 200, got {response.status_code}: {response.text}")

    data = response.json()
    if data["execution_status"] != "ok":
        raise RuntimeError("latest endpoint returned invalid status")

    print("LATEST RESPONSE:", data)
    print("PRICING EXECUTION CONTROLLER LATEST SMOKE OK")


if __name__ == "__main__":
    main()
