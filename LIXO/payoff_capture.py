# payoff_capture.py
"""
Módulo de captura automática de dados derivados do payoff.
Integra com o sistema existente para persistir dados no SQLite.
"""

import pandas as pd
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import logging

# Importa o sistema de DB
from db import save_payoff, save_decision, get_writer, get_reader

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PayoffCapture:
    """Capturador de dados derivados do payoff."""
    
    def __init__(self, db_path: str = "data/derived.db"):
        self.db_path = db_path
        self.writer = get_writer(db_path)
        self.reader = get_reader(db_path)
        logger.info(f"PayoffCapture inicializado com DB: {db_path}")
    
    def capture_from_dataframe(self, 
                              df: pd.DataFrame, 
                              aba: str,
                              spot_col: str = 'spot',
                              pl_col: str = 'pl',
                              timestamp: Optional[str] = None,
                              spot_ref: Optional[float] = None,
                              meta: Optional[Dict] = None) -> int:
        """
        Captura pontos do payoff de um DataFrame.
        
        Args:
            df: DataFrame com dados do payoff
            aba: Nome da aba/estratégia
            spot_col: Nome da coluna com preços spot
            pl_col: Nome da coluna com P&L
            timestamp: Timestamp (None = agora)
            spot_ref: Spot de referência
            meta: Metadados adicionais
            
        Returns:
            Número de pontos salvos
        """
        if df.empty:
            logger.warning(f"DataFrame vazio para aba {aba}")
            return 0
        
        # Timestamp padrão
        if timestamp is None:
            timestamp = datetime.now().isoformat(timespec="seconds")
        
        # Extrai pontos
        try:
            points = list(zip(df[spot_col], df[pl_col]))
            
            # Adiciona metadados sobre o DataFrame
            if meta is None:
                meta = {}
            
            meta.update({
                'total_points': len(points),
                'spot_range': [float(df[spot_col].min()), float(df[spot_col].max())],
                'pl_range': [float(df[pl_col].min()), float(df[pl_col].max())],
                'capture_method': 'dataframe'
            })
            
            # Salva no SQLite
            count = self.writer.save_payoff_points(
                timestamp=timestamp,
                aba=aba,
                points=points,
                spot_ref=spot_ref,
                meta=meta
            )
            
            logger.info(f"Salvos {count} pontos do payoff para {aba} em {timestamp}")
            return count
            
        except Exception as e:
            logger.error(f"Erro ao capturar payoff de {aba}: {e}")
            return 0
    
    def capture_decision(self,
                        aba: str,
                        decision: str,
                        context: Optional[Dict] = None,
                        timestamp: Optional[str] = None) -> int:
        """
        Captura uma decisão estrutural.
        
        Args:
            aba: Nome da aba/estratégia
            decision: Tipo de decisão (HOLD, CLOSE, ADJUST, etc.)
            context: Contexto com métricas da decisão
            timestamp: Timestamp (None = agora)
            
        Returns:
            ID do registro inserido
        """
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        # Extrai métricas do contexto
        kwargs = {}
        if context:
            kwargs.update({
                'ratio': context.get('ratio'),
                'dte_min': context.get('dte_min'),
                'pl_atual': context.get('pl_atual'),
                'pl_max': context.get('pl_max'),
                'pl_min': context.get('pl_min'),
                'spread_pct_medio': context.get('spread_pct_medio'),
                'why': context.get('why') or context.get('justificativa')
            })
        
        try:
            record_id = self.writer.save_structure_decision(
                timestamp=timestamp,
                aba=aba,
                decision=decision,
                **kwargs
            )
            
            logger.info(f"Decisão '{decision}' salva para {aba} (ID: {record_id})")
            return record_id
            
        except Exception as e:
            logger.error(f"Erro ao salvar decisão para {aba}: {e}")
            return 0
    
    def capture_from_excel_processing(self,
                                     processed_data: Dict,
                                     aba: str,
                                     timestamp: Optional[str] = None) -> Tuple[int, int]:
        """
        Captura dados após processamento do Excel.
        
        Args:
            processed_data: Dados processados do Excel
            aba: Nome da aba
            timestamp: Timestamp (None = agora)
            
        Returns:
            Tuple (pontos_salvos, decisoes_salvas)
        """
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        points_saved = 0
        decisions_saved = 0
        
        # Captura payoff se disponível
        if 'payoff_curve' in processed_data:
            payoff_df = processed_data['payoff_curve']
            if isinstance(payoff_df, pd.DataFrame) and not payoff_df.empty:
                points_saved = self.capture_from_dataframe(
                    df=payoff_df,
                    aba=aba,
                    timestamp=timestamp,
                    spot_ref=processed_data.get('spot_atual'),
                    meta={'source': 'excel_processing'}
                )
        
        # Captura decisão se disponível
        if 'decision' in processed_data:
            decision = processed_data['decision']
            context = {k: v for k, v in processed_data.items() 
                      if k not in ['payoff_curve', 'decision']}
            
            decision_id = self.capture_decision(
                aba=aba,
                decision=decision,
                context=context,
                timestamp=timestamp
            )
            decisions_saved = 1 if decision_id > 0 else 0
        
        logger.info(f"Captura completa para {aba}: {points_saved} pontos, {decisions_saved} decisões")
        return points_saved, decisions_saved
    
    def get_summary(self) -> Dict[str, Any]:
        """Retorna resumo dos dados capturados."""
        try:
            abas = self.reader.get_available_abas()
            
            summary = {
                'total_abas': len(abas),
                'abas': abas,
                'db_path': str(self.db_path),
                'capture_stats': {}
            }
            
            # Stats por aba
            for aba in abas[:5]:  # Limita para não sobrecarregar
                metrics = self.reader.get_pl_metrics(aba, days_back=7)
                summary['capture_stats'][aba] = metrics
            
            return summary
            
        except Exception as e:
            logger.error(f"Erro ao gerar resumo: {e}")
            return {'error': str(e)}

# Instância global
payoff_capture = PayoffCapture()

# Funções de conveniência para integração
def capture_payoff_data(df: pd.DataFrame, aba: str, **kwargs) -> int:
    """Função de conveniência para capturar payoff."""
    return payoff_capture.capture_from_dataframe(df, aba, **kwargs)

def capture_strategy_decision(aba: str, decision: str, context: Dict = None) -> int:
    """Função de conveniência para capturar decisão."""
    return payoff_capture.capture_decision(aba, decision, context)

def get_capture_summary() -> Dict:
    """Função de conveniência para obter resumo."""
    return payoff_capture.get_summary()
