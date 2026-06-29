# Projeto UI Terminal VWAP Payoff

## 1. Objetivo

Implementar uma nova camada visual local para análise de estruturas de opções, combinando:

- seleção por structure_id;
- resumo da estrutura;
- payoff analítico;
- VWAP do ativo-base;
- preço atual do ativo-base;
- status RTD;
- snapshot atual de mercado;
- snapshot de implantação;
- tabela analítica por perna;
- atualização controlada.

O layout visual discutido será usado como referência inicial, mas não define a arquitetura do sistema.

A regra principal deste projeto é:

O layout deve ser adaptado ao sistema atual, e não o sistema atual ao layout.

O sistema já possui regras, banco, RTD, payoff, ViewModels, testes e documentação. O novo terminal entra como camada visual local, consumindo serviços existentes e preservando o funcionamento atual.

## 2. Regras permanentes do projeto

Estas regras se aplicam a todos os projetos, fases e alterações.

### 2.1 Regras gerais

A. Não migrar para web.

B. Não utilizar emojis.

C. Manter-se ao escopo do projeto sem derivações.

D. Efetuar buscas de dados e arquivos antes de alterações.

E. Toda mudança deve ser testada após concluída.

F. Após o encerramento de cada fase, o teste deve compor todas as fases encerradas, evitando pendências acumuladas.

G. Evitar códigos intermediários em explicações. Ir direto ao ponto.

H. Em alterações, sempre gerar o código inteiro do arquivo quando houver necessidade de alteração de código.

I. A cada alteração concluída e testada, efetuar commit.

J. Não codar sem rumo. Se necessário, buscar a evolução no Git antes de alterar.

K. Criar e manter arquivo de auditoria atualizado com testes, conclusões, pendências e evolução.

L. Não gerar código intermediário desnecessário.

M. Excel é apenas ponte RTD.

N. Banco de dados é a fonte da verdade.

O. UI não deve depender de CSVs derivados antigos.

P. Cálculos devem ser efetuados pelo sistema.

Q. Novas estruturas devem nascer no sistema.

### 2.2 Regra central de integração

O novo terminal não substitui o sistema atual.

O terminal deve consumir dados do sistema atual por meio de ViewModels, controllers ou serviços, mantendo structure_id como referência central.

Fluxo permitido:

    Banco de dados
    Serviços existentes
    ViewModel analítico
    Controller do terminal
    Terminal VWAP Payoff

Fluxo não permitido:

    Terminal novo
    Cálculo financeiro paralelo
    Acesso direto a banco
    Acesso direto a CSV antigo
    Resultado divergente do sistema

## 3. Fonte dos dados

### 3.1 Excel RTD

O arquivo LISTA_RTD.xlsm será utilizado apenas como ponte para o RTD do BTG.

O Excel não é fonte da verdade de:

- estrutura;
- posição;
- pernas;
- preço de entrada;
- cálculo financeiro;
- payoff;
- PL;
- metadados da operação.

### 3.2 Banco de dados

O banco de dados é a fonte da verdade para:

- estruturas;
- pernas;
- preço de entrada;
- quantidade;
- ativo-base;
- vencimento;
- metadados da estrutura;
- snapshots persistidos;
- histórico necessário do sistema.

### 3.3 Sistema

O sistema é responsável por:

- cálculo de payoff;
- cálculo de PL atual;
- cálculo por perna;
- normalização de dados;
- validação de structure_id;
- montagem do ViewModel;
- separação entre PL atual e payoff no vencimento;
- controle de persistência;
- tratamento de ausência de dados.

## 4. RTD confirmado documentalmente

O documento LISTA RTD FUNCOES.pdf confirma o campo VWAP:

    =RTD("btg_pro_rtd";"";"QUOTE.VWAP";"BPAC11")

A primeira versão não deve calcular VWAP por conta própria.

O objetivo técnico é ler, normalizar, tratar falhas, registrar fonte e exibir a VWAP recebida do RTD.

## 5. Campos RTD relevantes

### 5.1 Ativo-base

Campos relevantes confirmados no documento RTD:

    QUOTE.BID_PRICE
    QUOTE.ASK_PRICE
    QUOTE.LAST_TRADE_PRICE
    QUOTE.LAST_TRADE_QUANTITY
    QUOTE.BID_QUANTITY
    QUOTE.ASK_QUANTITY
    QUOTE.OPEN
    QUOTE.HIGH
    QUOTE.LOW
    QUOTE.CLOSE
    QUOTE.PREV_CLOSE
    QUOTE.CHANGE
    QUOTE.CHANGE_PERCENT
    QUOTE.NUM_TRADES
    QUOTE.QUANTITY
    QUOTE.VOLUME
    QUOTE.VWAP
    QUOTE.STATUS
    QUOTE.SOURCE
    QUOTE.SYMBOL
    QUOTE.DESCRIPTION
    QUOTE.SECURITY_TYPE

### 5.2 Opções e pernas

Campos relevantes para opções e pernas:

    QUOTE.UNDERLYING_SYMBOL
    QUOTE.UNDERLYING_PRICE
    QUOTE.MATURITYDATE
    QUOTE.OPTION_TYPE
    QUOTE.OPTION_STYLE
    QUOTE.STRIKE_PRICE
    QUOTE.IMPLIED_VOLATILITY
    QUOTE.VOLATILITY
    QUOTE.DELTA
    QUOTE.GAMMA
    QUOTE.THETA
    QUOTE.VEGA
    QUOTE.RHO
    QUOTE.OPTION_PRICE
    QUOTE.INTRINSIC_VALUE
    QUOTE.EXTRINSIC_VALUE
    QUOTE.PREMIUM_PCT
    QUOTE.MONEYNESS_PCT
    QUOTE.STATUS

### 5.3 Indicadores complementares

Campos complementares disponíveis no RTD:

    QUOTE.HISTORICAL_VOLATILITY
    QUOTE.EMA5
    QUOTE.EMA20
    QUOTE.EMA200
    QUOTE.EMA12
    QUOTE.EMA26
    QUOTE.MACD
    QUOTE.MACD_SIGNAL
    QUOTE.MACD_HISTOGRAM
    QUOTE.RSI
    QUOTE.STOCH
    QUOTE.STOCH_SIGNAL
    QUOTE.ATR
    QUOTE.OBV

Esses campos não fazem parte obrigatória da primeira versão.

## 6. Escopo da primeira versão

A primeira versão do terminal deve contemplar:

- listagem de estruturas reais;
- seleção por structure_id;
- cards de resumo;
- preço atual do ativo-base;
- VWAP do ativo-base;
- status RTD;
- gráfico de payoff vindo do sistema;
- tabela analítica por perna;
- refresh manual;
- tratamento de ausência de RTD;
- auditoria da evolução.

Não entram na primeira versão:

- criação de estruturas;
- edição de estruturas;
- envio de ordens;
- automação operacional;
- migração web;
- dependência de CSVs antigos;
- novo motor de cálculo financeiro;
- reescrita do sistema atual;
- cálculo oficial de payoff dentro da UI.

## 7. Arquitetura recomendada

A arquitetura recomendada é:

    UI Terminal VWAP Payoff
    TerminalVwapPayoffController
    TerminalVwapPayoffViewModelBuilder
    Serviços existentes do sistema
    Structure Repository
    Payoff Analítico
    Market Snapshot Provider
    RTD Provider
    VWAP Provider
    Banco de dados
    Excel como ponte RTD

### 7.1 Responsabilidades da UI

A UI pode:

- renderizar dados;
- listar estruturas recebidas do controller;
- selecionar structure_id;
- acionar refresh;
- exibir mensagens de erro controladas;
- exibir horário da última atualização.

A UI não pode:

- calcular payoff oficial;
- acessar banco diretamente;
- acessar CSV antigo;
- acessar RTD bruto diretamente;
- criar estrutura;
- editar estrutura;
- alterar regra financeira;
- misturar pernas entre estruturas.

## 8. ViewModel esperado

O terminal deve receber um ViewModel pronto.

Campos mínimos:

    structure_id
    nome_estrutura
    ativo_base
    preco_atual
    vwap
    diferenca_preco_vwap_percentual
    variacao_percentual
    volume
    status_rtd
    fonte_rtd
    horario_cotacao
    payoff_curve_x
    payoff_curve_y
    preco_base_atual
    payoff_no_preco_atual
    pl_atual
    snapshot_implantacao
    snapshot_atual
    pernas
    mensagens

A diferença entre preço atual e VWAP, quando ambos existirem, deve ser calculada pelo sistema e apenas exibida pela UI.

Fórmula de referência:

$$
\text{Diferença \%} = \frac{\text{Preço Atual} - \text{VWAP}}{\text{VWAP}} \times 100
$$

## 9. Fases do projeto

### Fase 0 — Preparação, busca e proteção contra regressão

Objetivo:

Garantir que o sistema atual esteja íntegro antes de qualquer alteração.

Ações:

- verificar branch correta;
- verificar status do Git;
- verificar histórico recente;
- buscar arquivos existentes relacionados a estrutura, payoff, snapshot, RTD, ViewModel, UI e CSV;
- executar testes atuais;
- registrar estado inicial na auditoria.

Critério de conclusão:

- branch correta selecionada;
- arquivos relevantes identificados;
- testes atuais executados;
- auditoria inicial criada;
- nenhuma alteração funcional realizada.

Commit esperado:

    docs: inicia plano e auditoria do terminal vwap payoff

### Fase 1 — Documentação base e auditoria

Objetivo:

Criar documentação inicial para manter o projeto no trilho.

Ações:

- criar docs/ui_terminal_vwap_payoff_plano.md;
- criar docs/auditoria_ui_terminal_vwap_payoff.md;
- registrar regras permanentes;
- registrar fases;
- registrar fonte RTD confirmada;
- registrar riscos;
- registrar critérios de aceite.

Critério de conclusão:

- documentos criados;
- conteúdo revisado;
- commit realizado.

Commit esperado:

    docs: adiciona plano e auditoria do terminal vwap payoff

### Fase 2 — Spike visual isolado

Objetivo:

Criar protótipos executáveis sem dados reais, apenas para avaliar usabilidade.

Ações:

- criar modelo com lateral operacional;
- criar modelo dashboard executivo;
- criar modelo foco com abas;
- usar apenas dados mockados;
- não importar módulos reais do sistema;
- não acessar banco;
- não acessar RTD;
- não acessar CSV.

Critério de conclusão:

- pelo menos dois modelos executáveis avaliados;
- layout base escolhido;
- decisão registrada na auditoria.

Commit esperado:

    spike: adiciona mockups do terminal vwap payoff

### Fase 3 — Escolha do layout base

Objetivo:

Escolher o modelo visual antes da integração real.

Modelos avaliados:

- Modelo A: lateral operacional;
- Modelo B: dashboard executivo;
- Modelo C: modo foco com abas.

Recomendação inicial:

    Base visual: Modelo A
    Evolução interna: Modelo C

Layout recomendado:

    Barra lateral com estruturas
    Header da estrutura ativa
    Cards de preço, VWAP, PL e payoff
    Abas de Resumo, Payoff, VWAP, Pernas e Snapshots
    Tabela analítica inferior ou em aba própria

Critério de conclusão:

- layout aprovado;
- limitações registradas;
- próximos ajustes definidos.

Commit esperado:

    docs: registra decisao visual do terminal vwap payoff

### Fase 4 — Contrato do ViewModel

Objetivo:

Definir exatamente o que a UI nova precisa receber.

Ações:

- localizar ViewModels existentes;
- localizar serviços de payoff;
- localizar serviços de snapshot;
- definir TerminalVwapPayoffViewModel;
- definir campos obrigatórios;
- definir campos opcionais;
- definir comportamento para ausência de RTD;
- criar testes do contrato quando aplicável.

Critério de conclusão:

- contrato definido;
- UI sem acesso direto a banco;
- UI sem acesso direto a RTD;
- fallback documentado.

Commit esperado:

    feat: define contrato do terminal vwap payoff

### Fase 5 — Integração com estruturas reais

Objetivo:

Listar e carregar estruturas reais por structure_id.

Ações:

- localizar repositório ou serviço atual de estruturas;
- criar controller do terminal;
- listar estruturas reais;
- carregar estrutura selecionada;
- validar que cada estrutura carrega apenas suas próprias pernas;
- impedir dependência de CSV antigo.

Critério de conclusão:

- estrutura real aparece na tela;
- seleção por structure_id funciona;
- pernas não se misturam;
- dados vêm do sistema.

Commit esperado:

    feat: integra terminal com estruturas reais

### Fase 6 — Prova isolada do RTD VWAP

Objetivo:

Provar leitura de QUOTE.VWAP via RTD.

Campo confirmado:

    =RTD("btg_pro_rtd";"";"QUOTE.VWAP";"BPAC11")

Ações:

- criar rotina isolada de leitura;
- testar com BPAC11;
- testar com ativo-base real de estrutura;
- comparar com Excel aberto;
- tratar valor vazio;
- tratar None;
- tratar erro de RTD;
- tratar Excel fechado;
- tratar RTD inicializando;
- normalizar separador decimal;
- registrar fonte e horário.

Critério de conclusão:

- VWAP lida quando disponível;
- falha de VWAP não derruba o sistema;
- resultado registrado na auditoria.

Commit esperado:

    feat: adiciona leitura de vwap via rtd

### Fase 7 — Integração da VWAP no snapshot atual

Objetivo:

Adicionar VWAP ao snapshot atual sem substituir preço atual.

Campos recomendados:

    structure_id
    ativo_base
    preco_atual
    bid
    ask
    vwap
    volume
    variacao_percentual
    status
    fonte_preco
    fonte_vwap
    capturado_em

Critério de conclusão:

- snapshot atual contém VWAP;
- preço atual e VWAP aparecem separados;
- ausência de RTD é tratada;
- banco permanece fonte da verdade.

Commit esperado:

    feat: inclui vwap no snapshot de mercado

### Fase 8 — Payoff real no novo terminal

Objetivo:

Exibir payoff calculado pelo sistema atual.

Ações:

- reaproveitar serviço ou ViewModel de payoff existente;
- impedir cálculo financeiro oficial na UI;
- plotar curva recebida do sistema;
- destacar preço atual;
- destacar VWAP;
- destacar payoff no preço atual;
- separar PL atual de payoff no vencimento.

Critério de conclusão:

- gráfico usa payoff real do sistema;
- resultado bate com serviço existente;
- testes de regressão passam.

Commit esperado:

    feat: exibe payoff real no terminal vwap

### Fase 9 — Tabela analítica por perna

Objetivo:

Exibir tabela real por perna com dados operacionais e financeiros.

Campos mínimos:

    numero_perna
    ticker
    tipo
    direcao
    quantidade
    strike
    vencimento
    premio_entrada
    preco_atual
    bid
    ask
    intrinseco
    extrinseco
    delta
    theta
    vega
    pl_atual
    payoff_no_vencimento_ao_preco_atual
    fonte
    status

Critério de conclusão:

- tabela exibe pernas reais;
- dados vêm do ViewModel;
- cálculos vêm do sistema;
- não há dependência de CSV antigo.

Commit esperado:

    feat: adiciona tabela analitica de pernas ao terminal

### Fase 10 — Refresh controlado

Objetivo:

Atualizar dados sem travar a interface.

Ações:

- iniciar com refresh manual;
- implementar refresh automático opcional;
- evitar loop bloqueante;
- impedir refresh concorrente;
- exibir último horário de atualização;
- manter tela funcional se RTD falhar.

Critério de conclusão:

- refresh manual funcional;
- refresh automático opcional;
- UI não trava;
- falhas são exibidas sem encerrar aplicação.

Commit esperado:

    feat: adiciona refresh controlado ao terminal

### Fase 11 — Testes integrados e auditoria final

Objetivo:

Validar todas as fases encerradas.

Testes mínimos:

- testes antigos continuam passando;
- estruturas reais são listadas;
- structure_id correto é carregado;
- pernas corretas são exibidas;
- VWAP é lida quando disponível;
- ausência de VWAP é tratada;
- payoff vem do sistema;
- UI não usa CSV antigo;
- UI não cria estrutura;
- UI não altera banco indevidamente;
- refresh não trava;
- auditoria documenta resultado.

Critério de conclusão:

- todos os testes da fase atual passam;
- todos os testes das fases anteriores passam;
- auditoria está atualizada;
- commit final realizado.

Commit esperado:

    test: valida terminal vwap payoff integrado

## 10. Critérios de aceite do projeto

O projeto será considerado aprovado quando:

- rodar localmente;
- não depender de web;
- listar estruturas reais;
- carregar por structure_id;
- exibir VWAP vinda do RTD;
- exibir preço atual separado da VWAP;
- exibir payoff vindo do sistema;
- exibir tabela de pernas real;
- não usar CSV derivado antigo;
- não recriar cálculo financeiro na UI;
- não quebrar testes existentes;
- registrar auditoria de evolução;
- preservar banco como fonte da verdade;
- preservar Excel apenas como ponte RTD.

## 11. Riscos principais e mitigação

### Risco 1 — UI calcular regra financeira

Mitigação:

A UI só consome ViewModels. Cálculos permanecem nos serviços do sistema.

### Risco 2 — Dependência indevida do Excel

Mitigação:

Excel é ponte RTD. O sistema deve tratar indisponibilidade do Excel e não assumir que Excel é fonte da verdade.

### Risco 3 — Regressão no payoff atual

Mitigação:

Antes de cada fase, rodar testes existentes. Após cada fase, rodar testes acumulados.

### Risco 4 — Mistura de pernas entre estruturas

Mitigação:

Toda carga deve ser feita por structure_id.

### Risco 5 — Layout forçar reestruturação do sistema

Mitigação:

O layout será adaptado ao sistema. Não haverá reescrita do sistema em função da tela.

### Risco 6 — CSV antigo voltar como dependência

Mitigação:

A UI não deve depender de CSVs derivados antigos. Qualquer dado necessário deve vir do banco, serviços ou RTD por meio do sistema.

## 12. Decisão final

O layout é aprovado como referência inicial, mas não como arquitetura.

A arquitetura permanece sendo a do sistema atual.

O terminal será uma nova camada visual local, preservando:

- RTD como ponte;
- banco como fonte da verdade;
- sistema como responsável pelos cálculos;
- UI como camada de apresentação;
- structure_id como chave de análise;
- auditoria como trilha de evolução.

## Premissas de proteção contra regressão RTD

Esta fase adota como premissa que o arquivo LISTA_RTD.xlsx é legado e não deve ser restaurado.

O arquivo operacional vigente para a ponte RTD é LISTA_RTD.xlsm, com uso de macros.

A substituição de LISTA_RTD.xlsx por LISTA_RTD.xlsm é evolução consolidada do sistema e não deve ser revertida.

Qualquer tentativa de restaurar LISTA_RTD.xlsx deve ser tratada como regressão.

Antes de qualquer restauração, remoção, substituição ou alteração estrutural de arquivo, devem ser feitas verificações locais do estado atual do projeto.

As verificações devem observar o estado presente da branch e os registros de supersessão já existentes, evitando buscas profundas no histórico que tragam de volta problemas já resolvidos.

Fluxo obrigatório antes de modificar arquivos sensíveis:

    Verificar branch atual
    Verificar status do working tree
    Verificar arquivos deletados e não rastreados
    Verificar referências atuais no projeto
    Confirmar premissas vigentes
    Somente depois alterar documentos ou código

Arquivos sensíveis nesta fase:

    LISTA_RTD.xlsx
    LISTA_RTD.xlsm
    OPERACOES_E_OPCOES.xlsm

Regras de proteção:

    Não restaurar LISTA_RTD.xlsx
    Não executar git reset --hard
    Não executar git clean -fd
    Não executar git add -A
    Não misturar documentação com alterações de Excel
    Não misturar documentação com reports, spikes ou scripts locais

## Registro de evolução — Incremento 2 do Terminal VWAP Payoff

Marcador: PLANO_INCREMENTO_2_TERMINAL_VWAP_PAYOFF_594057f

Data de registro:

    2026-06-29 09:47:54 -0300

Commit funcional registrado:

    594057f feat(ui): adiciona app service do terminal vwap payoff

Escopo registrado:

    Inclusão do app service do Terminal VWAP Payoff.
    Inclusão dos testes correspondentes.
    Preservação da separação entre UI, serviços e fonte da verdade.

Arquivos funcionais do incremento:

    ATT/tests/test_terminal_vwap_payoff_app_service.py
    services/terminal_vwap_payoff_app_service.py

Validação:

    Testes acumulados do terminal executados com sucesso.
    Resultado observado: ============================== 7 passed in 0.17s ==============================

Regras preservadas:

    Não migrar para web.
    Não usar CSV derivado antigo como dependência da UI.
    Não restaurar LISTA_RTD.xlsx.
    Não incluir arquivos Excel em commit funcional ou documental.
    Não usar git add -A.
    Banco permanece como fonte da verdade.
    Excel permanece apenas como ponte RTD.

## Registro de alinhamento arquitetural — escopo local do controller

Data de registro:

    2026-06-29 10:57:22 -0300

Decisão de arquitetura reforçada:

    O Terminal VWAP Payoff permanece como camada visual local.
    O controller do terminal, quando existente, deve atuar apenas como orquestrador local entre UI, ViewModels e serviços.
    Não faz parte do escopo atual criar endpoint REST/API, router FastAPI ou integração web para o terminal.

Permitido:

    UI local.
    Controller local.
    ViewModel do terminal.
    App service do terminal.
    Serviços existentes do sistema.
    Testes locais do terminal.
    Integração por structure_id.
    Consumo de dados calculados pelo sistema.

Não permitido nesta etapa:

    FastAPI específico para o terminal.
    APIRouter específico para o terminal.
    Inclusão de router do terminal em main.py.
    Endpoint REST para o terminal.
    TestClient para endpoint do terminal.
    Cálculo financeiro oficial dentro da UI.
    Acesso direto da UI ao banco.
    Acesso direto da UI a CSV antigo.
    Restauração de LISTA_RTD.xlsx.

Critério de continuidade:

    Antes de novos incrementos, confirmar que main.py permanece sem router do terminal e que api/terminal_vwap_payoff_controller.py permanece ausente.
    Após cada incremento, executar os testes acumulados do terminal.
