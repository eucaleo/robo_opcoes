"""
patch_31 -- Fix UI/models/__init__.py

Histórico:
  O arquivo foi criado com typo: __ini__.py
  A correção manual já foi aplicada.
  Este patch valida o estado atual e documenta formalmente.

Critérios de aceite:
  [OK] UI/models/__init__.py existe
  [OK] UI/models/__ini__.py NÃO existe
  [OK] import UI.models funciona sem erro
  [OK] Backup do estado salvo em BAK/
"""

import sys
import shutil
from pathlib import Path
from datetime import datetime

#  Paths 
RAIZ      = Path(__file__).resolve().parent.parent.parent
UI_MODELS = RAIZ / "UI" / "models"
INIT_OK   = UI_MODELS / "__init__.py"
INIT_TYPO = UI_MODELS / "__ini__.py"
BAK_DIR   = RAIZ / "BAK"
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

erros = []

print("=" * 55)
print("  patch_31 -- Fix UI/models/__init__.py")
print(f"  Raiz : {RAIZ}")
print("=" * 55)

#  1. Verifica se o __init__.py correto existe 
print("\n[1] Verificando UI/models/__init__.py ...")
if INIT_OK.exists():
    print(f"  [OK]  {INIT_OK.relative_to(RAIZ)} existe")
else:
    print(f"  [FALHOU]  {INIT_OK.relative_to(RAIZ)} NÃO encontrado")
    print("      Criando arquivo vazio...")
    UI_MODELS.mkdir(parents=True, exist_ok=True)
    INIT_OK.write_text(
        "# UI/models/__init__.py\n# Corrigido via patch_31\n",
        encoding="utf-8"
    )
    if INIT_OK.exists():
        print(f"  [OK]  Criado: {INIT_OK.relative_to(RAIZ)}")
    else:
        erros.append("__init__.py não pôde ser criado")

#  2. Verifica se o typo ainda existe e remove 
print("\n[2] Verificando UI/models/__ini__.py (typo) ...")
if INIT_TYPO.exists():
    # Faz backup antes de remover
    BAK_DIR.mkdir(exist_ok=True)
    bak_dest = BAK_DIR / f"__ini__backup_{TIMESTAMP}.py"
    shutil.copy2(INIT_TYPO, bak_dest)
    print(f"  [SAVE]  Backup salvo: {bak_dest.relative_to(RAIZ)}")
    INIT_TYPO.unlink()
    if not INIT_TYPO.exists():
        print(f"  [OK]  Typo removido: {INIT_TYPO.relative_to(RAIZ)}")
    else:
        erros.append("__ini__.py não pôde ser removido")
else:
    print(f"  [OK]  Typo __ini__.py já foi removido (correção manual aplicada)")

#  3. Valida importação do módulo UI.models 
print("\n[3] Validando import UI.models ...")
sys.path.insert(0, str(RAIZ))
try:
    import importlib
    mod = importlib.import_module("UI.models")
    print(f"  [OK]  import UI.models OK -- {mod.__file__}")
except Exception as e:
    print(f"  [FALHOU]  import UI.models FALHOU: {e}")
    erros.append(f"import UI.models: {e}")

#  4. Resultado final 
print("\n" + "=" * 55)
if erros:
    print(f"  [FALHOU]  patch_31 FALHOU -- {len(erros)} erro(s):")
    for e in erros:
        print(f"     * {e}")
    sys.exit(1)

print("  [OK]  patch_31 CONCLUÍDO com sucesso")
print("  Próximo: patch_32 -- auditoria wiring UI")
print("=" * 55)
sys.exit(0)
