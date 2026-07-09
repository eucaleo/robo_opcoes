from __future__ import annotations

from datetime import datetime
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
EVID = ROOT / "FRENTE_BD_UNICO_APPDB" / "evidencias"

CONFIG = ROOT / "db" / "config.py"

OLD_DERIVED_LINE_RE = re.compile(
    r'^DERIVED_DB_PATH\s*=\s*Path\(os\.getenv\("DERIVED_DB_PATH",\s*str\(_PROJECT_ROOT / "dados/app\.db"\)\)\)\.resolve\(\)\s*$',
    re.MULTILINE,
)

CANONICAL_BLOCK = '''# Caminho canonico do banco unico da aplicacao.
APP_DB_PATH = Path(os.getenv("APP_DB_PATH", str(_PROJECT_ROOT / "dados/app.db"))).resolve()

# Alias legado preservado por compatibilidade temporaria.
# Importante: DERIVED_DB_PATH aponta para o banco unico app.db.
DERIVED_DB_PATH = APP_DB_PATH'''


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def main() -> None:
    EVID.mkdir(parents=True, exist_ok=True)

    lines: list[str] = []
    lines.append("===== DATA =====")
    lines.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    lines.append("")
    lines.append("===== OBJETIVO =====")
    lines.append("Introduzir APP_DB_PATH como nome canonico do banco unico em db/config.py.")
    lines.append("Preservar DERIVED_DB_PATH como alias legado apontando para APP_DB_PATH.")
    lines.append("Nao renomear modulos, arquivos, classes ou funcoes nesta subfase.")
    lines.append("")

    if not CONFIG.exists():
        lines.append("===== ERRO =====")
        lines.append("db/config.py nao encontrado.")
        out = EVID / "53_phase1f_c_appdb_canonical_aliases.txt"
        out.write_text("\n".join(lines), encoding="utf-8")
        raise SystemExit(1)

    text = read(CONFIG)
    original = text

    lines.append("===== ARQUIVO =====")
    lines.append("db/config.py")
    lines.append("")

    if "APP_DB_PATH" in text and "DERIVED_DB_PATH = APP_DB_PATH" in text:
        lines.append("[INFO] APP_DB_PATH e alias DERIVED_DB_PATH = APP_DB_PATH ja estavam presentes.")
        changed = False
    elif OLD_DERIVED_LINE_RE.search(text):
        text = OLD_DERIVED_LINE_RE.sub(CANONICAL_BLOCK, text)
        changed = text != original
        if changed:
            write(CONFIG, text)
            lines.append("[OK] Linha DERIVED_DB_PATH antiga substituida por bloco canonico APP_DB_PATH.")
        else:
            lines.append("[INFO] Nenhuma alteracao aplicada.")
    else:
        lines.append("[ATENCAO] Padrao exato antigo nao encontrado.")
        lines.append("[INFO] Tentando fallback conservador.")

        fallback_old = 'DERIVED_DB_PATH = Path(os.getenv("DERIVED_DB_PATH", str(_PROJECT_ROOT / "dados/app.db"))).resolve()'
        if fallback_old in text and "APP_DB_PATH" not in text:
            text = text.replace(fallback_old, CANONICAL_BLOCK)
            changed = text != original
            if changed:
                write(CONFIG, text)
                lines.append("[OK] Fallback aplicado com sucesso.")
            else:
                lines.append("[INFO] Fallback nao alterou o arquivo.")
        else:
            changed = False
            lines.append("[BLOQUEIO] Nao foi possivel aplicar alteracao automatica com seguranca.")

    final_text = read(CONFIG)

    lines.append("")
    lines.append("===== VERIFICACOES =====")
    checks = {
        "APP_DB_PATH presente": "APP_DB_PATH" in final_text,
        "DERIVED_DB_PATH alias para APP_DB_PATH": "DERIVED_DB_PATH = APP_DB_PATH" in final_text,
        "dados/app.db presente": "dados/app.db" in final_text,
        "literal derived.db ausente": "derived.db" not in final_text.lower(),
    }

    for name, ok in checks.items():
        lines.append(f"{'[OK]' if ok else '[FALHA]'} {name}: {ok}")

    lines.append("")
    lines.append("===== ALTERACAO APLICADA =====")
    lines.append("sim" if changed else "nao")
    lines.append("")
    lines.append("===== DECISAO =====")

    if all(checks.values()):
        lines.append("[OK] db/config.py passa a expor APP_DB_PATH como nome canonico.")
        lines.append("[OK] DERIVED_DB_PATH permanece como alias legado para compatibilidade.")
        lines.append("[OK] Proxima etapa pode migrar imports internos controlados de DERIVED_DB_PATH para APP_DB_PATH.")
    else:
        lines.append("[BLOQUEIO] Verificacoes falharam. Revisar db/config.py antes de prosseguir.")

    lines.append("")

    out = EVID / "53_phase1f_c_appdb_canonical_aliases.txt"
    out.write_text("\n".join(lines), encoding="utf-8")

    print("[OK] Fase 1F-C aliases canonicos executada.")
    print(f"Gerado: {out.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
