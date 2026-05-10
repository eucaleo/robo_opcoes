from fastapi.testclient import TestClient
from main import app


def main():
    client = TestClient(app)

    response = client.get("/pricing-executions/999999")
    if response.status_code != 404:
        raise RuntimeError(f"expected 404, got {response.status_code}: {response.text}")

    print("EXECUTION NOT FOUND RESPONSE:", response.json())
    print("PRICING EXECUTION CONTROLLER EXECUTION NOT FOUND SMOKE OK")


if __name__ == "__main__":
    main()
