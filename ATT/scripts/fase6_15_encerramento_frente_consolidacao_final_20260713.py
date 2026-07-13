from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import sqlite3
import subprocess


DATE_TAG = "20260713"

DB_PATH = Path("dados/app.db")
OUTPUT_DIR = Path("FRENTE_RTD_EXCEL_BTG_ONLINE/output")

MANIFEST13 = OUTPUT_DIR / f"fase6_13_execucao_real_limpeza_controlada_{DATE_TAG}.json"
MANIFEST14 = OUTPUT_DIR / f"fase6_14_validacao_pos_limpeza_performance_{DATE_TAG}.json"
MANIFEST15 = OUTPUT_DIR / f"fase6_15_encerramento_frente_consolidacao_final_{DATE_TAG}.json"
REPORT15 = OUTPUT_DIR / f"fase6_15_encerramento_frente_consolidacao_final_{DATE_TAG}.md"

HISTORY_TABLE = "rtd_option_quotes_intraday_history"
CANDLES_TABLE = "rtd_option_quotes_intraday_candles"

EXPECTED_HISTORY_TOTAL = 0
EXPECTED_CANDLES_TOTAL = 110
EXPECTED_REMOVED_IDS = 60


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def connect_readonly(path: Path) -> sqlite3.Connection:
    uri = f"file:{path.as_posix()}?mode=ro"
    return sqlite3.connect(uri, uri=True)


def git_output(args: list[str]) -> str:
    return subprocess.check_output(args, text=True, encoding="utf-8").strip()


def main() -> None:
    if not DB_PATH.exists():
        raise SystemExit("ERRO: banco dados/app.db nao encontrado.")

    if not MANIFEST13.exists():
        raise SystemExit("ERRO: manifesto da Fase 6.13 nao encontrado.")

    if not MANIFEST14.exists():
        raise SystemExit("ERRO: manifesto da Fase 6.14 nao encontrado.")

    data13 = json.loads(MANIFEST13.read_text(encoding="utf-8"))
    data14 = json.loads(MANIFEST14.read_text(encoding="utf-8"))

    if data13.get("phase") != "6.13":
        raise SystemExit("ERRO: manifesto 6.13 invalido.")

    if data14.get("phase") != "6.14":
        raise SystemExit("ERRO: manifesto 6.14 invalido.")

    decision13 = data13.get("decision", {})
    cleanup13 = data13.get("cleanup_execution", {})
    rollback13 = data13.get("rollback_reference", {})

    decision14 = data14.get("decision", {})
    validation14 = data14.get("post_cleanup_validation", {})
    database14 = data14.get("database", {})
    performance14 = data14.get("performance", {})

    validations = {
        "phase_6_13_real_cleanup_executed": decision13.get("real_cleanup_executed") is True,
        "phase_6_13_records_removed_60": int(decision13.get("records_removed", -1)) == EXPECTED_REMOVED_IDS,
        "phase_6_13_eligible_after_zero": int(cleanup13.get("eligible_count_after", cleanup13.get("eligible_count_after_detected", -1))) == 0,
        "phase_6_13_candles_preserved": decision13.get("candles_preserved") is True,
        "phase_6_13_rollback_available": rollback13.get("rollback_available") is True,
        "phase_6_14_status_approved": decision14.get("phase_6_14_status") == "APROVADA",
        "phase_6_14_post_cleanup_validated": decision14.get("post_cleanup_validated") is True,
        "phase_6_14_performance_validated": decision14.get("performance_validated") is True,
        "phase_6_14_regression_absent": decision14.get("regression_absent") is True,
        "phase_6_14_database_not_modified": database14.get("database_modified") is False,
        "phase_6_14_hash_unchanged": database14.get("sha256_unchanged") is True,
        "phase_6_14_history_zero": int(validation14.get("history_total", -1)) == EXPECTED_HISTORY_TOTAL,
        "phase_6_14_eligible_remaining_zero": int(validation14.get("eligible_ids_remaining", -1)) == 0,
        "phase_6_14_candles_110": int(validation14.get("candles_total", -1)) == EXPECTED_CANDLES_TOTAL,
        "phase_6_14_performance_ok": performance14.get("performance_ok") is True,
    }

    sha_before = sha256_file(DB_PATH)

    with connect_readonly(DB_PATH) as conn:
        integrity = conn.execute("PRAGMA integrity_check").fetchone()[0]
        history_total = conn.execute(f"SELECT COUNT(*) FROM {HISTORY_TABLE}").fetchone()[0]
        candles_total = conn.execute(f"SELECT COUNT(*) FROM {CANDLES_TABLE}").fetchone()[0]

        eligible_ids = cleanup13.get("eligible_ids_removed") or []
        eligible_ids = sorted({int(x) for x in eligible_ids})

        if len(eligible_ids) != EXPECTED_REMOVED_IDS:
            raise SystemExit(f"ERRO: quantidade de IDs removidos inesperada: {len(eligible_ids)}")

        placeholders = ",".join("?" for _ in eligible_ids)
        eligible_remaining = conn.execute(
            f"SELECT COUNT(*) FROM {HISTORY_TABLE} WHERE id IN ({placeholders})",
            tuple(eligible_ids),
        ).fetchone()[0]

    sha_after = sha256_file(DB_PATH)

    validations.update(
        {
            "final_sqlite_integrity_ok": str(integrity).lower() == "ok",
            "final_history_total_zero": int(history_total) == EXPECTED_HISTORY_TOTAL,
            "final_candles_total_110": int(candles_total) == EXPECTED_CANDLES_TOTAL,
            "final_eligible_ids_remaining_zero": int(eligible_remaining) == 0,
            "phase_6_15_database_hash_unchanged": sha_before == sha_after,
        }
    )

    all_valid = all(validations.values())

    branch = git_output(["git", "branch", "--show-current"])
    head_commit = git_output(["git", "rev-parse", "--short", "HEAD"])
    recent_log = git_output(["git", "log", "--oneline", "--decorate", "-8"])

    now = datetime.now(timezone.utc).replace(microsecond=0)

    manifest = {
        "phase": "6.15",
        "generated_at_utc": now.isoformat(),
        "nature": "encerramento_frente_consolidacao_final",
        "database": {
            "path": DB_PATH.as_posix(),
            "open_mode": "read_only",
            "sha256_before": sha_before,
            "sha256_after": sha_after,
            "sha256_unchanged": sha_before == sha_after,
            "sqlite_integrity": integrity,
            "database_modified": False,
            "history_total": int(history_total),
            "eligible_ids_remaining": int(eligible_remaining),
            "candles_total": int(candles_total),
        },
        "phase_6_13_summary": {
            "manifest": MANIFEST13.as_posix(),
            "real_cleanup_executed": decision13.get("real_cleanup_executed"),
            "regularization_only": decision13.get("regularization_only"),
            "records_removed": decision13.get("records_removed"),
            "eligible_count_after": cleanup13.get("eligible_count_after", cleanup13.get("eligible_count_after_detected")),
            "rollback_available": rollback13.get("rollback_available"),
            "candles_preserved": decision13.get("candles_preserved"),
            "status": decision13.get("phase_6_13_status"),
        },
        "phase_6_14_summary": {
            "manifest": MANIFEST14.as_posix(),
            "status": decision14.get("phase_6_14_status"),
            "post_cleanup_validated": decision14.get("post_cleanup_validated"),
            "performance_validated": decision14.get("performance_validated"),
            "regression_absent": decision14.get("regression_absent"),
            "database_modified": database14.get("database_modified"),
            "max_elapsed_ms": performance14.get("max_elapsed_ms"),
        },
        "git": {
            "branch": branch,
            "head_commit_before_phase_6_15_commit": head_commit,
            "recent_log": recent_log.splitlines(),
        },
        "consolidated_validations": validations,
        "decision": {
            "phase_6_15_status": "APROVADA" if all_valid else "REPROVADA",
            "front_status": "ENCERRADA_TECNICAMENTE" if all_valid else "PENDENTE_CORRECAO",
            "cleanup_front_completed": all_valid,
            "post_cleanup_validated": validations["phase_6_14_post_cleanup_validated"],
            "performance_validated": validations["phase_6_14_performance_validated"],
            "regression_absent": validations["phase_6_14_regression_absent"],
            "rollback_documented": validations["phase_6_13_rollback_available"],
            "database_modified": False,
            "ready_for_review_or_merge": all_valid,
            "next_recommended_action": "Revisao final e merge da branch de feature",
        },
    }

    MANIFEST15.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    validations_md = "\n".join(
        f"- {name}: {'ok' if value else 'falha'}"
        for name, value in validations.items()
    )

    recent_log_md = "\n".join(f"- `{line}`" for line in recent_log.splitlines())

    report = f"""# Fase 6.15 - Encerramento da frente e consolidacao final

Marcador inicio: INICIO_FASE6_15_ENCERRAMENTO_FRENTE_CONSOLIDACAO_FINAL_{DATE_TAG}

Data de geracao: {now.isoformat()}

## Natureza

Encerramento tecnico da frente RTD Excel BTG Online - retencao e limpeza.

Esta fase consolida as evidencias das Fases 6.13 e 6.14 e nao modifica o banco.

## Banco

- Caminho: `{DB_PATH.as_posix()}`
- Modo de abertura: read-only
- SHA256 antes: `{sha_before}`
- SHA256 depois: `{sha_after}`
- Hash inalterado: {'sim' if sha_before == sha_after else 'nao'}
- Banco modificado nesta fase: nao
- SQLite integrity_check: `{integrity}`
- Total historico final: {history_total}
- IDs elegiveis remanescentes: {eligible_remaining}
- Total candles final: {candles_total}

## Consolidacao Fase 6.13

- Manifesto: `{MANIFEST13.as_posix()}`
- Limpeza real executada: {decision13.get("real_cleanup_executed")}
- Regularizacao apenas documental/tecnica: {decision13.get("regularization_only")}
- Registros removidos: {decision13.get("records_removed")}
- IDs elegiveis apos limpeza: {cleanup13.get("eligible_count_after", cleanup13.get("eligible_count_after_detected"))}
- Rollback disponivel: {rollback13.get("rollback_available")}
- Candles preservados: {decision13.get("candles_preserved")}
- Status: `{decision13.get("phase_6_13_status")}`

## Consolidacao Fase 6.14

- Manifesto: `{MANIFEST14.as_posix()}`
- Status: `{decision14.get("phase_6_14_status")}`
- Pos-limpeza validado: {decision14.get("post_cleanup_validated")}
- Performance validada: {decision14.get("performance_validated")}
- Ausencia de regressao: {decision14.get("regression_absent")}
- Banco modificado na Fase 6.14: {database14.get("database_modified")}
- Maior tempo medido na Fase 6.14: {performance14.get("max_elapsed_ms")}

## Validacoes consolidadas

{validations_md}

## Git

- Branch: `{branch}`
- HEAD antes do commit da Fase 6.15: `{head_commit}`

### Historico recente

{recent_log_md}

## Resultado

- Status: {'FASE6_15_ENCERRAMENTO_FRENTE_CONSOLIDACAO_FINAL_APROVADA' if all_valid else 'FASE6_15_ENCERRAMENTO_FRENTE_CONSOLIDACAO_FINAL_REPROVADA'}
- Frente encerrada tecnicamente: {'sim' if all_valid else 'nao'}
- Limpeza real consolidada: {'sim' if validations["phase_6_13_real_cleanup_executed"] else 'nao'}
- Pos-limpeza validado: {'sim' if validations["phase_6_14_post_cleanup_validated"] else 'nao'}
- Performance validada: {'sim' if validations["phase_6_14_performance_validated"] else 'nao'}
- Ausencia de regressao: {'sim' if validations["phase_6_14_regression_absent"] else 'nao'}
- Rollback documentado: {'sim' if validations["phase_6_13_rollback_available"] else 'nao'}
- Banco modificado nesta fase: nao
- Integridade final: {'ok' if str(integrity).lower() == 'ok' else 'falha'}
- Historico final limpo: {'sim' if int(history_total) == 0 else 'nao'}
- Candles finais preservados: {'sim' if int(candles_total) == 110 else 'nao'}
- Pronto para revisao ou merge: {'sim' if all_valid else 'nao'}
- Fase 6.15 encerrada tecnicamente: {'sim' if all_valid else 'nao'}

## Decisao

A frente de retencao e limpeza da Fase 6 fica encerrada tecnicamente.

Acao recomendada: revisao final e merge da branch de feature.

Marcador fim: FIM_FASE6_15_ENCERRAMENTO_FRENTE_CONSOLIDACAO_FINAL_{DATE_TAG}
"""

    REPORT15.write_text(report, encoding="utf-8")

    print("Manifesto:", MANIFEST15.as_posix())
    print("Relatorio:", REPORT15.as_posix())
    print("integrity:", integrity)
    print("history_total:", history_total)
    print("eligible_ids_remaining:", eligible_remaining)
    print("candles_total:", candles_total)
    print("sha_unchanged:", sha_before == sha_after)
    print("all_valid:", all_valid)

    if not all_valid:
        raise SystemExit("ERRO: encerramento consolidado da Fase 6.15 nao aprovado.")


if __name__ == "__main__":
    main()
