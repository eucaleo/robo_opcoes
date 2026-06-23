# NOVA ROTA REVISAO FUNCIONAL POS USO REAL

Data de congelamento: 2026-06-22
Data de retomada operacional: 2026-06-23
Branch de trabalho: reinicio-normalizacao-idioma-ptbr

## Origem da rota

Esta rota foi criada a partir da segunda revisao de testes com o sistema em funcionamento, com base no uso real do sistema e nos problemas observados na implantacao, atualizacao, recalculo, RTD, metricas financeiras, duplicidade de estrutura, normalizacao para Portugues Brasil, payoff e remocao de chamadas obsoletas de aba ou alias.

A Fase 7 documental anterior fica pausada como empacotamento. A prioridade passa a ser a revisao funcional pos uso real.

## Problemas identificados no uso real

1. Sistema nao atualiza dados na implantacao da estrutura conforme solicitado.
2. Ao clicar em recalculo na estrutura nova, o sistema apresenta mensagem de snapshot nao mudou e recalculo desnecessario.
3. Estrutura aparentemente nao atualiza automaticamente via RTD.
4. Dados de metricas financeiras nao sao preenchidos.
5. Sistema mostra duplicidade na estrutura numero 2 na listagem, mas a duplicidade nao aparece no filtro de decisao.
6. E necessario normalizar comandos, decisoes, dados, mensagens e interface para Portugues Brasil.
7. E necessario adicionar comentario de posicao do grafico de payoff, indicando ganho, perda, melhor regiao para ganho e demais interpretacoes possiveis.
8. E necessario melhorar a visibilidade da estrutura implantada com atualizacao de posicao e atualizacao automatica instantanea, semelhante ao comportamento esperado no Excel.
9. Existe descricao de aba ou alias, mas o sistema deixou de usar abas; se a chamada estiver obsoleta, deve ser eliminada.

## Decisoes fixadas

1. Nao migrar para web.
2. Nao utilizar emojis.
3. Manter o trabalho dentro do escopo do projeto.
4. Efetuar buscas de dados, arquivos e historico Git antes de alteracoes.
5. Toda mudanca deve ser testada apos concluida.
6. Apos o encerramento de fase, o teste deve compor todas as fases encerradas.
7. Evitar codigos intermediarios em explicacoes e ir direto ao ponto.
8. Em alteracoes de codigo, trabalhar com o arquivo inteiro quando necessario.
9. A cada alteracao concluida e testada, commitar.
10. Nao codar sem rumo; se necessario, buscar a evolucao no Git.
11. Manter arquivo de auditoria vivo atualizado com testes, conclusoes e caminho de evolucao.
12. Nao gerar codigo com crase dentro dos arquivos do projeto.

## Escopo permitido

1. Reproducao controlada dos problemas observados no uso real.
2. Normalizacao numerica para aceitar formatos brasileiros e tecnicos.
3. Cadastro assistido de estrutura com preenchimento automatico por simbolo de opcao.
4. Integracao de estruturas manuais com payoff e decisoes.
5. Melhorias no botao Atualizar Dados e no resumo do pipeline.
6. Validacao e correcao da execucao RTD.
7. Correcao de recalculo, snapshot e metricas financeiras.
8. Correcao ou justificativa de duplicidade de estrutura.
9. Normalizacao para Portugues Brasil.
10. Comentario textual do grafico de payoff.
11. Visibilidade e atualizacao instantanea da estrutura implantada.
12. Remocao ou justificativa de chamadas obsoletas de aba ou alias.
13. Validacao integrada.
14. Fechamento documental da rota.

## Escopo proibido

1. Migrar o sistema para web.
2. Alterar arquitetura fora da necessidade direta da rota.
3. Introduzir funcionalidades nao relacionadas aos problemas listados.
4. Remover historico documental sem justificativa.
5. Exibir conceitos obsoletos ao usuario final, como aba ou alias, se nao forem mais funcionais.
6. Fazer alteracoes sem busca previa e sem teste posterior.
7. Encerrar fase sem atualizar a auditoria viva.

## Ordem de execucao

1. Marco 0: congelamento da nova rota.
2. Marco 1: auditoria viva da revisao funcional.
3. Marco 2: plano operacional da revisao.
4. Fase 1: reproducao controlada.
5. Fase 2: correcao da normalizacao numerica.
6. Fase 3: cadastro assistido de estrutura.
7. Fase 4: integracao da estrutura manual com payoff e decisoes.
8. Fase 5: botao Atualizar Dados e resumo do pipeline.
9. Fase 6: execucao RTD.
10. Fase 7: recalculo, snapshot e metricas financeiras.
11. Fase 8: duplicidade da estrutura numero 2.
12. Fase 9: normalizacao para Portugues Brasil.
13. Fase 10: comentario do grafico de payoff.
14. Fase 11: visibilidade da estrutura implantada e atualizacao instantanea.
15. Fase 12: remocao de chamada obsoleta de aba ou alias.
16. Fase 13: validacao integrada.
17. Fase 14: fechamento documental da rota.

## Criterio de encerramento

A rota somente pode ser encerrada quando:

1. Todos os problemas confirmados no uso real forem corrigidos ou documentados com limitacao explicita.
2. Todas as fases tiverem evidencia.
3. A auditoria viva estiver atualizada.
4. Os testes automatizados existentes forem executados.
5. A compilacao estiver sem erro.
6. A validacao integrada estiver registrada.
7. Os commits forem criados por fase.
8. O checklist final estiver concluido.
