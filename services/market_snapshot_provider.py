from datetime import date
from typing import Any, Callable


DEFAULT_MARKET_BY_ASSET: dict[str, dict[str, Any]] = {
    "BOVA11": {
        "spot_price": 198.35,
        "interest_rate": 0.1175,
        "volatility": 0.22,
    },
    "SMAL11": {
        "spot_price": 124.66,
        "interest_rate": 0.1175,
        "volatility": 0.30,
    },
    "SBSP3": {
        "spot_price": 168.67,
        "interest_rate": 0.1175,
        "volatility": 0.28,
    },
    "PRIO3": {
        "spot_price": 66.84,
        "interest_rate": 0.1175,
        "volatility": 0.35,
    },
    "EMBJ3": {
        "spot_price": 87.37,
        "interest_rate": 0.1175,
        "volatility": 0.32,
    },
    "PETR4": {
        "spot_price": 37.42,
        "interest_rate": 0.1175,
        "volatility": 0.31,
    },
    "VALE3": {
        "spot_price": 61.80,
        "interest_rate": 0.1175,
        "volatility": 0.28,
    },
}


class MarketSnapshotProvider:
    def __init__(
        self,
        market_by_asset: dict[str, dict[str, Any]] | None = None,
        today_provider: Callable[[], date] | None = None,
    ):
        self.market_by_asset = market_by_asset or DEFAULT_MARKET_BY_ASSET
        self.today_provider = today_provider or date.today

    def get_snapshot(self, underlying_asset: str, reference_date: str | None = None) -> dict[str, Any]:
        asset = str(underlying_asset or "").strip().upper()
        if not asset:
            raise ValueError("underlying_asset is required")

        market = self.market_by_asset.get(asset)
        if market is None:
            raise ValueError(f"market snapshot not found for asset: {asset}")

        effective_reference_date = reference_date or self.today_provider().isoformat()

        return {
            "reference_date": effective_reference_date,
            "underlying_asset": asset,
            "spot_price": float(market["spot_price"]),
            "interest_rate": float(market["interest_rate"]),
            "volatility": float(market["volatility"]),
        }
