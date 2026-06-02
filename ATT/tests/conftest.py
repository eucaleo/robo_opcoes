# tests/conftest.py
import sys
from pathlib import Path

# tests/ -> ATT/ -> projeto/
_TESTS_DIR   = Path(__file__).resolve().parent          # ATT/tests
_ATT_ROOT    = _TESTS_DIR.parent                        # ATT/
PROJECT_ROOT = _ATT_ROOT.parent                         # projeto/

# Injeta projeto/ no sys.path para que UI, dados, etc. sejam importáveis
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Injeta ATT/ no sys.path para que `tests.paths` seja importável
if str(_ATT_ROOT) not in sys.path:
    sys.path.insert(0, str(_ATT_ROOT))

DB_PATH = PROJECT_ROOT / "dados" / "derived.db"

print(f"\n[conftest] PROJECT_ROOT : {PROJECT_ROOT}")
print(f"[conftest] DB_PATH      : {DB_PATH}")
print(f"[conftest] DB existe?   : {DB_PATH.exists()}")
