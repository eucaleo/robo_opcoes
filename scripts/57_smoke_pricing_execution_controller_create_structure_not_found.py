from fastapi.testclient import TestClient
from main import app


def main():
    client = TestClient(app)

    response = client.post(
        "/pricing-executions",
        json={
            "structure_id": 999999,
            "reference_date": "2026-05-10"
        },
    )

    if response.status_code not in (400, 404):
        raise RuntimeError(f"expected 400 or 404, got {response.status_code}: {response.text}")

    print("CREATE STRUCTURE NOT FOUND RESPONSE:", response.json())
    print("PRICING EXECUTION CONTROLLER CREATE STRUCTURE NOT FOUND SMOKE OK")


if __name__ == "__main__":
    main()
