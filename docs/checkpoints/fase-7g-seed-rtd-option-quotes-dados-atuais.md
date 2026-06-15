# Checkpoint — Fase 7G — Seed atual rtd_option_quotes

## Objetivo

Remover dados desatualizados da tabela `rtd_option_quotes` e popular o banco local com dados atuais das estruturas SPSB-SMAL e PRIO, permitindo testes com uma base consistente e sem alertas de obsolescência.

## Estruturas inseridas

### SPSB-SMAL

Referência do ativo: `108,45`

| Código | C/V | Quantidade | Valor executado |
|---|---:|---:|---:|
| SMALF129 | C | 4500 | 1,25 |
| SMALF103 | V | 2000 | 4,00 |
| SMALR127 | V | 2100 | 10,32 |
| SMALR108 | C | 2500 | 1,41 |

### PRIO

Referência do ativo: `61,34`

| Código | C/V | Quantidade | Valor executado |
|---|---:|---:|---:|
| PRIOG800 | C | 1000 | 0,46 |
| PRIOH515 | V | 1000 | 13,94 |
| PRIOT700 | V | 1000 | 6,64 |
| PRIOS525 | C | 1000 | 0,20 |

## Implementação

Foi criado o script:

```text
scripts/seed_current_rtd_option_quotes.py

