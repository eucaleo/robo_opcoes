from __future__ import annotations

import json
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT_DIR / "reports"

INITIAL_JSON = REPORTS_DIR / "phase_3c_initial_conference.json"
CODE_JSON = REPORTS_DIR / "phase_3c_code_surface_conference.json"


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    missing = [str(p) for p in [INITIAL_JSON, CODE_JSON] if not p.exists()]
    if missing:
        print("ERROR: missing required reports")
        for item in missing:
            print(item)
        return 1

    initial = _load_json(INITIAL_JSON)
    code = _load_json(CODE_JSON)

    print("=== PHASE 3C INITIAL CHECKPOINT ===")
    print(f"initial_report: {INITIAL_JSON}")
    print(f"code_report:    {CODE_JSON}")
    print("")

    statuses = [item["status"] for item in initial.get("results", [])]
    has_error = any(status == "error" for status in statuses)
    has_warning = any(status == "warning" for status in statuses)

    print("Initial conference statuses:")
    for item in initial.get("results", []):
        print(f"- {item['name']}: {item['status']}")

    print("")
    print("Code surface token totals:")
    for token, total in code.get("by_token", {}).items():
        print(f"- {token}: {total}")

    print("")
    if has_error:
        print("CHECKPOINT_RESULT=BLOCKED")
        return 1
    if has_warning:
        print("CHECKPOINT_RESULT=PROCEED_WITH_REVIEW")
        return 0

    print("CHECKPOINT_RESULT=READY_FOR_NEXT_PATCHES")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
