# Decisões técnicas

## Decisão 1: Excel como ponte viva

Status: proposta aprovada como direção da frente.

Decisão:

- O Excel `LISTA_RTD.xlsm` ficará aberto durante o uso do sistema.
- O sistema Python observará a tabela viva.
- O RTD não será consultado sob demanda por símbolo.

Motivo:

- Reduz subprocessos.
- Reduz espera.
- Reduz risco de travamento.
- Permite UI viva, snapshot e histórico.

## Decisão 2: Snapshot separado de histórico

Status: proposta aprovada como direção da frente.

Decisão:

- Snapshot guarda último estado por símbolo.
- Histórico guarda pontos relevantes no tempo.

Motivo:

- Evita crescimento infinito do banco.
- Mantém UI rápida.
- Permite candles, replay e auditoria.

## Decisão 3: Candles gerados internamente

Status: proposta aprovada como direção da frente.

Decisão:

- O sistema gerará candles a partir dos snapshots/pontos históricos.
- O gráfico será desenhado a partir dos dados, não de imagem.

Motivo:

- Permite indicadores.
- Permite replay.
- Permite backtest.
- Permite auditoria.

## Decisão 4: Desenvolvimento sem dívida técnica

Status: regra obrigatória.

Decisão:

- Antes de alterar, auditar.
- Depois de alterar, testar.
- Depois de testar, commitar.
- Código morto deve ser removido ou documentado como fallback temporário.
