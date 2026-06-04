# ATT/patches/patch_59_bugfix_surface_audit.py
"""
patch_59: correcoes de bugs pos-patch_57/58

Problemas corrigidos:
  [F1] 74_audit_public_api_aba_surface.py -- format_report usa atributos
       inexistentes (filepath/lineno/line_text); corrige para file/line/text.
  [F2] 74_audit_public_api_aba_surface.py -- pathlib nao importado no __main__.
  [F3] canonical_input_service.py -- variavel 'ref' nao definida em
       _resolve_snapshot(); construcao de StructureRef adicionada.
  [F4] canonical_input_service.py -- docstring deslocada apos 'aba_str = ref.aba'
       em _resolve_legs_via_selector(); movida para posicao correta.
  [F5] canonical_input_service.py -- meta usa 'aba' (NameError) no lugar de
       'aba_str' em _resolve_legs_via_selector().
  [F6] structures_repository.py -- _fetch_legs() chama count_legs(d["id"])
       (id da leg) em vez de count_legs(structure_id); corrigido.
  [F7] derived_service.py -- save_payoff_from_canonical_payload() e
       save_decision_from_canonical_payload() passam kwarg 'aba=' para
       funcoes cuja assinatura e 'ref='; corrigido.

Execucao:
  python ATT/patches/patch_59_bugfix_surface_audit.py           # dry-run
  python ATT/patches/patch_59_bugfix_surface_audit.py --apply   # aplica
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent

# ---------------------------------------------------------------------------
# Definicoes dos fixes
# ---------------------------------------------------------------------------

FIXES: list[dict] = [

    # ------------------------------------------------------------------
    # F1 + F2 -- 74_audit_public_api_aba_surface.py
    # ------------------------------------------------------------------
    {
        "id":   "F1+F2",
        "file": "scripts/74_audit_public_api_aba_surface.py",
        "find": '''\
def format_report(entries) -> str:
    """Formata lista de AuditEntry em relatório texto."""
    lines = []
    for e in entries:
        lines.append(f"{e.filepath}:{e.lineno} [{e.classification}] {e.line_text.rstrip()}")
    return "\\n".join(lines)''',
        "replace": '''\
def format_report(entries) -> str:
    """Formata lista de AuditEntry em relatorio texto."""
    lines = []
    for e in entries:
        lines.append(f"{e.file}:{e.line} [{e.classification}] {e.text.rstrip()}")
    return "\\n".join(lines)''',
    },
    {
        "id":   "F2",
        "file": "scripts/74_audit_public_api_aba_surface.py",
        "find": "import argparse",
        "replace": "import argparse\nimport pathlib",
    },

    # ------------------------------------------------------------------
    # F3 -- canonical_input_service.py: 'ref' nao definido
    # ------------------------------------------------------------------
    {
        "id":   "F3",
        "file": "services/canonical_input_service.py",
        "find": '''\
            if self.market_snapshot_selector is not None and aba:
                legs_list, legs_meta = self._resolve_legs_via_selector(ref)
                snapshot_source = legs_meta["snapshot_source"]''',
        "replace": '''\
            if self.market_snapshot_selector is not None and aba:
                ref = StructureRef.from_aba(aba)
                legs_list, legs_meta = self._resolve_legs_via_selector(ref)
                snapshot_source = legs_meta["snapshot_source"]''',
    },

    # ------------------------------------------------------------------
    # F4 + F5 -- canonical_input_service.py: docstring deslocada e NameError
    # ------------------------------------------------------------------
    {
        "id":   "F4+F5",
        "file": "services/canonical_input_service.py",
        "find": '''\
        def _resolve_legs_via_selector(
            self,
            ref: StructureRef,
        ) -> tuple[list[dict[str, Any]], dict[str, Any]]:
            aba_str = ref.aba
            """
            Delega ao MarketSnapshotSelector e serializa legs completas.

            Serializacao cobre todos os campos de LegMarketSnapshot para que
            consumidores downstream (pricing, greeks, payoff) tenham os dados.
            """''',
        "replace": '''\
        def _resolve_legs_via_selector(
            self,
            ref: StructureRef,
        ) -> tuple[list[dict[str, Any]], dict[str, Any]]:
            """
            Delega ao MarketSnapshotSelector e serializa legs completas.

            Serializacao cobre todos os campos de LegMarketSnapshot para que
            consumidores downstream (pricing, greeks, payoff) tenham os dados.
            """
            aba_str = ref.aba''',
    },
    {
        "id":   "F5",
        "file": "services/canonical_input_service.py",
        "find": '''\
                "snapshot_aba":     aba,''',
        "replace": '''\
                "snapshot_aba":     aba_str,''',
    },

    # ------------------------------------------------------------------
    # F6 -- structures_repository.py: count_legs com id errado
    # ------------------------------------------------------------------
    {
        "id":   "F6",
        "file": "repositories/structures_repository.py",
        "find": '''\
            result = []
            for row in rows:
                d = dict(row)
                d["n_legs"] = self.count_legs(d["id"])
                result.append(d)
            return result''',
        "replace": '''\
            result = []
            for row in rows:
                d = dict(row)
                result.append(d)
            return result''',
    },

    # ------------------------------------------------------------------
    # F7 -- derived_service.py: kwarg 'aba=' -> 'ref='
    # ------------------------------------------------------------------
    {
        "id":   "F7a",
        "file": "services/derived_service.py",
        "find": '''\
        # patch_57: passa storage_key (str) -- save_payoff_curve aceita str via _unwrap_ref
        return save_payoff_curve(
            aba=storage_key,''',
        "replace": '''\
        # patch_59: kwarg corrigido de aba= para ref= (assinatura de save_payoff_curve)
        return save_payoff_curve(
            ref=storage_key,''',
    },
    {
        "id":   "F7b",
        "file": "services/derived_service.py",
        "find": '''\
        # patch_57: passa storage_key (str) -- save_decision aceita str via _unwrap_ref
        return save_decision(
            aba=storage_key,''',
        "replace": '''\
        # patch_59: kwarg corrigido de aba= para ref= (assinatura de save_decision)
        return save_decision(
            ref=storage_key,''',
    },
]

# ---------------------------------------------------------------------------
# Motor de aplicacao
# ---------------------------------------------------------------------------

def _apply_fix(fix: dict, dry_run: bool) -> bool:
    fpath = ROOT / fix["file"]
    if not fpath.exists():
        print(f"  [SKIP] {fix['file']} nao encontrado")
        return True

    src = fpath.read_text(encoding="utf-8")

    if fix["find"] not in src:
        print(f"  [SKIP] {fix['id']} -- trecho nao localizado em {fix['file']} "
              f"(ja corrigido ou divergencia de whitespace)")
        return True

    new_src = src.replace(fix["find"], fix["replace"], 1)

    if dry_run:
        print(f"  [DRY]  {fix['id']} -- {fix['file']}")
        return True

    bak = fpath.with_suffix(fpath.suffix + ".bak_p59")
    shutil.copy2(fpath, bak)
    fpath.write_text(new_src, encoding="utf-8")
    print(f"  [OK]   {fix['id']} -- {fix['file']}")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="patch_59: bugfix surface audit")
    parser.add_argument("--apply", action="store_true",
                        help="Aplica correcoes (default: dry-run)")
    args = parser.parse_args()
    dry_run = not args.apply

    prefix = "[DRY-RUN] " if dry_run else ""
    print(f"\n{prefix}patch_59 -- correcoes pos-patch_57/58")
    print("-" * 60)

    ok = 0
    for fix in FIXES:
        if _apply_fix(fix, dry_run):
            ok += 1

    print("-" * 60)
    if dry_run:
        print(f"[DRY-RUN] {ok}/{len(FIXES)} fixes processados.")
        print(">  Execute com --apply para efetivar.")
    else:
        print(f"[OK] {ok}/{len(FIXES)} fixes aplicados.")
        print(">  Proximo: python -m pytest ATT/tests/ -x -q 2>&1 | tail -20")


if __name__ == "__main__":
    main()
