from __future__ import annotations

import hashlib
import json
import shutil
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


DB_PATH = Path("dados/app.db")
PLAN_MANIFEST_PATH = Path("FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_10_manifesto_ids_elegiveis_20260713.json")

BACKUP_DIR = Path("backups_local/fase6_11_backup_fisico_controlado_20260713")
BACKUP_DB_PATH = BACKUP_DIR / "app_fase6_11_backup_fisico_controlado_20260713.db"

REPORT_PATH = Path("FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_11_backup_fisico_controlado_20260713.md")
MANIFEST_PATH = Path("FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_11_backup_fisico_controlado_20260713.json")

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


def load_phase_6_10_manifest() -> dict:
    if not PLAN_MANIFEST_PATH.exists():
        raise FileNotFoundError(f"Manifesto da Fase 6.10 nao encontrado: {PLAN_MANIFEST_PATH}")

    return json.loads(PLAN_MANIFEST_PATH.read_text(encoding="utf-8"))


def ensure_local_backup_ignored() -> None:
    exclude_path = Path(".git/info/exclude")
    exclude_path.parent.mkdir(parents=True, exist_ok=True)

    line = "backups_local/\n"

    existing = exclude_path.read_text(encoding="utf-8") if exclude_path.exists() else ""

    if line not in existing:
        with exclude_path.open("a", encoding="utf-8") as file_obj:
            if existing and not existing.endswith("\n"):
                file_obj.write("\n")
            file_obj.write(line)


def create_physical_backup() -> dict:
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Banco nao encontrado: {DB_PATH}")

    phase_6_10 = load_phase_6_10_manifest()

    expected_sha256 = phase_6_10["database"]["sha256"]
    expected_eligible = phase_6_10["summary"]["eligible_count"]
    expected_blocked = phase_6_10["summary"]["blocked_count"]
    expected_approval = phase_6_10["summary"]["real_cleanup_approved"]
    expected_backup_required = phase_6_10["summary"]["backup_required_before_cleanup"]

    source_sha_before = sha256_file(DB_PATH)
    source_size_before = DB_PATH.stat().st_size

    if source_sha_before != expected_sha256:
        raise RuntimeError(
            "SHA256 atual do banco diverge do manifesto da Fase 6.10. "
            f"Atual={source_sha_before}; esperado={expected_sha256}"
        )

    if expected_eligible != 60 or expected_blocked != 0:
        raise RuntimeError(
            "Volumetria do manifesto da Fase 6.10 nao esta no estado esperado "
            f"eligible={expected_eligible}, blocked={expected_blocked}"
        )

    if expected_approval is not False:
        raise RuntimeError("Manifesto da Fase 6.10 nao bloqueia limpeza real.")

    if expected_backup_required is not True:
        raise RuntimeError("Manifesto da Fase 6.10 nao exige backup obrigatorio.")

    original_integrity = sqlite_integrity_check(DB_PATH)

    if original_integrity.lower() != "ok":
        raise RuntimeError(f"Integridade do banco original invalida: {original_integrity}")

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    if BACKUP_DB_PATH.exists():
        raise FileExistsError(f"Backup ja existe e nao sera sobrescrito: {BACKUP_DB_PATH}")

    shutil.copy2(DB_PATH, BACKUP_DB_PATH)

    source_sha_after = sha256_file(DB_PATH)
    source_size_after = DB_PATH.stat().st_size
    backup_sha256 = sha256_file(BACKUP_DB_PATH)
    backup_size = BACKUP_DB_PATH.stat().st_size
    backup_integrity = sqlite_integrity_check(BACKUP_DB_PATH)

    if source_sha_after != source_sha_before:
        raise RuntimeError(
            "Banco original mudou durante a criacao do backup. "
            f"Antes={source_sha_before}; depois={source_sha_after}"
        )

    if backup_sha256 != source_sha_before:
        raise RuntimeError(
            "SHA256 do backup diverge do banco original. "
            f"Backup={backup_sha256}; original={source_sha_before}"
        )

    if backup_size != source_size_before:
        raise RuntimeError(
            "Tamanho do backup diverge do banco original. "
            f"Backup={backup_size}; original={source_size_before}"
        )

    if backup_integrity.lower() != "ok":
        raise RuntimeError(f"Integridade do backup invalida: {backup_integrity}")

    return {
        "source_sha_before": source_sha_before,
        "source_sha_after": source_sha_after,
        "source_size_before": source_size_before,
        "source_size_after": source_size_after,
        "backup_sha256": backup_sha256,
        "backup_size": backup_size,
        "original_integrity": original_integrity,
        "backup_integrity": backup_integrity,
        "expected_eligible": expected_eligible,
        "expected_blocked": expected_blocked,
    }


def build_manifest(result: dict, now: datetime) -> dict:
    return {
        "phase": "6.11",
        "generated_at_utc": now.replace(microsecond=0).isoformat(),
        "source_database": {
            "path": DB_PATH.as_posix(),
            "sha256_before_backup": result["source_sha_before"],
            "sha256_after_backup": result["source_sha_after"],
            "size_before_backup": result["source_size_before"],
            "size_after_backup": result["source_size_after"],
            "sqlite_integrity_check": result["original_integrity"],
        },
        "backup_database": {
            "path": BACKUP_DB_PATH.as_posix(),
            "sha256": result["backup_sha256"],
            "size_bytes": result["backup_size"],
            "sqlite_integrity_check": result["backup_integrity"],
            "versioned_in_git": False,
        },
        "phase_6_10_reference": {
            "manifest": PLAN_MANIFEST_PATH.as_posix(),
            "eligible_count": result["expected_eligible"],
            "blocked_count": result["expected_blocked"],
            "real_cleanup_approved": False,
            "backup_required_before_cleanup": True,
        },
        "rule": {
            "timezone": LOCAL_TZ_NAME,
            "cleanup_executed": False,
            "records_removed": 0,
            "database_modified": False,
        },
        "decision": {
            "backup_created": True,
            "backup_validated": True,
            "approved_for_real_cleanup": False,
        },
    }


def render_report(result: dict, now: datetime) -> str:
    lines: list[str] = []

    lines.append("# Fase 6.11 - Backup fisico controlado")
    lines.append("")
    lines.append("Marcador inicio: INICIO_FASE6_11_BACKUP_FISICO_CONTROLADO_20260713")
    lines.append("")
    lines.append(f"Data de geracao: {now.replace(microsecond=0).isoformat()}")
    lines.append("")
    lines.append("## Natureza")
    lines.append("")
    lines.append("Criacao de backup fisico local antes de qualquer limpeza real.")
    lines.append("")
    lines.append("Esta fase nao executa limpeza, nao remove registros e nao altera o banco original.")
    lines.append("")
    lines.append("## Referencia da Fase 6.10")
    lines.append("")
    lines.append(f"- Manifesto: `{PLAN_MANIFEST_PATH.as_posix()}`")
    lines.append(f"- IDs elegiveis confirmados: {result['expected_eligible']}")
    lines.append(f"- IDs bloqueados confirmados: {result['expected_blocked']}")
    lines.append("- Limpeza real aprovada na Fase 6.10: nao")
    lines.append("- Backup obrigatorio antes da limpeza real: sim")
    lines.append("")
    lines.append("## Banco original")
    lines.append("")
    lines.append(f"- Caminho: `{DB_PATH.as_posix()}`")
    lines.append(f"- SHA256 antes do backup: `{result['source_sha_before']}`")
    lines.append(f"- SHA256 depois do backup: `{result['source_sha_after']}`")
    lines.append(f"- Tamanho antes do backup: {result['source_size_before']}")
    lines.append(f"- Tamanho depois do backup: {result['source_size_after']}")
    lines.append(f"- SQLite integrity_check: `{result['original_integrity']}`")
    lines.append("")
    lines.append("## Backup fisico")
    lines.append("")
    lines.append(f"- Caminho local: `{BACKUP_DB_PATH.as_posix()}`")
    lines.append(f"- SHA256 do backup: `{result['backup_sha256']}`")
    lines.append(f"- Tamanho do backup: {result['backup_size']}")
    lines.append(f"- SQLite integrity_check: `{result['backup_integrity']}`")
    lines.append("- Backup versionado no Git: nao")
    lines.append("")
    lines.append("## Validacoes")
    lines.append("")
    lines.append("- SHA256 do banco atual confere com o manifesto da Fase 6.10: sim")
    lines.append("- SHA256 do banco original permaneceu estavel durante o backup: sim")
    lines.append("- SHA256 do backup confere com o banco original: sim")
    lines.append("- Tamanho do backup confere com o banco original: sim")
    lines.append("- Integridade SQLite do banco original: ok")
    lines.append("- Integridade SQLite do backup: ok")
    lines.append("")
    lines.append("## Resultado")
    lines.append("")
    lines.append("- Status: BACKUP_FISICO_CONTROLADO_CRIADO_E_VALIDADO")
    lines.append("- Backup criado: sim")
    lines.append("- Backup validado: sim")
    lines.append("- Registros removidos: 0")
    lines.append("- Banco original alterado: nao")
    lines.append("- Limpeza real aprovada: nao")
    lines.append("")
    lines.append("## Decisao")
    lines.append("")
    lines.append("A Fase 6.11 encerra a preparacao de backup.")
    lines.append("")
    lines.append("A limpeza real permanece bloqueada ate fase posterior explicitamente aprovada.")
    lines.append("")
    lines.append("Marcador fim: FIM_FASE6_11_BACKUP_FISICO_CONTROLADO_20260713")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    now = datetime.now(timezone.utc)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)

    ensure_local_backup_ignored()

    result = create_physical_backup()
    manifest = build_manifest(result, now)

    MANIFEST_PATH.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    REPORT_PATH.write_text(render_report(result, now), encoding="utf-8")

    print("Backup fisico controlado criado e validado.")
    print(f"Banco original: {DB_PATH.as_posix()}")
    print(f"Backup fisico local: {BACKUP_DB_PATH.as_posix()}")
    print(f"Relatorio gerado em: {REPORT_PATH.as_posix()}")
    print(f"Manifesto gerado em: {MANIFEST_PATH.as_posix()}")
    print(f"SHA256 original antes: {result['source_sha_before']}")
    print(f"SHA256 original depois: {result['source_sha_after']}")
    print(f"SHA256 backup: {result['backup_sha256']}")
    print(f"Integridade original: {result['original_integrity']}")
    print(f"Integridade backup: {result['backup_integrity']}")
    print("Backup versionado no Git: nao")
    print("Registros removidos: 0")
    print("Banco original alterado: nao")
    print("Limpeza real aprovada: nao")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
