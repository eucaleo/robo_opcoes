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
            result = execution.get("result", {})
            metrics = result.get("metrics", {})
            valuation = result.get("valuation", {})

            summary = {
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

            if structure_id is not None and summary["structure_id"] != structure_id:
                continue

            if (
                underlying_asset is not None
                and summary["underlying_asset"] != underlying_asset
            ):
                continue

            if status is not None and summary["status"] != status:
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
