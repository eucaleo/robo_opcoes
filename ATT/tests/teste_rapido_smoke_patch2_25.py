# ATT/tests/teste_rapido_smoke_patch2_25.py
"""
Smoke tests — patch_25
Cobertura:
  [S01] Provider retorna contrato completo (5 campos obrigatórios)
  [S02] Provider falha para ativo desconhecido
  [S03] Provider usa reference_date injetada
  [S04] Provider infere reference_date via today_provider
  [S05] _resolve_snapshot sem selector → legs vêm do provider (lista vazia)
  [S06] _resolve_snapshot com selector e aba → legs vêm do selector
  [S07] _resolve_snapshot com selector mas sem aba → legs do provider
  [S08] _resolve_snapshot com selector → snapshot_source correto no meta
  [S09] snapshot final sempre tem os 5 campos obrigatórios do assembler
  [S10] build_structure_market_input → meta contém reference_date
  [S11] build_structure_market_input → meta contém snapshot_source
  [S12] build_structure_market_input → structure not found levanta ValueError
  [S13] _resolve_legs_via_selector serializa todos os 23 campos de LegMarketSnapshot
  [S14] _resolve_legs_via_selector → manual_overrides refletidos no meta
  [S15] _reference_date_from_legs retorna None se legs sem timestamp
  [S16] _reference_date_from_legs retorna YYYY-MM-DD do timestamp mais recente
  [S17] SnapshotSource.MANUAL serializado como string "manual" na leg
  [S18] SnapshotSource.RTD serializado como string "rtd" na leg
  [S19] Selector não é chamado quando aba é string vazia
  [S20] _resolve_legs_via_selector com 0 legs retorna lista vazia e meta válido
"""

from __future__ import annotations

from datetime import date
from unittest.mock import MagicMock, patch

import pytest

# ── domínio ───────────────────────────────────────────────────────────────────
from domain.market_snapshot import LegMarketSnapshot, SnapshotSource

# ── serviços ──────────────────────────────────────────────────────────────────
from services.canonical_input_service import CanonicalInputService
from services.market_snapshot_provider import MarketSnapshotProvider
from services.market_snapshot_selector import (
    MarketSnapshotSelector,
    SnapshotSelectionResult,
)


# ─────────────────────────────────────────────────────────────────────────────
# Constantes de teste
# ─────────────────────────────────────────────────────────────────────────────

_ASSET       = "PETR4"
_ABA         = "PETR4_TEST"
_FIXED_DATE  = "2025-05-28"
_FIXED_TODAY = date(2025, 5, 28)

_MARKET_DATA = {
    _ASSET: {
        "spot_price":    37.42,
        "interest_rate": 0.1175,
        "volatility":    0.31,
    }
}

# Todos os campos que _resolve_legs_via_selector deve serializar
_LEG_SERIALIZED_FIELDS = {
    "aba", "ativo", "source",
    "cv", "call_put", "quant", "valor_executado",
    "bid", "ask", "mid", "spread", "spread_pct",
    "iv", "delta", "gamma", "theta", "vega",
    "strike", "vencimento", "dte", "pl_realista",
    "timestamp",
}

# Campos obrigatórios do contrato do assembler
_ASSEMBLER_REQUIRED_FIELDS = {
    "reference_date", "underlying_asset",
    "spot_price", "interest_rate", "volatility",
}


# ─────────────────────────────────────────────────────────────────────────────
# Factories
# ─────────────────────────────────────────────────────────────────────────────

def _leg(
    ativo: str = "PETR4C37",
    source: SnapshotSource = SnapshotSource.RTD,
    timestamp: str | None = "2025-05-28 10:00:00",
) -> LegMarketSnapshot:
    """Cria LegMarketSnapshot com todos os campos preenchidos."""
    return LegMarketSnapshot(
        aba             = _ABA,
        ativo           = ativo,
        cv              = "C",
        call_put        = "call",
        quant           = 1.0,
        valor_executado = 1.20,
        bid             = 1.10,
        ask             = 1.30,
        mid             = 1.20,
        spread          = 0.20,
        spread_pct      = 0.1667,
        iv              = 0.31,
        delta           = 0.45,
        gamma           = 0.05,
        theta           = -0.02,
        vega            = 0.10,
        strike          = 37.0,
        vencimento      = "2025-07-18",
        dte             = 50.0,
        pl_realista     = None,
        timestamp       = timestamp,
        source          = source,
    )


def _selection(
    source: SnapshotSource = SnapshotSource.RTD,
    legs: list[LegMarketSnapshot] | None = None,
    manual_overrides: list[str] | None = None,
) -> SnapshotSelectionResult:
    return SnapshotSelectionResult(
        aba              = _ABA,
        source           = source,
        legs             = legs if legs is not None else [_leg()],
        manual_overrides = manual_overrides or [],
    )


def _provider() -> MarketSnapshotProvider:
    return MarketSnapshotProvider(
        market_by_asset = _MARKET_DATA,
        today_provider  = lambda: _FIXED_TODAY,
    )


def _mock_selector(result: SnapshotSelectionResult) -> MagicMock:
    sel = MagicMock(spec=MarketSnapshotSelector)
    sel.select.return_value = result
    return sel


def _mock_repo(asset: str = _ASSET, aba: str | None = _ABA) -> MagicMock:
    repo = MagicMock()
    repo.get_structure.return_value = {
        "id":                1,
        "name":              "Teste PETR4",
        "underlying_asset":  asset,
        "alias_legacy_aba":  aba,
        "legs":              [],
    }
    return repo


def _service(
    selector: MarketSnapshotSelector | MagicMock | None = None,
    repo: MagicMock | None = None,
    aba: str | None = _ABA,
) -> CanonicalInputService:
    """
    Monta CanonicalInputService com dependências falsas.
    O assembler é mockado para isolar a lógica de resolve/enrich.
    """
    svc = CanonicalInputService(
        repository               = repo or _mock_repo(aba=aba),
        market_snapshot_provider = _provider(),
        market_snapshot_selector = selector,
        robo_legs_service        = MagicMock(),
    )
    # Neutraliza o fallback legado (não é foco dos testes de snapshot)
    svc.legacy_robo_legs_fallback = MagicMock()
    svc.legacy_robo_legs_fallback.load.return_value = ([], {})
    return svc


def _assembled_stub() -> dict:
    """Retorno mínimo que o assembler precisa devolver para o service não quebrar."""
    return {
        "structure": {"underlying_asset": _ASSET},
        "market": {
            "reference_date":   _FIXED_DATE,
            "underlying_asset": _ASSET,
            "spot_price":       37.42,
            "interest_rate":    0.1175,
            "volatility":       0.31,
        },
        "meta": {"input_source": "structure_market_input_assembler"},
    }


# ─────────────────────────────────────────────────────────────────────────────
# [S01–S04] MarketSnapshotProvider
# ─────────────────────────────────────────────────────────────────────────────

class TestMarketSnapshotProvider:

    def test_s01_retorna_campos_obrigatorios(self):
        """[S01] get_snapshot retorna os 5 campos exigidos pelo assembler."""
        snap = _provider().get_snapshot(_ASSET, reference_date=_FIXED_DATE)

        assert snap["underlying_asset"] == _ASSET
        assert snap["reference_date"]   == _FIXED_DATE
        assert isinstance(snap["spot_price"],    float)
        assert isinstance(snap["interest_rate"], float)
        assert isinstance(snap["volatility"],    float)

    def test_s02_ativo_desconhecido_levanta_valueerror(self):
        """[S02] Ativo não cadastrado deve lançar ValueError."""
        with pytest.raises(ValueError, match="market snapshot not found"):
            _provider().get_snapshot("XPTO99")

    def test_s03_usa_reference_date_injetada(self):
        """[S03] reference_date explícita é preservada no retorno."""
        snap = _provider().get_snapshot(_ASSET, reference_date="2025-01-15")
        assert snap["reference_date"] == "2025-01-15"

    def test_s04_infere_reference_date_via_today_provider(self):
        """[S04] Sem reference_date → usa today_provider."""
        snap = _provider().get_snapshot(_ASSET)
        assert snap["reference_date"] == _FIXED_DATE


# ─────────────────────────────────────────────────────────────────────────────
# [S05–S09] _resolve_snapshot
# ─────────────────────────────────────────────────────────────────────────────

class TestResolveSnapshot:

    def _structure(self, aba: str | None = _ABA) -> dict:
        return {"underlying_asset": _ASSET, "alias_legacy_aba": aba}

    def test_s05_sem_selector_legs_vem_do_provider(self):
        """[S05] Sem selector → legs = [] e source = provider_legacy."""
        svc = _service(selector=None)
        snap, meta = svc._resolve_snapshot(self._structure(), _FIXED_DATE)

        assert snap["legs"] == []
        assert meta["snapshot_source"] == "provider_legacy"

    def test_s06_com_selector_e_aba_legs_vem_do_selector(self):
        """[S06] Com selector e aba válida → legs serializadas do selector."""
        leg = _leg()
        sel = _mock_selector(_selection(legs=[leg]))
        svc = _service(selector=sel)

        snap, _ = svc._resolve_snapshot(self._structure(), _FIXED_DATE)

        assert len(snap["legs"]) == 1
        assert snap["legs"][0]["ativo"] == leg.ativo
        sel.select.assert_called_once_with(_ABA)

    def test_s07_com_selector_mas_sem_aba_usa_provider(self):
        """[S07] Selector presente mas aba=None → selector NÃO é chamado."""
        sel = _mock_selector(_selection())
        svc = _service(selector=sel, aba=None)

        _, meta = svc._resolve_snapshot(self._structure(aba=None), _FIXED_DATE)

        sel.select.assert_not_called()
        assert meta["snapshot_source"] == "provider_legacy"

    def test_s08_snapshot_source_reflete_fonte_do_selector(self):
        """[S08] meta['snapshot_source'] == 'manual' quando selector retorna MANUAL."""
        sel = _mock_selector(_selection(source=SnapshotSource.MANUAL))
        svc = _service(selector=sel)

        _, meta = svc._resolve_snapshot(self._structure(), _FIXED_DATE)

        assert meta["snapshot_source"] == SnapshotSource.MANUAL.value  # "manual"

    def test_s09_snapshot_sempre_tem_campos_obrigatorios(self):
        """[S09] Os 5 campos do assembler presentes, com e sem selector."""
        for selector in [None, _mock_selector(_selection())]:
            svc = _service(selector=selector)
            snap, _ = svc._resolve_snapshot(self._structure(), _FIXED_DATE)
            missing = _ASSEMBLER_REQUIRED_FIELDS - snap.keys()
            assert not missing, f"Campos faltando (selector={selector}): {missing}"


# ─────────────────────────────────────────────────────────────────────────────
# [S10–S12] build_structure_market_input
# ─────────────────────────────────────────────────────────────────────────────

class TestBuildStructureMarketInput:

    def test_s10_meta_contem_reference_date(self):
        """[S10] meta.reference_date presente no resultado final."""
        svc = _service()
        with patch(
            "services.canonical_input_service.assemble_structure_market_input",
            return_value=_assembled_stub(),
        ):
            result = svc.build_structure_market_input(1, reference_date=_FIXED_DATE)

        assert result["meta"]["reference_date"] == _FIXED_DATE

    def test_s11_meta_contem_snapshot_source(self):
        """[S11] meta.snapshot_source presente no resultado final."""
        svc = _service()
        with patch(
            "services.canonical_input_service.assemble_structure_market_input",
            return_value=_assembled_stub(),
        ):
            result = svc.build_structure_market_input(1, reference_date=_FIXED_DATE)

        assert "snapshot_source" in result["meta"]

    def test_s12_structure_not_found_levanta_valueerror(self):
        """[S12] structure_id inexistente → ValueError com mensagem clara."""
        repo = MagicMock()
        repo.get_structure.return_value = None
        svc = _service(repo=repo)

        with pytest.raises(ValueError, match="structure not found"):
            svc.build_structure_market_input(999)


# ─────────────────────────────────────────────────────────────────────────────
# [S13–S14] _resolve_legs_via_selector
# ─────────────────────────────────────────────────────────────────────────────

class TestResolveLegsViaSelector:

    def test_s13_serializa_todos_os_campos(self):
        """[S13] Leg serializada contém os 23 campos do contrato."""
        sel = _mock_selector(_selection(legs=[_leg()]))
        svc = _service(selector=sel)

        legs_list, _ = svc._resolve_legs_via_selector(_ABA)

        assert len(legs_list) == 1
        missing = _LEG_SERIALIZED_FIELDS - legs_list[0].keys()
        assert not missing, f"Campos ausentes na serialização: {missing}"

    def test_s14_manual_overrides_refletidos_no_meta(self):
        """[S14] meta['manual_overrides'] e is_manual_first corretos."""
        leg_manual = _leg(source=SnapshotSource.MANUAL)
        sel = _mock_selector(_selection(
            source           = SnapshotSource.MANUAL,
            legs             = [leg_manual],
            manual_overrides = ["PETR4C37"],
        ))
        svc = _service(selector=sel)

        _, meta = svc._resolve_legs_via_selector(_ABA)

        assert "PETR4C37" in meta["manual_overrides"]
        assert meta["is_manual_first"] is True
        assert meta["snapshot_aba"]    == _ABA


# ─────────────────────────────────────────────────────────────────────────────
# [S15–S16] _reference_date_from_legs
# ─────────────────────────────────────────────────────────────────────────────

class TestReferenceDateFromLegs:

    def test_s15_retorna_none_se_sem_timestamp(self):
        """[S15] Todas as legs sem timestamp → retorna None."""
        legs = [_leg(timestamp=None), _leg(timestamp=None)]
        assert CanonicalInputService._reference_date_from_legs(legs) is None

    def test_s16_retorna_data_do_timestamp_mais_recente(self):
        """[S16] Retorna YYYY-MM-DD do max(timestamps)."""
        legs = [
            _leg(timestamp="2025-05-20 00:00:00"),
            _leg(timestamp="2025-05-28 14:30:00"),  # ← mais recente
            _leg(timestamp="2025-05-25 08:00:00"),
        ]
        assert CanonicalInputService._reference_date_from_legs(legs) == "2025-05-28"


# ─────────────────────────────────────────────────────────────────────────────
# [S17–S20] Edge cases
# ─────────────────────────────────────────────────────────────────────────────

class TestEdgeCases:

    def test_s17_source_manual_serializado_como_string(self):
        """[S17] source=MANUAL → serializado como 'manual' (não como Enum)."""
        sel = _mock_selector(_selection(
            source = SnapshotSource.MANUAL,
            legs   = [_leg(source=SnapshotSource.MANUAL)],
        ))
        svc = _service(selector=sel)

        legs_list, _ = svc._resolve_legs_via_selector(_ABA)

        assert legs_list[0]["source"] == "manual"
        assert isinstance(legs_list[0]["source"], str)

    def test_s18_source_rtd_serializado_como_string(self):
        """[S18] source=RTD → serializado como 'rtd' (não como Enum)."""
        sel = _mock_selector(_selection(legs=[_leg(source=SnapshotSource.RTD)]))
        svc = _service(selector=sel)

        legs_list, _ = svc._resolve_legs_via_selector(_ABA)

        assert legs_list[0]["source"] == "rtd"
        assert isinstance(legs_list[0]["source"], str)

    def test_s19_selector_nao_chamado_para_aba_vazia(self):
        """[S19] aba='' (string vazia) → trata como ausente, selector não chamado."""
        sel = _mock_selector(_selection())
        svc = _service(selector=sel, aba="")

        structure = {"underlying_asset": _ASSET, "alias_legacy_aba": ""}
        _, meta = svc._resolve_snapshot(structure, _FIXED_DATE)

        sel.select.assert_not_called()
        assert meta["snapshot_source"] == "provider_legacy"

    def test_s20_resolve_legs_com_zero_legs_retorna_lista_vazia(self):
        """[S20] Selector retorna 0 legs → lista vazia e meta válido."""
        sel = _mock_selector(_selection(legs=[]))
        svc = _service(selector=sel)

        legs_list, meta = svc._resolve_legs_via_selector(_ABA)

        assert legs_list == []
        assert meta["snapshot_source"] in ("rtd", "manual")
        assert "legs_reference_date" in meta
        assert meta["legs_reference_date"] is None
