#derived_service.py
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Any, Tuple, Union

from db.config import get_connection
from db.derived_repo import (
    ensure_derived_tables,
    insert_payoff_points,
    insert_structure_decision,
    cleanup_old_payoff_data,
    cleanup_old_decisions,
)

def _now_iso() -> str:
    return datetime.now().isoformat()

def init_db():
    with get_connection() as conn:
        ensure_derived_tables(conn)

def save_payoff_curve(
    aba: str,
    points: List[Union[Tuple[float, float], Dict[str, float]]],
    spot_ref: Optional[float] = None,
    meta: Optional[Dict[str, Any]] = None,
    timestamp: Optional[str] = None,
) -> int:
    ts = timestamp or _now_iso()

    norm_points: List[Tuple[float, float]] = []
    for p in points or []:
        if isinstance(p, (tuple, list)) and len(p) == 2:
            norm_points.append((float(p[0]), float(p[1])))
        elif isinstance(p, dict):
            x = p.get("point_spot")
            y = p.get("point_pl")
            if x is None or y is None:
                continue
            norm_points.append((float(x), float(y)))

    with get_connection() as conn:
        ensure_derived_tables(conn)
        return insert_payoff_points(
            conn=conn,
            timestamp=ts,
            aba=aba,
            points=norm_points,
            spot_ref=spot_ref,
            meta=meta,
        )
def insert_payoff_points(
    conn: sqlite3.Connection,
    timestamp: str,
    aba: str,
    points: List[Union[Tuple[float, float], Dict[str, float]]],
    spot_ref: Optional[float] = None,
    meta: Optional[Dict[str, Any]] = None
) -> int:
    ensure_derived_tables(conn)

    meta_json = json.dumps(meta) if meta else None
    cursor = conn.cursor()
    count = 0

    for p in points or []:
        if isinstance(p, (tuple, list)) and len(p) == 2:
            s_t, pl_venc = float(p[0]), float(p[1])
        elif isinstance(p, dict):
            s_t = p.get("s_t", p.get("point_spot"))
            pl_venc = p.get("pl_venc", p.get("point_pl"))
            if s_t is None or pl_venc is None:
                continue
            s_t, pl_venc = float(s_t), float(pl_venc)
        else:
            continue

        cursor.execute("""
            INSERT INTO payoff_curve_points
            (timestamp, aba, s_t, pl_venc, spot_ref, meta_json)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (timestamp, aba, s_t, pl_venc, spot_ref, meta_json))
        count += 1

    conn.commit()
    return count

def save_decision(
    aba: str,
    decision: Dict[str, Any],
    timestamp: Optional[str] = None,
) -> int:
    """
    Grava uma decisão para a estrutura.
    decision: dict com chaves como decision, level, pl_atual, etc.
    """
    ts = timestamp or _now_iso()
    with get_connection() as conn:
        ensure_derived_tables(conn)
        return insert_structure_decision(
            conn=conn,
            timestamp=ts,
            aba=aba,
            decision_dict=decision
        )

def cleanup_derived(days_to_keep: int = 30) -> Dict[str, int]:
    """
    Limpa dados antigos (com base em 'timestamp') nas duas tabelas.
    """
    with get_connection() as conn:
        ensure_derived_tables(conn)
        deleted_payoff = cleanup_old_payoff_data(conn, days_to_keep=days_to_keep)
        deleted_dec = cleanup_old_decisions(conn, days_to_keep=days_to_keep)
        return {"payoff_deleted": deleted_payoff, "decisions_deleted": deleted_dec}

def get_all_payoff_curves():
    """Recupera todas as curvas de payoff salvas"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, underlying_price, payoff_value, strategy_type, created_at
        FROM payoff_points 
        ORDER BY created_at DESC, underlying_price
    """)
    
    results = cursor.fetchall()
    conn.close()
    
    return [
        {
            'id': row[0],
            'underlying_price': row[1], 
            'payoff_value': row[2],
            'strategy_type': row[3],
            'created_at': row[4]
        }
        for row in results
    ]

def get_payoff_by_strategy(strategy_type: str):
    """Recupera payoffs de uma estratégia específica"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT underlying_price, payoff_value, created_at
        FROM payoff_points 
        WHERE strategy_type = ?
        ORDER BY underlying_price
    """, (strategy_type,))
    
    results = cursor.fetchall()
    conn.close()
    
    return [
        {
            'underlying_price': row[0],
            'payoff_value': row[1],
            'created_at': row[2]
        }
        for row in results
    ]

def get_recent_decisions():
    """Recupera decisões recentes da tabela structure_decisions"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, timestamp, aba, decision, ratio, dte_min, pl_atual, pl_max, pl_min, spread_pct_medio, why_json, created_at
        FROM structure_decisions
        ORDER BY timestamp DESC
        LIMIT 50
    """)
    results = cursor.fetchall()
    conn.close()
    # Se quiser um dicionário:
    colunas = [
        'id', 'timestamp', 'aba', 'decision', 'ratio', 'dte_min', 'pl_atual',
        'pl_max', 'pl_min', 'spread_pct_medio', 'why_json', 'created_at'
    ]
    return [dict(zip(colunas, row)) for row in results]

def insert_consolidacao_close_reopen(
    aba: str,
    timestamp: str,
    pl_atual: float,
    pl_max: float,
    ratio: float,
    db_path: str = "Data/app.db"
):
    """Insere linha padronizada em rtd_consolidacoes para CLOSE_REOPEN"""
    obs = f"CLOSE_REOPEN: PL_atual={pl_atual:.2f}, PL_max={pl_max:.2f}, Ratio={ratio:.3%}"
    row = (
        timestamp,
        aba,
        "", "", "", "", "", "",  # campos opcionais
        obs
    )
    conn = sqlite3.connect(str(Path(db_path).resolve()))
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO rtd_consolidacoes (
            timestamp, aba, pernas_abertas, total_executado_aberto,
            total_atual_aberto, ganho_atual_aberto, pl_realizado, pl_total, obs
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, row)
    conn.commit()
    conn.close()

