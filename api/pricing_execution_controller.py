from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from services.pricing_execution_app_service import PricingExecutionAppService

router = APIRouter(tags=["pricing-executions"])
service = PricingExecutionAppService()


class CreatePricingExecutionRequest(BaseModel):
    structure_id: int
    reference_date: str


@router.post("/pricing-executions")
def create_pricing_execution(request: CreatePricingExecutionRequest):
    try:
        return service.execute_pricing(
            structure_id=request.structure_id,
            reference_date=request.reference_date,
        )
    except ValueError as exc:
        message = str(exc)
        status_code = 404 if "not found" in message else 400
        raise HTTPException(status_code=status_code, detail=message) from exc


@router.get("/pricing-executions")
def list_pricing_executions(
    structure_id: int | None = None,
    underlying_asset: str | None = None,
    status: str | None = None,
    reference_date: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
):
    try:
        return service.paginate_execution_summaries(
            structure_id=structure_id,
            underlying_asset=underlying_asset,
            status=status,
            reference_date=reference_date,
            page=page,
            page_size=page_size,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/pricing-executions/latest")
def get_latest_pricing_execution(
    structure_id: int | None = None,
    underlying_asset: str | None = None,
    status: str | None = None,
    reference_date: str | None = None,
):
    try:
        return service.get_latest_execution_summary(
            structure_id=structure_id,
            underlying_asset=underlying_asset,
            status=status,
            reference_date=reference_date,
        )
    except ValueError as exc:
        message = str(exc)
        status_code = (
            404
            if "not found" in message
            or "no pricing execution summaries found" in message
            else 400
        )
        raise HTTPException(status_code=status_code, detail=message) from exc


@router.get("/pricing-executions/{execution_id}")
def get_pricing_execution(execution_id: int):
    try:
        return service.get_execution(execution_id)
    except ValueError as exc:
        message = str(exc)
        status_code = 404 if "not found" in message else 400
        raise HTTPException(status_code=status_code, detail=message) from exc
