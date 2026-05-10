from services.pricing_execution_query_service import PricingExecutionQueryService


def main():
    service = PricingExecutionQueryService()

    latest_ok = service.get_latest_execution_summary(status="ok")
    if latest_ok["execution_status"] != "ok":
        raise RuntimeError("latest ok execution returned invalid status")

    latest_error = service.get_latest_execution_summary(status="error")
    if latest_error["execution_status"] != "error":
        raise RuntimeError("latest error execution returned invalid status")

    print("LATEST OK:", latest_ok)
    print("LATEST ERROR:", latest_error)
    print("PRICING EXECUTION LATEST SUMMARY BY STATUS SMOKE OK")


if __name__ == "__main__":
    main()
