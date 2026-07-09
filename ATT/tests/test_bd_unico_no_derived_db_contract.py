from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

SCAN_DIRS = [
    "db",
    "scripts",
    "services",
    "ui",
    "UI",
    "ATT",
]

EXCLUDED_PARTS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    "FRENTE_BD_UNICO_APPDB",
}

TEXT_SUFFIXES = {
    ".py",
    ".md",
    ".txt",
    ".sh",
    ".sql",
    ".yml",
    ".yaml",
    ".json",
    ".ini",
    ".cfg",
    ".toml",
}

LEGACY_PREFIX = "derived"
DB_TOKEN = "db"

SELF_CONTRACT_RELATIVE_PATH = Path("ATT") / "tests" / (
    "test_bd_unico_no_" + "_".join([LEGACY_PREFIX, DB_TOKEN]) + "_contract.py"
)

FORBIDDEN_TEXT_TOKENS = [
    "_".join([LEGACY_PREFIX, DB_TOKEN]),
    "_".join([LEGACY_PREFIX, DB_TOKEN, "path"]),
    "_".join([LEGACY_PREFIX.upper(), DB_TOKEN.upper(), "PATH"]),
    "_".join(["connect", LEGACY_PREFIX]),
    "_".join(["get", LEGACY_PREFIX, "connection"]),
    LEGACY_PREFIX + ".db",
    "dados/" + LEGACY_PREFIX,
    "dados" + "\\\\" + LEGACY_PREFIX,
]

FORBIDDEN_FILENAME_TOKENS = [
    "_".join(["validate", LEGACY_PREFIX]),
    "_".join(["repair", LEGACY_PREFIX]),
    "_".join([LEGACY_PREFIX, DB_TOKEN]),
]


def _relative_path(path: Path) -> Path:
    return path.relative_to(PROJECT_ROOT)


def _is_excluded(path: Path) -> bool:
    relative = _relative_path(path)
    return bool(set(relative.parts) & EXCLUDED_PARTS)


def _iter_scan_files():
    for dirname in SCAN_DIRS:
        root = PROJECT_ROOT / dirname
        if not root.exists():
            continue

        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if _is_excluded(path):
                continue
            if path.suffix not in TEXT_SUFFIXES:
                continue
            yield path


def test_no_forbidden_legacy_database_text_tokens():
    occurrences = []

    for path in _iter_scan_files():
        relative = _relative_path(path).as_posix()
        text = path.read_text(encoding="utf-8", errors="ignore")

        for line_no, line in enumerate(text.splitlines(), start=1):
            for token in FORBIDDEN_TEXT_TOKENS:
                if token in line:
                    occurrences.append(
                        f"{relative}:{line_no}: {token}: {line.strip()}"
                    )

    assert occurrences == []


def test_no_forbidden_legacy_database_filenames():
    occurrences = []

    for dirname in SCAN_DIRS:
        root = PROJECT_ROOT / dirname
        if not root.exists():
            continue

        for path in root.rglob("*"):
            if _is_excluded(path):
                continue

            relative_path = _relative_path(path)

            if relative_path == SELF_CONTRACT_RELATIVE_PATH:
                continue

            relative = relative_path.as_posix()
            lower_name = path.name.lower()

            for token in FORBIDDEN_FILENAME_TOKENS:
                if token in lower_name:
                    occurrences.append(f"{relative}: {token}")

    assert occurrences == []
