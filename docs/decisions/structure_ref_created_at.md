
## Causa raiz

| Camada | Situação |
|---|---|
| DDL de teste (`_make_db`) | Sem coluna `created_at` |
| DDL de produção | `created_at DEFAULT CURRENT_TIMESTAMP` |
| `_insert_decision` | Inseria `created_at` explicitamente  quebrava no teste |

## Decisão

Remover `created_at` da lista de colunas e valores do `INSERT` em
`_insert_decision`. O SQLite usa automaticamente o `DEFAULT CURRENT_TIMESTAMP`
definido no DDL de produção.

**Princípio:** colunas com `DEFAULT` não devem ser inseridas explicitamente
salvo necessidade de override. Isso mantém compatibilidade entre DDL de
produção e DDL de teste mínimo.

## Fix aplicado

# Decisão Arquitetural: created_at removido do INSERT explícito

**Data:** 2026-06-03  
**Branch:** patch/53-structure-ref  
**Status:** FECHADO [OK]

---

## Contexto

Durante a implementação do `StructureRef` (tipo canônico para identificação de
estrutura), o método `_insert_decision` em `db/derived_repo.py` inseria
explicitamente a coluna `created_at` com `datetime.now().isoformat()`.

## Problema

O DB temporário criado nos testes (`_make_db`) usava um DDL mínimo **sem**
a coluna `created_at`, causando:





```sql
-- ANTES
INSERT INTO structure_decisions
(timestamp, aba, decision, level, pl_atual, pl_max, pl_pct_of_max,
 dte_min, why, why_json, spot_ref, meta_json, structure_id, created_at)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

-- DEPOIS
INSERT INTO structure_decisions
(timestamp, aba, decision, level, pl_atual, pl_max, pl_pct_of_max,
 dte_min, why, why_json, spot_ref, meta_json, structure_id)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
