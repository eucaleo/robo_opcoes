import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

FORBIDDEN_PATTERNS = [
    r"\bscripts/",
    r"\bscripts\\",
    r"\bscripts\b",
    r"run_real_smokes",
    r"check_calculation_pipeline",
    r"check_result_repository",
    r"smoke_pricing_execution",
    r"smoke_calculation_request",
    r"smoke_market_snapshot",
    r"smoke_pipeline",
    r"canonical_flow_smoke",
    r"canonical_execution_probe",
    r"audit_fase8",
    r"audit_patch",
    r"audit_legacy",
    r"audit_domain_dto_boundary",
    r"audit_public_api",
    r"audit_aba",
    r"phase_3a",
    r"phase_3b",
    r"phase_3c",
    r"patch3b",
    r"tmp_.*\.py",
]

SEARCH_PATHS = [
    "ATT",
    "README.md",
    "pyproject.toml",
    "Makefile",
    ".github",
]

ALLOW_PATTERNS = [
    # Teste intencional que valida ausência de scripts temporários.
    r"ATT/tests/test_patch61\.py",

    # Este próprio check contém os padrões proibidos.
    r"ATT/checks/check_cleanup_residuals\.py",
]


def log(level: str, message: str) -> None:
    print(f"[{level}] {message}")


def run_git_grep(pattern: str) -> list[str]:
    existing_paths = [p for p in SEARCH_PATHS if (ROOT / p).exists()]
    if not existing_paths:
        return []

    cmd = [
        "git",
        "grep",
        "-n",
        "-E",
        pattern,
        "--",
        *existing_paths,
    ]

    result = subprocess.run(
        cmd,
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


def is_allowed(line: str) -> bool:
    return any(re.search(pattern, line) for pattern in ALLOW_PATTERNS)


def check_no_forbidden_references() -> None:
    violations: list[str] = []

    for pattern in FORBIDDEN_PATTERNS:
        matches = run_git_grep(pattern)
        for line in matches:
            if not is_allowed(line):
                violations.append(f"{pattern} -> {line}")

    if violations:
        log("FAIL", "Referências residuais encontradas:")
        for violation in violations:
            print(f"  - {violation}")
        raise AssertionError(f"{len(violations)} referência(s) residual(is) encontrada(s)")

    log("OK", "Nenhuma referência residual proibida encontrada")


def check_lowercase_scripts_dir_absent() -> None:
    scripts_dir = ROOT / "scripts"
    if scripts_dir.exists():
        remaining = sorted(p.relative_to(ROOT).as_posix() for p in scripts_dir.rglob("*") if p.is_file())
        if remaining:
            log("FAIL", "Arquivos restantes em scripts/:")
            for path in remaining:
                print(f"  - {path}")
            raise AssertionError("Diretório scripts/ ainda contém arquivos")

    log("OK", "Diretório scripts/ minúsculo ausente ou vazio")


def check_run_all_checks_targets_exist() -> None:
    run_all = ROOT / "ATT" / "checks" / "run_all_checks.py"
    text = run_all.read_text(encoding="utf-8")

    referenced = sorted(set(re.findall(r'"([^"]+\.py)"', text) + re.findall(r"'([^']+\.py)'", text)))
    missing = []

    for name in referenced:
        if name == Path(__file__).name:
            continue

        candidate = run_all.parent / name
        if not candidate.exists():
            missing.append(name)

    if missing:
        log("FAIL", "run_all_checks.py referencia checks inexistentes:")
        for name in missing:
            print(f"  - {name}")
        raise AssertionError("Há checks inexistentes referenciados em run_all_checks.py")

    log("OK", "run_all_checks.py referencia apenas checks existentes")


def main() -> int:
    try:
        log("INFO", "Iniciando verificação residual de limpeza")
        check_lowercase_scripts_dir_absent()
        check_run_all_checks_targets_exist()
        check_no_forbidden_references()
        log("OK", "Verificação residual de limpeza concluída com sucesso")
        return 0
    except Exception as exc:
        log("FAIL", str(exc))
        return 1


if __name__ == "__main__":
    sys.exit(main())
