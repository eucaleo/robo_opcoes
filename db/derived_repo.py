"""
Repositório para operações com dados derivados (payoff e decisões).
Tabelas: payoff_curve_points, structure_decisions
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

def ensure_derived_tables(conn: sqlite3.Connection):
    """Cria as tabelas derivadas se não existirem."""
    
    # Tabela para pontos da curva de payoff
    conn.execute("""
        CREATE TABLE IF NOT EXISTS payoff_curve_points (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            aba TEXT NOT NULL,
            s_t REAL NOT NULL,
            pl_venc REAL NOT NULL,
            spot_ref REAL,
            meta_json TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Tabela para decisões das estruturas
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
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()

def insert_payoff_points(
    conn: sqlite3.Connection,
    timestamp: str,
    aba: str,
    points: List[Dict[str, float]],
    spot_ref: Optional[float] = None,
    meta: Optional[Dict[str, Any]] = None
) -> int:
    """
    Insere pontos da curva de payoff.
    
    Args:
        conn: Conexão SQLite
        timestamp: Timestamp dos dados (ISO format)
        aba: Nome da aba/estrutura
        points: Lista de dicts com 's_t' e 'pl_venc'
        spot_ref: Preço spot de referência
        meta: Metadados adicionais (JSON)
    
    Returns:
        Número de pontos inseridos
    """
    ensure_derived_tables(conn)
    
    meta_json = json.dumps(meta) if meta else None
    
    cursor = conn.cursor()
    count = 0
    
    for point in points:
        cursor.execute("""
            INSERT INTO payoff_curve_points 
            (timestamp, aba, s_t, pl_venc, spot_ref, meta_json)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            timestamp,
            aba,
            point['s_t'],
            point['pl_venc'],
            spot_ref,
            meta_json
        ))
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
    Insere uma decisão de estrutura.
    
    Args:
        conn: Conexão SQLite
        timestamp: Timestamp dos dados (ISO format)
        aba: Nome da aba/estrutura
        decision_dict: Dicionário com campos da decisão
    
    Returns:
        ID do registro inserido
    """
    ensure_derived_tables(conn)
    
    # Extrair campos obrigatórios
    decision = decision_dict.get('decision', 'HOLD')
    level = decision_dict.get('level', 0)
    
    # Campos opcionais
    pl_atual = decision_dict.get('pl_atual')
    pl_max = decision_dict.get('pl_max')
    pl_pct_of_max = decision_dict.get('pl_pct_of_max')
    dte_min = decision_dict.get('dte_min')
    
    # Metadados extras como JSON
    why_data = {k: v for k, v in decision_dict.items() 
                if k not in ['decision', 'level', 'pl_atual', 'pl_max', 'pl_pct_of_max', 'dte_min']}
    why_json = json.dumps(why_data) if why_data else None
    
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO structure_decisions 
        (timestamp, aba, decision, level, pl_atual, pl_max, pl_pct_of_max, dte_min, why_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        timestamp,
        aba,
        decision,
        level,
        pl_atual,
        pl_max,
        pl_pct_of_max,
        dte_min,
        why_json
    ))
    
    conn.commit()
    return cursor.lastrowid

def get_latest_decisions(conn: sqlite3.Connection, limit: int = 10) -> List[Dict]:
    """Recupera as últimas decisões registradas."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM structure_decisions 
        ORDER BY created_at DESC 
        LIMIT ?
    """, (limit,))
    
    columns = [desc[0] for desc in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def get_payoff_points(
    conn: sqlite3.Connection, 
    aba: str, 
    timestamp: Optional[str] = None
) -> List[Dict]:
    """Recupera pontos de payoff para uma estrutura."""
    cursor = conn.cursor()
    
    if timestamp:
        cursor.execute("""
            SELECT * FROM payoff_curve_points 
            WHERE aba = ? AND timestamp = ?
            ORDER BY s_t
        """, (aba, timestamp))
    else:
        cursor.execute("""
            SELECT * FROM payoff_curve_points 
            WHERE aba = ?
            ORDER BY timestamp DESC, s_t
            LIMIT 100
        """, (aba,))
    
    columns = [desc[0] for desc in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def cleanup_old_payoff_data(conn, days_to_keep=30):
    cursor = conn.cursor()
    cursor.execute(f"""
        DELETE FROM payoff_curve_points
        WHERE datetime(timestamp) < datetime('now', '-{days_to_keep} days')
    """)
    deleted = cursor.rowcount
    conn.commit()
    return deleted

def cleanup_old_decisions(conn, days_to_keep=30):
    """
    Remove registros antigos de structure_decisions, considerando o campo timestamp.
    """
    cursor = conn.cursor()
    cursor.execute(f"""
        DELETE FROM structure_decisions
        WHERE datetime(timestamp) < datetime('now', '-{days_to_keep} days')
    """)
    deleted = cursor.rowcount
    conn.commit()
    return deleted


