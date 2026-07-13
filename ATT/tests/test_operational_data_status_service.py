import sqlite3

from services.operational_data_status_service import (
    OperationalDataStatusService,
    build_operational_data_status,
)


def test_status_operacional_retorna_database_missing_sem_criar_arquivo(tmp_path):
    db_path = tmp_path / "app.db"

    status = build_operational_data_status(db_path)

    assert status.database_exists is False
    assert status.status == "database_missing"
    assert status.snapshot_available is False
    assert status.intraday_available is False
    assert status.candles_available is False
    assert status.snapshot_symbols_count == 0
    assert status.intraday_rows_count == 0
    assert status.candles_count == 0
    assert status.latest_update is None
    assert status.errors == ["database_file_not_found"]
    assert db_path.exists() is False


def test_status_operacional_retorna_empty_para_banco_sem_tabelas(tmp_path):
    db_path = tmp_path / "app.db"
    sqlite3.connect(db_path).close()

    service = OperationalDataStatusService(db_path)
    status = service.get_status()

    assert status.database_exists is True
    assert status.status == "empty"
    assert status.snapshot_available is False
    assert status.intraday_available is False
    assert status.candles_available is False
    assert status.snapshot_table is None
    assert status.intraday_table is None
    assert status.candle_table is None
    assert status.errors == []


def test_status_operacional_resume_snapshot_intraday_e_candles(tmp_path):
    db_path = tmp_path / "app.db"

    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE rtd_option_quotes (
                codigo_opcao TEXT,
                updated_at TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE rtd_option_quotes_intraday_history (
                codigo_opcao TEXT,
                captured_at TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE rtd_option_quotes_intraday_candles (
                codigo_opcao TEXT,
                timestamp TEXT
            )
            """
        )

        conn.executemany(
            """
            INSERT INTO rtd_option_quotes (codigo_opcao, updated_at)
            VALUES (?, ?)
            """,
            [
                ("PETRA100", "2026-07-10 10:00:00"),
                ("PETRA100", "2026-07-10 10:01:00"),
                ("PETRA101", "2026-07-10 10:02:00"),
            ],
        )
        conn.executemany(
            """
            INSERT INTO rtd_option_quotes_intraday_history (codigo_opcao, captured_at)
            VALUES (?, ?)
            """,
            [
                ("PETRA100", "2026-07-10 10:03:00"),
                ("PETRA101", "2026-07-10 10:04:00"),
            ],
        )
        conn.execute(
            """
            INSERT INTO rtd_option_quotes_intraday_candles (codigo_opcao, timestamp)
            VALUES (?, ?)
            """,
            ("PETRA100", "2026-07-10 10:05:00"),
        )

    status = build_operational_data_status(db_path)
    payload = status.to_dict()

    assert status.database_exists is True
    assert status.status == "ok"
    assert status.source == "sqlite:" + str(db_path)

    assert status.snapshot_available is True
    assert status.intraday_available is True
    assert status.candles_available is True

    assert status.snapshot_table == "rtd_option_quotes"
    assert status.intraday_table == "rtd_option_quotes_intraday_history"
    assert status.candle_table == "rtd_option_quotes_intraday_candles"

    assert status.snapshot_symbols_count == 2
    assert status.intraday_rows_count == 2
    assert status.candles_count == 1

    assert status.latest_snapshot_update == "2026-07-10 10:02:00"
    assert status.latest_intraday_update == "2026-07-10 10:04:00"
    assert status.latest_candle_update == "2026-07-10 10:05:00"
    assert status.latest_update == "2026-07-10 10:05:00"

    assert payload["status"] == "ok"
    assert payload["snapshot_symbols_count"] == 2


def test_status_operacional_aceita_tabela_alternativa_de_candles(tmp_path):
    db_path = tmp_path / "app.db"

    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE rtd_option_quotes_intraday_candle (
                symbol TEXT,
                created_at TEXT
            )
            """
        )
        conn.execute(
            """
            INSERT INTO rtd_option_quotes_intraday_candle (symbol, created_at)
            VALUES (?, ?)
            """,
            ("PETRA100", "2026-07-10 11:00:00"),
        )

    status = build_operational_data_status(db_path)

    assert status.status == "partial"
    assert status.candles_available is True
    assert status.candle_table == "rtd_option_quotes_intraday_candle"
    assert status.candles_count == 1
    assert status.latest_update == "2026-07-10 11:00:00"


def test_status_operacional_nao_depende_de_excel_ou_subprocesso():
    import inspect
    import services.operational_data_status_service as module

    source = inspect.getsource(module)

    assert "win32com" not in source
    assert "subprocess" not in source
    assert "xlwings" not in source
