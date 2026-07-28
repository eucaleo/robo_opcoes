#!/usr/bin/env python3
"""
CORREÇÃO DE JANELA RAIZ DUPLICADA (tk.Tk + ctk.CTk)
=====================================================
Detecta e corrige o problema de duas janelas raiz no mesmo processo.
Isso causa conflito de mainloop — eventos de uma janela não são processados.

Executar via Git Bash: python scripts/fix_dual_root.py
"""

import os
import sys
import shutil
from datetime import datetime
from pathlib import Path

# ─── CONFIGURAÇÃO ───────────────────────────────────────────
PROJETO_RAIZ = Path(r"C:\Users\eucal\projeto")
BACKUP_DIR = PROJETO_RAIZ / "ATT" / "CORRECAO_UI" / "backups" / f"dual_root_fix_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

MAIN_WINDOW = PROJETO_RAIZ / "UI" / "main_window.py"
DARK_WINDOW = PROJETO_RAIZ / "UI" / "modern" / "dark_window.py"

SEPARADOR = "=" * 70


def analisar_arquivo(caminho: Path) -> dict:
    """Analisa um arquivo em busca de criação de janela raiz."""
    if not caminho.exists():
        return {"existe": False}
    
    conteudo = caminho.read_text(encoding="utf-8", errors="ignore")
    linhas = conteudo.splitlines()
    
    info = {
        "existe": True,
        "tem_tk": "tk.Tk()" in conteudo,
        "tem_ctk": "ctk.CTk()" in conteudo or "CTk()" in conteudo,
        "tem_mainloop": ".mainloop()" in conteudo,
        "tk_linhas": [],
        "ctk_linhas": [],
        "mainloop_linhas": [],
    }
    
    for i, linha in enumerate(linhas, 1):
        if "tk.Tk()" in linha:
            info["tk_linhas"].append((i, linha.strip()))
        if "CTk()" in linha or "ctk.CTk()" in linha:
            info["ctk_linhas"].append((i, linha.strip()))
        if ".mainloop()" in linha:
            info["mainloop_linhas"].append((i, linha.strip()))
    
    return info


def corrigir_dark_window(dry_run: bool = True) -> bool:
    """
    Estratégia: dark_window.py herda de ctk.CTk ou cria sua própria raiz?
    
    O problema: main_window.py cria tk.Tk() como raiz e dark_window.py cria 
    ctk.CTk() como OUTRA raiz. Duas raízes = dois mainloops conflitantes.
    
    Solução ideal: dark_window.py deve usar ctk.CTkToplevel() em vez de CTk(),
    vinculando-se à raiz de main_window.py. Ou main_window.py deve usar ctk.CTk().
    
    Como não temos visibilidade total da arquitetura, vamos:
    1. Fazer backup
    2. Substituir CTk() por CTkToplevel() no dark_window.py
    3. Adicionar a raiz de main_window como parent
    """
    if not DARK_WINDOW.exists():
        print("❌ dark_window.py não encontrado")
        return False
    
    conteudo = DARK_WINDOW.read_text(encoding="utf-8", errors="ignore")
    linhas = conteudo.splitlines()
    
    info = analisar_arquivo(DARK_WINDOW)
    if not info["tem_ctk"]:
        print("✓ dark_window.py não cria CTk() — OK")
        return True
    
    print(f"\n📄 dark_window.py")
    for lin, trecho in info["ctk_linhas"]:
        print(f"   Linha {lin}: {trecho}")
    for lin, trecho in info["mainloop_linhas"]:
        print(f"   Linha {lin}: {trecho}")
    
    if dry_run:
        print("\n🔧 [DRY-RUN] Estratégia de correção:")
        print("   1. Substituir ctk.CTk() por ctk.CTkToplevel()")
        print("   2. CTkToplevel aceita um parent — vincular à raiz de main_window")
        print("   3. Remover .mainloop() do dark_window (só a raiz principal chama mainloop)")
        print("\n   Execute com --apply para aplicar.")
        return True
    
    # Aplicar correção
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backup_path = BACKUP_DIR / "dark_window.py"
    shutil.copy2(DARK_WINDOW, backup_path)
    print(f"\n📁 Backup: {backup_path}")
    
    # Substituições
    novo_conteudo = conteudo
    
    # 1. CTk() → CTkToplevel()
    novo_conteudo = novo_conteudo.replace("ctk.CTk()", "ctk.CTkToplevel()")
    novo_conteudo = novo_conteudo.replace("CTk()", "CTkToplevel()")
    
    # 2. Remover .mainloop() — só a raiz principal deve ter
    # Comentamos em vez de remover para segurança
    novo_conteudo = novo_conteudo.replace(
        "self.root.mainloop()",
        "# self.root.mainloop()  # REMOVIDO: só a raiz principal (main_window) chama mainloop"
    )
    
    if novo_conteudo != conteudo:
        DARK_WINDOW.write_text(novo_conteudo, encoding="utf-8")
        print("✅ dark_window.py corrigido:")
        print("   - CTk() → CTkToplevel()")
        print("   - .mainloop() comentado")
        return True
    else:
        print("⚠️ Nenhuma alteração necessária ou possível")
        return False


def main():
    dry_run = "--apply" not in sys.argv
    
    print(SEPARADOR)
    print("  CORREÇÃO DE JANELA RAIZ DUPLICADA")
    print(f"  Modo: {'DRY-RUN (simulação)' if dry_run else 'APLICAÇÃO REAL'}")
    print(f"  Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(SEPARADOR)
    
    # ─── Analisar main_window.py ───
    print("\n[1] main_window.py")
    info_main = analisar_arquivo(MAIN_WINDOW)
    if info_main["existe"]:
        print(f"   tk.Tk(): {info_main['tem_tk']}")
        print(f"   CTk(): {info_main['tem_ctk']}")
        print(f"   mainloop(): {info_main['tem_mainloop']}")
        for lin, trecho in info_main["tk_linhas"]:
            print(f"     Linha {lin}: {trecho}")
        for lin, trecho in info_main["mainloop_linhas"]:
            print(f"     Linha {lin}: {trecho}")
    else:
        print("   ❌ Arquivo não encontrado")
    
    # ─── Analisar dark_window.py ───
    print("\n[2] dark_window.py")
    info_dark = analisar_arquivo(DARK_WINDOW)
    if info_dark["existe"]:
        print(f"   tk.Tk(): {info_dark['tem_tk']}")
        print(f"   CTk(): {info_dark['tem_ctk']}")
        print(f"   mainloop(): {info_dark['tem_mainloop']}")
        for lin, trecho in info_dark["ctk_linhas"]:
            print(f"     Linha {lin}: {trecho}")
        for lin, trecho in info_dark["mainloop_linhas"]:
            print(f"     Linha {lin}: {trecho}")
    else:
        print("   ❌ Arquivo não encontrado")
    
    # ─── Diagnóstico ───
    conflito = (info_main.get("tem_tk") or info_main.get("tem_ctk")) and \
               (info_dark.get("tem_ctk") or info_dark.get("tem_tk"))
    
    print(f"\n[3] Diagnóstico: {'🔴 CONFLITO DETECTADO' if conflito else '✓ Sem conflito'}")
    
    if conflito:
        print("   Duas janelas raiz no mesmo processo:")
        print(f"   - main_window.py cria {'tk.Tk()' if info_main.get('tem_tk') else 'CTk()'}")
        print(f"   - dark_window.py cria {'CTk()' if info_dark.get('tem_ctk') else 'tk.Tk()'}")
        print("   ⚠️ Isso causa: eventos de uma janela bloqueiam a outra,")
        print("   ⚠️ callbacks de refresh não executam, UI 'congela' parcialmente.")
        
        corrigir_dark_window(dry_run=dry_run)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
