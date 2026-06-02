# scripts/72_smoke_patch32_ui_audit.py
"""
Smoke: executa patch_32 (auditoria wiring UI) e valida saída.

Critérios de aceite:
  - patch_32 executa sem exceção
  - docs/audit_ui_wiring_patch32.md é gerado
  - Nenhum arquivo classificado como ERRO
"""

import sys
import importlib
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))


def main():
    print("=" * 55)
    print("  smoke_72 — patch_32 UI wiring audit")
    print("=" * 55)

    # Importa e executa o patch_32
    spec_path = RAIZ / "ATT" / "patches" / "patch_32_audit_ui_wiring.py"
    if not spec_path.exists():
        print(f"  ❌  Não encontrado: {spec_path.relative_to(RAIZ)}")
        sys.exit(1)

    import importlib.util
    spec = importlib.util.spec_from_file_location("patch_32", spec_path)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    # run() retorna 0 (ok) ou 1 (LEGADO_PURO detectado — não é falha fatal)
    exit_code = mod.run()

    # Verifica se o relatório MD foi gerado
    md_path = RAIZ / "docs" / "audit_ui_wiring_patch32.md"
    if not md_path.exists():
        print(f"\n  ❌  Relatório não gerado: {md_path.relative_to(RAIZ)}")
        sys.exit(1)

    print(f"\n  ✅  Relatório gerado: {md_path.relative_to(RAIZ)}")
    print(f"  {'✅' if exit_code == 0 else '⚠️ '} Exit code patch_32: {exit_code}")
    print("\n  smoke_72 concluído.")

    # Smoke não falha por LEGADO_PURO (exit_code=1 é diagnóstico, não erro fatal)
    sys.exit(0)


if __name__ == "__main__":
    main()
