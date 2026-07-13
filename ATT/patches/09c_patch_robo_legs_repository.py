from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TARGET = PROJECT_ROOT / "repositories" / "robo_legs_repository.py"


HELPERS = '''
    @staticmethod
    def _parse_float(value):
        if value is None:
            return None
        if isinstance(value, (int, float)):
            return float(value)

        s = str(value).strip()
        if not s:
            return None

        try:
            if "," in s:
                s = s.replace(".", "").replace(",", ".")
            return float(s)
        except ValueError:
            return None

    @staticmethod
    def _parse_int(value):
        if value is None:
            return None
        if isinstance(value, int):
            return value
        if isinstance(value, float):
            return int(value)

        s = str(value).strip()
        if not s:
            return None

        try:
            if "," in s:
                s = s.replace(".", "").replace(",", ".")
            return int(float(s))
        except ValueError:
            return None
'''


def fail(msg: str) -> int:
    print(f"ERRO: {msg}")
    return 1


def main() -> int:
    print("== PATCH ROBO LEGS REPOSITORY ==")
    print(f"PROJECT_ROOT: {PROJECT_ROOT}")
    print(f"TARGET: {TARGET}")

    if not TARGET.exists():
        return fail(f"Arquivo não encontrado: {TARGET}")

    original = TARGET.read_text(encoding="utf-8")
    patched = original

    changed = False

    # 1) Inserir helpers na classe, se ainda não existirem
    if "_parse_float" not in patched and "_parse_int" not in patched:
        class_match = re.search(
            r"(?m)^class\s+RoboLegsRepository\b.*:\s*$",
            patched,
        )
        if not class_match:
            return fail("Não foi possível localizar a classe RoboLegsRepository.")

        insert_pos = class_match.end()
        patched = patched[:insert_pos] + "\n" + HELPERS + patched[insert_pos:]
        changed = True
        print("- Helpers _parse_float/_parse_int inseridos.")
    else:
        print("- Helpers já existem, não serão inseridos.")

    # 2) Substituir parsing frágil de strike
    new_patched = re.sub(
        r"strike\s*=\s*float\(strike\)\s*if\s*strike\s*is\s*not\s*None\s*else\s*0\.0",
        "strike=self._parse_float(strike) if self._parse_float(strike) is not None else 0.0",
        patched,
    )
    if new_patched != patched:
        patched = new_patched
        changed = True
        print("- Parsing de strike atualizado.")
    else:
        print("- Nenhum trecho exato de strike encontrado para substituição.")

    # 3) Substituir parsing frágil de quant
    new_patched = re.sub(
        r"quant\s*=\s*int\(quant\)\s*if\s*quant\s*is\s*not\s*None\s*else\s*0",
        "quant=self._parse_int(quant) if self._parse_int(quant) is not None else 0",
        patched,
    )
    if new_patched != patched:
        patched = new_patched
        changed = True
        print("- Parsing de quant atualizado.")
    else:
        print("- Nenhum trecho exato de quant encontrado para substituição.")

    if not changed:
        print("Nenhuma alteração necessária.")
        return 0

    backup = TARGET.with_suffix(TARGET.suffix + ".bak")
    shutil.copy2(TARGET, backup)
    print(f"- Backup criado em: {backup}")

    TARGET.write_text(patched, encoding="utf-8")
    print("- Patch aplicado com sucesso.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
