# derived_service.py
import sqlite3
import json
from typing import List, Dict, Optional, Any, Tuple, Union

from db.config import connect_derived
from db.derived_repo import (
    ensure_derived_tables,
    insert_payoff_points,
    insert_structure_decision,
    cleanup_old_payoff_data,
    cleanup_old_decisions,
)


def _now_iso() -> str:
    from datetime import datetime
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
            x = p.get("point_spot")
            y = p.get("point_pl")

            if x is None:
                x = p.get("s_t")
            if y is None:
                y = p.get("pl_venc")

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
                "timestamp": row[0],
                "aba": row[1],
                "point_spot": row[2],
                "point_pl": row[3],
                "meta_json": json.loads(row[4]) if row[4] else None,
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
                "timestamp": row[0],
                "point_spot": row[1],
                "point_pl": row[2],
                "meta_json": json.loads(row[3]) if row[3] else None,
            }
            for row in results
        ]


def get_recent_decisions():
    """
    Recupera decisões recentes da tabela structure_decisions.
    Prioriza 'why' e mantém fallback para 'why_json'.
    """
    with connect_derived() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cols = [
            row["name"]
            for row in cursor.execute("PRAGMA table_info(structure_decisions)").fetchall()
        ]

        select_cols = [
            "timestamp", "aba", "decision", "level",
            "pl_atual", "pl_max", "pl_pct_of_max", "dte_min",
            "spot_ref", "meta_json", "created_at",
        ]
        if "why" in cols:
            select_cols.append("why")
        if "why_json" in cols:
            select_cols.append("why_json")

        cursor.execute(
            f"""
            SELECT {", ".join(select_cols)}
            FROM structure_decisions
            ORDER BY timestamp DESC
            LIMIT 50
            """
        )
        results = cursor.fetchall()

        decisions = []
        for row in results:
            item = dict(row)

            why_val = item.get("why")
            why_json_val = item.get("why_json")

            if isinstance(why_val, str):
                try:
                    item["why"] = json.loads(why_val)
                except Exception:
                    pass
            elif why_val is None and why_json_val is not None:
                try:
                    item["why"] = json.loads(why_json_val) if isinstance(why_json_val, str) else why_json_val
                except Exception:
                    item["why"] = why_json_val

            decisions.append(item)

        return decisions
