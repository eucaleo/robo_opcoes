#!/usr/bin/env python3
"""
Teste das funções de inserção de dados derivados.
"""

import sqlite3
import sys
import os
from datetime import datetime, timedelta

# Adicionar o diretório pai ao path para importar os módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from db.derived_repo import (
    insert_payoff_points,
    insert_structure_decision,
    get_latest_decisions,
    get_payoff_points,
    cleanup_old_payoff_data
)

def test_derived_inserts():
    """Testa inserções nas tabelas derivadas."""
    
    # Conectar ao banco (pode usar :memory: para teste)
    db_path = "test_derived.db"
    conn = sqlite3.connect(db_path)
    
    try:
        # Timestamp base para os testes
        base_time = datetime.now()
        timestamp = base_time.isoformat()
        
        print(f"🧪 Testando inserções derivadas - {timestamp}")
        
        # === TESTE 1: Inserir pontos de payoff ===
        print("\n📈 Teste 1: Inserindo pontos de payoff...")
        
        # Simular curva de payoff (estrutura comprada)
        payoff_points = []
        spot_base = 100.0
        
        for i in range(50, 151):  # 50% a 150% do spot
            s_t = spot_base * (i / 100.0)
            
            # Payoff simulado de uma operação comprada
            if s_t < 90:
                pl_venc = -(100 - s_t) * 10  # Perda limitada
            elif s_t < 110:
                pl_venc = (s_t - 90) * 5    # Zona de recuperação
            else:
                pl_venc = (s_t - 90) * 15   # Ganho exponencial
                
            payoff_points.append({
                's_t': s_t,
                'pl_venc': pl_venc
            })
        
        # Inserir pontos
        count_inserted = insert_payoff_points(
            conn=conn,
            timestamp=timestamp,
            aba="TESTE_IRON_CONDOR",
            points=payoff_points,
            spot_ref=spot_base,
            meta={
                "strategy": "iron_condor",
                "legs": 4,
                "max_risk": 1000,
                "max_profit": 300
            }
        )
        
        print(f"   ✅ {count_inserted} pontos inseridos para TESTE_IRON_CONDOR")
        
        # === TESTE 2: Inserir decisões ===
        print("\n🎯 Teste 2: Inserindo decisões...")
        
        # Decisão 1: HOLD (nível baixo)
        decision_1 = {
            'decision': 'HOLD',
            'level': 1,
            'pl_atual': 50.0,
            'pl_max': 300.0,
            'pl_pct_of_max': 0.167,
            'dte_min': 15,
            'spot_atual': 105.2,
            'volatilidade': 0.25,
            'motivo': 'PL abaixo de 30% do máximo'
        }
        
        id_1 = insert_structure_decision(
            conn=conn,
            timestamp=timestamp,
            aba="TESTE_IRON_CONDOR",
            decision_dict=decision_1
        )
        
        print(f"   ✅ Decisão HOLD inserida (ID: {id_1})")
        
        # Decisão 2: CLOSE_REOPEN (nível alto) 
        decision_2 = {
            'decision': 'CLOSE_REOPEN',
            'level': 3,
            'pl_atual': 240.0,
            'pl_max': 300.0,
            'pl_pct_of_max': 0.80,
            'dte_min': 12,
            'spot_atual': 108.7,
            'volatilidade': 0.18,
            'motivo': 'PL atingiu 80% do máximo'
        }
        
        timestamp_2 = (base_time + timedelta(minutes=10)).isoformat()
        
        id_2 = insert_structure_decision(
            conn=conn,
            timestamp=timestamp_2,
            aba="TESTE_IRON_CONDOR",
            decision_dict=decision_2
        )
        
        print(f"   ✅ Decisão CLOSE_REOPEN inserida (ID: {id_2})")
        
        # === TESTE 3: Consultar dados inseridos ===
        print("\n📋 Teste 3: Consultando dados...")
        
        # Buscar decisões recentes
        recent_decisions = get_latest_decisions(conn, limit=5)
        print(f"   📊 {len(recent_decisions)} decisões encontradas:")
        
        for dec in recent_decisions:
            print(f"      - {dec['aba']}: {dec['decision']} (nível {dec['level']}) @ {dec['timestamp'][:19]}")
        
        # Buscar pontos de payoff
        payoff_data = get_payoff_points(conn, "TESTE_IRON_CONDOR", timestamp)
        print(f"   📈 {len(payoff_data)} pontos de payoff encontrados")
        
        if payoff_data:
            first_point = payoff_data[0]
            last_point = payoff_data[-1]
            print(f"      - Primeiro: S_T={first_point['s_t']}, PL={first_point['pl_venc']}")
            print(f"      - Último: S_T={last_point['s_t']}, PL={last_point['pl_venc']}")
        
        # === TESTE 4: Limpeza (opcional) ===
        print("\n🧹 Teste 4: Testando limpeza de dados antigos...")
        
        # Simular dados antigos
        old_timestamp = (base_time - timedelta(days=35)).isoformat()
        insert_payoff_points(
            conn=conn,
            timestamp=old_timestamp,
            aba="TESTE_OLD_DATA",
            points=[{'s_t': 100, 'pl_venc': 0}],
            spot_ref=100.0
        )
        
        deleted = cleanup_old_payoff_data(conn, days_to_keep=30)
        print(f"   🗑️  {deleted} registros antigos removidos")
        
        print(f"\n🎉 Todos os testes concluídos com sucesso!")
        print(f"   📁 Banco de teste salvo em: {os.path.abspath(db_path)}")
        
    except Exception as e:
        print(f"❌ Erro durante os testes: {e}")
        raise
        
    finally:
        conn.close()

if __name__ == "__main__":
    test_derived_inserts()
