#!/usr/bin/env bash
set -u

echo "=== Inicio: geracao de documentacao RTD ==="
echo "Diretorio atual:"
pwd
echo

python - <<'PY'
from pathlib import Path

root = Path(".")
docs = root / "docs"

print("=== Busca de documentos existentes ===")

candidates = []

if docs.exists():
    for path in sorted(docs.rglob("*")):
        if path.is_file():
            suffix = path.suffix.lower()
            name = path.name.lower()
            if suffix in [".md", ".txt", ".rst"] or "readme" in name or "doc" in name:
                candidates.append(path)

if not candidates:
    for path in sorted(root.rglob("*")):
        if ".git" in path.parts or "__pycache__" in path.parts:
            continue
        if path.is_file():
            suffix = path.suffix.lower()
            name = path.name.lower()
            parts = " ".join(path.parts).lower()
            if suffix in [".md", ".txt", ".rst"] and (
                "readme" in name
                or "doc" in name
                or "arquitetura" in parts
                or "rtd" in parts
                or "market" in parts
                or "snapshot" in parts
                or "canonical" in parts
            ):
                candidates.append(path)

if candidates:
    for path in candidates:
        print(path.as_posix())
else:
    print("Nenhum documento existente encontrado. A pasta docs sera criada.")

docs.mkdir(exist_ok=True)
(docs / "arquitetura").mkdir(parents=True, exist_ok=True)
(docs / "checklists").mkdir(parents=True, exist_ok=True)

arquitetura_path = docs / "arquitetura" / "fonte_autoritativa_rtd_ativos_base.md"
checklist_path = docs / "checklists" / "rtd_underlying_quotes.md"

arquitetura = """# Fonte autoritativa RTD para ativos-base

## Objetivo

Este documento registra a fonte autoritativa de precos atuais dos ativos-base usados pelo fluxo canonico de precificacao.

A validacao em runtime confirmou que o servico MarketSnapshotProvider consome corretamente os precos vindos da tabela rtd_underlying_quotes no banco dados/app.db.

## Fluxo validado

    BTG RTD via Excel
        |
        v
    LISTA_RTD.xlsm
        |
        v
    dados/RTD_UNDERLYING_QUOTES.csv
        |
        v
    scripts/import_rtd_underlying_quotes_csv.py
        |
        v
    dados/app.db
        |
        v
    rtd_underlying_quotes
        |
        v
    services/market_snapshot_provider.py
        |
        v
    services/canonical_input_service.py
        |
        v
    pipeline canonico de precificacao

## Banco operacional

O banco operacional esperado para os precos RTD dos ativos-base e:

    dados/app.db

A tabela esperada e:

    rtd_underlying_quotes

A tabela rtd_underlying_quotes nao deve ser criada em dados/derived.db.

## Separacao entre bancos

A separacao esperada e:

    dados/app.db
        Dados operacionais e fontes autoritativas de entrada.

    dados/derived.db
        Dados derivados, como curvas de payoff, decisoes e resultados calculados.

Portanto, rtd_underlying_quotes pertence ao banco operacional dados/app.db.

## Provider de mercado

O servico autoritativo para resolver spot, taxa e volatilidade e:

    services/market_snapshot_provider.py

O metodo publico validado e:

    MarketSnapshotProvider.get_snapshot

Em execucao normal, o provider usa o banco padrao:

    dados/app.db

Esse caminho pode ser sobrescrito pela variavel de ambiente:

    MYHUBIA_DB_PATH

Em ambiente normal de desenvolvimento, essa variavel deve estar vazia ou apontar explicitamente para dados/app.db.

## Integracao com o fluxo canonico

O servico canonico instancia o provider assim:

    CanonicalInputService
        |
        v
    MarketSnapshotProvider()

Esse comportamento foi encontrado em:

    services/canonical_input_service.py

Nao foi encontrado uso runtime apontando MarketSnapshotProvider para dados/derived.db.

## Evidencia de validacao

A validacao em runtime retornou snapshots com os seguintes sinais:

    snapshot_source: rtd_underlying_quotes
    market_snapshot_source: rtd_underlying_quotes
    is_static_fallback: False
    is_current_market: True
    market_snapshot_rtd_source: btg_rtd_excel_underlying

Exemplo validado para BOVA11:

    reference_date: 2026-06-26
    underlying_asset: BOVA11
    spot_price: 170.55
    interest_rate: 0.1175
    volatility: 0.22
    snapshot_source: rtd_underlying_quotes
    market_snapshot_source: rtd_underlying_quotes
    is_static_fallback: False
    is_current_market: True

Exemplo validado para PRIO3:

    reference_date: 2026-06-26
    underlying_asset: PRIO3
    spot_price: 53.2
    interest_rate: 0.1175
    volatility: 0.35
    snapshot_source: rtd_underlying_quotes
    market_snapshot_source: rtd_underlying_quotes
    is_static_fallback: False
    is_current_market: True

## Contrato esperado

O fluxo canonico de precificacao deve obter spot por meio do MarketSnapshotProvider.

O uso de fallback estatico deve ser tratado como excecao operacional e deve ser sinalizado por:

    is_static_fallback: True

Quando os dados RTD estiverem disponiveis, o esperado e:

    is_static_fallback: False
    snapshot_source: rtd_underlying_quotes
    market_snapshot_source: rtd_underlying_quotes

## Comandos principais

Atualizar RTD de ativos-base:

    python scripts/run_rtd_underlying_refresh_full.py --db dados/app.db

Validar variavel de ambiente:

    echo ${MYHUBIA_DB_PATH:-vazio}

Validar snapshots pelo provider:

    python
        from services.market_snapshot_provider import MarketSnapshotProvider

        provider = MarketSnapshotProvider()

        for asset in ["BOVA11", "PRIO3"]:
            print()
            print("===", asset, "===")
            print(provider.get_snapshot(asset))

## Decisao registrada

A fonte autoritativa para precos atuais de ativos-base e:

    dados/app.db:rtd_underlying_quotes

O consumidor canonico e:

    MarketSnapshotProvider.get_snapshot

O banco dados/derived.db nao deve ser usado como fonte de precos RTD de ativos-base.
"""

checklist = """# Checklist RTD Underlying Quotes

## Objetivo

Validar que os precos dos ativos-base vindos do RTD estao sendo importados e consumidos corretamente pelo pipeline canonico.

## Banco esperado

    dados/app.db

## Tabela esperada

    rtd_underlying_quotes

## Arquivos principais

    LISTA_RTD.xlsm
    dados/rtd_underlying_symbols.txt
    dados/RTD_UNDERLYING_QUOTES.csv
    scripts/run_rtd_underlying_refresh_full.py
    scripts/import_rtd_underlying_quotes_csv.py
    scripts/refresh_rtd_underlying_quotes_excel.ps1
    services/market_snapshot_provider.py
    services/canonical_input_service.py

## Passo 1: verificar variavel de ambiente

Executar:

    echo ${MYHUBIA_DB_PATH:-vazio}

Resultado esperado:

    vazio

Tambem e aceitavel:

    dados/app.db

Resultado indevido:

    dados/derived.db

Se o resultado for dados/derived.db, corrigir o ambiente antes de rodar o pipeline.

## Passo 2: atualizar RTD de ativos-base

Executar:

    python scripts/run_rtd_underlying_refresh_full.py --db dados/app.db

Resultado esperado:

    OK: pipeline RTD de ativos-base finalizado.

Tambem devem aparecer os dados antes e depois da atualizacao, com aumento de max_updated_at.

## Passo 3: consultar tabela no banco

Executar Python com esta logica:

    import sqlite3

    con = sqlite3.connect("dados/app.db")
    con.row_factory = sqlite3.Row

    rows = con.execute(
        "SELECT ativo, ultimo_preco, source, updated_at FROM rtd_underlying_quotes ORDER BY ativo"
    ).fetchall()

    for row in rows:
        print(dict(row))

    con.close()

Resultado esperado:

    ativo preenchido
    ultimo_preco numerico e maior que zero
    source igual a btg_rtd_excel_underlying
    updated_at recente

## Passo 4: validar MarketSnapshotProvider

Executar Python com esta logica:

    from services.market_snapshot_provider import MarketSnapshotProvider

    provider = MarketSnapshotProvider()

    for asset in ["BOVA11", "PRIO3"]:
        print()
        print("===", asset, "===")
        snapshot = provider.get_snapshot(asset)
        print(snapshot)

Resultado esperado no snapshot:

    snapshot_source: rtd_underlying_quotes
    market_snapshot_source: rtd_underlying_quotes
    is_static_fallback: False
    is_current_market: True
    market_snapshot_rtd_source: btg_rtd_excel_underlying

## Passo 5: interpretar resultado

Se snapshot_source for rtd_underlying_quotes, o provider esta lendo corretamente de dados/app.db.

Se is_static_fallback for False, o fluxo nao esta usando fallback estatico.

Se is_current_market for True, o snapshot foi considerado atual.

## Passo 6: investigar falhas

Se o provider nao retornar rtd_underlying_quotes, verificar:

    MYHUBIA_DB_PATH
    existencia de dados/app.db
    existencia da tabela rtd_underlying_quotes
    conteudo da coluna ultimo_preco
    caminho passado explicitamente para MarketSnapshotProvider
    chamadas em services/canonical_input_service.py

Buscar referencias:

    grep -R "MarketSnapshotProvider" -n . --exclude-dir=.git --exclude-dir=__pycache__ --exclude-dir=docs --binary-files=without-match

Buscar caminhos de banco:

    grep -R "dados/app.db\\|dados/derived.db\\|MYHUBIA_DB_PATH\\|APP_DB_PATH\\|DERIVED_DB_PATH" -n services scripts ATT db repositories --exclude-dir=.git --exclude-dir=__pycache__ --binary-files=without-match

## Criterio de aceite

O checklist esta aprovado quando:

    rtd_underlying_quotes existe em dados/app.db
    a tabela possui linhas para os ativos-base ativos
    ultimo_preco esta preenchido
    MarketSnapshotProvider.get_snapshot retorna snapshot_source igual a rtd_underlying_quotes
    MarketSnapshotProvider.get_snapshot retorna is_static_fallback igual a False
    CanonicalInputService instancia MarketSnapshotProvider sem apontar para dados/derived.db

## Decisao operacional

Nao criar rtd_underlying_quotes em dados/derived.db.

Nao usar dados/derived.db como fonte de precos RTD de ativos-base.

Usar dados/app.db como banco operacional da fonte RTD.
"""

arquitetura_path.write_text(arquitetura, encoding="utf-8")
checklist_path.write_text(checklist, encoding="utf-8")

index_candidates = [
    docs / "README.md",
    docs / "index.md",
    root / "README.md",
]

section = """
## Documentacao RTD de ativos-base

- docs/arquitetura/fonte_autoritativa_rtd_ativos_base.md
- docs/checklists/rtd_underlying_quotes.md
"""

for index_path in index_candidates:
    if index_path.exists():
        current = index_path.read_text(encoding="utf-8", errors="replace")
        if "fonte_autoritativa_rtd_ativos_base.md" not in current:
            if current and not current.endswith("\n"):
                current += "\n"
            current += section
            index_path.write_text(current, encoding="utf-8")
            print("Indice atualizado:", index_path.as_posix())
        else:
            print("Indice ja continha os links:", index_path.as_posix())
        break
else:
    readme = docs / "README.md"
    readme.write_text("# Documentacao\n" + section, encoding="utf-8")
    print("Indice criado:", readme.as_posix())

print()
print("=== Arquivos gerados ou atualizados ===")
for path in [arquitetura_path, checklist_path, docs / "README.md", docs / "index.md", root / "README.md"]:
    if path.exists():
        print(path.as_posix())

print()
print("=== Validacao sem crase nos documentos RTD gerados ===")

bad = []
for path in [arquitetura_path, checklist_path]:
    text = path.read_text(encoding="utf-8", errors="replace")
    if chr(96) in text:
        bad.append(path)

if bad:
    print("Falha: crase encontrada em:")
    for path in bad:
        print(path.as_posix())
    raise SystemExit(1)

print("OK: documentos RTD gerados sem crase.")
PY

py_status=$?

echo
echo "=== Status Python ==="
echo "$py_status"

if [ "$py_status" -ne 0 ]; then
    echo "Falha na geracao dos documentos."
    exit "$py_status"
fi

echo
echo "=== Diff dos documentos ==="
git diff -- docs README.md 2>/dev/null || git diff -- docs

echo
echo "=== Status Git ==="
git status --short

echo
echo "=== Fim: geracao concluida ==="
