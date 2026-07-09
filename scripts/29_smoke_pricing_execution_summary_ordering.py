from services.pricing_execution_query_service import PricingExecutionQueryService


def main():
    service = PricingExecutionQueryService()

    summaries = service.list_execution_summaries()
    if len(summaries) < 2:
        raise RuntimeError("at least two summaries are required for ordering smoke")

    first_id = summaries[0]["id"]
    second_id = summaries[1]["id"]

    if first_id < second_id:
        raise RuntimeError("summaries should be ordered by id descending by default")

    print("ORDERED SUMMARIES:", summaries)
    print("PRICING EXECUTION SUMMARY ORDERING SMOKE OK")


if __name__ == "__main__":
    main()
