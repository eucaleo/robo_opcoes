import importlib
import sys
import types

import pytest


def _install_dark_panel_import_stubs():
    ctk = types.ModuleType("customtkinter")

    class DummyWidget:
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs

        def configure(self, **kwargs):
            self.kwargs.update(kwargs)

        def pack(self, *args, **kwargs):
            return None

        def grid(self, *args, **kwargs):
            return None

        def destroy(self):
            return None

        def insert(self, *args, **kwargs):
            return None

        def delete(self, *args, **kwargs):
            return None

        def winfo_children(self):
            return []

        def winfo_toplevel(self):
            raise RuntimeError("tk indisponivel no teste")

    class DummyFont:
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs

    ctk.CTkFrame = DummyWidget
    ctk.CTkLabel = DummyWidget
    ctk.CTkButton = DummyWidget
    ctk.CTkTextbox = DummyWidget
    ctk.CTkScrollableFrame = DummyWidget
    ctk.CTkFont = DummyFont

    sys.modules["customtkinter"] = ctk

    backend_tkagg = types.ModuleType("matplotlib.backends.backend_tkagg")

    class DummyFigureCanvasTkAgg:
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs

        def draw(self):
            return None

        def get_tk_widget(self):
            return DummyWidget()

    backend_tkagg.FigureCanvasTkAgg = DummyFigureCanvasTkAgg
    sys.modules["matplotlib.backends.backend_tkagg"] = backend_tkagg


_install_dark_panel_import_stubs()
dark_panel = importlib.import_module("UI.components.terminal_vwap_payoff_dark_panel")


def make_dark_panel_instance():
    instance = object.__new__(dark_panel.TerminalVWAPPayoffDarkPanel)
    instance.selected_structure = None
    instance.status_calls = []
    instance.warning_calls = []
    instance.render_list_calls = 0
    instance.clear_side_calls = 0

    def safe_status(message):
        instance.status_calls.append(message)

    def render_structures_list():
        instance.render_list_calls += 1

    def clear_side():
        instance.clear_side_calls += 1

    instance._safe_status = safe_status
    instance._render_structures_list = render_structures_list
    instance._clear_side = clear_side
    return instance


@pytest.fixture
def captured_warnings(monkeypatch):
    calls = []

    def fake_showwarning(title, message, parent=None):
        calls.append(
            {
                "title": title,
                "message": message,
                "parent": parent,
            }
        )

    monkeypatch.setattr(dark_panel.messagebox, "showwarning", fake_showwarning)
    return calls


def test_require_selected_structure_reports_clear_status_without_tk(captured_warnings):
    instance = make_dark_panel_instance()

    result = instance._require_selected_structure()

    assert result is None
    assert instance.status_calls == [
        "Nenhuma estrutura selecionada. "
        "Selecione uma estrutura no menu lateral antes de executar esta acao."
    ]
    assert captured_warnings == [
        {
            "title": "Estrutura",
            "message": (
                "Nenhuma estrutura selecionada. "
                "Selecione uma estrutura no menu lateral antes de executar esta acao."
            ),
            "parent": None,
        }
    ]


def test_require_selected_structure_returns_current_structure_without_warning(
    captured_warnings,
):
    instance = make_dark_panel_instance()
    structure = {
        "id": 10,
        "name": "Condor PETR4",
        "underlying_asset": "PETR4",
        "status": "active",
    }
    instance.selected_structure = structure

    result = instance._require_selected_structure()

    assert result is structure
    assert instance.status_calls == []
    assert captured_warnings == []


def test_render_structure_actions_without_selection_returns_to_structures_list(
    captured_warnings,
):
    instance = make_dark_panel_instance()

    instance._render_structure_actions()

    assert instance.render_list_calls == 1
    assert instance.clear_side_calls == 0
    assert instance.status_calls == [
        "Nenhuma estrutura selecionada. "
        "Selecione uma estrutura no menu lateral antes de executar esta acao."
    ]
    assert len(captured_warnings) == 1


@pytest.mark.parametrize(
    ("method_name", "args"),
    [
        ("_render_adjust_structure_block", ()),
        ("edit_selected_structure", ()),
        ("duplicate_selected_structure", ()),
        ("recalculate_selected_structure", ()),
        ("archive_selected_structure", ()),
        ("_register_structure_decision", ("HOLD",)),
    ],
)
def test_operational_actions_stop_safely_without_selected_structure(
    captured_warnings,
    method_name,
    args,
):
    instance = make_dark_panel_instance()

    def fail_if_called(*_args, **_kwargs):
        pytest.fail("Acao operacional nao deveria continuar sem estrutura selecionada.")

    instance._load_legs = fail_if_called
    instance._load_market = fail_if_called
    instance._calculate_payoff_from_legs = fail_if_called
    instance._is_structures_repository_available = fail_if_called
    instance._insert_structure_decision = fail_if_called

    getattr(instance, method_name)(*args)

    assert instance.status_calls == [
        "Nenhuma estrutura selecionada. "
        "Selecione uma estrutura no menu lateral antes de executar esta acao."
    ]
    assert len(captured_warnings) == 1
