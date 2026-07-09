from __future__ import annotations

from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVID = ROOT / "FRENTE_BD_UNICO_APPDB" / "evidencias"

CONFIG = ROOT / "db" / "config.py"
SCRIPT_1FC = ROOT / "FRENTE_BD_UNICO_APPDB" / "scripts" / "phase1f_c_appdb_canonical_aliases.py"

OLD_COMMENT = "# Importante: DERIVED_DB_PATH nao aponta mais para derived.db; aponta para app.db."
NEW_COMMENT = "# Importante: DERIVED_DB_PATH aponta para o banco unico app.db."


def replace_if_present(path: Path, lines: list[str]) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    lines.append(f"===== ARQUIVO: {rel} =====")

    if not path.exists():
        lines.append("[ERRO] Arquivo nao encontrado.")
        lines.append("")
        return False

    text = path.read_text(encoding="utf-8", errors="replace")
    original = text

    if OLD_COMMENT in text:
        text = text.replace(OLD_COMMENT, NEW_COMMENT)
        path.write_text(text, encoding="utf-8")
        lines.append("[OK] Comentario com literal derived.db substituido.")
        lines.append(f"Antes: {OLD_COMMENT}")
        lines.append(f"Depois: {NEW_COMMENT}")
        changed = True
    else:
        lines.append("[INFO] Comentario antigo nao encontrado; possivelmente ja limpo.")
        changed = False

    final_text = path.read_text(encoding="utf-8", errors="replace")
    has_literal = "derived.db" in final_text.lower()

    lines.append(f"{'[OK]' if not has_literal else '[ATENCAO]'} literal derived.db ausente no arquivo: {not has_literal}")
    lines.append("")
    return changed or (text != original)


def main() -> None:
    EVID.mkdir(parents=True, exist_ok=True)

    lines: list[str] = []
    lines.append("===== DATA =====")
    lines.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    lines.append("")
    lines.append("===== OBJETIVO =====")
    lines.append("Remover literal derived.db introduzido em comentario operacional de db/config.py.")
    lines.append("Atualizar tambem o script gerador da Fase 1F-C para nao reintroduzir o comentario antigo.")
    lines.append("Nao alterar comportamento de runtime.")
    lines.append("")

    changed_config = replace_if_present(CONFIG, lines)
    changed_script = replace_if_present(SCRIPT_1FC, lines)

    config_text = CONFIG.read_text(encoding="utf-8", errors="replace") if CONFIG.exists() else ""
    script_text = SCRIPT_1FC.read_text(encoding="utf-8", errors="replace") if SCRIPT_1FC.exists() else ""

    checks = {
        "db/config.py sem literal derived.db": "derived.db" not in config_text.lower(),
        "APP_DB_PATH presente": "APP_DB_PATH" in config_text,
        "DERIVED_DB_PATH alias para APP_DB_PATH": "DERIVED_DB_PATH = APP_DB_PATH" in config_text,
        "dados/app.db presente": "dados/app.db" in config_text,
        "script 1F-C nao reintroduz comentario antigo": OLD_COMMENT not in script_text,
    }

    lines.append("===== VERIFICACOES =====")
    for name, ok in checks.items():
        lines.append(f"{'[OK]' if ok else '[FALHA]'} {name}: {ok}")

    lines.append("")
    lines.append("===== ARQUIVOS ALTERADOS =====")
    if changed_config:
        lines.append("- db/config.py")
    if changed_script:
        lines.append("- FRENTE_BD_UNICO_APPDB/scripts/phase1f_c_appdb_canonical_aliases.py")
    if not changed_config and not changed_script:
        lines.append("Nenhum.")

    lines.append("")
    lines.append("===== DECISAO =====")
    if all(checks.values()):
        lines.append("[OK] Comentario operacional limpo.")
        lines.append("[OK] APP_DB_PATH permanece canonico e DERIVED_DB_PATH permanece alias legado.")
        lines.append("[OK] Auditoria pode ser reexecutada.")
    else:
        lines.append("[BLOQUEIO] Ainda ha falhas. Revisar arquivos antes de prosseguir.")

    lines.append("")

    out = EVID / "57_phase1f_c1_clean_config_comment.txt"
    out.write_text("\n".join(lines), encoding="utf-8")

    print("[OK] Fase 1F-C.1 limpeza de comentario executada.")
    print(f"Gerado: {out.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
