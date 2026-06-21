# services/structure_analysis_service.py
from __future__ import annotations

from typing import Any, Dict, Optional

from domain.decision import compute_decision_from_payoff
from domain.payoff import compute_payoff_from_canonical_input
from domain.structure_metrics import (
    compute_dte_min_from_canonical_input,
    compute_structure_metrics_from_canonical_input,
)


class StructureAnalysisService:
    def __init__(self, canonical_input_service):
        self._canonical_input_service = canonical_input_service

    def analyze(
        self,
        structure_id: int,
        reference_date: Optional[str] = None,
        dte_min: Optional[int] = None,
        spread_pct_medio: Optional[float] = None,
        thresholds: Optional[Dict[str, float]] = None,
        dte_gate: int = 7,
    ) -> Dict[str, Any]:

        # 1. Busca input canônico
        canonical_input = self._canonical_input_service.build_structure_market_input(
            structure_id=structure_id,
            reference_date=reference_date,
        )

        # 2. Calcula métricas internas da estrutura
        structure_metrics = compute_structure_metrics_from_canonical_input(canonical_input)

        # 3. Calcula DTE inferido preservando o contrato legado
        #
        # Mantemos compute_dte_min_from_canonical_input como fonte explícita do
        # dte_min_inferred para compatibilidade com testes e integrações já
        # existentes. O motor novo também calcula dte_min, mas nesta etapa ele é
        # exposto dentro de structure_metrics.
        dte_min_inferred = compute_dte_min_from_canonical_input(canonical_input)

        # 4. DTE efetivo: explícito > inferido > 0
        if dte_min is not None:
            dte_min_effective = dte_min
        elif dte_min_inferred is not None:
            dte_min_effective = dte_min_inferred
        else:
            dte_min_effective = 0

        # 5. Spread efetivo: explícito > calculado internamente
        spread_pct_medio_inferred = structure_metrics.get("spread_pct_medio")

        if spread_pct_medio is not None:
            spread_pct_medio_effective = spread_pct_medio
        else:
            spread_pct_medio_effective = spread_pct_medio_inferred

        # 6. Calcula payoff
        payoff = compute_payoff_from_canonical_input(canonical_input)

        # 7. Valida payoff -- se inválido, retorna HOLD com erro estruturado
        if not payoff or not payoff.get("pl_max"):
            why_dict = {
                "error": "payoff is required",
                "validation_errors": ["pl_max ausente ou zero"],
                "reasons": ["invalid_payoff"],
                "alternatives": [],
            }
            decision = {
                "decision":      "HOLD",
                "level":         0,
                "ratio":         0.0,
                "pl_pct_of_max": 0.0,
                "dte_min":       dte_min_effective,
                "why":           why_dict,
                "why_json":      "{}",
                "alternatives":  [],
            }
            return {
                "canonical_input": canonical_input,
                "metrics": {
                    "dte_min_inferred":             dte_min_inferred,
                    "dte_min_effective":            dte_min_effective,
                    "spread_pct_medio":             spread_pct_medio_effective,
                    "spread_pct_medio_inferred":    spread_pct_medio_inferred,
                    "structure_metrics":            structure_metrics,
                },
                "payoff":   payoff,
                "decision": decision,
            }

        # 8. Computa decisão -- passa TODOS os parâmetros como keyword
        decision = compute_decision_from_payoff(
            payoff=payoff,
            dte_min=dte_min_effective,
            spread_pct_medio=spread_pct_medio_effective,
            thresholds=thresholds,
            dte_gate=dte_gate,
        )

        # 9. Injeta dte_min no retorno (esperado pelos testes)
        decision["dte_min"] = dte_min_effective

        # 10. Injeta dte_gate em why (esperado por test_propagates_custom_thresholds_and_dte_gate)
        decision["why"]["dte_gate"] = dte_gate

        return {
            "canonical_input": canonical_input,
            "metrics": {
                "dte_min_inferred":             dte_min_inferred,
                "dte_min_effective":            dte_min_effective,
                "spread_pct_medio":             spread_pct_medio_effective,
                "spread_pct_medio_inferred":    spread_pct_medio_inferred,
                "structure_metrics":            structure_metrics,
            },
            "payoff":   payoff,
            "decision": decision,
        }
