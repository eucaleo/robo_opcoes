# Auditoria RTD Excel Vivo

Atualizado em: 2026-06-30 18:50:17

## Objetivo

Acompanhar a implementação da arquitetura RTD sempre online com Excel aberto, app.db como fonte oficial de mercado vivo e derived.db restrito a resultados derivados e artefatos regeneráveis.

## Escopo

Baseado nos documentos:

    docs/PLANO_RTD_EXCEL_VIVO.md
    PLANO_RTD_EXCEL_VIVO.pdf

## Decisão arquitetural auditada

A fonte oficial de mercado vivo é:

    dados/app.db

O banco de derivados é:

    dados/derived.db

Tabelas de mercado vivo:

    rtd_option_quotes -> dados/app.db
    rtd_underlying_quotes -> dados/app.db

As mesmas tabelas não devem ser usadas como fonte ativa em:

    dados/derived.db

Regra crítica:

    não manter sync contínuo derived.db -> app.db
    não manter sync contínuo app.db -> derived.db

Conclusão arquitetural:

    app.db é o único banco canônico para mercado vivo
    derived.db fica para derivados, caches, payoff, simulações e artefatos regeneráveis
    LISTA_RTD.xlsm permanece aberto como antena RTD viva
    coletor Python observa o Excel e atualiza app.db
    UI e pricing runtime consomem app.db

## Regras operacionais principais

    não migrar para web
    não utilizar emojis
    manter o escopo do projeto
    efetuar buscas de dados e arquivos antes de alterações
    toda mudança deve ser testada após concluída
    após encerramento de fase, o teste deve compor todas as fases encerradas
    evitar códigos intermediários em explicações
    em alterações, gerar código automatizado via Git Bash
    a cada alteração concluída e testada, commitar
    não codar sem rumo
    se necessário, buscar a evolução no Git
    atualizar este arquivo com testes, conclusões e evolução
    não alterar lógica funcional sem auditoria prévia
    não gerar código com crase em documentação operacional
    não permitir dívida técnica para cotação viva

## Retificação da Fase 0

A auditoria inicial registrava que o cache principal de opções era:

    dados/derived.db:rtd_option_quotes

Essa informação fica retificada pela decisão arquitetural do PDF.

A partir desta revisão, o entendimento oficial é:

    dados/app.db:rtd_option_quotes é a fonte operacional de opções RTD
    dados/app.db:rtd_underlying_quotes é a fonte operacional de underlyings RTD
    dados/derived.db não deve ser fonte ativa de cotação viva

Qualquer ocorrência histórica tratando derived.db como fonte ativa de RTD deve ser interpretada como estado anterior, diagnóstico intermediário ou decisão superada.

## Fases

### Fase 0: Documentação e verificação operacional

Status:

    Concluída documentalmente, com retificação arquitetural aplicada.

Achados consolidados:

    projeto possui documentação RTD e auditoria inicial
    LISTA_RTD.xlsm deve existir na raiz e permanecer aberto durante a operação
    fluxo antigo sob demanda via subprocess, PowerShell, Excel COM, CSV e import SQLite deixa de ser fluxo principal
    fonte oficial de mercado vivo passa a ser dados/app.db
    rtd_option_quotes pertence operacionalmente a dados/app.db
    rtd_underlying_quotes pertence operacionalmente a dados/app.db
    dados/derived.db fica restrito a derivados, caches, payoff, simulações e artefatos regeneráveis
    Terminal VWAP Payoff não deve acessar Excel diretamente
    UI e pricing devem ler estado vivo em app.db
    subprocessos podem permanecer apenas para manutenção, diagnóstico, importação emergencial ou recuperação operacional
    não deve existir sync contínuo entre app.db e derived.db

Pendências da Fase 0:

    confirmar manualmente Excel aberto
    confirmar corretora conectada
    confirmar LISTA_RTD.xlsm aberto
    confirmar aba RTD disponível
    confirmar campos RTD obrigatórios
    confirmar existência operacional de rtd_option_quotes em app.db
    confirmar existência operacional de rtd_underlying_quotes em app.db
    mapear pontos do projeto que ainda apontam RTD vivo para derived.db
    mapear scripts que ainda fazem reconciliação entre app.db e derived.db
    classificar scripts de reconciliação como manutenção, diagnóstico ou recuperação emergencial

Resultado:

    documentação corrigida conforme PDF
    decisão de banco canônico registrada
    regra contra sync contínuo registrada
    nenhuma alteração funcional realizada

Teste documental:

    verificar presença de dados/app.db
    verificar presença de dados/derived.db
    verificar presença de rtd_option_quotes -> dados/app.db
    verificar presença de rtd_underlying_quotes -> dados/app.db
    verificar regra contra sync contínuo
    verificar que derived.db não aparece como fonte ativa de cotação viva

Commit:

    Pendente.

### Fase 1: Transformar RTD em fonte online

Status:

    Não iniciada.

Objetivo:

    manter LISTA_RTD.xlsm aberto
    detectar Excel aberto
    ler tabela viva
    atualizar snapshot em app.db
    exibir status RTD na UI
    eliminar subprocesso para preencher leg

Critério de conclusão:

    sistema lê dados vivos do Excel
    snapshot é atualizado em app.db
    UI consegue consultar status RTD
    preenchimento de leg usa snapshot, não subprocesso por símbolo

### Fase 2: Snapshot centralizado

Status:

    Não iniciada.

Objetivo:

    criar estado atual por símbolo
    atualizar por sobrescrita
    normalizar campos em camada única
    fazer legs e estruturas lerem snapshot
    botão Preencher por RTD usa snapshot

Critério de conclusão:

    app.db possui snapshot atual por símbolo
    leitura de UI e pricing usa snapshot
    derived.db não é usado como fonte ativa de RTD

### Fase 3: Histórico intraday

Status:

    Não iniciada.

Objetivo:

    armazenar pontos temporais relevantes
    gravar timestamp, símbolo, preço, VWAP, bid, ask e volume
    controlar frequência
    evitar crescimento exagerado

Critério de conclusão:

    pontos intraday são gravados com controle de frequência
    histórico não cresce sem limite
    snapshot e histórico ficam conceitualmente separados

### Fase 4: Motor de candles

Status:

    Não iniciada.

Objetivo:

    gerar candles de 1 minuto
    depois gerar candles de 5 e 15 minutos
    associar VWAP ao candle
    exibir candles em gráfico

Critério de conclusão:

    candles são gerados pelo sistema a partir dos snapshots ou pontos intraday
    gráfico não depende de gráfico pronto do BTG

### Fase 5: UI operacional em tempo real

Status:

    Não iniciada.

Objetivo:

    atualizar painel de opções
    atualizar legs
    atualizar estruturas
    atualizar gráfico
    mostrar VWAP, preço, spread e decisão
    mostrar status de atualização

Critério de conclusão:

    UI se comporta como terminal operacional vivo
    atualizações visuais têm limite de redesenho
    menu Ajuda disponibiliza resumo de conexão RTD

### Fase 6: Retenção, limpeza e consolidação

Status:

    Não iniciada.

Objetivo:

    consolidar candles no fim do dia
    limpar ticks brutos antigos
    manter candles históricos
    criar rotina de manutenção
    compactar banco se necessário

Critério de conclusão:

    política de retenção aplicada
    banco não cresce indefinidamente
    candles históricos permanecem utilizáveis

### Fase 7: Alertas e decisão operacional

Status:

    Não iniciada.

Objetivo:

    criar regras de decisão com VWAP
    alertar cruzamento de preço com VWAP
    alertar spread anormal
    alertar liquidez baixa
    alertar estrutura favorável
    alertar mudança relevante no payoff

Critério de conclusão:

    dados vivos alimentam alertas e decisão operacional
    alertas usam snapshot e histórico conforme necessidade

## Registro Fase 0 - correção conforme PDF

### Ação

Correção documental para alinhar a auditoria com o PDF de arquitetura RTD Excel Vivo.

### Arquivos verificados

    docs/PLANO_RTD_EXCEL_VIVO.md
    docs/AUDITORIA_RTD_EXCEL_VIVO.md
    PLANO_RTD_EXCEL_VIVO.pdf

### Resultado

    auditoria corrigida
    plano corrigido
    decisão app.db como fonte oficial registrada
    regra contra sync contínuo registrada
    derived.db removido como fonte ativa de cotação viva
    nenhuma alteração funcional realizada

### Pendências

    validar operacionalmente Excel aberto
    validar corretora conectada
    validar LISTA_RTD.xlsm aberto
    validar campos RTD
    mapear código que ainda use derived.db para RTD vivo
    mapear scripts de reconciliação e classificá-los como não runtime

### Teste

    validação documental por termos obrigatórios
    validação de ausência de frase antiga indicando derived.db como cache principal ativo
    validação de presença da decisão rtd_option_quotes -> app.db
    validação de presença da decisão rtd_underlying_quotes -> app.db

### Commit

    Pendente.

## Registro operacional - Fase 0 concluída em 2026-06-30

Status:

    Fase 0 concluída documental e operacionalmente, com pendências localizadas para saneamento controlado.

Evidências produzidas:

    docs/levantamentos/rtd_fase0_resumo_20260630_215822.txt
    docs/levantamentos/rtd_fase0_mapa_bancos_20260630_215847.txt
    docs/levantamentos/rtd_fase0_mapa_excel_subprocess_20260630_215903.txt
    docs/levantamentos/rtd_fase0_arquivos_candidatos_20260630_215918.txt
    docs/levantamentos/rtd_fase0_sqlite_tabelas_20260630_215939.txt
    docs/levantamentos/rtd_fase0_conclusao_20260630_220155.md
    docs/levantamentos/rtd_fase1_alvos_iniciais_20260630_220530.md

Confirmações operacionais:

    dados/app.db existe
    dados/derived.db existe
    dados/app.db.rtd_option_quotes existe
    dados/app.db.rtd_underlying_quotes existe
    dados/app.db.rtd_option_quotes possui registros
    dados/app.db.rtd_underlying_quotes possui registros

Contagens observadas na auditoria SQLite:

    dados/app.db.rtd_option_quotes: 11 registros
    dados/app.db.rtd_underlying_quotes: 2 registros
    dados/derived.db.rtd_option_quotes: 11 registros
    dados/derived.db.rtd_underlying_quotes: 2 registros

Decisão arquitetural reafirmada:

    dados/app.db é a fonte operacional de mercado vivo RTD.
    dados/derived.db não é fonte ativa de cotação viva.
    dados/derived.db pode conter tabelas RTD legadas apenas como resíduo, diagnóstico, manutenção, recuperação ou evidência histórica.
    Não deve existir sincronização contínua app.db -> derived.db ou derived.db -> app.db no runtime.

Pendências localizadas:

    scripts/rtd_reconciliar_app_para_derived.py
        classificar explicitamente como manutenção, diagnóstico ou recuperação emergencial.
        não pertence ao fluxo runtime.

    UI/components/structure_editor_dialog.py
        ainda contém atualização RTD sob demanda via subprocess.
        alvo funcional inicial da Fase 1.
        deve ser alterado para preencher leg a partir do snapshot/cache operacional em dados/app.db.

    scripts/import_rtd_option_quotes_wide_csv.py
    scripts/refresh_rtd_option_quotes_excel.ps1
        manter apenas como importação, manutenção ou recuperação operacional.
        não devem ser fluxo principal de preenchimento de leg.

Alvo inicial recomendado para Fase 1:

    UI/components/structure_editor_dialog.py

Objetivo da Fase 1:

    Eliminar subprocesso por símbolo no preenchimento RTD da leg.
    Ler a última cotação disponível em dados/app.db.rtd_option_quotes.
    Usar o repositório operacional/snapshot já apontado para app.db.
    Manter Excel LISTA_RTD.xlsm como antena viva, não como chamada sob demanda por botão.
