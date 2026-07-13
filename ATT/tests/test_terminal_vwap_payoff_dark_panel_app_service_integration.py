import sys
import types


customtkinter_stub = types.ModuleType("customtkinter")


class CTkFrame:
    pass


customtkinter_stub.CTkFrame = CTkFrame
customtkinter_stub.CTkLabel = object
customtkinter_stub.CTkButton = object
customtkinter_stub.CTkScrollableFrame = object
customtkinter_stub.CTkTabview = object
customtkinter_stub.CTkOptionMenu = object
customtkinter_stub.CTkEntry = object
customtkinter_stub.CTkTextbox = object
customtkinter_stub.CTkSwitch = object

sys.modules.setdefault("customtkinter", customtkinter_stub)



backend_tkagg_stub = types.ModuleType("matplotlib.backends.backend_tkagg")


class FigureCanvasTkAgg:
    pass


backend_tkagg_stub.FigureCanvasTkAgg = FigureCanvasTkAgg
sys.modules.setdefault("matplotlib.backends.backend_tkagg", backend_tkagg_stub)

from UI.components.terminal_vwap_payoff_dark_panel import TerminalVWAPPayoffDarkPanel


class DummyHeader:
    def __init__(self):
        self.configured = {}

    def configure(self, **kwargs):
        self.configured.update(kwargs)


def test_select_structure_uses_injected_app_service_viewmodel():
    panel = object.__new__(TerminalVWAPPayoffDarkPanel)

    calls = {}
    statuses = []
    rendered = {}

    class FakeAppService:
        def build_for_structure_id(self, structure_id):
            calls["structure_id"] = structure_id
            return {
                "structure": {
                    "id": structure_id,
                    "name": "VM Estrutura",
                    "underlying_asset": "PETR4",
                    "legs": [{"symbol": "PETRA100", "quantity": 1}],
                },
                "market": {
                    "current_price": 30.5,
                    "vwap": 30.1,
                    "series": [{"price": 30.5, "vwap": 30.1}],
                },
                "payoff_points": [
                    {"price": 25.0, "payoff": -100.0},
                    {"price": 35.0, "payoff": 150.0},
                ],
            }

    panel._app_service = FakeAppService()
    panel.header = DummyHeader()
    panel.on_status = statuses.append

    panel._load_legs = lambda _sid: (_ for _ in ()).throw(
        AssertionError("_load_legs nao deveria ser chamado com viewmodel completo")
    )
    panel._load_market = lambda _asset: (_ for _ in ()).throw(
        AssertionError("_load_market nao deveria ser chamado com viewmodel completo")
    )
    panel._load_payoff_points = lambda _sid, _legs: (_ for _ in ()).throw(
        AssertionError("_load_payoff_points nao deveria ser chamado com viewmodel completo")
    )

    panel._update_kpis = lambda market, payoff_points: rendered.setdefault(
        "kpis", (market, payoff_points)
    )
    panel._render_legs = lambda legs: rendered.setdefault("legs", legs)
    panel._render_charts = lambda market, payoff_points, asset, legs: rendered.setdefault(
        "charts", (market, payoff_points, asset, legs)
    )
    panel._render_alerts = lambda market, payoff_points, legs: rendered.setdefault(
        "alerts", (market, payoff_points, legs)
    )
    panel._render_structure_actions = lambda: rendered.setdefault("actions", True)

    TerminalVWAPPayoffDarkPanel.select_structure(
        panel,
        {
            "id": 10,
            "name": "Estrutura Original",
            "underlying_asset": "VALE3",
        },
    )

    assert calls["structure_id"] == 10
    assert panel.selected_structure["name"] == "VM Estrutura"
    assert panel.selected_structure["underlying_asset"] == "PETR4"

    assert "ID 10 - VM Estrutura | Ativo: PETR4" in panel.header.configured["text"]
    assert rendered["legs"] == [{"symbol": "PETRA100", "quantity": 1}]
    assert rendered["charts"][2] == "PETR4"
    assert statuses[-1] == "Estrutura carregada: ID 10"
