# scripts/verify_patch20.py
"""
Verifica se patch_20 foi aplicado corretamente.
Critério: todos os conn.close() devem estar dentro de blocos try/finally
ou usar context manager (with conn:).
"""

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Arquivos que patch_20 deveria ter tocado
TARGET_FILES = [
    "repositories/structures_repository.py",
    "repositories/robo_legs_repository.py",
    "repositories/snapshot_repository.py",
    "repositories/derived_repository.py",
    "infrastructure/db.py",
]

# ──────────────────────────────────────────────
# AST visitor: detecta conn.close() fora de finally
# ──────────────────────────────────────────────
class ConnCloseChecker(ast.NodeVisitor):
    def __init__(self, source: str):
        self.source = source
        self.issues: list[dict] = []
        self._in_finally = False

    def visit_Try(self, node: ast.Try):
        # Visita corpo e handlers normalmente
        for child in node.body:
            self.visit(child)
        for handler in node.handlers:
            self.visit(handler)
        for child in node.orelse:
            self.visit(child)

        # Marca que estamos dentro de finally
        prev = self._in_finally
        self._in_finally = True
        for child in node.finalbody:
            self.visit(child)
        self._in_finally = prev

    def visit_With(self, node: ast.With):
        """with conn: é padrão seguro — não reporta."""
        self.generic_visit(node)

    def visit_Expr(self, node: ast.Expr):
        """Detecta conn.close() como statement solto."""
        if isinstance(node.value, ast.Call):
            call = node.value
            if (
                isinstance(call.func, ast.Attribute)
                and call.func.attr == "close"
                and isinstance(call.func.value, ast.Name)
                and "conn" in call.func.value.id
            ):
                if not self._in_finally:
                    self.issues.append({
                        "line": node.lineno,
                        "col": node.col_offset,
                        "code": ast.get_source_segment(self.source, node) or "conn.close()",
                    })
        self.generic_visit(node)


# ──────────────────────────────────────────────
# Verifica também uso de context manager
# ──────────────────────────────────────────────
def uses_context_manager(source: str) -> bool:
    """Retorna True se o arquivo usa 'with ... as conn' (padrão seguro)."""
    try:
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.With):
                for item in node.items:
                    if isinstance(item.optional_vars, ast.Name):
                        if "conn" in item.optional_vars.id:
                            return True
    except Exception:
        pass
    return False


# ──────────────────────────────────────────────
# Runner principal
# ──────────────────────────────────────────────
def verify_file(rel_path: str) -> dict:
    path = ROOT / rel_path
    result = {
        "file": rel_path,
        "exists": path.exists(),
        "issues": [],
        "uses_context_manager": False,
        "status": "⬜ NÃO ENCONTRADO",
    }

    if not path.exists():
        return result

    source = path.read_text(encoding="utf-8")
    result["uses_context_manager"] = uses_context_manager(source)

    try:
        tree = ast.parse(source)
        checker = ConnCloseChecker(source)
        checker.visit(tree)
        result["issues"] = checker.issues
    except SyntaxError as e:
        result["issues"] = [{"line": 0, "col": 0, "code": f"SyntaxError: {e}"}]

    if result["issues"]:
        result["status"] = "🔴 PROBLEMA DETECTADO"
    elif result["uses_context_manager"]:
        result["status"] = "✅ OK (context manager)"
    else:
        result["status"] = "✅ OK (try/finally)"

    return result


def main():
    print("=" * 60)
    print("  VERIFICAÇÃO patch_20 — conn.close() safety")
    print("=" * 60)

    all_ok = True

    for rel_path in TARGET_FILES:
        result = verify_file(rel_path)
        print(f"\n📄 {result['file']}")
        print(f"   Status : {result['status']}")

        if result["uses_context_manager"]:
            print("   Padrão : with conn: (context manager)")

        if result["issues"]:
            all_ok = False
            for issue in result["issues"]:
                print(f"   ⚠️  Linha {issue['line']}: {issue['code']}")

    print("\n" + "=" * 60)
    if all_ok:
        print("  ✅ patch_20 CONFIRMADO — nenhum conn.close() exposto")
    else:
        print("  🔴 patch_20 INCOMPLETO — revisar itens acima")
    print("=" * 60)

    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
