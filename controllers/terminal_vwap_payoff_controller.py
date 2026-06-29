"""Controller do Terminal VWAP Payoff.

Camada fina de entrada para a futura UI.

Responsabilidades:
- validar structure_id recebido pela interface;
- delegar carga do terminal ao app service;
- expor listagem normalizada de estruturas quando disponível;
- não acessar Excel, RTD bruto, CSV antigo ou arquivos operacionais.
"""

from __future__ import annotations

from typing import Any


class TerminalVWAPPayoffController:
    """Controller fino para seleção e carga do Terminal VWAP Payoff."""

    def __init__(self, app_service: Any) -> None:
        if app_service is None:
            raise ValueError("app_service é obrigatório")
        self._app_service = app_service

    def load_structure(self, structure_id: Any) -> dict[str, Any]:
        """Carrega o ViewModel do terminal para um structure_id validado."""
        normalized_structure_id = self._normalize_structure_id(structure_id)

        if hasattr(self._app_service, "build_for_structure_id"):
            return self._app_service.build_for_structure_id(normalized_structure_id)

        if hasattr(self._app_service, "load_structure"):
            return self._app_service.load_structure(normalized_structure_id)

        raise AttributeError(
            "app_service deve expor build_for_structure_id ou load_structure"
        )

    def build_for_structure_id(self, structure_id: Any) -> dict[str, Any]:
        """Alias compatível com o app service."""
        return self.load_structure(structure_id)

    def select_structure(self, structure_id: Any) -> dict[str, Any]:
        """Alias semântico para uso pela futura UI."""
        return self.load_structure(structure_id)

    def list_structures(self) -> list[dict[str, Any]]:
        """Lista estruturas disponíveis em formato estável para a UI.

        A listagem é opcional neste incremento. Quando o app service ainda não
        expõe listagem, retorna lista vazia em vez de acessar repositórios ou
        fontes externas diretamente.
        """
        raw_structures = self._call_first_available(
            self._app_service,
            (
                "list_structures",
                "list_available_structures",
                "listar_estruturas",
            ),
        )

        if raw_structures is None:
            return []

        return [
            self._normalize_structure_summary(item)
            for item in raw_structures
            if item is not None
        ]

    def _call_first_available(
        self,
        target: Any,
        method_names: tuple[str, ...],
    ) -> Any:
        for method_name in method_names:
            method = getattr(target, method_name, None)
            if callable(method):
                return method()
        return None

    def _normalize_structure_id(self, structure_id: Any) -> int:
        if structure_id is None:
            raise ValueError("structure_id é obrigatório")

        if isinstance(structure_id, bool):
            raise ValueError("structure_id inválido")

        try:
            normalized = int(str(structure_id).strip())
        except (TypeError, ValueError) as exc:
            raise ValueError("structure_id deve ser inteiro positivo") from exc

        if normalized <= 0:
            raise ValueError("structure_id deve ser inteiro positivo")

        return normalized

    def _normalize_structure_summary(self, structure: Any) -> dict[str, Any]:
        structure_id = self._get(
            structure,
            "structure_id",
            "id",
            "estrutura_id",
            default=None,
        )

        try:
            normalized_id = self._normalize_structure_id(structure_id)
        except ValueError:
            normalized_id = None

        legs = self._get(structure, "legs", "pernas", default=None)
        if legs is None:
            legs_count = self._get(
                structure,
                "legs_count",
                "quantidade_pernas",
                default=None,
            )
        else:
            try:
                legs_count = len(legs)
            except TypeError:
                legs_count = None

        return {
            "structure_id": normalized_id,
            "name": self._get(structure, "name", "nome", default=None),
            "underlying_asset": self._get(
                structure,
                "underlying_asset",
                "ativo_objeto",
                "ticker",
                default=None,
            ),
            "status": self._get(structure, "status", default=None),
            "legs_count": legs_count,
        }

    def _get(self, source: Any, *keys: str, default: Any = None) -> Any:
        if source is None:
            return default

        for key in keys:
            if isinstance(source, dict) and key in source:
                return source[key]

            if hasattr(source, key):
                return getattr(source, key)

        return default
