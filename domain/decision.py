#!/usr/bin/env python3
"""
Domain: Decision logic (30/60/80 thresholds + DTE gate) from real data.
"""

import json
from dataclasses import is_dataclass
from typing import Any

from domain.payoff import compute_payoff_from_canonical_input
from domain.structure_metrics import compute_dte_min_from_canonical_input

try:
    from domain.contracts import CanonicalStructureMarketInput
except ImportError:  # pragma: no cover
    CanonicalStructureMarketInput = None  # type: ignore


DEFAULT_THRESHOLDS = {
    "watch": 0.30,
    "prepare": 0.60,
    "close": 0.80,
}


def _interp_payoff(points, spot: float) -> float:
    """Interpolação linear do payoff no preço spot com base em uma lista [(x, y), ...]."""
    if not points:
        return 0.0

    pts = sorted(points, key=lambda t: t[0])

    if spot <= pts[0][0]:
        return float(pts[0][1])
    if spot >= pts[-1][0]:
        return float(pts[-1][1])

    for i in range(1, len(pts)):
        x1, y1 = pts[i - 1]
        x2, y2 = pts[i]
        if x2 >= spot:
            if x2 == x1:
                return float(y2)
            t = (spot - x1) / (x2 - x1)
            return float(y1 + t * (y2 - y1))

    return float(pts[-1][1])


def safe_float(value, default: float = 0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def safe_int(value, default: int = 0) -> int:
    try:
        if value is None or value == "":
            return default
        return int(value)
    except (TypeError, ValueError):
        return default


def _resolve_thresholds(thresholds: dict[str, float] | None) -> dict[str, float]:
    if thresholds is None:
        return DEFAULT_THRESHOLDS.copy()
    return {
        "watch": safe_float(thresholds.get("watch"), DEFAULT_THRESHOLDS["watch"]),
        "prepare": safe_float(thresholds.get("prepare"), DEFAULT_THRESHOLDS["prepare"]),
        "close": safe_float(thresholds.get("close"), DEFAULT_THRESHOLDS["close"]),
    }


def _to_json_payload(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, default=str)


def _build_why_payload(
    reasons,
    alternatives,
    thresholds,
    dte_gate: int,
    extra_info: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "reasons": reasons,
        "alternatives": alternatives,
        "thresholds_used": thresholds,
        "dte_gate": dte_gate,
        "extra_info": extra_info or {},
    }


def _build_error_decision(
    message: str,
    dte_min: int = 0,
    pl_max: float = 0.0,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload = {"error": message}
    if extra:
        payload.update(extra)

    return {
        "decision": "HOLD",
        "level": 0,
        "pl_atual": 0.0,
        "pl_max": pl_max,
        "pl_pct_of_max": 0.0,
        "dte_min": dte_min,
        "why": payload,
        "why_json": _to_json_payload(payload),
    }


def _is_invalid_payoff(payoff: dict[str, Any] | None) -> bool:
    if not payoff:
        return True

    meta = payoff.get("meta") or {}
    validation_errors = meta.get("validation_errors") or []
    if validation_errors:
        return True

    points = payoff.get("points") or []
    if not points:
        return True

    return False


def _normalize_contract_input(contract: Any) -> dict[str, Any]:
    if contract is None:
        return {}

    if CanonicalStructureMarketInput is not None and isinstance(contract, CanonicalStructureMarketInput):
        return contract.to_dict()

    if is_dataclass(contract) and hasattr(contract, "to_dict"):
        return contract.to_dict()

    if isinstance(contract, dict):
        return contract

    return {}


def _resolve_dte_min(
    normalized_contract: dict[str, Any],
    dte_min: int | None,
) -> int:
    if dte_min is not None:
        return safe_int(dte_min, 0)

    inferred_dte_min = compute_dte_min_from_canonical_input(normalized_contract)
    if inferred_dte_min is not None:
        return safe_int(inferred_dte_min, 0)

    return 0


def compute_decision_from_contract(
    contract: dict[str, Any] | Any,
    dte_min: int | None = None,
    spread_pct_medio: float = 0.0,
    thresholds: dict[str, float] | None = None,
    dte_gate: int = 7,
) -> dict[str, Any]:
    normalized_contract = _normalize_contract_input(contract)
    effective_dte_min = _resolve_dte_min(normalized_contract, dte_min)
    payoff = compute_payoff_from_canonical_input(normalized_contract)

    if _is_invalid_payoff(payoff):
        return _build_error_decision(
            message="unable to compute payoff from contract",
            dte_min=effective_dte_min,
            pl_max=safe_float((payoff or {}).get("pl_max"), 0.0),
            extra={
                "structure_id": (payoff or {}).get("structure_id"),
                "structure_name": (payoff or {}).get("structure_name"),
                "underlying_asset": (payoff or {}).get("underlying_asset"),
                "reference_date": (payoff or {}).get("reference_date"),
                "validation_errors": ((payoff or {}).get("meta") or {}).get("validation_errors", []),
            },
        )

    return compute_decision_from_payoff(
        payoff=payoff,
        dte_min=effective_dte_min,
        spread_pct_medio=spread_pct_medio,
        thresholds=thresholds,
        dte_gate=dte_gate,
    )


def compute_decision_for_aba(
    aba: str,
    pl_max: float,
    thresholds: dict[str, float] | None = None,
    dte_gate: int = 7,
) -> dict[str, Any]:
    """
    Legacy compatibility path.
    Prefer compute_decision_from_contract(...) for the canonical flow.
    """
    thresholds = _resolve_thresholds(thresholds)

    try:
        from .payoff import compute_payoff_for_aba, read_structure_summary
    except ImportError:
        return _build_error_decision(
            message="legacy aba decision path unavailable",
            dte_min=0,
            pl_max=pl_max,
            extra={"aba": aba},
        )

    summary = read_structure_summary(aba)
    if not summary:
        return _build_error_decision(
            message="No data found for aba",
            dte_min=0,
            pl_max=pl_max,
            extra={"aba": aba},
        )

    dte_min = safe_int(summary.get("dte_min"), 999)
    spread_pct_medio = safe_float(summary.get("spread_pct_medio"), 0.0)

    payoff = compute_payoff_for_aba(aba)
    if not payoff:
        return _build_error_decision(
            message="Unable to compute payoff for aba",
            dte_min=dte_min,
            pl_max=pl_max,
            extra={"aba": aba},
        )

    spot = safe_float(payoff.get("spot_ref"), safe_float(summary.get("spot"), 0.0))
    points = payoff.get("points", [])
    pl_atual = _interp_payoff(points, spot)

    extra_info = {
        "spot": spot,
        "spread_pct_medio": spread_pct_medio,
        "dte_min": dte_min,
        "aba": aba,
        "pl_max": pl_max,
        "pl_pct_of_max": (pl_atual / pl_max) if (pl_max and pl_max > 0) else 0.0,
        "points_count": len(points),
    }

    return compute_decision_from_inputs(
        pl_atual=pl_atual,
        pl_max=pl_max,
        dte_min=dte_min,
        spread_pct_medio=spread_pct_medio,
        thresholds=thresholds,
        dte_gate=dte_gate,
        extra_info=extra_info,
    )


def compute_decision_from_inputs(
    pl_atual: float,
    pl_max: float,
    dte_min: int,
    spread_pct_medio: float = 0.0,
    thresholds: dict[str, float] | None = None,
    dte_gate: int = 7,
    extra_info: dict[str, Any] | None = None,
) -> dict[str, Any]:
    thresholds = _resolve_thresholds(thresholds)

    ratio = (pl_atual / pl_max) if (pl_max and pl_max > 0) else 0.0

    decision = "HOLD"
    level = 0
    reasons = []
    alternatives = []

    if ratio >= thresholds["close"]:
        decision = "CLOSE_REOPEN"
        level = 3
        reasons.append(
            f"PL atual ({pl_atual:.2f}) atingiu {ratio*100:.1f}% do máximo (>= {thresholds['close']*100:.0f}%)"
        )
        alternatives.append("Executar fechamento e reabertura")
    elif ratio >= thresholds["prepare"]:
        decision = "PREPARE_ROLL"
        level = 2
        reasons.append(
            f"PL atual ({pl_atual:.2f}) atingiu {ratio*100:.1f}% do máximo (>= {thresholds['prepare']*100:.0f}%)"
        )
        alternatives.append("Preparar para fechamento ou aguardar 80%")
    elif ratio >= thresholds["watch"]:
        decision = "HOLD"
        level = 1
        reasons.append(
            f"PL atual ({pl_atual:.2f}) atingiu {ratio*100:.1f}% do máximo (>= {thresholds['watch']*100:.0f}%)"
        )
        alternatives.append("Continuar monitorando")
    else:
        reasons.append(f"PL atual ({pl_atual:.2f}) ainda baixo ({ratio*100:.1f}% do máximo)")
        alternatives.append("Aguardar evolução")

    if dte_min <= dte_gate and ratio >= thresholds["prepare"]:
        old_decision = decision
        decision = "CLOSE_REOPEN"
        level = 3
        reasons.append(
            f"Gate DTE: {dte_min} <= {dte_gate} dias e ratio >= {thresholds['prepare']*100:.0f}% → promovido para CLOSE"
        )
        alternatives.append(f"Era {old_decision}, mas DTE baixo força fechamento")
    elif dte_min <= dte_gate:
        reasons.append(f"DTE baixo ({dte_min} dias), mas ratio ainda insuficiente para close")
        alternatives.append("Avaliar fechamento manual por vencimento próximo")

    if spread_pct_medio > 0.015:
        alternatives.append(
            f"ATENÇÃO: Spread alto ({spread_pct_medio:.1%}) pode dificultar execução"
        )

    merged_extra_info = {
        **(extra_info or {}),
        "pl_max": pl_max,
        "pl_pct_of_max": ratio,
    }

    why = _build_why_payload(
        reasons=reasons,
        alternatives=alternatives,
        thresholds=thresholds,
        dte_gate=dte_gate,
        extra_info=merged_extra_info,
    )

    return {
        "decision": decision,
        "level": level,
        "pl_atual": pl_atual,
        "pl_max": pl_max,
        "pl_pct_of_max": ratio,
        "dte_min": dte_min,
        "why": why,
        "why_json": _to_json_payload(why),
    }


def compute_decision_from_payoff(
    payoff: dict[str, Any],
    dte_min: int,
    spread_pct_medio: float = 0.0,
    thresholds: dict[str, float] | None = None,
    dte_gate: int = 7,
) -> dict[str, Any]:
    if _is_invalid_payoff(payoff):
        return _build_error_decision(
            message="payoff is required",
            dte_min=dte_min,
            pl_max=safe_float((payoff or {}).get("pl_max"), 0.0),
            extra={
                "structure_id": (payoff or {}).get("structure_id"),
                "structure_name": (payoff or {}).get("structure_name"),
                "underlying_asset": (payoff or {}).get("underlying_asset"),
                "reference_date": (payoff or {}).get("reference_date"),
                "validation_errors": ((payoff or {}).get("meta") or {}).get("validation_errors", []),
            },
        )

    spot = safe_float(payoff.get("spot_ref"), 0.0)
    points = payoff.get("points", [])
    pl_max = safe_float(payoff.get("pl_max"), 0.0)
    pl_atual = _interp_payoff(points, spot)

    extra_info = {
        "spot": spot,
        "spread_pct_medio": spread_pct_medio,
        "dte_min": dte_min,
        "structure_id": payoff.get("structure_id"),
        "structure_name": payoff.get("structure_name"),
        "underlying_asset": payoff.get("underlying_asset"),
        "reference_date": payoff.get("reference_date"),
        "input_meta": payoff.get("input_meta", {}),
        "points_count": len(points),
    }

    return compute_decision_from_inputs(
        pl_atual=pl_atual,
        pl_max=pl_max,
        dte_min=dte_min,
        spread_pct_medio=spread_pct_medio,
        thresholds=thresholds,
        dte_gate=dte_gate,
        extra_info=extra_info,
    )


if __name__ == "__main__":
    from .payoff import get_app_db_connection

    print("Testando decision com dados reais (legacy aba path)...")

    conn = get_app_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT aba, pl_realista_total FROM rtd_analise_robo ORDER BY aba")
    abas_data = cursor.fetchall()
    conn.close()

    print(f"Abas com dados: {len(abas_data)}")

    for aba, pl_total in abas_data[:3]:
        pl_max_simulado = safe_float(pl_total) * 3
        decision_result = compute_decision_for_aba(aba, pl_max_simulado)
        print(
            f"Aba '{aba}': {decision_result['decision']} "
            f"(nível {decision_result['level']}) - "
            f"ratio: {decision_result['pl_pct_of_max']*100:.1f}%"
        )
