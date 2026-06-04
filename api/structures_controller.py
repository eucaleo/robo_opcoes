"""
api/structures_controller.py
patch_51 -- Exposição REST do CRUD de estruturas.

Endpoints:
    POST   /structures                 cria estrutura
    GET    /structures                 lista (ativas por padrão)
    GET    /structures/{id}            detalhe + legs
    PATCH  /structures/{id}            atualiza campos (merge)
    DELETE /structures/{id}            arquiva (soft-delete)
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from repositories.structures_repository import StructuresRepository

router = APIRouter(tags=["structures"])

# Repositório compartilhado -- instância única por processo (sem estado mutável)
_repo = StructuresRepository()


# ---------------------------------------------------------------------------
# Schemas
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
    status: str | None = Field(default=None, pattern=r"^(active|inactive|archived)$")


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


class CreateStructureResponse(BaseModel):
    structure_id: int


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_or_404(structure_id: int) -> dict[str, Any]:
    structure = _repo.get_structure(structure_id)
    if structure is None:
        raise HTTPException(status_code=404, detail=f"structure not found: {structure_id}")
    return structure


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post("/structures", response_model=CreateStructureResponse, status_code=201)
def create_structure(request: CreateStructureRequest) -> CreateStructureResponse:
    """Cria uma nova estrutura. Retorna o ID gerado."""
    try:
        structure_id = _repo.create_structure(request.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return CreateStructureResponse(structure_id=structure_id)


@router.get("/structures", response_model=list[StructureSummaryResponse])
def list_structures(
    include_archived: bool = Query(False, description="Inclui estruturas arquivadas"),
) -> list[StructureSummaryResponse]:
    """Lista estruturas. Por padrão exclui arquivadas."""
    rows = _repo.list_structures(include_archived=include_archived)
    return [StructureSummaryResponse(**row) for row in rows]


@router.get("/structures/{structure_id}", response_model=StructureDetailResponse)
def get_structure(structure_id: int) -> StructureDetailResponse:
    """Retorna detalhes completos de uma estrutura, incluindo suas pernas."""
    structure = _get_or_404(structure_id)
    return StructureDetailResponse(**structure)


@router.patch("/structures/{structure_id}", status_code=204)
def update_structure(structure_id: int, request: UpdateStructureRequest) -> None:
    """
    Atualiza campos da estrutura (merge parcial).
    Campos omitidos ou None mantêm o valor atual.
    """
    _get_or_404(structure_id)  # garante 404 antes de tentar update

    # Exclui campos explicitamente None para não sobrescrever com vazio
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
    """
    Arquiva a estrutura (soft-delete).
    A estrutura permanece no banco com status='archived'.
    """
    _get_or_404(structure_id)

    try:
        _repo.archive_structure(structure_id)
    except ValueError as exc:
        message = str(exc)
        status_code = 404 if "not found" in message else 400
        raise HTTPException(status_code=status_code, detail=message) from exc
