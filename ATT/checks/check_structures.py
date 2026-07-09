import sys
import sqlite3
import traceback
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]

WORKBOOK_CANDIDATES = [
    ROOT_DIR / "OPERACOES_E_OPCOES.xlsm",
    ROOT_DIR / "OPERACOES_E_OPCOES.xlsx",
]

BRIDGE_CANDIDATES = [
    ROOT_DIR / "bridge" / "analise_robo.csv",
    ROOT_DIR / "bridge" / "analise_robo_legs.csv",
    ROOT_DIR / "bridge" / "configurações.csv",
    ROOT_DIR / "bridge" / "consolidações.csv",
]

MODULE_CANDIDATES = [
    ROOT_DIR / "domain" / "payoff.py",
    ROOT_DIR / "domain" / "payoff_features.py",
]

DB_CANDIDATES = [
    ROOT_DIR / "dados" / "app.db",
    ROOT_DIR / "dados" / "app.db",
]

SCRIPT_CANDIDATES = [
    ROOT_DIR / "Scripts" / "run_derived_pipeline.py",
    ROOT_DIR / "Scripts" / "build_payoff_summaries.py",
    ROOT_DIR / "Scripts" / "validate_derived_db.py",
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


def inspect_module(path: Path) -> None:
    content = path.read_text(encoding="utf-8")
    if "class " not in content and "def " not in content:
        raise ValueError(f"Módulo sem funções/classes aparentes: {path.name}")
    log("INFO", f"Módulo validado: {path.name}")


def inspect_db(path: Path) -> None:
    conn = sqlite3.connect(str(path))
    try:
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = [row[0] for row in cursor.fetchall()]
        if not tables:
            raise ValueError(f"Banco sem tabelas: {path.name}")
        log("INFO", f"Banco validado: {path.name} ({len(tables)} tabelas)")
    finally:
        conn.close()


def main() -> int:
    try:
        log("INFO", "Iniciando check de estruturas baseado em artefatos reais")

        require_any(WORKBOOK_CANDIDATES, "workbook")
        require_any(BRIDGE_CANDIDATES, "bridge/estrutura")

        modules = require_any(MODULE_CANDIDATES, "módulo de domínio")
        for module_path in modules:
            inspect_module(module_path)

        dbs = require_any(DB_CANDIDATES, "banco")
        for db_path in dbs:
            inspect_db(db_path)

        scripts = [p for p in SCRIPT_CANDIDATES if p.exists()]
        if scripts:
            for script in scripts:
                log("INFO", f"Script operacional encontrado: {script.name}")
        else:
            log("WARN", "Nenhum script operacional de estrutura encontrado; seguindo com validação por artefatos")

        log("OK", "check_structures concluído com sucesso")
        return 0

    except Exception as e:
        log("FAIL", f"Erro no check_structures: {e}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
