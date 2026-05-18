#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from services.pricing_execution_app_service import PricingExecutionAppService
from repositories.structures_repository import StructuresRepository


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


def preview(data, limit: int = 3000) -> str:
    text = json.dumps(data, ensure_ascii=False, indent=2, default=str)
    if len(text) > limit:
        return text[:limit] + "\n... [truncated]"
    return text


def choose_structure_id() -> int | None:
    repo = StructuresRepository()
    structures = repo.list_structures(include_archived=False)

    if not structures:
        warn("nenhuma estrutura ativa encontrada; tentando qualquer estrutura")
        structures = repo.list_structures(include_archived=True)

    if not structures:
        fail("nenhuma estrutura encontrada no repositório")
        return None

    chosen = structures[0]
    structure_id = chosen["id"]
    ok(
        f"estrutura escolhida: id={structure_id}, "
        f"name={chosen.get('name')}, "
        f"underlying={chosen.get('underlying_asset')}, "
        f"status={chosen.get('status')}"
    )
    return structure_id


def main() -> None:
    section("1) ESCOLHA DA ESTRUTURA")
    structure_id = choose_structure_id()
    if structure_id is None:
        raise SystemExit(1)

    section("2) EXECUÇÃO DO PRICING")
    app = PricingExecutionAppService()

    try:
        result = app.execute_pricing(structure_id=structure_id)
        ok("execute_pricing executado com sucesso")
        print(preview(result))
    except Exception as exc:
        fail(f"execute_pricing falhou: {type(exc).__name__}: {exc}")
        raise SystemExit(2)

    section("3) CONSULTA DO ÚLTIMO RESULTADO")
    try:
        latest = app.get_latest_execution_summary(structure_id=structure_id)
        ok("get_latest_execution_summary executado com sucesso")
        print(preview(latest))
    except Exception as exc:
        fail(f"consulta do último resultado falhou: {type(exc).__name__}: {exc}")
        raise SystemExit(3)

    section("4) VALIDAÇÃO RÁPIDA")
    if isinstance(result, dict):
        if "structure_id" in result or "execution" in result or "id" in result:
            ok("retorno tem indícios de execução persistida")
        else:
            warn("retorno não mostrou identificadores esperados de execução")

    if isinstance(latest, dict):
        expected = ["structure_id", "reference_date", "execution_status"]
        present = [k for k in expected if k in latest]
        if present:
            ok(f"campos esperados presentes no latest: {', '.join(present)}")
        else:
            warn("latest não exibiu os campos esperados")

    print()
    print("Conclusão:")
    print("- Se este smoke passar, o fluxo principal já executa por structure_id ponta a ponta.")
    print("- Nesse caso, o restante vira limpeza de acoplamento residual, não bloqueio arquitetural.")


if __name__ == "__main__":
    main()
