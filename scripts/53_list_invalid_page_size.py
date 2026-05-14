from fastapi.testclient import TestClient
from main import app


def main():
    client = TestClient(app)

    response = client.get("/pricing-executions?page_size=0")
    if response.status_code != 400:
        raise RuntimeError(f"expected 400, got {response.status_code}: {response.text}")

    print("LIST INVALID PAGE SIZE RESPONSE:", response.json())
    print("PRICING EXECUTION CONTROLLER LIST INVALID PAGE SIZE SMOKE OK")


if __name__ == "__main__":
    main()
