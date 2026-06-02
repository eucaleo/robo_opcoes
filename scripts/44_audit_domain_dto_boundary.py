"""
patch_44 — Auditoria: domínio como receptor de DTO
Verifica que payoff.py e decision.py NÃO acessam banco diretamente.
Gera relatório em ATT/reports/auditoria_patch44.json
"""
import os
import sys
import ast
import json
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

DOMAIN_FILES = [
    os.path.join(ROOT, "domain", "payoff.py"),
    os.path.join(ROOT, "domain", "decision.py"),
]

FORBIDDEN_IMPORTS = [
    "sqlite3",
    "get_app_db_connection",
    "get_derived_db_connection",
    "connect",
]

FORBIDDEN_CALLS = [
    "get_app_db_connection",
    "get_derived_db_connection",
    "sqlite3.connect",
    "cursor",
    "execute",
]

REPORT_DIR = os.path.join(ROOT, "ATT", "reports")


def _extract_imports(tree: ast.Module) -> list[dict]:
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                found.append({"type": "import", "name": alias.name, "line": node.lineno})
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                found.append({
                    "type": "from_import",
                    "module": module,
                    "name": alias.name,
                    "line": node.lineno,
                })
    return found


def _extract_calls(tree: ast.Module) -> list[dict]:
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                found.append({"call": node.func.id, "line": node.lineno})
            elif isinstance(node.func, ast.Attribute):
                found.append({
                    "call": f"{getattr(node.func.value, 'id', '?')}.{node.func.attr}",
                    "line": node.lineno,
                })
    return found


def audit_file(filepath: str) -> dict:
    rel = os.path.relpath(filepath, ROOT)
    result = {
        "file": rel,
        "exists": os.path.isfile(filepath),
        "violations_imports": [],
        "violations_calls": [],
        "clean": False,
    }

    if not result["exists"]:
        return result

    with open(filepath, encoding="utf-8") as f:
        source = f.read()

    try:
        tree = ast.parse(source, filename=filepath)
    except SyntaxError as e:
        result["parse_error"] = str(e)
        return result

    imports = _extract_imports(tree)
    calls = _extract_calls(tree)

    for imp in imports:
        name = imp.get("name", "")
        module = imp.get("module", "")
        for forbidden in FORBIDDEN_IMPORTS:
            if forbidden in name or forbidden in module:
                result["violations_imports"].append({
                    "forbidden": forbidden,
                    "line": imp["line"],
                    "detail": imp,
                })

    for call in calls:
        for forbidden in FORBIDDEN_CALLS:
            if forbidden in call["call"]:
                result["violations_calls"].append({
                    "forbidden": forbidden,
                    "line": call["line"],
                    "detail": call,
                })

    result["clean"] = (
        len(result["violations_imports"]) == 0
        and len(result["violations_calls"]) == 0
    )
    return result


def run_audit() -> dict:
    results = []
    for f in DOMAIN_FILES:
        results.append(audit_file(f))

    all_clean = all(r["clean"] for r in results)

    report = {
        "patch": "patch_44",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "root": ROOT,
        "domain_files_audited": [os.path.relpath(f, ROOT) for f in DOMAIN_FILES],
        "all_clean": all_clean,
        "results": results,
        "summary": {
            "total_files": len(results),
            "clean": sum(1 for r in results if r["clean"]),
            "with_violations": sum(1 for r in results if not r["clean"]),
        },
    }
    return report


def main():
    print("=" * 60)
    print("  PATCH 44 — Auditoria fronteira domínio/DTO")
    print("=" * 60)

    report = run_audit()

    # Exibe resumo
    for r in report["results"]:
        status = "✅ limpo" if r["clean"] else "❌ VIOLAÇÃO"
        print(f"\n  {status}  {r['file']}")
        for v in r.get("violations_imports", []):
            print(f"    [import] linha {v['line']}: '{v['forbidden']}'")
        for v in r.get("violations_calls", []):
            print(f"    [call]   linha {v['line']}: '{v['forbidden']}'")

    print(f"\n  Resultado geral: {'✅ DOMÍNIO LIMPO' if report['all_clean'] else '❌ HÁ VIOLAÇÕES'}")

    # Grava relatório JSON
    os.makedirs(REPORT_DIR, exist_ok=True)
    report_path = os.path.join(REPORT_DIR, "auditoria_patch44.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n  Relatório gravado em: {os.path.relpath(report_path, ROOT)}")

    sys.exit(0 if report["all_clean"] else 1)


if __name__ == "__main__":
    main()
