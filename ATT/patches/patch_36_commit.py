# ATT/patches/patch_36_commit.py
"""
Patch_36 -- Remove fallback legado 'aba' de details_panel e main_window.
Executa os testes e realiza commit automático se todos passarem.
"""
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
TESTS = [
    "ATT/tests/test_patch36_details_panel.py",
    "ATT/tests/test_patch36_main_window.py",
]
FILES_TO_COMMIT = [
    "UI/components/details_panel.py",
    "UI/main_window.py",
    "ATT/tests/test_patch36_details_panel.py",
    "ATT/tests/test_patch36_main_window.py",
    "ATT/patches/patch_36_commit.py",
    "scripts/audit_patches.py",          # auditoria atualizada
]
COMMIT_MSG = (
    "refactor(patch_36): remove fallback legado 'aba' -- details_panel + main_window\n\n"
    "- _resolve_structure_key: aceita int ou str numérica, rejeita None/alpha\n"
    "- _get_latest_snapshot_timestamp_for_structure: query direta por structure_id INTEGER\n"
    "- _fetch_latest_decision_from_derived: sem PRAGMA condicional por aba\n"
    "- _fetch_payoff_points_from_derived: filtro direto por structure_id\n"
    "- _fetch_audit_info_from_derived: guards aba removidos\n"
    "- update_decision: fallback 'or aba' removido\n"
    "- _on_recalculate_click: fallback 'or aba' removido\n"
    "- recalculate_aba(): método DEPRECATED removido de main_window\n"
    "- refresh_data: 'or aba' removido nas duas ocorrências\n"
    "- on_decision_selected: 'or aba' removido\n"
    "Testes: 60/60 passed (details_panel=44, main_window=16)"
)


def run(cmd: list, **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=str(PROJECT_ROOT), **kwargs)


def main() -> int:
    print("=" * 62)
    print("  Patch_36 -- Commit Automático")
    print("=" * 62)

    # 1. Roda os testes
    print("\n[1/3] Executando testes patch_36...")
    result = run(
        [sys.executable, "-m", "pytest"] + TESTS + ["-v", "--tb=short"],
        capture_output=False,
    )
    if result.returncode != 0:
        print("\n[FALHOU] Testes falharam -- commit abortado.")
        return result.returncode

    print("\n[OK] 60/60 testes passaram.")

    # 2. git add
    print("\n[2/3] Staging dos arquivos...")
    run(["git", "add"] + FILES_TO_COMMIT, check=True)

    # 3. git commit
    print("\n[3/3] Realizando commit...")
    diff = run(["git", "diff", "--cached", "--quiet"])
    if diff.returncode == 0:
        print("[INFO]  Nada a commitar -- arquivos já atualizados.")
        return 0

    run(["git", "commit", "-m", COMMIT_MSG], check=True)

    print("\n" + "=" * 62)
    print("  [OK] Commit patch_36 realizado com sucesso")
    print("=" * 62)
    run(["git", "log", "--oneline", "-1"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
