from datetime import datetime

from repositories.robo_legs_status_repository import (
    RoboLegsStatusRepoConfig,
    RoboLegsStatusRepository,
)


def test_latest_timestamps_returns_parsed_manual_and_rtd(tmp_path):
    db_path = tmp_path / "app.db"

    import sqlite3
    conn = sqlite3.connect(db_path)
    conn.execute("CREATE TABLE manual_analise_robo_legs (aba TEXT, timestamp TEXT)")
    conn.execute("CREATE TABLE rtd_analise_robo_legs (aba TEXT, timestamp TEXT)")

    conn.execute(
        "INSERT INTO manual_analise_robo_legs (aba, timestamp) VALUES (?, ?)",
        ("TESTE", "2026-05-19 10:00:00"),
    )
    conn.execute(
        "INSERT INTO manual_analise_robo_legs (aba, timestamp) VALUES (?, ?)",
        ("TESTE", "2026-05-19 11:00:00"),
    )
    conn.execute(
        "INSERT INTO rtd_analise_robo_legs (aba, timestamp) VALUES (?, ?)",
        ("TESTE", "19/05/2026 10:30:00"),
    )
    conn.commit()
    conn.close()

    repo = RoboLegsStatusRepository(
        RoboLegsStatusRepoConfig(app_db_path=str(db_path))
    )

    manual_latest, rtd_latest = repo.latest_timestamps("TESTE")

    assert manual_latest == datetime(2026, 5, 19, 11, 0, 0)
    assert rtd_latest == datetime(2026, 5, 19, 10, 30, 0)


def test_latest_timestamps_returns_none_when_missing(tmp_path):
    db_path = tmp_path / "app.db"

    import sqlite3
    conn = sqlite3.connect(db_path)
    conn.execute("CREATE TABLE manual_analise_robo_legs (aba TEXT, timestamp TEXT)")
    conn.execute("CREATE TABLE rtd_analise_robo_legs (aba TEXT, timestamp TEXT)")
    conn.commit()
    conn.close()

    repo = RoboLegsStatusRepository(
        RoboLegsStatusRepoConfig(app_db_path=str(db_path))
    )

    manual_latest, rtd_latest = repo.latest_timestamps("INEXISTENTE")

    assert manual_latest is None
    assert rtd_latest is None
