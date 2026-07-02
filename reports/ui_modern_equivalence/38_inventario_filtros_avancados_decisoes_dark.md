# Frente 38 - Inventario de filtros avancados de decisoes no modo dark

## 1. Objetivo

Inventariar os filtros de decisoes necessarios para aproximar a aba Decisoes do modo dark da UI atual auditada.

Esta frente e documental e deve ocorrer antes de qualquer patch funcional.

## 2. Base de comparacao

A UI atual possui filtros e controles relacionados a decisoes:

- Periodo De/Ate
- Estrutura
- Decisao
- Level >=
- DTE <=
- Aplicar
- Limpar
- Indicador de filtros aplicados
- Tabela de decisoes
- Selecao de decisao
- Detalhe da decisao

## 3. Estado conhecido do modo dark

A aba Decisoes do modo dark ja possui evolucoes parciais:

- listagem global de decisoes
- selecao de decisao
- detalhe textual enriquecido
- copia do detalhe
- busca por estrutura ativa
- exportacao CSV da listagem filtrada
- carregamento da estrutura selecionada no Terminal VWAP

## 4. Lacunas a mapear

Devem ser mapeadas antes do patch:

- filtro por periodo inicial e final
- filtro por estrutura em controle dedicado
- filtro por decisao
- filtro por level minimo
- filtro por DTE maximo
- comportamento do botao Aplicar
- comportamento do botao Limpar
- indicador visual de filtros ativos
- interacao entre busca textual e filtros avancados
- impacto da exportacao CSV sobre a visao filtrada
- impacto da selecao de decisao apos filtragem

## 5. Arquivos candidatos para leitura

Arquivos a inspecionar:

- UI/components/decisions_dark_panel.py
- UI/modern/dark_window.py
- UI/modern/main_window.py
- UI/components/filters_panel.py
- UI/components/decisions_grid.py
- UI/components/details_panel.py

## 6. Restricoes

Esta frente nao deve alterar:

- codigo funcional
- layout operacional
- callbacks
- banco de dados
- services
- controllers
- repositories
- regra de negocio
- contratos canonicos
- entrypoint principal
- UI atual legada

## 7. Criterio de saida

A frente somente estara pronta para patch quando estiverem definidos:

- quais filtros existem na UI atual
- quais filtros ja existem no modo dark
- quais campos estao disponiveis nos registros de decisao
- quais filtros podem ser implementados sem alterar banco
- qual e o menor patch seguro
- quais validacoes manuais serao obrigatorias

## 8. Decisao

A proxima etapa autorizada e leitura e classificacao dos arquivos candidatos.

Nao iniciar patch funcional de filtros antes de concluir este inventario.
