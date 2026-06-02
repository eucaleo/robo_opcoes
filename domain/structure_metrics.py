from datetime import date, datetime
from typing import Any


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None

    value = str(value).strip()
    if not value:
        return None

    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue

    return None


def compute_dte(reference_date: str | None, expiration_date: str | None) -> int | None:
    ref = _parse_date(reference_date)
    exp = _parse_date(expiration_date)

    if ref is None or exp is None:
        return None

    return (exp - ref).days


def compute_dte_min_from_canonical_input(canonical_input: dict[str, Any]) -> int | None:
    structure = canonical_input.get("structure") or {}
    market = canonical_input.get("market") or {}

    reference_date = market.get("reference_date")
    legs = structure.get("legs", [])

    dtes = []
    for leg in legs:
        expiration_date = leg.get("expiration_date")
        dte = compute_dte(reference_date, expiration_date)
        if dte is not None:
            dtes.append(dte)

    if not dtes:
        return None

    return min(dtes)
