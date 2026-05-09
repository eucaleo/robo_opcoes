import os

DEFAULT_EXCLUDE_DIRS = {
    ".git", ".github",
    ".venv", "venv", "env",
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    "node_modules",
    "ATT", "BAK",
    "dist", "build", ".eggs",
}

DEFAULT_EXCLUDE_PARTS = {
    os.sep + "site-packages" + os.sep,
}

def should_skip_dir(dirpath: str) -> bool:
    parts = set(dirpath.replace("\\", "/").split("/"))
    if parts & DEFAULT_EXCLUDE_DIRS:
        return True
    norm = dirpath.replace("\\", "/")
    for p in DEFAULT_EXCLUDE_PARTS:
        if p.replace("\\", "/") in norm:
            return True
    return False

def iter_files(root=".", exts=(".py",)):
    for dirpath, dirnames, filenames in os.walk(root):
        if should_skip_dir(dirpath):
            dirnames[:] = []  # não desce
            continue
        # também filtra a descida
        dirnames[:] = [d for d in dirnames if d not in DEFAULT_EXCLUDE_DIRS]
        for fn in filenames:
            if fn.endswith(exts):
                yield os.path.join(dirpath, fn)
def should_skip_dir(dirpath: str) -> bool:
    norm = dirpath.replace("\\", "/")
    parts = norm.split("/")

    if any(p in DEFAULT_EXCLUDE_DIRS for p in parts):
        return True

    # backup_*
    if any(p.startswith("backup_") for p in parts):
        return True

    # site-packages
    if "/site-packages/" in norm:
        return True

    return False
