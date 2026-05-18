from typing import Any

from domain.decision import compute_decision_from_payoff
from domain.payoff import compute_payoff_from_canonical_input
from domain.structure_metrics import compute_dte_min_from_canonical_input
from services.canonical_input_service import CanonicalInputService


class StructureAnalysisService:
    def __init__(
        self,
        canonical_input_service: CanonicalInputService | None = None,
    ):
        self.canonical_input_service = (
            canonical_input_service or CanonicalInputService()
        )

    def analyze(
        self,
        structure_id: int,
        reference_date: str | None = None,
        dte_min: int | None = None,
        spread_pct_medio: float = 0.0,
        thresholds: dict[str, float] | None = None,
        dte_gate: int = 7,
    ) -> dict[str, Any]:
        canonical_input = self.canonical_input_service.build_structure_market_input(
            structure_id=structure_id,
            reference_date=reference_date,
        )

        inferred_dte_min = compute_dte_min_from_canonical_input(canonical_input)

        if dte_min is not None:
            effective_dte_min = dte_min
        elif inferred_dte_min is not None:
            effective_dte_min = inferred_dte_min
        else:
            effective_dte_min = 0

        payoff = compute_payoff_from_canonical_input(canonical_input)

        decision = compute_decision_from_payoff(
            payoff=payoff,
            dte_min=effective_dte_min,
            spread_pct_medio=spread_pct_medio,
            thresholds=thresholds,
            dte_gate=dte_gate,
        )

        return {
            "canonical_input": canonical_input,
            "metrics": {
                "dte_min_inferred": inferred_dte_min,
                "dte_min_effective": effective_dte_min,
                "spread_pct_medio": spread_pct_medio,
            },
            "payoff": payoff,
            "decision": decision,
        }
