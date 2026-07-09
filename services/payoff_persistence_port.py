# services/payoff_persistence_port.py
from typing import Any, Protocol


class PayoffPersistencePort(Protocol):
    """
    Contrato de persistência derivada (payoff + decisão).

    Implementações devem gravar os dados no app.db após
    uma execução de pricing bem-sucedida.
    """

    def persist(
        self,
        pricing_payload: dict[str, Any] | None,
        result: dict[str, Any],
    ) -> None:
        ...
