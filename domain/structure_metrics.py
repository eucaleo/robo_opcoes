from datetime import date, datetime
from typing import Any, Iterable

from domain.position_side import to_pricing_engine_side


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


def _to_float(value: Any) -> float | None:
    if value is None:
        return None

    if isinstance(value, bool):
        return None

    if isinstance(value, int | float):
        return float(value)

    text = str(value).strip()
    if not text:
        return None

    text = text.replace(".", "").replace(",", ".") if "," in text else text

    try:
        return float(text)
    except ValueError:
        return None


def _first_value(source: dict[str, Any], keys: Iterable[str]) -> Any:
    for key in keys:
        value = source.get(key)
        if value is not None and str(value).strip() != "":
            return value

    return None


def _first_float(source: dict[str, Any], keys: Iterable[str]) -> float | None:
    for key in keys:
        value = _to_float(source.get(key))
        if value is not None:
            return value

    return None


def _average(values: Iterable[float | None]) -> float | None:
    valid_values = [value for value in values if value is not None]

    if not valid_values:
        return None

    return sum(valid_values) / len(valid_values)


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


def compute_mid(bid: Any, ask: Any) -> float | None:
    bid_value = _to_float(bid)
    ask_value = _to_float(ask)

    if bid_value is None or ask_value is None:
        return None

    return (bid_value + ask_value) / 2


def compute_spread(bid: Any, ask: Any) -> float | None:
    bid_value = _to_float(bid)
    ask_value = _to_float(ask)

    if bid_value is None or ask_value is None:
        return None

    return ask_value - bid_value


def compute_spread_pct(bid: Any, ask: Any, mid: Any = None) -> float | None:
    spread = compute_spread(bid, ask)
    mid_value = _to_float(mid)

    if mid_value is None:
        mid_value = compute_mid(bid, ask)

    if spread is None or mid_value is None or mid_value == 0:
        return None

    return spread / mid_value


def normalize_position_side(leg: dict[str, Any]) -> str | None:
    side = _first_value(
        leg,
        (
            "position_side",
            "side",
            "cv",
            "compra_venda",
            "buy_sell",
        ),
    )

    if side is None:
        quantity = _first_float(leg, ("quantity", "quant", "qty", "qtd"))
        if quantity is None:
            return None
        return "SHORT" if quantity < 0 else "LONG"

    try:
        return to_pricing_engine_side(side)
    except ValueError:
        return None


def position_multiplier(leg: dict[str, Any]) -> int:
    side = normalize_position_side(leg)

    if side == "SHORT":
        return -1

    return 1


def leg_quantity(leg: dict[str, Any]) -> float | None:
    quantity = _first_float(leg, ("quantity", "quant", "qty", "qtd"))

    if quantity is None:
        return None

    return abs(quantity)


def compute_realistic_price(leg: dict[str, Any]) -> float | None:
    side = normalize_position_side(leg)

    bid = _first_float(leg, ("bid",))
    ask = _first_float(leg, ("ask",))
    mid = _first_float(leg, ("mid",))
    last = _first_float(leg, ("last", "ultimo", "último", "preco", "price"))

    if mid is None:
        mid = compute_mid(bid, ask)

    if side == "SHORT":
        for value in (ask, mid, bid, last):
            if value is not None:
                return value

        return None

    for value in (bid, mid, ask, last):
        if value is not None:
            return value

    return None

def compute_pl_realista(leg: dict[str, Any]) -> float | None:
    quantity = leg_quantity(leg)

    entry_price = _first_float(
        leg,
        (
            "valor_executado",
            "execution_price",
            "entry_price",
            "preco_execucao",
            "preço_execução",
            "preco_entrada",
            "preço_entrada",
        ),
    )

    realistic_price = compute_realistic_price(leg)

    if entry_price is None:
        premium = _first_float(leg, ("premium", "premio", "prêmio"))

        if premium is not None:
            entry_price = premium

            bid = _first_float(leg, ("bid",))
            ask = _first_float(leg, ("ask",))
            mid = _first_float(leg, ("mid",))

            if mid is None:
                mid = compute_mid(bid, ask)

            if mid is not None:
                realistic_price = mid

    if quantity is None or entry_price is None or realistic_price is None:
        return _first_float(leg, ("pl_realista",))

    return (realistic_price - entry_price) * quantity * position_multiplier(leg)

def compute_greek_exposure(leg: dict[str, Any], greek_name: str) -> float | None:
    greek_value = _first_float(leg, (greek_name,))
    quantity = leg_quantity(leg)

    if greek_value is None or quantity is None:
        return None

    return greek_value * quantity * position_multiplier(leg)


def compute_leg_metrics(
    leg: dict[str, Any],
    reference_date: str | None = None,
) -> dict[str, Any]:
    bid = _first_float(leg, ("bid",))
    ask = _first_float(leg, ("ask",))

    mid = compute_mid(bid, ask)
    if mid is None:
        mid = _first_float(leg, ("mid",))

    spread = compute_spread(bid, ask)
    if spread is None:
        spread = _first_float(leg, ("spread",))

    spread_pct = compute_spread_pct(bid, ask, mid)
    if spread_pct is None:
        spread_pct = _first_float(leg, ("spread_pct",))

    dte = _first_float(leg, ("dte",))
    if dte is not None:
        dte = int(dte)
    else:
        expiration_date = _first_value(
            leg,
            (
                "expiration_date",
                "vencimento",
                "maturity_date",
                "expiry",
            ),
        )
        dte = compute_dte(reference_date, expiration_date)

    return {
        "side": normalize_position_side(leg),
        "quantity": leg_quantity(leg),
        "mid": mid,
        "spread": spread,
        "spread_pct": spread_pct,
        "preco_realista": compute_realistic_price(leg),
        "pl_realista": compute_pl_realista(leg),
        "delta_exposto": compute_greek_exposure(leg, "delta"),
        "gamma_exposto": compute_greek_exposure(leg, "gamma"),
        "theta_exposto": compute_greek_exposure(leg, "theta"),
        "vega_exposto": compute_greek_exposure(leg, "vega"),
        "dte": dte,
    }


def compute_structure_metrics(
    legs: list[dict[str, Any]],
    reference_date: str | None = None,
) -> dict[str, Any]:
    computed_legs = []

    for leg in legs:
        leg_metrics = compute_leg_metrics(leg, reference_date=reference_date)
        computed_legs.append(
            {
                **leg,
                **leg_metrics,
            }
        )

    pl_values = [leg.get("pl_realista") for leg in computed_legs]
    delta_values = [leg.get("delta_exposto") for leg in computed_legs]
    gamma_values = [leg.get("gamma_exposto") for leg in computed_legs]
    theta_values = [leg.get("theta_exposto") for leg in computed_legs]
    vega_values = [leg.get("vega_exposto") for leg in computed_legs]
    dte_values = [leg.get("dte") for leg in computed_legs if leg.get("dte") is not None]

    valid_pl_values = [value for value in pl_values if value is not None]
    valid_delta_values = [value for value in delta_values if value is not None]
    valid_gamma_values = [value for value in gamma_values if value is not None]
    valid_theta_values = [value for value in theta_values if value is not None]
    valid_vega_values = [value for value in vega_values if value is not None]

    return {
        "num_pernas": len(computed_legs),
        "legs": computed_legs,
        "pl_realista_total": sum(valid_pl_values) if valid_pl_values else None,
        "delta_liq": sum(valid_delta_values) if valid_delta_values else None,
        "gamma_liq": sum(valid_gamma_values) if valid_gamma_values else None,
        "theta_liq": sum(valid_theta_values) if valid_theta_values else None,
        "vega_liq": sum(valid_vega_values) if valid_vega_values else None,
        "spread_medio": _average(leg.get("spread") for leg in computed_legs),
        "spread_pct_medio": _average(leg.get("spread_pct") for leg in computed_legs),
        "dte_min": min(dte_values) if dte_values else None,
    }


def compute_structure_metrics_from_canonical_input(
    canonical_input: dict[str, Any],
) -> dict[str, Any]:
    structure = canonical_input.get("structure") or {}
    market = canonical_input.get("market") or {}

    reference_date = market.get("reference_date")
    legs = structure.get("legs", [])

    return compute_structure_metrics(legs, reference_date=reference_date)
