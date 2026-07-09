from __future__ import annotations

from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVID = ROOT / "FRENTE_BD_UNICO_APPDB" / "evidencias"

TARGETS = {
    ROOT / "scripts" / "repair_derived_db_consistency.py": {
        'print("=== REPARO DE CONSISTENCIA DO DERIVED.DB ===")':
        'print("=== REPARO DE CONSISTENCIA DO APP.DB ===")',
    },
    ROOT / "scripts" / "validate_derived_db.py": {
        'print("=== VALIDACAO DO BANCO DERIVED.DB ===")':
        'print("=== VALIDACAO DO BANCO APP.DB ===")',
    },
}


def main() -> None:
    EVID.mkdir(parents=True, exist_ok=True)

    lines = []
    lines.append("===== DATA =====")
    lines.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    lines.append("")
    lines.append("===== OBJETIVO =====")
    lines.append("Limpar labels operacionais remanescentes contendo DERIVED.DB em maiusculo.")
    lines.append("Nao renomeia arquivos, APIs, funcoes ou imports legados.")
    lines.append("")

    changed = []

    for path, replacements in TARGETS.items():
        rel = path.relative_to(ROOT).as_posix()
        lines.append(f"===== ARQUIVO: {rel} =====")

        if not path.exists():
            lines.append("[ERRO] Arquivo nao encontrado.")
            lines.append("")
            continue

        text = path.read_text(encoding="utf-8", errors="replace")
        original = text

        for old, new in replacements.items():
            if old in text:
                text = text.replace(old, new)
                lines.append(f"[OK] Substituido: {old}")
                lines.append(f"     Por:        {new}")
            else:
                lines.append(f"[INFO] Padrao nao encontrado, possivelmente ja limpo: {old}")

        if text != original:
            path.write_text(text, encoding="utf-8")
            changed.append(rel)
            lines.append("[OK] Arquivo atualizado.")
        else:
            lines.append("[INFO] Nenhuma alteracao aplicada.")

        lines.append("")

    lines.append("===== ARQUIVOS ALTERADOS =====")
    if changed:
        for item in changed:
            lines.append(f"- {item}")
    else:
        lines.append("Nenhum.")

    lines.append("")
    lines.append("===== DECISAO =====")
    lines.append("[OK] Labels operacionais DERIVED.DB foram normalizados para APP.DB quando presentes.")
    lines.append("[OK] Nomes tecnicos derived_* permanecem preservados por compatibilidade.")
    lines.append("")

    out = EVID / "49_phase1f_b1_clean_uppercase_derived_db_labels.txt"
    out.write_text("\n".join(lines), encoding="utf-8")

    print("[OK] Fase 1F-B.1 concluida.")
    print(f"Gerado: {out.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
