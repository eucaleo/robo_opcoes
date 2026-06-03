# ATT/tests/test_patch40.py
"""Testes formais do patch_40 — isolamento de acoplamento legado."""
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

ROBO_LEGS_REPO    = str(ROOT / "repositories" / "robo_legs_repository.py")
ROBO_STATUS_REPO  = str(ROOT / "repositories" / "robo_legs_status_repository.py")
DERIVED_SERVICE   = str(ROOT / "services" / "derived_service.py")
ROBO_LEGS_SERVICE = str(ROOT / "services" / "robo_legs_service.py")
PATCH_SCRIPT      = str(ROOT / "scripts" / "40_patch_legacy_coupling_isolation.py")


def _read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def _skip_if_absent(path):
    if not os.path.isfile(path):
        raise unittest.SkipTest(f"Arquivo nao encontrado: {path}")


class TestPatch40ArquivosExistem(unittest.TestCase):
    def test_robo_legs_repo(self):
        self.assertTrue(os.path.isfile(ROBO_LEGS_REPO),
            f"Nao encontrado: {ROBO_LEGS_REPO}")

    def test_robo_status_repo(self):
        self.assertTrue(os.path.isfile(ROBO_STATUS_REPO),
            f"Nao encontrado: {ROBO_STATUS_REPO}")

    def test_derived_service(self):
        self.assertTrue(os.path.isfile(DERIVED_SERVICE),
            f"Nao encontrado: {DERIVED_SERVICE}")

    def test_robo_legs_service(self):
        self.assertTrue(os.path.isfile(ROBO_LEGS_SERVICE),
            f"Nao encontrado: {ROBO_LEGS_SERVICE}")

    def test_patch_script(self):
        self.assertTrue(os.path.isfile(PATCH_SCRIPT),
            f"Nao encontrado: {PATCH_SCRIPT}")


class TestPatch40RoboLegsRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _skip_if_absent(ROBO_LEGS_REPO)
        cls.src = _read(ROBO_LEGS_REPO)

    def test_get_legs_by_structure_id(self):
        self.assertIn("get_legs_by_structure_id", self.src)

    def test_resolve_aba_from_structure_id(self):
        self.assertIn("_resolve_aba_from_structure_id", self.src)

    def test_has_manual_by_structure_id(self):
        self.assertIn("has_manual_by_structure_id", self.src)

    def test_list_timestamps_by_structure_id(self):
        self.assertIn("list_timestamps_by_structure_id", self.src)

    def test_backward_compat_get_legs(self):
        self.assertIn("def get_legs(", self.src)

    def test_backward_compat_has_manual(self):
        self.assertIn("def has_manual(", self.src)

    def test_backward_compat_list_timestamps(self):
        self.assertIn("def list_timestamps(", self.src)


class TestPatch40RoboLegsStatusRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _skip_if_absent(ROBO_STATUS_REPO)
        cls.src = _read(ROBO_STATUS_REPO)

    def test_latest_timestamps_by_structure_id(self):
        self.assertIn("latest_timestamps_by_structure_id", self.src)

    def test_resolve_aba_from_structure_id(self):
        self.assertIn("_resolve_aba_from_structure_id", self.src)


class TestPatch40DerivedService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _skip_if_absent(DERIVED_SERVICE)
        cls.src = _read(DERIVED_SERVICE)

    def test_get_payoff_by_structure_id(self):
        self.assertIn("get_payoff_by_structure_id", self.src)

    def test_backward_compat_get_payoff_by_aba(self):
        self.assertIn("get_payoff_by_aba", self.src)


class TestPatch40RoboLegsService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _skip_if_absent(ROBO_LEGS_SERVICE)
        cls.src = _read(ROBO_LEGS_SERVICE)

    def test_get_legs_by_structure_id(self):
        self.assertIn("get_legs_by_structure_id", self.src)


if __name__ == "__main__":
    unittest.main()
