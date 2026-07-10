#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


from services.excel_rtd_reader import read_excel_rtd_options_as_dict


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workbook", default="LISTA_RTD.xlsm")
    parser.add_argument("--sheet", default="RTD_OPTION_QUOTES")
    parser.add_argument("--min-records", type=int, default=1)
    parser.add_argument("--output", default="")
    args = parser.parse_args()

    result = read_excel_rtd_options_as_dict(
        workbook_name=args.workbook,
        sheet_name=args.sheet,
    )

    safe_result = dict(result)
    safe_result["sample_records"] = safe_result.get("records", [])[:5]
    safe_result.pop("records", None)

    output_text = json.dumps(safe_result, ensure_ascii=False, indent=2)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output_text + "\n", encoding="utf-8")

    print(output_text)

    if not result.get("ok"):
        return 2

    record_count = int(result.get("record_count") or 0)

    if record_count < args.min_records:
        print(
            "falha: quantidade de registros menor que o minimo esperado",
            file=sys.stderr,
        )
        return 3

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
