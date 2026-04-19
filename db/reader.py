# db/reader.py
"""
Reader para análise de dados derivados do SQLite.
"""
import sqlite3
import json
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path

class PayoffReader:
    """Leitor para análise de pontos do payoff curve e decisões estruturais."""
    
    def __init__(self, db_path: str = "data/derived.db"):
        self.db_path = Path(db_path)
    
    def _get_connection(self):
        """Retorna conexão com row factory configurada."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def get_payoff_curve(self, aba: str, timestamp: Optional[str] = None) -> pd.DataFrame:
        """
        Retorna pontos do payoff curve como DataFrame.
        
        Args:
            aba: Nome da aba/estratégia
            timestamp: Timestamp específico (None = mais recente)
            
        Returns:
            DataFrame com colunas [spot, pl, timestamp, spot_ref]
        """
        with self._get_connection() as conn:
            if timestamp:
                query = """
                    SELECT point_spot as spot, point_pl as pl, 
                           timestamp, spot_ref, meta_json
                    FROM payoff_curve_points 
                    WHERE aba = ? AND timestamp = ?
                    ORDER BY point_spot
                """
                params = (aba, timestamp)
            else:
                # Pega o timestamp mais recente
                query = """
                    SELECT point_spot as spot, point_pl as pl, 
                           timestamp, spot_ref, meta_json
                    FROM payoff_curve_points 
                    WHERE aba = ? AND timestamp = (
                        SELECT MAX(timestamp) FROM payoff_curve_points WHERE aba = ?
                    )
                    ORDER BY point_spot
                """
                params = (aba, aba)
            
            df = pd.read_sql_query(query, conn, params=params)
            
            # Parse meta_json se existir
            if 'meta_json' in df.columns:
                df['meta'] = df['meta_json'].apply(
                    lambda x: json.loads(x) if x else None
                )
                df = df.drop('meta_json', axis=1)
            
            return df
    
    def get_decision_history(self, aba: str, days_back: int = 30) -> pd.DataFrame:
        """
        Retorna histórico de decisões como DataFrame.
        
        Args:
            aba: Nome da aba/estratégia
            days_back: Número de dias para retroceder
            
        Returns:
            DataFrame com histórico de decisões
        """
        cutoff_date = (datetime.now() - timedelta(days=days_back)).isoformat()
        
        with self._get_connection() as conn:
            query = """
                SELECT timestamp, decision, ratio, dte_min, 
                       pl_atual, pl_max, pl_min, spread_pct_medio, 
                       why_json, created_at
                FROM structure_decisions 
                WHERE aba = ? AND timestamp >= ?
                ORDER BY timestamp DESC
            """
            
            df = pd.read_sql_query(query, conn, params=(aba, cutoff_date))
            
            # Parse why_json se existir
            if 'why_json' in df.columns:
                df['why'] = df['why_json'].apply(
                    lambda x: json.loads(x) if x else None
                )
                df = df.drop('why_json', axis=1)
            
            return df
    
    def get_pl_metrics(self, aba: str, days_back: int = 7) -> Dict[str, Any]:
        """
        Calcula métricas de P&L para uma aba.
        
        Args:
            aba: Nome da aba/estratégia
            days_back: Período para análise
            
        Returns:
            Dict com métricas calculadas
        """
        df = self.get_decision_history(aba, days_back)
        
        if df.empty:
            return {"error": "Sem dados no período"}
        
        metrics = {
            "period_days": days_back,
            "total_decisions": len(df),
            "decision_types": df['decision'].value_counts().to_dict(),
        }
        
        # Métricas de P&L se disponíveis
        if 'pl_atual' in df.columns and df['pl_atual'].notna().any():
            pl_values = df['pl_atual'].dropna()
            metrics.update({
                "pl_current": pl_values.iloc[0] if len(pl_values) > 0 else None,
                "pl_mean": pl_values.mean(),
                "pl_std": pl_values.std(),
                "pl_min_period": pl_values.min(),
                "pl_max_period": pl_values.max(),
            })
        
        # Métricas de ratio se disponíveis
        if 'ratio' in df.columns and df['ratio'].notna().any():
            ratio_values = df['ratio'].dropna()
            metrics.update({
                "ratio_current": ratio_values.iloc[0] if len(ratio_values) > 0 else None,
                "ratio_mean": ratio_values.mean(),
                "ratio_changes": len(ratio_values.unique()) - 1,
            })
        
        return metrics
    
    def get_payoff_evolution(self, aba: str, timestamps: List[str]) -> Dict[str, pd.DataFrame]:
        """
        Retorna evolução do payoff curve em múltiplos timestamps.
        
        Args:
            aba: Nome da aba/estratégia
            timestamps: Lista de timestamps para comparar
            
        Returns:
            Dict mapeando timestamp -> DataFrame do payoff
        """
        result = {}
        
        for ts in timestamps:
            df = self.get_payoff_curve(aba, ts)
            if not df.empty:
                result[ts] = df
        
        return result
    
    def get_available_abas(self) -> List[str]:
        """Retorna lista de abas com dados disponíveis."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Abas com pontos de payoff
            cursor.execute("SELECT DISTINCT aba FROM payoff_curve_points ORDER BY aba")
            payoff_abas = set(row[0] for row in cursor.fetchall())
            
            # Abas com decisões
            cursor.execute("SELECT DISTINCT aba FROM structure_decisions ORDER BY aba")
            decision_abas = set(row[0] for row in cursor.fetchall())
            
            # União de ambas
            all_abas = sorted(payoff_abas.union(decision_abas))
            return all_abas
    
    def get_latest_timestamps(self, aba: str, limit: int = 10) -> List[str]:
        """Retorna os timestamps mais recentes para uma aba."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT DISTINCT timestamp 
                FROM payoff_curve_points 
                WHERE aba = ? 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (aba, limit))
            
            return [row[0] for row in cursor.fetchall()]
