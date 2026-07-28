#!/usr/bin/env python3
"""
DIAGNÓSTICO DE FLUXO DE DADOS: RTD → DB → UI
=============================================
Verifica por que dados novos não chegam na interface.
Executar via Git Bash: python scripts/diagnose_data_flow.py
"""

import sqlite3
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# ─── CONFIGURAÇÃO ───────────────────────────────────────────
PROJETO_RAIZ = Path(r"C:\Users\eucal\projeto")
APP_DB = PROJETO_RAIZ / "app.db"
LEGACY_DB = PROJETO_RAIZ / "db" / "legacy.db"

# Possíveis localizações do banco
DB_CANDIDATOS = [
    APP_DB,
    LEGACY_DB,
    PROJETO_RAIZ / "data" / "app.db",
    PROJETO_RAIZ / "ATT" / "app.db",
]

SEPARADOR = "=" * 70


def encontrar_banco() -> Path | None:
    """Encontra o banco de dados SQLite do sistema."""
    for candidato in DB_CANDIDATOS:
        if candidato.exists():
            return candidato
    return None


def diagnosticar_tabela(conn: sqlite3.Connection, nome: str, 
                         col_timestamp: str = "updated_at") -> dict:
    """Diagnostica uma tabela: qtde de registros, timestamps mais recentes."""
    cursor = conn.cursor()
    resultado = {"tabela": nome, "existe": False, "total": 0, "mais_recente": None}
    
    try:
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (nome,)
        )
        if not cursor.fetchone():
            return resultado
        
        resultado["existe"] = True
        cursor.execute(f"SELECT COUNT(*) FROM [{nome}]")
        resultado["total"] = cursor.fetchone()[0]
        
        # Tentar colunas de timestamp comuns
        for col in [col_timestamp, "created_at", "timestamp", "data_hora", "captured_at"]:
            try:
                cursor.execute(
                    f"SELECT MAX([{col}]) FROM [{nome}] WHERE [{col}] IS NOT NULL"
                )
                val = cursor.fetchone()[0]
                if val:
                    resultado["mais_recente"] = str(val)
                    resultado["coluna_ts"] = col
                    break
            except sqlite3.OperationalError:
                continue
        
        return resultado
    except Exception as e:
        resultado["erro"] = str(e)
        return resultado


def verificar_conexao_ui() -> list[dict]:
    """Verifica quais arquivos da UI conectam ao banco e como."""
    arquivos_ui = [
        PROJETO_RAIZ / "UI" / "models" / "ui_data.py",
        PROJETO_RAIZ / "UI" / "components" / "details_panel.py",
        PROJETO_RAIZ / "UI" / "components" / "terminal_vwap_payoff_dark_panel.py",
        PROJETO_RAIZ / "UI" / "components" / "payoff_chart.py",
        PROJETO_RAIZ / "UI" / "main_window.py",
        PROJETO_RAIZ / "UI" / "modern" / "dark_window.py",
    ]
    
    resultados = []
    for arq in arquivos_ui:
        info = {"arquivo": str(arq.relative_to(PROJETO_RAIZ)) if arq.exists() else str(arq),
                "existe": arq.exists()}
        if arq.exists():
            conteudo = arq.read_text(encoding="utf-8", errors="ignore")
            info["tem_connect"] = "sqlite3.connect" in conteudo or "connect(" in conteudo
            info["tem_commit"] = ".commit()" in conteudo
            info["tem_execute"] = ".execute(" in conteudo or ".executemany(" in conteudo
            info["tem_isolation_level"] = "isolation_level" in conteudo
            info["linhas"] = len(conteudo.splitlines())
        resultados.append(info)
    return resultados


def verificar_dual_root() -> dict:
    """Verifica se há duas janelas raiz (CTk e Tk) no sistema."""
    main_window = PROJETO_RAIZ / "UI" / "main_window.py"
    dark_window = PROJETO_RAIZ / "UI" / "modern" / "dark_window.py"
    
    resultado = {"main_window_tk": False, "dark_window_ctk": False, "conflito": False}
    
    if main_window.exists():
        conteudo = main_window.read_text(encoding="utf-8", errors="ignore")
        resultado["main_window_tk"] = "tk.Tk()" in conteudo
        # Encontrar a linha exata
        for i, linha in enumerate(conteudo.splitlines(), 1):
            if "tk.Tk()" in linha:
                resultado["main_window_linha"] = i
                resultado["main_window_trecho"] = linha.strip()
    
    if dark_window.exists():
        conteudo = dark_window.read_text(encoding="utf-8", errors="ignore")
        resultado["dark_window_ctk"] = "ctk.CTk()" in conteudo or "CTk()" in conteudo
        for i, linha in enumerate(conteudo.splitlines(), 1):
            if "CTk()" in linha or "ctk.CTk()" in linha:
                resultado["dark_window_linha"] = i
                resultado["dark_window_trecho"] = linha.strip()
    
    resultado["conflito"] = resultado["main_window_tk"] and resultado["dark_window_ctk"]
    return resultado


def verificar_derived_repo_duplicadas() -> dict:
    """Verifica funções duplicadas em derived_repo.py."""
    derived = PROJETO_RAIZ / "db" / "derived_repo.py"
    resultado = {"existe": derived.exists(), "duplicadas": []}
    
    if not derived.exists():
        return resultado
    
    conteudo = derived.read_text(encoding="utf-8", errors="ignore")
    linhas = conteudo.splitlines()
    
    # Encontrar definições de função
    funcoes = {}
    for i, linha in enumerate(linhas, 1):
        linha_strip = linha.strip()
        if linha_strip.startswith("def "):
            nome = linha_strip.split("(")[0].replace("def ", "").strip()
            if nome not in funcoes:
                funcoes[nome] = []
            funcoes[nome].append(i)
    
    for nome, ocorrencias in funcoes.items():
        if len(ocorrencias) > 1:
            resultado["duplicadas"].append({
                "nome": nome,
                "linhas": ocorrencias,
                "total": len(ocorrencias)
            })
    
    resultado["total_duplicadas"] = len(resultado["duplicadas"])
    return resultado


def main():
    print(SEPARADOR)
    print("  DIAGNÓSTICO DE FLUXO DE DADOS — RTD → DB → UI")
    print(f"  Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(SEPARADOR)
    
    # ─── 1. ENCONTRAR BANCO ───
    print("\n[1] BANCO DE DADOS")
    print("-" * 40)
    banco = encontrar_banco()
    if not banco:
        print("❌ ERRO CRÍTICO: Nenhum banco de dados encontrado!")
        print("   Candidatos verificados:")
        for c in DB_CANDIDATOS:
            print(f"     {'✓' if c.exists() else '✗'} {c}")
        return 1
    
    print(f"✓ Banco encontrado: {banco}")
    tamanho_mb = banco.stat().st_size / (1024 * 1024)
    print(f"  Tamanho: {tamanho_mb:.2f} MB")
    
    # ─── 2. DIAGNOSTICAR TABELAS ───
    print("\n[2] TABELAS DO BANCO")
    print("-" * 40)
    
    conn = sqlite3.connect(str(banco))
    
    tabelas_criticas = [
        ("rtd_option_quotes", "updated_at"),
        ("rtd_option_quotes_snapshot", "captured_at"),
        ("payoff_curve_points", "created_at"),
        ("canonical_payoff_curve_points", "created_at"),
        ("system_snapshots", "created_at"),
        ("structure_leg_snapshots", "created_at"),
        ("pricing_executions", "created_at"),
        ("robo_legs", "updated_at"),
        ("manual_legs", "updated_at"),
    ]
    
    for nome, col_ts in tabelas_criticas:
        info = diagnosticar_tabela(conn, nome, col_ts)
        status = "✓" if info["existe"] else "✗"
        print(f"  {status} {nome}: ", end="")
        if info["existe"]:
            print(f"{info['total']} registros", end="")
            if info.get("mais_recente"):
                print(f" | Último: {info['mais_recente']}", end="")
            if info.get("coluna_ts"):
                print(f" (col: {info['coluna_ts']})", end="")
        else:
            print("NÃO EXISTE", end="")
        print()
    
    # Verificar se há dados RECENTES (últimas 24h)
    print("\n[3] VERIFICAÇÃO DE DADOS RECENTES (últimas 24h)")
    print("-" * 40)
    
    cursor = conn.cursor()
    tem_dados_recentes = False
    
    for nome, col_ts in tabelas_criticas:
        try:
            cursor.execute(
                f"SELECT COUNT(*) FROM [{nome}] "
                f"WHERE [{col_ts}] >= datetime('now', '-1 day')"
            )
            count = cursor.fetchone()[0]
            if count > 0:
                print(f"  ✓ {nome}: {count} registros nas últimas 24h")
                tem_dados_recentes = True
        except sqlite3.OperationalError:
            pass
    
    if not tem_dados_recentes:
        print("  ❌ ALERTA: NENHUMA tabela tem dados das últimas 24 horas!")
        print("     Isso explica por que a UI só mostra dados antigos.")
    
    conn.close()
    
    # ─── 4. VERIFICAR CONEXÕES DA UI ───
    print("\n[4] CONEXÕES SQLITE NOS ARQUIVOS DA UI")
    print("-" * 40)
    
    conexoes_ui = verificar_conexao_ui()
    for info in conexoes_ui:
        status = "✓" if info["existe"] else "✗"
        print(f"  {status} {info['arquivo']}")
        if info["existe"]:
            print(f"     connect: {info['tem_connect']} | "
                  f"execute: {info['tem_execute']} | "
                  f"commit: {info['tem_commit']} | "
                  f"isolation_level: {info['tem_isolation_level']}")
            if info["tem_execute"] and not info["tem_commit"]:
                print(f"     ⚠️ ALERTA: Faz execute() mas NÃO tem commit()!")
    
    # ─── 5. VERIFICAR JANELAS RAIZ ───
    print("\n[5] VERIFICAÇÃO DE JANELAS RAIZ (DUAL ROOT)")
    print("-" * 40)
    
    dual = verificar_dual_root()
    if dual["conflito"]:
        print("  🔴 CONFLITO CRÍTICO: Duas janelas raiz detectadas!")
        print(f"     main_window.py linha {dual.get('main_window_linha', '?')}: "
              f"{dual.get('main_window_trecho', '?')}")
        print(f"     dark_window.py linha {dual.get('dark_window_linha', '?')}: "
              f"{dual.get('dark_window_trecho', '?')}")
        print("     ⚠️ Isso causa conflito de mainloop — uma janela 'rouba' eventos da outra")
    else:
        print("  ✓ Nenhum conflito de janela raiz detectado")
    
    # ─── 6. VERIFICAR FUNÇÕES DUPLICADAS ───
    print("\n[6] FUNÇÕES DUPLICADAS EM derived_repo.py")
    print("-" * 40)
    
    dup = verificar_derived_repo_duplicadas()
    if dup["total_duplicadas"] > 0:
        print(f"  ⚠️ {dup['total_duplicadas']} funções duplicadas encontradas:")
        for d in dup["duplicadas"]:
            print(f"     - {d['nome']}: {d['total']}x (linhas {d['linhas']})")
        print("     ⚠️ A segunda definição sobrescreve a primeira!")
    else:
        print("  ✓ Nenhuma função duplicada em derived_repo.py")
    
    # ─── 7. RESUMO ───
    print("\n" + SEPARADOR)
    print("  RESUMO DO DIAGNÓSTICO")
    print(SEPARADOR)
    
    problemas = []
    
    if not tem_dados_recentes:
        problemas.append("🔴 Dados RTD não estão chegando ao banco (sem registros nas últimas 24h)")
    
    for info in conexoes_ui:
        if info["existe"] and info["tem_execute"] and not info["tem_commit"]:
            problemas.append(f"🟠 {info['arquivo']}: execute() sem commit()")
    
    if dual["conflito"]:
        problemas.append("🔴 Duas janelas raiz (tk.Tk + ctk.CTk) — conflito de mainloop")
    
    if dup["total_duplicadas"] > 0:
        problemas.append(f"🟠 derived_repo.py: {dup['total_duplicadas']} funções duplicadas")
    
    if problemas:
        print("\nProblemas encontrados:")
        for i, p in enumerate(problemas, 1):
            print(f"  {i}. {p}")
        print(f"\n⚠️ Total: {len(problemas)} problema(s) precisam de correção.")
        print("   Execute: python scripts/fix_critical_commits.py")
        print("   Execute: python scripts/fix_dual_root.py")
    else:
        print("\n✓ Nenhum problema crítico detectado.")
    
    return 0 if not problemas else 1


if __name__ == "__main__":
    sys.exit(main())
