from __future__ import annotations

import re
import sys
from pathlib import Path

TARGET = Path("UI/components/details_panel.py")

NEW_BLOCK = r'''def _get_latest_snapshot_timestamp_for_aba(self, aba: str) -> str | None:
        """
        Timestamp canônico por aba para dedupe de recálculo.

        Regra:
          1) Se manual_analise_robo_legs existir e tiver linhas para a aba, usa MAX(timestamp) do manual
          2) Senão, usa MAX(timestamp) do rtd_analise_robo_legs (se existir)
          3) Por fim, tenta snapshots (robo_legs_snapshot / robo_snapshot) se existirem
        """
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
'''

def main() -> int:
    if not TARGET.exists():
        print(f"Arquivo não encontrado: {TARGET}")
        return 2

    s = TARGET.read_text(encoding="utf-8", errors="replace").splitlines(True)

    # localizar def (com indent de 4 espaços típico de método)
    starts = [i for i,l in enumerate(s) if re.match(r"^\s{4}def _get_latest_snapshot_timestamp_for_aba\s*\(", l)]
    if len(starts) != 1:
        print(f"Esperava 1 definição, encontrei {len(starts)}: {starts}")
        return 3

    start = starts[0]

    # achar fim do bloco: próxima linha com indent 4 e 'def ' (ou EOF)
    end = len(s)
    for i in range(start + 1, len(s)):
        if re.match(r"^\s{4}def\s+\w+", s[i]):
            end = i
            break

    # manter indent original (4 espaços) do bloco novo
    new_lines = []
    for line in NEW_BLOCK.splitlines(True):
        new_lines.append("    " + line if line.startswith("def ") else ("    " + line if line and not line.startswith("        ") and not line.startswith("    ") else line))
    # acima: NEW_BLOCK já vem com indent interno correto a partir de 'def' sem 4 espaços;
    # vamos prefixar o primeiro nível com 4 espaços e preservar o resto.

    out = s[:start] + new_lines + s[end:]
    TARGET.write_text("".join(out), encoding="utf-8")
    print("✅ Atualizado:", TARGET)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
