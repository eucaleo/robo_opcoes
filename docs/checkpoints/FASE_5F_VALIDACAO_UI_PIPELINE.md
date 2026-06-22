# Fase 5F - Validacao da UI do resumo do pipeline

## Objetivo

Validar que a interface executa o pipeline e exibe corretamente o resumo operacional ao usuario.

## Ambiente

- Sistema: Sistema de Derivados - Analise de Decisoes
- Banco derivado: dados/derived.db
- Execucao pela UI: Ferramentas > Executar Pipeline
- Data da validacao: 2026-06-22
- Branch: fase-3a4-auto-pricing-manual-save

## Evidencia da UI

A interface exibiu mensagem de sucesso apos execucao do pipeline.

Resumo operacional observado:

    Pipeline executado com sucesso.

    Resumo operacional:
    - Estruturas: n/d
    - Decisoes: 2
    - Pontos de payoff: 202
    - Resumos de payoff: n/d
    - Execucoes de pricing: n/d
    - Cotacoes RTD atualizadas: 4
    - Avisos: 0
    - Erros: 0

## Evidencia do terminal

### Estado do Git

    On branch fase-3a4-auto-pricing-manual-save
    Your branch is ahead of origin/fase-3a4-auto-pricing-manual-save by 5 commits.

    nothing to commit, working tree clean

### Ultimos commits observados

    aab7e92 Integra importacao RTD CSV ao pipeline derived
    a64a464 Restaura e valida cadeia historica RTD de opcoes
    711f088 fase 4: detalha feedback operacional do pipeline
    a1088b3 docs: add phase 3f payoff diagnostic evidence
    861c17f fix: normalize manual legs for derived payoff persistence

### Testes automatizados

Comando executado:

    python -m pytest ATT/tests -q

Resultado observado:

    667 passed, 2 skipped, 6 subtests passed in 37.91s

### Compileall

Comando executado:

    python -m compileall repositories services domain ATT/tests

Resultado observado:

    Listing 'repositories'...
    Listing 'services'...
    Listing 'domain'...
    Listing 'ATT/tests'...
    Compiling 'ATT/tests\\test_canonical_pricing_facade_manual_without_alias.py'...
    Compiling 'ATT/tests\\test_run_derived_pipeline_rtd_integration.py'...
    Compiling 'ATT/tests\\test_structure_editor_dialog.py'...

Sem erro de compilacao observado.

## Evidencia do pipeline pela UI

A UI executou o pipeline e registrou no console:

    [PIPELINE] Importando cotacoes RTD para derived.db...
    Importacao RTD wide CSV
    -----------------------
    input_rows: 4
    inserted: 0
    updated: 4
    skipped: 0
    updated_at: 2026-06-22 09:24:21

    Auditoria rtd_option_quotes
    Banco: dados\derived.db
    Tabela: rtd_option_quotes
    Status: ok

    Metricas:
    - distinct_codigo_count: 4
    - duplicate_codigo_count: 0
    - max_age_minutes: 30
    - missing_codigo_count: 0
    - row_count: 4
    - stale_rows: 0

    Pipeline concluido com sucesso.

    [PIPELINE] Validando consistencia final dos snapshots...
    [ok] Snapshots consistentes

    [PIPELINE] Resumo operacional:
      Estruturas: n/d
      Decisoes: 2
      Pontos de payoff: 202
      Resumos de payoff: n/d
      Execucoes de pricing: n/d
      Cotacoes RTD atualizadas: 4
      Avisos: 0
      Erros: 0

Resumo JSON observado:

    {
      "decisions": 2,
      "errors": 0,
      "payoff_points": 202,
      "payoff_summaries": null,
      "pricing_executions": null,
      "rtd_import": {
        "errors": 0,
        "input_rows": 4,
        "inserted": 0,
        "returncode": 0,
        "skipped": 0,
        "updated": 4,
        "warnings": 0
      },
      "rtd_quotes_updated": 4,
      "structures": null,
      "table_counts": {
        "payoff_curve_points": 202,
        "rtd_option_quotes": 4,
        "structure_decisions": 2
      },
      "warnings": 0
    }

## Validacoes funcionais

| Item | Resultado |
|---|---|
| Pipeline executado pela UI | OK |
| Mensagem de sucesso exibida | OK |
| Resumo operacional exibido ao usuario | OK |
| Decisoes exibidas no resumo | OK |
| Pontos de payoff exibidos no resumo | OK |
| Cotacoes RTD atualizadas exibidas no resumo | OK |
| Avisos exibidos | OK |
| Erros exibidos | OK |
| Curva de payoff visivel | OK |
| Decisao listada na grade | OK |
| Banco derived.db usado pela UI | OK |
| Contrato canonico de payoff_curve_points usado | OK |
| Snapshots consistentes | OK |
| Sem dependencia direta perceptivel de Excel na execucao da UI | OK |
| Sem acionamento de PowerShell pela UI | OK |

## Observacao

Os campos Estruturas, Resumos de payoff e Execucoes de pricing permanecem como n/d.

Isso nao bloqueia a Fase 5F, pois o objetivo desta validacao era confirmar que a interface exibe corretamente o resumo operacional principal do pipeline, incluindo:

- decisoes;
- pontos de payoff;
- cotacoes RTD atualizadas;
- avisos;
- erros;
- status final de sucesso.

## Conclusao

A Fase 5F foi validada com sucesso.

A UI confirma a execucao do pipeline, apresenta o resumo operacional esperado, reflete corretamente os dados persistidos no derived.db e mantem coerencia com a execucao em terminal.

A cadeia validada ate este ponto esta pronta para avancar para a Fase 6 - Validacao integrada final.
