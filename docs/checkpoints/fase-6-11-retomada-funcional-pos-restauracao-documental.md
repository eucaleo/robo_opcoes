# Fase 6.11 — Retomada funcional pós-restauração documental

## Status

Em andamento.

## Objetivo

Retomar o desenvolvimento funcional de forma controlada após a restauração documental da ROTA_MESTRE_3.

A fase parte da main já sincronizada com as Fases 6.7, 6.8, 6.9 e 6.10.

## Base

    ed7825c docs: sincroniza rota mestre 3 apos fases 6.7 a 6.9
    fase-6-10-restauracao-documental-rota-mestre-3

## Branch

    fase-6-11-retomada-funcional-pos-restauracao-documental

## Escopo permitido

    RTD
    canonical pricing
    pricing execution
    diagnóstico funcional
    testes automatizados
    documentação de checkpoint

## Escopo proibido

    alteração de UI/API
    alteração de banco
    migração
    limpeza destrutiva
    refatoração ampla sem teste
    mudança funcional sem evidência

## Baseline inicial

Testes executados:

    python -m pytest ATT/tests/test_canonical_pricing_facade.py -q
    python -m pytest ATT/tests/test_pricing_execution_service.py ATT/tests/test_pricing_execution_app_service.py -q

Evidências:

    docs/checkpoints/evidencias/fase-6-11-pytest-canonical-pricing-facade-baseline.txt
    docs/checkpoints/evidencias/fase-6-11-pytest-pricing-execution-baseline.txt
    docs/checkpoints/evidencias/fase-6-11-inventario-testes-rtd-option-canonical.txt

## Observação sobre filtro inicial

O filtro rtd_option_quotes não selecionou testes no baseline inicial.

Resultado observado:

    585 deselected

Portanto, a fase deve primeiro inventariar os nomes reais de testes e caminhos relacionados a RTD, options, quotes, canonical pricing e pricing execution antes de executar nova alteração funcional.

## Próxima microfatia candidata

Identificar o menor ponto funcional ainda descoberto no caminho RTD/canonical pricing e protegê-lo com teste automatizado antes de qualquer expansão de escopo.


## Ajuste de enquadramento da retomada

Fica registrado que a frente atual permanece classificada como Fase 6.11 — retomada funcional pos-restauracao documental.

Qualquer mencao anterior ou lateral a Fase 11 deve ser tratada apenas como referencia futura da rota mestre, e nao como classificacao do trabalho em andamento.

### Classificacao corrigida

Fase: 6.11

Nome: Retomada funcional pos-restauracao documental

Natureza: baseline tecnico e preparacao de guardrail funcional leve

Escopo: RTD, fallback legado, canonical input, pricing input e pricing payload

### Classificacao a evitar

Fase: 11

Nome: Validacao integrada pos-retomada

Motivo: a Fase 11 envolve fluxo integrado mais amplo, incluindo importacao, persistencia, cadastro de estrutura, enriquecimento completo, pricing, snapshot e UI. Esse escopo ainda nao foi iniciado nesta retomada funcional.

### Decisao

A continuidade deve seguir dentro da Fase 6.11, com uma microfatia de guardrail automatizado leve para proteger a cadeia RTD e fallback legado ate pricing payload.

### Restricoes para continuidade

- nao alterar banco
- nao alterar schema
- nao alterar UI
- nao alterar API
- nao depender de Excel real
- nao depender de RTD real
- nao depender de integracao externa
- nao reclassificar esta frente como Fase 11

### Proxima microfatia autorizada

Nome: guardrail-rtd-legacy-canonical-pricing-input

Descricao: criar teste automatizado leve validando que uma estrutura sem legs canonicas internas consegue montar entrada de pricing usando fallback RTD ou legado quando houver legs RTD disponiveis.

Fluxo protegido:

- RTD ou fallback legado
- canonical input
- pricing input
- pricing payload

Criterio de sucesso:

- novo teste automatizado passa
- regressao do recorte atual continua passando
- payload final nao expoe alias legado indevido
- nenhuma alteracao em banco, schema, UI ou API

## Auditoria de estado atual RTD, bancos, scripts e testes

Foi realizada auditoria sem alteração funcional para identificar o estado atual de RTD/rtd_option_quotes após a restauração documental.

Evidência registrada em:

- `docs/checkpoints/evidencias/fase-6-11-estado-atual-rtd-db-scripts-testes.txt`

Conclusões:

- `rtd_option_quotes` existe em `dados/app.db` e `dados/derived.db`.
- Ambos os bancos passaram em `pragma integrity_check`.
- Ambos possuem 4 registros funcionais equivalentes em `rtd_option_quotes`.
- A comparação funcional entre `app.db` e `derived.db` retornou:
  - `somente_app: 0`
  - `somente_derived: 0`
  - `comuns_diferentes: 0`
- A fonte dos registros atuais é `BTG_RTD_EXCEL`.
- Não há duplicados por `codigo_opcao`.
- Não há scripts RTD versionados ativos de import/audit/pipeline/refresh.
- A camada RTD vigente é de leitura/enriquecimento/uso em pricing e snapshots.
- Testes ativos relacionados passaram com sucesso: `23 passed`.

Decisão:

Referências documentais antigas indicando `rtd_option_quotes` como ausente devem ser tratadas como histórico de um estado anterior, não como descrição do estado atual da branch.

## Mapa runtime de leitura RTD no pricing

Foi realizado diagnóstico sem alteração funcional para identificar o caminho real de leitura RTD usado pelo fluxo runtime principal de pricing.

Evidência registrada em:

- `docs/checkpoints/evidencias/fase-6-11-mapa-runtime-leitura-rtd-pricing.txt`

Conclusões:

- O fluxo runtime principal de pricing não lê diretamente `rtd_option_quotes`.
- A entrada produtiva parte de `services/pricing_execution_app_service.py`.
- `PricingExecutionAppService` instancia `CanonicalPricingFacade` usando `dados/app.db` como banco padrão.
- O caminho confirmado passa por:
  - `PricingExecutionAppService`
  - `CanonicalPricingFacade`
  - `MarketSnapshotRepository`
  - `MarketSnapshotSelector`
  - `PricingExecutionService`
  - `PricingExecutionPersistenceService`
- As tabelas efetivamente lidas pelo caminho runtime são:
  - `manual_analise_robo_legs`
  - `rtd_analise_robo_legs`
  - `rtd_analise_robo`
- A política de seleção observada é manual > RTD por ativo.
- `rtd_option_quotes` existe na branch atual, possui repository e serviço de enriquecimento relacionados, mas não foi encontrada instanciação produtiva desses componentes no fluxo runtime principal de pricing.
- Portanto, nesta branch, `rtd_option_quotes` deve ser tratada como camada RTD latente/de staging/enriquecimento, não como fonte ativa do pipeline principal de pricing.

Decisão:

A continuidade funcional da Fase 6.11 deve considerar que o runtime atual de pricing está ancorado em `MarketSnapshotRepository`/`MarketSnapshotSelector`, não em `rtd_option_quotes`.

Qualquer integração futura de `rtd_option_quotes` ao pricing runtime deve ser feita como microfatia explícita, com teste automatizado antes da alteração funcional.

