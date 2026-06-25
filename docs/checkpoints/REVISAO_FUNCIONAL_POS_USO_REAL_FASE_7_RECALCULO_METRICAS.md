# Revisão Funcional Pós Uso Real — Fase 7 — Recálculo, Snapshot e Métricas Financeiras

## Objetivo

Corrigir o comportamento em que o recálculo informa que o snapshot não mudou e as métricas financeiras não são preenchidas.

## Problemas tratados

- Recálculo da estrutura nova retorna mensagem de recálculo desnecessário.
- Snapshot não muda.
- Métricas financeiras ficam vazias.
- Estrutura implantada não atualiza dados corretamente.
- Sistema pode não diferenciar ausência de dados, falha e execução real.

## Documento de origem

Rota:

- NOVA_ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.pdf

Documento desta fase:

- docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_7_RECALCULO_METRICAS.md

Evidência de buscas:

- docs/evidencias/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_7_BUSCAS.txt

## Commit base

Commit base informado ao início da fase:

- 05111e1 Atualiza planilha RTD

## Pontos a revisar

Conforme rota, os pontos obrigatórios desta fase são:

- Critério de comparação de snapshot.
- Data e hora de atualização.
- Dependência de RTD.
- Dependência de payoff.
- Dependência de decisões.
- Serviço de métricas financeiras.
- Campos obrigatórios para cálculo das métricas.
- Fluxo após implantação de estrutura.

## Hipóteses iniciais

As hipóteses que devem ser confirmadas ou descartadas nesta fase são:

- O snapshot pode estar comparando apenas dados estáticos da estrutura, ignorando cotações atualizadas.
- O recálculo pode estar sendo abortado antes de atualizar payoff, decisões ou métricas.
- A estrutura nova pode não estar recebendo horário de atualização adequado.
- As métricas financeiras podem depender de campos que não estão preenchidos após cadastro manual ou assistido.
- O pipeline pode considerar ausência de alteração como sucesso, mesmo quando faltam métricas.
- A mensagem exibida ao usuário pode estar correta tecnicamente, mas insuficiente funcionalmente.

## Critérios de aceite

| Critério | Status | Evidência |
|---|---:|---|
| Estrutura nova implantada atualiza dados | Pendente | A validar |
| Recálculo executa quando há dado novo | Pendente | A validar |
| Mensagem diferencia sem mudança, falha e execução real | Pendente | A validar |
| Métricas financeiras são preenchidas quando há dados suficientes | Pendente | A validar |
| Quando não houver dados, sistema informa o motivo | Pendente | A validar |
| Testes automatizados aprovados | Pendente | A executar |
| Auditoria viva atualizada | Pendente | A atualizar |
| Commit gerado | Pendente | A gerar após validação |

## Plano de execução

### Etapa 1 — Buscar arquivos relacionados

Gerar evidência com buscas por:

- recálculo;
- snapshot;
- métricas financeiras;
- atualização;
- implantação;
- payoff;
- decisões.

Resultado esperado:

- Lista de arquivos e pontos de entrada para análise.

### Etapa 2 — Identificar fluxo real do recálculo

Confirmar:

- onde o botão ou ação de recálculo chama o serviço;
- quais dados entram no snapshot;
- qual critério define que o snapshot mudou ou não mudou;
- onde a mensagem ao usuário é gerada.

Resultado esperado:

- Fluxo documentado.
- Causa provável identificada.

### Etapa 3 — Identificar fluxo real das métricas financeiras

Confirmar:

- qual serviço calcula métricas;
- quais campos são obrigatórios;
- quais tabelas recebem os resultados;
- quais condições fazem as métricas ficarem vazias;
- se há dependência de RTD, payoff ou decisões.

Resultado esperado:

- Campos obrigatórios mapeados.
- Motivos de ausência documentados.

### Etapa 4 — Teste antes da correção

Registrar comportamento atual:

- estrutura usada no teste;
- mensagem exibida ao recalcular;
- snapshot antes;
- snapshot depois;
- métricas antes;
- métricas depois;
- registros de payoff;
- registros de decisões;
- cotações RTD disponíveis.

Resultado esperado:

- Problema reproduzido ou limitação documentada.

### Etapa 5 — Correção

A correção só deve ser feita depois das buscas e da reprodução controlada.

Regras:

- Não migrar para web.
- Não alterar fora do escopo.
- Não remover histórico documental.
- Toda alteração deve ser testada.
- Gerar arquivo inteiro quando houver alteração de código.
- Commitar após validação.

### Etapa 6 — Testes

Testes mínimos esperados:

- teste focado em recálculo;
- teste focado em snapshot;
- teste focado em métricas financeiras;
- teste de pipeline se houver integração;
- suíte completa.

### Etapa 7 — Encerramento

A fase só será encerrada quando:

- comportamento estiver corrigido ou limitação estiver documentada;
- critérios de aceite estiverem preenchidos;
- auditoria viva estiver atualizada;
- testes estiverem aprovados;
- commit estiver criado.

## Resultado parcial

Fase iniciada.

Nenhuma alteração funcional realizada neste documento inicial.
