# fix_test_isolation.py
"""
Script de correção automática para isolamento de testes tkinter.

Problemas corrigidos:
  1. test_patch35_details_panel.py
     - _build_tk_modules() não retornava nem injetava tkinter.filedialog
     - _TK_MODULES_TO_PURGE não incluía tkinter.filedialog

  2. test_patch36_main_window.py  (sem alteração necessária -- já está correto)

Uso:
    python fix_test_isolation.py
    python fix_test_isolation.py --dry-run   # mostra diffs sem gravar
"""

import sys
import re
import shutil
import argparse
from pathlib import Path

#  Cores para terminal 
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
CYAN   = "\033[96m"
RESET  = "\033[0m"

def ok(msg):    print(f"{GREEN}[v] {msg}{RESET}")
def warn(msg):  print(f"{YELLOW}[AVISO] {msg}{RESET}")
def err(msg):   print(f"{RED}[x] {msg}{RESET}")
def info(msg):  print(f"{CYAN} {msg}{RESET}")


# 
# PATCH 1 -- test_patch35_details_panel.py
# 

TARGET_35 = Path("ATT/tests/test_patch35_details_panel.py")

#  1a. _TK_MODULES_TO_PURGE -- adiciona tkinter.filedialog 
PURGE_OLD = '''\
_TK_MODULES_TO_PURGE = [
    "tkinter",
    "tkinter.ttk",
    "tkinter.scrolledtext",
    "tkinter.messagebox",
    "tkinter.simpledialog",
    "UI.components.details_panel",  # força re-import com fakes corretos
]'''

PURGE_NEW = '''\
_TK_MODULES_TO_PURGE = [
    "tkinter",
    "tkinter.ttk",
    "tkinter.scrolledtext",
    "tkinter.messagebox",
    "tkinter.simpledialog",
    "tkinter.filedialog",           #  patch: evita contaminação entre suítes
    "UI.components.details_panel",  # força re-import com fakes corretos
]'''

#  1b. _build_tk_modules() -- adiciona fd e corrige return 
# Substitui o bloco que começa em "tk.ttk = ttk" até o "return tk, ttk, st, mb, sd"
BUILD_OLD = '''\
    tk.ttk          = ttk
    fd = types.ModuleType("tkinter.filedialog")
    fd.askopenfilename   = lambda *a, **kw: None
    fd.asksaveasfilename = lambda *a, **kw: None
    fd.askdirectory      = lambda *a, **kw: None
    tk.filedialog = fd
    tk.scrolledtext = st

    return tk, ttk, st, mb, sd'''

BUILD_NEW = '''\
    tk.ttk          = ttk
    tk.scrolledtext = st

    fd = types.ModuleType("tkinter.filedialog")
    fd.askopenfilename   = lambda *a, **kw: None
    fd.asksaveasfilename = lambda *a, **kw: None
    fd.askdirectory      = lambda *a, **kw: None
    tk.filedialog = fd

    return tk, ttk, st, mb, sd, fd  #  patch: expõe fd para injeção'''

# Fallback: se o arquivo não tiver o bloco acima (ex: fd ainda não foi adicionado)
BUILD_OLD_FALLBACK = '''\
    tk.ttk          = ttk
    tk.scrolledtext = st

    return tk, ttk, st, mb, sd'''

BUILD_NEW_FALLBACK = '''\
    tk.ttk          = ttk
    tk.scrolledtext = st

    fd = types.ModuleType("tkinter.filedialog")
    fd.askopenfilename   = lambda *a, **kw: None
    fd.asksaveasfilename = lambda *a, **kw: None
    fd.askdirectory      = lambda *a, **kw: None
    tk.filedialog = fd

    return tk, ttk, st, mb, sd, fd  #  patch: expõe fd para injeção'''

#  1c. Desempacotamento -- 5  6 variáveis 
UNPACK_OLD = "_tk, _ttk, _st, _mb, _sd = _build_tk_modules()"
UNPACK_NEW = "_tk, _ttk, _st, _mb, _sd, _fd = _build_tk_modules()  #  patch"

#  1d. Loop de injeção -- adiciona tkinter.filedialog 
INJECT_OLD = '''\
for _name, _mod in [
    ("tkinter",              _tk),
    ("tkinter.ttk",          _ttk),
    ("tkinter.scrolledtext", _st),
    ("tkinter.messagebox",   _mb),
    ("tkinter.simpledialog", _sd),
]:
    sys.modules[_name] = _mod'''

INJECT_NEW = '''\
for _name, _mod in [
    ("tkinter",              _tk),
    ("tkinter.ttk",          _ttk),
    ("tkinter.scrolledtext", _st),
    ("tkinter.messagebox",   _mb),
    ("tkinter.simpledialog", _sd),
    ("tkinter.filedialog",   _fd),   #  patch: evita ImportError em UI.main_window
]:
    sys.modules[_name] = _mod'''


def _apply_substitution(text: str, old: str, new: str, label: str) -> tuple[str, bool]:
    """Aplica substituição simples. Retorna (novo_texto, aplicado)."""
    if old in text:
        return text.replace(old, new, 1), True
    warn(f"  [{label}] bloco não encontrado -- pulando")
    return text, False


def patch_35(content: str) -> tuple[str, list[str]]:
    """Aplica todas as correções no conteúdo do test_patch35. Retorna (novo, [log])."""
    applied = []

    # 1a -- _TK_MODULES_TO_PURGE
    content, ok_ = _apply_substitution(content, PURGE_OLD, PURGE_NEW, "_TK_MODULES_TO_PURGE")
    if ok_:
        applied.append("_TK_MODULES_TO_PURGE  tkinter.filedialog adicionado")

    # 1b -- corpo do _build_tk_modules (tenta variante com fd já presente primeiro)
    content, ok_ = _apply_substitution(content, BUILD_OLD, BUILD_NEW, "_build_tk_modules (variante fd presente)")
    if ok_:
        applied.append("_build_tk_modules  return corrigido (variante fd presente)")
    else:
        content, ok_ = _apply_substitution(content, BUILD_OLD_FALLBACK, BUILD_NEW_FALLBACK, "_build_tk_modules (variante sem fd)")
        if ok_:
            applied.append("_build_tk_modules  fd criado e return corrigido")

    # 1c -- desempacotamento
    if UNPACK_OLD in content:
        content = content.replace(UNPACK_OLD, UNPACK_NEW, 1)
        applied.append("desempacotamento _build_tk_modules: 5  6 variáveis")
    elif UNPACK_NEW in content:
        applied.append("desempacotamento já correto (6 variáveis) -- sem alteração")
    else:
        warn("  [unpack] linha de desempacotamento não encontrada")

    # 1d -- loop de injeção
    content, ok_ = _apply_substitution(content, INJECT_OLD, INJECT_NEW, "loop sys.modules")
    if ok_:
        applied.append("loop injeção sys.modules  tkinter.filedialog adicionado")

    return content, applied


# 
# VERIFICAÇÃO DE IDEMPOTÊNCIA
# 

def already_patched_35(content: str) -> bool:
    """True se todas as 4 correções já estiverem presentes."""
    checks = [
        '"tkinter.filedialog",           #  patch: evita contaminação entre suítes' in content,
        'return tk, ttk, st, mb, sd, fd  #  patch: expõe fd para injeção' in content,
        '_tk, _ttk, _st, _mb, _sd, _fd = _build_tk_modules()' in content,
        '"tkinter.filedialog",   _fd),   #  patch: evita ImportError em UI.main_window' in content,
    ]
    return all(checks)


# 
# RUNNER
# 

def process_file(path: Path, patch_fn, already_fn, dry_run: bool) -> bool:
    """
    Lê, aplica patches, grava (ou simula).
    Retorna True se tudo OK.
    """
    if not path.exists():
        err(f"Arquivo não encontrado: {path}")
        return False

    original = path.read_text(encoding="utf-8")

    if already_fn(original):
        ok(f"{path.name} -- já corrigido (idempotente, sem alteração)")
        return True

    patched, log = patch_fn(original)

    if not log:
        warn(f"{path.name} -- nenhuma substituição aplicada (verifique manualmente)")
        return False

    info(f"{path.name} -- {len(log)} correção(ões):")
    for item in log:
        print(f"    * {item}")

    if dry_run:
        warn("  [dry-run] arquivo NÃO gravado")
        # Mostra diff resumido
        orig_lines = original.splitlines()
        patched_lines = patched.splitlines()
        diffs = [(i+1, o, n) for i,(o,n) in enumerate(zip(orig_lines, patched_lines)) if o != n]
        if diffs:
            info("  Primeiras diferenças linha a linha:")
            for lineno, old_line, new_line in diffs[:8]:
                print(f"    L{lineno:4d} - {old_line.rstrip()}")
                print(f"    L{lineno:4d} + {new_line.rstrip()}")
    else:
        # Backup antes de gravar
        backup = path.with_suffix(".py.bak")
        shutil.copy2(path, backup)
        path.write_text(patched, encoding="utf-8")
        ok(f"  Gravado. Backup em: {backup.name}")

    return True


def run_validation():
    """Executa pytest dos dois arquivos para confirmar resultado."""
    import subprocess
    info("\nExecutando validação automática com pytest...")

    cmd = [
        sys.executable, "-m", "pytest",
        "ATT/tests/test_patch35_details_panel.py",
        "ATT/tests/test_patch36_main_window.py",
        "ATT/tests/test_patch36_details_panel.py",
        "-v", "--tb=line", "-q",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout[-3000:] if len(result.stdout) > 3000 else result.stdout)
    if result.returncode == 0:
        ok("TODOS OS TESTES PASSARAM [v]")
    else:
        err("Ainda há falhas -- verifique o output acima")
    return result.returncode == 0


# 
# MAIN
# 

def main():
    parser = argparse.ArgumentParser(description="Corrige isolamento de testes tkinter")
    parser.add_argument("--dry-run", action="store_true",
                        help="Mostra o que seria feito sem gravar nada")
    parser.add_argument("--no-validate", action="store_true",
                        help="Pula a validação pytest automática")
    args = parser.parse_args()

    print(f"\n{'='*60}")
    print(" fix_test_isolation.py -- Correção automática de isolamento")
    print(f"{'='*60}\n")

    if args.dry_run:
        warn("MODO DRY-RUN -- nenhum arquivo será modificado\n")

    success = process_file(TARGET_35, patch_35, already_patched_35, args.dry_run)

    if not success:
        err("\nCorreção incompleta. Verifique os avisos acima.")
        sys.exit(1)

    if not args.dry_run and not args.no_validate:
        ok_ = run_validation()
        sys.exit(0 if ok_ else 2)
    else:
        print()
        info("Para validar manualmente:")
        print("  python -m pytest ATT/tests/test_patch35_details_panel.py "
              "ATT/tests/test_patch36_main_window.py "
              "ATT/tests/test_patch36_details_panel.py -v --tb=short 2>&1 | tail -10")


if __name__ == "__main__":
    main()
