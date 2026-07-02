# Mapa de equivalência funcional da UI moderna

Data de referência: 2026-07-02

Objetivo:

- comparar as funções obrigatórias preservadas pela auditoria visual com a implementação atual em UI.modern;
- identificar o que já possui evidência textual;
- separar presença textual de equivalência funcional validada;
- impedir avanço de layout sem mapa de cobertura.

Observação importante:

- este relatório não declara equivalência funcional final;
- evidência por busca textual é apenas indício;
- cada item marcado como parcial ainda exige validação manual e/ou teste.

## Tabela de equivalência

| Função obrigatória | Evidência em UI.modern | Status sugerido | Destino no novo layout |
|---|---|---|---|
| Filtros de decisões | UI/modern/main_window.py: filtro, filtros, decisão, aplicar, limpar | PENDENTE - evidência apenas no shell temporário ou sem confirmação no dark | Preservar ou realocar no painel lateral/superior do layout moderno. |
| Seleção de decisões | UI/modern/main_window.py: decisão, selecion | PENDENTE - evidência apenas no shell temporário ou sem confirmação no dark | Preservar seleção operacional para detalhamento e análise. |
| Detalhamento de decisão | UI/modern/main_window.py: detalhes, detail, decisão | PENDENTE - evidência apenas no shell temporário ou sem confirmação no dark | Realocar para painel de análise ou painel lateral contextual. |
| Recalcular estrutura | UI/modern/main_window.py: recalculate | PENDENTE - evidência apenas no shell temporário ou sem confirmação no dark | Preservar como ação operacional explícita. |
| Curva de Payoff | UI/modern/main_window.py: payoff, curve, curva, payoff_curve_points; UI/modern/dark_window.py: payoff | PARCIAL - evidência no modo dark; requer validação manual | Preservar no bloco principal de Payoff. |
| Comparação Curva A | sem ocorrência textual nos arquivos modernos analisados | PENDENTE - não evidenciado em UI.modern | Preservar ou documentar substituto funcional. |
| Exportação PNG | UI/modern/app.py: arquivo; UI/modern/main_window.py: exportar, arquivo | PENDENTE - evidência apenas no shell temporário ou sem confirmação no dark | Preservar como ação do bloco de Payoff. |
| CRUD de estruturas | UI/modern/theme.py: duplicar; UI/modern/main_window.py: estrutura, structures; UI/modern/dark_window.py: estrutura, structures | PARCIAL - evidência no modo dark; requer validação manual | Preservar no painel de estruturas. |
| Terminal VWAP Payoff | UI/modern/main_window.py: vwap, terminal, legs; UI/modern/dark_window.py: vwap, terminal | PARCIAL - evidência no modo dark; requer validação manual | Preservar como bloco/painel operacional. |
| Legs/pernas da estrutura | UI/modern/app.py: componentes; UI/modern/theme.py: componentes; UI/modern/main_window.py: legs, componentes, strike, position_side | PENDENTE - evidência apenas no shell temporário ou sem confirmação no dark | Preservar em rodapé ou painel dedicado. |
| Mensagens de status | UI/modern/theme.py: erro, error, warning; UI/modern/main_window.py: status, erro, error; UI/modern/dark_window.py: status, erro, error, warning | PARCIAL - evidência no modo dark; requer validação manual | Preservar em barra de status ou área de validação. |
| Banco e contratos canônicos | UI/modern/main_window.py: app.db, payoff_curve_points; UI/modern/dark_window.py: app.db | PARCIAL - evidência no modo dark; requer validação manual | Não mudar nesta fase. Apenas registrar uso atual. |

## Arquivos modernos analisados

- UI/modern/__main__.py - existe
- UI/modern/app.py - existe
- UI/modern/theme.py - existe
- UI/modern/main_window.py - existe
- UI/modern/dark_window.py - existe

## Próxima interpretação

- Itens sem evidência no modo dark devem ser tratados como pendentes.
- Itens com evidência apenas no shell não estão preservados no caminho preferencial.
- Itens com evidência no dark ainda são parciais até validação manual.
- A próxima alteração de código deve continuar pequena e limitada a tema/tokens visuais, sem alterar regra funcional.

# Evidências detalhadas por função

## Filtros de decisões

Status sugerido: PENDENTE - evidência apenas no shell temporário ou sem confirmação no dark

Destino previsto:

- Preservar ou realocar no painel lateral/superior do layout moderno.

Evidências:

- UI/modern/main_window.py: filtro, filtros, decisão, aplicar, limpar

## Seleção de decisões

Status sugerido: PENDENTE - evidência apenas no shell temporário ou sem confirmação no dark

Destino previsto:

- Preservar seleção operacional para detalhamento e análise.

Evidências:

- UI/modern/main_window.py: decisão, selecion

## Detalhamento de decisão

Status sugerido: PENDENTE - evidência apenas no shell temporário ou sem confirmação no dark

Destino previsto:

- Realocar para painel de análise ou painel lateral contextual.

Evidências:

- UI/modern/main_window.py: detalhes, detail, decisão

## Recalcular estrutura

Status sugerido: PENDENTE - evidência apenas no shell temporário ou sem confirmação no dark

Destino previsto:

- Preservar como ação operacional explícita.

Evidências:

- UI/modern/main_window.py: recalculate

## Curva de Payoff

Status sugerido: PARCIAL - evidência no modo dark; requer validação manual

Destino previsto:

- Preservar no bloco principal de Payoff.

Evidências:

- UI/modern/main_window.py: payoff, curve, curva, payoff_curve_points
- UI/modern/dark_window.py: payoff

## Comparação Curva A

Status sugerido: PENDENTE - não evidenciado em UI.modern

Destino previsto:

- Preservar ou documentar substituto funcional.

Evidências:

- Sem ocorrência textual nos arquivos modernos analisados.

## Exportação PNG

Status sugerido: PENDENTE - evidência apenas no shell temporário ou sem confirmação no dark

Destino previsto:

- Preservar como ação do bloco de Payoff.

Evidências:

- UI/modern/app.py: arquivo
- UI/modern/main_window.py: exportar, arquivo

## CRUD de estruturas

Status sugerido: PARCIAL - evidência no modo dark; requer validação manual

Destino previsto:

- Preservar no painel de estruturas.

Evidências:

- UI/modern/theme.py: duplicar
- UI/modern/main_window.py: estrutura, structures
- UI/modern/dark_window.py: estrutura, structures

## Terminal VWAP Payoff

Status sugerido: PARCIAL - evidência no modo dark; requer validação manual

Destino previsto:

- Preservar como bloco/painel operacional.

Evidências:

- UI/modern/main_window.py: vwap, terminal, legs
- UI/modern/dark_window.py: vwap, terminal

## Legs/pernas da estrutura

Status sugerido: PENDENTE - evidência apenas no shell temporário ou sem confirmação no dark

Destino previsto:

- Preservar em rodapé ou painel dedicado.

Evidências:

- UI/modern/app.py: componentes
- UI/modern/theme.py: componentes
- UI/modern/main_window.py: legs, componentes, strike, position_side

## Mensagens de status

Status sugerido: PARCIAL - evidência no modo dark; requer validação manual

Destino previsto:

- Preservar em barra de status ou área de validação.

Evidências:

- UI/modern/theme.py: erro, error, warning
- UI/modern/main_window.py: status, erro, error
- UI/modern/dark_window.py: status, erro, error, warning

## Banco e contratos canônicos

Status sugerido: PARCIAL - evidência no modo dark; requer validação manual

Destino previsto:

- Não mudar nesta fase. Apenas registrar uso atual.

Evidências:

- UI/modern/main_window.py: app.db, payoff_curve_points
- UI/modern/dark_window.py: app.db

