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
