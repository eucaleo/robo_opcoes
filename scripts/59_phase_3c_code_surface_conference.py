from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT_DIR / "reports"
OUTPUT_JSON = REPORTS_DIR / "phase_3c_code_surface_conference.json"
OUTPUT_MD = REPORTS_DIR / "phase_3c_code_surface_conference.md"

TARGET_DIRS = [
    ROOT_DIR / "services",
    ROOT_DIR / "repositories",
    ROOT_DIR / "domain",
    ROOT_DIR / "db",
    ROOT_DIR / "api",
]

TOKENS = [
    "aba",
    "alias_legacy_aba",
    "structure_id",
    "timestamp",
    "manual_analise_robo_legs",
    "rtd_analise_robo_legs",
    "read_structure_legs",
    "to_canonical_leg",
    "CanonicalInputService",
    "LegacyRoboLegsFallback",
]


@dataclass
class TokenHit:
    file: str
    token: str
    count: int


def _utc_now_iso() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat()


def _iter_python_files() -> list[Path]:
    files: list[Path] = []
    for base in TARGET_DIRS:
        if not base.exists():
            continue
        files.extend(sorted(base.rglob("*.py")))
    return files


def _count_token(text: str, token: str) -> int:
    return len(re.findall(re.escape(token), text))


def main() -> int:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    files = _iter_python_files()
    hits: list[TokenHit] = []
    by_token: dict[str, int] = {token: 0 for token in TOKENS}

    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = path.read_text(encoding="latin-1")

        rel = str(path.relative_to(ROOT_DIR))
        for token in TOKENS:
            count = _count_token(text, token)
            if count > 0:
                hits.append(TokenHit(file=rel, token=token, count=count))
                by_token[token] += count

    payload: dict[str, Any] = {
        "generated_at": _utc_now_iso(),
        "root_dir": str(ROOT_DIR),
        "files_scanned": [str(p.relative_to(ROOT_DIR)) for p in files],
        "total_files_scanned": len(files),
        "by_token": by_token,
        "hits": [asdict(hit) for hit in hits],
    }

    OUTPUT_JSON.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    lines: list[str] = []
    lines.append("# Phase 3C — Code Surface Conference")
    lines.append("")
    lines.append(f"Generated at: `{payload['generated_at']}`")
    lines.append("")
    lines.append("## Totais por token")
    lines.append("")
    for token, total in by_token.items():
        lines.append(f"- **{token}**: {total}")
    lines.append("")
    lines.append("## Ocorrências")
    lines.append("")
    for hit in hits:
        lines.append(f"- `{hit.token}` -> `{hit.file}` ({hit.count})")
    lines.append("")

    OUTPUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print("OK: code surface conference generated")
    print(f"JSON: {OUTPUT_JSON}")
    print(f"MD:   {OUTPUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
