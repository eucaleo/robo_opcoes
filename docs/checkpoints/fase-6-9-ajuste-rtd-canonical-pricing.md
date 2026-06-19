# Fase 6.9 — Ajuste RTD Canonical Pricing

## Objetivo

Robustecer a normalização numérica usada pela fachada canônica de pricing RTD, preservando o contrato do payload protegido pelos guardrails da Fase 6.8.

## Escopo

Arquivo produtivo alterado:

- `services/canonical_pricing_facade.py`

Arquivo de teste alterado:

- `ATT/tests/test_canonical_pricing_facade.py`

## Alteração produtiva

A função `_to_float()` passou a aceitar formatos numéricos comuns vindos de RTD, planilhas e fontes mistas BR/US:

- `R$ 1.234,56`
- `1.234,56`
- `1,234.56`
- `R$ 124,66`

A normalização preserva compatibilidade com os formatos já suportados e mantém retorno default em caso de valor inválido.

## Contrato preservado

A alteração não muda o formato do `pricing_payload`.

Campos preservados:

- `structure_id`
- `underlying_asset`
- `reference_date`
- `spot_price`
- `legs`
- `meta`
- `price`
- `premium`
- `strike`
- `side`
- `position_side`
- `expiration_date`

Também permanece preservado o guardrail da Fase 6.8 que garante que o `underlying_asset` vem explicitamente da estrutura canônica, e não da aba legada do snapshot.

## Evidências

Evidências geradas:

- `docs/checkpoints/evidencias/fase-6-9-pytest-canonical-pricing-rtd-number-formats.txt`
- `docs/checkpoints/evidencias/fase-6-9-pytest-pricing-execution-services.txt`

Resultado esperado:

- `ATT/tests/test_canonical_pricing_facade.py`: 11 testes passando
- `ATT/tests/test_pricing_execution_service.py` + `ATT/tests/test_pricing_execution_app_service.py`: 11 testes passando

## Conclusão

A Fase 6.9 adiciona robustez ao parsing numérico do fluxo RTD canonical pricing sem alterar contrato público do payload e sem quebrar os serviços de execução de pricing existentes.
