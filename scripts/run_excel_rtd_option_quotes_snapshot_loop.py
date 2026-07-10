#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


from services.excel_rtd_reader import DEFAULT_SHEET_NAME, DEFAULT_WORKBOOK_NAME
from services.rtd_option_quotes_sync_service import sync_rtd_option_quotes_from_excel


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Mantem rtd_option_quotes atualizado a partir do Excel RTD vivo."
    )

    parser.add_argument(
        "--db",
        default="dados/app.db",
        help="Caminho do banco SQLite. Padrao: dados/app.db",
    )

    parser.add_argument(
        "--workbook",
        default=DEFAULT_WORKBOOK_NAME,
        help=f"Nome ou caminho do workbook. Padrao: {DEFAULT_WORKBOOK_NAME}",
    )

    parser.add_argument(
        "--sheet",
        default=DEFAULT_SHEET_NAME,
        help=f"Nome da aba. Padrao: {DEFAULT_SHEET_NAME}",
    )

    parser.add_argument(
        "--interval-seconds",
        type=float,
        default=2.0,
        help="Intervalo entre leituras. Padrao: 2.0",
    )

    parser.add_argument(
        "--max-iterations",
        type=int,
        default=0,
        help="Limite de ciclos. Zero significa rodar ate interromper.",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    db_path = Path(args.db)
    if not db_path.is_absolute():
        db_path = ROOT / db_path

    iteration = 0

    while True:
        iteration += 1

        result = sync_rtd_option_quotes_from_excel(
            db_path=db_path,
            workbook_name=args.workbook,
            sheet_name=args.sheet,
        )

        payload = result.to_dict()
        payload["iteration"] = iteration

        print(json.dumps(payload, ensure_ascii=False), flush=True)

        if args.max_iterations and iteration >= int(args.max_iterations):
            return 0 if result.ok else 1

        time.sleep(float(args.interval_seconds))


if __name__ == "__main__":
    raise SystemExit(main())
