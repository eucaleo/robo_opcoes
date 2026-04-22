#!/usr/bin/env python3
import os
from datetime import datetime
from typing import List, Dict

# Opcional: carregar .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# Importar domain modules
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from domain.payoff import compute_payoff_for_aba, get_app_db_connection
from domain.decision import compute_decision_for_aba
from services.derived_service import init_db, save_payoff_curve, save_decision, cleanup_derived


def get_active_abas() -> List[str]:
    """Busca abas ativas no app.db"""
    conn = get_app_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT aba FROM rtd_analise_robo 
        WHERE aba IS NOT NULL AND aba != ''
        ORDER BY aba
    """)
    abas = [row[0] for row in cursor.fetchall()]
    conn.close()
    return abas


def process_aba_payoff_and_decision(aba: str) -> Dict:
    """Processa uma aba: calcula payoff + decisão + grava no derived.db"""
    timestamp = datetime.now().isoformat()
    result = {"aba": aba, "success": False, "errors": []}
    
    try:
        # 1. Calcular payoff
        payoff_data = compute_payoff_for_aba(aba)
        if not payoff_data:
            result["errors"].append("Não foi possível calcular payoff")
            return result
        
        # 2. Salvar pontos de payoff
        points_count = save_payoff_curve(
            aba=aba,
            points=payoff_data["points"],    # lista de tuplas (point_spot, point_pl)
            spot_ref=payoff_data["spot_ref"],
            meta=payoff_data["meta"],
            timestamp=timestamp
        )
        result["payoff_points"] = points_count
        
        # 3. Calcular decisão
        decision_data = compute_decision_for_aba(
            aba=aba, 
            pl_max=payoff_data["pl_max"]
        )
        
        # 4. Salvar decisão
        decision_id = save_decision(
            aba=aba,
            decision=decision_data,
            timestamp=timestamp
        )
        result["decision_id"] = decision_id
        result["decision"] = decision_data["decision"]
        result["level"] = decision_data["level"]
        result["pl_atual"] = decision_data["pl_atual"]
        result["pl_max"] = payoff_data["pl_max"]
        result["ratio"] = decision_data["pl_pct_of_max"]
        
        result["success"] = True
        
    except Exception as e:
        result["errors"].append(f"Erro no processamento: {str(e)}")
    
    return result


def main():
    print("[DERIVED] Iniciando pipeline derivadas com dados reais...")
    
    # 1. Inicializar derived.db
    init_db()
    print("[DERIVED] derived.db inicializado")
    
    # 2. Buscar abas ativas
    abas = get_active_abas()
    print(f"[DERIVED] {len(abas)} abas encontradas: {abas}")
    
    if not abas:
        print("[DERIVED] Nenhuma aba encontrada no app.db")
        return
    
    # 3. Processar cada aba
    results = []
    for aba in abas:
        print(f"\n[DERIVED] Processando {aba}...")
        result = process_aba_payoff_and_decision(aba)
        results.append(result)
        
        if result["success"]:
            print(f"  [DERIVED] Payoff: {result['payoff_points']} pontos, PL_max: {result['pl_max']:.2f}")
            print(f"  [DERIVED] Decisão: {result['decision']} (nível {result['level']}) - ratio: {result['ratio']*100:.1f}%")
        else:
            print(f"  [DERIVED] Erros: {result['errors']}")
    
    # 4. Resumo
    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]
    
    print(f"\n[DERIVED] RESUMO:")
    print(f"  [DERIVED] Processadas com sucesso: {len(successful)}")
    print(f"  [DERIVED] Falharam: {len(failed)}")
    
    if successful:
        decisions_summary = {}
        for r in successful:
            dec = r["decision"]
            decisions_summary[dec] = decisions_summary.get(dec, 0) + 1
        
        print(f"  [DERIVED] Decisões: {decisions_summary}")
    
    # 5. Limpeza de dados antigos
    deleted = cleanup_derived(days_to_keep=30)
    print(f"[DERIVED] Limpeza: {deleted}")
    
    # Caminho dos DBs para referência
    app_db = "Data/app.db"
    derived_db = os.getenv("DERIVED_DB_PATH", "derived.db")
    print(f"\n[DERIVED] Bancos:")
    print(f"  Raw: {os.path.abspath(app_db)}")
    print(f"  Derived: {os.path.abspath(derived_db)}")


if __name__ == "__main__":
    main()
