# C:/users/eucal/projeto/ATT/tests/test_patch37_residuals.py
"""
patch_37 — Testes de remoção de resíduos aba/abas
Verifica que:
  - _cache_abas (property + setter) foi removido de UIDataModel
  - get_abas() foi removido de UIDataModel
  - update_abas() foi removido de FiltersPanel
  - main_window não chama mais update_abas() nem get_abas()
  - get_structures() e get_structure_ids() funcionam corretamente
  - Nenhuma regressão nos métodos canônicos do patch_34/patch_3a
"""

import ast
import sys
import pytest
from pathlib import Path
from unittest.mock import patch

# ---------------------------------------------------------------------------
# Raiz do projeto e caminhos dos arquivos-alvo
# ---------------------------------------------------------------------------

ROOT         = Path("C:/users/eucal/projeto")
UI_DATA_PATH = ROOT / "UI" / "models"     / "ui_data.py"
FILTERS_PATH = ROOT / "UI" / "components" / "filters_panel.py"
MAIN_WIN_PATH= ROOT / "UI"               / "main_window.py"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_source(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _parse_ast(path: Path) -> ast.Module:
    return ast.parse(_load_source(path), filename=str(path))


def _all_method_names(tree: ast.Module, class_name: str) -> list[str]:
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            return [
                n.name
                for n in ast.walk(node)
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
            ]
    return []


# ===========================================================================
# BLOCO 1 — Análise estática: resíduos removidos de ui_data.py
# ===========================================================================

class TestPatch37StaticUIData:

    def setup_method(self):
        self.tree = _parse_ast(UI_DATA_PATH)
        self.src  = _load_source(UI_DATA_PATH)

    # --- _cache_abas --------------------------------------------------------

    def test_no_cache_abas_property(self):
        """@property _cache_abas não deve existir em UIDataModel."""
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef) and node.name == "UIDataModel":
                for item in ast.walk(node):
                    if isinstance(item, ast.FunctionDef) and item.name == "_cache_abas":
                        decorators = [
                            d.id if isinstance(d, ast.Name) else
                            (d.attr if isinstance(d, ast.Attribute) else "")
                            for d in item.decorator_list
                        ]
                        assert "property" not in decorators, (
                            "@property _cache_abas ainda presente em UIDataModel"
                        )

    def test_no_cache_abas_setter(self):
        """@_cache_abas.setter não deve existir."""
        assert "@_cache_abas.setter" not in self.src, (
            "@_cache_abas.setter ainda presente em ui_data.py"
        )

    def test_no_cache_abas_self_reference(self):
        """self._cache_abas não deve ser referenciado."""
        assert "self._cache_abas" not in self.src, (
            "self._cache_abas ainda referenciado em ui_data.py"
        )

    # --- get_abas -----------------------------------------------------------

    def test_no_get_abas_method(self):
        """get_abas() não deve existir em UIDataModel."""
        methods = _all_method_names(self.tree, "UIDataModel")
        assert "get_abas" not in methods, (
            "get_abas() ainda presente em UIDataModel"
        )

    def test_no_get_abas_any_reference(self):
        """Nenhuma referência textual a get_abas no arquivo."""
        assert "get_abas" not in self.src, (
            "Referência a get_abas ainda encontrada em ui_data.py"
        )

    # --- Métodos canônicos presentes ----------------------------------------

    def test_get_structure_ids_present(self):
        """get_structure_ids() deve existir (método canônico patch_34)."""
        methods = _all_method_names(self.tree, "UIDataModel")
        assert "get_structure_ids" in methods, (
            "get_structure_ids() não encontrado em UIDataModel"
        )

    def test_get_structures_present(self):
        """get_structures() deve existir (alias de compatibilidade)."""
        methods = _all_method_names(self.tree, "UIDataModel")
        assert "get_structures" in methods, (
            "get_structures() não encontrado em UIDataModel"
        )

    def test_cache_structures_in_source(self):
        """_cache_structures deve estar presente no arquivo."""
        assert "self._cache_structures" in self.src, (
            "self._cache_structures não encontrado em ui_data.py"
        )


# ===========================================================================
# BLOCO 2 — Análise estática: resíduos removidos de filters_panel.py
# ===========================================================================

class TestPatch37StaticFiltersPanel:

    def setup_method(self):
        self.src  = _load_source(FILTERS_PATH)
        self.tree = _parse_ast(FILTERS_PATH)

    def test_no_update_abas_method(self):
        """update_abas() não deve existir em nenhuma classe de filters_panel."""
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                methods = [
                    n.name for n in ast.walk(node)
                    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                ]
                assert "update_abas" not in methods, (
                    f"update_abas() ainda presente na classe {node.name} "
                    f"em filters_panel.py"
                )

    def test_no_update_abas_reference(self):
        """Nenhuma referência textual a update_abas em filters_panel."""
        assert "update_abas" not in self.src, (
            "Referência a update_abas ainda em filters_panel.py"
        )


# ===========================================================================
# BLOCO 3 — Análise estática: main_window.py limpo
# ===========================================================================

class TestPatch37StaticMainWindow:

    def setup_method(self):
        self.src = _load_source(MAIN_WIN_PATH)

    def test_no_update_abas_call(self):
        """main_window não deve chamar update_abas()."""
        assert "update_abas" not in self.src, (
            "Chamada a update_abas() ainda presente em main_window.py"
        )

    def test_no_get_abas_call(self):
        """main_window não deve chamar get_abas()."""
        assert "get_abas" not in self.src, (
            "Chamada a get_abas() ainda presente em main_window.py"
        )

    def test_no_cache_abas_reference(self):
        """main_window não deve referenciar _cache_abas."""
        assert "_cache_abas" not in self.src, (
            "Referência a _cache_abas ainda presente em main_window.py"
        )


# ===========================================================================
# BLOCO 4 — Testes funcionais com mock de DB
# ===========================================================================

@pytest.fixture
def model(tmp_path):
    """UIDataModel com derived.db mínimo em memória."""
    import sqlite3

    db_path = tmp_path / "derived.db"
    conn = sqlite3.connect(str(db_path))
    conn.execute("""
        CREATE TABLE structure_decisions (
            timestamp       TEXT,
            structure_id    INTEGER,
            aba             TEXT,
            decision        TEXT,
            level           INTEGER,
            pl_pct_of_max   REAL,
            dte_min         INTEGER,
            why             TEXT,
            why_json        TEXT,
            pl_atual        REAL,
            pl_max          REAL,
            spot_ref        REAL
        )
    """)
    conn.executemany(
        "INSERT INTO structure_decisions VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
        [
            ("2026-01-01 10:00:00", 7, "PETR4", "HOLD", 2, 0.75, 10, None, None, 100.0, 200.0, 50.0),
            ("2026-01-02 10:00:00", 8, "VALE3", "EXIT", 3, 0.90,  5, None, None, 150.0, 180.0, 60.0),
        ]
    )
    conn.commit()
    conn.close()

    sys.path.insert(0, str(ROOT))
    with patch("UI.models.ui_data.DERIVED_DB_PATH", str(db_path)):
        from UI.models.ui_data import UIDataModel
        m = UIDataModel(derived_db_path=db_path)
        m.refresh()
        yield m


class TestPatch37Functional:

    def test_get_structures_returns_list(self, model):
        """get_structures() retorna lista não-vazia após refresh()."""
        result = model.get_structures()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_get_structure_ids_matches_get_structures(self, model):
        """get_structure_ids() e get_structures() devem retornar os mesmos valores."""
        assert sorted(model.get_structures()) == sorted(model.get_structure_ids())

    def test_get_structure_ids_contains_expected(self, model):
        """IDs 7 e 8 devem estar presentes."""
        ids = model.get_structure_ids()
        assert "7" in ids or 7 in ids
        assert "8" in ids or 8 in ids

    def test_no_cache_abas_attribute(self, model):
        """_cache_abas não deve existir como atributo de instância."""
        assert not hasattr(model, "_cache_abas")

    def test_no_get_abas_method(self, model):
        """get_abas() não deve existir no objeto."""
        assert not hasattr(model, "get_abas")

    def test_get_decisions_aba_filter_no_crash(self, model):
        """get_decisions(aba=) não deve lançar exceção."""
        result = model.get_decisions(filters={"aba": "PETR4"})
        assert isinstance(result, list)

    def test_get_decisions_structure_id_filter(self, model):
        """get_decisions(structure_id=7) retorna exatamente 1 linha."""
        result = model.get_decisions(filters={"structure_id": 7})
        assert len(result) == 1
        assert result[0]["structure_id"] == 7

    def test_cache_structures_is_list(self, model):
        """_cache_structures é list após refresh()."""
        assert isinstance(model._cache_structures, list)

    def test_clear_cache_resets_structures(self, model):
        """clear_cache() zera _cache_structures."""
        model.clear_cache()
        assert model._cache_structures == []

    def test_lazy_load_after_clear(self, model):
        """get_structure_ids() recarrega após clear_cache()."""
        model.clear_cache()
        ids = model.get_structure_ids()
        assert len(ids) > 0


# ===========================================================================
# BLOCO 5 — Não-regressão patch_34 / patch_3a
# ===========================================================================

class TestPatch37NoRegression:

    def setup_method(self):
        self.src_ui   = _load_source(UI_DATA_PATH)
        self.src_main = _load_source(MAIN_WIN_PATH)

    def test_structure_filter_col_canonical(self):
        """_structure_filter_col deve usar structure_id."""
        assert "_structure_filter_col" in self.src_ui

    def test_resolve_structure_key_present(self):
        """_resolve_structure_key deve existir (patch_34)."""
        assert "_resolve_structure_key" in self.src_ui

    def test_patch_3a_aba_filter_preserved(self):
        """Filtro aba (patch_3a) deve existir em get_decisions()."""
        assert 'filters.get("aba")' in self.src_ui or \
               "filters.get('aba')"  in self.src_ui

    def test_update_structures_in_main_window(self):
        """update_structures() não deve ter sido removido de main_window."""
        assert "update_structures" in self.src_main
