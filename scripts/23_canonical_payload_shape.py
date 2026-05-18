#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from services.canonical_input_service import CanonicalInputService
from services.pricing_input_service import PricingInputService


def section(title: str) -> None:
    print()
    print("=" * 80)
    print(title)
    print("=" * 80)


def walk_shape(data: Any, level: int = 0, max_level: int = 2) -> None:
    indent = "  " * level

    if level > max_level:
        return

    if isinstance(data, dict):
        for k, v in data.items():
            print(f"{indent}- {k}: {type(v).__name__}")
            if isinstance(v, (dict, list)) and level < max_level:
                walk_shape(v, level + 1, max_level)
    elif isinstance(data, list):
        print(f"{indent}[list size={len(data)}]")
        if data and level < max_level:
            first = data[0]
            print(f"{indent}primeiro_item: {type(first).__name__}")
            walk_shape(first, level + 1, max_level)


def find_markers(data: Any, path: str = "") -> list[str]:
    found = []
    markers = {"aba", "timestamp", "alias_legacy_aba", "reference_date", "market_snapshot"}

    if isinstance(data, dict):
        for k, v in data.items():
            current = f"{path}.{k}" if path else k
            if k in markers:
                found.append(current)
            found.extend(find_markers(v, current))
    elif isinstance(data, list):
        for i, item in enumerate(data):
            current = f"{path}[{i}]"
            found.extend(find_markers(item, current))

    return found


def preview(data: Any, limit: int = 2000) -> str:
    text = json.dumps(data, ensure_ascii=False, indent=2, default=str)
    if len(text) > limit:
        return text[:limit] + "\n... [truncated]"
    return text


def main() -> None:
    section("1) BUILD DO CANONICAL INPUT")
    cis = CanonicalInputService()
    payload = cis.build_structure_market_input(structure_id=1)
    print(preview(payload))

    section("2) SHAPE DO PAYLOAD CANÔNICO")
    walk_shape(payload)

    section("3) MARCADORES ENCONTRADOS")
    markers = find_markers(payload)
    if markers:
        for m in markers:
            print(f"- {m}")
    else:
        print("- nenhum marcador encontrado")

    section("4) BUILD DO PRICING PAYLOAD")
    pis = PricingInputService()
    pricing_payload = pis.build_pricing_payload(structure_id=1)
    print(preview(pricing_payload))

    section("5) SHAPE DO PRICING PAYLOAD")
    walk_shape(pricing_payload)

    section("6) MARCADORES NO PRICING PAYLOAD")
    markers = find_markers(pricing_payload)
    if markers:
        for m in markers:
            print(f"- {m}")
    else:
        print("- nenhum marcador encontrado")


if __name__ == "__main__":
    main()
