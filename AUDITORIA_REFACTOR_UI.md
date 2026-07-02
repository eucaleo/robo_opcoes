\n## Frente 36 — Detalhe enriquecido da decisão no modo dark

Status: concluída
Data: 2026-07-02
Commit funcional: 7c66ead
Tag funcional: checkpoint-modern-decisions-detail-rich-dark
Relatório: reports/ui_modern_equivalence/36_decisions_detail_rich_dark.md

### Resumo

Foi enriquecida a apresentação do detalhe da decisão no painel dark de decisões.

A alteração ficou restrita a:

- UI/components/decisions_dark_panel.py

### Resultado

O painel passou a apresentar:

- resumo operacional;
- identificação da estrutura;
- status da estrutura;
- decisão;
- nível;
- timestamps;
- métricas principais;
- rationale / why;
- campos adicionais brutos.

### Validação

Executado com sucesso:

    python -m py_compile UI/components/decisions_dark_panel.py UI/modern/dark_window.py
    python -m UI.modern --info
    python -m UI.modern

Validação manual aprovada na UI moderna dark.\n

## 35. Exportacao CSV de decisoes filtradas no modo dark

Foi implementada e registrada a exportacao CSV da listagem filtrada de decisoes no modo dark.

### 35.1. Objetivo

Permitir que a visao atual da aba Decisoes no modo dark seja exportada para CSV, respeitando a listagem filtrada exibida ao usuario.

### 35.2. Resultado funcional

A UI moderna dark passou a oferecer exportacao CSV associada ao fluxo de decisoes.

A funcionalidade preserva o escopo da camada visual:

- nao altera banco;
- nao altera regra de negocio;
- nao altera services, controllers ou repositories;
- nao substitui a UI atual;
- nao troca o entrypoint principal.

### 35.3. Commits e tags associados

Commits associados:

- ad3c15f feat(ui): exporta csv de decisoes filtradas no modo dark
- 82e13fe docs(ui): registra exportacao csv de decisoes filtradas dark

Tags associadas:

- checkpoint-modern-decisions-filtered-csv-dark
- checkpoint-modern-decisions-filtered-csv-dark-audit

## 36. Detalhe enriquecido de decisao no modo dark

Foi implementado e registrado o detalhe enriquecido de decisao na aba Decisoes do modo dark.

### 36.1. Objetivo

Melhorar a leitura operacional da decisao selecionada, exibindo mais campos relevantes sem recriar regra de negocio na UI.

### 36.2. Resultado funcional

O detalhe da decisao no modo dark passou a apresentar informacoes mais completas da decisao selecionada, mantendo o fluxo paralelo da UI moderna.

A alteracao preserva:

- banco de dados;
- contratos canonicos;
- regra de negocio;
- services;
- controllers;
- repositories;
- UI atual como caminho principal.

### 36.3. Commits e tags associados

Commits associados:

- 7c66ead feat(ui): enriquece detalhe de decisao no modo dark
- 9aaa8fa docs(ui): registra detalhe enriquecido de decisoes dark

Tags associadas:

- checkpoint-modern-decisions-detail-rich-dark
- checkpoint-modern-decisions-detail-rich-dark-docs

## 37. Copia do detalhe de decisao no modo dark

Foi implementada e registrada a copia do detalhe da decisao no modo dark.

Relatorio gerado:

- reports/ui_modern_equivalence/37_decisions_copy_detail_dark.md

### 37.1. Objetivo

Permitir copiar o detalhe da decisao selecionada na aba Decisoes do modo dark, facilitando auditoria, suporte operacional e registro externo.

### 37.2. Resultado funcional

A aba Decisoes do modo dark passou a oferecer acao de copia do detalhe da decisao selecionada.

A entrega complementa as frentes anteriores de:

- listagem global de decisoes;
- busca por estrutura ativa;
- carregamento da estrutura no Terminal VWAP;
- exportacao CSV;
- detalhe enriquecido.

### 37.3. Restricoes preservadas

A alteracao nao modifica:

- banco;
- schema;
- regra de negocio;
- services;
- controllers;
- repositories;
- contratos canonicos;
- entrypoint principal;
- UI atual legada.

### 37.4. Commits e tags associados

Commits associados:

- fb857d3 feat(ui): copia detalhe de decisao no modo dark
- 4d61c43 docs(ui): registra copia de detalhe de decisao dark

Tags associadas:

- checkpoint-modern-decisions-copy-detail-dark
- checkpoint-modern-decisions-copy-detail-dark-docs

## 38. Inventario de filtros avancados de decisoes no modo dark

Foi aberta a proxima frente documental da equivalencia funcional de decisoes no modo dark.

Relatorio gerado:

- reports/ui_modern_equivalence/38_inventario_filtros_avancados_decisoes_dark.md

### 38.1. Objetivo

Inventariar os filtros avancados de decisoes antes de qualquer patch funcional.

A comparacao deve considerar os filtros da UI atual:

- Periodo De/Ate;
- Estrutura;
- Decisao;
- Level >=;
- DTE <=;
- Aplicar;
- Limpar;
- indicador de filtros aplicados.

### 38.2. Estado atual considerado

O modo dark ja possui evolucoes parciais importantes no fluxo de decisoes:

- listagem global;
- selecao;
- detalhe enriquecido;
- copia do detalhe;
- busca por estrutura ativa;
- exportacao CSV filtrada;
- carregamento da estrutura no Terminal VWAP.

Ainda falta classificar a equivalencia dos filtros avancados da UI atual.

### 38.3. Decisao de seguranca

Esta frente e documental.

Nao deve alterar:

- codigo funcional;
- layout operacional;
- callbacks;
- banco;
- regra de negocio;
- services;
- controllers;
- repositories;
- contratos canonicos;
- entrypoint principal;
- UI atual legada.

### 38.4. Proximo passo

Ler os arquivos candidatos, classificar campos disponiveis e definir o menor patch seguro para filtros avancados de decisoes no modo dark.

## 39. Classificacao tecnica dos filtros avancados de decisoes no modo dark

Foi criada a classificacao tecnica dos filtros avancados de decisoes no modo dark.

Relatorio gerado:

- reports/ui_modern_equivalence/39_classificacao_filtros_avancados_decisoes_dark.md

### 39.1. Objetivo

Ler os arquivos candidatos da frente 38 e classificar o menor caminho seguro para filtros avancados na aba Decisoes do modo dark.

### 39.2. Arquivos considerados

Foram considerados os seguintes arquivos:

- UI/components/decisions_dark_panel.py
- UI/modern/dark_window.py
- UI/modern/main_window.py
- UI/components/filters_panel.py
- UI/components/decisions_grid.py
- UI/components/details_panel.py

### 39.3. Decisao tecnica preliminar

A proxima implementacao deve preferir filtragem em memoria sobre as decisoes ja carregadas por UIDataModel.get_decisions(), desde que os campos necessarios estejam disponiveis.

Filtros candidatos de menor risco:

- decisao;
- level minimo;
- DTE maximo;
- estrutura usando indice ja existente;
- limpar filtros;
- indicador textual de quantidade filtrada.

Filtro que exige cuidado adicional:

- periodo De/Ate, por depender da padronizacao do campo de data ou timestamp.

### 39.4. Restricoes preservadas

A classificacao nao altera:

- codigo funcional;
- layout operacional;
- callbacks;
- banco;
- schema;
- services;
- controllers;
- repositories;
- regra de negocio;
- contratos canonicos;
- entrypoint principal;
- UI atual legada.

### 39.5. Proximo passo

Revisar o relatorio tecnico e, se confirmado, abrir patch funcional minimo para filtros simples na aba Decisoes dark.

---

## 40. Filtros simples e estabilizacao da selecao de decisoes no modo dark

### 40.1. Objetivo

Avancar a equivalencia parcial da aba Decisoes no modo dark, adicionando filtros simples e corrigindo problemas operacionais de selecao, detalhe e mensagens de status.

Esta rodada continua a evolucao iniciada nas secoes anteriores sobre:

- listagem global de decisoes;
- selecao de decisao;
- detalhe textual;
- carregamento da estrutura da decisao no Terminal VWAP;
- busca por estrutura ativa.

### 40.2. Restricoes preservadas

As alteracoes desta rodada preservaram as restricoes arquiteturais do projeto:

- a UI atual nao foi eliminada;
- o modo dark permanece como UI moderna paralela;
- nao houve migracao para web;
- nao houve alteracao de banco;
- nao houve sincronismo continuo entre derived.db e app.db;
- nao houve recriacao de regra de negocio na UI;
- nao houve alteracao em repositories, services ou controllers;
- os contratos canonicos foram preservados.

### 40.3. Inventario e classificacao de filtros avancados

Antes da implementacao dos filtros simples, foram registradas etapas documentais de inventario e classificacao dos filtros avancados de decisoes no modo dark.

Commits associados:

- b5ec20c docs(ui): abre inventario de filtros avancados de decisoes dark
- d23f8ef docs(ui): classifica filtros avancados de decisoes dark

Tags associadas:

- checkpoint-modern-decisions-advanced-filters-dark-inventory
- checkpoint-modern-decisions-advanced-filters-dark-classification

Decisao registrada:

- filtros avancados completos nao deveriam ser implementados de uma vez;
- a proxima entrega funcional deveria ser pequena;
- o primeiro passo funcional seria adicionar filtros simples de baixo risco.

### 40.4. Implementacao de filtros simples

Foi implementada evolucao funcional no componente:

- UI/components/decisions_dark_panel.py

Funcionalidades adicionadas ou estabilizadas:

- filtro textual por estrutura ativa;
- filtro por decisao;
- filtro numerico minimo por level;
- filtro numerico maximo por DTE;
- limpeza dos filtros;
- preservacao da listagem filtrada;
- selecao operando sobre filtered_decisions;
- detalhe textual sincronizado com a decisao filtrada;
- botao de carregar estrutura preservado no fluxo filtrado.

Commit associado:

- a137c1e feat(ui): adiciona filtros simples em decisoes dark

Tag associada:

- checkpoint-modern-decisions-simple-filters-dark

### 40.5. Correcao de detalhe sem selecao

Foi corrigido comportamento no qual o painel de detalhe poderia ser acessado em situacao sem selecao valida.

A correcao tornou o fluxo mais defensivo em relacao a:

- selected_index ausente;
- selected_index fora da faixa;
- lista filtrada vazia;
- tentativa de copiar detalhe sem decisao valida.

Commit associado:

- 2ce94a6 fix(ui): corrige detalhe de decisao sem selecao

Tag associada:

- checkpoint-modern-decisions-simple-filters-dark-selection-fix

### 40.6. Dedupe de status de selecao

Foi corrigido excesso de mensagens repetidas de status quando a mesma decisao era selecionada repetidamente.

Problema observado:

- a UI registrava status repetido para a mesma selecao;
- isso gerava ruido no console operacional;
- a mensagem de selecao deveria ser emitida apenas quando o texto de status mudasse.

Correcao aplicada:

- criado controle interno para evitar emissao duplicada consecutiva do mesmo status de selecao.

Commit associado:

- 436b168 fix(ui): evita status duplicado em decisoes dark

Tag associada:

- checkpoint-modern-decisions-dark-dedupe-selection-status

### 40.7. Centralizacao do status de selecao

Foi aplicada refatoracao pequena para centralizar o controle de status de selecao em helper dedicado.

Arquivo alterado:

- UI/components/decisions_dark_panel.py

Helper criado:

- _status_selected_decision

Objetivo:

- reduzir duplicacao;
- concentrar a regra de dedupe;
- manter _select_decision mais legivel;
- facilitar manutencao futura.

Commit associado:

- 954585c refactor(ui): centraliza status de selecao em decisoes dark

Tag associada:

- checkpoint-modern-decisions-dark-selection-status-helper

### 40.8. Inicializacao explicita do estado de status

Foi inicializado explicitamente no construtor o estado interno usado para deduplicar status de selecao.

Estado adicionado:

- self._last_decision_status_text: Optional[str] = None

Motivo:

- evitar atributo implicito criado apenas durante o fluxo;
- tornar o estado do painel mais previsivel;
- reduzir risco de manutencao futura.

Commit associado:

- d4ab1be refactor(ui): inicializa status de selecao em decisoes dark

Tag associada:

- checkpoint-modern-decisions-dark-selection-status-state

### 40.9. Validacoes executadas

Validacoes executadas ao longo da rodada:

- python -m py_compile UI/components/decisions_dark_panel.py
- git diff --check
- git diff --cached --check
- python -m UI.modern

Resultados observados:

- UI moderna abriu em modo dark;
- estruturas reais foram carregadas;
- decisoes foram carregadas no modo dark;
- filtros simples permaneceram funcionais;
- selecao de decisoes funcionou;
- detalhe da decisao foi atualizado;
- copia do detalhe funcionou;
- carregamento de estrutura a partir da decisao funcionou;
- Terminal VWAP recebeu a estrutura carregada;
- mensagens duplicadas consecutivas de mesma selecao foram evitadas.

### 40.10. Estado atual apos a rodada

Checkpoint atual da main:

- d4ab1be refactor(ui): inicializa status de selecao em decisoes dark

Tag atual:

- checkpoint-modern-decisions-dark-selection-status-state

A aba Decisoes do modo dark possui agora equivalencia parcial mais robusta:

- listagem global;
- filtros simples;
- selecao;
- detalhe;
- copia de detalhe;
- carregamento da estrutura no Terminal VWAP;
- controle de status sem repeticao consecutiva.

### 40.11. Pendencia tecnica identificada

Foi identificada uma pendencia pequena de robustez:

- quando a selecao e limpa com selected_index = None, o cache _last_decision_status_text permanece com o ultimo texto.

Risco:

- baixo;
- nao quebra o fluxo atual;
- mas deixa estado antigo preservado apos limpeza da selecao.

Proxima correcao recomendada:

- centralizar a limpeza de selecao em helper;
- ao limpar selected_index, tambem limpar _last_decision_status_text;
- aplicar apenas em UI/components/decisions_dark_panel.py;
- validar com py_compile e python -m UI.modern.

## 41. Rota alinhada para a proxima frente

### 41.1. Proxima frente recomendada

Frente recomendada:

- resetar estado de status quando a selecao de decisao for limpa.

Escopo permitido:

- UI/components/decisions_dark_panel.py

Objetivo:

- substituir pontos diretos de selected_index = None por helper local;
- garantir que _last_decision_status_text tambem seja limpo;
- preservar comportamento visual e funcional atual.

### 41.2. Restricoes da proxima frente

A proxima frente nao deve:

- alterar banco;
- alterar repositories;
- alterar services;
- alterar controllers;
- alterar contratos canonicos;
- recriar regra de negocio na UI;
- alterar layout funcional;
- trocar entrypoint;
- eliminar UI atual.

### 41.3. Validacoes obrigatorias da proxima frente

Validacoes obrigatorias:

- python -m py_compile UI/components/decisions_dark_panel.py
- git diff --check
- python -m UI.modern

Validacao manual minima:

- abrir aba Decisoes;
- selecionar decisao;
- aplicar filtro sem resultado;
- limpar filtro;
- selecionar decisao novamente;
- copiar detalhe;
- carregar estrutura no Terminal VWAP.

Resultado esperado:

- nenhuma regressao;
- selecao limpa corretamente;
- status continua sem duplicacao consecutiva;
- carregamento de estrutura permanece funcional.
