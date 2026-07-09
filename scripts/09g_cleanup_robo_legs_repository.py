from __future__ import annotations

import re
import shutil
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TARGET = PROJECT_ROOT / "repositories" / "robo_legs_repository.py"


def fail(msg: str) -> int:
    print(f"ERRO: {msg}")
    return 1


def main() -> int:
    print("== CLEANUP ROBO LEGS REPOSITORY ==")
    print(f"PROJECT_ROOT: {PROJECT_ROOT}")
    print(f"TARGET: {TARGET}")

    if not TARGET.exists():
        return fail(f"Arquivo não encontrado: {TARGET}")

    original = TARGET.read_text(encoding="utf-8")
    patched = original

    # Inserir variáveis locais no início de _row_to_dto
    pattern_header = re.compile(
        r"(?ms)(def\s+_row_to_dto\s*\(self,\s*row:\s*sqlite3\.Row,\s*fonte:\s*FonteType\s*\)\s*->\s*RoboLegDTO:\s*\n\s*\"\"\".*?\"\"\"\s*\n)(\s+)(aba\s*=.*?\n\s*vencimento\s*=.*?\n)",
    )

    def repl_header(match: re.Match) -> str:
        prefix = match.group(1)
        indent = match.group(2)
        body = match.group(3)

        if "strike_parsed =" in body or "quant_parsed =" in body:
            return match.group(0)

        extra = (
            f"{indent}strike_parsed = self._parse_float(strike)\n"
            f"{indent}quant_parsed = self._parse_int(quant)\n"
        )
        return prefix + body + extra

    patched = pattern_header.sub(repl_header, patched, count=1)

    # Substituir chamadas duplicadas
    patched = patched.replace(
        "strike=self._parse_float(strike) if self._parse_float(strike) is not None else 0.0",
        "strike=strike_parsed if strike_parsed is not None else 0.0",
    )

    patched = patched.replace(
        "quant=self._parse_int(quant) if self._parse_int(quant) is not None else 0",
        "quant=quant_parsed if quant_parsed is not None else 0",
    )

    if patched == original:
        print("Nenhuma alteração necessária.")
        return 0

    backup = TARGET.with_suffix(TARGET.suffix + ".cleanup.bak")
    shutil.copy2(TARGET, backup)
    print(f"- Backup criado em: {backup}")

    TARGET.write_text(patched, encoding="utf-8")
    print("- Cleanup aplicado com sucesso.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
