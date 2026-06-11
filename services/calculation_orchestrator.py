# services/calculation_orchestrator.py
# alteracao_45: CalculationRequest contract + build_calculation_request
# alteracao_46: _request_to_payoff_dict, run_payoff, run_decision
# alteracao_47: run_full_pipeline, multiplier fix (1.0), run_decision auto-extract
# alteracao_48: CalculationOrchestrator class, build_calculation_request_from_db,
#           run_full_pipeline_from_db

from __future__ import annotations

import logging
from types import SimpleNamespace
from typing import Optional, Dict, Any, List

from domain.calculation_request import (
    CalculationRequest,
    MarketSnapshotInput,
    StructureInput,
    StructureLegInput,
)
from domain.payoff import compute_payoff_from_canonical_input
from domain.decision import compute_decision_from_contract

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Mapeamento legado -> canonico (mantido do alteracao_45)
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
# Funcao legada build_calculation_request (alteracao_45 -- mantida para
# retrocompatibilidade com testes anteriores)
# ---------------------------------------------------------------------------
def build_calculation_request(
    structure_row: dict,
    legs_rows: list,
    snapshot_row: dict,
) -> CalculationRequest:
    """
    Monta um CalculationRequest a partir de dicts vindos do repositorio.
    Mantida para retrocompatibilidade (alteracao_45).
    """
    if not isinstance(legs_rows, list) or len(legs_rows) == 0:
        raise ValueError("legs_rows nao pode ser vazio")

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

    structure = StructureInput(
        structure_id=int(structure_row["id"]),
        underlying_asset=str(structure_row["underlying_asset"]),
        legs=legs,
        name=structure_row.get("name"),
        alias_legacy_aba=structure_row.get("alias_legacy_aba"),
    )

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

    return CalculationRequest(structure=structure, market_snapshot=snapshot)


# ---------------------------------------------------------------------------
# Funcoes legadas de pipeline (alteracao_46/47 -- mantidas para
# retrocompatibilidade com testes anteriores)
# ---------------------------------------------------------------------------
def _request_to_payoff_dict(
    request: CalculationRequest,
    extra_meta: Optional[dict] = None,
) -> dict:
    """alteracao_47: multiplier usa leg.multiplier com fallback 1.0."""
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
            "multiplier":      getattr(leg, "multiplier",  1.0),
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
    """alteracao_47: extrai pl_max/pl_atual/dte_min automaticamente."""
    _pl_max = pl_max
    if _pl_max is None and payoff:
        _pl_max = float(payoff.get("pl_max") or 0.0)
    if _pl_max is None:
        _pl_max = 0.0

    _pl_atual = pl_atual
    if _pl_atual is None and payoff:
        _pl_atual = float(payoff.get("pl_atual") or payoff.get("pl_now") or 0.0)
    if _pl_atual is None:
        _pl_atual = 0.0

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
    """alteracao_47: pipeline completo payoff + decision."""
    payoff_result = run_payoff(
        request,
        low_pct=low_pct,
        high_pct=high_pct,
        step_pct=step_pct,
        extra_meta=extra_meta,
    )
    decision_result = run_decision(request, payoff=payoff_result)

    return {
        "payoff":           payoff_result,
        "decision":         decision_result,
        "structure_id":     request.structure.structure_id,
        "underlying_asset": request.structure.underlying_asset,
    }


# ===========================================================================
# alteracao_48 -- CalculationOrchestrator (classe canonica)
# ===========================================================================

class CalculationOrchestrator:
    """
    Orquestrador canonico de calculo.

    Responsabilidades:
    - Montar CalculationRequest a partir de dicts ja normalizados
    - Executar payoff e decisao sem acessar raw DB diretamente
    - Montar CalculationRequest a partir dos repositorios canonicos (alteracao_48)

    via repositórios injetados.
    """

    def __init__(
        self,
        structures_repository=None,
        market_snapshot_repository=None,
    ):
        self._structures_repo = structures_repository
        self._snapshot_repo   = market_snapshot_repository

    # ------------------------------------------------------------------
    # Construcao manual do CalculationRequest
    # ------------------------------------------------------------------

    def build_calculation_request(
        self,
        structure_dict: Dict[str, Any],
        market_snapshot_dict: Dict[str, Any],
    ) -> CalculationRequest:
        """Monta CalculationRequest a partir de dicts ja normalizados."""
        legs = []
        for i, leg in enumerate(structure_dict.get("legs", [])):
            legs.append(
                StructureLegInput(
                    position_side=_normalize_position_side(
                        leg.get("position_side") or leg.get("cv", "LONG")
                    ),
                    option_type=_normalize_option_type(
                        leg.get("option_type") or leg.get("call_put", "CALL")
                    ),
                    strike=float(leg["strike"]),
                    expiration_date=str(leg["expiration_date"]),
                    quantity=int(leg["quantity"]),
                    symbol=leg.get("symbol"),
                    premium=float(leg["premium"]) if leg.get("premium") is not None else None,
                    multiplier=float(leg.get("multiplier") or 1.0),
                    leg_order=int(leg.get("leg_order") or i),
                    notes=leg.get("notes"),
                )
            )

        structure = StructureInput(
            structure_id=int(structure_dict["structure_id"]),
            name=structure_dict.get("name", ""),
            underlying_asset=str(structure_dict.get("underlying_asset", "")),
            alias_legacy_aba=structure_dict.get("alias_legacy_aba"),
            legs=legs,
        )

        snapshot = MarketSnapshotInput(
            snapshot_id=market_snapshot_dict.get("snapshot_id"),
            snapshot_timestamp=str(market_snapshot_dict.get("snapshot_timestamp", "")),
            underlying_asset=str(market_snapshot_dict.get("underlying_asset", "")),
            spot_price=float(market_snapshot_dict.get("spot_price", 0.0)),
            source=str(market_snapshot_dict.get("source", "rtd")),
            option_quotes=market_snapshot_dict.get("option_quotes"),
            greeks=market_snapshot_dict.get("greeks"),
            volatility_context=market_snapshot_dict.get("volatility_context"),
        )

        return CalculationRequest(structure=structure, market_snapshot=snapshot)

    # ------------------------------------------------------------------
    # Adaptacao interna
    # ------------------------------------------------------------------

    def _request_to_payoff_dict(self, request: CalculationRequest) -> Dict[str, Any]:
        """Converte CalculationRequest para o dict de payoff."""
        legs = []
        for leg in request.structure.legs:
            legs.append({
                "position_side":   leg.position_side,
                "option_type":     leg.option_type,
                "strike":          leg.strike,
                "expiration_date": leg.expiration_date,
                "quantity":        leg.quantity,
                "symbol":          getattr(leg, "symbol",     None),
                "premium":         getattr(leg, "premium",    None),
                "multiplier":      getattr(leg, "multiplier", 1.0),
                "leg_order":       getattr(leg, "leg_order",  0),
                "notes":           getattr(leg, "notes",      None),
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
                "option_quotes":    getattr(request.market_snapshot, "option_quotes", {}),
                "greeks":           getattr(request.market_snapshot, "greeks",        {}),
            },
            "meta": {},
        }

    # ------------------------------------------------------------------
    # run_payoff / run_decision / run_full_pipeline
    # ------------------------------------------------------------------

    def run_payoff(
        self,
        request: CalculationRequest,
        low_pct: float = 0.5,
        high_pct: float = 1.5,
        step_pct: float = 0.01,
    ) -> Dict[str, Any]:
        canonical = self._request_to_payoff_dict(request)
        return compute_payoff_from_canonical_input(
            canonical,
            low_pct=low_pct,
            high_pct=high_pct,
            step_pct=step_pct,
        )

    def run_decision(
        self,
        request: CalculationRequest,
        payoff_result: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if payoff_result is None:
            payoff_result = self.run_payoff(request)

        _pl_max = float(
            payoff_result.get("pl_max") or payoff_result.get("max_profit") or 0.0
        )
        _pl_atual = float(
            payoff_result.get("pl_atual")
            or payoff_result.get("current_pl")
            or payoff_result.get("pl_now")
            or 0.0
        )
        _dte_min = (
            payoff_result.get("dte_min")
            or getattr(request.market_snapshot, "dte_min", None)
            or 0
        )

        contract = SimpleNamespace(
            pl_max=_pl_max,
            pl_atual=_pl_atual,
            dte_min=_dte_min,
        )
        return compute_decision_from_contract(contract, payoff=payoff_result)

    def run_full_pipeline(
        self,
        request: CalculationRequest,
        low_pct: float = 0.5,
        high_pct: float = 1.5,
        step_pct: float = 0.01,
    ) -> Dict[str, Any]:
        """Executa run_payoff -> run_decision em sequencia."""
        payoff_result   = self.run_payoff(request, low_pct=low_pct, high_pct=high_pct, step_pct=step_pct)
        decision_result = self.run_decision(request, payoff_result=payoff_result)

        return {
            "payoff":           payoff_result,
            "decision":         decision_result,
            "structure_id":     request.structure.structure_id,
            "underlying_asset": request.structure.underlying_asset,
        }

    # ------------------------------------------------------------------
    # alteracao_48 -- resolucao via repositorios canonicos
    # ------------------------------------------------------------------

    def build_calculation_request_from_db(
        self,
        structure_id: int,
        snapshot_timestamp: Optional[str] = None,
    ) -> CalculationRequest:
        """
        Monta CalculationRequest buscando dados dos repositorios canonicos.

        Raises:
            RuntimeError: se repositorios nao foram injetados
            ValueError  : se estrutura nao encontrada, arquivada ou sem legs
            ValueError  : se snapshot nao encontrado
        """
        if self._structures_repo is None:
            raise RuntimeError(
                "StructuresRepository nao foi injetado no orquestrador. "
                "Passe structures_repository= no construtor."
            )
        if self._snapshot_repo is None:
            raise RuntimeError(
                "MarketSnapshotRepository nao foi injetado no orquestrador. "
                "Passe market_snapshot_repository= no construtor."
            )

        # 1. Busca estrutura
        structure = self._structures_repo.get_structure(structure_id)
        if structure is None:
            raise ValueError(
                f"Estrutura nao encontrada: structure_id={structure_id}"
            )
        if structure.get("status") == "archived":
            raise ValueError(
                f"Estrutura arquivada nao pode ser recalculada: "
                f"structure_id={structure_id}"
            )

        legs_raw = structure.get("legs", [])
        if not legs_raw:
            raise ValueError(
                f"Estrutura sem legs: structure_id={structure_id}"
            )

        # 2. Busca snapshot
        underlying = structure.get("underlying_asset", "")
        snapshot = self._snapshot_repo.get_snapshot(
            underlying_asset=underlying,
            timestamp=snapshot_timestamp,
        )
        if snapshot is None:
            raise ValueError(
                f"Snapshot nao encontrado para underlying_asset='{underlying}' "
                f"timestamp={snapshot_timestamp!r}"
            )

        # 3. Monta dicts e delega para build_calculation_request
        structure_dict = {
            "structure_id":    structure["id"],
            "name":            structure.get("name", ""),
            "underlying_asset": underlying,
            "alias_legacy_aba": structure.get("alias_legacy_aba"),
            "legs": [
                {
                    "position_side":   leg["position_side"],
                    "option_type":     leg["option_type"],
                    "strike":          leg["strike"],
                    "expiration_date": leg["expiration_date"],
                    "quantity":        leg["quantity"],
                    "symbol":          leg.get("symbol"),
                    "premium":         leg.get("premium"),
                    "multiplier":      leg.get("multiplier", 1.0),
                    "leg_order":       leg.get("leg_order", 0),
                    "notes":           leg.get("notes"),
                }
                for leg in legs_raw
            ],
        }

        market_snapshot_dict = {
            "snapshot_id":        snapshot.get("id"),
            "snapshot_timestamp": snapshot.get("snapshot_timestamp", ""),
            "underlying_asset":   snapshot.get("underlying_asset", underlying),
            "spot_price":         snapshot.get("spot_price", 0.0),
            "source":             snapshot.get("source", "rtd"),
            "option_quotes":      snapshot.get("option_quotes"),
            "greeks":             snapshot.get("greeks"),
            "volatility_context": snapshot.get("volatility_context"),
        }

        return self.build_calculation_request(structure_dict, market_snapshot_dict)

    def run_full_pipeline_from_db(
        self,
        structure_id: int,
        snapshot_timestamp: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Pipeline completo resolvendo estrutura e snapshot pelos repositorios.

        Retorna dict com chaves: structure_id, payoff, decision.
        """
        request        = self.build_calculation_request_from_db(
            structure_id=structure_id,
            snapshot_timestamp=snapshot_timestamp,
        )
        pipeline_result = self.run_full_pipeline(request)

        return {
            "structure_id": structure_id,
            "payoff":       pipeline_result["payoff"],
            "decision":     pipeline_result["decision"],
        }
