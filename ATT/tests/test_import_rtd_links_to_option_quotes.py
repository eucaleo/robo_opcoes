import csv
import importlib.util
import sqlite3
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = ROOT / "scripts" / "import_rtd_links_to_option_quotes.py"


spec = importlib.util.spec_from_file_location(
    "import_rtd_links_to_option_quotes",
    SCRIPT_PATH,
)
importer = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = importer
spec.loader.exec_module(importer)


def create_rtd_option_quotes_schema(db_path: Path) -> None:
    conn = sqlite3.connect(str(db_path))

    try:
        conn.execute(
            """
            CREATE TABLE rtd_option_quotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                codigo_opcao TEXT NOT NULL,
                ativo_base TEXT,

                call_put TEXT,
                strike REAL,
                vencimento TEXT,

                ultimo_preco REAL,
                ultima_quantidade REAL,

                bid REAL,
                ask REAL,
                volume REAL,

                iv REAL,
                delta REAL,
                gamma REAL,
                theta REAL,
                vega REAL,

                source TEXT NOT NULL DEFAULT 'rtd_links',
                raw_json TEXT,

                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                UNIQUE(codigo_opcao)
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def write_rtd_links_csv(path: Path, rows: list[list[str]]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "codigo_opcao",
                "ativo_base",
                "campo",
                "valor",
                "atualizado_em",
            ]
        )
        writer.writerows(rows)


def fetch_option(db_path: Path, codigo_opcao: str) -> sqlite3.Row | None:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row

    try:
        return conn.execute(
            """
            SELECT
                codigo_opcao,
                ativo_base,
                call_put,
                strike,
                vencimento,
                ultimo_preco,
                bid,
                ask,
                volume,
                source,
                updated_at,
                raw_json
            FROM rtd_option_quotes
            WHERE codigo_opcao = ?
            """,
            (codigo_opcao,),
        ).fetchone()
    finally:
        conn.close()


def count_options(db_path: Path) -> int:
    conn = sqlite3.connect(str(db_path))

    try:
        return conn.execute("SELECT COUNT(*) FROM rtd_option_quotes").fetchone()[0]
    finally:
        conn.close()


def test_parse_br_number_accepts_common_br_and_us_formats():
    assert importer.parse_br_number("1.234,56") == pytest.approx(1234.56)
    assert importer.parse_br_number("1,23") == pytest.approx(1.23)
    assert importer.parse_br_number("32.50") == pytest.approx(32.50)
    assert importer.parse_br_number("10,000.75") == pytest.approx(10000.75)
    assert importer.parse_br_number("10000") == pytest.approx(10000.0)
    assert importer.parse_br_number("") is None
    assert importer.parse_br_number("-") is None


def test_normalize_call_put_accepts_aliases():
    assert importer.normalize_call_put("CALL") == "CALL"
    assert importer.normalize_call_put("c") == "CALL"
    assert importer.normalize_call_put("compra") == "CALL"

    assert importer.normalize_call_put("PUT") == "PUT"
    assert importer.normalize_call_put("p") == "PUT"
    assert importer.normalize_call_put("venda") == "PUT"

    assert importer.normalize_call_put("") is None


def test_load_and_normalize_vertical_csv(tmp_path: Path):
    csv_path = tmp_path / "RTD_LINKS.csv"

    write_rtd_links_csv(
        csv_path,
        [
            ["PETRA123", "PETR4", "call_put", "CALL", "2026-06-06 17:50:00"],
            ["PETRA123", "PETR4", "strike", "32.50", "2026-06-06 17:50:00"],
            ["PETRA123", "PETR4", "vencimento", "2026-07-19", "2026-06-06 17:50:00"],
            ["PETRA123", "PETR4", "ultimo_preco", "1.23", "2026-06-06 17:50:00"],
            ["PETRA123", "PETR4", "bid", "1.20", "2026-06-06 17:50:00"],
            ["PETRA123", "PETR4", "ask", "1.25", "2026-06-06 17:50:00"],
            ["PETRA123", "PETR4", "volume", "10000", "2026-06-06 17:50:00"],
        ],
    )

    records, stats = importer.load_and_normalize(csv_path)

    assert stats.rows_read == 7
    assert stats.rows_ignored == 0
    assert stats.options_normalized == 1

    record = records[0]

    assert record["codigo_opcao"] == "PETRA123"
    assert record["ativo_base"] == "PETR4"
    assert record["call_put"] == "CALL"
    assert record["strike"] == pytest.approx(32.50)
    assert record["vencimento"] == "2026-07-19"
    assert record["ultimo_preco"] == pytest.approx(1.23)
    assert record["bid"] == pytest.approx(1.20)
    assert record["ask"] == pytest.approx(1.25)
    assert record["volume"] == pytest.approx(10000.0)
    assert record["source"] == "rtd_links"
    assert record["updated_at"] == "2026-06-06 17:50:00"
    assert "PETRA123" in record["raw_json"]


def test_import_csv_to_db_dry_run_does_not_write(tmp_path: Path):
    db_path = tmp_path / "app.db"
    csv_path = tmp_path / "RTD_LINKS.csv"

    create_rtd_option_quotes_schema(db_path)

    write_rtd_links_csv(
        csv_path,
        [
            ["PETRA123", "PETR4", "call_put", "CALL", "2026-06-06 17:50:00"],
            ["PETRA123", "PETR4", "strike", "32.50", "2026-06-06 17:50:00"],
        ],
    )

    stats = importer.import_csv_to_db(
        csv_path=csv_path,
        db_path=db_path,
        dry_run=True,
    )

    assert stats.dry_run is True
    assert stats.rows_read == 2
    assert stats.options_normalized == 1
    assert stats.inserted == 1
    assert stats.updated == 0
    assert count_options(db_path) == 0


def test_import_csv_to_db_upsert_is_idempotent_and_updates_existing_row(tmp_path: Path):
    db_path = tmp_path / "app.db"
    csv_path = tmp_path / "RTD_LINKS.csv"

    create_rtd_option_quotes_schema(db_path)

    write_rtd_links_csv(
        csv_path,
        [
            ["PETRA123", "PETR4", "call_put", "CALL", "2026-06-06 17:50:00"],
            ["PETRA123", "PETR4", "strike", "32.50", "2026-06-06 17:50:00"],
            ["PETRA123", "PETR4", "bid", "1.20", "2026-06-06 17:50:00"],
            ["PETRA123", "PETR4", "ask", "1.25", "2026-06-06 17:50:00"],
        ],
    )

    first_stats = importer.import_csv_to_db(
        csv_path=csv_path,
        db_path=db_path,
        dry_run=False,
    )

    assert first_stats.inserted == 1
    assert first_stats.updated == 0
    assert count_options(db_path) == 1

    write_rtd_links_csv(
        csv_path,
        [
            ["PETRA123", "PETR4", "call_put", "CALL", "2026-06-06 18:00:00"],
            ["PETRA123", "PETR4", "strike", "32.50", "2026-06-06 18:00:00"],
            ["PETRA123", "PETR4", "bid", "1.35", "2026-06-06 18:00:00"],
            ["PETRA123", "PETR4", "ask", "1.40", "2026-06-06 18:00:00"],
        ],
    )

    second_stats = importer.import_csv_to_db(
        csv_path=csv_path,
        db_path=db_path,
        dry_run=False,
    )

    assert second_stats.inserted == 0
    assert second_stats.updated == 1
    assert count_options(db_path) == 1

    option = fetch_option(db_path, "PETRA123")

    assert option is not None
    assert option["codigo_opcao"] == "PETRA123"
    assert option["ativo_base"] == "PETR4"
    assert option["call_put"] == "CALL"
    assert option["strike"] == pytest.approx(32.50)
    assert option["bid"] == pytest.approx(1.35)
    assert option["ask"] == pytest.approx(1.40)
    assert option["source"] == "rtd_links"
    assert option["updated_at"] == "2026-06-06 18:00:00"
