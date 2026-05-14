import sys
import sqlite3
import traceback
import subprocess
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
DB_PATH = ROOT_DIR / "dados" / "derived.db"

SMOKE_SCRIPTS = [
    ROOT_DIR / "Scripts" / "16_smoke_pricing_execution_persistence.py",
    ROOT_DIR / "Scripts" / "17_smoke_pricing_execution_query_service.py",
]


def log(level: str, message: str) -> None:
    print(f"[{level}] {message}")


def inspect_db(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Banco não encontrado: {path}")

    conn = sqlite3.connect(str(path))
    try:
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        tables = [row[0] for row in cursor.fetchall()]
        log("INFO", f"Tabelas encontradas em {path.name}: {tables[:30]}")

        if not tables:
            raise ValueError("Banco SQLite sem tabelas")
    finally:
        conn.close()


def run_script(script_path: Path) -> None:
    log("INFO", f"Executando: {script_path.name}")
    result = subprocess.run([sys.executable, str(script_path)], cwd=str(ROOT_DIR))
    if result.returncode != 0:
        raise RuntimeError(f"{script_path.name} falhou com código {result.returncode}")
    log("OK", f"{script_path.name} passou")


def main() -> int:
    try:
        log("INFO", "Iniciando check do repositório de resultados")

        inspect_db(DB_PATH)

        found_any = False
        for script in SMOKE_SCRIPTS:
            if script.exists():
                run_script(script)
                found_any = True

        if not found_any:
            log("WARN", "Nenhum smoke de persistência/query encontrado; inspeção do banco foi executada")

        log("OK", "check_result_repository concluído com sucesso")
        return 0

    except Exception as e:
        log("FAIL", f"Erro no check_result_repository: {e}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
