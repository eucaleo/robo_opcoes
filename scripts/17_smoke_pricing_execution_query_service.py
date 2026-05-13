from services.pricing_execution_query_service import PricingExecutionQueryService


def main():
    service = PricingExecutionQueryService()

    executions = service.list_executions()
    if not executions:
        raise RuntimeError("no executions found for pricing execution query smoke test")

    first_execution = executions[0]
    execution_id = first_execution["id"]

    loaded = service.get_execution(execution_id)

    print("EXECUTIONS COUNT:", len(executions))
    print("FIRST EXECUTION:", first_execution)
    print("LOADED EXECUTION:", loaded)
    print("PRICING EXECUTION QUERY SERVICE SMOKE OK")


if __name__ == "__main__":
    main()
