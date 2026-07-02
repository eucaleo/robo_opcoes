# Frente 37 — Copiar detalhe da decisão no modo dark

Data: 2026-07-02
Commit funcional: fb857d3
Tag funcional: checkpoint-modern-decisions-copy-detail-dark

## Objetivo

Adicionar à UI moderna em modo dark a capacidade de copiar o detalhe textual da decisão selecionada para a área de transferência.

## Arquivo alterado

- UI/components/decisions_dark_panel.py

## Escopo executado

A alteração concentrou-se exclusivamente no componente visual de decisões em modo dark, sem modificar:

- banco de dados;
- contratos derivados;
- queries;
- services;
- repositories;
- controllers;
- regras de negócio;
- cálculo de payoff;
- carregamento de estruturas;
- persistência de decisões.

## Melhorias implementadas

Foi adicionado um botão no painel de detalhe da decisão:

- `Copiar detalhe`

O botão permanece desabilitado quando não há decisão selecionada e é habilitado automaticamente quando uma decisão válida é selecionada.

Ao acionar o botão, o conteúdo atualmente exibido no painel de detalhe é copiado para a área de transferência.

Também foram adicionadas mensagens de status para os cenários:

- nenhuma decisão selecionada para copiar;
- detalhe vazio;
- detalhe copiado com sucesso.

## Ajustes técnicos

Foram realizados os seguintes ajustes no layout e comportamento do painel:

- criação de uma segunda coluna no frame de detalhe;
- posicionamento do botão ao lado do título do detalhe;
- expansão do campo textual de detalhe usando `columnspan=2`;
- novo método `_copy_selected_detail`;
- controle automático do estado do botão em `_set_detail_text`;
- preservação do estado desabilitado do botão quando não existe seleção válida.

## Validações executadas

Foi executado com sucesso:

    python -m compileall UI/components/decisions_dark_panel.py

Também foram executadas as verificações de versionamento:

    git diff --check
    git status --short

## Resultado

A Frente 37 foi concluída com sucesso.

O modo dark agora permite copiar rapidamente o detalhe enriquecido da decisão selecionada, melhorando a usabilidade sem alterar contratos, persistência ou lógica de negócio.
