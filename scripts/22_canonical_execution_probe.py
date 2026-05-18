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


def load_symbol(module_name: str, symbol_name: str):
    try:
        mod = importlib.import_module(module_name)
        obj = getattr(mod, symbol_name)
        ok(f"carregado: {module_name}.{symbol_name}")
        return obj
    except Exception as exc:
        fail(f"falha ao carregar {module_name}.{symbol_name}: {type(exc).__name__}: {exc}")
        return None


def format_signature(obj) -> str:
    try:
        return str(inspect.signature(obj))
    except Exception:
        return "(assinatura indisponível)"


def instantiate_if_possible(cls):
    try:
        sig = inspect.signature(cls)
        required = []
        for p in sig.parameters.values():
            if p.name == "self":
                continue
            if p.default is inspect._empty and p.kind in (
                inspect.Parameter.POSITIONAL_ONLY,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                inspect.Parameter.KEYWORD_ONLY,
            ):
                required.append(p.name)

        if required:
            warn(f"{cls.__name__} exige dependências: {required}")
            return None

        instance = cls()
        ok(f"instanciado: {cls.__name__}")
        return instance
    except Exception as exc:
        fail(f"falha ao instanciar {cls.__name__}: {type(exc).__name__}: {exc}")
        return None


def probe_method(instance, method_name: str, sample_kwargs: dict[str, Any] | None = None):
    sample_kwargs = sample_kwargs or {}
    if not hasattr(instance, method_name):
        warn(f"método ausente: {instance.__class__.__name__}.{method_name}")
        return

    method = getattr(instance, method_name)
    sig = format_signature(method)
    ok(f"assinatura {instance.__class__.__name__}.{method_name}{sig}")

    try:
        result = method(**sample_kwargs)
        ok(f"chamada ok: {instance.__class__.__name__}.{method_name}")
        preview = repr(result)
        if len(preview) > 300:
            preview = preview[:300] + "..."
        print(f"     retorno: {preview}")
    except TypeError as exc:
        warn(f"TypeError em {instance.__class__.__name__}.{method_name}: {exc}")
    except Exception as exc:
        warn(f"execução interrompida em {instance.__class__.__name__}.{method_name}: {type(exc).__name__}: {exc}")


def main() -> None:
    section("1) CARREGAMENTO DAS CLASSES")
    CanonicalInputService = load_symbol("services.canonical_input_service", "CanonicalInputService")
    PricingInputService = load_symbol("services.pricing_input_service", "PricingInputService")
    PricingExecutionOrchestrationService = load_symbol(
        "services.pricing_execution_orchestration_service",
        "PricingExecutionOrchestrationService",
    )
    PricingExecutionAppService = load_symbol(
        "services.pricing_execution_app_service",
        "PricingExecutionAppService",
    )
    StructuresRepository = load_symbol("repositories.structures_repository", "StructuresRepository")

    classes = [
        CanonicalInputService,
        PricingInputService,
        PricingExecutionOrchestrationService,
        PricingExecutionAppService,
        StructuresRepository,
    ]

    section("2) ASSINATURAS DOS CONSTRUTORES")
    instances: dict[str, Any] = {}
    for cls in classes:
        if cls is None:
            continue
        ok(f"construtor {cls.__name__}{format_signature(cls)}")
        instance = instantiate_if_possible(cls)
        if instance is not None:
            instances[cls.__name__] = instance

    section("3) PROBE DOS MÉTODOS PRINCIPAIS")
    cis = instances.get("CanonicalInputService")
    if cis:
        probe_method(cis, "build_structure_market_input")
        probe_method(cis, "_select_legacy_timestamp")

    pis = instances.get("PricingInputService")
    if pis:
        probe_method(pis, "build_pricing_payload")
        probe_method(pis, "build_pricing_payload_from_canonical_input")

    peos = instances.get("PricingExecutionOrchestrationService")
    if peos:
        probe_method(peos, "execute_and_persist")

    peas = instances.get("PricingExecutionAppService")
    if peas:
        probe_method(peas, "execute_pricing")
        probe_method(peas, "get_latest_execution_summary")
        probe_method(peas, "list_execution_summaries")
        probe_method(peas, "paginate_execution_summaries")

    repo = instances.get("StructuresRepository")
    if repo:
        probe_method(repo, "list_structures")
        probe_method(repo, "get_structure")

    section("4) AMOSTRAS MÍNIMAS CONTROLADAS")
    if cis:
        sample = {
            "structure_id": 1,
        }
        warn(f"tentando CanonicalInputService.build_structure_market_input com {json.dumps(sample)}")
        probe_method(cis, "build_structure_market_input", sample)

    if repo:
        sample = {
            "structure_id": 1,
        }
        warn(f"tentando StructuresRepository.get_structure com {json.dumps(sample)}")
        probe_method(repo, "get_structure", sample)

    section("5) FECHAMENTO")
    print("- Este probe não quer validar regra de negócio final.")
    print("- Ele quer descobrir contratos reais e dependências implícitas.")
    print("- Se aparecer exigência de aba/timestamp/reference_date, o acoplamento legado estará objetivamente exposto.")


if __name__ == "__main__":
    main()
