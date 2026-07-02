# Validacao manual das acoes laterais de estruturas no painel dark

Data de referencia: 2026-07-02

## Objetivo

Registrar a validacao manual dirigida das acoes laterais de estruturas na UI moderna dark.

## Ambiente

- comando executado: python -m UI.modern
- modo: dark
- branch: patch-side-actions-structures

## Resultado da validacao manual

| Acao | Resultado | Observacao |
|---|---|---|
| Recarregar estruturas | OK | Funcional |
| Abrir lista de estruturas | OK | Funcional |
| Selecionar uma estrutura existente | OK | Funcional |
| Recalcular Payoff | Parcial | Executa, mas precisa feedback visivel em avisos operacionais ou area equivalente |
| Editar pernas | OK | Funcionando e calculando |
| Cancelar edicao | OK | Sem alteracao desejada |
| Duplicar estrutura | Falha | Erro: metodo _cmd_duplicate nao encontrado neste componente |
| Voltar para lista | OK | Funcional |
| Abrir acoes da estrutura | OK | Funcional |
| Abrir ajuste | Falha | Nao funciona no fluxo manual |
| Encerrar estrutura | Parcial | Tela pisca e o log registra decisao CLOSE, mas a UI nao apresenta feedback claro |
| Arquivar estrutura | Falha | Nao funciona no fluxo manual |

## Evidencias de console

- estruturas carregadas no modo dark
- estrutura ID 2 carregada
- payoff recalculado para ID 2
- estrutura ID 2 atualizada
- decisoes HOLD registradas
- decisoes CLOSE registradas
- decisao ADJUST registrada
- payoff recalculado para ID 3 e ID 2

## Classificacao das lacunas

### Lacunas funcionais

- duplicar estrutura falha por callback ou metodo incorreto
- abrir ajuste nao executa corretamente no fluxo manual
- arquivar estrutura nao executa corretamente no fluxo manual

### Lacunas de feedback visual

- recalcular Payoff executa, mas nao deixa evidencia visivel suficiente na UI
- encerrar estrutura registra decisao no console, mas nao deixa evidencia visivel suficiente na UI

## Decisao

A proxima etapa deve aplicar patch funcional minimo no painel dark.

O patch deve ser restrito a UI moderna dark e nao deve alterar regras de negocio, contratos canonicos, banco de dados ou calculos.

## Proximo passo recomendado

- corrigir duplicacao para usar implementacao local segura ou servico existente
- corrigir abertura do bloco de ajuste
- corrigir arquivamento
- adicionar feedback operacional visivel para recalculo, encerramento, ajuste, duplicacao e arquivamento
