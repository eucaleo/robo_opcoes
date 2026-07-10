from services.pricing_execution_query_service import PricingExecutionQueryService


def main():
    service = PricingExecutionQueryService()

    try:
        service.paginate_execution_summaries(page=0, page_size=10)
    except ValueError as exc:
        print("EXPECTED ERROR:", exc)
        print("PRICING EXECUTION INVALID PAGE VALIDATION SMOKE OK")
        return

    raise RuntimeError("expected ValueError for invalid page")


if __name__ == "__main__":
    main()
