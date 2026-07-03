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

---

## 42. Reset do estado de status ao limpar selecao de decisoes dark

### 42.1. Objetivo

Corrigir pendencia tecnica registrada na secao 40.11, garantindo que o estado interno de status da selecao seja limpo sempre que a selecao de decisao for resetada.

### 42.2. Arquivo alterado

Arquivo alterado nesta rodada:

- UI/components/decisions_dark_panel.py

### 42.3. Implementacao realizada

Foi criado helper local para centralizar a limpeza de selecao:

- _clear_selection

Responsabilidades do helper:

- limpar selected_index;
- limpar _last_decision_status_text;
- evitar que o cache de status preserve texto antigo apos a selecao ser resetada.

Os pontos diretos de limpeza de selecao foram substituidos por chamada centralizada ao helper.

### 42.4. Restricoes preservadas

A alteracao nao modifica:

- layout funcional;
- banco de dados;
- repositories;
- services;
- controllers;
- contratos canonicos;
- regra de negocio;
- entrypoint principal;
- UI atual.

O modo dark permanece como UI moderna paralela.

### 42.5. Validacoes obrigatorias

Validacoes previstas para esta rodada:

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

### 42.6. Resultado esperado

Resultado esperado:

- selecao limpa corretamente;
- cache de status tambem e limpo;
- status continua sem duplicacao consecutiva;
- detalhe permanece funcional;
- copia de detalhe permanece funcional;
- carregamento de estrutura no Terminal VWAP permanece funcional.

---

## 43. Mapa de equivalencia atual da aba Decisoes dark

### 43.1. Objetivo

Registrar o estado atual da equivalencia parcial da aba Decisoes no modo dark apos as rodadas de filtros, detalhe, copia, exportacao, carregamento de estrutura e estabilizacao de selecao/status.

### 43.2. Recursos ja cobertos no modo dark

Recursos atualmente cobertos na UI moderna dark:

- listagem global de decisoes;
- carregamento de decisoes a partir do data model existente;
- filtros simples de baixo risco;
- selecao de decisao na tabela/listagem;
- painel de detalhe enriquecido da decisao selecionada;
- protecao contra detalhe sem selecao valida;
- copia do detalhe da decisao para a area de transferencia;
- exportacao CSV respeitando a listagem filtrada;
- carregamento da estrutura associada no Terminal VWAP;
- deduplicacao de mensagens consecutivas de status de selecao;
- limpeza consistente de selecao e cache interno de status.

### 43.3. Restricoes preservadas

As rodadas recentes preservaram:

- UI atual como caminho principal;
- modo dark como UI moderna paralela;
- entrypoint principal existente;
- contratos canonicos;
- repositories;
- services;
- controllers;
- banco de dados;
- regra de negocio.

### 43.4. Equivalencia parcial consolidada

A aba Decisoes no modo dark atingiu equivalencia parcial operacional para consulta, filtro simples, leitura, copia, exportacao e acionamento da estrutura associada.

Esta equivalencia ainda nao significa substituicao da UI atual.

### 43.5. Pendencias candidatas para proximas frentes

Pendencias candidatas, a serem tratadas apenas em frentes pequenas e isoladas:

- revisar filtros avancados ainda nao implementados;
- avaliar ordenacao visual da listagem;
- revisar estados vazios e mensagens auxiliares;
- avaliar indicadores de contagem filtrada versus total;
- revisar ergonomia dos botoes de acao;
- confirmar se ha diferencas relevantes em relacao a UI atual.

### 43.6. Proxima direcao recomendada

A proxima frente funcional recomendada deve ser pequena e de baixo risco.

Candidata preferencial:

- adicionar indicador textual de contagem filtrada versus total na aba Decisoes dark.

Objetivo da candidata:

- melhorar feedback operacional dos filtros;
- nao alterar regra de negocio;
- nao alterar repositories, services ou controllers;
- manter escopo restrito a UI/components/decisions_dark_panel.py.

---

## 44. Robustez de acoes sem selecao na aba Decisoes dark

### 44.1. Objetivo

Reforcar a robustez das acoes dependentes de selecao na aba Decisoes do modo dark, evitando comparacoes invalidas quando o indice selecionado estiver ausente ou inconsistente.

### 44.2. Arquivo alterado

Arquivo alterado:

- UI/components/decisions_dark_panel.py

### 44.3. Implementacao realizada

Foi criado um helper interno para validar o indice atualmente selecionado:

- retorna o indice quando ele e inteiro e esta dentro dos limites da lista filtrada;
- retorna vazio quando nao ha selecao valida.

O helper passou a ser usado em:

- atualizacao do estado do botao de copia de detalhe;
- acao de copiar detalhe da decisao selecionada.

### 44.4. Ganho operacional

A aba Decisoes dark passa a tolerar melhor estados transitorios de UI, como:

- selecao limpa;
- filtro aplicado apos uma selecao anterior;
- lista filtrada vazia;
- acionamento defensivo de comando sem selecao valida.

### 44.5. Restricoes preservadas

A frente preservou:

- regra de negocio;
- contratos canonicos;
- repositories;
- services;
- controllers;
- banco de dados;
- entrypoint principal;
- UI atual como caminho principal;
- modo dark como UI moderna paralela.

### 44.6. Validacoes obrigatorias

Validacoes recomendadas:

- compilar UI/components/decisions_dark_panel.py;
- executar git diff --check;
- abrir UI moderna dark;
- abrir aba Decisoes;
- aplicar filtros com e sem resultado;
- tentar copiar detalhe com selecao valida;
- confirmar que copia sem selecao valida nao quebra a UI.

### 44.7. Resultado esperado

Resultado esperado:

- copia de detalhe permanece funcional com selecao valida;
- estado sem selecao passa a ser tratado de forma defensiva;
- filtros e detalhe permanecem operacionais;
- nenhum contrato externo e alterado.

---

## 45. Consolidacao do feedback de filtros na aba Decisoes dark

### 45.1. Objetivo

Reduzir ruido operacional no status da UI moderna dark ao aplicar filtros na aba Decisoes, evitando repeticao consecutiva da mesma mensagem de filtro.

### 45.2. Arquivo alterado

Arquivo alterado:

- UI/components/decisions_dark_panel.py

### 45.3. Implementacao realizada

Foi adicionado um estado interno especifico para mensagens de filtro:

- `_last_filter_status_text`

Tambem foi criado um helper dedicado:

- `_status_filter_result`

Esse helper centraliza o envio de mensagens relacionadas a filtro e evita repetir consecutivamente o mesmo texto.

### 45.4. Separacao preservada entre selecao e filtro

A frente manteve separados os fluxos de status:

- `_status_selected_decision` continua dedicado a mensagens de selecao de decisao;
- `_status_filter_result` passa a tratar mensagens de filtro, erro de filtro e ausencia de resultados.

Essa separacao evita misturar dedupe de selecao com dedupe de filtros.

### 45.5. Casos cobertos

Passaram a usar o helper de feedback de filtro:

- filtro invalido por campo numerico incorreto;
- filtro sem resultados em decisoes de estruturas ativas;
- ausencia de decisao de estrutura ativa;
- resumo de decisoes exibidas apos reload com filtro aplicado;
- filtro sem resultados apos reload.

### 45.6. Restricoes preservadas

A frente preservou:

- regra de negocio;
- contratos canonicos;
- repositories;
- services;
- controllers;
- banco de dados;
- entrypoint principal;
- UI atual como caminho principal;
- modo dark como UI moderna paralela.

### 45.7. Validacoes obrigatorias

Validacoes recomendadas:

- compilar UI/components/decisions_dark_panel.py;
- executar git diff --check;
- abrir UI moderna dark;
- abrir aba Decisoes;
- aplicar filtro sem resultado mais de uma vez;
- confirmar que mensagens repetidas nao poluem o status;
- aplicar filtro invalido;
- limpar filtros;
- selecionar decisao;
- copiar detalhe;
- carregar estrutura no Terminal VWAP.

### 45.8. Resultado esperado

Resultado esperado:

- mensagens consecutivas identicas de filtro deixam de ser repetidas;
- mensagens de selecao continuam funcionando;
- resumo visual de filtros permanece preservado;
- filtros, detalhe, copia, exportacao e carregamento de estrutura continuam operacionais.

---

## 46. Separacao entre selecao automatica e selecao manual na aba Decisoes dark

### 46.1. Objetivo

Reduzir ruido de status na aba Decisoes da UI moderna dark ao diferenciar selecoes automaticas feitas pela propria tela de selecoes manuais feitas pelo usuario.

### 46.2. Arquivo alterado

Arquivo alterado:

- UI/components/decisions_dark_panel.py

### 46.3. Implementacao realizada

A rotina de selecao de decisao passou a aceitar um parametro opcional:

- `notify_status`

Quando esse parametro esta desabilitado, a decisao continua sendo selecionada internamente, com atualizacao de detalhe e botoes, mas sem emitir mensagem de status de selecao.

### 46.4. Selecoes automaticas ajustadas

Passaram a usar selecao silenciosa:

- selecao da primeira decisao apos reload;
- selecao da primeira decisao apos aplicacao de filtro com resultado.

Isso evita repeticoes como mensagens consecutivas de decisao selecionada quando a propria UI apenas esta mantendo uma selecao valida.

### 46.5. Selecao manual preservada

A selecao acionada pelo usuario na lista continua usando o comportamento padrao:

- atualiza detalhe;
- habilita acoes relacionadas;
- emite status de decisao selecionada.

### 46.6. Feedback de filtro com resultado

Foi adicionado um helper para identificar filtros ativos:

- `_has_active_filters`

Com isso, filtros com resultado passam a emitir status de filtro, sem depender de uma mensagem indireta de selecao automatica.

### 46.7. Restricoes preservadas

A frente preservou:

- regra de negocio;
- contratos canonicos;
- repositories;
- services;
- controllers;
- banco de dados;
- entrypoint principal;
- UI atual como caminho principal;
- modo dark como UI moderna paralela.

### 46.8. Validacoes obrigatorias

Validacoes recomendadas:

- compilar UI/components/decisions_dark_panel.py;
- executar git diff --check;
- abrir UI moderna dark;
- abrir aba Decisoes;
- recarregar dados;
- aplicar filtro com resultado;
- aplicar filtro sem resultado;
- limpar filtros;
- selecionar manualmente uma decisao;
- copiar detalhe;
- carregar estrutura no Terminal VWAP.

### 46.9. Resultado esperado

Resultado esperado:

- reload e filtros deixam de repetir status de decisao selecionada por selecao automatica;
- selecao manual continua informando a decisao selecionada;
- filtros com resultado informam quantidade exibida;
- detalhe, copia, exportacao e carregamento de estrutura continuam operacionais.

---

## 47. Silenciamento de filtro limpo em estado neutro na aba Decisoes dark

### 47.1. Objetivo

Evitar ruido de status na aba Decisoes da UI moderna dark quando a tela esta apenas renderizando em estado neutro, sem filtros ativos.

### 47.2. Arquivo alterado

Arquivo alterado:

- UI/components/decisions_dark_panel.py

### 47.3. Implementacao realizada

A rotina de aplicacao de filtro passou a aceitar um parametro opcional:

- `announce_clear`

Esse parametro controla se a mensagem de filtros limpos deve ser emitida quando nao existem filtros ativos.

### 47.4. Comportamento ajustado

A mensagem:

- `Filtros limpos: X decisões de estruturas ativas`

passa a ser emitida apenas em acoes explicitas de limpeza, como:

- limpar busca;
- limpar filtros avancados.

### 47.5. Estado neutro preservado

Quando a tela apenas carrega, recarrega ou re-renderiza sem filtros ativos, a UI deixa de emitir a mensagem de filtros limpos.

Isso reduz ruido operacional apos reload e evita status redundante logo depois da mensagem de decisoes carregadas.

### 47.6. Comportamentos preservados

Foram preservados:

- filtro aplicado com resultado;
- filtro sem resultado;
- filtro invalido;
- selecao automatica silenciosa;
- selecao manual com status;
- detalhe da decisao;
- copia de detalhe;
- carregamento de estrutura no Terminal VWAP.

### 47.7. Restricoes preservadas

A frente preservou:

- regra de negocio;
- contratos canonicos;
- repositories;
- services;
- controllers;
- banco de dados;
- entrypoint principal;
- UI atual como caminho principal;
- modo dark como UI moderna paralela.

### 47.8. Validacoes obrigatorias

Validacoes recomendadas:

- compilar UI/components/decisions_dark_panel.py;
- executar git diff --check;
- abrir UI moderna dark;
- abrir aba Decisoes;
- confirmar que o carregamento inicial nao mostra filtros limpos;
- aplicar filtro com resultado;
- limpar filtros pelo botao;
- confirmar que a limpeza explicita informa filtros limpos;
- aplicar filtro sem resultado;
- aplicar filtro invalido;
- selecionar manualmente decisao;
- copiar detalhe;
- carregar estrutura no Terminal VWAP.

### 47.9. Resultado esperado

Resultado esperado:

- estado neutro sem filtros nao polui o status;
- limpeza explicita continua comunicada;
- feedback de filtros permanece rastreavel;
- operacoes da aba Decisoes dark continuam funcionais.

---

## 48. Correcao do anuncio explicito de limpeza de filtros na aba Decisoes dark

### 48.1. Objetivo

Corrigir a separacao entre mudanca normal de filtro e acao explicita de limpeza na aba Decisoes da UI moderna dark.

### 48.2. Arquivo alterado

Arquivo alterado:

- UI/components/decisions_dark_panel.py

### 48.3. Ajuste realizado

A rotina de alteracao textual da busca voltou a aplicar filtro sem anunciar limpeza:

- `_on_search_changed`

A rotina de limpeza explicita dos filtros avancados passou a anunciar limpeza:

- `_clear_advanced_filters`

### 48.4. Comportamento esperado

Com o ajuste:

- digitar ou alterar busca apenas aplica filtro;
- limpar busca pelo botao comunica filtros limpos;
- limpar filtros avancados pelo botao comunica filtros limpos;
- carregamento neutro permanece silencioso quanto a filtros limpos.

### 48.5. Motivo da correcao

A frente anterior introduziu corretamente o parametro `announce_clear`, mas o uso precisava ficar restrito a acoes explicitas de limpeza.

Isso evita que uma simples alteracao de texto na busca seja interpretada como limpeza completa de filtros.

### 48.6. Restricoes preservadas

A frente preservou:

- regra de negocio;
- contratos canonicos;
- repositories;
- services;
- controllers;
- banco de dados;
- entrypoint principal;
- UI atual como caminho principal;
- modo dark como UI moderna paralela.

### 48.7. Validacoes obrigatorias

Validacoes recomendadas:

- compilar UI/components/decisions_dark_panel.py;
- executar git diff --check;
- abrir UI moderna dark;
- abrir aba Decisoes;
- confirmar carregamento neutro sem mensagem de filtros limpos;
- digitar busca com resultado;
- limpar busca pelo botao;
- limpar filtros avancados pelo botao;
- aplicar filtro invalido;
- selecionar decisao manualmente;
- copiar detalhe;
- carregar estrutura no Terminal VWAP.

### 48.8. Resultado esperado

Resultado esperado:

- anuncio de filtros limpos fica restrito a limpeza explicita;
- busca textual continua responsiva;
- filtros avancados comunicam limpeza corretamente;
- status da aba Decisoes dark fica mais previsivel e menos ruidoso.

---

## 49. Clarificacao de filtro ativo sem reducao de resultados na aba Decisoes dark

### 49.1. Objetivo

Melhorar a clareza operacional do status de filtros na aba Decisoes da UI moderna dark quando existe filtro ativo, mas ele nao reduz a quantidade de decisoes exibidas.

### 49.2. Arquivo alterado

Arquivo alterado:

- UI/components/decisions_dark_panel.py

### 49.3. Ajuste realizado

O feedback de filtro aplicado passou a diferenciar dois cenarios:

- filtro ativo que reduz a lista;
- filtro ativo que mantem todas as decisoes de estruturas ativas visiveis.

### 49.4. Comportamento anterior

Antes do ajuste, um filtro ativo que retornava todos os itens emitia mensagem no mesmo formato de um filtro realmente restritivo:

- `Filtro aplicado: 8 de 8 decisões de estruturas ativas`

Embora correta, a mensagem nao deixava claro que o filtro nao reduziu a lista.

### 49.5. Comportamento novo

Quando o filtro ativo nao reduz os resultados, a mensagem passa a ser:

- `Filtro aplicado sem reduzir resultados: X decisões de estruturas ativas`

Quando o filtro reduz resultados, permanece:

- `Filtro aplicado: X de Y decisões de estruturas ativas`

### 49.6. Comportamentos preservados

Foram preservados:

- filtro com reducao de resultados;
- filtro sem resultados;
- filtro invalido;
- limpeza explicita de filtros;
- estado neutro silencioso quanto a filtros limpos;
- selecao automatica silenciosa;
- selecao manual com status;
- copia de detalhe;
- carregamento de estrutura no Terminal VWAP.

### 49.7. Restricoes preservadas

A frente preservou:

- regra de negocio;
- contratos canonicos;
- repositories;
- services;
- controllers;
- banco de dados;
- entrypoint principal;
- UI atual como caminho principal;
- modo dark como UI moderna paralela.

### 49.8. Validacoes obrigatorias

Validacoes recomendadas:

- compilar UI/components/decisions_dark_panel.py;
- executar git diff --check;
- abrir UI moderna dark;
- abrir aba Decisoes;
- aplicar filtro que reduza resultados;
- aplicar filtro ativo que mantenha todos os resultados;
- aplicar filtro sem resultado;
- limpar filtros explicitamente;
- selecionar decisao manualmente;
- copiar detalhe;
- carregar estrutura no Terminal VWAP.

### 49.9. Resultado esperado

Resultado esperado:

- filtros restritivos continuam indicando X de Y decisoes;
- filtros nao restritivos passam a indicar que nao houve reducao;
- status da aba Decisoes dark fica mais informativo;
- operacoes da aba permanecem funcionais.

---

## 50. Centralizacao do status de resultado de filtros na aba Decisoes dark

### 50.1. Objetivo

Melhorar a organizacao interna da aba Decisoes da UI moderna dark centralizando a montagem do status de resultado de filtros em um metodo dedicado.

### 50.2. Arquivo alterado

Arquivo alterado:

- UI/components/decisions_dark_panel.py

### 50.3. Ajuste realizado

Foi criado o metodo:

- `_status_filter_summary`

Esse metodo concentra a decisao de qual mensagem emitir apos aplicacao de filtros com resultado.

### 50.4. Comportamentos preservados

Foram preservadas as mensagens para:

- filtro aplicado com reducao de resultados;
- filtro aplicado sem reducao de resultados;
- limpeza explicita de filtros;
- estado neutro silencioso quanto a filtros limpos.

### 50.5. Reducao de complexidade local

A rotina `_apply_filter` deixou de conter diretamente o bloco aninhado de decisao de status para filtros com resultado.

Com isso, `_apply_filter` permanece focada em:

- ler filtros;
- validar filtros numericos;
- montar lista filtrada;
- renderizar linhas;
- selecionar automaticamente quando aplicavel;
- delegar o feedback consolidado.

### 50.6. Escopo preservado

A frente nao altera:

- regra de negocio;
- repositories;
- services;
- controllers;
- banco de dados;
- contratos canonicos;
- entrypoint principal;
- UI atual como caminho principal.

### 50.7. Validacoes obrigatorias

Validacoes recomendadas:

- compilar UI/components/decisions_dark_panel.py;
- executar git diff --check;
- abrir UI moderna dark;
- abrir aba Decisoes;
- aplicar filtro que reduza resultados;
- aplicar filtro que nao reduza resultados;
- aplicar filtro sem resultado;
- limpar filtros explicitamente;
- selecionar decisao manualmente;
- copiar detalhe;
- carregar estrutura no Terminal VWAP.

### 50.8. Resultado esperado

Resultado esperado:

- comportamento visual inalterado;
- status de filtros preservado;
- codigo mais legivel;
- decisao de status concentrada em metodo dedicado.

---

## 51. Centralizacao do rotulo de decisoes ativas na aba Decisoes dark

### 51.1. Objetivo

Melhorar a manutencao dos textos de status da aba Decisoes da UI moderna dark centralizando o rotulo de contagem de decisoes de estruturas ativas.

### 51.2. Arquivo alterado

Arquivo alterado:

- UI/components/decisions_dark_panel.py

### 51.3. Ajuste realizado

Foi criado o metodo:

- `_active_decisions_label`

Esse metodo retorna o texto padronizado usado nas mensagens de status relacionadas a filtros:

- `X decisões de estruturas ativas`

### 51.4. Comportamento preservado

Foram preservadas as mensagens funcionais para:

- filtro aplicado com reducao;
- filtro aplicado sem reducao;
- limpeza explicita de filtros.

### 51.5. Motivo da mudanca

Antes do ajuste, o trecho `decisões de estruturas ativas` aparecia repetido dentro da montagem do status de filtros.

A centralizacao reduz duplicidade e facilita ajustes futuros de texto sem alterar a regra de filtragem.

### 51.6. Escopo preservado

A frente nao altera:

- regra de negocio;
- filtros;
- selecao automatica;
- selecao manual;
- repositories;
- services;
- controllers;
- banco de dados;
- contratos canonicos;
- entrypoint principal;
- UI atual como caminho principal.

### 51.7. Validacoes obrigatorias

Validacoes recomendadas:

- compilar UI/components/decisions_dark_panel.py;
- executar git diff --check;
- abrir UI moderna dark;
- abrir aba Decisoes;
- aplicar filtro que reduza resultados;
- aplicar filtro que nao reduza resultados;
- limpar filtros explicitamente;
- selecionar decisao manualmente;
- copiar detalhe;
- carregar estrutura no Terminal VWAP.

### 51.8. Resultado esperado

Resultado esperado:

- comportamento visual inalterado;
- mensagens de status preservadas;
- texto de contagem de decisoes ativas centralizado;
- codigo mais facil de manter.

## Frente 53 — refactor agressivo interno da aba Decisões dark

Bloco maior aplicado na branch refactor/decisions-dark-panel-large-block.

Escopo:

- criação de estado explícito para filtros da aba Decisões dark;
- decomposição do pipeline de filtragem em helpers dedicados;
- redução da responsabilidade direta de _apply_filter;
- separação entre coleta de filtros, validação, filtragem e exibição de resultado vazio;
- preservação do comportamento visual e dos contratos externos da aba.

Arquivos impactados:

- UI/components/decisions_dark_panel.py
- AUDITORIA_REFACTOR_UI.md

Validação esperada:

    python -m py_compile UI/components/decisions_dark_panel.py
    git diff --check
    python -m UI.modern

Critério de aceite:

- aba Decisões dark carrega normalmente;
- filtros continuam funcionando;
- filtros numéricos inválidos exibem mensagem de erro;
- limpar filtros restaura a listagem esperada;
- seleção de decisão atualiza o detalhe;
- copiar detalhe continua funcionando;
- carregar estrutura continua funcionando;
- exportação CSV continua funcionando.

- DecisionsDarkPanel: busca unificada por decisão, ID e nome; limpeza consolidada em um único botão.

- DecisionsDarkPanel: _build_layout dividido em helpers privados de grade, cabeçalho, ações, busca, filtros, listagem e detalhe.

- DecisionsDarkPanel: seção de filtros dividida em helpers privados para controles de level, DTE, botões e resumo.
