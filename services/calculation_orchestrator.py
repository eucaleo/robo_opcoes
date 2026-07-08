# services/calculation_orchestrator.py

from __future__ import annotations

import logging
from types import SimpleNamespace
from typing import Any, Dict, List, Optional

from domain.calculation_request import (
    CalculationRequest,
    MarketSnapshotInput,
    StructureInput,
    StructureLegInput,
)
from domain.decision import compute_decision_from_contract
from domain.payoff import compute_payoff_from_canonical_input
from domain.position_side import to_pricing_engine_side

logger = logging.getLogger(__name__)


_CP_NORM = {
    "CALL": "CALL",
    "PUT": "PUT",
    "C": "CALL",
    "P": "PUT",
}


def _normalize_position_side(raw: str) -> str:
    try:
        return to_pricing_engine_side(raw)
    except ValueError as exc:
        raise ValueError(f"position_side desconhecido: {raw!r}") from exc


def _normalize_option_type(raw: str) -> str:
    value = str(raw).strip().upper()
    if value not in _CP_NORM:
        raise ValueError(f"option_type desconhecido: {raw!r}")
    return _CP_NORM[value]


class CalculationOrchestrator:
    """
    Orquestrador canônico de cálculo.

    Responsabilidades:
    - montar CalculationRequest a partir de dicts normalizados;
    - adaptar CalculationRequest para o contrato de payoff;
    - executar payoff;
    - executar decisão;
    - executar pipeline completo;
    - resolver estrutura/snapshot via repositórios injetados.
    """

    def __init__(
        self,
        structures_repository=None,
        market_snapshot_repository=None,
    ):
        self._structures_repo = structures_repository
        self._snapshot_repo = market_snapshot_repository

    def build_calculation_request(
        self,
        structure_dict: Dict[str, Any],
        market_snapshot_dict: Dict[str, Any],
    ) -> CalculationRequest:
        """
        Monta CalculationRequest a partir de dicts normalizados.

        Espera structure_dict com:
        - structure_id
        - underlying_asset
        - legs

        Espera market_snapshot_dict com:
        - snapshot_timestamp
        - underlying_asset
        - spot_price
        """
        legs_rows = structure_dict.get("legs", [])
        if not isinstance(legs_rows, list) or not legs_rows:
            raise ValueError("structure_dict['legs'] nao pode ser vazio")

        legs: List[StructureLegInput] = []

        for index, leg_dict in enumerate(legs_rows):
            try:
                legs.append(
                    StructureLegInput(
                        position_side=_normalize_position_side(
                            leg_dict.get("position_side") or leg_dict.get("cv", "")
                        ),
                        option_type=_normalize_option_type(
                            leg_dict.get("option_type")
                            or leg_dict.get("call_put", "CALL")
                        ),
                        strike=float(leg_dict["strike"]),
                        expiration_date=str(leg_dict["expiration_date"]),
                        quantity=int(leg_dict["quantity"]),
                        symbol=leg_dict.get("symbol"),
                        premium=(
                            float(leg_dict["premium"])
                            if leg_dict.get("premium") is not None
                            else None
                        ),
                        multiplier=float(leg_dict.get("multiplier") or 1.0),
                        leg_order=int(leg_dict.get("leg_order") or index),
                        notes=leg_dict.get("notes"),
                    )
                )
            except (KeyError, TypeError, ValueError) as exc:
                raise ValueError(f"Erro ao montar leg[{index}]: {exc}") from exc

        structure = StructureInput(
            structure_id=int(structure_dict["structure_id"]),
            underlying_asset=str(structure_dict["underlying_asset"]),
            legs=legs,
            name=structure_dict.get("name"),
            alias_legacy_aba=structure_dict.get("alias_legacy_aba"),
        )

        snapshot = MarketSnapshotInput(
            snapshot_timestamp=str(market_snapshot_dict["snapshot_timestamp"]),
            underlying_asset=str(market_snapshot_dict["underlying_asset"]),
            spot_price=float(market_snapshot_dict["spot_price"]),
            source=str(market_snapshot_dict.get("source", "rtd")),
            snapshot_id=(
                market_snapshot_dict.get("snapshot_id")
                or market_snapshot_dict.get("id")
            ),
            option_quotes=market_snapshot_dict.get("option_quotes"),
            greeks=market_snapshot_dict.get("greeks"),
            volatility_context=market_snapshot_dict.get("volatility_context"),
        )

        return CalculationRequest(
            structure=structure,
            market_snapshot=snapshot,
        )

    def _request_to_payoff_dict(
        self,
        request: CalculationRequest,
        extra_meta: Optional[dict] = None,
    ) -> Dict[str, Any]:
        """
        Converte CalculationRequest para o dict canônico esperado pelo domínio de payoff.
        """
        legs = []

        for leg in request.structure.legs:
            legs.append(
                {
                    "position_side": leg.position_side,
                    "option_type": leg.option_type,
                    "strike": leg.strike,
                    "expiration_date": leg.expiration_date,
                    "quantity": leg.quantity,
                    "symbol": getattr(leg, "symbol", None),
                    "premium": getattr(leg, "premium", None),
                    "multiplier": getattr(leg, "multiplier", 1.0),
                    "leg_order": getattr(leg, "leg_order", 0),
                    "notes": getattr(leg, "notes", None),
                }
            )

        return {
            "structure": {
                "structure_id": request.structure.structure_id,
                "underlying_asset": request.structure.underlying_asset,
                "name": getattr(request.structure, "name", None),
                "legs": legs,
            },
            "market": {
                "spot_price": request.market_snapshot.spot_price,
                "underlying_asset": request.market_snapshot.underlying_asset,
                "reference_date": getattr(
                    request.market_snapshot,
                    "snapshot_timestamp",
                    None,
                ),
                "option_quotes": getattr(
                    request.market_snapshot,
                    "option_quotes",
                    {},
                ),
                "greeks": getattr(
                    request.market_snapshot,
                    "greeks",
                    {},
                ),
            },
            "meta": extra_meta or {},
        }

    def run_payoff(
        self,
        request: CalculationRequest,
        low_pct: float = 0.5,
        high_pct: float = 1.5,
        step_pct: float = 0.01,
        extra_meta: Optional[dict] = None,
    ) -> Dict[str, Any]:
        """
        Executa cálculo de payoff a partir de um CalculationRequest.
        """
        canonical = self._request_to_payoff_dict(
            request,
            extra_meta=extra_meta,
        )

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
        *,
        payoff: Optional[Dict[str, Any]] = None,
        pl_atual: Optional[float] = None,
        pl_max: Optional[float] = None,
        dte_min: Optional[int] = None,
        auto_run_payoff: bool = True,
    ) -> Dict[str, Any]:
        """
        Executa decisão a partir do request e, opcionalmente, do resultado de payoff.

        Aceita o alias keyword-only `payoff` para preservar compatibilidade
        com chamadas anteriores.

        Quando auto_run_payoff=True, calcula payoff se nenhum resultado for informado.
        Wrappers legados usam auto_run_payoff=False para preservar contrato anterior.
        """
        if payoff_result is None:
            payoff_result = payoff

        if payoff_result is None and auto_run_payoff:
            payoff_result = self.run_payoff(request)

        resolved_pl_max = pl_max
        if resolved_pl_max is None and payoff_result:
            resolved_pl_max = float(
                payoff_result.get("pl_max")
                or payoff_result.get("max_profit")
                or 0.0
            )
        if resolved_pl_max is None:
            resolved_pl_max = 0.0

        resolved_pl_atual = pl_atual
        if resolved_pl_atual is None and payoff_result:
            resolved_pl_atual = float(
                payoff_result.get("pl_atual")
                or payoff_result.get("current_pl")
                or payoff_result.get("pl_now")
                or 0.0
            )
        if resolved_pl_atual is None:
            resolved_pl_atual = 0.0

        resolved_dte_min = dte_min
        if resolved_dte_min is None and payoff_result:
            resolved_dte_min = payoff_result.get("dte_min")
        if resolved_dte_min is None:
            resolved_dte_min = getattr(request.market_snapshot, "dte_min", None)

        contract = SimpleNamespace(
            pl_max=resolved_pl_max,
            pl_atual=resolved_pl_atual,
            dte_min=resolved_dte_min,
        )

        return compute_decision_from_contract(
            contract,
            payoff=payoff_result,
        )

    def run_full_pipeline(
        self,
        request: CalculationRequest,
        low_pct: float = 0.5,
        high_pct: float = 1.5,
        step_pct: float = 0.01,
        extra_meta: Optional[dict] = None,
    ) -> Dict[str, Any]:
        """
        Executa pipeline completo: payoff -> decisão.
        """
        payoff_result = self.run_payoff(
            request,
            low_pct=low_pct,
            high_pct=high_pct,
            step_pct=step_pct,
            extra_meta=extra_meta,
        )

        decision_result = self.run_decision(
            request,
            payoff_result=payoff_result,
        )

        return {
            "payoff": payoff_result,
            "decision": decision_result,
            "structure_id": request.structure.structure_id,
            "underlying_asset": request.structure.underlying_asset,
        }

    def build_calculation_request_from_db(
        self,
        structure_id: int,
        snapshot_timestamp: Optional[str] = None,
    ) -> CalculationRequest:
        """
        Monta CalculationRequest buscando estrutura e snapshot nos repositórios injetados.
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

        structure = self._structures_repo.get_structure(structure_id)
        if structure is None:
            raise ValueError(
                f"Estrutura nao encontrada: structure_id={structure_id}"
            )

        if structure.get("status") == "archived":
            raise ValueError(
                "Estrutura arquivada nao pode ser recalculada: "
                f"structure_id={structure_id}"
            )

        legs_raw = structure.get("legs", [])
        if not legs_raw:
            raise ValueError(
                f"Estrutura sem legs: structure_id={structure_id}"
            )

        underlying = structure.get("underlying_asset", "")

        snapshot = self._snapshot_repo.get_snapshot(
            underlying_asset=underlying,
            timestamp=snapshot_timestamp,
        )
        if snapshot is None:
            raise ValueError(
                f"Snapshot nao encontrado para underlying_asset={underlying!r} "
                f"timestamp={snapshot_timestamp!r}"
            )

        structure_dict = {
            "structure_id": structure["id"],
            "name": structure.get("name", ""),
            "underlying_asset": underlying,
            "alias_legacy_aba": structure.get("alias_legacy_aba"),
            "legs": [
                {
                    "position_side": leg["position_side"],
                    "option_type": leg["option_type"],
                    "strike": leg["strike"],
                    "expiration_date": leg["expiration_date"],
                    "quantity": leg["quantity"],
                    "symbol": leg.get("symbol"),
                    "premium": leg.get("premium"),
                    "multiplier": leg.get("multiplier", 1.0),
                    "leg_order": leg.get("leg_order", 0),
                    "notes": leg.get("notes"),
                }
                for leg in legs_raw
            ],
        }

        market_snapshot_dict = {
            "snapshot_id": snapshot.get("id"),
            "snapshot_timestamp": snapshot.get("snapshot_timestamp", ""),
            "underlying_asset": snapshot.get("underlying_asset", underlying),
            "spot_price": snapshot.get("spot_price", 0.0),
            "source": snapshot.get("source", "rtd"),
            "option_quotes": snapshot.get("option_quotes"),
            "greeks": snapshot.get("greeks"),
            "volatility_context": snapshot.get("volatility_context"),
        }

        return self.build_calculation_request(
            structure_dict,
            market_snapshot_dict,
        )

    def run_full_pipeline_from_db(
        self,
        structure_id: int,
        snapshot_timestamp: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Resolve estrutura/snapshot via repositórios e executa pipeline completo.
        """
        request = self.build_calculation_request_from_db(
            structure_id=structure_id,
            snapshot_timestamp=snapshot_timestamp,
        )

        pipeline_result = self.run_full_pipeline(request)

        return {
            "structure_id": structure_id,
            "payoff": pipeline_result["payoff"],
            "decision": pipeline_result["decision"],
        }


# ---------------------------------------------------------------------------
# Wrappers de compatibilidade
# ---------------------------------------------------------------------------

def build_calculation_request(
    structure_row: dict,
    legs_rows: list,
    snapshot_row: dict,
) -> CalculationRequest:
    """
    Wrapper de compatibilidade.

    A implementação canônica fica em CalculationOrchestrator.build_calculation_request().
    """
    if not isinstance(legs_rows, list) or not legs_rows:
        raise ValueError("legs_rows nao pode ser vazio")

    structure_dict = {
        "structure_id": structure_row.get("structure_id", structure_row.get("id")),
        "underlying_asset": structure_row["underlying_asset"],
        "name": structure_row.get("name"),
        "alias_legacy_aba": structure_row.get("alias_legacy_aba"),
        "legs": legs_rows,
    }

    market_snapshot_dict = {
        "snapshot_id": snapshot_row.get("snapshot_id") or snapshot_row.get("id"),
        "snapshot_timestamp": snapshot_row["snapshot_timestamp"],
        "underlying_asset": snapshot_row["underlying_asset"],
        "spot_price": snapshot_row["spot_price"],
        "source": snapshot_row.get("source", "rtd"),
        "option_quotes": snapshot_row.get("option_quotes"),
        "greeks": snapshot_row.get("greeks"),
        "volatility_context": snapshot_row.get("volatility_context"),
    }

    return CalculationOrchestrator().build_calculation_request(
        structure_dict,
        market_snapshot_dict,
    )


def _request_to_payoff_dict(
    request: CalculationRequest,
    extra_meta: Optional[dict] = None,
) -> dict:
    """
    Wrapper de compatibilidade.

    A implementação canônica fica em CalculationOrchestrator._request_to_payoff_dict().
    """
    return CalculationOrchestrator()._request_to_payoff_dict(
        request,
        extra_meta=extra_meta,
    )


def run_payoff(
    request: CalculationRequest,
    low_pct: float = 0.5,
    high_pct: float = 1.5,
    step_pct: float = 0.01,
    extra_meta: Optional[dict] = None,
) -> dict:
    """
    Wrapper de compatibilidade.

    A implementação canônica fica em CalculationOrchestrator.run_payoff().
    """
    return CalculationOrchestrator().run_payoff(
        request,
        low_pct=low_pct,
        high_pct=high_pct,
        step_pct=step_pct,
        extra_meta=extra_meta,
    )


def run_decision(
    request: CalculationRequest,
    payoff: Optional[dict] = None,
    pl_atual: Optional[float] = None,
    pl_max: Optional[float] = None,
    dte_min: Optional[int] = None,
) -> dict:
    """
    Wrapper de compatibilidade.

    A implementação canônica fica em CalculationOrchestrator.run_decision().
    """
    return CalculationOrchestrator().run_decision(
        request,
        payoff=payoff,
        pl_atual=pl_atual,
        pl_max=pl_max,
        dte_min=dte_min,
        auto_run_payoff=False,
    )


def run_full_pipeline(
    request: CalculationRequest,
    low_pct: float = 0.5,
    high_pct: float = 1.5,
    step_pct: float = 0.01,
    extra_meta: Optional[dict] = None,
) -> dict:
    """
    Wrapper de compatibilidade.

    A implementação canônica fica em CalculationOrchestrator.run_full_pipeline().
    """
    return CalculationOrchestrator().run_full_pipeline(
        request,
        low_pct=low_pct,
        high_pct=high_pct,
        step_pct=step_pct,
        extra_meta=extra_meta,
    )
