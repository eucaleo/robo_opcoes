from fastapi.testclient import TestClient

from main import app


def main():
    client = TestClient(app)

    response = client.get("/pricing-executions/8")
    if response.status_code != 200:
        raise RuntimeError(f"expected 200, got {response.status_code}: {response.text}")

    data = response.json()
    if data["id"] != 8:
        raise RuntimeError("detail endpoint returned wrong execution id")

    print("DETAIL RESPONSE:", data)
    print("PRICING EXECUTION CONTROLLER DETAIL SMOKE OK")


if __name__ == "__main__":
    main()
