from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE_SCRIPT = Path(__file__).resolve().with_name("refresh_rtd_symbol_to_option_quotes.py")


def ensure_json_arg(args: list[str]) -> list[str]:
    if "--json" not in args:
        return args + ["--json"]
    return args


def set_visible_arg(args: list[str], visible: bool) -> list[str]:
    cleaned = [a for a in args if a != "--visible"]

    if visible:
        cleaned.append("--visible")

    return cleaned


def extract_json(stdout: str) -> dict | None:
    text = stdout.strip()

    if not text:
        return None

    try:
        return json.loads(text)
    except Exception:
        pass

    start = text.find("{")
    end = text.rfind("}")

    if start >= 0 and end > start:
        try:
            return json.loads(text[start:end + 1])
        except Exception:
            return None

    return None


def run_attempt(args: list[str], visible: bool) -> dict:
    attempt_args = ensure_json_arg(set_visible_arg(args, visible))

    cmd = [
        sys.executable,
        str(BASE_SCRIPT),
        *attempt_args,
    ]

    cp = subprocess.run(
        cmd,
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )

    data = extract_json(cp.stdout)

    return {
        "visible": visible,
        "command": cmd,
        "returncode": cp.returncode,
        "stdout": cp.stdout,
        "stderr": cp.stderr,
        "json": data,
        "ok": cp.returncode == 0 and isinstance(data, dict) and data.get("status") == "ok",
        "status": data.get("status") if isinstance(data, dict) else None,
        "errors": data.get("errors") if isinstance(data, dict) else None,
    }


def summarize_attempt(attempt: dict) -> dict:
    return {
        "visible": attempt["visible"],
        "returncode": attempt["returncode"],
        "ok": attempt["ok"],
        "status": attempt["status"],
        "errors": attempt["errors"],
    }


def main(argv: list[str]) -> int:
    if not BASE_SCRIPT.exists():
        result = {
            "status": "error",
            "errors": [f"Script base não encontrado: {BASE_SCRIPT}"],
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1

    original_args = argv[:]

    # Se o usuário já pediu --visible explicitamente, não faz fallback.
    # Apenas delega para o script original.
    if "--visible" in original_args:
        attempt = run_attempt(original_args, visible=True)

        data = attempt["json"] or {
            "status": "error",
            "errors": ["Falha ao executar tentativa visível."],
            "stdout": attempt["stdout"],
            "stderr": attempt["stderr"],
        }

        if isinstance(data, dict):
            data["fallback"] = {
                "used": False,
                "reason": "visible_requested_explicitly",
                "attempts": [summarize_attempt(attempt)],
            }

        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0 if attempt["ok"] else 1

    # 1) Primeira tentativa: invisível/silenciosa.
    first = run_attempt(original_args, visible=False)

    if first["ok"]:
        data = first["json"]
        data["fallback"] = {
            "used": False,
            "reason": "invisible_attempt_succeeded",
            "attempts": [summarize_attempt(first)],
        }
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0

    # 2) Segunda tentativa: visível.
    second = run_attempt(original_args, visible=True)

    data = second["json"] or {
        "status": "error",
        "errors": ["Tentativa invisível falhou e tentativa visível também não retornou JSON válido."],
        "visible_attempt_stdout": second["stdout"],
        "visible_attempt_stderr": second["stderr"],
    }

    if isinstance(data, dict):
        data["fallback"] = {
            "used": True,
            "reason": "invisible_attempt_failed_then_visible_retry",
            "attempts": [
                summarize_attempt(first),
                summarize_attempt(second),
            ],
        }

    print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0 if second["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
