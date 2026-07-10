from services.pricing_execution_query_service import PricingExecutionQueryService


def main():
    service = PricingExecutionQueryService()

    summaries = service.list_execution_summaries()
    if not summaries:
        raise RuntimeError("no execution summaries found for details query smoke test")

    latest = summaries[-1]
    execution = service.get_execution(latest["id"])

    if execution["id"] != latest["id"]:
        raise RuntimeError("execution id does not match requested execution id")

    if "pricing_payload" not in execution:
        raise RuntimeError("pricing_payload not found in execution details")

    if "result" not in execution:
        raise RuntimeError("result not found in execution details")

    if execution["structure_id"] != latest["structure_id"]:
        raise RuntimeError("execution structure_id does not match summary")

    print("EXECUTION DETAILS:", execution)
    print("PRICING EXECUTION DETAILS QUERY SMOKE OK")


if __name__ == "__main__":
    main()
