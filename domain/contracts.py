from dataclasses import dataclass, field
from typing import Any


@dataclass
class CanonicalLeg:
    position_side: str
    option_type: str
    symbol: str | None
    strike: float
    expiration_date: str | None
    quantity: float
    premium: float | None
    multiplier: float = 1.0


@dataclass
class CanonicalStructure:
    structure_id: int
    name: str
    underlying_asset: str
    legs: list[CanonicalLeg] = field(default_factory=list)


@dataclass
class CanonicalMarket:
    reference_date: str
    underlying_asset: str
    spot_price: float
    interest_rate: float | None = None
    volatility: float | None = None


@dataclass
class CanonicalMeta:
    reference_date: str | None = None
    legs_source: str | None = None
    legacy_timestamp: str | None = None
    input_source: str | None = None


@dataclass
class CanonicalStructureMarketInput:
    structure: CanonicalStructure
    market: CanonicalMarket
    meta: CanonicalMeta | None = None

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "CanonicalStructureMarketInput":
        structure_raw = payload.get("structure") or {}
        market_raw = payload.get("market") or {}
        meta_raw = payload.get("meta") or {}

        legs = [
            CanonicalLeg(
                position_side=leg.get("position_side"),
                option_type=leg.get("option_type"),
                symbol=leg.get("symbol"),
                strike=float(leg.get("strike")),
                expiration_date=leg.get("expiration_date"),
                quantity=float(leg.get("quantity")),
                premium=leg.get("premium"),
                multiplier=float(leg.get("multiplier", 1.0)),
            )
            for leg in structure_raw.get("legs", [])
        ]

        structure = CanonicalStructure(
            structure_id=int(structure_raw.get("structure_id")),
            name=structure_raw.get("name"),
            underlying_asset=structure_raw.get("underlying_asset"),
            legs=legs,
        )

        market = CanonicalMarket(
            reference_date=market_raw.get("reference_date"),
            underlying_asset=market_raw.get("underlying_asset"),
            spot_price=float(market_raw.get("spot_price")),
            interest_rate=market_raw.get("interest_rate"),
            volatility=market_raw.get("volatility"),
        )

        meta = CanonicalMeta(
            reference_date=meta_raw.get("reference_date"),
            legs_source=meta_raw.get("legs_source"),
            legacy_timestamp=meta_raw.get("legacy_timestamp"),
            input_source=meta_raw.get("input_source"),
        )

        return cls(
            structure=structure,
            market=market,
            meta=meta,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "structure": {
                "structure_id": self.structure.structure_id,
                "name": self.structure.name,
                "underlying_asset": self.structure.underlying_asset,
                "legs": [
                    {
                        "position_side": leg.position_side,
                        "option_type": leg.option_type,
                        "symbol": leg.symbol,
                        "strike": leg.strike,
                        "expiration_date": leg.expiration_date,
                        "quantity": leg.quantity,
                        "premium": leg.premium,
                        "multiplier": leg.multiplier,
                    }
                    for leg in self.structure.legs
                ],
            },
            "market": {
                "reference_date": self.market.reference_date,
                "underlying_asset": self.market.underlying_asset,
                "spot_price": self.market.spot_price,
                "interest_rate": self.market.interest_rate,
                "volatility": self.market.volatility,
            },
            "meta": {
                "reference_date": self.meta.reference_date if self.meta else None,
                "legs_source": self.meta.legs_source if self.meta else None,
                "legacy_timestamp": self.meta.legacy_timestamp if self.meta else None,
                "input_source": self.meta.input_source if self.meta else None,
            },
        }
