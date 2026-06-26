# Checklist RTD Underlying Quotes

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

    grep -R "dados/app.db\|dados/derived.db\|MYHUBIA_DB_PATH\|APP_DB_PATH\|DERIVED_DB_PATH" -n services scripts ATT db repositories --exclude-dir=.git --exclude-dir=__pycache__ --binary-files=without-match

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
