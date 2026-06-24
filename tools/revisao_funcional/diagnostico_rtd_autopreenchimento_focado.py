import os
from pathlib import Path

output_path = Path("docs/checkpoints/evidencias/diagnostico_rtd_autopreenchimento_focado.txt")

files = [
    "services/structure_leg_rtd_enrichment_service.py",
    "repositories/rtd_option_quotes_repository.py",
    "UI/components/structure_editor_dialog.py",
    "UI/main_window.py",
    "scripts/import_lista_rtd_excel_to_option_quotes.py",
    "scripts/run_lista_rtd_option_quotes_pipeline.py",
    "scripts/run_rtd_option_quotes_pipeline.py",
    "scripts/run_rtd_refresh_full.py",
    "scripts/import_rtd_option_quotes_wide_csv.py",
    "scripts/import_rtd_links_to_option_quotes.py",
]

terms = [
    "class ",
    "def ",
    "enrich",
    "get_by_codigo",
    "option quote not found",
    "rtd_option_quotes",
    "run_lista",
    "run_rtd",
    "import_lista",
    "import_rtd",
    "win32com",
    "Excel.Application",
    "Dispatch",
    "subprocess",
    "argparse",
    "add_argument",
    "PETRS424",
    "autopreench",
    "preench",
]

def read_text(path):
    for enc in ("utf-8", "cp1252", "latin-1"):
        try:
            return Path(path).read_text(encoding=enc)
        except Exception:
            pass
    return None

def interesting_line(line):
    lower = line.lower()
    return any(term.lower() in lower for term in terms)

def write_file_section(out, path):
    out.write("\n")
    out.write("=" * 100 + "\n")
    out.write("ARQUIVO: " + path + "\n")
    out.write("=" * 100 + "\n")

    if not os.path.exists(path):
        out.write("NAO ENCONTRADO\n")
        return

    text = read_text(path)
    if text is None:
        out.write("NAO FOI POSSIVEL LER\n")
        return

    lines = text.splitlines()
    hit_lines = []

    for i, line in enumerate(lines, start=1):
        if interesting_line(line):
            hit_lines.append(i)

    if not hit_lines:
        out.write("SEM OCORRENCIAS FOCADAS\n")
        return

    ranges = []
    for line_no in hit_lines:
        start = max(1, line_no - 8)
        end = min(len(lines), line_no + 12)
        ranges.append((start, end))

    merged = []
    for start, end in sorted(ranges):
        if not merged or start > merged[-1][1] + 3:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)

    for start, end in merged:
        out.write("\n--- linhas " + str(start) + " a " + str(end) + " ---\n")
        for n in range(start, end + 1):
            out.write(str(n).rjust(5) + ": " + lines[n - 1] + "\n")

output_path.parent.mkdir(parents=True, exist_ok=True)

with output_path.open("w", encoding="utf-8") as out:
    out.write("DIAGNOSTICO FOCADO RTD AUTOPREENCHIMENTO\n")
    out.write("Objetivo: localizar fluxo atual e ponto de acoplamento para atualizar RTD sob demanda.\n")

    for path in files:
        write_file_section(out, path)

print("Arquivo gerado:", output_path)
