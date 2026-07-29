import sys
import sqlite3
import traceback
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]

WORKBOOK_CANDIDATES = [
    ROOT_DIR / "OPERACOES_E_OPCOES.xlsm",
    ROOT_DIR / "OPERACOES_E_OPCOES.xlsx",
]

BRIDGE_FILES = [
    ROOT_DIR / "bridge" / "analise_robo_legs.csv",
    ROOT_DIR / "bridge" / "analise_robo.csv",
    ROOT_DIR / "bridge" / "analise_raiox.csv",
]

MODULE_CANDIDATES = [
    ROOT_DIR / "domain" / "payoff.py",
    ROOT_DIR / "domain" / "payoff_features.py",
    ROOT_DIR / "db" / "derived_repo.py",
    ROOT_DIR / "db" / "reader.py",
    ROOT_DIR / "db" / "writer.py",
]

DB_FILES = [
    ROOT_DIR / "dados" / "app.db",
    ROOT_DIR / "dados" / "app.db",
]

SCRIPT_CANDIDATES = [
    ROOT_DIR / "scripts" / "run_derived_pipeline.py",
    ROOT_DIR / "scripts" / "validate_app_db.py",
]


def log(level: str, message: str) -> None:
    print(f"[{level}] {message}")


def require_any(paths, label: str):
    found = [p for p in paths if p.exists()]
    if not found:
        names = ", ".join(str(p) for p in paths)
        raise FileNotFoundError(f"Nenhum artefato de {label} encontrado. Esperado um de: {names}")
    for path in found:
        log("INFO", f"{label} encontrado: {path}")
    return found


def check_modules() -> None:
    found = require_any(MODULE_CANDIDATES, "módulo central")
    valid_count = 0
    for path in found:
        content = path.read_text(encoding="utf-8")
        if "class " in content or "def " in content:
            valid_count += 1
            log("INFO", f"Módulo validado: {path.name}")

    if valid_count == 0:
        raise ValueError("Nenhum módulo central possui classes/funções detectáveis")


def check_databases() -> None:
    dbs = require_any(DB_FILES, "banco")
    for path in dbs:
        conn = sqlite3.connect(str(path))
        try:
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
            )
            tables = [row[0] for row in cursor.fetchall()]
            if not tables:
                raise ValueError(f"Banco sem tabelas: {path.name}")
            log("INFO", f"{path.name}: {len(tables)} tabelas")
        finally:
            conn.close()


def check_scripts() -> None:
    found = [p for p in SCRIPT_CANDIDATES if p.exists()]
    if not found:
        log("WARN", "Nenhum script operacional E2E encontrado; validação seguirá por artefatos")
        return
    for path in found:
        log("INFO", f"Script operacional encontrado: {path.name}")


def main() -> int:
    try:
        log("INFO", "Iniciando check ponta a ponta local")

        require_any(WORKBOOK_CANDIDATES, "workbook")
        require_any(BRIDGE_FILES, "bridge")
        check_modules()
        check_databases()
        check_scripts()

        log("OK", "check_end_to_end concluído com sucesso")
        return 0

    except Exception as e:
        log("FAIL", f"Erro no check_end_to_end: {e}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
