from __future__ import annotations

import hashlib
import json
import os
import shutil
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DB_PATH = Path("dados/app.db")

PHASE_6_12_MANIFEST = Path(
    "FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_12_prepara_execucao_real_rollback_20260713.json"
)

REPORT_PATH = Path(
    "FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_13_execucao_real_limpeza_controlada_20260713.md"
)
MANIFEST_PATH = Path(
    "FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_13_execucao_real_limpeza_controlada_20260713.json"
)

LOCAL_SAFETY_BACKUP_DIR = Path(
    "backups_local/fase6_13_pre_delete_safety_20260713"
)
LOCAL_SAFETY_BACKUP_PATH = LOCAL_SAFETY_BACKUP_DIR / "app_fase6_13_pre_delete_safety_20260713.db"

CONFIRM_ENV = "CONFIRM_REAL_CLEANUP_FASE6_13"
CONFIRM_VALUE = "SIM"

TARGET_TABLE = "rtd_option_quotes_intraday_history"
TARGET_ID_COLUMN = "id"
CANDLES_TABLE = "rtd_option_quotes_intraday_candles"
EXPECTED_ELIGIBLE_COUNT = 60
EXPECTED_BLOCKED_COUNT = 0


def sha256_file(path: Path) -> str:
    hasher = hashlib.sha256()

    with path.open("rb") as file_obj:
        for chunk in iter(lambda: file_obj.read(1024 * 1024), b""):
            hasher.update(chunk)

    return hasher.hexdigest()


def connect_read_only(path: Path) -> sqlite3.Connection:
    absolute_path = path.resolve().as_posix()
    uri = f"file:{absolute_path}?mode=ro"
    return sqlite3.connect(uri, uri=True)


def connect_write(path: Path) -> sqlite3.Connection:
    return sqlite3.connect(path.as_posix())


def sqlite_integrity_check_read_only(path: Path) -> str:
    with connect_read_only(path) as conn:
        row = conn.execute("PRAGMA integrity_check").fetchone()

    if not row:
        return "sem_resultado"

    return str(row[0])


def sqlite_integrity_check_write_conn(conn: sqlite3.Connection) -> str:
    row = conn.execute("PRAGMA integrity_check").fetchone()

    if not row:
        return "sem_resultado"

    return str(row[0])


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Arquivo obrigatorio nao encontrado: {path}")

    return json.loads(path.read_text(encoding="utf-8"))


def table_exists(conn: sqlite3.Connection, table_name: str) -> bool:
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type = ? AND name = ?",
        ("table", table_name),
    ).fetchone()

    return row is not None


def table_columns(conn: sqlite3.Connection, table_name: str) -> list[str]:
    rows = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    return [str(row[1]) for row in rows]


def count_table(conn: sqlite3.Connection, table_name: str) -> int:
    row = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()

    if not row:
        return 0

    return int(row[0])


def count_ids_present(conn: sqlite3.Connection, ids: list[int]) -> int:
    if not ids:
        return 0

    placeholders = ",".join("?" for _ in ids)
    row = conn.execute(
        f"SELECT COUNT(*) FROM {TARGET_TABLE} WHERE {TARGET_ID_COLUMN} IN ({placeholders})",
        ids,
    ).fetchone()

    if not row:
        return 0

    return int(row[0])


def min_max_ids_present(conn: sqlite3.Connection, ids: list[int]) -> tuple[int | None, int | None]:
    if not ids:
        return None, None

    placeholders = ",".join("?" for _ in ids)
    row = conn.execute(
        f"""
        SELECT MIN({TARGET_ID_COLUMN}), MAX({TARGET_ID_COLUMN})
        FROM {TARGET_TABLE}
        WHERE {TARGET_ID_COLUMN} IN ({placeholders})
        """,
        ids,
    ).fetchone()

    if not row:
        return None, None

    return row[0], row[1]


def normalize_ids(values: Any) -> list[int]:
    if not isinstance(values, list):
        raise RuntimeError("Lista de IDs elegiveis ausente ou invalida.")

    result: list[int] = []

    for value in values:
        if isinstance(value, int):
            result.append(value)
        elif isinstance(value, str) and value.strip().isdigit():
            result.append(int(value.strip()))
        else:
            raise RuntimeError(f"ID elegivel invalido: {value!r}")

    return sorted(set(result))


def require_confirmation() -> None:
    value = os.environ.get(CONFIRM_ENV, "")

    if value != CONFIRM_VALUE:
        raise RuntimeError(
            f"Confirmacao explicita ausente. Defina {CONFIRM_ENV}={CONFIRM_VALUE} "
            "para executar a limpeza real controlada."
        )


def validate_phase_6_12_manifest(manifest: dict[str, Any]) -> list[int]:
    if manifest.get("phase") != "6.12":
        raise RuntimeError("Manifesto de entrada nao corresponde a Fase 6.12.")

    decision = manifest["decision"]
    database = manifest["database"]
    backup = manifest["backup_reference"]
    cleanup = manifest["cleanup_candidate"]

    if decision["preflight_ready"] is not True:
        raise RuntimeError("Fase 6.12 nao marcou pre-flight como pronto.")

    if decision["real_cleanup_executed"] is not False:
        raise RuntimeError("Fase 6.12 nao deveria ter executado limpeza real.")

    if decision["real_cleanup_approved"] is not False:
        raise RuntimeError("Fase 6.12 nao deveria ter aprovado limpeza real.")

    if decision["records_removed"] != 0:
        raise RuntimeError("Fase 6.12 deveria ter removido 0 registros.")

    if decision["database_modified"] is not False:
        raise RuntimeError("Fase 6.12 deveria manter banco inalterado.")

    if decision["next_phase_requires_explicit_confirmation"] is not True:
        raise RuntimeError("Fase 6.12 deveria exigir confirmacao explicita para proxima fase.")

    if database["path"] != DB_PATH.as_posix():
        raise RuntimeError("Banco informado na Fase 6.12 diverge do banco canonico.")

    if backup["validated"] is not True:
        raise RuntimeError("Backup da Fase 6.12 nao esta validado.")

    if backup["versioned_in_git"] is not False:
        raise RuntimeError("Backup fisico nao deve estar versionado no Git.")

    if cleanup["target_table"] != TARGET_TABLE:
        raise RuntimeError("Tabela alvo da Fase 6.12 diverge da tabela esperada.")

    if cleanup["target_id_column"] != TARGET_ID_COLUMN:
        raise RuntimeError("Coluna alvo da Fase 6.12 diverge da coluna esperada.")

    if int(cleanup["eligible_count"]) != EXPECTED_ELIGIBLE_COUNT:
        raise RuntimeError("Quantidade elegivel da Fase 6.12 diverge do esperado.")

    if int(cleanup["blocked_count"]) != EXPECTED_BLOCKED_COUNT:
        raise RuntimeError("Quantidade bloqueada da Fase 6.12 diverge do esperado.")

    eligible_ids = normalize_ids(cleanup["eligible_ids"])

    if len(eligible_ids) != EXPECTED_ELIGIBLE_COUNT:
        raise RuntimeError("Lista de IDs elegiveis da Fase 6.12 nao tem 60 IDs.")

    return eligible_ids


def create_local_safety_backup(expected_sha: str) -> dict[str, Any]:
    LOCAL_SAFETY_BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    if LOCAL_SAFETY_BACKUP_PATH.exists():
        LOCAL_SAFETY_BACKUP_PATH.unlink()

    shutil.copy2(DB_PATH, LOCAL_SAFETY_BACKUP_PATH)

    backup_sha = sha256_file(LOCAL_SAFETY_BACKUP_PATH)
    backup_integrity = sqlite_integrity_check_read_only(LOCAL_SAFETY_BACKUP_PATH)

    if backup_sha != expected_sha:
        raise RuntimeError(
            "Backup local de seguranca da Fase 6.13 diverge do banco antes da limpeza."
        )

    if backup_integrity.lower() != "ok":
        raise RuntimeError(
            f"Backup local de seguranca da Fase 6.13 com integridade invalida: {backup_integrity}"
        )

    return {
        "path": LOCAL_SAFETY_BACKUP_PATH.as_posix(),
        "sha256": backup_sha,
        "sqlite_integrity_check": backup_integrity,
        "versioned_in_git": False,
    }


def validate_pre_delete_state(manifest_6_12: dict[str, Any], eligible_ids: list[int]) -> dict[str, Any]:
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Banco nao encontrado: {DB_PATH}")

    expected_db_sha = manifest_6_12["database"]["sha256_current"]
    expected_backup_path = Path(manifest_6_12["backup_reference"]["path"])
    expected_backup_sha = manifest_6_12["backup_reference"]["sha256_current"]

    current_db_sha = sha256_file(DB_PATH)
    current_db_integrity = sqlite_integrity_check_read_only(DB_PATH)

    if current_db_sha != expected_db_sha:
        raise RuntimeError(
            "SHA256 atual do banco diverge do pre-flight da Fase 6.12. "
            f"Atual={current_db_sha}; esperado={expected_db_sha}"
        )

    if current_db_integrity.lower() != "ok":
        raise RuntimeError(f"Integridade do banco antes da limpeza invalida: {current_db_integrity}")

    if not expected_backup_path.exists():
        raise FileNotFoundError(f"Backup fisico da Fase 6.11 nao encontrado: {expected_backup_path}")

    current_backup_sha = sha256_file(expected_backup_path)
    current_backup_integrity = sqlite_integrity_check_read_only(expected_backup_path)

    if current_backup_sha != expected_backup_sha:
        raise RuntimeError(
            "SHA256 atual do backup fisico diverge do manifesto da Fase 6.12."
        )

    if current_backup_sha != current_db_sha:
        raise RuntimeError("Backup fisico validado nao confere com banco atual antes da limpeza.")

    if current_backup_integrity.lower() != "ok":
        raise RuntimeError(f"Integridade do backup fisico invalida: {current_backup_integrity}")

    with connect_read_only(DB_PATH) as conn:
        if not table_exists(conn, TARGET_TABLE):
            raise RuntimeError(f"Tabela alvo nao existe: {TARGET_TABLE}")

        columns = table_columns(conn, TARGET_TABLE)

        if TARGET_ID_COLUMN not in columns:
            raise RuntimeError(f"Coluna alvo nao existe: {TARGET_TABLE}.{TARGET_ID_COLUMN}")

        total_before = count_table(conn, TARGET_TABLE)
        eligible_present = count_ids_present(conn, eligible_ids)
        min_id, max_id = min_max_ids_present(conn, eligible_ids)

        candles_exists = table_exists(conn, CANDLES_TABLE)
        candles_before = count_table(conn, CANDLES_TABLE) if candles_exists else 0

    if eligible_present != EXPECTED_ELIGIBLE_COUNT:
        raise RuntimeError(
            "Quantidade de IDs elegiveis presentes antes da limpeza diverge do esperado. "
            f"Presentes={eligible_present}; esperado={EXPECTED_ELIGIBLE_COUNT}"
        )

    return {
        "db_sha_before": current_db_sha,
        "db_integrity_before": current_db_integrity,
        "rollback_backup_path": expected_backup_path.as_posix(),
        "rollback_backup_sha": current_backup_sha,
        "rollback_backup_integrity": current_backup_integrity,
        "total_before": total_before,
        "eligible_present_before": eligible_present,
        "min_eligible_id": min_id,
        "max_eligible_id": max_id,
        "candles_exists": candles_exists,
        "candles_before": candles_before,
    }


def execute_controlled_delete(eligible_ids: list[int], pre: dict[str, Any]) -> dict[str, Any]:
    placeholders = ",".join("?" for _ in eligible_ids)

    conn = connect_write(DB_PATH)

    try:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("BEGIN IMMEDIATE")

        integrity_in_transaction = sqlite_integrity_check_write_conn(conn)

        if integrity_in_transaction.lower() != "ok":
            raise RuntimeError(
                f"Integridade invalida dentro da transacao: {integrity_in_transaction}"
            )

        total_before_tx = count_table(conn, TARGET_TABLE)
        present_before_tx = count_ids_present(conn, eligible_ids)
        candles_before_tx = count_table(conn, CANDLES_TABLE) if table_exists(conn, CANDLES_TABLE) else 0

        if total_before_tx != pre["total_before"]:
            raise RuntimeError("Total da tabela mudou entre pre-flight e transacao.")

        if present_before_tx != EXPECTED_ELIGIBLE_COUNT:
            raise RuntimeError("IDs elegiveis mudaram entre pre-flight e transacao.")

        if candles_before_tx != pre["candles_before"]:
            raise RuntimeError("Tabela de candles mudou entre pre-flight e transacao.")

        cursor = conn.execute(
            f"DELETE FROM {TARGET_TABLE} WHERE {TARGET_ID_COLUMN} IN ({placeholders})",
            eligible_ids,
        )

        removed = int(cursor.rowcount)

        if removed != EXPECTED_ELIGIBLE_COUNT:
            raise RuntimeError(
                f"Quantidade removida inesperada. Removidos={removed}; esperado={EXPECTED_ELIGIBLE_COUNT}"
            )

        present_after_tx = count_ids_present(conn, eligible_ids)
        total_after_tx = count_table(conn, TARGET_TABLE)
        candles_after_tx = count_table(conn, CANDLES_TABLE) if table_exists(conn, CANDLES_TABLE) else 0

        if present_after_tx != 0:
            raise RuntimeError("Ainda existem IDs elegiveis apos DELETE dentro da transacao.")

        if total_after_tx != total_before_tx - EXPECTED_ELIGIBLE_COUNT:
            raise RuntimeError("Total apos DELETE nao corresponde ao esperado.")

        if candles_after_tx != candles_before_tx:
            raise RuntimeError("Tabela de candles foi alterada indevidamente.")

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

    db_sha_after = sha256_file(DB_PATH)
    db_integrity_after = sqlite_integrity_check_read_only(DB_PATH)

    if db_sha_after == pre["db_sha_before"]:
        raise RuntimeError("SHA256 do banco nao mudou apos limpeza real.")

    if db_integrity_after.lower() != "ok":
        raise RuntimeError(f"Integridade do banco apos limpeza invalida: {db_integrity_after}")

    with connect_read_only(DB_PATH) as conn:
        total_after = count_table(conn, TARGET_TABLE)
        eligible_present_after = count_ids_present(conn, eligible_ids)
        candles_after = count_table(conn, CANDLES_TABLE) if table_exists(conn, CANDLES_TABLE) else 0

    if total_after != pre["total_before"] - EXPECTED_ELIGIBLE_COUNT:
        raise RuntimeError("Total final da tabela historica diverge do esperado.")

    if eligible_present_after != 0:
        raise RuntimeError("IDs elegiveis ainda presentes apos limpeza real.")

    if candles_after != pre["candles_before"]:
        raise RuntimeError("Candles foram alterados apos limpeza real.")

    return {
        "removed": EXPECTED_ELIGIBLE_COUNT,
        "db_sha_after": db_sha_after,
        "db_integrity_after": db_integrity_after,
        "total_after": total_after,
        "eligible_present_after": eligible_present_after,
        "candles_after": candles_after,
    }


def build_manifest(
    manifest_6_12: dict[str, Any],
    eligible_ids: list[int],
    safety_backup: dict[str, Any],
    pre: dict[str, Any],
    post: dict[str, Any],
    now: datetime,
) -> dict[str, Any]:
    return {
        "phase": "6.13",
        "generated_at_utc": now.replace(microsecond=0).isoformat(),
        "nature": "execucao_real_limpeza_controlada",
        "confirmation": {
            "environment_variable": CONFIRM_ENV,
            "expected_value": CONFIRM_VALUE,
            "confirmed": True,
        },
        "source_preflight": {
            "phase": "6.12",
            "manifest": PHASE_6_12_MANIFEST.as_posix(),
            "preflight_ready": manifest_6_12["decision"]["preflight_ready"],
        },
        "database": {
            "path": DB_PATH.as_posix(),
            "sha256_before": pre["db_sha_before"],
            "sha256_after": post["db_sha_after"],
            "sqlite_integrity_before": pre["db_integrity_before"],
            "sqlite_integrity_after": post["db_integrity_after"],
            "database_modified": True,
        },
        "rollback_reference": {
            "primary_backup_phase": "6.11",
            "primary_backup_path": pre["rollback_backup_path"],
            "primary_backup_sha256": pre["rollback_backup_sha"],
            "primary_backup_integrity": pre["rollback_backup_integrity"],
            "local_safety_backup": safety_backup,
            "rollback_available": True,
        },
        "cleanup_execution": {
            "target_table": TARGET_TABLE,
            "target_id_column": TARGET_ID_COLUMN,
            "eligible_count_before": pre["eligible_present_before"],
            "blocked_count": EXPECTED_BLOCKED_COUNT,
            "records_removed": post["removed"],
            "eligible_count_after": post["eligible_present_after"],
            "table_total_before": pre["total_before"],
            "table_total_after": post["total_after"],
            "expected_table_total_after": pre["total_before"] - EXPECTED_ELIGIBLE_COUNT,
            "min_eligible_id": pre["min_eligible_id"],
            "max_eligible_id": pre["max_eligible_id"],
            "eligible_ids_removed": eligible_ids,
        },
        "candles_preservation": {
            "table": CANDLES_TABLE,
            "table_exists": pre["candles_exists"],
            "rows_before": pre["candles_before"],
            "rows_after": post["candles_after"],
            "modified": False,
        },
        "decision": {
            "real_cleanup_executed": True,
            "real_cleanup_approved": True,
            "records_removed": post["removed"],
            "database_modified": True,
            "rollback_documented": True,
            "candles_preserved": True,
            "phase_6_13_status": "ENCERRADA_TECNICAMENTE",
        },
    }


def render_report(
    eligible_ids: list[int],
    safety_backup: dict[str, Any],
    pre: dict[str, Any],
    post: dict[str, Any],
    now: datetime,
) -> str:
    ids_text = ", ".join(str(value) for value in eligible_ids)

    lines: list[str] = []

    lines.append("# Fase 6.13 - Execucao real controlada da limpeza intraday")
    lines.append("")
    lines.append("Marcador inicio: INICIO_FASE6_13_EXECUCAO_REAL_LIMPEZA_CONTROLADA_20260713")
    lines.append("")
    lines.append(f"Data de geracao: {now.replace(microsecond=0).isoformat()}")
    lines.append("")
    lines.append("## Natureza")
    lines.append("")
    lines.append("Execucao real controlada da limpeza de registros intraday elegiveis.")
    lines.append("")
    lines.append("Esta fase executou DELETE limitado exclusivamente aos IDs elegiveis validados na Fase 6.12.")
    lines.append("")
    lines.append("## Confirmacao explicita")
    lines.append("")
    lines.append(f"- Variavel exigida: `{CONFIRM_ENV}`")
    lines.append(f"- Valor exigido: `{CONFIRM_VALUE}`")
    lines.append("- Confirmacao recebida: sim")
    lines.append("")
    lines.append("## Banco")
    lines.append("")
    lines.append(f"- Caminho: `{DB_PATH.as_posix()}`")
    lines.append(f"- SHA256 antes: `{pre['db_sha_before']}`")
    lines.append(f"- SHA256 depois: `{post['db_sha_after']}`")
    lines.append(f"- SQLite integrity_check antes: `{pre['db_integrity_before']}`")
    lines.append(f"- SQLite integrity_check depois: `{post['db_integrity_after']}`")
    lines.append("- Banco alterado: sim")
    lines.append("")
    lines.append("## Backup e rollback")
    lines.append("")
    lines.append(f"- Backup primario Fase 6.11: `{pre['rollback_backup_path']}`")
    lines.append(f"- SHA256 backup primario: `{pre['rollback_backup_sha']}`")
    lines.append(f"- Integridade backup primario: `{pre['rollback_backup_integrity']}`")
    lines.append(f"- Backup local de seguranca Fase 6.13: `{safety_backup['path']}`")
    lines.append(f"- SHA256 backup local: `{safety_backup['sha256']}`")
    lines.append(f"- Integridade backup local: `{safety_backup['sqlite_integrity_check']}`")
    lines.append("- Rollback disponivel: sim")
    lines.append("")
    lines.append("## Execucao da limpeza")
    lines.append("")
    lines.append(f"- Tabela alvo: `{TARGET_TABLE}`")
    lines.append(f"- Coluna alvo: `{TARGET_ID_COLUMN}`")
    lines.append(f"- Total antes: {pre['total_before']}")
    lines.append(f"- Total depois: {post['total_after']}")
    lines.append(f"- IDs elegiveis antes: {pre['eligible_present_before']}")
    lines.append(f"- IDs elegiveis depois: {post['eligible_present_after']}")
    lines.append(f"- Registros removidos: {post['removed']}")
    lines.append(f"- IDs bloqueados: {EXPECTED_BLOCKED_COUNT}")
    lines.append(f"- Menor ID removido: {pre['min_eligible_id']}")
    lines.append(f"- Maior ID removido: {pre['max_eligible_id']}")
    lines.append(f"- IDs removidos: `{ids_text}`")
    lines.append("")
    lines.append("## Preservacao de candles")
    lines.append("")
    lines.append(f"- Tabela de candles: `{CANDLES_TABLE}`")
    lines.append(f"- Tabela existe: {'sim' if pre['candles_exists'] else 'nao'}")
    lines.append(f"- Linhas antes: {pre['candles_before']}")
    lines.append(f"- Linhas depois: {post['candles_after']}")
    lines.append("- Candles modificados: nao")
    lines.append("")
    lines.append("## Plano de rollback")
    lines.append("")
    lines.append("Se for necessario reverter esta fase:")
    lines.append("")
    lines.append("1. Parar qualquer processo que escreva no banco.")
    lines.append("2. Preservar copia do banco atual para auditoria, se necessario.")
    lines.append(f"3. Restaurar `{DB_PATH.as_posix()}` usando o backup primario `{pre['rollback_backup_path']}`.")
    lines.append("4. Alternativamente, usar o backup local de seguranca da Fase 6.13.")
    lines.append("5. Calcular SHA256 do banco restaurado.")
    lines.append("6. Executar SQLite integrity_check.")
    lines.append("7. Registrar a reversao em auditoria.")
    lines.append("")
    lines.append("## Resultado")
    lines.append("")
    lines.append("- Status: LIMPEZA_REAL_CONTROLADA_EXECUTADA")
    lines.append("- Limpeza real executada: sim")
    lines.append("- Limpeza real aprovada: sim")
    lines.append(f"- Registros removidos: {post['removed']}")
    lines.append("- Banco alterado: sim")
    lines.append("- Rollback documentado: sim")
    lines.append("- Candles preservados: sim")
    lines.append("- Integridade final: ok")
    lines.append("- Fase 6.13 encerrada tecnicamente: sim")
    lines.append("")
    lines.append("## Decisao")
    lines.append("")
    lines.append("A Fase 6.13 executou a limpeza real controlada dos 60 registros elegiveis.")
    lines.append("")
    lines.append("A proxima etapa recomendada e a Fase 6.14 - validacao pos-limpeza, performance e ausencia de regressao.")
    lines.append("")
    lines.append("Marcador fim: FIM_FASE6_13_EXECUCAO_REAL_LIMPEZA_CONTROLADA_20260713")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    now = datetime.now(timezone.utc)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)

    require_confirmation()

    manifest_6_12 = load_json(PHASE_6_12_MANIFEST)
    eligible_ids = validate_phase_6_12_manifest(manifest_6_12)

    pre = validate_pre_delete_state(manifest_6_12, eligible_ids)

    safety_backup = create_local_safety_backup(pre["db_sha_before"])

    post = execute_controlled_delete(eligible_ids, pre)

    manifest = build_manifest(
        manifest_6_12=manifest_6_12,
        eligible_ids=eligible_ids,
        safety_backup=safety_backup,
        pre=pre,
        post=post,
        now=now,
    )

    MANIFEST_PATH.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    REPORT_PATH.write_text(
        render_report(
            eligible_ids=eligible_ids,
            safety_backup=safety_backup,
            pre=pre,
            post=post,
            now=now,
        ),
        encoding="utf-8",
    )

    print("Limpeza real controlada executada com sucesso.")
    print(f"Relatorio gerado em: {REPORT_PATH.as_posix()}")
    print(f"Manifesto gerado em: {MANIFEST_PATH.as_posix()}")
    print(f"Banco: {DB_PATH.as_posix()}")
    print(f"SHA256 antes: {pre['db_sha_before']}")
    print(f"SHA256 depois: {post['db_sha_after']}")
    print(f"Integridade antes: {pre['db_integrity_before']}")
    print(f"Integridade depois: {post['db_integrity_after']}")
    print(f"Backup primario rollback: {pre['rollback_backup_path']}")
    print(f"Backup local seguranca: {safety_backup['path']}")
    print(f"Tabela alvo: {TARGET_TABLE}")
    print(f"Total antes: {pre['total_before']}")
    print(f"Total depois: {post['total_after']}")
    print(f"IDs elegiveis antes: {pre['eligible_present_before']}")
    print(f"IDs elegiveis depois: {post['eligible_present_after']}")
    print(f"Registros removidos: {post['removed']}")
    print(f"Candles antes: {pre['candles_before']}")
    print(f"Candles depois: {post['candles_after']}")
    print("Limpeza real executada: sim")
    print("Limpeza real aprovada: sim")
    print("Banco alterado: sim")
    print("Rollback documentado: sim")
    print("Candles preservados: sim")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
