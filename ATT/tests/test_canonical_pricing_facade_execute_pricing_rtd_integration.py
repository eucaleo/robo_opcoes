import sqlite3

from services.canonical_pricing_facade import CanonicalPricingFacade


class FakePricingExecutionService:
    def __init__(self):
        self.calls = []

    def execute_payload(self, pricing_payload):
        self.calls.append(pricing_payload)

        return {
            "pricing_payload": pricing_payload,
            "result": {
                "engine": "fake",
                "status": "ok",
                "metrics": {
                    "number_of_legs": len(pricing_payload["legs"]),
                    "total_quantity": sum(
                        int(leg["quantity"]) for leg in pricing_payload["legs"]
                    ),
                    "spot_price": float(pricing_payload["spot_price"]),
                },
                "valuation": {
                    "theoretical_value": 0.0,
                },
            },
        }


class FakePricingExecutionPersistenceService:
    def __init__(self):
        self.calls = []

    def persist_execution(
        self,
        pricing_payload,
        result,
        duration_ms,
        error_message=None,
    ):
        self.calls.append(
            {
                "pricing_payload": pricing_payload,
                "result": result,
                "duration_ms": duration_ms,
                "error_message": error_message,
            }
        )

        return {
            "record": {
                "id": 1,
                "execution_status": "ok",
                "execution_engine": result.get("engine"),
            }
        }


def _create_controlled_app_db(db_path):
    with sqlite3.connect(str(db_path)) as conn:
        conn.execute(
            """
            CREATE TABLE structures (
                id INTEGER PRIMARY KEY,
                alias_legacy_aba TEXT,
                underlying_asset TEXT
            )
            """
        )

        conn.execute(
            """
            INSERT INTO structures (
                id,
                alias_legacy_aba,
                underlying_asset
            ) VALUES (?, ?, ?)
            """,
            (123, "ABCD", "ABCD"),
        )

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
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "2026-06-15T10:00:00",
                "ABCD",
                "ABCD11",
                "C",
                "CALL",
                "100",
                "5,55",
                "5,40",
                "5,70",
                "0,30",
                "5,00",
                "0,20",
                "0,50",
                "0,01",
                "-0,02",
                "0,03",
                "10,00",
                "2026-06-15",
                "30",
                "0",
            ),
        )

        conn.execute(
            """
            CREATE TABLE manual_analise_robo_legs (
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
                pl_realista TEXT,
                source TEXT,
                created_at TEXT
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE rtd_analise_robo (
                aba TEXT,
                spot TEXT,
                num_pernas TEXT,
                dte_min TEXT,
                pl_realista_total TEXT,
                delta_liq TEXT,
                gamma_liq TEXT,
                theta_liq TEXT,
                vega_liq TEXT,
                spread_medio TEXT,
                spread_pct_medio TEXT,
                alertas_v2 TEXT
            )
            """
        )

        conn.execute(
            """
            INSERT INTO rtd_analise_robo (
                aba,
                spot,
                num_pernas,
                dte_min,
                pl_realista_total,
                delta_liq,
                gamma_liq,
                theta_liq,
                vega_liq,
                spread_medio,
                spread_pct_medio,
                alertas_v2
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "ABCD",
                "100,00",
                "1",
                "30",
                "0",
                "0",
                "0",
                "0",
                "0",
                "0",
                "0",
                "[]",
            ),
        )

        conn.execute(
            """
            CREATE TABLE rtd_option_quotes (
                codigo_opcao TEXT PRIMARY KEY,
                ativo_base TEXT,
                call_put TEXT,
                strike TEXT,
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
                source TEXT,
                raw_json TEXT,
                updated_at TEXT,
                created_at TEXT
            )
            """
        )

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
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "ABCD11",
                "ABCD",
                "CALL",
                "10.0",
                "2026-06-15",
                9.99,
                100,
                9.80,
                10.20,
                1000,
                0.20,
                0.50,
                0.01,
                -0.02,
                0.03,
                "rtd_option_quotes",
                "{}",
                "2026-06-15T10:01:00",
                "2026-06-15T10:01:00",
            ),
        )

        conn.commit()


def test_execute_pricing_uses_persisted_rtd_option_quote_price(tmp_path):
    app_db = tmp_path / "app.db"
    _create_controlled_app_db(app_db)

    fake_engine_service = FakePricingExecutionService()
    fake_persistence_service = FakePricingExecutionPersistenceService()

    facade = CanonicalPricingFacade(
        db_path=app_db,
        pricing_execution_service=fake_engine_service,
        persistence_service=fake_persistence_service,
    )

    response = facade.execute_pricing(
        structure_id=123,
        reference_date="2026-06-15",
    )

    assert response["status"] == "ok"

    assert len(fake_engine_service.calls) == 1
    pricing_payload = fake_engine_service.calls[0]

    leg = pricing_payload["legs"][0]

    assert pricing_payload["structure_id"] == 123
    assert pricing_payload["underlying_asset"] == "ABCD"
    assert pricing_payload["reference_date"] == "2026-06-15"
    assert pricing_payload["spot_price"] == 100.0

    # O preço original do snapshot era 5.55.
    # O preço efetivo deve vir de rtd_option_quotes.ultimo_preco = 9.99.
    assert leg["symbol"] == "ABCD11"
    assert leg["asset"] == "ABCD11"
    assert leg["price"] == 9.99
    assert leg["premium"] == 9.99
    assert leg["price_source"] == "rtd_option_quotes"
    assert leg["rtd_price_field"] == "ultimo_preco"
    assert leg["rtd_quote_codigo_opcao"] == "ABCD11"
    assert leg["rtd_quote_ativo_base"] == "ABCD"
    assert leg["rtd_price_source"] == "rtd_option_quotes"
    assert leg["rtd_price_updated_at"] == "2026-06-15T10:01:00"
    assert leg["rtd_price_created_at"] == "2026-06-15T10:01:00"

    assert len(fake_persistence_service.calls) == 1
    persisted_payload = fake_persistence_service.calls[0]["pricing_payload"]

    assert persisted_payload["legs"][0]["price"] == 9.99
    assert persisted_payload["legs"][0]["premium"] == 9.99
    assert persisted_payload["legs"][0]["price_source"] == "rtd_option_quotes"
    assert persisted_payload["legs"][0]["rtd_price_field"] == "ultimo_preco"
    assert persisted_payload["legs"][0]["rtd_quote_codigo_opcao"] == "ABCD11"
    assert persisted_payload["legs"][0]["rtd_quote_ativo_base"] == "ABCD"
    assert persisted_payload["legs"][0]["rtd_price_source"] == "rtd_option_quotes"
    assert persisted_payload["legs"][0]["rtd_price_updated_at"] == "2026-06-15T10:01:00"
    assert persisted_payload["legs"][0]["rtd_price_created_at"] == "2026-06-15T10:01:00"


def test_execute_pricing_falls_back_to_snapshot_when_rtd_option_quote_is_missing(tmp_path):
    app_db = tmp_path / "app.db"
    _create_controlled_app_db(app_db)

    with sqlite3.connect(str(app_db)) as conn:
        conn.execute("DELETE FROM rtd_option_quotes WHERE codigo_opcao = ?", ("ABCD11",))
        conn.commit()

    fake_engine_service = FakePricingExecutionService()
    fake_persistence_service = FakePricingExecutionPersistenceService()

    facade = CanonicalPricingFacade(
        db_path=app_db,
        pricing_execution_service=fake_engine_service,
        persistence_service=fake_persistence_service,
    )

    response = facade.execute_pricing(
        structure_id=123,
        reference_date="2026-06-15",
    )

    assert response["status"] == "ok"

    assert len(fake_engine_service.calls) == 1
    pricing_payload = fake_engine_service.calls[0]
    leg = pricing_payload["legs"][0]

    assert pricing_payload["structure_id"] == 123
    assert pricing_payload["underlying_asset"] == "ABCD"
    assert pricing_payload["reference_date"] == "2026-06-15"
    assert pricing_payload["spot_price"] == 100.0

    # Sem quote em rtd_option_quotes, o preço efetivo deve voltar
    # para o preço original do snapshot RTD da perna: valor_executado = 5,55.
    assert leg["symbol"] == "ABCD11"
    assert leg["asset"] == "ABCD11"
    assert leg["price"] == 5.55
    assert leg["premium"] == 5.55
    assert leg["price_source"] == "snapshot"
    assert leg["price_resolution_status"] == "missing_rtd_quote"
    assert leg["rtd_quote_found"] is False
    assert leg["rtd_validation_status"] == "error"
    assert "não encontrada" in leg["rtd_validation_message"]

    assert "rtd_price_field" not in leg
    assert "rtd_quote_codigo_opcao" not in leg
    assert "rtd_quote_ativo_base" not in leg
    assert "rtd_price_source" not in leg
    assert "rtd_price_updated_at" not in leg
    assert "rtd_price_created_at" not in leg

    assert len(fake_persistence_service.calls) == 1
    persisted_payload = fake_persistence_service.calls[0]["pricing_payload"]
    persisted_leg = persisted_payload["legs"][0]

    assert persisted_leg["price"] == 5.55
    assert persisted_leg["premium"] == 5.55
    assert persisted_leg["price_source"] == "snapshot"
    assert persisted_leg["price_resolution_status"] == "missing_rtd_quote"
    assert persisted_leg["rtd_quote_found"] is False
    assert persisted_leg["rtd_validation_status"] == "error"
    assert "não encontrada" in persisted_leg["rtd_validation_message"]

    assert "rtd_price_field" not in persisted_leg
    assert "rtd_quote_codigo_opcao" not in persisted_leg
    assert "rtd_quote_ativo_base" not in persisted_leg
    assert "rtd_price_source" not in persisted_leg
    assert "rtd_price_updated_at" not in persisted_leg
    assert "rtd_price_created_at" not in persisted_leg


def test_execute_pricing_falls_back_to_snapshot_when_rtd_option_quote_price_is_invalid(tmp_path):
    app_db = tmp_path / "app.db"
    _create_controlled_app_db(app_db)

    with sqlite3.connect(str(app_db)) as conn:
        conn.execute(
            """
            UPDATE rtd_option_quotes
            SET ultimo_preco = ?, bid = ?, ask = ?
            WHERE codigo_opcao = ?
            """,
            (0, 0, 0, "ABCD11"),
        )
        conn.commit()

    fake_engine_service = FakePricingExecutionService()
    fake_persistence_service = FakePricingExecutionPersistenceService()

    facade = CanonicalPricingFacade(
        db_path=app_db,
        pricing_execution_service=fake_engine_service,
        persistence_service=fake_persistence_service,
    )

    response = facade.execute_pricing(
        structure_id=123,
        reference_date="2026-06-15",
    )

    assert response["status"] == "ok"

    assert len(fake_engine_service.calls) == 1
    pricing_payload = fake_engine_service.calls[0]
    leg = pricing_payload["legs"][0]

    assert pricing_payload["structure_id"] == 123
    assert pricing_payload["underlying_asset"] == "ABCD"
    assert pricing_payload["reference_date"] == "2026-06-15"
    assert pricing_payload["spot_price"] == 100.0

    # Com quote RTD presente, mas sem preço utilizável, o preço efetivo
    # deve voltar para o snapshot original da perna: valor_executado = 5,55.
    assert leg["symbol"] == "ABCD11"
    assert leg["asset"] == "ABCD11"
    assert leg["price"] == 5.55
    assert leg["premium"] == 5.55
    assert leg["price_source"] == "snapshot"
    assert leg["price_resolution_status"] == "invalid_rtd_price"
    assert leg["rtd_quote_found"] is True
    assert leg["rtd_validation_status"] == "error"
    assert "sem preço utilizável" in leg["rtd_validation_message"]

    assert "rtd_price_field" not in leg
    assert leg["rtd_quote_codigo_opcao"] == "ABCD11"
    assert leg["rtd_quote_ativo_base"] == "ABCD"
    assert leg["rtd_price_source"] == "rtd_option_quotes"
    assert leg["rtd_price_updated_at"] == "2026-06-15T10:01:00"
    assert leg["rtd_price_created_at"] == "2026-06-15T10:01:00"

    assert len(fake_persistence_service.calls) == 1
    persisted_payload = fake_persistence_service.calls[0]["pricing_payload"]
    persisted_leg = persisted_payload["legs"][0]

    assert persisted_leg["price"] == 5.55
    assert persisted_leg["premium"] == 5.55
    assert persisted_leg["price_source"] == "snapshot"
    assert persisted_leg["price_resolution_status"] == "invalid_rtd_price"
    assert persisted_leg["rtd_quote_found"] is True
    assert persisted_leg["rtd_validation_status"] == "error"
    assert "sem preço utilizável" in persisted_leg["rtd_validation_message"]

    assert "rtd_price_field" not in persisted_leg
    assert persisted_leg["rtd_quote_codigo_opcao"] == "ABCD11"
    assert persisted_leg["rtd_quote_ativo_base"] == "ABCD"
    assert persisted_leg["rtd_price_source"] == "rtd_option_quotes"
    assert persisted_leg["rtd_price_updated_at"] == "2026-06-15T10:01:00"
    assert persisted_leg["rtd_price_created_at"] == "2026-06-15T10:01:00"
