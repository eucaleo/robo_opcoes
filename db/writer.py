# db/writer.py
"""
Writer para persistência de dados derivados no SQLite.
"""
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

class PayoffWriter:
    """Escritor para pontos do payoff curve e decisões estruturais."""
    
    def __init__(self, db_path: str = "dados/derived.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        """Inicializa o banco com o schema."""
        from .schema import SCHEMA_SQL
        
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript(SCHEMA_SQL)
    
    def save_payoff_points(self, 
                          timestamp: str,
                          aba: str,
                          points: List[Dict[str, Any]],
                          spot_ref: Optional[float] = None,
                          meta: Optional[Dict] = None) -> int:
        """
        Salva pontos do payoff curve.
        
        Args:
            timestamp: Timestamp da captura (ISO format)
            aba: Nome da aba/estratégia
            points: Lista de pontos [(spot, pl), ...]
            spot_ref: Spot de referência (atual)
            meta: Metadados adicionais
            
        Returns:
            Número de pontos inseridos
        """
        if not points:
            return 0
        
        meta = dict(meta) if meta else {}
        if spot_ref is not None:
            meta.setdefault('spot_ref', spot_ref)
        meta_json = json.dumps(meta) if meta else None
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            records = []
            for point in points:
                if isinstance(point, (list, tuple)) and len(point) >= 2:
                    spot, pl = point[0], point[1]
                elif isinstance(point, dict):
                    spot = point.get('spot') or point.get('x')
                    pl = point.get('pl') or point.get('y')
                else:
                    continue
                
                records.append((
                    timestamp, aba, float(spot), float(pl), meta_json
                ))
            
            cursor.executemany("""
                INSERT INTO payoff_curve_points 
                (timestamp, aba, point_spot, point_pl, meta_json)
                VALUES (?, ?, ?, ?, ?)
            """, records)
            
            return len(records)
    
    def save_structure_decision(self,
                           timestamp: str,
                           aba: str,
                           decision: str,
                           ratio: Optional[float] = None,
                           dte_min: Optional[int] = None,
                           pl_atual: Optional[float] = None,
                           pl_max: Optional[float] = None,
                           pl_min: Optional[float] = None,
                           spread_pct_medio: Optional[float] = None,
                           why: Optional[Dict] = None) -> int:
        """
        DEPRECATED: Use db.derived_repo.write_decision_snapshot_atomic()
        Mantido para compatibilidade, mas agora usa Política A.
        """
        import warnings
        warnings.warn(
            "PayoffWriter.save_structure_decision está deprecated. "
            "Use db.derived_repo.write_decision_snapshot_atomic() diretamente.",
            DeprecationWarning,
            stacklevel=2
        )
        
        from db.derived_repo import get_derived_connection, write_decision_snapshot_atomic
        
        decision_dict = {
            "decision": decision,
            "ratio": ratio,
            "dte_min": dte_min,
            "pl_atual": pl_atual,
            "pl_max": pl_max,
            "pl_min": pl_min,
            "spread_pct_medio": spread_pct_medio,
            "why": why
        }
        
        conn = get_derived_connection()
        try:
            return write_decision_snapshot_atomic(conn, timestamp, aba, decision_dict)
        finally:
            conn.close()


    def get_latest_decision(self, aba: str) -> Optional[Dict]:
        """Retorna a última decisão para uma aba."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM structure_decisions 
                WHERE aba = ? 
                ORDER BY timestamp DESC, id DESC 
                LIMIT 1
            """, (aba,))
            
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_payoff_history(self, aba: str, limit: int = 100) -> List[Dict]:
        """Retorna histórico de payoff points para uma aba."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT timestamp, spot_ref, point_spot, point_pl, meta_json
                FROM payoff_curve_points 
                WHERE aba = ? 
                ORDER BY timestamp DESC, id DESC 
                LIMIT ?
            """, (aba, limit))
            
            return [dict(row) for row in cursor.fetchall()]
