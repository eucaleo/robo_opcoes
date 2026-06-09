import os
import re
import json
import sqlite3
from datetime import datetime
from pathlib import Path

ROOT = Path.cwd()

DBS = [
    ROOT / "dados" / "app.db",
    ROOT / "dados" / "derived.db",
]

OUTPUT_DIR = ROOT / "reports"
OUTPUT_MD = OUTPUT_DIR / "mapeamento_rtd_opcoes.md"
OUTPUT_JSON = OUTPUT_DIR / "mapeamento_rtd_opcoes.json"

IGNORAR_DIRS = {
    ".git",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
    "dist",
    "build",
    ".next",
    ".cache",
    "reports",
}

EXTENSOES_ANALISAR = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".json",
    ".sql",
    ".env",
    ".ini",
    ".yaml",
    ".yml",
    ".toml",
    ".md",
    ".txt",
    ".html",
    ".css",
}

PADROES = {
    "excel": [
        r"\bexcel\b",
        r"\bxlsx\b",
        r"\bxlsm\b",
        r"\bxlwings\b",
        r"\bopenpyxl\b",
        r"\bwin32com\b",
        r"\bWorkbook\b",
        r"\bWorksheet\b",
        r"\bsheet\b",
        r"\baba\b",
        r"\brange\b",
        r"\bcells?\b",
    ],
    "rtd": [
        r"\brtd\b",
        r"RTD\(",
        r"RTD",
        r"Profit",
        r"Tryd",
        r"Broadcast",
        r"Nelógica",
        r"NelOGICA",
        r"Excel\.Application",
    ],
    "bancos_sqlite": [
        r"app\.db",
        r"derived\.db",
        r"sqlite",
        r"sqlite3",
        r"SQLAlchemy",
        r"create_engine",
        r"INSERT INTO",
        r"UPDATE",
        r"DELETE FROM",
        r"SELECT",
        r"FROM rtd_",
        r"FROM structures",
        r"FROM structure_legs",
    ],
    "opcoes_campos": [
        r"ativo",
        r"underlying",
        r"ticker",
        r"symbol",
        r"codigo",
        r"código",
        r"opcao",
        r"opção",
        r"option",
        r"strike",
        r"vencimento",
        r"expiry",
        r"expiration",
        r"call",
        r"put",
        r"tipo",
        r"preco",
        r"preço",
        r"price",
        r"last",
        r"ultimo",
        r"último",
        r"quantidade",
        r"qty",
        r"volume",
        r"bid",
        r"ask",
        r"delta",
        r"gamma",
        r"theta",
        r"vega",
        r"iv",
        r"volatilidade",
    ],
    "tabelas_sistema": [
        r"rtd_analise_robo",
        r"rtd_analise_robo_legs",
        r"rtd_analise_raiox",
        r"rtd_consolidacoes",
        r"rtd_configuracoes",
        r"rtd_encerramentos_manuais",
        r"rtd_hist_robo",
        r"rtd_rolls_detectados",
        r"manual_analise_robo_legs",
        r"pricing_executions",
        r"structures",
        r"structure_legs",
        r"structure_audit_log",
        r"payoff_curve_points",
        r"payoff_curve_summary",
        r"structure_decisions",
    ],
    "frontend_backend_rotas": [
        r"fetch\(",
        r"axios",
        r"api/",
        r"/api",
        r"router",
        r"express",
        r"FastAPI",
        r"Flask",
        r"@app\.route",
        r"@router",
        r"useEffect",
        r"useState",
    ],
}

def deve_ignorar(path: Path) -> bool:
    partes = set(path.parts)
    return bool(partes.intersection(IGNORAR_DIRS))

def ler_arquivo_texto(path: Path):
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        try:
            return path.read_text(encoding="latin-1", errors="ignore")
        except Exception:
            return None

def procurar_ocorrencias():
    resultados = []

    for path in ROOT.rglob("*"):
        if deve_ignorar(path):
            continue

        if not path.is_file():
            continue

        if path.suffix.lower() not in EXTENSOES_ANALISAR:
            continue

        conteudo = ler_arquivo_texto(path)
        if conteudo is None:
            continue

        linhas = conteudo.splitlines()

        for categoria, padroes in PADROES.items():
            for padrao in padroes:
                regex = re.compile(padrao, re.IGNORECASE)

                for idx, linha in enumerate(linhas, start=1):
                    if regex.search(linha):
                        resultados.append({
                            "categoria": categoria,
                            "padrao": padrao,
                            "arquivo": str(path.relative_to(ROOT)),
                            "linha": idx,
                            "trecho": linha.strip()[:250],
                        })

    return resultados

def mapear_banco(db_path: Path):
    info = {
        "arquivo": str(db_path.relative_to(ROOT)) if db_path.exists() else str(db_path),
        "existe": db_path.exists(),
        "tabelas": [],
    }

    if not db_path.exists():
        return info

    try:
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        tabelas = cur.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """).fetchall()

        for row in tabelas:
            tabela = row["name"]

            colunas = cur.execute(f"PRAGMA table_info({tabela})").fetchall()
            fks = cur.execute(f"PRAGMA foreign_key_list({tabela})").fetchall()

            try:
                qtd = cur.execute(f"SELECT COUNT(*) AS total FROM {tabela}").fetchone()["total"]
            except Exception:
                qtd = None

            info["tabelas"].append({
                "nome": tabela,
                "total_linhas": qtd,
                "colunas": [
                    {
                        "cid": c["cid"],
                        "nome": c["name"],
                        "tipo": c["type"],
                        "notnull": c["notnull"],
                        "default": c["dflt_value"],
                        "pk": c["pk"],
                    }
                    for c in colunas
                ],
                "foreign_keys": [
                    dict(fk) for fk in fks
                ],
            })

        conn.close()

    except Exception as e:
        info["erro"] = str(e)

    return info

def consolidar_por_arquivo(ocorrencias):
    por_arquivo = {}

    for item in ocorrencias:
        arq = item["arquivo"]
        por_arquivo.setdefault(arq, {
            "arquivo": arq,
            "categorias": {},
            "ocorrencias": [],
            "score": 0,
        })

        categoria = item["categoria"]
        por_arquivo[arq]["categorias"].setdefault(categoria, 0)
        por_arquivo[arq]["categorias"][categoria] += 1
        por_arquivo[arq]["ocorrencias"].append(item)

    pesos = {
        "excel": 4,
        "rtd": 5,
        "bancos_sqlite": 4,
        "opcoes_campos": 3,
        "tabelas_sistema": 5,
        "frontend_backend_rotas": 2,
    }

    for arq, dados in por_arquivo.items():
        score = 0
        for categoria, qtd in dados["categorias"].items():
            score += pesos.get(categoria, 1) * qtd
        dados["score"] = score

    return sorted(por_arquivo.values(), key=lambda x: x["score"], reverse=True)

def gerar_markdown(dados):
    linhas = []

    linhas.append("# Mapeamento RTD / Opções / SQLite")
    linhas.append("")
    linhas.append(f"Gerado em: `{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}`")
    linhas.append(f"Projeto analisado: `{ROOT}`")
    linhas.append("")

    linhas.append("## 1. Objetivo")
    linhas.append("")
    linhas.append("Este relatório mapeia onde o sistema parece lidar com:")
    linhas.append("")
    linhas.append("- Excel")
    linhas.append("- RTD")
    linhas.append("- SQLite")
    linhas.append("- Dados de opções")
    linhas.append("- Tabelas relacionadas a robô, estruturas e legs")
    linhas.append("")
    linhas.append("A intenção é identificar onde mexer para automatizar a busca dos dados básicos das opções.")
    linhas.append("")

    linhas.append("## 2. Bancos SQLite encontrados")
    linhas.append("")

    for banco in dados["bancos"]:
        linhas.append(f"### `{banco['arquivo']}`")
        linhas.append("")
        linhas.append(f"- Existe: `{banco['existe']}`")
        linhas.append("")

        if not banco["existe"]:
            continue

        if banco.get("erro"):
            linhas.append(f"- Erro ao ler banco: `{banco['erro']}`")
            linhas.append("")
            continue

        for tabela in banco["tabelas"]:
            linhas.append(f"#### Tabela `{tabela['nome']}`")
            linhas.append("")
            linhas.append(f"- Linhas atuais: `{tabela['total_linhas']}`")
            linhas.append("")
            linhas.append("| Coluna | Tipo | PK | Not Null | Default |")
            linhas.append("|---|---|---:|---:|---|")

            for col in tabela["colunas"]:
                linhas.append(
                    f"| `{col['nome']}` | `{col['tipo']}` | `{col['pk']}` | `{col['notnull']}` | `{col['default']}` |"
                )

            if tabela["foreign_keys"]:
                linhas.append("")
                linhas.append("Foreign keys:")
                linhas.append("")
                for fk in tabela["foreign_keys"]:
                    linhas.append(f"- `{fk}`")

            linhas.append("")

    linhas.append("## 3. Arquivos mais prováveis para alteração")
    linhas.append("")
    linhas.append("Estes arquivos receberam maior pontuação por conterem referências a Excel, RTD, SQLite, opções ou tabelas do sistema.")
    linhas.append("")

    linhas.append("| Score | Arquivo | Categorias encontradas |")
    linhas.append("|---:|---|---|")

    for item in dados["arquivos_prioritarios"][:40]:
        cats = ", ".join([f"{k}: {v}" for k, v in item["categorias"].items()])
        linhas.append(f"| {item['score']} | `{item['arquivo']}` | {cats} |")

    linhas.append("")

    linhas.append("## 4. Ocorrências detalhadas")
    linhas.append("")

    for item in dados["arquivos_prioritarios"][:30]:
        linhas.append(f"### `{item['arquivo']}`")
        linhas.append("")
        linhas.append(f"Score: `{item['score']}`")
        linhas.append("")
        linhas.append("| Categoria | Linha | Trecho |")
        linhas.append("|---|---:|---|")

        for occ in item["ocorrencias"][:80]:
            trecho = occ["trecho"].replace("|", "\\|")
            linhas.append(f"| `{occ['categoria']}` | {occ['linha']} | `{trecho}` |")

        linhas.append("")

    linhas.append("## 5. Campos que precisam estar automatizados")
    linhas.append("")
    linhas.append("Para cada opção inserida no sistema, o fluxo ideal deveria preencher automaticamente:")
    linhas.append("")
    linhas.append("| Campo | Origem provável | Observação |")
    linhas.append("|---|---|---|")
    linhas.append("| Ativo base | RTD ou cadastro interno | Exemplo: PETR4, VALE3, BOVA11 |")
    linhas.append("| Código da opção | Usuário ou estrutura | Exemplo: PETRA123 |")
    linhas.append("| Tipo | RTD ou parser do código | CALL ou PUT |")
    linhas.append("| Strike | RTD ou parser/cadastro B3 | Preço de exercício |")
    linhas.append("| Vencimento | RTD ou parser/cadastro B3 | Data de expiração |")
    linhas.append("| Último preço | RTD | Último negócio da opção |")
    linhas.append("| Última quantidade negociada | RTD | Quantidade do último negócio |")
    linhas.append("| Bid | RTD | Melhor comprador |")
    linhas.append("| Ask | RTD | Melhor vendedor |")
    linhas.append("| Volume | RTD | Volume negociado |")
    linhas.append("")

    linhas.append("## 6. Sugestão de arquitetura com aba única RTD")
    linhas.append("")
    linhas.append("A sugestão de usar uma aba única com todos os links RTD é boa.")
    linhas.append("")
    linhas.append("Modelo recomendado:")
    linhas.append("")
    linhas.append("### Aba Excel: `RTD_LINKS`")
    linhas.append("")
    linhas.append("| Coluna | Nome | Função |")
    linhas.append("|---|---|---|")
    linhas.append("| A | `chave` | Identificador único, exemplo `PETRA123_ULTIMO` |")
    linhas.append("| B | `codigo_opcao` | Código da opção |")
    linhas.append("| C | `campo` | Campo desejado: `ultimo`, `strike`, `vencimento`, `tipo`, `quantidade` |")
    linhas.append("| D | `formula_rtd` | Fórmula RTD usada pelo Excel |")
    linhas.append("| E | `valor` | Valor retornado pelo RTD |")
    linhas.append("| F | `atualizado_em` | Timestamp opcional |")
    linhas.append("")
    linhas.append("O sistema então passa a ler sempre a mesma aba e as mesmas colunas.")
    linhas.append("")
    linhas.append("Vantagens:")
    linhas.append("")
    linhas.append("- Remove dependência de várias abas diferentes.")
    linhas.append("- Facilita manutenção.")
    linhas.append("- Permite cache no SQLite.")
    linhas.append("- Facilita descobrir quando algum campo RTD veio vazio.")
    linhas.append("- Permite logar erros de atualização.")
    linhas.append("")

    linhas.append("## 7. Próximo passo recomendado")
    linhas.append("")
    linhas.append("Depois de analisar os arquivos prioritários deste relatório, implementar uma camada única:")
    linhas.append("")
    linhas.append("```text")
    linhas.append("Excel RTD_LINKS")
    linhas.append("    ↓")
    linhas.append("Leitor RTD centralizado")
    linhas.append("    ↓")
    linhas.append("Tabela SQLite de cache/cotações")
    linhas.append("    ↓")
    linhas.append("Robô / análise / payoff / telas")
    linhas.append("```")
    linhas.append("")
    linhas.append("Tabela sugerida para cache:")
    linhas.append("")
    linhas.append("```sql")
    linhas.append("CREATE TABLE IF NOT EXISTS rtd_option_quotes (")
    linhas.append("    id INTEGER PRIMARY KEY AUTOINCREMENT,")
    linhas.append("    codigo_opcao TEXT NOT NULL,")
    linhas.append("    ativo_base TEXT,")
    linhas.append("    tipo TEXT,")
    linhas.append("    strike REAL,")
    linhas.append("    vencimento TEXT,")
    linhas.append("    ultimo_preco REAL,")
    linhas.append("    ultima_quantidade REAL,")
    linhas.append("    bid REAL,")
    linhas.append("    ask REAL,")
    linhas.append("    volume REAL,")
    linhas.append("    fonte TEXT DEFAULT 'EXCEL_RTD',")
    linhas.append("    atualizado_em TEXT DEFAULT CURRENT_TIMESTAMP,")
    linhas.append("    UNIQUE(codigo_opcao)")
    linhas.append(");")
    linhas.append("```")
    linhas.append("")

    return "\n".join(linhas)

def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    print("Mapeando arquivos do projeto...")
    ocorrencias = procurar_ocorrencias()

    print("Mapeando bancos SQLite...")
    bancos = [mapear_banco(db) for db in DBS]

    arquivos_prioritarios = consolidar_por_arquivo(ocorrencias)

    dados = {
        "gerado_em": datetime.now().isoformat(),
        "root": str(ROOT),
        "total_ocorrencias": len(ocorrencias),
        "bancos": bancos,
        "arquivos_prioritarios": arquivos_prioritarios,
        "ocorrencias": ocorrencias,
    }

    OUTPUT_JSON.write_text(
        json.dumps(dados, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    OUTPUT_MD.write_text(
        gerar_markdown(dados),
        encoding="utf-8"
    )

    print("")
    print("Mapeamento concluído.")
    print(f"Relatório Markdown: {OUTPUT_MD}")
    print(f"Relatório JSON:     {OUTPUT_JSON}")
    print("")
    print("Arquivos mais prováveis para mexer:")
    print("")

    for item in arquivos_prioritarios[:15]:
        cats = ", ".join([f"{k}:{v}" for k, v in item["categorias"].items()])
        print(f"- score {item['score']:>4} | {item['arquivo']} | {cats}")

if __name__ == "__main__":
    main()
