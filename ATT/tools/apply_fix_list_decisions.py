from __future__ import annotations

from pathlib import Path
import re
import sys

path = Path("services/terminal_vwap_payoff_app_service.py")

if not path.exists():
    raise SystemExit(f"Arquivo não encontrado: {path}")

source = path.read_text(encoding="utf-8")

old = '''        return self._call_first_available(
            self.decision_repository,
            "list_decisions",
            structure_id=structure_id,
            limit=limit,
        ) or []
'''

new = '''        return self._call_first_available(
            self.decision_repository,
            method_names=(
                "list_decisions",
            ),
            call_variants=(
                lambda method: method(
                    structure_id=structure_id,
                    limit=limit,
                ),
                lambda method: method(
                    structure_id,
                    limit,
                ),
                lambda method: method(limit=limit),
                lambda method: method(),
            ),
            default=[],
        ) or []
'''

expected_signature = (
    r"def _call_first_available\(\s*self,\s*target,\s*method_names,\s*"
    r"call_variants,\s*default\s*\)"
)

if not re.search(expected_signature, source):
    raise SystemExit(
        "Assinatura inesperada de _call_first_available. "
        "Patch cancelado para evitar alteração indevida."
    )

if new in source:
    print(f"Sem alteração: {path} já possui o contrato corrigido.")
elif old in source:
    path.write_text(source.replace(old, new, 1), encoding="utf-8")
    print(f"Corrigido: {path}")
else:
    raise SystemExit(
        "Bloco esperado de list_decisions() não encontrado. "
        "Patch cancelado para evitar alteração indevida."
    )
