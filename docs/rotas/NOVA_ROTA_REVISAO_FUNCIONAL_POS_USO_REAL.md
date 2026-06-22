# NOVA_ROTA_REVISAO_FUNCIONAL_POS_USO_REAL

## Objetivo

Registrar oficialmente a nova rota de revisao funcional apos uso real do sistema, priorizando a correcao dos fluxos quebrados antes de qualquer empacotamento final ou nova funcionalidade fora do escopo.

## Origem da rota

Esta rota nasce a partir de testes reais com o sistema em funcionamento, apos a identificacao de falhas operacionais em cadastro, atualizacao, recalculo, RTD, payoff, decisoes, metricas financeiras, duplicidade visual e padronizacao de interface.

## Estado de referencia

- Data de criacao documental: 2026-06-22 13:22:21
- Branch atual: fase-3a4-auto-pricing-manual-save
- Commit base: bce681f docs: consolida checklist de entrega da fase 7

## Decisao de congelamento

A Fase 7 documental fica pausada como empacotamento final. A prioridade passa a ser a revisao funcional pos uso real, com foco em corrigir e validar os fluxos principais antes do fechamento.

## Diretrizes obrigatorias

- Nao migrar para web.
- Nao utilizar emojis.
- Manter-se ao escopo do projeto sem derivacoes.
- Efetuar buscas de dados e arquivos antes de alteracoes.
- Toda mudanca deve ser testada apos concluida.
- Apos o encerramento de fase, o teste deve compor todas as fases encerradas.
- Evitar codigos intermediarios em explicacoes, indo direto ao ponto.
- Em alteracoes, sempre gerar codigo inteiro do arquivo.
- A cada alteracao concluida e testada, commitar.
- Nao codar sem rumo; se necessario, buscar a evolucao no Git.
- Criar e manter arquivo de auditoria atualizado com testes, conclusoes e caminho de evolucao.
- Nao gerar codigo com crase.

## Decisoes tecnicas fixadas

- Excel e apenas ponte RTD.
- Banco de dados e a fonte da verdade.
- UI nao deve depender de CSVs derivados antigos.
- Calculos devem ser efetuados pelo sistema.
- Novas estruturas devem nascer no sistema.
- A entrega final so pode ocorrer apos validacao funcional integrada.

## Problemas identificados no uso real

### Base original da revisao

- Erro ao adicionar estrutura manual com virgula decimal, exibindo mensagem semelhante a strike must be numeric.
- Inclusao de estrutura precisa evoluir para modelo assistido, em que o usuario informa campos principais e o sistema preenche dados derivados a partir do simbolo da opcao.
- Estrutura incluida aparece no sistema, mas payoff e busca de decisoes nao funcionam.
- Botao atualizar dados apresenta feedback inexistente, insuficiente ou generico.
- Atualizacoes RTD nao executam ou nao refletem no sistema mesmo com conexao aberta.
- Possivel divergencia de horario nos campos de criado e atualizado.

### Segunda revisao de testes com sistema em funcionamento

- Nao esta atualizando dados na implantacao da estrutura conforme solicitado.
- Ao clicar em recalculo na estrutura nova, aparece mensagem de snapshot nao mudou e recalculo desnecessario.
- Estrutura aparentemente nao esta atualizando automaticamente via RTD.
- Dados de metricas financeiras nao estao sendo preenchidos.
- Sistema mostra duplicidade na estrutura numero 2, mas a duplicidade nao aparece no filtro de decisao.
- E necessario normalizar comandos, decisoes e dados para Portugues Brasil.
- E necessario adicionar comentario de posicao do grafico de payoff, incluindo ganho, perda e melhor regiao para ganho.
- E necessario melhorar a visibilidade da estrutura implantada com atualizacao de posicao automatica e instantanea.
- Existe descricao de aba ou alias, mas o sistema deixou de usar abas; se for obsoleto, a chamada deve ser eliminada.

## Escopo permitido

- Reproducao controlada dos problemas.
- Busca e analise de arquivos antes de alteracoes.
- Correcao de validadores numericos.
- Correcao de cadastro manual e assistido.
- Integracao da estrutura manual com payoff e decisoes.
- Correcao do botao atualizar dados e resumo do pipeline.
- Correcao ou documentacao da execucao RTD.
- Correcao de recalculo, snapshot e metricas financeiras.
- Correcao de duplicidade visual ou inconsistencia de origem.
- Normalizacao de interface para Portugues Brasil.
- Comentario interpretativo do grafico de payoff.
- Melhoria de visibilidade da estrutura implantada.
- Remocao ou justificativa de chamada obsoleta de aba ou alias.
- Testes automatizados e evidencias manuais.
- Atualizacao da auditoria viva.

## Escopo proibido

- Migrar para web.
- Criar nova arquitetura fora do escopo.
- Voltar a depender de CSVs derivados antigos como fonte principal.
- Usar Excel como fonte da verdade.
- Gerar pacote final antes das correcoes funcionais.
- Alterar arquivos sem busca previa.
- Encerrar fase sem teste e evidencia.
- Fazer alteracoes sem commit correspondente.
- Incluir dados reais em pacote externo sem revisao explicita.
- Criar codigo intermediario sem finalidade clara.

## Ordem de execucao

1. Congelamento da nova rota.
2. Auditoria viva da revisao funcional.
3. Plano operacional da revisao.
4. Reproducao controlada dos problemas.
5. Correcao da normalizacao numerica.
6. Cadastro assistido de estrutura.
7. Integracao da estrutura manual com payoff e decisoes.
8. Botao atualizar dados e resumo do pipeline.
9. Execucao RTD.
10. Recalculo, snapshot e metricas financeiras.
11. Duplicidade da estrutura numero 2.
12. Normalizacao para Portugues Brasil.
13. Comentario do grafico de payoff.
14. Visibilidade da estrutura implantada e atualizacao instantanea.
15. Remocao de chamada obsoleta de aba ou alias.
16. Validacao integrada.
17. Fechamento documental da rota.

## Criterio de encerramento

A rota somente pode ser encerrada quando:

- A auditoria estiver atualizada.
- Cada problema confirmado tiver correcao, justificativa tecnica ou limitacao documentada.
- Os testes automatizados previstos forem executados.
- A compilacao prevista for executada.
- Os fluxos manuais principais forem validados.
- Os resultados forem registrados em evidencia final.
- O checklist final estiver completo.
- Cada fase concluida tiver commit correspondente.

## Estado inicial

- Rota criada documentalmente.
- Nenhuma alteracao funcional realizada nesta etapa.
- Proxima etapa: reproducao controlada dos problemas.
