from fastapi.testclient import TestClient
from main import app


def main():
    client = TestClient(app)

    response = client.get("/pricing-executions/latest?reference_date=10-05-2026")
    if response.status_code != 400:
        raise RuntimeError(f"expected 400, got {response.status_code}: {response.text}")

    print("LATEST INVALID REFERENCE DATE RESPONSE:", response.json())
    print("PRICING EXECUTION CONTROLLER LATEST INVALID REFERENCE DATE SMOKE OK")


if __name__ == "__main__":
    main()
