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

    def get_execution(self, execution_id: int) -> dict[str, Any] | None:
        if execution_id <= 0:
            raise ValueError("execution_id must be greater than zero")

        return self.pricing_executions_repository.get_execution(execution_id)
