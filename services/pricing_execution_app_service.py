from typing import Any

from services.pricing_execution_orchestration_service import (
    PricingExecutionOrchestrationService,
)
from services.pricing_execution_query_service import PricingExecutionQueryService


class PricingExecutionAppService:
    def __init__(
        self,
        pricing_execution_orchestration_service: (
            PricingExecutionOrchestrationService | None
        ) = None,
        pricing_execution_query_service: PricingExecutionQueryService | None = None,
    ):
        self.pricing_execution_orchestration_service = (
            pricing_execution_orchestration_service
            or PricingExecutionOrchestrationService()
        )
        self.pricing_execution_query_service = (
            pricing_execution_query_service or PricingExecutionQueryService()
        )

    def execute_pricing(
        self,
        structure_id: int,
        reference_date: str | None = None,
    ) -> dict[str, Any]:
        return self.pricing_execution_orchestration_service.execute_and_persist(
            structure_id=structure_id,
            reference_date=reference_date,
        )

    def list_execution_summaries(
        self,
        structure_id: int | None = None,
        underlying_asset: str | None = None,
        status: str | None = None,
        reference_date: str | None = None,
        descending: bool = True,
    ) -> list[dict[str, Any]]:
        return self.pricing_execution_query_service.list_execution_summaries(
            structure_id=structure_id,
            underlying_asset=underlying_asset,
            status=status,
            reference_date=reference_date,
            descending=descending,
        )

    def get_latest_execution_summary(
        self,
        structure_id: int | None = None,
        underlying_asset: str | None = None,
        status: str | None = None,
        reference_date: str | None = None,
    ) -> dict[str, Any]:
        return self.pricing_execution_query_service.get_latest_execution_summary(
            structure_id=structure_id,
            underlying_asset=underlying_asset,
            status=status,
            reference_date=reference_date,
        )

    def get_execution(self, execution_id: int) -> dict[str, Any]:
        return self.pricing_execution_query_service.get_execution(execution_id)
