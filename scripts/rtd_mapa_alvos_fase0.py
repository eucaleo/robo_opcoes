from __future__ import annotations

import os
import re
import sqlite3
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "docs" / "levantamentos"
OUTDIR.mkdir(parents=True, exist_ok=True)

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
out = OUTDIR / f"mapa_alvos_rtd_fase0_{run_id}.md"

KEY_FILES = [
    "scripts/refresh_rtd_option_quotes_excel.ps1",
    "scripts/refresh_rtd_symbol_to_option_quotes.py",
    "scripts/refresh_rtd_symbol_to_option_quotes_fallback.py",
    "scripts/import_rtd_option_quotes_wide_csv.py",
    "scripts/run_derived_pipeline.py",
    "repositories/rtd_option_quotes_repository.py",
    "repositories/market_snapshot_repository.py",
    "services/market_snapshot_provider.py",
    "services/market_snapshot_selector.py",
    "services/structure_leg_rtd_enrichment_service.py",
    "services/structure_market_input_assembler.py",
    "services/pricing_input_service.py",
    "services/canonical_input_service.py",
    "services/canonical_pricing_facade.py",
    "infra/bootstrap_rtd_option_quotes_schema.py",
    "UI/components/structure_editor_dialog.py",
    "UI/components/terminal_vwap_payoff_dark_panel.py",
    "UI/components/terminal_vwap_payoff_panel.py",
    "UI/main_window.py",
    "controllers/terminal_vwap_payoff_controller.py",
    "services/terminal_vwap_payoff_app_service.py",
]

TERMS = [
    "RTD",
    "LISTA_RTD",
    "rtd_option_quotes",
    "derived.db",
    "subprocess",
    "Popen",
    "run(",
    "refresh_rtd",
    "option_quotes",
    "Excel",
    "win32com",
    "xlwings",
    "openpyxl",
    "vwap",
    "VWAP",
    "bid",
    "ask",
    "last",
    "volume",
    "delta",
    "gamma",
    "theta",
    "vega",
    "iv",
]

TEXT_EXTS = {
    ".py",
    ".ps1",
    ".sh",
    ".md",
    ".txt",
    ".sql",
    ".json",
    ".yml",
    ".yaml",
    ".toml",
    ".ini",
}

EXCLUDE_DIRS = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    "docs/levantamentos",
}

def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except Exception:
        return path.as_posix()

def run_cmd(args: list[str]) -> str:
    try:
        p = subprocess.run(
            args,
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=20,
        )
        data = ""
        if p.stdout:
            data += p.stdout
        if p.stderr:
            data += "\nSTDERR:\n" + p.stderr
        return data.strip()
    except Exception as exc:
        return f"erro ao executar {' '.join(args)}: {exc}"

def is_excluded(path: Path) -> bool:
    parts = path.relative_to(ROOT).parts
    joined = "/".join(parts)
    for ex in EXCLUDE_DIRS:
        if ex in parts or joined.startswith(ex + "/"):
            return True
    return False

def read_text(path: Path) -> list[str]:
    try:
        return path.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception:
        return []

def find_matches(path: Path, max_matches: int = 80, context: int = 2) -> list[str]:
    lines = read_text(path)
    if not lines:
        return []

    pattern = re.compile("|".join(re.escape(t) for t in TERMS), re.IGNORECASE)
    hit_lines = []
    used = set()

    for idx, line in enumerate(lines):
        if pattern.search(line):
            start = max(0, idx - context)
            end = min(len(lines), idx + context + 1)
            for n in range(start, end):
                if n not in used:
                    used.add(n)
                    hit_lines.append(f"{n + 1}: {lines[n]}")
            hit_lines.append("---")
            if len([x for x in hit_lines if x == "---"]) >= max_matches:
                hit_lines.append("LIMITE_DE_TRECHOS_ATINGIDO")
                break

    return hit_lines

def list_candidate_files() -> list[str]:
    candidates = []
    name_pattern = re.compile(
        r"(rtd|excel|option|quote|derived|snapshot|market|pricing|payoff|structure)",
        re.IGNORECASE,
    )

    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if is_excluded(path):
            continue
        if path.suffix.lower() not in TEXT_EXTS:
            continue
        if name_pattern.search(path.name) or rel(path) in KEY_FILES:
            candidates.append(rel(path))

    return sorted(set(candidates))

def sqlite_report() -> str:
    db_path = ROOT / "dados" / "derived.db"
    if not db_path.exists():
        return "Banco dados/derived.db nao encontrado."

    blocks = []
    blocks.append(f"Banco encontrado: {rel(db_path)}")

    try:
        con = sqlite3.connect(str(db_path))
        cur = con.cursor()

        tables = [r[0] for r in cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        ).fetchall()]

        blocks.append("")
        blocks.append("### Tabelas")
        blocks.append("")
        for table in tables:
            blocks.append(f"- {table}")

        focus_tables = [
            t for t in tables
            if any(k in t.lower() for k in ["rtd", "quote", "snapshot", "candle", "market", "payoff", "decision"])
        ]

        blocks.append("")
        blocks.append("### Tabelas focadas")
        blocks.append("")
        if focus_tables:
            for table in focus_tables:
                blocks.append(f"- {table}")
        else:
            blocks.append("- Nenhuma tabela focada encontrada por nome.")

        for table in focus_tables:
            blocks.append("")
            blocks.append(f"### Schema tabela `{table}`")
            blocks.append("")
            blocks.append("```text")
            for row in cur.execute(f"PRAGMA table_info({table})").fetchall():
                blocks.append(str(row))
            blocks.append("```")

            blocks.append("")
            blocks.append(f"### Indices tabela `{table}`")
            blocks.append("")
            blocks.append("```text")
            for row in cur.execute(f"PRAGMA index_list({table})").fetchall():
                blocks.append(str(row))
            blocks.append("```")

            try:
                count = cur.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            except Exception as exc:
                count = f"erro: {exc}"

            blocks.append("")
            blocks.append(f"Total de linhas em `{table}`: {count}")

            if table == "rtd_option_quotes":
                blocks.append("")
                blocks.append("### Amostra `rtd_option_quotes`")
                blocks.append("")
                blocks.append("```text")
                try:
                    cols = [r[1] for r in cur.execute("PRAGMA table_info(rtd_option_quotes)").fetchall()]
                    blocks.append("colunas: " + ", ".join(cols))
                    rows = cur.execute("SELECT * FROM rtd_option_quotes LIMIT 10").fetchall()
                    for row in rows:
                        blocks.append(str(row))
                except Exception as exc:
                    blocks.append(f"erro ao consultar amostra: {exc}")
                blocks.append("```")

        con.close()
    except Exception as exc:
        blocks.append(f"Erro ao inspecionar SQLite: {exc}")

    return "\n".join(blocks)

def file_summary(path: Path) -> str:
    if not path.exists():
        return "arquivo nao encontrado"
    lines = read_text(path)
    return f"{len(lines)} linhas"

def main() -> None:
    lines: list[str] = []

    lines.append("# Mapa compacto de alvos RTD - Fase 0.2")
    lines.append("")
    lines.append(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    lines.append(f"Raiz: {ROOT.as_posix()}")
    lines.append("")

    lines.append("## 1. Git")
    lines.append("")
    lines.append("### Branch")
    lines.append("")
    lines.append("```text")
    lines.append(run_cmd(["git", "branch", "--show-current"]))
    lines.append("```")
    lines.append("")
    lines.append("### Status")
    lines.append("")
    lines.append("```text")
    lines.append(run_cmd(["git", "status", "--short"]))
    lines.append("```")
    lines.append("")
    lines.append("### Ultimo commit")
    lines.append("")
    lines.append("```text")
    lines.append(run_cmd(["git", "log", "-1", "--oneline"]))
    lines.append("```")
    lines.append("")

    lines.append("## 2. Arquivos-chave esperados")
    lines.append("")
    for item in KEY_FILES:
        path = ROOT / item
        status = "existe" if path.exists() else "ausente"
        lines.append(f"- `{item}`: {status}; {file_summary(path) if path.exists() else ''}")
    lines.append("")

    lines.append("## 3. Banco derived.db")
    lines.append("")
    lines.append(sqlite_report())
    lines.append("")

    lines.append("## 4. Arquivos candidatos por nome")
    lines.append("")
    for item in list_candidate_files():
        lines.append(f"- `{item}`")
    lines.append("")

    lines.append("## 5. Trechos focados dos arquivos-chave")
    lines.append("")
    for item in KEY_FILES:
        path = ROOT / item
        if not path.exists():
            continue

        matches = find_matches(path, max_matches=60, context=2)
        lines.append(f"### `{item}`")
        lines.append("")
        if not matches:
            lines.append("Nenhum trecho encontrado pelos termos de busca.")
            lines.append("")
            continue

        lines.append("```text")
        lines.extend(matches)
        lines.append("```")
        lines.append("")

    lines.append("## 6. Busca ampla compacta")
    lines.append("")
    lines.append("```text")

    total_files = 0
    total_hits = 0
    max_total_hits = 500

    for path in ROOT.rglob("*"):
        if total_hits >= max_total_hits:
            lines.append("LIMITE_TOTAL_DE_HITS_ATINGIDO")
            break
        if not path.is_file():
            continue
        if is_excluded(path):
            continue
        if path.suffix.lower() not in TEXT_EXTS:
            continue

        matches = find_matches(path, max_matches=8, context=0)
        if not matches:
            continue

        total_files += 1
        for m in matches:
            if m == "---":
                continue
            if m == "LIMITE_DE_TRECHOS_ATINGIDO":
                continue
            lines.append(f"{rel(path)}:{m}")
            total_hits += 1
            if total_hits >= max_total_hits:
                break

    lines.append("```")
    lines.append("")
    lines.append(f"Arquivos com hits: {total_files}")
    lines.append(f"Hits registrados: {total_hits}")
    lines.append("")
    lines.append("## 7. Conclusao operacional preliminar")
    lines.append("")
    lines.append("- Relatorio gerado sem alteracao funcional.")
    lines.append("- Usar este mapa para definir os pontos exatos da Fase 1.")
    lines.append("- Confirmar manualmente Excel aberto, corretora conectada e RTD atualizando.")
    lines.append("")

    out.write_text("\n".join(lines), encoding="utf-8")
    print(out.relative_to(ROOT).as_posix())

if __name__ == "__main__":
    main()
