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
        record = self.pricing_executions_repository.save_execution(
            pricing_payload=pricing_payload,
            result=result,
        )

        return {
            "record": record,
            "duration_ms": duration_ms,
            "error_message": error_message,
        }
