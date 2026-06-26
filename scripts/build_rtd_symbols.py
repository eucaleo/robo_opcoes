from pathlib import Path
import argparse
import sqlite3


INVALID_SYMBOLS = {
    "",
    "0",
    "NONE",
    "NULL",
    "N/A",
    "NA",
    "#N/A",
    "#VALUE!",
    "#REF!",
    "#NAME?",
}


DEFAULT_ACTIVE_STATUSES = [
    "active",
]


def table_exists(cur, table_name):
    cur.execute(
        """
        SELECT name
          FROM sqlite_master
         WHERE type = 'table'
           AND name = ?
        """,
        (table_name,),
    )
    return cur.fetchone() is not None


def table_columns(cur, table_name):
    if not table_exists(cur, table_name):
        return set()

    cur.execute(f"PRAGMA table_info({table_name})")
    return {row[1] for row in cur.fetchall()}


def normalize_symbol(value):
    if value is None:
        return None

    text = str(value).strip().upper()

    if text in INVALID_SYMBOLS:
        return None

    return text


def normalize_status(value):
    if value is None:
        return ""

    return str(value).strip().lower()


def normalize_symbols(values):
    symbols = set()

    for value in values:
        symbol = normalize_symbol(value)
        if symbol:
            symbols.add(symbol)

    return sorted(symbols)


def collect_active_structure_legs(cur, active_statuses, include_inactive=False):
    if not table_exists(cur, "structure_legs"):
        return []

    leg_columns = table_columns(cur, "structure_legs")

    if "symbol" not in leg_columns:
        return []

    if include_inactive:
        cur.execute(
            """
            SELECT DISTINCT TRIM(symbol)
              FROM structure_legs
             WHERE symbol IS NOT NULL
               AND TRIM(symbol) <> ''
             ORDER BY TRIM(symbol)
            """
        )
        return normalize_symbols(row[0] for row in cur.fetchall())

    if not table_exists(cur, "structures"):
        return []

    structure_columns = table_columns(cur, "structures")

    if "id" not in structure_columns:
        return []

    normalized_statuses = [
        normalize_status(status)
        for status in active_statuses
        if normalize_status(status)
    ]

    params = []

    where_parts = [
        "l.symbol IS NOT NULL",
        "TRIM(l.symbol) <> ''",
    ]

    if "status" in structure_columns and normalized_statuses:
        placeholders = ", ".join(["?"] * len(normalized_statuses))
        where_parts.append(f"LOWER(TRIM(COALESCE(s.status, ''))) IN ({placeholders})")
        params.extend(normalized_statuses)

    sql = f"""
        SELECT DISTINCT TRIM(l.symbol)
          FROM structure_legs l
          JOIN structures s
            ON s.id = l.structure_id
         WHERE {" AND ".join(where_parts)}
         ORDER BY TRIM(l.symbol)
    """

    cur.execute(sql, params)

    return normalize_symbols(row[0] for row in cur.fetchall())


def collect_from_structure_leg_snapshots(cur):
    if not table_exists(cur, "structure_leg_snapshots"):
        return []

    columns = table_columns(cur, "structure_leg_snapshots")

    if "symbol" not in columns:
        return []

    cur.execute(
        """
        SELECT DISTINCT TRIM(symbol)
          FROM structure_leg_snapshots
         WHERE symbol IS NOT NULL
           AND TRIM(symbol) <> ''
         ORDER BY TRIM(symbol)
        """
    )

    return normalize_symbols(row[0] for row in cur.fetchall())


def collect_from_rtd_option_quotes(cur):
    if not table_exists(cur, "rtd_option_quotes"):
        return []

    columns = table_columns(cur, "rtd_option_quotes")

    if "codigo_opcao" not in columns:
        return []

    cur.execute(
        """
        SELECT DISTINCT TRIM(codigo_opcao)
          FROM rtd_option_quotes
         WHERE codigo_opcao IS NOT NULL
           AND TRIM(codigo_opcao) <> ''
         ORDER BY TRIM(codigo_opcao)
        """
    )

    return normalize_symbols(row[0] for row in cur.fetchall())


def load_symbols(
    db_path,
    scope="active-structures",
    active_statuses=None,
    include_inactive=False,
    include_snapshots=False,
    include_existing_quotes=False,
):
    active_statuses = active_statuses or DEFAULT_ACTIVE_STATUSES

    conn = sqlite3.connect(db_path)

    try:
        cur = conn.cursor()
        sources = []
        all_symbols = []

        if scope == "active-structures":
            leg_symbols = collect_active_structure_legs(
                cur,
                active_statuses=active_statuses,
                include_inactive=include_inactive,
            )

            sources.append(("structure_legs active structures", leg_symbols))
            all_symbols.extend(leg_symbols)

            return normalize_symbols(all_symbols), sources

        if scope == "all-cache":
            leg_symbols = collect_active_structure_legs(
                cur,
                active_statuses=active_statuses,
                include_inactive=include_inactive,
            )
            sources.append(("structure_legs", leg_symbols))
            all_symbols.extend(leg_symbols)

            if include_snapshots:
                snapshot_symbols = collect_from_structure_leg_snapshots(cur)
                sources.append(("structure_leg_snapshots", snapshot_symbols))
                all_symbols.extend(snapshot_symbols)

            if include_existing_quotes:
                quote_symbols = collect_from_rtd_option_quotes(cur)
                sources.append(("rtd_option_quotes", quote_symbols))
                all_symbols.extend(quote_symbols)

            return normalize_symbols(all_symbols), sources

        raise ValueError(f"Scope inválido: {scope}")

    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(
        description="Gera arquivo de símbolos RTD de opções."
    )
    parser.add_argument("--db", default="dados/app.db")
    parser.add_argument("--out", default="dados/rtd_symbols.txt")
    parser.add_argument("--allow-empty", action="store_true")

    parser.add_argument(
        "--scope",
        choices=["active-structures", "all-cache"],
        default="active-structures",
        help="Escopo de geração. Padrão: active-structures.",
    )

    parser.add_argument(
        "--active-status",
        action="append",
        dest="active_statuses",
        help="Status considerado ativo. Pode repetir. Padrão: active.",
    )

    # Compatibilidade com fluxo antigo/run_rtd_refresh_full.py.
    parser.add_argument(
        "--include-inactive",
        action="store_true",
        help="Inclui structure_legs sem filtrar structures.status.",
    )
    parser.add_argument(
        "--no-snapshots",
        action="store_true",
        help="Ignorado no escopo active-structures. Mantido por compatibilidade.",
    )
    parser.add_argument(
        "--no-existing-quotes",
        action="store_true",
        help="Ignorado no escopo active-structures. Mantido por compatibilidade.",
    )
    parser.add_argument(
        "--include-snapshots",
        action="store_true",
        help="Usado apenas com --scope all-cache.",
    )
    parser.add_argument(
        "--include-existing-quotes",
        action="store_true",
        help="Usado apenas com --scope all-cache.",
    )

    args = parser.parse_args()

    db_path = Path(args.db)
    out_path = Path(args.out)

    active_statuses = args.active_statuses or DEFAULT_ACTIVE_STATUSES

    if not db_path.exists():
        raise SystemExit(f"Banco não encontrado: {db_path}")

    out_path.parent.mkdir(parents=True, exist_ok=True)

    include_snapshots = args.include_snapshots and not args.no_snapshots
    include_existing_quotes = args.include_existing_quotes and not args.no_existing_quotes

    symbols, sources = load_symbols(
        db_path=db_path,
        scope=args.scope,
        active_statuses=active_statuses,
        include_inactive=args.include_inactive,
        include_snapshots=include_snapshots,
        include_existing_quotes=include_existing_quotes,
    )

    print("Escopo:", args.scope)
    print("Status ativos considerados:", ", ".join(active_statuses))
    print()
    print("Fontes encontradas para opções:")

    if not sources:
        print("- nenhuma")

    for source_name, values in sources:
        print(f"- {source_name}: {len(normalize_symbols(values))}")

    if not symbols and not args.allow_empty:
        raise SystemExit(
            "Nenhum símbolo de opção encontrado. Use --allow-empty para permitir arquivo vazio."
        )

    out_path.write_text(
        "\n".join(symbols) + ("\n" if symbols else ""),
        encoding="utf-8",
    )

    print()
    print(f"Símbolos exportados: {len(symbols)}")
    print(f"Arquivo: {out_path}")

    for symbol in symbols:
        print(symbol)


if __name__ == "__main__":
    main()
