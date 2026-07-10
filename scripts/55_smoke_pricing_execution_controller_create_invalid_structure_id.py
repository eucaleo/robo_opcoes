from fastapi.testclient import TestClient
from main import app


def main():
    client = TestClient(app)

    response = client.post(
        "/pricing-executions",
        json={
            "structure_id": 0,
            "reference_date": "2026-05-10"
        },
    )

    if response.status_code != 400:
        raise RuntimeError(f"expected 400, got {response.status_code}: {response.text}")

    print("CREATE INVALID STRUCTURE RESPONSE:", response.json())
    print("PRICING EXECUTION CONTROLLER CREATE INVALID STRUCTURE SMOKE OK")


if __name__ == "__main__":
    main()
