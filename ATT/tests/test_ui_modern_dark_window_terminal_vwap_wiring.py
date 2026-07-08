import importlib
import sys
import types


class FakeStringVar:
    def __init__(self, value=""):
        self.value = value

    def set(self, value):
        self.value = value

    def get(self):
        return self.value


class FakeMenu:
    def __init__(self, *args, **kwargs):
        self.commands = []

    def add_command(self, **kwargs):
        self.commands.append(("command", kwargs))

    def add_separator(self):
        self.commands.append(("separator", {}))

    def add_cascade(self, **kwargs):
        self.commands.append(("cascade", kwargs))


class FakeRoot:
    def __init__(self):
        self.config = {}
        self.quit_called = False

    def title(self, value):
        self.window_title = value

    def geometry(self, value):
        self.window_geometry = value

    def minsize(self, width, height):
        self.window_minsize = (width, height)

    def configure(self, **kwargs):
        self.config.update(kwargs)

    def quit(self):
        self.quit_called = True


class FakeTabView:
    last_instance = None

    def __init__(self, parent):
        self.parent = parent
        self.tabs = []
        self.selected = None
        FakeTabView.last_instance = self

    def pack(self, *args, **kwargs):
        self.pack_args = (args, kwargs)

    def add(self, name):
        self.tabs.append(name)
        return {"tab": name}

    def set(self, name):
        self.selected = name


class PlaceholderWidget:
    def __init__(self, *args, **kwargs):
        pass

    def pack(self, *args, **kwargs):
        pass


def import_dark_window_with_safe_stubs(monkeypatch):
    sys.modules.pop("UI.modern.dark_window", None)

    fake_ctk = types.ModuleType("customtkinter")
    fake_ctk.CTk = FakeRoot
    fake_ctk.CTkTabview = FakeTabView
    fake_ctk.CTkFrame = PlaceholderWidget
    fake_ctk.CTkButton = PlaceholderWidget
    fake_ctk.CTkLabel = PlaceholderWidget
    fake_ctk.set_appearance_mode = lambda *args, **kwargs: None
    fake_ctk.set_default_color_theme = lambda *args, **kwargs: None

    terminal_module = types.ModuleType("UI.components.terminal_vwap_payoff_dark_panel")
    terminal_module.TerminalVWAPPayoffDarkPanel = PlaceholderWidget

    decisions_module = types.ModuleType("UI.components.decisions_dark_panel")
    decisions_module.DecisionsDarkPanel = PlaceholderWidget

    ui_data_module = types.ModuleType("UI.models.ui_data")

    class FakeUIDataModel:
        pass

    ui_data_module.UIDataModel = FakeUIDataModel

    monkeypatch.setitem(sys.modules, "customtkinter", fake_ctk)
    monkeypatch.setitem(
        sys.modules,
        "UI.components.terminal_vwap_payoff_dark_panel",
        terminal_module,
    )
    monkeypatch.setitem(
        sys.modules,
        "UI.components.decisions_dark_panel",
        decisions_module,
    )
    monkeypatch.setitem(sys.modules, "UI.models.ui_data", ui_data_module)

    return importlib.import_module("UI.modern.dark_window")


def patch_common_runtime(monkeypatch, module, app_db):
    monkeypatch.setattr(module, "APP_DB_PATH", app_db)

    monkeypatch.setattr(module.tk, "StringVar", FakeStringVar)
    monkeypatch.setattr(module.tk, "Menu", FakeMenu)

    monkeypatch.setattr(module.ctk, "CTk", FakeRoot)
    monkeypatch.setattr(module.ctk, "CTkTabview", FakeTabView)
    monkeypatch.setattr(module.ctk, "set_appearance_mode", lambda *args, **kwargs: None)
    monkeypatch.setattr(module.ctk, "set_default_color_theme", lambda *args, **kwargs: None)

    monkeypatch.setattr(module.messagebox, "showwarning", lambda *args, **kwargs: None)
    monkeypatch.setattr(module.messagebox, "showerror", lambda *args, **kwargs: None)


def test_modern_dark_window_wires_terminal_vwap_and_decisions(monkeypatch, tmp_path):
    module = import_dark_window_with_safe_stubs(monkeypatch)

    app_db = tmp_path / "app.db"
    app_db.write_text("", encoding="utf-8")

    patch_common_runtime(monkeypatch, module, app_db)

    class FakeUIDataModel:
        pass

    class FakeTerminalVWAPPayoffDarkPanel:
        instances = []

        def __init__(self, parent, db_path, on_status):
            self.parent = parent
            self.db_path = db_path
            self.on_status = on_status
            self.structures = [
                {"id": 7, "name": "Estrutura 7"},
                {"id": 9, "name": "Estrutura 9"},
            ]
            self.selected_structures = []
            self.reload_count = 0
            FakeTerminalVWAPPayoffDarkPanel.instances.append(self)

        def pack(self, *args, **kwargs):
            self.pack_args = (args, kwargs)

        def reload_structures(self):
            self.reload_count += 1

        def select_structure(self, structure):
            self.selected_structures.append(structure)

    class FakeDecisionsDarkPanel:
        instances = []

        def __init__(
            self,
            parent,
            data_model,
            on_status,
            on_load_structure,
            get_structures,
        ):
            self.parent = parent
            self.data_model = data_model
            self.on_status = on_status
            self.on_load_structure = on_load_structure
            self.get_structures = get_structures
            self.reload_count = 0
            FakeDecisionsDarkPanel.instances.append(self)

        def pack(self, *args, **kwargs):
            self.pack_args = (args, kwargs)

        def reload_decisions(self):
            self.reload_count += 1

    monkeypatch.setattr(module, "UIDataModel", FakeUIDataModel)
    monkeypatch.setattr(module, "TerminalVWAPPayoffDarkPanel", FakeTerminalVWAPPayoffDarkPanel)
    monkeypatch.setattr(module, "DecisionsDarkPanel", FakeDecisionsDarkPanel)

    window = module.ModernDarkWindow()

    tabs = FakeTabView.last_instance
    terminal_panel = FakeTerminalVWAPPayoffDarkPanel.instances[0]
    decisions_panel = FakeDecisionsDarkPanel.instances[0]

    assert tabs.tabs == ["Terminal VWAP", "Decisões"]

    assert terminal_panel.db_path == str(app_db)
    assert callable(terminal_panel.on_status)

    assert decisions_panel.on_load_structure.__self__ is window
    assert decisions_panel.get_structures.__self__ is window

    assert decisions_panel.get_structures() == terminal_panel.structures

    window._load_structure_from_decision("7")

    assert terminal_panel.selected_structures == [{"id": 7, "name": "Estrutura 7"}]
    assert tabs.selected == "Terminal VWAP"
    assert "Estrutura 7 carregada" in window.status_var.get()


def test_modern_dark_window_get_structures_reloads_terminal_when_empty(monkeypatch, tmp_path):
    module = import_dark_window_with_safe_stubs(monkeypatch)

    app_db = tmp_path / "app.db"
    app_db.write_text("", encoding="utf-8")

    patch_common_runtime(monkeypatch, module, app_db)

    class FakeUIDataModel:
        pass

    class FakeTerminalVWAPPayoffDarkPanel:
        instances = []

        def __init__(self, parent, db_path, on_status):
            self.parent = parent
            self.db_path = db_path
            self.on_status = on_status
            self.structures = []
            self.reload_count = 0
            FakeTerminalVWAPPayoffDarkPanel.instances.append(self)

        def pack(self, *args, **kwargs):
            self.pack_args = (args, kwargs)

        def reload_structures(self):
            self.reload_count += 1
            self.structures = [{"id": 11, "name": "Estrutura recarregada"}]

    class FakeDecisionsDarkPanel:
        def __init__(self, *args, **kwargs):
            pass

        def pack(self, *args, **kwargs):
            pass

    monkeypatch.setattr(module, "UIDataModel", FakeUIDataModel)
    monkeypatch.setattr(module, "TerminalVWAPPayoffDarkPanel", FakeTerminalVWAPPayoffDarkPanel)
    monkeypatch.setattr(module, "DecisionsDarkPanel", FakeDecisionsDarkPanel)

    window = module.ModernDarkWindow()

    result = window._get_structures_for_decisions()

    terminal_panel = FakeTerminalVWAPPayoffDarkPanel.instances[0]

    assert terminal_panel.reload_count == 1
    assert result == [{"id": 11, "name": "Estrutura recarregada"}]



def test_modern_dark_window_get_structures_returns_empty_when_terminal_reload_fails(
    monkeypatch,
    tmp_path,
):
    module = import_dark_window_with_safe_stubs(monkeypatch)

    app_db = tmp_path / "app.db"
    app_db.write_text("", encoding="utf-8")

    patch_common_runtime(monkeypatch, module, app_db)

    class FakeUIDataModel:
        pass

    class FakeTerminalVWAPPayoffDarkPanel:
        instances = []

        def __init__(self, parent, db_path, on_status):
            self.parent = parent
            self.db_path = db_path
            self.on_status = on_status
            self.structures = []
            self.reload_count = 0
            FakeTerminalVWAPPayoffDarkPanel.instances.append(self)

        def pack(self, *args, **kwargs):
            self.pack_args = (args, kwargs)

        def reload_structures(self):
            self.reload_count += 1
            raise RuntimeError("falha no terminal")

    class FakeDecisionsDarkPanel:
        def __init__(self, *args, **kwargs):
            pass

        def pack(self, *args, **kwargs):
            pass

    monkeypatch.setattr(module, "UIDataModel", FakeUIDataModel)
    monkeypatch.setattr(module, "TerminalVWAPPayoffDarkPanel", FakeTerminalVWAPPayoffDarkPanel)
    monkeypatch.setattr(module, "DecisionsDarkPanel", FakeDecisionsDarkPanel)

    window = module.ModernDarkWindow()

    result = window._get_structures_for_decisions()

    terminal_panel = FakeTerminalVWAPPayoffDarkPanel.instances[0]

    assert result == []
    assert terminal_panel.reload_count == 1
    assert window.status_var.get() == (
        "Erro ao recarregar estruturas para decisões: falha no terminal"
    )


def test_modern_dark_window_load_structure_from_decision_handles_terminal_reload_failure(
    monkeypatch,
    tmp_path,
):
    module = import_dark_window_with_safe_stubs(monkeypatch)

    app_db = tmp_path / "app.db"
    app_db.write_text("", encoding="utf-8")

    patch_common_runtime(monkeypatch, module, app_db)

    class FakeUIDataModel:
        pass

    class FakeTerminalVWAPPayoffDarkPanel:
        instances = []

        def __init__(self, parent, db_path, on_status):
            self.parent = parent
            self.db_path = db_path
            self.on_status = on_status
            self.structures = []
            self.reload_count = 0
            self.selected_structures = []
            FakeTerminalVWAPPayoffDarkPanel.instances.append(self)

        def pack(self, *args, **kwargs):
            self.pack_args = (args, kwargs)

        def reload_structures(self):
            self.reload_count += 1
            raise RuntimeError("falha ao recarregar terminal")

        def select_structure(self, structure):
            self.selected_structures.append(structure)

    class FakeDecisionsDarkPanel:
        def __init__(self, *args, **kwargs):
            pass

        def pack(self, *args, **kwargs):
            pass

    monkeypatch.setattr(module, "UIDataModel", FakeUIDataModel)
    monkeypatch.setattr(module, "TerminalVWAPPayoffDarkPanel", FakeTerminalVWAPPayoffDarkPanel)
    monkeypatch.setattr(module, "DecisionsDarkPanel", FakeDecisionsDarkPanel)

    window = module.ModernDarkWindow()

    window._load_structure_from_decision("7")

    terminal_panel = FakeTerminalVWAPPayoffDarkPanel.instances[0]

    assert terminal_panel.reload_count == 1
    assert terminal_panel.selected_structures == []
    assert window.status_var.get() == (
        "Erro ao recarregar estruturas para decisão 7: falha ao recarregar terminal"
    )


def test_modern_dark_window_load_structure_from_decision_handles_terminal_select_failure(
    monkeypatch,
    tmp_path,
):
    module = import_dark_window_with_safe_stubs(monkeypatch)

    app_db = tmp_path / "app.db"
    app_db.write_text("", encoding="utf-8")

    patch_common_runtime(monkeypatch, module, app_db)

    class FakeUIDataModel:
        pass

    class FakeTerminalVWAPPayoffDarkPanel:
        instances = []

        def __init__(self, parent, db_path, on_status):
            self.parent = parent
            self.db_path = db_path
            self.on_status = on_status
            self.structures = [{"id": 7, "name": "Estrutura com falha"}]
            self.reload_count = 0
            self.selected_attempts = []
            FakeTerminalVWAPPayoffDarkPanel.instances.append(self)

        def pack(self, *args, **kwargs):
            self.pack_args = (args, kwargs)

        def reload_structures(self):
            self.reload_count += 1

        def select_structure(self, structure):
            self.selected_attempts.append(structure)
            raise RuntimeError("falha ao selecionar terminal")

    class FakeDecisionsDarkPanel:
        def __init__(self, *args, **kwargs):
            pass

        def pack(self, *args, **kwargs):
            pass

    class FakeTabs:
        def __init__(self):
            self.set_calls = []

        def set(self, tab_name):
            self.set_calls.append(tab_name)

    monkeypatch.setattr(module, "UIDataModel", FakeUIDataModel)
    monkeypatch.setattr(module, "TerminalVWAPPayoffDarkPanel", FakeTerminalVWAPPayoffDarkPanel)
    monkeypatch.setattr(module, "DecisionsDarkPanel", FakeDecisionsDarkPanel)

    window = module.ModernDarkWindow()
    window.tabs = FakeTabs()

    window._load_structure_from_decision(7)

    terminal_panel = FakeTerminalVWAPPayoffDarkPanel.instances[0]

    assert terminal_panel.reload_count == 0
    assert terminal_panel.selected_attempts == [{"id": 7, "name": "Estrutura com falha"}]
    assert window.tabs.set_calls == []
    assert window.status_var.get() == (
        "Erro ao selecionar estrutura 7: falha ao selecionar terminal"
    )

def test_modern_dark_window_load_structure_from_decision_selects_existing_structure(
    monkeypatch,
    tmp_path,
):
    module = import_dark_window_with_safe_stubs(monkeypatch)

    app_db = tmp_path / "app.db"
    app_db.write_text("", encoding="utf-8")

    patch_common_runtime(monkeypatch, module, app_db)

    class FakeUIDataModel:
        pass

    class FakeTerminalVWAPPayoffDarkPanel:
        instances = []

        def __init__(self, parent, db_path, on_status):
            self.parent = parent
            self.db_path = db_path
            self.on_status = on_status
            self.structures = [
                {"id": 7, "name": "Estrutura alvo"},
                {"id": 8, "name": "Outra estrutura"},
            ]
            self.reload_count = 0
            self.selected_structures = []
            FakeTerminalVWAPPayoffDarkPanel.instances.append(self)

        def pack(self, *args, **kwargs):
            self.pack_args = (args, kwargs)

        def reload_structures(self):
            self.reload_count += 1

        def select_structure(self, structure):
            self.selected_structures.append(structure)

    class FakeDecisionsDarkPanel:
        def __init__(self, *args, **kwargs):
            pass

        def pack(self, *args, **kwargs):
            pass

    class FakeTabs:
        def __init__(self):
            self.set_calls = []

        def set(self, tab_name):
            self.set_calls.append(tab_name)

    class FakeMessagebox:
        warning_calls = []
        error_calls = []

        @classmethod
        def showwarning(cls, *args, **kwargs):
            cls.warning_calls.append((args, kwargs))

        @classmethod
        def showerror(cls, *args, **kwargs):
            cls.error_calls.append((args, kwargs))

    monkeypatch.setattr(module, "UIDataModel", FakeUIDataModel)
    monkeypatch.setattr(module, "TerminalVWAPPayoffDarkPanel", FakeTerminalVWAPPayoffDarkPanel)
    monkeypatch.setattr(module, "DecisionsDarkPanel", FakeDecisionsDarkPanel)
    monkeypatch.setattr(module, "messagebox", FakeMessagebox)

    window = module.ModernDarkWindow()
    window.tabs = FakeTabs()

    window._load_structure_from_decision("7")

    terminal_panel = FakeTerminalVWAPPayoffDarkPanel.instances[0]

    assert terminal_panel.reload_count == 0
    assert terminal_panel.selected_structures == [{"id": 7, "name": "Estrutura alvo"}]
    assert window.tabs.set_calls == ["Terminal VWAP"]
    assert FakeMessagebox.warning_calls == []
    assert FakeMessagebox.error_calls == []
    assert window.status_var.get() == "Estrutura 7 carregada a partir da decisão"

def test_modern_dark_window_load_structure_from_decision_reloads_empty_structures_and_selects(
    monkeypatch,
    tmp_path,
):
    module = import_dark_window_with_safe_stubs(monkeypatch)

    app_db = tmp_path / "app.db"
    app_db.write_text("", encoding="utf-8")

    patch_common_runtime(monkeypatch, module, app_db)

    class FakeUIDataModel:
        pass

    class FakeTerminalVWAPPayoffDarkPanel:
        instances = []

        def __init__(self, parent, db_path, on_status):
            self.parent = parent
            self.db_path = db_path
            self.on_status = on_status
            self.structures = []
            self.reload_count = 0
            self.selected_structures = []
            FakeTerminalVWAPPayoffDarkPanel.instances.append(self)

        def pack(self, *args, **kwargs):
            self.pack_args = (args, kwargs)

        def reload_structures(self):
            self.reload_count += 1
            self.structures = [
                {"id": 7, "name": "Estrutura recarregada"},
                {"id": 9, "name": "Outra estrutura"},
            ]

        def select_structure(self, structure):
            self.selected_structures.append(structure)

    class FakeDecisionsDarkPanel:
        def __init__(self, *args, **kwargs):
            pass

        def pack(self, *args, **kwargs):
            pass

    class FakeTabs:
        def __init__(self):
            self.set_calls = []

        def set(self, tab_name):
            self.set_calls.append(tab_name)

    class FakeMessagebox:
        warning_calls = []
        error_calls = []

        @classmethod
        def showwarning(cls, *args, **kwargs):
            cls.warning_calls.append((args, kwargs))

        @classmethod
        def showerror(cls, *args, **kwargs):
            cls.error_calls.append((args, kwargs))

    monkeypatch.setattr(module, "UIDataModel", FakeUIDataModel)
    monkeypatch.setattr(module, "TerminalVWAPPayoffDarkPanel", FakeTerminalVWAPPayoffDarkPanel)
    monkeypatch.setattr(module, "DecisionsDarkPanel", FakeDecisionsDarkPanel)
    monkeypatch.setattr(module, "messagebox", FakeMessagebox)

    window = module.ModernDarkWindow()
    window.tabs = FakeTabs()

    window._load_structure_from_decision("7")

    terminal_panel = FakeTerminalVWAPPayoffDarkPanel.instances[0]

    assert terminal_panel.reload_count == 1
    assert terminal_panel.selected_structures == [
        {"id": 7, "name": "Estrutura recarregada"}
    ]
    assert window.tabs.set_calls == ["Terminal VWAP"]
    assert FakeMessagebox.warning_calls == []
    assert FakeMessagebox.error_calls == []
    assert window.status_var.get() == "Estrutura 7 carregada a partir da decisão"

def test_modern_dark_window_load_structure_from_decision_warns_when_structure_missing_after_reload(
    monkeypatch,
    tmp_path,
):
    module = import_dark_window_with_safe_stubs(monkeypatch)

    app_db = tmp_path / "app.db"
    app_db.write_text("", encoding="utf-8")

    patch_common_runtime(monkeypatch, module, app_db)

    class FakeUIDataModel:
        pass

    class FakeTerminalVWAPPayoffDarkPanel:
        instances = []

        def __init__(self, parent, db_path, on_status):
            self.parent = parent
            self.db_path = db_path
            self.on_status = on_status
            self.structures = []
            self.reload_count = 0
            self.selected_structures = []
            FakeTerminalVWAPPayoffDarkPanel.instances.append(self)

        def pack(self, *args, **kwargs):
            self.pack_args = (args, kwargs)

        def reload_structures(self):
            self.reload_count += 1
            self.structures = [
                {"id": 8, "name": "Outra estrutura"},
                {"id": 9, "name": "Mais uma estrutura"},
            ]

        def select_structure(self, structure):
            self.selected_structures.append(structure)

    class FakeDecisionsDarkPanel:
        def __init__(self, *args, **kwargs):
            pass

        def pack(self, *args, **kwargs):
            pass

    class FakeTabs:
        def __init__(self):
            self.set_calls = []

        def set(self, tab_name):
            self.set_calls.append(tab_name)

    class FakeMessagebox:
        warning_calls = []
        error_calls = []

        @classmethod
        def showwarning(cls, *args, **kwargs):
            cls.warning_calls.append((args, kwargs))

        @classmethod
        def showerror(cls, *args, **kwargs):
            cls.error_calls.append((args, kwargs))

    monkeypatch.setattr(module, "UIDataModel", FakeUIDataModel)
    monkeypatch.setattr(module, "TerminalVWAPPayoffDarkPanel", FakeTerminalVWAPPayoffDarkPanel)
    monkeypatch.setattr(module, "DecisionsDarkPanel", FakeDecisionsDarkPanel)
    monkeypatch.setattr(module, "messagebox", FakeMessagebox)

    window = module.ModernDarkWindow()
    window.tabs = FakeTabs()

    window._load_structure_from_decision("7")

    terminal_panel = FakeTerminalVWAPPayoffDarkPanel.instances[0]

    assert terminal_panel.reload_count == 1
    assert terminal_panel.selected_structures == []
    assert window.tabs.set_calls == []
    assert len(FakeMessagebox.warning_calls) == 1
    assert FakeMessagebox.error_calls == []
    assert "7" in window.status_var.get()

def test_modern_dark_window_load_structure_from_decision_warns_when_reload_fails(
    monkeypatch,
    tmp_path,
):
    module = import_dark_window_with_safe_stubs(monkeypatch)

    app_db = tmp_path / "app.db"
    app_db.write_text("", encoding="utf-8")

    patch_common_runtime(monkeypatch, module, app_db)

    class FakeUIDataModel:
        pass

    class FakeTerminalVWAPPayoffDarkPanel:
        instances = []

        def __init__(self, parent, db_path, on_status):
            self.parent = parent
            self.db_path = db_path
            self.on_status = on_status
            self.structures = []
            self.reload_count = 0
            self.selected_structures = []
            FakeTerminalVWAPPayoffDarkPanel.instances.append(self)

        def pack(self, *args, **kwargs):
            self.pack_args = (args, kwargs)

        def reload_structures(self):
            self.reload_count += 1
            raise RuntimeError("falha ao recarregar estruturas")

        def select_structure(self, structure):
            self.selected_structures.append(structure)

    class FakeDecisionsDarkPanel:
        def __init__(self, *args, **kwargs):
            pass

        def pack(self, *args, **kwargs):
            pass

    class FakeTabs:
        def __init__(self):
            self.set_calls = []

        def set(self, tab_name):
            self.set_calls.append(tab_name)

    class FakeMessagebox:
        warning_calls = []
        error_calls = []

        @classmethod
        def showwarning(cls, *args, **kwargs):
            cls.warning_calls.append((args, kwargs))

        @classmethod
        def showerror(cls, *args, **kwargs):
            cls.error_calls.append((args, kwargs))

    monkeypatch.setattr(module, "UIDataModel", FakeUIDataModel)
    monkeypatch.setattr(module, "TerminalVWAPPayoffDarkPanel", FakeTerminalVWAPPayoffDarkPanel)
    monkeypatch.setattr(module, "DecisionsDarkPanel", FakeDecisionsDarkPanel)
    monkeypatch.setattr(module, "messagebox", FakeMessagebox)

    window = module.ModernDarkWindow()
    window.tabs = FakeTabs()

    window._load_structure_from_decision("7")

    terminal_panel = FakeTerminalVWAPPayoffDarkPanel.instances[0]

    assert terminal_panel.reload_count == 1
    assert terminal_panel.selected_structures == []
    assert window.tabs.set_calls == []
    assert len(FakeMessagebox.warning_calls) == 1

    warning_args, warning_kwargs = FakeMessagebox.warning_calls[0]

    assert warning_args[0] == "Estruturas indisponíveis"
    assert "Não foi possível recarregar" in warning_args[1]
    assert "falha ao recarregar estruturas" in warning_args[1]
    assert "parent" in warning_kwargs
    assert FakeMessagebox.error_calls == []

    status = window.status_var.get()

    assert "recarregar" in status.lower()
    assert "estrutura" in status.lower()
