# REVISAO FUNCIONAL POS USO REAL - PLANO DE EXECUCAO

Data base da nova fase: 2026-06-22
Data de consolidacao deste plano: 2026-06-23
Branch de trabalho: reinicio-normalizacao-idioma-ptbr

## Objetivo

Transformar a rota de revisao funcional pos uso real em um plano executavel por fases, mantendo rastreabilidade, testes, auditoria viva e commits por etapa.

## Fase 1 - Reproducao controlada

Objetivo: confirmar o estado atual antes de corrigir.

Documento de evidencia:

- docs/evidencias/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_1_REPRODUCAO.md

Testes manuais a registrar:

1. Criar estrutura usando ponto decimal.
2. Criar estrutura usando virgula decimal.
3. Aplicar leg.
4. Salvar estrutura.
5. Verificar listagem.
6. Verificar detalhes.
7. Abrir estrutura recem-criada.
8. Verificar se a curva de payoff aparece.
9. Verificar se ha pontos em payoff_curve_points.
10. Executar busca de decisoes.
11. Verificar se ha registros em structure_decisions.
12. Clicar em Atualizar Dados.
13. Registrar mensagem exibida.
14. Verificar se houve pipeline.
15. Verificar se houve RTD.
16. Verificar se houve payoff.
17. Verificar se houve decisoes.
18. Testar RTD com conexao aberta, se disponivel.
19. Verificar se rtd_option_quotes foi atualizada.

Saida esperada:

1. Lista de problemas confirmados.
2. Lista de problemas nao reproduzidos.
3. Evidencia manual.
4. Estado do banco antes e depois.
5. Commit documental.

## Fase 2 - Correcao da normalizacao numerica

Objetivo: aceitar formato brasileiro e formato tecnico.

Problemas tratados:

1. Valor como 158,00 gera erro de campo numerico.
2. Sistema aceita 158.00, mas falha com virgula.
3. Aplicar leg e salvar precisam aceitar virgula.

Documento:

- docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_2_NORMALIZACAO_NUMERICA.md

Antes de alterar, buscar:

1. Validadores de strike.
2. Validadores de preco.
3. Conversores numericos.
4. Formularios de cadastro manual.
5. Handler do botao Aplicar Leg.
6. Handler do botao Salvar.

Criterios de aceite:

1. Aceitar 10,50.
2. Aceitar 10.50.
3. Aceitar 1.234,56.
4. Aceitar 1234,56.
5. Aceitar 1234.56.
6. Rejeitar texto invalido.
7. Exibir mensagem clara em Portugues Brasil.
8. Ter testes cobrindo virgula e ponto.

## Fase 3 - Cadastro assistido de estrutura

Objetivo: o usuario informa apenas os campos principais e o sistema preenche o restante pelo simbolo da opcao.

Documento:

- docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_3_CADASTRO_ASSISTIDO.md

Campos informados pelo usuario:

1. Nome da estrutura.
2. Lado: compra ou venda.
3. Tipo: put ou call.
4. Quantidade executada.
5. Valor executado.
6. Simbolo da opcao.

Campos preenchidos pelo sistema:

1. Ativo objeto.
2. Strike.
3. Vencimento.
4. Multiplicador.
5. Metadados necessarios para payoff.
6. Metadados necessarios para decisoes.

Criterios de aceite:

1. Simbolo reconhecido preenche dados automaticamente.
2. Simbolo nao encontrado gera mensagem clara.
3. Divergencia entre tipo informado e tipo detectado bloqueia ou pede confirmacao.
4. Estrutura so pode ser salva como funcional se tiver dados minimos.
5. Teste manual ou automatizado registrado.

## Fase 4 - Integracao da estrutura manual com payoff e decisoes

Objetivo: garantir que estrutura criada manualmente seja funcional.

Documento:

- docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_4_PAYOFF_DECISOES.md

Pontos a investigar:

1. Tabela principal de estruturas.
2. Tabela de legs.
3. Relacao structure_id.
4. Filtro mode canonical.
5. Campos obrigatorios para payoff.
6. Campos obrigatorios para decisoes.
7. Normalizacao de comprado e vendido.
8. Status active.
9. Motivo de rejeicao no pipeline.

Criterios de aceite:

1. Estrutura manual valida gera curva de payoff.
2. Estrutura manual valida gera decisoes.
3. structure_decisions recebe registros ou informa rejeicao.
4. payoff_curve_points recebe pontos ou informa rejeicao.
5. Sistema mostra motivo claro quando faltar dado.
6. Logs indicam estruturas lidas, processadas, ignoradas e rejeitadas.

## Fase 5 - Botao Atualizar Dados e resumo do pipeline

Objetivo: transformar o botao Atualizar Dados em acao rastreavel e compreensivel.

Documento:

- docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_5_ATUALIZAR_DADOS_PIPELINE.md

Feedback esperado:

1. Estruturas lidas.
2. Estruturas processadas.
3. Estruturas ignoradas.
4. Decisoes geradas.
5. Pontos de payoff gerados.
6. Cotacoes RTD atualizadas.
7. Avisos.
8. Erros.

Regra importante:

Se tudo retornar zero, nao deve mostrar apenas sucesso. Deve informar que o pipeline executou, mas nenhum dado novo foi gerado.

## Fase 6 - Execucao RTD

Objetivo: garantir que conexao RTD aberta resulte em coleta efetiva.

Documento:

- docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_6_RTD.md

Pontos a revisar:

1. Adaptador RTD.
2. Servico de atualizacao RTD.
3. Integracao com botao Atualizar Dados.
4. Persistencia em rtd_option_quotes.
5. Normalizacao de tickers.
6. Atualizacao da tela apos coleta.
7. Mensagem quando RTD nao retorna dados.

Criterios de aceite:

1. Com RTD conectado, coleta e executada.
2. Sistema informa sucesso ou falha.
3. Sistema informa quantos registros foram atualizados.
4. Dados persistem no banco.
5. Tela mostra dados novos ou horario da ultima atualizacao.
6. Logs permitem diagnostico.

## Fase 7 - Recalculo, snapshot e metricas financeiras

Objetivo: corrigir o comportamento em que o recalculo informa que o snapshot nao mudou e as metricas financeiras nao sao preenchidas.

Documento:

- docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_7_RECALCULO_METRICAS.md

Pontos a revisar:

1. Criterio de comparacao de snapshot.
2. Data e hora de atualizacao.
3. Dependencia de RTD.
4. Dependencia de payoff.
5. Dependencia de decisoes.
6. Servico de metricas financeiras.
7. Campos obrigatorios para calculo das metricas.
8. Fluxo apos implantacao de estrutura.

Criterios de aceite:

1. Estrutura nova implantada atualiza dados.
2. Recalculo executa quando ha dado novo.
3. Mensagem diferencia sem mudanca, falha e execucao real.
4. Metricas financeiras sao preenchidas quando ha dados suficientes.
5. Quando nao houver dados, o sistema informa o motivo.

## Fase 8 - Duplicidade da estrutura numero 2

Objetivo: eliminar duplicidade visual e inconsistencia entre listagem e filtro de decisao.

Documento:

- docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_8_DUPLICIDADE_ESTRUTURA.md

Pontos a revisar:

1. Consulta da listagem de estruturas.
2. Consulta do filtro de decisao.
3. Criterio de unicidade.
4. Fonte usada pela UI.
5. Fonte usada pelo motor de decisao.
6. Possivel duplicidade entre estrutura manual e estrutura consolidada.
7. Uso de alias, canonical ID ou snapshot.

Criterios de aceite:

1. Estrutura aparece uma unica vez na listagem.
2. Filtro de decisao usa a mesma referencia funcional.
3. Nao ha perda de dados.
4. Se houver duplicidade real no banco, sistema indica origem ou consolida conforme regra definida.

## Fase 9 - Normalizacao para Portugues Brasil

Objetivo: padronizar comandos, decisoes, mensagens, dados exibidos e textos de interface para Portugues Brasil.

Documento:

- docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_9_PORTUGUES_BRASIL.md

Escopo:

1. Mensagens de erro.
2. Mensagens de sucesso.
3. Botoes.
4. Status.
5. Decisoes.
6. Descricoes de payoff.
7. Alertas.
8. Logs visiveis ao usuario.

Criterios de aceite:

1. Usuario final nao ve mensagens tecnicas em ingles.
2. Mensagens tecnicas internas podem permanecer em log.
3. Erros de validacao sao claros.
4. Status e decisoes usam vocabulario padronizado.

## Fase 10 - Comentario do grafico de payoff

Objetivo: adicionar interpretacao textual ao grafico de payoff.

Documento:

- docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_10_COMENTARIO_PAYOFF.md

Comentarios esperados:

1. Regiao de ganho.
2. Regiao de perda.
3. Melhor regiao para ganho.
4. Pior regiao.
5. Ponto ou faixa de equilibrio, se calculavel.
6. Situacao atual em relacao ao preco do ativo.
7. Alerta quando dados forem insuficientes.

## Fase 11 - Visibilidade da estrutura implantada e atualizacao instantanea

Objetivo: melhorar a experiencia da estrutura implantada, refletindo atualizacao automatica semelhante ao comportamento esperado no Excel.

Documento:

- docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_11_VISIBILIDADE_ATUALIZACAO.md

Pontos a revisar:

1. Atualizacao da tela apos RTD.
2. Atualizacao da tela apos recalculo.
3. Atualizacao da tela apos pipeline.
4. Horario da ultima atualizacao.
5. Estado visual de carregamento.
6. Estado visual de erro.
7. Estado visual sem dados novos.

Criterios de aceite:

1. Usuario ve quando atualizacao comeca.
2. Usuario ve quando termina.
3. Usuario ve o que mudou.
4. Dados da estrutura refletem o ultimo calculo.
5. Se nao houver mudanca, o motivo fica claro.

## Fase 12 - Remocao de chamada obsoleta de aba ou alias

Objetivo: eliminar referencia a aba ou alias se o sistema deixou de usar abas.

Documento:

- docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_12_ABA_ALIAS.md

Pontos a revisar:

1. Textos de interface.
2. Filtros.
3. Campos de banco.
4. Servicos.
5. Documentacao.
6. Testes.
7. Referencias historicas.

Criterios de aceite:

1. Se aba ou alias ainda for necessario, justificar.
2. Se for obsoleto, remover da chamada funcional.
3. Nao remover historico documental sem necessidade.
4. Sistema nao deve exibir conceito inexistente ao usuario.

## Fase 13 - Validacao integrada

Objetivo: garantir que as correcoes nao quebraram fases anteriores.

Documento:

- docs/evidencias/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_13_VALIDACAO_INTEGRADA.md

Testes obrigatorios:

1. Testes automatizados existentes.
2. Compilacao.
3. Cadastro manual com virgula.
4. Cadastro manual com ponto.
5. Cadastro assistido por simbolo.
6. Payoff.
7. Busca de decisoes.
8. Atualizar Dados.
9. RTD com conexao aberta, se disponivel.
10. RTD com mock ou simulacao, se ambiente externo nao estiver disponivel.
11. Recalculo.
12. Metricas financeiras.
13. Duplicidade de estrutura.
14. Mensagens em Portugues Brasil.
15. Comentario de payoff.
16. Atualizacao visual da estrutura.

Comandos previstos de validacao:

1. python -m pytest ATT/tests -q
2. python -m compileall repositories services domain ATT/tests

## Fase 14 - Fechamento documental da rota

Objetivo: encerrar a revisao funcional pos uso real com rastreabilidade completa.

Documentos:

- docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FECHAMENTO.md
- docs/checklists/CHECKLIST_REVISAO_FUNCIONAL_POS_USO_REAL.md
- docs/decisoes/DECISOES_REVISAO_FUNCIONAL_POS_USO_REAL.md

Checklist final:

1. Virgula em strike aceita e testada.
2. Virgula em preco aceita e testada.
3. Cadastro manual funcional.
4. Cadastro assistido busca dados pelo simbolo.
5. Payoff gerado para estrutura valida.
6. Decisoes geradas para estrutura valida.
7. Atualizar Dados com feedback detalhado.
8. RTD executa ou tem limitacao documentada.
9. Metricas financeiras preenchidas ou motivo informado.
10. Recalculo com mensagem coerente.
11. Duplicidade corrigida ou causa documentada.
12. Portugues Brasil normalizado na interface.
13. Comentario de payoff disponivel.
14. Atualizacao visual rastreavel.
15. Aba ou alias removido ou justificado.
16. Testes executados.
17. Auditoria atualizada.
18. Commits criados por fase.
