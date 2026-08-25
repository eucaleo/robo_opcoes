"""Repositorio local para consultas de metadata do app.db."""

from typing import List


def list_tables(conn) -> List[str]:
    """Retorna nomes de tabelas registradas no banco local."""
    cur = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    )
    return [row["name"] for row in cur.fetchall()]

def list_columns(conn, table: str) -> List[str]:
    """Retorna nomes de colunas de uma tabela do banco local."""
    cur = conn.execute(f"PRAGMA table_info({table})")
    return [row["name"] for row in cur.fetchall()]

