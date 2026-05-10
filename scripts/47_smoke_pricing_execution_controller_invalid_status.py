from fastapi.testclient import TestClient

from main import app


def main():
    client = TestClient(app)

    response = client.get("/pricing-executions?status=invalid")
    if response.status_code != 400:
        raise RuntimeError(f"expected 400, got {response.status_code}: {response.text}")

    data = response.json()
    print("INVALID STATUS RESPONSE:", data)
    print("PRICING EXECUTION CONTROLLER INVALID STATUS SMOKE OK")


if __name__ == "__main__":
    main()
