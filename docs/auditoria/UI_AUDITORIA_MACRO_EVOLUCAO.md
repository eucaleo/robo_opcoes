# Auditoria macro de evolucao UI moderna e Terminal VWAP

Data de consolidacao: 2026-07-07 15:37:09

Branch auditada: audit/ui-modern-terminal-vwap

HEAD atual: bd08ff7

## 1. Objetivo

Este documento registra a mudanca controlada de estrategia da auditoria UI.

A frente deixa de evoluir por microcorrecoes isoladas e passa a evoluir por blocos operacionais maiores, mantendo separacao de escopo, rastreabilidade, testes e commits pequenos por intencao.

A decisao nao autoriza alteracao de banco, schema, pipeline, regra de negocio, services, repositories ou controllers.

A decisao nao declara equivalencia global da UI moderna dark.

## 2. Contexto de rota

A auditoria documental anterior consolidou que:

- a UI atual permanece como caminho principal;
- a UI moderna dark permanece como caminho paralelo e incremental;
- Terminal VWAP deve ser tratado em frente propria;
- payoff, UIDataModel, banco e pipeline devem permanecer fora desta frente;
- a matriz global de equivalencia UI ainda precisa ser preenchida antes de qualquer substituicao ampla.

A branch atual materializa a abertura da frente propria de Terminal VWAP e infraestrutura da UI moderna.

## 3. Estado git no momento da auditoria

Branch:

audit/ui-modern-terminal-vwap

HEAD:

bd08ff7

Status resumido antes desta auditoria:

LIMPO

Ultimos commits relevantes:

bd08ff7 test: cover partial ui modern cli env precedence
3341dee test: document ui modern cli help options
a356a9b test: add ui modern cli invalid env fallback smoke
34a6e8d feat: honor ui modern launcher environment options
50fbf49 test: add ui modern cli help smoke
3ef66a5 test: add ui modern cli subprocess smoke
fedd676 test: add ui modern package entrypoint smoke
cf4e39c test: add ui modern launcher routing smoke
fafe28c test: add ui modern terminal vwap wiring smoke
ef7d17d docs: normalize decisions smoke record formatting
1e23db3 docs: record approved decisions ui smoke without backticks
644f73c fix: correct root ui quick launcher
d3846a0 fix: add root ui launcher
938a2c7 docs: correct invalid decisions ui smoke result

## 4. Documentos de controle localizados

- reports/auditoria/UI_FRENTES_ENCERRADAS.md: PRESENTE
- reports/auditoria/UI_PENDENCIAS_REMANESCENTES.md: PRESENTE
- docs/MATRIZ_EQUIVALENCIA_UI.md: PRESENTE
- docs/REGISTRO_EXECUCAO_SMOKE_DECISOES_UI.md: PRESENTE
- docs/DESENVOLVIMENTO_UI.md: PRESENTE

## 5. Testes automatizados localizados

- ATT/tests/test_ui_modern_cli_env_routing.py: PRESENTE
- ATT/tests/test_ui_modern_cli_help.py: PRESENTE
- ATT/tests/test_ui_modern_cli_subprocess.py: PRESENTE
- ATT/tests/test_ui_modern_package_entrypoint.py: PRESENTE
- ATT/tests/test_ui_modern_app_launcher.py: PRESENTE
- ATT/tests/test_ui_modern_dark_window_terminal_vwap_wiring.py: PRESENTE

## 6. Frentes em que houve avancos

### 6.1. Documentacao de controle

Situacao:

AVANCADA

Evidencia:

- consolidacao previa de frentes encerradas;
- consolidacao de pendencias remanescentes;
- diretrizes de desenvolvimento registradas;
- proibicoes de escopo formalizadas;
- regra de validacao antes de commit registrada.

Evolucao estimada:

90 por cento na fase documental anterior.

Pendencia atual:

Registrar a frente Terminal VWAP como auditoria propria de evolucao macro.

### 6.2. Separacao de escopos

Situacao:

AVANCADA

Evidencia:

- Terminal VWAP foi separado da branch Decisoes dark panel;
- a branch atual trata Terminal VWAP como frente propria;
- banco, pipeline, payoff e UIDataModel continuam fora da frente atual.

Evolucao estimada:

85 por cento.

Pendencia atual:

Manter os proximos blocos sem misturar areas proibidas.

### 6.3. Launcher moderno, CLI, help, package entrypoint e subprocess

Situacao:

MUITO AVANCADA

Evidencia:

- testes de help CLI;
- testes de subprocess;
- testes de package entrypoint;
- testes de app launcher;
- testes de roteamento por ambiente;
- testes de fallback para ambiente invalido;
- testes de precedencia de CLI sobre ambiente;
- testes de precedencia parcial preservando configuracao de ambiente nao sobrescrita.

Evolucao estimada:

90 por cento.

Pendencia atual:

Fechar pacote de regressao automatizada da infraestrutura antes de entrar em validacao funcional maior.

### 6.4. Terminal VWAP na UI moderna

Situacao:

INICIADA

Evidencia:

- existe teste de wiring inicial com dark window e Terminal VWAP;
- a branch atual esta aberta como frente propria de auditoria Terminal VWAP;
- a infraestrutura de abertura e roteamento ja esta coberta por testes.

Evolucao estimada:

40 por cento na preparacao tecnica da frente.

Evolucao funcional estimada:

15 por cento no fluxo operacional completo do Terminal VWAP.

Pendencias funcionais ainda nao encerradas:

- fluxo completo de estruturas;
- fluxo completo de pernas;
- estados vazios;
- mensagens de status;
- acoes operacionais proprias;
- alertas;
- KPIs;
- graficos;
- validacao visual;
- regressao manual ou automatizada de comportamento.

### 6.5. Matriz global de equivalencia UI

Situacao:

ABERTA

Evolucao estimada:

20 por cento.

A matriz global ainda nao deve ser usada para autorizar substituicao da UI atual.

### 6.6. Banco, dados e pipeline

Situacao:

FORA DE ESCOPO DA FRENTE ATUAL

Evolucao estimada nesta branch:

0 por cento por decisao correta de escopo.

Nao deve ser tratado como atraso desta branch.

### 6.7. Payoff e UIDataModel

Situacao:

FORA DE ESCOPO DA FRENTE ATUAL

Evolucao estimada nesta branch:

0 por cento por decisao correta de escopo.

## 7. Mudanca de estrategia

A partir deste ponto, a evolucao deixa de ser conduzida por microalteracoes isoladas e passa a ser conduzida por blocos macro.

Cada bloco macro deve conter:

1. busca previa de arquivos e historico;
2. classificacao de escopo;
3. alteracao concentrada em uma unica frente;
4. teste automatizado ou validacao documental;
5. revisao de diff;
6. commit unico por intencao;
7. registro de evidencia quando a mudanca for relevante.

## 8. Tamanho autorizado das proximas correcoes

As proximas correcoes podem ser maiores que as anteriores, desde que respeitem estas regras:

- uma frente por bloco;
- uma intencao por commit;
- nenhum banco;
- nenhum schema;
- nenhum pipeline;
- nenhuma regra de negocio;
- nenhum service;
- nenhum repository;
- nenhum controller;
- nenhuma mistura com payoff;
- nenhuma mistura com UIDataModel;
- nenhuma declaracao de equivalencia global da UI moderna.

Correcoes maiores autorizadas nesta frente:

- consolidar cobertura automatizada de launcher moderno;
- consolidar contratos de CLI e ambiente;
- auditar carregamento inicial do Terminal VWAP;
- validar criacao da janela dark com Terminal VWAP;
- validar estados vazios do Terminal VWAP se estiverem restritos a UI;
- validar mensagens de status do Terminal VWAP se estiverem restritas a UI;
- validar selecao e exibicao visual se nao exigir banco, service, repository ou controller;
- organizar roteiro de regressao macro do Terminal VWAP.

## 9. Blocos macro recomendados

### Bloco M1 - Fechamento da infraestrutura do launcher moderno

Objetivo:

Consolidar entrada, CLI, ambiente, help, subprocess, package entrypoint e wiring inicial.

Criterio de conclusao:

- pacote automatizado executado;
- resultado registrado;
- diff limpo;
- commit registrado.

Status atual:

EM ANDAMENTO AVANCADO.

### Bloco M2 - Auditoria funcional inicial do Terminal VWAP

Objetivo:

Mapear arquivos reais do Terminal VWAP e identificar pontos de entrada, componentes visuais, estados vazios e acoes.

Criterio de conclusao:

- inventario de arquivos do Terminal VWAP;
- classificacao dos componentes;
- lista de testes possiveis sem alterar banco ou regra de negocio.

Status atual:

PENDENTE.

### Bloco M3 - Correcoes UI-only do Terminal VWAP

Objetivo:

Aplicar correcoes maiores, mas restritas a UI, depois da auditoria M2.

Permitido:

- ajuste de montagem visual;
- ajuste de estado vazio;
- ajuste de mensagem;
- ajuste de wiring;
- ajuste de guard clause de UI;
- teste automatizado de comportamento da UI.

Proibido:

- alterar origem de dados;
- alterar consulta;
- alterar contrato de repository;
- alterar regra de negocio;
- alterar banco.

Status atual:

PENDENTE.

### Bloco M4 - Regressao automatizada acumulada

Objetivo:

Executar todos os testes da frente e registrar evidencia.

Criterio de conclusao:

- suite da UI moderna executada;
- falhas classificadas;
- correcoes feitas em lote unico por frente;
- commit registrado.

Status atual:

PENDENTE.

### Bloco M5 - Matriz de equivalencia e decisao de continuidade

Objetivo:

Atualizar criterio global apenas depois de estabilizar a frente Terminal VWAP.

Criterio de conclusao:

- matriz atualizada;
- decisao formal sobre equivalencia parcial;
- nenhuma substituicao global sem regressao.

Status atual:

PENDENTE.

## 10. Percentual de evolucao revisado

### Infraestrutura do launcher moderno

Evolucao estimada:

90 por cento.

### Frente atual Terminal VWAP, considerando auditoria e preparacao

Evolucao estimada:

45 por cento.

### Terminal VWAP funcional completo

Evolucao estimada:

15 por cento.

### Frente UI completa

Evolucao estimada:

25 por cento.

## 11. Decisao de rota

A branch atual permanece dentro da rota.

A estrategia passa a aceitar passos maiores, desde que cada passo seja um bloco operacional fechado e auditavel.

Nao ha autorizacao para desenvolvimento amplo sem auditoria previa.

Nao ha autorizacao para misturar Terminal VWAP com banco, pipeline, payoff, UIDataModel ou regra de negocio.

A proxima acao recomendada e executar o Bloco M1 e depois iniciar o Bloco M2.

## 12. Proxima acao obrigatoria

Executar regressao automatizada acumulada da infraestrutura ja criada.

Depois, iniciar inventario real dos arquivos do Terminal VWAP para planejar correcoes maiores de UI-only.

Classificacao:

DOCUMENTACAO_DE_CONTROLE

CRITERIO_GLOBAL_UI

AUDITORIA_TERMINAL_VWAP


---

## Nota de rastreabilidade

Este documento foi promovido para `docs/auditoria/` porque a pasta `reports/` esta ignorada pelo Git e deve ser tratada como area local/temporaria de saidas.

A partir desta auditoria, a documentacao de controle versionada da rota UI deve permanecer em `docs/auditoria/`.
