# services/market_snapshot_selector.py
"""
Política de precedência de snapshots: manual > rtd_option_quotes > rtd.

Para cada aba:
  - Se existir snapshot manual para o ativo, usa manual
  - Caso contrário, se existir cotação em rtd_option_quotes para a leg RTD, usa rtd_option_quotes
  - Caso contrário, usa rtd_analise_robo_legs
"""
from __future__ import annotations

from dataclasses import dataclass, field

from domain.market_snapshot import LegMarketSnapshot, SnapshotSource
from repositories.market_snapshot_repository import MarketSnapshotRepository
from domain.refs.structure_ref import StructureRef


RTD_OPTION_QUOTES_SOURCE = "rtd_option_quotes"


def _ref_to_aba(ref: StructureRef | str | int) -> str:
    """
    Fallback local para obter um rótulo de aba.

    A resolução real structure_id -> alias_legacy_aba deve ser feita pelo
    repository quando ele expõe resolve_aba(). Este helper preserva compatibilidade
    para testes/fakes e para chamadas legadas por aba.
    """
    if isinstance(ref, StructureRef):
        if ref.aba:
            return str(ref.aba)
        if ref.structure_id is not None:
            return str(ref.structure_id)
        raise ValueError("StructureRef precisa ter aba ou structure_id.")
    return str(ref)


@dataclass
class SnapshotSelectionResult:
    """Resultado da seleção de snapshots para uma aba."""

    aba: str
    source: SnapshotSource | str
    legs: list[LegMarketSnapshot] = field(default_factory=list)
    manual_overrides: list[str] = field(default_factory=list)

    @property
    def is_manual_first(self) -> bool:
        return self.source == SnapshotSource.MANUAL or bool(self.manual_overrides)


class MarketSnapshotSelector:
    """
    Aplica a política manual > rtd_option_quotes > rtd para selecionar o snapshot canônico.
    """

    def __init__(self, repository: MarketSnapshotRepository) -> None:
        self._repo = repository

    def select(
        self,
        ref: StructureRef | str | int | None = None,
        *,
        aba: str | None = None,
        structure_id: int | None = None,
    ) -> SnapshotSelectionResult:
        """
        Seleciona as legs canônicas para a estrutura informada.

        Compatibilidade:
          - select(ref=StructureRef(...))
          - select(StructureRef(...))
          - select(aba="SMAL11")
          - select("SMAL11")
          - select(structure_id=123)
          - select(StructureRef.from_id(123))
        """
        if ref is None and aba is None and structure_id is None:
            raise ValueError("Informe ref, aba ou structure_id para selecionar snapshot.")

        if ref is not None:
            effective_ref: StructureRef | str | int = ref
        elif structure_id is not None:
            effective_ref = StructureRef.from_id(int(structure_id))
        else:
            effective_ref = aba

        resolve_aba = getattr(self._repo, "resolve_aba", None)
        if callable(resolve_aba):
            aba_str = resolve_aba(effective_ref)
        else:
            aba_str = _ref_to_aba(effective_ref)

        manual_legs = self._repo.get_manual_legs(effective_ref)
        rtd_legs = self._repo.get_rtd_legs(effective_ref)

        get_rtd_option_quote_legs = getattr(
            self._repo,
            "get_rtd_option_quote_legs",
            None,
        )
        if callable(get_rtd_option_quote_legs):
            rtd_option_quote_legs = get_rtd_option_quote_legs(effective_ref)
        else:
            rtd_option_quote_legs = []

        # Como as consultas vêm em timestamp DESC, preserva a primeira ocorrência
        # por ativo, que tende a ser a mais recente.

        manual_by_ativo: dict[str, LegMarketSnapshot] = {}
        for leg in manual_legs:
            if leg.ativo and leg.ativo not in manual_by_ativo:
                manual_by_ativo[leg.ativo] = leg

        rtd_option_quote_by_ativo: dict[str, LegMarketSnapshot] = {}
        for leg in rtd_option_quote_legs:
            if leg.ativo and leg.ativo not in rtd_option_quote_by_ativo:
                rtd_option_quote_by_ativo[leg.ativo] = leg

        rtd_by_ativo: dict[str, LegMarketSnapshot] = {}
        for leg in rtd_legs:
            if leg.ativo and leg.ativo not in rtd_by_ativo:
                rtd_by_ativo[leg.ativo] = leg

        todos_ativos = sorted(
            set(manual_by_ativo)
            | set(rtd_option_quote_by_ativo)
            | set(rtd_by_ativo)
        )

        legs_selected: list[LegMarketSnapshot] = []
        overrides: list[str] = []

        for ativo in todos_ativos:
            if ativo in manual_by_ativo:
                legs_selected.append(manual_by_ativo[ativo])
                if ativo in rtd_option_quote_by_ativo or ativo in rtd_by_ativo:
                    overrides.append(ativo)
            elif ativo in rtd_option_quote_by_ativo:
                legs_selected.append(rtd_option_quote_by_ativo[ativo])
            else:
                legs_selected.append(rtd_by_ativo[ativo])

        if manual_legs:
            source: SnapshotSource | str = SnapshotSource.MANUAL
        elif rtd_option_quote_legs:
            source = RTD_OPTION_QUOTES_SOURCE
        else:
            source = SnapshotSource.RTD

        return SnapshotSelectionResult(
            aba=aba_str,
            source=source,
            legs=legs_selected,
            manual_overrides=overrides,
        )
