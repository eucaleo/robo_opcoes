# api/structures_controller.py
"""
alteracao_51 -- Exposição REST do CRUD de estruturas.
alteracao_63 -- Endpoints de legs:
    POST   /structures/{id}/legs            adiciona uma perna
    PUT    /structures/{id}/legs            substitui todas as pernas (atômico)
    DELETE /structures/{id}/legs/{leg_id}   remove perna individual

    Fix: leg_order >= 0 (corrigido em _validate_leg do repositório).
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from repositories.structures_repository import StructuresRepository

router = APIRouter(tags=["structures"])

_repo: StructuresRepository = StructuresRepository()


# ---------------------------------------------------------------------------
# Schemas de entrada — estrutura
# ---------------------------------------------------------------------------

class CreateStructureRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    underlying_asset: str = Field(..., min_length=1, max_length=50)
    alias_legacy_aba: str | None = Field(default=None, max_length=100)
    notes: str | None = None


class UpdateStructureRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    underlying_asset: str | None = Field(default=None, min_length=1, max_length=50)
    alias_legacy_aba: str | None = Field(default=None, max_length=100)
    notes: str | None = None
    status: str | None = Field(default=None, pattern=r"^(active|archived)$")


# ---------------------------------------------------------------------------
# Schemas de entrada — legs  (alteracao_63)
# ---------------------------------------------------------------------------

class LegRequest(BaseModel):
    """Schema compartilhado por AddLegRequest e ReplaceLegRequest."""
    position_side: str   = Field(..., pattern=r"^(LONG|SHORT)$")
    option_type: str     = Field(..., pattern=r"^(CALL|PUT)$")
    strike: float        = Field(..., gt=0)
    expiration_date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    quantity: int        = Field(..., gt=0)
    multiplier: float    = Field(default=1.0, gt=0)
    # alteracao_63 fix: leg_order >= 0
    leg_order: int       = Field(default=0, ge=0)
    symbol: str | None   = None
    premium: float | None = None
    notes: str | None    = None


class ReplaceLegRequest(BaseModel):
    """Payload para PUT /structures/{id}/legs — lista de legs completa."""
    legs: list[LegRequest] = Field(..., min_length=1)


# ---------------------------------------------------------------------------
# Schemas de resposta
# ---------------------------------------------------------------------------

class CreateStructureResponse(BaseModel):
    structure_id: int


class StructureSummaryResponse(BaseModel):
    id: int
    name: str
    underlying_asset: str
    alias_legacy_aba: str | None
    status: str
    notes: str | None
    created_at: str
    updated_at: str


class StructureDetailResponse(StructureSummaryResponse):
    legs: list[dict[str, Any]]


class AddLegResponse(BaseModel):
    leg_id: int


# ---------------------------------------------------------------------------
# Helpers internos
# ---------------------------------------------------------------------------

def _get_or_404(structure_id: int) -> dict[str, Any]:
    structure = _repo.get_structure(structure_id)
    if structure is None:
        raise HTTPException(
            status_code=404,
            detail=f"structure not found: {structure_id}",
        )
    return structure


# ---------------------------------------------------------------------------
# Endpoints — estrutura (alteracao_51, inalterados)
# ---------------------------------------------------------------------------

@router.post("/structures", response_model=CreateStructureResponse, status_code=201)
def create_structure(request: CreateStructureRequest) -> CreateStructureResponse:
    try:
        structure_id = _repo.create_structure(request.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return CreateStructureResponse(structure_id=structure_id)


@router.get("/structures", response_model=list[StructureSummaryResponse])
def list_structures(
    include_archived: bool = Query(False, description="Inclui estruturas arquivadas"),
) -> list[StructureSummaryResponse]:
    rows = _repo.list_structures(include_archived=include_archived)
    return [StructureSummaryResponse(**row) for row in rows]


@router.get("/structures/{structure_id}", response_model=StructureDetailResponse)
def get_structure(structure_id: int) -> StructureDetailResponse:
    structure = _get_or_404(structure_id)
    return StructureDetailResponse(**structure)


@router.patch("/structures/{structure_id}", status_code=204)
def update_structure(structure_id: int, request: UpdateStructureRequest) -> None:
    _get_or_404(structure_id)

    data = {k: v for k, v in request.model_dump().items() if v is not None}
    if not data:
        raise HTTPException(status_code=400, detail="nenhum campo fornecido para atualização")

    try:
        _repo.update_structure(structure_id, data)
    except ValueError as exc:
        message = str(exc)
        status_code = 404 if "not found" in message else 400
        raise HTTPException(status_code=status_code, detail=message) from exc


@router.delete("/structures/{structure_id}", status_code=204)
def archive_structure(structure_id: int) -> None:
    _get_or_404(structure_id)
    try:
        _repo.archive_structure(structure_id)
    except ValueError as exc:
        message = str(exc)
        status_code = 404 if "not found" in message else 400
        raise HTTPException(status_code=status_code, detail=message) from exc


# ---------------------------------------------------------------------------
# Endpoints — legs  (alteracao_63)
# ---------------------------------------------------------------------------

@router.post(
    "/structures/{structure_id}/legs",
    response_model=AddLegResponse,
    status_code=201,
)
def add_leg(structure_id: int, request: LegRequest) -> AddLegResponse:
    """
    Adiciona uma perna à estrutura.
    Retorna o leg_id gerado.
    """
    _get_or_404(structure_id)

    try:
        leg_id = _repo.add_leg(structure_id, request.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return AddLegResponse(leg_id=leg_id)


@router.put("/structures/{structure_id}/legs", status_code=204)
def replace_legs(structure_id: int, request: ReplaceLegRequest) -> None:
    """
    Substitui TODAS as pernas da estrutura atomicamente.
    A lista enviada substitui completamente o conjunto existente.
    """
    _get_or_404(structure_id)

    try:
        _repo.replace_legs(
            structure_id,
            [leg.model_dump() for leg in request.legs],
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.delete("/structures/{structure_id}/legs/{leg_id}", status_code=204)
def remove_leg(structure_id: int, leg_id: int) -> None:
    """
    Remove uma perna específica da estrutura.
    Retorna 404 se a estrutura ou a leg não forem encontradas.
    """
    _get_or_404(structure_id)

    conn = _repo._connect()
    try:
        row = conn.execute(
            "SELECT id FROM structure_legs WHERE id=? AND structure_id=?",
            (leg_id, structure_id),
        ).fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail=f"leg not found: {leg_id} in structure {structure_id}",
            )

        from datetime import datetime, timezone
        now = datetime.now(timezone.utc).isoformat()

        conn.execute(
            "DELETE FROM structure_legs WHERE id=?",
            (leg_id,),
        )
        conn.execute(
            "UPDATE structures SET updated_at=? WHERE id=?",
            (now, structure_id),
        )
        conn.commit()
    except HTTPException:
        raise
    except Exception as exc:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Endpoints — eventos operacionais
# ---------------------------------------------------------------------------

from datetime import datetime as _StructureEventsDateTime
from typing import Any as _StructureEventsAny

from fastapi import HTTPException as _StructureEventsHTTPException
from pydantic import BaseModel as _StructureEventsBaseModel

from services.structure_events_service import (
    StructureEventsService as _StructureEventsService,
)


_events_service = _StructureEventsService()


_STRUCTURE_EVENT_TYPES = {
    "opening",
    "adjustment",
    "rollover",
    "partial_close",
    "full_close",
    "manual_close",
    "note",
    "assignment",
    "exercise",
    "expiration",
}

_STRUCTURE_EVENT_STATUSES = {
    "registered",
    "confirmed",
    "cancelled",
}

_STRUCTURE_EVENT_SOURCES = {
    "manual",
    "system",
    "import",
    "broker",
}


class RecordStructureEventRequest(_StructureEventsBaseModel):
    event_type: str
    event_date: str
    leg_id: int | None = None
    event_status: str = "registered"
    quantity: int | None = None
    price: float | None = None
    symbol: str | None = None
    source: str = "manual"
    notes: str | None = None
    metadata: dict[str, _StructureEventsAny] | list[_StructureEventsAny] | None = None


class CancelStructureEventRequest(_StructureEventsBaseModel):
    notes: str | None = None


def _structure_events_model_dump(model: _StructureEventsBaseModel) -> dict[str, _StructureEventsAny]:
    if hasattr(model, "model_dump"):
        return model.model_dump()
    return model.dict()


def _structure_events_result_payload(result: _StructureEventsAny) -> dict[str, _StructureEventsAny]:
    if isinstance(result, dict):
        return result
    return {"event_id": result}


def _structure_events_value_error_to_http(exc: ValueError) -> _StructureEventsHTTPException:
    message = str(exc)
    status_code = 404 if "not found" in message else 400
    return _StructureEventsHTTPException(status_code=status_code, detail=message)


def _ensure_structure_exists_for_events(structure_id: int) -> None:
    structure = _repo.get_structure(structure_id)
    if structure is None:
        raise _StructureEventsHTTPException(
            status_code=404,
            detail=f"structure not found: {structure_id}",
        )


def _validate_record_structure_event_request(
    request: RecordStructureEventRequest,
) -> None:
    if request.event_type not in _STRUCTURE_EVENT_TYPES:
        raise _StructureEventsHTTPException(
            status_code=422,
            detail="invalid event_type",
        )

    try:
        _StructureEventsDateTime.strptime(request.event_date, "%Y-%m-%d")
    except ValueError as exc:
        raise _StructureEventsHTTPException(
            status_code=422,
            detail="event_date must be in YYYY-MM-DD format",
        ) from exc

    if request.leg_id is not None and request.leg_id <= 0:
        raise _StructureEventsHTTPException(
            status_code=422,
            detail="leg_id must be greater than zero",
        )

    if request.event_status not in _STRUCTURE_EVENT_STATUSES:
        raise _StructureEventsHTTPException(
            status_code=422,
            detail="invalid event_status",
        )

    if request.quantity is not None and request.quantity < 0:
        raise _StructureEventsHTTPException(
            status_code=422,
            detail="quantity must be greater than or equal to zero",
        )

    if request.price is not None and request.price < 0:
        raise _StructureEventsHTTPException(
            status_code=422,
            detail="price must be greater than or equal to zero",
        )

    if request.source not in _STRUCTURE_EVENT_SOURCES:
        raise _StructureEventsHTTPException(
            status_code=422,
            detail="invalid source",
        )


@router.post(
    "/structures/{structure_id}/events",
    response_model=dict[str, _StructureEventsAny],
    status_code=201,
)
def record_structure_event(
    structure_id: int,
    request: RecordStructureEventRequest,
) -> dict[str, _StructureEventsAny]:
    _ensure_structure_exists_for_events(structure_id)
    _validate_record_structure_event_request(request)

    try:
        result = _events_service.record_event(
            structure_id=structure_id,
            **_structure_events_model_dump(request),
        )
    except ValueError as exc:
        raise _structure_events_value_error_to_http(exc) from exc

    return _structure_events_result_payload(result)


@router.get(
    "/structures/{structure_id}/events",
    response_model=list[dict[str, _StructureEventsAny]],
)
def list_structure_events(
    structure_id: int,
    include_cancelled: bool = False,
) -> list[dict[str, _StructureEventsAny]]:
    _ensure_structure_exists_for_events(structure_id)

    try:
        return _events_service.list_events_for_structure(
            structure_id,
            include_cancelled=include_cancelled,
        )
    except ValueError as exc:
        raise _structure_events_value_error_to_http(exc) from exc


@router.get(
    "/structure-events",
    response_model=list[dict[str, _StructureEventsAny]],
)
def list_events(
    structure_id: int | None = None,
    event_type: str | None = None,
    event_status: str | None = None,
    include_cancelled: bool = False,
    limit: int = 100,
    offset: int = 0,
) -> list[dict[str, _StructureEventsAny]]:
    if structure_id is not None and structure_id <= 0:
        raise _StructureEventsHTTPException(
            status_code=422,
            detail="structure_id must be greater than zero",
        )

    if limit <= 0:
        raise _StructureEventsHTTPException(
            status_code=422,
            detail="limit must be greater than zero",
        )

    if offset < 0:
        raise _StructureEventsHTTPException(
            status_code=422,
            detail="offset must be greater than or equal to zero",
        )

    try:
        return _events_service.list_events(
            structure_id=structure_id,
            event_type=event_type,
            event_status=event_status,
            include_cancelled=include_cancelled,
            limit=limit,
            offset=offset,
        )
    except ValueError as exc:
        raise _structure_events_value_error_to_http(exc) from exc


@router.get(
    "/structure-events/{event_id}",
    response_model=dict[str, _StructureEventsAny],
)
def get_structure_event(event_id: int) -> dict[str, _StructureEventsAny]:
    try:
        event = _events_service.get_event(event_id)
    except ValueError as exc:
        raise _structure_events_value_error_to_http(exc) from exc

    if event is None:
        raise _StructureEventsHTTPException(
            status_code=404,
            detail=f"event not found: {event_id}",
        )

    return event


@router.post(
    "/structure-events/{event_id}/cancel",
    response_model=dict[str, _StructureEventsAny],
)
def cancel_structure_event(
    event_id: int,
    request: CancelStructureEventRequest,
) -> dict[str, _StructureEventsAny]:
    try:
        result = _events_service.cancel_event(event_id, notes=request.notes)
    except ValueError as exc:
        raise _structure_events_value_error_to_http(exc) from exc

    return _structure_events_result_payload(result)

