# services/calculation_orchestrator.py
# PATCH_45: CalculationRequest contract + build_calculation_request
# PATCH_46: _request_to_payoff_dict, run_payoff, run_decision
# PATCH_47: run_full_pipeline, multiplier fix (1.0), run_decision auto-extract
# PATCH_48: build_calculation_request_from_db, run_full_pipeline_from_db

from __future__ import annotations

from typing import Optional, List, Dict, Any

from domain.calculation_request import (
    CalculationRequest,
    StructureInput,
    StructureLegInput,
    MarketSnapshotInput,
)
from domain.payoff import compute_payoff_from_canonical_input
from domain.decision import compute_decision_from_contract


class CalculationOrchestrator:
    """
    Orquestrador canonico de calculo.

    Responsabilidades:
    - Montar CalculationRequest a partir de dados ja normalizados (patch_45/46)
    - Executar payoff e decisao sem acessar raw DB diretamente
    - Montar CalculationRequest a partir dos repositorios canonicos (patch_48)
    """

    def __init__(
        self,
        structures_repository=None,
        market_snapshot_repository=None,
    ):
        """
        Parametros opcionais para permitir uso sem DB (testes unitarios puros).

        structures_repository     : instancia de StructuresRepository
        market_snapshot_repository: instancia de MarketSnapshotRepository
        """
        self._structures_repo = structures_repository
        self._snapshot_repo = market_snapshot_repository

    # ------------------------------------------------------------------
    # PATCH_45/46 — construcao manual do CalculationRequest
    # ------------------------------------------------------------------

    def build_calculation_request(
        self,
        structure_dict: Dict[str, Any],
        market_snapshot_dict: Dict[str, Any],
    ) -> CalculationRequest:
        """
        Monta CalculationRequest a partir de dicts ja normalizados.

        Nao acessa banco. Entrada deve ser pre-processada pelo chamador.
        """
        legs = [
            StructureLegInput(
                position_side=leg["position_side"],
                option_type=leg["option_type"],
                strike=float(leg["strike"]),
                expiration_date=leg["expiration_date"],
                quantity=int(leg["quantity"]),
                symbol=leg.get("symbol"),
                premium=leg.get("premium"),
                multiplier=float(leg.get("multiplier") or 1.0),
            )
            for leg in structure_dict.get("legs", [])
        ]

        structure = StructureInput(
            structure_id=structure_dict["structure_id"],
            name=structure_dict.get("name", ""),
            underlying_asset=structure_dict.get("underlying_asset", ""),
            alias_legacy_aba=structure_dict.get("alias_legacy_aba"),
            legs=legs,
        )

        snapshot = MarketSnapshotInput(
            snapshot_id=market_snapshot_dict.get("snapshot_id"),
            snapshot_timestamp=market_snapshot_dict.get("snapshot_timestamp", ""),
            underlying_asset=market_snapshot_dict.get("underlying_asset", ""),
            spot_price=float(market_snapshot_dict.get("spot_price", 0.0)),
            source=market_snapshot_dict.get("source", ""),
        )

        return CalculationRequest(structure=structure, market_snapshot=snapshot)

    # ------------------------------------------------------------------
    # PATCH_46 — adaptacao interna para o dominio
    # ------------------------------------------------------------------

    def _request_to_payoff_dict(self, request: CalculationRequest) -> Dict[str, Any]:
        """
        Converte CalculationRequest para o dict esperado por
        compute_payoff_from_canonical_input.

        multiplier: usa valor da leg ou fallback 1.0 (patch_47: corrige 100 -> 1.0)
        """
        legs = []
        for leg in request.structure.legs:
            multiplier = leg.multiplier if leg.multiplier is not None else 1.0
            legs.append(
                {
                    "position_side": leg.position_side,
                    "option_type": leg.option_type,
                    "strike": leg.strike,
                    "expiration_date": leg.expiration_date,
                    "quantity": leg.quantity,
                    "symbol": leg.symbol,
                    "premium": leg.premium,
                    "multiplier": multiplier,
                }
            )

        return {
            "structure_id": request.structure.structure_id,
            "underlying_asset": request.structure.underlying_asset,
            "spot_price": request.market_snapshot.spot_price,
            "snapshot_timestamp": request.market_snapshot.snapshot_timestamp,
            "legs": legs,
            "low_pct": 0.7,
            "high_pct": 1.3,
            "step_pct": 0.005,
        }

    # ------------------------------------------------------------------
    # PATCH_46 — run_payoff / run_decision
    # ------------------------------------------------------------------

    def run_payoff(self, request: CalculationRequest) -> Dict[str, Any]:
        """
        Executa calculo de payoff a partir de um CalculationRequest.

        Retorna o dict de resultado do dominio.
        """
        payoff_dict = self._request_to_payoff_dict(request)
        result = compute_payoff_from_canonical_input(payoff_dict)
        return result

    def run_decision(
        self,
        request: CalculationRequest,
        payoff_result: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Executa calculo de decisao a partir de um CalculationRequest.

        patch_47: pl_max, pl_atual e dte_min sao extraidos automaticamente
        de payoff_result e market_snapshot quando nao informados explicitamente.

        payoff_result: resultado de run_payoff (opcional; se None, executa payoff
                       internamente antes de calcular decisao)
        """
        if payoff_result is None:
            payoff_result = self.run_payoff(request)

        pl_max = payoff_result.get("pl_max") or payoff_result.get("max_profit") or 0.0
        pl_atual = (
            payoff_result.get("pl_atual")
            or payoff_result.get("current_pl")
            or payoff_result.get("pl_at_spot")
            or 0.0
        )
        dte_min = request.market_snapshot.spot_price and (
            payoff_result.get("dte_min")
            or getattr(request.market_snapshot, "dte_min", None)
            or 0
        )

        contract = {
            "structure_id": request.structure.structure_id,
            "underlying_asset": request.structure.underlying_asset,
            "spot_price": request.market_snapshot.spot_price,
            "snapshot_timestamp": request.market_snapshot.snapshot_timestamp,
            "pl_max": pl_max,
            "pl_atual": pl_atual,
            "dte_min": dte_min,
            "payoff_result": payoff_result,
        }

        result = compute_decision_from_contract(contract)
        return result

    # ------------------------------------------------------------------
    # PATCH_47 — run_full_pipeline
    # ------------------------------------------------------------------

    def run_full_pipeline(
        self, request: CalculationRequest
    ) -> Dict[str, Any]:
        """
        Executa run_payoff -> run_decision em sequencia.

        Retorna dict consolidado com chaves:
            payoff  : resultado do calculo de payoff
            decision: resultado do calculo de decisao
        """
        payoff_result = self.run_payoff(request)
        decision_result = self.run_decision(request, payoff_result=payoff_result)

        return {
            "payoff": payoff_result,
            "decision": decision_result,
        }

    # ------------------------------------------------------------------
    # PATCH_48 — resolucao via repositorios canonicos
    # ------------------------------------------------------------------

    def build_calculation_request_from_db(
        self,
        structure_id: int,
        snapshot_timestamp: Optional[str] = None,
    ) -> CalculationRequest:
        """
        Monta CalculationRequest buscando dados dos repositorios canonicos.

        Fluxo:
        1. Busca estrutura + legs em StructuresRepository
        2. Busca snapshot em MarketSnapshotRepository
        3. Monta e retorna CalculationRequest

        Raises:
            RuntimeError: se repositorios nao foram injetados
            ValueError  : se estrutura nao for encontrada ou estiver arquivada
            ValueError  : se snapshot nao for encontrado para a estrutura
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

        # 3. Monta structure_dict compativel com build_calculation_request
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
                }
                for leg in legs_raw
            ],
        }

        market_snapshot_dict = {
            "snapshot_id": snapshot.get("id"),
            "snapshot_timestamp": snapshot.get("snapshot_timestamp", ""),
            "underlying_asset": snapshot.get("underlying_asset", underlying),
            "spot_price": snapshot.get("spot_price", 0.0),
            "source": snapshot.get("source", ""),
        }

        return self.build_calculation_request(structure_dict, market_snapshot_dict)

    def run_full_pipeline_from_db(
        self,
        structure_id: int,
        snapshot_timestamp: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Pipeline completo resolvendo estrutura e snapshot pelos repositorios.

        Equivalente a:
            request = build_calculation_request_from_db(structure_id, ...)
            return run_full_pipeline(request)

        Retorna dict com chaves:
            structure_id: int
            payoff      : resultado do calculo de payoff
            decision    : resultado do calculo de decisao
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
