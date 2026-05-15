from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from _smoke_context import require_context_value
from services.pricing_execution_orchestration_service import PricingExecutionOrchestrationService
from services.pricing_input_service import PricingInputService


def main() -> None:
    try:
        structure_id = require_context_value("structure_id")
    except RuntimeError as exc:
        raise RuntimeError(
            "structure_id não encontrado no smoke context. "
            "Execute primeiro o smoke 10 ou rode pelo runner ATT/checks/run_real_smokes.py."
        ) from exc

    pricing_input_service = PricingInputService()
    orchestration_service = PricingExecutionOrchestrationService()

    pricing_payload = pricing_input_service.build_pricing_payload(
        structure_id=structure_id,
        reference_date="2026-05-14",
    )

    if not pricing_payload:
        raise RuntimeError("pricing payload should not be empty")

    if pricing_payload.get("structure_id") != structure_id:
        raise RuntimeError("pricing payload structure_id should match smoke context structure_id")

    legs = pricing_payload.get("legs", [])
    if not legs:
        raise RuntimeError("expected pricing payload with real legs")

    total_quantity = 0
    for leg in legs:
        quantity = leg.get("quantity")
        if quantity is None:
            raise RuntimeError("pricing leg should contain quantity")
        total_quantity += quantity

    if total_quantity <= 0:
        raise RuntimeError("expected total_quantity > 0 for real pricing payload")

    response = orchestration_service.execute_and_persist(
        structure_id=structure_id,
        reference_date="2026-05-14",
    )

    if not response:
        raise RuntimeError("orchestration response should not be empty")

    response_pricing_payload = response.get("pricing_payload")
    result = response.get("result")
    persisted = response.get("persisted")

    if not response_pricing_payload:
        raise RuntimeError("response should contain pricing_payload")

    if not result:
        raise RuntimeError("response should contain result")

    if not persisted:
        raise RuntimeError("response should contain persisted")

    response_legs = response_pricing_payload.get("legs", [])
    if not response_legs:
        raise RuntimeError("response pricing_payload should contain real legs")

    record = persisted.get("record")
    if not record:
        raise RuntimeError("persisted response should contain record")

    if record.get("structure_id") != structure_id:
        raise RuntimeError("persisted record structure_id should match smoke context structure_id")

    if record.get("number_of_legs", 0) <= 0:
        raise RuntimeError("persisted record should indicate number_of_legs > 0")

    if record.get("total_quantity", 0) <= 0:
        raise RuntimeError("persisted record should indicate total_quantity > 0")

    print("REAL PRICING PAYLOAD:", pricing_payload)
    print("ORCHESTRATED REAL EXECUTION RESPONSE:", response)
    print("PRICING EXECUTION ORCHESTRATION WITH REAL LEGS SMOKE OK")


if __name__ == "__main__":
    main()
