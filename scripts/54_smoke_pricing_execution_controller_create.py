from fastapi.testclient import TestClient
from main import app


def main():
    client = TestClient(app)

    response = client.post(
        "/pricing-executions",
        json={
            "structure_id": 1,
            "reference_date": "2026-05-10"
        },
    )

    if response.status_code != 200:
        raise RuntimeError(f"expected 200, got {response.status_code}: {response.text}")

    data = response.json()

    if data["structure_id"] != 1:
        raise RuntimeError("structure_id mismatch")

    if data["reference_date"] != "2026-05-10":
        raise RuntimeError("reference_date mismatch")

    if "id" not in data:
        raise RuntimeError("response must contain id")

    print("CREATE RESPONSE:", data)
    print("PRICING EXECUTION CONTROLLER CREATE SMOKE OK")


if __name__ == "__main__":
    main()
