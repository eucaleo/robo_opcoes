from services.canonical_input_service import CanonicalInputService
from _smoke_context import require_context_value


def main():
    service = CanonicalInputService()

    structure_id = require_context_value("structure_id")
    payload = service.build_structure_market_input(
        structure_id=structure_id,
        reference_date="2026-05-14",
    )

    structure = payload["structure"]
    legs = structure["legs"]

    if not isinstance(legs, list):
        raise RuntimeError("structure.legs should be a list")

    print("LEGS COUNT:", len(legs))
    if legs:
        sample = legs[0]
        required = [
            "position_side",
            "option_type",
            "strike",
            "expiration_date",
            "quantity",
            "multiplier",
        ]
        for field in required:
            if field not in sample:
                raise RuntimeError(f"missing leg field: {field}")

    print("CANONICAL INPUT WITH ROBO LEGS SMOKE OK")


if __name__ == "__main__":
    main()
