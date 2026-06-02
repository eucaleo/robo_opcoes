#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import importlib
import inspect
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def section(title: str) -> None:
    print()
    print("=" * 80)
    print(title)
    print("=" * 80)


def ok(msg: str) -> None:
    print(f"[OK] {msg}")


def warn(msg: str) -> None:
    print(f"[WARN] {msg}")


def fail(msg: str) -> None:
    print(f"[FAIL] {msg}")


def preview(data: Any, limit: int = 2000) -> str:
    text = json.dumps(data, ensure_ascii=False, indent=2, default=str)
    if len(text) > limit:
        return text[:limit] + "\n... [truncated]"
    return text


def load_symbol(module_name: str, symbol_name: str):
    mod = importlib.import_module(module_name)
    return getattr(mod, symbol_name)


def has_param(callable_obj, param_name: str) -> bool:
    try:
        sig = inspect.signature(callable_obj)
        return param_name in sig.parameters
    except Exception:
        return False


def choose_structure_id():
    StructuresRepository = load_symbol("repositories.structures_repository", "StructuresRepository")
    repo = StructuresRepository()

    active = repo.list_structures(include_archived=False)
    if active:
        chosen = active[0]
        return chosen["id"], chosen

    all_items = repo.list_structures(include_archived=True)
    if all_items:
        chosen = all_items[0]
        return chosen["id"], chosen

    return None, None


def main() -> None:
    checks = []
    structure_id = None

    section("1) IMPORTS E CONTRATOS PÚBLICOS")
    try:
        CanonicalInputService = load_symbol("services.canonical_input_service", "CanonicalInputService")
        PricingInputService = load_symbol("services.pricing_input_service", "PricingInputService")
        PricingExecutionAppService = load_symbol(
            "services.pricing_execution_app_service",
            "PricingExecutionAppService",
        )
        StructuresRepository = load_symbol("repositories.structures_repository", "StructuresRepository")
        ok("imports principais carregados")
        checks.append(True)
    except Exception as exc:
        fail(f"falha nos imports principais: {type(exc).__name__}: {exc}")
        checks.append(False)
        raise SystemExit(1)

    try:
        cis = CanonicalInputService()
        pis = PricingInputService()
        app = PricingExecutionAppService()
        repo = StructuresRepository()
        ok("serviços principais instanciados")
        checks.append(True)
    except Exception as exc:
        fail(f"falha na instanciação: {type(exc).__name__}: {exc}")
        checks.append(False)
        raise SystemExit(1)

    public_contract_ok = True
    if has_param(cis.build_structure_market_input, "structure_id"):
        ok("CanonicalInputService.build_structure_market_input usa structure_id")
    else:
        fail("CanonicalInputService.build_structure_market_input não expõe structure_id")
        public_contract_ok = False

    if has_param(pis.build_pricing_payload, "structure_id"):
        ok("PricingInputService.build_pricing_payload usa structure_id")
    else:
        fail("PricingInputService.build_pricing_payload não expõe structure_id")
        public_contract_ok = False

    if has_param(app.execute_pricing, "structure_id"):
        ok("PricingExecutionAppService.execute_pricing usa structure_id")
    else:
        fail("PricingExecutionAppService.execute_pricing não expõe structure_id")
        public_contract_ok = False

    checks.append(public_contract_ok)

    section("2) ESCOLHA DE ESTRUTURA")
    try:
        structure_id, chosen = choose_structure_id()
        if structure_id is None:
            fail("nenhuma estrutura encontrada")
            checks.append(False)
            raise SystemExit(1)

        ok(
            f"estrutura escolhida: id={structure_id}, "
            f"name={chosen.get('name')}, "
            f"underlying={chosen.get('underlying_asset')}, "
            f"status={chosen.get('status')}"
        )
        checks.append(True)
    except Exception as exc:
        fail(f"falha ao escolher estrutura: {type(exc).__name__}: {exc}")
        checks.append(False)
        raise SystemExit(1)

    section("3) BUILD DO CANONICAL INPUT")
    try:
        canonical_input = cis.build_structure_market_input(structure_id=structure_id)
        ok("canonical input montado")

        if isinstance(canonical_input, dict) and all(
            key in canonical_input for key in ("structure", "market", "meta")
        ):
            ok("canonical input contém structure, market e meta")
            checks.append(True)
        else:
            warn("canonical input não contém todas as chaves esperadas")
            checks.append(False)

        print(preview(canonical_input))
    except Exception as exc:
        fail(f"falha ao montar canonical input: {type(exc).__name__}: {exc}")
        checks.append(False)

    section("4) BUILD DO PRICING PAYLOAD")
    try:
        pricing_payload = pis.build_pricing_payload(structure_id=structure_id)
        ok("pricing payload montado")

        expected_keys = ["structure_id", "underlying_asset", "reference_date", "legs"]
        present = [k for k in expected_keys if k in pricing_payload]
        if len(present) == len(expected_keys):
            ok("pricing payload contém campos essenciais")
            checks.append(True)
        else:
            warn(f"pricing payload incompleto; presentes: {present}")
            checks.append(False)

        print(preview(pricing_payload))
    except Exception as exc:
        fail(f"falha ao montar pricing payload: {type(exc).__name__}: {exc}")
        checks.append(False)

    section("5) EXECUÇÃO PONTA A PONTA")
    execution = None
    try:
        execution = app.execute_pricing(structure_id=structure_id)
        ok("execute_pricing executado com sucesso")

        if isinstance(execution, dict) and execution.get("structure_id") == structure_id:
            ok("execução retornou structure_id coerente")
            checks.append(True)
        else:
            warn("execução não retornou structure_id coerente")
            checks.append(False)

        print(preview(execution))
    except Exception as exc:
        fail(f"falha na execução ponta a ponta: {type(exc).__name__}: {exc}")
        checks.append(False)

    section("6) CONSULTA DA ÚLTIMA EXECUÇÃO")
    try:
        latest = app.get_latest_execution_summary(structure_id=structure_id)
        ok("consulta da última execução realizada")

        if isinstance(latest, dict) and latest.get("structure_id") == structure_id:
            ok("última execução consultada com sucesso")
            checks.append(True)
        else:
            warn("última execução não retornou structure_id esperado")
            checks.append(False)

        print(preview(latest))
    except Exception as exc:
        fail(f"falha ao consultar última execução: {type(exc).__name__}: {exc}")
        checks.append(False)

    section("7) RESULTADO FINAL DA FASE 3A")
    passed = sum(1 for item in checks if item)
    total = len(checks)

    print(f"Checks aprovados: {passed}/{total}")

    if passed == total:
        ok("FASE 3A ENCERRADA COM SUCESSO")
        print("- Contrato público principal está orientado por structure_id")
        print("- Canonical input está operacional")
        print("- Pricing payload está operacional")
        print("- Execução ponta a ponta está operacional")
        print("- Persistência e consulta de execução estão operacionais")
        print("- Resíduos legados restantes são cleanup técnico, não bloqueio funcional")
    else:
        warn("FASE 3A COM RESSALVAS")
        print("- O fluxo principal existe, mas um ou mais checks adicionais precisam revisão")

    print()
    print("Próximo passo recomendado:")
    print("- iniciar cleanup residual de alias/timestamp legado")
    print("- isolar derived_service como compatibilidade")
    print("- limpar decision.py")
    print("- evoluir execution_engine além do stub")


if __name__ == "__main__":
    main()
