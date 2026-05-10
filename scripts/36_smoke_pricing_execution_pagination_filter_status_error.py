from services.pricing_execution_query_service import PricingExecutionQueryService


def main():
    service = PricingExecutionQueryService()

    page_data = service.paginate_execution_summaries(status="error", page=1, page_size=10)

    items = page_data["items"]
    if not items:
        raise RuntimeError("expected at least one error execution")

    for item in items:
        if item["execution_status"] != "error":
            raise RuntimeError("pagination filter by status=error returned invalid item")

    print("FILTER STATUS ERROR PAGINATION:", page_data)
    print("PRICING EXECUTION PAGINATION FILTER STATUS ERROR SMOKE OK")


if __name__ == "__main__":
    main()
