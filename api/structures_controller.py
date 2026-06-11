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
