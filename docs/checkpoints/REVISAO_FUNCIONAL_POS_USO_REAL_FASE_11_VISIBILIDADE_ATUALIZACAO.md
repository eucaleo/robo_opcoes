# Revisão Funcional Pós Uso Real — Fase 11
# Visibilidade da estrutura implantada e atualização instantânea

## 1. Objetivo

Melhorar a experiência visual da estrutura implantada, refletindo de forma clara o estado de atualização da estrutura após RTD, recálculo e pipeline.

A interface deve permitir que o usuário entenda:

- quando uma atualização começou;
- quando terminou;
- se houve mudança nos dados;
- se não houve dados novos;
- se ocorreu erro;
- qual foi o horário da última atualização;
- se a estrutura exibida reflete o último cálculo disponível.

## 2. Origem da fase

Esta fase deriva da rota NOVA_ROTA_REVISAO_FUNCIONAL_POS_USO_REAL, com base na segunda revisão de uso real.

Problema principal registrado:

- melhorar a visibilidade da estrutura implantada com atualização de posição e atualização automática instantânea, refletindo no sistema comportamento semelhante ao observado no Excel.

## 3. Problemas tratados

Conforme a rota da revisão funcional, esta fase trata:

- estrutura implantada não mostra atualização clara;
- usuário espera atualização instantânea após RTD ou recálculo;
- métricas, posição e status precisam refletir o estado atual;
- tela pode não evidenciar quando os dados foram atualizados;
- mensagem de ausência de mudança precisa ser clara;
- erro de atualização precisa ser visível;
- carregamento precisa ter indicação visual.

## 4. Escopo permitido

Nesta fase está permitido revisar e alterar:

- atualização da tela após RTD;
- atualização da tela após recálculo;
- atualização da tela após pipeline;
- mensagens visíveis ao usuário;
- status bar;
- painel de detalhes da estrutura;
- indicadores de carregamento;
- indicadores de erro;
- indicadores de ausência de dados novos;
- exibição do horário da última atualização;
- atualização visual da estrutura selecionada após uma ação concluída.

## 5. Escopo proibido

Nesta fase não será feito:

- migração para web;
- alteração do motor financeiro sem necessidade comprovada;
- mudança de regra de cálculo de payoff;
- mudança de regra de decisão;
- mudança de schema de banco sem necessidade comprovada;
- refatoração ampla fora do fluxo de atualização visual;
- alteração de fases já encerradas sem evidência de regressão;
- remoção de aba ou alias, pois isso pertence à Fase 12.

## 6. Arquivos inicialmente identificados

Busca inicial indicou os seguintes arquivos como principais candidatos de análise:

- UI/main_window.py
- UI/components/details_panel.py
- UI/components/structure_editor_dialog.py
- services/calculation_orchestrator.py
- services/canonical_pricing_facade.py
- services/market_snapshot_selector.py
- repositories/market_snapshot_repository.py
- repositories/rtd_option_quotes_repository.py
- repositories/system_snapshots_repository.py
- ATT/tests/test_run_derived_pipeline_rtd_integration.py
- ATT/tests/test_run_rtd_option_quotes_pipeline.py
- ATT/tests/test_system_snapshots_repository.py

A intervenção funcional deve começar preferencialmente por UI/main_window.py e UI/components/details_panel.py, pois a fase é prioritariamente de visibilidade da interface.

## 7. Evidência inicial antes de alteração funcional

Estado inicial registrado antes de modificar código:

- árvore de trabalho limpa;
- testes automatizados executados;
- compilação executada.

Resultado dos testes informado:

- 669 passed;
- 2 skipped;
- 6 subtests passed.

Comando executado:

- python -m pytest ATT/tests -q

Resultado:

- aprovado.

Comando executado:

- python -m compileall repositories services domain ATT/tests UI

Resultado:

- aprovado.

## 8. Pontos técnicos a revisar

### 8.1 Atualização após pipeline

Verificar em UI/main_window.py:

- run_pipeline;
- mensagem antes da execução;
- mensagem após sucesso;
- mensagem após erro;
- chamada de atualização da lista;
- chamada de atualização do painel de detalhes;
- resumo exibido ao usuário.

### 8.2 Atualização após recálculo

Verificar em UI/main_window.py e UI/components/details_panel.py:

- fluxo de recálculo manual;
- mensagem de recálculo iniciado;
- mensagem de recálculo finalizado;
- mensagem de snapshot sem alteração;
- comportamento quando há erro;
- atualização do painel após conclusão.

### 8.3 Atualização após RTD

Verificar:

- se o fluxo RTD atualiza rtd_option_quotes;
- se a tela usa dados novos após a coleta;
- se o usuário vê horário ou confirmação da última atualização;
- se ausência de retorno RTD é comunicada.

### 8.4 Horário da última atualização

Verificar se já existe dado confiável em:

- snapshots;
- structure_decisions;
- payoff_curve_points;
- pricing executions;
- rtd_option_quotes;
- estado interno da UI.

Caso não exista fonte única consolidada, a primeira melhoria aceitável é exibir o horário da última atualização visual da tela, sem prometer que houve alteração financeira.

## 9. Critérios de aceite

A Fase 11 será considerada concluída quando:

- usuário vê quando uma atualização começa;
- usuário vê quando uma atualização termina;
- usuário vê se a atualização terminou com sucesso;
- usuário vê se ocorreu erro;
- usuário vê quando não houve mudança ou dados novos;
- usuário vê o horário da última atualização visual ou operacional;
- painel da estrutura selecionada é atualizado após pipeline, recálculo ou RTD quando aplicável;
- mensagens estão em Português Brasil;
- não há promessa de resultado financeiro;
- testes automatizados continuam aprovados;
- compilação continua sem erro;
- auditoria viva foi atualizada;
- commit da fase foi criado.

## 10. Plano de execução

1. Criar este checkpoint.
2. Atualizar a auditoria viva.
3. Fazer commit documental de início da Fase 11.
4. Inspecionar os trechos relevantes da UI.
5. Implementar melhoria mínima e rastreável de visibilidade.
6. Testar com pytest.
7. Testar com compileall.
8. Atualizar checkpoint com evidência final.
9. Atualizar auditoria com resultado.
10. Commitar a implementação funcional.

## 11. Resultado esperado

Ao final da fase, a estrutura implantada deve ficar visualmente mais confiável para o usuário, com feedback claro de atualização e estado atual da tela.

## Evidência final da Fase 11 - visibilidade de atualização da estrutura

Data da validação: 2026-06-26

Branch: reinicio-normalizacao-idioma-ptbr

Commit de trabalho antes do fechamento: 420e912

### Arquivos funcionais alterados

- UI/main_window.py
- UI/components/details_panel.py

### Implementação realizada

Foi adicionada visibilidade explícita do ciclo de atualização da estrutura na UI, sem alterar regra de negócio, pipeline, pricing ou modelo de dados.

A alteração inclui:

- indicador visual no painel de detalhes: Atualização visual;
- método público DetailsPanel.set_update_status(...);
- mensagens de início e fim para:
  - carregamento inicial;
  - atualização manual;
  - atualização automática;
  - execução de pipeline;
  - recálculo de estrutura;
- assinatura leve dos dados visíveis para indicar:
  - dados carregados;
  - sem mudança aparente;
  - com mudanças visíveis;
- preservação da seleção existente por structure_id;
- manutenção da compatibilidade das chamadas legadas de refresh_data() via parâmetro default source="manual".

### Validação executada

Comandos executados:

    python -m py_compile UI/main_window.py UI/components/details_panel.py
    python -m pytest ATT/tests -q
    python -m compileall repositories services domain ATT/tests UI
    grep -R "refresh_data(" -n UI ATT/tests | head -50

Resultados:

    python -m py_compile UI/main_window.py UI/components/details_panel.py
    OK sem saída

    python -m pytest ATT/tests -q
    669 passed, 2 skipped, 6 subtests passed in 40.61s

    python -m compileall repositories services domain ATT/tests UI
    OK

    grep -R "refresh_data(" -n UI ATT/tests | head -50
    UI/main_window.py:74:        self.refresh_data(source="inicial")
    UI/main_window.py:168:        self.root.bind("<F5>", lambda e: self.refresh_data())
    UI/main_window.py:320:    def refresh_data(self, show_errors: bool = True, source: str = "manual")
    UI/main_window.py:498:            self.refresh_data(show_errors=False, source="automática")
    UI/main_window.py:639:                self.root.after(0, lambda: self.refresh_data(source="recálculo"))
    UI/main_window.py:763:            self.refresh_data(source="pipeline")
    UI/main_window.py:1146:                        self.refresh_data()

### Conclusão

A Fase 11 foi implementada com escopo controlado e validação automatizada completa.

A UI agora informa claramente ao usuário quando os dados visíveis foram atualizados, quando não houve mudança aparente e quando pipeline ou recálculo estão em andamento ou foram concluídos.
