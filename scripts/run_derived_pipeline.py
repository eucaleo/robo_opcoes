#!/usr/bin/env python3
import os
from datetime import datetime
from typing import List, Dict

# Opcional: carregar .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

from services.derived_service import init_db, save_payoff_curve, save_decision, cleanup_derived

def simulate_payoff_points(spot_base: float = 100.0) -> List[Dict[str, float]]:
    points = []
    for i in range(50, 151):
        s_t = spot_base * (i / 100.0)
        if s_t < 90:
            pl_venc = -(100 - s_t) * 10
        elif s_t < 110:
            pl_venc = (s_t - 90) * 5
        else:
            pl_venc = (s_t - 90) * 15
        points.append({"s_t": s_t, "pl_venc": pl_venc})
    return points

def main():
    init_db()

    aba = "EXEMPLO_IRON_CONDOR"
    spot_base = 100.0
    timestamp = datetime.now().isoformat()

    # 1) Gerar e salvar pontos de payoff
    points = simulate_payoff_points(spot_base)
    count_points = save_payoff_curve(
        aba=aba,
        points=points,
        spot_ref=spot_base,
        meta={"strategy": "iron_condor", "legs": 4},
        timestamp=timestamp
    )
    print(f"✅ {count_points} pontos de payoff gravados para {aba} @ {timestamp}")

    # 2) Salvar uma decisão exemplo
    decision_id = save_decision(
        aba=aba,
        decision={
            "decision": "HOLD",
            "level": 1,
            "pl_atual": 42.0,
            "pl_max": 300.0,
            "pl_pct_of_max": 0.14,
            "dte_min": 14,
            "spot_atual": 104.9,
            "volatilidade": 0.22,
            "motivo": "PL abaixo da meta de 30%",
        },
        timestamp=timestamp
    )
    print(f"✅ Decisão gravada (ID: {decision_id}) para {aba}")

    # 3) Limpeza de dados antigos (padrão: 30 dias)
    deleted = cleanup_derived(days_to_keep=30)
    print(f"🧹 Limpeza concluída: {deleted}")

    # Caminho do DB para referência
    db_path = os.getenv("DERIVED_DB_PATH", "derived.db")
    print(f"📁 Banco: {os.path.abspath(db_path)}")

if __name__ == "__main__":
    main()
