#!/usr/bin/env python3
"""
Domain: Payoff calculation (expiry curve) from real rtd_* data.
"""
import sqlite3
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from db.config import connect_app


def get_app_db_connection():
    """Conexão com app.db (dados raw) - resolve caminho para evitar erro de pasta"""
    db_path = Path("data/app.db").resolve()
    return sqlite3.connect(str(db_path))


def safe_float(value, default=0.0) -> float:
    """Converte TEXT para float, tolerante a erros do Excel/RTD"""
    if value is None or value == '' or value == 'N/A':
        return default
    try:
        return float(str(value).replace(',', '.'))  # Excel às vezes usa vírgula
    except (ValueError, TypeError):
        return default


def safe_int(value, default=0) -> int:
    """Converte TEXT para int, tolerante a erros"""
    if value is None or value == '' or value == 'N/A':
        return default
    try:
        return int(float(str(value).replace(',', '.')))
    except (ValueError, TypeError):
        return default


def normalize_side(cv_raw: str) -> Optional[str]:
    """Normaliza sentido da operação para LONG/SHORT"""
    if cv_raw is None:
        return None
    s = str(cv_raw).strip().upper()
    if s in ("C", "COMPRA", "COMPRADO", "BUY", "B", "LONG"):
        return "LONG"
    if s in ("V", "VENDA", "VENDIDO", "SELL", "S", "SHORT"):
        return "SHORT"
    return None


def read_structure_legs(aba: str, timestamp: Optional[str] = None) -> List[Dict]:
    """
    Lê pernas de uma estrutura do app.db.
    Se timestamp for None, pega o timestamp mais recente da aba e retorna TODAS as legs daquele snapshot.
    """
    conn = connect_app()
    cursor = conn.cursor()

    ts = timestamp
    if ts is None:
        cursor.execute(
            "SELECT MAX(timestamp) FROM rtd_analise_robo_legs WHERE aba = ?",
            (aba,)
        )
        row = cursor.fetchone()
        ts = row[0] if row else None

    if not ts:
        conn.close()
        return []

    cursor.execute(
        """
        SELECT * FROM rtd_analise_robo_legs
        WHERE aba = ? AND timestamp = ?
        ORDER BY strike
        """,
        (aba, ts)
    )

    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    conn.close()

    return [dict(zip(columns, row)) for row in rows]


def read_structure_summary(aba: str) -> Optional[Dict]:
    """
    Lê dados agregados da estrutura (spot, dte_min, pl_total).
    """
    conn = connect_app()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM rtd_analise_robo 
        WHERE aba = ? 
        ORDER BY rowid DESC 
        LIMIT 1
    """, (aba,))

    row = cursor.fetchone()
    if not row:
        conn.close()
        return None

    columns = [desc[0] for desc in cursor.description]
    conn.close()
    return dict(zip(columns, row))


def compute_payoff_curve(
    legs: List[Dict], 
    spot: float,
    grid_low_pct: float = 0.5,
    grid_high_pct: float = 1.5,
    step_pct: float = 0.01
) -> Dict:
    """
    Calcula curva de payoff no vencimento para uma estrutura.

    Returns:
        {
            "points": [(point_spot, point_pl), ...],
            "pl_max": float,
            "pl_min": float,
            "spot_ref": float,
            "meta": {...}
        }
    """
    if not legs or spot <= 0:
        return {"points": [], "pl_max": 0, "pl_min": 0, "spot_ref": spot, "meta": {}}

    # Grid de preços
    s_min = spot * grid_low_pct
    s_max = spot * grid_high_pct
    step = max(spot * step_pct, 0.01)

    points = []
    pl_values = []

    # Para cada preço do underlying no vencimento
    s_t = s_min
    while s_t <= s_max:
        pl_total = 0.0

        # Para cada perna
        for leg in legs:
            # --- normalização de parâmetros
            cp = str(leg.get('call_put', '')).strip().upper()
            is_call = ("CALL" in cp) or (cp == "C")
            is_put  = ("PUT" in cp)  or (cp == "P")
            if not (is_call or is_put):
                continue

            side = normalize_side(leg.get('cv'))
            if side is None:
                continue

            quant = safe_float(leg.get('quant'), 0)
            valor_executado = safe_float(leg.get('valor_executado'), 0)
            strike = safe_float(leg.get('strike'), 0)

            if quant == 0 or strike == 0:
                continue

            # Valor intrínseco no vencimento
            if is_call:
                intrinsic = max(s_t - strike, 0)
            else:  # PUT
                intrinsic = max(strike - s_t, 0)

            # P&L unitário
            if side == "LONG":  # Comprado
                pl_unit = intrinsic - valor_executado
            else:  # Vendido
                pl_unit = valor_executado - intrinsic

            # P&L desta perna
            pl_perna = quant * pl_unit
            pl_total += pl_perna

        points.append((s_t, pl_total))  # ordem: (point_spot, point_pl)
        pl_values.append(pl_total)
        s_t += step

    # Métricas
    pl_max = max(pl_values) if pl_values else 0
    pl_min = min(pl_values) if pl_values else 0

    return {
        "points": points,
        "pl_max": pl_max,
        "pl_min": pl_min,
        "spot_ref": spot,
        "meta": {
            "legs_count": len(legs),
            "grid_params": {"low_pct": grid_low_pct, "high_pct": grid_high_pct, "step_pct": step_pct}
        }
    }


def compute_payoff_for_aba(aba: str, timestamp: Optional[str] = None) -> Optional[Dict]:
    """
    Função principal: calcula payoff para uma aba usando dados reais.
    """
    # 1. Ler estrutura agregada (spot, etc.)
    summary = read_structure_summary(aba)
    if not summary:
        return None

    spot = safe_float(summary.get('spot'), 0)
    if spot <= 0:
        return None

    # 2. Ler pernas do snapshot correto
    legs = read_structure_legs(aba, timestamp)
    if not legs:
        return None

    # 3. Calcular payoff
    result = compute_payoff_curve(legs, spot)
    result["aba"] = aba
    result["timestamp_used"] = legs[0].get('timestamp') if legs else None

    return result


if __name__ == "__main__":
    # Teste rápido
    print("Testando payoff com dados reais...")

    # Listar abas disponíveis
    conn = connect_app()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT aba FROM rtd_analise_robo ORDER BY aba")
    abas = [row[0] for row in cursor.fetchall()]
    conn.close()

    print(f"Abas disponíveis: {abas}")

    if abas:
        test_aba = abas[0]
        result = compute_payoff_for_aba(test_aba)
        if result:
            points_count = len(result["points"])
            print(f"✅ Aba '{test_aba}': {points_count} pontos, PL_max={result['pl_max']:.2f}")
        else:
            print(f"❌ Não foi possível calcular payoff para '{test_aba}'")
