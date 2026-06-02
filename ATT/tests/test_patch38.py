# ATT/tests/test_patch38.py
# Testes formais do patch_38
# Polish pós-patch_37 — get_structures() lazy-load consolidado;
# comentário regex corrigido

import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

UI_DATA = os.path.join(ROOT, "UI", "models", "ui_data.py")
PATCHES_MD = os.path.join(ROOT, "ATT", "PATCHES.md")


def _read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


class TestPatch38UIDataExists(unittest.TestCase):
    """Check 1 — UI/models/ui_data.py existe"""

    def test_ui_data_existe(self):
        self.assertTrue(os.path.isfile(UI_DATA), "UI/models/ui_data.py não encontrado")


class TestPatch38LazyLoad(unittest.TestCase):
    """Checks 2 e 3 — get_structures() com lazy-load e _cache_structures"""

    @classmethod
    def setUpClass(cls):
        cls.src = _read(UI_DATA)

    def test_get_structures_lazy_load_presente(self):
        self.assertIn(
            "get_structures",
            self.src,
            "get_structures() com lazy-load não encontrado em ui_data.py",
        )

    def test_cache_structures_no_lazy_load(self):
        self.assertIn(
            "_cache_structures",
            self.src,
            "_cache_structures não encontrado em ui_data.py",
        )


class TestPatch38SemResiduos(unittest.TestCase):
    """Checks 4 e 5 — sem resíduos _cache_abas / self.abas"""

    @classmethod
    def setUpClass(cls):
        cls.src = _read(UI_DATA)

    def test_sem_cache_abas(self):
        self.assertNotIn(
            "_cache_abas",
            self.src,
            "Resíduo _cache_abas ainda presente em ui_data.py",
        )

    def test_sem_self_abas(self):
        self.assertNotIn(
            "self.abas",
            self.src,
            "Resíduo self.abas ainda presente em ui_data.py",
        )


class TestPatch38PatchesMd(unittest.TestCase):
    """Checks 6, 7 e 8 — ATT/PATCHES.md existe e registra patch_37 e patch_38"""

    @classmethod
    def setUpClass(cls):
        cls.src = _read(PATCHES_MD)

    def test_patches_md_existe(self):
        self.assertTrue(os.path.isfile(PATCHES_MD), "ATT/PATCHES.md não encontrado")

    def test_patch37_registrado(self):
        self.assertIn(
            "patch_37",
            self.src,
            "patch_37 não registrado em ATT/PATCHES.md",
        )

    def test_patch38_registrado(self):
        self.assertIn(
            "patch_38",
            self.src,
            "patch_38 não registrado em ATT/PATCHES.md",
        )


class TestPatch38BackupGerado(unittest.TestCase):
    """Check 9 — backup ui_data.py.bak_p38_* gerado"""

    def test_backup_nao_existe(self):
        """Nenhum .bak_p38 deve existir — removidos em chore 1bbe32e.
        Repo usa git para historico; backups manuais sao proibidos.
        """
        models_dir = os.path.join(ROOT, "UI", "models")
        backups = [
            f for f in os.listdir(models_dir)
            if f.startswith("ui_data.py.bak_p38_")
        ]
        self.assertEqual(
            len(backups), 0,
            f"Arquivos .bak_p38 encontrados (devem ser removidos): {backups}",
        )


if __name__ == "__main__":
    unittest.main()
