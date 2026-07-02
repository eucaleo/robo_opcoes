# Classificacao das acoes laterais de estruturas no painel dark

Data de referencia: 2026-07-02

## Objetivo

Classificar as acoes laterais de estruturas da UI moderna dark quanto a presenca visual e existencia de callbacks.

## Escopo

- painel dark de VWAP e Payoff
- acoes laterais de estruturas
- verificacao de botoes, textos e callbacks
- comparacao entre caminho ativo UI e espelho ui

## Resultado resumido

- Recarregar estruturas: equivalente nos arquivos verificados
- Nova estrutura: equivalente nos arquivos verificados
- Selecionar estrutura: equivalente nos arquivos verificados
- Recalcular payoff: equivalente nos arquivos verificados
- Editar pernas: equivalente nos arquivos verificados
- Duplicar estrutura: equivalente nos arquivos verificados
- Arquivar estrutura: equivalente nos arquivos verificados
- Registrar decisao HOLD: equivalente nos arquivos verificados
- Abrir ajuste de estrutura: equivalente nos arquivos verificados
- Registrar decisao CLOSE: equivalente nos arquivos verificados
- Registrar decisao ADJUST: equivalente nos arquivos verificados
- Voltar para lista: equivalente nos arquivos verificados

## Detalhamento por acao

### Recarregar estruturas

- classificacao geral: equivalente nos arquivos verificados
- UI/components/terminal_vwap_payoff_dark_panel.py: callback existe sem evidencia visual direta
- ui/components/terminal_vwap_payoff_dark_panel.py: callback existe sem evidencia visual direta

### Nova estrutura

- classificacao geral: equivalente nos arquivos verificados
- UI/components/terminal_vwap_payoff_dark_panel.py: presente com callback
- ui/components/terminal_vwap_payoff_dark_panel.py: presente com callback

### Selecionar estrutura

- classificacao geral: equivalente nos arquivos verificados
- UI/components/terminal_vwap_payoff_dark_panel.py: presente com callback
- ui/components/terminal_vwap_payoff_dark_panel.py: presente com callback

### Recalcular payoff

- classificacao geral: equivalente nos arquivos verificados
- UI/components/terminal_vwap_payoff_dark_panel.py: presente com callback
- ui/components/terminal_vwap_payoff_dark_panel.py: presente com callback

### Editar pernas

- classificacao geral: equivalente nos arquivos verificados
- UI/components/terminal_vwap_payoff_dark_panel.py: presente com callback
- ui/components/terminal_vwap_payoff_dark_panel.py: presente com callback

### Duplicar estrutura

- classificacao geral: equivalente nos arquivos verificados
- UI/components/terminal_vwap_payoff_dark_panel.py: presente com callback
- ui/components/terminal_vwap_payoff_dark_panel.py: presente com callback

### Arquivar estrutura

- classificacao geral: equivalente nos arquivos verificados
- UI/components/terminal_vwap_payoff_dark_panel.py: presente com callback
- ui/components/terminal_vwap_payoff_dark_panel.py: presente com callback

### Registrar decisao HOLD

- classificacao geral: equivalente nos arquivos verificados
- UI/components/terminal_vwap_payoff_dark_panel.py: presente com callback
- ui/components/terminal_vwap_payoff_dark_panel.py: presente com callback

### Abrir ajuste de estrutura

- classificacao geral: equivalente nos arquivos verificados
- UI/components/terminal_vwap_payoff_dark_panel.py: presente com callback
- ui/components/terminal_vwap_payoff_dark_panel.py: presente com callback

### Registrar decisao CLOSE

- classificacao geral: equivalente nos arquivos verificados
- UI/components/terminal_vwap_payoff_dark_panel.py: presente com callback
- ui/components/terminal_vwap_payoff_dark_panel.py: presente com callback

### Registrar decisao ADJUST

- classificacao geral: equivalente nos arquivos verificados
- UI/components/terminal_vwap_payoff_dark_panel.py: presente com callback
- ui/components/terminal_vwap_payoff_dark_panel.py: presente com callback

### Voltar para lista

- classificacao geral: equivalente nos arquivos verificados
- UI/components/terminal_vwap_payoff_dark_panel.py: presente com callback
- ui/components/terminal_vwap_payoff_dark_panel.py: presente com callback

## Leitura tecnica

O inventario indica que o painel dark ja possui as principais acoes laterais de estruturas ligadas a callbacks.

As acoes cobrem o fluxo de carregar, criar, recalcular, editar, duplicar, arquivar, registrar decisoes e ajustar estrutura.

A etapa nao alterou codigo funcional.

## Decisao

Antes de aplicar qualquer patch funcional, recomenda-se validacao manual dirigida das acoes ja existentes.

Se a validacao manual confirmar funcionamento, a proxima demanda pode ser apenas documentar equivalencia funcional.

Se alguma acao falhar em tempo de execucao, o patch deve ser pontual e restrito ao callback correspondente.
