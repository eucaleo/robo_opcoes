# Frente 36 — Detalhe enriquecido da decisão no modo dark

Data: 2026-07-02
Commit funcional: 7c66ead
Tag funcional: checkpoint-modern-decisions-detail-rich-dark

## Objetivo

Enriquecer a apresentação do detalhe da decisão na UI moderna em modo dark, mantendo o escopo restrito ao componente visual de decisões.

## Arquivo alterado

- UI/components/decisions_dark_panel.py

## Escopo executado

A alteração concentrou-se exclusivamente na formatação do painel de detalhe da decisão, sem modificar:

- banco de dados;
- contratos derivados;
- queries;
- services;
- repositories;
- controllers;
- componentes principais da janela dark;
- regras de negócio.

## Melhorias implementadas

O detalhe textual da decisão passou a exibir seções mais claras:

- Resumo operacional;
- Estrutura com nome quando disponível;
- Status da estrutura;
- Decisão;
- Nível;
- Timestamp;
- Data de criação;
- Métricas principais;
- PL atual;
- PL máximo;
- PL percentual do máximo;
- DTE mínimo;
- Spot referência;
- Rationale;
- Rationale / why;
- Campos adicionais / raw.

Também foram adicionados helpers locais para melhorar a apresentação de:

- valores monetários;
- percentuais;
- números;
- valores alternativos entre chaves equivalentes;
- status da estrutura.

## Validações executadas

Foram executadas com sucesso:

    python -m py_compile UI/components/decisions_dark_panel.py UI/modern/dark_window.py
    python -m UI.modern --info
    python -m UI.modern

## Validação manual

Na UI moderna em modo dark foram validados:

- carregamento das estruturas;
- carregamento das decisões;
- seleção de decisões;
- exibição enriquecida do detalhe;
- troca entre decisões de estruturas diferentes;
- carregamento da estrutura a partir da decisão;
- recálculo de payoff;
- preservação do fluxo existente.

Logs observados:

    [ModernDarkUI] 4 estruturas carregadas
    [ModernDarkUI] 8 decisões carregadas no modo dark
    [ModernDarkUI] Decisão selecionada: estrutura=3, decisão=HOLD
    [ModernDarkUI] Decisão selecionada: estrutura=2, decisão=HOLD
    [ModernDarkUI] Estrutura carregada: ID 3
    [ModernDarkUI] Estrutura 3 carregada a partir da decisão
    [ModernDarkUI] Payoff recalculado: ID 3

## Resultado

A Frente 36 foi concluída com sucesso.

O modo dark agora possui detalhe de decisão mais informativo, legível e próximo do painel legado, sem alterar contratos, persistência ou lógica de negócio.
