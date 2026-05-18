from __future__ import annotations

import json
from pathlib import Path

ROOT_PATH = Path(".").resolve()

INCLUDE_EXTENSIONS = {".py", ".md", ".txt", ".yaml", ".yml", ".json"}
IGNORE_DIRS = {
    ".git",
    ".idea",
    ".vscode",
    "__pycache__",
    "venv",
    ".venv",
    "node_modules",
    "dist",
    "build",
    ".mypy_cache",
    ".pytest_cache",
}

OUTPUT_FILE = ROOT_PATH / "module_inventory.json"


def should_ignore(path: Path) -> bool:
    return any(part in IGNORE_DIRS for part in path.parts)


def collect_files(root: Path) -> list[dict]:
    items: list[dict] = []

    for path in root.rglob("*"):
        if path.is_dir():
            continue
        if should_ignore(path):
            continue
        if path.suffix.lower() not in INCLUDE_EXTENSIONS:
            continue

        try:
            stat = path.stat()
            relative_path = path.relative_to(root)
            items.append(
                {
                    "file": str(relative_path),
                    "extension": path.suffix.lower(),
                    "size_bytes": stat.st_size,
                }
            )
        except OSError:
            continue

    return sorted(items, key=lambda x: x["file"])


def summarize(items: list[dict]) -> dict:
    by_extension: dict[str, int] = {}
    for item in items:
        ext = item["extension"]
        by_extension[ext] = by_extension.get(ext, 0) + 1

    return {
        "root": str(ROOT_PATH),
        "total_files": len(items),
        "by_extension": dict(sorted(by_extension.items())),
        "files": items,
    }


def main() -> int:
    print(f"[INFO] Lendo arquivos em: {ROOT_PATH}")
    items = collect_files(ROOT_PATH)
    summary = summarize(items)

    OUTPUT_FILE.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"[OK] Inventário gerado em: {OUTPUT_FILE}")
    print(f"[INFO] Total de arquivos encontrados: {summary['total_files']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
