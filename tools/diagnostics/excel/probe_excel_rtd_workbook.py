from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from services.excel_rtd_workbook_probe import (  # noqa: E402
    DEFAULT_WORKBOOK_NAME,
    ExcelRtdWorkbookProbe,
    ExcelRtdWorkbookProbeConfig,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Diagnostica o workbook RTD aberto no Excel sem gravar banco."
    )
    parser.add_argument(
        "--workbook",
        default=DEFAULT_WORKBOOK_NAME,
        help="Nome do workbook alvo. Padrao: LISTA_RTD.xlsm",
    )
    parser.add_argument(
        "--sheet",
        default=None,
        help="Aba preferencial. Se omitida, usa a primeira aba encontrada.",
    )
    parser.add_argument(
        "--max-rows",
        type=int,
        default=8,
        help="Quantidade maxima de linhas para amostra.",
    )
    parser.add_argument(
        "--max-cols",
        type=int,
        default=40,
        help="Quantidade maxima de colunas para amostra.",
    )

    args = parser.parse_args()

    probe = ExcelRtdWorkbookProbe(
        config=ExcelRtdWorkbookProbeConfig(
            workbook_name=args.workbook,
            preferred_sheet=args.sheet,
            max_rows=args.max_rows,
            max_cols=args.max_cols,
        )
    )

    result = probe.run()

    print(json.dumps(asdict(result), ensure_ascii=False, indent=2))

    return 0 if result.ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
