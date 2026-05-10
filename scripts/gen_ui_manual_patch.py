#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


def _ensure_repo_on_syspath() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))


def main() -> None:
    _ensure_repo_on_syspath()
    
    ui_file = Path("UI/components/details_panel.py")
    if not ui_file.exists():
        print(f"Erro: {ui_file} não encontrado")
        return 1
    
    content = ui_file.read_text(encoding="utf-8")
    lines = content.splitlines(True)
    
    # Encontrar onde começam as funções duplicadas
    func_starts = []
    for i, line in enumerate(lines):
        if "def _get_latest_snapshot_timestamp_for_aba" in line:
            func_starts.append(i)
    
    if len(func_starts) != 2:
        print(f"Esperava 2 definições da função, encontrei {len(func_starts)}")
        return 1
    
    print(f"Encontradas funções duplicadas nas linhas: {[i+1 for i in func_starts]}")
    
    # Encontrar onde termina a segunda função (aproximação)
    second_start = func_starts[1]
    second_end = len(lines)
    
    # Procurar próxima definição de função ou final da classe
    for i in range(second_start + 1, len(lines)):
        line = lines[i].strip()
        if line.startswith("def ") and not line.startswith("def _compute_recalc_signature"):
            second_end = i
            break
    
    # Nova implementação da função
    new_function = '''    def _get_latest_snapshot_timestamp_for_aba(self, aba: str) -> str | None:
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

    def _compute_recalc_signature(self, aba: str) -> tuple[str, str | None]:
        return (aba, self._get_latest_snapshot_timestamp_for_aba(aba))

'''
    
    # Reconstruir o arquivo:
    # 1. Até a primeira função (exclusive)
    # 2. Nova implementação
    # 3. Pular tudo até depois da segunda função
    
    first_start = func_starts[0]
    
    new_lines = lines[:first_start] + [new_function]
    
    # Pular toda a região das funções duplicadas
    skip_until = second_end
    new_lines.extend(lines[skip_until:])
    
    # Criar backup
    backup_file = ui_file.with_suffix(".py.bak")
    ui_file.rename(backup_file)
    
    # Escrever nova versão
    new_content = "".join(new_lines)
    ui_file.write_text(new_content, encoding="utf-8")
    
    print(f"✅ UI atualizada")
    print(f"📁 Backup salvo em: {backup_file}")
    print("🧪 Testando sintaxe...")
    
    try:
        import py_compile
        py_compile.compile(str(ui_file), doraise=True)
        print("✅ Sintaxe OK")
    except Exception as e:
        print(f"❌ Erro de sintaxe: {e}")
        # Restaurar backup
        backup_file.rename(ui_file)
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
