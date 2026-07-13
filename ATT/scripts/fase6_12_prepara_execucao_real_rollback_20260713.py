from __future__ import annotations

import hashlib
import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DB_PATH = Path("dados/app.db")

PHASE_6_10_MANIFEST = Path(
    "FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_10_manifesto_ids_elegiveis_20260713.json"
)
PHASE_6_10_REPORT = Path(
    "FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_10_plano_execucao_controlada_backup_20260713.md"
)
PHASE_6_11_MANIFEST = Path(
    "FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_11_backup_fisico_controlado_20260713.json"
)

REPORT_PATH = Path(
    "FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_12_prepara_execucao_real_rollback_20260713.md"
)
MANIFEST_PATH = Path(
    "FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_12_prepara_execucao_real_rollback_20260713.json"
)

TARGET_TABLE = "rtd_option_quotes_intraday_history"
TARGET_ID_COLUMN = "id"
LOCAL_TZ_NAME = "America/Sao_Paulo"


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


def sqlite_integrity_check(path: Path) -> str:
    with connect_read_only(path) as conn:
        row = conn.execute("PRAGMA integrity_check").fetchone()

    if not row:
        return "sem_resultado"

    return str(row[0])


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Arquivo obrigatorio nao encontrado: {path}")

    return json.loads(path.read_text(encoding="utf-8"))


def normalize_int_list(values: Any) -> list[int]:
    if not isinstance(values, list):
        return []

    result: list[int] = []

    for value in values:
        if isinstance(value, int):
            result.append(value)
        elif isinstance(value, str) and value.strip().isdigit():
            result.append(int(value.strip()))

    return sorted(set(result))


def recursive_find_eligible_ids(payload: Any) -> list[int]:
    if isinstance(payload, dict):
        for key, value in payload.items():
            key_lower = str(key).lower()

            if key_lower in {
                "eligible_ids",
                "ids_elegiveis",
                "eligible_id_list",
                "manifest_eligible_ids",
            }:
                ids = normalize_int_list(value)
                if ids:
                    return ids

        for value in payload.values():
            ids = recursive_find_eligible_ids(value)
            if ids:
                return ids

    if isinstance(payload, list):
        extracted: list[int] = []

        for item in payload:
            if isinstance(item, dict):
                status_text = json.dumps(item, ensure_ascii=False).lower()
                possible_id = item.get("id") or item.get("row_id") or item.get("history_id")

                if possible_id is not None and "elegivel" in status_text:
                    if isinstance(possible_id, int):
                        extracted.append(possible_id)
                    elif isinstance(possible_id, str) and possible_id.strip().isdigit():
                        extracted.append(int(possible_id.strip()))

        if extracted:
            return sorted(set(extracted))

        for item in payload:
            ids = recursive_find_eligible_ids(item)
            if ids:
                return ids

    return []


def extract_ids_from_phase_6_10_report() -> list[int]:
    if not PHASE_6_10_REPORT.exists():
        return []

    text = PHASE_6_10_REPORT.read_text(encoding="utf-8")

    match = re.search(r"IDs elegiveis:\s*`([^`]+)`", text)

    if not match:
        return []

    raw_ids = match.group(1)
    ids: list[int] = []

    for part in raw_ids.split(","):
        value = part.strip()
        if value.isdigit():
            ids.append(int(value))

    return sorted(set(ids))


def extract_eligible_ids(phase_6_10_manifest: dict[str, Any]) -> list[int]:
    ids = recursive_find_eligible_ids(phase_6_10_manifest)

    if ids:
        return ids

    return extract_ids_from_phase_6_10_report()


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


def build_preflight() -> dict[str, Any]:
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Banco nao encontrado: {DB_PATH}")

    phase_6_10 = load_json(PHASE_6_10_MANIFEST)
    phase_6_11 = load_json(PHASE_6_11_MANIFEST)

    phase_6_10_sha = phase_6_10["database"]["sha256"]
    phase_6_10_summary = phase_6_10["summary"]

    phase_6_10_eligible_count = int(phase_6_10_summary["eligible_count"])
    phase_6_10_blocked_count = int(phase_6_10_summary["blocked_count"])
    phase_6_10_real_cleanup_approved = phase_6_10_summary["real_cleanup_approved"]
    phase_6_10_backup_required = phase_6_10_summary["backup_required_before_cleanup"]

    phase_6_11_source_sha_after = phase_6_11["source_database"]["sha256_after_backup"]
    phase_6_11_backup_path = Path(phase_6_11["backup_database"]["path"])
    phase_6_11_backup_sha = phase_6_11["backup_database"]["sha256"]
    phase_6_11_backup_versioned = phase_6_11["backup_database"]["versioned_in_git"]
    phase_6_11_backup_validated = phase_6_11["decision"]["backup_validated"]
    phase_6_11_approved_for_real_cleanup = phase_6_11["decision"]["approved_for_real_cleanup"]

    source_sha_current = sha256_file(DB_PATH)
    source_integrity = sqlite_integrity_check(DB_PATH)

    if source_sha_current != phase_6_10_sha:
        raise RuntimeError(
            "SHA256 atual do banco diverge do manifesto da Fase 6.10. "
            f"Atual={source_sha_current}; Fase6.10={phase_6_10_sha}"
        )

    if source_sha_current != phase_6_11_source_sha_after:
        raise RuntimeError(
            "SHA256 atual do banco diverge do manifesto da Fase 6.11. "
            f"Atual={source_sha_current}; Fase6.11={phase_6_11_source_sha_after}"
        )

    if source_integrity.lower() != "ok":
        raise RuntimeError(f"Integridade do banco original invalida: {source_integrity}")

    if phase_6_10_eligible_count != 60:
        raise RuntimeError(f"Quantidade elegivel inesperada na Fase 6.10: {phase_6_10_eligible_count}")

    if phase_6_10_blocked_count != 0:
        raise RuntimeError(f"Quantidade bloqueada inesperada na Fase 6.10: {phase_6_10_blocked_count}")

    if phase_6_10_real_cleanup_approved is not False:
        raise RuntimeError("A Fase 6.10 nao deve aprovar limpeza real.")

    if phase_6_10_backup_required is not True:
        raise RuntimeError("A Fase 6.10 deve exigir backup obrigatorio.")

    if phase_6_11_approved_for_real_cleanup is not False:
        raise RuntimeError("A Fase 6.11 nao deve aprovar limpeza real.")

    if phase_6_11_backup_validated is not True:
        raise RuntimeError("Backup da Fase 6.11 nao esta validado.")

    if phase_6_11_backup_versioned is not False:
        raise RuntimeError("Backup fisico nao deve estar versionado no Git.")

    if not phase_6_11_backup_path.exists():
        raise FileNotFoundError(f"Backup fisico da Fase 6.11 nao encontrado: {phase_6_11_backup_path}")

    backup_sha_current = sha256_file(phase_6_11_backup_path)
    backup_integrity = sqlite_integrity_check(phase_6_11_backup_path)

    if backup_sha_current != phase_6_11_backup_sha:
        raise RuntimeError(
            "SHA256 atual do backup diverge do manifesto da Fase 6.11. "
            f"Atual={backup_sha_current}; Fase6.11={phase_6_11_backup_sha}"
        )

    if backup_sha_current != source_sha_current:
        raise RuntimeError(
            "Backup fisico nao confere com banco atual. "
            f"Backup={backup_sha_current}; banco={source_sha_current}"
        )

    if backup_integrity.lower() != "ok":
        raise RuntimeError(f"Integridade do backup invalida: {backup_integrity}")

    eligible_ids = extract_eligible_ids(phase_6_10)

    if len(eligible_ids) != phase_6_10_eligible_count:
        raise RuntimeError(
            "Nao foi possivel confirmar a lista completa de IDs elegiveis. "
            f"Lista={len(eligible_ids)}; esperado={phase_6_10_eligible_count}"
        )

    with connect_read_only(DB_PATH) as conn:
        if not table_exists(conn, TARGET_TABLE):
            raise RuntimeError(f"Tabela alvo nao existe: {TARGET_TABLE}")

        columns = table_columns(conn, TARGET_TABLE)

        if TARGET_ID_COLUMN not in columns:
            raise RuntimeError(f"Coluna alvo nao existe: {TARGET_TABLE}.{TARGET_ID_COLUMN}")

        total_before = count_table(conn, TARGET_TABLE)
        eligible_present = count_ids_present(conn, eligible_ids)
        min_id, max_id = min_max_ids_present(conn, eligible_ids)

        candles_total = 0
        candles_table_exists = table_exists(conn, "rtd_option_quotes_intraday_candles")

        if candles_table_exists:
            candles_total = count_table(conn, "rtd_option_quotes_intraday_candles")

    if eligible_present != phase_6_10_eligible_count:
        raise RuntimeError(
            "Quantidade de IDs elegiveis presentes no banco diverge do plano. "
            f"Presentes={eligible_present}; esperado={phase_6_10_eligible_count}"
        )

    return {
        "source_sha_current": source_sha_current,
        "source_integrity": source_integrity,
        "backup_path": phase_6_11_backup_path.as_posix(),
        "backup_sha_current": backup_sha_current,
        "backup_integrity": backup_integrity,
        "eligible_ids": eligible_ids,
        "eligible_count": phase_6_10_eligible_count,
        "blocked_count": phase_6_10_blocked_count,
        "total_before": total_before,
        "eligible_present": eligible_present,
        "min_eligible_id": min_id,
        "max_eligible_id": max_id,
        "candles_table_exists": candles_table_exists,
        "candles_total": candles_total,
    }


def build_manifest(preflight: dict[str, Any], now: datetime) -> dict[str, Any]:
    return {
        "phase": "6.12",
        "generated_at_utc": now.replace(microsecond=0).isoformat(),
        "nature": "preparacao_execucao_real_com_rollback",
        "database": {
            "path": DB_PATH.as_posix(),
            "sha256_current": preflight["source_sha_current"],
            "sqlite_integrity_check": preflight["source_integrity"],
            "database_modified": False,
        },
        "backup_reference": {
            "phase": "6.11",
            "path": preflight["backup_path"],
            "sha256_current": preflight["backup_sha_current"],
            "sqlite_integrity_check": preflight["backup_integrity"],
            "validated": True,
            "versioned_in_git": False,
        },
        "cleanup_candidate": {
            "source_phase": "6.10",
            "target_table": TARGET_TABLE,
            "target_id_column": TARGET_ID_COLUMN,
            "eligible_count": preflight["eligible_count"],
            "blocked_count": preflight["blocked_count"],
            "eligible_ids": preflight["eligible_ids"],
            "eligible_present_in_database": preflight["eligible_present"],
            "min_eligible_id": preflight["min_eligible_id"],
            "max_eligible_id": preflight["max_eligible_id"],
            "table_total_before": preflight["total_before"],
        },
        "candles_preservation": {
            "table": "rtd_option_quotes_intraday_candles",
            "table_exists": preflight["candles_table_exists"],
            "rows_before": preflight["candles_total"],
            "planned_to_modify": False,
        },
        "rollback_plan": {
            "method": "restaurar_arquivo_db_a_partir_do_backup_fisico_validado",
            "backup_path": preflight["backup_path"],
            "requires_system_stopped": True,
            "requires_sha256_validation_after_restore": True,
            "requires_sqlite_integrity_check_after_restore": True,
        },
        "decision": {
            "preflight_ready": True,
            "real_cleanup_executed": False,
            "real_cleanup_approved": False,
            "records_removed": 0,
            "database_modified": False,
            "next_phase_requires_explicit_confirmation": True,
        },
        "guardrails_for_next_phase": [
            "branch_correta",
            "working_tree_limpo",
            "processos_de_escrita_parados",
            "backup_fisico_existente",
            "backup_integrity_check_ok",
            "sha256_banco_atual_compativel",
            "ids_elegiveis_conferidos",
            "rollback_documentado",
            "confirmacao_explicita_obrigatoria",
        ],
    }


def render_report(preflight: dict[str, Any], now: datetime) -> str:
    eligible_ids_text = ", ".join(str(value) for value in preflight["eligible_ids"])

    lines: list[str] = []

    lines.append("# Fase 6.12 - Preparacao da execucao real controlada com rollback")
    lines.append("")
    lines.append("Marcador inicio: INICIO_FASE6_12_PREPARA_EXECUCAO_REAL_ROLLBACK_20260713")
    lines.append("")
    lines.append(f"Data de geracao: {now.replace(microsecond=0).isoformat()}")
    lines.append("")
    lines.append("## Natureza")
    lines.append("")
    lines.append("Preparacao read-only da fase posterior de limpeza real controlada.")
    lines.append("")
    lines.append("Esta fase nao remove registros, nao altera o banco e nao aprova limpeza real.")
    lines.append("")
    lines.append("## Referencias obrigatorias")
    lines.append("")
    lines.append(f"- Manifesto Fase 6.10: `{PHASE_6_10_MANIFEST.as_posix()}`")
    lines.append(f"- Relatorio Fase 6.10: `{PHASE_6_10_REPORT.as_posix()}`")
    lines.append(f"- Manifesto Fase 6.11: `{PHASE_6_11_MANIFEST.as_posix()}`")
    lines.append("")
    lines.append("## Banco atual")
    lines.append("")
    lines.append(f"- Caminho: `{DB_PATH.as_posix()}`")
    lines.append(f"- SHA256 atual: `{preflight['source_sha_current']}`")
    lines.append(f"- SQLite integrity_check: `{preflight['source_integrity']}`")
    lines.append("- Banco alterado nesta fase: nao")
    lines.append("")
    lines.append("## Backup fisico validado")
    lines.append("")
    lines.append(f"- Caminho: `{preflight['backup_path']}`")
    lines.append(f"- SHA256 atual do backup: `{preflight['backup_sha_current']}`")
    lines.append(f"- SQLite integrity_check do backup: `{preflight['backup_integrity']}`")
    lines.append("- Backup versionado no Git: nao")
    lines.append("")
    lines.append("## Candidato de limpeza para fase posterior")
    lines.append("")
    lines.append(f"- Tabela alvo: `{TARGET_TABLE}`")
    lines.append(f"- Coluna alvo: `{TARGET_ID_COLUMN}`")
    lines.append(f"- Total atual na tabela alvo: {preflight['total_before']}")
    lines.append(f"- IDs elegiveis no plano: {preflight['eligible_count']}")
    lines.append(f"- IDs elegiveis presentes no banco: {preflight['eligible_present']}")
    lines.append(f"- IDs bloqueados: {preflight['blocked_count']}")
    lines.append(f"- Menor ID elegivel: {preflight['min_eligible_id']}")
    lines.append(f"- Maior ID elegivel: {preflight['max_eligible_id']}")
    lines.append(f"- Lista de IDs elegiveis: `{eligible_ids_text}`")
    lines.append("")
    lines.append("## Preservacao de candles")
    lines.append("")
    lines.append(f"- Tabela de candles existe: {'sim' if preflight['candles_table_exists'] else 'nao'}")
    lines.append(f"- Linhas em candles antes da fase posterior: {preflight['candles_total']}")
    lines.append("- Candles planejados para modificacao: nao")
    lines.append("")
    lines.append("## Plano de rollback documentado")
    lines.append("")
    lines.append("Caso a fase posterior precise ser revertida:")
    lines.append("")
    lines.append("1. Parar qualquer processo que escreva no banco.")
    lines.append("2. Preservar uma copia do banco pos-execucao para auditoria, se necessario.")
    lines.append(f"3. Restaurar o arquivo `{DB_PATH.as_posix()}` a partir do backup `{preflight['backup_path']}`.")
    lines.append("4. Calcular SHA256 do banco restaurado.")
    lines.append("5. Confirmar que o SHA256 restaurado confere com o SHA256 do backup validado.")
    lines.append("6. Executar SQLite integrity_check no banco restaurado.")
    lines.append("7. Registrar resultado em auditoria.")
    lines.append("")
    lines.append("## Guardrails obrigatorios para fase posterior")
    lines.append("")
    lines.append("- Branch correta.")
    lines.append("- Working tree limpo.")
    lines.append("- Processos de escrita parados.")
    lines.append("- Backup fisico existente e validado.")
    lines.append("- SHA256 atual compativel com Fases 6.10 e 6.11.")
    lines.append("- IDs elegiveis conferidos.")
    lines.append("- Candles preservados.")
    lines.append("- Rollback documentado.")
    lines.append("- Confirmacao explicita obrigatoria para limpeza real.")
    lines.append("")
    lines.append("## Resultado")
    lines.append("")
    lines.append("- Status: PRE_FLIGHT_EXECUCAO_REAL_COM_ROLLBACK_PRONTO")
    lines.append("- Pre-flight pronto: sim")
    lines.append("- Backup validado: sim")
    lines.append("- Rollback documentado: sim")
    lines.append("- Limpeza real executada: nao")
    lines.append("- Limpeza real aprovada: nao")
    lines.append("- Registros removidos: 0")
    lines.append("- Banco alterado: nao")
    lines.append("- Proxima fase exige confirmacao explicita: sim")
    lines.append("")
    lines.append("## Decisao")
    lines.append("")
    lines.append("A Fase 6.12 prepara a execucao real controlada, mas nao executa limpeza.")
    lines.append("")
    lines.append("A limpeza real permanece bloqueada ate a Fase 6.13, se houver confirmacao explicita.")
    lines.append("")
    lines.append("Marcador fim: FIM_FASE6_12_PREPARA_EXECUCAO_REAL_ROLLBACK_20260713")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    now = datetime.now(timezone.utc)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)

    preflight = build_preflight()
    manifest = build_manifest(preflight, now)

    MANIFEST_PATH.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    REPORT_PATH.write_text(render_report(preflight, now), encoding="utf-8")

    print("Preparacao da execucao real com rollback concluida em modo read-only.")
    print(f"Relatorio gerado em: {REPORT_PATH.as_posix()}")
    print(f"Manifesto gerado em: {MANIFEST_PATH.as_posix()}")
    print(f"Banco atual: {DB_PATH.as_posix()}")
    print(f"SHA256 banco atual: {preflight['source_sha_current']}")
    print(f"Integridade banco atual: {preflight['source_integrity']}")
    print(f"Backup fisico: {preflight['backup_path']}")
    print(f"SHA256 backup: {preflight['backup_sha_current']}")
    print(f"Integridade backup: {preflight['backup_integrity']}")
    print(f"Tabela alvo futura: {TARGET_TABLE}")
    print(f"IDs elegiveis confirmados: {preflight['eligible_present']}/{preflight['eligible_count']}")
    print(f"IDs bloqueados: {preflight['blocked_count']}")
    print("Pre-flight pronto: sim")
    print("Rollback documentado: sim")
    print("Limpeza real executada: nao")
    print("Limpeza real aprovada: nao")
    print("Registros removidos: 0")
    print("Banco alterado: nao")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
