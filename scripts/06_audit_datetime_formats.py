from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from infra.sqlite_conn import sqlite_conn
from utils.leg_normalizers import parse_timestamp


APP_DB = "./dados/app.db"

TABLES_AND_COLUMNS = [
    ("manual_analise_robo_legs", ["timestamp", "vencimento"]),
    ("rtd_analise_robo_legs", ["timestamp", "vencimento"]),
]


RE_BR_DATETIME = re.compile(r"^\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2}:\d{2}$")
RE_BR_DATE = re.compile(r"^\d{2}/\d{2}/\d{4}$")
RE_ISO_DATETIME = re.compile(r"^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}(\.\d+)?$")
RE_ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
RE_EXCEL_SERIAL = re.compile(r"^\d+(?:[.,]\d+)?$")


def classify_datetime_value(value: Any) -> str:
    if value is None:
        return "null"

    s = str(value).strip()
    if not s:
        return "blank"

    if RE_BR_DATETIME.match(s):
        return "br_datetime"

    if RE_BR_DATE.match(s):
        return "br_date"

    if RE_ISO_DATETIME.match(s):
        return "iso_datetime"

    if RE_ISO_DATE.match(s):
        return "iso_date"

    if RE_EXCEL_SERIAL.match(s):
        return "excel_serial"

    return "other"


def try_parse(value: Any) -> Tuple[bool, str]:
    try:
        dt = parse_timestamp(value)
        return True, dt.isoformat(sep=" ")
    except Exception as e:
        return False, str(e)


def fetch_column_values(conn, table: str, column: str) -> List[Any]:
    rows = conn.execute(f"SELECT {column} FROM {table}").fetchall()
    return [r[column] for r in rows]


def summarize_values(values: Iterable[Any]) -> Dict[str, Any]:
    class_counter = Counter()
    parse_ok = 0
    parse_fail = 0
    samples_by_class: Dict[str, List[str]] = {}
    fail_samples: List[str] = []

    total = 0
    for value in values:
        total += 1
        cls = classify_datetime_value(value)
        class_counter[cls] += 1

        if cls not in samples_by_class:
            samples_by_class[cls] = []

        s = repr(value)
        if len(samples_by_class[cls]) < 5 and s not in samples_by_class[cls]:
            samples_by_class[cls].append(s)

        ok, result = try_parse(value)
        if ok:
            parse_ok += 1
        else:
            parse_fail += 1
            sample = f"value={value!r} err={result}"
            if len(fail_samples) < 10 and sample not in fail_samples:
                fail_samples.append(sample)

    return {
        "total": total,
        "class_counter": class_counter,
        "parse_ok": parse_ok,
        "parse_fail": parse_fail,
        "samples_by_class": samples_by_class,
        "fail_samples": fail_samples,
    }


def print_summary(table: str, column: str, summary: Dict[str, Any]) -> None:
    print("=" * 80)
    print(f"TABELA : {table}")
    print(f"COLUNA : {column}")
    print(f"TOTAL  : {summary['total']}")
    print(f"PARSE_OK   : {summary['parse_ok']}")
    print(f"PARSE_FAIL : {summary['parse_fail']}")
    print()

    print("CLASSIFICAÇÃO:")
    for cls, count in summary["class_counter"].most_common():
        print(f"  - {cls:15s} {count}")

    print()
    print("EXEMPLOS POR CLASSE:")
    for cls, samples in summary["samples_by_class"].items():
        print(f"  [{cls}]")
        for sample in samples:
            print(f"    - {sample}")

    print()
    print("FALHAS DE PARSE:")
    if summary["fail_samples"]:
        for sample in summary["fail_samples"]:
            print(f"  - {sample}")
    else:
        print("  - nenhuma")


def main() -> int:
    print("== AUDIT DATETIME FORMATS ==")
    print(f"PROJECT_ROOT: {PROJECT_ROOT}")
    print(f"DB: {APP_DB}")
    print()

    with sqlite_conn(APP_DB) as conn:
        for table, columns in TABLES_AND_COLUMNS:
            for column in columns:
                values = fetch_column_values(conn, table, column)
                summary = summarize_values(values)
                print_summary(table, column, summary)
                print()

    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
