# Fonte autoritativa RTD para ativos-base

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
