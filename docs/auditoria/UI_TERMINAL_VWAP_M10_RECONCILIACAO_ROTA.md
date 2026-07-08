# M10 - Reconciliacao documental da rota Terminal VWAP

## 1. Objetivo

Registrar o estado real da frente Terminal VWAP apos as PRs recentes e reconciliar a documentacao macro com os incrementos ja mergeados no main.

Esta M10 e exclusivamente documental.

Nao altera codigo produtivo, testes, banco, pipeline, payoff, UIDataModel, services, repositories, controllers ou regra de negocio.

## 2. Motivacao

A documentacao macro original ainda contem trechos que tratam M1, M2, M3, M4 e M5 como pendentes.

Entretanto, o historico atual do main ja contem evidencias posteriores, incluindo documentos especificos de M2, M3, M6, M7 e commits recentes relacionados a M4, M8 e M9.

Portanto, a M10 registra que a rota macro precisa ser lida com este adendo de reconciliacao.

## 3. Estado observado no historico recente

Commits recentes relevantes no main:

    d3091a3 test(ui): consolida fakes no wiring terminal vwap (#18)
    44a28f9 test(ui): reduz duplicacao no wiring terminal vwap (#16)
    f1ff1e5 fix(ui-modern): estabiliza regressao operacional do M4 (#14)

Interpretacao documental:

- f1ff1e5 indica estabilizacao operacional relacionada ao M4;
- 44a28f9 indica reducao de duplicacao no teste de wiring Terminal VWAP;
- d3091a3 indica consolidacao de fakes no teste de wiring Terminal VWAP.

## 4. Documentos especificos ja existentes

Foram localizados documentos especificos da frente Terminal VWAP:

    docs/auditoria/UI_TERMINAL_VWAP_M2_INVENTARIO_REAL.md
    docs/auditoria/UI_TERMINAL_VWAP_M3_2_TESTES_RENDER_SEM_TK.md
    docs/auditoria/UI_TERMINAL_VWAP_M3_FECHAMENTO.md
    docs/auditoria/UI_TERMINAL_VWAP_M3_INSPECAO_ARQUIVO_AUTORIZADO.md
    docs/auditoria/UI_TERMINAL_VWAP_M3_PATCH_RENDER_SEGURO.md
    docs/auditoria/UI_TERMINAL_VWAP_M3_UI_ONLY_REGRESSAO_ATT.md
    docs/auditoria/UI_TERMINAL_VWAP_M6_FECHAMENTO_REGRESSAO.md
    docs/auditoria/UI_TERMINAL_VWAP_M7_IDEMPOTENCIA_TESTE.md

Esses documentos demonstram que a frente ja avancou alem do estado inicial descrito nos documentos macro.

## 5. Classificacao da M9

A PR M9, mergeada como d3091a3, teve escopo restrito a teste:

    ATT/tests/test_ui_modern_dark_window_terminal_vwap_wiring.py

A M9 consolidou:

- FakeUIDataModel comum;
- helper patch_window_dependencies;
- reducao de repeticao de monkeypatches;
- organizacao de infraestrutura de testes do wiring Terminal VWAP.

A M9 nao implementou novo fluxo funcional macro.

A M9 nao validou integralmente:

- fluxo completo de estruturas;
- fluxo completo de pernas;
- estados vazios visuais;
- mensagens de status em execucao real;
- KPIs;
- graficos;
- matriz final de equivalencia;
- validacao manual assistida;
- equivalencia funcional completa contra UI canonica.

Portanto, a M9 deve ser classificada como preparacao e consolidacao de infraestrutura de testes, nao como fechamento funcional amplo da frente Terminal VWAP.

## 6. Reconciliacao com documentos macro

Os documentos abaixo permanecem historicamente validos como planejamento original, mas estao defasados quanto ao estado executado:

    docs/auditoria/UI_AUDITORIA_MACRO_EVOLUCAO.md
    docs/auditoria/UI_COMPARATIVO_ROTA_MACRO.md

Sempre que esses documentos indicarem que M1, M2, M3, M4 ou M5 estao integralmente pendentes, deve-se ler essa informacao em conjunto com esta M10.

A M10 nao apaga o historico original. Ela apenas registra o estado real atual.

## 7. Estado consolidado ate M10

Estado documental recomendado:

| Bloco | Estado reconciliado |
|---|---|
| M1 | Superado parcialmente por infraestrutura e wiring ja presentes |
| M2 | Existe inventario real documentado |
| M3 | Existe fechamento UI-only documentado |
| M4 | Ha commit de estabilizacao operacional relacionado ao M4 |
| M5 | Citado em fechamento posterior como parte da frente M5/M6 |
| M6 | Existe fechamento de regressao documentado |
| M7 | Existe evidencia automatizada de idempotencia documentada |
| M8 | Interpretado como reducao de duplicacao em teste de wiring |
| M9 | Consolidacao de fakes no teste de wiring; preparacao, nao macro funcional |
| M10 | Reconciliacao documental da rota |

## 8. Pendencias que permanecem abertas

Mesmo com M2 a M9 documentados ou mergeados, permanecem abertas pendencias macro de equivalencia e validacao funcional ampla:

- validacao assistida ou manual do Terminal VWAP na UI moderna;
- confirmacao visual de estados vazios;
- confirmacao visual de selecao invalida;
- validacao de mensagens e status em execucao real;
- validacao ampla de navegacao entre abas;
- equivalencia contra UI canonica;
- revisao da matriz global de equivalencia UI;
- decisao formal sobre maturidade operacional do Terminal VWAP moderno;
- separacao continua entre UI-only e camadas de banco, pipeline, payoff, UIDataModel e regra de negocio.

## 9. Regra de continuidade

A proxima frente apos esta M10 nao deve presumir que o Terminal VWAP funcional completo esta encerrado.

A proxima frente deve escolher explicitamente um destes caminhos:

1. documentar roteiro de validacao assistida ou manual;
2. criar regressao automatizada adicional restrita a UI;
3. atualizar matriz de equivalencia com status parcial;
4. abrir nova correcao UI-only pequena e bem delimitada.

Nao ha autorizacao para misturar Terminal VWAP com banco, pipeline, payoff, UIDataModel, services, repositories, controllers ou regra de negocio sem nova classificacao formal.

## 10. Status da M10

M10 registra reconciliacao documental da rota ate M9.

Status: concluida documentalmente quando este arquivo for commitado e a PR correspondente for mergeada.
