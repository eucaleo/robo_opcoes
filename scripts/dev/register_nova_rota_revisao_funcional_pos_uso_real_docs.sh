#!/usr/bin/env bash
set -euo pipefail

echo "[INFO] Criando documentos da NOVA_ROTA_REVISAO_FUNCIONAL_POS_USO_REAL"

mkdir -p docs/rotas
mkdir -p docs/auditoria
mkdir -p docs/checkpoints
mkdir -p docs/evidencias
mkdir -p docs/checklists
mkdir -p docs/decisoes

BRANCH="$(git branch --show-current)"
HEAD_LINE="$(git log --oneline -1)"
DATE_REF="$(date '+%Y-%m-%d %H:%M:%S')"

ROTA="docs/rotas/NOVA_ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md"
AUDITORIA="docs/auditoria/AUDITORIA_REVISAO_FUNCIONAL_POS_USO_REAL.md"
PLANO="docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_PLANO_EXECUCAO.md"
EVIDENCIA_FASE_1="docs/evidencias/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_1_REPRODUCAO.md"
CHECKLIST="docs/checklists/CHECKLIST_REVISAO_FUNCIONAL_POS_USO_REAL.md"
DECISOES="docs/decisoes/DECISOES_REVISAO_FUNCIONAL_POS_USO_REAL.md"

if [[ ! -f "${ROTA}" ]]; then
cat > "${ROTA}" <<DOC
# NOVA_ROTA_REVISAO_FUNCIONAL_POS_USO_REAL

## Objetivo

Registrar oficialmente a nova rota de revisao funcional apos uso real do sistema, priorizando a correcao dos fluxos quebrados antes de qualquer empacotamento final ou nova funcionalidade fora do escopo.

## Origem da rota

Esta rota nasce a partir de testes reais com o sistema em funcionamento, apos a identificacao de falhas operacionais em cadastro, atualizacao, recalculo, RTD, payoff, decisoes, metricas financeiras, duplicidade visual e padronizacao de interface.

## Estado de referencia

- Data de criacao documental: ${DATE_REF}
- Branch atual: ${BRANCH}
- Commit base: ${HEAD_LINE}

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
DOC
fi

if [[ ! -f "${AUDITORIA}" ]]; then
cat > "${AUDITORIA}" <<DOC
# AUDITORIA_REVISAO_FUNCIONAL_POS_USO_REAL

## Objetivo

Manter registro vivo da revisao funcional pos uso real, documentando testes, arquivos analisados, alteracoes, resultados, commits e pendencias.

## Estado inicial

- Data de criacao: ${DATE_REF}
- Branch atual: ${BRANCH}
- Commit base: ${HEAD_LINE}
- Rota relacionada: docs/rotas/NOVA_ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md

## Regras de auditoria

- Toda fase deve atualizar este arquivo.
- Toda correcao deve registrar busca previa.
- Toda alteracao deve registrar teste executado.
- Toda fase concluida deve registrar commit.
- Pendencias devem permanecer explicitas.
- Limitacoes externas, especialmente RTD, devem ser documentadas.

## Registro 001 - Criacao documental da rota

### Data

${DATE_REF}

### Branch usada

${BRANCH}

### Commit base

${HEAD_LINE}

### Problema testado

Nenhum problema funcional foi testado nesta etapa.

### Evidencia observada

Foi recebido documento refatorado da NOVA_ROTA_REVISAO_FUNCIONAL_POS_USO_REAL contendo problemas confirmados em uso real e ordem proposta de execucao.

### Arquivos analisados

- NOVA_ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.pdf

### Alteracao feita

Criacao dos documentos-base da rota, plano, auditoria, checklist, decisoes e evidencia inicial de reproducao.

### Teste executado

Validacao documental por diff e verificacao de ausencia de crase nos arquivos gerados.

### Resultado

Pendente de execucao local.

### Commit gerado

Pendente.

### Pendencia restante

Executar reproducao controlada dos problemas antes de qualquer alteracao funcional.

## Modelo para proximos registros

### Registro NNN - Titulo

#### Data

A preencher.

#### Branch usada

A preencher.

#### Commit base

A preencher.

#### Problema testado

A preencher.

#### Evidencia observada

A preencher.

#### Arquivos analisados

A preencher.

#### Alteracao feita

A preencher.

#### Teste executado

A preencher.

#### Resultado

A preencher.

#### Commit gerado

A preencher.

#### Pendencia restante

A preencher.
DOC
fi

if [[ ! -f "${PLANO}" ]]; then
cat > "${PLANO}" <<DOC
# REVISAO_FUNCIONAL_POS_USO_REAL_PLANO_EXECUCAO

## Objetivo

Transformar a NOVA_ROTA_REVISAO_FUNCIONAL_POS_USO_REAL em plano operacional executavel, com fases, documentos, criterios de aceite e saidas esperadas.

## Estado de referencia

- Data de criacao: ${DATE_REF}
- Branch atual: ${BRANCH}
- Commit base: ${HEAD_LINE}

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
DOC
fi

if [[ ! -f "${EVIDENCIA_FASE_1}" ]]; then
cat > "${EVIDENCIA_FASE_1}" <<DOC
# REVISAO_FUNCIONAL_POS_USO_REAL_FASE_1_REPRODUCAO

## Objetivo

Confirmar o estado atual dos problemas em ambiente local antes de qualquer correcao funcional.

## Estado de referencia

- Data de criacao: ${DATE_REF}
- Branch atual: ${BRANCH}
- Commit base: ${HEAD_LINE}

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
DOC
fi

if [[ ! -f "${CHECKLIST}" ]]; then
cat > "${CHECKLIST}" <<DOC
# CHECKLIST_REVISAO_FUNCIONAL_POS_USO_REAL

## Objetivo

Controlar o encerramento da NOVA_ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.

## Estado de referencia

- Data de criacao: ${DATE_REF}
- Branch atual: ${BRANCH}
- Commit base: ${HEAD_LINE}

## Checklist final

| Item | Criterio de encerramento | Status | Evidencia | Commit |
| --- | --- | --- | --- | --- |
| Virgula em strike | Aceita e testada | Pendente | A preencher | A preencher |
| Virgula em preco | Aceita e testada | Pendente | A preencher | A preencher |
| Cadastro manual | Funcional | Pendente | A preencher | A preencher |
| Cadastro assistido | Busca dados pelo simbolo | Pendente | A preencher | A preencher |
| Payoff | Gerado para estrutura valida | Pendente | A preencher | A preencher |
| Decisoes | Geradas para estrutura valida | Pendente | A preencher | A preencher |
| Atualizar dados | Feedback detalhado | Pendente | A preencher | A preencher |
| RTD | Executa ou limitacao documentada | Pendente | A preencher | A preencher |
| Metricas financeiras | Preenchidas ou motivo informado | Pendente | A preencher | A preencher |
| Recalculo | Mensagem coerente | Pendente | A preencher | A preencher |
| Duplicidade | Corrigida ou causa documentada | Pendente | A preencher | A preencher |
| Portugues Brasil | Normalizado na interface | Pendente | A preencher | A preencher |
| Comentario de payoff | Disponivel | Pendente | A preencher | A preencher |
| Atualizacao visual | Rastreavel | Pendente | A preencher | A preencher |
| Aba ou alias | Removido ou justificado | Pendente | A preencher | A preencher |
| Testes automatizados | Executados | Pendente | A preencher | A preencher |
| Compilacao | Executada sem erro critico | Pendente | A preencher | A preencher |
| Auditoria | Atualizada | Pendente | A preencher | A preencher |
| Commits | Criados por fase | Pendente | A preencher | A preencher |

## Regra de fechamento

A rota nao deve ser encerrada enquanto houver item pendente sem justificativa tecnica registrada.
DOC
fi

if [[ ! -f "${DECISOES}" ]]; then
cat > "${DECISOES}" <<DOC
# DECISOES_REVISAO_FUNCIONAL_POS_USO_REAL

## Objetivo

Registrar decisoes tomadas durante a NOVA_ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.

## Estado de referencia

- Data de criacao: ${DATE_REF}
- Branch atual: ${BRANCH}
- Commit base: ${HEAD_LINE}

## Decisoes iniciais fixadas

### Decisao 001 - Prioridade da revisao funcional

A Fase 7 documental fica pausada como empacotamento final. A prioridade passa a ser corrigir os problemas identificados em uso real.

### Decisao 002 - Excel como ponte RTD

Excel permanece apenas como ponte RTD. O banco de dados segue como fonte da verdade.

### Decisao 003 - Sem migracao para web

A rota nao permite migracao para web.

### Decisao 004 - Sem dependencia de CSVs antigos

A UI nao deve depender de CSVs derivados antigos como fonte principal.

### Decisao 005 - Calculos no sistema

Calculos de payoff, decisoes, metricas e atualizacoes devem ser realizados pelo sistema.

### Decisao 006 - Auditoria viva obrigatoria

Cada teste, alteracao, resultado, commit e pendencia deve ser registrado na auditoria viva.

### Decisao 007 - Uma correcao concluida exige teste e commit

Cada correcao funcional deve ser testada e commitada antes de seguir para a proxima.

## Registro de novas decisoes

### Decisao NNN - Titulo

- Data: a preencher.
- Contexto: a preencher.
- Decisao: a preencher.
- Impacto: a preencher.
- Arquivos relacionados: a preencher.
- Commit relacionado: a preencher.
DOC
fi

python - <<'PY'
from pathlib import Path

files = [
    Path("docs/rotas/NOVA_ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md"),
    Path("docs/auditoria/AUDITORIA_REVISAO_FUNCIONAL_POS_USO_REAL.md"),
    Path("docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_PLANO_EXECUCAO.md"),
    Path("docs/evidencias/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_1_REPRODUCAO.md"),
    Path("docs/checklists/CHECKLIST_REVISAO_FUNCIONAL_POS_USO_REAL.md"),
    Path("docs/decisoes/DECISOES_REVISAO_FUNCIONAL_POS_USO_REAL.md"),
]

for path in files:
    if path.exists():
        text = path.read_text(encoding="utf-8")
        text = text.replace(chr(96), "'")
        path.write_text(text, encoding="utf-8", newline="\n")
PY

echo "[OK] Documentos-base da nova rota criados ou preservados."
