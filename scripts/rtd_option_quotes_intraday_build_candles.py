from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from services.rtd_option_quotes_intraday_candle_service import (
    RtdOptionQuotesIntradayCandleService,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Gera candles intraday a partir do historico RTD capturado"
    )
    parser.add_argument("--db", required=True, help="Caminho do banco SQLite")
    parser.add_argument("--symbol", required=False, help="Simbolo opcional")
    parser.add_argument(
        "--interval-minutes",
        type=int,
        default=1,
        choices=[1, 5, 15],
        help="Intervalo do candle em minutos",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Calcula sem persistir",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    service = RtdOptionQuotesIntradayCandleService()
    candles = service.build_candles_from_history(
        Path(args.db),
        symbol=args.symbol,
        interval_minutes=args.interval_minutes,
    )

    print(f"candles_calculados={len(candles)}")
    print(f"interval_minutes={args.interval_minutes}")

    if args.symbol:
        print(f"symbol={args.symbol}")

    if args.dry_run:
        print("dry_run=sim")
        return 0

    persisted = service.persist_candles(Path(args.db), candles)
    print(f"candles_gravados={persisted}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
