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

## 28. Integracao do patch de acoes laterais na main

O patch funcional das acoes laterais de estruturas do painel dark foi integrado na branch principal.

### 28.1. Estado registrado

Branch de trabalho anterior:

- patch-side-actions-structures

Branch principal atual:

- main

Commit integrado:

- f454cb2 fix(ui): corrige acoes laterais de estruturas no dark

Tag principal da rodada:

- checkpoint-modern-side-actions-structures-fix

### 28.2. Resultado da integracao

A integracao foi realizada por fast-forward, sem conflito manual.

A branch main passou a conter:

- UI moderna dark em paralelo
- painel dark de Terminal VWAP Payoff
- exportacao PNG validada
- acoes laterais de estruturas corrigidas
- relatorios de inventario, classificacao, validacao e patch
- auditoria atualizada ate a frente de acoes laterais

### 28.3. Publicacao remota

Foi executado push da branch main para o remoto.

Tambem foi executado push das tags locais.

Resultado final observado:

- main enviada para origin/main
- tags enviadas ao remoto
- segunda execucao de push confirmou Everything up-to-date

### 28.4. Fechamento da secao 27

A secao 27 fica considerada encerrada.

O patch validado de acoes laterais esta agora:

- testado manualmente
- compilado com py_compile
- commitado
- tageado
- integrado na main
- publicado no remoto

### 28.5. Restricoes preservadas

A integracao nao altera a diretriz arquitetural registrada anteriormente:

- a UI atual ainda nao deve ser eliminada
- o modo dark permanece como UI moderna paralela
- regra de negocio nao deve ser recriada na UI
- banco nao deve ser alterado junto com layout
- derived.db e app.db nao devem ter sincronismo continuo
- app.db permanece o destino canonico para mercado vivo

### 28.6. Proxima frente recomendada

A proxima frente deve voltar ao mapa de equivalencia funcional.

Frente recomendada:

- inventario dirigido de filtros, tabela e detalhe de decisoes no modo dark

Objetivo da proxima frente:

- identificar o que ja existe no modo dark relacionado a decisoes
- comparar com a UI atual auditada
- mapear lacunas de filtros, tabela, selecao, detalhe e rationale/why JSON
- nao alterar codigo antes do inventario
- produzir relatorio em reports/ui_modern_equivalence

### 28.7. Comandos de verificacao recomendados

Antes da proxima alteracao, recomenda-se validar o estado da main com:

- git status --short
- git log --oneline -8 --decorate
- python -m py_compile UI/modern/__main__.py UI/modern/app.py UI/modern/theme.py UI/modern/dark_window.py UI/components/terminal_vwap_payoff_dark_panel.py
- python -m UI.modern --info
- python -m UI.modern

### 28.8. Decisao

A proxima etapa autorizada e documental.

Nao iniciar novo patch funcional antes de concluir o inventario dirigido de decisoes no modo dark.

## 29. Inventario dirigido de decisoes, filtros e tabela no modo dark

Foi iniciado inventario dirigido das funcionalidades de decisoes no modo dark da UI moderna.

Relatorio gerado:

- reports/ui_modern_equivalence/11_inventario_decisoes_filtros_tabela_dark.md

### 29.1. Objetivo

Mapear, antes de qualquer patch funcional, a presenca ou ausencia de:

- filtros de decisoes
- tabela/listagem de decisoes
- selecao de decisao
- detalhe da decisao
- rationale/why JSON
- conexoes com controllers, services e repositories

### 29.2. Decisao de seguranca

Esta etapa e documental.

Nao altera:

- codigo funcional
- layout operacional
- callbacks
- banco
- regra de negocio
- contratos canonicos

### 29.3. Proximo passo

Ler o inventario gerado, classificar lacunas e definir o menor patch seguro para equivalencia parcial de decisoes no modo dark.

## 30. Classificacao das lacunas de decisoes no modo dark

Foi criada classificacao das lacunas de decisoes no modo dark a partir do inventario dirigido.

Relatorio gerado:

- reports/ui_modern_equivalence/12_classificacao_lacunas_decisoes_dark.md

### 30.1. Resultado

O modo dark ainda nao possui equivalencia funcional de decisoes.

Foram classificados como ausentes no modo dark:

- filtros de decisoes
- tabela/listagem de decisoes
- selecao de decisao
- detalhe da decisao
- rationale/why JSON no fluxo dark
- payoff acionado a partir de selecao de decisao

### 30.2. Componentes reaproveitaveis

A classificacao indica reaproveitamento provavel de componentes ja existentes:

- UI.components.filters_panel.FiltersPanel
- UI.components.decisions_grid.DecisionsGrid
- UI.components.details_panel.DetailsPanel
- fluxo de dados usado pelo shell moderno em UI/modern/main_window.py

### 30.3. Decisao de seguranca

A proxima etapa autorizada pode ser patch funcional minimo no modo dark para adicionar filtros, tabela e detalhe de decisoes.

Restricoes do patch futuro:

- nao criar regra de negocio na UI
- nao alterar banco
- nao alterar repositories, services ou controllers sem necessidade comprovada
- nao trocar entrypoint principal
- nao eliminar a UI atual
- manter o modo dark como UI moderna paralela

### 30.4. Proximo passo

Aplicar patch pequeno e restrito para equivalencia parcial de decisoes no modo dark, iniciando por:

- filtros
- tabela/listagem
- selecao
- detalhe

## 31. Historico de decisoes no painel dark

Foi implementado e validado o historico de decisoes operacionais por estrutura no painel dark da UI moderna.

Relatorio gerado:

- reports/ui_modern_equivalence/13_historico_decisoes_dark_panel.md

### 31.1. Objetivo

Registrar e exibir, no fluxo operacional da estrutura selecionada, as ultimas decisoes tomadas pelo usuario.

Decisoes cobertas:

- HOLD / Manter
- ADJUST / Ajustar
- CLOSE / Encerrar

### 31.2. Arquivo alterado

Arquivo alterado nesta rodada:

- UI/components/terminal_vwap_payoff_dark_panel.py

### 31.3. Persistencia criada

Foi criada, quando inexistente, a tabela:

- structure_decisions

Campos principais:

- id
- structure_id
- decision
- label
- note
- created_at

Tambem foi criado indice por structure_id para consulta do historico.

### 31.4. Resultado funcional

O painel dark passou a:

- registrar decisao operacional por estrutura;
- salvar label amigavel;
- salvar data e hora local;
- exibir bloco ULTIMAS DECISOES no painel lateral;
- manter o comportamento de CLOSE arquivando a estrutura;
- manter o modo dark como UI moderna paralela.

### 31.5. Validacao

Validacao manual executada:

- python -m UI.modern

Resultado observado:

- UI moderna abriu em modo dark;
- estruturas reais foram carregadas;
- estrutura ID 2 foi carregada;
- decisao HOLD foi registrada;
- historico apareceu na interface com data e hora;
- registro foi confirmado em dados/app.db na tabela structure_decisions.

Registro confirmado:

- structure_id: 2
- decision: HOLD
- label: Manter
- created_at: 2026-07-02 11:07:16

### 31.6. Commit funcional associado

Commit:

- 2830b8c Adiciona historico de decisoes no painel dark

### 31.7. Decisao de seguranca

A alteracao nao encerra a equivalencia funcional completa de decisoes registrada na secao 30.

Continuam pendentes:

- filtros globais de decisoes;
- tabela/listagem global de decisoes;
- selecao de decisao;
- detalhe da decisao;
- rationale/why JSON;
- payoff acionado a partir de decisao selecionada.

### 31.8. Proxima frente recomendada

A proxima frente deve continuar a secao 30.4, agora considerando que o historico operacional por estrutura ja existe.

Frente recomendada:

- equivalencia parcial de decisoes no modo dark

Escopo inicial:

- adicionar bloco/listagem global de decisoes no modo dark;
- reutilizar componentes existentes quando possivel;
- preservar filtros, tabela, selecao e detalhe;
- nao alterar banco sem necessidade;
- nao eliminar a UI atual;
- nao trocar entrypoint principal;
- nao recriar regra de negocio na UI.

---

## 32. Listagem global minima de decisoes no modo dark

### 32.1. Objetivo

Avancar a equivalencia parcial do fluxo de decisoes no modo dark, sem alterar a UI legada, sem trocar entrypoint principal e sem modificar banco de dados.

A frente foi orientada pelo inventario tecnico registrado em:

- reports/ui_modern_equivalence/14_decisions_flow_dark_inventory.md

### 32.2. Decisao tecnica

Foi adotada a opcao de adaptador minimo, em vez de reaproveitamento direto dos componentes existentes da UI clara.

Motivos:

- FiltersPanel, DecisionsGrid e DetailsPanel usam tkinter/ttk;
- o modo dark atual usa customtkinter;
- DetailsPanel possui acoplamentos maiores com recalc, derived.db, payoff e estado operacional;
- a primeira entrega funcional deveria reduzir risco e manter escopo pequeno.

### 32.3. Implementacao realizada

Foi criado o componente:

- UI/components/decisions_dark_panel.py

Responsabilidades do novo painel:

- carregar decisoes via UIDataModel.get_decisions();
- exibir listagem global simples em customtkinter;
- permitir selecao de decisao;
- exibir detalhe textual da decisao selecionada;
- preservar campos principais como timestamp, structure_id, decision, level, dte_min, pl_atual, pl_max, pl_pct_of_max e rationale/why quando disponivel;
- limitar exibicao inicial a 300 registros para evitar sobrecarga visual;
- nao alterar schema, tabelas ou regras de negocio.

O arquivo UI/modern/dark_window.py foi ajustado para:

- instanciar UIDataModel;
- criar CTkTabview;
- manter o Terminal VWAP na aba "Terminal VWAP";
- adicionar nova aba "Decisões";
- recarregar tambem a listagem de decisoes pelo menu Aplicacao > Atualizar.

### 32.4. Validacao manual

Comando executado:

- python -m py_compile UI/modern/dark_window.py UI/components/decisions_dark_panel.py
- python -m UI.modern

Resultado observado:

- aplicacao abriu no modo dark;
- painel Terminal VWAP continuou funcional;
- 4 estruturas foram carregadas;
- aba Decisões foi exibida;
- 8 decisoes foram carregadas no modo dark;
- selecao de decisoes alternou entre estruturas reais;
- detalhe textual foi atualizado conforme a decisao selecionada.

Logs observados:

- [ModernDarkUI] 4 estruturas carregadas
- [ModernDarkUI] 8 decisões carregadas no modo dark
- [ModernDarkUI] Decisão selecionada: estrutura=3, decisão=HOLD
- [ModernDarkUI] Decisão selecionada: estrutura=2, decisão=HOLD

### 32.5. Commit funcional associado

Commit:

- 004f0c0 feat(ui): adiciona listagem de decisoes no modo dark

Tag:

- checkpoint-modern-decisions-list-dark-minimal

### 32.6. Resultado funcional

A UI dark agora possui equivalencia parcial do fluxo de decisoes:

- listagem global de decisoes;
- selecao de decisao;
- detalhe textual simples;
- carregamento via UIDataModel existente;
- integracao ao shell dark por aba dedicada.

### 32.7. Pendencias conhecidas

Ainda nao foram migrados nesta frente:

- filtros avancados;
- grid completo equivalente ao DecisionsGrid;
- painel completo equivalente ao DetailsPanel;
- atualizacao do payoff a partir da decisao selecionada;
- acao direta para carregar a estrutura selecionada no Terminal VWAP;
- exportacao CSV da listagem dark;
- ordenacao/Busca textual no painel dark.

### 32.8. Proxima frente recomendada

A proxima frente deve conectar a decisao selecionada a uma acao operacional simples.

Opcoes recomendadas:

1. adicionar botao "Carregar estrutura no Terminal" na aba Decisões;
2. adicionar busca/filtro textual minimo por estrutura, decisao ou timestamp;
3. adicionar exportacao CSV da listagem de decisoes exibida.

Prioridade recomendada:

- carregar a estrutura da decisao selecionada no Terminal VWAP, se houver metodo seguro ja existente no TerminalVWAPPayoffDarkPanel.


---

## 33. Carregamento de estrutura a partir da decisao no modo dark

### 33.1. Objetivo

Conectar a listagem de decisoes do modo dark ao Terminal VWAP, permitindo que uma decisao selecionada carregue diretamente a estrutura associada.

A frente foi uma evolucao da entrega registrada na secao 32, que havia introduzido a listagem global minima de decisoes no modo dark.

### 33.2. Decisao tecnica

Foi adotada integracao por callback entre o painel de decisoes e a janela dark principal.

Motivos:

- manter DecisionsDarkPanel desacoplado do TerminalVWAPPayoffDarkPanel;
- evitar que o painel de decisoes conheca detalhes internos do terminal;
- preservar o Terminal VWAP como responsavel por carregar estrutura, pernas, mercado, payoff, KPIs, graficos e alertas;
- nao alterar banco de dados;
- nao modificar regra de negocio.

### 33.3. Inspecao previa

Foi confirmado que TerminalVWAPPayoffDarkPanel ja mantem as estruturas carregadas em:

- self.structures

Tambem foi confirmado metodo existente para carregamento operacional:

- select_structure(self, structure: Dict[str, Any]) -> None

Esse metodo ja executa o fluxo completo do Terminal VWAP:

- define selected_structure;
- carrega pernas;
- carrega mercado;
- carrega pontos de payoff;
- atualiza cabecalho;
- atualiza KPIs;
- renderiza pernas;
- renderiza graficos;
- renderiza alertas;
- renderiza painel de acoes da estrutura.

### 33.4. Implementacao realizada

O componente UI/components/decisions_dark_panel.py foi ajustado para receber callback opcional:

- on_load_structure

Foi adicionado o botao:

- Carregar estrutura no Terminal

Comportamento do botao:

- inicia desabilitado;
- habilita quando a decisao selecionada possui structure_id ou aba;
- ao clicar, chama o callback com o identificador da estrutura;
- exibe status quando nao ha decisao selecionada, quando a selecao e invalida ou quando nao ha callback disponivel.

O arquivo UI/modern/dark_window.py foi ajustado para:

- passar on_load_structure=self._load_structure_from_decision ao DecisionsDarkPanel;
- localizar a estrutura em self.panel.structures;
- recarregar estruturas se necessario;
- chamar self.panel.select_structure(selected);
- trocar a aba ativa para "Terminal VWAP";
- emitir status de sucesso ou erro.

### 33.5. Validacao manual

Comandos executados:

- python -m py_compile UI/modern/dark_window.py UI/components/decisions_dark_panel.py
- python -m UI.modern

Resultado observado:

- aplicacao abriu no modo dark;
- aba Decisões carregou as decisoes;
- botao "Carregar estrutura no Terminal" ficou ativo apos selecionar decisao com estrutura;
- clique no botao carregou a estrutura correspondente no Terminal VWAP;
- UI alternou para a aba Terminal VWAP;
- Terminal atualizou a analise ativa;
- fluxo funcionou para mais de uma estrutura.

Logs observados:

- [ModernDarkUI] Estrutura carregada: ID 3
- [ModernDarkUI] Estrutura 3 carregada a partir da decisão
- [ModernDarkUI] Estrutura carregada: ID 2
- [ModernDarkUI] Estrutura 2 carregada a partir da decisão

### 33.6. Commit funcional associado

Commit:

- 2b45b47 feat(ui): carrega estrutura da decisao no terminal dark

Tag:

- checkpoint-modern-decisions-load-structure-dark

### 33.7. Resultado funcional

A UI dark passa a oferecer fluxo operacional integrado:

- visualizar decisoes;
- selecionar uma decisao;
- carregar a estrutura associada diretamente no Terminal VWAP;
- continuar a analise pelo painel operacional ja existente.

### 33.8. Pendencias conhecidas

Ainda nao foram implementados nesta frente:

- filtro textual na listagem dark;
- filtros avancados equivalentes a FiltersPanel;
- grid completo equivalente ao DecisionsGrid;
- painel completo equivalente ao DetailsPanel;
- exportacao CSV;
- acao inversa Terminal VWAP -> Decisoes filtradas por estrutura;
- destaque visual persistente da decisao ja carregada.

### 33.9. Proxima frente recomendada

A proxima frente recomendada e adicionar busca/filtro textual minimo na aba Decisões.

Campos sugeridos para busca:

- structure_id;
- decision;
- timestamp;
- level;
- rationale/why.

Essa frente tem baixo risco, melhora bastante a usabilidade e nao exige alteracao de banco nem regra de negocio.

---

## 34. Busca por estrutura ativa na aba Decisoes dark

### 34.1. Objetivo

Adicionar busca textual na aba Decisoes do modo dark, mantendo o escopo operacional correto:

- buscar por ID da estrutura;
- buscar por nome da estrutura;
- exibir somente decisoes associadas a estruturas ativas;
- evitar busca em campos ruidosos como timestamp, rationale, why, level ou demais metadados internos.

A frente evoluiu diretamente a entrega da secao 33, que havia conectado a decisao selecionada ao carregamento da estrutura no Terminal VWAP.

### 34.2. Problema identificado

A primeira versao da busca textual foi ampla demais.

Ela permitia procurar em muitos campos da decisao, incluindo:

- timestamp;
- decision;
- level;
- rationale;
- why;
- why_json;
- demais chaves internas do registro.

Durante o teste manual, foi observado que isso gerava comportamento confuso:

- buscas por timestamp dependiam de sequencias numericas longas e pouco previsiveis;
- numeros soltos podiam coincidir com campos internos sem significado operacional;
- a busca deixava de refletir o uso real esperado na tela;
- o usuario precisava localizar decisoes a partir da estrutura, nao a partir dos metadados da decisao.

A diretriz operacional validada foi:

- a busca da aba Decisoes deve localizar decisoes por estrutura;
- estrutura significa ID ou nome;
- estruturas inativas nao devem participar da listagem principal.

### 34.3. Decisao tecnica

Foi mantido o componente DecisionsDarkPanel desacoplado do Terminal VWAP.

Para permitir que o painel de decisoes conheca as estruturas ativas sem acessar diretamente o terminal, foi criado callback opcional:

- get_structures

Responsabilidades:

- dark_window.py fornece as estruturas carregadas no Terminal VWAP;
- DecisionsDarkPanel monta indice local structure_id -> structure;
- DecisionsDarkPanel identifica estruturas ativas;
- DecisionsDarkPanel filtra decisoes com base nesse indice;
- DecisionsDarkPanel restringe a busca ao ID e nome/rotulo/descricao da estrutura.

Essa abordagem preserva:

- baixo acoplamento;
- ausencia de alteracao no banco;
- ausencia de alteracao em regras de negocio;
- compatibilidade com o fluxo ja existente do Terminal VWAP.

### 34.4. Implementacao realizada

Arquivo alterado:

- UI/components/decisions_dark_panel.py

Principais mudancas:

- adicionado atributo filtered_decisions;
- adicionado indice structure_index;
- adicionado conjunto active_structure_ids;
- adicionado campo de busca no cabecalho;
- adicionado botao Limpar;
- listagem passou a renderizar filtered_decisions;
- selecao passou a operar sobre filtered_decisions;
- carregamento da estrutura passou a usar a decisao filtrada selecionada;
- busca passou a ser aplicada em tempo real no evento KeyRelease;
- busca foi restringida a ID e nome/rotulo/descricao da estrutura;
- decisoes de estruturas inativas passaram a ser excluidas da listagem.

Campos considerados para nome/rotulo da estrutura:

- name;
- nome;
- label;
- title;
- titulo;
- título;
- description;
- descricao;
- descrição;
- structure_name;
- nome_estrutura;
- estrutura.

Campos considerados para status ativo/inativo de forma defensiva:

- active;
- is_active;
- ativo;
- enabled;
- status;
- state;
- situacao;
- situação.

Valores tratados como inativos incluem:

- inactive;
- inativo;
- inativa;
- closed;
- fechado;
- fechada;
- encerrado;
- encerrada;
- finalizado;
- finalizada;
- archived;
- arquivado;
- arquivada;
- deleted;
- removido;
- removida;
- cancelado;
- cancelada.

Arquivo alterado:

- UI/modern/dark_window.py

Principais mudancas:

- DecisionsDarkPanel passou a receber get_structures=self._get_structures_for_decisions;
- criado helper _get_structures_for_decisions;
- helper retorna self.panel.structures;
- se necessario, tenta recarregar estruturas via reload_structures.

### 34.5. Comportamento funcional validado

A aba Decisoes passou a apresentar busca ativa caractere a caractere.

Comportamento validado:

- buscar por ID da estrutura funciona;
- buscar por nome da estrutura funciona;
- busca por trechos do nome funciona;
- a listagem considera somente estruturas ativas;
- a selecao continua funcionando apos filtro;
- o botao "Carregar estrutura no Terminal" continua funcionando;
- ao carregar estrutura a partir da decisao, a UI alterna corretamente para o Terminal VWAP;
- a busca nao depende mais de timestamp nem campos internos ruidosos.

Exemplo validado:

- nome de estrutura no teste: SBSP+SMAL=BOVA;
- busca por ID funcionou;
- busca por nome/trecho funcionou;
- log indicou reducao da lista exibida para decisoes de estruturas ativas.

### 34.6. Validacao tecnica

Comandos executados:

- python -m py_compile UI/components/decisions_dark_panel.py UI/modern/dark_window.py
- python -m UI.modern

Resultado:

- compilacao sem erro;
- aplicacao abriu no modo dark;
- Terminal VWAP carregou estruturas;
- aba Decisoes carregou decisoes;
- filtro textual funcionou em tempo real;
- carregamento de estrutura a partir da decisao continuou funcional.

Logs observados:

- [ModernDarkUI] 4 estruturas carregadas
- [ModernDarkUI] 8 decisões carregadas no modo dark
- [ModernDarkUI] Decisão selecionada: estrutura=2, decisão=HOLD (3 de 8 exibidas)
- [ModernDarkUI] Estrutura carregada: ID 2
- [ModernDarkUI] Estrutura 2 carregada a partir da decisão

### 34.7. Commit funcional associado

Commit:

- bceedfa feat/ui): adiciona busca por estrutura ativa em decisoes dark

Observacao:

- a mensagem do commit foi publicada com pequeno desvio no padrao conventional commit: feat/ui) em vez de feat(ui);
- como o commit ja foi enviado ao repositorio remoto, nao foi reescrito historico apenas por esse detalhe.

Tag:

- checkpoint-modern-decisions-active-structure-search-dark

### 34.8. Resultado funcional

A UI dark passa a oferecer um fluxo operacional mais consistente para decisoes:

- listar decisoes relevantes;
- restringir a exibicao a estruturas ativas;
- buscar rapidamente por ID ou nome da estrutura;
- selecionar uma decisao;
- carregar a estrutura associada diretamente no Terminal VWAP.

A busca deixou de ser generica e passou a refletir o fluxo real de uso da tela.

### 34.9. Pendencias conhecidas

Ainda nao foram implementados nesta frente:

- exportacao CSV da listagem filtrada;
- filtros avancados equivalentes ao FiltersPanel legado;
- grid completo equivalente ao DecisionsGrid legado;
- painel completo equivalente ao DetailsPanel legado;
- destaque visual persistente da decisao ja carregada;
- acao inversa Terminal VWAP -> Decisoes filtradas pela estrutura selecionada;
- testes automatizados especificos para DecisionsDarkPanel.

### 34.10. Proxima frente recomendada

A proxima frente recomendada e uma das seguintes, em ordem sugerida:

1. exportar CSV da listagem filtrada de decisoes no modo dark;
2. enriquecer o detalhe da decisao com nome da estrutura e status ativo;
3. adicionar acao Terminal VWAP -> Decisoes filtradas pela estrutura selecionada;
4. iniciar equivalencia parcial com o DetailsPanel legado.

Prioridade recomendada:

- implementar exportacao CSV da listagem filtrada, pois reaproveita filtered_decisions, tem baixo risco e melhora a utilidade operacional da aba Decisoes sem alterar banco nem regra de negocio.

