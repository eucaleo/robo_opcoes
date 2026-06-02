from datetime import datetime

from repositories.robo_legs_repository import RoboLegsRepoConfig, RoboLegsRepository


def _prepare_db(db_path):
    import sqlite3

    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE manual_analise_robo_legs (
            id INTEGER,
            aba TEXT,
            timestamp TEXT,
            cv TEXT,
            call_put TEXT,
            strike REAL,
            quant INTEGER,
            ativo TEXT,
            vencimento TEXT,
            preco REAL
        )
    """)
    conn.execute("""
        CREATE TABLE rtd_analise_robo_legs (
            id INTEGER,
            aba TEXT,
            timestamp TEXT,
            cv TEXT,
            call_put TEXT,
            strike REAL,
            quant INTEGER,
            ativo TEXT,
            vencimento TEXT,
            preco REAL
        )
    """)
    conn.commit()
    conn.close()


def test_get_legs_prefers_manual_over_rtd(tmp_path):
    db_path = tmp_path / "app.db"
    _prepare_db(db_path)

    import sqlite3
    conn = sqlite3.connect(db_path)
    conn.execute("""
        INSERT INTO manual_analise_robo_legs
        (id, aba, timestamp, cv, call_put, strike, quant, ativo, vencimento, preco)
        VALUES (1, 'AB1', '2026-05-19 10:00:00', 'C', 'CALL', 100, 2, 'PETR4', '2026-06-20', 1.5)
    """)
    conn.execute("""
        INSERT INTO rtd_analise_robo_legs
        (id, aba, timestamp, cv, call_put, strike, quant, ativo, vencimento, preco)
        VALUES (2, 'AB1', '2026-05-19 10:00:00', 'V', 'PUT', 90, 1, 'VALE3', '2026-06-20', 2.0)
    """)
    conn.commit()
    conn.close()

    repo = RoboLegsRepository(RoboLegsRepoConfig(app_db_path=str(db_path)))
    legs = repo.get_legs("AB1", "2026-05-19 10:00:00")

    assert len(legs) == 1
    assert legs[0].id == 1
    assert legs[0].aba == "AB1"
    assert legs[0].cv == "C"
    assert legs[0].call_put == "CALL"
    assert legs[0].ativo == "PETR4"


def test_get_legs_falls_back_to_rtd_when_manual_empty(tmp_path):
    db_path = tmp_path / "app.db"
    _prepare_db(db_path)

    import sqlite3
    conn = sqlite3.connect(db_path)
    conn.execute("""
        INSERT INTO rtd_analise_robo_legs
        (id, aba, timestamp, cv, call_put, strike, quant, ativo, vencimento, preco)
        VALUES (2, 'AB2', '2026-05-19 10:00:00', 'V', 'PUT', 90, 1, 'VALE3', '2026-06-20', 2.0)
    """)
    conn.commit()
    conn.close()

    repo = RoboLegsRepository(RoboLegsRepoConfig(app_db_path=str(db_path)))
    legs = repo.get_legs("AB2", "2026-05-19 10:00:00")

    assert len(legs) == 1
    assert legs[0].id == 2
    assert legs[0].cv == "V"
    assert legs[0].call_put == "PUT"
    assert legs[0].ativo == "VALE3"


def test_has_manual_detects_existing_row(tmp_path):
    db_path = tmp_path / "app.db"
    _prepare_db(db_path)

    import sqlite3
    conn = sqlite3.connect(db_path)
    conn.execute("""
        INSERT INTO manual_analise_robo_legs
        (id, aba, timestamp, cv, call_put, strike, quant, ativo, vencimento, preco)
        VALUES (1, 'AB3', '2026-05-19 10:00:00', 'C', 'CALL', 100, 2, 'PETR4', '2026-06-20', 1.5)
    """)
    conn.commit()
    conn.close()

    repo = RoboLegsRepository(RoboLegsRepoConfig(app_db_path=str(db_path)))

    assert repo.has_manual("AB3", "2026-05-19 10:00:00") is True
    assert repo.has_manual("AB3", "2026-05-19 11:00:00") is False


def test_list_timestamps_prefers_manual_then_rtd(tmp_path):
    db_path = tmp_path / "app.db"
    _prepare_db(db_path)

    import sqlite3
    conn = sqlite3.connect(db_path)
    conn.execute("""
        INSERT INTO manual_analise_robo_legs
        (id, aba, timestamp, cv, call_put, strike, quant, ativo, vencimento, preco)
        VALUES (1, 'AB4', '2026-05-19 09:00:00', 'C', 'CALL', 100, 1, 'PETR4', '2026-06-20', 1.0)
    """)
    conn.execute("""
        INSERT INTO manual_analise_robo_legs
        (id, aba, timestamp, cv, call_put, strike, quant, ativo, vencimento, preco)
        VALUES (2, 'AB4', '2026-05-19 10:00:00', 'V', 'PUT', 95, 1, 'PETR4', '2026-06-20', 1.2)
    """)
    conn.execute("""
        INSERT INTO rtd_analise_robo_legs
        (id, aba, timestamp, cv, call_put, strike, quant, ativo, vencimento, preco)
        VALUES (3, 'AB4', '2026-05-19 11:00:00', 'V', 'PUT', 95, 1, 'PETR4', '2026-06-20', 1.2)
    """)
    conn.commit()
    conn.close()

    repo = RoboLegsRepository(RoboLegsRepoConfig(app_db_path=str(db_path)))
    timestamps = repo.list_timestamps("AB4")

    assert timestamps == ["2026-05-19 09:00:00", "2026-05-19 10:00:00"]


def test_list_timestamps_all_returns_union(tmp_path):
    db_path = tmp_path / "app.db"
    _prepare_db(db_path)

    import sqlite3
    conn = sqlite3.connect(db_path)
    conn.execute("""
        INSERT INTO manual_analise_robo_legs
        (id, aba, timestamp, cv, call_put, strike, quant, ativo, vencimento, preco)
        VALUES (1, 'AB5', '2026-05-19 10:00:00', 'C', 'CALL', 100, 1, 'PETR4', '2026-06-20', 1.0)
    """)
    conn.execute("""
        INSERT INTO rtd_analise_robo_legs
        (id, aba, timestamp, cv, call_put, strike, quant, ativo, vencimento, preco)
        VALUES (2, 'AB5', '2026-05-19 11:00:00', 'V', 'PUT', 95, 1, 'PETR4', '2026-06-20', 1.2)
    """)
    conn.commit()
    conn.close()

    repo = RoboLegsRepository(RoboLegsRepoConfig(app_db_path=str(db_path)))
    timestamps = repo.list_timestamps("AB5", prefer="all")

    assert timestamps == ["2026-05-19 10:00:00", "2026-05-19 11:00:00"]


def test_timestamp_candidates_include_multiple_formats():
    repo = RoboLegsRepository()
    ts = datetime(2026, 5, 19, 10, 30, 0)

    candidates = repo._timestamp_candidates("19/05/2026 10:30:00", ts)

    assert "19/05/2026 10:30:00" in candidates
    assert "2026-05-19 10:30:00" in candidates
    assert "2026-05-19" in candidates
    assert "19/05/2026" in candidates
