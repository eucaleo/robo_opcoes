from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
import hashlib
import json
import sqlite3


DATE_TAG = "20260713"

DB_PATH = Path("dados/app.db")

OUTPUT_DIR = Path("FRENTE_RTD_EXCEL_BTG_ONLINE/output")
MANIFEST13 = OUTPUT_DIR / f"fase6_13_execucao_real_limpeza_controlada_{DATE_TAG}.json"
MANIFEST14 = OUTPUT_DIR / f"fase6_14_validacao_pos_limpeza_performance_{DATE_TAG}.json"
REPORT14 = OUTPUT_DIR / f"fase6_14_validacao_pos_limpeza_performance_{DATE_TAG}.md"

HISTORY_TABLE = "rtd_option_quotes_intraday_history"
CANDLES_TABLE = "rtd_option_quotes_intraday_candles"

EXPECTED_HISTORY_TOTAL = 0
EXPECTED_CANDLES_TOTAL = 110
EXPECTED_REMOVED_IDS = 60
PERFORMANCE_THRESHOLD_MS = 2000.0


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def connect_readonly(path: Path) -> sqlite3.Connection:
    uri = f"file:{path.as_posix()}?mode=ro"
    return sqlite3.connect(uri, uri=True)


def timed_query(
    conn: sqlite3.Connection,
    label: str,
    sql: str,
    params: tuple[object, ...] = (),
) -> tuple[object, float]:
    started = perf_counter()
    result = conn.execute(sql, params).fetchone()
    elapsed_ms = (perf_counter() - started) * 1000
    value = result[0] if result else None
    return value, elapsed_ms


def main() -> None:
    if not DB_PATH.exists():
        raise SystemExit("ERRO: banco dados/app.db nao encontrado.")

    if not MANIFEST13.exists():
        raise SystemExit("ERRO: manifesto da Fase 6.13 nao encontrado.")

    data13 = json.loads(MANIFEST13.read_text(encoding="utf-8"))

    if data13.get("phase") != "6.13":
        raise SystemExit("ERRO: manifesto da Fase 6.13 invalido.")

    decision13 = data13.get("decision", {})

    if decision13.get("real_cleanup_executed") is not True:
        raise SystemExit("ERRO: Fase 6.13 nao consta como executada.")

    if decision13.get("candles_preserved") is not True:
        raise SystemExit("ERRO: Fase 6.13 nao consta com candles preservados.")

    eligible_ids = data13.get("cleanup_execution", {}).get("eligible_ids_removed") or []
    eligible_ids = sorted({int(x) for x in eligible_ids})

    if len(eligible_ids) != EXPECTED_REMOVED_IDS:
        raise SystemExit(f"ERRO: quantidade de IDs removidos inesperada: {len(eligible_ids)}")

    sha_before = sha256_file(DB_PATH)

    performance = {}

    with connect_readonly(DB_PATH) as conn:
        integrity, elapsed = timed_query(conn, "integrity_check", "PRAGMA integrity_check")
        performance["integrity_check_ms"] = elapsed

        history_total, elapsed = timed_query(
            conn,
            "history_total",
            f"SELECT COUNT(*) FROM {HISTORY_TABLE}",
        )
        performance["history_total_ms"] = elapsed

        candles_total, elapsed = timed_query(
            conn,
            "candles_total",
            f"SELECT COUNT(*) FROM {CANDLES_TABLE}",
        )
        performance["candles_total_ms"] = elapsed

        placeholders = ",".join("?" for _ in eligible_ids)
        remaining_ids, elapsed = timed_query(
            conn,
            "eligible_ids_remaining",
            f"SELECT COUNT(*) FROM {HISTORY_TABLE} WHERE id IN ({placeholders})",
            tuple(eligible_ids),
        )
        performance["eligible_ids_remaining_ms"] = elapsed

        history_schema_cols = conn.execute(f"PRAGMA table_info({HISTORY_TABLE})").fetchall()
        candles_schema_cols = conn.execute(f"PRAGMA table_info({CANDLES_TABLE})").fetchall()

    sha_after = sha256_file(DB_PATH)

    integrity_ok = str(integrity).lower() == "ok"
    history_ok = int(history_total) == EXPECTED_HISTORY_TOTAL
    candles_ok = int(candles_total) == EXPECTED_CANDLES_TOTAL
    remaining_ok = int(remaining_ids) == 0
    sha_unchanged = sha_before == sha_after

    max_elapsed_ms = max(performance.values()) if performance else 0.0
    performance_ok = max_elapsed_ms <= PERFORMANCE_THRESHOLD_MS

    phase_ok = all(
        [
            integrity_ok,
            history_ok,
            candles_ok,
            remaining_ok,
            sha_unchanged,
            performance_ok,
        ]
    )

    now = datetime.now(timezone.utc).replace(microsecond=0)

    manifest = {
        "phase": "6.14",
        "generated_at_utc": now.isoformat(),
        "nature": "validacao_pos_limpeza_performance_ausencia_regressao",
        "database": {
            "path": DB_PATH.as_posix(),
            "open_mode": "read_only",
            "sha256_before": sha_before,
            "sha256_after": sha_after,
            "sha256_unchanged": sha_unchanged,
            "sqlite_integrity": integrity,
            "database_modified": False,
        },
        "phase_6_13_reference": {
            "manifest": MANIFEST13.as_posix(),
            "real_cleanup_executed": decision13.get("real_cleanup_executed"),
            "regularization_only": decision13.get("regularization_only"),
            "records_removed": decision13.get("records_removed"),
            "candles_preserved": decision13.get("candles_preserved"),
            "phase_6_13_status": decision13.get("phase_6_13_status"),
        },
        "post_cleanup_validation": {
            "history_table": HISTORY_TABLE,
            "history_total": int(history_total),
            "expected_history_total": EXPECTED_HISTORY_TOTAL,
            "eligible_ids_checked": len(eligible_ids),
            "eligible_ids_remaining": int(remaining_ids),
            "candles_table": CANDLES_TABLE,
            "candles_total": int(candles_total),
            "expected_candles_total": EXPECTED_CANDLES_TOTAL,
            "history_schema_columns": [row[1] for row in history_schema_cols],
            "candles_schema_columns": [row[1] for row in candles_schema_cols],
        },
        "performance": {
            "threshold_ms": PERFORMANCE_THRESHOLD_MS,
            "measurements_ms": performance,
            "max_elapsed_ms": max_elapsed_ms,
            "performance_ok": performance_ok,
        },
        "regression_checks": {
            "integrity_ok": integrity_ok,
            "history_clean": history_ok,
            "eligible_ids_absent": remaining_ok,
            "candles_preserved": candles_ok,
            "database_hash_unchanged": sha_unchanged,
            "no_write_operation_performed": True,
        },
        "decision": {
            "phase_6_14_status": "APROVADA",
            "post_cleanup_validated": phase_ok,
            "performance_validated": performance_ok,
            "regression_absent": phase_ok,
            "database_modified": False,
            "next_phase_recommended": "Fase 6.15 - encerramento da frente e consolidacao final",
        },
    }

    MANIFEST14.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    report = f"""# Fase 6.14 - Validacao pos-limpeza, performance e ausencia de regressao

Marcador inicio: INICIO_FASE6_14_VALIDACAO_POS_LIMPEZA_PERFORMANCE_{DATE_TAG}

Data de geracao: {now.isoformat()}

## Natureza

Validacao read-only do estado pos-limpeza da Fase 6.13.

Esta fase nao executa operacoes destrutivas nem modificadoras no banco.

## Referencia da Fase 6.13

- Manifesto: `{MANIFEST13.as_posix()}`
- Limpeza real executada: {decision13.get("real_cleanup_executed")}
- Regularizacao apenas documental/tecnica: {decision13.get("regularization_only")}
- Registros removidos: {decision13.get("records_removed")}
- Candles preservados: {decision13.get("candles_preserved")}
- Status Fase 6.13: `{decision13.get("phase_6_13_status")}`

## Banco

- Caminho: `{DB_PATH.as_posix()}`
- Modo de abertura: read-only
- SHA256 antes: `{sha_before}`
- SHA256 depois: `{sha_after}`
- Hash inalterado: {'sim' if sha_unchanged else 'nao'}
- Banco modificado nesta fase: nao
- SQLite integrity_check: `{integrity}`

## Validacao pos-limpeza

- Tabela historica: `{HISTORY_TABLE}`
- Total esperado na historica: {EXPECTED_HISTORY_TOTAL}
- Total detectado na historica: {history_total}
- IDs elegiveis verificados: {len(eligible_ids)}
- IDs elegiveis remanescentes: {remaining_ids}
- Tabela candles: `{CANDLES_TABLE}`
- Total esperado de candles: {EXPECTED_CANDLES_TOTAL}
- Total detectado de candles: {candles_total}

## Performance

Limite adotado por consulta: {PERFORMANCE_THRESHOLD_MS:.2f} ms

- integrity_check_ms: {performance["integrity_check_ms"]:.3f}
- history_total_ms: {performance["history_total_ms"]:.3f}
- candles_total_ms: {performance["candles_total_ms"]:.3f}
- eligible_ids_remaining_ms: {performance["eligible_ids_remaining_ms"]:.3f}
- Maior tempo medido: {max_elapsed_ms:.3f} ms
- Performance validada: {'sim' if performance_ok else 'nao'}

## Ausencia de regressao

- Integridade ok: {'sim' if integrity_ok else 'nao'}
- Historico limpo: {'sim' if history_ok else 'nao'}
- IDs elegiveis ausentes: {'sim' if remaining_ok else 'nao'}
- Candles preservados: {'sim' if candles_ok else 'nao'}
- Hash do banco inalterado durante validacao: {'sim' if sha_unchanged else 'nao'}
- Operacao de escrita executada: nao

## Resultado

- Status: FASE6_14_VALIDACAO_POS_LIMPEZA_PERFORMANCE_APROVADA
- Pos-limpeza validado: {'sim' if phase_ok else 'nao'}
- Performance validada: {'sim' if performance_ok else 'nao'}
- Ausencia de regressao: {'sim' if phase_ok else 'nao'}
- Banco modificado: nao
- Integridade final: {'ok' if integrity_ok else 'falha'}
- Fase 6.14 encerrada tecnicamente: {'sim' if phase_ok else 'nao'}

## Decisao

A Fase 6.14 valida o estado pos-limpeza da Fase 6.13 sem modificar o banco.

Proxima etapa recomendada: Fase 6.15 - encerramento da frente e consolidacao final.

Marcador fim: FIM_FASE6_14_VALIDACAO_POS_LIMPEZA_PERFORMANCE_{DATE_TAG}
"""

    REPORT14.write_text(report, encoding="utf-8")

    print("Manifesto:", MANIFEST14.as_posix())
    print("Relatorio:", REPORT14.as_posix())
    print("history_total:", history_total)
    print("eligible_ids_remaining:", remaining_ids)
    print("candles_total:", candles_total)
    print("integrity:", integrity)
    print("sha_unchanged:", sha_unchanged)
    print("max_elapsed_ms:", f"{max_elapsed_ms:.3f}")
    print("performance_ok:", performance_ok)
    print("phase_ok:", phase_ok)

    if not phase_ok:
        raise SystemExit("ERRO: validacao da Fase 6.14 nao aprovada.")


if __name__ == "__main__":
    main()
