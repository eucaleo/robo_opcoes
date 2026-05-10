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
