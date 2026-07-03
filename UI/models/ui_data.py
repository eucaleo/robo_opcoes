# UI/models/ui_data.py
# alteracao_36_E: eliminar self._conn compartilhada
# Toda conexao de leitura passa a ser por chamada (igual a _connect_derived_threadsafe)
from src.domain.refs.structure_ref import StructureRef
import sqlite3
from sqlite3 import Row
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from db.config import DERIVED_DB_PATH
import json
import csv
from datetime import datetime

from repositories.ui_data_table_candidates import (
    CANDIDATE_CONSOLIDATION_TABLES,
    CANDIDATE_PAYOFF_TABLES,
)

# Mapeamento de colunas preferidas -> alternativas
COLUMN_ALIASES = {
    "timestamp":     ["timestamp", "ts", "decided_at", "dt_ref"],
    "structure_id":  ["structure_id"],                              #  alteracao_33: chave canônica
    "aba":           ["aba", "sheet", "tab"],                       # mantido para compat
    "decision":      ["decision", "decisao", "action"],
    "level":         ["level", "nivel", "severity_level"],
    "pl_pct_of_max": ["pl_pct_of_max", "pl_ratio", "pl_pct"],
    "ratio":         ["ratio", "pl_ratio", "pl_pct_of_max", "pl_pct"],
    "dte_min":       ["dte_min", "dte", "days_to_expiry"],
    "why":           ["why", "rationale", "rationale_json"],
    "why_json":      ["why_json", "meta_json"],
    "pl_atual":      ["pl_atual", "pl_current"],
    "pl_max":        ["pl_max", "pl_best", "pl_top"],
    "spot_ref":      ["spot_ref", "spot_reference", "ref_spot"],
}

PAYOFF_COLUMN_ALIASES = {
    "timestamp": ["timestamp", "ts", "dt_ref"],
    "structure_id": ["structure_id"],   #  alteracao_33
    "spot":      ["point_spot", "spot", "underlying", "x", "s_t"],
    "pl":        ["point_pl", "pl", "pl_value", "y", "payoff", "pl_venc"],
}

def _first_match(cols: List[str], candidates: List[str]) -> Optional[str]:
    for c in candidates:
        if c in cols:
            return c
    return None

class UIDataModel:
    def __init__(self, derived_db_path: Optional[Path] = None):
        from db.config import DERIVED_DB_PATH
        self.derived_db_path = (
            Path(derived_db_path).resolve()
            if derived_db_path
            else Path(DERIVED_DB_PATH).resolve()
        )
        print(f"[UI] Usando derived DB: {self.derived_db_path}")

        # alteracao_36_E: self._conn REMOVIDO -- cada metodo abre sua propria conexao
        self._consolidations_table: Optional[str] = None
        self._payoff_table: Optional[str] = None
        self._consolidations_cols: Dict[str, str] = {}
        self._payoff_cols: Dict[str, str] = {}
        self._cache_structures: List[str] = []

        self._payoff_cache: Dict[Tuple[str, str], Dict[str, Any]] = {}
        self._payoff_cache_max = 128

    # alteracao_36_E: _connect agora e sempre uma nova conexao por chamada
    def _connect(self) -> sqlite3.Connection:
        if not self.derived_db_path.exists():
            raise FileNotFoundError(
                f"Banco derived.db nao encontrado em: {self.derived_db_path}"
            )
        conn = sqlite3.connect(str(self.derived_db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def _list_tables(self) -> List[str]:
        # alteracao_36_E: abre e fecha conexao local
        conn = self._connect()
        try:
            cur = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
            return [r["name"] for r in cur.fetchall()]
        finally:
            conn.close()

    def _detect_tables(self):
        tables = self._list_tables()
        for t in CANDIDATE_CONSOLIDATION_TABLES:
            if t in tables:
                self._consolidations_table = t
                break
        if not self._consolidations_table:
            raise RuntimeError(
                "Tabela de consolidações não encontrada. Esperadas: "
                + ", ".join(CANDIDATE_CONSOLIDATION_TABLES)
            )
        for t in CANDIDATE_PAYOFF_TABLES:
            if t in tables:
                self._payoff_table = t
                break

    def _inspect_columns(self, table: str) -> List[str]:
        # alteracao_36_E: abre e fecha conexao local
        conn = self._connect()
        try:
            cur = conn.execute(f"PRAGMA table_info({table})")
            return [r["name"] for r in cur.fetchall()]
        finally:
            conn.close()

    def _build_consolidations_colmap(self):
        cols = self._inspect_columns(self._consolidations_table)
        colmap = {}
        for alias, candidates in COLUMN_ALIASES.items():
            m = _first_match(cols, candidates)
            if m:
                colmap[alias] = m
        self._consolidations_cols = colmap

    def _build_payoff_colmap(self):
        if not self._payoff_table:
            self._payoff_cols = {}
            return

        cols = self._inspect_columns(self._payoff_table)
        colmap = {}

        if self._payoff_table == "payoff_curve_points":
            aliases = {
                "spot":         ["point_spot"],
                "pl":           ["point_pl"],
                "timestamp":    ["timestamp"],
                # alteracao_36_F: structure_id e opcional aqui --
                # pode nao existir ainda se a migration ainda nao rodou.
                # _structure_filter_col vai lancar RuntimeError com mensagem clara.
                "structure_id": ["structure_id"],   #  alteracao_34: único identificador canônico
            }
            print(f"[UI] Usando contrato canônico para {self._payoff_table}")
        else:
            aliases = PAYOFF_COLUMN_ALIASES
            print(f"[UI] Usando aliases flexíveis para {self._payoff_table}")

        for alias, candidates in aliases.items():
            m = _first_match(cols, candidates)
            if m:
                colmap[alias] = m
            # alteracao_36_F: nao lanca erro se structure_id ausente --
            # isso ocorre antes da migration e e tratado em _structure_filter_col

        self._payoff_cols = colmap

        if ("spot" not in self._payoff_cols) or ("pl" not in self._payoff_cols):
            raise RuntimeError(
                f"Tabela {self._payoff_table} não apresenta colunas obrigatórias "
                f"para payoff (point_spot/point_pl ou spot/pl)."
            )

        # alteracao_36_F: aviso explicito quando structure_id ausente (pre-migration)
        if "structure_id" not in self._payoff_cols:
            print(
                f"[UI] AVISO: {self._payoff_table} nao tem coluna structure_id. "
                "Execute a migration (alteracao_36) para habilitar filtro canonico."
            )

    # ------------------------------------------------------------------
    #  alteracao_33: resolve a coluna de filtro por estrutura
    #   Prioriza structure_id; cai em aba se structure_id não mapeado.
    # ------------------------------------------------------------------
    def _structure_filter_col(self, colmap: Dict[str, str]) -> str:
        """
        alteracao_34: retorna apenas o nome da coluna structure_id.
        Branch aba removido -- schemas sem structure_id nao sao mais suportados.
        """
        if colmap.get("structure_id"):
            return colmap["structure_id"]
        raise RuntimeError(
            "Coluna 'structure_id' nao encontrada no colmap. "
            "Execute a migration do alteracao_33 antes de continuar."
        )

    def _resolve_structure_key(self, structure_id: str) -> int:
        """
        alteracao_34: structure_id e sempre INTEGER.
        Aceita str ("7") ou int (7). Lanca ValueError se nao conversivel.
        """
        try:
            return int(structure_id)
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"structure_id invalido: {structure_id!r}. "
                "Esperado inteiro ou string numerica."
            ) from exc

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------

    def refresh(self):
        self._detect_tables()
        self._build_consolidations_colmap()
        self._build_payoff_colmap()
        self._cache_structures = self._load_structures()

    def _load_structures(self) -> List[str]:
        # alteracao_36_E: abre e fecha conexao local
        c = self._consolidations_cols
        if not c.get("structure_id"):
            raise RuntimeError(
                "Coluna 'structure_id' nao encontrada em "
                f"{self._consolidations_table}. "
                "Execute a migration do alteracao_33 antes de continuar."
            )
        sid_col = c["structure_id"]
        conn = self._connect()
        try:
            q = (
                f"SELECT DISTINCT CAST({sid_col} AS TEXT) AS structure_id "
                f"FROM {self._consolidations_table} "
                f"WHERE {sid_col} IS NOT NULL "
                f"ORDER BY structure_id"
            )
            rows = conn.execute(q).fetchall()
            return [r["structure_id"] for r in rows]
        finally:
            conn.close()

    def get_structures(self) -> List[str]:
        """Alias de get_structure_ids() para compatibilidade."""
        if not self._cache_structures:
            self._cache_structures = self._load_structures()
        return list(self._cache_structures)

    def get_structure_ids(self) -> List[str]:
        """alteracao_34: metodo canonico. Substitui get_structures()."""
        if not self._cache_structures:
            self._cache_structures = self._load_structures()
        return list(self._cache_structures)

    def get_abas(self) -> list:
        """Alias readonly de get_structure_ids() -- compat UI (alteracao_34:filtro_aba)."""
        return self.get_structure_ids()

    def get_decisions(self, filters: Optional[Dict] = None) -> List[Dict]:
        """
        Retorna lista de decisões.
        alteracao_33: filtra por structure_id quando disponível.
        alteracao_36_E: conn local por chamada.
        """
        if not self._consolidations_table:
            self.refresh()

        c = self._consolidations_cols
        pl_pct_expr = self._decision_pl_pct_expr(c)
        select_parts = self._decision_select_parts(c, pl_pct_expr)
        subq = self._decision_subquery(select_parts)

        where, params = self._build_decisions_where(filters)
        where_sql = f"WHERE {' AND '.join(where)}" if where else ""
        sql = self._build_decisions_sql(subq, where_sql)

        rows = self._fetch_decision_rows(sql, params)
        return [self._normalize_decision_row(row) for row in rows]

    def _decision_pl_pct_expr(self, cols: Dict[str, str]) -> str:
        if cols.get("pl_pct_of_max"):
            return cols["pl_pct_of_max"]

        if cols.get("ratio"):
            return cols["ratio"]

        if cols.get("pl_atual") and cols.get("pl_max"):
            return (
                f"CASE WHEN {cols['pl_max']} IS NULL OR {cols['pl_max']} = 0 "
                f"THEN NULL ELSE ({cols['pl_atual']} * 1.0 / {cols['pl_max']}) END"
            )

        return "NULL"

    def _decision_select_parts(
        self,
        cols: Dict[str, str],
        pl_pct_expr: str,
    ) -> List[str]:
        select_parts = [
            self._decision_select_expr(cols, alias)
            for alias in self._decision_base_aliases()
        ]
        select_parts.append(f"({pl_pct_expr}) AS pl_pct_of_max")
        return select_parts

    def _decision_base_aliases(self) -> List[str]:
        return [
            "timestamp", "structure_id", "aba", "decision", "level",
            "dte_min", "why", "why_json", "pl_atual", "pl_max", "spot_ref",
        ]

    def _decision_select_expr(self, cols: Dict[str, str], alias: str) -> str:
        src = cols.get(alias)
        if src:
            return f"{src} AS {alias}"

        if alias == "aba":
            return self._decision_aba_select_expr(cols)

        if alias == "structure_id":
            return self._decision_structure_id_select_expr(cols)

        return f"NULL AS {alias}"

    def _decision_aba_select_expr(self, cols: Dict[str, str]) -> str:
        sid_src = cols.get("structure_id")
        if sid_src:
            return f"CAST({sid_src} AS TEXT) AS aba"
        return "NULL AS aba"

    def _decision_structure_id_select_expr(self, cols: Dict[str, str]) -> str:
        aba_src = cols.get("aba")
        if aba_src:
            return (
                f"CASE WHEN CAST({aba_src} AS TEXT) GLOB '[0-9]*' "
                f"THEN CAST({aba_src} AS INTEGER) ELSE NULL END AS structure_id"
            )
        return "NULL AS structure_id"

    def _decision_subquery(self, select_parts: List[str]) -> str:
        return f"(SELECT {', '.join(select_parts)} FROM {self._consolidations_table}) t"

    def _build_decisions_where(
        self,
        filters: Optional[Dict],
    ) -> Tuple[List[str], List[Any]]:
        where: List[str] = []
        params: List[Any] = []

        if not filters:
            return where, params

        self._append_decision_date_filters(filters, where, params)
        self._append_decision_structure_filter(filters, where, params)
        self._append_decision_simple_filters(filters, where, params)

        return where, params

    def _append_decision_date_filters(
        self,
        filters: Dict,
        where: List[str],
        params: List[Any],
    ) -> None:
        if filters.get("date_from"):
            try:
                dt_from = datetime.strptime(filters["date_from"], "%Y-%m-%d")
                where.append("t.timestamp >= ?")
                params.append(dt_from.strftime("%Y-%m-%d 00:00:00"))
            except Exception:
                pass

        if filters.get("date_to"):
            try:
                dt_to = datetime.strptime(filters["date_to"], "%Y-%m-%d")
                where.append("t.timestamp <= ?")
                params.append(dt_to.strftime("%Y-%m-%d 23:59:59"))
            except Exception:
                pass

    def _append_decision_structure_filter(
        self,
        filters: Dict,
        where: List[str],
        params: List[Any],
    ) -> None:
        structure_filter = filters.get("structure_id")
        if structure_filter is None:
            return

        try:
            where.append("t.structure_id = ?")
            params.append(int(structure_filter))
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"structure_id deve ser inteiro; recebido: {structure_filter!r}"
            ) from exc

    def _append_decision_simple_filters(
        self,
        filters: Dict,
        where: List[str],
        params: List[Any],
    ) -> None:
        aba_filter = filters.get("aba")
        if aba_filter is not None:
            where.append("t.aba = ?")
            params.append(str(aba_filter))

        if filters.get("decision"):
            where.append("t.decision = ?")
            params.append(filters["decision"])

        if filters.get("level_min"):
            where.append("t.level >= ?")
            params.append(int(filters["level_min"]))

        if filters.get("dte_max"):
            where.append("t.dte_min <= ?")
            params.append(int(filters["dte_max"]))

    def _build_decisions_sql(self, subq: str, where_sql: str) -> str:
        return f"""
            SELECT
                t.timestamp, t.structure_id, t.aba, t.decision, t.level,
                t.pl_pct_of_max, t.dte_min, t.why, t.why_json,
                t.pl_atual, t.pl_max, t.spot_ref
            FROM {subq}
            {where_sql}
            ORDER BY t.timestamp DESC
        """

    def _fetch_decision_rows(self, sql: str, params: List[Any]) -> List[Row]:
        # alteracao_36_E: conn local por chamada, sempre fechada.
        conn = self._connect()
        try:
            return conn.execute(sql, params).fetchall()
        finally:
            conn.close()

    def _normalize_decision_row(self, row: Row) -> Dict:
        item = dict(row)
        self._normalize_decision_structure_fields(item)
        self._normalize_decision_why(item)
        return item

    def _normalize_decision_structure_fields(self, item: Dict) -> None:
        if item.get("structure_id") is None and item.get("aba") is not None:
            try:
                item["structure_id"] = int(item["aba"])
            except (TypeError, ValueError):
                pass

        if item.get("aba") is None and item.get("structure_id") is not None:
            item["aba"] = str(item["structure_id"])

    def _normalize_decision_why(self, item: Dict) -> None:
        why_val = item.get("why")
        why_json_val = item.get("why_json")

        if isinstance(why_val, str):
            try:
                item["why"] = json.loads(why_val)
            except Exception:
                pass
            return

        if why_val is None and why_json_val is not None:
            item["why"] = self._parse_decision_why_json(why_json_val)

    def _parse_decision_why_json(self, why_json_val: Any) -> Any:
        try:
            if isinstance(why_json_val, str):
                return json.loads(why_json_val)
            return why_json_val
        except Exception:
            return why_json_val

    def get_payoff_curve(self, structure_id: str, timestamp: str) -> List[Dict]:
        """
         alteracao_33: resolve chave via _structure_filter_col.
        Aceita structure_id como inteiro ou string numerica ("7").
        Strings nao-numericas lancam ValueError.
        """
        ts_key = timestamp if timestamp is not None else "__latest__"
        cache_key = (str(structure_id), ts_key)

        if hasattr(self, "_payoff_cache") and cache_key in self._payoff_cache:
            cached = self._payoff_cache[cache_key]
            if isinstance(cached, list):
                return cached
            if isinstance(cached, dict) and "points" in cached:
                return cached["points"]

        if not self._payoff_table:
            raise RuntimeError(
                "Tabela de payoff não encontrada. Esperadas: "
                + ", ".join(CANDIDATE_PAYOFF_TABLES)
            )

        conn = self._connect()
        p = self._payoff_cols

        required = ["timestamp", "spot", "pl"]
        if any(k not in p for k in required):
            raise RuntimeError(
                f"Tabela {self._payoff_table} não possui colunas esperadas para payoff."
            )

        #  alteracao_33: resolve coluna de estrutura
        # alteracao_34: structure_id e sempre INTEGER
        filter_col = self._structure_filter_col(p)
        filter_val = self._resolve_structure_key(structure_id)

        sql_exact = f"""
            SELECT {p['spot']} AS spot, {p['pl']} AS pl
            FROM {self._payoff_table}
            WHERE {filter_col} = ? AND {p['timestamp']} = ?
            ORDER BY spot
        """
        pts = conn.execute(sql_exact, (filter_val, timestamp)).fetchall()
        if pts:
            res = [dict(r) for r in pts]
            self._cache_put(cache_key, res)
            return res

        # Fallback: timestamp mais recente
        sql_ts = f"""
            SELECT {p['timestamp']} AS ts
            FROM {self._payoff_table}
            WHERE {filter_col} = ?
            ORDER BY ts DESC
            LIMIT 1
        """
        r = conn.execute(sql_ts, (filter_val,)).fetchone()
        if not r:
            self._cache_put(cache_key, [])
            return []

        ts_near = r["ts"]
        pts2 = conn.execute(
            f"""
            SELECT {p['spot']} AS spot, {p['pl']} AS pl
            FROM {self._payoff_table}
            WHERE {filter_col} = ? AND {p['timestamp']} = ?
            ORDER BY spot
            """,
            (filter_val, ts_near),
        ).fetchall()
        res = [dict(x) for x in pts2]
        self._cache_put(cache_key, res)
        return res

    def _ensure_payoff_table_loaded(self) -> None:
        if not self._payoff_table:
            self.refresh()

    def _payoff_curve_info_cache_key(
        self, structure_id: str, timestamp: str
    ) -> Tuple[str, str]:
        ts_key = timestamp if timestamp is not None else "__latest__"
        return str(structure_id), ts_key

    def _get_payoff_curve_info_from_cache(
        self, cache_key: Tuple[str, str]
    ) -> Tuple[List[Dict], Dict] | None:
        cached = self._cache_get(cache_key)
        if (
            cached is not None
            and isinstance(cached, dict)
            and "points" in cached
            and "info" in cached
        ):
            return cached.get("points", []), cached.get("info", {})
        return None

    def _build_payoff_curve_info(
        self,
        structure_id: str,
        timestamp: str,
        filter_col: str,
        filter_val: Any,
    ) -> Dict[str, Any]:
        return {
            "structure_id": structure_id,
            "aba": structure_id,
            "requested_timestamp": timestamp,
            "used_timestamp": timestamp,
            "fallback": False,
            "source_table": self._payoff_table,
            "filter_col": filter_col,
            "filter_val": filter_val,
            "count_points": 0,
            "created_at": None,
            "meta_json": None,
        }

    def _load_payoff_curve_info_points(
        self,
        conn,
        p: Dict[str, str],
        filter_col: str,
        filter_val: Any,
        timestamp: str,
        info: Dict[str, Any],
    ) -> List[Dict]:
        if self._payoff_table == "payoff_curve_points":
            return self._load_canonical_payoff_curve_info_points(
                conn, filter_col, filter_val, timestamp, info
            )

        return self._load_legacy_payoff_curve_info_points(
            conn, p, filter_col, filter_val, timestamp, info
        )

    def _canonical_payoff_curve_extra_cols(self) -> str:
        extra_cols = ""
        if "meta_json" in self._inspect_columns("payoff_curve_points"):
            extra_cols = ", meta_json, created_at"
        return extra_cols

    def _fetch_canonical_payoff_curve_points(
        self,
        conn,
        filter_col: str,
        filter_val: Any,
        timestamp: str,
        extra_cols: str,
    ):
        sql = (
            f"SELECT point_spot AS spot, point_pl AS pl{extra_cols} "
            f"FROM payoff_curve_points "
            f"WHERE {filter_col} = ? AND timestamp = ? "
            f"ORDER BY point_spot"
        )
        return conn.execute(sql, (filter_val, timestamp)).fetchall()

    def _fetch_latest_canonical_payoff_timestamp(
        self, conn, filter_col: str, filter_val: Any
    ):
        row_ts = conn.execute(
            f"SELECT timestamp FROM payoff_curve_points "
            f"WHERE {filter_col} = ? ORDER BY timestamp DESC LIMIT 1",
            (filter_val,),
        ).fetchone()
        if row_ts and row_ts["timestamp"]:
            return row_ts["timestamp"]
        return None

    def _rows_to_payoff_points(self, rows) -> List[Dict]:
        return [{"spot": r["spot"], "pl": r["pl"]} for r in rows]

    def _apply_canonical_payoff_curve_metadata(
        self, rows, extra_cols: str, info: Dict[str, Any]
    ) -> None:
        if rows and extra_cols:
            info["created_at"] = rows[0]["created_at"]
            info["meta_json"] = rows[0]["meta_json"]

    def _load_canonical_payoff_curve_info_points(
        self,
        conn,
        filter_col: str,
        filter_val: Any,
        timestamp: str,
        info: Dict[str, Any],
    ) -> List[Dict]:
        extra_cols = self._canonical_payoff_curve_extra_cols()
        rows = self._fetch_canonical_payoff_curve_points(
            conn, filter_col, filter_val, timestamp, extra_cols
        )

        if not rows:
            used_ts = self._fetch_latest_canonical_payoff_timestamp(
                conn, filter_col, filter_val
            )
            if used_ts:
                info["used_timestamp"] = used_ts
                info["fallback"] = True
                rows = self._fetch_canonical_payoff_curve_points(
                    conn, filter_col, filter_val, used_ts, extra_cols
                )

        points = self._rows_to_payoff_points(rows)
        info["count_points"] = len(points)
        self._apply_canonical_payoff_curve_metadata(rows, extra_cols, info)
        return points

    def _ensure_legacy_payoff_curve_columns(self, p: Dict[str, str]) -> None:
        required = ["timestamp", "spot", "pl"]
        if any(k not in p for k in required):
            raise RuntimeError(
                f"Tabela {self._payoff_table} não possui colunas esperadas."
            )

    def _build_legacy_payoff_curve_exact_sql(
        self, p: Dict[str, str], filter_col: str
    ) -> str:
        return (
            f"SELECT {p['spot']} AS spot, {p['pl']} AS pl "
            f"FROM {self._payoff_table} "
            f"WHERE {filter_col} = ? AND {p['timestamp']} = ? "
            f"ORDER BY spot"
        )

    def _fetch_latest_legacy_payoff_timestamp(
        self, conn, p: Dict[str, str], filter_col: str, filter_val: Any
    ):
        sql_ts = (
            f"SELECT {p['timestamp']} AS ts FROM {self._payoff_table} "
            f"WHERE {filter_col} = ? ORDER BY ts DESC LIMIT 1"
        )
        rts = conn.execute(sql_ts, (filter_val,)).fetchone()
        if rts and rts["ts"]:
            return rts["ts"]
        return None

    def _load_legacy_payoff_curve_info_points(
        self,
        conn,
        p: Dict[str, str],
        filter_col: str,
        filter_val: Any,
        timestamp: str,
        info: Dict[str, Any],
    ) -> List[Dict]:
        self._ensure_legacy_payoff_curve_columns(p)
        sql_exact = self._build_legacy_payoff_curve_exact_sql(p, filter_col)
        rows = conn.execute(sql_exact, (filter_val, timestamp)).fetchall()

        if not rows:
            used_ts = self._fetch_latest_legacy_payoff_timestamp(
                conn, p, filter_col, filter_val
            )
            if used_ts:
                info["used_timestamp"] = used_ts
                info["fallback"] = True
                rows = conn.execute(sql_exact, (filter_val, used_ts)).fetchall()

        points = self._rows_to_payoff_points(rows)
        info["count_points"] = len(points)
        return points

    def _store_payoff_curve_info_cache(
        self,
        cache_key: Tuple[str, str],
        points: List[Dict],
        info: Dict[str, Any],
    ) -> None:
        payload = {"points": points, "info": info}
        self._cache_put(cache_key, payload)

    def get_payoff_curve_info(
        self, structure_id: str, timestamp: str
    ) -> Tuple[List[Dict], Dict]:
        """
         alteracao_33: usa structure_id como chave primária quando disponível.
        Fallback para aba mantido para compatibilidade.
        """
        import time

        t0 = time.time()
        self._ensure_payoff_table_loaded()

        cache_key = self._payoff_curve_info_cache_key(structure_id, timestamp)
        cached = self._get_payoff_curve_info_from_cache(cache_key)
        if cached is not None:
            return cached

        p = self._payoff_cols
        filter_col = self._structure_filter_col(p)
        conn = self._connect_derived_threadsafe()

        try:
            filter_val = self._resolve_structure_key(structure_id)
            info = self._build_payoff_curve_info(
                structure_id, timestamp, filter_col, filter_val
            )
            points = self._load_payoff_curve_info_points(
                conn, p, filter_col, filter_val, timestamp, info
            )
        finally:
            try:
                conn.close()
            except Exception:
                pass

        info["query_ms"] = int((time.time() - t0) * 1000)
        self._store_payoff_curve_info_cache(cache_key, points, info)
        return points, info

    def export_to_csv(self, data: List[Dict], filename: str):
        if not data:
            headers = [
                "timestamp", "structure_id", "aba", "decision", "level",
                "pl_pct_of_max", "dte_min", "why", "why_json",
                "pl_atual", "pl_max", "spot_ref",
            ]
            with open(filename, "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=headers)
                w.writeheader()
            return

        headers = list({k for row in data for k in row.keys()})
        with open(filename, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=headers)
            w.writeheader()
            for row in data:
                out = dict(row)
                if isinstance(out.get("why"), (dict, list)):
                    out["why"] = json.dumps(out["why"], ensure_ascii=False)
                w.writerow(out)

    def check_database_status(self) -> str:
        self.refresh()
        conn = self._connect()
        ctbl = self._consolidations_table
        c = self._consolidations_cols

        cnt = conn.execute(f"SELECT COUNT(*) AS n FROM {ctbl}").fetchone()["n"]

        ts_col = c.get("timestamp")
        last_ts = None
        if ts_col:
            r = conn.execute(
                f"SELECT {ts_col} AS ts FROM {ctbl} ORDER BY ts DESC LIMIT 1"
            ).fetchone()
            last_ts = r["ts"] if r else None

        n_structures = len(self._cache_structures)
        payoff_ok = bool(self._payoff_table)

        #  alteracao_33: reporta qual coluna de filtro está ativa
        p = self._payoff_cols
        try:
            filter_col = self._structure_filter_col(p)
            filter_info = f"{filter_col} (mode=canonical)"  # alteracao_34: sempre canonico
        except Exception:
            filter_info = "N/A"

        return (
            f"derived.db: OK\n"
            f"Consolidações: {ctbl} (linhas: {cnt}, estruturas: {n_structures})\n"
            f"Timestamp mais recente: {last_ts}\n"
            f"Tabela de payoff: {self._payoff_table if payoff_ok else 'NÃO ENCONTRADA'}\n"
            f"Filtro de estrutura ativo: {filter_info}"    #  alteracao_33
        )

    def clear_cache(self):
        self._cache_structures = []
        self._payoff_cache = {}

    # _connect_derived_threadsafe agora e apenas alias de _connect
    def _connect_derived_threadsafe(self) -> sqlite3.Connection:
        return self._connect()

    def _cache_get(self, key: Tuple) -> Optional[Any]:
        try:
            return self._payoff_cache.get(key)
        except Exception:
            return None

    def _cache_put(self, key: Tuple, value: Any):
        try:
            self._payoff_cache[key] = value
            mx = getattr(self, "_payoff_cache_max", 0) or 0
            if mx > 0 and len(self._payoff_cache) > mx:
                self._payoff_cache.pop(next(iter(self._payoff_cache)))
        except Exception:
            pass
