from typing import Any

from repositories.pricing_executions_repository import PricingExecutionsRepository


class PricingExecutionQueryService:
    def __init__(
        self,
        pricing_executions_repository: PricingExecutionsRepository | None = None,
    ):
        self.pricing_executions_repository = (
            pricing_executions_repository or PricingExecutionsRepository()
        )

    def list_executions(self) -> list[dict[str, Any]]:
        return self.pricing_executions_repository.list_executions()

    def list_execution_summaries(self) -> list[dict[str, Any]]:
        executions = self.pricing_executions_repository.list_executions()

        summaries = []
        for execution in executions:
            result = execution.get("result", {})
            metrics = result.get("metrics", {})
            valuation = result.get("valuation", {})

            summaries.append(
                {
                    "id": execution["id"],
                    "created_at": execution["created_at"],
                    "structure_id": execution["structure_id"],
                    "underlying_asset": execution["underlying_asset"],
                    "reference_date": execution["reference_date"],
                    "engine": result.get("engine"),
                    "status": result.get("status"),
                    "number_of_legs": metrics.get("number_of_legs"),
                    "total_quantity": metrics.get("total_quantity"),
                    "theoretical_value": valuation.get("theoretical_value"),
                }
            )

        return summaries

    def get_execution(self, execution_id: int) -> dict[str, Any] | None:
        if execution_id <= 0:
            raise ValueError("execution_id must be greater than zero")

        return self.pricing_executions_repository.get_execution(execution_id)
