from __future__ import annotations

from pathlib import Path
import argparse
import json
import re
import sys


ROOT = Path(__file__).resolve().parents[1]

UI_EXTENSIONS = {
    ".tsx",
    ".ts",
    ".jsx",
    ".js",
    ".vue",
}

IGNORE_DIRS = {
    ".git",
    "node_modules",
    "dist",
    "build",
    "docs",
    "reports",
    ".pytest_cache",
    "__pycache__",
}

REQUIRED_VISIBLE_TERMS = {
    "snapshot_implantacao": [
        "Snapshot da implantação",
        "Snapshot da implantacao",
        "Preço base na implantação",
        "Preco base na implantacao",
    ],
    "snapshot_atual": [
        "Snapshot atual",
        "Preço base atual",
        "Preco base atual",
    ],
    "tabela_pernas": [
        "Ticker",
        "Intrínseco atual",
        "Intrinseco atual",
        "Extrínseco atual",
        "Extrinseco atual",
        "PL atual",
    ],
    "payoff_vencimento": [
        "Payoff no vencimento ao preço atual",
        "Payoff no vencimento ao preco atual",
        "Resultado simulado no vencimento",
    ],
}

BLOCKED_VISIBLE_TERMS = [
    "Preço ref.",
    "Preço ref",
    "Preco ref.",
    "Preco ref",
]


def iter_ui_files() -> list[Path]:
    files: list[Path] = []

    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue

        if path.suffix not in UI_EXTENSIONS:
            continue

        parts = set(path.parts)
        if parts.intersection(IGNORE_DIRS):
            continue

        files.append(path)

    return files


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    files = iter_ui_files()
    corpus_by_file = {str(path.relative_to(ROOT)): read_text(path) for path in files}
    corpus = "\n".join(corpus_by_file.values())

    blocked_hits: list[dict[str, str]] = []
    for rel_path, text in corpus_by_file.items():
        for term in BLOCKED_VISIBLE_TERMS:
            if term in text:
                blocked_hits.append({"arquivo": rel_path, "termo": term})

    missing_groups: list[str] = []
    present_groups: list[str] = []

    for group, alternatives in REQUIRED_VISIBLE_TERMS.items():
        if any(term in corpus for term in alternatives):
            present_groups.append(group)
        else:
            missing_groups.append(group)

    report = {
        "ui_files_scanned": len(files),
        "present_groups": present_groups,
        "missing_groups": missing_groups,
        "blocked_hits": blocked_hits,
        "status": "ok" if not blocked_hits and not missing_groups else "incompleto",
    }

    out_dir = ROOT / "reports" / "payoff_conferencia"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "payoff_ui_analitica.json"
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print(json.dumps(report, indent=2, ensure_ascii=False))
    print(f"Relatorio gerado em {out_path}")

    if blocked_hits:
        return 1

    if args.strict and missing_groups:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
