from __future__ import annotations

import re
import sys
from pathlib import Path

FILE = Path("UI/components/details_panel.py")

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
    raw = [ln.rstrip() for ln in src.splitlines()]
    out: list[str] = []
    for ln in raw:
        if ln == "":
            out.append("\n")
            continue
        m = re.match(r"^( *)", ln)
        nspaces = len(m.group(1)) if m else 0
        level = nspaces // 4
        out.append(base + (" " * 4 * level) + ln[nspaces:] + "\n")
    return out

def find_def_blocks(lines: list[str], func_name: str) -> list[tuple[int,int,str]]:
    # retorna lista de (start, end, base_indent)
    pat = re.compile(rf"^(\s*)def {re.escape(func_name)}\s*\(")
    matches = [(i, pat.match(lines[i]).group(1)) for i in range(len(lines)) if pat.match(lines[i])]
    blocks: list[tuple[int,int,str]] = []
    for start, base in matches:
        end = len(lines)
        next_def_same_indent = re.compile(rf"^{re.escape(base)}def\s+\w+")
        for j in range(start + 1, len(lines)):
            if next_def_same_indent.match(lines[j]):
                end = j
                break
        blocks.append((start, end, base))
    # ordenar por start
    blocks.sort(key=lambda x: x[0])
    return blocks

def main() -> int:
    if not FILE.exists():
        print(f"Arquivo não encontrado: {FILE}")
        return 2

    lines = FILE.read_text(encoding="utf-8", errors="replace").splitlines(True)

    blocks = find_def_blocks(lines, "_get_latest_snapshot_timestamp_for_aba")
    if len(blocks) == 0:
        print("Não encontrei a função alvo no arquivo.")
        return 3

    print(f"Encontradas {len(blocks)} definições; vou manter 1 e remover o resto.")

    # manter a primeira
    keep_start, keep_end, base_indent = blocks[0]
    new_func_lines = indent_block(FUNC_SRC, base_indent)

    # remover todas as outras ocorrências (de trás pra frente para não bagunçar índices)
    out = lines[:]
    for start, end, _ in reversed(blocks[1:]):
        del out[start:end]

    # após deletar, precisamos recalcular posição do bloco mantido (pode ter mudado se existia bloco antes dele - não existe, pois é o primeiro)
    # substitui o bloco mantido pelo novo
    out = out[:keep_start] + new_func_lines + out[keep_end:]

    FILE.write_text("".join(out), encoding="utf-8")
    print(f"✅ Atualizado: {FILE}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
