# REVISAO_FUNCIONAL_POS_USO_REAL_FASE_1_REPRODUCAO

## Objetivo

Confirmar o estado atual do sistema antes de qualquer correção funcional.

Esta fase não altera código de produção.

## Base

Tag base:

marco-zero-reinicio-limpo-20260622

Branch:

reinicio-normalizacao-idioma-ptbr

## Escopo da Fase 1

Reproduzir e registrar evidências dos problemas descritos na revisão funcional pós uso real:

1. Estrutura não atualiza dados na implantação.
2. Recalculo de estrutura nova informa que snapshot não mudou e recálculo é desnecessário.
3. Estrutura aparentemente não atualiza automaticamente via RTD.
4. Métricas financeiras não são preenchidas.
5. Estrutura número 2 aparece duplicada na listagem.
6. Duplicidade não aparece no filtro de decisão.
7. Sistema precisa ser normalizado para Português Brasil.
8. Gráfico de payoff precisa comentar ganho, perda e melhor posição.
9. Estrutura implantada precisa melhorar visibilidade e atualização instantânea.
10. Chamada de aba ou alias deve ser removida se não existir mais uso funcional.

## Regra da fase

Nenhuma correção será feita nesta fase.

Apenas:

- reproduzir;
- observar;
- registrar;
- localizar arquivos candidatos;
- classificar problemas confirmados e não reproduzidos.

## 1. Estado inicial do Git

Comando executado:

git status --short

Resultado:

Pendente.

Comando executado:

git log --oneline -6

Resultado:

Pendente.

## 2. Estado inicial do banco

Banco analisado:

Pendente.

Tabelas a observar, quando existirem:

- structures
- structure_legs
- structure_decisions
- payoff_curve_points
- rtd_option_quotes
- pricing_executions
- system_snapshots
- structure_events

Resultado antes dos testes:

Pendente.

## 3. Cadastro manual com ponto decimal

Teste:

- Criar estrutura usando ponto decimal.
- Aplicar leg.
- Salvar estrutura.
- Verificar listagem.
- Verificar detalhes.

Resultado:

Pendente.

Evidência:

Pendente.

Problema confirmado:

Pendente.

## 4. Cadastro manual com vírgula decimal

Teste:

- Criar estrutura usando vírgula decimal.
- Aplicar leg.
- Salvar estrutura.
- Verificar listagem.
- Verificar detalhes.

Resultado:

Pendente.

Evidência:

Pendente.

Problema confirmado:

Pendente.

## 5. Payoff

Teste:

- Abrir estrutura recém-criada.
- Verificar se a curva aparece.
- Verificar se há pontos em payoff_curve_points.

Resultado:

Pendente.

Evidência:

Pendente.

Problema confirmado:

Pendente.

## 6. Decisões

Teste:

- Executar busca de decisões.
- Verificar se há registros em structure_decisions.
- Verificar se a estrutura manual participa da análise.

Resultado:

Pendente.

Evidência:

Pendente.

Problema confirmado:

Pendente.

## 7. Atualizar dados

Teste:

- Clicar em Atualizar Dados.
- Registrar mensagem exibida.
- Verificar se houve pipeline.
- Verificar se houve RTD.
- Verificar se houve payoff.
- Verificar se houve decisões.

Resultado:

Pendente.

Mensagem exibida:

Pendente.

Problema confirmado:

Pendente.

## 8. RTD

Teste:

- Testar com conexão RTD aberta, se disponível.
- Verificar se rtd_option_quotes foi atualizada.
- Verificar se a tela usa dados novos ou cache antigo.

Resultado:

Pendente.

Evidência:

Pendente.

Problema confirmado:

Pendente.

## 9. Recalculo, snapshot e métricas financeiras

Teste:

- Criar ou selecionar estrutura nova.
- Executar recálculo.
- Registrar mensagem exibida.
- Verificar se snapshot mudou.
- Verificar se métricas financeiras foram preenchidas.

Resultado:

Pendente.

Mensagem exibida:

Pendente.

Problema confirmado:

Pendente.

## 10. Duplicidade da estrutura número 2

Teste:

- Verificar listagem de estruturas.
- Verificar se estrutura número 2 aparece duplicada.
- Comparar com filtro de decisão.
- Identificar se a duplicidade é visual ou real no banco.

Resultado:

Pendente.

Evidência:

Pendente.

Problema confirmado:

Pendente.

## 11. Português Brasil

Teste:

- Registrar mensagens em inglês visíveis ao usuário.
- Registrar botões, status, erros, decisões e textos misturados.
- Não corrigir nesta fase.

Ocorrências encontradas:

Pendente.

Problema confirmado:

Pendente.

## 12. Comentário do gráfico de payoff

Teste:

- Abrir gráfico de payoff.
- Verificar se há comentário textual de ganho, perda, melhor região, pior região e ponto de equilíbrio.

Resultado:

Pendente.

Problema confirmado:

Pendente.

## 13. Visibilidade da estrutura implantada

Teste:

- Verificar atualização visual após implantação.
- Verificar atualização visual após RTD.
- Verificar atualização visual após recálculo.
- Verificar se há horário de última atualização.
- Verificar se há estado visual de carregamento, erro ou sem dados novos.

Resultado:

Pendente.

Problema confirmado:

Pendente.

## 14. Aba ou alias

Teste:

- Verificar se o sistema ainda exibe aba ou alias ao usuário.
- Verificar se aba ou alias ainda tem uso funcional.
- Não remover nesta fase.

Resultado:

Pendente.

Problema confirmado:

Pendente.

## 15. Localização inicial de desenvolvimento

Arquivos candidatos a investigar antes de qualquer alteração:

### Interface e cadastro manual

- UI/main_window.py
- UI/components/structure_editor_dialog.py
- UI/components/structures_list_panel.py
- UI/components/details_panel.py
- UI/components/payoff_chart.py
- UI/components/decisions_grid.py

### Serviços e pipeline

- services/canonical_pricing_facade.py
- services/pricing_execution_app_service.py
- services/pricing_execution_orchestration_service.py
- services/pricing_execution_persistence_service.py
- services/pricing_execution_query_service.py
- services/structure_analysis_service.py
- services/structure_market_input_assembler.py
- services/structure_leg_rtd_enrichment_service.py

### Domínio

- domain/canonical_validators.py
- domain/payoff.py
- domain/payoff_features.py
- domain/structure_metrics.py
- domain/market_snapshot.py
- domain/decision.py

### Repositórios

- repositories/structures_repository.py
- repositories/structure_events_repository.py
- repositories/pricing_executions_repository.py
- repositories/market_snapshot_repository.py
- repositories/rtd_option_quotes_repository.py
- repositories/system_snapshots_repository.py
- repositories/robo_legs_repository.py
- repositories/robo_legs_status_repository.py

### API e controladores

- api/pricing_execution_controller.py
- api/structures_controller.py

### Testes candidatos

- ATT/tests/test_structure_editor_dialog.py
- ATT/tests/test_structure_editor_integration.py
- ATT/tests/test_structures_repository.py
- ATT/tests/test_structures_api.py
- ATT/tests/test_canonical_validators.py
- ATT/tests/test_payoff_canonical.py
- ATT/tests/test_payoff_chart.py
- ATT/tests/test_pricing_execution_service.py
- ATT/tests/test_pricing_execution_orchestration_service.py
- ATT/tests/test_pricing_execution_controller.py
- ATT/tests/test_rtd_option_quotes_repository_contract.py
- ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py

## 16. Buscas obrigatórias antes de alterar código

As buscas devem localizar mensagens, handlers, validações e referências obsoletas antes de qualquer correção.

Termos a buscar:

- Atualizar Dados
- recalculo
- recálculo
- snapshot
- snapshot não mudou
- snapshot nao mudou
- strike must be numeric
- payoff
- structure_decisions
- payoff_curve_points
- rtd_option_quotes
- alias
- aba
- aba_alias
- manual
- canonical
- Português
- Portuguese
- ganho
- perda

Resultado das buscas:

Pendente.

## 17. Estado final do banco

Resultado depois dos testes:

Pendente.

Diferenças observadas:

Pendente.

## 18. Classificação final da Fase 1

### Problemas confirmados

Pendente.

### Problemas não reproduzidos

Pendente.

### Problemas inconclusivos

Pendente.

### Próxima fase recomendada

Pendente.

## 19. Validação técnica da fase

Comando previsto:

python -m pytest ATT/tests -q

Resultado:

Pendente.

Comando previsto:

python -m compileall repositories services domain ATT/tests

Resultado:

Pendente.

## 20. Fechamento da Fase 1

Status:

Em aberto.

Commit de abertura:

Pendente.

Commit de fechamento:

Pendente.
