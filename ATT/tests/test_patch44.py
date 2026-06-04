"""
Testes do patch_44 -- fronteira domínio/DTO.
Garante que payoff.py e decision.py não acessam banco diretamente.
"""
import os
import sys
import ast
import json
import unittest
import subprocess

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)

DOMAIN_PAYOFF   = os.path.join(ROOT, "domain", "payoff.py")
DOMAIN_DECISION = os.path.join(ROOT, "domain", "decision.py")
SCRIPT          = os.path.join(ROOT, "scripts", "44_audit_domain_dto_boundary.py")
REPORT_PATH     = os.path.join(ROOT, "ATT", "reports", "domain_dto_boundary.json")

FORBIDDEN_IMPORTS = ["sqlite3", "get_app_db_connection", "get_derived_db_connection"]


def _has_forbidden(filepath: str) -> list[str]:
    """Retorna lista de termos proibidos encontrados via AST."""
    if not os.path.isfile(filepath):
        return [f"FILE_NOT_FOUND:{filepath}"]
    with open(filepath, encoding="utf-8") as f:
        source = f.read()
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return ["SYNTAX_ERROR"]

    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                for fb in FORBIDDEN_IMPORTS:
                    if fb in alias.name:
                        found.append(f"import:{fb}:L{node.lineno}")
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                for fb in FORBIDDEN_IMPORTS:
                    if fb in module or fb in alias.name:
                        found.append(f"from_import:{fb}:L{node.lineno}")
    return found


class TestPatch44DomainNaoAcessaDB(unittest.TestCase):
    """Verifica ausência de acoplamento ao DB nos módulos de domínio."""

    def test_payoff_nao_importa_sqlite3(self):
        self.assertTrue(os.path.isfile(DOMAIN_PAYOFF), "domain/payoff.py não encontrado")
        with open(DOMAIN_PAYOFF, encoding="utf-8") as f:
            src = f.read()
        self.assertNotIn("import sqlite3", src,
                         "domain/payoff.py importa sqlite3 diretamente -- violação de fronteira")

    def test_decision_nao_importa_sqlite3(self):
        self.assertTrue(os.path.isfile(DOMAIN_DECISION), "domain/decision.py não encontrado")
        with open(DOMAIN_DECISION, encoding="utf-8") as f:
            src = f.read()
        self.assertNotIn("import sqlite3", src,
                         "domain/decision.py importa sqlite3 diretamente -- violação de fronteira")

    def test_payoff_nao_chama_get_app_db_connection(self):
        self.assertTrue(os.path.isfile(DOMAIN_PAYOFF))
        with open(DOMAIN_PAYOFF, encoding="utf-8") as f:
            src = f.read()
        self.assertNotIn("get_app_db_connection", src,
                         "domain/payoff.py chama get_app_db_connection -- violação de fronteira")

    def test_decision_nao_chama_get_app_db_connection(self):
        self.assertTrue(os.path.isfile(DOMAIN_DECISION))
        with open(DOMAIN_DECISION, encoding="utf-8") as f:
            src = f.read()
        self.assertNotIn("get_app_db_connection", src,
                         "domain/decision.py chama get_app_db_connection -- violação de fronteira")


class TestPatch44PayoffPuro(unittest.TestCase):
    """payoff.py deve ser importável sem efeitos de banco."""

    def test_payoff_importavel(self):
        """Importação não levanta exceção."""
        import importlib.util
        spec = importlib.util.spec_from_file_location("domain.payoff", DOMAIN_PAYOFF)
        self.assertIsNotNone(spec, "Não foi possível carregar spec de domain/payoff.py")
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
        except Exception as e:
            self.fail(f"domain/payoff.py levantou exceção ao importar: {e}")

    def test_payoff_sem_violacoes_ast(self):
        violations = _has_forbidden(DOMAIN_PAYOFF)
        self.assertEqual(violations, [],
                         f"domain/payoff.py tem importações proibidas: {violations}")


class TestPatch44DecisionPuro(unittest.TestCase):
    """decision.py deve ser importável sem efeitos de banco."""

    def test_decision_importavel(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("domain.decision", DOMAIN_DECISION)
        self.assertIsNotNone(spec)
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
        except Exception as e:
            self.fail(f"domain/decision.py levantou exceção ao importar: {e}")

    def test_decision_sem_violacoes_ast(self):
        violations = _has_forbidden(DOMAIN_DECISION)
        self.assertEqual(violations, [],
                         f"domain/decision.py tem importações proibidas: {violations}")

    def test_script_auditoria_existe(self):
        self.assertTrue(
            os.path.isfile(SCRIPT),
            f"scripts/44_audit_domain_dto_boundary.py não encontrado em {SCRIPT}",
        )

    def test_relatorio_gerado_apos_execucao(self):
        """Executa o script e verifica se o JSON de relatório é gerado."""
        result = subprocess.run(
            [sys.executable, SCRIPT],
            capture_output=True, text=True, cwd=ROOT
        )
        # exit 0 = domínio limpo, exit 1 = violações encontradas -- ambos geram relatório
        self.assertTrue(
            os.path.isfile(REPORT_PATH),
            f"Relatório JSON não foi gerado em {os.path.relpath(REPORT_PATH, ROOT)}",
        )
        with open(REPORT_PATH, encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("patch", data)
        self.assertIn("results", data)
        self.assertIn("all_clean", data)


if __name__ == "__main__":
    unittest.main()
