from services.pricing_execution_app_service import PricingExecutionAppService


def main():
    service = PricingExecutionAppService()

    summaries = service.list_execution_summaries()
    if not summaries:
        raise RuntimeError("no execution summaries found via app service")

    latest = summaries[-1]

    if "id" not in latest:
        raise RuntimeError("summary id not found via app service")

    if "execution_status" not in latest:
        raise RuntimeError("summary execution_status not found via app service")

    if "execution_engine" not in latest:
        raise RuntimeError("summary execution_engine not found via app service")

    print("APP SERVICE SUMMARIES:", summaries)
    print("PRICING EXECUTION APP SERVICE LIST SMOKE OK")


if __name__ == "__main__":
    main()
