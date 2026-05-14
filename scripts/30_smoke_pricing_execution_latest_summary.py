from services.pricing_execution_query_service import PricingExecutionQueryService


def main():
    service = PricingExecutionQueryService()

    latest = service.get_latest_execution_summary()
    summaries = service.list_execution_summaries()

    if latest["id"] != summaries[0]["id"]:
        raise RuntimeError("latest summary should match first item from descending summaries")

    print("LATEST SUMMARY:", latest)
    print("PRICING EXECUTION LATEST SUMMARY SMOKE OK")


if __name__ == "__main__":
    main()
