from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

FORBIDDEN_TRACKED_PREFIXES = (
    "FRENTE_RTD_EXCEL_BTG_ONLINE/output/",
)

FORBIDDEN_TRACKED_SUFFIXES = (
    "project_search_hits.txt",
)

MAX_TRACKED_FILE_BYTES = 50 * 1024 * 1024


def _git_ls_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return [
        line.strip().replace("\\", "/")
        for line in result.stdout.splitlines()
        if line.strip()
    ]


def test_generated_rtd_output_artifacts_are_not_tracked() -> None:
    tracked_files = _git_ls_files()

    forbidden = [
        path
        for path in tracked_files
        if path.startswith(FORBIDDEN_TRACKED_PREFIXES)
        or path.endswith(FORBIDDEN_TRACKED_SUFFIXES)
    ]

    assert forbidden == []


def test_no_tracked_file_exceeds_github_recommended_limit() -> None:
    tracked_files = _git_ls_files()

    oversized = []

    for relative_path in tracked_files:
        path = ROOT / relative_path

        if not path.exists() or not path.is_file():
            continue

        size = path.stat().st_size

        if size > MAX_TRACKED_FILE_BYTES:
            oversized.append(
                {
                    "path": relative_path,
                    "size_bytes": size,
                }
            )

    assert oversized == []
