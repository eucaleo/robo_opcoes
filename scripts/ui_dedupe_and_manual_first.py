from __future__ import annotations

import re
from pathlib import Path

P = Path("UI/components/details_panel.py")

MANUAL_FIRST_BODY = [
    '        """\n',
    '        Timestamp canônico por aba para dedupe de recálculo.\n',
    '\n',
    '        Regra:\n',
    '          1) Se manual_analise_robo_legs existir e tiver linhas para a aba, usa MAX(timestamp) do manual\n',
    '          2) Senão, usa MAX(timestamp) do rtd_analise_robo_legs (se existir)\n',
    '          3) Por fim, tenta snapshots (robo_legs_snapshot / robo_snapshot) se existirem\n',
    '        """\n',
    '        import sqlite3\n',
    '\n',
    '        db_path = self._raw_db_path()\n',
    '        if not db_path.exists():\n',
    '            return None\n',
    '\n',
    '        con = sqlite3.connect(str(db_path))\n',
    '        try:\n',
    '            cur = con.cursor()\n',
    '\n',
    '            def has_table(name: str) -> bool:\n',
    '                cur.execute(\n',
    '                    "SELECT 1 FROM sqlite_master WHERE type=\'table\' AND name=? LIMIT 1",\n',
    '                    (name,),\n',
    '                )\n',
    '                return cur.fetchone() is not None\n',
    '\n',
    '            # 1) Manual domina se tiver dados para a aba\n',
    '            if has_table("manual_analise_robo_legs"):\n',
    '                cur.execute(\n',
    '                    "SELECT 1 FROM manual_analise_robo_legs WHERE aba=? LIMIT 1",\n',
    '                    (aba,),\n',
    '                )\n',
    '                if cur.fetchone() is not None:\n',
    '                    cur.execute(\n',
    '                        "SELECT MAX(timestamp) FROM manual_analise_robo_legs WHERE aba=?",\n',
    '                        (aba,),\n',
    '                    )\n',
    '                    row = cur.fetchone()\n',
    '                    if row and row[0]:\n',
    '                        return str(row[0])\n',
    '\n',
    '            # 2) Fallback RTD\n',
    '            if has_table("rtd_analise_robo_legs"):\n',
    '                cur.execute(\n',
    '                    "SELECT MAX(timestamp) FROM rtd_analise_robo_legs WHERE aba=?",\n',
    '                    (aba,),\n',
    '                )\n',
    '                row = cur.fetchone()\n',
    '                if row and row[0]:\n',
    '                    return str(row[0])\n',
    '\n',
    '            # 3) Snapshots (se existirem)\n',
    '            for tname in ("robo_legs_snapshot", "robo_snapshot"):\n',
    '                if has_table(tname):\n',
    '                    cur.execute(f"SELECT MAX(timestamp) FROM {tname} WHERE aba=?", (aba,))\n',
    '                    row = cur.fetchone()\n',
    '                    if row and row[0]:\n',
    '                        return str(row[0])\n',
    '\n',
    '            return None\n',
    '        finally:\n',
    '            con.close()\n',
]

def find_blocks(lines: list[str], name: str) -> list[tuple[int,int,str]]:
    pat = re.compile(rf"^(\s*)def {re.escape(name)}\s*\(")
    hits = []
    for i, ln in enumerate(lines):
        m = pat.match(ln)
        if m:
            base = m.group(1)
            end = len(lines)
            next_def = re.compile(rf"^{re.escape(base)}def\s+\w+")
            for j in range(i+1, len(lines)):
                if next_def.match(lines[j]):
                    end = j
                    break
            hits.append((i, end, base))
    return hits

def main() -> int:
    lines = P.read_text(encoding="utf-8").splitlines(True)

    # 1) remover o bloco duplicado inferior:
    # vamos remover do SEGUNDO _raw_db_path até antes do próximo bloco "não relacionado".
    raw_blocks = find_blocks(lines, "_raw_db_path")
    if len(raw_blocks) >= 2:
        start2, _, base = raw_blocks[1]
        # removemos até EOF (porque pelo seu contexto o duplicado vai até o final do arquivo ou até a próxima seção)
        # mais seguro: remover até o fim do segundo _compute_recalc_signature
        sig_blocks = find_blocks(lines, "_compute_recalc_signature")
        if len(sig_blocks) >= 2:
            _, end2, _ = sig_blocks[1]
            # estende para incluir linhas em branco seguintes
            k = end2
            while k < len(lines) and lines[k].strip() == "":
                k += 1
            end2 = k
            del lines[start2:end2]
        else:
            # fallback: remove do 2o raw_db_path até o fim
            del lines[start2:]
    else:
        # se não tiver duplicado, segue
        pass

    # 2) aplicar manual-first na PRIMEIRA ocorrência de _get_latest_snapshot_timestamp_for_aba
    ts_blocks = find_blocks(lines, "_get_latest_snapshot_timestamp_for_aba")
    if not ts_blocks:
        raise SystemExit("Não encontrei _get_latest_snapshot_timestamp_for_aba após dedupe.")
    start, end, base = ts_blocks[0]

    # garantir assinatura com type hint (mantém a sua primeira)
    # substitui todo o bloco pela def atual + body manual-first
    def_line = lines[start]
    # se a def não tiver return annotation, não forçamos; mas no seu caso a primeira tem
    new_block = [def_line] + MANUAL_FIRST_BODY

    lines = lines[:start] + new_block + lines[end:]

    P.write_text("".join(lines), encoding="utf-8")
    print("✅ Dedupe aplicado + manual-first instalado em details_panel.py")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
