# ATT/checks/check_patch34.py  (v2 -- fix falso positivo docstring)
"""
Checker cirúrgico para patch_34.
Valida que ui_data.py está no estado canônico correto.
Uso: python ATT/checks/check_patch34.py
"""
import sys
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "UI" / "models" / "ui_data.py"

PASS = "  [OK]"
FAIL = "  [FALHOU]"

results = []


def check(label: str, ok: bool, detail: str = ""):
    results.append((label, ok, detail))
    icon = PASS if ok else FAIL
    msg = f"{icon}  {label}"
    if detail:
        msg += f"\n        -> {detail}"
    print(msg)


def strip_docstrings_and_comments(code: str) -> str:
    """Remove docstrings triplas e comentários de linha do trecho."""
    # Remove docstrings (triple-quoted)
    code = re.sub(r'""".*?"""', "", code, flags=re.DOTALL)
    code = re.sub(r"'''.*?'''", "", code, flags=re.DOTALL)
    # Remove comentários de linha
    code = re.sub(r"#.*", "", code)
    return code


def extract_fn_body(src: str, fn_name: str) -> str:
    """Extrai o corpo bruto de uma função (tudo após 'def fn_name...:')."""
    match = re.search(
        rf"def {re.escape(fn_name)}\(.*?\n(.*?)(?=\n    def |\Z)",
        src,
        re.DOTALL,
    )
    return match.group(1) if match else ""


def run():
    print("=" * 70)
    print(f"  CHECKER patch_34 -- {TARGET.relative_to(ROOT)}")
    print("=" * 70)

    if not TARGET.exists():
        print(f"{FAIL}  Arquivo não encontrado: {TARGET}")
        sys.exit(2)

    src = TARGET.read_text(encoding="utf-8")
    lines = src.splitlines()

    # ------------------------------------------------------------------
    # 1. key_type NÃO deve aparecer em nenhuma linha (nem comentário)
    # ------------------------------------------------------------------
    kt_lines = [
        f"L{i+1}: {l.strip()}"
        for i, l in enumerate(lines)
        if "key_type" in l
    ]
    check(
        "key_type removido por completo (inclusive comentários)",
        len(kt_lines) == 0,
        "; ".join(kt_lines) if kt_lines else "",
    )

    # ------------------------------------------------------------------
    # 2. _structure_filter_col NÃO deve conter branch aba em CÓDIGO
    #    (docstrings e comentários são ignorados)
    # ------------------------------------------------------------------
    fn_body = extract_fn_body(src, "_structure_filter_col")
    fn_code = strip_docstrings_and_comments(fn_body)
    aba_in_code = '"aba"' in fn_code or "'aba'" in fn_code

    check(
        "branch 'aba' removido de _structure_filter_col() [código, não docstring]",
        not aba_in_code,
        f"Código (sem doc/comentários) ainda contém 'aba': {fn_code[:200]!r}"
        if aba_in_code
        else "",
    )

    # ------------------------------------------------------------------
    # 3. Código morto após return em _load_structures removido
    # ------------------------------------------------------------------
    dead_marker = "# Fallback: aba"
    dead_lines = [
        f"L{i+1}" for i, l in enumerate(lines) if dead_marker in l
    ]
    check(
        "Código morto '# Fallback: aba' removido de _load_structures",
        len(dead_lines) == 0,
        f"Ainda presente em: {', '.join(dead_lines)}" if dead_lines else "",
    )

    aba_col_dead = [
        f"L{i+1}: {l.strip()}"
        for i, l in enumerate(lines)
        if "aba_col = c.get" in l
    ]
    check(
        'Linha \'aba_col = c.get("aba")\' removida de _load_structures',
        len(aba_col_dead) == 0,
        "; ".join(aba_col_dead) if aba_col_dead else "",
    )

    # ------------------------------------------------------------------
    # 4. PAYOFF_COLUMN_ALIASES NÃO deve ter "aba" como chave
    # ------------------------------------------------------------------
    payoff_alias_block_match = re.search(
        r"PAYOFF_COLUMN_ALIASES\s*=\s*\{(.*?)\}",
        src,
        re.DOTALL,
    )
    payoff_block = payoff_alias_block_match.group(1) if payoff_alias_block_match else ""
    check(
        '"aba" removido de PAYOFF_COLUMN_ALIASES',
        '"aba"' not in payoff_block,
        f"Bloco: {payoff_block.strip()[:200]}" if '"aba"' in payoff_block else "",
    )

    # ------------------------------------------------------------------
    # 5. _build_payoff_colmap NÃO deve ter "aba" no bloco canônico
    # ------------------------------------------------------------------
    bpm_body = extract_fn_body(src, "_build_payoff_colmap")
    canonical_block_match = re.search(
        r'payoff_curve_points.*?aliases\s*=\s*\{(.*?)\}',
        bpm_body,
        re.DOTALL,
    )
    canonical_aliases = canonical_block_match.group(1) if canonical_block_match else ""
    check(
        '"aba" removido do bloco canônico em _build_payoff_colmap',
        '"aba"' not in canonical_aliases,
        f"Aliases canônicos: {canonical_aliases.strip()[:200]}"
        if '"aba"' in canonical_aliases
        else "",
    )

    # ------------------------------------------------------------------
    # 6. COLUMN_ALIASES DEVE manter "aba" (compat de leitura SELECT)
    # ------------------------------------------------------------------
    col_alias_match = re.search(
        r"COLUMN_ALIASES\s*=\s*\{(.*?)\}",
        src,
        re.DOTALL,
    )
    col_block = col_alias_match.group(1) if col_alias_match else ""
    check(
        '"aba" mantido em COLUMN_ALIASES (compat leitura SELECT)',
        '"aba"' in col_block,
        "COLUMN_ALIASES não contém 'aba' -- pode quebrar SELECT"
        if '"aba"' not in col_block
        else "",
    )

    # ------------------------------------------------------------------
    # 7. _resolve_structure_key deve existir e lançar ValueError
    # ------------------------------------------------------------------
    check(
        "_resolve_structure_key() implementado",
        "def _resolve_structure_key" in src,
    )
    check(
        "_resolve_structure_key levanta ValueError",
        "raise ValueError" in src and "structure_id invalido" in src,
    )

    # ------------------------------------------------------------------
    # 8. get_decisions NÃO usa filters.get('aba') em código
    # ------------------------------------------------------------------
    gd_body = extract_fn_body(src, "get_decisions")
    gd_code = strip_docstrings_and_comments(gd_body)
    aba_filter = 'filters.get("aba")' in gd_code or "filters.get('aba')" in gd_code
    check(
        "filters.get('aba') removido de get_decisions()",
        not aba_filter,
        "Ainda filtra por 'aba' em get_decisions" if aba_filter else "",
    )

    # ------------------------------------------------------------------
    # 9. check_database_status usa mode=canonical
    # ------------------------------------------------------------------
    check(
        "check_database_status usa 'mode=canonical'",
        "mode=canonical" in src,
    )
    check(
        "check_database_status sem 'mode=aba'",
        "mode=aba" not in src,
    )

    # ------------------------------------------------------------------
    # 10. Docstring de get_payoff_curve não menciona aba("BOVA11")
    # ------------------------------------------------------------------
    gpc_match = re.search(
        r'def get_payoff_curve\(.*?"""(.*?)"""',
        src,
        re.DOTALL,
    )
    gpc_doc = gpc_match.group(1) if gpc_match else ""
    check(
        'Docstring get_payoff_curve não menciona \'aba ("BOVA11")\'',
        'aba ("BOVA11")' not in gpc_doc,
        f"Docstring: {gpc_doc.strip()}" if 'aba ("BOVA11")' in gpc_doc else "",
    )

    # ------------------------------------------------------------------
    # Resultado final
    # ------------------------------------------------------------------
    total = len(results)
    passed = sum(1 for _, ok, _ in results if ok)
    failed = total - passed

    print()
    print("=" * 70)
    print(f"  Resultado: {passed}/{total} OK | {failed} FALHOU")
    print("=" * 70)

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    run()
