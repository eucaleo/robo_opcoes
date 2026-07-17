# Relatorio 32.10 - Teste real PayoffRefreshCommandService

Status: ok

Objetivo

Executar o comando oficial de refresh de payoff sem UI e confirmar persistencia real no banco.

Entrada

- Banco: C:\users\eucal\projeto\dados\app.db
- Structure ID: 2
- Backup criado: C:\users\eucal\projeto\dados\app.db.bak_32_10_20260717_203059

Comando executado

- Metodo chamado: refresh_payoff_for_structure
- Chamado com sucesso: True
- Erro: None

Deltas observados

- pricing_executions_all: 1
- pricing_executions_structure: 1
- payoff_curve_points_all: 101
- payoff_curve_points_structure: 101
- structure_decisions_all: 1
- structure_decisions_structure: 1

Checks

- OK: service_called = True
- OK: service_status = ok
- OK: pricing_execution_incremented = True
- OK: payoff_points_incremented = True
- OK: structure_decision_incremented = True
- OK: ok_only_with_payoff_points = True
- OK: backup_created = True

Conclusao

O comando oficial executou e gerou evidencia de persistencia de payoff e decisao derivada.

Proxima etapa recomendada

1. Se status ok, iniciar quarentena dos scripts paralelos.
2. Se status warning, corrigir o ponto indicado pelos checks.
3. Se status error, abrir o traceback do JSON e corrigir o metodo oficial chamado pela UI.
