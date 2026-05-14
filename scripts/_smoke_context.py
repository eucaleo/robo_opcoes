import json
import os
from pathlib import Path


def _context_file_path():
    env_path = os.environ.get("SMOKE_CONTEXT_FILE")
    if env_path:
        return Path(env_path)

    return Path(__file__).resolve().parent / ".smoke_context.json"


def load_context():
    path = _context_file_path()

    if not path.exists():
        return {}

    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_context(data):
    path = _context_file_path()
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def update_context(**kwargs):
    data = load_context()
    data.update(kwargs)
    save_context(data)
    return data


def require_context_value(key):
    data = load_context()

    if key not in data:
        raise RuntimeError(f"smoke context should contain '{key}'")

    return data[key]


def clear_context():
    path = _context_file_path()

    if path.exists():
        path.unlink()
