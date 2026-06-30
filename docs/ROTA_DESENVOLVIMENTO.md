# Rota de Desenvolvimento

Atualizado em: 2026-06-30 18:42:54

## Estado decidido

A arquitetura oficial para dados vivos está definida.

Fonte oficial de mercado vivo:

    dados/app.db

Banco de derivados:

    dados/derived.db

Excel operacional:

    LISTA_RTD.xlsm aberto durante o uso do sistema

## Ordem de execução

### Marco 1: documentação alinhada

Objetivo:

    atualizar documentação oficial
    registrar decisão arquitetural
    criar auditoria de desenvolvimento
    garantir que não haja divergência documental

Critérios de conclusão:

    docs atualizados
    README apontando para documentação nova
    auditoria criada ou atualizada
    validação documental executada
    commit realizado

### Marco 2: contrato de banco

Objetivo:

    app.db vira fonte única de dados vivos
    derived.db deixa de ser fonte ativa de RTD
    defaults de RTD apontam para app.db
    teste de contrato protege regressão

Critérios de conclusão:

    rtd_option_quotes disponível em app.db
    rtd_underlying_quotes disponível em app.db
    repositórios RTD usam app.db por default
    scripts RTD usam app.db por default
    testes de market snapshot passam
    suíte relevante passa
    commit realizado

### Marco 3: desativação segura do RTD em derived.db

Objetivo:

    impedir uso acidental de derived.db como fonte de cotação viva

Critérios de conclusão:

    tabelas RTD antigas em derived.db arquivadas como legado ou removidas
    nenhum fluxo runtime depende delas
    testes passam
    auditoria atualizada
    commit realizado

### Marco 4: Excel RTD vivo

Objetivo:

    manter LISTA_RTD.xlsm aberto
    detectar Excel aberto
    detectar planilha correta
    ler tabela viva de RTD
    atualizar snapshot em app.db

Critérios de conclusão:

    sistema detecta Excel
    sistema valida workbook e aba
    coletor lê dados em bloco
    snapshot app.db atualiza
    status RTD aparece na UI ou em ajuda
    testes passam
    commit realizado

### Marco 5: snapshot centralizado

Objetivo:

    legs, estruturas, UI e pricing consomem snapshot centralizado

Critérios de conclusão:

    botão Preencher por RTD lê snapshot
    subprocesso por opção deixa de ser caminho principal
    normalização centralizada
    testes passam
    auditoria atualizada
    commit realizado

### Marco 6: histórico intraday

Objetivo:

    gravar pontos relevantes com controle de frequência

Critérios de conclusão:

    histórico possui timestamp, símbolo, preço, VWAP, bid, ask e volume
    gravação evita linhas idênticas excessivas
    política de retenção documentada
    testes passam
    commit realizado

### Marco 7: candles

Objetivo:

    gerar candles a partir do histórico capturado

Critérios de conclusão:

    candle de 1 minuto gerado
    VWAP associado ao candle
    fonte de preço identificada
    gráfico usa dados, não imagem como base principal
    testes passam
    commit realizado

### Marco 8: UI operacional viva

Objetivo:

    tela operacional acompanha dados vivos com limite de atualização

Critérios de conclusão:

    painel de opções atualiza
    estruturas atualizam
    gráfico atualiza
    status de RTD aparece
    UI não redesenha a cada microalteração
    testes passam
    commit realizado

### Marco 9: retenção e alertas

Objetivo:

    manter performance e adicionar decisão operacional

Critérios de conclusão:

    limpeza de ticks brutos
    consolidação de candles
    compactação se necessária
    alertas por VWAP, spread, liquidez e payoff
    testes passam
    commit realizado

## Regra de teste acumulado

Ao encerrar uma fase, o teste deve cobrir também as fases já encerradas.

Não deixar pendências sem auditoria.

## Regra de commit

Cada alteração concluída e testada deve ser commitada.

Mensagem recomendada para este marco:

    docs: alinhar rota RTD vivo e contrato de bancos
