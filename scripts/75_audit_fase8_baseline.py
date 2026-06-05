# scripts/75_audit_fase8_baseline.py
"""
patch_67 -- Auditoria de baseline fase 8: governança, rastreabilidade e operação.

Verifica:
  - Tabelas canônicas existem e têm schema esperado (structures, structure_legs,
    pricing_executions, payoff_curve_points, structure_decisions)
  - Conexões app.db e derived.db acessíveis
  - StructuresRepository operacional (CRUD básico)
  - DerivedRepo operacional (bootstrap + colunas)
  - derived_service: funções de leitura e cleanup presentes
  - bootstrap_structures_schema: idempotente
  - Scripts de auditoria de fases anteriores presentes (patch_52, patch_74)
  - Relatórios de fases anteriores presentes
  - Diretório ATT/reports/ gravável

Saída:
  ATT/reports/fase8_baseline.md
  ATT/reports/fase8_baseline.json
"""
from __future__ import annotations

import json
import sqlite3
import sys
import traceback
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuração de paths
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR  = PROJECT_ROOT / "ATT" / "reports"
DB_APP       = PROJECT_ROOT / "dados" / "app.db"
DB_DERIVED   = PROJECT_ROOT / "dados" / "derived.db"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ---------------------------------------------------------------------------
# Estruturas de resultado
# ---------------------------------------------------------------------------

@dataclass
class CheckResult:
    categoria:   str
    check:       str
    status:      str        # OK | WARN | FAIL
    detalhe:     str = ""
    exc:         str = ""


@dataclass
class AuditReport:
    gerado_em:   str
    raiz:        str
    total_ok:    int = 0
    total_warn:  int = 0
    total_fail:  int = 0
    checks:      list = field(default_factory=list)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _ok(cat: str, check: str, detalhe: str = "") -> CheckResult:
    return CheckResult(cat, check, "OK", detalhe)

def _warn(cat: str, check: str, detalhe: str = "") -> CheckResult:
    return CheckResult(cat, check, "WARN", detalhe)

def _fail(cat: str, check: str, detalhe: str = "", exc: str = "") -> CheckResult:
    return CheckResult(cat, check, "FAIL", detalhe, exc)


def _table_columns(conn: sqlite3.Connection, table: str) -> list[str]:
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return [r[1] for r in rows]


def _table_exists(conn: sqlite3.Connection, table: str) -> bool:
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
        (table,),
    ).fetchone()
    return row is not None


# ---------------------------------------------------------------------------
# Categoria 1: Infraestrutura de banco de dados
# ---------------------------------------------------------------------------

def check_databases() -> list[CheckResult]:
    results = []
    cat = "infra_db"

    # --- app.db ---
    try:
        conn = sqlite3.connect(str(DB_APP))
        conn.execute("SELECT 1").fetchone()
        conn.close()
        results.append(_ok(cat, "app.db acessível", str(DB_APP)))
    except Exception as e:
        results.append(_fail(cat, "app.db acessível", str(DB_APP), str(e)))
        return results  # sem DB não adianta testar tabelas

    # Tabelas esperadas em app.db
    EXPECTED_APP_TABLES = {
        "structures": [
            "id", "name", "underlying_asset", "alias_legacy_aba",
            "status", "notes", "created_at", "updated_at",
        ],
        "structure_legs": [
            "id", "structure_id", "position_side", "option_type",
            "strike", "expiration_date", "quantity", "multiplier",
            "leg_order", "created_at", "updated_at",
        ],
        "pricing_executions": [
            "id", "created_at", "structure_id",
        ],
    }

    conn = sqlite3.connect(str(DB_APP))
    try:
        for table, expected_cols in EXPECTED_APP_TABLES.items():
            if not _table_exists(conn, table):
                results.append(_fail(cat, f"tabela {table} existe", f"não encontrada em app.db"))
                continue
            actual = _table_columns(conn, table)
            missing = [c for c in expected_cols if c not in actual]
            if missing:
                results.append(_warn(cat, f"schema {table}", f"colunas faltando: {missing}"))
            else:
                results.append(_ok(cat, f"tabela {table} + schema", f"{len(actual)} colunas"))
    finally:
        conn.close()

    # --- derived.db ---
    try:
        conn = sqlite3.connect(str(DB_DERIVED))
        conn.execute("SELECT 1").fetchone()
        conn.close()
        results.append(_ok(cat, "derived.db acessível", str(DB_DERIVED)))
    except Exception as e:
        results.append(_warn(cat, "derived.db acessível", f"não existe ainda ou erro: {e}"))
        return results

    EXPECTED_DERIVED_TABLES = {
        "payoff_curve_points": [
            "timestamp", "aba", "point_spot", "point_pl",
        ],
        "structure_decisions": [
            "id", "timestamp", "aba", "decision", "level",
        ],
    }

    conn = sqlite3.connect(str(DB_DERIVED))
    try:
        for table, expected_cols in EXPECTED_DERIVED_TABLES.items():
            if not _table_exists(conn, table):
                results.append(_warn(cat, f"tabela {table} existe",
                                     "não encontrada em derived.db (bootstrap pendente)"))
                continue
            actual = _table_columns(conn, table)
            missing = [c for c in expected_cols if c not in actual]
            if missing:
                results.append(_warn(cat, f"schema {table}", f"colunas faltando: {missing}"))
            else:
                results.append(_ok(cat, f"tabela derived/{table} + schema",
                                   f"{len(actual)} colunas"))
    finally:
        conn.close()

    return results


# ---------------------------------------------------------------------------
# Categoria 2: StructuresRepository
# ---------------------------------------------------------------------------

def check_structures_repository() -> list[CheckResult]:
    results = []
    cat = "structures_repo"

    try:
        from repositories.structures_repository import StructuresRepository
        results.append(_ok(cat, "import StructuresRepository"))
    except Exception as e:
        results.append(_fail(cat, "import StructuresRepository", exc=str(e)))
        return results

    try:
        repo = StructuresRepository(db_path=DB_APP)
        structs = repo.list_structures(include_archived=True)
        results.append(_ok(cat, "list_structures()", f"{len(structs)} estruturas"))
    except Exception as e:
        results.append(_fail(cat, "list_structures()", exc=str(e)))
        return results

    # Verifica métodos canônicos
    expected_methods = [
        "create_structure", "get_structure", "update_structure",
        "archive_structure", "add_leg", "replace_legs",
        "get_structure_by_alias", "get_structure_id_by_alias",
        "count_legs",
    ]
    for method in expected_methods:
        if hasattr(repo, method):
            results.append(_ok(cat, f"método {method} presente"))
        else:
            results.append(_fail(cat, f"método {method} presente", "não encontrado"))

    return results


# ---------------------------------------------------------------------------
# Categoria 3: DerivedRepo
# ---------------------------------------------------------------------------

def check_derived_repo() -> list[CheckResult]:
    results = []
    cat = "derived_repo"

    try:
        from db.derived_repo import DerivedRepo, ensure_derived_tables
        results.append(_ok(cat, "import DerivedRepo + ensure_derived_tables"))
    except Exception as e:
        results.append(_fail(cat, "import DerivedRepo", exc=str(e)))
        return results

    try:
        repo = DerivedRepo(db_path=str(DB_DERIVED))
        results.append(_ok(cat, "DerivedRepo.__init__() + bootstrap"))
    except Exception as e:
        results.append(_fail(cat, "DerivedRepo.__init__()", exc=str(e)))
        return results

    # Verifica colunas críticas via _table_columns
    try:
        cols_decisions = repo._table_columns("structure_decisions")
        required = {"timestamp", "aba", "decision", "level", "structure_id", "why"}
        missing = required - set(cols_decisions)
        if missing:
            results.append(_warn(cat, "colunas structure_decisions",
                                 f"faltando: {sorted(missing)}"))
        else:
            results.append(_ok(cat, "colunas structure_decisions",
                               f"{len(cols_decisions)} colunas"))
    except Exception as e:
        results.append(_fail(cat, "colunas structure_decisions", exc=str(e)))

    try:
        cols_payoff = repo._table_columns("payoff_curve_points")
        required_p = {"timestamp", "aba", "point_spot", "point_pl"}
        missing_p = required_p - set(cols_payoff)
        if missing_p:
            results.append(_warn(cat, "colunas payoff_curve_points",
                                 f"faltando: {sorted(missing_p)}"))
        else:
            results.append(_ok(cat, "colunas payoff_curve_points",
                               f"{len(cols_payoff)} colunas"))
    except Exception as e:
        results.append(_fail(cat, "colunas payoff_curve_points", exc=str(e)))

    # Métodos canônicos
    expected_methods = [
        "write_decision_snapshot_atomic", "write_payoff_snapshot_atomic",
        "write_complete_snapshot_atomic", "insert_structure_decision",
        "insert_payoff_points", "get_payoff_points", "get_recent_decisions",
        "validate_snapshot_consistency", "cleanup_old_payoff_data",
        "cleanup_old_decisions",
    ]
    for method in expected_methods:
        if hasattr(repo, method):
            results.append(_ok(cat, f"método {method} presente"))
        else:
            results.append(_fail(cat, f"método {method} presente", "não encontrado"))

    return results


# ---------------------------------------------------------------------------
# Categoria 4: derived_service
# ---------------------------------------------------------------------------

def check_derived_service() -> list[CheckResult]:
    results = []
    cat = "derived_service"

    try:
        import services.derived_service as svc
        results.append(_ok(cat, "import derived_service"))
    except Exception as e:
        results.append(_fail(cat, "import derived_service", exc=str(e)))
        return results

    expected_funcs = [
        "save_payoff_curve", "save_payoff_from_canonical_payload",
        "save_decision", "save_decision_from_canonical_payload",
        "cleanup_derived", "get_all_payoff_curves",
        "get_payoff_by_structure_id", "get_recent_decisions",
        "invalidate_aba_cache", "init_db",
        "format_report", "snapshot_aba",
    ]
    for fn in expected_funcs:
        if hasattr(svc, fn):
            results.append(_ok(cat, f"função {fn} presente"))
        else:
            results.append(_fail(cat, f"função {fn} presente", "não encontrada"))

    # Garante que get_payoff_by_aba foi removida (patch_65)
    if hasattr(svc, "get_payoff_by_aba"):
        results.append(_fail(cat, "get_payoff_by_aba removida (patch_65)",
                             "ainda presente — regressão"))
    else:
        results.append(_ok(cat, "get_payoff_by_aba removida (patch_65)"))

    return results


# ---------------------------------------------------------------------------
# Categoria 5: bootstrap_structures_schema
# ---------------------------------------------------------------------------

def check_bootstrap_schema() -> list[CheckResult]:
    results = []
    cat = "bootstrap_schema"

    try:
        from infra.bootstrap_structures_schema import (
            ensure_structures_schema,
            bootstrap_pricing_executions,
        )
        results.append(_ok(cat, "import bootstrap_structures_schema"))
    except Exception as e:
        results.append(_fail(cat, "import bootstrap_structures_schema", exc=str(e)))
        return results

    # Idempotência: chamar duas vezes não deve lançar erro
    try:
        import tempfile, os
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            tmp = Path(f.name)
        try:
            ensure_structures_schema(tmp)
            ensure_structures_schema(tmp)  # segunda chamada -- idempotente
            results.append(_ok(cat, "ensure_structures_schema idempotente"))
        finally:
            os.unlink(tmp)
    except Exception as e:
        results.append(_fail(cat, "ensure_structures_schema idempotente", exc=str(e)))

    return results


# ---------------------------------------------------------------------------
# Categoria 6: Scripts e relatórios de auditoria anteriores
# ---------------------------------------------------------------------------

def check_audit_artifacts() -> list[CheckResult]:
    results = []
    cat = "audit_artifacts"

    scripts_esperados = [
        "scripts/audit_legacy_residuals_patch52.py",
        "scripts/74_audit_public_api_aba_surface.py",
    ]
    for rel in scripts_esperados:
        p = PROJECT_ROOT / rel
        if p.exists():
            results.append(_ok(cat, f"script {rel} presente"))
        else:
            results.append(_warn(cat, f"script {rel} presente", "não encontrado"))

    reports_esperados = [
        "ATT/reports/legacy_residuals_patch52.md",
        "ATT/reports/legacy_residuals_patch52.json",
    ]
    for rel in reports_esperados:
        p = PROJECT_ROOT / rel
        if p.exists():
            sz = p.stat().st_size
            results.append(_ok(cat, f"report {rel} presente", f"{sz} bytes"))
        else:
            results.append(_warn(cat, f"report {rel} presente",
                                 "não encontrado (execute patch_52 para gerar)"))

    # Diretório ATT/reports gravável
    try:
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        probe = REPORTS_DIR / ".write_probe"
        probe.write_text("ok")
        probe.unlink()
        results.append(_ok(cat, "ATT/reports/ gravável"))
    except Exception as e:
        results.append(_fail(cat, "ATT/reports/ gravável", exc=str(e)))

    return results


# ---------------------------------------------------------------------------
# Categoria 7: patches ATT registrados
# ---------------------------------------------------------------------------

def check_att_patches() -> list[CheckResult]:
    results = []
    cat = "att_patches"

    patches_dir = PROJECT_ROOT / "ATT" / "patches"
    if not patches_dir.exists():
        results.append(_warn(cat, "ATT/patches/ existe", "diretório não encontrado"))
        return results

    results.append(_ok(cat, "ATT/patches/ existe"))

    patch_files = sorted(patches_dir.glob("patch_*.py"))
    results.append(_ok(cat, "patches registrados", f"{len(patch_files)} arquivo(s)"))

    # Verifica os dois últimos patches como sanidade
    for recent in ["patch_65", "patch_66"]:
        matches = [p for p in patch_files if recent in p.name]
        if matches:
            results.append(_ok(cat, f"{recent} presente", matches[0].name))
        else:
            results.append(_warn(cat, f"{recent} presente", "não encontrado"))

    return results


# ---------------------------------------------------------------------------
# Runner principal
# ---------------------------------------------------------------------------

def run_audit() -> AuditReport:
    report = AuditReport(
        gerado_em=datetime.now().isoformat(timespec="seconds"),
        raiz=str(PROJECT_ROOT),
    )

    checkers = [
        check_databases,
        check_structures_repository,
        check_derived_repo,
        check_derived_service,
        check_bootstrap_schema,
        check_audit_artifacts,
        check_att_patches,
    ]

    for checker in checkers:
        try:
            partial = checker()
        except Exception as e:
            partial = [_fail(
                checker.__name__, "execução do checker",
                exc=traceback.format_exc(),
            )]
        for r in partial:
            if r.status == "OK":
                report.total_ok += 1
            elif r.status == "WARN":
                report.total_warn += 1
            else:
                report.total_fail += 1
            report.checks.append(asdict(r))

    return report


# ---------------------------------------------------------------------------
# Geração de saídas
# ---------------------------------------------------------------------------

def _status_emoji(s: str) -> str:
    return {"OK": "✅", "WARN": "⚠️", "FAIL": "❌"}.get(s, "?")


def gerar_markdown(report: AuditReport, destino: Path) -> None:
    linhas = [
        "# patch_67 — Auditoria Baseline Fase 8",
        "",
        f"**Gerado em:** {report.gerado_em}  ",
        f"**Raiz:** `{report.raiz}`  ",
        "",
        "## Resumo",
        "",
        "| Status | Quantidade |",
        "|--------|------------|",
        f"| ✅ OK   | {report.total_ok} |",
        f"| ⚠️ WARN | {report.total_warn} |",
        f"| ❌ FAIL | {report.total_fail} |",
        f"| **Total** | **{report.total_ok + report.total_warn + report.total_fail}** |",
        "",
        "## Resultado por categoria",
        "",
    ]

    # Agrupa por categoria
    por_cat: dict[str, list[dict]] = {}
    for c in report.checks:
        por_cat.setdefault(c["categoria"], []).append(c)

    for cat, checks in por_cat.items():
        n_ok   = sum(1 for c in checks if c["status"] == "OK")
        n_warn = sum(1 for c in checks if c["status"] == "WARN")
        n_fail = sum(1 for c in checks if c["status"] == "FAIL")
        linhas += [
            f"### {cat}  ✅{n_ok} ⚠️{n_warn} ❌{n_fail}",
            "",
            "| Status | Check | Detalhe |",
            "|--------|-------|---------|",
        ]
        for c in checks:
            emoji   = _status_emoji(c["status"])
            detalhe = c["detalhe"] or ""
            if c["exc"]:
                detalhe += f" — `{c['exc'][:120]}`"
            linhas.append(
                f"| {emoji} | {c['check']} | {detalhe} |"
            )
        linhas.append("")

    # FAILs consolidados no final
    fails = [c for c in report.checks if c["status"] == "FAIL"]
    if fails:
        linhas += [
            "---",
            "",
            "## ❌ Itens com FAIL (consolidado)",
            "",
        ]
        for c in fails:
            linhas.append(f"- **[{c['categoria']}]** `{c['check']}`")
            if c["detalhe"]:
                linhas.append(f"  - detalhe: {c['detalhe']}")
            if c["exc"]:
                linhas.append(f"  - exc: `{c['exc'][:200]}`")
        linhas.append("")

    linhas += [
        "---",
        "",
        "_Gerado por scripts/75_audit_fase8_baseline.py — patch_67_",
    ]

    destino.write_text("\n".join(linhas), encoding="utf-8")


def gerar_json(report: AuditReport, destino: Path) -> None:
    destino.write_text(
        json.dumps(asdict(report), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Ponto de entrada
# ---------------------------------------------------------------------------

def main() -> int:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    print("patch_67 — auditoria baseline fase 8...")
    print(f"raiz: {PROJECT_ROOT}")

    report = run_audit()

    md_path   = REPORTS_DIR / "fase8_baseline.md"
    json_path = REPORTS_DIR / "fase8_baseline.json"

    gerar_markdown(report, md_path)
    gerar_json(report, json_path)

    print(f"✅  OK   : {report.total_ok}")
    print(f"⚠️  WARN : {report.total_warn}")
    print(f"❌  FAIL : {report.total_fail}")
    print(f"relatório md   : {md_path}")
    print(f"relatório json : {json_path}")

    return 0 if report.total_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
