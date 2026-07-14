# Checklist de testes da frente RTD Excel BTG Online

## Testes acumulativos

A cada fase concluída, os testes anteriores devem continuar compondo a validação.

## Fase 0

- Documentação criada.
- Auditoria gerada.
- Git sem alterações inesperadas.
- Commit realizado.

## Fase 1

- Excel fechado: sistema detecta e informa erro controlado.
- Excel aberto sem planilha correta: sistema detecta.
- Excel aberto com `LISTA_RTD.xlsm`: sistema detecta.
- Aba RTD ausente: sistema detecta.
- Campos obrigatórios ausentes: sistema detecta.
- Leitura em bloco funciona.
- Sistema não usa subprocesso para consulta individual.

## Fase 2

- Snapshot cria ou atualiza uma linha por símbolo.
- Snapshot não duplica símbolo.
- Campos são normalizados.
- Legs leem do snapshot.
- Estruturas conseguem consumir snapshot.

## Fase 3

- Histórico grava ponto relevante.
- Histórico respeita limite de frequência.
- Histórico não grava ruído infinito.
- Banco permanece íntegro.

## Fase 4

- Candle de 1 minuto é gerado.
- VWAP é associado ao candle.
- Volume é tratado corretamente.
- Candle sintético de opção é marcado quando usar mid price.

## Fase 5

- UI atualiza sem travar.
- Painel mostra status.
- Legs atualizam com dados vivos.
- Gráfico não redesenha em excesso.

## Fase 6

- Ticks antigos são limpos.
- Candles são preservados.
- Banco é compactado quando aplicável.
- Integridade do banco continua ok.

## Fase 7

- Alertas disparam corretamente.
- Alertas não duplicam sem mudança relevante.
- Alertas ficam auditáveis.
