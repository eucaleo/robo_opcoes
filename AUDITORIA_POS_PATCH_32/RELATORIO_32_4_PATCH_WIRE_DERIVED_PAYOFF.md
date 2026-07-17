# Relatorio 32.4 - Patch wiring DerivedPayoffPersistence

Arquivo alterado:
services\pricing_execution_orchestration_service.py

Backup:
services\pricing_execution_orchestration_service.py.bak_32_4_20260717_200400

Status:
patch aplicado

Import DerivedPayoffPersistence inserido:
True

Chamada PricingExecutionPersistenceService alterada:
True

Intencao:

Conectar o fluxo atual:

PayoffRefreshCommandService
  -> PricingExecutionAppService
    -> PricingExecutionOrchestrationService
      -> PricingExecutionPersistenceService
        -> DerivedPayoffPersistence
          -> payoff_curve_points
          -> structure_decisions

Motivo:

PricingExecutionAppService usa PricingExecutionOrchestrationService.
O CanonicalPricingFacade ja tinha DerivedPayoffPersistence conectado, mas ele nao esta no caminho principal atual.
Este patch conecta DerivedPayoffPersistence no default wiring de PricingExecutionOrchestrationService.
