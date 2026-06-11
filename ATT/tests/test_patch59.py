# ATT/tests/test_patch59.py
"""
Testes formais do patch_59.

Cobre:
  F1+F2 -- format_report usa atributos corretos (file/line/text)
  F1+F2 -- pathlib importado em 74_audit_public_api_aba_surface.py
  F3    -- StructureRef construido antes de _resolve_legs_via_selector
  F4    -- docstring em posicao correta em _resolve_legs_via_selector
  F5    -- meta usa aba_str, nao 'aba'
  F6    -- _fetch_legs nao chama count_legs com id de leg
  F7    -- save_payoff_curve e save_decision recebem ref=, nao aba=
"""

from __future__ import annotations

import ast
import sys
import unittest
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def _ast(rel: str) -> ast.Module:
    src = _read(rel)
    return ast.parse(src, filename=rel)


# ---------------------------------------------------------------------------
# F1+F2 -- 74_audit_public_api_aba_surface.py
# ---------------------------------------------------------------------------

class TestF1FormatReport(unittest.TestCase):
    """format_report deve usar atributos corretos do dataclass AuditEntry."""

    SRC = "scripts/74_audit_public_api_aba_surface.py"

    def test_atributos_corretos_no_format_report(self):
        src = _read(self.SRC)
        self.assertIn("e.file", src,
                      "format_report deve usar 'e.file' (nao e.filepath)")
        self.assertIn("e.line", src,
                      "format_report deve usar 'e.line' (nao e.lineno)")
        self.assertIn("e.text", src,
                      "format_report deve usar 'e.text' (nao e.line_text)")

    def test_atributos_errados_ausentes(self):
        src = _read(self.SRC)
        self.assertNotIn("e.filepath", src,
                         "atributo 'e.filepath' nao existe em AuditEntry")
        self.assertNotIn("e.lineno", src,
                         "atributo 'e.lineno' nao existe em AuditEntry")
        self.assertNotIn("e.line_text", src,
                         "atributo 'e.line_text' nao existe em AuditEntry")


class TestF2PathlibImportado(unittest.TestCase):
    """pathlib deve estar importado no modulo."""

    SRC = "scripts/74_audit_public_api_aba_surface.py"

    def test_import_pathlib_presente(self):
        src = _read(self.SRC)
        self.assertIn("import pathlib", src,
                      "'import pathlib' deve estar presente no modulo")


class TestF1FormatReportFuncional(unittest.TestCase):
    """format_report deve executar sem AttributeError."""

    def test_format_report_executa(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "audit74",
            str(ROOT / "scripts/74_audit_public_api_aba_surface.py"),
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        AuditEntry = mod.AuditEntry
        entry = AuditEntry(
            file="services/derived_service.py",
            line=42,
            text="    aba_str = ref.aba",
            classification="READY",
        )
        result = mod.format_report([entry])
        self.assertIn("READY", result)
        self.assertIn("42", result)
        self.assertIn("derived_service.py", result)


# ---------------------------------------------------------------------------
# F3 -- canonical_input_service.py: StructureRef construido antes do selector
# ---------------------------------------------------------------------------

class TestF3StructureRefAntesSeletor(unittest.TestCase):

    SRC = "services/canonical_input_service.py"

    def test_from_aba_presente_antes_de_resolve_legs(self):
        src = _read(self.SRC)
        idx_from_aba = src.find("StructureRef.from_aba(aba)")
        idx_selector = src.find("_resolve_legs_via_selector(ref)")
        self.assertGreater(idx_from_aba, 0,
                           "StructureRef.from_aba(aba) deve estar presente")
        self.assertGreater(idx_selector, 0,
                           "_resolve_legs_via_selector(ref) deve estar presente")
        self.assertLess(idx_from_aba, idx_selector,
                        "StructureRef.from_aba deve aparecer antes de _resolve_legs_via_selector")


# ---------------------------------------------------------------------------
# F4 -- canonical_input_service.py: docstring na posicao correta
# ---------------------------------------------------------------------------

class TestF4DocstringPosicao(unittest.TestCase):

    SRC = "services/canonical_input_service.py"

    def test_aba_str_apos_docstring(self):
        src = _read(self.SRC)
        # aba_str = ref.aba deve vir DEPOIS da docstring do metodo
        idx_docstring_open = src.find(
            'def _resolve_legs_via_selector'
        )
        self.assertGreater(idx_docstring_open, 0)

        bloco = src[idx_docstring_open:]
        idx_triple = bloco.find('"""')
        idx_aba_str = bloco.find("aba_str = ref.aba")

        self.assertGreater(idx_triple, 0,
                           "Docstring deve estar presente em _resolve_legs_via_selector")
        self.assertGreater(idx_aba_str, idx_triple,
                           "aba_str = ref.aba deve aparecer APOS a docstring")


# ---------------------------------------------------------------------------
# F5 -- canonical_input_service.py: meta usa aba_str
# ---------------------------------------------------------------------------

class TestF5MetaUsaAbaStr(unittest.TestCase):

    SRC = "services/canonical_input_service.py"

    def test_snapshot_aba_usa_aba_str(self):
        src = _read(self.SRC)
        self.assertIn('"snapshot_aba":     aba_str', src,
                      "meta deve usar 'aba_str', nao 'aba' (NameError)")

    def test_snapshot_aba_nao_usa_aba_solto(self):
        src = _read(self.SRC)
        # Garante que nao existe a forma errada
        self.assertNotIn('"snapshot_aba":     aba,', src,
                         "'snapshot_aba': aba seria NameError no escopo")


# ---------------------------------------------------------------------------
# F6 -- structures_repository.py: _fetch_legs sem count_legs(leg_id)
# ---------------------------------------------------------------------------

class TestF6FetchLegsCountLegs(unittest.TestCase):

    SRC = "repositories/structures_repository.py"

    def test_count_legs_nao_usa_id_de_leg(self):
        src = _read(self.SRC)
        # O padrao errado era: self.count_legs(d["id"]) dentro de _fetch_legs
        # Buscamos o bloco de _fetch_legs e garantimos que o padrao nao existe
        inicio = src.find("def _fetch_legs(")
        fim = src.find("\n    def ", inicio + 1)
        bloco = src[inicio:fim] if fim > 0 else src[inicio:]
        self.assertNotIn('self.count_legs(d["id"])', bloco,
                         "_fetch_legs nao deve chamar count_legs com id da leg")

    def test_count_legs_ainda_existe_no_modulo(self):
        src = _read(self.SRC)
        self.assertIn("def count_legs(", src,
                      "metodo count_legs deve continuar existindo")


# ---------------------------------------------------------------------------
# F7 -- derived_service.py: kwarg ref= (nao aba=)
# ---------------------------------------------------------------------------

class TestF7DerivedServiceKwarg(unittest.TestCase):
    """F7: save_payoff_curve e save_decision devem receber ref=storage_key."""

    @staticmethod
    def _get_func_block(src: str, func_name: str) -> str:
        """Extrai o corpo completo da funcao ate a proxima def de modulo."""
        start = src.find(f"def {func_name}(")
        if start == -1:
            return ""
        # Proxima 'def ' no nivel de modulo (coluna 0)
        m = re.search(r'\ndef [a-zA-Z_]', src[start + 1:])
        end = (start + 1 + m.start()) if m else len(src)
        return src[start:end]

    def _src(self) -> str:
        return (ROOT / "services/derived_service.py").read_text(encoding="utf-8")

    def test_save_payoff_curve_usa_ref_kwarg(self):
        bloco = self._get_func_block(self._src(), "save_payoff_from_canonical_payload")
        self.assertIn(
            "ref=storage_key",
            bloco,
            "save_payoff_curve deve ser chamada com ref=storage_key",
        )

    def test_save_decision_usa_ref_kwarg(self):
        bloco = self._get_func_block(self._src(), "save_decision_from_canonical_payload")
        self.assertIn(
            "ref=storage_key",
            bloco,
            "save_decision deve ser chamada com ref=storage_key",
        )


class TestPatch59SintaxeArquivos(unittest.TestCase):
    """Todos os arquivos corrigidos devem ser validos sintaticamente."""

    ARQUIVOS = [
        "scripts/74_audit_public_api_aba_surface.py",
        "services/canonical_input_service.py",
        "repositories/structures_repository.py",
        "services/derived_service.py",
    ]

    def test_sintaxe_valida(self):
        for rel in self.ARQUIVOS:
            with self.subTest(arquivo=rel):
                src = _read(rel)
                try:
                    ast.parse(src, filename=rel)
                except SyntaxError as exc:
                    self.fail(f"SyntaxError em {rel}: {exc}")

if __name__ == "__main__":
    unittest.main(verbosity=2)
