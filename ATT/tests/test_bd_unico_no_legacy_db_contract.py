from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

ACTIVE_SCAN_DIRS = [
    "ATT/tests",
    "scripts",
    "services",
    "db",
    "UI",
    "ui",
]

TEXT_SUFFIXES = {
    ".py",
    ".sh",
    ".sql",
    ".md",
    ".txt",
    ".yml",
    ".yaml",
    ".json",
    ".ini",
    ".cfg",
    ".toml",
}

EXCLUDED_DIR_NAMES = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
}

LEGACY_PREFIX = "derived"
DB_TOKEN = "db"

FORBIDDEN_TEXT_TOKENS = {
    LEGACY_PREFIX + "." + DB_TOKEN,
    LEGACY_PREFIX + "_" + DB_TOKEN,
    "DERIVED" + "_" + "DB",
    "DERIVED" + "_" + "DB" + "_" + "PATH",
    "dados/" + LEGACY_PREFIX,
    "data/" + LEGACY_PREFIX,
    "connect" + "_" + LEGACY_PREFIX,
    "get" + "_" + LEGACY_PREFIX + "_connection",
    "validate" + "_" + LEGACY_PREFIX,
    "repair" + "_" + LEGACY_PREFIX,
    "pricing_results" + "." + DB_TOKEN,
    "market_data" + "." + DB_TOKEN,
    "artifacts" + "." + DB_TOKEN,
}

FORBIDDEN_FILENAME_TOKENS = {
    LEGACY_PREFIX + "_" + DB_TOKEN,
    LEGACY_PREFIX + "." + DB_TOKEN,
    "pricing_results",
    "market_data",
    "artifacts" + "." + DB_TOKEN,
}

SELF_FILE = Path("ATT") / "tests" / "test_bd_unico_no_legacy_db_contract.py"


def _relative_path(path: Path) -> Path:
    return path.resolve().relative_to(PROJECT_ROOT)


def _is_excluded(path: Path) -> bool:
    return bool(set(path.parts) & EXCLUDED_DIR_NAMES)


def _iter_scan_files():
    for scan_dir in ACTIVE_SCAN_DIRS:
        base = PROJECT_ROOT / scan_dir
        if not base.exists():
            continue

        for path in base.rglob("*"):
            if _is_excluded(path):
                continue

            if not path.is_file():
                continue

            if path.suffix not in TEXT_SUFFIXES:
                continue

            yield path


def test_no_forbidden_legacy_database_text_tokens():
    occurrences = []

    for path in _iter_scan_files():
        relative = _relative_path(path).as_posix()

        # Este próprio contrato precisa montar os tokens proibidos dinamicamente.
        if Path(relative) == SELF_FILE:
            continue

        text = path.read_text(encoding="utf-8", errors="ignore")

        for line_no, line in enumerate(text.splitlines(), start=1):
            for token in FORBIDDEN_TEXT_TOKENS:
                if token in line:
                    occurrences.append(
                        f"{relative}:{line_no}: {token}: {line.strip()}"
                    )

    assert occurrences == []


def test_no_forbidden_legacy_database_filename_tokens():
    occurrences = []

    for path in _iter_scan_files():
        relative = _relative_path(path).as_posix()

        # Este próprio contrato pode conter "legacy_db" no nome.
        if Path(relative) == SELF_FILE:
            continue

        lower_name = path.name.lower()

        for token in FORBIDDEN_FILENAME_TOKENS:
            if token.lower() in lower_name:
                occurrences.append(f"{relative}: filename token: {token}")

    assert occurrences == []
