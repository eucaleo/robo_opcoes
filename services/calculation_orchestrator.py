"""
patch_45/patch_47 — Orquestrador canonico de calculo.

Responsabilidade:
  - Ler Structure + legs do repositorio canonico
  - Obter MarketSnapshot via selector
  - Normalizar e montar CalculationRequest
  - Passar ao dominio SEM expor raw DB

patch_47: correcoes
  - run_decision extrai pl_max/dte_min automaticamente
  - multiplier usa leg.multiplier (sem hardcode)
  - run_full_pipeline(request) adicionado
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
# Mapeamento legado -> canonico
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
# Builder publico
# ---------------------------------------------------------------------------
def build_calculation_request(
    structure_row: dict,
    legs_rows: list[dict],
    snapshot_row: dict,
) -> CalculationRequest:
    """
    Monta um CalculationRequest a partir de dicts vindos do repositorio.

    Parameters
    ----------
    structure_row : dict com campos de `structures`
    legs_rows     : lista de dicts com campos de `structure_legs`
    snapshot_row  : dict com campos de snapshot de mercado

    Returns
    -------
    CalculationRequest validado e imutavel.

    Raises
    ------
    ValueError  se algum campo obrigatorio estiver ausente ou invalido.
    TypeError   se legs_rows nao for lista de dicts.
    """
    if not isinstance(legs_rows, list) or len(legs_rows) == 0:
        raise ValueError("legs_rows nao pode ser vazio")

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


# ---------------------------------------------------------------------------
# Adaptadores: CalculationRequest -> contrato do dominio
# ---------------------------------------------------------------------------
from types import SimpleNamespace

from domain.payoff import compute_payoff_from_canonical_input
from domain.decision import compute_decision_from_contract


def _request_to_payoff_dict(
    request: CalculationRequest,
    extra_meta: Optional[dict] = None,
) -> dict:
    """
    Traduz CalculationRequest para o dict canonico que
    compute_payoff_from_canonical_input() espera.

    patch_47: multiplier usa leg.multiplier com fallback 1.0 (era hardcode 100).
    """
    legs = []
    for leg in request.structure.legs:
        legs.append({
            "position_side":   leg.position_side,
            "option_type":     leg.option_type,
            "strike":          leg.strike,
            "expiration_date": leg.expiration_date,
            "quantity":        leg.quantity,
            "symbol":          getattr(leg, "symbol",      None),
            "premium":         getattr(leg, "premium",     None),
            "multiplier":      getattr(leg, "multiplier",  1.0),   # patch_47: era 100
            "leg_order":       getattr(leg, "leg_order",   0),
            "notes":           getattr(leg, "notes",       None),
        })

    return {
        "structure": {
            "structure_id":     request.structure.structure_id,
            "underlying_asset": request.structure.underlying_asset,
            "name":             getattr(request.structure, "name", None),
            "legs":             legs,
        },
        "market": {
            "spot_price":       request.market_snapshot.spot_price,
            "underlying_asset": request.market_snapshot.underlying_asset,
            "reference_date":   getattr(request.market_snapshot, "snapshot_timestamp", None),
            "option_quotes":    getattr(request.market_snapshot, "option_quotes",      {}),
            "greeks":           getattr(request.market_snapshot, "greeks",             {}),
        },
        "meta": extra_meta or {},
    }


def run_payoff(
    request: CalculationRequest,
    low_pct: float = 0.5,
    high_pct: float = 1.5,
    step_pct: float = 0.01,
    extra_meta: Optional[dict] = None,
) -> dict:
    """Executa calculo de payoff a partir de um CalculationRequest."""
    canonical = _request_to_payoff_dict(request, extra_meta=extra_meta)
    return compute_payoff_from_canonical_input(
        canonical,
        low_pct=low_pct,
        high_pct=high_pct,
        step_pct=step_pct,
    )


def run_decision(
    request: CalculationRequest,
    payoff: Optional[dict] = None,
    pl_atual: Optional[float] = None,
    pl_max: Optional[float] = None,
    dte_min: Optional[int] = None,
) -> dict:
    """
    Executa calculo de decisao a partir de um CalculationRequest.

    patch_47:
      - pl_max extraido de payoff["pl_max"] quando nao fornecido explicitamente
      - pl_atual extraido de payoff["pl_atual"] ou interpolado quando disponivel
      - dte_min extraido do request.market_snapshot quando nao fornecido
      - Elimina risco de HOLD silencioso por valores zerados
    """
    # Extrair pl_max do payoff calculado, se disponivel
    _pl_max = pl_max
    if _pl_max is None and payoff:
        _pl_max = float(payoff.get("pl_max") or 0.0)
    if _pl_max is None:
        _pl_max = 0.0

    # Extrair pl_atual do payoff, se disponivel
    _pl_atual = pl_atual
    if _pl_atual is None and payoff:
        _pl_atual = float(payoff.get("pl_atual") or payoff.get("pl_now") or 0.0)
    if _pl_atual is None:
        _pl_atual = 0.0

    # Extrair dte_min do snapshot quando nao fornecido
    _dte_min = dte_min
    if _dte_min is None:
        _dte_min = getattr(request.market_snapshot, "dte_min", None)

    contract = SimpleNamespace(
        pl_max=_pl_max,
        pl_atual=_pl_atual,
        dte_min=_dte_min,
    )
    return compute_decision_from_contract(contract, payoff=payoff)


def run_full_pipeline(
    request: CalculationRequest,
    low_pct: float = 0.5,
    high_pct: float = 1.5,
    step_pct: float = 0.01,
    extra_meta: Optional[dict] = None,
) -> dict:
    """
    Executa payoff + decision em sequencia a partir de um CalculationRequest.

    patch_47: entrada unica para o pipeline completo.
    Garante que run_decision recebe o payoff real calculado por run_payoff,
    eliminando dependencia de passagem manual de pl_max/pl_atual.

    Returns
    -------
    dict com chaves:
      - "payoff"   : resultado completo de run_payoff
      - "decision" : resultado completo de run_decision
      - "structure_id"     : int
      - "underlying_asset" : str
    """
    payoff_result = run_payoff(
        request,
        low_pct=low_pct,
        high_pct=high_pct,
        step_pct=step_pct,
        extra_meta=extra_meta,
    )

    decision_result = run_decision(
        request,
        payoff=payoff_result,
    )

    return {
        "payoff":           payoff_result,
        "decision":         decision_result,
        "structure_id":     request.structure.structure_id,
        "underlying_asset": request.structure.underlying_asset,
    }
