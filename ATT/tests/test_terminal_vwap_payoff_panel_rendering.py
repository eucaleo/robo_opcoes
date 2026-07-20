from UI.components import terminal_vwap_payoff_panel as panel


class FakeVar:
    def __init__(self, value=""):
        self.value = value

    def set(self, value):
        self.value = value

    def get(self):
        return self.value


class FakeTree:
    def __init__(self):
        self.children = []
        self.rows = {}

    def get_children(self):
        return list(self.children)

    def delete(self, item):
        if item in self.children:
            self.children.remove(item)
        self.rows.pop(item, None)

    def insert(self, parent, index, iid=None, values=()):
        item_id = str(iid if iid is not None else len(self.children))
        self.children.append(item_id)
        self.rows[item_id] = tuple(values)
        return item_id


class FakeText:
    def __init__(self):
        self.state = None
        self.content = ""

    def configure(self, **kwargs):
        if "state" in kwargs:
            self.state = kwargs["state"]

    def delete(self, start, end):
        self.content = ""

    def insert(self, index, text):
        self.content = text


def make_panel_instance():
    instance = object.__new__(panel.TerminalVWAPPayoffPanel)
    instance._summary_vars = {
        "structure_id": FakeVar(),
        "name": FakeVar(),
        "underlying_asset": FakeVar(),
        "status": FakeVar(),
        "current_price": FakeVar(),
        "vwap": FakeVar(),
        "price_vs_vwap_percent": FakeVar(),
        "market_source": FakeVar(),
        "market_timestamp": FakeVar(),
        "points_count": FakeVar(),
        "min_result": FakeVar(),
        "max_result": FakeVar(),
        "break_even_points": FakeVar(),
    }
    instance._legs_tree = FakeTree()
    instance._payoff_tree = FakeTree()
    instance._payoff_summary_var = FakeVar()
    instance._warnings_text = FakeText()
    instance._status_var = FakeVar()
    instance._on_status = None
    return instance


def test_render_viewmodel_populates_summary_tables_and_warnings_without_tk():
    instance = make_panel_instance()

    viewmodel = {
        "structure": {
            "structure_id": 10,
            "name": "Condor PETR4",
            "underlying_asset": "PETR4",
            "status": "ACTIVE",
        },
        "market": {
            "current_price": "31,25",
            "vwap": 30,
            "price_vs_vwap_percent": 4.166,
            "source": "provider-test",
            "timestamp": "2026-07-07 16:30:00",
        },
        "legs": [
            {
                "leg_order": 1,
                "symbol": "PETR4C30",
                "position_side": "BUY",
                "option_type": "CALL",
                "strike": "30,50",
                "expiration_date": "2026-08-21",
                "quantity": 100,
                "premium": "1,25",
            }
        ],
        "payoff": {
            "points_count": 1,
            "min_result": -10,
            "max_result": 20,
            "break_even_points": [30, "32,5"],
            "points": [
                {
                    "underlying_price": "31,25",
                    "result": "125,75",
                }
            ],
        },
        "meta": {
            "warnings": ["Aviso principal", "", None, 123],
        },
    }

    instance.render_viewmodel(viewmodel)

    assert instance._current_viewmodel == viewmodel

    assert instance._summary_vars["structure_id"].get() == "10"
    assert instance._summary_vars["name"].get() == "Condor PETR4"
    assert instance._summary_vars["current_price"].get() == "31,25"
    assert instance._summary_vars["vwap"].get() == "30,00"
    assert instance._summary_vars["price_vs_vwap_percent"].get() == "4,17%"
    assert instance._summary_vars["break_even_points"].get() == "30,00, 32,50"

    assert instance._legs_tree.rows == {
        "0": (
            "1",
            "PETR4C30",
            "BUY",
            "CALL",
            "30,50",
            "2026-08-21",
            "100",
            "R$ 1,25",
        )
    }

    assert instance._payoff_tree.rows == {
        "0": (
            "31,25",
            "R$ 125,75",
        )
    }

    assert instance._payoff_summary_var.get() == (
        "Pontos: 1 | Mín: R$ -10,00 | Máx: R$ 20,00 | BE: 30,00, 32,50"
    )

    assert instance._warnings_text.content == "- Aviso principal\n- 123"
    assert instance._warnings_text.state == "disabled"


def test_render_viewmodel_tolerates_non_mapping_input_without_tk():
    instance = make_panel_instance()

    instance.render_viewmodel("entrada invalida")

    assert instance._current_viewmodel == {}
    assert instance._summary_vars["structure_id"].get() == "N/A"
    assert instance._summary_vars["name"].get() == "N/A"
    assert instance._legs_tree.rows == {}
    assert instance._payoff_tree.rows == {}
    assert instance._warnings_text.content == "Sem avisos."


def test_render_structures_replaces_previous_rows_and_skips_invalid_items():
    instance = make_panel_instance()
    instance._structures_tree = FakeTree()
    instance._structures_tree.insert("", "end", iid="old", values=("old",))

    instance._structures = [
        "ignorar",
        {
            "structure_id": 1,
            "name": "Estrutura A",
            "underlying_asset": "VALE3",
            "status": "ACTIVE",
            "legs_count": 2,
        },
        None,
        {
            "structure_id": 2,
            "name": "Estrutura B",
            "underlying_asset": "PETR4",
            "status": "DRAFT",
            "legs_count": None,
        },
    ]

    instance._render_structures()

    assert instance._structures_tree.children == ["0", "1"]
    assert instance._structures_tree.rows == {
        "0": ("1", "Estrutura A", "VALE3", "ACTIVE", "2"),
        "1": ("2", "Estrutura B", "PETR4", "DRAFT", "N/A"),
    }


def test_render_payoff_replaces_previous_rows_without_tk():
    instance = make_panel_instance()
    instance._payoff_tree.insert("", "end", iid="old", values=("old", "old"))

    instance._render_payoff(
        {
            "payoff": {
                "points_count": 2,
                "min_result": "-100,5",
                "max_result": "200,25",
                "break_even_points": ["10,5"],
                "points": [
                    {"underlying_price": 10, "result": -100.5},
                    {"underlying_price": "12,25", "result": "200,25"},
                ],
            }
        }
    )

    assert instance._payoff_tree.children == ["0", "1"]
    assert instance._payoff_tree.rows == {
        "0": ("10,00", "R$ -100,50"),
        "1": ("12,25", "R$ 200,25"),
    }
    assert instance._payoff_summary_var.get() == (
        "Pontos: 2 | Mín: R$ -100,50 | Máx: R$ 200,25 | BE: 10,50"
    )


def test_render_warnings_accepts_scalar_warning_without_tk():
    instance = make_panel_instance()

    instance._render_warnings({"meta": {"warnings": "Aviso unico"}})

    assert instance._warnings_text.content == "- Aviso unico"
    assert instance._warnings_text.state == "disabled"


def test_set_status_updates_status_var_and_callback_without_tk():
    instance = make_panel_instance()
    calls = []
    instance._on_status = calls.append

    instance._set_status("Processando")

    assert instance._status_var.get() == "Processando"
    assert calls == ["Processando"]


def test_set_status_swallows_callback_exception_without_tk():
    instance = make_panel_instance()

    def broken_callback(message):
        raise RuntimeError(message)

    instance._on_status = broken_callback

    instance._set_status("Nao deve quebrar")

    assert instance._status_var.get() == "Nao deve quebrar"
