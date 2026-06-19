import sqlite3

import pytest

from repositories.market_snapshot_repository import MarketSnapshotRepository


def _create_rtd_legs_table(conn):
    conn.execute(
        """
        CREATE TABLE rtd_analise_robo_legs (
            timestamp TEXT,
            aba TEXT,
            ativo TEXT,
            cv TEXT,
            call_put TEXT,
            quant TEXT,
            valor_executado TEXT,
            bid TEXT,
            ask TEXT,
            spread TEXT,
            spread_pct TEXT,
            iv TEXT,
            delta TEXT,
            gamma TEXT,
            theta TEXT,
            vega TEXT,
            strike TEXT,
            vencimento TEXT,
            dte TEXT,
            pl_realista TEXT
        )
        """
    )


def _create_rtd_option_quotes_table(conn):
    conn.execute(
        """
        CREATE TABLE rtd_option_quotes (
            codigo_opcao TEXT,
            ativo_base TEXT,
            call_put TEXT,
            strike TEXT,
            vencimento TEXT,
            ultimo_preco TEXT,
            ultima_quantidade TEXT,
            bid TEXT,
            ask TEXT,
            volume TEXT,
            iv TEXT,
            delta TEXT,
            gamma TEXT,
            theta TEXT,
            vega TEXT,
            source TEXT,
            raw_json TEXT,
            updated_at TEXT,
            created_at TEXT
        )
        """
    )


def _insert_base_rtd_leg(conn):
    conn.execute(
        """
        INSERT INTO rtd_analise_robo_legs (
            timestamp,
            aba,
            ativo,
            cv,
            call_put,
            quant,
            valor_executado,
            bid,
            ask,
            spread,
            spread_pct,
            iv,
            delta,
            gamma,
            theta,
            vega,
            strike,
            vencimento,
            dte,
            pl_realista
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "2026-05-18 10:00:00",
            "BOVA11",
            "BOVAE195",
            "C",
            "C",
            "5000",
            "1,10",
            "1,00",
            "1,20",
            "0,20",
            "18,18",
            "0,22",
            "0,50",
            "0,01",
            "-0,02",
            "0,03",
            "195,00",
            "2026-05-15",
            "10",
            "100,00",
        ),
    )


def test_get_rtd_option_quote_legs_enriches_base_rtd_leg_with_quote_cache(tmp_path):
    db_path = tmp_path / "app.db"

    with sqlite3.connect(str(db_path)) as conn:
        _create_rtd_legs_table(conn)
        _create_rtd_option_quotes_table(conn)
        _insert_base_rtd_leg(conn)

        conn.execute(
            """
            INSERT INTO rtd_option_quotes (
                codigo_opcao,
                ativo_base,
                call_put,
                strike,
                vencimento,
                ultimo_preco,
                ultima_quantidade,
                bid,
                ask,
                volume,
                iv,
                delta,
                gamma,
                theta,
                vega,
                source,
                raw_json,
                updated_at,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "BOVAE195",
                "BOVA11",
                "CALL",
                "195,00",
                "2026-05-15",
                "1,23",
                "100",
                "1,22",
                "1,24",
                "1000",
                "0,33",
                "0,44",
                "0,055",
                "-0,066",
                "0,077",
                "rtd_option_quotes",
                "{}",
                "2026-05-18 10:05:00",
                "2026-05-18 10:04:00",
            ),
        )
        conn.commit()

    repo = MarketSnapshotRepository(db_path=db_path)

    legs = repo.get_rtd_option_quote_legs("BOVA11")

    assert len(legs) == 1

    leg = legs[0]

    # Identidade/composição vêm da leg estrutural RTD.
    assert leg.aba == "BOVA11"
    assert leg.ativo == "BOVAE195"
    assert leg.cv == "C"
    assert leg.quant == 5000.0
    assert leg.dte == 10.0
    assert leg.pl_realista == 100.0

    # Cotação/greeks vêm do cache centralizado rtd_option_quotes.
    assert leg.source == "rtd_option_quotes"
    assert leg.call_put == "CALL"
    assert leg.bid == 1.22
    assert leg.ask == 1.24
    assert leg.mid == pytest.approx(1.23)
    assert leg.valor_executado == pytest.approx(1.23)
    assert leg.strike == 195.0
    assert leg.vencimento == "2026-05-15"
    assert leg.iv == 0.33
    assert leg.delta == 0.44
    assert leg.gamma == 0.055
    assert leg.theta == -0.066
    assert leg.vega == 0.077
    assert leg.timestamp == "2026-05-18 10:05:00"


def test_get_rtd_option_quote_legs_returns_empty_list_when_cache_table_is_missing(tmp_path):
    db_path = tmp_path / "app.db"

    with sqlite3.connect(str(db_path)) as conn:
        _create_rtd_legs_table(conn)
        _insert_base_rtd_leg(conn)
        conn.commit()

    repo = MarketSnapshotRepository(db_path=db_path)

    assert repo.get_rtd_option_quote_legs("BOVA11") == []
