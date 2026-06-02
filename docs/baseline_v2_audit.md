<!-- docs/baseline_v2_audit.md -->
# Baseline v2 — Auditoria e Inventário

**Gerado em:** 2026-05-27  
**Projeto:** ATT — Análise de Estruturas de Opções  
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
| StructuresRepository | `repositories/structures_repository.py` | ✅ v2 |
| RoboLegsRepository | `repositories/robo_legs_repository.py` | ✅ |
| RoboLegsStatusRepository | `repositories/robo_legs_status_repository.py` | ✅ |
| PricingExecutionsRepository | `repositories/pricing_executions_repository.py` | ✅ |
| MarketSnapshotRepository | `repositories/market_snapshot_repository.py` | ⏳ patch_12 |

---

## 4. Serviços — Fase 3A

| Serviço | Status |
|---------|--------|
| `structure_input_mapper.py` | ✅ |
| `market_snapshot_provider.py` | ✅ |
| `canonical_input_service.py` | ✅ |
| `pricing_execution_service.py` | ✅ |
| `pricing_execution_app_service.py` | ✅ |

---

## 5. Camada de Domínio

| Módulo | Arquivo | Status |
|--------|---------|--------|
| Contratos canônicos | `domain/contracts.py` | ✅ |
| Validadores canônicos | `domain/canonical_validators.py` | ✅ |
| Payoff | `domain/payoff.py` | ✅ |
| Payoff features | `domain/payoff_features.py` | ✅ |
| Decision | `domain/decision.py` | ✅ |
| Structure metrics | `domain/structure_metrics.py` | ✅ |
| MarketSnapshot | `domain/market_snapshot.py` | ⏳ patch_12 |

---

## 6. Dívida Técnica Conhecida

- 16 arquivos `.bak` em `BAK/` e `repositories/` — candidatos a remoção após validação
- 7 bancos `.db` soltos em `BAK/` — backups históricos, não usados em produção
- `patch_12` e `patch_13` pendentes (MarketSnapshot canônico)

---

## 7. Patches Aplicados

| Patch | Descrição | Status |
|-------|-----------|--------|
| patch_01 | Auditoria baseline_v2 | ✅ |
| patch_02 | Contratos canônicos de structures | ✅ |
| patch_03 | Camada de compatibilidade legado | ✅ |
| patch_04 | CRUD canônico StructuresRepository | ✅ |
| patch_05 | Testes smoke/contrato | ✅ |
| patch_06 | Normalização repositories | ✅ |
| patch_10 | Smoke tests pytest (19 testes) | ✅ |
| patch_11 | conn.close() explícito (ResourceWarning) | ✅ |
| patch_12 | MarketSnapshot repositório + domínio | ⏳ |
| patch_13 | Política timestamp canônico | ⏳ |
