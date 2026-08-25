from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable


SQL_DIRECT_PATTERNS = (
    re.compile(r"\bexecute\s*\(", re.IGNORECASE),
    re.compile(r"\bexecutemany\s*\(", re.IGNORECASE),
    re.compile(r"\bSELECT\b", re.IGNORECASE),
    re.compile(r"\bINSERT\b", re.IGNORECASE),
    re.compile(r"\bUPDATE\b", re.IGNORECASE),
    re.compile(r"\bDELETE\b", re.IGNORECASE),
    re.compile(r"\bFROM\b", re.IGNORECASE),
    re.compile(r"\bJOIN\b", re.IGNORECASE),
)

DEFAULT_EXCLUDE_PARTS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    "venv",
    ".venv",
    "node_modules",
}


def _is_excluded(path: Path, exclude_parts: set[str] | None = None) -> bool:
    excluded = exclude_parts or DEFAULT_EXCLUDE_PARTS
    return any(part in excluded for part in path.parts)


def iter_python_files(
    roots: Iterable[Path],
    *,
    exclude_parts: set[str] | None = None,
) -> list[Path]:
    files: list[Path] = []

    for root in roots:
        if not root.exists():
            continue

        if root.is_file() and root.suffix == ".py" and not _is_excluded(root, exclude_parts):
            files.append(root)
            continue

        if not root.is_dir():
            continue

        for path in root.rglob("*.py"):
            if _is_excluded(path, exclude_parts):
                continue
            files.append(path)

    return sorted(files)


def detect_sql_direct_usage(path: Path, *, root: Path | None = None) -> dict:
    root = root or path.parents[0]
    findings: list[dict] = []

    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        lines = []

    for line_number, line in enumerate(lines, start=1):
        stripped = line.strip()

        if not stripped or stripped.startswith("#"):
            continue

        matched = [
            pattern.pattern
            for pattern in SQL_DIRECT_PATTERNS
            if pattern.search(line)
        ]

        if matched:
            findings.append(
                {
                    "line": line_number,
                    "patterns": matched,
                    "preview": stripped[:240],
                }
            )

    try:
        relative = str(path.relative_to(root))
    except ValueError:
        relative = str(path)

    return {
        "path": relative,
        "finding_count": len(findings),
        "findings": findings,
    }


def build_sql_direct_usage_inventory(
    roots: Iterable[Path],
    *,
    root: Path,
    exclude_parts: set[str] | None = None,
) -> dict:
    files = iter_python_files(roots, exclude_parts=exclude_parts)
    entries = []

    for path in files:
        entry = detect_sql_direct_usage(path, root=root)
        if entry["finding_count"]:
            entries.append(entry)

    entries = sorted(entries, key=lambda item: (-item["finding_count"], item["path"]))

    return {
        "inventory": "sql_direct_usage_inventory",
        "scope": "UI/services",
        "file_count_scanned": len(files),
        "file_count_with_findings": len(entries),
        "total_findings": sum(item["finding_count"] for item in entries),
        "entries": entries,
        "persistence_change": False,
        "schema_change": False,
        "operational_change": False,
        "versioning_operation": False,
    }


def write_inventory(
    output_path: Path,
    roots: Iterable[Path],
    *,
    root: Path,
    exclude_parts: set[str] | None = None,
) -> dict:
    inventory = build_sql_direct_usage_inventory(
        roots,
        root=root,
        exclude_parts=exclude_parts,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(inventory, indent=4, ensure_ascii=False),
        encoding="utf-8",
    )
    return inventory
