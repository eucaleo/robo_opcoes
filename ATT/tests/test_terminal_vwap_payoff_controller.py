import pytest

from controllers.terminal_vwap_payoff_controller import (
    TerminalVWAPPayoffController,
)


class FakeTerminalVWAPPayoffAppService:
    def __init__(self):
        self.loaded_structure_ids = []
        self.structures = [
            {
                "structure_id": "7",
                "name": "Trava BOVA11",
                "underlying_asset": "BOVA11",
                "status": "active",
                "legs": [{"symbol": "BOVAE195"}],
            },
            {
                "id": 8,
                "nome": "Estrutura PETR4",
                "ativo_objeto": "PETR4",
                "status": "draft",
                "legs_count": 2,
            },
        ]

    def build_for_structure_id(self, structure_id):
        self.loaded_structure_ids.append(structure_id)
        return {
            "terminal": {
                "name": "ui-terminal-vwap-payoff",
                "ready": True,
            },
            "structure": {
                "structure_id": structure_id,
            },
        }

    def list_structures(self):
        return self.structures


def test_load_structure_validates_structure_id_and_delegates_to_app_service():
    app_service = FakeTerminalVWAPPayoffAppService()
    controller = TerminalVWAPPayoffController(app_service)

    result = controller.load_structure("7")

    assert app_service.loaded_structure_ids == [7]
    assert result["terminal"]["name"] == "ui-terminal-vwap-payoff"
    assert result["terminal"]["ready"] is True
    assert result["structure"]["structure_id"] == 7


def test_controller_keeps_aliases_for_future_ui_and_service_compatibility():
    app_service = FakeTerminalVWAPPayoffAppService()
    controller = TerminalVWAPPayoffController(app_service)

    result_from_build_alias = controller.build_for_structure_id(11)
    result_from_select_alias = controller.select_structure("12")

    assert result_from_build_alias["structure"]["structure_id"] == 11
    assert result_from_select_alias["structure"]["structure_id"] == 12
    assert app_service.loaded_structure_ids == [11, 12]


@pytest.mark.parametrize(
    "invalid_structure_id",
    [None, "", "abc", 0, -1, True, False],
)
def test_load_structure_rejects_invalid_structure_id(invalid_structure_id):
    controller = TerminalVWAPPayoffController(
        FakeTerminalVWAPPayoffAppService()
    )

    with pytest.raises(ValueError):
        controller.load_structure(invalid_structure_id)


def test_list_structures_returns_normalized_structure_summaries():
    controller = TerminalVWAPPayoffController(
        FakeTerminalVWAPPayoffAppService()
    )

    result = controller.list_structures()

    assert result == [
        {
            "structure_id": 7,
            "name": "Trava BOVA11",
            "underlying_asset": "BOVA11",
            "status": "active",
            "legs_count": 1,
        },
        {
            "structure_id": 8,
            "name": "Estrutura PETR4",
            "underlying_asset": "PETR4",
            "status": "draft",
            "legs_count": 2,
        },
    ]


def test_list_structures_returns_empty_list_when_app_service_has_no_listing():
    class AppServiceWithoutListing:
        def build_for_structure_id(self, structure_id):
            return {"structure": {"structure_id": structure_id}}

    controller = TerminalVWAPPayoffController(AppServiceWithoutListing())

    assert controller.list_structures() == []


def test_controller_requires_app_service():
    with pytest.raises(ValueError):
        TerminalVWAPPayoffController(None)
