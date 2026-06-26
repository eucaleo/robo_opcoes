# Revisão Funcional Pós Uso Real — Fase 9 — Português Brasil

## Status

Em andamento.

## Objetivo

Normalizar textos visíveis ao usuário para Português do Brasil, preservando a lógica funcional já validada nas fases anteriores.

Esta fase não tem como objetivo alterar cálculo, persistência, estrutura de banco, RTD, payoff, decisão ou fluxo operacional. O escopo é restrito à revisão de idioma, clareza e consistência textual.

## Escopo inicial

A Fase 9 deve revisar:

- rótulos de botões, menus, painéis e abas;
- mensagens exibidas ao usuário;
- textos de status operacional;
- mensagens de erro controladas;
- títulos e descrições da interface;
- termos técnicos quando expostos na UI;
- eventuais textos em inglês remanescentes;
- eventuais textos com acentuação corrompida;
- consistência entre termos já usados nas fases anteriores.

## Fora de escopo

Não fazem parte desta fase:

- alteração de regra de cálculo;
- alteração de schema de banco;
- alteração de RTD;
- alteração de motor de precificação;
- alteração de cadastro de estruturas;
- alteração de fluxo de salvar, editar, arquivar ou recalcular;
- limpeza histórica ampla de documentação antiga;
- tradução de nomes internos de classes, funções, tabelas ou APIs.

## Critério de segurança

Qualquer alteração deve ser limitada a textos de apresentação ou mensagens controladas.

Se uma string fizer parte de contrato técnico, teste, nome de coluna, nome de tabela, payload, chave de dicionário, rota interna ou identificador persistido, ela não deve ser traduzida sem análise específica.

## Plano de execução

1. Levantar pontos de texto expostos ao usuário.
2. Classificar cada ocorrência como UI, mensagem controlada, documentação viva, teste ou identificador técnico.
3. Corrigir apenas textos seguros.
4. Executar validação técnica.
5. Registrar evidências.
6. Encerrar a fase com checkpoint e auditoria.

## Evidências previstas

- inventário de ocorrências textuais;
- lista de arquivos alterados;
- validação por compileall;
- pytest quando aplicável;
- verificação final da rota.

## Estado inicial observado

A Fase 8 foi encerrada no commit 7027499.

A Fase 9 inicia com foco exclusivo em normalização de Português do Brasil.


## Baseline técnica inicial

Após a abertura da Fase 9, foi executado `pytest`.

Resultado observado:

- 671 testes coletados;
- 666 testes passaram;
- 3 testes falharam;
- 2 testes foram ignorados.

As falhas observadas foram registradas em:

- docs/evidencias/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_9_BASELINE_PYTEST.txt

Classificação:

As falhas são consideradas fora do escopo direto da Fase 9 de Português Brasil, pois tratam de contrato de timestamp e guardrail arquitetural sobre importação direta de sqlite3 na UI.

A Fase 9 seguirá limitada a textos de interface, mensagens controladas e documentação viva.
