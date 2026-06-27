from pathlib import Path
import sqlite3
import sys
from datetime import datetime

db_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("dados/app.db")
out_dir = Path("reports/payoff_conferencia")
out_dir.mkdir(parents=True, exist_ok=True)
stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
out_file = out_dir / f"conferencia_db_payoff_{stamp}.txt"

def write(line=""):
    lines.append(str(line))

def table_exists(cur, table):
    cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
        (table,),
    )
    return cur.fetchone() is not None

def columns(cur, table):
    if not table_exists(cur, table):
        return []
    cur.execute(f"PRAGMA table_info({table})")
    return [row[1] for row in cur.fetchall()]

def scalar(cur, sql, params=()):
    try:
        cur.execute(sql, params)
        row = cur.fetchone()
        if row is None:
            return None
        return row[0]
    except Exception as exc:
        return f"ERRO: {exc}"

def rows(cur, sql, params=()):
    try:
        cur.execute(sql, params)
        return cur.fetchall()
    except Exception as exc:
        return [("ERRO", str(exc))]

def pick_column(cols, candidates):
    for candidate in candidates:
        if candidate in cols:
            return candidate
    return None

lines = []

write("Conferencia DB - Payoff por estrutura individual")
write(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
write(f"Banco: {db_path}")
write("")

if not db_path.exists():
    write("FALHA: banco não encontrado.")
    out_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"Relatorio gerado em: {out_file}")
    raise SystemExit(1)

conn = sqlite3.connect(str(db_path))
cur = conn.cursor()

tables = [
    "structures",
    "structure_legs",
    "structure_leg_snapshots",
    "rtd_option_quotes",
    "rtd_underlying_quotes",
    "derived_payoffs",
    "derived_payoff_points",
    "payoff_snapshots",
    "pricing_snapshots",
]

write("Tabelas principais")
for table in tables:
    exists = table_exists(cur, table)
    write(f"- {table}: {'OK' if exists else 'AUSENTE'}")
write("")

write("Colunas por tabela encontrada")
for table in tables:
    if table_exists(cur, table):
        write(f"{table}: {', '.join(columns(cur, table))}")
write("")

if table_exists(cur, "structures"):
    cols = columns(cur, "structures")
    id_col = pick_column(cols, ["id", "structure_id"])
    status_col = pick_column(cols, ["status"])
    underlying_col = pick_column(cols, ["underlying_asset", "underlying", "ativo_base", "asset"])
    name_col = pick_column(cols, ["name", "nome", "structure_name"])

    write("Resumo structures")
    write(f"- total: {scalar(cur, 'SELECT COUNT(*) FROM structures')}")
    if status_col:
        write(f"- ativas: {scalar(cur, f'SELECT COUNT(*) FROM structures WHERE {status_col} = ?', ('active',))}")
    if underlying_col:
        write("- estruturas por ativo-base:")
        for row in rows(cur, f"SELECT {underlying_col}, COUNT(*) FROM structures GROUP BY {underlying_col} ORDER BY COUNT(*) DESC, {underlying_col}"):
            write(f"  {row}")
    if id_col:
        select_cols = [id_col]
        if name_col:
            select_cols.append(name_col)
        if underlying_col:
            select_cols.append(underlying_col)
        if status_col:
            select_cols.append(status_col)
        sql = f"SELECT {', '.join(select_cols)} FROM structures ORDER BY {id_col} LIMIT 30"
        write("- amostra structures:")
        for row in rows(cur, sql):
            write(f"  {row}")
    write("")

if table_exists(cur, "structure_legs"):
    cols = columns(cur, "structure_legs")
    sid_col = pick_column(cols, ["structure_id", "structureId"])
    ticker_col = pick_column(cols, ["ticker", "codigo_opcao", "option_symbol", "symbol"])
    underlying_col = pick_column(cols, ["underlying_asset", "underlying", "ativo_base", "asset"])
    status_col = pick_column(cols, ["status"])
    type_col = pick_column(cols, ["call_put", "option_type", "type", "tipo"])
    side_col = pick_column(cols, ["side", "direction", "direcao"])
    strike_col = pick_column(cols, ["strike"])

    write("Resumo structure_legs")
    write(f"- total: {scalar(cur, 'SELECT COUNT(*) FROM structure_legs')}")
    if sid_col:
        write("- pernas por structure_id:")
        for row in rows(cur, f"SELECT {sid_col}, COUNT(*) FROM structure_legs GROUP BY {sid_col} ORDER BY {sid_col}"):
            write(f"  {row}")
    if status_col:
        write("- pernas por status:")
        for row in rows(cur, f"SELECT {status_col}, COUNT(*) FROM structure_legs GROUP BY {status_col} ORDER BY {status_col}"):
            write(f"  {row}")
    if type_col:
        write("- tipos de opcao encontrados:")
        for row in rows(cur, f"SELECT {type_col}, COUNT(*) FROM structure_legs GROUP BY {type_col} ORDER BY {type_col}"):
            write(f"  {row}")
    if sid_col and underlying_col and table_exists(cur, "structures"):
        s_cols = columns(cur, "structures")
        s_id_col = pick_column(s_cols, ["id", "structure_id"])
        s_underlying_col = pick_column(s_cols, ["underlying_asset", "underlying", "ativo_base", "asset"])
        if s_id_col and s_underlying_col:
            write("- divergencias ativo-base entre structures e structure_legs:")
            sql = f"""
                SELECT l.{sid_col}, s.{s_underlying_col}, l.{underlying_col}, COUNT(*)
                FROM structure_legs l
                JOIN structures s ON s.{s_id_col} = l.{sid_col}
                WHERE COALESCE(s.{s_underlying_col}, '') <> COALESCE(l.{underlying_col}, '')
                GROUP BY l.{sid_col}, s.{s_underlying_col}, l.{underlying_col}
                ORDER BY l.{sid_col}
            """
            result = rows(cur, sql)
            if result:
                for row in result:
                    write(f"  {row}")
            else:
                write("  nenhuma divergencia encontrada")
    if sid_col and ticker_col:
        write("- amostra de pernas:")
        select_cols = [sid_col, ticker_col]
        for col in [underlying_col, type_col, side_col, strike_col, status_col]:
            if col and col not in select_cols:
                select_cols.append(col)
        sql = f"SELECT {', '.join(select_cols)} FROM structure_legs ORDER BY {sid_col}, {ticker_col} LIMIT 50"
        for row in rows(cur, sql):
            write(f"  {row}")
    write("")

if table_exists(cur, "rtd_underlying_quotes"):
    cols = columns(cur, "rtd_underlying_quotes")
    asset_col = pick_column(cols, ["ativo", "underlying", "underlying_asset", "asset"])
    price_col = pick_column(cols, ["ultimo_preco", "last_price", "price"])
    source_col = pick_column(cols, ["source", "fonte"])
    updated_col = pick_column(cols, ["updated_at", "updatedAt"])
    write("Resumo rtd_underlying_quotes")
    write(f"- total: {scalar(cur, 'SELECT COUNT(*) FROM rtd_underlying_quotes')}")
    if asset_col:
        select_cols = [asset_col]
        for col in [price_col, source_col, updated_col]:
            if col:
                select_cols.append(col)
        sql = f"SELECT {', '.join(select_cols)} FROM rtd_underlying_quotes ORDER BY {asset_col}"
        for row in rows(cur, sql):
            write(f"  {row}")
    write("")

if table_exists(cur, "rtd_option_quotes"):
    cols = columns(cur, "rtd_option_quotes")
    ticker_col = pick_column(cols, ["codigo_opcao", "ticker", "option_symbol", "symbol"])
    underlying_col = pick_column(cols, ["ativo_base", "underlying_asset", "underlying", "asset"])
    type_col = pick_column(cols, ["call_put", "option_type", "type", "tipo"])
    price_col = pick_column(cols, ["ultimo_preco", "last_price", "price"])
    bid_col = pick_column(cols, ["bid"])
    ask_col = pick_column(cols, ["ask"])
    updated_col = pick_column(cols, ["updated_at", "updatedAt"])

    write("Resumo rtd_option_quotes")
    write(f"- total: {scalar(cur, 'SELECT COUNT(*) FROM rtd_option_quotes')}")
    if ticker_col:
        write(f"- codigos duplicados: {scalar(cur, f'SELECT COUNT(*) FROM (SELECT {ticker_col} FROM rtd_option_quotes GROUP BY {ticker_col} HAVING COUNT(*) > 1)')}")
    if type_col:
        write("- call_put ou tipo invalido/suspeito:")
        sql = f"""
            SELECT {ticker_col if ticker_col else type_col}, {type_col}
            FROM rtd_option_quotes
            WHERE {type_col} IS NULL
               OR TRIM(CAST({type_col} AS TEXT)) = ''
               OR UPPER(TRIM(CAST({type_col} AS TEXT))) NOT IN ('CALL','PUT','C','P')
            ORDER BY 1
        """
        result = rows(cur, sql)
        if result:
            for row in result:
                write(f"  {row}")
        else:
            write("  nenhum")
    if price_col:
        write("- opcoes com ultimo_preco zerado ou ausente:")
        select_cols = []
        for col in [ticker_col, underlying_col, type_col, price_col, bid_col, ask_col, updated_col]:
            if col:
                select_cols.append(col)
        sql = f"""
            SELECT {', '.join(select_cols)}
            FROM rtd_option_quotes
            WHERE {price_col} IS NULL OR {price_col} <= 0
            ORDER BY {ticker_col if ticker_col else price_col}
        """
        result = rows(cur, sql)
        if result:
            for row in result:
                write(f"  {row}")
        else:
            write("  nenhuma")
    write("")

if table_exists(cur, "structure_legs") and table_exists(cur, "rtd_option_quotes"):
    l_cols = columns(cur, "structure_legs")
    q_cols = columns(cur, "rtd_option_quotes")
    l_ticker = pick_column(l_cols, ["ticker", "codigo_opcao", "option_symbol", "symbol"])
    q_ticker = pick_column(q_cols, ["codigo_opcao", "ticker", "option_symbol", "symbol"])
    l_sid = pick_column(l_cols, ["structure_id", "structureId"])
    if l_ticker and q_ticker:
        write("Cruzamento pernas x rtd_option_quotes")
        sql = f"""
            SELECT l.{l_sid if l_sid else l_ticker}, l.{l_ticker}
            FROM structure_legs l
            LEFT JOIN rtd_option_quotes q ON q.{q_ticker} = l.{l_ticker}
            WHERE q.{q_ticker} IS NULL
            ORDER BY 1, 2
        """
        result = rows(cur, sql)
        if result:
            write("- pernas sem cotacao RTD:")
            for row in result:
                write(f"  {row}")
        else:
            write("- todas as pernas encontradas possuem cotacao RTD")
        write("")

conn.close()

out_file.write_text("\n".join(lines), encoding="utf-8")
print(f"Relatorio gerado em: {out_file}")
