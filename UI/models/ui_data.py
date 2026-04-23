# UI/models/ui_data.py
import sqlite3
from sqlite3 import Row
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import json
import csv
from datetime import datetime

CANDIDATE_CONSOLIDATION_TABLES = [
    "rtd_consolidacoes",
    "rtd_consolidations",
    "decisions",
    "rtd_decisions",
]
CANDIDATE_PAYOFF_TABLES = [
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
    "dte_min": ["dte_min", "dte", "days_to_expiry"],
    "why_json": ["why_json", "why", "rationale_json", "meta_json"],
}

PAYOFF_COLUMN_ALIASES = {
    "timestamp": ["timestamp", "ts", "dt_ref"],
    "aba": ["aba", "sheet", "tab"],
    "spot": ["spot", "underlying", "x"],
    "pl": ["pl", "pl_value", "y", "payoff"],
}

def _first_match(cols: List[str], candidates: List[str]) -> Optional[str]:
    for c in candidates:
        if c in cols:
            return c
    return None


class UIDataModel:
    def __init__(self, derived_db_path: Optional[Path] = None):
        # Ajuste o caminho conforme seu projeto (ex.: data/derived.db)
        self.derived_db_path = Path(derived_db_path) if derived_db_path else Path("data/derived.db")
        self._conn: Optional[sqlite3.Connection] = None
        self._consolidations_table: Optional[str] = None
        self._payoff_table: Optional[str] = None
        self._consolidations_cols: Dict[str, str] = {}
        self._payoff_cols: Dict[str, str] = {}
        self._cache_abas: List[str] = []
    
    # ---------- Infra ----------
    def _connect(self) -> sqlite3.Connection:
        if not self._conn:
            if not self.derived_db_path.exists():
                raise FileNotFoundError(f"Banco derived.db não encontrado em: {self.derived_db_path}")
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
        # Payoff
        for t in CANDIDATE_PAYOFF_TABLES:
            if t in tables:
                self._payoff_table = t
                break
        # payoff é opcional para a UI iniciar; só alertaremos quando tentar plotar
    
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
        for alias, candidates in PAYOFF_COLUMN_ALIASES.items():
            m = _first_match(cols, candidates)
            if m:
                colmap[alias] = m
        self._payoff_cols = colmap
    
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
        # Subselect para podermos filtrar por aliases
        select_parts = []
        for alias in ["timestamp", "aba", "decision", "level", "pl_pct_of_max", "dte_min", "why_json"]:
            src = c.get(alias)
            if src:
                select_parts.append(f"{src} AS {alias}")
            else:
                # Campos ausentes: retornam NULL
                select_parts.append(f"NULL AS {alias}")
        subq = f"(SELECT {', '.join(select_parts)} FROM {self._consolidations_table}) t"
        
        where = []
        params = []
        if filters:
            # Datas
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
            # Aba
            if filters.get("aba"):
                where.append("t.aba = ?")
                params.append(filters["aba"])
            # Decisão
            if filters.get("decision"):
                where.append("t.decision = ?")
                params.append(filters["decision"])
        
        where_sql = f"WHERE {' AND '.join(where)}" if where else ""
        sql = f"""
            SELECT t.timestamp, t.aba, t.decision, t.level, t.pl_pct_of_max, t.dte_min, t.why_json
            FROM {subq}
            {where_sql}
            ORDER BY t.timestamp DESC
        """
        rows = conn.execute(sql, params).fetchall()
        out = []
        for r in rows:
            d = dict(r)
            # Normalizações leves
            if isinstance(d.get("pl_pct_of_max"), (int, float)) and d["pl_pct_of_max"] is not None:
                # já está em fração? assumimos fração (ex.: 0.12 = 12%)
                pass
            out.append(d)
        return out
    
    def get_payoff_curve(self, aba: str, timestamp: str) -> List[Dict]:
        if not self._payoff_table:
            raise RuntimeError("Tabela de payoff não encontrada. Esperadas: " + ", ".join(CANDIDATE_PAYOFF_TABLES))
        conn = self._connect()
        p = self._payoff_cols
        required = ["timestamp", "aba", "spot", "pl"]
        if any(k not in p for k in required):
            raise RuntimeError(f"Tabela {self._payoff_table} não possui colunas esperadas para payoff.")
        
        # Primeiro tenta match exato por timestamp
        sql_exact = f"""
            SELECT {p['spot']} AS spot, {p['pl']} AS pl
            FROM {self._payoff_table}
            WHERE {p['aba']} = ? AND {p['timestamp']} = ?
            ORDER BY spot
        """
        pts = conn.execute(sql_exact, (aba, timestamp)).fetchall()
        if pts:
            return [dict(r) for r in pts]
        
        # Senão, pega o timestamp mais próximo anterior
        sql_ts = f"""
            SELECT {p['timestamp']} AS ts
            FROM {self._payoff_table}
            WHERE {p['aba']} = ?
            ORDER BY ts DESC
            LIMIT 1
        """
        r = conn.execute(sql_ts, (aba,)).fetchone()
        if not r:
            return []
        ts_near = r["ts"]
        pts2 = conn.execute(
            f"SELECT {p['spot']} AS spot, {p['pl']} AS pl FROM {self._payoff_table} WHERE {p['aba']} = ? AND {p['timestamp']} = ? ORDER BY spot",
            (aba, ts_near)
        ).fetchall()
        return [dict(x) for x in pts2]
    
    def export_to_csv(self, data: List[Dict], filename: str):
        if not data:
            # cria CSV vazio com cabeçalhos padrão
            headers = ["timestamp", "aba", "decision", "level", "pl_pct_of_max", "dte_min", "why_json"]
            with open(filename, "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=headers)
                w.writeheader()
            return
        headers = list({k for row in data for k in row.keys()})
        with open(filename, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=headers)
            w.writeheader()
            for row in data:
                w.writerow(row)
    
    def check_database_status(self) -> str:
        self.refresh()
        conn = self._connect()
        ctbl = self._consolidations_table
        c = self._consolidations_cols
        cnt = conn.execute(f"SELECT COUNT(*) AS n FROM {ctbl}").fetchone()["n"]
        # ts mais recente
        ts_col = c.get("timestamp")
        last_ts = None
        if ts_col:
            r = conn.execute(f"SELECT {ts_col} AS ts FROM {ctbl} ORDER BY ts DESC LIMIT 1").fetchone()
            last_ts = r["ts"] if r else None
        abas = len(self._cache_abas)
        payoff_ok = bool(self._payoff_table)
        return (
            f"derived.db: OK\n"
            f"Consolidações: {ctbl} (linhas: {cnt}, abas: {abas})\n"
            f"Timestamp mais recente: {last_ts}\n"
            f"Tabela de payoff: {'OK' if payoff_ok else 'NÃO ENCONTRADA'}"
        )
    
    def clear_cache(self):
        self._cache_abas = []
        # conexão mantida para performance
