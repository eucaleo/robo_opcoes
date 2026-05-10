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

    def list_execution_summaries(
        self,
        structure_id: int | None = None,
        underlying_asset: str | None = None,
        status: str | None = None,
        reference_date: str | None = None,
    ) -> list[dict[str, Any]]:
        executions = self.pricing_executions_repository.list_executions()

        summaries = []
        for execution in executions:
            persisted_number_of_legs = execution.get("number_of_legs")
            persisted_total_quantity = execution.get("total_quantity")
            persisted_theoretical_value = execution.get("theoretical_value")

            nested_result = execution.get("result", {})
            engine_result = nested_result.get("result", {})
            metrics = engine_result.get("metrics", {})
            valuation = engine_result.get("valuation", {})

            summary = {
                "id": execution["id"],
                "created_at": execution["created_at"],
                "structure_id": execution["structure_id"],
                "underlying_asset": execution["underlying_asset"],
                "reference_date": execution["reference_date"],
                "execution_engine": execution.get("execution_engine"),
                "execution_status": execution.get("execution_status"),
                "duration_ms": execution.get("duration_ms"),
                "error_message": execution.get("error_message"),
                "number_of_legs": (
                    persisted_number_of_legs
                    if persisted_number_of_legs is not None
                    else metrics.get("number_of_legs")
                ),
                "total_quantity": (
                    persisted_total_quantity
                    if persisted_total_quantity is not None
                    else metrics.get("total_quantity")
                ),
                "theoretical_value": (
                    persisted_theoretical_value
                    if persisted_theoretical_value is not None
                    else valuation.get("theoretical_value")
                ),
            }

            if structure_id is not None and summary["structure_id"] != structure_id:
                continue

            if (
                underlying_asset is not None
                and summary["underlying_asset"] != underlying_asset
            ):
                continue

            if status is not None and summary["execution_status"] != status:
                continue

            if (
                reference_date is not None
                and summary["reference_date"] != reference_date
            ):
                continue

            summaries.append(summary)

        return summaries

    def get_execution(self, execution_id: int) -> dict[str, Any] | None:
        if execution_id <= 0:
            raise ValueError("execution_id must be greater than zero")

        return self.pricing_executions_repository.get_execution(execution_id)
