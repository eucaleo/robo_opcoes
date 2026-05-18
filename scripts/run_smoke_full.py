import os
import sys
import time
import subprocess
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT_DIR / "scripts"

FULL_SMOKES = [
    "10_smoke_structures_repository.py",
    "11_smoke_structure_input_mapper.py",
    "12_smoke_structure_market_input.py",
    "13_smoke_canonical_input_service.py",
    "14_smoke_pricing_input_service.py",
    "15_smoke_pricing_execution_service.py",
    "16_smoke_pricing_execution_persistence.py",
    "17_smoke_pricing_execution_query_service.py",
    "18_smoke_pricing_execution_summary_query.py",
    "19_smoke_pricing_execution_filtered_summary_query.py",
    "20_smoke_pricing_execution_operational_metadata.py",
    "21_smoke_pricing_execution_error_persistence.py",
    "22_smoke_pricing_execution_orchestration_success.py",
    "23_smoke_pricing_execution_orchestration_error.py",
    "24_smoke_pricing_execution_details_query.py",
    "25_smoke_pricing_execution_details_not_found.py",
    "26_smoke_pricing_execution_app_service_execute.py",
    "27_smoke_pricing_execution_app_service_list.py",
    "28_smoke_pricing_execution_app_service_detail.py",
    "29_smoke_pricing_execution_summary_ordering.py",
    "30_smoke_pricing_execution_latest_summary.py",
    "31_smoke_pricing_execution_app_service_latest_summary.py",
    "32_smoke_pricing_execution_summary_pagination.py",
    "33_smoke_pricing_execution_summary_pagination_second_page.py",
    "34_smoke_pricing_execution_app_service_pagination.py",
    "35_smoke_pricing_execution_pagination_filter_status_ok.py",
    "36_smoke_pricing_execution_pagination_filter_status_error.py",
    "37_smoke_pricing_execution_latest_summary_by_status.py",
    "38_smoke_pricing_execution_app_service_paginated_filtered.py",
    "39_smoke_pricing_execution_invalid_status_validation.py",
    "40_smoke_pricing_execution_invalid_page_validation.py",
    "41_smoke_pricing_execution_invalid_page_size_validation.py",
    "42_smoke_pricing_execution_invalid_reference_date_validation.py",
    "43_smoke_pricing_execution_invalid_structure_id_validation.py",
    "44_smoke_pricing_execution_controller_list.py",
    "45_smoke_pricing_execution_controller_latest.py",
    "46_smoke_pricing_execution_controller_detail.py",
    "47_smoke_pricing_execution_controller_invalid_status.py",
    "48_smoke_pricing_execution_controller_invalid_execution_id.py",
    "49_smoke_pricing_execution_controller_execution_not_found.py",
    "50_smoke_pricing_execution_controller_latest_invalid_structure_id.py",
    "51_smoke_pricing_execution_controller_latest_invalid_reference_date.py",
    "52_smoke_pricing_execution_controller_list_invalid_page.py",
    "53_smoke_pricing_execution_controller_list_invalid_page_size.py",
    "54_smoke_pricing_execution_controller_create.py",
    "55_smoke_pricing_execution_controller_create_invalid_structure_id.py",
    "56_smoke_pricing_execution_controller_create_invalid_reference_date.py",
    "57_smoke_pricing_execution_controller_create_structure_not_found.py",
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
    log("INFO", "Resumo final da smoke full")
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
    log("INFO", "Iniciando smoke full do fluxo real")
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

    for script_name in FULL_SMOKES:
        log("INFO", f"Executando: {script_name}")
        result = run_smoke(script_name, env)
        results.append(result)

        if result["status"] == "fail":
            failures.append(result)
        elif result["status"] == "missing":
            missing.append(result)

    print_summary(results)

    if failures:
        log("FAIL", f"Smoke full reprovada: {len(failures)} smoke(s) com falha")
        return 1

    if missing:
        log("WARN", f"Smoke full concluída com {len(missing)} smoke(s) ausente(s)")
        return 0

    log("OK", "Smoke full aprovada com sucesso")
    return 0


if __name__ == "__main__":
    sys.exit(main())
