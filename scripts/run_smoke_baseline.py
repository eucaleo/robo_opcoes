# scripts/run_smoke_baseline.py

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

# Ajuste esta lista conforme os scripts reais existentes
BASELINE_SCRIPTS = [
    "smoke_quick_flow.py",
    "smoke_quick_persistence.py",
]


def run_script(script_name: str) -> int:
    script_path = BASE_DIR / script_name

    if not script_path.exists():
        print(f"[ERRO] Script não encontrado: {script_path}")
        return 1

    print(f"\n[INFO] Executando: {script_name}")
    print("-" * 60)

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(PROJECT_ROOT),
    )

    if result.returncode == 0:
        print(f"[OK] {script_name} finalizado com sucesso")
    else:
        print(f"[FALHA] {script_name} retornou código {result.returncode}")

    return result.returncode


def main() -> int:
    print("=" * 60)
    print("SMOKE BASELINE")
    print("=" * 60)

    failures = []

    for script in BASELINE_SCRIPTS:
        code = run_script(script)
        if code != 0:
            failures.append((script, code))

    print("\n" + "=" * 60)
    print("RESUMO")
    print("=" * 60)

    if not failures:
        print("[OK] Todos os scripts baseline passaram")
        return 0

    for script, code in failures:
        print(f"[FALHA] {script}: código {code}")

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
