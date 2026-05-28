# services/market_snapshot_selector.py
"""
patch_13 — Política de precedência de snapshots: manual > rtd.

Para cada aba:
  - Se existir snapshot manual → usa manual
  - Caso contrário             → usa rtd

O selector não decide quais abas existem — apenas escolhe a fonte.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from domain.market_snapshot import LegMarketSnapshot, SnapshotSource
from repositories.market_snapshot_repository import MarketSnapshotRepository


@dataclass
class SnapshotSelectionResult:
    """Resultado da seleção de snapshots para uma aba."""

    aba             : str
    source          : SnapshotSource
    legs            : list[LegMarketSnapshot] = field(default_factory=list)
    manual_overrides: list[str]               = field(default_factory=list)  # ativos onde manual venceu

    @property
    def is_manual_first(self) -> bool:
        return self.source == SnapshotSource.MANUAL or bool(self.manual_overrides)


class MarketSnapshotSelector:
    """
    Aplica a política manual > rtd para selecionar o snapshot canônico.

    Args:
        repository: Instância de MarketSnapshotRepository.
    """

    def __init__(self, repository: MarketSnapshotRepository) -> None:
        self._repo = repository

    def select(self, aba: str) -> SnapshotSelectionResult:
        """
        Seleciona as legs canônicas para a aba informada.

        Regra:
            1. Busca legs manuais  (manual_analise_robo_legs)
            2. Busca legs RTD      (rtd_analise_robo_legs)
            3. Para cada ativo presente nas duas fontes → manual vence
            4. Ativos só no RTD   → usa RTD
            5. Ativos só manual   → usa manual

        Returns:
            SnapshotSelectionResult com a lista final de legs e metadados.
        """
        manual_legs = self._repo.get_manual_legs(aba)
        rtd_legs    = self._repo.get_rtd_legs(aba)

        # Indexa por ativo para facilitar merge
        manual_by_ativo: dict[str, LegMarketSnapshot] = {
            l.ativo: l for l in manual_legs if l.ativo
        }
        rtd_by_ativo: dict[str, LegMarketSnapshot] = {
            l.ativo: l for l in rtd_legs if l.ativo
        }

        todos_ativos  = sorted(set(manual_by_ativo) | set(rtd_by_ativo))
        legs_selected : list[LegMarketSnapshot] = []
        overrides     : list[str] = []

        for ativo in todos_ativos:
            if ativo in manual_by_ativo:
                legs_selected.append(manual_by_ativo[ativo])
                if ativo in rtd_by_ativo:
                    overrides.append(ativo)   # manual sobrepôs rtd
            else:
                legs_selected.append(rtd_by_ativo[ativo])

        # Fonte predominante
        source = SnapshotSource.MANUAL if manual_legs else SnapshotSource.RTD

        return SnapshotSelectionResult(
            aba              = aba,
            source           = source,
            legs             = legs_selected,
            manual_overrides = overrides,
        )
