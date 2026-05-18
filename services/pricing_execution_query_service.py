from datetime import datetime
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

    def _validate_summary_filters(
        self,
        structure_id: int | None = None,
        underlying_asset: str | None = None,
        status: str | None = None,
        reference_date: str | None = None,
    ) -> None:
        if structure_id is not None and structure_id <= 0:
            raise ValueError("structure_id must be greater than zero")

        if underlying_asset is not None and not underlying_asset.strip():
            raise ValueError("underlying_asset must not be empty")

        if status is not None and status not in {"ok", "error"}:
            raise ValueError("status must be either 'ok' or 'error'")

        if reference_date is not None:
            if not reference_date.strip():
                raise ValueError("reference_date must not be empty")

            try:
                datetime.strptime(reference_date, "%Y-%m-%d")
            except ValueError as exc:
                raise ValueError(
                    "reference_date must be in YYYY-MM-DD format"
                ) from exc

    def list_executions(self) -> list[dict[str, Any]]:
        return self.pricing_executions_repository.list_executions()

    def list_execution_summaries(
        self,
        structure_id: int | None = None,
        underlying_asset: str | None = None,
        status: str | None = None,
        reference_date: str | None = None,
        descending: bool = True,
    ) -> list[dict[str, Any]]:
        self._validate_summary_filters(
            structure_id=structure_id,
            underlying_asset=underlying_asset,
            status=status,
            reference_date=reference_date,
        )

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

        summaries.sort(key=lambda item: item["id"], reverse=descending)
        return summaries

    def paginate_execution_summaries(
        self,
        structure_id: int | None = None,
        underlying_asset: str | None = None,
        status: str | None = None,
        reference_date: str | None = None,
        descending: bool = True,
        page: int = 1,
        page_size: int = 10,
    ) -> dict[str, Any]:
        self._validate_summary_filters(
            structure_id=structure_id,
            underlying_asset=underlying_asset,
            status=status,
            reference_date=reference_date,
        )

        if page <= 0:
            raise ValueError("page must be greater than zero")

        if page_size <= 0:
            raise ValueError("page_size must be greater than zero")

        summaries = self.list_execution_summaries(
            structure_id=structure_id,
            underlying_asset=underlying_asset,
            status=status,
            reference_date=reference_date,
            descending=descending,
        )

        total_items = len(summaries)
        total_pages = (
            (total_items + page_size - 1) // page_size if total_items > 0 else 0
        )

        start = (page - 1) * page_size
        end = start + page_size
        items = summaries[start:end]

        return {
            "items": items,
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages,
        }

    def get_latest_execution_summary(
        self,
        structure_id: int | None = None,
        underlying_asset: str | None = None,
        status: str | None = None,
        reference_date: str | None = None,
    ) -> dict[str, Any]:
        self._validate_summary_filters(
            structure_id=structure_id,
            underlying_asset=underlying_asset,
            status=status,
            reference_date=reference_date,
        )

        summaries = self.list_execution_summaries(
            structure_id=structure_id,
            underlying_asset=underlying_asset,
            status=status,
            reference_date=reference_date,
            descending=True,
        )

        if not summaries:
            raise ValueError("no pricing execution summaries found")

        return summaries[0]

    def get_execution(self, execution_id: int) -> dict[str, Any]:
        if execution_id <= 0:
            raise ValueError("execution_id must be greater than zero")

        execution = self.pricing_executions_repository.get_execution(execution_id)

        if execution is None:
            raise ValueError(f"pricing execution {execution_id} not found")

        return execution

    def get_execution_details(self, execution_id: int) -> dict[str, Any]:
        return self.get_execution(execution_id)
