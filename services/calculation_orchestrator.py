"""
patch_45 — Orquestrador canônico de cálculo.

Responsabilidade:
  - Ler Structure + legs do repositório canônico
  - Obter MarketSnapshot via selector
  - Normalizar e montar CalculationRequest
  - Passar ao domínio SEM expor raw DB

O domínio não sabe de onde vieram os dados.
"""
from __future__ import annotations

import logging
from typing import Optional

from domain.calculation_request import (
    CalculationRequest,
    MarketSnapshotInput,
    StructureInput,
    StructureLegInput,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Mapeamento legado → canônico
# ---------------------------------------------------------------------------
_CV_TO_SIDE = {"C": "LONG", "V": "SHORT", "LONG": "LONG", "SHORT": "SHORT"}
_CP_NORM    = {"CALL": "CALL", "PUT": "PUT", "C": "CALL", "P": "PUT"}


def _normalize_position_side(raw: str) -> str:
    v = str(raw).strip().upper()
    if v not in _CV_TO_SIDE:
        raise ValueError(f"position_side desconhecido: {raw!r}")
    return _CV_TO_SIDE[v]


def _normalize_option_type(raw: str) -> str:
    v = str(raw).strip().upper()
    if v not in _CP_NORM:
        raise ValueError(f"option_type desconhecido: {raw!r}")
    return _CP_NORM[v]


# ---------------------------------------------------------------------------
# Builder público
# ---------------------------------------------------------------------------
def build_calculation_request(
    structure_row: dict,
    legs_rows: list[dict],
    snapshot_row: dict,
) -> CalculationRequest:
    """
    Monta um CalculationRequest a partir de dicts vindos do repositório.

    Parameters
    ----------
    structure_row : dict com campos de `structures`
    legs_rows     : lista de dicts com campos de `structure_legs`
    snapshot_row  : dict com campos de snapshot de mercado

    Returns
    -------
    CalculationRequest validado e imutável.

    Raises
    ------
    ValueError  se algum campo obrigatório estiver ausente ou inválido.
    TypeError   se legs_rows não for lista de dicts.
    """
    if not isinstance(legs_rows, list) or len(legs_rows) == 0:
        raise ValueError("legs_rows não pode ser vazio")

    # ---- Legs ----
    legs = []
    for i, row in enumerate(legs_rows):
        try:
            leg = StructureLegInput(
                position_side=_normalize_position_side(
                    row.get("position_side") or row.get("cv", "")
                ),
                option_type=_normalize_option_type(
                    row.get("option_type") or row.get("call_put", "")
                ),
                strike=float(row["strike"]),
                expiration_date=str(row["expiration_date"]),
                quantity=int(row["quantity"]),
                symbol=row.get("symbol"),
                premium=float(row["premium"]) if row.get("premium") is not None else None,
                multiplier=float(row.get("multiplier") or 1.0),
                leg_order=int(row.get("leg_order") or i),
                notes=row.get("notes"),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"Erro ao montar leg[{i}]: {exc}") from exc
        legs.append(leg)

    # ---- Structure ----
    structure = StructureInput(
        structure_id=int(structure_row["id"]),
        underlying_asset=str(structure_row["underlying_asset"]),
        legs=legs,
        name=structure_row.get("name"),
        alias_legacy_aba=structure_row.get("alias_legacy_aba"),
    )

    # ---- Snapshot ----
    snapshot = MarketSnapshotInput(
        snapshot_timestamp=str(snapshot_row["snapshot_timestamp"]),
        underlying_asset=str(snapshot_row["underlying_asset"]),
        spot_price=float(snapshot_row["spot_price"]),
        source=str(snapshot_row.get("source", "rtd")),
        snapshot_id=snapshot_row.get("snapshot_id") or snapshot_row.get("id"),
        option_quotes=snapshot_row.get("option_quotes"),
        greeks=snapshot_row.get("greeks"),
        volatility_context=snapshot_row.get("volatility_context"),
    )

    logger.debug(
        "CalculationRequest montado: structure_id=%s underlying=%s legs=%d",
        structure.structure_id,
        structure.underlying_asset,
        len(legs),
    )
    return CalculationRequest(structure=structure, market_snapshot=snapshot)
