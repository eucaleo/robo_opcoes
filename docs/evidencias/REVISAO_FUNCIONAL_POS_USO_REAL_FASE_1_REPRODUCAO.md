# REVISAO_FUNCIONAL_POS_USO_REAL_FASE_1_REPRODUCAO

## Objetivo

Confirmar o estado atual dos problemas em ambiente local antes de qualquer correcao funcional.

## Estado de referencia

- Data de criacao: 2026-06-22 13:22:21
- Branch atual: fase-3a4-auto-pricing-manual-save
- Commit base: bce681f docs: consolida checklist de entrega da fase 7

## Regra da fase

Esta fase e apenas de reproducao, observacao e registro. Nenhuma correcao funcional deve ser feita antes do encerramento desta evidencia.

## Preparacao

### Banco de dados

- Estado antes dos testes: a preencher.
- Tabelas verificadas antes dos testes: a preencher.
- Estruturas existentes antes dos testes: a preencher.
- Observacoes relevantes: a preencher.

### Sistema

- Forma de execucao do sistema: a preencher.
- Usuario ou ambiente de teste: a preencher.
- RTD conectado: sim, nao ou nao aplicavel.
- Horario local do teste: a preencher.
- Observacao sobre timezone: a preencher.

## Teste 1 - Cadastro manual com ponto decimal

### Passos

- Criar estrutura manual usando ponto decimal.
- Aplicar leg.
- Salvar estrutura.
- Verificar listagem.
- Verificar detalhes.

### Resultado esperado

- Estrutura salva sem erro.
- Legs exibidas corretamente.
- Dados numericos persistidos corretamente.

### Resultado observado

A preencher.

### Evidencia

A preencher.

### Status

Pendente.

## Teste 2 - Cadastro manual com virgula decimal

### Passos

- Criar estrutura manual usando virgula decimal.
- Aplicar leg.
- Salvar estrutura.
- Verificar listagem.
- Verificar detalhes.

### Resultado esperado

- Sistema aceita virgula decimal em valores validos.
- Mensagem strike must be numeric nao aparece para valores como 158,00.
- Dados numericos sao normalizados internamente.

### Resultado observado

A preencher.

### Evidencia

A preencher.

### Status

Pendente.

## Teste 3 - Payoff da estrutura recem-criada

### Passos

- Abrir estrutura recem-criada.
- Verificar se a curva de payoff aparece.
- Verificar se existem pontos em payoff_curve_points.
- Registrar se o filtro structure_id e mode canonical encontram a estrutura.

### Resultado esperado

- Estrutura valida gera curva de payoff.
- payoff_curve_points possui pontos vinculados ou o sistema informa motivo de rejeicao.

### Resultado observado

A preencher.

### Evidencia

A preencher.

### Status

Pendente.

## Teste 4 - Busca de decisoes da estrutura recem-criada

### Passos

- Executar busca de decisoes.
- Verificar se ha registros em structure_decisions.
- Verificar se a estrutura aparece no filtro de decisao.
- Comparar listagem de estruturas com filtro de decisao.

### Resultado esperado

- Estrutura valida participa da busca de decisoes.
- structure_decisions possui registros vinculados ou o sistema informa motivo de rejeicao.

### Resultado observado

A preencher.

### Evidencia

A preencher.

### Status

Pendente.

## Teste 5 - Botao Atualizar Dados

### Passos

- Clicar em Atualizar Dados.
- Registrar feedback imediato.
- Registrar mensagem final.
- Verificar se houve pipeline.
- Verificar se houve RTD.
- Verificar se houve payoff.
- Verificar se houve decisoes.
- Verificar se a tela atualizou.

### Resultado esperado

- Sistema informa estruturas lidas, processadas, ignoradas, decisoes geradas, pontos de payoff gerados, cotacoes RTD atualizadas, avisos e erros.
- Se nada for gerado, o sistema informa que nenhum dado novo foi produzido.

### Resultado observado

A preencher.

### Evidencia

A preencher.

### Status

Pendente.

## Teste 6 - RTD com conexao aberta

### Passos

- Confirmar conexao RTD aberta.
- Executar atualizacao.
- Verificar se rtd_option_quotes foi atualizada.
- Verificar horario da ultima atualizacao.
- Verificar se tela refletiu dados novos.

### Resultado esperado

- Coleta RTD executa.
- Sistema informa sucesso ou falha.
- Dados persistem ou limitacao e documentada claramente.

### Resultado observado

A preencher.

### Evidencia

A preencher.

### Status

Pendente.

## Teste 7 - Recalculo da estrutura nova

### Passos

- Abrir estrutura nova.
- Clicar em recalculo.
- Registrar mensagem exibida.
- Verificar se snapshot mudou.
- Verificar se houve atualizacao de dados.

### Resultado esperado

- Recalculo executa quando ha dado novo.
- Mensagem diferencia sem mudanca, execucao real e falha.

### Resultado observado

A preencher.

### Evidencia

A preencher.

### Status

Pendente.

## Teste 8 - Metricas financeiras

### Passos

- Abrir estrutura implantada.
- Verificar campos de metricas financeiras.
- Verificar se metricas dependem de RTD, payoff ou decisoes.
- Registrar campos vazios e possiveis causas.

### Resultado esperado

- Metricas sao preenchidas quando ha dados suficientes.
- Quando nao houver dados, o sistema informa o motivo.

### Resultado observado

A preencher.

### Evidencia

A preencher.

### Status

Pendente.

## Teste 9 - Duplicidade da estrutura numero 2

### Passos

- Verificar listagem de estruturas.
- Verificar se estrutura numero 2 aparece duplicada.
- Verificar filtro de decisao.
- Comparar origem dos dados da listagem e do filtro.

### Resultado esperado

- Estrutura aparece uma unica vez.
- Filtro de decisao usa mesma referencia funcional.
- Se houver duplicidade real, origem e documentada.

### Resultado observado

A preencher.

### Evidencia

A preencher.

### Status

Pendente.

## Teste 10 - Portugues Brasil

### Passos

- Navegar pelas telas principais.
- Registrar mensagens em ingles.
- Registrar comandos, decisoes e dados fora do padrao Portugues Brasil.
- Registrar mensagens tecnicas visiveis ao usuario.

### Resultado esperado

- Usuario final recebe mensagens claras em Portugues Brasil.

### Resultado observado

A preencher.

### Evidencia

A preencher.

### Status

Pendente.

## Teste 11 - Comentario do grafico de payoff

### Passos

- Abrir grafico de payoff.
- Verificar se ha comentario de ganho, perda, melhor regiao, pior regiao e equilibrio.
- Verificar mensagem quando nao houver payoff.

### Resultado esperado

- Payoff possui comentario interpretativo em Portugues Brasil ou informa motivo de ausencia.

### Resultado observado

A preencher.

### Evidencia

A preencher.

### Status

Pendente.

## Teste 12 - Visibilidade e atualizacao instantanea da estrutura implantada

### Passos

- Implantar ou abrir estrutura.
- Executar atualizacao.
- Observar carregamento, conclusao, erro e ausencia de dados novos.
- Verificar se posicao e metricas refletem o ultimo calculo.

### Resultado esperado

- Usuario ve quando atualizacao comeca, termina e o que mudou.
- Se nao houver mudanca, motivo fica claro.

### Resultado observado

A preencher.

### Evidencia

A preencher.

### Status

Pendente.

## Teste 13 - Chamada de aba ou alias

### Passos

- Buscar referencias a aba ou alias na interface, filtros, banco, servicos, documentacao e testes.
- Confirmar se ainda ha uso funcional.
- Registrar se a chamada e necessaria ou obsoleta.

### Resultado esperado

- Chamada obsoleta e removida em fase propria ou uso e justificado.

### Resultado observado

A preencher.

### Evidencia

A preencher.

### Status

Pendente.

## Conclusao da fase

### Problemas confirmados

A preencher.

### Problemas nao reproduzidos

A preencher.

### Estado do banco depois dos testes

A preencher.

### Logs relevantes

A preencher.

### Arquivos candidatos para analise nas proximas fases

A preencher.

### Pendencias

A preencher.

### Commit documental

Pendente.
