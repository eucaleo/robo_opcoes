#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path


DEFAULT_EXCLUDE_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "dist",
    "build",
}

DEFAULT_EXCLUDE_SUFFIXES = {
    ".pyc",
    ".pyo",
    ".db",
    ".sqlite",
    ".sqlite3",
    ".log",
    ".tmp",
    ".bak",
}


def format_size(size: int) -> str:
    units = ["B", "KB", "MB", "GB"]
    value = float(size)

    for unit in units:
        if value < 1024 or unit == units[-1]:
            if unit == "B":
                return f"{int(value)} {unit}"
            return f"{value:.1f} {unit}"
        value /= 1024

    return f"{size} B"


def should_skip_dir(path: Path, include_hidden: bool) -> bool:
    name = path.name

    if name in DEFAULT_EXCLUDE_DIRS:
        return True

    if not include_hidden and name.startswith("."):
        return True

    return False


def should_skip_file(path: Path, include_hidden: bool) -> bool:
    name = path.name

    if not include_hidden and name.startswith("."):
        return True

    if path.suffix.lower() in DEFAULT_EXCLUDE_SUFFIXES:
        return True

    return False


def sorted_children(path: Path, include_hidden: bool) -> list[Path]:
    children = []

    for child in path.iterdir():
        if child.is_dir() and should_skip_dir(child, include_hidden):
            continue

        if child.is_file() and should_skip_file(child, include_hidden):
            continue

        children.append(child)

    return sorted(children, key=lambda p: (not p.is_dir(), p.name.lower()))


def build_tree(
    root: Path,
    current: Path,
    prefix: str,
    lines: list[str],
    stats: dict[str, int],
    include_hidden: bool,
    max_depth: int | None,
    show_size: bool,
) -> None:
    relative = current.relative_to(root)
    depth = len(relative.parts)

    if max_depth is not None and depth >= max_depth:
        return

    children = sorted_children(current, include_hidden)

    for index, child in enumerate(children):
        is_last = index == len(children) - 1
        connector = "└── " if is_last else "├── "
        next_prefix = prefix + ("    " if is_last else "│   ")

        if child.is_dir():
            stats["dirs"] += 1
            lines.append(f"{prefix}{connector}📁 {child.name}/")
            build_tree(
                root=root,
                current=child,
                prefix=next_prefix,
                lines=lines,
                stats=stats,
                include_hidden=include_hidden,
                max_depth=max_depth,
                show_size=show_size,
            )
        else:
            stats["files"] += 1

            if show_size:
                try:
                    size = format_size(child.stat().st_size)
                    lines.append(f"{prefix}{connector}📄 {child.name} ({size})")
                except OSError:
                    lines.append(f"{prefix}{connector}📄 {child.name}")
            else:
                lines.append(f"{prefix}{connector}📄 {child.name}")


def generate_map(
    root: Path,
    output: Path,
    include_hidden: bool,
    max_depth: int | None,
    show_size: bool,
) -> None:
    root = root.resolve()
    output = output.resolve()

    if not root.exists():
        raise FileNotFoundError(f"Raiz não encontrada: {root}")

    if not root.is_dir():
        raise NotADirectoryError(f"Raiz não é uma pasta: {root}")

    stats = {
        "dirs": 0,
        "files": 0,
    }

    tree_lines = [f"📁 {root.name}/"]

    build_tree(
        root=root,
        current=root,
        prefix="",
        lines=tree_lines,
        stats=stats,
        include_hidden=include_hidden,
        max_depth=max_depth,
        show_size=show_size,
    )

    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    content = [
        "# Mapa do Sistema",
        "",
        f"- **Raiz:** `{root}`",
        f"- **Gerado em:** `{generated_at}`",
        f"- **Pastas mapeadas:** `{stats['dirs']}`",
        f"- **Arquivos mapeados:** `{stats['files']}`",
        f"- **Inclui ocultos:** `{'sim' if include_hidden else 'não'}`",
        f"- **Profundidade máxima:** `{max_depth if max_depth is not None else 'sem limite'}`",
        "",
        "## Estrutura",
        "",
        "```text",
        *tree_lines,
        "```",
        "",
    ]

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(content), encoding="utf-8")

    print(f"[OK] mapa gerado: {output}")
    print(f"[INFO] pastas: {stats['dirs']}")
    print(f"[INFO] arquivos: {stats['files']}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Gera um mapa de pastas, subpastas e arquivos do projeto."
    )

    parser.add_argument(
        "--root",
        default=".",
        help="Pasta raiz do projeto. Padrão: diretório atual.",
    )

    parser.add_argument(
        "--out",
        default="docs/mapa_sistema.md",
        help="Arquivo Markdown de saída. Padrão: docs/mapa_sistema.md.",
    )

    parser.add_argument(
        "--include-hidden",
        action="store_true",
        help="Inclui arquivos e pastas ocultos.",
    )

    parser.add_argument(
        "--max-depth",
        type=int,
        default=None,
        help="Profundidade máxima do mapa. Exemplo: 3.",
    )

    parser.add_argument(
        "--no-size",
        action="store_true",
        help="Não mostra tamanho dos arquivos.",
    )

    args = parser.parse_args()

    generate_map(
        root=Path(args.root),
        output=Path(args.out),
        include_hidden=args.include_hidden,
        max_depth=args.max_depth,
        show_size=not args.no_size,
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
