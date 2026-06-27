from datetime import date
import os
import sqlite3
from pathlib import Path
from typing import Any, Callable


DEFAULT_INTEREST_RATE = 0.1175
DEFAULT_VOLATILITY = 0.30


DEFAULT_MARKET_BY_ASSET: dict[str, dict[str, Any]] = {
    "BOVA11": {
        "interest_rate": 0.1175,
        "volatility": 0.22,
    },
    "SMAL11": {
        "interest_rate": 0.1175,
        "volatility": 0.30,
    },
    "SBSP3": {
        "interest_rate": 0.1175,
        "volatility": 0.28,
    },
    "PRIO3": {
        "interest_rate": 0.1175,
        "volatility": 0.35,
    },
    "EMBJ3": {
        "interest_rate": 0.1175,
        "volatility": 0.32,
    },
    "PETR4": {
        "interest_rate": 0.1175,
        "volatility": 0.31,
    },
    "VALE3": {
        "interest_rate": 0.1175,
        "volatility": 0.28,
    },
}


def _env_allows_static_fallback() -> bool:
    raw = os.getenv("MYHUBIA_ALLOW_STATIC_MARKET_SNAPSHOT", "")
    return raw.strip().lower() in {"1", "true", "yes", "sim"}


def _default_db_path() -> Path:
    return Path(os.getenv("MYHUBIA_DB_PATH", "dados/app.db"))


class MarketSnapshotProvider:
    def __init__(
        self,
        market_by_asset: dict[str, dict[str, Any]] | None = None,
        today_provider: Callable[[], date] | None = None,
        allow_static_fallback: bool | None = None,
        db_path: str | Path | None = None,
    ):
        self.market_by_asset = market_by_asset
        self.today_provider = today_provider or date.today
        self.db_path = Path(db_path) if db_path is not None else _default_db_path()

        if allow_static_fallback is None:
            allow_static_fallback = _env_allows_static_fallback()

        self.allow_static_fallback = bool(allow_static_fallback)

    def get_snapshot(self, underlying_asset: str, reference_date: str | None = None) -> dict[str, Any]:
        asset = str(underlying_asset or '').strip().upper()
        if not asset:
            raise ValueError("underlying_asset is required")

        effective_reference_date = reference_date or self.today_provider().isoformat()

        if self.market_by_asset is not None:
            return self._snapshot_from_injected_market(asset, effective_reference_date)

        db_snapshot = self._snapshot_from_rtd_underlying_quotes(asset, effective_reference_date)
        if db_snapshot is not None:
            return db_snapshot

        if self.allow_static_fallback:
            return self._snapshot_from_static_fallback(asset, effective_reference_date)

        raise ValueError(
            "market snapshot real/atual ausente para asset="
            f'{asset}. O fallback estático está bloqueado.'
        )

    def _snapshot_from_injected_market(
        self,
        asset: str,
        effective_reference_date: str,
    ) -> dict[str, Any]:
        market = self.market_by_asset.get(asset) if self.market_by_asset is not None else None
        if market is None:
            raise ValueError(f'market snapshot not found for asset: {asset}')

        return {
            "reference_date": effective_reference_date,
            "underlying_asset": asset,
            "spot_price": float(market["spot_price"]),
            "interest_rate": float(market.get("interest_rate", DEFAULT_INTEREST_RATE)),
            "volatility": float(market.get("volatility", DEFAULT_VOLATILITY)),
        }

    def _snapshot_from_rtd_underlying_quotes(
        self,
        asset: str,
        effective_reference_date: str,
    ) -> dict[str, Any] | None:
        if not self.db_path.exists():
            return None

        try:
            with sqlite3.connect(self.db_path) as con:
                con.row_factory = sqlite3.Row
                row = con.execute(
                    """
                    SELECT
                        ativo,
                        ultimo_preco,
                        source,
                        updated_at
                    FROM rtd_underlying_quotes
                    WHERE UPPER(ativo) = ?
                    ORDER BY updated_at DESC, id DESC
                    LIMIT 1
                    """,
                    (asset,),
                ).fetchone()
        except sqlite3.Error as exc:
            if self.allow_static_fallback:
                return None
            raise ValueError(
                f'erro ao consultar rtd_underlying_quotes para asset={asset}: {exc}'
            ) from exc

        if row is None:
            return None

        spot_price = row["ultimo_preco"]
        if spot_price is None or float(spot_price) <= 0:
            if self.allow_static_fallback:
                return None
            raise ValueError(
                f'rtd_underlying_quotes sem ultimo_preco válido para asset={asset}'
            )

        defaults = DEFAULT_MARKET_BY_ASSET.get(asset, {})

        return {
            "reference_date": effective_reference_date,
            "underlying_asset": asset,
            "spot_price": float(spot_price),
            "interest_rate": float(defaults.get("interest_rate", DEFAULT_INTEREST_RATE)),
            "volatility": float(defaults.get("volatility", DEFAULT_VOLATILITY)),
            "snapshot_source": "rtd_underlying_quotes",
            "market_snapshot_source": "rtd_underlying_quotes",
            "is_static_fallback": False,
            "is_current_market": True,
            "snapshot_warning": None,
            "market_snapshot_updated_at": row["updated_at"],
            "market_snapshot_rtd_source": row["source"],
        }

    def _snapshot_from_static_fallback(
        self,
        asset: str,
        effective_reference_date: str,
    ) -> dict[str, Any]:
        defaults = DEFAULT_MARKET_BY_ASSET.get(asset)
        if defaults is None:
            raise ValueError(f'market snapshot not found for asset: {asset}')

        raise ValueError(
            "market snapshot real/atual ausente para asset="
            f"{asset}. O fallback estático não fornece spot_price operacional."
        )

