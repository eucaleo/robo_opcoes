from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Tuple

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path
    sys.path.insert(0, str(PROJECT_ROOT))

from infra.sqlite_conn import sqlite_conn


APP_DB = .dadosapp.db
TABLES = [
    manual_analise_robo_legs,
    rtd_analise_robo_legs,
]


def is_blank(value Any) - bool
    return value is None or str(value).strip() == 


def fetch_rows(conn, table str) - List[dict]
    rows = conn.execute(
        f
        SELECT aba, timestamp
        FROM {table}
        
    ).fetchall()
    return [dict(r) for r in rows]


def summarize_table(rows List[dict]) - Dict[str, Any]
    total_rows = len(rows)

    abas = []
    timestamps = []
    pair_counter Counter[Tuple[str, str]] = Counter()

    blank_aba = 0
    blank_timestamp = 0
    blank_both = 0

    for row in rows
        aba = row.get(aba)
        ts = row.get(timestamp)

        aba_blank = is_blank(aba)
        ts_blank = is_blank(ts)

        if aba_blank
            blank_aba += 1
        if ts_blank
            blank_timestamp += 1
        if aba_blank and ts_blank
            blank_both += 1

        if not aba_blank
            abas.append(str(aba).strip())

        if not ts_blank
            timestamps.append(str(ts).strip())

        if not aba_blank and not ts_blank
            pair_counter[(str(aba).strip(), str(ts).strip())] += 1

    unique_abas = sorted(set(abas))
    unique_timestamps = sorted(set(timestamps))
    unique_pairs = list(pair_counter.keys())

    duplicated_pairs = [(pair, count) for pair, count in pair_counter.items() if count  1]
    duplicated_pairs.sort(key=lambda x (-x[1], x[0][0], x[0][1]))

    legs_per_snapshot = Counter(pair_counter.values())

    top_abas = Counter(abas).most_common(10)
    top_timestamps = Counter(timestamps).most_common(10)

    return {
        total_rows total_rows,
        distinct_abas len(unique_abas),
        distinct_timestamps len(unique_timestamps),
        distinct_pairs len(unique_pairs),
        blank_aba blank_aba,
        blank_timestamp blank_timestamp,
        blank_both blank_both,
        duplicated_pairs duplicated_pairs,
        legs_per_snapshot legs_per_snapshot,
        top_abas top_abas,
        top_timestamps top_timestamps,
    }


def print_summary(table str, summary Dict[str, Any]) - None
    print(=  80)
    print(fTABELA {table})
    print(fTOTAL_ROWS           {summary['total_rows']})
    print(fDISTINCT_ABAS        {summary['distinct_abas']})
    print(fDISTINCT_TIMESTAMPS  {summary['distinct_timestamps']})
    print(fDISTINCT_PAIRS       {summary['distinct_pairs']})
    print()

    print(BLANKS)
    print(f  - aba blank        {summary['blank_aba']})
    print(f  - timestamp blank  {summary['blank_timestamp']})
    print(f  - ambos blank      {summary['blank_both']})
    print()

    print(LEGS POR SNAPSHOT (qtd_linhas por chave aba+timestamp))
    for legs_count, snapshots in sorted(summary[legs_per_snapshot].items())
        print(f  - {legs_count} legs - {snapshots} snapshot(s))
    print()

    print(TOP ABAS)
    for aba, count in summary[top_abas]
        print(f  - {aba} {count})
    print()

    print(TOP TIMESTAMPS)
    for ts, count in summary[top_timestamps]
        print(f  - {ts} {count})
    print()

    print(DUPLICATED SNAPSHOT KEYS (aba+timestamp com mais de 1 linha))
    if summary[duplicated_pairs]
        for (aba, ts), count in summary[duplicated_pairs][20]
            print(f  - aba={aba!r} timestamp={ts!r} rows={count})
    else
        print(  - nenhuma)


def main() - int
    print(== AUDIT SNAPSHOT KEYS ==)
    print(fPROJECT_ROOT {PROJECT_ROOT})
    print(fDB {APP_DB})
    print()

    with sqlite_conn(APP_DB) as conn
        for table in TABLES
            rows = fetch_rows(conn, table)
            summary = summarize_table(rows)
            print_summary(table, summary)
            print()

    print(OK)
    return 0


if __name__ == __main__
    raise SystemExit(main())
