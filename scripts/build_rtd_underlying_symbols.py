from pathlib import Path
import argparse
import sqlite3


POSSIBLE_STRUCTURE_COLUMNS = [
    "underlying_asset",
    "ativo_base",
    "underlying",
    "underlying_symbol",
    "base_asset",
]


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


def collect_active_structure_underlyings(cur, active_statuses):
    if not table_exists(cur, "structures"):
        return [], []

    columns = table_columns(cur, "structures")

    sources = []
    all_symbols = []

    normalized_statuses = [
        normalize_status(status)
        for status in active_statuses
        if normalize_status(status)
    ]

    for column_name in POSSIBLE_STRUCTURE_COLUMNS:
        if column_name not in columns:
            continue

        params = []

        where_parts = [
            f"{column_name} IS NOT NULL",
            f"TRIM({column_name}) <> ''",
        ]

        if "status" in columns and normalized_statuses:
            placeholders = ", ".join(["?"] * len(normalized_statuses))
            where_parts.append(f"LOWER(TRIM(status)) IN ({placeholders})")
            params.extend(normalized_statuses)

        sql = f"""
            SELECT DISTINCT TRIM({column_name})
              FROM structures
             WHERE {" AND ".join(where_parts)}
             ORDER BY TRIM({column_name})
        """

        cur.execute(sql, params)

        values = []

        for row in cur.fetchall():
            symbol = normalize_symbol(row[0])
            if symbol:
                values.append(symbol)

        if values:
            sources.append((f"structures.{column_name}", values))
            all_symbols.extend(values)

    return sorted(set(all_symbols)), sources


def collect_from_column(cur, table_name, column_name):
    if not table_exists(cur, table_name):
        return []

    columns = table_columns(cur, table_name)

    if column_name not in columns:
        return []

    cur.execute(
        f"""
        SELECT DISTINCT TRIM({column_name})
          FROM {table_name}
         WHERE {column_name} IS NOT NULL
           AND TRIM({column_name}) <> ''
         ORDER BY TRIM({column_name})
        """
    )

    values = []

    for row in cur.fetchall():
        symbol = normalize_symbol(row[0])
        if symbol:
            values.append(symbol)

    return values


def load_underlying_symbols(db_path, scope, active_statuses):
    conn = sqlite3.connect(db_path)

    try:
        cur = conn.cursor()

        if scope == "active-structures":
            return collect_active_structure_underlyings(cur, active_statuses)

        if scope == "all-cache":
            sources = []
            all_symbols = []

            active_symbols, active_sources = collect_active_structure_underlyings(
                cur,
                active_statuses,
            )
            sources.extend(active_sources)
            all_symbols.extend(active_symbols)

            values = collect_from_column(cur, "rtd_option_quotes", "ativo_base")
            if values:
                sources.append(("rtd_option_quotes.ativo_base", values))
                all_symbols.extend(values)

            values = collect_from_column(cur, "structure_legs", "ativo_base")
            if values:
                sources.append(("structure_legs.ativo_base", values))
                all_symbols.extend(values)

            values = collect_from_column(cur, "structure_leg_snapshots", "ativo_base")
            if values:
                sources.append(("structure_leg_snapshots.ativo_base", values))
                all_symbols.extend(values)

            return sorted(set(all_symbols)), sources

        raise ValueError(f"Scope inválido: {scope}")

    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(
        description="Gera arquivo de símbolos RTD para ativos-base."
    )
    parser.add_argument("--db", default="dados/app.db")
    parser.add_argument("--out", default="dados/rtd_underlying_symbols.txt")
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

    args = parser.parse_args()

    db_path = Path(args.db)
    out_path = Path(args.out)

    active_statuses = args.active_statuses or DEFAULT_ACTIVE_STATUSES

    if not db_path.exists():
        raise SystemExit(f"Banco não encontrado: {db_path}")

    out_path.parent.mkdir(parents=True, exist_ok=True)

    symbols, sources = load_underlying_symbols(
        db_path=db_path,
        scope=args.scope,
        active_statuses=active_statuses,
    )

    print("Escopo:", args.scope)
    print("Status ativos considerados:", ", ".join(active_statuses))
    print()
    print("Fontes encontradas para ativos-base:")

    if not sources:
        print("- nenhuma")

    for source_name, values in sources:
        print(f"- {source_name}: {len(set(values))}")

    if not symbols and not args.allow_empty:
        raise SystemExit(
            "Nenhum ativo-base encontrado. Use --allow-empty para permitir arquivo vazio."
        )

    out_path.write_text(
        "\n".join(symbols) + ("\n" if symbols else ""),
        encoding="utf-8",
    )

    print()
    print(f"Ativos-base exportados: {len(symbols)}")
    print(f"Arquivo: {out_path}")

    for symbol in symbols:
        print(symbol)


if __name__ == "__main__":
    main()
