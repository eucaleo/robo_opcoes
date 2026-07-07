# Smoke manual Terminal VWAP UI

Data de criacao: 2026-07-06

Branch:

    audit/terminal-vwap-ui

Classificacao:

    REGRESSAO_UI

Componente principal provavel:

    UI/components/terminal_vwap_payoff_dark_panel.py

## 1. Objetivo

Executar smoke manual observacional do Terminal VWAP sem alterar funcionalidade, banco, pipeline, services, repositories, controllers ou regra de negocio.

## 2. Escopo

Este smoke cobre somente validacao visual e operacional minima da area Terminal VWAP.

Nao declara equivalencia global da UI moderna dark.

Nao encerra a frente UI completa.

## 3. Pre-condicoes

- branch audit/terminal-vwap-ui ativa;
- arvore Git limpa antes da execucao;
- UI aberta pelo caminho atual do projeto;
- nenhuma alteracao funcional aplicada durante o smoke;
- Terminal VWAP acessivel pela navegacao atual;
- usuario operador deve registrar qualquer falha observada.

## 4. Checklist de execucao

1. Abrir a UI pelo entrypoint atual do projeto.
2. Confirmar que a janela principal abre sem erro visivel.
3. Confirmar que o modo visual dark permanece ativo quando aplicavel.
4. Acessar a area Terminal VWAP.
5. Confirmar que o painel Terminal VWAP renderiza sem excecao visivel.
6. Confirmar presenca ou ausencia esperada de estruturas.
7. Selecionar uma estrutura quando houver estrutura disponivel.
8. Confirmar exibicao de detalhes da estrutura selecionada.
9. Confirmar exibicao de pernas quando houver pernas associadas.
10. Confirmar comportamento correto quando nao houver pernas.
11. Confirmar exibicao de KPIs quando aplicavel.
12. Confirmar exibicao de graficos quando aplicavel.
13. Confirmar exibicao de alertas quando aplicavel.
14. Confirmar estados vazios sem quebra visual.
15. Confirmar mensagens de status.
16. Testar botoes sem selecao, apenas observando bloqueios ou mensagens.
17. Testar botoes com selecao, sem confirmar acao destrutiva se houver risco.
18. Navegar para outra area e retornar ao Terminal VWAP.
19. Confirmar que nao houve travamento da UI.
20. Registrar resultado final como APROVADO, APROVADO_COM_RESSALVAS ou REPROVADO.

## 5. Criterio de aprovacao

APROVADO se:

- Terminal VWAP abre;
- painel renderiza;
- navegacao basica funciona;
- estados vazios nao quebram a UI;
- selecao basica nao trava a aplicacao;
- nao ha excecao visivel durante o fluxo minimo.

APROVADO_COM_RESSALVAS se:

- Terminal VWAP abre;
- fluxo minimo funciona;
- existem falhas visuais ou comportamentos incompletos nao bloqueantes.

REPROVADO se:

- UI nao abre;
- Terminal VWAP nao carrega;
- ocorre excecao visivel bloqueante;
- navegacao trava;
- selecao basica quebra o painel.

## 6. Proibicoes durante o smoke

Nao alterar:

- banco;
- schema;
- pipeline;
- regra de negocio;
- services;
- repositories;
- controllers;
- entrypoint principal;
- estrutura global da UI.

## 7. Evidencias minimas

Registrar:

- horario de inicio;
- horario de fim;
- branch;
- commit;
- resultado;
- itens aprovados;
- itens com ressalva;
- falhas;
- prints, se forem coletados manualmente;
- decisao de continuidade.
