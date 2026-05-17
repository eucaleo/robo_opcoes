from datetime import datetime

from dto.robo_leg_dto import FonteType
from repositories.robo_legs_repository import RoboLegsRepoConfig, RoboLegsRepository


def create_legacy_tables(db_path):
    import sqlite3

    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE manual_analise_robo_legs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aba TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                cv TEXT,
                call_put TEXT,
                strike REAL,
                quant INTEGER,
                ativo TEXT,
                vencimento TEXT,
                preco REAL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE rtd_analise_robo_legs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aba TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                cv TEXT,
                call_put TEXT,
                strike REAL,
                quant INTEGER,
                ativo TEXT,
                vencimento TEXT,
                preco REAL
            )
            """
        )
        conn.commit()


def insert_leg(db_path, table, aba, timestamp, cv, call_put, strike, quant, ativo, vencimento, preco):
    import sqlite3

    with sqlite3.connect(db_path) as conn:
        conn.execute(
            f"""
            INSERT INTO {table} (
                aba, timestamp, cv, call_put, strike, quant, ativo, vencimento, preco
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (aba, timestamp, cv, call_put, strike, quant, ativo, vencimento, preco),
        )
        conn.commit()


def test_get_legs_prefers_manual_over_rtd(tmp_path):
    db_path = tmp_path / "app.db"
    create_legacy_tables(db_path)

    insert_leg(
        db_path,
        "manual_analise_robo_legs",
        "BOVA11",
        "2026-05-16 10:00:00",
        "C",
        "CALL",
        120.0,
        2,
        "BOVA11C120",
        "2026-06-20",
        1.5,
    )

    insert_leg(
        db_path,
        "rtd_analise_robo_legs",
        "BOVA11",
        "2026-05-16 10:00:00",
        "V",
        "PUT",
        110.0,
        1,
        "BOVA11P110",
        "2026-06-20",
        0.9,
    )

    repo = RoboLegsRepository(RoboLegsRepoConfig(app_db_path=str(db_path)))

    result = repo.get_legs("BOVA11", "2026-05-16 10:00:00")

    assert len(result) == 1
    assert result[0].fonte == FonteType.MANUAL
    assert result[0].cv == "C"
    assert result[0].call_put == "CALL"


def test_get_legs_falls_back_to_rtd_when_manual_missing(tmp_path):
    db_path = tmp_path / "app.db"
    create_legacy_tables(db_path)

    insert_leg(
        db_path,
        "rtd_analise_robo_legs",
        "PETR4",
        "2026-05-16 10:00:00",
        "V",
        "PUT",
        30.0,
        3,
        "PETR4P30",
        "2026-06-20",
        0.7,
    )

    repo = RoboLegsRepository(RoboLegsRepoConfig(app_db_path=str(db_path)))

    result = repo.get_legs("PETR4", "2026-05-16 10:00:00")

    assert len(result) == 1
    assert result[0].fonte == FonteType.RTD
    assert result[0].ativo == "PETR4P30"


def test_has_manual_returns_true_when_manual_exists(tmp_path):
    db_path = tmp_path / "app.db"
    create_legacy_tables(db_path)

    insert_leg(
        db_path,
        "manual_analise_robo_legs",
        "VALE3",
        "2026-05-16 10:00:00",
        "C",
        "CALL",
        55.0,
        1,
        "VALE3C55",
        "2026-06-20",
        2.1,
    )

    repo = RoboLegsRepository(RoboLegsRepoConfig(app_db_path=str(db_path)))

    assert repo.has_manual("VALE3", "2026-05-16 10:00:00") is True
    assert repo.has_manual("VALE3", "2026-05-16 11:00:00") is False


def test_list_timestamps_prefers_manual_then_rtd(tmp_path):
    db_path = tmp_path / "app.db"
    create_legacy_tables(db_path)

    insert_leg(
        db_path,
        "manual_analise_robo_legs",
        "BOVA11",
        "2026-05-16 09:00:00",
        "C",
        "CALL",
        120.0,
        1,
        "BOVA11C120",
        "2026-06-20",
        1.0,
    )
    insert_leg(
        db_path,
        "rtd_analise_robo_legs",
        "BOVA11",
        "2026-05-16 10:00:00",
        "V",
        "PUT",
        110.0,
        1,
        "BOVA11P110",
        "2026-06-20",
        0.8,
    )

    repo = RoboLegsRepository(RoboLegsRepoConfig(app_db_path=str(db_path)))

    result = repo.list_timestamps("BOVA11")

    assert result == ["2026-05-16 09:00:00"]


def test_list_timestamps_all_returns_union(tmp_path):
    db_path = tmp_path / "app.db"
    create_legacy_tables(db_path)

    insert_leg(
        db_path,
        "manual_analise_robo_legs",
        "BOVA11",
        "2026-05-16 09:00:00",
        "C",
        "CALL",
        120.0,
        1,
        "BOVA11C120",
        "2026-06-20",
        1.0,
    )
    insert_leg(
        db_path,
        "rtd_analise_robo_legs",
        "BOVA11",
        "2026-05-16 10:00:00",
        "V",
        "PUT",
        110.0,
        1,
        "BOVA11P110",
        "2026-06-20",
        0.8,
    )

    repo = RoboLegsRepository(RoboLegsRepoConfig(app_db_path=str(db_path)))

    result = repo.list_timestamps("BOVA11", prefer="all")

    assert result == ["2026-05-16 09:00:00", "2026-05-16 10:00:00"]


def test_timestamp_candidates_supports_multiple_formats():
    ts = datetime(2026, 5, 16, 10, 0, 0)

    result = RoboLegsRepository._timestamp_candidates("2026-05-16 10:00:00", ts)

    assert result == [
        "2026-05-16 10:00:00",
        "16/05/2026 10:00:00",
        "2026-05-16",
        "16/05/2026",
    ]
