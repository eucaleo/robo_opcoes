# scripts/sanitize_emojis.py
"""
Sanitiza emojis e caracteres fora do range cp1252 em arquivos .py e .md do projeto.
Substitui por equivalentes ASCII/texto ou remove silenciosamente.

Uso:
    python scripts/sanitize_emojis.py              # dry-run (só mostra o que mudaria)
    python scripts/sanitize_emojis.py --apply      # aplica as substituições
    python scripts/sanitize_emojis.py --stdin      # lê stdin, escreve stdout (pipe)
    python scripts/sanitize_emojis.py --file PATH  # sanitiza arquivo específico
"""
from __future__ import annotations


import argparse
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Tabela de substituição: emoji/símbolo -> representação ASCII legível
# ---------------------------------------------------------------------------
EMOJI_MAP: dict[str, str] = {
    # Status
    "[OK]": "[OK]",
    "[FALHOU]": "[FALHOU]",
    "[AVISO]": "[AVISO]",
    "[AVISO]":  "[AVISO]",
    "[INFO]": "[INFO]",
    "[INFO]":  "[INFO]",
    "[ERRO]": "[ERRO]",
    "[PARCIAL]": "[PARCIAL]",
    "[OK]": "[OK]",
    "[INFO]": "[INFO]",
    "[AVISO]": "[AVISO]",

    # Ações / objetos
    "[FIXO]": "[FIXO]",
    "[LISTA]": "[LISTA]",
    "[DIR]": "[DIR]",
    "[ARQUIVO]": "[ARQUIVO]",
    "[NOTA]": "[NOTA]",
    "[PACOTE]": "[PACOTE]",
    "[RELATORIO]": "[RELATORIO]",
    "[GRAFICO]": "[GRAFICO]",
    "[GRAFICO]": "[GRAFICO]",
    "[INDICE]": "[INDICE]",
    "[INDICE]":  "[INDICE]",
    "[CONFIG]": "[CONFIG]",
    "[BUILD]": "[BUILD]",
    "[TOOLS]": "[TOOLS]",
    "[TOOLS]":  "[TOOLS]",
    "[DEPLOY]": "[DEPLOY]",
    "[TESTE]": "[TESTE]",
    "[CLEANUP]": "[CLEANUP]",
    "[BUSCA]": "[BUSCA]",
    "[BUSCA]": "[BUSCA]",
    "[SAVE]": "[SAVE]",
    "[DELETE]": "[DELETE]",
    "[DELETE]":  "[DELETE]",
    "[BLOQUEADO]": "[BLOQUEADO]",
    "[PROIBIDO]": "[PROIBIDO]",
    "[v]": "[v]",
    "[v]":  "[v]",
    "[x]":  "[x]",
    "[x]":  "[x]",
    "->": "->",
    "->":  "->",
    "<-": "<-",
    "<-":  "<-",
    "[^]": "[^]",
    "[^]":  "[^]",
    "[v]": "[v]",
    "[v]":  "[v]",
    "[volta]": "[volta]",
    "[volta]":  "[volta]",

    # Símbolos tipográficos fora cp1252
    "\u2019": "'",   # aspas tipográficas direita
    "\u2018": "'",   # aspas tipográficas esquerda
    "\u201c": '"',   # aspas duplas esquerda
    "\u201d": '"',   # aspas duplas direita
    "\u2013": "-",   # en dash
    "\u2014": "--",  # em dash
    "\u2026": "...", # reticências
    "\u00b7": ".",   # ponto médio
    "\u2022": "*",   # bullet
    "\u2023": "*",   # bullet triangular
    "\u25b6": ">",   # triângulo direita
    "\u25c0": "<",   # triângulo esquerda
}

# Extensões alvo (sanitização em arquivo)
TARGET_EXTENSIONS = {".py", ".md", ".txt", ".log", ".json"}

# Pastas a ignorar
IGNORE_DIRS = {
    ".git", "__pycache__", ".pytest_cache",
    "node_modules", ".venv", "venv", "env",
    "backups",  # preserva backups históricos intactos
}


# ---------------------------------------------------------------------------
# Core
# ---------------------------------------------------------------------------

def build_pattern() -> re.Pattern:
    """Compila regex que captura qualquer char fora do range cp1252."""
    # cp1252 cobre U+0000-U+00FF mais alguns codepoints extras (U+0152, etc.)
    # A forma mais segura: tentar encode; via regex, capturamos tudo acima U+00FF
    # exceto os que cp1252 cobre explicitamente.
    CP1252_EXTRAS = {
        0x20AC, 0x201A, 0x0192, 0x201E, 0x2026, 0x2020, 0x2021,
        0x02C6, 0x2030, 0x0160, 0x2039, 0x0152, 0x017D,
        0x2018, 0x2019, 0x201C, 0x201D, 0x2022, 0x2013, 0x2014,
        0x02DC, 0x2122, 0x0161, 0x203A, 0x0153, 0x017E, 0x0178,
    }
    # Regex que pega qualquer char que não seja encodável em cp1252
    return re.compile(r'[^\x00-\xff]|[\U00010000-\U0010ffff]', re.UNICODE)


_PATTERN = build_pattern()


def sanitize_line(line: str) -> tuple[str, list[str]]:
    """
    Sanitiza uma linha substituindo emojis/símbolos.
    Retorna (linha_sanitizada, lista_de_substituições_realizadas).
    """
    substitutions: list[str] = []
    result = line

    # 1. Substituições explícitas do mapa (ordem importa: mais longos primeiro)
    for emoji, replacement in sorted(EMOJI_MAP.items(), key=lambda x: -len(x[0])):
        if emoji in result:
            substitutions.append(f"{emoji!r} -> {replacement!r}")
            result = result.replace(emoji, replacement)

    # 2. Qualquer char restante fora de cp1252 -> remove (fallback seguro)
    def _fallback(m: re.Match) -> str:
        ch = m.group(0)
        substitutions.append(f"{ch!r} -> ''  [removido - fora cp1252]")
        return ""

    result = _PATTERN.sub(_fallback, result)

    return result, substitutions


def sanitize_text(text: str) -> tuple[str, list[tuple[int, list[str]]]]:
    """
    Sanitiza texto completo linha a linha.
    Retorna (texto_sanitizado, [(n_linha, [substituicoes])]).
    """
    lines = text.splitlines(keepends=True)
    out_lines: list[str] = []
    report: list[tuple[int, list[str]]] = []

    for i, line in enumerate(lines, start=1):
        sanitized, subs = sanitize_line(line)
        out_lines.append(sanitized)
        if subs:
            report.append((i, subs))

    return "".join(out_lines), report


def sanitize_file(path: Path, apply: bool = False) -> list[tuple[int, list[str]]]:
    """
    Sanitiza um arquivo. Se apply=True, sobrescreve no lugar.
    Retorna o relatório de substituições.
    """
    try:
        original = path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        print(f"  [ERRO leitura] {path}: {e}", file=sys.stderr)
        return []

    sanitized, report = sanitize_text(original)

    if report and apply:
        # Backup lateral antes de sobrescrever
        backup = path.with_suffix(path.suffix + ".bak_emoji")
        backup.write_text(original, encoding="utf-8")
        path.write_text(sanitized, encoding="utf-8")

    return report


def walk_project(root: Path) -> list[Path]:
    """Coleta todos os arquivos alvo no projeto, ignorando pastas de sistema."""
    files: list[Path] = []
    for p in root.rglob("*"):
        if any(part in IGNORE_DIRS for part in p.parts):
            continue
        if p.is_file() and p.suffix in TARGET_EXTENSIONS:
            files.append(p)
    return sorted(files)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sanitiza emojis/símbolos fora de cp1252 em arquivos do projeto."
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--apply", action="store_true",
        help="Aplica substituições nos arquivos (cria .bak_emoji antes)."
    )
    mode.add_argument(
        "--stdin", action="store_true",
        help="Lê stdin, escreve stdout sanitizado (uso em pipe)."
    )
    mode.add_argument(
        "--file", metavar="PATH",
        help="Sanitiza apenas o arquivo especificado."
    )
    parser.add_argument(
        "--root", metavar="DIR", default=".",
        help="Raiz do projeto (default: diretório atual)."
    )
    parser.add_argument(
        "--quiet", action="store_true",
        help="Suprime detalhes, mostra só o resumo."
    )
    args = parser.parse_args()

    # -- modo pipe (stdin -> stdout) -----------------------------------------
    if args.stdin:
        sys.stdin.reconfigure(encoding="utf-8", errors="replace")
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        text = sys.stdin.read()
        sanitized, _ = sanitize_text(text)
        sys.stdout.write(sanitized)
        return

    # -- modo arquivo único --------------------------------------------------
    if args.file:
        path = Path(args.file)
        report = sanitize_file(path, apply=args.apply)
        _print_file_report(path, report, args.quiet, args.apply)
        return

    # -- modo projeto completo -----------------------------------------------
    root = Path(args.root).resolve()
    files = walk_project(root)
    total_files_changed = 0
    total_subs = 0

    print(f"{'[DRY-RUN]' if not args.apply else '[APPLY]'} "
          f"Varrendo {len(files)} arquivo(s) em: {root}\n")

    for path in files:
        report = sanitize_file(path, apply=args.apply)
        if report:
            total_files_changed += 1
            total_subs += sum(len(s) for _, s in report)
            _print_file_report(path, report, args.quiet, args.apply)

    print("-" * 60)
    print(f"Arquivos com ocorrencias : {total_files_changed}")
    print(f"Substituicoes totais     : {total_subs}")
    if not args.apply:
        print("\n[!] Dry-run. Use --apply para aplicar as substituicoes.")
    else:
        print("\n[OK] Substituicoes aplicadas. Backups .bak_emoji criados.")


def _print_file_report(
    path: Path,
    report: list[tuple[int, list[str]]],
    quiet: bool,
    apply: bool,
) -> None:
    if not report:
        return
    n_subs = sum(len(s) for _, s in report)
    tag = "[APLICADO]" if apply else "[DRY-RUN]"
    print(f"{tag} {path}  ({n_subs} substituicao(oes))")
    if not quiet:
        for lineno, subs in report:
            for s in subs:
                print(f"  linha {lineno:>5}: {s}")
    print()


if __name__ == "__main__":
    main()
