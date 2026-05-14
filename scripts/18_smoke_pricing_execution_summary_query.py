from services.pricing_execution_query_service import PricingExecutionQueryService
from _smoke_context import require_context_value


def main():
    service = PricingExecutionQueryService()

    structure_id = require_context_value("structure_id")
    execution_id = require_context_value("execution_id")

    summaries = service.list_execution_summaries()

    if not isinstance(summaries, list):
        raise RuntimeError("summaries should be a list")

    if not summaries:
        raise RuntimeError("summaries should not be empty")

    summary = next((item for item in summaries if item["id"] == execution_id), None)

    if summary is None:
        raise RuntimeError("summary list should contain smoke context execution_id")

    if summary["structure_id"] != structure_id:
        raise RuntimeError("summary structure_id should match smoke context structure_id")

    if summary["execution_status"] != "ok":
        raise RuntimeError("summary execution_status should be ok")

    print("SUMMARIES COUNT:", len(summaries))
    print("SMOKE SUMMARY:", summary)
    print("PRICING EXECUTION SUMMARY QUERY SMOKE OK")


if __name__ == "__main__":
    main()
