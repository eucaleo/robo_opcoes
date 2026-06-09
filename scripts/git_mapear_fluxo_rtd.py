import ast
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path.cwd()
OUTPUT_DIR = ROOT / "reports"
OUTPUT_MD = OUTPUT_DIR / "git_mapeamento_fluxo_rtd.md"
OUTPUT_JSON = OUTPUT_DIR / "git_mapeamento_fluxo_rtd.json"

EXTENSOES = {
    ".py",
    ".sql",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".env",
    ".txt",
}

IGNORAR_PREFIXOS = (
    ".trash/",
    "dados/",
    "reports/",
    "docs/",
    "ATT/tests/",
    "tests/",
    "__pycache__/",
)

IGNORAR_PARTES = (
    "/__pycache__/",
    "/.pytest_cache/",
)

PADROES = {
    "excel_rtd": [
        r"\bRTD\b",
        r"RTD\(",
        r"\bExcel\b",
        r"Excel\.Application",
        r"\bxlwings\b",
        r"\bopenpyxl\b",
        r"\bwin32com\b",
        r"\bDispatch\b",
        r"\bWorkbook\b",
        r"\bWorksheet\b",
        r"\bRange\b",
        r"\bCells\b",
        r"\bsheet\b",
        r"\baba\b",
    ],
    "tabelas_legadas_rtd": [
        r"rtd_analise_robo",
        r"rtd_analise_robo_legs",
        r"manual_analise_robo_legs",
        r"rtd_hist_robo",
        r"rtd_configuracoes",
        r"rtd_consolidacoes",
        r"rtd_encerramentos_manuais",
        r"rtd_rolls_detectados",
    ],
    "tabelas_canonicas": [
        r"\bstructures\b",
        r"\bstructure_legs\b",
        r"\bstructure_audit_log\b",
        r"\bpricing_executions\b",
    ],
    "campos_opcoes": [
        r"\bativo\b",
        r"\bunderlying_asset\b",
        r"\bsymbol\b",
        r"\bticker\b",
        r"\bcodigo\b",
        r"\bcódigo\b",
        r"\boption_type\b",
        r"\bcall_put\b",
        r"\bcall\b",
        r"\bput\b",
        r"\bstrike\b",
        r"\bvencimento\b",
        r"\bexpiration_date\b",
        r"\bexpiry\b",
        r"\bquantity\b",
        r"\bquant\b",
        r"\bqtd\b",
        r"\bpremium\b",
        r"\bpreco\b",
        r"\bpreço\b",
        r"\blast\b",
        r"\bultimo\b",
        r"\búltimo\b",
        r"\bbid\b",
        r"\bask\b",
        r"\bvolume\b",
        r"\biv\b",
        r"\bdelta\b",
        r"\bgamma\b",
        r"\btheta\b",
        r"\bvega\b",
    ],
    "market_snapshot": [
        r"MarketSnapshot",
        r"market_snapshot",
        r"snapshot",
        r"manual > rtd",
        r"rtd > manual",
        r"source=RTD",
        r"source.*RTD",
    ],
    "sqlite_db": [
        r"sqlite3",
        r"app\.db",
        r"derived\.db",
        r"PROJECT_ROOT",
        r"_connect",
        r"connect\(",
        r"SELECT ",
        r"INSERT INTO",
        r"UPDATE ",
        r"DELETE FROM",
        r"CREATE TABLE",
    ],
    "ui_fluxo": [
        r"StructureEditor",
        r"DetailsPanel",
        r"MainWindow",
        r"StructuresList",
        r"UIDataModel",
        r"refresh_data",
        r"recalculate",
        r"replace_legs",
        r"create_structure",
        r"update_structure",
    ],
}

PESOS = {
    "excel_rtd": 8,
    "tabelas_legadas_rtd": 9,
    "tabelas_canonicas": 7,
    "campos_opcoes": 4,
    "market_snapshot": 10,
    "sqlite_db": 5,
    "ui_fluxo": 3,
}


def git_ls_files():
    proc = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        capture_output=True,
        text=False,
        check=True,
    )
    raw = proc.stdout.decode("utf-8", errors="ignore")
    return [p for p in raw.split("\x00") if p.strip()]


def deve_ignorar(rel_path: str) -> bool:
    normal = rel_path.replace("\\", "/")

    if normal.startswith(IGNORAR_PREFIXOS):
        return True

    for parte in IGNORAR_PARTES:
        if parte in normal:
            return True

    suffix = Path(normal).suffix.lower()
    if suffix not in EXTENSOES:
        return True

    return False


def ler(path: Path):
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        try:
            return path.read_text(encoding="latin-1", errors="ignore")
        except Exception:
            return ""


def extrair_funcoes_classes(rel_path: str, conteudo: str):
    if not rel_path.endswith(".py"):
        return {
            "classes": [],
            "funcoes": [],
        }

    try:
        tree = ast.parse(conteudo)
    except Exception:
        return {
            "classes": [],
            "funcoes": [],
        }

    classes = []
    funcoes = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            classes.append(
                {
                    "nome": node.name,
                    "linha": node.lineno,
                }
            )

        elif isinstance(node, ast.FunctionDef):
            funcoes.append(
                {
                    "nome": node.name,
                    "linha": node.lineno,
                }
            )

        elif isinstance(node, ast.AsyncFunctionDef):
            funcoes.append(
                {
                    "nome": node.name,
                    "linha": node.lineno,
                }
            )

    return {
        "classes": sorted(classes, key=lambda x: x["linha"]),
        "funcoes": sorted(funcoes, key=lambda x: x["linha"]),
    }


def analisar_arquivo(rel_path: str):
    path = ROOT / rel_path
    conteudo = ler(path)
    linhas = conteudo.splitlines()

    ocorrencias = []
    categorias = {}

    for categoria, padroes in PADROES.items():
        for padrao in padroes:
            regex = re.compile(padrao, re.IGNORECASE)

            for idx, linha in enumerate(linhas, start=1):
                if regex.search(linha):
                    categorias[categoria] = categorias.get(categoria, 0) + 1
                    ocorrencias.append(
                        {
                            "categoria": categoria,
                            "padrao": padrao,
                            "linha": idx,
                            "trecho": linha.strip()[:240],
                        }
                    )

    score = 0
    for categoria, qtd in categorias.items():
        score += PESOS.get(categoria, 1) * qtd

    estrutura_py = extrair_funcoes_classes(rel_path, conteudo)

    return {
        "arquivo": rel_path,
        "score": score,
        "categorias": categorias,
        "classes": estrutura_py["classes"],
        "funcoes": estrutura_py["funcoes"],
        "ocorrencias": ocorrencias,
    }


def gerar_markdown(resultado):
    linhas = []

    linhas.append("# Git Mapeamento Fluxo RTD / Opções")
    linhas.append("")
    linhas.append(f"Gerado em: `{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}`")
    linhas.append(f"Projeto: `{ROOT}`")
    linhas.append("")
    linhas.append("Este relatório usa `git ls-files`, ignorando lixo operacional, bases, reports, docs e testes.")
    linhas.append("")

    linhas.append("## 1. Arquivos prioritários")
    linhas.append("")
    linhas.append("| Score | Arquivo | Categorias |")
    linhas.append("|---:|---|---|")

    for item in resultado["arquivos"][:50]:
        cats = ", ".join(f"{k}: {v}" for k, v in item["categorias"].items())
        linhas.append(f"| {item['score']} | `{item['arquivo']}` | {cats} |")

    linhas.append("")
    linhas.append("## 2. Arquivos candidatos principais")
    linhas.append("")
    linhas.append("Pelo tipo de ocorrência, estes são os arquivos mais prováveis para mexer primeiro:")
    linhas.append("")

    candidatos = [
        "repositories/market_snapshot_repository.py",
        "repositories/structures_repository.py",
        "db/derived_repo.py",
        "UI/models/ui_data.py",
        "UI/components/details_panel.py",
        "UI/main_window.py",
        "services/canonical_input_service.py",
        "domain/payoff.py",
        "domain/decision.py",
        "infra/sqlite_conn.py",
        "db/sqlite.py",
    ]

    for cand in candidatos:
        achado = next((x for x in resultado["arquivos"] if x["arquivo"].replace("\\", "/") == cand), None)

        if achado:
            linhas.append(f"### `{achado['arquivo']}`")
            linhas.append("")
            linhas.append(f"- Score: `{achado['score']}`")
            linhas.append(f"- Categorias: `{achado['categorias']}`")
            linhas.append("")

            if achado["classes"]:
                linhas.append("Classes:")
                for c in achado["classes"][:30]:
                    linhas.append(f"- Linha {c['linha']}: `{c['nome']}`")
                linhas.append("")

            if achado["funcoes"]:
                linhas.append("Funções/métodos:")
                for f in achado["funcoes"][:60]:
                    linhas.append(f"- Linha {f['linha']}: `{f['nome']}`")
                linhas.append("")

    linhas.append("")
    linhas.append("## 3. Ocorrências detalhadas dos top arquivos")
    linhas.append("")

    for item in resultado["arquivos"][:30]:
        linhas.append(f"### `{item['arquivo']}`")
        linhas.append("")
        linhas.append(f"Score: `{item['score']}`")
        linhas.append("")
        linhas.append("| Categoria | Linha | Trecho |")
        linhas.append("|---|---:|---|")

        for occ in item["ocorrencias"][:100]:
            trecho = occ["trecho"].replace("|", "\\|")
            linhas.append(f"| `{occ['categoria']}` | {occ['linha']} | `{trecho}` |")

        linhas.append("")

    linhas.append("## 4. Comandos Git úteis")
    linhas.append("")
    linhas.append("Buscar leitura RTD/Excel:")
    linhas.append("")
    linhas.append("```bash")
    linhas.append("git grep -n -I -E \"RTD|Excel|xlwings|openpyxl|win32com|Dispatch|Worksheet|Workbook|Range|Cells\" -- '*.py'")
    linhas.append("```")
    linhas.append("")
    linhas.append("Buscar tabelas RTD legadas:")
    linhas.append("")
    linhas.append("```bash")
    linhas.append("git grep -n -I -E \"rtd_analise_robo_legs|manual_analise_robo_legs|rtd_analise_robo|rtd_hist_robo\" -- '*.py'")
    linhas.append("```")
    linhas.append("")
    linhas.append("Buscar tabela canônica de legs:")
    linhas.append("")
    linhas.append("```bash")
    linhas.append("git grep -n -I -E \"structure_legs|replace_legs|create_structure|option_type|expiration_date|strike|premium\" -- '*.py'")
    linhas.append("```")
    linhas.append("")
    linhas.append("Buscar snapshot de mercado:")
    linhas.append("")
    linhas.append("```bash")
    linhas.append("git grep -n -I -E \"MarketSnapshot|market_snapshot|snapshot|manual.*rtd|rtd.*manual|source.*RTD\" -- '*.py'")
    linhas.append("```")
    linhas.append("")

    linhas.append("## 5. Próxima arquitetura recomendada")
    linhas.append("")
    linhas.append("Fluxo recomendado:")
    linhas.append("")
    linhas.append("```text")
    linhas.append("Aba Excel fixa RTD_LINKS")
    linhas.append("        ↓")
    linhas.append("Leitor RTD centralizado")
    linhas.append("        ↓")
    linhas.append("Tabela app.db/rtd_option_quotes")
    linhas.append("        ↓")
    linhas.append("MarketSnapshotRepository")
    linhas.append("        ↓")
    linhas.append("UI / payoff / decisões / detalhes")
    linhas.append("```")
    linhas.append("")

    return "\n".join(linhas)


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    arquivos_git = git_ls_files()
    analisados = []

    for rel_path in arquivos_git:
        if deve_ignorar(rel_path):
            continue

        item = analisar_arquivo(rel_path)
        if item["score"] > 0:
            analisados.append(item)

    analisados.sort(key=lambda x: x["score"], reverse=True)

    resultado = {
        "gerado_em": datetime.now().isoformat(),
        "root": str(ROOT),
        "total_arquivos_git": len(arquivos_git),
        "total_analisados_com_score": len(analisados),
        "arquivos": analisados,
    }

    OUTPUT_JSON.write_text(
        json.dumps(resultado, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    OUTPUT_MD.write_text(
        gerar_markdown(resultado),
        encoding="utf-8",
    )

    print("")
    print("Mapeamento Git concluído.")
    print(f"Relatório Markdown: {OUTPUT_MD}")
    print(f"Relatório JSON:     {OUTPUT_JSON}")
    print("")
    print("Top 25 arquivos reais mais prováveis:")
    print("")

    for item in analisados[:25]:
        cats = ", ".join(f"{k}:{v}" for k, v in item["categorias"].items())
        print(f"- score {item['score']:>5} | {item['arquivo']} | {cats}")


if __name__ == "__main__":
    main()
