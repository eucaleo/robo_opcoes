import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from domain.decision import compute_decision_from_payoff
from domain.payoff import compute_payoff_from_canonical_input
from domain.structure_metrics import compute_dte_min_from_canonical_input
from services.canonical_input_service import CanonicalInputService
from services.pricing_input_service import PricingInputService


def main():
    canonical_service = CanonicalInputService()
    pricing_input_service = PricingInputService(canonical_input_service=canonical_service)

    structure_id = 1
    reference_date = "2026-05-15"

    canonical_input = canonical_service.build_structure_market_input(
        structure_id=structure_id,
        reference_date=reference_date,
    )
    print("=== CANONICAL INPUT ===")
    print(canonical_input)

    pricing_payload = pricing_input_service.build_pricing_payload_from_canonical_input(
        canonical_input
    )
    print("=== PRICING PAYLOAD ===")
    print(pricing_payload)

    dte_min = compute_dte_min_from_canonical_input(canonical_input)
    print("=== METRICS ===")
    print({"dte_min": dte_min})

    payoff = compute_payoff_from_canonical_input(canonical_input)
    print("=== PAYOFF ===")
    print(payoff)

    if payoff:
        decision = compute_decision_from_payoff(
            payoff=payoff,
            dte_min=dte_min if dte_min is not None else 0,
            spread_pct_medio=0.02,
        )
        print("=== DECISION ===")
        print(decision)


if __name__ == "__main__":
    main()
