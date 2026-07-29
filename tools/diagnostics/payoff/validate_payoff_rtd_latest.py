#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import sqlite3
import sys
from pathlib import Path


def row_to_dict(cursor, row):
    return {cursor.description[i][0]: row[i] for i in range(len(row))}


def parse_json(value):
    if value is None:
        return {}

    if isinstance(value, dict):
        return value

    try:
        return json.loads(value)
    except Exception:
        return {}


def get_latest_timestamps(conn, structure_ids):
    if structure_ids:
        placeholders = ",".join("?" for _ in structure_ids)
        query = f"""
            SELECT structure_id, MAX(timestamp) AS timestamp
            FROM payoff_curve_points
            WHERE structure_id IN ({placeholders})
            GROUP BY structure_id
            ORDER BY structure_id
        """
        params = structure_ids
    else:
        query = """
            SELECT structure_id, MAX(timestamp) AS timestamp
            FROM payoff_curve_points
            GROUP BY structure_id
            ORDER BY structure_id
        """
        params = []

    cursor = conn.execute(query, params)
    return [row_to_dict(cursor, row) for row in cursor.fetchall()]


def validate_one(conn, structure_id, timestamp, min_rows, require_rtd, print_legs):
    cursor = conn.execute(
        """
        SELECT
            COUNT(*) AS linhas,
            MIN(point_spot) AS min_spot,
            MAX(point_spot) AS max_spot,
            MIN(point_pl) AS min_pl,
            MAX(point_pl) AS max_pl,
            MAX(spot_ref) AS spot_ref
        FROM payoff_curve_points
        WHERE structure_id = ?
          AND timestamp = ?
        """,
        (structure_id, timestamp),
    )
    summary = row_to_dict(cursor, cursor.fetchone())

    cursor = conn.execute(
        """
        SELECT point_spot, point_pl, spot_ref, meta_json
        FROM payoff_curve_points
        WHERE structure_id = ?
          AND timestamp = ?
        ORDER BY point_spot
        LIMIT 1
        """,
        (structure_id, timestamp),
    )
    sample = row_to_dict(cursor, cursor.fetchone())
    meta = parse_json(sample.get("meta_json"))

    errors = []

    if summary["linhas"] < min_rows:
        errors.append(f"linhas abaixo do esperado: {summary['linhas']} < {min_rows}")

    if summary["spot_ref"] is None:
        errors.append("spot_ref está NULL")

    if require_rtd:
        snapshot_source = str(meta.get("snapshot_source", ""))
        source = str(meta.get("source", ""))
        spot_ref_source = str(meta.get("spot_ref_source", ""))

        if "rtd" not in snapshot_source.lower() and "rtd" not in source.lower():
            errors.append(
                f"snapshot/source não parecem RTD: source={source} snapshot_source={snapshot_source}"
            )

        if "rtd_underlying_quotes" not in spot_ref_source:
            errors.append(f"spot_ref_source inesperado: {spot_ref_source}")

    print("")
    print(f"[validate-payoff] structure_id={structure_id}")
    print(f"  timestamp={timestamp}")
    print(f"  linhas={summary['linhas']}")
    print(f"  spot_ref={summary['spot_ref']}")
    print(f"  min_spot={summary['min_spot']}")
    print(f"  max_spot={summary['max_spot']}")
    print(f"  min_pl={summary['min_pl']}")
    print(f"  max_pl={summary['max_pl']}")
    print(f"  meta.source={meta.get('source')}")
    print(f"  meta.snapshot_source={meta.get('snapshot_source')}")
    print(f"  meta.spot_ref_source={meta.get('spot_ref_source')}")
    print(f"  meta.underlying_asset={meta.get('underlying_asset')}")

    if print_legs:
        print("  legs:")
        for leg in meta.get("legs", []):
            quote = leg.get("rtd_quote") or {}
            print(
                "   - "
                f"symbol={leg.get('symbol')} "
                f"side={leg.get('position_side')} "
                f"type={leg.get('option_type')} "
                f"strike={leg.get('strike')} "
                f"entry={leg.get('entry_premium')} "
                f"premium_usado={leg.get('premium')} "
                f"premium_source={leg.get('premium_source')} "
                f"rtd_found={leg.get('rtd_quote_found')} "
                f"rtd_updated_at={quote.get('updated_at')}"
            )

    if errors:
        print("  status=FAIL")
        for error in errors:
            print(f"  erro={error}")
        return False

    print("  status=OK")
    return True


def parse_args():
    parser = argparse.ArgumentParser(
        description="Valida o último snapshot em payoff_curve_points."
    )

    parser.add_argument(
        "--db",
        default="dados/app.db",
        help="Caminho do banco SQLite. Padrão: dados/app.db",
    )

    parser.add_argument(
        "--structure-ids",
        nargs="*",
        type=int,
        default=None,
        help="IDs das estruturas. Exemplo: --structure-ids 2 3",
    )

    parser.add_argument(
        "--min-rows",
        type=int,
        default=101,
        help="Mínimo de pontos esperado por snapshot. Padrão: 101",
    )

    parser.add_argument(
        "--no-require-rtd",
        action="store_true",
        help="Não exige metadados RTD no snapshot.",
    )

    parser.add_argument(
        "--print-legs",
        action="store_true",
        help="Mostra as pernas usadas no cálculo.",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    db_path = Path(args.db).resolve()
    if not db_path.exists():
        raise SystemExit(f"[validate-payoff] ERRO: banco não encontrado: {db_path}")

    conn = sqlite3.connect(db_path)

    latest_rows = get_latest_timestamps(conn, args.structure_ids)

    if not latest_rows:
        raise SystemExit("[validate-payoff] ERRO: nenhum snapshot encontrado.")

    all_ok = True

    for row in latest_rows:
        ok = validate_one(
            conn=conn,
            structure_id=row["structure_id"],
            timestamp=row["timestamp"],
            min_rows=args.min_rows,
            require_rtd=not args.no_require_rtd,
            print_legs=args.print_legs,
        )
        all_ok = all_ok and ok

    conn.close()

    if not all_ok:
        raise SystemExit(1)

    print("")
    print("[validate-payoff] validação concluída com sucesso.")


if __name__ == "__main__":
    main()
