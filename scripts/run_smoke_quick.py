import os
import sys
import time
import subprocess
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT_DIR / "scripts"

QUICK_SMOKES = [
    "10_smoke_structures_repository.py",
    "13_smoke_canonical_input_service.py",
    "22_smoke_pricing_execution_orchestration_success.py",
]


def log(level: str, message: str) -> None:
    print(f"[{level}] {message}")


def build_env() -> dict:
    env = os.environ.copy()
    current_pythonpath = env.get("PYTHONPATH", "")

    paths = [str(ROOT_DIR)]
    if current_pythonpath:
        paths.append(current_pythonpath)

    env["PYTHONPATH"] = os.pathsep.join(paths)
    return env


def run_smoke(script_name: str, env: dict) -> dict:
    script_path = SCRIPTS_DIR / script_name

    if not script_path.exists():
        return {
            "script": script_name,
            "status": "missing",
            "exit_code": 2,
            "duration_sec": 0.0,
        }

    start = time.perf_counter()
    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(ROOT_DIR),
        env=env,
    )
    duration = time.perf_counter() - start

    status = "ok" if result.returncode == 0 else "fail"

    return {
        "script": script_name,
        "status": status,
        "exit_code": result.returncode,
        "duration_sec": round(duration, 3),
    }


def print_summary(results: list[dict]) -> None:
    log("INFO", "Resumo final da smoke quick")
    total_time = 0.0

    for item in results:
        total_time += item["duration_sec"]

        if item["status"] == "ok":
            log("OK", f'{item["script"]} | {item["duration_sec"]:.3f}s')
        elif item["status"] == "missing":
            log("WARN", f'{item["script"]} | ausente')
        else:
            log(
                "FAIL",
                f'{item["script"]} | exit_code={item["exit_code"]} | {item["duration_sec"]:.3f}s',
            )

    log("INFO", f"Tempo total: {total_time:.3f}s")


def main() -> int:
    log("INFO", "Iniciando smoke quick do fluxo real")
    log("INFO", f"Raiz do projeto: {ROOT_DIR}")
    log("INFO", f"Pasta scripts: {SCRIPTS_DIR}")

    if not SCRIPTS_DIR.exists():
        log("FAIL", f"Pasta scripts não encontrada: {SCRIPTS_DIR}")
        return 1

    env = build_env()
    log("INFO", f"PYTHONPATH ativo: {env.get('PYTHONPATH', '')}")

    results = []
    failures = []
    missing = []

    for script_name in QUICK_SMOKES:
        log("INFO", f"Executando: {script_name}")
        result = run_smoke(script_name, env)
        results.append(result)

        if result["status"] == "fail":
            failures.append(result)
        elif result["status"] == "missing":
            missing.append(result)

    print_summary(results)

    if failures:
        log("FAIL", f"Smoke quick reprovada: {len(failures)} smoke(s) com falha")
        return 1

    if missing:
        log("WARN", f"Smoke quick concluída com {len(missing)} smoke(s) ausente(s)")
        return 0

    log("OK", "Smoke quick aprovada com sucesso")
    return 0


if __name__ == "__main__":
    sys.exit(main())
