"""
Testes formais do patch_61 -- remocao de scripts tmp_*
"""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS_DIR = ROOT / "scripts"

TMP_TARGETS = [
    "tmp_fix_todos_patch53b.py",
    "tmp_show_todos_patch53.py",
    "tmp_verify_patch53b.py",
]


class TestPatch61TmpScriptsRemovidos(unittest.TestCase):

    def test_tmp_fix_todos_nao_existe(self):
        path = SCRIPTS_DIR / "tmp_fix_todos_patch53b.py"
        self.assertFalse(
            path.exists(),
            f"Arquivo tmp residual ainda presente: {path}"
        )

    def test_tmp_show_todos_nao_existe(self):
        path = SCRIPTS_DIR / "tmp_show_todos_patch53.py"
        self.assertFalse(
            path.exists(),
            f"Arquivo tmp residual ainda presente: {path}"
        )

    def test_tmp_verify_nao_existe(self):
        path = SCRIPTS_DIR / "tmp_verify_patch53b.py"
        self.assertFalse(
            path.exists(),
            f"Arquivo tmp residual ainda presente: {path}"
        )

    def test_zero_tmp_em_scripts(self):
        remaining = list(SCRIPTS_DIR.glob("tmp_*.py"))
        self.assertEqual(
            remaining,
            [],
            f"Scripts tmp_*.py ainda presentes: {[f.name for f in remaining]}"
        )



if __name__ == "__main__":
    unittest.main()
