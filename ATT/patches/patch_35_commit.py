# ATT/patches/patch_35_commit.py
"""
patch_35 -- Commit condicional
Executa os testes do patch_35 e, somente se todos passarem,
faz git add + git commit com mensagem padronizada.

Execução:
    python ATT/patches/patch_35_commit.py
    python ATT/patches/patch_35_commit.py --dry-run   # só testa, sem commit
"""

import sys
import subprocess
import argparse
from pathlib import Path
from datetime import datetime

RAIZ       = Path(__file__).resolve().parents[2]
TEST_FILE  = RAIZ / "ATT" / "tests" / "test_patch35_details_panel.py"
TARGET_FILE = RAIZ / "UI" / "components" / "details_panel.py"

COMMIT_MSG = (
    "patch_35: details_panel -- migrate internal queries to structure_id (INTEGER)\n\n"
    "- _fetch_latest_decision_from_derived: WHERE aba=?  WHERE structure_id=?\n"
    "- _fetch_payoff_points_from_derived:   WHERE aba=?  WHERE structure_id=?\n"
    "- _fetch_audit_info_from_derived:      WHERE aba=? × 2  WHERE structure_id=? × 2\n"
    "- _get_latest_snapshot_timestamp:      structure_id preferred; aba fallback for unmigrated tables\n"
    "- _resolve_structure_key() added (aligns with ui_data.py patch_34)\n"
    "- _query_by_structure() removed (dead adapter)\n"
    "- update_decision: structure_id is authoritative display key\n"
    "- _on_recalculate_click: removed aba fallback\n\n"
    "Refs: patch_33 (structure_id canonical), patch_34 (INTEGER enforcement)"
)


def run_cmd(cmd: list[str], cwd: Path = RAIZ) -> tuple[int, str, str]:
    result = subprocess.run(
        cmd,
        cwd=str(cwd),
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout, result.stderr


def print_section(title: str):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Executa testes mas não faz commit.",
    )
    args = parser.parse_args()

    print_section("patch_35 -- Commit condicional")
    print(f"  Raiz      : {RAIZ}")
    print(f"  Alvo      : {TARGET_FILE.relative_to(RAIZ)}")
    print(f"  Testes    : {TEST_FILE.relative_to(RAIZ)}")
    print(f"  Dry-run   : {args.dry_run}")
    print(f"  Timestamp : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    #  1. Verifica existência dos arquivos 
    print_section("1. Verificando arquivos")

    missing = []
    for f in [TARGET_FILE, TEST_FILE]:
        exists = f.exists()
        print(f"  {'[OK]' if exists else '[FALHOU]'}  {f.relative_to(RAIZ)}")
        if not exists:
            missing.append(f)

    if missing:
        print("\n  [FALHOU]  Arquivos ausentes. Abortando.")
        return 1

    #  2. Executa testes 
    print_section("2. Executando testes")

    code, stdout, stderr = run_cmd(
        [sys.executable, str(TEST_FILE)]
    )

    print(stdout)
    if stderr:
        print(stderr)

    if code != 0:
        print("\n  [FALHOU]  Testes falharam. Commit abortado.")
        return 1

    print("\n  [OK]  Todos os testes passaram.")

    #  3. Dry-run: para aqui 
    if args.dry_run:
        print_section("Dry-run ativo -- commit NÃO realizado")
        return 0

    #  4. git status (pré-commit) 
    print_section("3. Git status")
    _, status_out, _ = run_cmd(["git", "status", "--short"])
    print(status_out or "  (nada a reportar)")

    #  5. git add 
    print_section("4. git add")

    files_to_add = [
        str(TARGET_FILE.relative_to(RAIZ)),
        str(TEST_FILE.relative_to(RAIZ)),
        str(Path("ATT/patches/patch_35_commit.py")),
    ]

    for f in files_to_add:
        code, _, err = run_cmd(["git", "add", f])
        status = "[OK]" if code == 0 else "[FALHOU]"
        print(f"  {status}  git add {f}")
        if code != 0:
            print(f"       {err.strip()}")

    #  6. git commit 
    print_section("5. git commit")

    code, out, err = run_cmd(["git", "commit", "-m", COMMIT_MSG])
    print(out)
    if err:
        print(err)

    if code == 0:
        print("\n  [OK]  Commit realizado com sucesso.")

        # Mostra hash do commit
        _, hash_out, _ = run_cmd(["git", "log", "--oneline", "-1"])
        print(f"  [FIXO]  {hash_out.strip()}")
    else:
        print("\n  [FALHOU]  Falha no commit.")
        return 1

    #  7. Sumário final 
    print_section("Sumário patch_35")
    print("  Arquivos commitados:")
    for f in files_to_add:
        print(f"    * {f}")
    print(
        "\n  Próximo passo sugerido:\n"
        "    python ATT/patches/patch_36_...py\n"
        "    (verificar outros componentes com WHERE aba=? remanescentes)"
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
