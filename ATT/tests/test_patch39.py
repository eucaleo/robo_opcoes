# ATT/tests/test_patch39.py
"""Testes formais do patch_39 — auditoria pre-patch/3b baseline."""
import os
import sys
import unittest
from pathlib import Path


def _find_project_root(start: Path) -> Path:
    for parent in [start, *start.parents]:
        if (parent / ".git").exists():
            return parent
        if (parent / "scripts").is_dir() and (parent / "ATT").is_dir():
            return parent
    return start.parent.parent.parent


ROOT = _find_project_root(Path(__file__).resolve())
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SCRIPT_FILE = str(ROOT / "scripts" / "39_audit_patch3b_baseline.py")


def _read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


class TestPatch39ScriptExiste(unittest.TestCase):
    def test_script_existe(self):
        self.assertTrue(
            os.path.isfile(SCRIPT_FILE),
            f"Nao encontrado: {SCRIPT_FILE}"
        )


class TestPatch39ConteudoEstrutura(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not os.path.isfile(SCRIPT_FILE):
            raise unittest.SkipTest("Script nao encontrado — skip conteudo")
        cls.src = _read(SCRIPT_FILE)

    def test_run_audit_presente(self):
        self.assertIn("def run_audit(", self.src)

    def test_suspected_residuals(self):
        self.assertIn("SUSPECTED_RESIDUALS", self.src)

    def test_legacy_patterns(self):
        self.assertIn("LEGACY_PATTERNS", self.src)

    def test_domain_files_to_check(self):
        self.assertIn("DOMAIN_FILES_TO_CHECK", self.src)

    def test_relatorio_auditoria_patch39(self):
        self.assertIn("auditoria_patch39", self.src)

    def test_git_branch(self):
        self.assertIn("_git_branch", self.src)


class TestPatch39ImportsBasicos(unittest.TestCase):
    def test_imports(self):
        import importlib
        for m in ["os", "re", "sys", "hashlib", "subprocess", "pathlib"]:
            with self.subTest(m=m):
                self.assertIsNotNone(importlib.import_module(m))


if __name__ == "__main__":
    unittest.main()
