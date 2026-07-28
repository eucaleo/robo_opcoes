import inspect

from services.terminal_vwap_payoff_app_service import TerminalVWAPPayoffAppService


def test_call_first_available_nao_recebe_structure_id_como_keyword():
    """
    Protege o contrato interno usado pela UI de Decisões.

    structure_id deve ser repassado à função candidata (normalmente por lambda),
    não diretamente ao helper _call_first_available, salvo se sua assinatura
    declarar explicitamente esse parâmetro.
    """
    assinatura = inspect.signature(
        TerminalVWAPPayoffAppService._call_first_available
    )

    assert "structure_id" not in assinatura.parameters
