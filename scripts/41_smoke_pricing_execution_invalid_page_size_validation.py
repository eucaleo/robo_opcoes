from services.pricing_execution_query_service import PricingExecutionQueryService


def main():
    service = PricingExecutionQueryService()

    try:
        service.paginate_execution_summaries(page=1, page_size=0)
    except ValueError as exc:
        print("EXPECTED ERROR:", exc)
        print("PRICING EXECUTION INVALID PAGE SIZE VALIDATION SMOKE OK")
        return

    raise RuntimeError("expected ValueError for invalid page_size")


if __name__ == "__main__":
    main()
