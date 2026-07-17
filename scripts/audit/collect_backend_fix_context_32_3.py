#!/usr/bin/env python3
from __future__ import annotations

import ast
import os
import sqlite3
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path.cwd()
OUT_DIR = ROOT / "AUDITORIA_POS_PATCH_32"
OUT_MD = OUT_DIR / "RELATORIO_32_3_CONTEXTO_CORRECAO_BACKEND.md"

FILES = [
    "services/pricing_execution_app_service.py",
    "services/pricing_execution_orchestration_service.py",
    "services/pricing_execution_persistence_service.py",
    "services/derived_payoff_persistence.py",
    "services/derived_service.py",
    "services/canonical_pricing_facade.py",
    "services/payoff_refresh_command_service.py",
]


TOKENS = [
    "execute_pricing",
    "PricingExecutionAppService",
    "PricingExecutionOrchestrationService",
    "PricingExecutionPersistenceService",
    "DerivedPayoffPersistence",
    "payoff_persistence_port",
    "payoff_curve_points",
    "structure_decisions",
    "persist",
    "save",
    "insert",
    "payoff_points",
    "payoff_curve",
    "decision",
]


def run(cmd: list[str]) -> str:
    try:
        return subprocess.check_output(
            cmd,
            cwd=ROOT,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
        ).strip()
    except Exception as exc:
        return f"ERRO ao executar {' '.join(cmd)}: {exc}"


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def line_hits(text: str) -> list[str]:
    hits: list[str] = []
    for idx, line in enumerate(text.splitlines(), start=1):
        lowered = line.lower()
        if any(token.lower() in lowered for token in TOKENS):
            hits.append(f"L{idx}: {line.rstrip()}")
    return hits


def ast_summary(path: Path, text: str) -> list[str]:
    result: list[str] = []
    if not text.strip():
        return result

    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        return [f"ERRO DE SINTAXE AST: {exc}"]

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            result.append(f"class {node.name} @ L{node.lineno}")
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    args = [arg.arg for arg in item.args.args]
                    result.append(
                        f"  def {item.name}({', '.join(args)}) @ L{item.lineno}"
                    )
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            parent_classes = [
                cls
                for cls in ast.walk(tree)
                if isinstance(cls, ast.ClassDef)
                and any(child is node for child in cls.body)
            ]
            if not parent_classes:
                args = [arg.arg for arg in node.args.args]
                result.append(f"def {node.name}({', '.join(args)}) @ L{node.lineno}")

    return result


def extract_context(text: str, center_line: int, radius: int = 35) -> str:
    lines = text.splitlines()
    start = max(1, center_line - radius)
    end = min(len(lines), center_line + radius)

    rendered = []
    for line_no in range(start, end + 1):
        rendered.append(f"{line_no:04d}: {lines[line_no - 1]}")
    return "\n".join(rendered)


def find_token_contexts(text: str, tokens: list[str], radius: int = 25) -> list[str]:
    contexts: list[str] = []
    lines = text.splitlines()

    matched_lines = []
    for idx, line in enumerate(lines, start=1):
        lowered = line.lower()
        if any(token.lower() in lowered for token in tokens):
            matched_lines.append(idx)

    selected: list[int] = []
    for line_no in matched_lines:
        if not selected or line_no - selected[-1] > radius:
            selected.append(line_no)

    for line_no in selected[:12]:
        contexts.append(extract_context(text, line_no, radius=radius))

    return contexts


def db_schema_section() -> str:
    db_path = os.environ.get("APP_DB_PATH")
    if not db_path:
        return "APP_DB_PATH não definido. Schema do banco não coletado."

    path = Path(db_path)
    if not path.is_absolute():
        path = ROOT / path

    if not path.exists():
        return f"Banco não encontrado: {path}"

    wanted_tables = [
        "pricing_executions",
        "structure_snapshots",
        "system_snapshots",
        "payoff_curve_points",
        "structure_decisions",
        "structures",
        "structure_legs",
        "rtd_option_quotes",
        "rtd_underlying_quotes",
    ]

    out: list[str] = []
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row

    try:
        for table in wanted_tables:
            exists = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                (table,),
            ).fetchone()

            out.append(f"### `{table}`")
            if not exists:
                out.append("")
                out.append("Tabela ausente.")
                out.append("")
                continue

            cols = conn.execute(f"PRAGMA table_info({table})").fetchall()
            out.append("")
            out.append("| cid | name | type | notnull | pk |")
            out.append("|---:|---|---|---:|---:|")
            for col in cols:
                out.append(
                    f"| {col['cid']} | {col['name']} | {col['type']} | "
                    f"{col['notnull']} | {col['pk']} |"
                )

            count = conn.execute(f"SELECT COUNT(*) AS n FROM {table}").fetchone()["n"]
            out.append("")
            out.append(f"Total de linhas: `{count}`")
            out.append("")

    finally:
        conn.close()

    return "\n".join(out)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    md: list[str] = []
    md.append("# Relatório 32.3 - Contexto para correção backend payoff")
    md.append("")
    md.append("## 1. Git")
    md.append("")
    md.append("```text")
    md.append(run(["git", "branch", "--show-current"]))
    md.append(run(["git", "status", "--short"]))
    md.append("```")
    md.append("")

    md.append("## 2. Arquivos backend analisados")
    md.append("")

    for rel in FILES:
        path = ROOT / rel
        text = read_text(path)

        md.append(f"## Arquivo `{rel}`")
        md.append("")

        if not path.exists():
            md.append("Arquivo não encontrado.")
            md.append("")
            continue

        md.append("### 2.1 Classes e métodos")
        md.append("")
        md.append("```text")
        summary = ast_summary(path, text)
        md.append("\n".join(summary) if summary else "Sem classes/métodos detectados.")
        md.append("```")
        md.append("")

        md.append("### 2.2 Linhas relevantes")
        md.append("")
        md.append("```text")
        hits = line_hits(text)
        md.append("\n".join(hits[:220]) if hits else "Sem hits.")
        md.append("```")
        md.append("")

        md.append("### 2.3 Contextos de persistência/payoff")
        md.append("")
        contexts = find_token_contexts(
            text,
            [
                "payoff_persistence_port",
                "DerivedPayoffPersistence",
                "payoff_curve_points",
                "structure_decisions",
                "payoff_points",
                "execute_pricing",
            ],
            radius=28,
        )
        if not contexts:
            md.append("Sem contextos relevantes.")
            md.append("")
        else:
            for i, context in enumerate(contexts, start=1):
                md.append(f"#### Contexto {i}")
                md.append("")
                md.append("```python")
                md.append(context)
                md.append("```")
                md.append("")

    md.append("## 3. Schema do banco")
    md.append("")
    md.append(db_schema_section())
    md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    print(f"OK: relatório gerado em {OUT_MD}")


if __name__ == "__main__":
    main()
