Consolidação da fase 3A (canonical domain decoupling).

Evidências validadas por smoke scripts:
- imports e instanciação dos serviços principais
- contratos públicos orientados por `structure_id`
- canonical input com shape estruturado (`structure`, `market`, `meta`)
- pricing payload derivado do input canônico
- execução ponta a ponta via PricingExecutionAppService.execute_pricing(structure_id=...)
- persistência e consulta do resultado executado

Conclusão:
A 3A está concluída funcionalmente. O legado remanescente ficou reduzido
a compatibilidade interna/metadado e passa a ser tratado como cleanup técnico
nas próximas etapas.
