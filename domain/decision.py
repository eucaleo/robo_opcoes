#!/usr/bin/env python3
"""
Domain: Decision logic (30/60/80 thresholds + DTE gate) from real data.

Codigo legado removido neste modulo.
Funcoes canonicas: compute_decision_from_inputs, compute_decision_from_payoff,
compute_decision_from_contract.
"""
from __future__ import annotations

import json
import math
from typing import Any, Dict, List, Optional, Tuple

from domain.contracts import CanonicalStructureMarketInput


# ---------------------------------------------------------------------------
# Constantes de decisão
# ---------------------------------------------------------------------------
THRESHOLD_CLOSE   = 0.80
THRESHOLD_PREPARE = 0.60
THRESHOLD_WATCH   = 0.30

DTE_GATE_DEFAULT  = 7


# ---------------------------------------------------------------------------
# Helpers internos (exportados para testes de interpolação)
# ---------------------------------------------------------------------------

def _interp_payoff(points: List[Tuple[float, float]], spot: float) -> float:
    """Interpola P&L no spot dado a partir dos pontos da curva."""
    if not points:
        return 0.0
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    if spot <= xs[0]:
        return ys[0]
    if spot >= xs[-1]:
        return ys[-1]
    for i in range(len(xs) - 1):
        if xs[i] <= spot <= xs[i + 1]:
            t = (spot - xs[i]) / (xs[i + 1] - xs[i])
            return ys[i] + t * (ys[i + 1] - ys[i])
    return 0.0


def _ratio(numerator: float, denominator: float) -> float:
    if denominator == 0.0:
        return 0.0
    return numerator / denominator


# Mapeamento decision → level
_DECISION_LEVEL = {
    "HOLD":         0,
    "WATCH":        1,   # nível interno, mapeado para decision="HOLD" level=1
    "PREPARE_ROLL": 2,
    "CLOSE_REOPEN": 3,
}


# ---------------------------------------------------------------------------
# API pública
# ---------------------------------------------------------------------------

def compute_decision_from_inputs(
    pl_atual: float,
    pl_max: float,
    dte_min: Optional[int] = None,
    dte_gate: int = DTE_GATE_DEFAULT,
    spread_pct_medio: Optional[float] = None,
    thresholds: Optional[Dict[str, float]] = None,
) -> Dict[str, Any]:
    _t_close   = (thresholds or {}).get("close",   THRESHOLD_CLOSE)
    _t_prepare = (thresholds or {}).get("prepare", THRESHOLD_PREPARE)
    _t_watch   = (thresholds or {}).get("watch",   THRESHOLD_WATCH)

    ratio = _ratio(pl_atual, pl_max)
    alts: List[str] = []

    if spread_pct_medio is not None and spread_pct_medio > 0.015:
        alts.append("Spread alto — aguardar execução")

    # ✅ Gate só dispara se dte_min foi fornecido E é > 0
    #    dte_min=0 significa "expirado/sem DTE real" — não aciona gate
    if dte_min is not None and dte_min > 0 and dte_min <= dte_gate:
        _internal = "CLOSE_REOPEN"
        level = 3
        reason = "DTE gate"
        extra: Dict[str, Any] = {"dte_min": dte_min, "dte_gate": dte_gate}
    elif ratio >= _t_close:
        _internal = "CLOSE_REOPEN"
        level = 3
        reason = "threshold_close"
        extra = {}
    elif ratio >= _t_prepare:
        _internal = "PREPARE_ROLL"
        level = 2
        reason = "threshold_prepare"
        extra = {}
    elif ratio >= _t_watch:
        _internal = "WATCH"
        level = 1
        reason = "threshold_watch"
        extra = {}
    else:
        _internal = "HOLD"
        level = 0
        reason = "below_watch"
        extra = {}

    decision = "HOLD" if _internal == "WATCH" else _internal

    why_dict: Dict[str, Any] = {
        "reasons":        [reason],
        "ratio":          round(ratio, 4),
        "alternatives":   alts,
        "thresholds_used": {
            "watch":   _t_watch,
            "prepare": _t_prepare,
            "close":   _t_close,
        },
        **extra,
    }

    return {
        "decision":      decision,
        "level":         level,
        "ratio":         round(ratio, 4),
        "pl_pct_of_max": round(ratio, 4),
        "why_json":      json.dumps(why_dict),
        "why":           why_dict,
        "alternatives":  alts,
    }


def compute_decision_from_payoff(
    payoff: Dict[str, Any],
    dte_min: Optional[int] = None,
    dte_gate: int = DTE_GATE_DEFAULT,
    spread_pct_medio: Optional[float] = None,
    thresholds: Optional[Dict[str, float]] = None,
) -> Dict[str, Any]:
    """
    Decide a partir de um dict de payoff.
    Payoff vazio ou inválido → HOLD com 'error' em why_json.
    """
    if not payoff:
        why_dict = {"error": "payoff vazio ou invalido", "reason": "invalid_input"}
        return {
            "decision":      "HOLD",
            "level":         0,
            "ratio":         0.0,
            "pl_pct_of_max": 0.0,
            "why_json":      json.dumps(why_dict),
            "why":           why_dict,
            "alternatives":  [],
        }

    pl_atual = payoff.get("pl_atual") or payoff.get("pl_now") or 0.0
    pl_max   = payoff.get("pl_max") or 0.0

    # Interpolação via points + spot, se disponíveis
    points = payoff.get("points") or []
    spot   = payoff.get("spot")
    if points and spot is not None and pl_atual == 0.0:
        pl_atual = _interp_payoff(points, float(spot))

    if not math.isfinite(float(pl_max)):
        why_dict = {"error": "pl_max invalido", "reason": "invalid_pl_max"}
        return {
            "decision":      "HOLD",
            "level":         0,
            "ratio":         0.0,
            "pl_pct_of_max": 0.0,
            "why_json":      json.dumps(why_dict),
            "why":           why_dict,
            "alternatives":  [],
        }

    return compute_decision_from_inputs(
        pl_atual=float(pl_atual),
        pl_max=float(pl_max),
        dte_min=dte_min,
        dte_gate=dte_gate,
        spread_pct_medio=spread_pct_medio,
        thresholds=thresholds,
    )


def compute_decision_from_contract(
    contract: CanonicalStructureMarketInput,
    payoff: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Entrada canônica via CanonicalStructureMarketInput."""
    pl_max  = float(getattr(contract, "pl_max",  None) or 0.0)
    dte_min = getattr(contract, "dte_min", None)

    if payoff:
        return compute_decision_from_payoff(payoff=payoff, dte_min=dte_min)

    pl_atual = float(
        getattr(contract, "pl_atual", None)
        or getattr(contract, "pl_now", None)
        or 0.0
    )
    return compute_decision_from_inputs(
        pl_atual=pl_atual,
        pl_max=pl_max,
        dte_min=dte_min,
    )
