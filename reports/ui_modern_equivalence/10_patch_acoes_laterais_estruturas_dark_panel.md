# Patch funcional das acoes laterais de estruturas no painel dark

Data de referencia: 2026-07-02

## Objetivo

Registrar o patch funcional minimo aplicado nas acoes laterais de estruturas da UI moderna dark.

## Arquivos alterados

- UI/components/terminal_vwap_payoff_dark_panel.py
- ui/components/terminal_vwap_payoff_dark_panel.py

## Observacao sobre paths

No ambiente Windows validado, UI e ui apontam para o mesmo arquivo.

## Correcoes aplicadas

- duplicar estrutura passou a usar StructuresRepository diretamente
- duplicacao copia dados principais e legs da estrutura selecionada
- abrir ajuste passou a emitir status e aviso visual no painel lateral
- recalcular Payoff passou a exibir aviso visual de sucesso no painel lateral
- decisoes HOLD e ADJUST passaram a exibir aviso visual no painel lateral
- decisao CLOSE passou a arquivar a estrutura via StructuresRepository.archive_structure
- CLOSE em estrutura ja arquivada passou a exibir aviso sem repetir gravacao
- arquivar estrutura passou a validar status, confirmar por nome e exibir feedback final

## Restricoes preservadas

- nenhuma regra de calculo foi alterada
- nenhum contrato canonico foi alterado
- nenhum schema de banco foi alterado
- patch restrito a UI moderna dark e espelho ui
- status canonico preservado como active ou archived

## Validacao tecnica

- py_compile executado nos dois caminhos do painel dark
- assinatura confirmada de StructuresRepository.archive_structure
- list_structures sem include_archived confirmou apenas estruturas ativas na lista padrao

## Validacao manual executada

- selecionar estrutura
- recalcular Payoff
- abrir ajuste
- registrar ADJUST
- duplicar estrutura
- arquivar estrutura duplicada de teste
- encerrar estrutura ativa de teste com CLOSE
- repetir CLOSE em estrutura ja arquivada

## Resultado

As acoes laterais de estruturas da UI moderna dark ficaram funcionais para o fluxo validado.
