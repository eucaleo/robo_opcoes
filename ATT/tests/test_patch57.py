# ATT/tests/test_patch57.py
"""
patch_57 -- testes de validacao:
  - from __future__ na posicao correta nos 3 servicos corrigidos
  - StructureRef importado de src.domain.refs (canonico)
  - derived_service: _unwrap_ref() presente e funcional
  - canonical_input_service: _resolve_legs_via_selector usa ref.aba
  - robo_legs_service: get_legs extrai aba de StructureRef
  - scripts tmp_* removidos do inventario principal
  - 74_audit_public_api_aba_surface.py existe e executa
"""

from __future__ import annotations

import ast
import importlib
import inspect
import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def _first_non_docstring_line(source: str) -> str:
    """Retorna o primeiro token de codigo real (apos docstring e shebang)."""
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module == "__future__":
                return f"from __future__ import {node.names[0].name}"
    return ""


class TestFutureImportOrdem(unittest.TestCase):
    """from __future__ deve ser a primeira instrucao real de cada modulo."""

    def _check_future_first(self, rel: str) -> None:
        src   = _read(rel)
        lines = src.splitlines()
        code_lines = [
            ln.strip() for ln in lines
            if ln.strip()
            and not ln.strip().startswith("#")
            and not ln.strip().startswith('"""')
            and not ln.strip().startswith("'''")
        ]
        # primeira linha de codigo real deve ser from __future__
        first = code_lines[0] if code_lines else ""
        self.assertTrue(
            first.startswith("from __future__"),
            f"{rel}: primeira linha de codigo nao e 'from __future__', encontrado: {first!r}",
        )

    def test_canonical_input_service_future_primeiro(self):
        self._check_future_first("services/canonical_input_service.py")

    def test_robo_legs_service_future_primeiro(self):
        self._check_future_first("services/robo_legs_service.py")

    def test_derived_service_future_primeiro(self):
        self._check_future_first("services/derived_service.py")


class TestStructureRefCanonical(unittest.TestCase):
    """src/domain/refs/structure_ref.py e' o modulo canonico."""

    def test_importavel(self):
        from src.domain.refs.structure_ref import StructureRef
        self.assertTrue(callable(StructureRef.from_id))
        self.assertTrue(callable(StructureRef.from_aba))
        self.assertTrue(callable(StructureRef.from_dict))

    def test_db_pair_from_id(self):
        from src.domain.refs.structure_ref import StructureRef
        ref = StructureRef.from_id(99)
        col, val = ref.db_pair()
        self.assertEqual(col, "structure_id")
        self.assertEqual(val, 99)

    def test_db_pair_aba_only(self):
        from src.domain.refs.structure_ref import StructureRef
        ref = StructureRef(aba="PETR4")
        col, val = ref.db_pair()
        self.assertEqual(col, "aba")
        self.assertEqual(val, "PETR4")

    def test_ref_vazio_levanta_value_error(self):
        from src.domain.refs.structure_ref import StructureRef
        with self.assertRaises(ValueError):
            StructureRef()

    def test_is_canonical_com_id(self):
        from src.domain.refs.structure_ref import StructureRef
        self.assertTrue(StructureRef.from_id(1).is_canonical())

    def test_is_canonical_sem_id(self):
        from src.domain.refs.structure_ref import StructureRef
        self.assertFalse(StructureRef(aba="X").is_canonical())


class TestDerivedServiceUnwrapRef(unittest.TestCase):
    """_unwrap_ref() extrai aba de StructureRef ou passa str diretamente."""

    def test_unwrap_structure_ref_com_aba(self):
        from src.domain.refs.structure_ref import StructureRef
        from services.derived_service import _unwrap_ref
        ref = StructureRef(aba="BOVA11")
        self.assertEqual(_unwrap_ref(ref), "BOVA11")

    def test_unwrap_str_direto(self):
        from services.derived_service import _unwrap_ref
        self.assertEqual(_unwrap_ref("PRIO3"), "PRIO3")

    def test_unwrap_none(self):
        from services.derived_service import _unwrap_ref
        self.assertIsNone(_unwrap_ref(None))

    def test_unwrap_ref_sem_aba_retorna_none(self):
        from src.domain.refs.structure_ref import StructureRef
        from services.derived_service import _unwrap_ref
        ref = StructureRef.from_id(42)   # sem aba
        self.assertIsNone(_unwrap_ref(ref))


class TestDerivedServiceImportCanonical(unittest.TestCase):

    def test_nao_redefine_structure_ref(self):
        src = _read("services/derived_service.py")
        self.assertNotIn("class StructureRef", src)

    def test_importa_de_src_domain_refs(self):
        src = _read("services/derived_service.py")
        self.assertIn("src.domain.refs.structure_ref", src)


class TestCanonicalInputServiceImport(unittest.TestCase):

    def test_importa_structure_ref_de_src(self):
        src = _read("services/canonical_input_service.py")
        self.assertIn("src.domain.refs.structure_ref", src)

    def test_resolve_legs_usa_ref_aba(self):
        src = _read("services/canonical_input_service.py")
        self.assertIn("ref.aba", src)

    def test_sem_aba_solta_em_selector_call(self):
        """Garante que o bug 'select(aba)' com aba nao definida foi corrigido."""
        src = _read("services/canonical_input_service.py")
        # a chamada correta e select(aba_str) onde aba_str = ref.aba
        self.assertIn("aba_str", src)
        self.assertIn("self.market_snapshot_selector.select(aba_str)", src)


class TestRoboLegsServiceImport(unittest.TestCase):

    def test_importa_structure_ref_de_src(self):
        src = _read("services/robo_legs_service.py")
        self.assertIn("src.domain.refs.structure_ref", src)

    def test_get_legs_extrai_aba_de_ref(self):
        src = _read("services/robo_legs_service.py")
        self.assertIn("ref.aba", src)

    def test_sem_aba_solta_no_body(self):
        """get_legs nao deve usar 'aba' como variavel nao inicializada."""
        src = _read("services/robo_legs_service.py")
        # depois da correcao, 'aba' e' atribuido explicitamente
        self.assertIn("aba = ref.aba", src)


class TestTmpScriptsRemovidos(unittest.TestCase):
    """Scripts temporarios do patch_53 devem estar fora do inventario principal."""

    TMP_PARA_REMOVER = [
        "scripts/tmp_show_todos_patch53.py",
        "scripts/tmp_fix_todos_patch53b.py",
        "scripts/tmp_verify_patch53b.py",
    ]

    def test_tmp_nao_existem_em_scripts(self):
        for rel in self.TMP_PARA_REMOVER:
            path = ROOT / rel
            self.assertFalse(
                path.exists(),
                f"Script temporario ainda presente: {rel}  -- execute git rm {rel}",
            )

    def test_audit_permanente_existe(self):
        path = ROOT / "scripts" / "74_audit_public_api_aba_surface.py"
        self.assertTrue(path.exists(), "74_audit_public_api_aba_surface.py nao encontrado")


class TestAuditScript74(unittest.TestCase):
    """74_audit_public_api_aba_surface.py executa sem erro."""

    def test_importavel(self):
        spec = importlib.util.spec_from_file_location(
            "audit74",
            ROOT / "scripts" / "74_audit_public_api_aba_surface.py",
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        self.assertTrue(hasattr(mod, "scan_directory"))
        self.assertTrue(hasattr(mod, "classify"))
        self.assertTrue(hasattr(mod, "format_report"))

    def test_scan_nao_levanta_excecao(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "audit74",
            ROOT / "scripts" / "74_audit_public_api_aba_surface.py",
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        reports = mod.scan_directory(ROOT / "services")
        self.assertIsInstance(reports, list)


if __name__ == "__main__":
    unittest.main()
