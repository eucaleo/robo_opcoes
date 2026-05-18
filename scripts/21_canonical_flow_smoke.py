#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import importlib
import inspect
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


def try_import(module_name: str):
    try:
        mod = importlib.import_module(module_name)
        ok(f"import ok: {module_name}")
        return mod
    except Exception as exc:
        fail(f"import falhou: {module_name} -> {type(exc).__name__}: {exc}")
        return None


def find_classes(mod) -> list[type]:
    return [
        obj for _, obj in inspect.getmembers(mod, inspect.isclass)
        if obj.__module__ == mod.__name__
    ]


def find_functions(mod) -> list[str]:
    return [
        name for name, obj in inspect.getmembers(mod, inspect.isfunction)
        if obj.__module__ == mod.__name__
    ]


def try_get_attr(mod, name: str):
    if hasattr(mod, name):
        ok(f"símbolo encontrado em {mod.__name__}: {name}")
        return getattr(mod, name)
    warn(f"símbolo não encontrado em {mod.__name__}: {name}")
    return None


def try_instantiate(cls):
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
            warn(f"não foi possível instanciar {cls.__name__} sem dependências: requer {required}")
            return None

        instance = cls()
        ok(f"instanciação ok: {cls.__name__}")
        return instance
    except Exception as exc:
        fail(f"instanciação falhou: {cls.__name__} -> {type(exc).__name__}: {exc}")
        return None


def describe_module(module_name: str, expected_symbols: list[str]) -> dict[str, Any]:
    mod = try_import(module_name)
    result = {
        "module": module_name,
        "imported": mod is not None,
        "symbols": {},
        "classes": [],
        "functions": [],
    }
    if mod is None:
        return result

    classes = find_classes(mod)
    funcs = find_functions(mod)
    result["classes"] = [c.__name__ for c in classes]
    result["functions"] = funcs

    if classes:
        ok(f"classes em {module_name}: {', '.join(result['classes'])}")
    else:
        warn(f"nenhuma class local encontrada em {module_name}")

    if funcs:
        ok(f"funções em {module_name}: {', '.join(funcs)}")
    else:
        warn(f"nenhuma função local encontrada em {module_name}")

    for symbol in expected_symbols:
        result["symbols"][symbol] = hasattr(mod, symbol)
        if hasattr(mod, symbol):
            ok(f"{module_name}.{symbol} disponível")
        else:
            warn(f"{module_name}.{symbol} ausente")

    return result


def main() -> None:
    results: dict[str, Any] = {}

    section("1) IMPORTS DOS MÓDULOS DO FLUXO CANÔNICO")
    module_expectations = {
        "services.structure_input_mapper": [],
        "services.structure_market_input_assembler": [],
        "services.market_snapshot_provider": [],
        "services.canonical_input_service": [],
        "services.pricing_input_service": [],
        "services.pricing_payload_adapter": [],
        "services.pricing_execution_service": [],
        "services.pricing_execution_persistence_service": [],
        "services.pricing_execution_query_service": [],
        "services.pricing_execution_orchestration_service": [],
        "services.pricing_execution_app_service": [],
        "repositories.structures_repository": ["StructuresRepository"],
        "repositories.pricing_executions_repository": [],
        "api.pricing_execution_controller": [],
    }

    for module_name, expected_symbols in module_expectations.items():
        results[module_name] = describe_module(module_name, expected_symbols)

    section("2) TENTATIVA DE DESCOBRIR CLASSES PRINCIPAIS")
    candidate_modules = [
        "services.canonical_input_service",
        "services.pricing_input_service",
        "services.pricing_payload_adapter",
        "services.pricing_execution_orchestration_service",
        "services.pricing_execution_app_service",
        "repositories.structures_repository",
    ]

    discovered_instances = {}

    for module_name in candidate_modules:
        mod = importlib.import_module(module_name)
        classes = find_classes(mod)
        if not classes:
            warn(f"sem classes para testar em {module_name}")
            continue

        for cls in classes:
            instance = try_instantiate(cls)
            discovered_instances[f"{module_name}.{cls.__name__}"] = instance is not None

    section("3) BUSCA DE MÉTODOS-CHAVE")
    method_hints = [
        "build",
        "assemble",
        "map_structure",
        "get_structure",
        "list_structures",
        "create_structure",
        "execute",
        "run",
        "process",
        "orchestrate",
        "latest",
    ]

    for module_name in candidate_modules:
        mod = importlib.import_module(module_name)
        classes = find_classes(mod)
        for cls in classes:
            methods = [
                name for name, obj in inspect.getmembers(cls, inspect.isfunction)
                if not name.startswith("__")
            ]
            if methods:
                ok(f"métodos em {module_name}.{cls.__name__}: {', '.join(methods)}")
                found = [m for m in method_hints if m in methods]
                if found:
                    ok(f"métodos-chave detectados em {cls.__name__}: {', '.join(found)}")
                else:
                    warn(f"nenhum método-chave padrão detectado em {cls.__name__}")
            else:
                warn(f"nenhum método público em {module_name}.{cls.__name__}")

    section("4) SINAIS DE ACOPLAMENTO LEGADO")
    legacy_markers = [
        "aba",
        "timestamp",
        "rtd_analise_robo_legs",
        "manual_analise_robo_legs",
    ]

    files_to_scan = [
        ROOT / "domain" / "payoff.py",
        ROOT / "domain" / "decision.py",
        ROOT / "services" / "derived_service.py",
        ROOT / "services" / "structure_analysis_service.py",
        ROOT / "services" / "canonical_input_service.py",
        ROOT / "services" / "pricing_execution_app_service.py",
    ]

    for path in files_to_scan:
        if not path.exists():
            warn(f"arquivo não encontrado para scan: {path.relative_to(ROOT)}")
            continue
        content = path.read_text(encoding="utf-8", errors="ignore")
        found = [marker for marker in legacy_markers if marker in content]
        if found:
            warn(f"marcadores legados em {path.relative_to(ROOT)}: {', '.join(found)}")
        else:
            ok(f"sem marcadores legados explícitos em {path.relative_to(ROOT)}")

    section("5) RESUMO")
    imported_ok = all(v["imported"] for v in results.values())
    if imported_ok:
        ok("todos os módulos principais importaram")
    else:
        warn("nem todos os módulos principais importaram")

    instantiable = [k for k, v in discovered_instances.items() if v]
    blocked = [k for k, v in discovered_instances.items() if not v]

    if instantiable:
        ok(f"classes instanciáveis sem dependências explícitas: {', '.join(instantiable)}")
    else:
        warn("nenhuma class principal foi instanciável sem dependências")

    if blocked:
        warn(f"classes que exigem wiring/dependências: {', '.join(blocked)}")

    print()
    print("Conclusão operacional:")
    print("- Se os imports passam, a base do 3A existe de forma executável.")
    print("- Se quase nada instancia sem argumento, falta wiring/composição explícita.")
    print("- Se payoff/decision/derived ainda exibem marcadores legados, o cálculo principal ainda não virou totalmente para o canônico.")
    print("- O próximo passo será montar um smoke com composição real, assim que tivermos as assinaturas dos serviços centrais.")


if __name__ == "__main__":
    main()
