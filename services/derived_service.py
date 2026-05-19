# derived_service.py
import json
import sqlite3
from typing import Any, Dict, List, Optional, Tuple, Union

from db.config import connect_derived
from db.derived_repo import (
    cleanup_old_decisions,
    cleanup_old_payoff_data,
    ensure_derived_tables,
    insert_payoff_points,
    insert_structure_decision,
)


def _now_iso() -> str:
    from datetime import datetime
    return datetime.now().isoformat()


def _safe_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _resolve_storage_key(
    aba: Optional[str] = None,
    structure_id: Any = None,
    structure_name: Any = None,
    underlying_asset: Any = None,
) -> str:
    resolved_aba = _safe_str(aba)
    if resolved_aba:
        return resolved_aba

    resolved_structure_id = _safe_str(structure_id)
    if resolved_structure_id:
        return f"structure:{resolved_structure_id}"

    resolved_structure_name = _safe_str(structure_name)
    if resolved_structure_name:
        return resolved_structure_name

    resolved_underlying_asset = _safe_str(underlying_asset)
    if resolved_underlying_asset:
        return resolved_underlying_asset

    return "unknown"


def _merge_meta(
    meta: Optional[Dict[str, Any]] = None,
    structure_id: Any = None,
    structure_name: Any = None,
    underlying_asset: Any = None,
    reference_date: Any = None,
    input_meta: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    return {
        **(meta or {}),
        "structure_id": structure_id,
        "structure_name": structure_name,
        "underlying_asset": underlying_asset,
        "reference_date": reference_date,
        "input_meta": input_meta or {},
    }


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


def save_payoff_from_canonical_payload(
    payoff: Dict[str, Any],
    aba: Optional[str] = None,
    timestamp: Optional[str] = None,
) -> int:
    ts = timestamp or _now_iso()

    storage_key = _resolve_storage_key(
        aba=aba,
        structure_id=payoff.get("structure_id"),
        structure_name=payoff.get("structure_name"),
        underlying_asset=payoff.get("underlying_asset"),
    )

    meta = _merge_meta(
        meta=payoff.get("meta"),
        structure_id=payoff.get("structure_id"),
        structure_name=payoff.get("structure_name"),
        underlying_asset=payoff.get("underlying_asset"),
        reference_date=payoff.get("reference_date"),
        input_meta=payoff.get("input_meta"),
    )

    return save_payoff_curve(
        aba=storage_key,
        points=payoff.get("points", []),
        spot_ref=payoff.get("spot_ref"),
        meta=meta,
        timestamp=ts,
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
            decision_dict=decision,
        )


def save_decision_from_canonical_payload(
    decision: Dict[str, Any],
    structure_id: Any = None,
    structure_name: Any = None,
    underlying_asset: Any = None,
    aba: Optional[str] = None,
    timestamp: Optional[str] = None,
) -> int:
    ts = timestamp or _now_iso()

    storage_key = _resolve_storage_key(
        aba=aba,
        structure_id=structure_id,
        structure_name=structure_name,
        underlying_asset=underlying_asset,
    )

    enriched_decision = {
        **decision,
        "meta": {
            **(decision.get("meta") or {}),
            "structure_id": structure_id,
            "structure_name": structure_name,
            "underlying_asset": underlying_asset,
        },
    }

    return save_decision(
        aba=storage_key,
        decision=enriched_decision,
        timestamp=ts,
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
