from services.terminal_vwap_payoff_app_service import TerminalVWAPPayoffAppService


class DecisionRepositoryWithKeywords:
    def __init__(self):
        self.calls = []

    def list_decisions(self, structure_id=None, limit=50):
        self.calls.append(
            {
                "structure_id": structure_id,
                "limit": limit,
            }
        )
        return [
            {
                "id": 101,
                "structure_id": structure_id,
                "decision": "HOLD",
            }
        ]


class DecisionRepositoryWithPositionalArguments:
    def __init__(self):
        self.calls = []

    def list_decisions(self, structure_id, limit):
        self.calls.append((structure_id, limit))
        return [
            {
                "id": 202,
                "structure_id": structure_id,
                "decision": "ADJUST",
            }
        ]


def test_list_decisions_uses_repository_with_keyword_arguments():
    repository = DecisionRepositoryWithKeywords()
    service = TerminalVWAPPayoffAppService(
        decision_repository=repository,
    )

    result = service.list_decisions(structure_id=7, limit=12)

    assert result == [
        {
            "id": 101,
            "structure_id": 7,
            "decision": "HOLD",
        }
    ]
    assert repository.calls == [
        {
            "structure_id": 7,
            "limit": 12,
        }
    ]


def test_list_decisions_supports_repository_with_positional_arguments():
    repository = DecisionRepositoryWithPositionalArguments()
    service = TerminalVWAPPayoffAppService(
        decision_repository=repository,
    )

    result = service.list_decisions(structure_id=9, limit=3)

    assert result == [
        {
            "id": 202,
            "structure_id": 9,
            "decision": "ADJUST",
        }
    ]
    assert repository.calls == [(9, 3)]


def test_list_decisions_returns_empty_list_without_repository():
    service = TerminalVWAPPayoffAppService()

    assert service.list_decisions() == []
