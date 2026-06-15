# Checkpoint — Fase 8A — Auditoria de integração rtd_option_quotes com snapshot

## Objetivo

Auditar o ponto seguro de integração entre a tabela `rtd_option_quotes` e os serviços de snapshot/cálculo, sem alteração funcional em UI, schema, cálculo ou fluxo legado.

## Corte utilizado

A ROTA_MESTRE_2 foi delimitada pelo range:

```bash
a03a42f^..HEAD
```

Commit de abertura:

```text
a03a42f 2026-06-13T18:48:09-03:00 docs: abre ROTA_MESTRE_2 e auditoria do ciclo RTD
```

## Arquivos alterados na ROTA_MESTRE_2

A auditoria por range confirmou alterações em:

- documentação da rota;
- scripts de auditoria/importação/pipeline de `rtd_option_quotes`;
- testes dos scripts;
- ajustes em repositórios legados relacionados a ordenação cronológica e remoção de consultas inseguras.

Os serviços centrais de snapshot/cálculo ainda não foram alterados para consumir `rtd_option_quotes`.

## Achados de histórico

O arquivo:

```text
repositories/rtd_option_quotes_repository.py
```

não nasceu na ROTA_MESTRE_2. Ele já existia em commit anterior:

```text
525ad98 2026-06-06T18:08:49-03:00 Adiciona importacao de cotacoes RTD de opcoes via CSV
```

A ROTA_MESTRE_2 consolidou o fluxo operacional em volta da tabela, incluindo:

- `scripts/import_rtd_links_to_option_quotes.py`
- `scripts/audit_rtd_option_quotes.py`
- `scripts/run_rtd_option_quotes_pipeline.py`
- `scripts/seed_current_rtd_option_quotes.py`
- `scripts/import_lista_rtd_excel_to_option_quotes.py`
- `scripts/run_lista_rtd_option_quotes_pipeline.py`

## Contrato técnico esperado

A chave provável de integração continua sendo:

```text
structure_legs.symbol = rtd_option_quotes.codigo_opcao
rtd_analise_robo_legs.ativo = rtd_option_quotes.codigo_opcao
```

No domínio canônico, `symbol` representa o código da opção.

No fallback legado, `ativo`, `symbol` ou `ticker` são usados para formar o símbolo da leg.

## Validação no banco local

Banco auditado:

```text
dados/app.db
```

Tabelas encontradas:

```text
rtd_option_quotes: OK
rtd_analise_robo_legs: OK
manual_analise_robo_legs: OK
structures: OK
structure_legs: OK
```

Contagens observadas:

```text
rtd_option_quotes: 8
rtd_analise_robo_legs: 20
manual_analise_robo_legs: 0
structures: 5
structure_legs: 20
```

## Resultado crítico da validação

A auditoria de join retornou:

```text
total_legs: 20
matched_legs: 0
```

Também não houve match entre:

```text
structure_legs.symbol
```

e:

```text
rtd_option_quotes.codigo_opcao
```

## Cotações atuais encontradas em rtd_option_quotes

Foram observados códigos como:

```text
PRIOG800
PRIOH515
PRIOS525
PRIOT700
SMALF103
SMALF129
SMALR108
SMALR127
```

## Legs canônicas atuais observadas

Foram observados códigos como:

```text
BOVAE166
BOVAE195
BOVAQ164
BOVAQ195
EMBJE704
EMBJE868
EMBJQ660
EMBJQ878
PRIOD750
PRIOE515
PRIOP600
PRIOQ720
SBSPE155
SBSPE175
SBSPQ131
SBSPQ166
SMALD139
SMALE119
SMALP970
SMALQ119
```

## Conclusão

A integração por `codigo_opcao` é tecnicamente plausível, mas a base local atual não possui correspondência operacional entre as legs carregadas nas estruturas/snapshot legado e as cotações atuais em `rtd_option_quotes`.

Portanto, a Fase 8A não autoriza ainda alteração funcional em:

- `services/market_snapshot_selector.py`
- `services/canonical_pricing_facade.py`
- `repositories/market_snapshot_repository.py`
- cálculo
- UI

## Decisão técnica

Não implementar ainda o enriquecimento do snapshot com `rtd_option_quotes`.

Antes disso, é necessário reconciliar:

```text
estruturas/legs ativas
        com
códigos atuais carregados em rtd_option_quotes
```

## Risco identificado

Se a integração for feita agora, o fluxo provavelmente continuará sem usar as cotações RTD atuais, pois o join retorna zero correspondências.

Também há risco de mascarar o problema real: as cotações RTD atuais pertencem a vencimentos/códigos diferentes daqueles registrados nas estruturas canônicas e nas legs legadas.

## Próxima etapa recomendada

Abrir a fase:

```text
Fase 8B — Reconciliação de estruturas/legs com rtd_option_quotes
```

Objetivos:

1. Confirmar quais estruturas estão ativas.
2. Confirmar quais estruturas deveriam usar os códigos atuais de `rtd_option_quotes`.
3. Verificar se as estruturas canônicas estão desatualizadas.
4. Verificar se o Excel `LISTA_RTD.xlsm` contém as legs atuais que ainda não foram persistidas em `structure_legs`.
5. Definir se a origem da verdade para legs atuais será:
   - `structure_legs`;
   - `rtd_analise_robo_legs`;
   - uma aba do `LISTA_RTD.xlsm`;
   - ou outro importador controlado.

## Arquivos funcionais alterados nesta fase

Nenhum.

## Status

Fase 8A concluída como auditoria sem alteração funcional.
