# ATT/tests/test_patch22.py
"""
Testes do patch_22.

  patch_22 — Auditoria e validação do bootstrap completo:
             • pricing_executions no app.db (schema + índices)
             • PricingExecutionPersistenceService wiring correto
             • DerivedPayoffPersistence como implementação do port
             • CanonicalPricingFacade instancia o persister com o port
             • PricingExecutionsRepository compatível com o schema atual
             • Nenhum arquivo .json gerado por execuções de pricing

Execução:
    pytest ATT/tests/test_patch22.py -v
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

_PASS = "✅"
_FAIL = "❌"
_results: list[tuple[str, bool, str]] = []


def _check(name: str, condition: bool, detail: str = "") -> None:
    icon = _PASS if condition else _FAIL
    _results.append((name, condition, detail))
    print(f"  {icon}  {name}" + (f"  →  {detail}" if detail else ""))
    if not condition:
        raise AssertionError(f"FALHOU: {name}  {detail}")


# ---------------------------------------------------------------------------
# Fixture helpers
# ---------------------------------------------------------------------------

def _tmp_dir() -> tempfile.TemporaryDirectory:
    return tempfile.TemporaryDirectory(ignore_cleanup_errors=True)


def _make_db(tmp: str) -> Path:
    from infra.bootstrap_structures_schema import ensure_structures_schema

    db_path = Path(tmp) / "app.db"
    ensure_structures_schema(db_path)

    with sqlite3.connect(str(db_path)) as conn:
        conn.execute("PRAGMA foreign_keys = OFF")
        conn.commit()

    return db_path


def _make_repo(db_path: Path):
    from repositories.pricing_executions_repository import PricingExecutionsRepository

    repo = PricingExecutionsRepository(db_path=db_path)
    _patch_repo_conn(repo)
    return repo


def _patch_repo_conn(repo) -> None:
    def _patched_connect():
        conn = sqlite3.connect(str(repo._db_path))
        conn.execute("PRAGMA foreign_keys = OFF")
        return conn

    repo._connect = _patched_connect


# ===========================================================================
# patch_22 — T1: schema completo no bootstrap
# ===========================================================================

def test_patch22_schema_tables_and_indexes() -> None:
    print("\n── patch_22 / T1: schema — tabelas e índices no bootstrap ──────────")

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

        # tabelas obrigatórias
        for table in ("structures", "structure_legs", "pricing_executions"):
            _check(f"tabela '{table}' existe", table in tables)

        # índices obrigatórios — pricing_executions
        expected_indexes = {
            "idx_pricing_executions_structure_id",
            "idx_pricing_executions_created_at",
            "idx_pricing_executions_status",
        }
        for idx in expected_indexes:
            _check(f"índice '{idx}' existe", idx in indexes)

        # índices obrigatórios — structures / legs
        for idx in (
            "idx_structures_underlying_asset",
            "idx_structures_alias_legacy_aba",
            "idx_structure_legs_structure_id",
            "idx_structure_legs_structure_id_leg_order",
        ):
            _check(f"índice '{idx}' existe", idx in indexes)


# ===========================================================================
# patch_22 — T2: colunas da tabela pricing_executions
# ===========================================================================

def test_patch22_pricing_executions_columns() -> None:
    print("\n── patch_22 / T2: colunas da tabela pricing_executions ─────────────")

    from infra.bootstrap_structures_schema import ensure_structures_schema

    expected_columns = {
        "id", "created_at", "structure_id", "underlying_asset",
        "reference_date", "execution_status", "execution_engine",
        "error_message", "duration_ms", "number_of_legs",
        "total_quantity", "theoretical_value", "pricing_payload", "result",
    }

    with _tmp_dir() as tmp:
        db_path = Path(tmp) / "app.db"
        ensure_structures_schema(db_path)

        with sqlite3.connect(str(db_path)) as conn:
            pragma = conn.execute(
                "PRAGMA table_info(pricing_executions)"
            ).fetchall()
            actual_columns = {row[1] for row in pragma}

    for col in expected_columns:
        _check(f"coluna '{col}' presente", col in actual_columns)

    _check(
        "nenhuma coluna inesperada",
        actual_columns == expected_columns,
        f"diff={actual_columns.symmetric_difference(expected_columns)}",
    )


# ===========================================================================
# patch_22 — T3: PricingExecutionPersistenceService importável e wiring
# ===========================================================================

def test_patch22_persistence_service_importable() -> None:
    print("\n── patch_22 / T3: PricingExecutionPersistenceService importável ────")

    from services.pricing_execution_persistence_service import (
        PricingExecutionPersistenceService,
    )
    from repositories.pricing_executions_repository import PricingExecutionsRepository
    from services.payoff_persistence_port import PayoffPersistencePort

    svc = PricingExecutionPersistenceService()

    _check(
        "PricingExecutionPersistenceService instanciável sem args",
        svc is not None,
    )
    _check(
        "pricing_executions_repository inicializado",
        isinstance(svc.pricing_executions_repository, PricingExecutionsRepository),
    )
    _check(
        "_payoff_port é None quando não injetado",
        svc._payoff_port is None,
    )

    mock_port = MagicMock(spec=PayoffPersistencePort)
    svc_with_port = PricingExecutionPersistenceService(payoff_persistence_port=mock_port)
    _check(
        "_payoff_port preenchido quando injetado",
        svc_with_port._payoff_port is mock_port,
    )


# ===========================================================================
# patch_22 — T4: persist_execution retorna dict com 'record'
# ===========================================================================

def test_patch22_persist_execution_returns_record() -> None:
    print("\n── patch_22 / T4: persist_execution → dict com 'record' ────────────")

    from services.pricing_execution_persistence_service import (
        PricingExecutionPersistenceService,
    )

    with _tmp_dir() as tmp:
        db_path = _make_db(tmp)

        mock_port = MagicMock()
        svc = PricingExecutionPersistenceService(payoff_persistence_port=mock_port)
        svc.pricing_executions_repository = _make_repo(db_path)

        payload = {
            "structure_id":     10,
            "underlying_asset": "PETR4",
            "reference_date":   "2026-05-28",
            "spot_price":       38.0,
        }
        result = {
            "engine":    "stub",
            "status":    "success",
            "metrics":   {"number_of_legs": 2, "total_quantity": 200},
            "valuation": {"theoretical_value": 3.50},
        }

        out = svc.persist_execution(
            pricing_payload=payload,
            result=result,
            duration_ms=15,
        )

        _check("retorno é dict",               isinstance(out, dict))
        _check("chave 'record' presente",      "record" in out)
        _check("record é dict",                isinstance(out["record"], dict))
        _check("record tem id",                isinstance(out["record"].get("id"), int))
        _check("port.persist() chamado 1x",    mock_port.persist.call_count == 1)

        args = mock_port.persist.call_args
        got_payload = args.kwargs.get("pricing_payload") or (args.args[0] if args.args else None)
        got_result  = args.kwargs.get("result")          or (args.args[1] if len(args.args) > 1 else None)

        _check("port recebeu pricing_payload", got_payload is not None and got_payload["structure_id"] == 10)
        _check("port recebeu result correto",  got_result is not None and got_result["status"] == "success")


# ===========================================================================
# patch_22 — T5: port com falha não derruba persist_execution
# ===========================================================================

def test_patch22_port_failure_is_silent() -> None:
    print("\n── patch_22 / T5: falha no port não propaga exceção ────────────────")

    from services.pricing_execution_persistence_service import (
        PricingExecutionPersistenceService,
    )

    with _tmp_dir() as tmp:
        db_path = _make_db(tmp)

        mock_port = MagicMock()
        mock_port.persist.side_effect = RuntimeError("derived.db offline!")

        svc = PricingExecutionPersistenceService(payoff_persistence_port=mock_port)
        svc.pricing_executions_repository = _make_repo(db_path)

        raised = False
        out = None
        try:
            out = svc.persist_execution(
                pricing_payload={"structure_id": 5, "underlying_asset": "VALE3"},
                result={
                    "engine":    "stub",
                    "status":    "success",
                    "metrics":   {},
                    "valuation": {},
                },
            )
        except Exception:
            raised = True

        _check("exceção do port não propaga",                not raised)
        _check("retorno é dict mesmo com port falhando",     isinstance(out, dict))
        _check("record gravado no SQLite mesmo com port err", isinstance(out.get("record"), dict))


# ===========================================================================
# patch_22 — T6: DerivedPayoffPersistence importável
# ===========================================================================

def test_patch22_derived_payoff_persistence_importable() -> None:
    print("\n── patch_22 / T6: DerivedPayoffPersistence importável ──────────────")

    import sys
    from unittest.mock import MagicMock

    # stub para evitar ModuleNotFoundError de 'derived_service'
    fake_derived = MagicMock()
    fake_derived.save_payoff_from_canonical_payload = MagicMock()
    fake_derived.save_decision_from_canonical_payload = MagicMock()

    with patch.dict(sys.modules, {"derived_service": fake_derived}):
        for mod in list(sys.modules):
            if "derived_payoff_persistence" in mod:
                del sys.modules[mod]

        from services.derived_payoff_persistence import DerivedPayoffPersistence

        instance = DerivedPayoffPersistence()

        _check("DerivedPayoffPersistence instanciável",   instance is not None)
        _check("possui método persist()",                 callable(getattr(instance, "persist", None)))
        _check("possui método _persist_payoff()",         callable(getattr(instance, "_persist_payoff", None)))
        _check("possui método _persist_decision()",       callable(getattr(instance, "_persist_decision", None)))
        _check("possui método _build_canonical_input()",  callable(getattr(instance, "_build_canonical_input", None)))


# ===========================================================================
# patch_22 — T7: DerivedPayoffPersistence.persist() skip em status inelegível
# ===========================================================================

def test_patch22_derived_payoff_skip_on_error_status() -> None:
    print("\n── patch_22 / T7: DerivedPayoffPersistence.persist() skip em erro ──")

    import sys
    from unittest.mock import MagicMock

    fake_derived = MagicMock()

    with patch.dict(sys.modules, {"derived_service": fake_derived}):
        for mod in list(sys.modules):
            if "derived_payoff_persistence" in mod:
                del sys.modules[mod]

        from services.derived_payoff_persistence import DerivedPayoffPersistence

        instance = DerivedPayoffPersistence()

        instance.persist(
            pricing_payload={"structure_id": 1},
            result={"status": "error"},
        )

        _check(
            "save_payoff NÃO chamado para status=error",
            fake_derived.save_payoff_from_canonical_payload.call_count == 0,
        )
        _check(
            "save_decision NÃO chamado para status=error",
            fake_derived.save_decision_from_canonical_payload.call_count == 0,
        )

        instance.persist(
            pricing_payload=None,
            result={"status": "success"},
        )

        _check(
            "save_payoff NÃO chamado para pricing_payload=None",
            fake_derived.save_payoff_from_canonical_payload.call_count == 0,
        )


# ===========================================================================
# patch_22 — T8: CanonicalPricingFacade injeta DerivedPayoffPersistence
# ===========================================================================

def test_patch22_facade_injects_derived_payoff_persistence() -> None:
    print("\n── patch_22 / T8: CanonicalPricingFacade injeta DerivedPayoffPersistence ─")

    import sys
    from unittest.mock import MagicMock

    fake_derived = MagicMock()
    fake_derived.save_payoff_from_canonical_payload = MagicMock()
    fake_derived.save_decision_from_canonical_payload = MagicMock()

    with patch.dict(sys.modules, {"derived_service": fake_derived}):
        for mod in list(sys.modules):
            if "derived_payoff_persistence" in mod or "canonical_pricing_facade" in mod:
                del sys.modules[mod]

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
            _check(
                "facade._persister é PricingExecutionPersistenceService",
                type(facade._persister).__name__ == "PricingExecutionPersistenceService",
            )


# ===========================================================================
# patch_22 — T9: idempotência do bootstrap (ensure chamado 2x)
# ===========================================================================

def test_patch22_bootstrap_is_idempotent() -> None:
    print("\n── patch_22 / T9: bootstrap idempotente (IF NOT EXISTS) ────────────")

    from infra.bootstrap_structures_schema import ensure_structures_schema

    with _tmp_dir() as tmp:
        db_path = Path(tmp) / "app.db"

        raised = False
        try:
            ensure_structures_schema(db_path)
            ensure_structures_schema(db_path)   # segunda chamada não deve falhar
        except Exception as exc:
            raised = True
            print(f"    erro: {exc}")

        _check("segunda chamada ao bootstrap não levanta exceção", not raised)

        with sqlite3.connect(str(db_path)) as conn:
            count = conn.execute(
                "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='pricing_executions'"
            ).fetchone()[0]

        _check("tabela pricing_executions existe após 2 chamadas", count == 1)


# ===========================================================================
# patch_22 — T10: nenhum .json gerado em pipeline completo
# ===========================================================================

def test_patch22_no_json_artifact() -> None:
    print("\n── patch_22 / T10: nenhum .json gerado em save_execution ───────────")

    with _tmp_dir() as tmp:
        db_path = _make_db(tmp)
        repo = _make_repo(db_path)

        for i in range(3):
            repo.save_execution(
                pricing_payload={
                    "structure_id":     i + 1,
                    "underlying_asset": "BOVA11",
                    "reference_date":   "2026-05-28",
                    "spot_price":       100.0 + i,
                },
                result={
                    "engine":    "stub",
                    "status":    "success",
                    "metrics":   {"number_of_legs": 1, "total_quantity": 100},
                    "valuation": {"theoretical_value": 1.0 + i * 0.5},
                },
                execution_status="success",
                execution_engine="stub",
                duration_ms=10 + i,
                number_of_legs=1,
                total_quantity=100,
                theoretical_value=1.0 + i * 0.5,
            )

        json_files = list(Path(tmp).rglob("*.json"))
        _check("nenhum arquivo .json gerado",  len(json_files) == 0)
        _check("app.db existe",                db_path.exists())

        with sqlite3.connect(str(db_path)) as conn:
            conn.execute("PRAGMA foreign_keys = OFF")
            count = conn.execute(
                "SELECT COUNT(*) FROM pricing_executions"
            ).fetchone()[0]

        _check("3 registros no SQLite",        count == 3)


# ===========================================================================
# runner standalone
# ===========================================================================

def _run_all() -> None:
    tests = [
        test_patch22_schema_tables_and_indexes,
        test_patch22_pricing_executions_columns,
        test_patch22_persistence_service_importable,
        test_patch22_persist_execution_returns_record,
        test_patch22_port_failure_is_silent,
        test_patch22_derived_payoff_persistence_importable,
        test_patch22_derived_payoff_skip_on_error_status,
        
        test_patch22_facade_injects_derived_payoff_persistence,
        test_patch22_bootstrap_is_idempotent,
        test_patch22_no_json_artifact,
    ]

    passed = failed = 0
    for t in tests:
        try:
            t()
            passed += 1
        except Exception as exc:
            failed += 1
            print(f"  ❌  {t.__name__}: {exc}")

    print(f"\n{'='*55}")
    print(f"  {passed} passed  |  {failed} failed")
    print(f"{'='*55}")


if __name__ == "__main__":
    _run_all()
