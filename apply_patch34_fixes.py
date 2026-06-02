# apply_patch34_fixes.py  (v2 — usa regex para matches robustos)
import re
import sys
from pathlib import Path

TARGET = Path("UI/models/ui_data.py")
src = TARGET.read_text(encoding="utf-8")
original = src

# ------------------------------------------------------------------
# Fix 1 — "key_type" em comentário de _resolve_structure_key
# ------------------------------------------------------------------
src = re.sub(
    r"patch_34: structure_id e sempre INTEGER\. key_type e conn removidos\.",
    "patch_34: structure_id e sempre INTEGER.",
    src,
)

# ------------------------------------------------------------------
# Fix 2 — "aba" no bloco canônico de _build_payoff_colmap
# ------------------------------------------------------------------
src = re.sub(
    r'[ \t]*"aba"\s*:\s*\["aba"\],\s*#\s*fallback\s*\n',
    "",
    src,
)

# ------------------------------------------------------------------
# Fix 3 — Código morto após return em _load_structures
# ------------------------------------------------------------------
src = re.sub(
    r'\n[ \t]*# Fallback: aba\n[ \t]*aba_col = c\.get\("aba"\)\n'
    r'[ \t]*if not aba_col:\n[ \t]*return \[\]\n'
    r'[ \t]*q = \(\s*.*?ORDER BY structure_id"\s*\)\n'
    r'[ \t]*return \[r\["structure_id"\] for r in conn\.execute\(q\)\.fetchall\(\)\]\n',
    "\n",
    src,
    flags=re.DOTALL,
)

# ------------------------------------------------------------------
# Fix 4 — "aba" em PAYOFF_COLUMN_ALIASES (linha 45)
# ------------------------------------------------------------------
src = re.sub(
    r'[ \t]*"aba"\s*:\s*\["aba",\s*"sheet",\s*"tab"\],\s*\n'
    r'(?=[ \t]*"spot")',   # garante que é dentro de PAYOFF_COLUMN_ALIASES
    "",
    src,
)

# ------------------------------------------------------------------
# Fix 5 — Docstring de get_payoff_curve
# ------------------------------------------------------------------
src = src.replace(
    'Aceita structure_id como int-string ("7") ou aba ("BOVA11").',
    'Aceita structure_id como inteiro ou string numerica ("7").\n'
    '        Strings nao-numericas lancam ValueError.',
)

# ------------------------------------------------------------------
# Salvar
# ------------------------------------------------------------------
if src != original:
    TARGET.write_text(src, encoding="utf-8")
    print("✅ Fixes v2 aplicados com sucesso.")
else:
    print("⚠️  Nenhuma alteração detectada — verifique manualmente.")

sys.exit(0)
