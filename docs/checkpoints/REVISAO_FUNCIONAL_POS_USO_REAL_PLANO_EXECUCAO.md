# REVISAO_FUNCIONAL_POS_USO_REAL_PLANO_EXECUCAO

## Objetivo

Transformar a NOVA_ROTA_REVISAO_FUNCIONAL_POS_USO_REAL em plano operacional executavel, com fases, documentos, criterios de aceite e saidas esperadas.

## Estado de referencia

- Data de criacao: 2026-06-22 13:22:21
- Branch atual: fase-3a4-auto-pricing-manual-save
- Commit base: bce681f docs: consolida checklist de entrega da fase 7

## Premissas

- Nenhuma alteracao funcional deve ocorrer antes da reproducao controlada.
- Antes de alterar, devem ser buscados arquivos, dados, historico Git e testes relacionados.
- Toda alteracao deve ser testada.
- Cada fase concluida deve gerar commit.
- A auditoria viva deve ser atualizada ao final de cada fase.
- O banco de dados e a fonte da verdade.
- Excel permanece apenas como ponte RTD.

## Fase 1 - Reproducao controlada

### Documento

docs/evidencias/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_1_REPRODUCAO.md

### Objetivo

Confirmar o estado atual antes de corrigir.

### Saida esperada

- Problemas confirmados.
- Problemas nao reproduzidos.
- Evidencia manual.
- Estado do banco antes e depois.
- Auditoria atualizada.
- Commit documental.

## Fase 2 - Normalizacao numerica

### Documento

docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_2_NORMALIZACAO_NUMERICA.md

### Objetivo

Aceitar formato brasileiro e tecnico em entradas numericas.

### Criterios de aceite

- Aceitar 10,50.
- Aceitar 10.50.
- Aceitar 1.234,56.
- Aceitar 1234,56.
- Aceitar 1234.56.
- Rejeitar texto invalido.
- Exibir mensagem clara em Portugues Brasil.
- Criar ou ajustar testes.

## Fase 3 - Cadastro assistido de estrutura

### Documento

docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_3_CADASTRO_ASSISTIDO.md

### Objetivo

Permitir que o usuario informe os campos principais e o sistema complete dados derivados pelo simbolo da opcao.

### Criterios de aceite

- Simbolo reconhecido preenche dados automaticamente.
- Simbolo nao encontrado gera mensagem clara.
- Divergencias entre tipo, ativo e simbolo sao tratadas.
- Estrutura so e salva como funcional se tiver dados minimos.

## Fase 4 - Integracao da estrutura manual com payoff e decisoes

### Documento

docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_4_PAYOFF_DECISOES.md

### Objetivo

Garantir que estrutura manual valida gere payoff e participe da busca de decisoes.

### Criterios de aceite

- Estrutura manual valida gera curva de payoff.
- Estrutura manual valida gera decisoes.
- structure_decisions recebe registros ou informa rejeicao.
- payoff_curve_points recebe pontos ou informa rejeicao.
- Logs indicam estruturas lidas, processadas, ignoradas e rejeitadas.

## Fase 5 - Botao Atualizar Dados e resumo do pipeline

### Documento

docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_5_ATUALIZAR_DADOS_PIPELINE.md

### Objetivo

Transformar o botao Atualizar Dados em acao rastreavel e compreensivel.

### Criterios de aceite

- Clique gera feedback imediato.
- Sucesso detalha o que ocorreu.
- Erro mostra mensagem clara.
- Erro tecnico fica em log.
- Tela atualiza apos sucesso.
- Se tudo retornar zero, o sistema informa que nenhum dado novo foi gerado.

## Fase 6 - Execucao RTD

### Documento

docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_6_RTD.md

### Objetivo

Garantir que conexao RTD aberta resulte em coleta efetiva ou limitacao documentada.

### Criterios de aceite

- Com RTD conectado, coleta e executada.
- Sistema informa sucesso ou falha.
- Sistema informa quantos registros foram atualizados.
- Dados persistem no banco.
- Tela mostra dados novos ou horario da ultima atualizacao.
- Logs permitem diagnostico.

## Fase 7 - Recalculo, snapshot e metricas financeiras

### Documento

docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_7_RECALCULO_METRICAS.md

### Objetivo

Corrigir comportamento de recalculo desnecessario e metricas financeiras vazias.

### Criterios de aceite

- Estrutura nova implantada atualiza dados.
- Recalculo executa quando ha dado novo.
- Mensagem diferencia sem mudanca, falha e execucao real.
- Metricas financeiras sao preenchidas quando ha dados suficientes.
- Quando nao houver dados, o sistema informa o motivo.

## Fase 8 - Duplicidade da estrutura numero 2

### Documento

docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_8_DUPLICIDADE_ESTRUTURA.md

### Objetivo

Eliminar duplicidade visual e inconsistencia entre listagem e filtro de decisao.

### Criterios de aceite

- Estrutura aparece uma unica vez na listagem.
- Filtro de decisao usa a mesma referencia funcional.
- Nao ha perda de dados.
- Se houver duplicidade real no banco, sistema indica origem ou consolida conforme regra definida.

## Fase 9 - Normalizacao para Portugues Brasil

### Documento

docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_9_PORTUGUES_BRASIL.md

### Objetivo

Padronizar comandos, decisoes, mensagens, dados exibidos e textos de interface para Portugues Brasil.

### Criterios de aceite

- Usuario final nao ve mensagens tecnicas em ingles.
- Erros de validacao sao claros.
- Status e decisoes usam vocabulario padronizado.
- Logs internos podem preservar informacoes tecnicas quando necessario.

## Fase 10 - Comentario do grafico de payoff

### Documento

docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_10_COMENTARIO_PAYOFF.md

### Objetivo

Adicionar interpretacao textual ao grafico de payoff.

### Criterios de aceite

- Comentario aparece junto ao payoff.
- Comentario usa Portugues Brasil.
- Comentario nao promete resultado financeiro.
- Comentario depende dos dados calculados pelo sistema.
- Se nao houver payoff, explica o motivo.

## Fase 11 - Visibilidade da estrutura implantada e atualizacao instantanea

### Documento

docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_11_VISIBILIDADE_ATUALIZACAO.md

### Objetivo

Melhorar a experiencia da estrutura implantada com atualizacao visual clara.

### Criterios de aceite

- Usuario ve quando atualizacao comeca.
- Usuario ve quando termina.
- Usuario ve o que mudou.
- Dados refletem o ultimo calculo.
- Se nao houver mudanca, o motivo fica claro.

## Fase 12 - Remocao de chamada obsoleta de aba ou alias

### Documento

docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_12_ABA_ALIAS.md

### Objetivo

Eliminar ou justificar referencia a aba ou alias se o sistema deixou de usar abas.

### Criterios de aceite

- Se aba ou alias ainda for necessario, justificar.
- Se for obsoleto, remover da chamada funcional.
- Nao remover historico documental sem necessidade.
- Sistema nao deve exibir conceito inexistente ao usuario.

## Fase 13 - Validacao integrada

### Documento

docs/evidencias/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_13_VALIDACAO_INTEGRADA.md

### Objetivo

Garantir que as correcoes nao quebraram funcionalidades existentes.

### Comandos previstos

- python -m pytest ATT/tests -q
- python -m compileall repositories services domain ATT/tests

### Criterios de aceite

- Testes aprovados.
- Compilacao sem erro.
- Fluxos principais validados.
- Evidencia final registrada.
- Auditoria atualizada.

## Fase 14 - Fechamento documental

### Documentos

- docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FECHAMENTO.md
- docs/checklists/CHECKLIST_REVISAO_FUNCIONAL_POS_USO_REAL.md
- docs/decisoes/DECISOES_REVISAO_FUNCIONAL_POS_USO_REAL.md

### Objetivo

Encerrar a rota com rastreabilidade completa.

### Criterios de aceite

- Checklist final completo.
- Auditoria completa.
- Evidencia final registrada.
- Commits criados por fase.
- Possivel tag de encerramento, se mantido o padrao do projeto.
