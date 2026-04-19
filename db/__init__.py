# db/__init__.py
"""
Sistema de persistência para dados derivados do payoff.
"""

from .writer import PayoffWriter
from .reader import PayoffReader
from .schema import SCHEMA_SQL

__all__ = ['PayoffWriter', 'PayoffReader', 'SCHEMA_SQL']

# Instância global para facilitar uso
_writer = None
_reader = None

def get_writer(db_path: str = "data/derived.db") -> PayoffWriter:
    """Retorna instância singleton do writer."""
    global _writer
    if _writer is None or _writer.db_path != db_path:
        _writer = PayoffWriter(db_path)
    return _writer

def get_reader(db_path: str = "data/derived.db") -> PayoffReader:
    """Retorna instância singleton do reader."""
    global _reader
    if _reader is None or _reader.db_path != db_path:
        _reader = PayoffReader(db_path)
    return _reader

# Funções de conveniência
def save_payoff(timestamp: str, aba: str, points, **kwargs):
    """Conveniência para salvar pontos do payoff."""
    return get_writer().save_payoff_points(timestamp, aba, points, **kwargs)

def save_decision(timestamp: str, aba: str, decision: str, **kwargs):
    """Conveniência para salvar decisão."""
    return get_writer().save_structure_decision(timestamp, aba, decision, **kwargs)

def get_payoff(aba: str, timestamp=None):
    """Conveniência para obter payoff curve."""
    return get_reader().get_payoff_curve(aba, timestamp)

def get_decisions(aba: str, days_back=30):
    """Conveniência para obter histórico de decisões."""
    return get_reader().get_decision_history(aba, days_back)
