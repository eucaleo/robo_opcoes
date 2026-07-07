# Pendencias remanescentes da auditoria UI

Data de consolidacao: 2026-07-03 17:33

Branch de referencia: refactor/decisions-dark-panel-large-block

REGRAS EXPLICITAS PARA DESENVOLVIMENTO DO PROJETO:

A) Não migrar para web
B) Não utilizar emojis
C) Manter-se ao scopo do projeto sem derivações
D) Efetuar buscas de dados e arquivos antes de alterações
E) Toda mudança deve ser testada apos concluida
F) Apos o encerramento de fase o teste deve compor todas as fases encerradas, assim não ficara pendencias
G) Evitar codigos intermediarios em explicações, ir direto ao ponto
H) Em alterações sempre gerar CODIGO AUTOMATIZADO VIA GIT BASH INDENTADO.
I) A cada alteração concluida e testada, commitar.
J) Não codar sem rumo, se necessario buscar a evolução no git ou nos documentos obrigatorios.
K) Criar arquivo de auditoria pra ser atualizado com os testes, assim vamos testando as conclusoes e criando o caminho de evolução ao mesmo tempo auditando o que esta pronto
L) Não gerar codigo com crase, sempre com indentação
M)Não permitir dívida técnica, para cotação viva isso é risco operacional.

## 1. Objetivo

Este documento concentra o que ainda falta apos separar as frentes ja encerradas ou consolidadas da auditoria UI.
Este documento deve orientar as proximas decisoes sem reabrir indevidamente frentes ja encerradas.

## 2. Decisao geral

A frente UI completa permanece aberta.
A fatia Decisoes dark panel pode ser tratada como equivalencia parcial operacional, mas isso nao equivale a encerramento global da UI.
A UI atual permanece como caminho principal.

Nao esta autorizado:

- eliminar a UI atual;
- trocar o entrypoint principal;
- alterar banco;
- alterar regra de negocio;
- alterar services, repositories ou controllers;
- declarar equivalencia completa da UI moderna dark.

## 3. Pendencia imediata antes de encerrar documentalmente a branch atual

Antes de smoke manual, a pendencia imediata e revisar este desmembramento.

Passos recomendados agora:

1. revisar reports/auditoria/UI_FRENTES_ENCERRADAS.md;
2. revisar reports/auditoria/UI_PENDENCIAS_REMANESCENTES.md;
3. ajustar classificacoes se necessario;
4. validar diff;
5. commitar o desmembramento documental;
6. somente depois decidir a execucao do smoke manual.

Classificacao:

DOCUMENTACAO_DE_CONTROLE

## 4. Pendencias da fatia Decisoes dark panel

### 4.1. Backlog de melhorias da aba Decisoes

Itens remanescentes:

- filtros avancados equivalentes ao painel legado;
- exibicao estruturada de rationale ou why JSON;
- ordenacao visual da listagem;
- estados vazios mais detalhados;
- indicadores adicionais de contagem filtrada versus total;
- ergonomia dos botoes;
- destaque visual persistente da decisao carregada;
- acao inversa Terminal VWAP para Decisoes filtradas pela estrutura selecionada;
- testes automatizados especificos para DecisionsDarkPanel;
- configuracao customizada de colunas exportadas pelo usuario;
- revisao futura para equivalencia completa com a UI canonica.

Classificacao:

BACKLOG_MELHORIA_UI_DECISOES

Bloqueia encerramento parcial da fatia Decisoes:

NAO

Bloqueia equivalencia global da UI:

PODE_BLOQUEAR_DEPENDENDO_DO_CRITERIO_GLOBAL

## 5. Pendencias globais da frente UI

### 5.1. Matriz global de equivalencia UI

A matriz global de equivalencia foi criada, mas ainda precisa ser preenchida e usada como criterio de decisao.

Documento relacionado:

- docs/MATRIZ_EQUIVALENCIA_UI.md

Itens pendentes:

- preencher matriz com base em arquivos reais;
- classificar telas e fluxos como equivalentes, parciais, experimentais ou fora de escopo;
- definir checklist minimo por aba;
- definir criterio de substituicao segura;
- impedir troca do caminho principal sem validacao funcional e operacional.

Classificacao:

CRITERIO_GLOBAL_UI

Bloqueia encerramento da UI completa:

SIM

Bloqueia encerramento parcial da fatia Decisoes:

NAO

### 5.2. Inventario e classificacao de areas UI

Documentos ja criados:

- docs/INVENTARIO_ARQUIVOS_UI.md
- docs/CLASSIFICACAO_AREAS_UI.md
- docs/MATRIZ_CRUZADA_AREAS_UI.md

Itens pendentes:

- revisar classificacao por area;
- separar UI canonica, UI moderna, Decisoes, Terminal VWAP, payoff, UIDataModel e banco;
- manter escopos separados por branch;
- evitar misturar ajustes visuais com banco ou regra de negocio.

Classificacao:

CRITERIO_GLOBAL_UI

## 6. Pendencias fora do escopo da branch Decisoes dark panel

### 6.1. Terminal VWAP

Itens fora do escopo da branch atual:

- validacoes especificas do Terminal VWAP;
- fluxo completo de estruturas;
- fluxo completo de pernas;
- alertas;
- KPIs;
- graficos;
- estados vazios;
- acoes operacionais proprias do terminal.

Classificacao:

FORA_ESCOPO_BRANCH_DECISOES_DARK

Acao recomendada:

Abrir auditoria propria para Terminal VWAP.

### 6.2. Payoff curve

Itens fora do escopo da branch atual:

- consistencia da curva de payoff;
- comparacao de curvas;
- Curva A;
- exportacao PNG fora da fatia ja validada;
- contratos de payoff;
- formulas e dados de entrada.

Classificacao:

FORA_ESCOPO_BRANCH_DECISOES_DARK

Acao recomendada:

Abrir frente propria para payoff.

### 6.3. UIDataModel

Itens fora do escopo da branch atual:

- validacoes completas de UIDataModel;
- get_payoff_curve_info;
- get_payoff_curve;
- consistencia de queries;
- origem de dados consumidos pela UI moderna;
- novas refatoracoes tecnicas.

Classificacao:

FORA_ESCOPO_BRANCH_DECISOES_DARK

Acao recomendada:

Tratar em frente tecnica separada.

## 7. Pendencias de banco, dados e pipeline

Foi observada divergencia entre:

- dados/app.db;
- dados/derived.db.

Itens pendentes:

- verificar origem dos dados exibidos;
- confirmar contratos de leitura usados pela UI;
- confirmar papel de app.db como banco canonico;
- evitar sincronismo continuo entre derived.db e app.db;
- evitar sincronismo continuo entre app.db e derived.db;
- tratar saneamento de pipeline em frente propria.

Classificacao:

BANCO_DADOS_PIPELINE

Bloqueia encerramento parcial da fatia Decisoes dark panel:

NAO

Bloqueia conclusao arquitetural global:

SIM

Acao recomendada:

Abrir frente propria de banco, dados e pipeline.

## 8. Pendencias de regressao UI

Itens pendentes:

- roteiro manual por aba;
- validacao de abertura pelo entrypoint principal;
- validacao de navegacao entre abas;
- validacao de acoes sem selecao;
- validacao de dados ausentes;
- validacao de mensagens de status;
- validacao visual em dark mode;
- registro de evidencias minimas antes de merge amplo.

Classificacao:

REGRESSAO_UI

Acao recomendada:

Executar por fatias pequenas, iniciando por Decisoes somente apos revisar este desmembramento.

## 9. Pendencias de encerramento da frente UI

Para encerrar a frente UI completa, ainda faltam:

- matriz global de equivalencia preenchida;
- criterios objetivos de substituicao;
- validacao da UI canonica;
- validacao da UI moderna dark;
- decisao sobre o que permanece, o que substitui e o que sera descartado;
- regressao manual completa;
- confirmacao de que banco, regra de negocio, services, repositories e entrypoint foram preservados;
- plano de merge amplo, se aplicavel.

Classificacao:

PLANO_ENCERRAMENTO_UI

Status:

ABERTO

## 10. Proxima ordem recomendada

A ordem recomendada a partir deste ponto e:

1. revisar os dois documentos de desmembramento;
2. corrigir classificacoes, se necessario;
3. commitar somente o desmembramento documental;
4. depois executar smoke manual de Decisoes;
5. preencher registro de smoke;
6. validar diff;
7. commitar registro de smoke;
8. abrir frentes separadas para Terminal VWAP, payoff, UIDataModel e banco.

## 11. Decisao final deste documento

O documento historico de auditoria permanece como fonte de rastreabilidade.
Este documento passa a controlar as pendencias remanescentes.
A frente UI completa permanece aberta.
A branch atual nao deve tentar resolver toda a UI.
A entrega de Decisoes dark panel pode ser encerrada apenas como fatia parcial operacional depois da revisao documental e da validacao posterior definida para essa fatia.

## 12. Diretrizes de desenvolvimento para manter a rota

Esta secao define as diretrizes obrigatorias para proximas alteracoes relacionadas a auditoria UI.
O objetivo e evitar reabertura indevida de frentes ja encerradas, mistura de escopos e alteracoes fora da rota definida para a branch atual.

### 12.1. Principio principal

A UI atual permanece como caminho principal ate que exista criterio global de equivalencia, regressao e substituicao controlada.
A UI moderna dark permanece como caminho paralelo e incremental.
Nenhuma alteracao nesta branch deve declarar equivalencia completa da UI moderna dark.

### 12.2. Escopo permitido da branch atual

A branch atual deve permanecer limitada a:

- consolidacao documental da auditoria UI;
- separacao entre frentes encerradas e pendencias;
- validacao posterior da fatia Decisoes dark panel;
- ajustes documentais de classificacao;
- preparacao de registros para smoke manual;
- pequenas correcoes diretamente relacionadas a Decisoes dark panel, se forem indispensaveis e isoladas.

Qualquer item fora disso deve ser tratado em branch ou frente propria.

### 12.3. Escopos proibidos nesta branch

Nao esta autorizado nesta branch:

- eliminar a UI atual;
- trocar o entrypoint principal;
- alterar banco de dados;
- alterar schema;
- alterar regra de negocio;
- alterar services;
- alterar repositories;
- alterar controllers;
- alterar pipeline de dados;
- sincronizar app.db com derived.db;
- sincronizar derived.db com app.db;
- refatorar Terminal VWAP fora de Decisoes;
- refatorar payoff fora de ajuste estritamente necessario;
- resolver equivalencia global da UI;
- misturar melhoria visual com alteracao funcional ampla.

### 12.4. Criterio para novas alteracoes

Antes de qualquer nova alteracao, classificar o item como uma das categorias abaixo:

- DOCUMENTACAO_DE_CONTROLE
- REGRESSAO_UI_DECISOES
- BACKLOG_MELHORIA_UI_DECISOES
- CRITERIO_GLOBAL_UI
- FORA_ESCOPO_BRANCH_DECISOES_DARK
- BANCO_DADOS_PIPELINE
- REGRESSAO_UI
- PLANO_ENCERRAMENTO_UI

Se o item nao couber claramente em uma dessas categorias, ele nao deve ser implementado antes de nova decisao documental.

### 12.5. Regra de separacao por frente

Cada frente deve ter escopo proprio.

Decisoes dark panel:

- listagem;
- filtros simples;
- detalhe;
- copia;
- exportacao CSV;
- carregamento de estrutura associada;
- smoke manual da fatia.

Terminal VWAP:

- abrir frente propria.

Payoff:

- abrir frente propria.

UIDataModel:

- abrir frente tecnica propria.

Banco, dados e pipeline:

- abrir frente propria.

UI global:

- tratar somente apos matriz de equivalencia preenchida e criterio de regressao definido.

### 12.6. Regra para smoke manual

O smoke manual nao deve ser usado para descobrir escopo.
O smoke manual deve ser executado somente depois que:

- frentes encerradas estiverem separadas;
- pendencias remanescentes estiverem revisadas;
- diretrizes de desenvolvimento estiverem registradas;
- a fatia a validar estiver claramente delimitada.

O smoke manual de Decisoes deve validar apenas a fatia Decisoes dark panel.

### 12.7. Regra para documentacao

Toda nova decisao relevante deve atualizar pelo menos um dos documentos de controle:

- reports/auditoria/UI_FRENTES_ENCERRADAS.md
- reports/auditoria/UI_PENDENCIAS_REMANESCENTES.md
- docs/MATRIZ_EQUIVALENCIA_UI.md
- docs/REGISTRO_EXECUCAO_SMOKE_DECISOES_UI.md

Nao criar novos documentos se um documento de controle existente for suficiente.

### 12.8. Regra para commits

Commits devem ser pequenos e classificados por intencao:

- docs: documentacao;
- fix: correcao;
- feat: funcionalidade;
- refactor: refatoracao sem mudanca funcional;
- test: teste ou validacao automatizada.

Nao misturar no mesmo commit:

- documentacao e alteracao funcional ampla;
- UI e banco;
- UI e regra de negocio;
- Terminal VWAP e Decisoes;
- payoff e Decisoes;
- refatoracao tecnica e mudanca visual.

### 12.9. Regra para validacao antes de commit

Antes de commit, executar no minimo:

- git diff --check;
- revisao do diff;
- validacao de que os arquivos alterados pertencem ao escopo da frente atual.

Quando houver Python alterado, executar tambem validacao de compilacao aplicavel.

Quando houver UI alterada, registrar se a validacao foi:

- nao aplicavel;
- visual;
- smoke manual;
- teste automatizado;
- validacao documental.

### 12.10. Regra para classificacao de encerramento

Uma frente so pode sair de pendencias quando houver evidencia suficiente de uma das situacoes:

- documentacao consolidada;
- patch aplicado e validado;
- commit registrado;
- tag ou checkpoint registrado;
- smoke manual aprovado;
- decisao formal de fora de escopo;
- decisao formal de backlog.

Na duvida, manter como pendencia ou backlog.
Nao promover item duvidoso para encerrado.

### 12.11. Regra para evitar regressao de escopo

Se uma alteracao exigir mexer em banco, pipeline, regra de negocio, services, repositories ou controllers, a alteracao deve parar e ser reclassificada.
Se uma alteracao exigir mexer em Terminal VWAP fora do carregamento a partir de Decisoes, a alteracao deve parar e ser reclassificada.
Se uma alteracao exigir mexer em payoff fora de comportamento ja validado, a alteracao deve parar e ser reclassificada.

### 12.12. Regra sobre caminhos e nomes de arquivos

Manter atencao especial a diferencas entre caminhos com maiusculas e minusculas, especialmente:

- UI/
- ui/

Antes de alterar arquivos com nomes equivalentes em caixas diferentes, confirmar qual e o caminho canonico usado pelo projeto.
Nao criar duplicidade nova de arquivos por diferenca de caixa.

### 12.13. Ordem de trabalho a partir desta consolidacao

A ordem aprovada passa a ser:

1. consolidar estes dois documentos de auditoria;
2. adicionar estas diretrizes de desenvolvimento;
3. validar diff documental;
4. commitar a consolidacao documental;
5. somente depois executar smoke manual de Decisoes;
6. preencher registro de smoke;
7. commitar registro de smoke;
8. abrir frentes separadas para Terminal VWAP, payoff, UIDataModel e banco, se necessario.

### 12.14. Decisao de rota

A branch atual nao deve tentar resolver toda a UI.
A branch atual deve apenas consolidar a separacao entre encerrados, pendencias e criterios de continuidade.
A fatia Decisoes dark panel permanece como entrega parcial operacional, pendente de validacao posterior por smoke manual registrado.
A frente UI completa permanece aberta.

<!-- FECHAMENTO_DOCUMENTAL_DECISIONS_DARK_PANEL_2026_07_06 -->

## 13. Fechamento documental da branch Decisoes dark panel

Data: 2026-07-06

Branch: refactor/decisions-dark-panel-large-block

### 13.1. Situacao documental

A consolidacao documental da branch atual foi concluida como controle de rota da fatia Decisoes dark panel.

Esta conclusao documental nao declara encerramento global da frente UI e nao declara equivalencia completa da UI moderna dark.

A UI atual permanece como caminho principal.

### 13.2. Evidencias registradas

Foram registrados e publicados os seguintes pontos de controle:

- separacao entre frentes encerradas e pendencias remanescentes;
- reclassificacao de referencias de smoke manual como validacao legada quando nao forem bloqueadoras;
- remocao do smoke manual como bloqueador documental previo da lista de pendencias da UI de Decisoes;
- normalizacao versionada de line endings via .gitattributes;
- checkpoint local de evolucao da branch em docs/DESENVOLVIMENTO_UI.md;
- limpeza de whitespace do checkpoint documental.

### 13.3. Commits de referencia desta consolidacao

- 3dbe277 - docs(ui): reinicia reports com controle consolidado da auditoria
- 0bd8b82 - docs: remove smoke manual blocker from decisions UI pending list
- e54f90b - docs: reclassify smoke manual references as legacy validation
- d2a95ee - chore: normalize repository line endings
- 66ff4c8 - docs: record decisions ui refactor checkpoint
- e92395d - docs: clean decisions ui checkpoint whitespace

### 13.4. Decisao de rota

A fase documental da branch atual fica considerada consolidada para fins de continuidade operacional.

A proxima fase autorizada nao e desenvolvimento funcional amplo.

A proxima fase autorizada e a validacao da fatia Decisoes dark panel por smoke manual registrado.

### 13.5. Escopo permitido da proxima fase

A proxima fase deve validar apenas a fatia Decisoes dark panel, incluindo:

- abertura da UI pelo caminho atual do projeto;
- acesso a aba ou painel de Decisoes;
- listagem de decisoes;
- filtros simples existentes;
- detalhe da decisao;
- copia, quando aplicavel;
- exportacao CSV, quando aplicavel;
- carregamento de estrutura associada, quando aplicavel;
- comportamento sem selecao;
- comportamento com dados ausentes;
- mensagens de status;
- validacao visual em dark mode.

### 13.6. Escopos ainda proibidos nesta branch

Permanece nao autorizado nesta branch:

- eliminar a UI atual;
- trocar o entrypoint principal;
- alterar banco;
- alterar schema;
- alterar regra de negocio;
- alterar services;
- alterar repositories;
- alterar controllers;
- alterar pipeline;
- sincronizar app.db com derived.db;
- sincronizar derived.db com app.db;
- resolver Terminal VWAP fora do carregamento a partir de Decisoes;
- resolver payoff fora de comportamento ja validado;
- declarar equivalencia global da UI moderna dark.

### 13.7. Proxima acao obrigatoria

Executar smoke manual da fatia Decisoes dark panel e registrar a evidencia no documento de controle apropriado.

Documento indicado:

- docs/REGISTRO_EXECUCAO_SMOKE_DECISOES_UI.md

Somente apos esse registro deve ser decidida qualquer correcao funcional ou melhoria visual adicional.

<!-- ATUALIZACAO_POS_SMOKE_DECISOES_2026_07_06 -->

## 14. Atualizacao pos smoke Decisoes dark panel

Data: 2026-07-06

Branch de origem concluida:

    refactor/decisions-dark-panel-large-block

Commit final validado:

    ef7d17d

### 14.1. Situacao da fatia Decisoes dark panel

A fatia Decisoes dark panel foi validada operacionalmente por smoke manual registrado.

O registro aprovado esta em:

    docs/REGISTRO_EXECUCAO_SMOKE_DECISOES_UI.md

Resultado:

    APROVADO

Esta conclusao vale apenas para a fatia Decisoes dark panel.

Nao declara equivalencia global da UI moderna dark.

Nao encerra a frente UI completa.

### 14.2. Pendencias que permanecem abertas

Permanecem abertas as pendencias globais ja classificadas neste documento, incluindo:

- matriz global de equivalencia UI;
- regressao UI completa;
- Terminal VWAP;
- payoff;
- UIDataModel;
- banco, dados e pipeline;
- plano de encerramento global da UI.

### 14.3. Proxima fase aberta

A proxima fase operacional passa a ser auditoria propria de Terminal VWAP.

Classificacao:

    REGRESSAO_UI

Escopo inicial:

    auditoria documental e inventario de validacao, sem alteracao funcional ampla.
