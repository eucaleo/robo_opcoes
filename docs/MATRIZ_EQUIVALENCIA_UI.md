# Matriz Global de Equivalencia da UI

Data inicial: 2026-07-03 16:07:55 -0300

Branch de origem: refactor/decisions-dark-panel-large-block

## Objetivo

Este documento define a matriz global de equivalencia entre a UI atual/canonica e as frentes modernas/dark em desenvolvimento.

A matriz existe para impedir substituicao prematura da UI principal antes de validacao funcional, operacional e documental.

## Principios

1. A UI atual/canonica permanece como caminho principal.
2. A UI moderna/dark pode ser validada por fatias.
3. Equivalencia parcial nao significa encerramento global da frente UI.
4. Cada aba ou painel deve ter criterio proprio.
5. Banco, regra de negocio, services, repositories e entrypoint principal devem permanecer preservados.
6. Substituicao de caminho principal exige validacao global, nao apenas visual.

## Classificacoes possiveis

### CANONICA

Tela ou fluxo atualmente considerado principal para operacao.

### EQUIVALENTE

Tela ou fluxo moderno/dark validado contra a UI canonica, cobrindo funcionalidades essenciais, estados vazios, erros esperados e operacao manual.

### EQUIVALENCIA_PARCIAL_OPERACIONAL

Tela ou fluxo moderno/dark cobre uma parte operacional relevante, mas ainda nao substitui a UI canonica.

### EXPERIMENTAL

Tela, painel ou fluxo em desenvolvimento, sem garantia de equivalencia.

### PENDENTE

Area ainda nao auditada ou nao validada.

### FORA_ESCOPO

Area explicitamente fora da fatia atual.

## Matriz inicial

| Area / Aba / Fluxo | UI canonica preservada | UI moderna/dark | Estado atual | Evidencia | Proxima acao |
|---|---:|---:|---|---|---|
| Decisoes / painel dark | Sim | Sim | EQUIVALENCIA_PARCIAL_OPERACIONAL | AUDITORIA_REFACTOR_UI.md | Separar backlog de melhorias |
| Terminal VWAP | Sim | Parcial/indefinido | FORA_ESCOPO | AUDITORIA_REFACTOR_UI.md | Abrir auditoria propria |
| Payoff curve | Sim | Parcial/indefinido | FORA_ESCOPO | AUDITORIA_REFACTOR_UI.md | Auditar fluxo e UIDataModel |
| UIDataModel | Sim | Indefinido | FORA_ESCOPO | AUDITORIA_REFACTOR_UI.md | Mapear consumidores |
| Banco/dados/pipeline | Sim | Nao aplicavel | PENDENTE | AUDITORIA_REFACTOR_UI.md | Auditar origem dos dados |
| Navegacao geral entre abas | Sim | Indefinido | PENDENTE | A definir | Criar smoke manual |
| Mensagens de status | Sim | Parcial | PENDENTE | A definir | Criar checklist por aba |
| Estados vazios e selecao invalida | Sim | Parcial | PENDENTE | A definir | Criar roteiro manual |
| Entrypoint principal | Sim | Nao deve mudar | CANONICA | Politica de preservacao | Preservar |

## Checklist minimo por area

Cada area da UI somente pode sair de PENDENTE ou EXPERIMENTAL quando houver validacao minima dos itens abaixo.

### Funcionalidade

- abertura da tela sem erro;
- carregamento de dados esperado;
- comportamento com dados ausentes;
- comportamento com selecao vazia;
- comportamento com selecao invalida;
- botoes dependentes habilitados/desabilitados corretamente;
- acoes principais executadas sem excecao;
- mensagens de status compreensiveis.

### Equivalencia operacional

- fluxo equivalente identificado na UI canonica;
- entradas e saidas comparadas;
- efeitos colaterais conhecidos;
- ausencia de mudanca em banco fora do previsto;
- ausencia de alteracao em services/repositories;
- preservacao de contratos canonicos.

### Regressao

- py_compile dos arquivos Python alterados;
- git diff --check limpo;
- smoke manual registrado;
- evidencia minima documentada;
- rollback simples identificado.

## Criterio para declarar equivalencia completa

Uma area so pode ser declarada EQUIVALENTE quando:

1. a UI canonica correspondente estiver identificada;
2. todos os fluxos principais tiverem sido testados;
3. estados vazios e invalidos tiverem sido testados;
4. nao houver dependencia de banco volatil ou origem de dados ambigua;
5. nao houver alteracao silenciosa de regra de negocio;
6. o comportamento visual e operacional estiver documentado;
7. houver decisao explicita registrada em auditoria.

## Criterio para substituicao da UI principal

A UI moderna/dark so pode substituir a UI atual/canonica quando:

1. a matriz global estiver completa;
2. todas as areas criticas estiverem como EQUIVALENTE;
3. areas nao equivalentes estiverem documentadas e aceitas;
4. houver smoke manual global;
5. houver plano de rollback;
6. entrypoint principal for alterado apenas em branch propria;
7. a decisao estiver registrada em documento de auditoria.

## Pendencias abertas

- detalhar inventario completo de abas;
- identificar arquivos principais da UI canonica;
- identificar arquivos principais da UI moderna/dark;
- criar roteiro de smoke manual global;
- auditar Terminal VWAP separadamente;
- auditar payoff curve separadamente;
- auditar UIDataModel separadamente;
- auditar banco/dados/pipeline separadamente.

## Decisao operacional

Este documento nao encerra a frente UI.

Ele cria a matriz inicial para orientar proximas fatias pequenas e impedir mistura de escopos.

---

## Referencia inventario inicial de arquivos reais

Data: 2026-07-03 16:11:04 -0300

Foi criado o inventario inicial de arquivos reais relacionados a UI:

    docs/INVENTARIO_ARQUIVOS_UI.md

Este inventario passa a ser insumo para preencher a matriz por area, aba e fluxo.

A classificacao da matriz ainda deve ser feita manualmente ou em fatias documentadas, pois a varredura estatica apenas identifica candidatos.

---

## Referencia classificacao inicial por area

Data: 2026-07-03 16:29:46 -0300

Foi criada a classificacao inicial dos arquivos candidatos de UI por area:

    docs/CLASSIFICACAO_AREAS_UI.md

A classificacao devera ser usada para transformar o inventario bruto em uma matriz operacional por area, aba e fluxo.

Esta classificacao ainda nao declara equivalencia completa.

---

## Referencia matriz cruzada de areas UI

Data: 2026-07-03 16:33:19 -0300

Foi criada a matriz cruzada de areas da UI:

    docs/MATRIZ_CRUZADA_AREAS_UI.md

A matriz cruzada passa a orientar a escolha das proximas fatias pequenas por risco, area e status.

Esta matriz ainda nao declara equivalencia completa de nenhuma area.
