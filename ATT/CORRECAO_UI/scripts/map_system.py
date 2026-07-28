#!/usr/bin/env python3
"""
MAPEAMENTO COMPLETO DO SISTEMA
===============================
Rastreia: importação, fluxo de dados, conexões DB, refresh chain.
NÃO modifica nada — apenas mapeia.

Executar via Git Bash: python scripts/map_system.py
"""

import ast
import os
import sys
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# ─── CONFIGURAÇÃO ───────────────────────────────────────────
PROJETO_RAIZ = Path(r"C:\Users\eucal\projeto")
DB_CANDIDATOS = [
    PROJETO_RAIZ / "dados" / "app.db",
    PROJETO_RAIZ / "data" / "app.db",
    PROJETO_RAIZ / "app.db",
    PROJETO_RAIZ / "db" / "legacy.db",
    PROJETO_RAIZ / "ATT" / "app.db",
]

ARQUIVOS_ENTRY = [
    PROJETO_RAIZ / "UI" / "main_window.py",
    PROJETO_RAIZ / "UI" / "modern" / "dark_window.py",
    PROJETO_RAIZ / "__main__.py",
    PROJETO_RAIZ / "main.py",
    PROJETO_RAIZ / "run.py",
    PROJETO_RAIZ / "app.py",
]

ARQUIVOS_UI = [
    PROJETO_RAIZ / "UI" / "main_window.py",
    PROJETO_RAIZ / "UI" / "modern" / "dark_window.py",
    PROJETO_RAIZ / "UI" / "models" / "ui_data.py",
    PROJETO_RAIZ / "UI" / "components" / "details_panel.py",
    PROJETO_RAIZ / "UI" / "components" / "payoff_chart.py",
    PROJETO_RAIZ / "UI" / "components" / "terminal_vwap_payoff_dark_panel.py",
    PROJETO_RAIZ / "UI" / "components" / "decisions_dark_panel.py",
    PROJETO_RAIZ / "UI" / "components" / "structure_editor_dialog.py",
]

SEPARADOR = "=" * 70


# ─── UTILITÁRIOS ────────────────────────────────────────────

def ler_arquivo(caminho: Path) -> str | None:
    """Lê arquivo com fallback de encoding."""
    if not caminho.exists():
        return None
    for enc in ["utf-8", "latin-1", "cp1252"]:
        try:
            return caminho.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
    return caminho.read_text(encoding="utf-8", errors="ignore")


def extrair_imports(conteudo: str) -> list[dict]:
    """Extrai imports usando AST."""
    try:
        tree = ast.parse(conteudo)
    except SyntaxError:
        return []
    
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append({
                    "tipo": "import",
                    "modulo": alias.name,
                    "alias": alias.asname,
                })
        elif isinstance(node, ast.ImportFrom):
            modulo = node.module or ""
            for alias in node.names:
                nome_completo = f"{modulo}.{alias.name}" if modulo else alias.name
                imports.append({
                    "tipo": "from_import",
                    "modulo": modulo,
                    "nome": alias.name,
                    "alias": alias.asname,
                    "completo": nome_completo,
                })
    return imports


def extrair_funcoes(conteudo: str) -> list[dict]:
    """Extrai definições de função e classes."""
    try:
        tree = ast.parse(conteudo)
    except SyntaxError:
        return []
    
    funcoes = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # Contar quantos .execute() e .commit() dentro
            codigo = ast.unparse(node) if hasattr(ast, 'unparse') else ""
            tem_execute = ".execute(" in codigo or ".executemany(" in codigo
            tem_commit = ".commit()" in codigo
            tem_connect = "connect(" in codigo
            tem_insert = "INSERT" in codigo.upper()
            tem_update = "UPDATE" in codigo.upper()
            tem_delete = "DELETE" in codigo.upper()
            
            funcoes.append({
                "nome": node.name,
                "linha": node.lineno,
                "tem_execute": tem_execute,
                "tem_commit": tem_commit,
                "tem_connect": tem_connect,
                "tem_escrita": tem_insert or tem_update or tem_delete,
            })
    return funcoes


def encontrar_banco() -> Path | None:
    """Encontra o banco real."""
    for candidato in DB_CANDIDATOS:
        if candidato.exists():
            return candidato
    return None


# ─── MAPEAMENTO 1: BANCO DE DADOS ───────────────────────────

def mapear_banco() -> dict:
    """Mapeia localização e estado do banco."""
    banco = encontrar_banco()
    resultado = {
        "encontrado": banco is not None,
        "caminho": str(banco) if banco else None,
        "tamanho_mb": round(banco.stat().st_size / (1024 * 1024), 2) if banco else 0,
    }
    
    if not banco:
        resultado["candidatos_verificados"] = [
            f"{'✓' if c.exists() else '✗'} {c}" for c in DB_CANDIDATOS
        ]
        return resultado
    
    import sqlite3
    conn = sqlite3.connect(str(banco))
    cursor = conn.cursor()
    
    # Listar todas as tabelas
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    )
    tabelas = [row[0] for row in cursor.fetchall()]
    resultado["total_tabelas"] = len(tabelas)
    
    # Para cada tabela, contar registros e último timestamp
    resultado["tabelas"] = []
    for tabela in tabelas:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM [{tabela}]")
            count = cursor.fetchone()[0]
        except:
            count = 0
        
        # Encontrar coluna de timestamp
        col_ts = None
        ultimo_ts = None
        
        cursor.execute(f"PRAGMA table_info([{tabela}])")
        colunas = [c[1] for c in cursor.fetchall()]
        
        for col in ["updated_at", "created_at", "timestamp", "captured_at", "data_hora"]:
            if col in colunas:
                col_ts = col
                try:
                    cursor.execute(
                        f"SELECT MAX([{col}]) FROM [{tabela}] WHERE [{col}] IS NOT NULL"
                    )
                    ultimo_ts = cursor.fetchone()[0]
                except:
                    pass
                break
        
        # Verificar dados recentes (24h)
        dados_recentes = 0
        if col_ts:
            try:
                cursor.execute(
                    f"SELECT COUNT(*) FROM [{tabela}] "
                    f"WHERE [{col_ts}] >= datetime('now', '-1 day')"
                )
                dados_recentes = cursor.fetchone()[0]
            except:
                pass
        
        resultado["tabelas"].append({
            "nome": tabela,
            "registros": count,
            "col_ts": col_ts,
            "ultimo_ts": str(ultimo_ts) if ultimo_ts else None,
            "recentes_24h": dados_recentes,
            "colunas": colunas[:15],  # só as 15 primeiras
        })
    
    conn.close()
    return resultado


# ─── MAPEAMENTO 2: CADEIA DE IMPORTAÇÃO ────────────────────

def mapear_imports() -> dict:
    """Mapeia como os arquivos se importam entre si."""
    resultado = {"entradas": [], "ui_imports": defaultdict(list), "quem_importa_quem": defaultdict(list)}
    
    # Mapear entry points
    for arq in ARQUIVOS_ENTRY:
        if arq.exists():
            resultado["entradas"].append({
                "caminho": str(arq.relative_to(PROJETO_RAIZ)),
                "tem_tk_root": False,
                "tem_ctk_root": False,
                "tem_mainloop": False,
            })
    
    # Analisar imports da UI
    for arq in ARQUIVOS_UI:
        conteudo = ler_arquivo(arq)
        if not conteudo:
            continue
        
        relpath = str(arq.relative_to(PROJETO_RAIZ))
        imports = extrair_imports(conteudo)
        
        # Mapear imports internos do projeto
        for imp in imports:
            if imp["tipo"] == "import":
                nome = imp["modulo"]
            else:
                nome = imp["completo"] if imp["completo"] else imp["modulo"]
            
            if any(p in nome.lower() for p in ["ui", "dark_window", "main_window", 
                                                  "payoff", "details", "decisions",
                                                  "structure_editor", "models"]):
                resultado["quem_importa_quem"][nome].append(relpath)
        
        # Detectar padrões críticos
        tem_tk = "tk.Tk()" in conteudo
        tem_ctk = "ctk.CTk()" in conteudo or "CTk()" in conteudo
        tem_mainloop = ".mainloop()" in conteudo
        tem_after = ".after(" in conteudo
        tem_thread = "threading.Thread" in conteudo or "Thread(" in conteudo
        tem_connect_db = "sqlite3.connect" in conteudo or ".connect(" in conteudo
        
        resultado["ui_imports"][relpath] = {
            "tk_root": tem_tk,
            "ctk_root": tem_ctk,
            "mainloop": tem_mainloop,
            "after": tem_after,
            "thread": tem_thread,
            "db_connect": tem_connect_db,
            "qtde_imports": len(imports),
            "linha_tk": None,
            "linha_ctk": None,
            "linha_mainloop": None,
        }
        
        # Encontrar números de linha exatos
        for i, linha in enumerate(conteudo.splitlines(), 1):
            if "tk.Tk()" in linha and "self.root" in linha:
                resultado["ui_imports"][relpath]["linha_tk"] = i
                resultado["ui_imports"][relpath]["trecho_tk"] = linha.strip()
            if ("CTk()" in linha or "ctk.CTk()" in linha) and "self.root" in linha:
                resultado["ui_imports"][relpath]["linha_ctk"] = i
                resultado["ui_imports"][relpath]["trecho_ctk"] = linha.strip()
            if ".mainloop()" in linha and "self.root" in linha:
                resultado["ui_imports"][relpath]["linha_mainloop"] = i
                resultado["ui_imports"][relpath]["trecho_mainloop"] = linha.strip()
    
    return resultado


# ─── MAPEAMENTO 3: CADEIA DE REFRESH ───────────────────────

def mapear_refresh_chain() -> dict:
    """Mapeia todos os mecanismos de refresh e como se conectam."""
    resultado = {
        "polling": [],
        "after_callbacks": [],
        "threads": [],
        "rtd_connections": [],
        "canvas_redraw": [],
    }
    
    for arq in ARQUIVOS_UI:
        conteudo = ler_arquivo(arq)
        if not conteudo:
            continue
        
        relpath = str(arq.relative_to(PROJETO_RAIZ))
        linhas = conteudo.splitlines()
        
        for i, linha in enumerate(linhas, 1):
            ls = linha.strip()
            
            if ".after(" in ls and not ls.startswith("#"):
                resultado["after_callbacks"].append({
                    "arquivo": relpath,
                    "linha": i,
                    "trecho": ls[:120],
                })
            
            if "threading.Thread" in ls or "Thread(target=" in ls:
                resultado["threads"].append({
                    "arquivo": relpath,
                    "linha": i,
                    "trecho": ls[:120],
                })
            
            if "win32com" in ls.lower() or "xlwings" in ls.lower():
                resultado["rtd_connections"].append({
                    "arquivo": relpath,
                    "linha": i,
                    "trecho": ls[:120],
                })
            
            if "canvas.draw" in ls or "fig.canvas.draw" in ls:
                resultado["canvas_redraw"].append({
                    "arquivo": relpath,
                    "linha": i,
                    "trecho": ls[:120],
                })
            
            if ("_poll_" in ls or "_watcher" in ls or "poll_" in ls) and "def " in ls:
                resultado["polling"].append({
                    "arquivo": relpath,
                    "linha": i,
                    "funcao": ls.split("(")[0].replace("def ", "").strip(),
                })
    
    return resultado


# ─── MAPEAMENTO 4: QUEM CHAMA QUEM (MAIN ↔ DARK) ──────────

def mapear_relacao_main_dark() -> dict:
    """Mapeia a relação exata entre main_window e dark_window."""
    main = ler_arquivo(PROJETO_RAIZ / "UI" / "main_window.py")
    dark = ler_arquivo(PROJETO_RAIZ / "UI" / "modern" / "dark_window.py")
    
    resultado = {
        "main_importa_dark": False,
        "dark_importa_main": False,
        "main_referencia_dark": [],
        "dark_referencia_main": [],
    }
    
    if main:
        for i, linha in enumerate(main.splitlines(), 1):
            if "dark_window" in linha.lower() and ("import" in linha.lower() or "from" in linha.lower()):
                resultado["main_importa_dark"] = True
                resultado["main_referencia_dark"].append({
                    "linha": i,
                    "trecho": linha.strip(),
                })
            elif "dark_window" in linha.lower() or "DarkWindow" in linha:
                resultado["main_referencia_dark"].append({
                    "linha": i,
                    "trecho": linha.strip(),
                })
    
    if dark:
        for i, linha in enumerate(dark.splitlines(), 1):
            if "main_window" in linha.lower() and ("import" in linha.lower() or "from" in linha.lower()):
                resultado["dark_importa_main"] = True
                resultado["dark_referencia_main"].append({
                    "linha": i,
                    "trecho": linha.strip(),
                })
            elif "main_window" in linha.lower() or "MainWindow" in linha:
                resultado["dark_referencia_main"].append({
                    "linha": i,
                    "trecho": linha.strip(),
                })
    
    # Verificar como dark_window é invocado
    resultado["main_tem_CTk"] = "CTk()" in main if main else False
    resultado["main_tem_Tk"] = "tk.Tk()" in main if main else False
    resultado["dark_tem_CTk"] = "CTk()" in dark if dark else False
    resultado["dark_tem_Tk"] = "tk.Tk()" in dark if dark else False
    resultado["main_tem_mainloop"] = ".mainloop()" in main if main else False
    resultado["dark_tem_mainloop"] = ".mainloop()" in dark if dark else False
    
    # Verificar se dark_window é instanciado dentro de main_window após mainloop
    if main:
        linhas_mainloop = [
            i for i, l in enumerate(main.splitlines(), 1) 
            if ".mainloop()" in l
        ]
        linhas_dark = [
            i for i, l in enumerate(main.splitlines(), 1) 
            if "dark_window" in l.lower() or "DarkWindow" in l
        ]
        resultado["dark_antes_mainloop"] = any(
            dl < ml for dl in linhas_dark for ml in linhas_mainloop
        )
        resultado["dark_depois_mainloop"] = any(
            dl > ml for dl in linhas_dark for ml in linhas_mainloop
        )
    
    return resultado


# ─── MAPEAMENTO 5: CADEIA COMPLETA RTD → DB → UI ───────────

def mapear_fluxo_dados() -> dict:
    """Mapeia o fluxo completo de dados."""
    resultado = {
        "fonte_dados": [],
        "sync_services": [],
        "repositorios": [],
        "ui_readers": [],
    }
    
    # Procurar arquivos que sincronizam RTD/Excel → DB
    for arq in sorted(PROJETO_RAIZ.rglob("*.py")):
        if arq.name.startswith("__"):
            continue
        if "backup" in str(arq).lower():
            continue
        if "CORRECAO_UI" in str(arq):
            continue
        
        conteudo = ler_arquivo(arq)
        if not conteudo:
            continue
        
        relpath = str(arq.relative_to(PROJETO_RAIZ))
        
        # Detectar classe de serviço
        if ("rtd_option_quotes" in arq.name.lower() and "sync" in arq.name.lower()) or \
           ("populate" in arq.name.lower() and "rtd" in arq.name.lower()) or \
           ("excel_rtd" in arq.name.lower() and "sync" in arq.name.lower()):
            resultado["sync_services"].append(relpath)
        
        # Detectar fontes de dados
        if "win32com" in conteudo or "xlwings" in conteudo:
            if "dispatch(" in conteudo or "Workbooks(" in conteudo:
                resultado["fonte_dados"].append(relpath)
        
        # Detectar repositórios
        if "repository" in arq.name.lower() and "test" not in arq.name.lower():
            resultado["repositorios"].append(relpath)
        
        # Detectar leitores da UI
        if "UI" in relpath and ("sqlite3" in conteudo or ".connect(" in conteudo):
            resultado["ui_readers"].append(relpath)
    
    return resultado


# ─── MAIN ───────────────────────────────────────────────────

def main():
    print(SEPARADOR)
    print("  MAPEAMENTO COMPLETO DO SISTEMA")
    print(f"  Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Raiz: {PROJETO_RAIZ}")
    print(SEPARADOR)
    
    # ─── 1. BANCO ───
    print("\n" + "=" * 50)
    print("  [1/5] MAPEANDO BANCO DE DADOS")
    print("=" * 50)
    
    banco = mapear_banco()
    if banco["encontrado"]:
        print(f"\n  ✓ Banco encontrado: {banco['caminho']}")
        print(f"     Tamanho: {banco['tamanho_mb']} MB")
        print(f"     Tabelas: {banco['total_tabelas']}")
        print(f"\n  Tabelas com dados recentes (24h):")
        
        tem_recentes = False
        for t in banco.get("tabelas", []):
            if t.get("recentes_24h", 0) > 0:
                tem_recentes = True
                print(f"     ✓ {t['nome']}: {t['recentes_24h']} registros (total: {t['registros']}, último: {t.get('ultimo_ts', 'N/A')})")
        
        if not tem_recentes:
            print(f"     ❌ NENHUMA tabela tem dados das últimas 24h!")
        
        print(f"\n  Todas as tabelas:")
        for t in banco.get("tabelas", []):
            status = "🟢" if t.get("recentes_24h", 0) > 0 else "⚪"
            print(f"     {status} {t['nome']}: {t['registros']} registros | último: {t.get('ultimo_ts', 'N/A')}")
    else:
        print(f"\n  ❌ Banco NÃO encontrado!")
        for c in banco.get("candidatos_verificados", []):
            print(f"     {c}")
    
    # ─── 2. IMPORTS ───
    print("\n" + "=" * 50)
    print("  [2/5] MAPEANDO CADEIA DE IMPORTAÇÃO (UI)")
    print("=" * 50)
    
    imports_map = mapear_imports()
    
    print(f"\n  Entry points encontrados:")
    for e in imports_map["entradas"]:
        print(f"     {'✓' if Path(PROJETO_RAIZ, e['caminho']).exists() else '✗'} {e['caminho']}")
    
    print(f"\n  Arquivos UI com características críticas:")
    for arq, info in imports_map["ui_imports"].items():
        flags = []
        if info["tk_root"]:
            flags.append(f"🔴 tk.Tk() na linha {info.get('linha_tk', '?')}: {info.get('trecho_tk', '?')}")
        if info["ctk_root"]:
            flags.append(f"🔴 ctk.CTk() na linha {info.get('linha_ctk', '?')}: {info.get('trecho_ctk', '?')}")
        if info["mainloop"]:
            flags.append(f"🟡 mainloop() na linha {info.get('linha_mainloop', '?')}")
        if info["thread"]:
            flags.append("🔵 threading.Thread")
        if info["after"]:
            flags.append("🔵 .after()")
        if info["db_connect"]:
            flags.append("🟢 db connect")
        
        print(f"\n  📄 {arq}")
        for f in flags:
            print(f"     {f}")
    
    # ─── 3. MAIN ↔ DARK ───
    print("\n" + "=" * 50)
    print("  [3/5] MAPEANDO RELAÇÃO main_window ↔ dark_window")
    print("=" * 50)
    
    relacao = mapear_relacao_main_dark()
    
    print(f"\n  main_window.py")
    print(f"     tk.Tk(): {relacao['main_tem_Tk']}")
    print(f"     CTk(): {relacao['main_tem_CTk']}")
    print(f"     mainloop(): {relacao['main_tem_mainloop']}")
    print(f"     Importa dark_window: {relacao['main_importa_dark']}")
    if relacao["main_referencia_dark"]:
        print(f"     Referências a dark_window:")
        for ref in relacao["main_referencia_dark"]:
            print(f"       Linha {ref['linha']}: {ref['trecho']}")
    
    print(f"\n  dark_window.py")
    print(f"     tk.Tk(): {relacao['dark_tem_Tk']}")
    print(f"     CTk(): {relacao['dark_tem_CTk']}")
    print(f"     mainloop(): {relacao['dark_tem_mainloop']}")
    print(f"     Importa main_window: {relacao['dark_importa_main']}")
    if relacao["dark_referencia_main"]:
        print(f"     Referências a main_window:")
        for ref in relacao["dark_referencia_main"]:
            print(f"       Linha {ref['linha']}: {ref['trecho']}")
    
    # Diagnóstico do conflito
    print(f"\n  ╔══════════════════════════════════════════════════╗")
    if relacao["main_tem_Tk"] and relacao["dark_tem_CTk"] and \
       relacao["main_tem_mainloop"] and relacao["dark_tem_mainloop"]:
        print(f"  ║ 🔴 CONFLITO DE MAINLOOP CONFIRMADO               ║")
        print(f"  ║    main_window.py → tk.Tk() + mainloop()          ║")
        print(f"  ║    dark_window.py → ctk.CTk() + mainloop()        ║")
        print(f"  ║                                                    ║")
        print(f"  ║    Duas raízes = dois event loops independentes    ║")
        print(f"  ║    Callbacks de uma NUNCA executam se a outra      ║")
        print(f"  ║    estiver no mainloop.                            ║")
        print(f"  ╚══════════════════════════════════════════════════╝")
    else:
        print(f"  ║ ✓ Sem conflito aparente                           ║")
        print(f"  ╚══════════════════════════════════════════════════╝")
    
    # ─── 4. REFRESH CHAIN ───
    print("\n" + "=" * 50)
    print("  [4/5] MAPEANDO CADEIA DE REFRESH")
    print("=" * 50)
    
    refresh = mapear_refresh_chain()
    
    print(f"\n  Callbacks .after(): {len(refresh['after_callbacks'])}")
    for c in refresh["after_callbacks"][:10]:
        print(f"     {c['arquivo']}:{c['linha']} → {c['trecho'][:100]}")
    if len(refresh["after_callbacks"]) > 10:
        print(f"     ... e mais {len(refresh['after_callbacks']) - 10}")
    
    print(f"\n  Threads: {len(refresh['threads'])}")
    for c in refresh["threads"]:
        print(f"     {c['arquivo']}:{c['linha']} → {c['trecho'][:100]}")
    
    print(f"\n  Conexões RTD/Excel: {len(refresh['rtd_connections'])}")
    for c in refresh["rtd_connections"][:5]:
        print(f"     {c['arquivo']}:{c['linha']} → {c['trecho'][:100]}")
    
    print(f"\n  Canvas redraws: {len(refresh['canvas_redraw'])}")
    for c in refresh["canvas_redraw"]:
        print(f"     {c['arquivo']}:{c['linha']} → {c['trecho'][:100]}")
    
    print(f"\n  Funções de polling: {len(refresh['polling'])}")
    for c in refresh["polling"]:
        print(f"     {c['arquivo']}:{c['linha']} → {c['funcao']}()")
    
    # ─── 5. FLUXO DE DADOS ───
    print("\n" + "=" * 50)
    print("  [5/5] MAPEANDO FLUXO RTD → DB → UI")
    print("=" * 50)
    
    fluxo = mapear_fluxo_dados()
    
    print(f"\n  Fontes de dados (RTD/Excel): {len(fluxo['fonte_dados'])}")
    for f in fluxo["fonte_dados"]:
        print(f"     📥 {f}")
    
    print(f"\n  Serviços de sync (RTD → DB): {len(fluxo['sync_services'])}")
    for f in fluxo["sync_services"]:
        print(f"     🔄 {f}")
    
    print(f"\n  Repositórios: {len(fluxo['repositorios'])}")
    for f in fluxo["repositorios"]:
        print(f"     📦 {f}")
    
    print(f"\n  Leitores da UI (DB → UI): {len(fluxo['ui_readers'])}")
    for f in fluxo["ui_readers"]:
        print(f"     📤 {f}")
    
    # ─── RESUMO ───
    print(f"\n{SEPARADOR}")
    print("  RESUMO DO MAPEAMENTO")
    print(SEPARADOR)
    
    problemas = []
    
    if not banco["encontrado"]:
        problemas.append("🔴 Banco de dados não encontrado")
    else:
        tem_recentes = any(
            t.get("recentes_24h", 0) > 0 for t in banco.get("tabelas", [])
        )
        if not tem_recentes:
            problemas.append("🟠 Banco existe mas sem dados recentes (24h)")
    
    if relacao["main_tem_Tk"] and relacao["dark_tem_CTk"] and \
       relacao["main_tem_mainloop"] and relacao["dark_tem_mainloop"]:
        problemas.append("🔴 Dual root + dual mainloop (main_window + dark_window)")
    
    if len(fluxo["sync_services"]) == 0:
        problemas.append("🟠 Nenhum serviço de sync RTD→DB encontrado")
    
    if len(fluxo["ui_readers"]) == 0:
        problemas.append("🟠 Nenhum leitor DB→UI encontrado nos arquivos da UI")
    
    if problemas:
        print(f"\n  {len(problemas)} problema(s) encontrado(s):")
        for p in problemas:
            print(f"  • {p}")
    else:
        print("\n  ✓ Sistema mapeado sem problemas aparentes")
    
    print(f"\n  Próximos passos sugeridos:")
    if relacao["main_tem_Tk"] and relacao["dark_tem_CTk"]:
        print(f"  1. Resolver dual root: dark_window deve usar CTkToplevel")
        print(f"     ou main_window deve delegar o mainloop para dark_window")
    if not (banco["encontrado"] and tem_recentes):
        print(f"  2. Verificar por que dados RTD não chegam ao banco")
    print(f"  3. Após correções, rodar diagnose_data_flow.py novamente")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
