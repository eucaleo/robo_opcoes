# Plano de fases da frente RTD Excel BTG Online

## Fase 0: Auditoria e documentação

Status inicial: em abertura.

Objetivo:

- Criar documentação da frente.
- Gerar relatórios de busca.
- Mapear código existente.
- Evitar código morto ou duplicado.

Critérios de conclusão:

- Relatórios de auditoria gerados.
- Inventário inicial revisado.
- Nenhuma alteração funcional sem entendimento prévio.
- Commit da documentação inicial realizado.

## Fase 1: Excel RTD vivo

Objetivo:

- Detectar Excel aberto.
- Detectar `LISTA_RTD.xlsm`.
- Validar aba e campos obrigatórios.
- Ler tabela viva em bloco.
- Exibir status básico na UI ou log operacional.

Critérios de teste:

- Sistema identifica Excel aberto.
- Sistema identifica planilha correta.
- Sistema falha de forma controlada quando Excel está fechado.
- Sistema não trava se RTD estiver indisponível.

## Fase 2: Snapshot centralizado

Objetivo:

- Criar ou adaptar tabela de snapshot atual por símbolo.
- Atualizar por sobrescrita.
- Normalizar campos em camada única.
- Direcionar preenchimento de legs para o snapshot.

Critérios de teste:

- Uma linha por símbolo.
- Atualização não duplica registros.
- Legs conseguem preencher dados pelo snapshot.
- Código antigo sob demanda fica removido ou isolado como fallback documentado.

## Fase 3: Histórico intraday

Objetivo:

- Gravar pontos temporais relevantes.
- Controlar frequência.
- Evitar crescimento exagerado.

Critérios de teste:

- Não grava linhas idênticas sem necessidade.
- Respeita limite por intervalo.
- Grava timestamp, símbolo, preço, VWAP, bid, ask e volume quando disponíveis.

## Fase 4: Candles

Objetivo:

- Consolidar candles de 1 minuto.
- Associar VWAP ao candle.
- Preparar 5 e 15 minutos.

Critérios de teste:

- Candle possui abertura, máxima, mínima, fechamento.
- VWAP é associado.
- Volume é calculado conforme disponibilidade da fonte.
- Candle de opção sintético é marcado quando usar mid price.

## Fase 5: UI operacional

Objetivo:

- Atualizar painel, legs, estruturas e gráficos com limite de redesenho.
- Mostrar status RTD/Excel/corretora/dados.

Critérios de teste:

- UI não trava com atualizações frequentes.
- Atualização visual é limitada.
- Status mostra atraso e erros de símbolo.

## Fase 6: Retenção e manutenção

Objetivo:

- Limpar ticks brutos antigos.
- Manter candles consolidados.
- Compactar banco quando necessário.

Critérios de teste:

- Rotina preserva candles.
- Rotina remove apenas dados elegíveis.
- Banco continua íntegro após manutenção.

## Fase 7: Alertas e decisão operacional

Objetivo:

- Criar alertas baseados em VWAP, spread, liquidez, payoff e estrutura.

Critérios de teste:

- Alertas são reproduzíveis.
- Alertas não disparam em duplicidade sem mudança relevante.
- Eventos ficam auditáveis.
