from services.pricing_execution_query_service import PricingExecutionQueryService


def main():
    service = PricingExecutionQueryService()

    try:
        service.list_execution_summaries(status="invalid")
    except ValueError as exc:
        print("EXPECTED ERROR:", exc)
        print("PRICING EXECUTION INVALID STATUS VALIDATION SMOKE OK")
        return

    raise RuntimeError("expected ValueError for invalid status")


if __name__ == "__main__":
    main()
