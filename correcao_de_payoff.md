
<!-- CHECKPOINT_PAYOFF_MTM_OPCOES_20260627_INICIO -->

## Checkpoint 2026-06-27 - Separação entre payoff no spot e MTM por preço atual da opção

### Contexto

Após a validação da rota RTD, Market Snapshot real, Pricing Canônico e auditoria de nomenclatura, foi identificada uma necessidade adicional no motor de pricing/payoff.

O sistema já havia separado conceitualmente:

- payoff no vencimento;
- preço atual do ativo-base;
- estrutura individual por structure_id;
- bloqueio de fallback estático como mercado atual.

Entretanto, ainda era necessário garantir que o PL atual da estrutura pudesse ser calculado por marcação a mercado das opções, usando o preço atual de cada opção vindo do RTD/cache, sem confundir esse preço com o prêmio de entrada.

### Problema tratado

O fluxo de implantação/autopreenchimento via RTD utiliza corretamente o preço RTD atual como preço inicial da perna.

Esse comportamento deve ser preservado.

Exemplo na implantação:

    premium = preço RTD atual
    current_option_price = preço RTD atual
    MTM inicial = 0

Isso está correto porque a estrutura acabou de ser criada usando a cotação corrente.

O problema a evitar é outro:

    em uma estrutura já implantada,
    o prêmio de entrada salvo não pode ser sobrescrito pelo RTD atual
    durante a reprecificação.

Para cálculo de marcação a mercado, o sistema deve separar:

    premium / entry_price
        preço de entrada da perna

    current_option_price / mid / bid / ask / ultimo_preco
        preço atual da opção

### Correção aplicada

Foi criado o commit:

    30f49de feat(pricing): separar payoff no spot de MTM por preço atual da opção

Arquivos alterados:

    services/payoff_pricing_engine.py
    services/canonical_pricing_facade.py
    ATT/tests/test_payoff_pricing_engine_mtm.py

### Validações executadas

Foram executados:

    python -m py_compile services/canonical_pricing_facade.py services/payoff_pricing_engine.py repositories/market_snapshot_repository.py

Resultado:

    OK

Também foram executados:

    python -m pytest \
      ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py \
      ATT/tests/test_payoff_pricing_engine_mtm.py \
      ATT/tests/test_canonical_pricing_facade.py \
      -q

Resultado:

    18 passed

E a suíte filtrada:

    python -m pytest ATT/tests -q -k "payoff or pricing or rtd or canonical"

Resultado:

    244 passed
    430 deselected
    6 subtests passed

### Status atualizado da frente

    OK        Implantação automática via RTD preservada
    OK        MarketSnapshotRepository mantendo contrato de autopreenchimento
    OK        CanonicalPricingFacade preservando campos atuais RTD
    OK        PayoffPricingEngine separando payoff_at_spot de pl_atual_mtm
    OK        MTM por perna implementado
    OK        Fallback para payoff no spot quando MTM estiver incompleto
    OK        Testes focados aprovados
    OK        Suíte filtrada payoff/pricing/rtd/canonical aprovada
    pendente Validar reprecificação funcional de estrutura já salva
    pendente Completar UI com snapshots e tabela analítica por perna

### Relação com a pendência de UI

Este checkpoint não encerra a frente completa de payoff.

O checkpoint anterior de UI permanece vigente:

    Status: INCOMPLETO COM PATCH NECESSÁRIO.

Ainda falta completar a tela de payoff para exibir de forma auditável:

- snapshot da implantação;
- snapshot atual completo;
- tabela analítica por perna;
- intrínseco atual por perna;
- extrínseco atual por perna;
- PL atual por perna;
- payoff no vencimento ao preço atual por perna;
- separação visual clara entre PL atual e payoff no vencimento.

<!-- CHECKPOINT_PAYOFF_MTM_OPCOES_20260627_FIM -->
