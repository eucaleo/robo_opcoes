# derived_service.py
import sqlite3
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Any, Tuple, Union

from db.config import connect_app, connect_derived
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
    with connect_derived() as conn:
        ensure_derived_tables(conn)

def save_payoff_curve(
    aba: str,
    points: List[Union[Tuple[float, float], Dict[str, float]]],
    spot_ref: Optional[float] = None,
    meta: Optional[Dict[str, Any]] = None,
    timestamp: Optional[str] = None,
) -> int:
    """
    Salva pontos da curva de payoff suportando múltiplos formatos:
    - Tuplas/listas: (spot, pl) ou [spot, pl]
    - Dicts novos: {"point_spot": x, "point_pl": y}
    - Dicts legados: {"s_t": x, "pl_venc": y}
    """
    ts = timestamp or _now_iso()

    norm_points: List[Tuple[float, float]] = []
    for p in points or []:
        if isinstance(p, (tuple, list)) and len(p) == 2:
            norm_points.append((float(p[0]), float(p[1])))
        elif isinstance(p, dict):
            # Tenta primeiro os nomes novos
            x = p.get("point_spot")
            y = p.get("point_pl")
            
            # Se não encontrou, tenta os nomes legados
            if x is None:
                x = p.get("s_t")
            if y is None:
                y = p.get("pl_venc")
            
            # Se ainda não tem os dois valores, pula este ponto
            if x is None or y is None:
                continue
                
            norm_points.append((float(x), float(y)))

    with connect_derived() as conn:
        ensure_derived_tables(conn)
        return insert_payoff_points(
            conn=conn,
            timestamp=ts,
            aba=aba,
            points=norm_points,
            spot_ref=spot_ref,
            meta=meta,
        )

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
    with connect_derived() as conn:
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
    with connect_derived() as conn:
        ensure_derived_tables(conn)
        deleted_payoff = cleanup_old_payoff_data(conn, days_to_keep=days_to_keep)
        deleted_dec = cleanup_old_decisions(conn, days_to_keep=days_to_keep)
        return {"payoff_deleted": deleted_payoff, "decisions_deleted": deleted_dec}
def _get_canonical_snapshot_ts(self, aba: str) -> str | None:
    con = connect_app()
    try:
        cur = con.cursor()

        def has_table(name: str) -> bool:
            cur.execute(
                "SELECT 1 FROM sqlite_master WHERE type='table' AND name=? LIMIT 1",
                (name,)
            )
            return cur.fetchone() is not None

        # prioridade: manual primeiro (se existir)
        for table in ("manual_analise_robo_legs", "robo_legs_snapshot", "robo_snapshot", "rtd_analise_robo_legs"):
            if has_table(table):
                cur.execute(f"SELECT MAX(timestamp) FROM {table} WHERE aba=?", (aba,))
                row = cur.fetchone()
                if row and row[0]:
                    return str(row[0])

        return None
    finally:
        con.close()



def get_all_payoff_curves():
    """
    Recupera todas as curvas de payoff salvas da tabela payoff_curve_points
    """
    with connect_derived() as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT timestamp, aba, point_spot, point_pl, meta_json
            FROM payoff_curve_points 
            ORDER BY timestamp DESC, point_spot
        """)
        
        results = cursor.fetchall()
        
        return [
            {
                'timestamp': row[0],
                'aba': row[1],
                'point_spot': row[2],
                'point_pl': row[3],
                'meta_json': json.loads(row[4]) if row[4] else None
            }
            for row in results
        ]

def get_payoff_by_aba(aba: str):
    """
    Recupera payoffs de uma aba específica
    """
    with connect_derived() as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT timestamp, point_spot, point_pl, meta_json
            FROM payoff_curve_points 
            WHERE aba = ?
            ORDER BY point_spot
        """, (aba,))
        
        results = cursor.fetchall()
        
        return [
            {
                'timestamp': row[0],
                'point_spot': row[1],
                'point_pl': row[2],
                'meta_json': json.loads(row[3]) if row[3] else None
            }
            for row in results
        ]

def get_recent_decisions():
    """
    Recupera decisões recentes da tabela structure_decisions
    """
    with connect_derived() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT timestamp, aba, decision, level, pl_atual, pl_max, pl_pct_of_max, dte_min, why_json, spot_ref, meta_json, created_at
            FROM structure_decisions
            ORDER BY timestamp DESC
            LIMIT 50
        """)
        results = cursor.fetchall()
        
        colunas = [
            'timestamp', 'aba', 'decision', 'level', 'pl_atual', 'pl_max', 'pl_pct_of_max', 
            'dte_min', 'why_json', 'spot_ref', 'meta_json', 'created_at'
        ]
        return [dict(zip(colunas, row)) for row in results]

def insert_consolidacao_close_reopen(
    aba: str,
    timestamp: str,
    pl_atual: float,
    pl_max: float,
    ratio: float,
    db_path: Optional[str] = None
):
    if db_path is None:
        db_path = str(APP_DB_PATH)
    """
    Insere linha padronizada em rtd_consolidacoes para CLOSE_REOPEN
    """
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
