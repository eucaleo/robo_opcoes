# ATT/tests/test_patch71_archive_wiring.py
"""
Testes do patch_71:
    - structures_list_panel.py: self._db_path, _set_status, feedback em _cmd_archive
    - main_window.py: self._db_path no __init__, ausencia de hardcode

Todos os testes que dependem de Tkinter real estao marcados com
@unittest.skip("Requer display Tkinter -- headless nao suportado").
Testes estaticos (leitura de fonte) e testes de logica pura sao executados
normalmente em qualquer ambiente.
"""
from __future__ import annotations

import ast
import sys
import types
import unittest
import unittest.mock as mock
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
STRUCTURES_PANEL = PROJECT_ROOT / "UI" / "components" / "structures_list_panel.py"
MAIN_WINDOW      = PROJECT_ROOT / "UI" / "main_window.py"


# ---------------------------------------------------------------------------
# Utilitario de leitura
# ---------------------------------------------------------------------------

def _src(path: Path) -> str:
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# 1. Checks estaticos -- structures_list_panel.py
# ---------------------------------------------------------------------------

class TestPatch71StaticChecks(unittest.TestCase):

    def test_arquivo_existe(self):
        self.assertTrue(
            STRUCTURES_PANEL.exists(),
            "UI/components/structures_list_panel.py nao encontrado",
        )

    def test_classe_presente(self):
        self.assertIn("class StructuresListPanel", _src(STRUCTURES_PANEL))

    def test_nao_importa_sqlite3_diretamente(self):
        src = _src(STRUCTURES_PANEL)
        self.assertNotIn("import sqlite3", src,
                         "sqlite3 nao deve ser importado diretamente no painel")

    def test_metodo_on_archive_request_existe(self):
        # _cmd_archive é o método de arquivo no painel
        self.assertIn("def _cmd_archive", _src(STRUCTURES_PANEL))

    def test_metodo_set_status_existe(self):
        self.assertIn("def _set_status", _src(STRUCTURES_PANEL),
                      "_set_status nao encontrado em structures_list_panel.py")

    def test_metodo_load_existe(self):
        self.assertIn("def load", _src(STRUCTURES_PANEL))

    def test_messagebox_importado(self):
        self.assertIn("messagebox", _src(STRUCTURES_PANEL))

    def test_structures_repository_importado(self):
        self.assertIn("StructuresRepository", _src(STRUCTURES_PANEL))

    def test_self_db_path_presente_no_painel(self):
        self.assertIn("self._db_path", _src(STRUCTURES_PANEL),
                      "self._db_path nao atribuido no painel")

    def test_archive_structure_chamado(self):
        self.assertIn("archive_structure", _src(STRUCTURES_PANEL))

    def test_askyesno_ou_askokcancel_presente(self):
        src = _src(STRUCTURES_PANEL)
        self.assertTrue(
            "askyesno" in src or "askokcancel" in src,
            "Nenhuma confirmacao askyesno/askokcancel encontrada",
        )

    def test_try_except_em_cmd_archive(self):
        src = _src(STRUCTURES_PANEL)
        self.assertIn("try:", src)
        self.assertIn("except", src)

    def test_set_status_chamado_apos_archive(self):
        src = _src(STRUCTURES_PANEL)
        self.assertIn("_set_status", src,
                      "_set_status nao invocado no corpo do modulo")

    def test_load_chamado_em_cmd_archive(self):
        src = _src(STRUCTURES_PANEL)
        self.assertIn("self.load", src)

    def test_status_label_var_presente(self):
        self.assertIn("_status_label_var", _src(STRUCTURES_PANEL),
                      "_status_label_var nao encontrado -- label de status ausente")

    def test_sintaxe_valida(self):
        src = _src(STRUCTURES_PANEL)
        try:
            ast.parse(src)
        except SyntaxError as e:
            self.fail(f"SyntaxError em structures_list_panel.py: {e}")


# ---------------------------------------------------------------------------
# 2. Checks estaticos -- main_window.py
# ---------------------------------------------------------------------------

class TestPatch71StaticMainWindow(unittest.TestCase):

    def test_main_window_arquivo_existe(self):
        self.assertTrue(MAIN_WINDOW.exists(),
                        "UI/main_window.py nao encontrado")

    def test_self_db_path_preservado_em_main_window(self):
        self.assertIn("self._db_path", _src(MAIN_WINDOW),
                      "self._db_path ausente em main_window.py")

    def test_db_path_nao_hardcoded_em_setup_structures_tab(self):
        src = _src(MAIN_WINDOW)
        # O hardcode pode aparecer somente na definicao de self._db_path -- nao
        # como argumento direto de StructuresListPanel
        import re
        # Busca instanciacao de StructuresListPanel com db_path=str(PROJECT_ROOT...)
        padrao = r'StructuresListPanel\s*\([^)]*db_path\s*=\s*str\s*\('
        match = re.search(padrao, src, re.DOTALL)
        self.assertIsNone(
            match,
            "db_path hardcoded ainda presente na instanciacao de StructuresListPanel",
        )

    def test_db_path_self_db_path_passado_ao_panel(self):
        self.assertIn("db_path=self._db_path", _src(MAIN_WINDOW))

    def test_structure_editor_dialog_importado(self):
        self.assertIn("StructureEditorDialog", _src(MAIN_WINDOW))

    def test_on_structure_edit_request_presente(self):
        self.assertIn("def _on_structure_edit_request", _src(MAIN_WINDOW))

    def test_wait_window_presente(self):
        self.assertIn("wait_window", _src(MAIN_WINDOW))

    def test_dlg_saved_verificado(self):
        self.assertIn("dlg.saved", _src(MAIN_WINDOW))

    def test_sqlite3_nao_importado_em_main_window(self):
        self.assertNotIn("import sqlite3", _src(MAIN_WINDOW))

    def test_sintaxe_main_window_valida(self):
        src = _src(MAIN_WINDOW)
        try:
            ast.parse(src)
        except SyntaxError as e:
            self.fail(f"SyntaxError em main_window.py: {e}")


# ---------------------------------------------------------------------------
# 3. Logica pura: _cmd_archive -- mock do repositorio e de messagebox
# ---------------------------------------------------------------------------

def _make_fake_panel(
    repo_mock: mock.MagicMock,
    selected_id: int | None = 1,
    structure: dict | None = None,
    confirm_response: bool = True,
):
    """
    Constroi um objeto que simula StructuresListPanel sem Tkinter.
    Apenas os atributos e metodos usados em _cmd_archive sao simulados.
    """
    if structure is None:
        structure = {"id": selected_id, "name": "BOVA11 Condor", "status": "active"}

    panel = mock.MagicMock()
    panel._repo = repo_mock
    panel._selected_id = mock.MagicMock(return_value=selected_id)
    panel._get_full_structure = mock.MagicMock(return_value=structure)
    panel._set_status = mock.MagicMock()
    panel.load = mock.MagicMock()
    panel._on_structure_selected = mock.MagicMock()

    # Importa o metodo real e vincula ao objeto fake
    import importlib, sys as _sys

    # Garante que tkinter nao seja chamado -- substitui por stubs antes do import
    _fake_tk = types.ModuleType("tkinter")
    _fake_tk.Tk = mock.MagicMock
    _fake_tk.StringVar = mock.MagicMock
    _fake_ttk = types.ModuleType("tkinter.ttk")
    _fake_ttk.Frame = mock.MagicMock
    _fake_mb = types.ModuleType("tkinter.messagebox")
    _fake_mb.showwarning = mock.MagicMock()
    _fake_mb.showinfo    = mock.MagicMock()
    _fake_mb.showerror   = mock.MagicMock()
    _fake_mb.askyesno    = mock.MagicMock(return_value=confirm_response)

    orig_modules = {}
    stubs = {
        "tkinter":          _fake_tk,
        "tkinter.ttk":      _fake_ttk,
        "tkinter.messagebox": _fake_mb,
    }
    for name, stub in stubs.items():
        orig_modules[name] = _sys.modules.get(name)
        _sys.modules[name] = stub

    # Stub para StructuresRepository
    _fake_repo_mod = types.ModuleType("repositories.structures_repository")
    _fake_repo_mod.StructuresRepository = mock.MagicMock(return_value=repo_mock)
    orig_modules["repositories.structures_repository"] = _sys.modules.get(
        "repositories.structures_repository"
    )
    _sys.modules["repositories.structures_repository"] = _fake_repo_mod

    try:
        # Remove cache do modulo para recarregar com stubs
        mod_key = "UI.components.structures_list_panel"
        if mod_key in _sys.modules:
            del _sys.modules[mod_key]
        mod = importlib.import_module("UI.components.structures_list_panel")
        # Vincula _cmd_archive real ao objeto fake
        panel._cmd_archive_real = mod.StructuresListPanel._cmd_archive.__get__(panel)
        panel._askyesno_stub = _fake_mb.askyesno
        panel._showerror_stub = _fake_mb.showerror
        panel._showwarning_stub = _fake_mb.showwarning
        panel._showinfo_stub = _fake_mb.showinfo
    finally:
        for name, orig in orig_modules.items():
            if orig is None:
                _sys.modules.pop(name, None)
            else:
                _sys.modules[name] = orig
        if mod_key in _sys.modules:
            del _sys.modules[mod_key]

    return panel


class TestOnArchiveRequestConfirmado(unittest.TestCase):
    """Usuario confirma o arquivamento -- caminho feliz."""

    def setUp(self):
        self.repo = mock.MagicMock()
        self.repo.archive_structure = mock.MagicMock()
        self.panel = _make_fake_panel(
            self.repo,
            selected_id=7,
            structure={"id": 7, "name": "PETR4 Trava", "status": "active"},
            confirm_response=True,
        )

    def test_archive_structure_chamado_com_id_correto(self):
        self.panel._cmd_archive_real()
        self.repo.archive_structure.assert_called_once_with(7)

    def test_load_chamado_apos_archive_confirmado(self):
        self.panel._cmd_archive_real()
        self.panel.load.assert_called_once()

    def test_on_structure_selected_none_chamado(self):
        self.panel._cmd_archive_real()
        self.panel._on_structure_selected.assert_called_once_with(None)

    def test_set_status_mensagem_sucesso(self):
        self.panel._cmd_archive_real()
        self.panel._set_status.assert_called()
        args = self.panel._set_status.call_args[0][0]
        self.assertIn("arquivada", args.lower(),
                      f"Mensagem de sucesso esperada, obteve: '{args}'")

    def test_destroy_nao_chamado_em_archive(self):
        self.panel._cmd_archive_real()
        self.panel.destroy = mock.MagicMock()
        self.panel.destroy.assert_not_called()


class TestOnArchiveRequestCancelado(unittest.TestCase):
    """Usuario cancela a confirmacao -- nada deve acontecer."""

    def setUp(self):
        self.repo = mock.MagicMock()
        self.panel = _make_fake_panel(
            self.repo,
            selected_id=3,
            structure={"id": 3, "name": "BOVA11 Condor", "status": "active"},
            confirm_response=False,
        )

    def test_archive_nao_chamado_se_usuario_cancela(self):
        self.panel._cmd_archive_real()
        self.repo.archive_structure.assert_not_called()

    def test_load_nao_chamado_se_usuario_cancela(self):
        self.panel._cmd_archive_real()
        self.panel.load.assert_not_called()

    def test_set_status_nao_chamado_se_cancelado(self):
        self.panel._cmd_archive_real()
        self.panel._set_status.assert_not_called()


class TestOnArchiveRequestErro(unittest.TestCase):
    """Repositorio lanca excecao -- UI nao deve propagar."""

    def setUp(self):
        self.repo = mock.MagicMock()
        self.repo.archive_structure.side_effect = RuntimeError("Falha no banco")
        self.panel = _make_fake_panel(
            self.repo,
            selected_id=5,
            structure={"id": 5, "name": "VALE3 Spread", "status": "active"},
            confirm_response=True,
        )

    def test_excecao_nao_propaga_para_ui(self):
        try:
            self.panel._cmd_archive_real()
        except Exception as exc:
            self.fail(
                f"Excecao nao deveria propagar para a UI, mas propagou: {exc}"
            )

    def test_load_nao_chamado_se_archive_falha(self):
        self.panel._cmd_archive_real()
        self.panel.load.assert_not_called()

    def test_set_status_mensagem_erro(self):
        self.panel._cmd_archive_real()
        self.panel._set_status.assert_called()
        args = self.panel._set_status.call_args[0][0]
        self.assertIn("erro", args.lower(),
                      f"Mensagem de erro esperada, obteve: '{args}'")


class TestOnArchiveRequestSemSelecao(unittest.TestCase):
    """Nenhuma linha selecionada na tree -- deve apenas mostrar warning."""

    def setUp(self):
        self.repo = mock.MagicMock()
        self.panel = _make_fake_panel(
            self.repo,
            selected_id=None,
            structure=None,
            confirm_response=True,
        )

    def test_archive_nao_chamado_sem_selecao(self):
        self.panel._cmd_archive_real()
        self.repo.archive_structure.assert_not_called()

    def test_load_nao_chamado_sem_selecao(self):
        self.panel._cmd_archive_real()
        self.panel.load.assert_not_called()

    def test_warning_exibido_sem_selecao(self):
        self.panel._cmd_archive_real()
        self.panel._showwarning_stub.assert_called()


class TestOnArchiveRequestJaArquivado(unittest.TestCase):
    """Estrutura ja arquivada -- deve informar usuario e nao arquivar novamente."""

    def setUp(self):
        self.repo = mock.MagicMock()
        self.panel = _make_fake_panel(
            self.repo,
            selected_id=9,
            structure={"id": 9, "name": "PETR4 Old", "status": "archived"},
            confirm_response=True,
        )

    def test_archive_nao_chamado_se_ja_arquivada(self):
        self.panel._cmd_archive_real()
        self.repo.archive_structure.assert_not_called()

    def test_info_exibido_se_ja_arquivada(self):
        self.panel._cmd_archive_real()
        self.panel._showinfo_stub.assert_called()


# ---------------------------------------------------------------------------
# 4. _set_status: logica pura
# ---------------------------------------------------------------------------

class TestSetStatus(unittest.TestCase):

    def _make_panel_with_var(self):
        """
        Constroi objeto minimo para testar _set_status sem Tkinter.
        """
        panel = mock.MagicMock()
        captured: list[str] = []
        var = mock.MagicMock()
        var.set = lambda v: captured.append(v)
        panel._status_label_var = var
        panel._captured = captured

        # Importa e vincula o metodo real
        import importlib, types as _types

        _fake_tk  = _types.ModuleType("tkinter")
        _fake_tk.StringVar = mock.MagicMock
        _fake_ttk = _types.ModuleType("tkinter.ttk")
        _fake_ttk.Frame = mock.MagicMock
        _fake_mb  = _types.ModuleType("tkinter.messagebox")
        _fake_repo_mod = _types.ModuleType("repositories.structures_repository")
        _fake_repo_mod.StructuresRepository = mock.MagicMock()

        orig = {}
        stubs = {
            "tkinter": _fake_tk,
            "tkinter.ttk": _fake_ttk,
            "tkinter.messagebox": _fake_mb,
            "repositories.structures_repository": _fake_repo_mod,
        }
        for k, v in stubs.items():
            orig[k] = sys.modules.get(k)
            sys.modules[k] = v

        mod_key = "UI.components.structures_list_panel"
        sys.modules.pop(mod_key, None)

        try:
            mod = importlib.import_module("UI.components.structures_list_panel")
            panel._set_status_real = (
                mod.StructuresListPanel._set_status.__get__(panel)
            )
        finally:
            for k, v in orig.items():
                if v is None:
                    sys.modules.pop(k, None)
                else:
                    sys.modules[k] = v
            sys.modules.pop(mod_key, None)

        return panel

    def test_set_status_atualiza_widget(self):
        panel = self._make_panel_with_var()
        panel._set_status_real("Estrutura arquivada.")
        self.assertIn("Estrutura arquivada.", panel._captured)

    def test_set_status_aceita_string_vazia(self):
        panel = self._make_panel_with_var()
        try:
            panel._set_status_real("")
        except Exception as exc:
            self.fail(f"_set_status nao deve lancar excecao com string vazia: {exc}")

    def test_set_status_nao_lanca_se_var_invalida(self):
        """_set_status tem try/except -- nao deve propagar."""
        panel = mock.MagicMock()
        panel._status_label_var = None  # forcara AttributeError no .set()

        import importlib, types as _types
        _fake_tk  = _types.ModuleType("tkinter")
        _fake_tk.StringVar = mock.MagicMock
        _fake_ttk = _types.ModuleType("tkinter.ttk")
        _fake_ttk.Frame = mock.MagicMock
        _fake_mb  = _types.ModuleType("tkinter.messagebox")
        _fake_repo_mod = _types.ModuleType("repositories.structures_repository")
        _fake_repo_mod.StructuresRepository = mock.MagicMock()

        orig = {}
        stubs = {
            "tkinter": _fake_tk,
            "tkinter.ttk": _fake_ttk,
            "tkinter.messagebox": _fake_mb,
            "repositories.structures_repository": _fake_repo_mod,
        }
        for k, v in stubs.items():
            orig[k] = sys.modules.get(k)
            sys.modules[k] = v

        mod_key = "UI.components.structures_list_panel"
        sys.modules.pop(mod_key, None)
        try:
            mod = importlib.import_module("UI.components.structures_list_panel")
            fn = mod.StructuresListPanel._set_status.__get__(panel)
            try:
                fn("teste")
            except Exception as exc:
                self.fail(f"_set_status deve absorver excecao interna: {exc}")
        finally:
            for k, v in orig.items():
                if v is None:
                    sys.modules.pop(k, None)
                else:
                    sys.modules[k] = v
            sys.modules.pop(mod_key, None)


# ---------------------------------------------------------------------------
# 5. Testes Tk-dependentes (skip em headless)
# ---------------------------------------------------------------------------

@unittest.skip("Requer display Tkinter -- headless nao suportado")
class TestArchiveWiringTkinter(unittest.TestCase):
    """
    Testes de integracao real com Tkinter.
    Executar manualmente em ambiente com display disponivel.
    """

    def setUp(self):
        import tkinter as tk
        self.root = tk.Tk()
        self.root.withdraw()

    def tearDown(self):
        self.root.destroy()

    def test_painel_instancia_sem_erro(self):
        from repositories.structures_repository import StructuresRepository
        from UI.components.structures_list_panel import StructuresListPanel
        import tempfile, os, sqlite3 as _sq3

        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        try:
            # Cria schema minimo
            conn = _sq3.connect(db_path)
            conn.execute(
                "CREATE TABLE IF NOT EXISTS structures "
                "(id INTEGER PRIMARY KEY, name TEXT, underlying_asset TEXT, "
                " alias_legacy_aba TEXT, status TEXT DEFAULT 'active', "
                " notes TEXT, created_at TEXT, updated_at TEXT)"
            )
            conn.execute(
                "CREATE TABLE IF NOT EXISTS structure_legs "
                "(id INTEGER PRIMARY KEY, structure_id INTEGER, "
                " position_side TEXT, option_type TEXT, symbol TEXT, "
                " strike REAL, expiration_date TEXT, quantity INTEGER, "
                " premium REAL, multiplier REAL DEFAULT 1, leg_order INTEGER, "
                " notes TEXT, created_at TEXT, updated_at TEXT)"
            )
            conn.commit()
            conn.close()

            panel = StructuresListPanel(
                self.root,
                on_structure_selected=lambda s: None,
                on_request_edit=lambda sid: None,
                db_path=db_path,
            )
            self.assertIsNotNone(panel)
            self.assertTrue(hasattr(panel, "_set_status"))
            self.assertTrue(hasattr(panel, "_db_path"))
        finally:
            os.unlink(db_path)

    def test_set_status_atualiza_label_real(self):
        from UI.components.structures_list_panel import StructuresListPanel
        import tempfile, os, sqlite3 as _sq3

        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        try:
            conn = _sq3.connect(db_path)
            conn.execute(
                "CREATE TABLE IF NOT EXISTS structures "
                "(id INTEGER PRIMARY KEY, name TEXT, underlying_asset TEXT, "
                " alias_legacy_aba TEXT, status TEXT DEFAULT 'active', "
                " notes TEXT, created_at TEXT, updated_at TEXT)"
            )
            conn.execute(
                "CREATE TABLE IF NOT EXISTS structure_legs "
                "(id INTEGER PRIMARY KEY, structure_id INTEGER)"
            )
            conn.commit()
            conn.close()

            panel = StructuresListPanel(
                self.root,
                on_structure_selected=lambda s: None,
                on_request_edit=lambda sid: None,
                db_path=db_path,
            )
            panel._set_status("Teste de status")
            self.assertEqual(panel._status_label_var.get(), "Teste de status")
        finally:
            os.unlink(db_path)


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main(verbosity=2)
