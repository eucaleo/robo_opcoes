<!-- docs/baseline_v2_audit.md -->
# Baseline v2 -- Auditoria e Inventário

**Gerado em:** 2026-05-27  
**Projeto:** ATT -- Análise de Estruturas de Opções  
**Raiz:** `C:\Users\eucal\projeto`

---

## 1. Objetivo

Documentar o estado do projeto no momento da migração para a arquitetura v2,
com separação clara entre camada de domínio, repositórios canônicos e serviços.

---

## 2. Bancos de Dados

### `dados/app.db`
| Tabela | Descrição |
|--------|-----------|
| `structures` | Estruturas canônicas de opções |
| `structure_legs` | Legs vinculadas às structures |
| `rtd_analise_robo` | Snapshots RTD do robô |
| `rtd_analise_robo_legs` | Legs dos snapshots RTD |
| `manual_analise_robo_legs` | Legs inseridas manualmente |
| `rtd_analise_raiox` | Análise raio-x RTD |
| `rtd_configuracoes` | Configurações RTD |
| `rtd_consolidacoes` | Consolidações RTD |
| `rtd_encerramentos_manuais` | Encerramentos manuais |
| `rtd_hist_robo` | Histórico do robô |
| `rtd_rolls_detectados` | Rolls detectados automaticamente |

### `dados/derived.db`
| Tabela | Descrição |
|--------|-----------|
| `payoff_curve_points` | Pontos da curva de payoff |
| `payoff_curve_summary` | Resumo da curva de payoff |
| `structure_decisions` | Decisões por estrutura |

---

## 3. Repositórios Canônicos

| Repositório | Arquivo | Status |
|-------------|---------|--------|
| StructuresRepository | `repositories/structures_repository.py` | [OK] v2 |
| RoboLegsRepository | `repositories/robo_legs_repository.py` | [OK] |
| RoboLegsStatusRepository | `repositories/robo_legs_status_repository.py` | [OK] |
| PricingExecutionsRepository | `repositories/pricing_executions_repository.py` | [OK] |
| MarketSnapshotRepository | `repositories/market_snapshot_repository.py` |  patch_12 |

---

## 4. Serviços -- Fase 3A

| Serviço | Status |
|---------|--------|
| `structure_input_mapper.py` | [OK] |
| `market_snapshot_provider.py` | [OK] |
| `canonical_input_service.py` | [OK] |
| `pricing_execution_service.py` | [OK] |
| `pricing_execution_app_service.py` | [OK] |

---

## 5. Camada de Domínio

| Módulo | Arquivo | Status |
|--------|---------|--------|
| Contratos canônicos | `domain/contracts.py` | [OK] |
| Validadores canônicos | `domain/canonical_validators.py` | [OK] |
| Payoff | `domain/payoff.py` | [OK] |
| Payoff features | `domain/payoff_features.py` | [OK] |
| Decision | `domain/decision.py` | [OK] |
| Structure metrics | `domain/structure_metrics.py` | [OK] |
| MarketSnapshot | `domain/market_snapshot.py` |  patch_12 |

---

## 6. Dívida Técnica Conhecida

- 16 arquivos `.bak` em `BAK/` e `repositories/` -- candidatos a remoção após validação
- 7 bancos `.db` soltos em `BAK/` -- backups históricos, não usados em produção
- `patch_12` e `patch_13` pendentes (MarketSnapshot canônico)

---

## 7. Patches Aplicados

| Patch | Descrição | Status |
|-------|-----------|--------|
| patch_01 | Auditoria baseline_v2 | [OK] |
| patch_02 | Contratos canônicos de structures | [OK] |
| patch_03 | Camada de compatibilidade legado | [OK] |
| patch_04 | CRUD canônico StructuresRepository | [OK] |
| patch_05 | Testes smoke/contrato | [OK] |
| patch_06 | Normalização repositories | [OK] |
| patch_10 | Smoke tests pytest (19 testes) | [OK] |
| patch_11 | conn.close() explícito (ResourceWarning) | [OK] |
| patch_12 | MarketSnapshot repositório + domínio |  |
| patch_13 | Política timestamp canônico |  |
