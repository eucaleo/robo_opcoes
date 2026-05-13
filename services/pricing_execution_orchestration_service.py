import time
from typing import Any

from services.pricing_execution_persistence_service import (
    PricingExecutionPersistenceService,
)
from services.pricing_execution_service import PricingExecutionService
from services.pricing_input_service import PricingInputService


class PricingExecutionOrchestrationService:
    def __init__(
        self,
        pricing_input_service: PricingInputService | None = None,
        pricing_execution_service: PricingExecutionService | None = None,
        pricing_execution_persistence_service: PricingExecutionPersistenceService | None = None,
    ):
        self.pricing_input_service = pricing_input_service or PricingInputService()
        self.pricing_execution_service = pricing_execution_service or PricingExecutionService()
        self.pricing_execution_persistence_service = (
            pricing_execution_persistence_service or PricingExecutionPersistenceService()
        )

    def execute_and_persist(
        self,
        structure_id: int,
        reference_date: str | None = None,
    ) -> dict[str, Any]:
        pricing_payload = self.pricing_input_service.build_pricing_payload(
            structure_id=structure_id,
            reference_date=reference_date,
        )

        started_at = time.perf_counter()

        try:
            result = self.pricing_execution_service.execute(
                structure_id=structure_id,
                reference_date=reference_date,
            )
            duration_ms = int((time.perf_counter() - started_at) * 1000)

            persisted = self.pricing_execution_persistence_service.persist_execution(
                pricing_payload=pricing_payload,
                result=result,
                duration_ms=duration_ms,
                error_message=None,
            )

            return {
                "pricing_payload": pricing_payload,
                "result": result,
                "persisted": persisted,
            }

        except Exception as exc:
            duration_ms = int((time.perf_counter() - started_at) * 1000)
            error_message = str(exc)

            result = {
                "pricing_payload": pricing_payload,
                "result": {
                    "engine": "stub",
                    "status": "error",
                    "error_message": error_message,
                },
            }

            persisted = self.pricing_execution_persistence_service.persist_execution(
                pricing_payload=pricing_payload,
                result=result,
                duration_ms=duration_ms,
                error_message=error_message,
            )

            return {
                "pricing_payload": pricing_payload,
                "result": result,
                "persisted": persisted,
            }
