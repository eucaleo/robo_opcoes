#!/usr/bin/env python3
"""
VERIFICAÇÃO DO PIPELINE COMPLETO: RTD → DB → UI
=================================================
Testa cada etapa do fluxo de dados para identificar exatamente
onde está a quebra.

Executar via Git Bash: python scripts/check_rtd_to_ui_pipeline.py
"""

import sqlite3
import sys
from datetime import datetime
from pathlib import Path

PROJETO_RAIZ = Path(r"C:\Users\eucal\projeto")
SEPARADOR = "=" * 70


def encontrar_banco() -> Path | None:
    candidatos = [
        PROJETO_RAIZ / "app.db",
        PROJETO_RAIZ / "db" / "legacy.db",
        PROJETO_RAIZ / "data" / "app.db",
        PROJETO_RAIZ / "ATT" / "app.db",
    ]
    for c in candidatos:
        if c.exists():
            return c
    return None


def etapa_1_rtd_no_banco(conn: sqlite3.Connection) -> dict:
    """ETAPA 1: Dados RTD estão chegando ao banco?"""
    cursor = conn.cursor()
    resultado = {"ok": False, "detalhes": []}
    
    tabelas_rtd = [
        "rtd_option_quotes",
        "rtd_option_quotes_snapshot",
        "rtd_underlying_quotes",
    ]
    
    for tabela in tabelas_rtd:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM [{tabela}]")
            total = cursor.fetchone()[0]
            
            cursor.execute(
                f"SELECT MAX(updated_at) FROM [{tabela}]"
            )
            ultimo = cursor.fetchone()[0]
            
            info = f"{tabela}: {total} registros, último: {ultimo or 'N/A'}"
            resultado["detalhes"].append(info)
            
            if total > 0 and ultimo:
                resultado["ok"] = True
        except sqlite3.OperationalError as e:
            resultado["detalhes"].append(f"{tabela}: ERRO - {e}")
    
    return resultado


def etapa_2_payoff_calculado(conn: sqlite3.Connection) -> dict:
    """ETAPA 2: Payoff está sendo calculado e persistido?"""
    cursor = conn.cursor()
    resultado = {"ok": False, "detalhes": []}
    
    tabelas_payoff = [
        "payoff_curve_points",
        "canonical_payoff_curve_points",
    ]
    
    for tabela in tabelas_payoff:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM [{tabela}]")
            total = cursor.fetchone()[0]
            
            cursor.execute(
                f"SELECT MAX(created_at) FROM [{tabela}]"
            )
            ultimo = cursor.fetchone()[0]
            
            info = f"{tabela}: {total} registros, último: {ultimo or 'N/A'}"
            resultado["detalhes"].append(info)
            
            if total > 0:
                resultado["ok"] = True
        except sqlite3.OperationalError as e:
            resultado["detalhes"].append(f"{tabela}: ERRO - {e}")
    
    return resultado


def etapa_3_snapshots(conn: sqlite3.Connection) -> dict:
    """ETAPA 3: System snapshots estão sendo criados?"""
    cursor = conn.cursor()
    resultado = {"ok": False, "detalhes": []}
    
    try:
        cursor.execute("SELECT COUNT(*) FROM [system_snapshots]")
        total = cursor.fetchone()[0]
        
        cursor.execute(
            "SELECT MAX(created_at) FROM [system_snapshots]"
        )
        ultimo = cursor.fetchone()[0]
        
        resultado["detalhes"].append(
            f"system_snapshots: {total} registros, último: {ultimo or 'N/A'}"
        )
        
        if total > 0:
            resultado["ok"] = True
    except sqlite3.OperationalError as e:
        resultado["detalhes"].append(f"system_snapshots: ERRO - {e}")
    
    return resultado


def etapa_4_ui_leitura(conn: sqlite3.Connection) -> dict:
    """ETAPA 4: A UI consegue ler os dados mais recentes?"""
    cursor = conn.cursor()
    resultado = {"ok": False, "detalhes": []}
    
    # Simular o que a UI lê: buscar payoff mais recente
    try:
        cursor.execute("""
            SELECT structure_id, MAX(created_at) 
            FROM payoff_curve_points 
            GROUP BY structure_id 
            ORDER BY MAX(created_at) DESC 
            LIMIT 5
        """)
        recentes = cursor.fetchall()
        
        if recentes:
            resultado["ok"] = True
            resultado["detalhes"].append("Top 5 structures com payoff mais recente:")
            for struct_id, ts in recentes:
                resultado["detalhes"].append(f"  {struct_id}: {ts}")
        else:
            resultado["detalhes"].append("Nenhum payoff encontrado")
    except sqlite3.OperationalError as e:
        # Tentar tabela alternativa
        try:
            cursor.execute("""
                SELECT structure_id, MAX(created_at) 
                FROM canonical_payoff_curve_points 
                GROUP BY structure_id 
                ORDER BY MAX(created_at) DESC 
                LIMIT 5
            """)
            recentes = cursor.fetchall()
            if recentes:
                resultado["ok"] = True
                resultado["detalhes"].append("Top 5 structures (canonical):")
                for struct_id, ts in recentes:
                    resultado["detalhes"].append(f"  {struct_id}: {ts}")
        except sqlite3.OperationalError:
            resultado["detalhes"].append(f"ERRO: {e}")
    
    return resultado


def main():
    print(SEPARADOR)
    print("  VERIFICAÇÃO DO PIPELINE: RTD → DB → UI")
    print(f"  Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(SEPARADOR)
    
    banco = encontrar_banco()
    if not banco:
        print("\n❌ ERRO CRÍTICO: Nenhum banco de dados encontrado!")
        return 1
    
    print(f"\n📁 Banco: {banco}")
    print(f"   Tamanho: {banco.stat().st_size / (1024*1024):.2f} MB")
    
    conn = sqlite3.connect(str(banco))
    
    etapas = [
        ("RTD → Banco", etapa_1_rtd_no_banco(conn)),
        ("Cálculo Payoff", etapa_2_payoff_calculado(conn)),
        ("System Snapshots", etapa_3_snapshots(conn)),
        ("UI → Leitura", etapa_4_ui_leitura(conn)),
    ]
    
    todas_ok = True
    for nome, resultado in etapas:
        status = "✅" if resultado["ok"] else "❌"
        print(f"\n[{status}] ETAPA: {nome}")
        for detalhe in resultado["detalhes"]:
            print(f"     {detalhe}")
        if not resultado["ok"]:
            todas_ok = False
    
    conn.close()
    
    print(f"\n{SEPARADOR}")
    if todas_ok:
        print("  ✅ Pipeline completo funcionando")
    else:
        print("  ❌ Pipeline QUEBRADO — verificar etapas com ❌ acima")
    print(SEPARADOR)
    
    return 0 if todas_ok else 1


if __name__ == "__main__":
    sys.exit(main())
