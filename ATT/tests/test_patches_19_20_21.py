# ATT/tests/test_patches_19_20_21.py
"""
Testes dos patches 19, 20 e 21.

  patch_19 -- PricingExecutionsRepository: JSON  SQLite (app.db)
  patch_20 -- payoff_features.upsert_curve_summary: try/finally (ResourceWarning fix)
  patch_21 -- Pipeline conectado: payoff + decisão gravados no derived.db

Execução:
    pytest ATT/tests/test_patches_19_20_21.py -v
"""

from __future__ import annotations

import sqlite3
import sys
import tempfile
import traceback
from pathlib import Path
from unittest.mock import MagicMock, patch

# ---------------------------------------------------------------------------
# helpers de assert simples (sem pytest obrigatório)
# ---------------------------------------------------------------------------

_PASS = "[OK]"
_FAIL = "[FALHOU]"
_results: list[tuple[str, bool, str]] = []


def _check(name: str, condition: bool, detail: str = "") -> None:
    icon = _PASS if condition else _FAIL
    _results.append((name, condition, detail))
    print(f"  {icon}  {name}" + (f"    {detail}" if detail else ""))
    if not condition:
        raise AssertionError(f"FALHOU: {name}  {detail}")


# ---------------------------------------------------------------------------
# Fixture helpers
# ---------------------------------------------------------------------------

def _make_db(tmp: str) -> Path:
    """
    Cria app.db com schema completo e PRAGMA foreign_keys=OFF
    para permitir structure_id arbitrários nos testes.
    """
    from infra.bootstrap_structures_schema import ensure_structures_schema

    db_path = Path(tmp) / "app.db"
    ensure_structures_schema(db_path)

    # Desabilita FK para testes (banco isolado, sem dados de structures)
    with sqlite3.connect(str(db_path)) as conn:
        conn.execute("PRAGMA foreign_keys = OFF")
        conn.commit()

    return db_path


def _make_repo(db_path: Path):
    from repositories.pricing_executions_repository import PricingExecutionsRepository

    repo = PricingExecutionsRepository(db_path=db_path)
    # Garante FK desabilitada também na conexão interna do repo
    _patch_repo_conn(repo)
    return repo


def _patch_repo_conn(repo) -> None:
    """
    Monkey-patch: envolve _connect() para executar
    PRAGMA foreign_keys=OFF em cada nova conexão.
    """
    original_connect = repo._connect.__func__ if hasattr(repo._connect, "__func__") else None

    def _patched_connect():
        conn = sqlite3.connect(str(repo._db_path))
        conn.execute("PRAGMA foreign_keys = OFF")
        return conn

    repo._connect = _patched_connect


def _tmp_dir() -> tempfile.TemporaryDirectory:
    """TemporaryDirectory com ignore_cleanup_errors=True (fix WinError 32)."""
    return tempfile.TemporaryDirectory(ignore_cleanup_errors=True)


# ===========================================================================
# patch_19 -- PricingExecutionsRepository  SQLite
# ===========================================================================

def test_patch19_save_and_read() -> None:
    print("\n patch_19: PricingExecutionsRepository (SQLite) ")

    with _tmp_dir() as tmp:
        db_path = _make_db(tmp)
        repo = _make_repo(db_path)

        payload = {
            "structure_id":     42,
            "underlying_asset": "PETR4",
            "reference_date":   "2026-05-28",
            "spot_price":       37.50,
            "legs":             [{"strike": 38.0, "option_type": "call"}],
        }
        result = {
            "engine":    "stub",
            "status":    "success",
            "metrics":   {"number_of_legs": 1, "total_quantity": 100},
            "valuation": {"theoretical_value": 1.25},
        }

        record = repo.save_execution(
            pricing_payload=payload,
            result=result,
            execution_status="success",
            execution_engine="stub",
            duration_ms=42,
            number_of_legs=1,
            total_quantity=100,
            theoretical_value=1.25,
        )

        _check("save_execution retorna dict",         isinstance(record, dict))
        _check("record tem id inteiro",               isinstance(record.get("id"), int))
        _check("record.id >= 1",                      record["id"] >= 1)
        _check("structure_id preservado",             record["structure_id"] == 42)
        _check("underlying_asset preservado",         record["underlying_asset"] == "PETR4")
        _check("theoretical_value preservado",        record["theoretical_value"] == 1.25)

        fetched = repo.get_execution(record["id"])
        _check("get_execution retorna registro",              fetched is not None)
        _check("result deserializado é dict",                 isinstance(fetched["result"], dict))
        _check("pricing_payload deserializado é dict",        isinstance(fetched["pricing_payload"], dict))
        _check("pricing_payload.spot_price correto",          fetched["pricing_payload"]["spot_price"] == 37.50)


def test_patch19_list_and_count() -> None:
    print("\n patch_19: list_executions / count_executions ")

    with _tmp_dir() as tmp:
        db_path = _make_db(tmp)
        repo = _make_repo(db_path)

        base_result = {
            "engine": "stub", "status": "success",
            "metrics": {}, "valuation": {},
        }

        for i in range(5):
            repo.save_execution(
                pricing_payload={
                    "structure_id":     i + 1,
                    "underlying_asset": "BOVA11",
                    "reference_date":   "2026-05-28",
                },
                result=base_result,
                execution_status="success",
            )

        repo.save_execution(
            pricing_payload={
                "structure_id":     99,
                "underlying_asset": "BOVA11",
                "reference_date":   "2026-05-28",
            },
            result={**base_result, "status": "error"},
            execution_status="error",
        )

        total     = repo.count_executions()
        count_ok  = repo.count_executions(status="success")
        count_err = repo.count_executions(status="error")

        _check("count total = 6",   total     == 6)
        _check("count success = 5", count_ok  == 5)
        _check("count error = 1",   count_err == 1)

        page1 = repo.list_executions(page=1, page_size=3)
        page2 = repo.list_executions(page=2, page_size=3)

        _check("list page_size=3 retorna 3",            len(page1) == 3)
        _check("list page2 retorna 3",                  len(page2) == 3)

        all_ids = {r["id"] for r in page1} | {r["id"] for r in page2}
        _check("ids de page1 e page2 sem sobreposição", len(all_ids) == 6)


def test_patch19_get_latest_by_structure() -> None:
    print("\n patch_19: get_latest_by_structure ")

    with _tmp_dir() as tmp:
        db_path = _make_db(tmp)
        repo = _make_repo(db_path)

        base = {
            "engine": "stub", "status": "success",
            "metrics": {}, "valuation": {},
        }

        repo.save_execution(
            pricing_payload={
                "structure_id": 7, "underlying_asset": "VALE3",
                "reference_date": "2026-05-27",
            },
            result=base,
            execution_status="success",
        )
        r2 = repo.save_execution(
            pricing_payload={
                "structure_id": 7, "underlying_asset": "VALE3",
                "reference_date": "2026-05-28",
            },
            result=base,
            execution_status="success",
        )

        latest = repo.get_latest_by_structure(structure_id=7)
        _check("get_latest retorna o mais recente",           latest["id"] == r2["id"])

        none_result = repo.get_latest_by_structure(structure_id=9999)
        _check("get_latest structure inexistente retorna None", none_result is None)


def test_patch19_no_json_file_created() -> None:
    print("\n patch_19: arquivo JSON não deve ser criado ")

    with _tmp_dir() as tmp:
        db_path = _make_db(tmp)
        repo = _make_repo(db_path)

        repo.save_execution(
            pricing_payload={"structure_id": 1},
            result={
                "engine": "stub", "status": "success",
                "metrics": {}, "valuation": {},
            },
            execution_status="success",
        )

        json_files = list(Path(tmp).rglob("*.json"))
        _check("nenhum arquivo .json criado", len(json_files) == 0)
        _check("app.db existe",               db_path.exists())

        with sqlite3.connect(str(db_path)) as conn:
            conn.execute("PRAGMA foreign_keys = OFF")
            count = conn.execute(
                "SELECT COUNT(*) FROM pricing_executions"
            ).fetchone()[0]
        _check("1 registro no SQLite", count == 1)


# ===========================================================================
# patch_20 -- payoff_features try/finally
# ===========================================================================

def _create_derived_db(path: Path) -> None:
    """Cria tabela payoff_curve_summary no db temporário."""
    with sqlite3.connect(str(path)) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS payoff_curve_summary (
                structure_id       TEXT    NOT NULL,
                reference_date     TEXT    NOT NULL,
                timestamp          TEXT,
                aba                TEXT,
                spot_ref           REAL,
                points_count       INTEGER,
                pl_min             REAL,
                pl_max             REAL,
                pl_at_spot_ref     REAL,
                breakevens_json    TEXT,
                be_count           INTEGER,
                pos_ranges_json    TEXT,
                pos_ranges_count   INTEGER,
                max_drawdown_like  REAL,
                meta_json          TEXT,
                PRIMARY KEY (structure_id, reference_date)
            )
        """)
        conn.commit()


def test_patch20_upsert_no_resource_leak() -> None:
    print("\n patch_20: upsert_curve_summary try/finally (sem leak) ")

    import domain.payoff_features as pf

    with _tmp_dir() as tmp:
        derived_db = Path(tmp) / "derived.db"
        _create_derived_db(derived_db)

        original_get_conn = pf.get_derived_db_connection

        def _patched_conn():
            return sqlite3.connect(str(derived_db))

        pf.get_derived_db_connection = _patched_conn

        try:
            features = {
                "structure_id":      "patch20-petr4-001",
                "reference_date":    "2026-05-28",
                "timestamp":         "2026-05-28T10:00:00",
                "aba":               "PETR4",
                "spot_ref":          37.5,
                "points_count":      5,
                "pl_min":           -500.0,
                "pl_max":            800.0,
                "pl_at_spot_ref":    120.0,
                "breakevens":        [35.0, 40.0],
                "be_count":          2,
                "pos_ranges":        [[35.0, 40.0]],
                "pos_ranges_count":  1,
                "max_drawdown_like": 1300.0,
                "meta":              {"engine": "stub"},
            }

            pf.upsert_curve_summary(features)

            # Descobre o índice real da coluna pl_max via PRAGMA
            with sqlite3.connect(str(derived_db)) as conn:
                col_names = [
                    r[1] for r in conn.execute(
                        "PRAGMA table_info(payoff_curve_summary)"
                    ).fetchall()
                ]
                row = conn.execute(
                    "SELECT * FROM payoff_curve_summary WHERE aba='PETR4'"
                ).fetchone()

            _check("registro gravado no derived.db", row is not None)

            pl_max_idx = col_names.index("pl_max")
            _check(
                f"pl_max correto (coluna índice {pl_max_idx})",
                row[pl_max_idx] == 800.0,
                f"esperado=800.0 obtido={row[pl_max_idx]}",
            )

            # Idempotência -- upsert com pl_max diferente
            features["pl_max"] = 999.0
            pf.upsert_curve_summary(features)

            with sqlite3.connect(str(derived_db)) as conn:
                count = conn.execute(
                    "SELECT COUNT(*) FROM payoff_curve_summary WHERE aba='PETR4'"
                ).fetchone()[0]
                row2 = conn.execute(
                    "SELECT * FROM payoff_curve_summary WHERE aba='PETR4'"
                ).fetchone()

            _check("upsert não duplica registro",   count == 1)
            _check("pl_max atualizado pelo upsert", row2[pl_max_idx] == 999.0)

        finally:
            pf.get_derived_db_connection = original_get_conn


def test_patch20_missing_timestamp_raises() -> None:
    print("\n patch_20: ValueError se timestamp/aba ausente ")

    import domain.payoff_features as pf

    raised_ts = False
    try:
        pf.upsert_curve_summary({"aba": "PETR4"})
    except ValueError:
        raised_ts = True

    _check("ValueError levantado sem timestamp", raised_ts)

    raised_aba = False
    try:
        pf.upsert_curve_summary({"timestamp": "2026-05-28T10:00:00"})
    except ValueError:
        raised_aba = True

    _check("ValueError levantado sem aba", raised_aba)


# ===========================================================================
# patch_21 -- Pipeline connected: derived.db gravado após execute_pricing
# ===========================================================================

def _make_service_with_mock_port(db_path: Path):
    """Cria PricingExecutionPersistenceService com mock_port e repo patchado."""
    from repositories.pricing_executions_repository import PricingExecutionsRepository
    from services.pricing_execution_persistence_service import PricingExecutionPersistenceService

    mock_port = MagicMock()
    service = PricingExecutionPersistenceService(payoff_persistence_port=mock_port)
    repo = PricingExecutionsRepository(db_path=db_path)
    _patch_repo_conn(repo)
    service.pricing_executions_repository = repo
    return service, mock_port


def test_patch21_port_called_on_success() -> None:
    print("\n patch_21: PayoffPersistencePort.persist() chamado em sucesso ")

    with _tmp_dir() as tmp:
        db_path = _make_db(tmp)
        service, mock_port = _make_service_with_mock_port(db_path)

        payload = {
            "structure_id":     1,
            "underlying_asset": "PETR4",
            "reference_date":   "2026-05-28",
            "spot_price":       37.5,
        }
        result = {
            "engine":    "stub",
            "status":    "success",
            "metrics":   {"number_of_legs": 2, "total_quantity": 200},
            "valuation": {"theoretical_value": 2.50},
        }

        service.persist_execution(
            pricing_payload=payload,
            result=result,
            duration_ms=10,
        )

        _check("port.persist() foi chamado 1x", mock_port.persist.call_count == 1)

        call_args = mock_port.persist.call_args
        # Suporta chamada posicional ou keyword
        called_payload = (
            call_args.kwargs.get("pricing_payload")
            or (call_args.args[0] if call_args.args else None)
        )
        called_result = (
            call_args.kwargs.get("result")
            or (call_args.args[1] if len(call_args.args) > 1 else None)
        )

        _check("port recebeu pricing_payload correto", called_payload["structure_id"] == 1)
        _check("port recebeu result correto",          called_result["status"] == "success")


def test_patch21_port_not_called_without_injection() -> None:
    print("\n patch_21: sem injeção, pipeline não falha (retrocompatível) ")

    from repositories.pricing_executions_repository import PricingExecutionsRepository
    from services.pricing_execution_persistence_service import PricingExecutionPersistenceService

    with _tmp_dir() as tmp:
        db_path = _make_db(tmp)

        service = PricingExecutionPersistenceService()   # sem port
        repo = PricingExecutionsRepository(db_path=db_path)
        _patch_repo_conn(repo)
        service.pricing_executions_repository = repo

        result = service.persist_execution(
            pricing_payload={"structure_id": 1, "underlying_asset": "X"},
            result={
                "engine": "stub", "status": "success",
                "metrics": {}, "valuation": {},
            },
        )

        _check("persist_execution retorna dict mesmo sem port", isinstance(result, dict))
        _check("record presente no retorno",                    "record" in result)


def test_patch21_port_exception_does_not_raise() -> None:
    print("\n patch_21: exceção no port não derruba persist_execution ")

    with _tmp_dir() as tmp:
        db_path = _make_db(tmp)
        service, mock_port = _make_service_with_mock_port(db_path)
        mock_port.persist.side_effect = RuntimeError("derived.db offline!")

        raised = False
        result = None
        try:
            result = service.persist_execution(
                pricing_payload={"structure_id": 2, "underlying_asset": "Y"},
                result={
                    "engine": "stub", "status": "success",
                    "metrics": {}, "valuation": {},
                },
            )
        except Exception:
            raised = True

        _check("exceção no port não propaga",                            not raised)
        _check("persist_execution retorna dict mesmo com falha no port", isinstance(result, dict))


def test_patch21_facade_wiring() -> None:
    print("\n patch_21: CanonicalPricingFacade instancia DerivedPayoffPersistence ")

    # Mock do módulo derived_service antes de qualquer import da facade
    import sys
    from unittest.mock import MagicMock

    # Stub para evitar ModuleNotFoundError de 'derived_service'
    fake_derived_service = MagicMock()
    fake_derived_service.save_payoff_from_canonical_payload = MagicMock()
    fake_derived_service.save_decision_from_canonical_payload = MagicMock()

    with patch.dict(sys.modules, {"derived_service": fake_derived_service}):
        # Limpa cache de módulos que dependem de derived_service
        for mod_name in list(sys.modules.keys()):
            if "derived_payoff_persistence" in mod_name or "canonical_pricing_facade" in mod_name:
                del sys.modules[mod_name]

        from services.canonical_pricing_facade import CanonicalPricingFacade
        from services.derived_payoff_persistence import DerivedPayoffPersistence

        with _tmp_dir() as tmp:
            db_path = _make_db(tmp)
            facade = CanonicalPricingFacade(db_path=db_path)

            port = facade._persister._payoff_port
            _check(
                "facade._persister._payoff_port é DerivedPayoffPersistence",
                isinstance(port, DerivedPayoffPersistence),
            )


def test_patch21_bootstrap_has_pricing_executions_table() -> None:
    print("\n patch_19+21: tabela pricing_executions no bootstrap ")

    from infra.bootstrap_structures_schema import ensure_structures_schema

    with _tmp_dir() as tmp:
        db_path = Path(tmp) / "app.db"
        ensure_structures_schema(db_path)

        with sqlite3.connect(str(db_path)) as conn:
            tables = {
                r[0] for r in conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                ).fetchall()
            }
            indexes = {
                r[0] for r in conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='index'"
                ).fetchall()
            }

        _check("tabela structures existe",         "structures"         in tables)
        _check("tabela structure_legs existe",     "structure_legs"     in tables)
        _check("tabela pricing_executions existe", "pricing_executions" in tables)

        _check(
            "índice idx_pricing_executions_structure_id existe",
            "idx_pricing_executions_structure_id" in indexes,
        )
        _check(
            "índice idx_pricing_executions_created_at existe",
            "idx_pricing_executions_created_at" in indexes,
        )
        _check(
            "índice idx_pricing_executions_status existe",
            "idx_pricing_executions_status" in indexes,
        )


# ===========================================================================
# runner standalone
# ===========================================================================

def _run_all() -> None:
    tests = [
        test_patch19_save_and_read,
        test_patch19_list_and_count,
        test_patch19_get_latest_by_structure,
        test_patch19_no_json_file_created,
        test_patch20_upsert_no_resource_leak,
        test_patch20_missing_timestamp_raises,
        test_patch21_port_called_on_success,
        test_patch21_port_not_called_without_injection,
        test_patch21_port_exception_does_not_raise,
        test_patch21_facade_wiring,
        test_patch21_bootstrap_has_pricing_executions_table,
    ]

    print("=" * 65)
    print("  TESTES patches 19 / 20 / 21")
    print("=" * 65)

    failed: list[str] = []

    for test_fn in tests:
        try:
            test_fn()
        except AssertionError as exc:
            failed.append(str(exc))
        except Exception:
            name = test_fn.__name__
            failed.append(name)
            print(f"\n  [FALHOU]  {name} -- ERRO INESPERADO:")
            traceback.print_exc()

    print("\n" + "=" * 65)
    total  = len(tests)
    passed = total - len(failed)
    print(f"  Resultado: {passed}/{total} testes passaram")

    if failed:
        print("\n  Falhas:")
        for f in failed:
            print(f"    [FALHOU]  {f}")
        sys.exit(1)
    else:
        print("  [OK]  Todos os testes passaram.")

    print("=" * 65)


if __name__ == "__main__":
    _run_all()
