# Exportação PNG no painel dark

Data de referência: 2026-07-02

## Objetivo

Implementar exportação PNG do gráfico de Payoff no modo dark.

## Arquivos alterados

- UI/components/terminal_vwap_payoff_dark_panel.py
- ui/components/terminal_vwap_payoff_dark_panel.py

## Decisão técnica

- O painel dark já possuía canvas de payoff.
- A UI antiga já possuía exportação PNG via savefig.
- O patch adiciona botão Exportar PNG no bloco de Payoff.
- O patch guarda a figura atual em fig_payoff.
- O patch usa savefig com dpi 150 e bbox tight.

## Escopo preservado

Não altera:

- banco;
- contratos canônicos;
- decisões;
- cálculo de payoff;
- carregamento de estruturas;
- persistência;
- UI atual principal.

## Estados tratados

- Sem figura disponível: aviso ao usuário.
- Cancelamento do seletor de arquivo: status de cancelamento.
- Sucesso: mensagem de sucesso e status.
- Erro ao salvar: mensagem de erro e status.

## Validação pendente

- Abrir modo dark.
- Carregar uma estrutura com payoff.
- Clicar em Exportar PNG.
- Salvar arquivo PNG.
- Confirmar abertura do PNG gerado.
- Confirmar que banco e contratos não foram alterados.
