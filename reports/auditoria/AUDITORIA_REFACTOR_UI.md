# Auditoria da Refatoração de UI

## 1. Objetivo

Controlar a evolução da refatoração de UI do projeto, garantindo que nenhuma alteração visual ou estrutural seja feita sem inventário prévio, teste acumulado e commit rastreável.

## 2. Escopo da fase atual

Fase atual:

- UI-1: Inventário e Auditoria Inicial

Objetivo da fase:

- Mapear arquivos relacionados à UI
- Mapear entrada da aplicação
- Mapear classes visuais
- Mapear controllers, services e repositories
- Mapear usos de banco
- Registrar riscos antes de qualquer alteração de layout

## 3. Regras explícitas do projeto

A) Não migrar para web.

B) Não utilizar emojis.

C) Manter-se ao escopo do projeto sem derivações.

D) Efetuar buscas de dados e arquivos antes de alterações.

E) Toda mudança deve ser testada após concluída.

F) Após o encerramento de fase, o teste deve compor todas as fases encerradas, sem pendências.

G) Evitar códigos intermediários em explicações, ir direto ao ponto.

H) Em alterações, sempre gerar código automatizado via Git Bash indentado.

I) A cada alteração concluída e testada, commitar.

J) Não codar sem rumo; se necessário, buscar a evolução no git.

K) Criar arquivo de auditoria para ser atualizado com os testes, conclusões e caminho de evolução.

L) Não gerar código com crase; manter comandos e scripts organizados e indentados.

M) Não manter sync contínuo: derived.db -> app.db.

N) Não manter app.db -> derived.db.

O) Não permitir dívida técnica; para cotação viva isso é risco operacional.

P) Após testes, a melhor resposta como arquitetura final é um único banco canônico para mercado vivo: app.db.

## 4. Baseline de segurança

Branch base:

- patch-side-actions-structures

Tag de segurança:

- baseline-pre-refatoracao-ui-layout-20260701

Status:

- Tag criada localmente e enviada ao remoto.

## 5. Inventário executado

Diretório:

- reports/ui_inventory

Arquivos gerados:

- 01_python_files.txt
- 02_ui_related_files.txt
- 03_ui_entrypoints.txt
- 04_ui_classes.txt
- 05_ui_actions_widgets.txt
- 06_ui_layout_navigation.txt
- 07_theme_styles.txt
- 08_controllers.txt
- 09_services.txt
- 10_repositories.txt
- 11_api_endpoints.txt
- 12_database_usage.txt
- 13_tests_all.txt
- 14_tests_names_sorted.txt

Contagem recebida:

- 179 arquivos Python
- 71 arquivos relacionados à UI, view, window, dialog, panel, widget, controller, viewmodel, terminal, payoff ou structure
- 553 ocorrências relacionadas a entrypoints/UI
- 27 classes relacionadas à UI
- 0 ocorrências em ações/widgets no grep inicial
- 0 ocorrências em layout/navegação no grep inicial
- 202 ocorrências relacionadas a tema/estilo/cor
- 6 controllers
- 45 services
- 19 repositories
- 61 ocorrências de API/endpoints
- 630 ocorrências de uso de banco
- 58 testes

## 6. Leitura técnica inicial

Conclusão 1:

- A UI existe, mas o grep inicial não encontrou widgets ou layouts tradicionais.
- Isso indica possível abstração, criação dinâmica, framework diferente ou padrões ainda não mapeados.

Conclusão 2:

- Existe volume relevante de estilo/tema, com 202 ocorrências.
- Antes de implementar layout novo, é necessário classificar onde tema e estilos são definidos.

Conclusão 3:

- A presença de controllers, services e repositories indica separação razoável de camadas.
- A nova UI deve consumir camadas existentes, sem recriar regra de negócio.

Conclusão 4:

- O uso de banco é crítico.
- Não será criado sync contínuo entre derived.db e app.db.
- O destino arquitetural para mercado vivo é app.db como banco canônico.

## 7. Riscos identificados

Risco 1:

- Alterar UI antes de mapear ações pode remover função operacional.

Mitigação:

- Mapear ações reais por chamadas, métodos e conexões antes da alteração.

Risco 2:

- Reativar dark mode sem entender o ponto de aplicação pode afetar componentes ou legibilidade.

Mitigação:

- Inventariar estilos, temas, palettes, colors e arquivos de stylesheet antes de aplicar tema.

Risco 3:

- Misturar refatoração de layout com mudança de banco pode gerar dívida técnica.

Mitigação:

- Separar fase de UI da fase de arquitetura de dados.

Risco 4:

- Manter derived.db e app.db sincronizados continuamente criaria risco operacional.

Mitigação:

- Não implementar sync contínuo em nenhuma direção.

## 8. Decisões arquiteturais registradas

Decisão 1:

- A aplicação continuará desktop.

Decisão 2:

- A nova UI será implementada sem migração web.

Decisão 3:

- A nova UI deve preservar as funções existentes.

Decisão 4:

- A nova UI não deve modificar regra de negócio.

Decisão 5:

- A arquitetura final para mercado vivo deve convergir para app.db como banco canônico único.

Decisão 6:

- derived.db não será mantido em sincronismo contínuo com app.db.

Decisão 7:

- app.db não será mantido em sincronismo contínuo com derived.db.

## 9. Testes da fase

Status atual:

- Inventário gerado.
- Auditoria criada.
- Nenhuma alteração funcional executada nesta etapa.

Teste obrigatório antes de encerrar UI-1:

- pytest

Teste manual recomendado:

- python run_ui.py

## 10. Pendências da fase UI-1

Pendência 1:

- Ler conteúdo dos principais inventários para montar a tabela mestre da UI atual.

Arquivos prioritários:

- reports/ui_inventory/02_ui_related_files.txt
- reports/ui_inventory/03_ui_entrypoints.txt
- reports/ui_inventory/04_ui_classes.txt
- reports/ui_inventory/07_theme_styles.txt
- reports/ui_inventory/08_controllers.txt
- reports/ui_inventory/09_services.txt
- reports/ui_inventory/10_repositories.txt
- reports/ui_inventory/12_database_usage.txt

Pendência 2:

- Descobrir por que os inventários de ações/widgets e layout/navegação vieram vazios.

Pendência 3:

- Gerar busca ampliada para métodos, comandos, callbacks, slots e chamadas indiretas.

Pendência 4:

- Montar tabela mestre:

Área | Tela/Componente | Arquivo | Classe | Ações | Dados usados | Serviço chamado | Risco | Destino no novo layout

## 11. Critério de fechamento da fase UI-1

A fase UI-1 somente poderá ser encerrada quando:

- A tabela mestre da UI atual estiver criada.
- As ações reais da UI estiverem mapeadas.
- Os pontos de entrada da UI estiverem identificados.
- O uso de tema/estilo estiver classificado.
- pytest estiver aprovado.
- python run_ui.py tiver sido executado com sucesso.
- O commit da fase tiver sido criado.

## 12. Busca complementar UI-1

Executada busca ampliada para localizar ações, callbacks, layout, framework de UI, classes arquiteturais, conexões de banco e termos de negócio.

Arquivos gerados:

- reports/ui_inventory_deep/01_actions_callbacks_deep.txt
- reports/ui_inventory_deep/02_layout_navigation_deep.txt
- reports/ui_inventory_deep/03_ui_framework_detection.txt
- reports/ui_inventory_deep/04_architecture_classes.txt
- reports/ui_inventory_deep/05_database_connection_points.txt
- reports/ui_inventory_deep/06_business_terms_deep.txt

Contagem:

  2130 reports/ui_inventory_deep/01_actions_callbacks_deep.txt
  1495 reports/ui_inventory_deep/02_layout_navigation_deep.txt
   118 reports/ui_inventory_deep/03_ui_framework_detection.txt
    56 reports/ui_inventory_deep/04_architecture_classes.txt
   574 reports/ui_inventory_deep/05_database_connection_points.txt
  5841 reports/ui_inventory_deep/06_business_terms_deep.txt
 10214 total

## 13. Diretriz de novo layout baseada no anexo AppFinanceiraVwap.py

Foi analisado o arquivo de referência visual:

- AppFinanceiraVwap.py

Este arquivo não será adotado como implementação funcional do sistema. Ele será usado apenas como referência de layout e interação.

### 13.1. Elementos aproveitáveis do anexo

Serão considerados como referência para a nova UI:

- Aplicação desktop em CustomTkinter
- Aparência escura
- Barra lateral fixa
- Painel lateral retrátil para seleção de estruturas
- Área principal ampliada para análise
- Bloco visual de VWAP
- Bloco visual de Payoff
- Rodapé com componentes/pernas da estrutura
- Fluxo operacional de seleção de estrutura e foco na análise

### 13.2. Elementos descartados do anexo

Serão descartados integralmente:

- Banco fictício ESTRUTURAS_DB
- Dados simulados de estruturas
- Dados simulados de VWAP
- Dados simulados de payoff
- Uso de np.random para geração de mercado
- Cálculos de negócio implementados diretamente na UI
- Qualquer regra operacional embutida na camada visual

### 13.3. Diretriz arquitetural

A nova UI não definirá a regra do sistema.

Decisão registrada:

- A UI não molda o sistema.
- O sistema molda a UI.
- A nova interface será apenas uma camada visual conectada às funcionalidades já existentes.
- A regra de negócio continuará nos controllers, services, repositories e contratos canônicos atuais.
- A UI deve apenas orquestrar seleção, exibição, acionamento e atualização visual.

### 13.4. Destino da nova tela operacional

O novo layout deverá conter, no mínimo:

- Menu lateral fixo
- Painel lateral retrátil de estruturas
- Painel principal de análise
- Área de VWAP
- Área de Payoff
- Área de pernas/componentes da estrutura
- Espaço para status operacional
- Espaço para mensagens de validação/erro
- Integração com dados reais do sistema

### 13.5. Conexões funcionais obrigatórias

A nova UI deverá se conectar às camadas existentes, sem duplicar lógica:

- Estruturas
- Pernas da estrutura
- Eventos de estrutura
- Payoff
- Terminal VWAP Payoff
- Precificação
- Snapshots de mercado
- RTD/mercado vivo quando aplicável
- Serviços e controllers já testados

### 13.6. Restrições para implementação

Durante a substituição da UI atual:

- Não migrar para web.
- Não criar regra de negócio dentro da UI.
- Não usar dados simulados como fonte operacional.
- Não manter sync contínuo entre derived.db e app.db.
- Não criar dívida técnica.
- Não remover funcionalidade sem mapeamento prévio.
- Não alterar banco junto com layout sem fase específica.
- Não substituir a UI atual antes de mapear seus pontos de entrada e ações reais.
- Não implementar componentes visuais sem conexão prevista com serviço/controller existente.

### 13.7. Situação quanto à prontidão para alteração de UI

Status atual:

- Já existe inventário inicial.
- Já existe busca complementar.
- Testes automatizados passaram.
- A UI atual executou com sucesso via run_ui.py.
- O layout-alvo já possui referência visual.
- Ainda falta consolidar a tabela mestre da UI atual antes da eliminação da UI existente.

Conclusão:

- Há dados suficientes para desenhar o layout-alvo e planejar a substituição.
- Ainda não há segurança completa para eliminar a UI atual sem antes consolidar os pontos de entrada, componentes, ações e conexões reais.
- A próxima etapa deve ser a tabela mestre da UI atual e o plano de substituição por fases.


## 14. Auditoria visual da UI atual com base nos prints

Foram analisados prints da interface atual antes da substituição do layout.

Esta análise visual foi adicionada aos relatórios:

- reports/ui_visual_audit/01_prints_visual_controls.md
- reports/ui_visual_audit/02_code_concordance_visual_terms.txt
- reports/ui_visual_audit/03_menus.txt
- reports/ui_visual_audit/03_buttons.txt
- reports/ui_visual_audit/03_combos.txt
- reports/ui_visual_audit/03_tabs_notebooks.txt
- reports/ui_visual_audit/03_tables.txt
- reports/ui_visual_audit/03_bindings.txt
- reports/ui_visual_audit/03_matplotlib.txt
- reports/ui_visual_audit/03_services_controllers.txt

### 14.1. Controles visuais identificados

A UI atual contém os seguintes blocos funcionais:

- Menu superior:
  - Arquivo
  - Ferramentas
  - Ajuda

- Painel de filtros:
  - Período De/Até
  - Estrutura
  - Decisão
  - Level >=
  - DTE <=
  - Aplicar
  - Limpar
  - Indicador de filtros aplicados

- Tabela de decisões:
  - Data/Hora
  - Estrutura
  - Decisão
  - Nível
  - Ratio %
  - DTE
  - PL Atual
  - PL Máx

- Abas principais:
  - Detalhes da Decisão
  - Curva de Payoff
  - Estruturas
  - Terminal VWAP Payoff

- Ações de payoff:
  - Limpar Comparação
  - Fixar Curva A
  - Exportar PNG
  - Interações padrão da toolbar Matplotlib

- Ações de estruturas:
  - + Nova
  - Editar
  - Duplicar
  - Arquivar
  - Filtro por status
  - Busca

- Ações do Terminal VWAP Payoff:
  - Atualizar
  - Carregar
  - Subabas Resumo, Legs, Payoff e Avisos

- Ação operacional:
  - Recalcular esta estrutura

### 14.2. Diretriz de preservação funcional

A substituição visual não poderá remover implicitamente:

- filtros de decisões
- seleção de decisões
- detalhamento de decisão
- rationale/why JSON
- recalcular estrutura
- curva de payoff
- comparação por Curva A
- exportação PNG
- CRUD/arquivamento de estruturas
- terminal VWAP Payoff
- resumo de VWAP
- legs
- payoff
- avisos
- mensagens de status

Qualquer remoção deve ser decisão explícita, documentada e testada.

### 14.3. Relação com o novo layout

O layout de referência AppFinanceiraVwap.py continua sendo apenas referência visual.

Elementos aproveitáveis:

- barra lateral fixa
- painel retrátil de estruturas
- área principal de análise
- blocos para VWAP e Payoff
- rodapé/tabela de pernas
- foco operacional após seleção de estrutura

Elementos proibidos na implementação real:

- banco fictício
- simulação de mercado
- simulação de payoff
- cálculo de regra de negócio dentro da UI
- fonte operacional fora dos services/controllers existentes

### 14.4. Próxima etapa autorizada

Após conferência dos relatórios de auditoria visual, a próxima etapa poderá ser a preparação do novo shell visual em paralelo.

A UI atual ainda não deve ser eliminada diretamente.

Sequência recomendada:

1. Criar novo layout em paralelo.
2. Conectar painel de estruturas aos services/controllers existentes.
3. Conectar painel de payoff aos contratos existentes.
4. Conectar painel VWAP/Terminal aos services existentes.
5. Preservar filtros e tabela de decisões ou realocá-los no novo layout.
6. Validar manualmente.
7. Rodar testes.
8. Trocar entrypoint somente após equivalência funcional mínima.


## 15. Evolução executada após autorização do shell visual paralelo

Após a diretriz registrada na seção 14.4, foi iniciada a preparação do novo shell visual em paralelo, sem eliminar a UI atual.

A implementação seguiu a restrição principal da auditoria:

- a UI atual não foi removida;
- a regra de negócio não foi recriada na camada visual;
- os launchers antigos foram preservados;
- a evolução foi feita em checkpoints pequenos e rastreáveis;
- o novo layout moderno permanece paralelo até equivalência funcional mínima.

### 15.1. Checkpoints criados nesta frente

Foram criados os seguintes checkpoints locais:

- checkpoint-ui-audit-before-new-layout
- checkpoint-modern-ui-shell-opens
- checkpoint-modern-dark-ui-opens
- checkpoint-modern-unified-entrypoint
- checkpoint-modern-package-entrypoint
- checkpoint-modern-launcher-info

Commits associados na branch atual:

- bbd71f2 docs: registra auditoria e diretriz do novo layout desktop
- 05853ce docs: adiciona auditoria visual da UI atual
- ebcd5b3 feat(ui): adiciona shell paralelo para novo layout desktop
- 9402a43 feat(ui): adiciona launcher paralelo para layout dark
- 037fed2 feat(ui): adiciona entrypoint moderno unificado
- 8492f4b feat(ui): permite executar pacote moderno diretamente
- 38c2ff1 feat(ui): adiciona diagnostico ao launcher moderno

### 15.2. Estado atual da UI moderna

Foi criado um pacote moderno executável diretamente por módulo Python.

Comando canônico atual:

- python -m UI.modern

Modos disponíveis:

- python -m UI.modern --mode dark
- python -m UI.modern --mode shell

Diagnóstico disponível sem abrir janela:

- python -m UI.modern --info
- python -m UI.modern --mode shell --theme clean --info

O modo padrão atual é:

- dark

O módulo aberto por padrão é:

- UI.modern.dark_window

O modo shell permanece disponível como referência temporária:

- UI.modern.main_window

### 15.3. Decisão arquitetural sobre entrypoint moderno

Decisão registrada:

- UI.modern passa a ser o ponto de entrada canônico da UI moderna em paralelo.
- O modo dark é a base visual preferencial em evolução.
- O modo shell permanece como referência temporária para comparação e preservação de direção.
- Nenhum dos dois substitui a UI atual até validação funcional mínima.
- Novas features não devem ser adicionadas ao shell temporário sem decisão documentada.
- A evolução visual deve convergir para o modo dark ou para um sucessor documentado dele.

### 15.4. Regras de continuidade a partir deste ponto

Antes de novas alterações em layout, tema, navegação, painel lateral, payoff, VWAP, estruturas ou terminal:

- consultar este documento;
- verificar os checkpoints existentes;
- conferir se a alteração preserva a diretriz da seção 14.2;
- não remover função operacional sem decisão explícita;
- não duplicar regra de negócio na UI;
- não alterar banco junto com layout sem fase específica;
- atualizar esta auditoria após cada checkpoint relevante.

### 15.5. Validações executadas

Foram executadas validações de sintaxe e abertura dos entrypoints modernos.

Validação de compilação:

- python -m py_compile UI/modern/__main__.py UI/modern/app.py UI/modern/theme.py

Validação do pacote moderno:

- python -m UI.modern

Resultado observado:

- abertura da UI moderna em modo dark;
- carregamento de estruturas reais;
- log indicando ModernDarkUI com estruturas carregadas.

Validação do modo shell:

- python -m UI.modern --mode shell

Resultado observado:

- abertura do shell moderno;
- uso do banco derived.db;
- uso do contrato canônico para payoff_curve_points.

Validação do diagnóstico:

- python -m UI.modern --info
- python -m UI.modern --mode shell --theme clean --info

Resultado observado:

- impressão de mode;
- impressão de theme;
- impressão de appearance_mode;
- impressão de module;
- impressão de project_root;
- impressão de python;
- impressão de python_version;
- impressão de platform.

### 15.6. Pendências abertas da frente moderna

Pendência 1:

- Consolidar a tabela mestre da UI atual prevista na seção 10.

Pendência 2:

- Mapear explicitamente quais funções da UI atual já aparecem no novo layout moderno e quais ainda faltam.

Pendência 3:

- Classificar os tokens visuais hardcoded do arquivo UI/modern/dark_window.py.

Pendência 4:

- Integrar gradualmente UI/modern/theme.py ao layout dark, sem alterar regra de negócio.

Pendência 5:

- Preservar ou realocar filtros, tabela de decisões, payoff, comparação Curva A, exportação PNG, CRUD de estruturas e Terminal VWAP Payoff.

Pendência 6:

- Definir critério objetivo para considerar o modo dark equivalente o suficiente para substituir o shell temporário.

### 15.7. Próxima etapa autorizada

A próxima etapa autorizada não é eliminar a UI atual.

A próxima etapa autorizada é documental e de mapeamento:

1. atualizar esta auditoria com o estado da UI moderna;
2. criar ou complementar a tabela mestre de equivalência funcional;
3. mapear funções preservadas, ausentes e realocadas;
4. somente depois iniciar a troca de tokens visuais hardcoded por tema centralizado.

A próxima alteração de código recomendada, após esta atualização documental, será pequena e restrita:

- inventariar cores e estilos hardcoded em UI/modern/dark_window.py;
- substituir apenas tokens visuais por chamadas ao tema central;
- não mudar layout funcional;
- não mudar banco;
- não mudar regra de negócio;
- validar com python -m UI.modern, python -m UI.modern --info e py_compile.

## 16. Mapa de equivalência funcional da UI moderna

Foi criada a primeira versão do mapa de equivalência funcional entre a UI atual auditada e a UI moderna em paralelo.

Relatório gerado:

- reports/ui_modern_equivalence/01_mapa_equivalencia_funcional_ui_moderna.md

### 16.1. Objetivo do mapa

O mapa existe para impedir avanço visual sem controle funcional.

Ele compara as funções obrigatórias registradas na seção 14.2 com evidências textuais nos arquivos atuais de UI.modern.

### 16.2. Critério adotado

O relatório não declara equivalência funcional final.

Critério usado:

- ausência textual indica pendência;
- presença apenas no shell indica que a função ainda não está confirmada no caminho preferencial;
- presença no dark indica evidência parcial;
- equivalência final exige validação manual e, quando aplicável, teste.

### 16.3. Funções obrigatórias avaliadas

Foram avaliadas as seguintes funções:

- filtros de decisões;
- seleção de decisões;
- detalhamento de decisão;
- rationale/why JSON;
- recalcular estrutura;
- curva de payoff;
- comparação Curva A;
- exportação PNG;
- CRUD e arquivamento de estruturas;
- Terminal VWAP Payoff;
- legs/pernas da estrutura;
- mensagens de status;
- banco e contratos canônicos.

### 16.4. Decisão de continuidade

A UI atual ainda não será removida.

O modo dark continua sendo o caminho preferencial da UI moderna.

O shell continua como referência temporária.

A próxima alteração de código autorizada permanece pequena e restrita:

- inventariar tokens visuais hardcoded em UI/modern/dark_window.py;
- substituir tokens visuais por tema centralizado;
- não mudar layout funcional;
- não mudar regra de negócio;
- não mudar banco;
- validar abertura e diagnóstico do launcher moderno.

## 17. Inventário de tokens visuais da UI moderna

Foi criada a primeira etapa da rodada de tema da UI moderna.

Relatório gerado:

- reports/ui_modern_theme/01_inventario_tokens_visuais_dark.md

### 17.1. Objetivo

Identificar cores, dimensões e parâmetros visuais hardcoded em:

- UI/modern/dark_window.py
- UI/modern/theme.py

### 17.2. Restrição desta etapa

Esta etapa não altera código.

Ela apenas prepara o patch de centralização visual.

### 17.3. Decisão de continuidade

A próxima alteração de código autorizada será restrita a:

- UI/modern/theme.py
- UI/modern/dark_window.py

Escopo permitido:

- centralizar tokens visuais;
- substituir cores hardcoded por constantes/funções de tema;
- manter o mesmo layout funcional;
- manter os mesmos callbacks;
- manter os mesmos textos operacionais;
- não alterar banco;
- não alterar regra de negócio.

Validações obrigatórias após o patch:

- python -m py_compile UI/modern/__main__.py UI/modern/app.py UI/modern/theme.py UI/modern/dark_window.py
- python -m UI.modern --info
- python -m UI.modern

## 18. Centralização inicial dos tokens de tema CustomTkinter

Foi executada a primeira alteração de código da rodada de tema da UI moderna.

### 18.1. Arquivos alterados

Arquivos alterados:

- UI/modern/theme.py
- UI/modern/dark_window.py

### 18.2. Escopo da alteração

A alteração foi restrita a tokens visuais de inicialização do CustomTkinter.

Foram centralizados em UI/modern/theme.py:

- modo de aparência do CustomTkinter;
- tema base do CustomTkinter.

O modo dark passou a consumir estes tokens, em vez de literais diretos.

### 18.3. Restrições preservadas

A alteração não modificou:

- layout funcional;
- callbacks;
- consultas de banco;
- controllers;
- services;
- repositories;
- regra de negócio;
- textos operacionais;
- contratos canônicos.

### 18.4. Validações obrigatórias

Validações executadas nesta rodada:

- python -m py_compile UI/modern/__main__.py UI/modern/app.py UI/modern/theme.py UI/modern/dark_window.py
- python -m UI.modern --info
- python -m UI.modern

Resultado observado:

- diagnóstico do launcher moderno funcionando;
- abertura da UI moderna em modo dark;
- manutenção do carregamento de estruturas reais;
- ausência de regressão visual ou funcional perceptível.

### 18.5. Decisão de continuidade

A próxima etapa não é trocar a UI atual.

A próxima etapa recomendada é validar manualmente a equivalência parcial do modo dark contra o mapa criado em:

- reports/ui_modern_equivalence/01_mapa_equivalencia_funcional_ui_moderna.md

Prioridade da próxima rodada:

- confirmar visualmente o que já existe no modo dark;
- separar funções preservadas, ausentes e realocadas;
- só depois iniciar implementação funcional faltante por blocos pequenos.

## 19. Validação manual de equivalência funcional do modo dark

Foi criada a etapa de validação manual do modo dark contra o mapa de equivalência funcional.

Relatório gerado:

- reports/ui_modern_equivalence/02_validacao_manual_modo_dark.md

### 19.1. Objetivo

Validar manualmente o caminho preferencial da UI moderna antes de qualquer troca de entrypoint.

A validação compara o modo dark com as funções obrigatórias registradas no mapa:

- reports/ui_modern_equivalence/01_mapa_equivalencia_funcional_ui_moderna.md

### 19.2. Escopo

Esta etapa é documental e manual.

Ela não altera:

- código;
- layout;
- banco;
- callbacks;
- services;
- controllers;
- repositories;
- regra de negócio.

### 19.3. Decisão de continuidade

A UI atual permanece como caminho principal.

O modo dark continua como caminho moderno paralelo.

A próxima implementação funcional só deve ocorrer após classificação manual das funções como:

- validada;
- parcial;
- ausente;
- realocada;
- não testada.

### 19.4. Correção da tabela de validação manual

A tabela do relatório manual foi normalizada para manter o status na coluna correta.

Correção aplicada:

- status manual movido para a coluna Status manual;
- evidências resumidas na coluna Evidência/observação;
- próximas ações preenchidas sem alterar código;
- conclusões manuais marcadas conforme validação observada.

A correção não altera:

- código;
- layout;
- callbacks;
- banco;
- services;
- regra de negócio.

## 20. Inventário técnico da exportação PNG

Foi criada uma etapa documental para mapear a exportação PNG antes de qualquer implementação.

Relatório gerado:

- reports/ui_modern_equivalence/03_inventario_exportacao_png.md

### 20.1. Objetivo

Localizar pontos existentes relacionados a PNG, savefig, canvas, matplotlib, exportação e payoff.

### 20.2. Decisão de segurança

Nenhuma alteração funcional deve ser feita antes da leitura do inventário.

O modo dark permanece paralelo.

A UI atual permanece como caminho principal.

## 21. Inventário focado da exportação PNG

Foi criado um inventário focado para reduzir o ruído do levantamento amplo de exportação PNG.

Relatório gerado:

- reports/ui_modern_equivalence/04_inventario_focado_exportacao_png.md

### 21.1. Objetivo

Localizar apenas pontos relevantes da UI relacionados a gráfico, canvas, arquivo PNG e exportação.

### 21.2. Decisão de segurança

Esta etapa não altera código funcional.

O patch de exportação PNG só deve ser feito após identificar o arquivo alvo.

## 22. Exportação PNG no painel dark

Foi implementada exportação PNG do gráfico de Payoff no painel dark.

Relatório gerado:

- reports/ui_modern_equivalence/05_exportacao_png_dark_panel.md

### 22.1. Arquivos verificados

- UI/components/terminal_vwap_payoff_dark_panel.py alterado nesta rodada
- ui/components/terminal_vwap_payoff_dark_panel.py já possuía implementação equivalente

### 22.2. Decisão de segurança

O patch é isolado na UI dark.

Não altera banco, contratos canônicos, decisões ou cálculo.

A UI atual permanece como caminho principal.

## 23. Validação da exportação PNG no painel dark

A exportação PNG do gráfico de Payoff no painel dark foi validada manualmente.

Relatório gerado:

- reports/ui_modern_equivalence/06_validacao_exportacao_png_dark_panel.md

### 23.1. Resultado

A funcionalidade foi considerada 100 por cento funcional.

### 23.2. Evidência operacional

A execução de python -m UI.modern abriu a UI moderna em modo dark, carregou estruturas, carregou uma estrutura e registrou Payoff exportado em PNG.

### 23.3. Decisão

Checkpoint de validação manual recomendado: checkpoint-modern-export-png-dark-panel-validated.

## 24. Inventario das acoes laterais de estruturas no painel dark

Foi iniciado o inventario das acoes laterais de estruturas na UI moderna dark.

Relatorio gerado:

- reports/ui_modern_equivalence/07_acoes_laterais_estruturas_dark_panel.md

### 24.1. Objetivo

Mapear botoes, callbacks e comandos relacionados a estruturas antes de aplicar novo patch funcional.

### 24.2. Decisao de seguranca

Nenhuma regra de negocio deve ser alterada nesta etapa.

### 24.3. Proximo passo

Classificar lacunas e escolher o menor patch seguro para equivalencia das acoes laterais de estruturas.

## 25. Classificacao das acoes laterais de estruturas no painel dark

As acoes laterais de estruturas da UI moderna dark foram classificadas quanto a presenca visual e callbacks.

Relatorio gerado:

- reports/ui_modern_equivalence/08_classificacao_acoes_laterais_estruturas_dark_panel.md

### 25.1. Resultado

O painel dark indica cobertura das principais acoes laterais de estruturas.

### 25.2. Acoes classificadas

- recarregar estruturas
- nova estrutura
- selecionar estrutura
- recalcular payoff
- editar pernas
- duplicar estrutura
- arquivar estrutura
- registrar decisoes HOLD, CLOSE e ADJUST
- abrir bloco de ajuste
- voltar para lista

### 25.3. Decisao de seguranca

Nenhuma alteracao funcional foi aplicada nesta etapa.

### 25.4. Proximo passo

Executar validacao manual dirigida das acoes laterais no modo dark.

## 26. Validacao manual das acoes laterais de estruturas no painel dark

Foi executada validacao manual dirigida das acoes laterais de estruturas na UI moderna dark.

Relatorio gerado:

- reports/ui_modern_equivalence/09_validacao_manual_acoes_laterais_estruturas_dark_panel.md

### 26.1. Resultado

A validacao encontrou acoes funcionais, acoes parciais e falhas a corrigir.

### 26.2. Acoes funcionais

- recarregar estruturas
- abrir lista de estruturas
- selecionar estrutura
- editar pernas
- voltar para lista
- abrir acoes da estrutura

### 26.3. Acoes parciais

- recalcular Payoff executa, mas precisa feedback operacional visivel
- encerrar estrutura registra decisao CLOSE no console, mas precisa feedback operacional visivel

### 26.4. Falhas

- duplicar estrutura falha por metodo _cmd_duplicate nao encontrado neste componente
- abrir ajuste nao funciona no fluxo manual
- arquivar estrutura nao funciona no fluxo manual

### 26.5. Decisao

A proxima etapa deve aplicar patch funcional minimo restrito ao painel dark.

## 27. Patch funcional das acoes laterais de estruturas no painel dark

Foi aplicado patch funcional minimo nas acoes laterais de estruturas da UI moderna dark.

Relatorio gerado:

- reports/ui_modern_equivalence/10_patch_acoes_laterais_estruturas_dark_panel.md

### 27.1. Correcoes

- duplicacao implementada localmente com StructuresRepository
- feedback visual adicionado para recalculo e decisoes
- bloco de ajuste tornou-se visualmente explicito
- arquivamento recebeu validacao e feedback adicional
- decisao CLOSE passou a arquivar a estrutura via StructuresRepository.archive_structure

### 27.2. Decisao de seguranca

O patch ficou restrito aos arquivos do painel dark e seu espelho ui.

### 27.3. Validacao

- py_compile executado nos caminhos UI e ui
- validacao manual executada na UI moderna dark
- estruturas encerradas deixaram de aparecer em list_structures padrao

### 27.4. Proximo passo

Registrar checkpoint git do patch validado.
