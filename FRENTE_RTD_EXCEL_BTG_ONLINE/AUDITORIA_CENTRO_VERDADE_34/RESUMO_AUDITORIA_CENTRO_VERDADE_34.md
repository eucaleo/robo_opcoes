# Auditoria Centro de Verdade 34

Projeto: `C:\users\eucal\projeto`
Saida: `C:\users\eucal\projeto\FRENTE_RTD_EXCEL_BTG_ONLINE\AUDITORIA_CENTRO_VERDADE_34`
Gerado em: `2026-07-17T21:24:04`

## Resultado dos checks

- [OK] PayoffRefreshCommandService existe — C:\users\eucal\projeto\services\payoff_refresh_command_service.py
- [OK] PayoffRefreshCommandService referencia PricingExecutionAppService
- [OK] PayoffRefreshCommandService chama execute_pricing()
- [OK] PayoffRefreshCommandService bloqueia status diferente de active
- [OK] PayoffRefreshCommandService consulta payoff_curve_points
- [OK] PayoffRefreshCommandService consulta/valida structure_decisions
- [OK] PayoffRefreshCommandService possui estados ok/warning/error
- [OK] DerivedPayoffPersistence tem guard active
- [ATENCAO] DerivedPayoffPersistence referencia payoff_curve_points
- [ATENCAO] DerivedPayoffPersistence referencia structure_decisions
- [OK] PricingExecutionPersistenceService possui payoff_persistence_port
- [OK] PricingExecutionOrchestrationService usa PricingExecutionPersistenceService
- [OK] canonical_pricing_facade referencia DerivedPayoffPersistence
- [OK] UI nao chama execute_pricing diretamente
- [OK] UI nao faz INSERT direto em payoff_curve_points
- [ATENCAO] UI nao faz INSERT direto em structure_decisions
- [OK] UI nao chama subprocess/os.system
- [ATENCAO] UI sem metodos locais de calculo de payoff — se ATENCAO, limpar somente apos backend validado
- [OK] Script recalculate_payoff_curve_points_once possui aviso de manutencao/emergencia

## Leitura recomendada

1. Abrir `01_payoff_refresh_command_service_achados.txt`.
2. Confirmar se o comando chama `PricingExecutionAppService.execute_pricing()`.
3. Abrir `02_derived_payoff_persistence_achados.txt`.
4. Confirmar se a persistencia derivada gera/persiste `payoff_curve_points` e `structure_decisions`.
5. Abrir `06_terminal_vwap_payoff_dark_panel_ui_achados.txt`.
6. Se houver metodos `_calculate_*`, nao corrigir ainda antes do teste backend sem UI.

## Regra de seguimento

Nao criar novo motor de payoff.
Nao criar outro comando paralelo.
Nao mexer na UI antes de validar backend/comando oficial.

