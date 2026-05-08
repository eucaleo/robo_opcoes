from datetime import datetime
"""
Repositório para operações com dados derivados (payoff e decisões).
Tabelas: payoff_curve_points, structure_decisions

Contrato canônico payoff: point_spot / point_pl (opção B).
"""

import sqlite3
import json
from typing import List, Dict, Any, Optional, Tuple, Union

PayoffPoint = Union[Tuple[float, float], Dict[str, float]]


def ensure_derived_tables(conn: sqlite3.Connection) -> None:
    # Tabela canônica de payoff (SEM id autoincrement)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS payoff_curve_points (
            timestamp  TEXT NOT NULL,
            aba        TEXT NOT NULL,
            spot_ref   REAL,
            point_spot REAL NOT NULL,
            point_pl   REAL NOT NULL,
            meta_json  TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)

    # Idempotência do snapshot
    conn.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS ux_payoff_snapshot
        ON payoff_curve_points (timestamp, aba, point_spot)
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS ix_payoff_aba_ts
        ON payoff_curve_points (aba, timestamp)
    """)

    # Decisões: CRIAR tabela completa + migração das colunas faltantes
    conn.execute("""
        CREATE TABLE IF NOT EXISTS structure_decisions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            aba TEXT NOT NULL,
            decision TEXT NOT NULL,
            level INTEGER NOT NULL,
            pl_atual REAL,
            pl_max REAL,
            pl_pct_of_max REAL,
            dte_min INTEGER,
            why_json TEXT,
            spot_ref REAL,
            meta_json TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Migração: adicionar colunas faltantes se não existirem
    try:
        conn.execute("ALTER TABLE structure_decisions ADD COLUMN spot_ref REAL")
    except sqlite3.OperationalError:
        pass  # coluna já existe
    
    try:
        conn.execute("ALTER TABLE structure_decisions ADD COLUMN meta_json TEXT")
    except sqlite3.OperationalError:
        pass  # coluna já existe

    conn.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS ux_decision_snapshot
        ON structure_decisions (timestamp, aba)
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_decisions_aba_ts ON structure_decisions (aba, timestamp)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_decisions_ts ON structure_decisions (timestamp)")

    conn.commit()


def insert_payoff_points(
    conn: sqlite3.Connection,
    timestamp: str,
    aba: str,
    points: List[PayoffPoint],
    spot_ref: Optional[float] = None,
    meta: Optional[Dict[str, Any]] = None
) -> int:
    """
    Grava SOMENTE no contrato canônico:
      payoff_curve_points(timestamp, aba, point_spot, point_pl, meta_json)

    Aceita input legado:
      dict com s_t/pl_venc, mas converte para point_spot/point_pl na gravação.

    Idempotente:
      INSERT OR REPLACE + UNIQUE(timestamp, aba, point_spot)
    """
    ensure_derived_tables(conn)

    meta_json = json.dumps(meta, ensure_ascii=False) if meta else None
    cur = conn.cursor()
    count = 0

    sql = """
        INSERT OR REPLACE INTO payoff_curve_points
        (timestamp, aba, point_spot, point_pl, meta_json)
        VALUES (?, ?, ?, ?, ?)
    """

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

        cur.execute(sql, (timestamp, aba, x, y, meta_json))
        count += 1

    conn.commit()
    return count


def insert_structure_decision(
    conn: sqlite3.Connection,
    timestamp: str,
    aba: str,
    decision_dict: Dict[str, Any]
) -> int:
    """
    Insere/atualiza decisão (idempotente por timestamp+aba).
    """
    ensure_derived_tables(conn)

    decision = decision_dict.get("decision", "HOLD")
    level = int(decision_dict.get("level", 0))

    pl_atual = decision_dict.get("pl_atual")
    pl_max = decision_dict.get("pl_max")
    pl_pct_of_max = decision_dict.get("pl_pct_of_max")
    dte_min = decision_dict.get("dte_min")

    # opcionais
    spot_ref = decision_dict.get("spot_ref")
    meta = decision_dict.get("meta")

    why_data = {
        k: v for k, v in decision_dict.items()
        if k not in ["decision", "level", "pl_atual", "pl_max", "pl_pct_of_max", "dte_min", "spot_ref", "meta"]
    }

    why_json = json.dumps(why_data, ensure_ascii=False) if why_data else None
    meta_json = json.dumps(meta, ensure_ascii=False) if meta else None
    created_at = datetime.now().isoformat()

    cur = conn.cursor()
    cur.execute("""
        INSERT OR REPLACE INTO structure_decisions
        (timestamp, aba, decision, level, pl_atual, pl_max, pl_pct_of_max, dte_min, why_json, spot_ref, meta_json, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        timestamp, aba, decision, level,
        pl_atual, pl_max, pl_pct_of_max, dte_min,
        why_json, spot_ref, meta_json, created_at
    ))

    conn.commit()
    return cur.lastrowid


def get_payoff_points(
    conn: sqlite3.Connection,
    aba: str,
    timestamp: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Lê pontos no formato canônico.
    """
    ensure_derived_tables(conn)
    cur = conn.cursor()

    if timestamp:
        cur.execute("""
            SELECT timestamp, aba, point_spot, point_pl, meta_json
            FROM payoff_curve_points
            WHERE aba = ? AND timestamp = ?
            ORDER BY point_spot
        """, (aba, timestamp))
    else:
        cur.execute("""
            SELECT timestamp, aba, point_spot, point_pl, meta_json
            FROM payoff_curve_points
            WHERE aba = ?
            ORDER BY timestamp DESC, point_spot
            LIMIT 100
        """, (aba,))

    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]


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
