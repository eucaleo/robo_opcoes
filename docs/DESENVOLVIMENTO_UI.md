# Desenvolvimento UI

Documento de acompanhamento da frente UI.

---

## Checkpoint roadmap UI remanescente - Decisoes dark panel encerrado parcialmente

Data: 2026-07-03 15:55:24 -0300

Branch: refactor/decisions-dark-panel-large-block

### Estado atual registrado

A fatia Decisoes dark panel foi encerrada como:

    EQUIVALENCIA_PARCIAL_OPERACIONAL

Esta classificacao encerra apenas a entrega parcial e restrita da aba/painel de Decisoes no modo dark.

Nao encerra a frente UI completa.

A UI atual/canonica permanece como caminho principal ate que exista criterio global de equivalencia, regressao e substituicao controlada.

### O que foi considerado encerrado nesta fatia

- equivalencia operacional parcial da area de Decisoes no modo dark;
- callbacks essenciais presentes e documentados;
- selecao de decisao com validacao de indice;
- copia de detalhe;
- carregamento da estrutura associada;
- duplicacao de estrutura;
- arquivamento de estrutura;
- recalculo de payoff;
- registro de decisoes ADJUST e CLOSE;
- mensagens operacionais via _safe_status;
- preservacao de banco de dados, regra de negocio, services, repositories, entrypoint e contratos canonicos.

### Pendencias remanescentes da frente UI

As pendencias abaixo ficam fora do bloqueio desta branch e devem ser tratadas em frentes proprias.

#### 1. Backlog de melhorias da UI de Decisoes

Classificacao:

    BACKLOG_MELHORIA_UI_DECISOES

Itens:

- filtros avancados de decisoes;
- exibicao estruturada de rationale/why JSON;
- refinamentos visuais e ergonomicos;
- validacao manual ampliada de selecao vazia, selecao invalida e botoes dependentes;
- criterios adicionais de navegacao, ordenacao e leitura da tabela;
- revisao futura para eventual equivalencia completa com a UI atual.

#### 2. Criterio global de equivalencia da UI

Classificacao:

    CRITERIO_GLOBAL_UI

Itens:

- montar matriz de equivalencia entre UI atual/canonica e UI moderna/dark;
- definir quais telas podem ser consideradas equivalentes, parciais ou apenas experimentais;
- criar checklist minimo por aba;
- registrar criterios de substituicao segura;
- impedir troca do caminho principal sem validacao funcional e operacional.

#### 3. Terminal VWAP, payoff e UIDataModel

Classificacao:

    FORA_ESCOPO_BRANCH_DECISOES_DARK

Itens:

- Terminal VWAP;
- payoff curve;
- UI/models/ui_data.py;
- refatoracoes tecnicas de payoff;
- validacoes especificas de fluxo do terminal;
- consistencia de dados consumidos pela UI moderna.

Esta frente deve ser auditada separadamente, sem ser misturada com a entrega de Decisoes dark panel.

#### 4. Banco, dados e pipeline

Classificacao:

    BANCO_DADOS_PIPELINE

Itens:

- divergencia entre banco canonico moderno e banco volatil legado;
- verificacao de dados/app.db versus dados/derived.db;
- rastreio de origem dos dados exibidos;
- confirmacao dos contratos de leitura usados pela UI;
- saneamento de pipeline antes de qualquer conclusao global de UI.

Esta frente nao deve ser corrigida dentro de branch visual de Decisoes.

#### 5. Regressao e smoke manual da UI

Classificacao:

    REGRESSAO_UI

Itens:

- roteiro manual por aba;
- validacao de abertura da aplicacao pelo entrypoint principal;
- validacao de navegacao entre abas;
- validacao de acoes sem selecao;
- validacao de dados ausentes;
- validacao de mensagens de status;
- validacao visual em dark mode;
- registro de evidencias minimas antes de merge amplo.

#### 6. Estrategia de encerramento da frente UI

Classificacao:

    PLANO_ENCERRAMENTO_UI

Ordem sugerida:

1. manter a UI atual/canonica como caminho principal;
2. concluir documentacao das pendencias por classificacao;
3. abrir frentes pequenas e separadas por area;
4. evitar misturar banco, regra de negocio, services e UI visual na mesma branch;
5. validar cada fatia com py_compile, git diff --check e smoke manual;
6. somente discutir substituicao da UI atual apos matriz global de equivalencia.

### Decisao operacional

A branch atual pode seguir como encerrada para a fatia Decisoes dark panel, mas a frente UI permanece aberta.

Proximo trabalho recomendado:

    documentar matriz global de equivalencia UI
    separar backlog de Decisoes
    abrir auditoria propria para Terminal VWAP/payoff/UIDataModel
    abrir frente propria para banco/dados/pipeline

### Regra de preservacao

Enquanto a frente UI nao estiver encerrada globalmente, devem permanecer preservados:

- banco de dados;
- regras de negocio;
- services;
- repositories;
- entrypoint principal;
- contratos canonicos;
- UI atual como caminho principal.

---

## Referencia matriz global de equivalencia UI

Data: 2026-07-03 16:07:55 -0300

Foi criada a matriz global de equivalencia da UI em:

    docs/MATRIZ_EQUIVALENCIA_UI.md

A matriz passa a ser o documento de referencia para classificar telas e fluxos como:

- CANONICA;
- EQUIVALENTE;
- EQUIVALENCIA_PARCIAL_OPERACIONAL;
- EXPERIMENTAL;
- PENDENTE;
- FORA_ESCOPO.

Regra operacional:

A UI atual/canonica permanece como caminho principal ate que a matriz global esteja completa e validada.

---

## Referencia inventario inicial de arquivos reais da UI

Data: 2026-07-03 16:11:04 -0300

Foi criado o inventario inicial de arquivos reais relacionados a UI:

    docs/INVENTARIO_ARQUIVOS_UI.md

Este inventario deve ser usado para preencher a matriz global de equivalencia da UI com base em arquivos concretos do repositorio.

Regra operacional:

Nenhum arquivo identificado como possivel entrypoint deve ser alterado sem auditoria propria e plano de rollback.

---

## Referencia classificacao inicial dos arquivos UI por area

Data: 2026-07-03 16:29:46 -0300

Foi criada a classificacao inicial dos arquivos candidatos de UI por area:

    docs/CLASSIFICACAO_AREAS_UI.md

Esta classificacao complementa o inventario inicial e deve orientar o preenchimento da matriz global de equivalencia.

Regra operacional:

Arquivos classificados como possiveis entrypoints, banco, dados, services, repositories ou pipeline permanecem preservados ate auditoria propria.
