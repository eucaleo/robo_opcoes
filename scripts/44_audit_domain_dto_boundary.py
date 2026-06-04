# scripts/44_audit_domain_dto_boundary.py
"""
Auditoria de fronteira domínio/DTO -- patch_44.
Verifica que domain/payoff.py e domain/decision.py não importam
sqlite3, get_app_db_connection ou get_derived_db_connection.
Gera ATT/reports/domain_dto_boundary.json com:
  - patch
  - results   (dict por arquivo)
  - all_clean (bool)
Exit 0 se limpo, exit 1 se há violações (ambos geram o JSON).
"""
import ast
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

TARGETS = {
    "domain/payoff.py":    os.path.join(ROOT, "domain", "payoff.py"),
    "domain/decision.py":  os.path.join(ROOT, "domain", "decision.py"),
}

FORBIDDEN = ["sqlite3", "get_app_db_connection", "get_derived_db_connection"]

REPORT_DIR  = os.path.join(ROOT, "ATT", "reports")
REPORT_PATH = os.path.join(REPORT_DIR, "domain_dto_boundary.json")


def audit_file(path: str) -> dict:
    if not os.path.isfile(path):
        return {"status": "FILE_NOT_FOUND", "violations": [f"FILE_NOT_FOUND:{path}"]}

    with open(path, encoding="utf-8") as f:
        source = f.read()

    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        return {"status": "SYNTAX_ERROR", "violations": [f"SYNTAX_ERROR:{e}"]}

    violations = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                for fb in FORBIDDEN:
                    if fb in alias.name:
                        violations.append(f"import:{fb}:L{node.lineno}")
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                for fb in FORBIDDEN:
                    if fb in module or fb in alias.name:
                        violations.append(f"from_import:{fb}:L{node.lineno}")

    return {
        "status": "clean" if not violations else "violations_found",
        "violations": violations,
    }


def main() -> int:
    results = {}
    for label, path in TARGETS.items():
        results[label] = audit_file(path)

    all_clean = all(r["status"] == "clean" for r in results.values())

    report = {
        "patch":     "patch_44",
        "results":   results,
        "all_clean": all_clean,
    }

    os.makedirs(REPORT_DIR, exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    status = "LIMPO" if all_clean else "VIOLACOES ENCONTRADAS"
    print(f"[patch_44] Auditoria concluída: {status}")
    print(f"[patch_44] Relatório: {os.path.relpath(REPORT_PATH, ROOT)}")
    for label, res in results.items():
        print(f"  {label}: {res['status']}")
        for v in res["violations"]:
            print(f"    -> {v}")

    return 0 if all_clean else 1


if __name__ == "__main__":
    sys.exit(main())
