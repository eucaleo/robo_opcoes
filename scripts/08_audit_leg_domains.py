from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from infra.sqlite_conn import sqlite_conn


APP_DB = "./dados/app.db"
TABLES = [
    "manual_analise_robo_legs",
    "rtd_analise_robo_legs",
]


def is_blank(value: Any) -> bool:
    return value is None or str(value).strip() == ""


def try_float(value: Any) -> bool:
    if value is None:
        return False
    s = str(value).strip().replace(",", ".")
    if not s:
        return False
    try:
        float(s)
        return True
    except Exception:
        return False


def try_int(value: Any) -> bool:
    if value is None:
        return False
    s = str(value).strip().replace(",", ".")
    if not s:
        return False
    try:
        f = float(s)
        return f.is_integer()
    except Exception:
        return False


def fetch_rows(conn, table: str) -> List[dict]:
    rows = conn.execute(
        f"""
        SELECT aba, timestamp, cv, call_put, strike, quant, ativo, vencimento
        FROM {table}
        """
    ).fetchall()
    return [dict(r) for r in rows]


def summarize_rows(rows: List[dict]) -> Dict[str, Any]:
    cv_counter = Counter()
    cp_counter = Counter()
    ativo_counter = Counter()

    blanks = Counter()
    invalids = Counter()

    strike_samples_invalid = []
    quant_samples_invalid = []
    ativo_blank_samples = []

    for row in rows:
        cv = row.get("cv")
        cp = row.get("call_put")
        strike = row.get("strike")
        quant = row.get("quant")
        ativo = row.get("ativo")

        cv_key = "<blank>" if is_blank(cv) else str(cv).strip()
        cp_key = "<blank>" if is_blank(cp) else str(cp).strip()
        ativo_key = "<blank>" if is_blank(ativo) else str(ativo).strip()

        cv_counter[cv_key] += 1
        cp_counter[cp_key] += 1
        ativo_counter[ativo_key] += 1

        if is_blank(cv):
            blanks["cv"] += 1
        if is_blank(cp):
            blanks["call_put"] += 1
        if is_blank(strike):
            blanks["strike"] += 1
        if is_blank(quant):
            blanks["quant"] += 1
        if is_blank(ativo):
            blanks["ativo"] += 1
            if len(ativo_blank_samples) < 10:
                ativo_blank_samples.append(repr(row))

        if not is_blank(strike) and not try_float(strike):
            invalids["strike_not_numeric"] += 1
            if len(strike_samples_invalid) < 10:
                strike_samples_invalid.append(repr(row))

        if not is_blank(quant) and not try_int(quant):
            invalids["quant_not_integer"] += 1
            if len(quant_samples_invalid) < 10:
                quant_samples_invalid.append(repr(row))

        if try_float(strike):
            if float(str(strike).strip().replace(",", ".")) <= 0:
                invalids["strike_non_positive"] += 1

        if try_float(quant):
            if float(str(quant).strip().replace(",", ".")) <= 0:
                invalids["quant_non_positive"] += 1

    return {
        "total_rows": len(rows),
        "cv_counter": cv_counter,
        "cp_counter": cp_counter,
        "ativo_counter": ativo_counter,
        "blanks": blanks,
        "invalids": invalids,
        "strike_samples_invalid": strike_samples_invalid,
        "quant_samples_invalid": quant_samples_invalid,
        "ativo_blank_samples": ativo_blank_samples,
    }


def print_counter(title: str, counter: Counter, limit: int = 20) -> None:
    print(title)
    if not counter:
        print("  - nenhum")
        return
    for key, count in counter.most_common(limit):
        print(f"  - {key}: {count}")


def print_summary(table: str, summary: Dict[str, Any]) -> None:
    print("=" * 80)
    print(f"TABELA: {table}")
    print(f"TOTAL_ROWS: {summary['total_rows']}")
    print()

    print_counter("CV VALUES:", summary["cv_counter"])
    print()
    print_counter("CALL_PUT VALUES:", summary["cp_counter"])
    print()
    print_counter("ATIVO VALUES:", summary["ativo_counter"])
    print()
    print_counter("BLANK COUNTS:", summary["blanks"])
    print()
    print_counter("INVALID COUNTS:", summary["invalids"])
    print()

    print("INVALID STRIKE SAMPLES:")
    if summary["strike_samples_invalid"]:
        for s in summary["strike_samples_invalid"]:
            print(f"  - {s}")
    else:
        print("  - nenhuma")
    print()

    print("INVALID QUANT SAMPLES:")
    if summary["quant_samples_invalid"]:
        for s in summary["quant_samples_invalid"]:
            print(f"  - {s}")
    else:
        print("  - nenhuma")
    print()

    print("BLANK ATIVO SAMPLES:")
    if summary["ativo_blank_samples"]:
        for s in summary["ativo_blank_samples"]:
            print(f"  - {s}")
    else:
        print("  - nenhuma")


def main() -> int:
    print("== AUDIT LEG DOMAINS ==")
    print(f"PROJECT_ROOT: {PROJECT_ROOT}")
    print(f"DB: {APP_DB}")
    print()

    with sqlite_conn(APP_DB) as conn:
        for table in TABLES:
            rows = fetch_rows(conn, table)
            summary = summarize_rows(rows)
            print_summary(table, summary)
            print()

    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
