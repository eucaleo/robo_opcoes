# services/pricing_execution_persistence_service.py
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
        pricing_payload: dict[str, Any] | None,
        result: dict[str, Any],
        duration_ms: int | None = None,
        error_message: str | None = None,
    ) -> dict[str, Any]:
        # result é o dict do engine: { engine, status, metrics, valuation, ... }
        # a fachada garante que o wrapper externo já foi desempacotado antes de chegar aqui
        metrics   = result.get("metrics",   {})
        valuation = result.get("valuation", {})

        execution_engine        = result.get("engine")
        execution_status        = result.get("status")
        persisted_error_message = error_message or result.get("error_message")
        number_of_legs          = metrics.get("number_of_legs")
        total_quantity          = metrics.get("total_quantity")
        theoretical_value       = valuation.get("theoretical_value")

        record = self.pricing_executions_repository.save_execution(
            pricing_payload=pricing_payload,
            result=result,
            execution_status=execution_status,
            execution_engine=execution_engine,
            error_message=persisted_error_message,
            duration_ms=duration_ms,
            number_of_legs=number_of_legs,
            total_quantity=total_quantity,
            theoretical_value=theoretical_value,
        )

        return {
            "record": record,
        }
