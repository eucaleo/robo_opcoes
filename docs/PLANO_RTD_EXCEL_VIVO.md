# Plano RTD Excel Vivo

Atualizado em: 2026-06-30 18:50:17

## Objetivo

Este documento define a rota oficial para transformar o RTD em uma fonte viva de dados para o sistema, mantendo o Excel LISTA_RTD.xlsm aberto durante a operação e usando o banco correto para cada tipo de informação.

## Decisão arquitetural principal

A fonte oficial de mercado vivo é:

    dados/app.db

O banco de derivados é:

    dados/derived.db

A separação oficial é:

    dados/app.db
        banco canônico operacional
        dados vivos
        estruturas
        legs
        cotações RTD atuais
        UI
        pricing runtime

    dados/derived.db
        resultados derivados
        caches
        payoff
        simulações
        candles consolidados quando tratados como artefatos derivados
        artefatos regeneráveis

## Tabelas de mercado vivo

As tabelas abaixo pertencem ao banco canônico operacional:

    dados/app.db.rtd_option_quotes
    dados/app.db.rtd_underlying_quotes

As mesmas tabelas não devem ser usadas como fonte ativa em:

    dados/derived.db

Decisão final:

    rtd_option_quotes -> app.db
    rtd_underlying_quotes -> app.db

## Regra contra sincronização entre bancos

Não manter sync contínuo:

    derived.db -> app.db
    app.db -> derived.db

Para cotação viva, sincronização contínua entre bancos é dívida técnica e risco operacional.

Scripts de importação, reconciliação ou manutenção podem existir apenas para:

    diagnóstico
    manutenção
    recuperação emergencial
    rotina manual controlada
    migração pontual auditada

Eles não devem virar fluxo runtime nem sincronizador contínuo.

## Papel do Excel LISTA_RTD.xlsm

O Excel LISTA_RTD.xlsm deve permanecer aberto junto com o sistema durante o uso operacional.

Ele atua como antena RTD viva:

    programa da corretora mantém a conexão RTD
    Excel recebe os dados em tempo quase real
    Excel mantém uma tabela viva de símbolos monitorados
    coletor Python observa o Excel
    coletor normaliza os dados
    coletor atualiza snapshot em app.db
    UI e pricing leem app.db

## O que deixa de ser fluxo principal

O sistema não deve depender de subprocesso para consultar uma opção individual sob demanda.

O botão de preenchimento por RTD deve ler o último estado conhecido no snapshot, e não abrir Excel, salvar CSV ou chamar script externo para cada símbolo.

Subprocessos ficam restritos a manutenção, importação, recuperação emergencial e diagnóstico.

## Arquitetura alvo

    Corretora
        fornece conexão RTD

    Excel LISTA_RTD.xlsm
        fica aberto
        recebe dados RTD vivos
        mantém tabela viva de símbolos monitorados

    Coletor Python online
        detecta Excel aberto
        verifica planilha correta
        verifica aba RTD disponível
        lê dados em bloco
        normaliza campos
        valida símbolos
        atualiza snapshot em app.db
        grava histórico relevante
        informa status para UI

    dados/app.db
        mantém estado atual por símbolo
        serve UI, pricing, legs e estruturas

    dados/derived.db
        mantém somente derivados, caches, payoff, simulações e artefatos regeneráveis

    UI
        lê snapshot atual
        mostra status RTD
        atualiza painéis e estruturas com limite de redesenho

## Snapshot atual

Snapshot atual representa o último estado conhecido de cada ativo ou opção.

Características:

    uma linha por símbolo
    atualização por sobrescrita
    crescimento limitado
    leitura rápida
    fonte principal para UI e pricing

Uso:

    preencher legs
    atualizar painel
    calcular estruturas
    mostrar preço atual
    mostrar VWAP atual
    mostrar bid, ask, spread, volume e gregas

## Histórico intraday

Histórico intraday representa pontos gravados ao longo do tempo.

Regras:

    gravar apenas mudanças relevantes
    limitar frequência de gravação
    evitar milhares de linhas idênticas
    separar ticks brutos de candles consolidados
    manter política de retenção

Política sugerida:

    ticks brutos
        manter poucos dias

    candles de 1 minuto
        manter 60 ou 90 dias

    candles de 5 minutos
        manter 1 ano

    candles diários
        manter indefinidamente

## Candles

Candles devem ser gerados pelo sistema a partir dos pontos capturados.

Para cada intervalo:

    abertura: primeiro preço
    máxima: maior preço
    mínima: menor preço
    fechamento: último preço
    volume: diferença de volume ou volume consolidado
    VWAP: último VWAP ou VWAP médio do período
    bid: último ou médio
    ask: último ou médio
    spread: médio ou último
    quantidade de atualizações: total de pontos no intervalo

O candle não vem pronto do BTG. O sistema cria os candles a partir dos snapshots recebidos.

## VWAP

Se o BTG fornece VWAP atualizado ao longo do tempo, o sistema deve capturar esse valor com timestamp.

Assim o VWAP vira uma série temporal própria.

Uso do VWAP:

    preço acima ou abaixo do VWAP
    inclinação do VWAP
    distância percentual
    cruzamento de preço com VWAP
    confirmação por volume

Se só houver VWAP e nenhum preço de referência, não existe candle real. Nesse caso, existe apenas uma linha de VWAP.

## Fonte de preço para candle

Para ativo líquido:

    usar último negócio

Para opção pouco líquida:

    usar mid price entre bid e ask

Para decisão de compra:

    olhar ask e VWAP

Para decisão de venda:

    olhar bid e VWAP

Para gráfico operacional:

    permitir escolher a fonte
    diferenciar candle real de candle sintético
    exibir spread junto

## Frequências recomendadas

    snapshot atual
        atualizar sempre que detectar mudança

    histórico bruto
        gravar no máximo uma vez por segundo por símbolo, salvo mudança relevante

    candles
        consolidar por minuto

    UI
        atualizar algumas vezes por segundo, não a cada célula alterada

## Símbolos monitorados

Não monitorar o mercado inteiro sem necessidade.

Monitorar:

    ativos base principais
    opções das estruturas abertas
    opções favoritas
    lista operacional do dia
    símbolos adicionados pela UI

## Status operacional obrigatório

A UI deve mostrar ou disponibilizar no menu Ajuda um resumo com:

    RTD online
    Excel aberto
    planilha correta aberta
    aba RTD disponível
    corretora conectada
    última atualização
    quantidade de símbolos ativos
    símbolos com erro
    atraso dos dados

## Riscos

Excel pode virar gargalo.

Cuidados:

    não exagerar no número de símbolos
    evitar fórmulas pesadas
    evitar macros descontroladas
    ler em bloco
    prever reconexão

SQLite pode travar se escrever demais.

Cuidados:

    sobrescrever snapshot
    gravar histórico com redução inteligente
    evitar commit por célula
    usar fila de gravação
    consolidar candles
    usar modo adequado para escrita concorrente

UI pode ficar pesada.

Cuidados:

    separar coleta de renderização
    limitar redesenho
    atualizar apenas símbolos visíveis
    atualizar apenas estruturas abertas

Candle de opção pode ser ruidoso.

Cuidados:

    usar mid price quando não houver negócio
    marcar no gráfico qual fonte está sendo usada
    diferenciar candle real de candle sintético
    exibir spread junto
    não tomar decisão apenas pelo candle se o book estiver ruim

## Fluxo operacional sugerido

Antes de abrir o sistema:

    abrir o programa da corretora
    confirmar conexão
    abrir LISTA_RTD.xlsm
    confirmar que os dados estão atualizando

Ao abrir o sistema:

    verificar se o Excel está aberto
    verificar se a planilha correta está aberta
    verificar se a aba RTD está disponível
    verificar se os campos obrigatórios existem
    iniciar coletor online
    carregar snapshot atual
    começar atualização da UI

Durante o pregão:

    RTD atualiza Excel
    coletor lê mudanças
    snapshot é atualizado em app.db
    histórico recebe pontos relevantes
    motor de candles consolida intervalos
    UI atualiza painéis e gráficos
    estruturas são recalculadas

Ao encerrar o sistema:

    consolidar candles finais
    salvar estado do dia
    limpar ticks brutos antigos, se aplicável
    manter snapshots finais
    manter histórico consolidado

## Fases oficiais

### Fase 1: Transformar RTD em fonte online

    manter LISTA_RTD.xlsm aberto
    detectar Excel aberto
    ler tabela viva
    atualizar snapshot em app.db
    exibir status RTD na UI
    eliminar subprocesso para preencher leg

Objetivo:

    ter o sistema lendo dados vivos do Excel

### Fase 2: Snapshot centralizado

    criar estado atual por símbolo
    atualizar por sobrescrita
    normalizar campos em camada única
    fazer legs e estruturas lerem snapshot
    botão Preencher por RTD usa snapshot

Objetivo:

    deixar o sistema mais rápido e mais simples

### Fase 3: Histórico intraday

    armazenar pontos temporais relevantes
    gravar timestamp, símbolo, preço, VWAP, bid, ask e volume
    controlar frequência
    evitar crescimento exagerado

Objetivo:

    começar a formar a base dos gráficos

### Fase 4: Motor de candles

    gerar candles de 1 minuto
    depois gerar candles de 5 e 15 minutos
    associar VWAP ao candle
    exibir candles em gráfico

Objetivo:

    fazer o gráfico funcionar sem depender de gráfico pronto do BTG

### Fase 5: UI operacional em tempo real

    atualizar painel de opções
    atualizar legs
    atualizar estruturas
    atualizar gráfico
    mostrar VWAP, preço, spread e decisão
    mostrar status de atualização

Objetivo:

    transformar a tela em terminal operacional vivo

### Fase 6: Retenção, limpeza e consolidação

    consolidar candles no fim do dia
    limpar ticks brutos antigos
    manter candles históricos
    criar rotina de manutenção
    compactar banco se necessário

Objetivo:

    evitar crescimento infinito e manter performance

### Fase 7: Alertas e decisão operacional

    criar regras de decisão com VWAP
    alertar cruzamento de preço com VWAP
    alertar spread anormal
    alertar liquidez baixa
    alertar estrutura favorável
    alertar mudança relevante no payoff

Objetivo:

    usar os dados vivos para tomada de decisão, não apenas visualização

## Regras explícitas de desenvolvimento

    não migrar para web
    não utilizar emojis
    manter escopo do projeto
    efetuar buscas de dados e arquivos antes de alterações
    testar toda mudança concluída
    após encerramento de fase, o teste deve compor todas as fases encerradas
    evitar códigos intermediários em explicações
    gerar alterações automatizadas via Git Bash
    a cada alteração concluída e testada, commitar
    não codar sem rumo
    buscar evolução no Git quando necessário
    manter arquivo de auditoria atualizado
    não gerar código com crase em documentação operacional
    não manter sync contínuo derived.db -> app.db
    não manter sync contínuo app.db -> derived.db
    não permitir dívida técnica para cotação viva

## Resumo da decisão

A arquitetura final recomendada é:

    Excel aberto o tempo todo como receptor RTD
    sistema Python com coletor online interno
    snapshot em app.db para estado atual
    histórico intraday separado
    candles gerados pelo próprio sistema
    VWAP tratado como série temporal capturada
    UI atualizada por eventos e com limite de redesenho
    nada de subprocesso para consultar opção individual
    subprocessos apenas para manutenção, importação ou recuperação emergencial

Com isso, o sistema ganha:

    velocidade
    menos complexidade operacional
    menos subprocessos
    menos espera
    UI online
    estruturas online
    gráficos possíveis
    histórico útil
    base para replay e alertas
    melhor uso real do VWAP
