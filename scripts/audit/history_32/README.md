# Histórico de scripts auxiliares da rodada 32

Esta pasta preserva scripts pontuais usados durante correções/auditorias da rodada 32.

Eles são mantidos apenas para rastreabilidade local e auditoria histórica.

## Importante

- Não fazem parte do fluxo oficial de payoff.
- Não devem ser chamados pela UI.
- Não devem substituir serviços oficiais.
- Não devem ser reutilizados sem nova revisão.
- O fluxo oficial permanece:

UI -> PayoffRefreshCommandService -> PricingExecutionAppService -> PricingExecutionPersistenceService -> DerivedPayoffPersistence
