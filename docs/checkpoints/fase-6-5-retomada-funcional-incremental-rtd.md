# Fase 6.5 — Retomada funcional incremental pós-proteção do contrato RTD

## Estado inicial

Branch de trabalho:

- `fase-6-5-retomada-funcional-incremental-rtd`

Base inicial:

- `73506cd`

Branch de integração anterior:

- `fase-12-fechamento-ciclo`

Fase anterior concluída:

- Fase 6.4 — Proteção do contrato de leitura RTD para canonical pricing.

Evidências iniciais:

- `docs/checkpoints/evidencias/fase-6-5-git-status-inicial.txt`
- `docs/checkpoints/evidencias/fase-6-5-git-log-inicial.txt`

## Objetivo da Fase 6.5

Retomar a evolução funcional do fluxo RTD/canonical pricing de forma incremental, após a proteção contratual consolidada na Fase 6.4.

A fase deve priorizar alterações pequenas, testáveis e reversíveis, preservando os contratos já protegidos.

## Premissas herdadas da Fase 6.4

1. `repositories/rtd_option_quotes_repository.py` possui contrato público protegido por testes.
2. A leitura RTD por código, listagem e ativo-base está validada.
3. O comportamento quando a tabela `rtd_option_quotes` não existe está coberto.
4. O fluxo de canonical pricing relacionado a preço RTD permaneceu verde no pós-merge.
5. Excel permanece apenas como gateway RTD.
6. Nenhuma alteração em UI/API deve ser feita sem decisão explícita.
7. A evolução deve ser guiada por testes e evidências.

## Escopo permitido

A Fase 6.5 pode atuar, de forma incremental, em:

1. inventário de pontos funcionais pendentes após a proteção RTD;
2. identificação da menor fatia funcional segura para retomada;
3. testes de caracterização antes de alteração de comportamento;
4. ajustes internos em serviço/repository/facade, se necessários;
5. documentação de decisões técnicas;
6. registro de evidências de testes.

## Fora de escopo nesta fase

Não fazem parte da Fase 6.5 sem decisão explícita:

1. alteração de UI;
2. alteração de API pública;
3. alteração de schema persistente sem plano próprio;
4. substituição do Excel como gateway RTD;
5. refatoração ampla;
6. mudança em regras de negócio não cobertas por testes;
7. remoção de compatibilidade com comportamento validado na Fase 6.4.

## Invariantes obrigatórios

Durante a Fase 6.5, devem permanecer verdadeiros:

1. a suíte `rtd_option_quotes` deve continuar verde;
2. os testes de canonical pricing relacionados a RTD devem continuar verdes;
3. ausência da tabela RTD não deve quebrar o fluxo;
4. preços RTD válidos devem continuar tendo precedência conforme contrato atual;
5. ausência de preço RTD válido deve manter fallback esperado;
6. alterações devem ser acompanhadas por evidências em `docs/checkpoints/evidencias/`.

## Plano inicial

### Passo 1 — Inventário funcional pós-Fase 6.4

Mapear os pontos funcionais pendentes relacionados a RTD/canonical pricing.

Saída esperada:

- `docs/checkpoints/evidencias/fase-6-5-inventario-retomada-funcional-rtd.md`

### Passo 2 — Escolha da menor fatia funcional

Selecionar uma única fatia funcional pequena para evolução.

Critérios:

1. baixo risco;
2. teste objetivo;
3. sem alteração de UI/API;
4. compatível com contratos da Fase 6.4;
5. reversível.

### Passo 3 — Teste de caracterização

Antes de alterar código funcional, criar ou reforçar teste que descreva o comportamento atual ou esperado.

### Passo 4 — Implementação mínima

Executar apenas a alteração necessária para passar o teste escolhido.

### Passo 5 — Validação e evidência

Executar testes direcionados e registrar saídas em `docs/checkpoints/evidencias/`.

## Testes mínimos esperados

Antes do fechamento da fase, devem ser executados ao menos:

```bash
python -m pytest ATT/tests -k "rtd_option_quotes"
```

```bash
python -m pytest ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py
```

Outros testes poderão ser adicionados conforme a fatia funcional escolhida.

## Critério de fechamento

A Fase 6.5 poderá ser fechada quando:

1. a fatia funcional tiver sido definida;
2. testes de caracterização tiverem sido criados ou atualizados;
3. a alteração funcional, se houver, for mínima;
4. as suítes RTD/canonical pricing permanecerem verdes;
5. as evidências forem registradas;
6. o documento mestre for atualizado;
7. a branch for integrada posteriormente à `fase-12-fechamento-ciclo`.

## Status

Em andamento.
