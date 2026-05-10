from __future__ import annotations

import re
import sys
from pathlib import Path

FILE = Path("UI/components/details_panel.py")

# Corpo da função SEM indent inicial; o script adiciona indent certo automaticamente.
FUNC_SRC = """def _get_latest_snapshot_timestamp_for_aba(self, aba: str) -> str | None:
\"\"\"
Timestamp canônico por aba para dedupe de recálculo.

Regra:
  1) Se manual_analise_robo_legs existir e tiver linhas para a aba, usa MAX(timestamp) do manual
  2) Senão, usa MAX(timestamp) do rtd_analise_robo_legs (se existir)
  3) Por fim, tenta snapshots (robo_legs_snapshot / robo_snapshot) se existirem
\"\"\"
import sqlite3

db_path = self._raw_db_path()
if not db_path.exists():
    return None

con = sqlite3.connect(str(db_path))
try:
    cur = con.cursor()

    def has_table(name: str) -> bool:
        cur.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name=? LIMIT 1",
            (name,),
        )
        return cur.fetchone() is not None

    # 1) Manual domina se tiver dados para a aba
    if has_table("manual_analise_robo_legs"):
        cur.execute(
            "SELECT 1 FROM manual_analise_robo_legs WHERE aba=? LIMIT 1",
            (aba,),
        )
        if cur.fetchone() is not None:
            cur.execute(
                "SELECT MAX(timestamp) FROM manual_analise_robo_legs WHERE aba=?",
                (aba,),
            )
            row = cur.fetchone()
            if row and row[0]:
                return str(row[0])

    # 2) Fallback RTD
    if has_table("rtd_analise_robo_legs"):
        cur.execute(
            "SELECT MAX(timestamp) FROM rtd_analise_robo_legs WHERE aba=?",
            (aba,),
        )
        row = cur.fetchone()
        if row and row[0]:
            return str(row[0])

    # 3) Snapshots (se existirem)
    for tname in ("robo_legs_snapshot", "robo_snapshot"):
        if has_table(tname):
            cur.execute(f"SELECT MAX(timestamp) FROM {tname} WHERE aba=?", (aba,))
            row = cur.fetchone()
            if row and row[0]:
                return str(row[0])

    return None
finally:
    con.close()
"""

def indent_block(src: str, base: str) -> list[str]:
    # normaliza para linhas sem trailing whitespace
    raw = [ln.rstrip() for ln in src.splitlines()]
    # converte indent do template: 0, 4, 8... espaços (estilo Python)
    out: list[str] = []
    for ln in raw:
        if ln == "":
            out.append("\n")
            continue
        # conta indent em múltiplos de 4 no template
        m = re.match(r"^( *)", ln)
        nspaces = len(m.group(1)) if m else 0
        level = nspaces // 4
        out.append((base + (" " * 4 * level) + ln[nspaces:] + "\n"))
    return out

def main() -> int:
    if not FILE.exists():
        print(f"Arquivo não encontrado: {FILE}")
        return 2

    lines = FILE.read_text(encoding="utf-8", errors="replace").splitlines(True)

    # encontra a linha da def com indent base (geralmente 4 espaços)
    pat = re.compile(r"^(\s*)def _get_latest_snapshot_timestamp_for_aba\s*\(")
    starts = [(i, pat.match(lines[i]).group(1)) for i in range(len(lines)) if pat.match(lines[i])]
    if len(starts) != 1:
        print(f"Esperava 1 definição, encontrei {len(starts)}")
        return 3

    start_i, base_indent = starts[0]

    # fim: próxima def no mesmo nível de indent base
    end_i = len(lines)
    next_def = re.compile(rf"^{re.escape(base_indent)}def\s+\w+")
    for j in range(start_i + 1, len(lines)):
        if next_def.match(lines[j]):
            end_i = j
            break

    new_func_lines = indent_block(FUNC_SRC, base_indent)

    out = lines[:start_i] + new_func_lines + lines[end_i:]
    FILE.write_text("".join(out), encoding="utf-8")
    print(f"✅ Atualizado: {FILE}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
