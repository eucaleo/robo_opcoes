from types import SimpleNamespace

from domain.market_snapshot import SnapshotSource
from services.market_snapshot_selector import MarketSnapshotSelector


def _leg(ativo, source, valor_executado):
    return SimpleNamespace(
        ativo=ativo,
        source=source,
        valor_executado=valor_executado,
    )


class FakeMarketSnapshotRepository:
    def __init__(self, *, manual=None, rtd_option_quotes=None, rtd=None):
        self.manual = manual or []
        self.rtd_option_quotes = rtd_option_quotes or []
        self.rtd = rtd or []

    def get_manual_legs(self, ref):
        return self.manual

    def get_rtd_option_quote_legs(self, ref):
        return self.rtd_option_quotes

    def get_rtd_legs(self, ref):
        return self.rtd


def test_selector_prioritizes_rtd_option_quotes_over_legacy_rtd_when_no_manual_exists():
    legacy_rtd_leg = _leg("BOVAE195", "rtd", 1.10)
    quote_leg = _leg("BOVAE195", "rtd_option_quotes", 1.23)

    selector = MarketSnapshotSelector(
        repository=FakeMarketSnapshotRepository(
            rtd=[legacy_rtd_leg],
            rtd_option_quotes=[quote_leg],
        )
    )

    result = selector.select(aba="BOVA11")

    assert result.aba == "BOVA11"
    assert result.source == "rtd_option_quotes"
    assert result.legs == [quote_leg]
    assert result.manual_overrides == []


def test_selector_keeps_manual_leg_ahead_of_rtd_option_quotes():
    manual_leg = _leg("BOVAE195", "manual", 1.30)
    quote_leg = _leg("BOVAE195", "rtd_option_quotes", 1.23)
    legacy_rtd_leg = _leg("BOVAE195", "rtd", 1.10)

    selector = MarketSnapshotSelector(
        repository=FakeMarketSnapshotRepository(
            manual=[manual_leg],
            rtd_option_quotes=[quote_leg],
            rtd=[legacy_rtd_leg],
        )
    )

    result = selector.select(aba="BOVA11")

    assert result.aba == "BOVA11"
    assert result.source == SnapshotSource.MANUAL
    assert result.legs == [manual_leg]
    assert result.manual_overrides == ["BOVAE195"]
