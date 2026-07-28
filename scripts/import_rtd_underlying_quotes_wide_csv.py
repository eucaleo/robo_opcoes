import argparse
import csv
import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


EXPECTED_COLUMNS = [
    "ativo",
    "ultimo_preco",
    "bid",
    "ask",
    "close_price",
    "prev_close",
    "open_price",
    "high_price",
    "low_price",
    "volume",
    "change_percent",
]


def now_text():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def parse_number(value):
    if value is None:
        return None

    text = str(value).strip()

    if text == "":
        return None

    invalids = {
        "#N/D", "#N/A", "#VALOR!", "#VALUE!", "#REF!",
        "#NAME?", "#NOME?", "#DIV/0!", "N/A", "NA",
        "NULL", "NONE", "-",
    }

    if text.upper() in invalids:
        return None

    text = text.replace("R$", "").replace("%", "").strip()

    # Notação científica tipo "6,72E+08"
    if "E+" in text.upper() or "E-" in text.upper():
        text = text.replace(",", ".")
        try:
            return float(text)
        except ValueError:
            return None

    # Formato BR: 20.119,50 -> 20119.50
    if "," in text:
        text = text.replace(".", "").replace(",", ".")

    try:
        return float(text)
    except ValueError:
        return None


def clean_text(value):
    if value is None:
        return None

    text = str(value).strip()
    return text or None


def detect_dialect(csv_path):
    sample = Path(csv_path).read_text(encoding="utf-8-sig", errors="replace")[:4096]

    try:
        return csv.Sniffer().sniff(sample, delimiters=";,")
    except csv.Error:
        class Dialect(csv.excel):
            delimiter = ";"

        return Dialect


def load_csv(csv_path):
    dialect = detect_dialect(csv_path)
    rows = []

    with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, dialect=dialect)

        if not reader.fieldnames:
            raise ValueError("CSV sem cabeçalho.")

        fieldnames = [c.strip() for c in reader.fieldnames]
        missing = [c for c in EXPECTED_COLUMNS if c not in fieldnames]

        if missing:
            raise ValueError("CSV sem colunas obrigatórias: " + ", ".join(missing))

        for raw in reader:
            raw = {str(k).strip(): v for k, v in raw.items() if k is not None}
            ativo = clean_text(raw.get("ativo"))

            if not ativo:
                continue

            record = {
                "ativo": ativo.upper(),
                "ultimo_preco": parse_number(raw.get("ultimo_preco")),
                "bid": parse_number(raw.get("bid")),
                "ask": parse_number(raw.get("ask")),
                "close_price": parse_number(raw.get("close_price")),
                "prev_close": parse_number(raw.get("prev_close")),
                "open_price": parse_number(raw.get("open_price")),
                "high_price": parse_number(raw.get("high_price")),
                "low_price": parse_number(raw.get("low_price")),
                "volume": parse_number(raw.get("volume")),
                "change_percent": parse_number(raw.get("change_percent")),
                "vwap": parse_number(raw.get("vwap")),  # opcional, pode não existir no CSV
                "source": "BTG_RTD_EXCEL",
            }

            rows.append(record)

    return rows


def ensure_schema(con):
    con.execute("""
        CREATE TABLE IF NOT EXISTS rtd_underlying_quotes (
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
    """)

    con.execute("""
        CREATE INDEX IF NOT EXISTS idx_rtd_underlying_quotes_ativo
        ON rtd_underlying_quotes(ativo)
    """)


def import_rows(db_path, rows, dry_run=False):
    updated_at = now_text()

    stats = {
        "input_rows": len(rows),
        "inserted": 0,
        "updated": 0,
        "skipped": 0,
        "updated_at": updated_at,
    }

    if dry_run:
        return stats

    quote_columns = [
        "ativo", "ultimo_preco", "bid", "ask", "close_price",
        "prev_close", "open_price", "high_price", "low_price",
        "volume", "change_percent", "vwap", "source", "updated_at",
    ]

    update_columns = [c for c in quote_columns if c != "ativo"]
    insert_columns = quote_columns + ["created_at"]

    con = sqlite3.connect(db_path)

    try:
        ensure_schema(con)

        for rec in rows:
            ativo = rec["ativo"]

            existing = con.execute(
                "SELECT id FROM rtd_underlying_quotes WHERE ativo = ? ORDER BY id DESC LIMIT 1",
                (ativo,),
            ).fetchone()

            payload = {**rec, "updated_at": updated_at}

            if existing:
                row_id = existing[0]
                set_clause = ", ".join(f"{c} = ?" for c in update_columns)
                params = [payload.get(c) for c in update_columns]
                params.append(row_id)

                con.execute(
                    f"UPDATE rtd_underlying_quotes SET {set_clause} WHERE id = ?",
                    params,
                )
                stats["updated"] += 1
            else:
                payload["created_at"] = updated_at
                columns_sql = ", ".join(insert_columns)
                placeholders = ", ".join("?" for _ in insert_columns)
                params = [payload.get(c) for c in insert_columns]

                con.execute(
                    f"INSERT INTO rtd_underlying_quotes ({columns_sql}) VALUES ({placeholders})",
                    params,
                )
                stats["inserted"] += 1

        con.commit()
    finally:
        con.close()

    return stats


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True)
    parser.add_argument("--db", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    rows = load_csv(args.csv)
    stats = import_rows(args.db, rows, dry_run=args.dry_run)

    if args.json:
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    else:
        print("Importação RTD Underlying wide CSV")
        print("-----------------------------------")
        for k, v in stats.items():
            print(f"{k}: {v}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
