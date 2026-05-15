from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from services.canonical_input_service import CanonicalInputService
from _smoke_context import require_context_value


def main() -> None:
    service = CanonicalInputService()

    try:
        structure_id = require_context_value("structure_id")
    except RuntimeError as exc:
        raise RuntimeError(
            "structure_id não encontrado no smoke context. "
            "Execute primeiro o smoke 10 ou rode pelo runner ATT/checks/run_real_smokes.py."
        ) from exc

    payload = service.build_structure_market_input(
        structure_id=structure_id,
        reference_date="2026-05-14",
    )

    if not payload:
        raise RuntimeError("canonical input payload should not be empty")

    structure = payload.get("structure")
    market = payload.get("market")

    if not structure:
        raise RuntimeError("payload should contain structure section")

    if not market:
        raise RuntimeError("payload should contain market section")

    if structure.get("structure_id") != structure_id:
        raise RuntimeError("payload structure_id should match smoke context structure_id")

    if structure.get("underlying_asset") != "BOVA11":
        raise RuntimeError("expected underlying_asset to be BOVA11 in smoke")

    legs = structure.get("legs", [])
    if not legs:
        raise RuntimeError("expected canonical input service to load real legacy legs")

    first_leg = legs[0]
    required_leg_fields = [
        "position_side",
        "option_type",
        "strike",
        "expiration_date",
        "quantity",
        "multiplier",
    ]
    for field in required_leg_fields:
        if field not in first_leg:
            raise RuntimeError(f"canonical leg missing required field: {field}")

    print("CANONICAL INPUT PAYLOAD:", payload)
    print("CANONICAL INPUT SERVICE SMOKE OK")


if __name__ == "__main__":
    main()
