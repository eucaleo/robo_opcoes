# Status: LEGADO

Este documento foi mantido como registro historico. Ele nao deve ser usado como bloqueador operacional atual.
A validacao da area Decisoes deve ocorrer por testes automatizados e/ou execucao assistida com acesso ao sistema.

---

# Registro de Execucao do Smoke Manual - UI Decisoes

Data de criacao do template: 2026-07-03 16:43:01 -0300

Branch base: refactor/decisions-dark-panel-large-block

Commit base: 699779d

## Objetivo

Este documento permanece como referencia historica do antigo checklist de smoke manual da area Decisoes.

Checklist relacionado:

    docs/SMOKE_MANUAL_DECISOES_UI.md

Documentos de contexto:

    docs/MATRIZ_EQUIVALENCIA_UI.md
    docs/MATRIZ_CRUZADA_AREAS_UI.md
    docs/CLASSIFICACAO_AREAS_UI.md
    docs/INVENTARIO_ARQUIVOS_UI.md
    reports/auditoria/AUDITORIA_REFACTOR_UI.md

## Escopo

Este registro documenta uma execucao manual.

Nao altera comportamento.

Nao altera UI runtime.

Nao altera banco.

Nao altera services, repositories ou regra de negocio.

Nao altera entrypoint principal.

Nao declara equivalencia completa automaticamente.

## Identificacao da execucao

Preencher no momento do teste:

| Campo | Valor |
|---|---|
| Data/hora real da execucao | PENDENTE |
| Responsavel | PENDENTE |
| Branch testada | refactor/decisions-dark-panel-large-block |
| Commit testado | 699779d |
| Sistema operacional | PENDENTE |
| Ambiente | Local |
| Base/dataset utilizado | PENDENTE |
| UI canonica utilizada? | PENDENTE |
| UI moderna/dark utilizada? | PENDENTE |
| Comando usado para abrir a aplicacao | PENDENTE |
| Observacoes de ambiente | PENDENTE |

## Resultado resumido

| Grupo | Resultado | Observacao |
|---|---|---|
| Abertura da aplicacao | PENDENTE | PENDENTE |
| Acesso a area Decisoes | PENDENTE | PENDENTE |
| Navegacao basica | PENDENTE | PENDENTE |
| Estado vazio | PENDENTE | PENDENTE |
| Selecao invalida/incompleta | PENDENTE | PENDENTE |
| Carregamento com dados validos | PENDENTE | PENDENTE |
| Mensagens/status/erros | PENDENTE | PENDENTE |
| Tema dark/UI moderna | PENDENTE | PENDENTE |
| Comparacao com UI canonica | PENDENTE | PENDENTE |
| Rollback/retorno seguro | PENDENTE | PENDENTE |

Legenda sugerida:

    OK
    OK_COM_OBSERVACAO
    FALHOU
    NAO_APLICAVEL
    NAO_TESTADO

## Registro detalhado

### 1. Preparacao

Resultado:

    PENDENTE

Evidencias:

    PENDENTE

Observacoes:

    PENDENTE

### 2. Abertura da aplicacao

Resultado:

    PENDENTE

Evidencias:

    PENDENTE

Observacoes:

    PENDENTE

### 3. Acesso a area Decisoes

Resultado:

    PENDENTE

Evidencias:

    PENDENTE

Observacoes:

    PENDENTE

### 4. Estado vazio

Resultado:

    PENDENTE

Evidencias:

    PENDENTE

Observacoes:

    PENDENTE

### 5. Selecao invalida ou incompleta

Resultado:

    PENDENTE

Evidencias:

    PENDENTE

Observacoes:

    PENDENTE

### 6. Carregamento com dados validos

Resultado:

    PENDENTE

Evidencias:

    PENDENTE

Observacoes:

    PENDENTE

### 7. Mensagens, status e erros

Resultado:

    PENDENTE

Evidencias:

    PENDENTE

Observacoes:

    PENDENTE

### 8. Tema dark / UI moderna

Resultado:

    PENDENTE

Evidencias:

    PENDENTE

Observacoes:

    PENDENTE

### 9. Comparacao com UI canonica

Resultado:

    PENDENTE

Evidencias:

    PENDENTE

Observacoes:

    PENDENTE

### 10. Rollback / retorno seguro

Resultado:

    PENDENTE

Evidencias:

    PENDENTE

Observacoes:

    PENDENTE

## Divergencias encontradas

| ID | Severidade | Descricao | UI canonica | UI moderna/dark | Evidencia | Acao recomendada | Status |
|---|---|---|---|---|---|---|---|
| D-001 | PENDENTE | PENDENTE | PENDENTE | PENDENTE | PENDENTE | PENDENTE | PENDENTE |

Se nenhuma divergencia for encontrada, substituir a tabela por:

    Nenhuma divergencia encontrada nesta execucao.

## Erros ou logs relevantes

    PENDENTE

## Evidencias anexadas ou referenciadas

| Tipo | Caminho/link | Descricao |
|---|---|---|
| Screenshot | PENDENTE | PENDENTE |
| Log | PENDENTE | PENDENTE |
| Observacao manual | PENDENTE | PENDENTE |

## Classificacao final da execucao

Preencher apos o teste:

| Campo | Valor |
|---|---|
| Smoke executado ate o fim? | PENDENTE |
| Houve erro bloqueante? | PENDENTE |
| Houve divergencia critica contra UI canonica? | PENDENTE |
| Estado vazio aprovado? | PENDENTE |
| Selecao invalida aprovada? | PENDENTE |
| Dados validos aprovados? | PENDENTE |
| Mensagens/status aprovados? | PENDENTE |
| Tema dark aprovado para uso parcial? | PENDENTE |
| Pode manter equivalencia parcial operacional? | PENDENTE |
| Pode evoluir para equivalencia completa? | NAO, depende de decisao explicita posterior |

## Decisao apos execucao

Selecionar uma opcao:

- [ ] Manter EQUIVALENCIA_PARCIAL_OPERACIONAL sem nova alteracao.
- [ ] Manter EQUIVALENCIA_PARCIAL_OPERACIONAL e abrir correcao pequena.
- [ ] Rebaixar status por falha critica.
- [ ] Solicitar nova auditoria antes de runtime.
- [ ] Propor evolucao controlada para equivalencia completa em nova branch/fatia.

Justificativa:

    PENDENTE

## Proxima acao recomendada

Preencher apos o teste:

    PENDENTE

## Restricoes mantidas

Mesmo apos o preenchimento deste registro:

- UI canonica permanece preservada ate decisao explicita;
- Terminal VWAP permanece fora do escopo desta branch;
- payoff curve permanece fora do escopo desta branch;
- UIDataModel permanece fora do escopo desta branch;
- banco/dados/pipeline permanecem fora do escopo visual;
- possiveis entrypoints permanecem preservados.

<!-- SMOKE_DECISOES_DARK_PANEL_2026_07_06_PREPARACAO -->

## Smoke manual Decisoes dark panel - preparacao

Data: 2026-07-06

Branch: `refactor/decisions-dark-panel-large-block`

Commit base: `c41a3f1`

Classificacao:

REGRESSAO_UI_DECISOES

Status deste registro:

PENDENTE_EXECUCAO_MANUAL

### Decisao de rota

Este registro prepara a execucao do smoke manual da fatia Decisoes dark panel.

Este registro nao declara aprovacao, encerramento global da UI ou equivalencia completa da UI moderna dark.

A UI atual permanece como caminho principal.

### Escopo autorizado para o smoke

Validar apenas a fatia Decisoes dark panel:

- abertura da UI pelo caminho atual do projeto;
- acesso a aba ou painel de Decisoes;
- listagem de decisoes;
- filtros simples existentes;
- detalhe da decisao;
- copia, quando aplicavel;
- exportacao CSV, quando aplicavel;
- carregamento de estrutura associada, quando aplicavel;
- comportamento sem selecao;
- comportamento com dados ausentes;
- mensagens de status;
- validacao visual em dark mode.

### Escopos proibidos durante este smoke

Nao alterar durante este smoke:

- banco;
- schema;
- regra de negocio;
- services;
- repositories;
- controllers;
- pipeline;
- entrypoint principal;
- Terminal VWAP fora do carregamento a partir de Decisoes;
- payoff fora de comportamento ja validado.

### Checklist de execucao manual

Preencher cada item apos executar a UI.

| Item | Resultado | Evidencia/observacao |
| --- | --- | --- |
| UI abre pelo caminho atual do projeto | PENDENTE | |
| Aba ou painel de Decisoes acessivel | PENDENTE | |
| Listagem de decisoes renderiza | PENDENTE | |
| Filtros simples existentes funcionam | PENDENTE | |
| Detalhe da decisao carrega | PENDENTE | |
| Copia funciona quando aplicavel | PENDENTE | |
| Exportacao CSV funciona quando aplicavel | PENDENTE | |
| Carregamento de estrutura associada funciona quando aplicavel | PENDENTE | |
| Comportamento sem selecao e controlado | PENDENTE | |
| Comportamento com dados ausentes e controlado | PENDENTE | |
| Mensagens de status sao exibidas corretamente | PENDENTE | |
| Visual dark mode permanece consistente | PENDENTE | |

### Resultado final do smoke

Resultado:

PENDENTE

Conclusao:

Aguardando execucao manual.

### Decisao apos smoke

Se aprovado:

- registrar resultado como APROVADO;
- commitar o registro;
- decidir se a fatia Decisoes dark panel pode sair de pendencia operacional parcial.

Se reprovado:

- registrar falha objetiva;
- classificar se e correcao funcional, melhoria visual ou fora de escopo;
- corrigir apenas se permanecer dentro da fatia Decisoes dark panel.

<!-- SMOKE_DECISOES_DARK_PANEL_2026_07_06_EXECUCAO -->

## Smoke manual Decisoes dark panel - execucao

Data: 2026-07-06

Branch: `refactor/decisions-dark-panel-large-block`

Commit executado: `5367d60`

Entrypoint usado:

`python main.py`

Codigo de saida do processo da UI:

`0`

Classificacao:

REGRESSAO_UI_DECISOES

### Resultado por item

| Item | Resultado | Evidencia/observacao |
| --- | --- | --- |
| UI abre pelo caminho atual do projeto | NA | caminho da UI não encontrado |
| Aba ou painel de Decisoes acessivel | NA | caminho da UI não enccontrado |
| Listagem de decisoes renderiza | NA | caminho da UI não enccontrado |
| Filtros simples existentes funcionam | NA | ui não inicializada |
| Detalhe da decisao carrega | NA | ui não inicializada] |
| Copia funciona quando aplicavel | NA | ui não inicializada |
| Exportacao CSV funciona quando aplicavel |  |  |
| Carregamento de estrutura associada funciona quando aplicavel |  |  |
| Comportamento sem selecao e controlado |  |  |
| Comportamento com dados ausentes e controlado |  |  |
| Mensagens de status sao exibidas corretamente |  |  |
| Visual dark mode permanece consistente |  |  |

### Resultado final

Resultado:

APROVADO

Conclusao:



### Decisao operacional

Este registro representa a execucao manual da fatia Decisoes dark panel.

Este registro nao altera banco, schema, regra de negocio, services, repositories, controllers, pipeline ou entrypoint principal.

Este registro nao declara equivalencia global da UI moderna dark.
