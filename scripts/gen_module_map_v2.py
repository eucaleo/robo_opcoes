import json
from collections import defaultdict
from pathlib import Path

SQL_REPORT = Path("ATT/reports/sql_report_v3.json")
DOC_OUT = Path("docs/MAPA_MODULOS_FUNCOES.md")

def main():
    if not SQL_REPORT.exists():
        print(f"[ERRO] Não encontrado: {SQL_REPORT}")
        raise SystemExit(1)

    with SQL_REPORT.open(encoding='utf-8') as f:
        report = json.load(f)

    # tabela -> arquivo -> [(linha, contexto)]
    mapping = defaultdict(lambda: defaultdict(list))

    # Estrutura esperada: { "arquivo": [ {"table": ..., "line": ..., "context": ..., "op": ...}, ... ] }
    for filename, entries in report.items():
        if not isinstance(entries, list):
            continue
        for item in entries:
            table = (item.get('table') or '').strip()
            if not table:
                continue
            # heurística simples anti-ruído
            if table.startswith("#") or len(table) > 64:
                continue
            line = item.get('line') or "?"
            context = (item.get('context') or '').strip()
            op = (item.get('op') or '').upper()
            if op:
                context = f"[{op}] {context}" if context else f"[{op}]"
            mapping[table][filename].append((line, context))

    with DOC_OUT.open('w', encoding='utf-8') as out:
        out.write("# Mapa de Uso de SQL -- Tabela x Arquivo/Função (v2)\n\n")
        out.write("> Fonte: ATT/reports/sql_report_v3.json\n\n")
        for table in sorted(mapping):
            out.write(f"## {table}\n\n")
            for filename in sorted(mapping[table]):
                entries = mapping[table][filename]
                out.write(f"- **{filename}**\n")
                for line, context in entries:
                    ctx = f" `{context}`" if context else ""
                    out.write(f"    - linha {line}:{ctx}\n")
            out.write("\n---\n\n")
    print(f"[OK] Mapa gerado em {DOC_OUT}")

if __name__ == "__main__":
    main()
