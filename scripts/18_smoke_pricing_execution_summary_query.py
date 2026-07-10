from services.pricing_execution_query_service import PricingExecutionQueryService


def main():
    service = PricingExecutionQueryService()

    summaries = service.list_execution_summaries()
    if not summaries:
        raise RuntimeError("no execution summaries found for pricing summary query smoke test")

    first_summary = summaries[0]

    print("SUMMARIES COUNT:", len(summaries))
    print("FIRST SUMMARY:", first_summary)
    print("PRICING EXECUTION SUMMARY QUERY SMOKE OK")


if __name__ == "__main__":
    main()
