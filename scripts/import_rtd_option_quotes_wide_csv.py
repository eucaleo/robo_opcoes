import argparse
import csv
import json
import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from infra.bootstrap_rtd_option_quotes_schema import ensure_rtd_option_quotes_schema


NUMERIC_COLUMNS = {
    "strike",
    "ultimo_preco",
    "ultima_quantidade",
    "bid",
    "ask",
    "volume",
    "vwap",
    "iv",
    "delta",
    "gamma",
    "theta",
    "vega",
}


EXPECTED_COLUMNS = [
    "codigo_opcao",
    "ativo_base",
    "call_put",
    "strike",
    "vencimento",
    "ultimo_preco",
    "ultima_quantidade",
    "bid",
    "ask",
    "volume",
    "vwap",
    "iv",
    "delta",
    "gamma",
    "theta",
    "vega",
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
        "#N/D",
        "#N/A",
        "#VALOR!",
        "#VALUE!",
        "#REF!",
        "#NAME?",
        "#NOME?",
        "#DIV/0!",
        "N/A",
        "NA",
        "NULL",
        "NONE",
        "-",
    }

    if text.upper() in invalids:
        return None

    text = text.replace("R$", "").replace("%", "").strip()

    # Formato BR: 20.119,50 -> 20119.50
    if "," in text:
        text = text.replace(".", "").replace(",", ".")

    try:
        return float(text)
    except ValueError:
        return None


def parse_excel_date(value):
    if value is None:
        return None

    text = str(value).strip()

    if text == "":
        return None

    # Já veio como data textual.
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d/%m/%y"):
        try:
            return datetime.strptime(text, fmt).strftime("%Y-%m-%d")
        except ValueError:
            pass

    serial = parse_number(text)

    if serial is None:
        return None

    # Excel usa 1899-12-30 como base para compatibilidade histórica.
    days = int(serial)
    dt = datetime(1899, 12, 30) + timedelta(days=days)
    return dt.strftime("%Y-%m-%d")


def normalize_call_put(value):
    text = "" if value is None else str(value).strip().upper()

    if text in {"C", "CALL", "COMPRA"}:
        return "CALL"

    if text in {"P", "PUT", "VENDA"}:
        return "PUT"

    return text or None


def clean_text(value):
    if value is None:
        return None

    text = str(value).strip()

    if text == "":
        return None

    return text


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
            codigo = clean_text(raw.get("codigo_opcao"))

            if not codigo:
                continue

            record = {
                "codigo_opcao": codigo.upper(),
                "ativo_base": clean_text(raw.get("ativo_base")),
                "call_put": normalize_call_put(raw.get("call_put")),
                "strike": parse_number(raw.get("strike")),
                "vencimento": parse_excel_date(raw.get("vencimento")),
                "ultimo_preco": parse_number(raw.get("ultimo_preco")),
                "ultima_quantidade": parse_number(raw.get("ultima_quantidade")),
                "bid": parse_number(raw.get("bid")),
                "ask": parse_number(raw.get("ask")),
                "volume": parse_number(raw.get("volume")),
                "vwap": parse_number(raw.get("vwap")),
                "iv": parse_number(raw.get("iv")),
                "delta": parse_number(raw.get("delta")),
                "gamma": parse_number(raw.get("gamma")),
                "theta": parse_number(raw.get("theta")),
                "vega": parse_number(raw.get("vega")),
                "source": "BTG_RTD_EXCEL",
                "raw_json": json.dumps(raw, ensure_ascii=False),
            }

            rows.append(record)

    return rows


def ensure_index(con):
    con.execute("""
        CREATE INDEX IF NOT EXISTS idx_rtd_option_quotes_codigo_opcao
        ON rtd_option_quotes(codigo_opcao)
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

    ensure_rtd_option_quotes_schema(db_path)

    quote_columns = [
        "codigo_opcao",
        "ativo_base",
        "call_put",
        "strike",
        "vencimento",
        "ultimo_preco",
        "ultima_quantidade",
        "bid",
        "ask",
        "volume",
        "vwap",
        "iv",
        "delta",
        "gamma",
        "theta",
        "vega",
        "source",
        "raw_json",
        "updated_at",
    ]

    update_columns = [
        column
        for column in quote_columns
        if column != "codigo_opcao"
    ]

    insert_columns = quote_columns + ["created_at"]

    con = sqlite3.connect(db_path)

    try:
        ensure_index(con)

        for rec in rows:
            codigo = rec["codigo_opcao"]

            existing = con.execute(
                "SELECT id FROM rtd_option_quotes WHERE codigo_opcao = ? ORDER BY id DESC LIMIT 1",
                (codigo,),
            ).fetchone()

            payload = {
                **rec,
                "updated_at": updated_at,
            }

            if existing:
                row_id = existing[0]
                set_clause = ", ".join(
                    f"{column} = ?"
                    for column in update_columns
                )
                params = [
                    payload.get(column)
                    for column in update_columns
                ]
                params.append(row_id)

                con.execute(
                    f"UPDATE rtd_option_quotes SET {set_clause} WHERE id = ?",
                    params,
                )
                stats["updated"] += 1
            else:
                payload["created_at"] = updated_at
                columns_sql = ", ".join(insert_columns)
                placeholders = ", ".join("?" for _ in insert_columns)
                params = [
                    payload.get(column)
                    for column in insert_columns
                ]

                con.execute(
                    f"INSERT INTO rtd_option_quotes ({columns_sql}) VALUES ({placeholders})",
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
        print("Importação RTD wide CSV")
        print("-----------------------")
        for k, v in stats.items():
            print(f"{k}: {v}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
