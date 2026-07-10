from services.pricing_execution_query_service import PricingExecutionQueryService


def main():
    service = PricingExecutionQueryService()

    first_page = service.paginate_execution_summaries(page=1, page_size=2)
    second_page = service.paginate_execution_summaries(page=2, page_size=2)

    first_items = first_page["items"]
    second_items = second_page["items"]

    if not first_items:
        raise RuntimeError("first page should not be empty")

    if not second_items:
        raise RuntimeError("second page should not be empty")

    if first_items[0]["id"] == second_items[0]["id"]:
        raise RuntimeError("first and second page should not start with the same item")

    print("FIRST PAGE:", first_page)
    print("SECOND PAGE:", second_page)
    print("PRICING EXECUTION SUMMARY PAGINATION SECOND PAGE SMOKE OK")


if __name__ == "__main__":
    main()
