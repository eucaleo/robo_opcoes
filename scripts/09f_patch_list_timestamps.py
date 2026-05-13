from __future__ import annotations

import re
import shutil
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TARGET = PROJECT_ROOT / "repositories" / "robo_legs_repository.py"


NEW_METHOD = '''
    def list_timestamps(self, aba: str, prefer: str = "manual_then_rtd") -> List[str]:
        """Lista timestamps disponíveis para a aba."""
        prefer = (prefer or "").strip().lower()

        with sqlite_conn(self.config.app_db_path) as conn:
            rows_m = conn.execute(
                "SELECT DISTINCT timestamp FROM manual_analise_robo_legs WHERE aba = ? ORDER BY timestamp",
                (aba,),
            ).fetchall()
            manual = [r["timestamp"] for r in rows_m]

            rows_r = conn.execute(
                "SELECT DISTINCT timestamp FROM rtd_analise_robo_legs WHERE aba = ? ORDER BY timestamp",
                (aba,),
            ).fetchall()
            rtd = [r["timestamp"] for r in rows_r]

        if prefer == "manual_only":
            return manual

        if prefer == "rtd_only":
            return rtd

        if prefer == "manual_then_rtd":
            return manual if manual else rtd

        if prefer == "all":
            return sorted(set(manual) | set(rtd))

        raise ValueError(
            "prefer must be one of: 'manual_then_rtd', 'manual_only', 'rtd_only', 'all'"
        )
'''


def fail(msg: str) -> int:
    print(f"ERRO: {msg}")
    return 1


def main() -> int:
    print("== PATCH LIST_TIMESTAMPS ==")
    print(f"PROJECT_ROOT: {PROJECT_ROOT}")
    print(f"TARGET: {TARGET}")

    if not TARGET.exists():
        return fail(f"Arquivo não encontrado: {TARGET}")

    original = TARGET.read_text(encoding="utf-8")

    pattern = re.compile(
        r"(?ms)^(\s*)def\s+list_timestamps\s*\(.*?\n(?=^\s*def\s+|^\s*@|^\s*class\s+|\Z)"
    )

    match = pattern.search(original)
    if not match:
        return fail("Método list_timestamps não encontrado.")

    start, end = match.span()
    patched = original[:start] + NEW_METHOD + "\n" + original[end:]

    if patched == original:
        print("Nenhuma alteração necessária.")
        return 0

    backup = TARGET.with_suffix(TARGET.suffix + ".list_timestamps.bak")
    shutil.copy2(TARGET, backup)
    print(f"- Backup criado em: {backup}")

    TARGET.write_text(patched, encoding="utf-8")
    print("- Método list_timestamps atualizado com sucesso.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
