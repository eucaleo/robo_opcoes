"""
patches/_patch_56_worker.py
============================
Worker Python para o patch_56.
Executado pelo apply_patch_56.sh -- NÃO execute diretamente em produção.

Retorna:
  exit 0   tudo OK
  exit 1   erro fatal (arquivo não encontrado, escrita falhou, etc.)
  exit 2   patch já aplicado (idempotente, não é erro)
"""

import re
import sys
import os
import shutil
from datetime import datetime

#  Caminhos 
ROOT          = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))  #  era ".."
SERVICE_FILE  = os.path.join(ROOT, "services", "derived_service.py")
REPO_FILE     = os.path.join(ROOT, "db", "derived_repo.py")
BACKUP_DIR    = os.path.join(ROOT, "ATT", "patches", "backups", "patch_56")
TIMESTAMP     = datetime.now().strftime("%Y%m%d_%H%M%S")


#  Helpers 

def read(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)

def backup(path: str, label: str) -> str:
    os.makedirs(BACKUP_DIR, exist_ok=True)
    dest = os.path.join(BACKUP_DIR, f"{label}_{TIMESTAMP}.py")
    shutil.copy2(path, dest)
    print(f"  [backup] {dest}")
    return dest

def die(msg: str) -> None:
    print(f"\n[FATAL] {msg}", file=sys.stderr)
    sys.exit(1)

def warn(msg: str) -> None:
    print(f"  [WARN]  {msg}")

def ok(msg: str) -> None:
    print(f"  [OK]    {msg}")

#  Verificações iniciais 

print("\n Pré-flight ")

if not os.path.isfile(SERVICE_FILE):
    die(f"Arquivo não encontrado: {SERVICE_FILE}")
ok(f"Encontrado: {SERVICE_FILE}")

if not os.path.isfile(REPO_FILE):
    die(f"Arquivo não encontrado: {REPO_FILE}")
ok(f"Encontrado: {REPO_FILE}")

#  Backup 

print("\n Backup ")
backup(SERVICE_FILE, "derived_service")
backup(REPO_FILE,    "derived_repo")

# =============================================================================
# PATCH A + B    services/derived_service.py
# =============================================================================

print("\n Patch A+B: derived_service.py ")

src_service = read(SERVICE_FILE)
original_service = src_service

already_patched = (
    "col, val = ref.db_pair()" in src_service
    and "StructureRef.from_id(structure_id)" in src_service
)
if already_patched:
    print("  [SKIP] derived_service.py já contém patch_56 -- idempotente")
else:
    #  PATCH A: corrigir get_payoff_by_aba 

    # Localiza a função inteira pelo sinal do bug
    BUG_FSTRING   = "{ref.db_column()}"
    BUG_NAMEVAR   = "(aba,)"

    if BUG_FSTRING in src_service or BUG_NAMEVAR in src_service:
        # Passo 1: garantir que col, val = ref.db_pair() está logo após a def
        if "col, val = ref.db_pair()" not in src_service:
            # Insere após a primeira linha do corpo de get_payoff_by_aba
            src_service = re.sub(
                r'(def get_payoff_by_aba\(ref: StructureRef\):\n'
                r'(?:[ \t]+""".*?"""\n)?)',
                r'\g<1>    col, val = ref.db_pair()  # patch_56\n',
                src_service,
                count=1,
                flags=re.DOTALL,
            )

        # Passo 2: corrigir a f-string (adiciona 'f' antes das triple-quotes da execute)
        src_service = re.sub(
            r'(cursor\.execute\()(""")',
            r'\g<1>f\g<2>',
            src_service,
            count=1,
        )

        # Passo 3: trocar {ref.db_column()}  {col}
        src_service = src_service.replace(
            "{ref.db_column()}",
            "{col}",
        )

        # Passo 4: trocar (aba,)  (val,)  -- apenas dentro de cursor.execute
        src_service = re.sub(
            r'(cursor\.execute\(f?""".*?""",\s*)\(aba,\)',
            r'\g<1>(val,)',
            src_service,
            count=1,
            flags=re.DOTALL,
        )

        ok("Patch A: get_payoff_by_aba corrigido (f-string + val)")
    else:
        warn("Patch A: sinais do bug não encontrados -- talvez já corrigido parcialmente")

    #  PATCH B: migrar get_payoff_by_structure_id 

    OLD_CACHE_BLOCK = re.compile(
        r'def get_payoff_by_structure_id\(structure_id: int\):\n'
        r'    """.*?"""\n'                      # docstring (opcional)
        r'(?:.*?\n)*?'                          # corpo antigo (cache)
        r'    return get_payoff_by_aba\(aba\)',  # última linha do bloco antigo
        re.DOTALL,
    )

    NEW_BY_SID = (
        'def get_payoff_by_structure_id(structure_id: int):\n'
        '    """\n'
        '    patch_56: constrói StructureRef.from_id() em vez de resolver aba via cache.\n'
        '    """\n'
        '    ref = StructureRef.from_id(structure_id)\n'
        '    return get_payoff_by_aba(ref)'
    )

    if "StructureRef.from_id(structure_id)" not in src_service:
        src_service_new, n = OLD_CACHE_BLOCK.subn(NEW_BY_SID, src_service, count=1)
        if n > 0:
            src_service = src_service_new
            ok("Patch B: get_payoff_by_structure_id migrado para StructureRef.from_id()")
        else:
            # Fallback: substitui só o corpo interno se a regex completa não casar
            if "sid_to_aba = {v: k" in src_service:
                old_inner = (
                    "    if not _ABA_CACHE_LOADED:\n"
                    "        _load_aba_cache()\n\n"
                    "    # Inverter o cache para structure_id  aba\n"
                    "    sid_to_aba = {v: k for k, v in _ABA_TO_STRUCTURE_ID.items()}\n"
                    "    aba = sid_to_aba.get(structure_id)\n\n"
                    "    if aba is None:\n"
                    "        return []  # structure_id não mapeado -- retorna lista vazia\n\n"
                    "    return get_payoff_by_aba(aba)"
                )
                new_inner = (
                    "    # patch_56\n"
                    "    ref = StructureRef.from_id(structure_id)\n"
                    "    return get_payoff_by_aba(ref)"
                )
                src_service = src_service.replace(old_inner, new_inner, 1)
                ok("Patch B: fallback -- corpo interno de get_payoff_by_structure_id substituído")
            else:
                warn("Patch B: get_payoff_by_structure_id não encontrada ou já migrada")
    else:
        warn("Patch B: StructureRef.from_id já presente -- pulando")

    if src_service == original_service:
        warn("derived_service.py: NENHUMA alteração foi feita -- verifique manualmente")
    else:
        write(SERVICE_FILE, src_service)
        ok("derived_service.py gravado")

# =============================================================================
# PATCH C + D    db/derived_repo.py
# =============================================================================

print("\n Patch C+D: derived_repo.py ")

src_repo = read(REPO_FILE)
original_repo = src_repo

#  PATCH C: inserir import lazy + _unwrap_aba 

UNWRAP_BLOCK = '''\n#  patch_56: helper de compatibilidade StructureRef  str 
try:
    from src.domain.refs.structure_ref import StructureRef as _StructureRef
except ImportError:
    _StructureRef = None  # compatibilidade se módulo ainda não instalado


def _unwrap_aba(aba_or_ref) -> str:
    """
    patch_56: aceita str ou StructureRef no parâmetro 'aba'.
    Extrai .aba como string canônica quando recebe StructureRef.
    Compatibilidade retroativa: callers que passam str continuam funcionando.
    """
    if _StructureRef is not None and isinstance(aba_or_ref, _StructureRef):
        resolved = aba_or_ref.aba
        if resolved is None:
            raise ValueError(
                f"StructureRef.aba é None -- use StructureRef.from_aba() ou "
                f"verifique o mapeamento. ref={aba_or_ref!r}"
            )
        return resolved
    return aba_or_ref  # já é str (ou None, para wildcards)

# 
'''

if "_unwrap_aba" in src_repo:
    warn("Patch C: _unwrap_aba já presente -- pulando")
else:
    # Insere antes da primeira função standalone definida no módulo
    insert_candidates = [
        r'^def _table_columns',
        r'^def _normalize',
        r'^def ensure_derived_tables',
        r'^def write_',
        r'^def insert_',
        r'^def get_',
    ]
    inserted = False
    for pattern in insert_candidates:
        m = re.search(pattern, src_repo, re.MULTILINE)
        if m:
            pos = m.start()
            src_repo = src_repo[:pos] + UNWRAP_BLOCK + src_repo[pos:]
            ok(f"Patch C: _unwrap_aba inserido antes de '{m.group()}'")
            inserted = True
            break

    if not inserted:
        # Último fallback: após o último import
        import_positions = [m.end() for m in re.finditer(
            r'^(?:import |from )\S+.*', src_repo, re.MULTILINE
        )]
        if import_positions:
            pos = import_positions[-1]
            src_repo = src_repo[:pos] + "\n" + UNWRAP_BLOCK + src_repo[pos:]
            ok("Patch C: _unwrap_aba inserido após último import (fallback)")
        else:
            warn("Patch C: não foi possível localizar ponto de inserção")

#  PATCH D: injetar _unwrap_aba() nas funções standalone 

FUNCS_NORMAL = [
    "write_payoff_snapshot_atomic",
    "write_decision_snapshot_atomic",
    "write_complete_snapshot_atomic",
    "insert_payoff_points",
    "insert_structure_decision",
]

for fname in FUNCS_NORMAL:
    # Só funções standalone (def no início da linha)
    pattern = re.compile(
        rf'^(def {re.escape(fname)}\([^)]*(?:\n[^)]*)*\):[ \t]*\n)'
        rf'([ \t]+)',
        re.MULTILINE,
    )
    m = pattern.search(src_repo)
    if not m:
        warn(f"Patch D: função standalone '{fname}' não encontrada")
        continue

    # Verificar se já tem _unwrap_aba nas próximas 8 linhas
    snippet_start = m.start()
    snippet_end   = snippet_start + 400
    if "_unwrap_aba" in src_repo[snippet_start:snippet_end]:
        warn(f"Patch D: '{fname}' já contém _unwrap_aba -- pulando")
        continue

    inject_line  = f"{m.group(2)}aba = _unwrap_aba(aba)  # patch_56\n"
    src_repo     = src_repo[:m.end()] + inject_line + src_repo[m.end():]
    ok(f"Patch D: _unwrap_aba injetado em '{fname}'")

# get_payoff_points tem aba opcional  guard `if aba is not None`
GP_PATTERN = re.compile(
    r'^(def get_payoff_points\([^)]*(?:\n[^)]*)*\):[ \t]*\n)'
    r'([ \t]+)',
    re.MULTILINE,
)
gp_match = GP_PATTERN.search(src_repo)
if gp_match:
    snippet = src_repo[gp_match.start():gp_match.start() + 400]
    if "_unwrap_aba" in snippet:
        warn("Patch D: 'get_payoff_points' já contém _unwrap_aba -- pulando")
    else:
        indent = gp_match.group(2)
        inject = (
            f"{indent}if aba is not None:\n"
            f"{indent}    aba = _unwrap_aba(aba)  # patch_56\n"
        )
        src_repo = src_repo[:gp_match.end()] + inject + src_repo[gp_match.end():]
        ok("Patch D: _unwrap_aba (guard None) injetado em 'get_payoff_points'")
else:
    warn("Patch D: 'get_payoff_points' standalone não encontrada")

if src_repo == original_repo:
    warn("derived_repo.py: NENHUMA alteração foi feita -- verifique manualmente")
else:
    write(REPO_FILE, src_repo)
    ok("derived_repo.py gravado")

# =============================================================================
# Verificação de sanidade
# =============================================================================

print("\n Sanidade ")

errors = 0

srv = read(SERVICE_FILE)
if "{ref.db_column()}" in srv:
    print("  [FAIL] Bug remanescente: {ref.db_column()} ainda presente em derived_service.py")
    errors += 1
else:
    ok("f-string bug corrigido em derived_service.py")

if "col, val = ref.db_pair()" not in srv:
    print("  [FAIL] col, val = ref.db_pair() ausente em derived_service.py")
    errors += 1
else:
    ok("col, val = ref.db_pair() presente")

if "StructureRef.from_id(structure_id)" not in srv:
    print("  [FAIL] StructureRef.from_id() ausente em get_payoff_by_structure_id")
    errors += 1
else:
    ok("StructureRef.from_id() presente em get_payoff_by_structure_id")

rpo = read(REPO_FILE)
if "_unwrap_aba" not in rpo:
    print("  [FAIL] _unwrap_aba ausente em derived_repo.py")
    errors += 1
else:
    ok("_unwrap_aba presente em derived_repo.py")

print(f"\n  {'[OK] Patch_56 aplicado sem erros.' if errors == 0 else f'[FAIL] {errors} erro(s) de sanidade.'}")
sys.exit(1 if errors > 0 else 0)
