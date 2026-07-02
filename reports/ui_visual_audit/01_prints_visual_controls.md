# Auditoria Visual da UI Atual com Base nos Prints

Data: 2026-07-01
Fase: UI-1 / fechamento de inventário antes da substituição da interface

## 1. Objetivo

Registrar os controles, abas, botões, cortinas e áreas funcionais visíveis na UI atual, com base nos prints fornecidos, para impedir perda funcional durante a substituição do layout.

A nova UI poderá mudar completamente a disposição visual, porém não poderá eliminar funcionalidades sem decisão explícita.

Regra principal:

- A UI não molda o sistema.
- O sistema molda a UI.
- O novo layout deve apenas reorganizar e conectar funcionalidades existentes.

## 2. Estrutura visual atual identificada

A janela atual é um aplicativo desktop com:

- Menu superior
- Painel esquerdo de filtros e decisões
- Área direita com abas operacionais
- Barra/status inferior

Título visível:

- Sistema de Derivados - Análise de Decisões

Menus superiores visíveis:

- Arquivo
- Ferramentas
- Ajuda

## 3. Painel esquerdo: Filtros

Controles visíveis:

- Período:
  - De
  - Até
- Estrutura
- Decisão
- Level >=
- DTE <=
- Botão Aplicar
- Botão Limpar
- Indicador/link de filtros aplicados

Texto observado:

- Filtros aplicados (2 ativos)

Dropdown de Decisão observado com opções:

- HOLD
- PREPARE_ROLL
- CLOSE_REOPEN
- ROLL
- ENTER

Função esperada:

- Filtrar decisões listadas
- Limpar filtros
- Atualizar tabela de decisões
- Permitir navegação por decisão e estrutura

Destino no novo layout:

- Deve virar painel lateral, painel retrátil ou seção de filtros globais.
- Não deve ser removido.
- Pode ser visualmente simplificado, mas precisa manter a mesma capacidade funcional.

## 4. Painel esquerdo: tabela de Decisões

Colunas visíveis nos prints:

- Data/Hora
- Estrutura
- Decisão
- Nível
- Ratio %
- DTE
- PL Atual
- PL Máx

Observações:

- A seleção de uma linha altera o conteúdo das abas à direita.
- A tabela parece ser fonte principal de contexto operacional.
- Algumas linhas mostram decisão HOLD.
- Estruturas observadas: 2 e 3.
- Ratio observado: 152.5% e -7.6%.
- Há scroll vertical e horizontal.

Função esperada:

- Selecionar decisão
- Atualizar detalhes da decisão
- Atualizar payoff
- Atualizar contexto de estrutura
- Alimentar comparação de curva/payoff

Destino no novo layout:

- Deve permanecer como lista/grade de decisões.
- Pode ficar em painel lateral, drawer ou área inferior.
- Deve manter seleção e evento de atualização da análise principal.

## 5. Aba: Detalhes da Decisão

Campos visíveis:

### Informações Básicas

- Timestamp
- Decisão
- Estrutura
- Nível

### Métricas Financeiras

- PL Atual
- Ratio
- Spot Ref
- PL Máximo
- DTE Mín
- Breakevens

### Estado Operacional

- Eventos aplicados
- Cancelados ignorados
- Status

### Rationale / Why JSON

- Área de texto grande para rationale/JSON

### Auditoria & Ações

- Fonte
- Created At
- Botão Recalcular esta estrutura

Função esperada:

- Exibir detalhes da decisão selecionada
- Mostrar métricas calculadas
- Mostrar rationale/why JSON
- Permitir recalcular estrutura

Destino no novo layout:

- Deve ser transformado em painel de detalhes/contexto.
- A ação "Recalcular esta estrutura" precisa ser preservada ou explicitamente realocada.
- Campos podem ser reorganizados em cards.

## 6. Aba: Curva de Payoff

Controles visíveis:

- Toolbar Matplotlib:
  - Home
  - Back
  - Forward
  - Pan
  - Zoom
  - Configure/Subplots
  - Save
- Botão Limpar Comparação
- Botão Fixar Curva A
- Botão Exportar PNG

Elementos gráficos observados:

- Curva de Payoff vazia
- Payoff de estrutura/decisão selecionada
- Curva A fixada
- Comparação B vs Curva A
- Linha de Spot Ref
- Marcação de PL no Spot Ref
- Breakevens
- Legenda
- Eixos Spot e PL
- Formatação em R$

Status inferior observado:

- 101 pontos (payoff_curve_points)

Função esperada:

- Plotar payoff da decisão/estrutura selecionada
- Fixar curva A para comparação
- Limpar comparação
- Exportar imagem PNG
- Navegar/interagir no gráfico via Matplotlib

Destino no novo layout:

- Deve ser uma área principal de análise gráfica.
- Pode ser integrada ao painel principal junto com VWAP.
- Não deve recalcular payoff dentro da UI; deve consumir contrato/camada existente.

## 7. Aba: Estruturas

Controles visíveis:

- Status
- Busca
- Botão pequeno ao lado da busca
- Tabela de estruturas
- Painel de detalhes textual
- Botões:
  - + Nova
  - Editar
  - Duplicar
  - Arquivar

Colunas visíveis/parciais da tabela:

- ID
- Nome
- Ativo
- Aba legado

Detalhes textuais observados:

- ID
- Nome
- Ativo
- Aba legado
- Status
- Criado em
- Atualizado
- Obs
- Lista de legs/pernas

Estruturas observadas:

- ID 2: SBSP+SMAL=BOVA
- ID 3: PRIO

Pernas observadas:

- COMPRADO CALL
- VENDIDO CALL
- VENDIDO PUT
- COMPRADO PUT

Campos de legs observados:

- Strike
- Vencimento
- Quantidade
- Símbolo
- Prêmio
- Multiplicador

Função esperada:

- Listar estruturas
- Filtrar por status
- Buscar
- Criar nova estrutura
- Editar estrutura
- Duplicar estrutura
- Arquivar estrutura
- Exibir composição/pernas

Destino no novo layout:

- Deve virar painel lateral retrátil ou área de seleção de estruturas.
- Ações CRUD/arquivo precisam permanecer acessíveis.
- A seleção de estrutura deve alimentar payoff, VWAP e detalhes.

## 8. Aba: Terminal VWAP Payoff

Controles visíveis:

- Grupo Estruturas
- Botão Atualizar
- Botão Carregar
- Tabela de estruturas
- Painel direito com subabas:
  - Resumo
  - Legs
  - Payoff
  - Avisos

Subaba Resumo contém grupos:

### Estrutura

- ID
- Nome
- Ativo
- Status

### Mercado e VWAP

- Preço atual
- VWAP
- Preço vs VWAP
- Fonte
- Atualizado em

### Payoff

- Pontos
- Resultado mín.
- Resultado máx.
- Break-even

Subaba Legs contém tabela de pernas com colunas visíveis:

- #
- Símbolo
- Lado
- Tipo
- Strike

Status inferior observado:

- Estrutura 2 carregada no Terminal VWAP Payoff

Função esperada:

- Atualizar lista de estruturas
- Carregar estrutura no terminal
- Exibir resumo operacional
- Exibir legs
- Exibir payoff
- Exibir avisos
- Integrar VWAP e payoff por estrutura

Destino no novo layout:

- Deve ser incorporado como painel operacional principal.
- O conceito do anexo AppFinanceiraVwap.py pode aproveitar este fluxo:
  - lista/seleção de estrutura
  - análise VWAP
  - análise payoff
  - tabela de pernas
  - avisos/status

## 9. Componentes obrigatórios a preservar

A nova UI deve preservar ou realocar:

- Menus ou ações equivalentes de Arquivo/Ferramentas/Ajuda, caso tenham comandos reais.
- Filtros de decisão.
- Lista de decisões.
- Seleção de decisão.
- Detalhes da decisão.
- Rationale/Why JSON.
- Recalcular estrutura.
- Curva de payoff.
- Fixar curva A.
- Limpar comparação.
- Exportar PNG.
- Lista de estruturas.
- Busca de estruturas.
- Filtro de status.
- Nova estrutura.
- Editar estrutura.
- Duplicar estrutura.
- Arquivar estrutura.
- Terminal VWAP Payoff.
- Atualizar estruturas no terminal.
- Carregar estrutura no terminal.
- Resumo VWAP.
- Legs.
- Payoff.
- Avisos.
- Mensagens de status inferior.

## 10. Riscos identificados

Riscos se a UI atual for removida sem mapeamento:

- Perder ação de recalcular estrutura.
- Perder comparação de payoff com Curva A.
- Perder exportação PNG.
- Perder filtros atuais de decisão.
- Perder acesso a rationale/why JSON.
- Perder operações CRUD de estruturas.
- Perder arquivamento de estruturas.
- Perder fluxo Terminal VWAP Payoff.
- Perder status operacional inferior.
- Duplicar lógica de payoff na UI nova.
- Duplicar lógica de VWAP na UI nova.
- Conectar UI nova diretamente ao banco em vez de services/controllers.

## 11. Diretriz para substituição

A substituição da UI deve seguir este princípio:

- Primeiro mapear funcionalidades.
- Depois criar novo shell visual.
- Depois conectar cada área ao serviço/controller existente.
- Depois validar comportamento.
- Só então trocar o entrypoint.

