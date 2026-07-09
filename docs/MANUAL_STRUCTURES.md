# Estruturas Manuais (override de legs) — app.db

## Contexto
O pipeline atual usa tabelas `rtd_*` em `dados/app.db` como fonte raw.
Para permitir criar/editar estruturas sem depender do Excel/RDP, foi adicionada
uma tabela manual de legs que pode sobrescrever (override) a leitura do domínio.

## Tabela manual
Banco: `dados/app.db` (ou `APP_DB_PATH`)

Tabela: `manual_analise_robo_legs`

Campos (principais):
- `timestamp` (TEXT, NOT NULL)
- `aba` (TEXT, NOT NULL)
- `ativo`, `cv`, `call_put`, `quant`, `valor_executado`, `bid`, `ask`, `iv`, `delta`, ...
- `strike`, `vencimento`, `dte`, `pl_realista`
- `source` (DEFAULT 'manual')
- `created_at` (DEFAULT datetime('now'))

Índices:
- `ix_manual_legs_aba_ts (aba, timestamp)`

## Regra de seleção da fonte (domínio)
Função: `domain.payoff.read_structure_legs(aba, timestamp=None)`

Prioridade:
1. Se existir `manual_analise_robo_legs` e houver linhas para a `aba`, usar esta tabela.
2. Caso contrário, usar `rtd_analise_robo_legs`.

Resolução de timestamp:
- Se `timestamp` não for informado, usa `MAX(timestamp)` na fonte escolhida.

## Timestamp canônico (UI/Recalc)
O timestamp canônico por `aba` deve considerar `manual_analise_robo_legs` como
fonte prioritária. Assim, alterações manuais disparam recálculo corretamente.

## Próximos passos
- Implementar CRUD na UI para escrever legs em `manual_analise_robo_legs`.
- Garantir que o derived pipeline seja disparado/reprocessado ao salvar.
