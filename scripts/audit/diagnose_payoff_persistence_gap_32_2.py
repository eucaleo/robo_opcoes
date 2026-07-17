#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Diagnóstico 32.2 - Gap de persistência de payoff.

Objetivo:
- Confirmar onde o fluxo backend para depois do pricing.
- Mapear arquivos que mencionam:
  - PayoffRefreshCommandService
  - PricingExecutionAppService
  - PricingExecutionOrchestrationService
  - PricingExecutionService
  - DerivedPayoffPersistence
  - payoff_curve_points
  - structure_decisions
  - execute_pricing
- Inspecionar contagens e últimas linhas relevantes no banco informado por APP_DB_PATH.

Uso:
APP_DB_PATH="./dados/app.db" STRUCTURE_ID=2 python scripts/audit/diagnose_payoff_persistence_gap_32_2.py
"""

from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path
from datetime import datetime


ROOT = Path.cwd()
OUT_DIR = ROOT / "AUDITORIA_POS_PATCH_32"
OUT_DIR.mkdir(exist_ok=True)

REPORT_JSON = OUT_DIR / "RELATORIO_32_2_DIAGNOSE_PAYOFF_PERSISTENCE_GAP.json"
REPORT_MD = OUT_DIR / "RELATORIO_32_2_DIAGNOSE_PAYOFF_PERSISTENCE_GAP.md"

TOKENS = [
    "PayoffRefreshCommandService",
    "PricingExecutionAppService",
    "PricingExecutionOrchestrationService",
    "PricingExecutionService",
    "DerivedPayoffPersistence",
    "payoff_curve_points",
    "structure_decisions",
    "execute_pricing",
    "persist_derived",
    "derived_payoff",
    "payoff_curve",
]

IGNORE_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    "AUDITORIA_POS_PATCH_32",
}


def should_skip(path: Path) -> bool:
    parts = set(path.parts)
    return bool(parts & IGNORE_DIRS)


def safe_read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding="latin-1")
        except Exception:
            return ""
    except Exception:
        return ""


def scan_sources() -> dict:
    hits = {}

    for path in ROOT.rglob("*"):
        if should_skip(path):
            continue

        if not path.is_file():
            continue

        if path.suffix.lower() not in {".py", ".js", ".ts", ".tsx", ".jsx", ".sql", ".md"}:
            continue

        text = safe_read(path)
        if not text:
            continue

        found = []
        for token in TOKENS:
            if token in text:
                found.append(token)

        if found:
            rel = str(path.relative_to(ROOT)).replace("\\", "/")
            hits[rel] = {
                "tokens": found,
                "line_hits": collect_line_hits(text, found),
            }

    return hits


def collect_line_hits(text: str, tokens: list[str]) -> list[dict]:
    rows = []
    lines = text.splitlines()

    for idx, line in enumerate(lines, start=1):
        matched = [token for token in tokens if token in line]
        if matched:
            rows.append(
                {
                    "line": idx,
                    "tokens": matched,
                    "text": line.strip()[:300],
                }
            )

    return rows[:80]


def table_exists(cur: sqlite3.Cursor, table: str) -> bool:
    cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name = ?",
        (table,),
    )
    return cur.fetchone() is not None


def get_columns(cur: sqlite3.Cursor, table: str) -> list[str]:
    if not table_exists(cur, table):
        return []

    cur.execute(f"PRAGMA table_info({table})")
    return [row[1] for row in cur.fetchall()]


def count_table(cur: sqlite3.Cursor, table: str, structure_id: str | None = None) -> dict:
    if not table_exists(cur, table):
        return {"exists": False, "count_total": None, "count_structure": None}

    result = {"exists": True, "count_total": None, "count_structure": None}

    cur.execute(f"SELECT COUNT(*) FROM {table}")
    result["count_total"] = cur.fetchone()[0]

    columns = get_columns(cur, table)
    structure_col = None
    for candidate in ["structure_id", "id_structure", "estrutura_id"]:
        if candidate in columns:
            structure_col = candidate
            break

    if structure_id and structure_col:
        cur.execute(f"SELECT COUNT(*) FROM {table} WHERE {structure_col} = ?", (structure_id,))
        result["count_structure"] = cur.fetchone()[0]

    return result


def fetch_last_rows(cur: sqlite3.Cursor, table: str, limit: int = 5) -> list[dict]:
    if not table_exists(cur, table):
        return []

    columns = get_columns(cur, table)
    order_col = None

    for candidate in ["created_at", "updated_at", "id", "execution_id"]:
        if candidate in columns:
            order_col = candidate
            break

    cols_sql = ", ".join(columns[:20])

    if order_col:
        sql = f"SELECT {cols_sql} FROM {table} ORDER BY {order_col} DESC LIMIT ?"
    else:
        sql = f"SELECT {cols_sql} FROM {table} LIMIT ?"

    try:
        cur.execute(sql, (limit,))
        rows = cur.fetchall()
        return [dict(zip(columns[:20], row)) for row in rows]
    except Exception as exc:
        return [{"error": str(exc)}]


def inspect_db() -> dict:
    db_path = os.environ.get("APP_DB_PATH")
    structure_id = os.environ.get("STRUCTURE_ID")

    if not db_path:
        return {
            "enabled": False,
            "reason": "APP_DB_PATH não definido.",
        }

    path = Path(db_path)
    if not path.exists():
        return {
            "enabled": False,
            "reason": f"Banco não encontrado: {db_path}",
        }

    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    tables = [
        "structures",
        "pricing_executions",
        "structure_snapshots",
        "system_snapshots",
        "payoff_curve_points",
        "structure_decisions",
    ]

    result = {
        "enabled": True,
        "db_path": str(path.resolve()),
        "structure_id": structure_id,
        "tables": {},
    }

    for table in tables:
        result["tables"][table] = {
            "columns": get_columns(cur, table),
            "counts": count_table(cur, table, structure_id),
            "last_rows": fetch_last_rows(cur, table),
        }

    conn.close()
    return result


def build_markdown(payload: dict) -> str:
    lines = []
    lines.append("# Relatório 32.2 - Diagnóstico do gap de persistência de payoff")
    lines.append("")
    lines.append(f"- Gerado em: `{payload['generated_at']}`")
    lines.append(f"- Branch: `{payload.get('git_branch') or 'não detectada'}`")
    lines.append("")

    lines.append("## 1. Leitura do problema")
    lines.append("")
    lines.append("O teste anterior indicou que o pricing executa e snapshot incrementa, mas `payoff_curve_points` e `structure_decisions` não aumentam.")
    lines.append("")
    lines.append("Isso aponta para falha depois da execução do pricing e antes/durante a persistência derivada.")
    lines.append("")

    lines.append("## 2. Arquivos encontrados por token")
    lines.append("")

    source_hits = payload["source_hits"]

    if not source_hits:
        lines.append("Nenhum arquivo encontrado com os tokens procurados.")
    else:
        for file_path, info in sorted(source_hits.items()):
            lines.append(f"### `{file_path}`")
            lines.append("")
            lines.append("Tokens:")
            for token in info["tokens"]:
                lines.append(f"- `{token}`")
            lines.append("")
            lines.append("Linhas relevantes:")
            for hit in info["line_hits"][:30]:
                lines.append(f"- L{hit['line']}: `{hit['text']}`")
            lines.append("")

    lines.append("## 3. Inspeção do banco")
    lines.append("")

    db = payload["db"]

    if not db.get("enabled"):
        lines.append(f"Banco não inspecionado: {db.get('reason')}")
    else:
        lines.append(f"- DB: `{db['db_path']}`")
        lines.append(f"- STRUCTURE_ID: `{db.get('structure_id')}`")
        lines.append("")

        for table, info in db["tables"].items():
            counts = info["counts"]
            lines.append(f"### `{table}`")
            lines.append("")
            lines.append(f"- Existe: `{counts['exists']}`")
            lines.append(f"- Total: `{counts['count_total']}`")
            lines.append(f"- Total da estrutura: `{counts['count_structure']}`")
            lines.append(f"- Colunas: `{', '.join(info['columns'])}`")
            lines.append("")

    lines.append("## 4. Próxima correção sugerida")
    lines.append("")
    lines.append("Se o relatório confirmar que `DerivedPayoffPersistence` existe mas não é chamado no fluxo do comando, a correção deve conectar o resultado de `execute_pricing()` ao persistidor oficial.")
    lines.append("")
    lines.append("Se ele é chamado, mas não grava pontos, a correção deve ajustar o parser do payload retornado pelo pricing.")
    lines.append("")
    lines.append("Não corrigir UI ainda.")
    lines.append("")

    return "\n".join(lines)


def get_git_branch() -> str | None:
    head = ROOT / ".git" / "HEAD"
    if not head.exists():
        return None

    text = safe_read(head).strip()
    if text.startswith("ref:"):
        return text.split("/")[-1]

    return text[:12] if text else None


def main() -> None:
    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "git_branch": get_git_branch(),
        "source_hits": scan_sources(),
        "db": inspect_db(),
    }

    REPORT_JSON.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )

    REPORT_MD.write_text(
        build_markdown(payload),
        encoding="utf-8",
    )

    print(f"OK: JSON gerado em {REPORT_JSON}")
    print(f"OK: Markdown gerado em {REPORT_MD}")


if __name__ == "__main__":
    main()
