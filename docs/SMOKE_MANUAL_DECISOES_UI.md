# Status: LEGADO

Este documento foi mantido como registro historico. Ele nao deve ser usado como bloqueador operacional atual.
A validacao da area Decisoes deve ocorrer por testes automatizados e/ou execucao assistida com acesso ao sistema.

---

# Checklist de Smoke Manual da UI - Decisoes

Data: 2026-07-03 16:36:02 -0300

Branch: refactor/decisions-dark-panel-large-block

## Objetivo

Este documento define o checklist minimo de smoke manual para a area **Decisoes** da UI.

A finalidade e validar equivalencia operacional antes de qualquer nova alteracao de runtime ou substituicao da UI canonica.

Documentos relacionados:

- `docs/MATRIZ_EQUIVALENCIA_UI.md`
- `docs/INVENTARIO_ARQUIVOS_UI.md`
- `docs/CLASSIFICACAO_AREAS_UI.md`
- `docs/MATRIZ_CRUZADA_AREAS_UI.md`

## Escopo desta fatia

Esta etapa e somente documental.

Nao altera comportamento.

Nao altera UI runtime.

Nao altera banco.

Nao altera services, repositories ou regra de negocio.

Nao altera entrypoint principal.

Nao declara equivalencia completa.

## Premissas

A frente Decisoes esta registrada como:

- status inicial: `EQUIVALENCIA_PARCIAL_OPERACIONAL`;
- risco: medio;
- validacao pendente: smoke manual comparativo;
- regra: preservar UI canonica ate decisao explicita.

## Regras de execucao do smoke

1. Executar preferencialmente em ambiente local controlado.
2. Registrar data, branch e commit testado.
3. Nao alterar dados produtivos.
4. Nao executar migracoes.
5. Nao alterar configuracoes permanentes durante o smoke.
6. Se houver erro critico, interromper e registrar evidencia.
7. Comparar UI moderna/dark com a UI canonica quando ambas estiverem disponiveis.
8. Nao considerar equivalencia completa sem evidencia visual e funcional.

## Identificacao do teste

Preencher manualmente antes da execucao:

| Campo | Valor |
|---|---|
| Data/hora do teste | PENDENTE |
| Responsavel | PENDENTE |
| Branch | `refactor/decisions-dark-panel-large-block` |
| Commit | PENDENTE |
| Sistema operacional | PENDENTE |
| Ambiente | Local |
| Base/dataset utilizado | PENDENTE |
| UI canonica disponivel? | PENDENTE |
| UI moderna/dark disponivel? | PENDENTE |

## Checklist resumido

| Grupo | Item | Resultado | Evidencia/observacao |
|---|---|---|---|
| Abertura | Aplicacao inicia sem erro bloqueante | PENDENTE | PENDENTE |
| Abertura | Area Decisoes fica acessivel | PENDENTE | PENDENTE |
| Navegacao | Troca para aba/painel Decisoes sem travamento | PENDENTE | PENDENTE |
| Navegacao | Retorno para outras areas sem quebrar estado | PENDENTE | PENDENTE |
| Estado vazio | Tela renderiza sem dados validos | PENDENTE | PENDENTE |
| Estado vazio | Mensagem de ausencia de dados e compreensivel | PENDENTE | PENDENTE |
| Selecao invalida | Selecao inexistente ou incompleta nao quebra a tela | PENDENTE | PENDENTE |
| Selecao invalida | Mensagem de erro/alerta e exibida | PENDENTE | PENDENTE |
| Dados validos | Dados de decisoes carregam corretamente | PENDENTE | PENDENTE |
| Dados validos | Campos principais aparecem na ordem esperada | PENDENTE | PENDENTE |
| Dados validos | Valores numericos/textuais sao consistentes com UI canonica | PENDENTE | PENDENTE |
| Feedback | Status de carregamento aparece quando aplicavel | PENDENTE | PENDENTE |
| Feedback | Erros nao ficam silenciosos | PENDENTE | PENDENTE |
| Tema dark | Contraste basico e legivel | PENDENTE | PENDENTE |
| Tema dark | Componentes principais nao ficam cortados/sobrepostos | PENDENTE | PENDENTE |
| Equivalencia | Fluxo principal bate com UI canonica | PENDENTE | PENDENTE |
| Equivalencia | Divergencias sao registradas | PENDENTE | PENDENTE |
| Rollback | E possivel retornar ao estado anterior sem alteracao persistente | PENDENTE | PENDENTE |

## Roteiro detalhado

### 1. Preparacao

- Confirmar working tree limpo.
- Confirmar branch testada.
- Confirmar commit testado.
- Confirmar ambiente local.
- Confirmar se existe dataset minimo para Decisoes.
- Confirmar como abrir a UI canonica.
- Confirmar como abrir a UI moderna/dark, se aplicavel.

Resultado esperado:

- Ambiente pronto.
- Nenhuma alteracao pendente no Git.
- Nenhuma migracao ou alteracao persistente iniciada.

### 2. Abertura da aplicacao

Passos:

1. Abrir a aplicacao pelo fluxo atual do projeto.
2. Observar erros no terminal/log.
3. Acessar a area Decisoes.

Resultado esperado:

- Aplicacao abre.
- Area Decisoes fica acessivel.
- Nenhum erro bloqueante ocorre.

Resultado obtido:

- PENDENTE

Evidencia:

- PENDENTE

### 3. Estado vazio

Passos:

1. Abrir Decisoes sem selecionar dados validos ou usando base sem registros aplicaveis.
2. Observar renderizacao da tela.
3. Verificar mensagens exibidas.

Resultado esperado:

- A tela nao quebra.
- Mensagem de ausencia de dados e clara.
- Nenhum traceback aparece.
- A navegacao continua funcional.

Resultado obtido:

- PENDENTE

Evidencia:

- PENDENTE

### 4. Selecao invalida ou incompleta

Passos:

1. Simular selecao inexistente, incompleta ou inconsistente.
2. Observar comportamento da UI.
3. Validar mensagens de feedback.

Resultado esperado:

- Nao ha crash.
- Usuario recebe feedback compreensivel.
- O estado anterior nao e corrompido.

Resultado obtido:

- PENDENTE

Evidencia:

- PENDENTE

### 5. Carregamento com dados validos

Passos:

1. Selecionar um conjunto de dados conhecido.
2. Abrir a area Decisoes.
3. Validar campos principais.
4. Comparar com a UI canonica.

Resultado esperado:

- Dados aparecem.
- Campos principais estao presentes.
- Valores conferem com a UI canonica ou divergencias sao explicadas.
- Nao ha regressao visual bloqueante.

Resultado obtido:

- PENDENTE

Evidencia:

- PENDENTE

### 6. Mensagens, status e erros

Passos:

1. Observar mensagens durante carregamento.
2. Observar erros esperados.
3. Confirmar se mensagens nao ficam silenciosas.
4. Confirmar se mensagens nao poluem a tela indevidamente.

Resultado esperado:

- Status de carregamento aparece quando necessario.
- Erros sao visiveis e compreensiveis.
- Mensagens nao impedem navegacao.

Resultado obtido:

- PENDENTE

Evidencia:

- PENDENTE

### 7. Tema dark / UI moderna

Passos:

1. Abrir Decisoes no modo dark/moderno, se disponivel.
2. Verificar contraste.
3. Verificar alinhamento.
4. Verificar se blocos grandes nao quebram layout.
5. Verificar se textos ficam legiveis.

Resultado esperado:

- Contraste suficiente.
- Sem texto cortado relevante.
- Sem sobreposicao critica.
- Layout permanece navegavel.

Resultado obtido:

- PENDENTE

Evidencia:

- PENDENTE

### 8. Comparacao com UI canonica

Passos:

1. Executar o mesmo fluxo na UI canonica.
2. Executar o mesmo fluxo na UI moderna/dark.
3. Comparar dados, labels, mensagens e navegacao.
4. Registrar divergencias.

Resultado esperado:

- Fluxo principal equivalente ou divergencias documentadas.
- Nenhuma divergencia critica sem registro.

Resultado obtido:

- PENDENTE

Evidencia:

- PENDENTE

## Tabela de divergencias

| ID | Area | Descricao | Severidade | UI canonica | UI moderna/dark | Acao recomendada | Status |
|---|---|---|---|---|---|---|---|
| D-001 | PENDENTE | PENDENTE | PENDENTE | PENDENTE | PENDENTE | PENDENTE | PENDENTE |

## Criterios de aprovacao parcial

A area Decisoes pode permanecer como equivalencia parcial operacional se:

- a tela abre;
- a navegacao basica funciona;
- estado vazio nao quebra;
- selecao invalida nao quebra;
- dados validos carregam;
- mensagens principais aparecem;
- divergencias contra UI canonica estao registradas;
- nao ha alteracao de banco, services, repositories ou entrypoint.

## Criterios para nao aprovar

Nao aprovar se ocorrer qualquer item abaixo:

- crash na abertura;
- crash ao acessar Decisoes;
- erro silencioso em carregamento critico;
- dados divergentes sem explicacao;
- tela inutilizavel em estado vazio;
- acao que altera dados sem confirmacao;
- dependencia de mudanca em banco/pipeline para funcionar;
- necessidade de alterar entrypoint principal.

## Resultado final do smoke

Preencher apos execucao:

| Campo | Valor |
|---|---|
| Resultado geral | PENDENTE |
| Pode manter equivalencia parcial operacional? | PENDENTE |
| Pode evoluir para equivalencia completa? | NAO, pendente decisao explicita |
| Precisa nova correcao antes de seguir? | PENDENTE |
| Evidencias anexadas/registradas | PENDENTE |

## Decisao operacional

Este checklist nao autoriza substituicao da UI canonica.

A proxima alteracao de runtime na area Decisoes so deve ocorrer apos:

- execucao deste smoke;
- registro de resultado;
- escolha de uma divergencia pequena;
- plano de rollback simples.
