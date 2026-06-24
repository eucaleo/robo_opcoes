import os
import re
from datetime import datetime

root = "."
output_path = "docs/checkpoints/evidencias/diagnostico_fluxo_autopreenchimento_rtd.md"

ignored_dirs = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "node_modules",
    "backups",
}

extensions = {
    ".py",
    ".html",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".md",
    ".txt",
}

terms = [
    "autopreench",
    "auto preench",
    "auto-preench",
    "preencher",
    "enrich",
    "rtd",
    "RTD",
    "rtd_option_quotes",
    "get_by_codigo",
    "upsert",
    "insert into rtd_option_quotes",
    "win32com",
    "Dispatch",
    "Excel.Application",
    "BTG_RTD",
    "lista_rtd",
    "option quote not found",
    "StructureLegRtd",
    "quote_repository",
]

def should_skip_dir(path):
    parts = set(path.replace("\\", "/").split("/"))
    return bool(parts.intersection(ignored_dirs))

def read_file(path):
    for enc in ("utf-8", "cp1252", "latin-1"):
        try:
            with open(path, "r", encoding=enc) as f:
                return f.read()
        except Exception:
            pass
    return None

matches = []

for current_root, dirs, files in os.walk(root):
    dirs[:] = [d for d in dirs if d not in ignored_dirs]

    if should_skip_dir(current_root):
        continue

    for file_name in files:
        ext = os.path.splitext(file_name)[1].lower()
        if ext not in extensions:
            continue

        path = os.path.join(current_root, file_name)
        text = read_file(path)
        if text is None:
            continue

        lines = text.splitlines()

        for idx, line in enumerate(lines, start=1):
            lower = line.lower()
            hit_terms = []

            for term in terms:
                if term.lower() in lower:
                    hit_terms.append(term)

            if hit_terms:
                start = max(1, idx - 3)
                end = min(len(lines), idx + 3)
                context = []
                for n in range(start, end + 1):
                    context.append((n, lines[n - 1]))

                matches.append({
                    "path": path.replace("\\", "/"),
                    "line": idx,
                    "terms": sorted(set(hit_terms)),
                    "context": context,
                })

os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    f.write("# Diagnostico do fluxo de autopreenchimento RTD\n\n")
    f.write("Gerado em: " + datetime.now().isoformat(timespec="seconds") + "\n\n")
    f.write("Objetivo: localizar se o botao de autopreenchimento busca apenas cache local ou dispara atualizacao RTD sob demanda.\n\n")
    f.write("Total de ocorrencias: " + str(len(matches)) + "\n\n")

    current = None

    for item in matches:
        if item["path"] != current:
            current = item["path"]
            f.write("\n## " + current + "\n\n")

        f.write("### Linha " + str(item["line"]) + "\n\n")
        f.write("Termos: " + ", ".join(item["terms"]) + "\n\n")
        f.write("    ")
        f.write("\n    ".join([
            str(n).rjust(5) + ": " + line
            for n, line in item["context"]
        ]))
        f.write("\n\n")

print("Arquivo gerado:", output_path)
print("Ocorrencias:", len(matches))

interesting = sorted(set(item["path"] for item in matches))
print("")
print("Arquivos com ocorrencias:")
for path in interesting:
    print(path)
