from services.pricing_execution_app_service import PricingExecutionAppService


def main():
    service = PricingExecutionAppService()

    page_data = service.paginate_execution_summaries(
        underlying_asset="BOVA11",
        reference_date="2026-05-10",
        status="ok",
        page=1,
        page_size=10,
    )

    items = page_data["items"]
    if not items:
        raise RuntimeError("expected filtered app service pagination to return items")

    for item in items:
        if item["underlying_asset"] != "BOVA11":
            raise RuntimeError("invalid underlying_asset in filtered app service pagination")
        if item["reference_date"] != "2026-05-10":
            raise RuntimeError("invalid reference_date in filtered app service pagination")
        if item["execution_status"] != "ok":
            raise RuntimeError("invalid execution_status in filtered app service pagination")

    print("APP SERVICE FILTERED PAGINATION:", page_data)
    print("PRICING EXECUTION APP SERVICE FILTERED PAGINATION SMOKE OK")


if __name__ == "__main__":
    main()
