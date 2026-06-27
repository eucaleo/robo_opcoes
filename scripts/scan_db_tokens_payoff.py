from pathlib import Path
import sqlite3
import sys
from datetime import datetime

TOKENS = [
    "66.84",
    "66,84",
    "198.35",
    "198,35",
    "170.78",
    "170,78",
    "170.55",
    "170,55",
    "53.20",
    "53,20",
    "53.2",
    "53,2",
    "static_fallback",
    "DEFAULT_MARKET_BY_ASSET",
]

def list_tables(cur):
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    return [r[0] for r in cur.fetchall()]

def list_columns(cur, table):
    cur.execute(f"PRAGMA table_info({table})")
    return [(r[1], r[2]) for r in cur.fetchall()]

def count_like(cur, table, column, token):
    try:
        cur.execute(
            f"SELECT COUNT(*) FROM {table} WHERE CAST({column} AS TEXT) LIKE ?",
            (f"%{token}%",),
        )
        return cur.fetchone()[0]
    except Exception:
        return 0

def sample_rows(cur, table, column, token, limit=3):
    try:
        cur.execute(
            f"SELECT rowid, CAST({column} AS TEXT) FROM {table} "
            f"WHERE CAST({column} AS TEXT) LIKE ? LIMIT ?",
            (f"%{token}%", limit),
        )
        return cur.fetchall()
    except Exception as exc:
        return [("ERRO", str(exc))]

def scan_db(db_path: Path, lines: list[str]):
    lines.append("")
    lines.append("============================================================")
    lines.append(f"Banco: {db_path}")
    lines.append("============================================================")

    if not db_path.exists():
        lines.append("AUSENTE")
        return

    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()

    tables = list_tables(cur)
    lines.append(f"Tabelas: {len(tables)}")

    findings = []

    for table in tables:
        for column, col_type in list_columns(cur, table):
            for token in TOKENS:
                n = count_like(cur, table, column, token)
                if n:
                    findings.append((table, column, token, n))

    if not findings:
        lines.append("Nenhum token encontrado.")
    else:
        lines.append("Ocorrencias encontradas:")
        for table, column, token, n in findings:
            lines.append(f"- table={table} column={column} token={token} count={n}")
            for rowid, value in sample_rows(cur, table, column, token):
                text = str(value)
                if len(text) > 500:
                    text = text[:500] + "..."
                lines.append(f"  sample rowid={rowid}: {text}")

    conn.close()

def main():
    dbs = [Path(p) for p in sys.argv[1:]] if len(sys.argv) > 1 else [
        Path("dados/app.db"),
        Path("dados/derived.db"),
    ]

    out_dir = Path("reports/payoff_runtime_focado")
    out_dir.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_file = out_dir / f"scan_db_tokens_payoff_{stamp}.txt"

    lines = []
    lines.append("Scan DB tokens payoff")
    lines.append(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Tokens: {', '.join(TOKENS)}")

    for db in dbs:
        scan_db(db, lines)

    out_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"Relatorio gerado em: {out_file}")

if __name__ == "__main__":
    main()
