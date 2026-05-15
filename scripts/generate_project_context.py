from __future__ import annotations

import ast
import json
from collections import Counter
from pathlib import Path


ROOT_PATH = Path(r"C:\Users\eucal\projeto").resolve()
OUTPUT_FILE = ROOT_PATH / "project_context.json"

IGNORE_DIRS = {
    ".git",
    ".pytest_cache",
    "BAK",
    "docs",
    ".venv",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
}

INCLUDE_EXTENSIONS = {
    ".py",
    ".json",
    ".md",
    ".txt",
}

MAX_TEXT_PREVIEW = 500


def should_ignore(path: Path) -> bool:
    return any(part in IGNORE_DIRS for part in path.parts)


def safe_read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            try:
                return path.read_text(encoding="latin-1")
            except Exception:
                return None
    except Exception:
        return None


def extract_python_metadata(path: Path, root: Path) -> dict:
    relative_path = str(path.relative_to(root)).replace("\\", "/")
    source = safe_read_text(path)

    result = {
        "file": relative_path,
        "extension": ".py",
        "size_bytes": path.stat().st_size,
        "imports": [],
        "functions": [],
        "classes": [],
        "methods_by_class": {},
        "has_syntax_error": False,
        "syntax_error": None,
    }

    if source is None:
        result["has_syntax_error"] = True
        result["syntax_error"] = "unable_to_read_file"
        return result

    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as exc:
        result["has_syntax_error"] = True
        result["syntax_error"] = f"{exc.msg} (line {exc.lineno})"
        return result

    imports: list[str] = []
    functions: list[str] = []
    classes: list[str] = []
    methods_by_class: dict[str, list[str]] = {}

    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)

        elif isinstance(node, ast.ImportFrom):
            module_name = node.module or ""
            if node.level and module_name:
                imports.append("." * node.level + module_name)
            elif node.level and not module_name:
                imports.append("." * node.level)
            else:
                imports.append(module_name)

        elif isinstance(node, ast.FunctionDef):
            functions.append(node.name)

        elif isinstance(node, ast.AsyncFunctionDef):
            functions.append(node.name)

        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)
            methods: list[str] = []

            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    methods.append(child.name)

            methods_by_class[node.name] = methods

    result["imports"] = sorted(set(imports))
    result["functions"] = sorted(functions)
    result["classes"] = sorted(classes)
    result["methods_by_class"] = methods_by_class

    return result


def extract_generic_file_metadata(path: Path, root: Path) -> dict:
    relative_path = str(path.relative_to(root)).replace("\\", "/")
    text = safe_read_text(path)

    preview = None
    line_count = None

    if text is not None:
        preview = text[:MAX_TEXT_PREVIEW]
        line_count = text.count("\n") + 1 if text else 0

    return {
        "file": relative_path,
        "extension": path.suffix.lower(),
        "size_bytes": path.stat().st_size,
        "line_count": line_count,
        "preview": preview,
    }


def collect_files(root: Path) -> list[Path]:
    files: list[Path] = []

    for path in root.rglob("*"):
        if path.is_dir():
            continue
        if should_ignore(path):
            continue
        if path.suffix.lower() not in INCLUDE_EXTENSIONS:
            continue
        files.append(path)

    return sorted(files)


def build_summary(entries: list[dict], root: Path) -> dict:
    ext_counter = Counter(entry["extension"] for entry in entries)

    python_entries = [entry for entry in entries if entry["extension"] == ".py"]

    total_functions = sum(len(entry.get("functions", [])) for entry in python_entries)
    total_classes = sum(len(entry.get("classes", [])) for entry in python_entries)
    syntax_errors = [
        {
            "file": entry["file"],
            "error": entry.get("syntax_error"),
        }
        for entry in python_entries
        if entry.get("has_syntax_error")
    ]

    top_largest_files = sorted(
        (
            {
                "file": entry["file"],
                "extension": entry["extension"],
                "size_bytes": entry["size_bytes"],
            }
            for entry in entries
        ),
        key=lambda item: item["size_bytes"],
        reverse=True,
    )[:20]

    directories = Counter()
    for entry in entries:
        file_path = Path(entry["file"])
        top_level = file_path.parts[0] if len(file_path.parts) > 1 else "."
        directories[top_level] += 1

    return {
        "root": str(root),
        "total_files": len(entries),
        "by_extension": dict(sorted(ext_counter.items())),
        "top_level_distribution": dict(sorted(directories.items())),
        "python_files": len(python_entries),
        "total_functions": total_functions,
        "total_classes": total_classes,
        "python_syntax_errors": syntax_errors,
        "largest_files": top_largest_files,
        "ignored_dirs": sorted(IGNORE_DIRS),
    }


def main() -> int:
    print(f"[INFO] Gerando contexto do projeto em: {ROOT_PATH}")
    print(f"[INFO] Ignorando pastas: {', '.join(sorted(IGNORE_DIRS))}")

    files = collect_files(ROOT_PATH)
    entries: list[dict] = []

    for path in files:
        if path.suffix.lower() == ".py":
            entries.append(extract_python_metadata(path, ROOT_PATH))
        else:
            entries.append(extract_generic_file_metadata(path, ROOT_PATH))

    output = {
        "summary": build_summary(entries, ROOT_PATH),
        "files": entries,
    }

    OUTPUT_FILE.write_text(
        json.dumps(output, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"[OK] Arquivo gerado com sucesso: {OUTPUT_FILE}")
    print(f"[INFO] Total de arquivos analisados: {output['summary']['total_files']}")
    print(f"[INFO] Arquivos Python: {output['summary']['python_files']}")
    print(f"[INFO] Total de funções encontradas: {output['summary']['total_functions']}")
    print(f"[INFO] Total de classes encontradas: {output['summary']['total_classes']}")

    syntax_errors = output["summary"]["python_syntax_errors"]
    if syntax_errors:
        print(f"[ATENÇÃO] Arquivos Python com erro de sintaxe: {len(syntax_errors)}")
    else:
        print("[OK] Nenhum erro de sintaxe encontrado nos arquivos Python analisados")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
