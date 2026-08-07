from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class PricingEnginePort(Protocol):
    """Porta canonica minima para motores de pricing.

    A porta estabiliza a fronteira entre o fluxo de pricing e qualquer motor
    concreto. Ela nao define algoritmo financeiro, nao altera persistencia e
    nao altera schema. O contrato minimo exige apenas que o motor receba um
    pricing_payload e retorne um dict.
    """

    def run(self, pricing_payload: dict[str, Any]) -> dict[str, Any]:
        """Executa o motor de pricing para um payload canonico."""
        ...


def validate_pricing_payload_for_engine(pricing_payload: dict[str, Any]) -> dict[str, Any]:
    """Valida o payload minimo aceito pela porta de engine.

    Esta validacao e intencionalmente leve nesta frente. A validacao financeira
    forte deve ficar em frente propria, conforme plano de contencao.
    """

    if not isinstance(pricing_payload, dict):
        raise TypeError("pricing_payload deve ser dict")

    return pricing_payload


def validate_engine_result(engine_result: dict[str, Any]) -> dict[str, Any]:
    """Valida o retorno minimo do motor de pricing."""

    if not isinstance(engine_result, dict):
        raise TypeError("engine_result deve ser dict")

    return engine_result


def run_pricing_engine(
    engine: PricingEnginePort,
    pricing_payload: dict[str, Any],
) -> dict[str, Any]:
    """Executa um PricingEnginePort de forma controlada.

    Regras desta frente:
    - nao troca motor real;
    - nao altera persistencia;
    - nao altera schema;
    - nao muda fluxo operacional amplo;
    - apenas formaliza a chamada via porta.
    """

    payload = validate_pricing_payload_for_engine(pricing_payload)

    runner = getattr(engine, "run", None)
    if not callable(runner):
        raise TypeError("engine deve expor metodo run(pricing_payload)")

    result = runner(payload)
    return validate_engine_result(result)


__all__ = [
    "PricingEnginePort",
    "validate_pricing_payload_for_engine",
    "validate_engine_result",
    "run_pricing_engine",
]
