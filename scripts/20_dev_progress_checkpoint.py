#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import ast
import sqlite3
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]


def ok(msg: str) -> None:
    print(f"[OK] {msg}")


def warn(msg: str) -> None:
    print(f"[WARN] {msg}")


def fail(msg: str) -> None:
    print(f"[FAIL] {msg}")


def section(title: str) -> None:
    print()
    print("=" * 80)
    print(title)
    print("=" * 80)


def resolve(rel_path: str) -> Path:
    return ROOT / rel_path


def file_exists(rel_path: str) -> bool:
    path = resolve(rel_path)
    if path.exists():
        ok(f"arquivo existe: {rel_path}")
        return True
    fail(f"arquivo ausente: {rel_path}")
    return False


def parse_python(rel_path: str):
    path = resolve(rel_path)
    if not path.exists():
        return None
    try:
        return ast.parse(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"erro ao fazer parse de {rel_path}: {exc}")
        return None


def has_class(rel_path: str, class_name: str) -> bool:
    tree = parse_python(rel_path)
    if tree is None:
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            ok(f"class encontrada: {class_name} em {rel_path}")
            return True
    fail(f"class não encontrada: {class_name} em {rel_path}")
    return False


def has_function(rel_path: str, func_name: str) -> bool:
    tree = parse_python(rel_path)
    if tree is None:
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            ok(f"função encontrada: {func_name} em {rel_path}")
            return True
    fail(f"função não encontrada: {func_name} em {rel_path}")
    return False


def has_any_string(rel_path: str, patterns: Iterable[str]) -> bool:
    path = resolve(rel_path)
    if not path.exists():
        fail(f"arquivo ausente para inspeção textual: {rel_path}")
        return False
    content = path.read_text(encoding="utf-8", errors="ignore")
    missing = [p for p in patterns if p not in content]
    if not missing:
        ok(f"padrões encontrados em {rel_path}: {', '.join(patterns)}")
        return True
    fail(f"padrões ausentes em {rel_path}: {', '.join(missing)}")
    return False


def inspect_db(db_rel_path: str, expected_tables: list[str]) -> bool:
    db_path = resolve(db_rel_path)
    if not db_path.exists():
        fail(f"banco ausente: {db_rel_path}")
        return False

    try:
        conn = sqlite3.connect(db_path)
        rows = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
        conn.close()
        tables = {row[0] for row in rows}
    except Exception as exc:
        fail(f"erro ao inspecionar banco {db_rel_path}: {exc}")
        return False

    all_ok = True
    for table in expected_tables:
        if table in tables:
            ok(f"tabela encontrada em {db_rel_path}: {table}")
        else:
            fail(f"tabela ausente em {db_rel_path}: {table}")
            all_ok = False
    return all_ok


def summarize_stage(results: dict[str, bool]) -> None:
    section("RESUMO DE ANDAMENTO")

    phase1 = results.get("db_raw", False) and results.get("legacy_repo", False)
    phase2 = results.get("schema_structures", False) and results.get("repo_structures", False)
    phase3a_base = (
        results.get("canonical_services", False)
        and results.get("pricing_services", False)
        and results.get("pricing_api", False)
    )
    legacy_alive = results.get("legacy_domain", False)

    if phase1:
        ok("Fase 1: auditoria/base legada aparenta estar presente")
    else:
        warn("Fase 1: há lacunas na base legada/auditoria")

    if phase2:
        ok("Fase 2: modelo canônico de estruturas aparenta estar implementado")
    else:
        warn("Fase 2: modelo canônico de estruturas ainda incompleto")

    if phase3a_base:
        ok("Fase 3A: base de pipeline canônico e pricing execution aparenta existir")
    else:
        warn("Fase 3A: pipeline canônico/pricing execution ainda incompleto")

    if legacy_alive:
        warn("Legado ainda está vivo em domínio/serviços centrais (esperado nesta etapa)")
    else:
        ok("Legado por aba parece reduzido ou ausente")

    print()
    if phase2 and phase3a_base and legacy_alive:
        print("Conclusão: o projeto parece em transição controlada.")
        print("Há base canônica pronta, mas o legado ainda convive com o fluxo novo.")
        print("Próximo foco: consolidar o caminho funcional do 3A, sem ir ainda para UI final.")
    elif phase2 and not phase3a_base:
        print("Conclusão: estruturas canônicas avançaram, mas a integração funcional ainda está atrás.")
    else:
        print("Conclusão: ainda há lacunas estruturais antes de avançar para integração maior.")


def main() -> None:
    results: dict[str, bool] = {}

    section("1) BANCOS E TABELAS PRINCIPAIS")
    results["db_raw"] = inspect_db(
        "dados/app.db",
        [
            "rtd_analise_robo",
            "rtd_analise_robo_legs",
            "manual_analise_robo_legs",
        ],
    )
    inspect_db(
        "dados/derived.db",
        [],
    )

    section("2) SCHEMA CANÔNICO DE ESTRUTURAS")
    a = file_exists("infra/bootstrap_structures_schema.py")
    b = has_function("infra/bootstrap_structures_schema.py", "ensure_structures_schema")
    results["schema_structures"] = a and b

    section("3) REPOSITÓRIO CANÔNICO DE ESTRUTURAS")
    a = file_exists("repositories/structures_repository.py")
    b = has_class("repositories/structures_repository.py", "StructuresRepository")
    c = has_function("repositories/structures_repository.py", "_validate_leg")
    d = has_any_string(
        "repositories/structures_repository.py",
        [
            "create_structure",
            "add_leg",
            "get_structure",
            "list_structures",
            "update_structure",
            "replace_legs",
            "archive_structure",
        ],
    )
    results["repo_structures"] = a and b and c and d

    section("4) SMOKE DE CRUD DE ESTRUTURAS")
    results["smoke_structures"] = file_exists("scripts/10_smoke_structures_repository.py")

    section("5) SERVIÇOS DO PIPELINE CANÔNICO")
    canonical_files = [
        "services/structure_input_mapper.py",
        "services/structure_market_input_assembler.py",
        "services/market_snapshot_provider.py",
        "services/canonical_input_service.py",
        "services/pricing_input_service.py",
        "services/pricing_payload_adapter.py",
    ]
    canonical_ok = True
    for rel in canonical_files:
        canonical_ok = file_exists(rel) and canonical_ok
    results["canonical_services"] = canonical_ok

    section("6) SERVIÇOS DE PRICING EXECUTION")
    pricing_files = [
        "services/pricing_execution_service.py",
        "services/pricing_execution_persistence_service.py",
        "services/pricing_execution_query_service.py",
        "services/pricing_execution_orchestration_service.py",
        "services/pricing_execution_app_service.py",
        "repositories/pricing_executions_repository.py",
    ]
    pricing_ok = True
    for rel in pricing_files:
        pricing_ok = file_exists(rel) and pricing_ok
    results["pricing_services"] = pricing_ok

    section("7) API DE PRICING EXECUTION")
    a = file_exists("api/pricing_execution_controller.py")
    b = has_any_string(
        "api/pricing_execution_controller.py",
        [
            "/pricing-executions",
            "latest",
        ],
    )
    results["pricing_api"] = a and b

    section("8) LEGADO AINDA ACOPLADO")
    legacy_files = [
        "services/derived_service.py",
        "services/robo_legs_service.py",
        "services/robo_legs_status_service.py",
        "repositories/robo_legs_repository.py",
        "repositories/robo_legs_status_repository.py",
        "domain/payoff.py",
        "domain/decision.py",
    ]
    legacy_ok = True
    for rel in legacy_files:
        legacy_ok = file_exists(rel) and legacy_ok
    results["legacy_domain"] = legacy_ok
    results["legacy_repo"] = file_exists("repositories/robo_legs_repository.py")

    summarize_stage(results)


if __name__ == "__main__":
    main()
