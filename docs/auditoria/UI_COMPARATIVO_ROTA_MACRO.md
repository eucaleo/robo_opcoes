# Auditoria comparativa de rota UI e estrategia macro de correcoes

Data de consolidacao: 2026-07-07 15:46:35

Branch auditada: audit/ui-modern-terminal-vwap

HEAD atual: bd08ff7

Documento base comparado:

- reports/auditoria/UI_PENDENCIAS_REMANESCENTES.md: PRESENTE

Documento macro novo:

- docs/auditoria/UI_AUDITORIA_MACRO_EVOLUCAO.md: PRESENTE

## 1. Objetivo

Este documento compara a rota anterior de auditoria UI com a nova estrategia macro de evolucao.

A finalidade e manter coerencia, reduzir risco e aumentar o tamanho util das correcoes, sem perder controle operacional.

A estrategia anterior foi adequada para estabilizacao, separacao de escopos e reducao de risco inicial.

A partir deste ponto, a estrategia passa a priorizar blocos maiores de correcao, auditoria e validacao, mantendo uma frente por bloco.

## 2. Estado Git no momento desta auditoria

Branch:

audit/ui-modern-terminal-vwap

HEAD:

bd08ff7

Status resumido:

LIMPO

Ultimos commits:

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
5f8fe5c docs: record approved decisions ui smoke
5367d60 docs: prepare decisions ui smoke record

## 3. Diagnostico da estrategia anterior

A estrategia anterior teve valor porque:

- separou frentes encerradas de pendencias remanescentes;
- impediu troca indevida do entrypoint principal;
- preservou banco, schema, pipeline, regra de negocio, services, repositories e controllers;
- impediu declaracao prematura de equivalencia global da UI moderna dark;
- consolidou diretrizes de desenvolvimento;
- criou criterio minimo de validacao antes de commit;
- orientou a abertura de frente propria para Terminal VWAP.

Ponto fraco identificado:

- a execucao ficou excessivamente granular;
- a evolucao passou a ocorrer em microcorrecoes;
- o custo de auditoria por pequena alteracao ficou alto;
- a velocidade rumo ao encerramento ficou menor do que o nivel de seguranca atual permite.

## 4. O que continua valido do documento anterior

Continuam validas as seguintes regras:

- nao migrar para web;
- nao eliminar a UI atual;
- nao trocar o entrypoint principal;
- nao alterar banco;
- nao alterar schema;
- nao alterar pipeline;
- nao sincronizar app.db com derived.db;
- nao sincronizar derived.db com app.db;
- nao alterar regra de negocio;
- nao alterar services;
- nao alterar repositories;
- nao alterar controllers;
- nao misturar Terminal VWAP com payoff;
- nao misturar Terminal VWAP com UIDataModel;
- nao declarar equivalencia global da UI moderna dark;
- manter commits classificados por intencao;
- executar git diff --check antes de commit;
- testar toda alteracao apos concluida;
- registrar evidencia quando a mudanca for relevante.

## 5. O que deixa de ser estrategia principal

A partir desta auditoria, deixa de ser estrategia principal:

- abrir uma microfrente para cada teste isolado;
- fazer uma correcao minima por vez quando o problema pertence ao mesmo bloco;
- atrasar correcoes relacionadas apenas para manter granularidade excessiva;
- tratar cada lacuna de launcher como uma fase separada;
- tratar cada validacao de CLI, ENV e help como entrega isolada.

Esses itens nao ficam proibidos.

Eles apenas deixam de ser a forma preferencial de evolucao.

## 6. Nova estrategia aprovada

A nova estrategia passa a ser evolucao por blocos macro.

Cada bloco deve:

1. auditar arquivos reais e historico antes de alterar;
2. classificar a frente;
3. agrupar correcoes relacionadas;
4. manter uma unica frente operacional;
5. evitar mistura com banco, pipeline, regra de negocio, services, repositories e controllers;
6. gerar ou atualizar testes automatizados;
7. executar regressao acumulada da frente;
8. validar diff;
9. commitar com mensagem unica por intencao;
10. atualizar auditoria quando houver decisao relevante.

## 7. Novo criterio para tamanho das correcoes

Uma correcao pode ser maior quando todos os criterios abaixo forem verdadeiros:

- pertence a mesma frente;
- altera o mesmo fluxo operacional;
- pode ser validada por um pacote de testes unico;
- nao exige alteracao de banco;
- nao exige alteracao de schema;
- nao exige alteracao de pipeline;
- nao exige alteracao de regra de negocio;
- nao exige alteracao de services;
- nao exige alteracao de repositories;
- nao exige alteracao de controllers;
- nao mistura UI moderna com payoff ou UIDataModel;
- nao muda o entrypoint principal;
- nao declara equivalencia global.

Se qualquer criterio falhar, o bloco deve parar e ser reclassificado.

## 8. Roteiro macro revisado rumo ao encerramento

### M1 - Fechamento da infraestrutura do launcher moderno

Escopo:

- package entrypoint;
- app launcher;
- subprocess smoke;
- help CLI;
- opcoes CLI;
- roteamento por ambiente;
- fallback de ambiente invalido;
- precedencia CLI sobre ambiente;
- precedencia parcial CLI/ENV;
- wiring inicial com Terminal VWAP.

Status:

EM FECHAMENTO.

Evidencia atual:

- pacote acumulado executado;
- resultado registrado na execucao local: 18 passed.

Criterio para encerrar M1:

- documento macro criado;
- auditoria comparativa criada;
- git diff --check aprovado;
- commit documental registrado;
- regressao acumulada repetida antes do proximo bloco funcional.

### M2 - Auditoria real dos arquivos Terminal VWAP

Escopo:

- localizar arquivos reais do Terminal VWAP;
- identificar entrypoints internos;
- identificar componentes visuais;
- identificar estados vazios;
- identificar mensagens de status;
- identificar dependencias proibidas;
- identificar testes existentes;
- identificar lacunas testaveis sem banco.

Tipo de correcao permitida:

DOCUMENTACAO_DE_CONTROLE e TESTE_AUTOMATIZADO.

Criterio de encerramento:

- inventario criado;
- dependencias classificadas;
- lista de correcoes UI-only priorizada.

### M3 - Primeiro pacote grande UI-only do Terminal VWAP

Escopo permitido:

- montagem visual;
- guards de UI;
- estados vazios;
- mensagens de status;
- comportamento sem selecao;
- comportamento com dados ausentes;
- wiring entre painel e container;
- testes automatizados do comportamento acima.

Escopo proibido:

- banco;
- schema;
- pipeline;
- services;
- repositories;
- controllers;
- regra de negocio;
- payoff;
- UIDataModel.

Criterio de encerramento:

- pacote de correcao aplicado;
- testes novos e antigos aprovados;
- diff revisado;
- commit unico por intencao.

### M4 - Segundo pacote grande Terminal VWAP operacional de UI

Escopo permitido:

- estruturas na camada visual;
- pernas na camada visual;
- botoes e acoes de UI;
- mensagens de erro ou ausencia de dado;
- KPIs somente se ja estiverem disponiveis pela camada atual;
- graficos somente se ja estiverem disponiveis pela camada atual.

Regra especial:

Se exigir dado novo, query nova, service novo, repository novo ou controller novo, parar e reclassificar.

Criterio de encerramento:

- comportamento operacional basico validado sem alterar camadas proibidas;
- testes aprovados;
- auditoria atualizada.

### M5 - Regressao ampla da frente Terminal VWAP

Escopo:

- executar todos os testes UI moderna relacionados;
- executar smoke manual se aplicavel;
- registrar evidencias;
- classificar falhas por bloco;
- corrigir falhas em lote por frente.

Criterio de encerramento:

- suite automatizada aprovada;
- evidencia de smoke registrada quando aplicavel;
- pendencias restantes classificadas como backlog ou fora de escopo.

### M6 - Atualizacao da matriz global de equivalencia UI

Escopo:

- atualizar docs/MATRIZ_EQUIVALENCIA_UI.md;
- registrar equivalencia parcial, experimental ou fora de escopo;
- impedir substituicao global sem regressao ampla.

Criterio de encerramento:

- matriz atualizada com base em evidencias;
- decisao formal sobre o estado da UI moderna Terminal VWAP.

## 9. Estrategia de correcao por lote

A partir deste ponto, as correcoes devem ser agrupadas assim:

### Lote A - Infraestrutura de execucao

Agrupa:

- CLI;
- ENV;
- help;
- subprocess;
- package entrypoint;
- routing;
- fallback;
- precedencia.

Status:

PRATICAMENTE CONSOLIDADO.

### Lote B - Carregamento e montagem Terminal VWAP

Agrupa:

- imports;
- construcao de painel;
- acoplamento com dark window;
- fallback visual;
- ausencia de dependencia opcional;
- erro de inicializacao tratado na UI.

Status:

PROXIMO LOTE RECOMENDADO.

### Lote C - Estados e interacoes basicas

Agrupa:

- sem selecao;
- dados ausentes;
- lista vazia;
- mensagens de status;
- botoes desabilitados;
- selecao visual.

Status:

PENDENTE.

### Lote D - Fluxo visual de estruturas e pernas

Agrupa:

- exibicao de estruturas;
- exibicao de pernas;
- selecao;
- detalhe;
- atualizacao visual.

Status:

PENDENTE.

### Lote E - Evidencia, regressao e matriz

Agrupa:

- testes acumulados;
- smoke manual;
- registro de evidencia;
- matriz de equivalencia;
- decisao formal.

Status:

PENDENTE.

## 10. Percentual de evolucao apos revisao

Infraestrutura do launcher moderno:

90 por cento.

M1 como bloco macro:

85 por cento.

Frente Terminal VWAP considerando preparacao e wiring:

45 por cento.

Terminal VWAP funcional completo:

15 por cento.

Frente UI completa:

25 por cento.

Risco operacional atual:

MODERADO E CONTROLADO.

Motivo:

- existe backup e historico Git;
- existem testes automatizados acumulados;
- existe documentacao de controle;
- existem proibicoes claras;
- a nova estrategia aumenta o tamanho dos blocos sem liberar mistura de escopo.

## 11. Decisao de descarte controlado

O documento anterior nao deve ser removido fisicamente.

Ele permanece como fonte historica e rastreabilidade.

O que fica descartado e apenas a estrategia operacional de microcorrecoes como padrao principal.

A nova fonte de estrategia operacional passa a ser:

- docs/auditoria/UI_AUDITORIA_MACRO_EVOLUCAO.md;
- docs/auditoria/UI_COMPARATIVO_ROTA_MACRO.md.

## 12. Proxima acao obrigatoria

Encerrar documentalmente M1 com:

- diff validado;
- commit da auditoria comparativa;
- regressao acumulada registrada;
- status limpo.

Depois iniciar M2:

AUDITORIA REAL DOS ARQUIVOS TERMINAL VWAP.

Classificacao:

DOCUMENTACAO_DE_CONTROLE

AUDITORIA_TERMINAL_VWAP

CRITERIO_GLOBAL_UI


---

## Nota de rastreabilidade

Este documento foi promovido para `docs/auditoria/` porque a pasta `reports/` esta ignorada pelo Git e deve ser tratada como area local/temporaria de saidas.

A partir desta auditoria, a documentacao de controle versionada da rota UI deve permanecer em `docs/auditoria/`.

---

## Adendo M10 - leitura reconciliada

Este comparativo representa uma fotografia anterior da rota macro.

Como a frente Terminal VWAP avancou com documentos e PRs posteriores, a leitura atualizada deve considerar o documento:

    docs/auditoria/UI_TERMINAL_VWAP_M10_RECONCILIACAO_ROTA.md

A M10 reconcilia o estado real ate M9 e diferencia consolidacao de infraestrutura de testes de fechamento funcional macro.
