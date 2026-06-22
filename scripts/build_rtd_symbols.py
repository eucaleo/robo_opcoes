import argparse
import sqlite3
from pathlib import Path


INACTIVE_STATUSES = {
    "closed",
    "encerrada",
    "encerrado",
    "inactive",
    "inativa",
    "cancelled",
    "cancelada",
    "canceled",
    "arquivada",
}


def table_exists(cur, table):
    row = cur.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
          AND name = ?
    """, (table,)).fetchone()
    return row is not None


def collect_from_structure_legs(cur, include_inactive=False):
    if not table_exists(cur, "structure_legs"):
        return []

    if include_inactive or not table_exists(cur, "structures"):
        rows = cur.execute("""
            SELECT DISTINCT TRIM(symbol)
            FROM structure_legs
            WHERE symbol IS NOT NULL
              AND TRIM(symbol) <> ''
        """).fetchall()
    else:
        rows = cur.execute("""
            SELECT DISTINCT TRIM(l.symbol)
            FROM structure_legs l
            LEFT JOIN structures s
                   ON s.id = l.structure_id
            WHERE l.symbol IS NOT NULL
              AND TRIM(l.symbol) <> ''
              AND (
                    s.status IS NULL
                    OR LOWER(TRIM(s.status)) NOT IN (
                        'closed',
                        'encerrada',
                        'encerrado',
                        'inactive',
                        'inativa',
                        'cancelled',
                        'cancelada',
                        'canceled',
                        'arquivada'
                    )
              )
        """).fetchall()

    return [r[0] for r in rows if r and r[0]]


def collect_from_structure_leg_snapshots(cur):
    if not table_exists(cur, "structure_leg_snapshots"):
        return []

    rows = cur.execute("""
        SELECT DISTINCT TRIM(symbol)
        FROM structure_leg_snapshots
        WHERE symbol IS NOT NULL
          AND TRIM(symbol) <> ''
    """).fetchall()

    return [r[0] for r in rows if r and r[0]]


def collect_from_rtd_option_quotes(cur):
    if not table_exists(cur, "rtd_option_quotes"):
        return []

    rows = cur.execute("""
        SELECT DISTINCT TRIM(codigo_opcao)
        FROM rtd_option_quotes
        WHERE codigo_opcao IS NOT NULL
          AND TRIM(codigo_opcao) <> ''
    """).fetchall()

    return [r[0] for r in rows if r and r[0]]


def normalize_symbols(values):
    symbols = set()

    for value in values:
        if value is None:
            continue

        text = str(value).strip().upper()

        if not text:
            continue

        symbols.add(text)

    return sorted(symbols)


def load_symbols(db_path, include_inactive=False, include_snapshots=True, include_existing_quotes=True):
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    try:
        sources = []

        leg_symbols = collect_from_structure_legs(cur, include_inactive=include_inactive)
        sources.append(("structure_legs", leg_symbols))

        snapshot_symbols = []
        if include_snapshots:
            snapshot_symbols = collect_from_structure_leg_snapshots(cur)
            sources.append(("structure_leg_snapshots", snapshot_symbols))

        quote_symbols = []
        if include_existing_quotes:
            quote_symbols = collect_from_rtd_option_quotes(cur)
            sources.append(("rtd_option_quotes", quote_symbols))

        all_symbols = []
        for _, values in sources:
            all_symbols.extend(values)

        return normalize_symbols(all_symbols), sources

    finally:
        con.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--include-inactive", action="store_true")
    parser.add_argument("--no-snapshots", action="store_true")
    parser.add_argument("--no-existing-quotes", action="store_true")
    parser.add_argument("--allow-empty", action="store_true")
    args = parser.parse_args()

    symbols, sources = load_symbols(
        args.db,
        include_inactive=args.include_inactive,
        include_snapshots=not args.no_snapshots,
        include_existing_quotes=not args.no_existing_quotes,
    )

    print("Fontes encontradas:")
    for name, values in sources:
        print(f"- {name}: {len(normalize_symbols(values))}")

    out = Path(args.out)

    if not symbols and not args.allow_empty:
        print("")
        print("Nenhum símbolo encontrado.")
        print("Arquivo de saída NÃO foi sobrescrito para evitar apagar lista existente.")
        print("Use --allow-empty se realmente quiser gerar arquivo vazio.")
        return 2

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(symbols) + ("\n" if symbols else ""), encoding="utf-8")

    print("")
    print(f"Símbolos exportados: {len(symbols)}")
    print(f"Arquivo: {out}")

    for sym in symbols[:50]:
        print(sym)

    if len(symbols) > 50:
        print(f"... mais {len(symbols) - 50}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
