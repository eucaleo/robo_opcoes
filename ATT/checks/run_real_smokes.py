import os
import subprocess
import sys
from pathlib import Path


def main():
    print("[INFO] Iniciando execução dos smoke tests reais do projeto")

    project_root = Path(__file__).resolve().parents[2]
    scripts_dir = project_root / "scripts"
    smoke_context_file = scripts_dir / ".smoke_context.json"

    print(f"[INFO] Raiz do projeto: {project_root}")
    print(f"[INFO] Pasta de scripts: {scripts_dir}")

    env = os.environ.copy()
    env["PYTHONPATH"] = str(project_root)
    env["SMOKE_CONTEXT_FILE"] = str(smoke_context_file)

    print(f"[INFO] PYTHONPATH injetado: {env['PYTHONPATH']}")

    if smoke_context_file.exists():
        smoke_context_file.unlink()

    scripts = [
        "10_smoke_structures_repository.py",
        "11_smoke_structure_input_mapper.py",
        "12_smoke_structure_market_input.py",
        "13_smoke_canonical_input_service.py",
        "14_smoke_pricing_input_service.py",
        "15_smoke_pricing_execution_service.py",
        "16_smoke_pricing_execution_persistence.py",
        "22_smoke_pricing_execution_orchestration_success.py",
        "26_smoke_pricing_execution_app_service_execute.py",
        "17_smoke_pricing_execution_query_service.py",
        "18_smoke_pricing_execution_summary_query.py",
        "19_smoke_robo_legs_service.py",
        "99_smoke_cleanup.py",
    ]

    failures = []

    try:
        for script_name in scripts:
            script_path = scripts_dir / script_name
            print(f"[INFO] Executando {script_name} ...")

            result = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=str(project_root),
                env=env,
            )

            if result.returncode == 0:
                print(f"[OK] {script_name} finalizou com sucesso")
            else:
                print(f"[FAIL] {script_name} falhou com código {result.returncode}")
                failures.append((script_name, result.returncode))
                break
    finally:
        if smoke_context_file.exists():
            smoke_context_file.unlink()

    print("[INFO] Resumo final dos smoke tests reais")

    if failures:
        for script_name, returncode in failures:
            print(f"[FAIL] {script_name} -> código {returncode}")
        sys.exit(1)

    print("[OK] Todos os smoke tests reais executados com sucesso")


if __name__ == "__main__":
    main()
