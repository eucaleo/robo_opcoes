from services.pricing_execution_query_service import PricingExecutionQueryService


def main():
    service = PricingExecutionQueryService()

    all_summaries = service.list_execution_summaries()
    if not all_summaries:
        raise RuntimeError("no execution summaries found for filtered summary smoke test")

    first = all_summaries[0]

    filtered_by_structure = service.list_execution_summaries(
        structure_id=first["structure_id"]
    )
    filtered_by_asset = service.list_execution_summaries(
        underlying_asset=first["underlying_asset"]
    )
    filtered_by_status = service.list_execution_summaries(status=first["status"])
    filtered_by_reference_date = service.list_execution_summaries(
        reference_date=first["reference_date"]
    )

    if not filtered_by_structure:
        raise RuntimeError("structure_id filter returned no results")

    if not filtered_by_asset:
        raise RuntimeError("underlying_asset filter returned no results")

    if not filtered_by_status:
        raise RuntimeError("status filter returned no results")

    if not filtered_by_reference_date:
        raise RuntimeError("reference_date filter returned no results")

    print("ALL SUMMARIES:", all_summaries)
    print("FILTERED BY STRUCTURE:", filtered_by_structure)
    print("FILTERED BY ASSET:", filtered_by_asset)
    print("FILTERED BY STATUS:", filtered_by_status)
    print("FILTERED BY REFERENCE DATE:", filtered_by_reference_date)
    print("PRICING EXECUTION FILTERED SUMMARY QUERY SMOKE OK")


if __name__ == "__main__":
    main()
