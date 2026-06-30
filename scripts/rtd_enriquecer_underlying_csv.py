from pathlib import Path
import csv
import sqlite3
import sys
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]

DBS = [
    ROOT / "dados" / "app.db",
    ROOT / "dados" / "derived.db",
]

TABLE = "rtd_underlying_quotes"


def now_sqlite():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def norm_key(s):
    if s is None:
        return ""
    return (
        str(s)
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
        .replace(".", "_")
    )


def to_float(value):
    if value is None:
        return None

    s = str(value).strip()

    if s == "":
        return None

    s = (
        s.replace("R$", "")
        .replace(" ", "")
        .replace("\u00a0", "")
    )

    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".")

    try:
        return float(s)
    except Exception:
        return None


def detect_dialect(path):
    sample = path.read_text(encoding="utf-8-sig", errors="ignore")[:4096]
    try:
        return csv.Sniffer().sniff(sample, delimiters=";,|\t,")
    except Exception:
        class Fallback:
            delimiter = ";"
        return Fallback()


def pick(row, aliases):
    normalized = {norm_key(k): v for k, v in row.items()}

    for alias in aliases:
        key = norm_key(alias)
        if key in normalized:
            return normalized[key]

    return None


def ensure_columns(con):
    con.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {TABLE} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ativo TEXT NOT NULL,
            ultimo_preco REAL,
            bid REAL,
            ask REAL,
            close_price REAL,
            prev_close REAL,
            open_price REAL,
            high_price REAL,
            low_price REAL,
            volume REAL,
            change_percent REAL,
            source TEXT,
            updated_at TEXT,
            created_at TEXT,
            vwap REAL
        )
        """
    )

    existing = [r[1] for r in con.execute(f"PRAGMA table_info({TABLE})").fetchall()]

    wanted = {
        "ativo": "TEXT",
        "ultimo_preco": "REAL",
        "bid": "REAL",
        "ask": "REAL",
        "close_price": "REAL",
        "prev_close": "REAL",
        "open_price": "REAL",
        "high_price": "REAL",
        "low_price": "REAL",
        "volume": "REAL",
        "change_percent": "REAL",
        "source": "TEXT",
        "updated_at": "TEXT",
        "created_at": "TEXT",
        "vwap": "REAL",
    }

    for col, typ in wanted.items():
        if col not in existing:
            con.execute(f"ALTER TABLE {TABLE} ADD COLUMN {col} {typ}")


def parse_csv(path):
    dialect = detect_dialect(path)

    with path.open("r", encoding="utf-8-sig", errors="ignore", newline="") as f:
        reader = csv.DictReader(f, dialect=dialect)

        print("Colunas detectadas:")
        print(reader.fieldnames)
        print()

        items = []

        for row in reader:
            ativo = pick(row, ["ativo", "ticker", "codigo", "símbolo", "simbolo", "papel"])

            if not ativo:
                continue

            item = {
                "ativo": str(ativo).strip().upper(),
                "ultimo_preco": to_float(pick(row, ["ultimo_preco", "último_preço", "ultimo", "último", "last", "preco", "preço"])),
                "bid": to_float(pick(row, ["bid", "compra", "melhor_compra"])),
                "ask": to_float(pick(row, ["ask", "venda", "melhor_venda"])),
                "close_price": to_float(pick(row, ["close_price", "close", "fechamento"])),
                "prev_close": to_float(pick(row, ["prev_close", "previous_close", "fechamento_anterior"])),
                "open_price": to_float(pick(row, ["open_price", "open", "abertura"])),
                "high_price": to_float(pick(row, ["high_price", "high", "maxima", "máxima"])),
                "low_price": to_float(pick(row, ["low_price", "low", "minima", "mínima"])),
                "volume": to_float(pick(row, ["volume", "vol", "volume_financeiro"])),
                "change_percent": to_float(pick(row, ["change_percent", "change", "var_percent", "variação", "variacao"])),
                "vwap": to_float(pick(row, ["vwap", "preco_medio", "preço_médio", "medio", "médio"])),
                "source": "BTG_RTD_EXCEL_UNDERLYING_CSV",
                "updated_at": now_sqlite(),
                "created_at": now_sqlite(),
            }

            items.append(item)

    return items


def upsert(con, item):
    ensure_columns(con)

    existing = con.execute(
        f"""
        SELECT id
        FROM {TABLE}
        WHERE ativo = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (item["ativo"],),
    ).fetchone()

    if existing:
        con.execute(
            f"""
            UPDATE {TABLE}
            SET
                ultimo_preco = COALESCE(?, ultimo_preco),
                bid = COALESCE(?, bid),
                ask = COALESCE(?, ask),
                close_price = COALESCE(?, close_price),
                prev_close = COALESCE(?, prev_close),
                open_price = COALESCE(?, open_price),
                high_price = COALESCE(?, high_price),
                low_price = COALESCE(?, low_price),
                volume = COALESCE(?, volume),
                change_percent = COALESCE(?, change_percent),
                vwap = COALESCE(?, vwap),
                source = ?,
                updated_at = ?
            WHERE id = ?
            """,
            (
                item["ultimo_preco"],
                item["bid"],
                item["ask"],
                item["close_price"],
                item["prev_close"],
                item["open_price"],
                item["high_price"],
                item["low_price"],
                item["volume"],
                item["change_percent"],
                item["vwap"],
                item["source"],
                item["updated_at"],
                existing["id"],
            ),
        )
        return "updated"

    con.execute(
        f"""
        INSERT INTO {TABLE} (
            ativo,
            ultimo_preco,
            bid,
            ask,
            close_price,
            prev_close,
            open_price,
            high_price,
            low_price,
            volume,
            change_percent,
            vwap,
            source,
            updated_at,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            item["ativo"],
            item["ultimo_preco"],
            item["bid"],
            item["ask"],
            item["close_price"],
            item["prev_close"],
            item["open_price"],
            item["high_price"],
            item["low_price"],
            item["volume"],
            item["change_percent"],
            item["vwap"],
            item["source"],
            item["updated_at"],
            item["created_at"],
        ),
    )
    return "inserted"


def print_db(con, label):
    print()
    print("=" * 100)
    print(label)
    print("=" * 100)

    cols = [r[1] for r in con.execute(f"PRAGMA table_info({TABLE})").fetchall()]
    print("colunas:", cols)

    rows = con.execute(
        f"""
        SELECT
            ativo,
            ultimo_preco,
            bid,
            ask,
            close_price,
            prev_close,
            open_price,
            high_price,
            low_price,
            volume,
            change_percent,
            vwap,
            source,
            updated_at
        FROM {TABLE}
        ORDER BY ativo
        """
    ).fetchall()

    for row in rows:
        print(dict(row))


def main():
    if len(sys.argv) < 2:
        raise SystemExit(
            "Uso:\n"
            "  python scripts/rtd_enriquecer_underlying_csv.py dados/RTD_UNDERLYING_QUOTES.csv"
        )

    csv_path = Path(sys.argv[1])
    if not csv_path.is_absolute():
        csv_path = ROOT / csv_path

    if not csv_path.exists():
        raise SystemExit(f"CSV não encontrado: {csv_path}")

    items = parse_csv(csv_path)

    print("=" * 100)
    print("Itens lidos")
    print("=" * 100)
    for item in items:
        print(item)

    for db_path in DBS:
        con = sqlite3.connect(str(db_path))
        con.row_factory = sqlite3.Row

        inserted = 0
        updated = 0

        for item in items:
            action = upsert(con, item)
            if action == "inserted":
                inserted += 1
            else:
                updated += 1

        con.commit()

        print()
        print("=" * 100)
        print(f"Resumo {db_path.relative_to(ROOT)}")
        print("=" * 100)
        print("inseridos:", inserted)
        print("atualizados:", updated)

        print_db(con, str(db_path.relative_to(ROOT)))

        con.close()


if __name__ == "__main__":
    main()
