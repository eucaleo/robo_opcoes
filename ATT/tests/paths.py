# tests/paths.py
# Centraliza os caminhos do projeto — importável por qualquer test file

import sys
from pathlib import Path

# ATT/tests/ -> ATT/ -> projeto/
ATT_ROOT     = Path(__file__).resolve().parent.parent   # C:/users/eucal/projeto/ATT
PROJECT_ROOT = ATT_ROOT.parent                           # C:/users/eucal/projeto

# Garante imports do projeto raiz (UI, dados, etc.)
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Caminhos centralizados
DB_PATH = PROJECT_ROOT / "dados" / "derived.db"
