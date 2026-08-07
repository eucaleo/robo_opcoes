from __future__ import annotations

from repositories.derived_service_sql_boundary import (
    SQLITE3,
    DERIVED_SERVICE_SQL_BOUNDARY_001,
    DERIVED_SERVICE_SQL_BOUNDARY_002,
    DERIVED_SERVICE_SQL_BOUNDARY_003,
    DERIVED_SERVICE_SQL_BOUNDARY_004,
    DERIVED_SERVICE_SQL_BOUNDARY_005,
)
# services/derived_service.py
"""
alteracao_30/alteracao_57c -- Servico de persistencia de dados consolidados (payoff + decisoes).
alteracao_62           -- AbaResolverMixin extraído para repositories/_aba_resolver_mixin.py.
alteracao_65           -- get_payoff_by_aba() removida da interface pública (standalone).
"""

import inspect
import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple, Union

from db.config import connect_app
from db.derived_repo import (
    cleanup_old_decisions,
    cleanup_old_payoff_data,
    ensure_derived_tables,
    insert_payoff_points,
    insert_structure_decision,
)
from domain.refs.structure_ref import StructureRef


# ------------------------------------------------------------------
# Cache modulo-level: aba -> structure_id
# ------------------------------------------------------------------

_ABA_TO_STRUCTURE_ID: Dict[str, int] = {}
_ABA_CACHE_LOADED: bool = False


def _load_aba_cache() -> None:
    global _ABA_TO_STRUCTURE_ID, _ABA_CACHE_LOADED
    try:
        with connect_app() as conn:
            cur = conn.execute(DERIVED_SERVICE_SQL_BOUNDARY_002)
            _ABA_TO_STRUCTURE_ID = {row[1]: row[0] for row in cur.fetchall()}
    except Exception:
        _ABA_TO_STRUCTURE_ID = {}
    finally:
        _ABA_CACHE_LOADED = True


def _resolve_structure_id(aba: Optional[str]) -> Optional[int]:
    if not _ABA_CACHE_LOADED:
        _load_aba_cache()
    if not aba:
        return None
    return _ABA_TO_STRUCTURE_ID.get(aba)


def invalidate_aba_cache() -> None:
    global _ABA_CACHE_LOADED
    _ABA_CACHE_LOADED = False


# ------------------------------------------------------------------
# Helpers internos
# ------------------------------------------------------------------

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _safe_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _unwrap_ref(ref: Any) -> Optional[str]:
    """
    alteracao_57: extrai string aba de StructureRef ou passa str diretamente.
    Equivalente a _unwrap_aba do derived_repo, mas para a camada de servico.
    """
    if isinstance(ref, StructureRef):
        return ref.aba
    return _safe_str(ref)


def _resolve_storage_key(
    aba: Optional[str] = None,
    structure_id: Any = None,
    structure_name: Any = None,
    underlying_asset: Any = None,
) -> str:
    # 1. aba explícita tem prioridade máxima
    resolved_aba = _safe_str(aba)
    if resolved_aba:
        return resolved_aba

    # 2. structure_id → resolver alias_legacy_aba via cache (FIX alteracao_66)
    resolved_sid = _safe_str(structure_id)
    if resolved_sid:
        try:
            sid_int = int(resolved_sid)
            if not _ABA_CACHE_LOADED:
                _load_aba_cache()
            id_to_aba = {v: k for k, v in _ABA_TO_STRUCTURE_ID.items()}
            alias = id_to_aba.get(sid_int)
            if alias:
                return alias  # "BOVA11" em vez de "structure:7"
        except (ValueError, TypeError):
            pass
        return f"structure:{resolved_sid}"  # fallback sem alias

    # 3. fallbacks por nome/ativo
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
        "structure_id":     structure_id,
        "structure_name":   structure_name,
        "underlying_asset": underlying_asset,
        "reference_date":   reference_date,
        "input_meta":       input_meta or {},
        "storage_key":      storage_key,
    }


# ------------------------------------------------------------------
# Init
# ------------------------------------------------------------------

def init_db():
    with connect_app() as conn:
        ensure_derived_tables(conn)


# ------------------------------------------------------------------
# Payoff
# ------------------------------------------------------------------

def save_payoff_curve(
    ref: Any,
    points: List[Union[Tuple[float, float], Dict[str, float]]],
    spot_ref: Optional[float] = None,
    meta: Optional[Dict[str, Any]] = None,
    timestamp: Optional[str] = None,
    structure_id: Any = None,
) -> int:
    """
    alteracao_57: 'ref' aceita StructureRef, str ou None.
    _unwrap_ref() extrai a string aba de forma segura.
    """
    ts           = timestamp or _now_iso()
    storage_key  = _unwrap_ref(ref) or "unknown"
    resolved_sid = (
        int(structure_id)
        if structure_id is not None
        else _resolve_structure_id(storage_key)
    )

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
        "structure_id": resolved_sid,
    }

    with connect_app() as conn:
        ensure_derived_tables(conn)
        return insert_payoff_points(
            conn=conn,
            timestamp=ts,
            aba=storage_key,
            points=norm_points,
            spot_ref=spot_ref,
            meta=effective_meta,
            structure_id=resolved_sid,
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

    sid_from_payload = payoff.get("structure_id")
    resolved_sid = (
        int(sid_from_payload)
        if sid_from_payload is not None
        else _resolve_structure_id(storage_key)
    )

    meta = _merge_meta(
        meta=payoff.get("meta"),
        structure_id=resolved_sid,
        structure_name=payoff.get("structure_name"),
        underlying_asset=payoff.get("underlying_asset"),
        reference_date=payoff.get("reference_date"),
        input_meta=payoff.get("input_meta"),
        storage_key=storage_key,
    )

    try:
        sig = inspect.signature(save_payoff_curve)
        accepts_structure_id = (
            "structure_id" in sig.parameters
            or any(
                p.kind == inspect.Parameter.VAR_KEYWORD
                for p in sig.parameters.values()
            )
        )
    except (TypeError, ValueError):
        accepts_structure_id = True

    if accepts_structure_id:
        return save_payoff_curve(
            ref=storage_key,
            points=payoff.get("points", []),
            spot_ref=payoff.get("spot_ref"),
            meta=meta,
            timestamp=ts,
            structure_id=resolved_sid,
        )

    return save_payoff_curve(
        ref=storage_key,
        points=payoff.get("points", []),
        spot_ref=payoff.get("spot_ref"),
        meta=meta,
        timestamp=ts,
    )


def save_decision(
    ref: Any,
    decision: Dict[str, Any],
    timestamp: Optional[str] = None,
) -> int:
    """
    alteracao_57: 'ref' aceita StructureRef, str ou None.
    """
    ts           = timestamp or _now_iso()
    storage_key  = _unwrap_ref(ref) or "unknown"
    resolved_sid = _resolve_structure_id(storage_key)

    enriched_decision = {
        **decision,
        "structure_id": resolved_sid,
        "meta": {
            **(decision.get("meta") or {}),
            "storage_key":  storage_key,
            "structure_id": resolved_sid,
        },
    }

    # Patch 32.6: última barreira antes do insert em structure_decisions.
    if enriched_decision.get("structure_id") is None:
        sid_from_meta = (enriched_decision.get("meta") or {}).get("structure_id")
        if sid_from_meta is not None:
            enriched_decision["structure_id"] = int(sid_from_meta)

    if enriched_decision.get("structure_id") is None:
        resolved_sid = _resolve_structure_id(storage_key)
        if resolved_sid is not None:
            enriched_decision["structure_id"] = int(resolved_sid)

    # Patch 32.7: recupera structure_id do payload original antes do insert.
    if enriched_decision.get("structure_id") is None:
        _src_32_7 = locals().get("decision")
        if isinstance(_src_32_7, dict):
            _sid_32_7 = _src_32_7.get("structure_id")
            if _sid_32_7 is not None:
                enriched_decision["structure_id"] = int(_sid_32_7)

    if enriched_decision.get("structure_id") is None:
        _src_32_7 = locals().get("decision_dict")
        if isinstance(_src_32_7, dict):
            _sid_32_7 = _src_32_7.get("structure_id")
            if _sid_32_7 is not None:
                enriched_decision["structure_id"] = int(_sid_32_7)

    if enriched_decision.get("structure_id") is None:
        _src_32_7 = locals().get("decision")
        if isinstance(_src_32_7, dict):
            _meta_32_7 = _src_32_7.get("meta")
            if isinstance(_meta_32_7, dict):
                _sid_32_7 = _meta_32_7.get("structure_id")
                if _sid_32_7 is not None:
                    enriched_decision["structure_id"] = int(_sid_32_7)

    if enriched_decision.get("structure_id") is None:
        _src_32_7 = locals().get("decision_dict")
        if isinstance(_src_32_7, dict):
            _meta_32_7 = _src_32_7.get("meta")
            if isinstance(_meta_32_7, dict):
                _sid_32_7 = _meta_32_7.get("structure_id")
                if _sid_32_7 is not None:
                    enriched_decision["structure_id"] = int(_sid_32_7)

    if enriched_decision.get("structure_id") is None:
        _sid_32_7 = None
        try:
            _sid_32_7 = _resolve_structure_id(storage_key)
        except Exception:
            _sid_32_7 = None

        if _sid_32_7 is not None:
            enriched_decision["structure_id"] = int(_sid_32_7)

    if enriched_decision.get("structure_id") is not None:
        _sid_32_7 = int(enriched_decision.get("structure_id"))
        enriched_decision["structure_id"] = _sid_32_7

        _meta_32_7 = enriched_decision.get("meta")
        if not isinstance(_meta_32_7, dict):
            _meta_32_7 = {}
            enriched_decision["meta"] = _meta_32_7

        _meta_32_7["structure_id"] = _sid_32_7

    with connect_app() as conn:
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

    resolved_sid = (
        int(structure_id)
        if structure_id is not None
        else _resolve_structure_id(storage_key)
    )

    enriched_decision = {
        **decision,
        "structure_id": resolved_sid,
        "meta": {
            **(decision.get("meta") or {}),
            "structure_id":     resolved_sid,
            "structure_name":   structure_name,
            "underlying_asset": underlying_asset,
            "storage_key":      storage_key,
        },
    }

    # Patch 32.6: garante structure_id no topo antes de delegar para save_decision.
    if enriched_decision.get("structure_id") is None and structure_id is not None:
        enriched_decision["structure_id"] = int(structure_id)

    if enriched_decision.get("structure_id") is None:
        sid_from_meta = (enriched_decision.get("meta") or {}).get("structure_id")
        if sid_from_meta is not None:
            enriched_decision["structure_id"] = int(sid_from_meta)

    if enriched_decision.get("structure_id") is None:
        resolved_sid = _resolve_structure_id(storage_key)
        if resolved_sid is not None:
            enriched_decision["structure_id"] = int(resolved_sid)

    # Patch 32.7: espelha structure_id no meta antes de delegar para save_decision.
    if enriched_decision.get("structure_id") is not None:
        _sid_32_7 = int(enriched_decision.get("structure_id"))
        enriched_decision["structure_id"] = _sid_32_7

        _meta_32_7 = enriched_decision.get("meta")
        if not isinstance(_meta_32_7, dict):
            _meta_32_7 = {}
            enriched_decision["meta"] = _meta_32_7

        _meta_32_7["structure_id"] = _sid_32_7

    return save_decision(
        ref=storage_key,
        decision=enriched_decision,
        timestamp=ts,
    )


# ------------------------------------------------------------------
# Cleanup
# ------------------------------------------------------------------

def cleanup_derived(days_to_keep: int = 30) -> Dict[str, int]:
    with connect_app() as conn:
        ensure_derived_tables(conn)
        deleted_payoff = cleanup_old_payoff_data(conn, days_to_keep=days_to_keep)
        deleted_dec    = cleanup_old_decisions(conn, days_to_keep=days_to_keep)
        return {"payoff_deleted": deleted_payoff, "decisions_deleted": deleted_dec}


# ------------------------------------------------------------------
# Leituras
# ------------------------------------------------------------------

def get_all_payoff_curves():
    with connect_app() as conn:
        cursor = conn.cursor()
        cursor.execute(DERIVED_SERVICE_SQL_BOUNDARY_001)
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


def get_payoff_by_structure_id(structure_id: int):
    """
    alteracao_56/alteracao_65: único ponto de entrada canônico para leitura de payoff.
    get_payoff_by_aba() removida da interface pública (alteracao_65).
    """
    ref = StructureRef.from_id(structure_id)
    col, val = ref.db_pair()
    with connect_app() as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""DERIVED_SERVICE_SQL_BOUNDARY_003{col} = ?
             ORDER BY point_spot
            """,
            (val,),
        )
        return [
            {
                "timestamp":  row[0],
                "point_spot": row[1],
                "point_pl":   row[2],
                "meta_json":  json.loads(row[3]) if row[3] else None,
            }
            for row in cursor.fetchall()
        ]


def get_recent_decisions():
    with connect_app() as conn:
        conn.row_factory = SQLITE3.Row
        cursor = conn.cursor()

        cols = [
            row["name"]
            for row in cursor.execute(
                DERIVED_SERVICE_SQL_BOUNDARY_005
            ).fetchall()
        ]

        select_cols = [
            "timestamp", "aba", "decision", "level",
            "pl_atual", "pl_max", "pl_pct_of_max", "dte_min",
            "spot_ref", "meta_json", "created_at",
        ]
        if "structure_id" in cols:
            select_cols.append("structure_id")
        if "why" in cols:
            select_cols.append("why")
        if "why_json" in cols:
            select_cols.append("why_json")

        cursor.execute(f"""DERIVED_SERVICE_SQL_BOUNDARY_004{", ".join(select_cols)}
            FROM structure_decisions
            ORDER BY timestamp DESC
            LIMIT 50
        """)

        decisions = []
        for row in cursor.fetchall():
            item = dict(row)
            why_val      = item.get("why")
            why_json_val = item.get("why_json")

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


# ---------------------------------------------------------------------------
# alteracao_59 -- format_report + snapshot_aba (surface canônica)
# ---------------------------------------------------------------------------

def format_report(entries) -> str:
    """Formata relatório de auditoria de surface ABA em texto legível."""
    lines: list[str] = []
    for e in entries:
        aba_str = getattr(e, "aba_str", str(getattr(e, "structure_id", "")))
        sid     = getattr(e, "structure_id", "?")
        ref     = getattr(e, "reference_date", "?")
        lines.append(f"{sid} | {ref} | {aba_str}")
    return "\n".join(lines)


def snapshot_aba(ref: "StructureRef") -> str:
    """Retorna aba_str canônico a partir de um StructureRef."""
    aba_str = ref.aba if hasattr(ref, "aba") and ref.aba else str(ref.structure_id)
    return aba_str


# ------------------------------------------------------------------
# alteracao_65 -- DerivedService: fachada orientada a objetos
# get_payoff_by_aba() removida da interface pública.
# get_payoff_by_structure_id() é o único ponto de entrada canônico.
# ------------------------------------------------------------------

class DerivedService:
    """Fachada OO sobre as funcoes standalone do derived_service.
    alteracao_65: get_payoff_by_aba() nao exposta -- use get_payoff_by_structure_id().
    get_payoff_by_aba() ausente por decisao de design (alteracao_65): interface simplificada.
    """

    # alteracao_65: get_payoff_by_aba() deliberadamente nao implementada nesta classe.
    # Chamadores legados devem migrar para get_payoff_by_structure_id().

    def save_decision(self, *args, **kwargs):
        return save_decision(*args, **kwargs)

    def cleanup_derived(self, days_to_keep: int = 30):
        return cleanup_derived(days_to_keep)
