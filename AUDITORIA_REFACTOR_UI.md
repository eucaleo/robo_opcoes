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
