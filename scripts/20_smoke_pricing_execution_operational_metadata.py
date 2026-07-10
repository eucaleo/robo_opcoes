from services.pricing_execution_query_service import PricingExecutionQueryService


def main():
    service = PricingExecutionQueryService()

    summaries = service.list_execution_summaries()
    if not summaries:
        raise RuntimeError("no execution summaries found for operational metadata smoke test")

    first_summary = summaries[-1]

    if "execution_engine" not in first_summary:
        raise RuntimeError("execution_engine not found in summary")

    if "execution_status" not in first_summary:
        raise RuntimeError("execution_status not found in summary")

    if "duration_ms" not in first_summary:
        raise RuntimeError("duration_ms not found in summary")

    if "error_message" not in first_summary:
        raise RuntimeError("error_message not found in summary")

    print("LATEST SUMMARY:", first_summary)
    print("PRICING EXECUTION OPERATIONAL METADATA SMOKE OK")


if __name__ == "__main__":
    main()
