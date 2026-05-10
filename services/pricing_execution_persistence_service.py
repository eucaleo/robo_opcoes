from typing import Any

from repositories.pricing_executions_repository import PricingExecutionsRepository
from services.pricing_execution_service import PricingExecutionService


class PricingExecutionPersistenceService:
    def __init__(
        self,
        pricing_execution_service: PricingExecutionService | None = None,
        pricing_executions_repository: PricingExecutionsRepository | None = None,
    ):
        self.pricing_execution_service = pricing_execution_service or PricingExecutionService()
        self.pricing_executions_repository = (
            pricing_executions_repository or PricingExecutionsRepository()
        )

    def execute_and_persist(
        self,
        structure_id: int,
        reference_date: str | None = None,
    ) -> dict[str, Any]:
        execution = self.pricing_execution_service.execute(
            structure_id=structure_id,
            reference_date=reference_date,
        )

        record = self.pricing_executions_repository.save_execution(
            pricing_payload=execution["pricing_payload"],
            result=execution["result"],
        )

        return {
            "execution": execution,
            "record": record,
        }
