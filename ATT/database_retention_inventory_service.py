from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any


TEMPORAL_NAME_PARTS = (
    "date",
    "datetime",
    "time",
    "timestamp",
    "created",
    "updated",
    "captured",
    "snapshot",
    "intraday",
    "history",
    "historico",
    "data",
    "hora",
    "ts",
)


def _quote_identifier(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def _is_temporal_column_name(column_name: str) -> bool:
    lowered = column_name.lower()
    return any(part in lowered for part in TEMPORAL_NAME_PARTS)


def build_database_retention_inventory(db_path: str | Path) -> dict[str, Any]:
    path = Path(db_path)

    inventory: dict[str, Any] = {
        "database_path": str(path),
        "exists": path.exists(),
        "table_count": 0,
        "tables": [],
    }

    if not path.exists():
        return inventory

    connection = sqlite3.connect(str(path))
    connection.row_factory = sqlite3.Row

    try:
        connection.execute("PRAGMA query_only = ON")

        table_rows = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%'
            ORDER BY name
            """
        ).fetchall()

        tables: list[dict[str, Any]] = []

        for table_row in table_rows:
            table_name = table_row["name"]
            quoted_table_name = _quote_identifier(table_name)

            column_rows = connection.execute(
                f"PRAGMA table_info({quoted_table_name})"
            ).fetchall()

            columns = [
                {
                    "name": column_row["name"],
                    "type": column_row["type"],
                    "notnull": bool(column_row["notnull"]),
                    "primary_key": bool(column_row["pk"]),
                }
                for column_row in column_rows
            ]

            temporal_columns = [
                column["name"]
                for column in columns
                if _is_temporal_column_name(column["name"])
            ]

            row_count = connection.execute(
                f"SELECT COUNT(*) AS total FROM {quoted_table_name}"
            ).fetchone()["total"]

            tables.append(
                {
                    "name": table_name,
                    "row_count": int(row_count),
                    "columns": columns,
                    "column_count": len(columns),
                    "temporal_columns": temporal_columns,
                }
            )

        inventory["tables"] = tables
        inventory["table_count"] = len(tables)
        return inventory

    finally:
        connection.close()


def format_database_retention_inventory(inventory: dict[str, Any]) -> str:
    lines = [
        "Inventario tecnico do banco",
        f"Banco: {inventory['database_path']}",
        f"Existe: {'sim' if inventory['exists'] else 'nao'}",
        f"Tabelas: {inventory['table_count']}",
    ]

    for table in inventory["tables"]:
        temporal = ", ".join(table["temporal_columns"]) or "nenhuma"
        lines.extend(
            [
                "",
                f"Tabela: {table['name']}",
                f"Registros: {table['row_count']}",
                f"Colunas: {table['column_count']}",
                f"Colunas temporais candidatas: {temporal}",
            ]
        )

    return "\n".join(lines)
