# test_payoff_system.py
"""
Script de teste para o sistema de captura de payoff.
Demonstra todas as funcionalidades implementadas.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from db.derived_repo import
import json

# Importa o sistema
from payoff_capture import PayoffCapture, capture_payoff_data, capture_strategy_decision
from db import get_reader, get_writer

def test_basic_functionality():
    """Teste básico de funcionalidades."""
    print("🔧 Testando funcionalidades básicas...")
    
    # Cria capturador
    capture = PayoffCapture()
    
    # Cria dados de teste simulando payoff curve
    spots = np.linspace(4800, 5200, 50)
    pls = np.sin((spots - 5000) / 100) * 1000 + np.random.normal(0, 50, 50)
    
    df_test = pd.DataFrame({
        'spot': spots,
        'pl': pls
    })
    
    # Testa captura de payoff
    timestamp = datetime.now().isoformat()
    points_saved = capture.capture_from_dataframe(
        df=df_test,
        aba="TEST_IRON_CONDOR",
        timestamp=timestamp,
        spot_ref=5000.0,
        meta={'test': True, 'strategy': 'iron_condor'}
    )
    
    print(f"✅ Salvos {points_saved} pontos do payoff")
    
    # Testa captura de decisão
    decision_id = capture.capture_decision(
        aba="TEST_IRON_CONDOR",
        decision="HOLD",
        context={
            'ratio': 0.85,
            'dte_min': 15,
            'pl_atual': 250.0,
            'pl_max': 300.0,
            'pl_min': -100.0,
            'spread_pct_medio': 2.5,
            'why': {'reason': 'Within profit zone', 'confidence': 0.8}
        },
        timestamp=timestamp
    )
    
    print(f"✅ Decisão salva com ID: {decision_id}")
    
    return timestamp

def test_data_retrieval(timestamp):
    """Teste de recuperação de dados."""
    print("\n📊 Testando recuperação de dados...")
    
    reader = get_reader()
    
    # Testa recuperação do payoff
    payoff_df = reader.get_payoff_curve("TEST_IRON_CONDOR", timestamp)
    print(f"✅ Recuperados {len(payoff_df)} pontos do payoff")
    print(f"   Spot range: {payoff_df['spot'].min():.1f} - {payoff_df['spot'].max():.1f}")
    print(f"   PL range: {payoff_df['pl'].min():.1f} - {payoff_df['pl'].max():.1f}")
    
    # Testa recuperação de decisões
    decisions_df = reader.get_decision_history("TEST_IRON_CONDOR", days_back=1)
    print(f"✅ Recuperadas {len(decisions_df)} decisões")
    
    if not decisions_df.empty:
        latest = decisions_df.iloc[0]
        print(f"   Última decisão: {latest['decision']} (ratio: {latest['ratio']})")
    
    # Testa métricas
    metrics = reader.get_pl_metrics("TEST_IRON_CONDOR", days_back=1)
    print(f"✅ Métricas calculadas: {len(metrics)} campos")
    print(f"   P&L atual: {metrics.get('pl_current', 'N/A')}")

def test_integration_example():
    """Exemplo de integração com dados simulados do Excel."""
    print("\n🔄 Testando integração com dados do Excel...")
    
    capture = PayoffCapture()
    
    # Simula dados processados do Excel
    processed_data = {
        'payoff_curve': pd.DataFrame({
            'spot': np.linspace(4900, 5100, 30),
            'pl': np.random.normal(100, 200, 30)
        }),
        'decision': 'ADJUST',
        'ratio': 0.92,
        'dte_min': 8,
        'pl_atual': 150.0,
        'spot_atual': 5025.0,
        'why': {'trigger': 'ratio_threshold', 'target_ratio': 0.85}
    }
    
    # Captura tudo de uma vez
    points, decisions = capture.capture_from_excel_processing(
        processed_data=processed_data,
        aba="TEST_BUTTERFLY"
    )
    
    print(f"✅ Captura integrada: {points} pontos, {decisions} decisões")

def test_analysis_functions():
    """Teste das funções de análise."""
    print("\n📈 Testando funções de análise...")
    
    reader = get_reader()
    
    # Lista abas disponíveis
    abas = reader.get_available_abas()
    print(f"✅ Abas disponíveis: {abas}")
    
    # Para cada aba de teste
    for aba in abas:
        if aba.startswith("TEST_"):
            print(f"\n📋 Análise da aba: {aba}")
            
            # Timestamps disponíveis
            timestamps = reader.get_latest_timestamps(aba, limit=3)
            print(f"   Timestamps: {len(timestamps)} disponíveis")
            
            # Métricas de P&L
            metrics = reader.get_pl_metrics(aba, days_back=1)
            if 'error' not in metrics:
                print(f"   Decisões totais: {metrics.get('total_decisions', 0)}")
                print(f"   P&L atual: {metrics.get('pl_current', 'N/A')}")

def test_convenience_functions():
    """Teste das funções de conveniência."""
    print("\n⚡ Testando funções de conveniência...")
    
    # Usando funções diretas
    test_df = pd.DataFrame({
        'spot': [4950, 5000, 5050],
        'pl': [100, 200, 150]
    })
    
    points = capture_payoff_data(
        df=test_df,
        aba="TEST_CONVENIENCE",
        meta={'source': 'convenience_test'}
    )
    
    decision_id = capture_strategy_decision(
        aba="TEST_CONVENIENCE",
        decision="MONITOR",
        context={'note': 'Testing convenience functions'}
    )
    
    print(f"✅ Funções de conveniência: {points} pontos, decisão ID {decision_id}")

def show_summary():
    """Mostra resumo final."""
    print("\n📊 RESUMO FINAL:")
    
    from payoff_capture import get_capture_summary
    summary = get_capture_summary()
    
    print(f"✅ Total de abas: {summary.get('total_abas', 0)}")
    print(f"✅ Database: {summary.get('db_path', 'N/A')}")
    print(f"✅ Abas com dados: {summary.get('abas', [])}")
    
    if 'capture_stats' in summary:
        print("\n📈 Estatísticas por aba:")
        for aba, stats in summary['capture_stats'].items():
            if isinstance(stats, dict) and 'error' not in stats:
                decisions = stats.get('total_decisions', 0)
                pl_current = stats.get('pl_current', 'N/A')
                print(f"   {aba}: {decisions} decisões, P&L atual: {pl_current}")

def main():
    """Executa todos os testes."""
    print("🚀 TESTANDO SISTEMA DE CAPTURA DE PAYOFF")
    print("=" * 50)
    
    try:
        # Executa testes sequenciais
        timestamp = test_basic_functionality()
        test_data_retrieval(timestamp)
        test_integration_example()
        test_analysis_functions()
        test_convenience_functions()
        show_summary()
        
        print("\n" + "=" * 50)
        print("✅ TODOS OS TESTES CONCLUÍDOS COM SUCESSO!")
        print("✅ Sistema pronto para integração com o código existente!")
                print("\n🧹 Teste 5: Limpando decisions antigas...")
        # Inserir decisão antiga
        old_timestamp_dec = (base_time - timedelta(days=40)).isoformat()
        insert_structure_decision(
            conn=conn,
            timestamp=old_timestamp_dec,
            aba="TESTE_OLD_DECISION",
            decision_dict={'decision': 'HOLD', 'level': 1}
        )
        deleted_dec = cleanup_old_decisions(conn, days_to_keep=30)
        print(f"   🗑️  {deleted_dec} decisões antigas removidas")

        
    except Exception as e:
        print(f"\n❌ ERRO durante os testes: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
