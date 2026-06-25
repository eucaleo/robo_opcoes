# REVISÃO FUNCIONAL PÓS-USO REAL — FASE 5 — ATUALIZAR DADOS E RESUMO DO PIPELINE

## Status

Aberta para diagnóstico.

---

## Objetivo da fase

Auditar e melhorar o comportamento do botão Atualizar Dados, garantindo que a ação executada pelo usuário seja rastreável, compreensível e verificável.

O sistema deve informar claramente:

- o que foi executado;
- quais dados foram lidos;
- quais dados foram processados;
- quais dados foram ignorados;
- quais dados foram atualizados;
- quais decisões foram geradas;
- quais pontos de payoff foram gerados;
- quais cotações RTD foram atualizadas;
- se houve avisos;
- se houve erros;
- se a execução ocorreu, mas não gerou dados novos.

---

## Origem

Esta fase faz parte da rota:

    NOVA_ROTA_REVISAO_FUNCIONAL_POS_USO_REAL

Ela é iniciada após o encerramento da Fase 4, que validou a integração das estruturas manuais com payoff e decisões.

---

## Problema central

O botão Atualizar Dados pode executar ações importantes do pipeline, mas o usuário pode não receber feedback suficiente sobre o resultado.

O risco principal é o sistema exibir uma mensagem genérica de sucesso, mesmo quando:

- nenhuma estrutura foi processada;
- nenhuma cotação RTD foi atualizada;
- nenhum ponto de payoff foi gerado;
- nenhuma decisão foi criada;
- todos os contadores retornaram zero;
- ocorreu erro parcial;
- houve rejeições ou avisos não exibidos.

---

## Regra principal da fase

Se o pipeline executar corretamente, mas todos os resultados forem zero, o sistema não deve exibir apenas uma mensagem genérica de sucesso.

Deve informar algo equivalente a:

    Atualização executada, mas nenhum dado novo foi gerado.

E, quando possível, detalhar os contadores.

---

## Pontos a investigar

1. Onde está o botão Atualizar Dados.
2. Qual função é chamada pelo clique.
3. Qual serviço ou script é acionado.
4. Quais pipelines são executados.
5. Quais contadores já existem.
6. Quais contadores precisam ser criados.
7. Como erros são capturados.
8. Como avisos são tratados.
9. Onde a mensagem final é montada.
10. Se a tela é atualizada após a execução.
11. Se existe diferença entre sucesso com dados e sucesso sem dados novos.

---

## Informações mínimas esperadas no resumo

| Campo | Descrição |
|---|---|
| Estruturas lidas | Quantidade de estruturas consideradas |
| Estruturas processadas | Quantidade de estruturas efetivamente processadas |
| Estruturas ignoradas | Quantidade de estruturas ignoradas |
| Pontos de payoff gerados | Quantidade de registros gerados em payoff_curve_points |
| Decisões geradas | Quantidade de registros gerados em structure_decisions |
| Cotações RTD atualizadas | Quantidade de cotações atualizadas |
| Avisos | Lista ou quantidade de avisos |
| Erros | Lista ou quantidade de erros |
| Status final | Sucesso, sucesso sem dados novos, aviso ou erro |

---

## Arquivos inicialmente relacionados

Arquivos candidatos para investigação:

    scripts/run_derived_pipeline.py
    scripts/run_rtd_option_quotes_pipeline.py
    scripts/run_rtd_refresh_full.py
    scripts/refresh_rtd_option_quotes_excel.ps1
    repositories/rtd_option_quotes_repository.py
    UI/components/structure_editor_dialog.py
    ATT/tests/test_run_rtd_option_quotes_pipeline.py
    ATT/tests/test_run_derived_pipeline_rtd_integration.py
    ATT/tests/test_rtd_option_quotes_repository_contract.py
    ATT/tests/test_structure_leg_rtd_enrichment_service.py

Também foi identificado que o caminho antigo abaixo não representa mais necessariamente o fluxo atual:

    scripts/refresh_rtd_symbol_to_option_quotes.py

---

## Critérios de aceite

| Critério | Status inicial |
|---|---|
| Botão Atualizar Dados localizado | A validar |
| Handler do botão identificado | A validar |
| Pipeline acionado identificado | A validar |
| Resumo de execução identificado ou criado | A validar |
| Contadores de RTD identificados ou criados | A validar |
| Contadores de payoff identificados ou criados | A validar |
| Contadores de decisões identificados ou criados | A validar |
| Mensagem de sucesso detalhada | A validar |
| Execução sem dados novos não mostra sucesso genérico | A validar |
| Erros técnicos são registrados | A validar |
| Usuário recebe mensagem clara em caso de erro | A validar |
| Tela é atualizada após sucesso quando aplicável | A validar |
| Testes são criados ou ajustados | A validar |
| Auditoria é atualizada | A validar |
| Commit final é gerado | A validar |

---

## Plano de execução

1. Localizar o botão Atualizar Dados na interface.
2. Identificar o handler chamado pelo botão.
3. Mapear o fluxo até o pipeline real.
4. Verificar se o pipeline retorna resumo estruturado.
5. Levantar os contadores existentes.
6. Criar ou ajustar resumo de execução, se necessário.
7. Padronizar mensagens em Português Brasil.
8. Diferenciar sucesso com dados, sucesso sem dados novos, sucesso com avisos e erro.
9. Garantir atualização da tela após execução bem-sucedida.
10. Adicionar ou ajustar testes automatizados.
11. Atualizar auditoria.
12. Executar testes.
13. Gerar commit final da Fase 5.

---

## Estado inicial

A Fase 5 está aberta.

A prioridade inicial é diagnosticar o fluxo real do botão Atualizar Dados e confirmar quais pipelines ele aciona.
