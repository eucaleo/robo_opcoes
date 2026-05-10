# Roteiro de Migração de Estruturas

## Objetivo
Migrar criação/edição de estruturas para o sistema, deixando RTD/Excel apenas como ponte para dados de mercado.

## Estado atual confirmado
- Pipeline atual: Excel/RTD -> CSV bridge -> data/app.db -> domínio -> data/derived.db -> UI
- UI não lê Excel diretamente
- Domínio legado atual ainda está acoplado a `aba + timestamp`
- Leitura de legs validada via `RoboLegsRepository`
- Fontes atuais identificadas:
  - manual_analise_robo_legs
  - RTD/raw legado
- Política de precedência validada:
  - manual_then_rtd
  - manual_only
  - rtd_only

## Campos mínimos de leg já confirmados no legado
- aba
- ativo
- vencimento
- strike
- quant
- call_put
- cv
- timestamp
- fonte

## Observações da Fase 1
- `aba` hoje funciona como agrupador/identidade operacional no legado
- `timestamp` participa da chave de leitura
- Há distinção entre fonte manual e RTD
- `list_timestamps()` foi corrigido para respeitar a semântica por fonte
- Parsing numérico e leitura de legs foram estabilizados

## Riscos / acoplamentos identificados
- acoplamento do domínio à chave `aba + timestamp`
- estrutura ainda modelada indiretamente a partir do raw legado
- necessidade de separar canonicamente:
  - Estrutura
  - Snapshot de mercado

## Fase 2 — Modelo Canônico de Estrutura

### Objetivo
Definir uma entidade de estrutura independente de Excel, RTD e da chave legado `aba + timestamp`.

### Entidade Structure
Campos propostos:
- id
- name
- underlying_asset
- alias_legacy_aba
- status
- notes
- created_at
- updated_at

### Entidade StructureLeg
Campos propostos:
- id
- structure_id
- position_side
- option_type
- symbol
- strike
- expiration_date
- quantity
- premium
- multiplier
- leg_order
- notes
- created_at
- updated_at

### Regras de identidade
- `Structure.id` é a chave primária real do sistema
- `alias_legacy_aba` existe apenas para compatibilidade com o legado
- `aba` não deve ser usada como chave primária do modelo novo
- `timestamp` não faz parte da identidade da estrutura

### Regras de normalização
- `option_type`: armazenar apenas `CALL` ou `PUT`
- `position_side`: armazenar apenas `LONG` ou `SHORT`
- legado: `C` -> `LONG`, `V` -> `SHORT`
- `quantity`: inteiro positivo
- `strike`: decimal normalizado
- `expiration_date`: data válida e normalizada

### Separação estrutural obrigatória
- Estrutura = definição da operação
- Snapshot = estado de mercado em um instante
- O pipeline futuro deve combinar:
  - Structure
  - MarketSnapshot
  para gerar derivados

### Decisões da Fase 2
- o modelo novo não depende de Excel
- o modelo novo não usa `aba + timestamp` como identidade
- a compatibilidade com o legado será mantida via `alias_legacy_aba`

### Proposta inicial de persistência
Tabela `structures`:
- id
- name
- underlying_asset
- alias_legacy_aba
- status
- notes
- created_at
- updated_at

Tabela `structure_legs`:
- id
- structure_id
- position_side
- option_type
- symbol
- strike
- expiration_date
- quantity
- premium
- multiplier
- leg_order
- notes
- created_at
- updated_at
