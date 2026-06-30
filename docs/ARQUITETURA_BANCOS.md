# Arquitetura de Bancos

Atualizado em: 2026-06-30 18:42:54

## Decisão oficial

A partir desta etapa, o banco canônico de dados vivos é:

    dados/app.db

O banco de derivados é:

    dados/derived.db

## Responsabilidade do dados/app.db

O dados/app.db guarda estado operacional e dados vivos usados pela aplicação.

Inclui:

    estruturas
    legs
    configurações operacionais
    dados manuais operacionais
    rtd_option_quotes
    rtd_underlying_quotes
    snapshots atuais de mercado
    dados usados diretamente pela UI
    dados usados pelo pricing runtime

## Responsabilidade do dados/derived.db

O dados/derived.db guarda resultados derivados e artefatos regeneráveis.

Inclui:

    payoff
    simulações
    curvas calculadas
    caches derivados
    resultados pesados
    artefatos que podem ser recriados
    consolidações históricas quando forem tratadas como derivadas

## Regra para dados vivos

Dados vivos de mercado devem existir como fonte ativa somente em:

    dados/app.db

Tabelas oficiais:

    dados/app.db.rtd_option_quotes
    dados/app.db.rtd_underlying_quotes

## Regra para derived.db

O dados/derived.db não deve ser fonte ativa de cotação viva.

Se houver tabelas antigas de RTD em derived.db, elas devem ser tratadas como legado, arquivadas ou removidas em fase controlada.

## Regra contra sincronização

Não manter processo contínuo de sincronização:

    derived.db para app.db
    app.db para derived.db

Motivo:

    cria ambiguidade de fonte
    permite divergência silenciosa
    aumenta risco operacional
    dificulta debug
    pode fazer pricing usar preço defasado

## Contrato de leitura da UI e pricing

A UI e o pricing runtime devem ler dados vivos em:

    dados/app.db

O MarketSnapshotRepository deve usar app.db para snapshot de mercado vivo.

Repositórios de RTD devem ter default em:

    dados/app.db

## Contrato de escrita de RTD

Scripts e coletores de RTD devem gravar em:

    dados/app.db

Não devem gravar RTD vivo em:

    dados/derived.db

## Migração segura

A migração segura deve seguir:

    confirmar app.db completo
    alterar defaults de RTD para app.db
    testar repositories e selectors
    criar teste de contrato
    arquivar tabelas RTD antigas em derived.db
    rodar suíte completa
    commitar fase concluída
