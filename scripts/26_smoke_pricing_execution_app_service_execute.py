from services.pricing_execution_app_service import PricingExecutionAppService


def main():
    service = PricingExecutionAppService()

    response = service.execute_pricing(structure_id=2)
    if isinstance(response, dict) and "persisted" in response:
        record = response["persisted"]["record"]
    else:
        record = response

    if record["execution_status"] != "ok":
        raise RuntimeError("app service execution_status should be ok")

    if record["execution_engine"] != "stub":
        raise RuntimeError("app service execution_engine should be stub")

    if record["duration_ms"] is None:
        raise RuntimeError("app service duration_ms should not be None")

    print("APP SERVICE EXECUTE RESPONSE:", response)
    print("PRICING EXECUTION APP SERVICE EXECUTE SMOKE OK")


if __name__ == "__main__":
    main()
