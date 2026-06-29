from pathlib import Path
from datetime import datetime
import argparse
import csv
import json
import sqlite3


INVALID_TEXT_VALUES = {
    "",
    "0",
    "#N/A",
    "#VALUE!",
    "#REF!",
    "#NAME?",
    "N/A",
    "NA",
    "NULL",
    "NONE",
}


def now_text():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def clean_text(value, allow_zero=False):
    if value is None:
        return None

    text = str(value).strip()

    if not text:
        return None

    if not allow_zero and text.upper() in INVALID_TEXT_VALUES:
        return None

    return text


def parse_number(value):
    text = clean_text(value, allow_zero=True)

    if text is None:
        return None

    upper = text.upper()

    if upper in {
        "#N/A",
        "#VALUE!",
        "#REF!",
        "#NAME?",
        "N/A",
        "NA",
        "NULL",
        "NONE",
    }:
        return None

    text = (
        text.replace("R$", "")
        .replace("%", "")
        .replace("\u00a0", " ")
        .strip()
    )

    text = text.replace(" ", "")

    if "," in text and "." in text:
        text = text.replace(".", "").replace(",", ".")
    elif "," in text:
        text = text.replace(",", ".")

    try:
        return float(text)
    except ValueError:
        return None


def normalize_header(value):
    text = clean_text(value, allow_zero=True)

    if text is None:
        return ""

    return (
        text.strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
    )


def existing_columns(conn, table_name):
    cur = conn.execute(f'PRAGMA table_info("{table_name}")')
    return {row[1] for row in cur.fetchall()}


def ensure_column(conn, table_name, column_name, column_type):
    columns = existing_columns(conn, table_name)

    if column_name in columns:
        return

    conn.execute(
        f'ALTER TABLE "{table_name}" ADD COLUMN "{column_name}" {column_type}'
    )


def ensure_table(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS rtd_underlying_quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ativo TEXT NOT NULL UNIQUE,
            ultimo_preco REAL,
            vwap REAL,
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
            created_at TEXT
        )
        """
    )

    ensure_column(conn, "rtd_underlying_quotes", "vwap", "REAL")

    conn.execute(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS idx_rtd_underlying_quotes_ativo
        ON rtd_underlying_quotes(ativo)
        """
    )

    conn.commit()


def detect_delimiter(sample):
    semicolon_count = sample.count(";")
    comma_count = sample.count(",")

    if semicolon_count >= comma_count:
        return ";"

    return ","


def read_records(csv_path):
    with open(csv_path, "r", encoding="utf-8-sig", newline="") as fh:
        sample = fh.read(4096)
        fh.seek(0)

        delimiter = detect_delimiter(sample)
        reader = csv.DictReader(fh, delimiter=delimiter)

        if not reader.fieldnames:
            return []

        field_map = {
            original: normalize_header(original)
            for original in reader.fieldnames
        }

        records = []

        for raw in reader:
            normalized = {
                field_map[key]: value
                for key, value in raw.items()
            }

            ativo = clean_text(normalized.get("ativo"))

            if not ativo:
                continue

            record = {
                "ativo": ativo.upper(),
                "ultimo_preco": parse_number(normalized.get("ultimo_preco")),
                "vwap": parse_number(normalized.get("vwap")),
                "bid": parse_number(normalized.get("bid")),
                "ask": parse_number(normalized.get("ask")),
                "close_price": parse_number(normalized.get("close_price")),
                "prev_close": parse_number(normalized.get("prev_close")),
                "open_price": parse_number(normalized.get("open_price")),
                "high_price": parse_number(normalized.get("high_price")),
                "low_price": parse_number(normalized.get("low_price")),
                "volume": parse_number(normalized.get("volume")),
                "change_percent": parse_number(normalized.get("change_percent")),
            }

            records.append(record)

        return records


def row_exists(conn, ativo):
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id
          FROM rtd_underlying_quotes
         WHERE ativo = ?
         LIMIT 1
        """,
        (ativo,),
    )

    return cur.fetchone() is not None


def upsert_records(conn, records, dry_run=False):
    ensure_table(conn)

    updated_at = now_text()

    stats = {
        "input_rows": len(records),
        "inserted": 0,
        "updated": 0,
        "skipped": 0,
        "updated_at": updated_at,
    }

    if dry_run:
        return stats

    for rec in records:
        ativo = rec["ativo"]
        existed = row_exists(conn, ativo)

        conn.execute(
            """
            INSERT INTO rtd_underlying_quotes (
                ativo,
                ultimo_preco,
                vwap,
                bid,
                ask,
                close_price,
                prev_close,
                open_price,
                high_price,
                low_price,
                volume,
                change_percent,
                source,
                updated_at,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(ativo) DO UPDATE SET
                ultimo_preco = excluded.ultimo_preco,
                vwap = excluded.vwap,
                bid = excluded.bid,
                ask = excluded.ask,
                close_price = excluded.close_price,
                prev_close = excluded.prev_close,
                open_price = excluded.open_price,
                high_price = excluded.high_price,
                low_price = excluded.low_price,
                volume = excluded.volume,
                change_percent = excluded.change_percent,
                source = excluded.source,
                updated_at = excluded.updated_at
            """,
            (
                ativo,
                rec.get("ultimo_preco"),
                rec.get("vwap"),
                rec.get("bid"),
                rec.get("ask"),
                rec.get("close_price"),
                rec.get("prev_close"),
                rec.get("open_price"),
                rec.get("high_price"),
                rec.get("low_price"),
                rec.get("volume"),
                rec.get("change_percent"),
                "btg_rtd_excel_underlying",
                updated_at,
                updated_at,
            ),
        )

        if existed:
            stats["updated"] += 1
        else:
            stats["inserted"] += 1

    conn.commit()

    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM rtd_underlying_quotes")
    stats["row_count_after"] = cur.fetchone()[0]

    return stats


def main():
    parser = argparse.ArgumentParser(
        description="Importa CSV RTD de ativos-base para rtd_underlying_quotes."
    )
    parser.add_argument("--csv", default="dados/RTD_UNDERLYING_QUOTES.csv")
    parser.add_argument("--db", default="dados/app.db")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true")

    args = parser.parse_args()

    csv_path = Path(args.csv)
    db_path = Path(args.db)

    if not csv_path.exists():
        raise SystemExit(f"CSV não encontrado: {csv_path}")

    if not db_path.exists():
        raise SystemExit(f"Banco não encontrado: {db_path}")

    records = read_records(csv_path)

    conn = sqlite3.connect(db_path)

    try:
        stats = upsert_records(conn, records, dry_run=args.dry_run)
    finally:
        conn.close()

    if args.json:
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    else:
        print("Importação RTD underlying CSV")
        print("--------------------------------")
        for key, value in stats.items():
            print(f"{key}: {value}")


if __name__ == "__main__":
    main()
