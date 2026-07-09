from __future__ import annotations
import re
from pathlib import Path

FILE = Path("UI/components/details_panel.py")
FUNC = "_get_latest_snapshot_timestamp_for_aba"

def main() -> int:
    s = FILE.read_text(encoding="utf-8", errors="replace").splitlines(True)

    # acha todas as defs
    def_pat = re.compile(rf"^(\s*)def {re.escape(FUNC)}\s*\(")
    starts = []
    for i, ln in enumerate(s):
        m = def_pat.match(ln)
        if m:
            starts.append((i, m.group(1)))

    if not starts:
        print("Não encontrei a função alvo.")
        return 2

    # para cada ocorrência, reindentar o corpo (linhas até próxima def no mesmo indent)
    for start, base in starts:
        end = len(s)
        next_def = re.compile(rf"^{re.escape(base)}def\s+\w+")
        for j in range(start + 1, len(s)):
            if next_def.match(s[j]):
                end = j
                break

        body_start = start + 1
        if body_start >= end:
            continue

        # indent esperado do corpo = base + 4 espaços
        want = base + " " * 4

        # se a primeira linha do corpo já tem want, não mexe
        if s[body_start].startswith(want) or s[body_start].strip() == "":
            continue

        # reindenta TODAS as linhas do corpo que estejam no nível "base"
        for k in range(body_start, end):
            ln = s[k]
            if ln.strip() == "":
                continue
            # se a linha começa exatamente com base e NÃO com want, empurra 4 espaços
            if ln.startswith(base) and not ln.startswith(want):
                s[k] = want + ln[len(base):]

    FILE.write_text("".join(s), encoding="utf-8")
    print(f"✅ Indent corrigido para {len(starts)} ocorrência(s) em {FILE}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
