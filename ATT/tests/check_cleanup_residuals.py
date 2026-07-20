import re
import subprocess
import sys
from pathlib import Path

_LEGACY_TOKEN = "pa" + "tch"


ROOT = Path(__file__).resolve().parents[2]

FORBIDDEN_FILE_PATTERNS = [
    r"(^|/)ATT/tests/test_" + _LEGACY_TOKEN + r"10_smoke\.py$",
    r"(^|/)ATT/tests/teste_rapido_smoke_patch2_25\.py$",
    r"(^|/)scripts/_smoke_context\.py$",
    r"(^|/)scripts/run_smoke_baseline\.py$",
    r"(^|/)scripts/run_smoke_full\.py$",
    r"(^|/)scripts/run_smoke_quick\.py$",
    r"(^|/)scripts/smoke_canonical_and_domain\.py$",
    r"(^|/)scripts/__pycache__/",
    r"(^|/)scripts/.*\.pyc$",
]

FORBIDDEN_TEXT_PATTERNS = [
    r"run_real_smokes",
    r"check_calculation_pipeline",
    r"check_result_repository",
    r"run_smoke_baseline",
    r"run_smoke_full",
    r"run_smoke_quick",
    r"smoke_canonical_and_domain",
    r"test_" + _LEGACY_TOKEN + r"10_smoke",
    r"teste_rapido_smoke_patch2_25",
    r"09b_smoke_robo_legs_lookup",
    r"09_smoke_robo_legs_lookup",
    r"smoke_pricing_execution",
    r"smoke_calculation_request",
    r"smoke_market_snapshot",
    r"smoke_pipeline",
    r"canonical_flow_smoke",
    r"canonical_execution_probe",
    r"audit_fase8",
    r"audit_patch",
    r"audit_legacy_domain_coupling",
    r"audit_public_api_aba_surface",
    r"audit_aba_wrappers",
    r"phase_3a",
    r"phase_3b",
    r"phase_3c",
    r"patch3b",
]

SEARCH_PATHS = [
    "ATT",
    "README.md",
    "pyproject.toml",
    "Makefile",
    ".github",
]

ALLOW_PATH_PATTERNS = [
    r"ATT/checks/check_cleanup_residuals\.py",
    r"ATT/PATCHES\.md",
    r"ATT/tests/test_orchestrator_run_methods\.py",
    r"ATT/tests/test_" + _LEGACY_TOKEN + r"35_details_panel\.py",
    r"ATT/tests/test_" + _LEGACY_TOKEN + r"36_details_panel\.py",
    r"ATT/tests/test_" + _LEGACY_TOKEN + r"72\.py",
]


ALLOWED_SCRIPTS = {
    "scripts/apply_fase9_atomic_create.py",
    "scripts/apply_fase9_atomic_create.sh",
    "scripts/apply_fase9_update_tests_atomic_create.py",
    "scripts/check_rota_desenvolvimento.py",
    "scripts/import_legacy_structure_legs.py",
    "scripts/patch_derived_payoff_timestamp_consistency.sh",
    "scripts/purge_derived_snapshots.py",
    "scripts/repair_app_db_consistency.py",
    "scripts/run_derived_pipeline.py",
    "scripts/validate_app_db.py",
}


def log(level: str, message: str) -> None:
    print(f"[{level}] {message}")


def git_ls_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=str(ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git ls-files falhou")

    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def run_git_grep(pattern: str) -> list[str]:
    existing_paths = [p for p in SEARCH_PATHS if (ROOT / p).exists()]
    if not existing_paths:
        return []

    result = subprocess.run(
        ["git", "grep", "-n", "-E", pattern, "--", *existing_paths],
        cwd=str(ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if result.returncode == 1:
        return []

    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"git grep falhou para padrão: {pattern}")

    return [line for line in result.stdout.splitlines() if line.strip()]


def is_allowed_line(line: str) -> bool:
    return any(re.search(pattern, line) for pattern in ALLOW_PATH_PATTERNS)


def check_forbidden_files_absent() -> None:
    files = git_ls_files()
    violations = []

    for path in files:
        normalized = path.replace("\\", "/")
        for pattern in FORBIDDEN_FILE_PATTERNS:
            if re.search(pattern, normalized):
                violations.append(normalized)

    if violations:
        log("FAIL", "Arquivos residuais proibidos ainda versionados:")
        for path in sorted(set(violations)):
            print(f"  - {path}")
        raise AssertionError(f"{len(set(violations))} arquivo(s) residual(is) encontrado(s)")

    log("OK", "Nenhum arquivo residual proibido versionado")


def check_forbidden_text_absent() -> None:
    violations = []

    for pattern in FORBIDDEN_TEXT_PATTERNS:
        for line in run_git_grep(pattern):
            if not is_allowed_line(line):
                violations.append(f"{pattern} -> {line}")

    if violations:
        log("FAIL", "Referências residuais proibidas encontradas:")
        for violation in violations:
            print(f"  - {violation}")
        raise AssertionError(f"{len(violations)} referência(s) residual(is) encontrada(s)")

    log("OK", "Nenhuma referência residual proibida encontrada")


def check_run_all_checks_targets_exist() -> None:
    run_all = ROOT / "ATT" / "checks" / "run_all_checks.py"
    text = run_all.read_text(encoding="utf-8")

    referenced = sorted(set(re.findall(r'"([^"]+\.py)"', text) + re.findall(r"'([^']+\.py)'", text)))
    missing = []

    for name in referenced:
        candidate = run_all.parent / name
        if not candidate.exists():
            missing.append(name)

    if missing:
        log("FAIL", "run_all_checks.py referencia checks inexistentes:")
        for name in missing:
            print(f"  - {name}")
        raise AssertionError("Há checks inexistentes referenciados em run_all_checks.py")

    log("OK", "run_all_checks.py referencia apenas checks existentes")


def check_scripts_allowlist() -> None:
    files = git_ls_files()

    script_files = sorted(
        path.replace("\\", "/")
        for path in files
        if path.replace("\\", "/").startswith("scripts/")
    )

    unexpected = [
        path
        for path in script_files
        if path not in ALLOWED_SCRIPTS
    ]

    if unexpected:
        log("FAIL", "scripts/ contém arquivos fora da allowlist operacional:")
        for path in unexpected:
            print(f"  - {path}")
        raise AssertionError(f"{len(unexpected)} arquivo(s) inesperado(s) em scripts/")

    log("OK", "scripts/ contém apenas scripts operacionais permitidos")


def check_no_patch_tests() -> None:
    files = git_ls_files()

    patch_tests = sorted(
        item.replace("\\", "/")
        for item in files
        if item.replace("\\", "/").startswith("ATT/tests/test_" + _LEGACY_TOKEN)
        and item.replace("\\", "/").endswith(".py")
    )

    if patch_tests:
        log("FAIL", "Arquivos temporarios antigos ainda versionados em ATT/tests:")
        for item in patch_tests:
            print(f"  - {item}")
        raise AssertionError(f"{len(patch_tests)} arquivo(s) temporario(s) antigo(s) encontrado(s)")

    log("OK", "Nenhum arquivo temporario antigo versionado em ATT/tests")


def main() -> int:
    try:
        log("INFO", "Iniciando verificação residual de limpeza")
        check_forbidden_files_absent()
        check_scripts_allowlist()
        check_no_patch_tests()
        check_run_all_checks_targets_exist()
        check_forbidden_text_absent()
        log("OK", "Verificação residual de limpeza concluída com sucesso")
        return 0
    except Exception as exc:
        log("FAIL", str(exc))
        return 1


if __name__ == "__main__":
    sys.exit(main())
