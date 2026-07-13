import sys
import subprocess
from pathlib import Path


CHECKS_DIR = Path(__file__).resolve().parent

CHECK_SCRIPTS = [
    "check_api_routes.py",
    "check_legs.py",
    "check_structures.py",
    "check_end_to_end.py",
    "check_cleanup_residuals.py",
]


def main() -> int:
    failures = []

    print("[INFO] Iniciando execução de todos os checks")

    for script in CHECK_SCRIPTS:
        script_path = CHECKS_DIR / script
        print(f"\n[INFO] Executando {script} ...")

        result = subprocess.run([sys.executable, str(script_path)], cwd=str(CHECKS_DIR.parent))
        if result.returncode == 0:
            print(f"[OK] {script} finalizou com sucesso")
        else:
            print(f"[FAIL] {script} falhou com código {result.returncode}")
            failures.append((script, result.returncode))

    print("\n[INFO] Resumo final")
    if not failures:
        print("[OK] Todos os checks passaram")
        return 0

    for script, code in failures:
        print(f"[FAIL] {script} -> código {code}")

    return 1


if __name__ == "__main__":
    sys.exit(main())
