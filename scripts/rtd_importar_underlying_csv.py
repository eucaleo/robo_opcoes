from pathlib import Path
import csv
import sqlite3
import sys
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]

APP_DB = ROOT / "dados" / "app.db"
DERIVED_DB = ROOT / "dados" / "derived.db"

TARGET_TABLE = "rtd_underlying_quotes"


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

    # Remove moeda e espaços.
    s = (
        s.replace("R$", "")
        .replace(" ", "")
        .replace("\u00a0", "")
    )

    # Formato brasileiro: 1.234,56
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


def ensure_table(con):
    con.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {TARGET_TABLE} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ativo TEXT NOT NULL,
            ultimo_preco REAL,
            bid REAL,
            ask REAL,
            vwap REAL,
            volume REAL,
            source TEXT,
            raw_json TEXT,
            updated_at TEXT,
            created_at TEXT
        )
        """
    )

    cols = [r[1] for r in con.execute(f"PRAGMA table_info({TARGET_TABLE})").fetchall()]

    wanted = {
        "ativo": "TEXT",
        "ultimo_preco": "REAL",
        "bid": "REAL",
        "ask": "REAL",
        "vwap": "REAL",
        "volume": "REAL",
        "source": "TEXT",
        "raw_json": "TEXT",
        "updated_at": "TEXT",
        "created_at": "TEXT",
    }

    for col, typ in wanted.items():
        if col not in cols:
            con.execute(f"ALTER TABLE {TARGET_TABLE} ADD COLUMN {col} {typ}")


def upsert_underlying(con, item):
    ensure_table(con)

    ativo = item["ativo"]

    existing = con.execute(
        f"""
        SELECT id
        FROM {TARGET_TABLE}
        WHERE ativo = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (ativo,),
    ).fetchone()

    if existing:
        con.execute(
            f"""
            UPDATE {TARGET_TABLE}
            SET
                ultimo_preco = COALESCE(?, ultimo_preco),
                bid = COALESCE(?, bid),
                ask = COALESCE(?, ask),
                vwap = COALESCE(?, vwap),
                volume = COALESCE(?, volume),
                source = ?,
                updated_at = ?
            WHERE id = ?
            """,
            (
                item["ultimo_preco"],
                item["bid"],
                item["ask"],
                item["vwap"],
                item["volume"],
                item["source"],
                item["updated_at"],
                existing["id"],
            ),
        )
        return "updated"

    con.execute(
        f"""
        INSERT INTO {TARGET_TABLE} (
            ativo,
            ultimo_preco,
            bid,
            ask,
            vwap,
            volume,
            source,
            updated_at,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            item["ativo"],
            item["ultimo_preco"],
            item["bid"],
            item["ask"],
            item["vwap"],
            item["volume"],
            item["source"],
            item["updated_at"],
            item["created_at"],
        ),
    )
    return "inserted"


def parse_csv(path):
    dialect = detect_dialect(path)

    rows = []
    with path.open("r", encoding="utf-8-sig", errors="ignore", newline="") as f:
        reader = csv.DictReader(f, dialect=dialect)

        print("Colunas detectadas:")
        print(reader.fieldnames)
        print()

        for row in reader:
            ativo = pick(row, ["ativo", "ticker", "codigo", "símbolo", "simbolo", "papel"])

            if not ativo:
                continue

            ativo = str(ativo).strip().upper()

            item = {
                "ativo": ativo,
                "ultimo_preco": to_float(
                    pick(row, ["ultimo_preco", "último_preço", "ultimo", "último", "last", "preco", "preço"])
                ),
                "bid": to_float(
                    pick(row, ["bid", "compra", "melhor_compra"])
                ),
                "ask": to_float(
                    pick(row, ["ask", "venda", "melhor_venda"])
                ),
                "vwap": to_float(
                    pick(row, ["vwap", "preco_medio", "preço_médio", "medio", "médio"])
                ),
                "volume": to_float(
                    pick(row, ["volume", "vol", "volume_financeiro"])
                ),
                "source": "BTG_RTD_EXCEL_UNDERLYING_CSV",
                "updated_at": now_sqlite(),
                "created_at": now_sqlite(),
            }

            rows.append(item)

    return rows


def print_table(con, db_name):
    print()
    print("=" * 100)
    print(f"{db_name}:{TARGET_TABLE}")
    print("=" * 100)

    try:
        result = con.execute(
            f"""
            SELECT ativo, ultimo_preco, bid, ask, vwap, volume, source, updated_at
            FROM {TARGET_TABLE}
            ORDER BY ativo
            """
        ).fetchall()

        for r in result:
            print(dict(r))
    except Exception as exc:
        print("ERRO lendo tabela:", exc)


def main():
    if len(sys.argv) < 2:
        raise SystemExit(
            "Uso:\n"
            "  python scripts/rtd_importar_underlying_csv.py caminho/do/arquivo.csv\n\n"
            "Exemplo:\n"
            "  python scripts/rtd_importar_underlying_csv.py dados/RTD_UNDERLYING_QUOTES.csv"
        )

    csv_path = Path(sys.argv[1])

    if not csv_path.is_absolute():
        csv_path = ROOT / csv_path

    if not csv_path.exists():
        raise SystemExit(f"CSV não encontrado: {csv_path}")

    items = parse_csv(csv_path)

    print("=" * 100)
    print("Itens lidos do CSV")
    print("=" * 100)

    for item in items:
        print(item)

    if not items:
        raise SystemExit("Nenhum ativo encontrado no CSV.")

    for db_path in [APP_DB, DERIVED_DB]:
        con = sqlite3.connect(str(db_path))
        con.row_factory = sqlite3.Row

        inserted = 0
        updated = 0

        for item in items:
            action = upsert_underlying(con, item)

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

        print_table(con, str(db_path.relative_to(ROOT)))

        con.close()


if __name__ == "__main__":
    main()
