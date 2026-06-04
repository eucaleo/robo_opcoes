# services/derived_service.py
"""
Serviço de persistência de dados derivados (payoff + decisões).

patch_30: _resolve_structure_id() resolve aba  structure_id via app.db
          com cache em memória (uma leitura por processo).
          Todas as funções de escrita enriquecem automaticamente
          os registros com structure_id antes do INSERT.
"""

from src.domain.refs.structure_ref import StructureRef
import json
import sqlite3
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple, Union

from db.config import connect_app, connect_derived
from db.derived_repo import (
    cleanup_old_decisions,
    cleanup_old_payoff_data,
    ensure_derived_tables,
    insert_payoff_points,
    insert_structure_decision,
)


# 
# Cache módulo-level: aba  structure_id
# Carregado uma única vez por processo (lazy, thread-safe p/ GIL)
# 

_ABA_TO_STRUCTURE_ID: Dict[str, int] = {}
_ABA_CACHE_LOADED: bool = False


def _load_aba_cache() -> None:
    """
    Lê structures.alias_legacy_aba  id do app.db e popula o cache.
    Silencia erros: se app.db não existir, cache fica vazio
    e structure_id permanece NULL (comportamento anterior).
    """
    global _ABA_TO_STRUCTURE_ID, _ABA_CACHE_LOADED

    try:
        with connect_app() as conn:
            cur = conn.execute("""
                SELECT id, alias_legacy_aba
                FROM structures
                WHERE alias_legacy_aba IS NOT NULL
                  AND alias_legacy_aba != ''
            """)
            _ABA_TO_STRUCTURE_ID = {row[1]: row[0] for row in cur.fetchall()}
    except Exception:
        _ABA_TO_STRUCTURE_ID = {}
    finally:
        _ABA_CACHE_LOADED = True


def _resolve_structure_id(aba: Optional[str]) -> Optional[int]:
    """
    Retorna structure_id para a aba dada, ou None se não mapeada.
    O cache é carregado na primeira chamada (lazy init).
    """
    if not _ABA_CACHE_LOADED:
        _load_aba_cache()

    if not aba:
        return None

    return _ABA_TO_STRUCTURE_ID.get(aba)


def invalidate_aba_cache() -> None:
    """
    Força recarga do cache na próxima chamada.
    Útil em testes ou após inserção de nova structure em app.db.
    """
    global _ABA_CACHE_LOADED
    _ABA_CACHE_LOADED = False


# 
# Helpers internos (inalterados)
# 

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


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
    storage_key: Optional[str] = None,
) -> Dict[str, Any]:
    return {
        **(meta or {}),
        "structure_id": structure_id,
        "structure_name": structure_name,
        "underlying_asset": underlying_asset,
        "reference_date": reference_date,
        "input_meta": input_meta or {},
        "storage_key": storage_key,
    }


# 
# Init
# 

def init_db():
    with connect_derived() as conn:
        ensure_derived_tables(conn)


# 
# Payoff
# 

def save_payoff_curve(
    ref: StructureRef,
    points: List[Union[Tuple[float, float], Dict[str, float]]],
    spot_ref: Optional[float] = None,
    meta: Optional[Dict[str, Any]] = None,
    timestamp: Optional[str] = None,
) -> int:
    ts = timestamp or _now_iso()
    storage_key = _safe_str(aba) or "unknown"

    # patch_30: enriquece meta com structure_id resolvido
    resolved_sid = _resolve_structure_id(storage_key)

    norm_points: List[Tuple[float, float]] = []
    for p in points or []:
        if isinstance(p, (tuple, list)) and len(p) == 2:
            norm_points.append((float(p[0]), float(p[1])))
        elif isinstance(p, dict):
            x = p.get("point_spot") or p.get("s_t")
            y = p.get("point_pl")   or p.get("pl_venc")
            if x is None or y is None:
                continue
            norm_points.append((float(x), float(y)))

    effective_meta = {
        **(meta or {}),
        "storage_key":  storage_key,
        "structure_id": resolved_sid,   #  patch_30
    }

    with connect_derived() as conn:
        ensure_derived_tables(conn)
        return insert_payoff_points(
            conn=conn,
            timestamp=ts,
            aba=storage_key,
            points=norm_points,
            spot_ref=spot_ref,
            meta=effective_meta,
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

    # patch_30: prefere structure_id do payload; fallback para cache
    sid_from_payload = payoff.get("structure_id")
    resolved_sid = (
        int(sid_from_payload)
        if sid_from_payload is not None
        else _resolve_structure_id(storage_key)
    )

    meta = _merge_meta(
        meta=payoff.get("meta"),
        structure_id=resolved_sid,          #  patch_30
        structure_name=payoff.get("structure_name"),
        underlying_asset=payoff.get("underlying_asset"),
        reference_date=payoff.get("reference_date"),
        input_meta=payoff.get("input_meta"),
        storage_key=storage_key,
    )

    return save_payoff_curve(
        aba=storage_key,
        points=payoff.get("points", []),
        spot_ref=payoff.get("spot_ref"),
        meta=meta,
        timestamp=ts,
    )


# 
# Decisões
# 

def save_decision(
    ref: StructureRef,
    decision: Dict[str, Any],
    timestamp: Optional[str] = None,
) -> int:
    ts = timestamp or _now_iso()
    storage_key = _safe_str(aba) or "unknown"

    # patch_30: resolve structure_id e injeta na decisão
    resolved_sid = _resolve_structure_id(storage_key)

    enriched_decision = {
        **decision,
        "structure_id": resolved_sid,       #  patch_30
        "meta": {
            **(decision.get("meta") or {}),
            "storage_key":  storage_key,
            "structure_id": resolved_sid,   #  patch_30 (espelhado em meta)
        },
    }

    with connect_derived() as conn:
        ensure_derived_tables(conn)
        return insert_structure_decision(
            conn=conn,
            timestamp=ts,
            aba=storage_key,
            decision_dict=enriched_decision,
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

    # patch_30: prefere structure_id do argumento; fallback para cache
    resolved_sid = (
        int(structure_id)
        if structure_id is not None
        else _resolve_structure_id(storage_key)
    )

    enriched_decision = {
        **decision,
        "structure_id": resolved_sid,       #  patch_30
        "meta": {
            **(decision.get("meta") or {}),
            "structure_id":   resolved_sid, #  patch_30
            "structure_name": structure_name,
            "underlying_asset": underlying_asset,
            "storage_key":    storage_key,
        },
    }

    return save_decision(
        aba=storage_key,
        decision=enriched_decision,
        timestamp=ts,
    )


# 
# Cleanup
# 

def cleanup_derived(days_to_keep: int = 30) -> Dict[str, int]:
    with connect_derived() as conn:
        ensure_derived_tables(conn)
        deleted_payoff = cleanup_old_payoff_data(conn, days_to_keep=days_to_keep)
        deleted_dec    = cleanup_old_decisions(conn, days_to_keep=days_to_keep)
        return {"payoff_deleted": deleted_payoff, "decisions_deleted": deleted_dec}


# 
# Leituras (inalteradas)
# 

def get_all_payoff_curves():
    with connect_derived() as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT timestamp, aba, point_spot, point_pl, meta_json
            FROM payoff_curve_points
            ORDER BY timestamp DESC, point_spot
        """)
        return [
            {
                "timestamp":  row[0],
                "aba":        row[1],
                "point_spot": row[2],
                "point_pl":   row[3],
                "meta_json":  json.loads(row[4]) if row[4] else None,
            }
            for row in cursor.fetchall()
        ]


def get_payoff_by_aba(ref: StructureRef):
    col, val = ref.db_pair()  # patch_56
    with connect_derived() as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT timestamp, point_spot, point_pl, meta_json
            FROM payoff_curve_points
            WHERE {col} = ?
            ORDER BY point_spot
        """, (val,))
        return [
            {
                "timestamp":  row[0],
                "point_spot": row[1],
                "point_pl":   row[2],
                "meta_json":  json.loads(row[3]) if row[3] else None,
            }
            for row in cursor.fetchall()
        ]




def get_payoff_by_structure_id(structure_id: int):
    """
    patch_56: constrói StructureRef.from_id() em vez de resolver aba via cache.
    """
    ref = StructureRef.from_id(structure_id)
    return get_payoff_by_aba(ref)


def get_recent_decisions():
    with connect_derived() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cols = [
            row["name"]
            for row in cursor.execute(
                "PRAGMA table_info(structure_decisions)"
            ).fetchall()
        ]

        select_cols = [
            "timestamp", "aba", "decision", "level",
            "pl_atual", "pl_max", "pl_pct_of_max", "dte_min",
            "spot_ref", "meta_json", "created_at",
        ]
        if "structure_id" in cols:
            select_cols.append("structure_id")   #  patch_30
        if "why" in cols:
            select_cols.append("why")
        if "why_json" in cols:
            select_cols.append("why_json")

        cursor.execute(f"""
            SELECT {", ".join(select_cols)}
            FROM structure_decisions
            ORDER BY timestamp DESC
            LIMIT 50
        """)

        decisions = []
        for row in cursor.fetchall():
            item = dict(row)
            why_val      = item.get("why")
            why_json_val = item.get("why_json")

            # 1. desserializa why / why_json
            if isinstance(why_val, str):
                try:
                    item["why"] = json.loads(why_val)
                except Exception:
                    pass
            elif why_val is None and why_json_val is not None:
                try:
                    item["why"] = (
                        json.loads(why_json_val)
                        if isinstance(why_json_val, str)
                        else why_json_val
                    )
                except Exception:
                    item["why"] = why_json_val

            # 2. promove structure_id para o topo do dict
            #    (coluna física ausente  busca em why_json / meta_json)
            if item.get("structure_id") is None:
                for src_key in ("why_json", "meta_json"):
                    raw = item.get(src_key)
                    if not raw:
                        continue
                    try:
                        parsed = json.loads(raw) if isinstance(raw, str) else raw
                        sid = parsed.get("structure_id")
                        if sid is not None:
                            item["structure_id"] = sid
                            break
                    except Exception:
                        pass

            decisions.append(item)

        return decisions