#!/usr/bin/env python3
"""
Domain: Decision logic (30/60/80 thresholds + DTE gate) from real data.
"""
import json
from typing import Dict

from .payoff import read_structure_summary, safe_float, safe_int, compute_payoff_for_aba


def _interp_payoff(points, spot: float) -> float:
    """Interpolação linear do payoff no preço spot com base em uma lista [(x, y), ...]."""
    if not points:
        return 0.0

    # Garantir ordenação por preço
    pts = sorted(points, key=lambda t: t[0])

    # Clamp fora do range
    if spot <= pts[0][0]:
        return float(pts[0][1])
    if spot >= pts[-1][0]:
        return float(pts[-1][1])

    # Achar intervalo e interpolar
    for i in range(1, len(pts)):
        x1, y1 = pts[i - 1]
        x2, y2 = pts[i]
        if x2 >= spot:
            if x2 == x1:
                return float(y2)
            t = (spot - x1) / (x2 - x1)
            return float(y1 + t * (y2 - y1))

    return float(pts[-1][1])


def compute_decision_for_aba(
    aba: str,
    pl_max: float,
    thresholds: Dict[str, float] = None,
    dte_gate: int = 7
) -> Dict:
    if thresholds is None:
        thresholds = {"watch": 0.30, "prepare": 0.60, "close": 0.80}

    # 1) Ler dados agregados (DTE, spread, spot do DB)
    summary = read_structure_summary(aba)
    if not summary:
        return {
            "decision": "HOLD",
            "level": 0,
            "pl_atual": 0.0,
            "pl_max": pl_max,
            "pl_pct_of_max": 0.0,
            "dte_min": 0,
            "why_json": json.dumps({"error": "No data found for aba", "aba": aba})
        }

    dte_min = safe_int(summary.get("dte_min"), 999)
    spread_pct_medio = safe_float(summary.get("spread_pct_medio"), 0.0)

    # 2) Calcular PL atual a partir da curva de payoff no spot_ref
    payoff = compute_payoff_for_aba(aba)
    spot = safe_float(payoff.get("spot_ref"), safe_float(summary.get("spot"), 0.0))
    points = payoff.get("points", [])
    pl_atual = _interp_payoff(points, spot)

    # 3) Ratio (permite negativo; só protege pl_max)
    ratio = (pl_atual / pl_max) if (pl_max and pl_max > 0) else 0.0

    # 4) Lógica de decisão (igual à sua)
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

    # Gate de DTE
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

    extra_info = {
        "spot": spot,
        "spread_pct_medio": spread_pct_medio,
        "dte_min": dte_min
    }

    if spread_pct_medio > 1.5:
        alternatives.append(f"ATENÇÃO: Spread alto ({spread_pct_medio:.1%}) pode dificultar execução")

    why_json = json.dumps({
        "reasons": reasons,
        "alternatives": alternatives,
        "thresholds_used": thresholds,
        "dte_gate": dte_gate,
        "extra_info": extra_info
    })

    return {
        "decision": decision,
        "level": level,
        "pl_atual": pl_atual,
        "pl_max": pl_max,
        "pl_pct_of_max": ratio,
        "dte_min": dte_min,
        "why_json": why_json
    }



if __name__ == "__main__":
    # Teste rápido
    from .payoff import get_app_db_connection
    
    print("Testando decision com dados reais...")
    
    # Listar abas disponíveis
    conn = get_app_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT aba, pl_realista_total FROM rtd_analise_robo ORDER BY aba")
    abas_data = cursor.fetchall()
    conn.close()
    
    print(f"Abas com dados: {len(abas_data)}")
    
    for aba, pl_total in abas_data[:3]:  # Testar 3 primeiras
        pl_max_simulado = safe_float(pl_total) * 3  # Simular que o máximo é 3x o atual
        decision_result = compute_decision_for_aba(aba, pl_max_simulado)
        print(f"Aba '{aba}': {decision_result['decision']} (nível {decision_result['level']}) - ratio: {decision_result['pl_pct_of_max']*100:.1f}%")
