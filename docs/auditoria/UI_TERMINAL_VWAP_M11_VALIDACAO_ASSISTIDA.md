# M11 - Roteiro de validacao assistida Terminal VWAP

## 1. Objetivo

Definir um roteiro objetivo de validacao assistida da frente Terminal VWAP na UI moderna.

Esta M11 e exclusivamente documental.

Nao altera codigo produtivo, testes, banco, pipeline, payoff, UIDataModel, services, repositories, controllers ou regra de negocio.

A M11 existe para transformar as pendencias registradas na M10 em um plano verificavel de validacao UI-only.

## 2. Origem

A M10 reconciliou a rota documental Terminal VWAP ate M9 e registrou que a frente ainda nao deve ser considerada funcionalmente encerrada.

A M10 tambem indicou que a proxima frente deveria escolher explicitamente um caminho.

O caminho escolhido nesta M11 e:

    documentar roteiro de validacao assistida ou manual

## 3. Escopo da M11

Esta M11 cobre somente validacao assistida da interface moderna do Terminal VWAP.

A validacao deve observar comportamento visual, navegacao, mensagens, estados vazios, selecao invalida e consistencia operacional aparente da UI.

A M11 nao executa alteracao funcional.

A M11 nao autoriza mudancas em:

- banco;
- pipeline;
- payoff;
- UIDataModel;
- services;
- repositories;
- controllers;
- regra de negocio;
- calculos financeiros;
- integracao externa;
- persistencia;
- infraestrutura de producao.

## 4. Relacao com M9 e M10

A M9 consolidou infraestrutura de testes do wiring Terminal VWAP.

A M10 registrou que a M9 nao fecha validacao funcional ampla.

A M11 define o roteiro para validar, de forma assistida, os pontos que permanecem abertos apos M10.

## 5. Premissas de execucao

Antes da validacao assistida, o ambiente deve estar no main atualizado apos merge da M10.

Referencia esperada no historico:

    docs(ui): reconcilia rota terminal vwap ate m9 (#19)

A validacao deve ser feita sem alterar dados produtivos.

Se for necessario usar dados simulados, fakes ou massa controlada, isso deve ser documentado antes da execucao.

Se qualquer comportamento depender de banco, pipeline, payoff ou services reais, a validacao deve registrar essa dependencia e nao assumir conclusao funcional completa.

## 6. Matriz de validacao assistida

| ID | Area | Verificacao | Resultado esperado | Evidencia esperada |
|---|---|---|---|---|
| M11-01 | Inicializacao | Abrir UI moderna com Terminal VWAP disponivel | Tela carrega sem erro critico visivel | Registro textual do comportamento observado |
| M11-02 | Navegacao | Acessar area ou aba relacionada ao Terminal VWAP | Navegacao ocorre sem travamento | Registro textual e, se possivel, captura local |
| M11-03 | Estado vazio | Visualizar Terminal VWAP sem selecao ou sem dados | UI apresenta estado vazio compreensivel | Descricao da mensagem ou ausencia dela |
| M11-04 | Selecao invalida | Tentar interagir sem estrutura valida selecionada | UI nao quebra e informa ou preserva estado seguro | Descricao do comportamento |
| M11-05 | Estruturas | Selecionar estrutura valida quando disponivel | UI reflete selecao sem erro visual | Descricao da selecao e resultado |
| M11-06 | Pernas | Verificar area de pernas quando aplicavel | Dados ou estado vazio aparecem de forma coerente | Descricao do conteudo exibido |
| M11-07 | Status | Observar mensagens de status do Terminal VWAP | Mensagens sao legiveis e coerentes com a acao | Texto da mensagem observada |
| M11-08 | KPIs | Observar area de KPIs quando disponivel | KPIs aparecem ou estado vazio e apresentado | Descricao dos valores ou estado vazio |
| M11-09 | Graficos | Observar area grafica quando disponivel | Grafico aparece ou estado vazio e apresentado | Descricao visual do comportamento |
| M11-10 | Erros UI | Forcar caminho sem dados quando possivel | UI nao exibe traceback ao usuario | Registro do comportamento |
| M11-11 | Reentrada | Sair e retornar ao Terminal VWAP | Estado permanece seguro e navegavel | Registro textual |
| M11-12 | Idempotencia visual | Repetir a mesma navegacao mais de uma vez | Comportamento permanece consistente | Registro textual |
| M11-13 | Comparacao canonica | Comparar comportamento aparente com UI canonica quando possivel | Divergencias sao registradas, nao corrigidas nesta M11 | Lista de divergencias observadas |
| M11-14 | Encerramento | Fechar a UI apos navegacao | Encerramento ocorre sem erro critico visivel | Registro textual |

## 7. Checklist de execucao assistida

Durante a validacao, preencher manualmente ou em documento posterior:

- data da validacao;
- branch ou commit validado;
- sistema operacional;
- comando utilizado para abrir a UI;
- massa de dados utilizada;
- se houve banco real, fake ou ambiente controlado;
- resultado de cada item M11-01 a M11-14;
- divergencias observadas;
- conclusao parcial;
- recomendacao para proxima frente.

## 8. Comandos auxiliares recomendados

Antes de qualquer validacao assistida, recomenda-se conferir o estado do repositorio:

    git status --short
    git log --oneline -5

Se for apropriado executar regressao automatizada ja existente, usar somente testes UI relacionados e registrar o resultado.

Teste previamente relacionado a M9:

    python -m pytest ATT/tests/test_ui_modern_dark_window_terminal_vwap_wiring.py

A execucao desse teste nao substitui a validacao assistida.

Ela apenas complementa o registro de seguranca do wiring.

## 9. Criterios de aceite da M11

A M11 e considerada concluida quando:

- este roteiro estiver versionado em docs/auditoria;
- a PR correspondente estiver mergeada no main;
- nao houver alteracao de codigo produtivo;
- nao houver alteracao de testes;
- nao houver alteracao em banco, pipeline, payoff, UIDataModel, services, repositories, controllers ou regra de negocio;
- o documento estiver sem crases;
- o documento definir claramente que a validacao funcional ampla ainda depende de execucao assistida posterior.

## 10. Saida esperada apos M11

Apos a M11, a proxima frente pode ser uma destas:

1. M12 - execucao assistida e registro de evidencias;
2. M12 - regressao automatizada adicional UI-only para estados vazios;
3. M12 - matriz de equivalencia Terminal VWAP contra UI canonica;
4. M12 - correcao UI-only pequena, caso a validacao assistida encontre falha objetiva.

## 11. Status

Status da M11: roteiro documental proposto.

Esta M11 nao afirma que o Terminal VWAP moderno esta funcionalmente validado.

Ela apenas cria o roteiro formal para essa validacao.
