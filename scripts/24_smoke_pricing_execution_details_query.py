from services.pricing_execution_query_service import PricingExecutionQueryService


def main():
    service = PricingExecutionQueryService()

    summaries = service.list_execution_summaries()
    if not summaries:
        raise RuntimeError("no execution summaries found for details query smoke test")

    latest = summaries[-1]
    details = service.get_execution_details(latest["id"])

    if details["id"] != latest["id"]:
        raise RuntimeError("details id does not match requested execution id")

    if "pricing_payload" not in details:
        raise RuntimeError("pricing_payload not found in execution details")

    if "result" not in details:
        raise RuntimeError("result not found in execution details")

    if details["structure_id"] != latest["structure_id"]:
        raise RuntimeError("details structure_id does not match summary")

    print("EXECUTION DETAILS:", details)
    print("PRICING EXECUTION DETAILS QUERY SMOKE OK")


if __name__ == "__main__":
    main()
