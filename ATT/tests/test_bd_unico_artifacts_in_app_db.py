from __future__ import annotations

import re
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
APP_DB = ROOT / "dados" / "app.db"

APP_CODE_DIRS = (
    "db",
    "domain",
    "services",
    "controllers",
    "repositories",
    "Scripts",
    "scripts",
    "UI",
    "ui",
)

ARCHIVAL_DB_PARTS = {
    ("dados", "backups"),
}

DERIVED_ARTIFACT_TABLES = {
    "payoff_curve_points",
    "structure_decisions",
    "system_snapshots",
    "structure_snapshots",
    "pricing_executions",
    "pricing_execution_events",
    "market_snapshots",
    "simulation_results",
    "simulation_cache",
    "payoff_cache",
}

REQUIRED_CANONICAL_PAYOFF_COLUMNS = {
    "structure_id",
    "timestamp",
    "aba",
    "point_spot",
    "point_pl",
}

LEGACY_DATABASE_PATH_PATTERNS = (
    r"\b" + "derived" + r"\.db\b",
    r"\b" + "derived" + "_" + "db" + r"\.db\b",
    r"\bderivados\.db\b",
    r"\bderivado\.db\b",
    r"\bpayoff\.db\b",
    r"\bsimulation\.db\b",
    r"\bsimulations\.db\b",
    r"\bsimulacoes\.db\b",
    r"\bsimulações\.db\b",
    r"\bcache\.db\b",
    r"\bmarket_snapshot\.db\b",
    r"\bmarket_snapshots\.db\b",
    r"\bstructure_snapshot\.db\b",
    r"\bstructure_snapshots\.db\b",
    r"\b" + "DERIVED" + "_" + "DB" + "_" + "PATH" + r"\b",
    r"\b" + "derived" + "_" + "db" + "_" + "path" + r"\b",
)


def _sqlite_tables(db_path: Path) -> set[str]:
    with sqlite3.connect(str(db_path)) as conn:
        rows = conn.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            """
        ).fetchall()
    return {str(row[0]) for row in rows}


def _sqlite_columns(db_path: Path, table: str) -> set[str]:
    with sqlite3.connect(str(db_path)) as conn:
        rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return {str(row[1]) for row in rows}


def _is_archival_db(path: Path) -> bool:
    rel_parts = path.relative_to(ROOT).parts

    for prefix in ARCHIVAL_DB_PARTS:
        if rel_parts[: len(prefix)] == prefix:
            return True

    return False


def _iter_active_db_files_under_dados() -> list[Path]:
    dados = ROOT / "dados"
    if not dados.exists():
        return []

    files: list[Path] = []
    for pattern in ("*.db", "*.sqlite", "*.sqlite3"):
        files.extend(dados.rglob(pattern))

    active_files = [
        path.resolve()
        for path in files
        if not _is_archival_db(path.resolve())
    ]

    return sorted(set(active_files))


def _iter_application_python_files() -> list[Path]:
    files: list[Path] = []

    for rel_dir in APP_CODE_DIRS:
        base = ROOT / rel_dir
        if not base.exists():
            continue

        for path in base.rglob("*.py"):
            parts = set(path.parts)
            if "__pycache__" in parts:
                continue
            files.append(path)

    return sorted(files)


def test_app_db_exists_and_has_canonical_payoff_artifact_table():
    assert APP_DB.exists(), "dados/app.db deve existir como banco unico canonico."

    tables = _sqlite_tables(APP_DB)
    assert "payoff_curve_points" in tables, (
        "A tabela canonica payoff_curve_points deve existir em dados/app.db."
    )

    cols = _sqlite_columns(APP_DB, "payoff_curve_points")
    missing = REQUIRED_CANONICAL_PAYOFF_COLUMNS - cols

    assert not missing, (
        "payoff_curve_points em dados/app.db nao possui colunas canonicas "
        f"obrigatorias: {sorted(missing)}"
    )


def test_active_derived_artifact_tables_exist_only_in_app_db_under_dados():
    assert APP_DB.exists(), "dados/app.db deve existir."

    offenders: list[str] = []

    for db_path in _iter_active_db_files_under_dados():
        if db_path == APP_DB.resolve():
            continue

        try:
            tables = _sqlite_tables(db_path)
        except sqlite3.DatabaseError:
            continue

        artifact_tables = sorted(tables & DERIVED_ARTIFACT_TABLES)
        if artifact_tables:
            offenders.append(
                f"{db_path.relative_to(ROOT)} contem tabelas derivadas: "
                f"{artifact_tables}"
            )

    assert not offenders, (
        "Artefatos derivados ativos devem residir exclusivamente em dados/app.db. "
        "Bancos auxiliares ativos encontrados:\n- " + "\n- ".join(offenders)
    )


def test_application_code_does_not_reference_legacy_database_paths_for_artifacts():
    compiled = [
        re.compile(pattern, re.IGNORECASE)
        for pattern in LEGACY_DATABASE_PATH_PATTERNS
    ]

    offenders: list[str] = []

    for path in _iter_application_python_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in compiled:
            if pattern.search(text):
                offenders.append(
                    f"{path.relative_to(ROOT)} referencia padrao legado "
                    f"{pattern.pattern!r}"
                )

    assert not offenders, (
        "Codigo de aplicacao nao deve referenciar caminhos/variaveis de bancos "
        "auxiliares legados para artefatos derivados. Ocorrencias:\n- "
        + "\n- ".join(offenders)
    )


def test_payoff_readers_are_bound_to_app_db_canonical_payoff_table():
    ui_data = ROOT / "UI" / "models" / "ui_data.py"
    details_panel = ROOT / "UI" / "components" / "details_panel.py"

    assert ui_data.exists(), "UI/models/ui_data.py deve existir."
    assert details_panel.exists(), "UI/components/details_panel.py deve existir."

    ui_text = ui_data.read_text(encoding="utf-8", errors="ignore")
    details_text = details_panel.read_text(encoding="utf-8", errors="ignore")

    assert "payoff_curve_points" in ui_text, (
        "UI/models/ui_data.py deve reconhecer payoff_curve_points como tabela "
        "canonica de payoff no app.db."
    )
    assert "point_spot" in ui_text, (
        "UI/models/ui_data.py deve reconhecer point_spot no contrato canonico."
    )
    assert "point_pl" in ui_text, (
        "UI/models/ui_data.py deve reconhecer point_pl no contrato canonico."
    )

    assert "_fetch_payoff_points_from_app_db" in details_text, (
        "details_panel deve carregar pontos de payoff por fluxo explicito do app.db."
    )
    assert "payoff_curve_points" in details_text, (
        "details_panel deve consultar payoff_curve_points no app.db."
    )
