# db/derived_repo.py
"""
Repositório para operações com dados consolidados (payoff e decisões).
Tabelas: payoff_curve_points, structure_decisions

Contrato canônico payoff: point_spot / point_pl (opção B).

alteracao_33:
  - Encapsula lógica em classe DerivedRepo (resolve alteracao_26 / alteracao_30)
  - Gerenciamento de conexão interno com try/finally + conn.close() explícito
  - Adiciona get_recent_decisions() (gap alteracao_26)
  - Mantém funções avulsas como shims para compatibilidade com callers legados

alteracao_55:
  - Suporte a StructureRef como argumento aba em _extract_ts_aba e get_recent_decisions

alteracao_56:
  - fix: _MIGRATIONS removido (inexistente), _apply_schema reescrito sem IndentationError
  - fix: _DDL_PAYOFF_IDX -> _DDL_PAYOFF_IDX_STRUCTURE
  - fix: existing_payoff_cols -> existing_cols
  - fix: 5 placeholders -> 6 nos INSERTs com structure_id
"""
from __future__ import annotations

import json
import sqlite3
from db.config import connect_app
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union

# alteracao_55: StructureRef
try:
    from domain.refs.structure_ref import StructureRef as _StructureRef
except ImportError:
    _StructureRef = None  # type: ignore

# Import canônico para type hints (usado nas assinaturas públicas)
try:
    from domain.refs.structure_ref import StructureRef
except ImportError:
    StructureRef = Any  # type: ignore

PayoffPoint = Union[Tuple[float, float], Dict[str, float]]

# ---------------------------------------------------------------------------
# alteracao_56: helper de compatibilidade StructureRef -> str
# ---------------------------------------------------------------------------


def get_app_db_connection() -> sqlite3.Connection:
    """Retorna conexao para o banco unico da aplicacao app.db."""
    return connect_app()


def get_derived_connection() -> sqlite3.Connection:
    """Alias legado preservado temporariamente para compatibilidade."""
    return get_app_db_connection()

def _unwrap_aba(aba_or_ref) -> str:
    """
    alteracao_56: aceita str ou StructureRef no parâmetro 'aba'.
    Extrai .aba como string canônica quando recebe StructureRef.
    Compatibilidade retroativa: callers que passam str continuam funcionando.
    """
    if _StructureRef is not None and isinstance(aba_or_ref, _StructureRef):
        resolved = aba_or_ref.aba
        if resolved is None:
            raise ValueError(
                f"StructureRef.aba é None -- use StructureRef.from_aba() ou "
                f"verifique o mapeamento. ref={aba_or_ref!r}"
            )
        return resolved
    return aba_or_ref  # já é str (ou None, para wildcards)


def _table_columns(conn: sqlite3.Connection, table_name: str) -> List[str]:
    cur = conn.cursor()
    cur.execute(f"PRAGMA table_info({table_name})")
    return [row[1] for row in cur.fetchall()]


# ---------------------------------------------------------------------------
# DDL
# ---------------------------------------------------------------------------
# alteracao_36_A: adicionar structure_id ao DDL de payoff_curve_points

_DDL_PAYOFF_CURVE_POINTS = """
CREATE TABLE IF NOT EXISTS payoff_curve_points (
    timestamp    TEXT NOT NULL,
    aba          TEXT NOT NULL,
    structure_id INTEGER,
    spot_ref     REAL,
    point_spot   REAL NOT NULL,
    point_pl     REAL NOT NULL,
    meta_json    TEXT,
    created_at   TEXT DEFAULT (datetime('now'))
)
"""

_DDL_PAYOFF_UNIQUE_IDX = """
CREATE UNIQUE INDEX IF NOT EXISTS ux_payoff_snapshot
ON payoff_curve_points (timestamp, aba, point_spot)
"""

# alteracao_36_B: index por structure_id para queries canônicas
_DDL_PAYOFF_IDX_STRUCTURE = """
CREATE INDEX IF NOT EXISTS ix_payoff_structure_id
ON payoff_curve_points (structure_id, timestamp)
"""

_DDL_STRUCTURE_DECISIONS = """
CREATE TABLE IF NOT EXISTS structure_decisions (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp     TEXT    NOT NULL,
    aba           TEXT    NOT NULL,
    decision      TEXT    NOT NULL,
    level         INTEGER NOT NULL,
    pl_atual      REAL,
    pl_max        REAL,
    pl_pct_of_max REAL,
    dte_min       INTEGER,
    why_json      TEXT,
    spot_ref      REAL,
    meta_json     TEXT,
    created_at    TEXT    DEFAULT CURRENT_TIMESTAMP,
    why           TEXT,
    structure_id  INTEGER
)
"""

_DDL_DECISIONS_UNIQUE_IDX = """
CREATE UNIQUE INDEX IF NOT EXISTS ux_decision_snapshot
ON structure_decisions (timestamp, aba)
"""

_DDL_DECISIONS_IDX_ABA = """
CREATE INDEX IF NOT EXISTS idx_decisions_aba_ts
ON structure_decisions (aba, timestamp)
"""

_DDL_DECISIONS_IDX_TS = """
CREATE INDEX IF NOT EXISTS idx_decisions_ts
ON structure_decisions (timestamp)
"""

# alteracao_36_C: migration incremental (guard ALTER TABLE)
_PAYOFF_MIGRATIONS: Dict[str, str] = {
    "structure_id": (
        "ALTER TABLE payoff_curve_points ADD COLUMN structure_id INTEGER"
    ),
}

# ---------------------------------------------------------------------------
# Helpers internos (nível módulo -- reutilizados pela classe e shims)
# ---------------------------------------------------------------------------

def _normalize_why_fields(
    decision_dict: Dict[str, Any],
) -> tuple[Any, Optional[str]]:
    why_data = {
        k: v for k, v in decision_dict.items()
        if k not in {
            "decision", "level", "pl_atual", "pl_max",
            "pl_pct_of_max", "dte_min", "spot_ref", "meta",
            "why", "why_json",
        }
    }

    why = decision_dict.get("why")
    if why is None and why_data:
        why = why_data

    why_json = decision_dict.get("why_json")
    if why_json is None and why is not None:
        why_json = why if isinstance(why, str) else json.dumps(why, ensure_ascii=False)

    why_db = json.dumps(why, ensure_ascii=False) if (why is not None and not isinstance(why, str)) else why
    return why_db, why_json


def _apply_schema(conn: sqlite3.Connection) -> None:
    """Cria tabelas, índices e aplica migrations. Idempotente."""
    # Tabelas base
    conn.execute(_DDL_PAYOFF_CURVE_POINTS)
    conn.execute(_DDL_PAYOFF_UNIQUE_IDX)
    conn.execute(_DDL_STRUCTURE_DECISIONS)

    # alteracao_36_A: migration incremental payoff_curve_points
    existing_cols = _table_columns(conn, "payoff_curve_points")
    for col, sql in _PAYOFF_MIGRATIONS.items():
        if col not in existing_cols:
            try:
                conn.execute(sql)
            except sqlite3.OperationalError:
                pass

    # alteracao_36_B: index structure_id no payoff (após migration)
    try:
        conn.execute(_DDL_PAYOFF_IDX_STRUCTURE)
    except sqlite3.OperationalError:
        pass

    # Índices de structure_decisions
    conn.execute(_DDL_DECISIONS_UNIQUE_IDX)
    conn.execute(_DDL_DECISIONS_IDX_ABA)
    conn.execute(_DDL_DECISIONS_IDX_TS)

    conn.commit()


# ---------------------------------------------------------------------------
# Alias público para callers legados
# ---------------------------------------------------------------------------

def ensure_derived_tables(conn: sqlite3.Connection) -> None:
    """Shim de compatibilidade -- mantém callers legados funcionando."""
    _apply_schema(conn)


# ===========================================================================
# DerivedRepo -- API canônica com gerenciamento próprio de conexão
# ===========================================================================

class DerivedRepo:
    """
    Repositório canônico para app.db.
    alteracao_34: assinaturas alinhadas com o smoke 70 (decision_dict auto-extrai timestamp/aba).
    alteracao_55: suporte a StructureRef como argumento aba.
    alteracao_56: correções de bugs em _apply_schema e INSERTs do payoff.
    """

    def __init__(self, db_path: str = "dados/app.db", derived_db: Optional[str] = None) -> None:
        self._db_path = derived_db or db_path
        self._bootstrap()

    # ------------------------------------------------------------------
    # Infraestrutura
    # ------------------------------------------------------------------

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _bootstrap(self) -> None:
        conn = self._connect()
        try:
            _apply_schema(conn)
        finally:
            conn.close()

    def _table_columns(self, table: str) -> List[str]:
        """Alias privado -- requerido pelo smoke 70 e audit."""
        conn = self._connect()
        try:
            return _table_columns(conn, table)
        finally:
            conn.close()

    # Alias público para quem prefere sem underscore
    table_columns = _table_columns

    # ------------------------------------------------------------------
    # Helpers internos de extração
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_ts_aba(
        decision_dict: Dict[str, Any],
        timestamp: Optional[str] = None,
        aba: Optional[str] = None,
    ) -> Tuple[str, str]:
        """
        Extrai timestamp e aba do dict ou dos parâmetros explícitos.
        Permite tanto a API nova (só dict) quanto a legada (ts, aba, dict).
        alteracao_55: desempacota StructureRef se necessário.
        """
        if _StructureRef is not None and isinstance(aba, _StructureRef):
            _ref = aba
            aba = _ref.aba
            if _ref.structure_id is not None:
                decision_dict = dict(decision_dict)
                decision_dict["structure_id"] = _ref.structure_id

        ts = timestamp or decision_dict.get("timestamp") or datetime.now().isoformat()
        ab = aba       or decision_dict.get("aba")       or decision_dict.get("ticker", "unknown")
        return ts, ab

    # ------------------------------------------------------------------
    # Escrita -- decisões
    # ------------------------------------------------------------------

    def write_decision_snapshot_atomic(
        self,
        decision_dict: Dict[str, Any],
        timestamp: Optional[str] = None,
        aba: Optional[str] = None,
    ) -> int:
        """
        DELETE anterior + INSERT nova decisão.
        API canônica: timestamp e aba extraídos do dict se não passados.
        Retorna lastrowid.
        """
        ts, ab = self._extract_ts_aba(decision_dict, timestamp, aba)
        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute(
                "DELETE FROM structure_decisions WHERE aba = ? AND timestamp = ?",
                (ab, ts),
            )
            rowid = self._insert_decision(cur, ts, ab, decision_dict)
            conn.commit()
            return rowid
        finally:
            conn.close()

    def insert_structure_decision(
        self,
        decision_dict: Dict[str, Any],
        timestamp: Optional[str] = None,
        aba: Optional[str] = None,
    ) -> int:
        """
        INSERT OR REPLACE idempotente.
        API canônica: timestamp e aba extraídos do dict se não passados.
        Retorna lastrowid.
        """
        ts, ab = self._extract_ts_aba(decision_dict, timestamp, aba)
        conn = self._connect()
        try:
            cur = conn.cursor()
            rowid = self._insert_decision(cur, ts, ab, decision_dict, replace=True)
            conn.commit()
            return rowid
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # Escrita -- payoff
    # ------------------------------------------------------------------

    def write_payoff_snapshot_atomic(
        self,
        points: List[PayoffPoint],
        timestamp: Optional[str] = None,
        aba: Optional[str] = None,
        meta: Optional[Dict[str, Any]] = None,
        structure_id: Optional[int] = None,
    ) -> int:
        """
        DELETE anterior + INSERT novos pontos.
        timestamp e aba podem ser passados explicitamente ou via meta dict.
        Retorna contagem inserida.
        """
        ts  = timestamp    or (meta or {}).get("timestamp")    or datetime.now().isoformat()
        ab  = aba          or (meta or {}).get("aba")          or "unknown"
        sid = structure_id or (meta or {}).get("structure_id")

        conn = self._connect()
        try:
            meta_json = json.dumps(meta, ensure_ascii=False) if meta else None
            cur = conn.cursor()
            cur.execute(
                "DELETE FROM payoff_curve_points WHERE aba = ? AND timestamp = ?",
                (ab, ts),
            )
            # fix alteracao_56: 6 colunas → 6 placeholders
            sql = """
                INSERT INTO payoff_curve_points
                    (timestamp, aba, structure_id, point_spot, point_pl, meta_json)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            count = 0
            for p in points or []:
                if isinstance(p, (tuple, list)) and len(p) == 2:
                    x, y = float(p[0]), float(p[1])
                elif isinstance(p, dict):
                    x = p.get("point_spot", p.get("s_t"))
                    y = p.get("point_pl",   p.get("pl_venc"))
                    if x is None or y is None:
                        continue
                    x, y = float(x), float(y)
                else:
                    continue
                cur.execute(sql, (ts, ab, sid, x, y, meta_json))
                count += 1
            conn.commit()
            return count
        finally:
            conn.close()

    def insert_payoff_points(
        self,
        points: List[PayoffPoint],
        timestamp: Optional[str] = None,
        aba: Optional[str] = None,
        spot_ref: Optional[float] = None,
        meta: Optional[Dict[str, Any]] = None,
        structure_id: Optional[int] = None,
    ) -> int:
        """INSERT OR REPLACE idempotente por (timestamp, aba, point_spot)."""
        ts  = timestamp    or (meta or {}).get("timestamp")    or datetime.now().isoformat()
        ab  = aba          or (meta or {}).get("aba")          or "unknown"
        sid = structure_id or (meta or {}).get("structure_id")

        conn = self._connect()
        try:
            meta_json = json.dumps(meta, ensure_ascii=False) if meta else None
            cur = conn.cursor()
            # fix alteracao_56: 6 colunas → 6 placeholders
            sql = """
                INSERT OR REPLACE INTO payoff_curve_points
                    (timestamp, aba, structure_id, point_spot, point_pl, meta_json)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            count = 0
            for p in points or []:
                if isinstance(p, (tuple, list)) and len(p) == 2:
                    x, y = float(p[0]), float(p[1])
                elif isinstance(p, dict):
                    x = p.get("point_spot", p.get("s_t"))
                    y = p.get("point_pl",   p.get("pl_venc"))
                    if x is None or y is None:
                        continue
                    x, y = float(x), float(y)
                else:
                    continue
                cur.execute(sql, (ts, ab, sid, x, y, meta_json))
                count += 1
            conn.commit()
            return count
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # Escrita -- snapshot completo
    # ------------------------------------------------------------------

    def write_complete_snapshot_atomic(
        self,
        points: List[PayoffPoint],
        decision_dict: Dict[str, Any],
        timestamp: Optional[str] = None,
        aba: Optional[str] = None,
        points_meta: Optional[Dict] = None,
    ) -> Dict[str, int]:
        """Grava pontos + decisão atomicamente em uma única transação."""
        ts, ab = self._extract_ts_aba(decision_dict, timestamp, aba)
        sid = decision_dict.get("structure_id")

        conn = self._connect()
        try:
            meta_json = json.dumps(points_meta, ensure_ascii=False) if points_meta else None
            cur = conn.cursor()

            # --- payoff ---
            cur.execute(
                "DELETE FROM payoff_curve_points WHERE aba = ? AND timestamp = ?",
                (ab, ts),
            )
            # fix alteracao_56: 6 colunas → 6 placeholders
            sql_p = """
                INSERT INTO payoff_curve_points
                    (timestamp, aba, structure_id, point_spot, point_pl, meta_json)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            count = 0
            for p in points or []:
                if isinstance(p, (tuple, list)) and len(p) == 2:
                    x, y = float(p[0]), float(p[1])
                elif isinstance(p, dict):
                    x = p.get("point_spot", p.get("s_t"))
                    y = p.get("point_pl",   p.get("pl_venc"))
                    if x is None or y is None:
                        continue
                    x, y = float(x), float(y)
                else:
                    continue
                cur.execute(sql_p, (ts, ab, sid, x, y, meta_json))
                count += 1

            # --- decisão ---
            cur.execute(
                "DELETE FROM structure_decisions WHERE aba = ? AND timestamp = ?",
                (ab, ts),
            )
            decision_id = self._insert_decision(cur, ts, ab, decision_dict)

            conn.commit()
            return {"points_count": count, "decision_id": decision_id}
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # Leitura
    # ------------------------------------------------------------------

    def get_payoff_points(
        self,
        aba: Optional[str] = None,
        timestamp: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        conn = self._connect()
        try:
            cur = conn.cursor()
            if aba and timestamp:
                cur.execute(
                    """
                    SELECT timestamp, aba, point_spot, point_pl, meta_json
                    FROM payoff_curve_points
                    WHERE aba = ? AND timestamp = ?
                    ORDER BY point_spot
                    """,
                    (aba, timestamp),
                )
            elif aba:
                cur.execute(
                    """
                    SELECT timestamp, aba, point_spot, point_pl, meta_json
                    FROM payoff_curve_points
                    WHERE aba = ?
                    ORDER BY timestamp DESC, point_spot
                    LIMIT 100
                    """,
                    (aba,),
                )
            else:
                cur.execute(
                    """
                    SELECT timestamp, aba, point_spot, point_pl, meta_json
                    FROM payoff_curve_points
                    ORDER BY timestamp DESC, point_spot
                    LIMIT 100
                    """
                )
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, r)) for r in cur.fetchall()]
        finally:
            conn.close()

    def get_recent_decisions(
        self,
        aba: Optional[str] = None,
        structure_id: Optional[int] = None,
        ticker: Optional[str] = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        # alteracao_55: desempacotar StructureRef
        if _StructureRef is not None and isinstance(aba, _StructureRef):
            if structure_id is None and aba.structure_id is not None:
                structure_id = aba.structure_id
            aba = aba.aba

        conn = self._connect()
        try:
            conditions: List[str] = []
            params: List[Any] = []

            if aba is not None:
                conditions.append("aba = ?")
                params.append(aba)
            if structure_id is not None:
                conditions.append("structure_id = ?")
                params.append(structure_id)
            if ticker is not None and aba is None:
                conditions.append("aba = ?")
                params.append(ticker)

            where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
            params.append(limit)
            rows = conn.execute(
                f"SELECT * FROM structure_decisions {where} ORDER BY id DESC LIMIT ?",
                params,
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # Manutenção
    # ------------------------------------------------------------------

    def validate_snapshot_consistency(self) -> bool:
        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT d.aba, d.timestamp, COUNT(p.point_spot) as point_count
                FROM structure_decisions d
                LEFT JOIN payoff_curve_points p
                       ON (d.aba = p.aba AND d.timestamp = p.timestamp)
                GROUP BY d.aba, d.timestamp
                HAVING point_count = 0
            """)
            orphan_decisions = cur.fetchall()
            cur.execute("""
                SELECT p.aba, p.timestamp, COUNT(DISTINCT p.point_spot)
                FROM payoff_curve_points p
                LEFT JOIN structure_decisions d
                       ON (p.aba = d.aba AND p.timestamp = d.timestamp)
                WHERE d.aba IS NULL
                GROUP BY p.aba, p.timestamp
            """)
            orphan_points = cur.fetchall()
            ok = not orphan_decisions and not orphan_points
            if not ok:
                if orphan_decisions:
                    print(f"[FALHOU] {len(orphan_decisions)} decisões sem pontos")
                if orphan_points:
                    print(f"[FALHOU] {len(orphan_points)} pontos sem decisão")
            else:
                print("[ok] Snapshots consistentes")
            return ok
        finally:
            conn.close()

    def cleanup_old_payoff_data(self, days_to_keep: int = 30) -> int:
        conn = self._connect()
        try:
            cur = conn.execute(
                f"DELETE FROM payoff_curve_points "
                f"WHERE datetime(timestamp) < datetime('now', '-{days_to_keep} days')"
            )
            conn.commit()
            return cur.rowcount
        finally:
            conn.close()

    def cleanup_old_decisions(self, days_to_keep: int = 30) -> int:
        conn = self._connect()
        try:
            cur = conn.execute(
                f"DELETE FROM structure_decisions "
                f"WHERE datetime(timestamp) < datetime('now', '-{days_to_keep} days')"
            )
            conn.commit()
            return cur.rowcount
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # Privados
    # ------------------------------------------------------------------

    def _insert_decision(
        self,
        cur: sqlite3.Cursor,
        timestamp: str,
        aba: str,
        decision_dict: Dict[str, Any],
        replace: bool = False,
    ) -> int:
        why, why_json = _normalize_why_fields(decision_dict)
        meta = decision_dict.get("meta")
        verb = "INSERT OR REPLACE" if replace else "INSERT"
        cur.execute(
            f"""
            {verb} INTO structure_decisions
                (timestamp, aba, decision, level, pl_atual, pl_max, pl_pct_of_max,
                 dte_min, why, why_json, spot_ref, meta_json, structure_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                timestamp,
                aba,
                decision_dict.get("decision", "HOLD"),
                (lambda v: int(v) if str(v).lstrip("-").isdigit() else 0)(decision_dict.get("level", 0)),
                decision_dict.get("pl_atual"),
                decision_dict.get("pl_max"),
                decision_dict.get("pl_pct_of_max"),
                decision_dict.get("dte_min"),
                why,
                why_json,
                decision_dict.get("spot_ref"),
                json.dumps(meta, ensure_ascii=False) if meta else None,
                decision_dict.get("structure_id"),
            ),
        )
        return cur.lastrowid


# ===========================================================================
# Shims de compatibilidade -- funções avulsas legadas
# ===========================================================================

def write_payoff_snapshot_atomic(
    conn: sqlite3.Connection,
    timestamp: str,
    aba: str,
    points: List,
    meta: Optional[Dict[str, Any]] = None,
    structure_id: Optional[int] = None,
) -> int:
    ensure_derived_tables(conn)
    if structure_id is None and isinstance(meta, dict):
        structure_id = meta.get("structure_id") or meta.get("payload_structure_id")
    meta_json = json.dumps(meta, ensure_ascii=False) if meta else None
    aba = _unwrap_aba(aba)
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM payoff_curve_points WHERE aba = ? AND timestamp = ?",
        (aba, timestamp),
    )
    sql = """
        INSERT INTO payoff_curve_points
            (timestamp, aba, structure_id, point_spot, point_pl, meta_json)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    count = 0
    for p in points or []:
        if isinstance(p, (tuple, list)) and len(p) == 2:
            x, y = float(p[0]), float(p[1])
        elif isinstance(p, dict):
            x = p.get("point_spot", p.get("s_t"))
            y = p.get("point_pl", p.get("pl_venc"))
            if x is None or y is None:
                continue
            x, y = float(x), float(y)
        else:
            continue
        cur.execute(sql, (timestamp, aba, structure_id, x, y, meta_json))
        count += 1
    return count


def write_decision_snapshot_atomic(
    conn: sqlite3.Connection,
    timestamp: str,
    aba: str,
    decision_dict: Dict[str, Any],
) -> int:
    ensure_derived_tables(conn)
    aba = _unwrap_aba(aba)
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM structure_decisions WHERE aba = ? AND timestamp = ?",
        (aba, timestamp),
    )
    why, why_json = _normalize_why_fields(decision_dict)
    meta = decision_dict.get("meta")
    cur.execute("""
        INSERT INTO structure_decisions
            (timestamp, aba, decision, level, pl_atual, pl_max, pl_pct_of_max,
             dte_min, why, why_json, spot_ref, meta_json, created_at, structure_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        timestamp, aba,
        decision_dict.get("decision", "HOLD"),
        (lambda v: int(v) if str(v).lstrip("-").isdigit() else 0)(decision_dict.get("level", 0)),
        decision_dict.get("pl_atual"),
        decision_dict.get("pl_max"),
        decision_dict.get("pl_pct_of_max"),
        decision_dict.get("dte_min"),
        why, why_json,
        decision_dict.get("spot_ref"),
        json.dumps(meta, ensure_ascii=False) if meta else None,
        datetime.now().isoformat(),
        decision_dict.get("structure_id"),
    ))
    return cur.lastrowid


def write_complete_snapshot_atomic(
    conn: sqlite3.Connection,
    timestamp: str,
    aba: str,
    points: List,
    decision_dict: Dict[str, Any],
    points_meta: Optional[Dict] = None,
) -> Dict[str, int]:
    ensure_derived_tables(conn)
    aba = _unwrap_aba(aba)
    with conn:
        pc  = write_payoff_snapshot_atomic(conn, timestamp, aba, points, points_meta, structure_id=decision_dict.get("structure_id"))
        did = write_decision_snapshot_atomic(conn, timestamp, aba, decision_dict)
    return {"points_count": pc, "decision_id": did}


def insert_payoff_points(
    conn: sqlite3.Connection,
    timestamp: str,
    aba: str,
    points: List[PayoffPoint],
    spot_ref: Optional[float] = None,
    meta: Optional[Dict[str, Any]] = None,
    structure_id: Optional[int] = None,
) -> int:
    ensure_derived_tables(conn)
    if structure_id is None and isinstance(meta, dict):
        structure_id = meta.get("structure_id") or meta.get("payload_structure_id")
    aba = _unwrap_aba(aba)
    meta_json = json.dumps(meta, ensure_ascii=False) if meta else None
    cur = conn.cursor()
    sql = """
        INSERT OR REPLACE INTO payoff_curve_points
            (timestamp, aba, structure_id, point_spot, point_pl, meta_json)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    count = 0
    for p in points or []:
        if isinstance(p, (tuple, list)) and len(p) == 2:
            x, y = float(p[0]), float(p[1])
        elif isinstance(p, dict):
            x = p.get("point_spot", p.get("s_t"))
            y = p.get("point_pl", p.get("pl_venc"))
            if x is None or y is None:
                continue
            x, y = float(x), float(y)
        else:
            continue
        cur.execute(sql, (timestamp, aba, structure_id, x, y, meta_json))
        count += 1
    conn.commit()
    return count


def insert_structure_decision(
    conn: sqlite3.Connection,
    timestamp: str,
    aba: str,
    decision_dict: Dict[str, Any],
) -> int:
    ensure_derived_tables(conn)
    aba = _unwrap_aba(aba)
    why, why_json = _normalize_why_fields(decision_dict)
    meta = decision_dict.get("meta")
    cur = conn.cursor()
    cur.execute("""
        INSERT OR REPLACE INTO structure_decisions
            (timestamp, aba, decision, level, pl_atual, pl_max, pl_pct_of_max,
             dte_min, why, why_json, spot_ref, meta_json, created_at, structure_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        timestamp, aba,
        decision_dict.get("decision", "HOLD"),
        (lambda v: int(v) if str(v).lstrip("-").isdigit() else 0)(decision_dict.get("level", 0)),
        decision_dict.get("pl_atual"),
        decision_dict.get("pl_max"),
        decision_dict.get("pl_pct_of_max"),
        decision_dict.get("dte_min"),
        why, why_json,
        decision_dict.get("spot_ref"),
        json.dumps(meta, ensure_ascii=False) if meta else None,
        datetime.now().isoformat(),
        decision_dict.get("structure_id"),
    ))
    conn.commit()
    return cur.lastrowid


def get_payoff_points(
    conn: sqlite3.Connection,
    aba: Optional[str] = None,
    timestamp: Optional[str] = None,
) -> List[Dict[str, Any]]:
    ensure_derived_tables(conn)
    aba = _unwrap_aba(aba)
    cur = conn.cursor()
    if aba and timestamp:
        cur.execute("""
            SELECT timestamp, aba, point_spot, point_pl, meta_json
            FROM payoff_curve_points
            WHERE aba = ? AND timestamp = ?
            ORDER BY point_spot
        """, (aba, timestamp))
    elif aba:
        cur.execute("""
            SELECT timestamp, aba, point_spot, point_pl, meta_json
            FROM payoff_curve_points
            WHERE aba = ?
            ORDER BY timestamp DESC, point_spot
            LIMIT 100
        """, (aba,))
    else:
        cur.execute("""
            SELECT timestamp, aba, point_spot, point_pl, meta_json
            FROM payoff_curve_points
            ORDER BY timestamp DESC, point_spot
            LIMIT 100
        """)
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]


def validate_snapshot_consistency(conn: sqlite3.Connection) -> bool:
    ensure_derived_tables(conn)
    cur = conn.cursor()
    cur.execute("""
        SELECT d.aba, d.timestamp, COUNT(p.point_spot) as point_count
        FROM structure_decisions d
        LEFT JOIN payoff_curve_points p ON (d.aba = p.aba AND d.timestamp = p.timestamp)
        GROUP BY d.aba, d.timestamp
        HAVING point_count = 0
    """)
    orphan_decisions = cur.fetchall()
    cur.execute("""
        SELECT p.aba, p.timestamp, COUNT(DISTINCT p.point_spot)
        FROM payoff_curve_points p
        LEFT JOIN structure_decisions d ON (p.aba = d.aba AND p.timestamp = d.timestamp)
        WHERE d.aba IS NULL
        GROUP BY p.aba, p.timestamp
    """)
    orphan_points = cur.fetchall()
    ok = not orphan_decisions and not orphan_points
    if not ok:
        if orphan_decisions:
            print(f"[FALHOU] {len(orphan_decisions)} decisões sem pontos")
        if orphan_points:
            print(f"[FALHOU] {len(orphan_points)} pontos sem decisão")
    else:
        print("[ok] Snapshots consistentes")
    return ok


def cleanup_old_payoff_data(conn: sqlite3.Connection, days_to_keep: int = 30) -> int:
    ensure_derived_tables(conn)
    cur = conn.cursor()
    cur.execute(f"""
        DELETE FROM payoff_curve_points
        WHERE datetime(timestamp) < datetime('now', '-{days_to_keep} days')
    """)
    deleted = cur.rowcount
    conn.commit()
    return deleted


def cleanup_old_decisions(conn: sqlite3.Connection, days_to_keep: int = 30) -> int:
    ensure_derived_tables(conn)
    cur = conn.cursor()
    cur.execute(f"""
        DELETE FROM structure_decisions
        WHERE datetime(timestamp) < datetime('now', '-{days_to_keep} days')
    """)
    deleted = cur.rowcount
    conn.commit()
    return deleted
