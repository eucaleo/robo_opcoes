from services.canonical_input_service import CanonicalInputService
from _smoke_context import require_context_value


def main():
    service = CanonicalInputService()

    structure_id = require_context_value("structure_id")
    payload = service.build_structure_market_input(
        structure_id=structure_id,
        reference_date="2026-05-14",
    )

    if payload["structure"]["structure_id"] != structure_id:
        raise RuntimeError("canonical input structure_id should match smoke context structure_id")

    if payload["market"]["underlying_asset"] != payload["structure"]["underlying_asset"]:
        raise RuntimeError("canonical input market underlying_asset should match structure underlying_asset")

    print("CANONICAL INPUT PAYLOAD:", payload)
    print("CANONICAL INPUT SERVICE SMOKE OK")


if __name__ == "__main__":
    main()

