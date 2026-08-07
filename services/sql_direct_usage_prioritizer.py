from __future__ import annotations

import re
from collections import Counter
from typing import Any

SQL_KEYWORD_RE = re.compile(
    r"\b("
    r"select|with|pragma|insert\s+into|update|delete\s+from|"
    r"create\s+table|drop\s+table|join|from"
    r")\b",
    re.IGNORECASE,
)

EXECUTE_RE = re.compile(
    r"\b(conn|con|cur|cursor|connection)\.execute\s*\(",
    re.IGNORECASE,
)

PYTHON_IMPORT_RE = re.compile(
    r"^\s*(from\s+[\w.]+\s+import\b|import\s+[\w.]+)",
    re.IGNORECASE,
)

PYTHON_DEF_RE = re.compile(
    r"^\s*(def|async\s+def|class)\s+",
    re.IGNORECASE,
)


def _normalize_path(path: str) -> str:
    return str(path or "").replace("\\", "/").lower()


def _strip_literal_prefix(value: str) -> str:
    """
    Remove prefixos de literal Python como f, r, b, u, fr, rf etc.
    Implementação propositalmente sem loop para evitar travamento.
    """
    s = str(value or "").strip()
    s = s.lstrip(" \t([{")

    lower = s.lower()
    for prefix in ("fr", "rf", "br", "rb", "ur", "ru", "f", "r", "b", "u"):
        if lower.startswith(prefix) and len(s) > len(prefix) and s[len(prefix)] in ("'", '"'):
            s = s[len(prefix):].lstrip()
            break

    return s.lstrip("\"'").strip()


def _is_python_false_positive(preview: str) -> bool:
    s = str(preview or "").strip()
    lower = s.lower()

    if not s:
        return True
    if PYTHON_IMPORT_RE.search(s):
        return True
    if PYTHON_DEF_RE.search(s):
        return True
    if lower.startswith("#"):
        return True
    if lower.startswith("- from __future__"):
        return True
    if "__future__" in lower:
        return True
    if lower.startswith("yield from "):
        return True
    if lower.startswith("raise ") and " from " in lower:
        return True
    if lower.startswith(") from "):
        return True
    if lower.startswith("] from "):
        return True
    if lower.startswith("} from "):
        return True
    if lower == "from exc":
        return True
    if lower.endswith(" from exc") and not SQL_KEYWORD_RE.search(_strip_literal_prefix(s).lower().split(" from exc", 1)[0]):
        return True

    return False


def is_direct_sql_preview(preview: str) -> bool:
    s = str(preview or "").strip()

    if _is_python_false_positive(s):
        return False

    if EXECUTE_RE.search(s):
        return True

    candidate = _strip_literal_prefix(s)

    if _is_python_false_positive(candidate):
        return False

    if SQL_KEYWORD_RE.search(candidate):
        return True

    return False


def filter_direct_sql_findings(findings: Any) -> list[dict[str, Any]]:
    if not isinstance(findings, list):
        return []

    filtered: list[dict[str, Any]] = []
    seen: set[tuple[Any, str]] = set()

    for item in findings:
        if not isinstance(item, dict):
            continue

        preview = str(item.get("preview", ""))
        if is_direct_sql_preview(preview):
            key = (item.get("line"), preview)
            if key not in seen:
                seen.add(key)
                filtered.append(item)

    return filtered


def _direct_sql_findings(findings: Any) -> list[dict[str, Any]]:
    return filter_direct_sql_findings(findings)


def _path_text(entry: dict[str, Any]) -> str:
    return str(entry.get("path") or entry.get("file") or entry.get("target") or "")


def _is_ui(path: str) -> bool:
    p = path.replace("/", "\\").lower()
    return p.startswith("ui\\") or "\\ui\\" in p


def _is_service(path: str) -> bool:
    p = path.replace("/", "\\").lower()
    return p.startswith("services\\") or "\\services\\" in p


def _is_payoff_related(path: str, entry: dict[str, Any]) -> bool:
    parts = [
        path,
        str(entry.get("module", "") or ""),
        str(entry.get("component", "") or ""),
        str(entry.get("preview", "") or ""),
    ]

    for f in entry.get("direct_sql_findings", []) or []:
        if isinstance(f, dict):
            parts.append(str(f.get("preview", "")))

    for f in entry.get("findings", []) or []:
        if isinstance(f, dict):
            parts.append(str(f.get("preview", "")))

    txt = " ".join(parts).lower()
    return any(token in txt for token in ("payoff", "curve", "structure", "consolidation"))


def _score_entry(path: str, count: int, payoff: bool, ui: bool, service: bool) -> tuple[int, str, bool, bool, bool]:
    score = count * 10

    if payoff:
        score += 70
    if ui:
        score += 20
    if service:
        score += 8

    p = path.replace("/", "\\").lower()

    if "payoff" in p:
        score += 30
    if "terminal_vwap" in p:
        score += 40
    if p.endswith("ui\\models\\ui_data.py"):
        score += 30

    if score >= 120 or (payoff and count >= 2):
        priority = "P0"
    elif score >= 70:
        priority = "P1"
    elif score >= 25:
        priority = "P2"
    else:
        priority = "P3"

    return score, priority, payoff, ui, service


def _recommended_action(priority: str, payoff: bool, ui: bool, service: bool) -> str:
    if ui and payoff:
        return "extrair leitura SQL direta da UI para service/query adapter dedicado"
    if service and payoff:
        return "substituir SQL direto por repository existente ou criar porta local sem alterar schema"
    if priority in {"P0", "P1"}:
        return "avaliar migracao incremental para camada repository/service"
    return "manter em backlog tecnico apos P0/P1"


def prioritize_entries(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    prioritized: list[dict[str, Any]] = []

    for entry in entries:
        if not isinstance(entry, dict):
            continue

        path = _path_text(entry)
        findings = entry.get("findings") or entry.get("direct_sql_findings") or []
        direct = filter_direct_sql_findings(findings)
        count = len(direct)

        if count <= 0:
            continue

        payoff = _is_payoff_related(path, entry)
        ui = _is_ui(path)
        service = _is_service(path)
        score, priority, payoff, ui, service = _score_entry(path, count, payoff, ui, service)

        prioritized.append(
            {
                "path": path,
                "priority": priority,
                "score": score,
                "direct_sql_finding_count": count,
                "payoff_related": payoff,
                "ui_related": ui,
                "service_related": service,
                "direct_sql_findings": direct,
                "recommended_action": _recommended_action(priority, payoff, ui, service),
            }
        )

    prio_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    prioritized.sort(key=lambda x: (prio_order.get(x["priority"], 99), -x["score"], x["path"]))
    return prioritized


def prioritize_inventory(inventory: dict[str, Any]) -> dict[str, Any]:
    entries = inventory.get("entries", [])
    prioritized = prioritize_entries(list(entries) if isinstance(entries, list) else [])
    counts = Counter(x["priority"] for x in prioritized)

    return {
        "inventory": "sql_direct_usage_priority",
        "source_inventory": inventory.get("inventory", "sql_direct_usage_inventory"),
        "scope": "payoff/UI/services",
        "total_candidates": len(prioritized),
        "priority_counts": dict(sorted(counts.items())),
        "entries": prioritized,
        "persistence_change": False,
        "schema_change": False,
        "operational_change": False,
        "versioning_operation": False,
    }


def generate_priority_inventory(inventory: dict[str, Any] | None = None) -> dict[str, Any]:
    if inventory is None:
        inventory = {
            "inventory": "sql_direct_usage_inventory",
            "entries": [],
        }

    return prioritize_inventory(inventory)


__all__ = [
    "filter_direct_sql_findings",
    "generate_priority_inventory",
    "is_direct_sql_preview",
    "prioritize_entries",
    "prioritize_inventory",
]
