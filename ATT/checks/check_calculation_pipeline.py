import sys
import traceback
import subprocess
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]

SMOKE_SCRIPTS = [
    ROOT_DIR / "Scripts" / "12_smoke_structure_market_input.py",
    ROOT_DIR / "Scripts" / "13_smoke_canonical_input_service.py",
    ROOT_DIR / "Scripts" / "14_smoke_pricing_input_service.py",
    ROOT_DIR / "Scripts" / "15_smoke_pricing_execution_service.py",
]

MODULE_FILES = [
    ROOT_DIR / "services" / "canonical_input_service.py",
    ROOT_DIR / "services" / "pricing_input_service.py",
    ROOT_DIR / "services" / "pricing_execution_service.py",
    ROOT_DIR / "services" / "pricing_execution_orchestration_service.py",
    ROOT_DIR / "domain" / "payoff.py",
]


def log(level: str, message: str) -> None:
    print(f"[{level}] {message}")


def run_script(script_path: Path) -> None:
    log("INFO", f"Executando smoke: {script_path.name}")
    result = subprocess.run([sys.executable, str(script_path)], cwd=str(ROOT_DIR))
    if result.returncode != 0:
        raise RuntimeError(f"{script_path.name} falhou com código {result.returncode}")
    log("OK", f"{script_path.name} passou")


def inspect_module_file(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Módulo não encontrado: {path}")

    content = path.read_text(encoding="utf-8")
    log("INFO", f"Módulo localizado: {path.name}")

    if "class " not in content and "def " not in content:
        raise ValueError(f"Módulo sem classes/funções aparentes: {path.name}")


def main() -> int:
    try:
        log("INFO", "Iniciando check do pipeline de cálculo real")

        smoke_found = False
        for script in SMOKE_SCRIPTS:
            if script.exists():
                run_script(script)
                smoke_found = True

        module_found = False
        for module_file in MODULE_FILES:
            if module_file.exists():
                inspect_module_file(module_file)
                module_found = True

        if not smoke_found and not module_found:
            raise FileNotFoundError(
                "Nenhum smoke do pipeline e nenhum módulo real do pipeline foram encontrados"
            )

        log("OK", "check_calculation_pipeline concluído com sucesso")
        return 0

    except Exception as e:
        log("FAIL", f"Erro no check_calculation_pipeline: {e}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
