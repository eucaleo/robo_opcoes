from typing import Any

from repositories.pricing_executions_repository import PricingExecutionsRepository


class PricingExecutionPersistenceService:
    def __init__(
        self,
        pricing_executions_repository: PricingExecutionsRepository | None = None,
    ):
        self.pricing_executions_repository = (
            pricing_executions_repository or PricingExecutionsRepository()
        )

    def persist_execution(
        self,
        pricing_payload: dict[str, Any],
        result: dict[str, Any],
        duration_ms: int | None = None,
        error_message: str | None = None,
    ) -> dict[str, Any]:
        execution_result = result.get("result", {})
        metrics = execution_result.get("metrics", {})
        valuation = execution_result.get("valuation", {})

        execution_engine = execution_result.get("engine")
        execution_status = execution_result.get("status")
        number_of_legs = metrics.get("number_of_legs")
        total_quantity = metrics.get("total_quantity")
        theoretical_value = valuation.get("theoretical_value")

        record = self.pricing_executions_repository.save_execution(
            pricing_payload=pricing_payload,
            result=result,
            execution_status=execution_status,
            execution_engine=execution_engine,
            error_message=error_message,
            duration_ms=duration_ms,
            number_of_legs=number_of_legs,
            total_quantity=total_quantity,
            theoretical_value=theoretical_value,
        )

        return {
            "record": record,
        }
