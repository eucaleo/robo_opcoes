# Patch 24 — Auditoria de Acoplamento Legado · `domain/`

> Branch: `patch/3a-canonical-domain-decoupling`  
> Data: 2026-05-28  
> Escopo: módulos `domain/*.py` — sem alteração de lógica de negócio

---

## 1. Objetivo

Documentar todos os pontos de acoplamento residual com o modelo legado
(identificador `aba`, tabela `rtd_analise_robo`, funções `*_for_aba`) nos
módulos de domínio, classificá-los por severidade e prescrever o caminho
de desacoplamento para o próximo patch.

---

## 2. Mapa de severidade

| Nível    | Ícone | Critério |
|----------|-------|----------|
| CRÍTICO  | 🔴    | Bloqueia o desacoplamento canônico; deve ser removido antes do merge |
| MODERADO | 🟡    | Não bloqueia o pipeline canônico, mas cria dívida técnica mensurável |
| BAIXO    | 🔵    | Aceitável como metadata/rastreabilidade; revisar oportunisticamente |

---

## 3. Resultados por arquivo

---

### 3.1 `domain/decision.py`

**Perfil:** 🔴 CRÍTICO

#### Ocorrências

| Linha | Severidade | Termo | Contexto |
|-------|-----------|-------|---------|
| 207 | 🔴 CRÍTICO | `compute_decision_for_aba` | Assinatura da função legada |
| 220 | 🔴 CRÍTICO | `compute_payoff_for_aba` | Import condicional de função inexistente no payoff canônico |
| 220 | 🔴 CRÍTICO | `read_structure_summary` | Import condicional de função inexistente no payoff canônico |
| 229 | 🔴 CRÍTICO | `read_structure_summary` | Chamada direta |
| 241 | 🔴 CRÍTICO | `compute_payoff_for_aba` | Chamada direta |
| 407–419 | 🔴 CRÍTICO | `get_app_db_connection` + `rtd_analise_robo` | Bloco `__main__` com query direta ao banco legado |

#### Marcadores canônicos presentes ✅

- `compute_payoff_from_canonical_input`
- `compute_decision_from_contract`
- `compute_decision_from_payoff`
- `compute_decision_from_inputs`
- `CanonicalStructureMarketInput`

#### Diagnóstico

O módulo está **majoritariamente canônico**. A função `compute_decision_for_aba`
é um resquício de compatibilidade que referencia funções (`compute_payoff_for_aba`,
`read_structure_summary`) que **não existem no `payoff.py` canônico atual**.
O bloco `__main__` é um script de teste manual que nunca deveria ter sido
incorporado ao módulo de domínio.

#### Ação prescrita

