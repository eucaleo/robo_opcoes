from datetime import datetime
from typing import List, Dict, Optional, Any

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
    points: List[Dict[str, float]],
    spot_ref: Optional[float] = None,
    meta: Optional[Dict[str, Any]] = None,
    timestamp: Optional[str] = None,
) -> int:
    """
    Grava pontos de payoff (s_t, pl_venc) para uma aba/estrutura.
    """
    ts = timestamp or _now_iso()
    with get_connection() as conn:
        ensure_derived_tables(conn)
        return insert_payoff_points(
            conn=conn,
            timestamp=ts,
            aba=aba,
            points=points,
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
