# ATT/tests/test_patch41.py
"""Testes formais do patch_41 -- canonical_pricing_facade.py."""
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

FACADE_FILE = str(ROOT / "services" / "canonical_pricing_facade.py")


def _read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


class TestPatch41ArquivoExiste(unittest.TestCase):
    def test_facade_existe(self):
        self.assertTrue(
            os.path.isfile(FACADE_FILE),
            f"Nao encontrado: {FACADE_FILE}"
        )


class TestPatch41Renome(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not os.path.isfile(FACADE_FILE):
            raise unittest.SkipTest("Facade nao encontrada -- skip conteudo")
        cls.src = _read(FACADE_FILE)

    def test_get_structure_info_presente(self):
        self.assertIn("_get_structure_info", self.src)

    def test_get_alias_legacy_aba_removido(self):
        self.assertNotIn("def _get_alias_legacy_aba", self.src,
            "_get_alias_legacy_aba ainda presente -- patch_41 nao aplicado")


class TestPatch41InterfacePublica(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not os.path.isfile(FACADE_FILE):
            raise unittest.SkipTest("Facade nao encontrada -- skip interface")
        cls.src = _read(FACADE_FILE)

    def test_execute_pricing_presente(self):
        self.assertIn("def execute_pricing(", self.src)

    def test_class_presente(self):
        self.assertIn("class CanonicalPricingFacade", self.src)


class TestPatch41SemArquivoNovo(unittest.TestCase):
    def test_nenhum_patch41_em_att_patches(self):
        patches_dir = ROOT / "ATT" / "patches"
        if not patches_dir.is_dir():
            self.skipTest("ATT/patches/ nao existe")
        p41 = [f for f in os.listdir(patches_dir)
               if "patch_41" in f.lower() and f.endswith(".py")]
        self.assertEqual(len(p41), 0,
            f"Arquivo inesperado com patch_41 em ATT/patches/: {p41}")


if __name__ == "__main__":
    unittest.main()
