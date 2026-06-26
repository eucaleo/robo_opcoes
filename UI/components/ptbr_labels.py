"""
Rótulos PT-BR para valores canônicos usados internamente pelo sistema.

Regra:
- Banco/domínio/filtros internos continuam usando valores canônicos.
- UI exibe rótulos amigáveis em português.
"""

from __future__ import annotations

DECISION_VALUE_TO_LABEL = {
    "HOLD": "Manter",
    "PREPARE_ROLL": "Preparar rolagem",
    "CLOSE_REOPEN": "Fechar e reabrir",
    "ROLL": "Rolar",
    "ENTER": "Entrar",
}

DECISION_LABEL_TO_VALUE = {
    label: value for value, label in DECISION_VALUE_TO_LABEL.items()
}


def decision_to_label(value: object) -> str:
    """Converte valor canônico de decisão para rótulo PT-BR."""
    if value is None:
        return ""

    text = str(value)
    return DECISION_VALUE_TO_LABEL.get(text, text)


def decision_label_to_value(value: object) -> str:
    """Converte rótulo PT-BR de decisão para valor canônico."""
    if value is None:
        return ""

    text = str(value)
    return DECISION_LABEL_TO_VALUE.get(text, text)


def decision_filter_labels(include_blank: bool = True) -> list[str]:
    """Lista de opções visíveis no filtro de decisão."""
    labels = list(DECISION_VALUE_TO_LABEL.values())
    return ["", *labels] if include_blank else labels
