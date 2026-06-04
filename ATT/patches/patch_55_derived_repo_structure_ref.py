import os, shutil, sys

ROOT   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET = os.path.join(ROOT, "db", "derived_repo.py")
BAK    = os.path.join(ROOT, "BAK", "derived_repo.py.bak_patch55")
SENTINEL = "# patch_55:StructureRef"

IMP = [
    "# patch_55:StructureRef",
    "try:",
    "    from src.domain.refs.structure_ref import StructureRef as _StructureRef",
    "except ImportError:",
    "    _StructureRef = None  # type: ignore",
]
IMPORT_BLOCK = "\n".join(IMP)

def read(p):
    with open(p, encoding="utf-8") as f: return f.read()

def write(p, c):
    with open(p, "w", encoding="utf-8") as f: f.write(c)

def apply(dry_run=False):
    src = read(TARGET)
    if SENTINEL in src:
        print("  patch_55 ja aplicado.")
        return True
    NL = chr(10)
    idx = src.rfind("from typing import")
    if idx == -1:
        print("ERRO: ancora typing nao encontrada")
        return False
    eol = src.find(NL, idx)
    src = src[:eol+1] + NL + IMPORT_BLOCK + NL + src[eol+1:]
    ANCHOR = "def _extract_ts_aba("
    idx2 = src.find(ANCHOR)
    if idx2 == -1:
        print("ERRO: _extract_ts_aba nao encontrado")
        return False
    zone = src[idx2:idx2+800]
    pos = -1
    for mk in ("ts  =", "ts ="):
        p2 = zone.find(mk)
        if p2 != -1: pos = idx2 + p2; break
    if pos == -1:
        print("ERRO: corpo _extract_ts_aba nao localizado")
        print("TRECHO:", repr(zone[:400]))
        return False
    ls = src.rfind(NL, 0, pos) + 1
    ind = ""
    for ch in src[ls:]:
        if ch in (" ", "\t"): ind += ch
        else: break
    i1 = ind
    i2 = ind + "    "
    i3 = ind + "        "
    g = (NL
        + i1 + "# patch_55: desempacotar StructureRef" + NL
        + i1 + "if _StructureRef is not None and isinstance(aba, _StructureRef):" + NL
        + i2 + "_ref = aba" + NL
        + i2 + "aba  = _ref.aba" + NL
        + i2 + "if _ref.structure_id is not None:" + NL
        + i3 + "decision_dict = dict(decision_dict)" + NL
        + i3 + "decision_dict[chr(34)+\"structure_id\"+chr(34)] = _ref.structure_id" + NL
        + NL)
    src = src[:ls] + g + src[ls:]
    OLD = "        if aba is not None:"
    NEW = ("        # patch_55: StructureRef guard" + NL
           + "        if _StructureRef is not None and isinstance(aba, _StructureRef):" + NL
           + "            aba = aba.aba" + NL
           + "        if aba is not None:")
    if OLD in src: src = src.replace(OLD, NEW, 1)
    else: print("AVISO: ancora get_recent nao encontrada")
    if dry_run:
        print("  [dry-run] OK")
        return True
    os.makedirs(os.path.join(ROOT, "BAK"), exist_ok=True)
    shutil.copy2(TARGET, BAK)
    write(TARGET, src)
    print("  patch_55 aplicado com sucesso")
    return True

if __name__ == "__main__":
    dry = "--dry-run" in sys.argv
    sys.exit(0 if apply(dry_run=dry) else 1)
