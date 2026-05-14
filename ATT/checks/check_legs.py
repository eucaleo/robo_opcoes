import sys
import csv
import traceback
import subprocess
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
BRIDGE_DIR = ROOT_DIR / "bridge"

CSV_CANDIDATES = [
    BRIDGE_DIR / "analise_robo_legs.csv",
    BRIDGE_DIR / "analise_robo.csv",
    BRIDGE_DIR / "analise_raiox.csv",
]

SMOKE_SCRIPTS = [
    ROOT_DIR / "Scripts" / "09b_smoke_robo_legs_lookup.py",
    ROOT_DIR / "Scripts" / "09_smoke_robo_legs_lookup.py",
]


def log(level: str, message: str) -> None:
    print(f"[{level}] {message}")


def validate_csv(path: Path) -> None:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f, delimiter=";")
        rows = list(reader)

    if not rows:
        raise ValueError(f"CSV vazio: {path}")

    headers = rows[0]
    log("INFO", f"CSV validado: {path.name}")
    log("INFO", f"Colunas detectadas: {headers[:20]}")
    log("INFO", f"Quantidade de linhas (incluindo cabeçalho): {len(rows)}")

    if len(headers) <= 1:
        raise ValueError(
            f"CSV parece não ter sido interpretado corretamente: apenas {len(headers)} coluna(s)"
        )


def run_smoke(script_path: Path) -> None:
    log("INFO", f"Executando smoke real: {script_path.name}")
    result = subprocess.run([sys.executable, str(script_path)], cwd=str(ROOT_DIR))
    if result.returncode != 0:
        raise RuntimeError(f"Smoke falhou: {script_path.name} (código {result.returncode})")
    log("OK", f"Smoke passou: {script_path.name}")


def main() -> int:
    try:
        log("INFO", "Iniciando check de legs real do projeto")

        found_csv = False
        for path in CSV_CANDIDATES:
            if path.exists():
                validate_csv(path)
                found_csv = True

        smoke_found = False
        for script in SMOKE_SCRIPTS:
            if script.exists():
                run_smoke(script)
                smoke_found = True
                break

        if not found_csv and not smoke_found:
            raise FileNotFoundError("Nem CSV real nem smoke de robo legs foram encontrados")

        log("OK", "check_legs concluído com sucesso")
        return 0

    except Exception as e:
        log("FAIL", f"Erro no check_legs: {e}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
