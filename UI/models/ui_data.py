import sqlite3
from sqlite3 import Row
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from db.config import DERIVED_DB_PATH
import json
import csv
from datetime import datetime

CANDIDATE_CONSOLIDATION_TABLES = [
    "structure_decisions",
    "rtd_consolidacoes",
    "rtd_consolidations",
    "decisions",
    "rtd_decisions",
]
CANDIDATE_PAYOFF_TABLES = [
    "payoff_curve_points",
    "rtd_payoff_points",
    "rtd_payoff_curva",
    "payoff_points",
]

# Mapeamento de colunas preferidas -> alternativas
COLUMN_ALIASES = {
    "timestamp": ["timestamp", "ts", "decided_at", "dt_ref"],
    "aba": ["aba", "sheet", "tab"],
    "decision": ["decision", "decisao", "action"],
    "level": ["level", "nivel", "severity_level"],
    "pl_pct_of_max": ["pl_pct_of_max", "pl_ratio", "pl_pct"],
    "ratio": ["ratio", "pl_ratio", "pl_pct_of_max", "pl_pct"],
    "dte_min": ["dte_min", "dte", "days_to_expiry"],
    "why": ["why", "rationale", "rationale_json"],
    "why_json": ["why_json", "meta_json"],
    "pl_atual": ["pl_atual", "pl_current"],
    "pl_max": ["pl_max", "pl_best", "pl_top"],
    "spot_ref": ["spot_ref", "spot_reference", "ref_spot"],
}


PAYOFF_COLUMN_ALIASES = {
    "timestamp": ["timestamp", "ts", "dt_ref"],
    "aba": ["aba", "sheet", "tab"],
    "spot": ["point_spot", "spot", "underlying", "x", "s_t"],
    "pl": ["point_pl", "pl", "pl_value", "y", "payoff", "pl_venc"],
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

        self._conn: Optional[sqlite3.Connection] = None
        self._consolidations_table: Optional[str] = None
        self._payoff_table: Optional[str] = None
        self._consolidations_cols: Dict[str, str] = {}
        self._payoff_cols: Dict[str, str] = {}
        self._cache_abas: List[str] = []

        # Cache payoff: evita reconsulta repetida ao sqlite a cada clique
        # key: (aba, timestamp_requested)
        # val: {"points": [...], "info": {...}}
        self._payoff_cache: Dict[Tuple[str, str], Dict[str, Any]] = {}
        self._payoff_cache_max = 128

    def _connect(self) -> sqlite3.Connection:
        if not self._conn:
            if not self.derived_db_path.exists():
                raise FileNotFoundError(
                    f"Banco derived.db não encontrado em: {self.derived_db_path}"
                )
            self._conn = sqlite3.connect(str(self.derived_db_path))
            self._conn.row_factory = sqlite3.Row
        return self._conn

    def _list_tables(self) -> List[str]:
        conn = self._connect()
        cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        return [r["name"] for r in cur.fetchall()]

    def _detect_tables(self):
        tables = self._list_tables()
        # Consolidations
        for t in CANDIDATE_CONSOLIDATION_TABLES:
            if t in tables:
                self._consolidations_table = t
                break
        if not self._consolidations_table:
            raise RuntimeError("Tabela de consolidações não encontrada. Esperadas: " + ", ".join(CANDIDATE_CONSOLIDATION_TABLES))
        # Payoff - prioriza tabela canônica
        for t in CANDIDATE_PAYOFF_TABLES:
            if t in tables:
                self._payoff_table = t
                break

    def _inspect_columns(self, table: str) -> List[str]:
        conn = self._connect()
        cur = conn.execute(f"PRAGMA table_info({table})")
        return [r["name"] for r in cur.fetchall()]

    def _build_consolidations_colmap(self):
        cols = self._inspect_columns(self._consolidations_table)
        colmap = {}
        for alias, candidates in COLUMN_ALIASES.items():
            m = _first_match(cols, candidates)
            if m:
                colmap[alias] = m
        # Campos sem mapeamento ficam ausentes; trataremos como None
        self._consolidations_cols = colmap

    def _build_payoff_colmap(self):
        if not self._payoff_table:
            self._payoff_cols = {}
            return

        cols = self._inspect_columns(self._payoff_table)
        colmap = {}

        # Se a tabela é canônica, use contrato forte
        if self._payoff_table == "payoff_curve_points":
            aliases = {
                "spot": ["point_spot"],
                "pl": ["point_pl"],
                "timestamp": ["timestamp"],
                "aba": ["aba"]
            }
            print(f"[UI] Usando contrato canônico para {self._payoff_table}")
        else:
            aliases = PAYOFF_COLUMN_ALIASES
            print(f"[UI] Usando aliases flexíveis para {self._payoff_table}")

        for alias, candidates in aliases.items():
            m = _first_match(cols, candidates)
            if m:
                colmap[alias] = m
        self._payoff_cols = colmap

        # validação obrigatória
        if ("spot" not in self._payoff_cols) or ("pl" not in self._payoff_cols):
            raise RuntimeError(
                f"Tabela {self._payoff_table} não apresenta colunas obrigatórias para payoff (point_spot/point_pl ou spot/pl)."
            )

    # ---------- API ----------
    def refresh(self):
        self._detect_tables()
        self._build_consolidations_colmap()
        self._build_payoff_colmap()
        # Abas
        self._cache_abas = self._load_abas()

    def _load_abas(self) -> List[str]:
        conn = self._connect()
        aba_col = self._consolidations_cols.get("aba")
        if not aba_col:
            return []
        q = f"SELECT DISTINCT {aba_col} AS aba FROM {self._consolidations_table} ORDER BY aba"
        return [r["aba"] for r in conn.execute(q).fetchall()]

    def get_abas(self) -> List[str]:
        return self._cache_abas

    def get_decisions(self, filters: Optional[Dict] = None) -> List[Dict]:
        if not self._consolidations_table:
            self.refresh()
        conn = self._connect()
        c = self._consolidations_cols

        # Expressão para pl_pct_of_max (usando nomes reais das colunas)
        if c.get("pl_pct_of_max"):
            pl_pct_expr = c["pl_pct_of_max"]
        elif c.get("ratio"):
            pl_pct_expr = c["ratio"]
        elif c.get("pl_atual") and c.get("pl_max"):
            pl_atual_col = c["pl_atual"]
            pl_max_col = c["pl_max"]
            pl_pct_expr = (
                f"CASE WHEN {pl_max_col} IS NULL OR {pl_max_col} = 0 "
                f"THEN NULL ELSE ({pl_atual_col} * 1.0 / {pl_max_col}) END"
            )
        else:
            pl_pct_expr = "NULL"

        select_parts = []
        for alias in ["timestamp", "aba", "decision", "level", "dte_min", "why", "why_json", "pl_atual", "pl_max", "spot_ref"]:
            src = c.get(alias)
            select_parts.append(f"{src} AS {alias}" if src else f"NULL AS {alias}")

        select_parts.append(f"({pl_pct_expr}) AS pl_pct_of_max")

        subq = f"(SELECT {', '.join(select_parts)} FROM {self._consolidations_table}) t"

        where = []
        params = []
        if filters:
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

            if filters.get("aba"):
                where.append("t.aba = ?")
                params.append(filters["aba"])

            if filters.get("decision"):
                where.append("t.decision = ?")
                params.append(filters["decision"])

            if filters.get("level_min"):
                where.append("t.level >= ?")
                params.append(int(filters["level_min"]))

            if filters.get("dte_max"):
                where.append("t.dte_min <= ?")
                params.append(int(filters["dte_max"]))

        where_sql = f"WHERE {' AND '.join(where)}" if where else ""
        sql = f"""
            SELECT t.timestamp, t.aba, t.decision, t.level, t.pl_pct_of_max, t.dte_min,
                   t.why, t.why_json, t.pl_atual, t.pl_max, t.spot_ref

            FROM {subq}
            {where_sql}
            ORDER BY t.timestamp DESC
        """
        rows = conn.execute(sql, params).fetchall()

        result = []
        for r in rows:
            item = dict(r)
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

            result.append(item)

        return result

    def get_payoff_curve(self, aba: str, timestamp: str) -> List[Dict]:
        # --- payoff cache ---
        try:
            _aba = aba
        except NameError:
            _aba = None

        _ts = locals().get("timestamp")
        if _ts is None:
            _ts = locals().get("ts")

        _ts_key = _ts if _ts is not None else "__latest__"
        _cache_key = (_aba, _ts_key)

        if hasattr(self, "_payoff_cache") and _cache_key in self._payoff_cache:
            return self._payoff_cache[_cache_key]

        if not self._payoff_table:
            raise RuntimeError(
                "Tabela de payoff não encontrada. Esperadas: " + ", ".join(CANDIDATE_PAYOFF_TABLES)
            )
        conn = self._connect()
        p = self._payoff_cols
        required = ["timestamp", "aba", "spot", "pl"]
        if any(k not in p for k in required):
            raise RuntimeError(f"Tabela {self._payoff_table} não possui colunas esperadas para payoff.")

        sql_exact = f"""
            SELECT {p['spot']} AS spot, {p['pl']} AS pl
            FROM {self._payoff_table}
            WHERE {p['aba']} = ? AND {p['timestamp']} = ?
            ORDER BY spot
        """
        pts = conn.execute(sql_exact, (aba, timestamp)).fetchall()
        if pts:
            _res = [dict(r) for r in pts]
            if hasattr(self, "_payoff_cache"):
                self._payoff_cache[_cache_key] = _res
                if getattr(self, "_payoff_cache_max", 0) and len(self._payoff_cache) > self._payoff_cache_max:
                    try:
                        self._payoff_cache.pop(next(iter(self._payoff_cache)))
                    except Exception:
                        pass
            return _res

        sql_ts = f"""
            SELECT {p['timestamp']} AS ts
            FROM {self._payoff_table}
            WHERE {p['aba']} = ?
            ORDER BY ts DESC
            LIMIT 1
        """
        r = conn.execute(sql_ts, (aba,)).fetchone()
        if not r:
            _res = []
            if hasattr(self, "_payoff_cache"):
                self._payoff_cache[_cache_key] = _res
                if getattr(self, "_payoff_cache_max", 0) and len(self._payoff_cache) > self._payoff_cache_max:
                    try:
                        self._payoff_cache.pop(next(iter(self._payoff_cache)))
                    except Exception:
                        pass
            return _res
        ts_near = r["ts"]

        pts2 = conn.execute(
            f"""
            SELECT {p['spot']} AS spot, {p['pl']} AS pl
            FROM {self._payoff_table}
            WHERE {p['aba']} = ? AND {p['timestamp']} = ?
            ORDER BY spot
            """,
            (aba, ts_near),
        ).fetchall()
        _res = [dict(x) for x in pts2]
        if hasattr(self, "_payoff_cache"):
            self._payoff_cache[_cache_key] = _res
            if getattr(self, "_payoff_cache_max", 0) and len(self._payoff_cache) > self._payoff_cache_max:
                try:
                    self._payoff_cache.pop(next(iter(self._payoff_cache)))
                except Exception:
                    pass
        return _res

    def export_to_csv(self, data: List[Dict], filename: str):
        if not data:
            headers = ["timestamp", "aba", "decision", "level", "pl_pct_of_max", "dte_min", "why", "why_json", "pl_atual", "pl_max", "spot_ref"]
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

        abas = len(self._cache_abas)
        payoff_ok = bool(self._payoff_table)

        return (
            f"derived.db: OK\n"
            f"Consolidações: {ctbl} (linhas: {cnt}, abas: {abas})\n"
            f"Timestamp mais recente: {last_ts}\n"
            f"Tabela de payoff: {self._payoff_table if payoff_ok else 'NÃO ENCONTRADA'}"
        )

    def clear_cache(self):
        self._cache_abas = []
        # conexão mantida para performance

    def _connect_derived_threadsafe(self):
        """
        Retorna uma conexão SQLite NOVA (segura para uso em threads).
        NÃO reutiliza self._derived_conn.
        """
        import sqlite3
        from pathlib import Path

        db_path = getattr(self, "derived_db_path", None) or getattr(self, "DERIVED_DB_PATH", None)
        if not db_path:
            db_path = str(Path("dados") / "derived.db")

        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _cache_get(self, key):
        try:
            return self._payoff_cache.get(key)
        except Exception:
            return None

    def _cache_put(self, key, value):
        try:
            self._payoff_cache[key] = value
            mx = getattr(self, "_payoff_cache_max", 0) or 0
            if mx > 0 and len(self._payoff_cache) > mx:
                self._payoff_cache.pop(next(iter(self._payoff_cache)))
        except Exception:
            pass

    def get_payoff_curve_info(self, aba: str, timestamp: str):
        """Retorna (points, info_dict) com auditoria básica do snapshot."""
        import time

        t0 = time.time()

        if not self._payoff_table:
            self.refresh()

        ts_key = timestamp if timestamp is not None else "__latest__"
        cache_key = (aba, ts_key)
        cached = self._cache_get(cache_key)

        if cached is not None and isinstance(cached, dict) and "points" in cached and "info" in cached:
            return cached.get("points", []), cached.get("info", {})

        info = {
            "aba": aba,
            "requested_timestamp": timestamp,
            "used_timestamp": timestamp,
            "fallback": False,
            "source_table": self._payoff_table,
            "count_points": 0,
            "created_at": None,
            "meta_json": None,
        }

        conn = self._connect_derived_threadsafe()
        try:
            if self._payoff_table == "payoff_curve_points":
                sql = (
                    "SELECT point_spot AS spot, point_pl AS pl, meta_json, created_at "
                    "FROM payoff_curve_points "
                    "WHERE aba = ? AND timestamp = ? "
                    "ORDER BY point_spot"
                )
                rows = conn.execute(sql, (aba, timestamp)).fetchall()
                used_ts = timestamp

                if not rows:
                    row_ts = conn.execute(
                        "SELECT timestamp FROM payoff_curve_points WHERE aba = ? ORDER BY timestamp DESC LIMIT 1",
                        (aba,),
                    ).fetchone()
                    if row_ts and row_ts["timestamp"]:
                        used_ts = row_ts["timestamp"]
                        info["used_timestamp"] = used_ts
                        info["fallback"] = True
                        rows = conn.execute(sql, (aba, used_ts)).fetchall()

                points = [{"spot": r["spot"], "pl": r["pl"]} for r in rows]
                info["count_points"] = len(points)

                if rows:
                    info["created_at"] = rows[0]["created_at"]
                    info["meta_json"] = rows[0]["meta_json"]
            else:
                pcols = self._payoff_cols
                required = ["timestamp", "aba", "spot", "pl"]
                if any(k not in pcols for k in required):
                    raise RuntimeError(f"Tabela {self._payoff_table} não possui colunas esperadas para payoff.")

                sql_exact = (
                    f"SELECT {pcols['spot']} AS spot, {pcols['pl']} AS pl "
                    f"FROM {self._payoff_table} "
                    f"WHERE {pcols['aba']} = ? AND {pcols['timestamp']} = ? "
                    f"ORDER BY spot"
                )
                rows = conn.execute(sql_exact, (aba, timestamp)).fetchall()
                used_ts = timestamp

                if not rows:
                    sql_ts = (
                        f"SELECT {pcols['timestamp']} AS ts FROM {self._payoff_table} "
                        f"WHERE {pcols['aba']} = ? ORDER BY ts DESC LIMIT 1"
                    )
                    rts = conn.execute(sql_ts, (aba,)).fetchone()
                    if rts and rts["ts"]:
                        used_ts = rts["ts"]
                        info["used_timestamp"] = used_ts
                        info["fallback"] = True
                        rows = conn.execute(sql_exact, (aba, used_ts)).fetchall()

                points = [{"spot": r["spot"], "pl": r["pl"]} for r in rows]
                info["count_points"] = len(points)
        finally:
            try:
                conn.close()
            except Exception:
                pass

        info["query_ms"] = int((time.time() - t0) * 1000)

        payload = {"points": points, "info": info}
        self._cache_put(cache_key, payload)

        return points, info
