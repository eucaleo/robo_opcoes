from services.pricing_execution_query_service import PricingExecutionQueryService
from _smoke_context import require_context_value


def main():
    service = PricingExecutionQueryService()

    structure_id = require_context_value("structure_id")
    execution_id = require_context_value("execution_id")

    executions = service.list_executions()
    loaded_execution = service.get_execution(execution_id)

    if not isinstance(executions, list):
        raise RuntimeError("executions should be a list")

    if not executions:
        raise RuntimeError("executions should not be empty")

    if loaded_execution["id"] != execution_id:
        raise RuntimeError("loaded execution id should match smoke context execution_id")

    if loaded_execution["structure_id"] != structure_id:
        raise RuntimeError("loaded execution structure_id should match smoke context structure_id")

    print("EXECUTIONS COUNT:", len(executions))
    print("LOADED EXECUTION:", loaded_execution)
    print("PRICING EXECUTION QUERY SERVICE SMOKE OK")


if __name__ == "__main__":
    main()
