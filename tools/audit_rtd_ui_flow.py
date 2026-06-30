from __future__ import annotations

import inspect
import os
import re
import sqlite3
import sys
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)

DB_GLOBS = [
    "dados/*.db",
    "dados/*.bd",
    "dados/**/*.db",
    "dados/**/*.bd",
]

KEYWORDS = [
    "rtd",
    "excel",
    "win32com",
    "xlwings",
    "rtd_option_quotes",
    "codigo_opcao",
    "BOVAK900",
    "StructureLegRtdEnrichmentService",
    "RtdOptionQuotesRepository",
    "refresh",
    "atualiza",
    "atualizar",
    "hydrate",
    "populate",
    "cotacao",
    "quote",
]


def header(title: str) -> None:
    print()
    print("=" * 100)
    print(title)
    print("=" * 100)


def safe_read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception as exc:
        return f"<<ERRO AO LER {path}: {exc}>>"


def find_dbs() -> list[Path]:
    found: set[Path] = set()
    for pattern in DB_GLOBS:
        for p in ROOT.glob(pattern):
            if p.is_file():
                found.add(p.resolve())
    return sorted(found)


def sqlite_tables(db: Path) -> list[str]:
    try:
        with sqlite3.connect(str(db)) as conn:
            rows = conn.execute(
                "select name from sqlite_master where type='table' order by name"
            ).fetchall()
        return [r[0] for r in rows]
    except Exception as exc:
        print(f"[ERRO] Não consegui listar tabelas de {db}: {exc}")
        return []


def table_columns(conn: sqlite3.Connection, table: str) -> list[str]:
    try:
        return [r[1] for r in conn.execute(f"pragma table_info({table})").fetchall()]
    except Exception:
        return []


def try_query_rtd_table(db: Path) -> None:
    print(f"\nDB: {db.relative_to(ROOT)}")
    print(f"Existe: {db.exists()} | tamanho: {db.stat().st_size if db.exists() else 'N/A'} bytes")

    tables = sqlite_tables(db)
    print("Tabelas com rtd/option/quote/cotacao:")
    candidates = [
        t for t in tables
        if any(k in t.lower() for k in ["rtd", "option", "quote", "cotacao", "opcao"])
    ]
    for t in candidates:
        print(f"  - {t}")

    if "rtd_option_quotes" not in tables:
        print("Tabela rtd_option_quotes: NÃO encontrada.")
        return

    try:
        conn = sqlite3.connect(str(db))
        conn.row_factory = sqlite3.Row

        cols = table_columns(conn, "rtd_option_quotes")
        print("Colunas rtd_option_quotes:", cols)

        total = conn.execute("select count(*) as n from rtd_option_quotes").fetchone()["n"]
        print("Total linhas:", total)

        # Busca direta pelo ticker correto informado pelo usuário.
        if "codigo_opcao" in cols:
            print("\nBusca direta por codigo_opcao = BOVAK900:")
            rows = conn.execute(
                """
                select *
                from rtd_option_quotes
                where upper(codigo_opcao) = 'BOVAK900'
                limit 10
                """
            ).fetchall()
            for row in rows:
                print(dict(row))
            if not rows:
                print("  Nenhum registro direto.")

            print("\nBusca aproximada por BOVA/K900/900:")
            rows = conn.execute(
                """
                select *
                from rtd_option_quotes
                where upper(codigo_opcao) like '%BOVA%'
                   or upper(codigo_opcao) like '%K900%'
                   or upper(codigo_opcao) like '%900%'
                limit 30
                """
            ).fetchall()
            for row in rows:
                print(dict(row))
            if not rows:
                print("  Nenhum registro aproximado.")

        # Tenta identificar colunas de timestamp.
        time_cols = [
            c for c in cols
            if any(k in c.lower() for k in ["updated", "created", "timestamp", "data", "hora", "dt_"])
        ]

        for tc in time_cols[:3]:
            try:
                print(f"\nÚltimos registros por {tc}:")
                rows = conn.execute(
                    f"""
                    select *
                    from rtd_option_quotes
                    order by {tc} desc
                    limit 5
                    """
                ).fetchall()
                for row in rows:
                    print(dict(row))
                break
            except Exception:
                pass

        conn.close()

    except Exception as exc:
        print(f"[ERRO] Consulta rtd_option_quotes em {db}: {exc}")


def grep_sources() -> None:
    header("2) Varredura de código por RTD/Excel/repositories/services/UI")

    allowed_ext = {
        ".py",
        ".txt",
        ".md",
        ".sql",
        ".ini",
        ".toml",
        ".yaml",
        ".yml",
        ".json",
    }

    skip_dirs = {
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        ".pytest_cache",
        "node_modules",
    }

    hits: list[tuple[Path, int, str]] = []

    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in allowed_ext:
            continue
        if any(part in skip_dirs for part in path.parts):
            continue

        text = safe_read(path)
        low = text.lower()

        if not any(k.lower() in low for k in KEYWORDS):
            continue

        for i, line in enumerate(text.splitlines(), 1):
            line_low = line.lower()
            if any(k.lower() in line_low for k in KEYWORDS):
                hits.append((path.relative_to(ROOT), i, line.strip()))

    for path, line_no, line in hits:
        print(f"{path}:{line_no}: {line}")


def print_file(path_str: str, max_lines: int = 260) -> None:
    path = ROOT / path_str
    header(f"3) Fonte: {path_str}")
    if not path.exists():
        print("Arquivo não encontrado.")
        return

    lines = safe_read(path).splitlines()
    for i, line in enumerate(lines[:max_lines], 1):
        print(f"{i:04d}: {line}")


def inspect_runtime_imports() -> None:
    header("4) Inspeção runtime dos objetos RTD")

    imports = [
        ("repositories.rtd_option_quotes_repository", "RtdOptionQuotesRepository"),
        ("services.structure_leg_rtd_enrichment_service", "StructureLegRtdEnrichmentService"),
        ("UI.components.structure_editor_dialog", "StructureEditorDialog"),
    ]

    for mod_name, attr in imports:
        print(f"\nImportando {mod_name}.{attr}")
        try:
            mod = __import__(mod_name, fromlist=[attr])
            obj = getattr(mod, attr)
            print("OK:", obj)
            try:
                print("Assinatura:", inspect.signature(obj))
            except Exception:
                pass
            try:
                print("Arquivo:", inspect.getsourcefile(obj))
            except Exception:
                pass
        except Exception as exc:
            print("ERRO:", repr(exc))


def try_enrichment_against_all_dbs() -> None:
    header("5) Teste direto do enrichment service contra todos os bancos encontrados")

    try:
        from repositories.rtd_option_quotes_repository import RtdOptionQuotesRepository
        from services.structure_leg_rtd_enrichment_service import StructureLegRtdEnrichmentService
    except Exception as exc:
        print("Não consegui importar service/repository:", repr(exc))
        return

    for db in find_dbs():
        print(f"\nTestando DB: {db.relative_to(ROOT)}")
        try:
            repo = RtdOptionQuotesRepository(str(db))
            service = StructureLegRtdEnrichmentService(repo)
            result = service.enrich(
                {
                    "symbol": "BOVAK900",
                    "position_side": "COMPRA",
                    "quantity": 1,
                    "multiplier": 1,
                    "leg_order": 1,
                    "notes": None,
                }
            )
            print("SUCESSO:")
            print(result)
        except Exception as exc:
            print("FALHOU:", repr(exc))


def search_possible_old_refresh_functions() -> None:
    header("6) Candidatos a fluxo antigo de atualização RTD/Excel")

    patterns = [
        r"def\s+\w*refresh\w*",
        r"def\s+\w*atualiza\w*",
        r"def\s+\w*update\w*",
        r"def\s+\w*rtd\w*",
        r"def\s+\w*excel\w*",
        r"class\s+\w*Rtd\w*",
        r"class\s+\w*Excel\w*",
        r"win32com",
        r"xlwings",
        r"Dispatch\(",
        r"EnsureDispatch\(",
    ]

    regexes = [re.compile(p, re.IGNORECASE) for p in patterns]

    skip_dirs = {
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        ".pytest_cache",
    }

    for path in ROOT.rglob("*.py"):
        if any(part in skip_dirs for part in path.parts):
            continue

        text = safe_read(path)
        for i, line in enumerate(text.splitlines(), 1):
            if any(rx.search(line) for rx in regexes):
                print(f"{path.relative_to(ROOT)}:{i}: {line.strip()}")


def main() -> None:
    header("1) Bancos encontrados e estado de rtd_option_quotes")
    dbs = find_dbs()
    if not dbs:
        print("Nenhum banco .db/.bd encontrado em dados/.")
    for db in dbs:
        try_query_rtd_table(db)

    grep_sources()

    for f in [
        "repositories/rtd_option_quotes_repository.py",
        "services/structure_leg_rtd_enrichment_service.py",
        "UI/components/structure_editor_dialog.py",
        "UI/main_window.py",
        "UI/components/terminal_vwap_payoff_dark_panel.py",
    ]:
        print_file(f)

    inspect_runtime_imports()
    try_enrichment_against_all_dbs()
    search_possible_old_refresh_functions()

    header("FIM DA AUDITORIA")
    print("Cole a saída relevante aqui, principalmente:")
    print("- item 1: banco que contém rtd_option_quotes;")
    print("- item 5: se BOVAK900 funciona em algum banco;")
    print("- item 6: funções antigas de refresh/update/RTD/Excel.")


if __name__ == "__main__":
    main()
