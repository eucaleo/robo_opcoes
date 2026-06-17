# Fase 3 — Inventário de documentos vivos vs históricos

Data: 2026-06-17 09:46:30 -0300

## Objetivo

Inventariar documentos vivos, decisões, checkpoints históricos e artefatos documentais para orientar a reconciliação sem alterar código funcional.

## Estado Git inicial

```text
## fase-12-fechamento-ciclo...origin/fase-12-fechamento-ciclo
?? docs/checkpoints/fase-3-inventario-documentos-vivos-historicos.md
```

## Últimos commits

```text
0c994c4 docs: valida supersessao da ponte RTD
4cb4f50 docs: registra supersessao de LISTA_RTD xlsx
f53d74d docs: classifica referencias remanescentes LISTA_RTD
eb913ca docs: registra reconciliacao da ponte RTD oficial
6c68f37 chore: permite versionamento da ponte RTD oficial
3889e42 docs: oficializa LISTA_RTD.xlsm como ponte RTD
1750e0d docs: encerra fase 1 de higiene git
cb92957 docs: adiciona evidencias de auditoria de uso
440c6d5 docs: substitui referencia da planilha RTD legada
9cac302 docs: encerra fase 0 da ROTA_MESTRE_3
```

## Documentos principais em docs/

```text
docs/3A_CONSOLIDADO.md
docs/3B_CLOSURE_REPORT.md
docs/AUDITORIA_FASE_11_SNAPSHOTS_HISTORICO.md
docs/AUDITORIA_ROTA_MESTRE_2.md
docs/AUDITORIA_ROTA_MESTRE_3.md
docs/CONSOLIDADO_V1B_FINAL.md
docs/DATABASE_LOCATOR.md
docs/DB_PATHS.md
docs/EVOLUCAO_PRICING_PAYOFF.md
docs/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md
docs/FASE_3_CLASSIFICACAO_FONTES_DADOS.md
docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md
docs/FASE_5_ISOLAMENTO_BRIDGE_EXCEL_ADAPTADOR_LEGADO.md
docs/FASE_6_CAMADA_CANONICA_LEITURA.md
docs/FASE_7_ISOLAMENTO_NOMES_FISICOS_LEGADOS.md
docs/MAPA_MODULOS_FUNCOES.md
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md
docs/ROTA_MESTRE_3_RECONCILIACAO_POS_BACKUP.md
docs/SQL_SURFACE_MAP_v2.md
docs/auditoria_fase_9_cadastro_estruturas.md
docs/baseline_v1.md
docs/baseline_v1a.md
docs/baseline_v2.md
docs/changelog.md
docs/executed_v1.md
docs/fase_2_auditoria_contrato_rtd_excel.md
docs/fase_2_diagnostico_csvs_rtd_excel.json
docs/fase_2_diagnostico_csvs_rtd_excel.md
docs/fase_2_mapa_contrato_rtd_excel.md
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md
docs/fase_8_banco_fonte_verdade_auditoria.md
docs/lista_priorizada_automacao_opcoes_rtd.md
docs/mapeamento_automacao_opcoes_rtd.json
docs/mapeamento_automacao_opcoes_rtd.md
docs/roteiro_v2.md
```

## Decisões registradas

```text
docs/decisions/2026-06-17-supersessao-lista-rtd-xlsx.md
docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md
docs/decisions/structure_ref_created_at.md
```

## Checkpoints existentes

```text
docs/checkpoints/ciclo-2-fase-7a-auditoria-rtd-opcoes.md
docs/checkpoints/ciclo-2-fase-7b-auditoria-escrita-importacao-rtd-opcoes.md
docs/checkpoints/ciclo-2-sql-timestamp-clean.md
docs/checkpoints/fase-2-1-classificacao-referencias-lista-rtd.md
docs/checkpoints/fase-2-2-validacao-supersessao-lista-rtd.md
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md
docs/checkpoints/fase-3-inventario-documentos-vivos-historicos.md
docs/checkpoints/fase-7d-testes-importador-rtd-option-quotes.md
docs/checkpoints/fase-7e-auditoria-rtd-option-quotes.md
docs/checkpoints/fase-7f-pipeline-rtd-option-quotes.md
docs/checkpoints/fase-7g-seed-rtd-option-quotes-dados-atuais.md
docs/checkpoints/fase-7h-pipeline-lista-rtd-option-quotes.md
docs/checkpoints/fase-8a-auditoria-integracao-rtd-option-quotes-snapshot.md
docs/checkpoints/fase-8b-diagnostico-reconciliacao-rtd-option-quotes.txt
docs/checkpoints/fase-8b-reconciliacao-estruturas-legs-rtd-option-quotes.md
docs/checkpoints/fase-8c-conclusao-origem-verdade-legs.md
docs/checkpoints/fase-8c-diagnostico-origem-verdade-legs.txt
docs/checkpoints/fase-8d-auditoria-arquivos-chave-rtd.txt
docs/checkpoints/fase-8d-auditoria-codigo-funcional-rtd.txt
docs/checkpoints/fase-8d-auditoria-facade-snapshot-rtd.txt
docs/checkpoints/fase-8d-auditoria-fluxo-preco-rtd.txt
docs/checkpoints/fase-8d-auditoria-pontos-integracao-rtd.txt
docs/checkpoints/fase-8d-base-patch-rtd-option-quotes.txt
docs/checkpoints/fase-8d-before-canonical_pricing_facade-v2.py
docs/checkpoints/fase-8d-before-canonical_pricing_facade-v3.py
docs/checkpoints/fase-8d-before-canonical_pricing_facade-v4.py
docs/checkpoints/fase-8d-before-canonical_pricing_facade-v5.py
docs/checkpoints/fase-8d-before-canonical_pricing_facade.py
docs/checkpoints/fase-8d-before-rtd-db-path-fix.py
docs/checkpoints/fase-8d-final-summary.txt
docs/checkpoints/fase-8d-grep-fluxo-preco-rtd.txt
docs/checkpoints/fase-8d-patch-integracao-rtd-option-quotes.diff.txt
docs/checkpoints/fase-8d-uso-repository-rtd.txt
docs/checkpoints/fase-8e-auditoria-assinaturas-rtd-facade.txt
docs/checkpoints/fase-8e-auditoria-testes-rtd-facade.txt
docs/checkpoints/fase-8e-before-auditoria-rota-mestre-2.md
docs/checkpoints/fase-8f-conclusao-cobertura-rtd-price-resolution.txt
docs/checkpoints/fase-8f-inicio-auditoria-rtd-facade-flow.txt
```

## Rotas Mestre identificadas

```text
docs/AUDITORIA_ROTA_MESTRE_2.md
docs/AUDITORIA_ROTA_MESTRE_3.md
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md
docs/ROTA_MESTRE_3_RECONCILIACAO_POS_BACKUP.md
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md
docs/checkpoints/fase-8e-before-auditoria-rota-mestre-2.md
docs/validacoes/fechamento-rota-mestre-2.md
docs/validacoes/fechamento-rota-mestre-v1.md
```

## Documentos com referências à ponte RTD

```text
docs/AUDITORIA_ROTA_MESTRE_2.md:48:- docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md
docs/AUDITORIA_ROTA_MESTRE_2.md:53:- docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md
docs/AUDITORIA_ROTA_MESTRE_2.md:64:- docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md
docs/AUDITORIA_ROTA_MESTRE_2.md:104:test -f docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md
docs/AUDITORIA_ROTA_MESTRE_2.md:106:grep -n "INICIO ROTA_MESTRE_2" docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md
docs/AUDITORIA_ROTA_MESTRE_2.md:108:git diff -- docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md docs/AUDITORIA_ROTA_MESTRE_2.md
docs/AUDITORIA_ROTA_MESTRE_2.md:112:## Fase 1 — Mapeamento automatizado de RTD, Excel, Bridge, Serviços e UI
docs/AUDITORIA_ROTA_MESTRE_2.md:120:Executar mapeamento amplo de referências relacionadas a RTD, Excel, bridge, opções, persistência, serviços, cálculo e UI.
docs/AUDITORIA_ROTA_MESTRE_2.md:140:grep -n "Mapeamento automação opções RTD" docs/mapeamento_automacao_opcoes_rtd.md
docs/AUDITORIA_ROTA_MESTRE_2.md:174:- `dados/RTD_LINKS.csv`
docs/AUDITORIA_ROTA_MESTRE_2.md:230:- `dados/RTD_LINKS.csv`
docs/AUDITORIA_ROTA_MESTRE_2.md:257:## Fase 2 — Auditoria do contrato RTD/Excel e arquivos de entrada
docs/AUDITORIA_ROTA_MESTRE_2.md:265:Auditar o contrato entre RTD, Excel e arquivos locais de entrada, sem alteração funcional.
docs/AUDITORIA_ROTA_MESTRE_2.md:273:- `dados/RTD_LINKS.csv`
docs/AUDITORIA_ROTA_MESTRE_2.md:278:- `LISTA_RTD.xlsm`
docs/AUDITORIA_ROTA_MESTRE_2.md:299:## Fase 2 — Encerramento com mapa do contrato RTD/Excel
docs/AUDITORIA_ROTA_MESTRE_2.md:317:   - `dados/RTD_LINKS.csv`
docs/AUDITORIA_ROTA_MESTRE_2.md:327:- `dados/RTD_LINKS.csv`
docs/AUDITORIA_ROTA_MESTRE_2.md:339:- diferença de nomes de colunas entre contratos RTD e bridge
docs/AUDITORIA_ROTA_MESTRE_2.md:363:A próxima fase deve auditar a persistência de cotações RTD/opções, com foco em:
docs/AUDITORIA_ROTA_MESTRE_2.md:432:## Fase 8E — Cobertura regressiva da resolução de db path RTD no CanonicalPricingFacade
docs/AUDITORIA_ROTA_MESTRE_2.md:436:Adicionar cobertura automatizada para garantir que o `CanonicalPricingFacade` resolva corretamente o banco efetivo da tabela `rtd_option_quotes`, preservando a separação entre banco principal de execução/cálculo e banco operacional onde residem as cotações RTD de opções.
docs/AUDITORIA_ROTA_MESTRE_2.md:463:- Importadores RTD
docs/AUDITORIA_ROTA_MESTRE_2.md:540:- alterar importadores RTD;
docs/AUDITORIA_ROTA_MESTRE_2.md:596:## Fase 10B — Persistência da rastreabilidade da origem do preço RTD
docs/AUDITORIA_ROTA_MESTRE_2.md:645:A rastreabilidade da origem do preço RTD agora está coberta também na camada de persistência de execuções de pricing.
docs/AUDITORIA_ROTA_MESTRE_2.md:659:## Fase 10C — Validação da execução com preço RTD rastreável
docs/AUDITORIA_ROTA_MESTRE_2.md:663:Validar que o preço efetivo oriundo de `rtd_option_quotes` é aplicado ao payload canônico de pricing e que os metadados de rastreabilidade da cotação RTD permanecem disponíveis na execução.
docs/AUDITORIA_ROTA_MESTRE_2.md:667:- `_resolve_effective_leg_price` passou a preservar metadados de rastreabilidade da cotação RTD.
docs/AUDITORIA_ROTA_MESTRE_2.md:669:- O payload canônico de pricing passou a refletir o preço RTD efetivo e sua origem.
docs/AUDITORIA_ROTA_MESTRE_2.md:701:A execução de pricing agora preserva a rastreabilidade da cotação RTD usada para resolver o preço efetivo da leg.
docs/AUDITORIA_ROTA_MESTRE_2.md:715:## Fase 10D — Endurecimento da rastreabilidade do preço RTD
docs/AUDITORIA_ROTA_MESTRE_2.md:721:Endurecer a rastreabilidade do preço efetivo de opção resolvido a partir de `rtd_option_quotes`, garantindo que o payload canônico de pricing informe não apenas que o preço veio do RTD, mas também qual campo da cotação foi usado e qual registro RTD originou o preço.
docs/AUDITORIA_ROTA_MESTRE_2.md:725:Nesta fase, o RTD foi ativado com Excel como ponte operacional, alimentando os arquivos de banco de dados em tempo real. A validação técnica desta fase focou em transformar essa disponibilidade operacional em contrato auditável no backend.
docs/AUDITORIA_ROTA_MESTRE_2.md:729:- Criada a função `_pick_rtd_option_price_with_trace`, que retorna o preço RTD efetivo e o campo/critério usado.
docs/AUDITORIA_ROTA_MESTRE_2.md:732:- O payload canônico passou a carregar os campos adicionais de rastreabilidade RTD nas legs.
docs/AUDITORIA_ROTA_MESTRE_2.md:734:  - preservar preço manual explícito sem consultar RTD;
docs/AUDITORIA_ROTA_MESTRE_2.md:735:  - usar RTD quando a leg não é manual;
docs/AUDITORIA_ROTA_MESTRE_2.md:736:  - registrar campo usado da cotação RTD;
docs/AUDITORIA_ROTA_MESTRE_2.md:737:  - registrar código da opção e ativo-base da cotação RTD;
docs/AUDITORIA_ROTA_MESTRE_2.md:738:  - cair para snapshot quando a cotação RTD existe, mas não possui preço utilizável;
docs/AUDITORIA_ROTA_MESTRE_2.md:739:  - impedir vazamento de metadados RTD em legs manuais.
docs/AUDITORIA_ROTA_MESTRE_2.md:741:### Campos de rastreabilidade RTD consolidados
docs/AUDITORIA_ROTA_MESTRE_2.md:750:rtd_price_source = source da cotação RTD
docs/AUDITORIA_ROTA_MESTRE_2.md:785:- Legs manuais preservaram `price_source = manual` e não receberam metadados RTD.
docs/AUDITORIA_ROTA_MESTRE_2.md:791:A resolução de preço RTD agora é auditável em nível de campo utilizado e registro de cotação, reduzindo ambiguidade entre preço manual, preço de snapshot e preço vindo de `rtd_option_quotes`.
docs/AUDITORIA_ROTA_MESTRE_2.md:803:- Validar em ambiente operacional real com RTD/Excel ativo que legs reais carregam os campos:
docs/AUDITORIA_ROTA_MESTRE_2.md:811:## Fase 10E — Validação operacional da rastreabilidade RTD persistida
docs/AUDITORIA_ROTA_MESTRE_2.md:817:Validar que a rastreabilidade completa do preço RTD, já consolidada na Fase 10D no payload canônico de pricing, também é preservada nas camadas de persistência, consulta e snapshot do sistema.
docs/AUDITORIA_ROTA_MESTRE_2.md:819:Esta fase garante que os metadados RTD não se perdem após a execução de pricing ser salva e posteriormente recuperada.
docs/AUDITORIA_ROTA_MESTRE_2.md:823:A Fase 10D consolidou a exposição dos campos de rastreabilidade RTD no payload de pricing.
docs/AUDITORIA_ROTA_MESTRE_2.md:894:- Uma leg com `price_source = rtd_option_quotes` foi persistida com metadados RTD completos.
docs/AUDITORIA_ROTA_MESTRE_2.md:895:- A leitura por `get_execution` preservou todos os campos de rastreabilidade RTD.
docs/AUDITORIA_ROTA_MESTRE_2.md:896:- A leitura por `list_executions` preservou todos os campos de rastreabilidade RTD.
docs/AUDITORIA_ROTA_MESTRE_2.md:897:- O snapshot operacional recebeu a leg com os mesmos campos RTD.
docs/AUDITORIA_ROTA_MESTRE_2.md:898:- O `operation_state_json` preservou o `pricing_payload` com a rastreabilidade RTD completa.
docs/AUDITORIA_ROTA_MESTRE_2.md:905:A rastreabilidade do preço RTD agora é considerada preservada desde a resolução do preço no payload canônico até a persistência da execução, recuperação posterior e geração de snapshot do sistema.
docs/AUDITORIA_ROTA_MESTRE_2.md:915:2133966 test: valida rastreabilidade RTD persistida na fase 10E
docs/AUDITORIA_ROTA_MESTRE_2.md:918:## Fase 10F — Validação operacional fim-a-fim da rastreabilidade RTD/Excel
docs/AUDITORIA_ROTA_MESTRE_2.md:924:Validar, em cenário operacional mais próximo do real, que uma cotação RTD alimentada via Excel chega ao backend, é usada na resolução do preço da opção, entra no payload canônico de pricing e permanece rastreável após persistência.
docs/AUDITORIA_ROTA_MESTRE_2.md:928:As Fases 10C, 10D e 10E consolidaram a rastreabilidade do preço RTD em três camadas:
docs/AUDITORIA_ROTA_MESTRE_2.md:931:- exposição dos metadados RTD usados na resolução;
docs/AUDITORIA_ROTA_MESTRE_2.md:941:Excel / RTD
docs/AUDITORIA_ROTA_MESTRE_2.md:975:- Confirmar qual banco local contém `rtd_option_quotes` alimentado pelo Excel/RTD.
docs/AUDITORIA_ROTA_MESTRE_2.md:976:- Executar consulta de inspeção sobre cotações RTD disponíveis.
docs/AUDITORIA_ROTA_MESTRE_2.md:977:- Executar pricing usando opção com cotação RTD disponível.
docs/AUDITORIA_ROTA_MESTRE_2.md:987:## Fase 11 — Testes integrados RTD ponta a ponta
docs/AUDITORIA_ROTA_MESTRE_2.md:1001:RTD_LINKS.csv -> importação -> rtd_option_quotes -> CanonicalPricingFacade -> pricing_payload -> pricing_executions -> system snapshot/query
docs/AUDITORIA_ROTA_MESTRE_2.md:1034:- Criar CSV temporário simulando `RTD_LINKS.csv`.
docs/AUDITORIA_ROTA_MESTRE_2.md:1105:O teste usa banco temporário em `tmp_path`, CSV temporário simulando `RTD_LINKS.csv` e não acessa banco real nem arquivos operacionais em `dados/`.
docs/AUDITORIA_ROTA_MESTRE_2.md:1109:`RTD_LINKS.csv -> import_csv_to_db -> rtd_option_quotes -> CanonicalPricingFacade.execute_pricing -> pricing_payload -> pricing_executions -> structure_snapshots/system snapshot query`
docs/AUDITORIA_ROTA_MESTRE_2.md:1114:- Normalização de uma opção RTD.
docs/AUDITORIA_ROTA_MESTRE_2.md:1118:- Substituição do preço original do snapshot operacional pelo preço RTD importado.
docs/AUDITORIA_ROTA_MESTRE_2.md:1120:- Preservação de metadados de rastreabilidade RTD no `pricing_payload`.
docs/AUDITORIA_ROTA_MESTRE_2.md:1149:O fluxo RTD ponta a ponta está coberto por teste integrado isolado, auditável e sem dependência de banco real.
docs/AUDITORIA_ROTA_MESTRE_3.md:22:10. O Excel permanece apenas como gateway RTD.
docs/AUDITORIA_ROTA_MESTRE_3.md:72:D planilha RTD legada abolida
docs/AUDITORIA_ROTA_MESTRE_3.md:92:O dry-run com LISTA_RTD.xlsx falhou porque a aba disponível é diferente das esperadas pelos scripts:
docs/AUDITORIA_ROTA_MESTRE_3.md:95:Tentadas: RTD_OPTION_QUOTES, RTD_PROBE_OPTIONS
docs/AUDITORIA_ROTA_MESTRE_3.md:96:Disponível: RTD-BTG LISTA
docs/AUDITORIA_ROTA_MESTRE_3.md:109:- Classificar ponte RTD atual e planilha RTD legada abolida.
docs/AUDITORIA_ROTA_MESTRE_3.md:146:git ls-files --stage -- arquivo RTD legado
docs/AUDITORIA_ROTA_MESTRE_3.md:147:git cat-file -s HEAD:arquivo RTD legado
docs/AUDITORIA_ROTA_MESTRE_3.md:148:git log --oneline -10 -- arquivo RTD legado
docs/AUDITORIA_ROTA_MESTRE_3.md:157:planilha RTD legada: removida do working tree
docs/AUDITORIA_ROTA_MESTRE_3.md:161:O arquivo anteriormente usado como ponte RTD foi abolido do sistema.
docs/AUDITORIA_ROTA_MESTRE_3.md:163:A ponte RTD atual passa a ser:
docs/AUDITORIA_ROTA_MESTRE_3.md:166:LISTA_RTD.xlsm
docs/AUDITORIA_ROTA_MESTRE_3.md:169:A remoção da planilha RTD legada não deve ser revertida.
docs/AUDITORIA_ROTA_MESTRE_3.md:175:Foi executada substituição em documentos Markdown para consolidar o nome atual da ponte RTD:
docs/AUDITORIA_ROTA_MESTRE_3.md:178:LISTA_RTD.xlsm
docs/AUDITORIA_ROTA_MESTRE_3.md:224:440c6d5 docs: substitui referencia da planilha RTD legada
docs/AUDITORIA_ROTA_MESTRE_3.md:239:A planilha `LISTA_RTD.xlsm` foi preservada como ponte RTD oficial e testada.
docs/AUDITORIA_ROTA_MESTRE_3.md:241:A planilha RTD legada abolida foi removida do versionamento. A entrada `LISTA_RTD.xlsx` deixou de ser tratada como ponte RTD oficial.
docs/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:168:### Pernas de mercado, robô ou RTD legado
docs/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:233:### Cotações RTD de opções
docs/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:250:CSV exportado da aba RTD_LINKS
docs/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:287:O sistema possui repositórios de mercado, mas ainda mistura fonte RTD, tabelas legadas e provider interno temporário.
docs/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:476:LISTA_RTD.xlsm
docs/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:498:- vínculo com RTD: ainda indireto por alias/tabelas rtd_analise_robo_legs e manual_analise_robo_legs
docs/FASE_3_CLASSIFICACAO_FONTES_DADOS.md:52:LISTA_RTD.xlsm
docs/FASE_3_CLASSIFICACAO_FONTES_DADOS.md:53:CSV exportado da aba RTD_LINKS
docs/FASE_3_CLASSIFICACAO_FONTES_DADOS.md:54:cotações RTD de opções
docs/FASE_3_CLASSIFICACAO_FONTES_DADOS.md:70:Podem mudar de formato, depender de Excel, RTD, exportação manual ou captura externa.
docs/FASE_3_CLASSIFICACAO_FONTES_DADOS.md:286:| `LISTA_RTD.xlsm` | entrada bruta/configuração | separar dados de mercado, operação e parâmetros |
docs/FASE_3_CLASSIFICACAO_FONTES_DADOS.md:333:Cotações RTD e exportações da aba RTD_LINKS são entrada bruta.
docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:89:repositories/market_snapshot_repository.py:5:Le legs RTD (rtd_analise_robo_legs) e manuais (manual_analise_robo_legs),
docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:124:domain/calculation_request.py:207:    O orquestrador monta este objeto a partir do DB e do bridge/RTD,
docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:133:ATT/checks/check_api_routes.py:13:    ROOT_DIR / "LISTA_RTD.xlsm",
docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:135:ATT/checks/check_api_routes.py:27:        "Nenhum workbook principal encontrado: LISTA_RTD.xlsm/xlsx"
docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:145:ATT/checks/check_end_to_end.py:10:    ROOT_DIR / "LISTA_RTD.xlsm",
docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:147:ATT/checks/check_structures.py:10:    ROOT_DIR / "LISTA_RTD.xlsm",
docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:149:UI/main_window.py:508:* Excel RTD  CSV Bridge
docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:203:- Os arquivos em `ATT/checks/` fazem validações locais envolvendo workbook Excel, `win32com` ou presença de `LISTA_RTD.xlsm/xlsx`.
docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:277:Esses arquivos não leem Excel nem CSV diretamente, mas consomem tabelas que são alimentadas por dados vindos do bridge/RTD ou de estruturas manuais equivalentes.
docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:314:- `UI/main_window.py` apenas menciona visualmente o fluxo `Excel RTD CSV Bridge`.
docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:378:#### Dependência indireta por tabelas RTD/manuais
docs/FASE_5_ISOLAMENTO_BRIDGE_EXCEL_ADAPTADOR_LEGADO.md:121:É atualmente o principal acoplamento entre Excel/RTD/bridge e o banco dados/app.db.
docs/FASE_5_ISOLAMENTO_BRIDGE_EXCEL_ADAPTADOR_LEGADO.md:126:### 3.1 Tabelas staging/RTD vindas do bridge
docs/FASE_5_ISOLAMENTO_BRIDGE_EXCEL_ADAPTADOR_LEGADO.md:230:- Aplicar precedência entre dados manuais e dados RTD;
docs/FASE_5_ISOLAMENTO_BRIDGE_EXCEL_ADAPTADOR_LEGADO.md:367:### Consumo das tabelas RTD e manuais
docs/FASE_6_CAMADA_CANONICA_LEITURA.md:97:- A tabela `rtd_option_quotes` também deve ser tratada como tabela operacional/staging de cotações RTD, acessada via repository.
docs/FASE_6_CAMADA_CANONICA_LEITURA.md:168:- `services/robo_legs_status_service.py` usa nomes como `rtd_latest`, refletindo status da origem RTD.
docs/FASE_6_CAMADA_CANONICA_LEITURA.md:255:- A tabela `rtd_option_quotes` também deve ser tratada como tabela operacional/staging de cotações RTD, acessada via repository.
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:14:	- Fase 5 – Definição do Contrato RTD		      - (FINALIZADO E TESTADO)
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:15:	- Fase 6 – Consolidação da Camada BRIDGE RTD	      - (FINALIZADO E TESTADO)
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:16:	- Fase 7 – Ingestão Bruta do RTD			      - (FINALIZADO E TESTADO)
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:34:	- Fase 1 — Mapeamento amplo de RTD, Excel, Bridge, Serviços e UI
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:35:- Fase 2 — Auditoria do contrato dados/RTD_LINKS.csv
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:39:- Fase 6 — Importador somente-leitura do RTD_LINKS
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:64:O sistema tem como objetivo ser uma plataforma local de controle, análise e acompanhamento de operações com ações e opções, utilizando o Excel apenas como ponte de captura de dados RTD do BTG, e não como fonte da verdade operacional.
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:67:1.	Excel / RTD
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:68:•	Usado somente para capturar dados brutos de mercado via RTD.
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:86:•	capturar cotações brutas de ativos e opções via RTD;
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:101:1.	O BTG envia dados de mercado ao Excel via RTD.
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:103:3.	O sistema importa os dados RTD, valida e grava no banco.
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:109:9.	O Excel deixa de ser dependência operacional e passa a atuar somente como gateway RTD.
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:126:O Excel deixa de ser fonte operacional e passa a ser apenas gateway RTD.
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:131:3.	Formalizar contrato RTD
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:146:•	Excel é apenas ponte RTD.
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:170:•	LISTA_RTD.xlsm
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:204:•	RTD vindo do BTG
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:205:•	LISTA RTD
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:247:Fase 5 — Definição do Contrato RTD
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:251:A LISTA RTD passa a ser o modelo de referência da conexão BTG.
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:284:Contrato de campos definido entre Excel/RTD e sistema.
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:286:Fase 6 — Consolidação da Camada Bridge RTD
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:290:Transportar dados RTD sem calcular regra de negócio.
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:292:•	snapshot bruto RTD;
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:305:Fase 7 — Ingestão Bruta RTD
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:307:Importar dados brutos RTD para o banco.
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:324:RTD pode ser importado várias vezes sem duplicar nem corromper dados.
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:335:•	snapshots RTD;
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:354:4.	Sistema vincula pernas aos tickers RTD.
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:475:1.	RTD atualiza.
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:516:9.	Contrato RTD
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:517:10.	Bridge RTD
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:518:11.	Ingestão bruta RTD
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:643:dados/RTD_LINKS.csv
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:756:•	Cotações RTD de opções.
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:876:•	alterar UI antes de fechar o contrato RTD
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:906:Consolidar a ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md como documento norteador atualizado.
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:908:•	Excel é apenas ponte RTD.
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:936:- O arquivo dados/RTD_LINKS.csv é tratado como dado local operacional. O contrato versionado deve ser documentado em docs/, e não depender do versionamento direto do CSV real.
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:938:- RTD_LINKS.csv deve ser auditado inicialmente como catálogo/contrato de conexão RTD, não como fonte definitiva de snapshots de mercado, até que seu schema real confirme essa função.
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:940:Fase 1 — Mapeamento amplo de RTD, Excel, Bridge, Serviços e UI
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:946:•	identificar todos os arquivos que mencionam RTD, Excel, bridge, opções, persistência, serviços e UI
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:956:Fase 2 — Auditoria do contrato dados/RTD_LINKS.csv
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:969:•	presença de fórmulas RTD
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:974:•	validar presença de links ou fórmulas RTD
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:978:•	relatório do contrato RTD
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:984:•	saber exatamente quais campos existem no RTD_LINKS.csv
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:1015:•	pontos de entrada possíveis para cotações RTD
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:1047:Fase 6 — Importador somente-leitura do RTD_LINKS
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:1049:Criar importador inicial que leia dados/RTD_LINKS.csv, normalize campos e valide dados, sem ainda alterar UI ou cálculo.
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:1083:Permitir que cálculo use dados RTD persistidos como fonte de mercado.
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:1085:•	teste de cálculo usando snapshot RTD
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:1107:RTD_LINKS.csv→ importação→ persistência→ snapshot→ cálculo→ UI
docs/ROTA_MESTRE_3_RECONCILIACAO_POS_BACKUP.md:35:10. O Excel permanece apenas como gateway RTD.
docs/ROTA_MESTRE_3_RECONCILIACAO_POS_BACKUP.md:47:Classificar LISTA_RTD.xlsm e _usage_audit/ antes de qualquer limpeza.
docs/ROTA_MESTRE_3_RECONCILIACAO_POS_BACKUP.md:61:### Fase 5 — Reconciliação RTD/Excel
docs/ROTA_MESTRE_3_RECONCILIACAO_POS_BACKUP.md:77:## Nota de supersessão — LISTA_RTD.xlsx
docs/ROTA_MESTRE_3_RECONCILIACAO_POS_BACKUP.md:79:A partir da reconciliação registrada em `docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md` e `docs/checkpoints/fase-2-1-classificacao-referencias-lista-rtd.md`, a ponte RTD operacional oficial é `LISTA_RTD.xlsm`.
docs/ROTA_MESTRE_3_RECONCILIACAO_POS_BACKUP.md:81:Referências anteriores a `LISTA_RTD.xlsx` devem ser interpretadas como histórico/legado, salvo evidência funcional ativa em sentido contrário.
docs/baseline_v1.md:122:Transformar o Excel (com RTD) em fonte de dados, e o SQLite em sistema de verdade (histórico + consultas).
docs/baseline_v1.md:126:1) DataSource (Excel/RTD)
docs/baseline_v1.md:130:*	ExcelRTDSnapshotter
docs/baseline_v1.md:134:Força recálculo (ajuda RTD atualizar).
docs/baseline_v1.md:185:Se Excel travar/RTD falhar, reinicia a instância COM e segue.
docs/baseline_v1.md:222:2.	abre Excel  datasource/ExcelRTDSnapshotter
docs/baseline_v1.md:386:2.	Excel RTD  snapshot por aba
docs/baseline_v1.md:584:*	Tratamento de None, strings e erros RTD
docs/baseline_v1a.md:5:*	Excel: permanece como RTD bridge + exportador CSV (não mais COM direto)
docs/baseline_v1a.md:9:Excel RTD  CSV export  Python ingest  app.db (raw)  derivadores  derived.db
docs/baseline_v1a.md:16:*	Excel/RTD: ativo, mas apenas como bridge/exportador
docs/baseline_v1a.md:25:1.1 Excel/RTD Layer (bridge only)
docs/baseline_v1a.md:26:Responsabilidade: captura RTD + exportação CSV
docs/decisions/2026-06-17-supersessao-lista-rtd-xlsx.md:1:# Decisão — Supersessão de LISTA_RTD.xlsx por LISTA_RTD.xlsm
docs/decisions/2026-06-17-supersessao-lista-rtd-xlsx.md:7:Durante a reconciliação da ponte RTD, foram encontradas referências remanescentes a `LISTA_RTD.xlsx` em documentos históricos, checkpoints, validações antigas e no mapeamento documental `docs/mapeamento_automacao_opcoes_rtd.json`.
docs/decisions/2026-06-17-supersessao-lista-rtd-xlsx.md:9:Também foi confirmado que os scripts funcionais atuais usam `LISTA_RTD.xlsm` como workbook padrão:
docs/decisions/2026-06-17-supersessao-lista-rtd-xlsx.md:16:A ponte RTD operacional oficial passa a ser, de forma consolidada:
docs/decisions/2026-06-17-supersessao-lista-rtd-xlsx.md:18:`LISTA_RTD.xlsm`
docs/decisions/2026-06-17-supersessao-lista-rtd-xlsx.md:20:A planilha `LISTA_RTD.xlsx` fica classificada como referência legada/histórica e não deve ser usada como ponte operacional atual.
docs/decisions/2026-06-17-supersessao-lista-rtd-xlsx.md:24:Referências antigas a `LISTA_RTD.xlsx` em documentos, checkpoints, auditorias ou mapeamentos anteriores devem ser lidas como histórico do processo, salvo se uma nova evidência funcional ativa demonstrar consumo real em código de produção.
docs/decisions/2026-06-17-supersessao-lista-rtd-xlsx.md:29:- Não reintroduzir `LISTA_RTD.xlsx` como dependência operacional.
docs/decisions/2026-06-17-supersessao-lista-rtd-xlsx.md:30:- Manter `LISTA_RTD.xlsx` protegido no `.gitignore`.
docs/decisions/2026-06-17-supersessao-lista-rtd-xlsx.md:31:- Manter `LISTA_RTD.xlsm` versionável e tratado como ponte RTD oficial.
docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:49:| Cotações RTD | A preencher | A preencher | A preencher |
docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:73:## Decisão sobre fontes legadas e LISTA_RTD.xlsx
docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:82:- `LISTA_RTD.xlsx` passa a ser considerada candidata a fonte/gateway para o universo bruto RTD.
docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:84:- A integração RTD deve ser redesenhada para consumir uma camada bruta padronizada, sem depender das abas antigas como fonte de cadastro de operação.
docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:88:O fluxo novo não deve reconstruir o sistema em torno dos dados obsoletos. A Fase 2 deve mapear o legado existente e preparar a transição para um modelo onde a `LISTA_RTD.xlsx` alimenta dados RTD brutos, enquanto as estruturas operacionais nascem e vivem no banco do sistema.
docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:97:- `LISTA RTD`
docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:98:- `LISTA_RTD`
docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:113:- `db/import_excel.py` não consome `LISTA_RTD.xlsx`.
docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:128:- criar posteriormente um gateway específico para `LISTA_RTD.xlsx`;
docs/fase_2_auditoria_contrato_rtd_excel.md:1:# Fase 2 — Auditoria do contrato RTD/Excel e arquivos de entrada
docs/fase_2_auditoria_contrato_rtd_excel.md:9:Auditar, sem alteração funcional, o contrato entre RTD, Excel e arquivos locais usados como entrada no fluxo de opções.
docs/fase_2_auditoria_contrato_rtd_excel.md:15:- `dados/RTD_LINKS.csv`
docs/fase_2_auditoria_contrato_rtd_excel.md:20:- `LISTA_RTD.xlsm`
docs/fase_2_auditoria_contrato_rtd_excel.md:36:1. Qual é o papel de `dados/RTD_LINKS.csv`?
docs/fase_2_diagnostico_csvs_rtd_excel.json:3:    "path": "dados/RTD_LINKS.csv",
docs/fase_2_diagnostico_csvs_rtd_excel.md:1:# Diagnóstico CSVs RTD/Excel — Fase 2
docs/fase_2_diagnostico_csvs_rtd_excel.md:7:## `dados/RTD_LINKS.csv`
docs/fase_2_mapa_contrato_rtd_excel.md:1:# Mapa do contrato RTD/Excel — Fase 2
docs/fase_2_mapa_contrato_rtd_excel.md:13:Esta fase auditou, sem alteração funcional, arquivos locais relacionados ao contrato entre RTD, Excel e bridge.
docs/fase_2_mapa_contrato_rtd_excel.md:19:### `dados/RTD_LINKS.csv`
docs/fase_2_mapa_contrato_rtd_excel.md:22:- Classe: `fonte local RTD em formato atributo/valor`
docs/fase_2_mapa_contrato_rtd_excel.md:23:- Papel provável: Contrato simples para atributos de opções vindos de RTD/Excel.
docs/fase_2_mapa_contrato_rtd_excel.md:151:- `dados/RTD_LINKS.csv`
docs/fase_2_mapa_contrato_rtd_excel.md:221:### 1. Qual é o papel de `dados/RTD_LINKS.csv`?
docs/fase_2_mapa_contrato_rtd_excel.md:223:É uma fonte local RTD em formato atributo/valor por opção, com colunas:
docs/fase_2_mapa_contrato_rtd_excel.md:235:- `dados/RTD_LINKS.csv`, para atributos RTD/opções
docs/fase_2_mapa_contrato_rtd_excel.md:252:- `ATIVO` em arquivos de pernas contra `codigo_opcao` em `RTD_LINKS.csv`
docs/fase_2_mapa_contrato_rtd_excel.md:267:- `dados/RTD_LINKS.csv`
docs/fase_2_mapa_contrato_rtd_excel.md:287:1. `dados/RTD_LINKS.csv`
docs/fase_2_mapa_contrato_rtd_excel.md:292:A próxima fase deve auditar a persistência de cotações RTD/opções sem alterar schema, ingestão ou cálculo.
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:3:  "tema": "Auditoria da persistencia de cotacoes RTD/opcoes",
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:870:            "text": "\"Auditar scripts/patch_73_rtd_option_quotes.py para entender schema/tabela de cotações RTD de opções.\""
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:942:            "text": "- A tabela `rtd_option_quotes` também deve ser tratada como tabela operacional/staging de cotações RTD, acessada via repository."
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:950:            "text": "- A tabela `rtd_option_quotes` também deve ser tratada como tabela operacional/staging de cotações RTD, acessada via repository."
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:1006:        "path": "docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md",
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:1062:            "text": "\"repositories/rtd_option_quotes_repository.py\": \"Prioritário para auditoria de persistência RTD.\","
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:1252:            "text": "- vínculo com RTD: ainda indireto por alias/tabelas rtd_analise_robo_legs e manual_analise_robo_legs"
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:1284:            "text": "repositories/market_snapshot_repository.py:5:Le legs RTD (rtd_analise_robo_legs) e manuais (manual_analise_robo_legs),"
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:1494:            "text": "Le legs RTD (rtd_analise_robo_legs) e manuais (manual_analise_robo_legs),"
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:1768:            "text": "- vínculo com RTD: ainda indireto por alias/tabelas rtd_analise_robo_legs e manual_analise_robo_legs"
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:1816:            "text": "repositories/market_snapshot_repository.py:5:Le legs RTD (rtd_analise_robo_legs) e manuais (manual_analise_robo_legs),"
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:2124:            "text": "Le legs RTD (rtd_analise_robo_legs) e manuais (manual_analise_robo_legs),"
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:2268:            "text": "- vínculo com RTD: ainda indireto por alias/tabelas rtd_analise_robo_legs e manual_analise_robo_legs"
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:2292:            "text": "repositories/market_snapshot_repository.py:5:Le legs RTD (rtd_analise_robo_legs) e manuais (manual_analise_robo_legs),"
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:2392:            "text": "Le legs RTD (rtd_analise_robo_legs) e manuais (manual_analise_robo_legs),"
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:2438:    "RTD_LINKS": [
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:2444:            "text": "\"RTD_LINKS\","
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:2448:            "text": "\"dados/RTD_LINKS.csv\","
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:2452:            "text": "if \"dados/RTD_LINKS.csv\" in existing_paths:"
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:2456:            "text": "\"Auditar dados/RTD_LINKS.csv como possível fonte fixa de links RTD antes de criar nova estrutura.\""
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:2460:            "text": "\"Verificar se a lista fixa de links RTD precisa ser criada, pois dados/RTD_LINKS.csv não foi encontrado.\""
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:2470:            "text": "- `dados/RTD_LINKS.csv`"
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:2474:            "text": "- `dados/RTD_LINKS.csv`"
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:2478:            "text": "- `dados/RTD_LINKS.csv`"
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:2482:            "text": "- `dados/RTD_LINKS.csv`"
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:2486:            "text": "- `dados/RTD_LINKS.csv`"
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:2496:            "text": "- `dados/RTD_LINKS.csv`"
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:2500:            "text": "1. Qual é o papel de `dados/RTD_LINKS.csv`?"
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:2510:            "text": "## `dados/RTD_LINKS.csv`"
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:2520:            "text": "CSV exportado da aba RTD_LINKS"
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:2530:            "text": "### `dados/RTD_LINKS.csv`"
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:2534:            "text": "- `dados/RTD_LINKS.csv`"
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:2538:            "text": "### 1. Qual é o papel de `dados/RTD_LINKS.csv`?"
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:2542:            "text": "- `dados/RTD_LINKS.csv`, para atributos RTD/opções"
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:2546:            "text": "- `ATIVO` em arquivos de pernas contra `codigo_opcao` em `RTD_LINKS.csv`"
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:2550:            "text": "- `dados/RTD_LINKS.csv`"
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:2554:            "text": "1. `dados/RTD_LINKS.csv`"
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:2564:            "text": "CSV exportado da aba RTD_LINKS"
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:2568:            "text": "Cotações RTD e exportações da aba RTD_LINKS são entrada bruta."
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:2578:            "text": "### `dados/RTD_LINKS.csv`"
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:2588:            "text": "### `dados/RTD_LINKS.csv`"
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:2594:        "path": "docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md",
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:2598:            "text": "- Fase 2 — Auditoria do contrato dados/RTD_LINKS.csv"
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:2602:            "text": "- Fase 6 — Importador somente-leitura do RTD_LINKS"
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:2606:            "text": "dados/RTD_LINKS.csv"
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:2610:            "text": "- O arquivo dados/RTD_LINKS.csv é tratado como dado local operacional. O contrato versionado deve ser documentado em docs/, e não depender do versionamento direto do CSV real."
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:2614:            "text": "- RTD_LINKS.csv deve ser auditado inicialmente como catálogo/contrato de conexão RTD, não como fonte definitiva de snapshots de mercado, até que seu schema real confirme essa função."
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:2618:            "text": "Fase 2 — Auditoria do contrato dados/RTD_LINKS.csv"
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:2622:            "text": "•\tsaber exatamente quais campos existem no RTD_LINKS.csv"
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:2626:            "text": "Fase 6 — Importador somente-leitura do RTD_LINKS"
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:2630:            "text": "Criar importador inicial que leia dados/RTD_LINKS.csv, normalize campos e valide dados, sem ainda alterar UI ou cálculo."
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:2634:            "text": "RTD_LINKS.csv→ importação→ persistência→ snapshot→ cálculo→ UI"
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:2644:            "text": "dados/RTD_LINKS.csv"
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:2654:            "text": "Essa tabela é alimentada pelo CSV exportado da aba RTD_LINKS"
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:2664:            "text": "\"dados/RTD_LINKS.csv\": \"Prioritário para auditoria do contrato RTD/Excel.\","
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:3004:            "text": "- vínculo com RTD: ainda indireto por alias/tabelas rtd_analise_robo_legs e manual_analise_robo_legs"
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:3102:            "text": "repositories/market_snapshot_repository.py:5:Le legs RTD (rtd_analise_robo_legs) e manuais (manual_analise_robo_legs),"
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:3344:        "path": "docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md",
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:3392:            "text": "Le legs RTD (rtd_analise_robo_legs) e manuais (manual_analise_robo_legs),"
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json:3670:        "path": "docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md",
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:1:# Diagnóstico da persistência RTD/opções — Fase 3
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:7:Esta etapa audita, sem alteração funcional, a persistência e leitura de cotações RTD/opções.
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:437:  - linha `353`: `"Auditar scripts/patch_73_rtd_option_quotes.py para entender schema/tabela de cotações RTD de opções."`
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:453:  - linha `97`: `- A tabela `rtd_option_quotes` também deve ser tratada como tabela operacional/staging de cotações RTD, acessada via repository.`
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:455:  - linha `255`: `- A tabela `rtd_option_quotes` também deve ser tratada como tabela operacional/staging de cotações RTD, acessada via repository.`
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:467:- `docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md` — `5` ocorrência(s)
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:480:  - linha `69`: `"repositories/rtd_option_quotes_repository.py": "Prioritário para auditoria de persistência RTD.",`
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:525:  - linha `498`: `- vínculo com RTD: ainda indireto por alias/tabelas rtd_analise_robo_legs e manual_analise_robo_legs`
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:532:  - linha `89`: `repositories/market_snapshot_repository.py:5:Le legs RTD (rtd_analise_robo_legs) e manuais (manual_analise_robo_legs),`
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:566:  - linha `5`: `Le legs RTD (rtd_analise_robo_legs) e manuais (manual_analise_robo_legs),`
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:628:  - linha `498`: `- vínculo com RTD: ainda indireto por alias/tabelas rtd_analise_robo_legs e manual_analise_robo_legs`
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:638:  - linha `89`: `repositories/market_snapshot_repository.py:5:Le legs RTD (rtd_analise_robo_legs) e manuais (manual_analise_robo_legs),`
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:682:  - linha `5`: `Le legs RTD (rtd_analise_robo_legs) e manuais (manual_analise_robo_legs),`
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:717:  - linha `498`: `- vínculo com RTD: ainda indireto por alias/tabelas rtd_analise_robo_legs e manual_analise_robo_legs`
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:722:  - linha `89`: `repositories/market_snapshot_repository.py:5:Le legs RTD (rtd_analise_robo_legs) e manuais (manual_analise_robo_legs),`
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:743:  - linha `5`: `Le legs RTD (rtd_analise_robo_legs) e manuais (manual_analise_robo_legs),`
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:754:### Termo `RTD_LINKS`
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:757:  - linha `55`: `"RTD_LINKS",`
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:758:  - linha `146`: `"dados/RTD_LINKS.csv",`
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:759:  - linha `327`: `if "dados/RTD_LINKS.csv" in existing_paths:`
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:760:  - linha `329`: `"Auditar dados/RTD_LINKS.csv como possível fonte fixa de links RTD antes de criar nova estrutura."`
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:761:  - linha `333`: `"Verificar se a lista fixa de links RTD precisa ser criada, pois dados/RTD_LINKS.csv não foi encontrado."`
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:763:  - linha `174`: `- `dados/RTD_LINKS.csv``
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:764:  - linha `230`: `- `dados/RTD_LINKS.csv``
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:765:  - linha `273`: `- `dados/RTD_LINKS.csv``
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:766:  - linha `317`: `- `dados/RTD_LINKS.csv``
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:767:  - linha `327`: `- `dados/RTD_LINKS.csv``
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:769:  - linha `15`: `- `dados/RTD_LINKS.csv``
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:770:  - linha `36`: `1. Qual é o papel de `dados/RTD_LINKS.csv`?`
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:772:  - linha `7`: `## `dados/RTD_LINKS.csv``
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:774:  - linha `250`: `CSV exportado da aba RTD_LINKS`
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:776:  - linha `19`: `### `dados/RTD_LINKS.csv``
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:777:  - linha `151`: `- `dados/RTD_LINKS.csv``
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:778:  - linha `221`: `### 1. Qual é o papel de `dados/RTD_LINKS.csv`?`
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:779:  - linha `235`: `- `dados/RTD_LINKS.csv`, para atributos RTD/opções`
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:780:  - linha `252`: `- `ATIVO` em arquivos de pernas contra `codigo_opcao` em `RTD_LINKS.csv``
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:781:  - linha `267`: `- `dados/RTD_LINKS.csv``
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:782:  - linha `287`: `1. `dados/RTD_LINKS.csv``
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:784:  - linha `53`: `CSV exportado da aba RTD_LINKS`
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:785:  - linha `333`: `Cotações RTD e exportações da aba RTD_LINKS são entrada bruta.`
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:787:  - linha `28`: `### `dados/RTD_LINKS.csv``
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:789:  - linha `700`: `### `dados/RTD_LINKS.csv``
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:790:- `docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md` — `10` ocorrência(s)
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:791:  - linha `35`: `- Fase 2 — Auditoria do contrato dados/RTD_LINKS.csv`
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:792:  - linha `39`: `- Fase 6 — Importador somente-leitura do RTD_LINKS`
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:793:  - linha `643`: `dados/RTD_LINKS.csv`
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:794:  - linha `936`: `- O arquivo dados/RTD_LINKS.csv é tratado como dado local operacional. O contrato versionado deve ser documentado em docs/, e não depender do versionamento direto do CSV real.`
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:795:  - linha `938`: `- RTD_LINKS.csv deve ser auditado inicialmente como catálogo/contrato de conexão RTD, não como fonte definitiva de snapshots de mercado, até que seu schema real confirme essa função.`
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:796:  - linha `956`: `Fase 2 — Auditoria do contrato dados/RTD_LINKS.csv`
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:797:  - linha `984`: `•	saber exatamente quais campos existem no RTD_LINKS.csv`
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:798:  - linha `1047`: `Fase 6 — Importador somente-leitura do RTD_LINKS`
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:800:  - linha `363`: `dados/RTD_LINKS.csv`
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:802:  - linha `14`: `Essa tabela é alimentada pelo CSV exportado da aba RTD_LINKS`
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:804:  - linha `75`: `"dados/RTD_LINKS.csv": "Prioritário para auditoria do contrato RTD/Excel.",`
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:899:  - linha `89`: `repositories/market_snapshot_repository.py:5:Le legs RTD (rtd_analise_robo_legs) e manuais (manual_analise_robo_legs),`
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:932:- `docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md` — `2` ocorrência(s)
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:942:  - linha `5`: `Le legs RTD (rtd_analise_robo_legs) e manuais (manual_analise_robo_legs),`
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:1005:- `docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md` — `2` ocorrência(s)
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:1231:2. `repositories/market_snapshot_repository.py` lê snapshots RTD e manuais a partir de tabelas normalizadas.
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:1233:4. `services/market_snapshot_provider.py` usa valores estáticos por ativo e não acessa RTD ou banco.
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:1234:5. Os arquivos inicialmente auditados não demonstram, por si só, o ponto de persistência/importação das cotações RTD.
docs/fase_3_diagnostico_persistencia_rtd_opcoes.md:1238:Identificar qual rotina cria, importa, atualiza ou sincroniza as tabelas RTD a partir de CSV/Excel/bridge.
docs/fase_8_banco_fonte_verdade_auditoria.md:14:- snapshots RTD;
docs/fase_8_banco_fonte_verdade_auditoria.md:148:### Tabelas RTD ou legado importado
docs/fase_8_banco_fonte_verdade_auditoria.md:173:- snapshots/importações RTD legadas
docs/fase_8_banco_fonte_verdade_auditoria.md:209:Enquanto structure_legs permanecer vazio, o sistema provavelmente ainda precisa recorrer a dados legados, RTD ou mapeamentos auxiliares para montar pernas operacionais.
docs/fase_8_banco_fonte_verdade_auditoria.md:273:Foi executada inspeção das tabelas centrais da Fase 8 para avaliar se as estruturas persistidas em `structures` possuem vínculo confiável com pernas vindas das tabelas RTD legadas.
docs/fase_8_banco_fonte_verdade_auditoria.md:392:- BOVA11 encontrou 4 pernas RTD
docs/fase_8_banco_fonte_verdade_auditoria.md:393:- EMBJ3 encontrou 4 pernas RTD
docs/fase_8_banco_fonte_verdade_auditoria.md:394:- PRIO3 encontrou 4 pernas RTD
docs/fase_8_banco_fonte_verdade_auditoria.md:395:- SBSP3 encontrou 4 pernas RTD
docs/fase_8_banco_fonte_verdade_auditoria.md:396:- SMAL11 encontrou 4 pernas RTD
docs/fases/fase-10g-guardrails-operacionais-preco-rtd.md:1:# Fase 10g — Guardrails Operacionais do Preço RTD
docs/fases/fase-10g-guardrails-operacionais-preco-rtd.md:7:Endurecer o fluxo operacional de precificação usando RTD para evitar uso silencioso de preços ausentes, inválidos ou inconsistentes.
docs/fases/fase-10g-guardrails-operacionais-preco-rtd.md:13:RTD Excel -> rtd_option_quotes -> CanonicalPricingFacade -> pricing_executions
docs/fases/fase-10g-guardrails-operacionais-preco-rtd.md:15:A fase 10g existe para garantir que falhas operacionais no uso do preço RTD sejam rastreáveis no pricing_payload e não sejam mascaradas como precificação válida.
docs/fases/fase-10g-guardrails-operacionais-preco-rtd.md:21:- quote RTD ausente;
docs/fases/fase-10g-guardrails-operacionais-preco-rtd.md:22:- preço RTD nulo;
docs/fases/fase-10g-guardrails-operacionais-preco-rtd.md:23:- preço RTD zero ou inválido;
docs/fases/fase-10g-guardrails-operacionais-preco-rtd.md:24:- ativo_base divergente entre estrutura e quote RTD;
docs/fases/fase-10g-guardrails-operacionais-preco-rtd.md:56:### RTD válido
docs/fases/fase-10g-guardrails-operacionais-preco-rtd.md:58:Quando a quote RTD existir e o preço for válido:
docs/fases/fase-10g-guardrails-operacionais-preco-rtd.md:66:### Quote RTD ausente
docs/fases/fase-10g-guardrails-operacionais-preco-rtd.md:68:Quando não existir quote RTD para o código da opção:
docs/fases/fase-10g-guardrails-operacionais-preco-rtd.md:73:- rtd_validation_message deve explicar que a quote RTD não foi encontrada.
docs/fases/fase-10g-guardrails-operacionais-preco-rtd.md:77:### Preço RTD inválido
docs/fases/fase-10g-guardrails-operacionais-preco-rtd.md:84:- rtd_validation_message deve explicar que o preço RTD está ausente ou inválido.
docs/fases/fase-10g-guardrails-operacionais-preco-rtd.md:95:Quando a quote RTD existir, mas o ativo_base da quote divergir do underlying_asset da estrutura:
docs/fases/fase-10g-guardrails-operacionais-preco-rtd.md:109:Se o fallback ocorrer porque o RTD falhou, o diagnóstico RTD deve continuar preservado na leg.
docs/fases/fase-10g-guardrails-operacionais-preco-rtd.md:115:- RTD válido continua funcionando;
docs/fases/fase-10g-guardrails-operacionais-preco-rtd.md:116:- quote RTD ausente é diagnosticada;
docs/fases/fase-10g-guardrails-operacionais-preco-rtd.md:118:- preço RTD inválido é diagnosticado;
docs/fases/fase-10g-guardrails-operacionais-preco-rtd.md:120:- fallback manual ou snapshot não apaga diagnóstico RTD;
docs/fases/fase-10g-guardrails-operacionais-preco-rtd.md:135:- falhas RTD forem diagnosticáveis no pricing_payload;
docs/lista_priorizada_automacao_opcoes_rtd.md:1:# Lista priorizada — automação opções RTD
docs/lista_priorizada_automacao_opcoes_rtd.md:16:- RTD/Excel
docs/lista_priorizada_automacao_opcoes_rtd.md:28:### `dados/RTD_LINKS.csv`
docs/lista_priorizada_automacao_opcoes_rtd.md:32:- Motivo: Contrato local RTD/Excel. Base para Fase 2.
docs/lista_priorizada_automacao_opcoes_rtd.md:40:- Motivo: Persistência de cotações RTD/opções. Base para Fase 3.
docs/lista_priorizada_automacao_opcoes_rtd.md:171:- arquivos derivados ou volumosos sem papel claro no fluxo RTD
docs/lista_priorizada_automacao_opcoes_rtd.md:179:1. Fase 2 deve auditar o contrato RTD/Excel e arquivos de entrada.
docs/lista_priorizada_automacao_opcoes_rtd.md:180:2. Fase 3 deve auditar persistência de cotações RTD/opções.
docs/mapeamento_automacao_opcoes_rtd.json:23:      "path": "docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md",
docs/mapeamento_automacao_opcoes_rtd.json:675:      "note": "Prioritário para auditoria de persistência RTD."
docs/mapeamento_automacao_opcoes_rtd.json:1373:      "path": "dados/RTD_LINKS.csv",
docs/mapeamento_automacao_opcoes_rtd.json:1384:      "note": "Prioritário para auditoria do contrato RTD/Excel."
docs/mapeamento_automacao_opcoes_rtd.json:2539:      "path": "LISTA_RTD.xlsx",
docs/mapeamento_automacao_opcoes_rtd.md:1:# Mapeamento automação opções RTD — ROTA_MESTRE_2 Fase 1
docs/mapeamento_automacao_opcoes_rtd.md:7:Mapeamento amplo de RTD, Excel, bridge, opções, persistência, serviços e UI.
docs/mapeamento_automacao_opcoes_rtd.md:28:### `docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md`
docs/mapeamento_automacao_opcoes_rtd.md:328:- Nota: Prioritário para auditoria de persistência RTD.
docs/mapeamento_automacao_opcoes_rtd.md:700:### `dados/RTD_LINKS.csv`
docs/mapeamento_automacao_opcoes_rtd.md:704:- Nota: Prioritário para auditoria do contrato RTD/Excel.
docs/mapeamento_automacao_opcoes_rtd.md:1254:- `LISTA_RTD.xlsx` — `outros` — score `6`
docs/mapeamento_automacao_opcoes_rtd.md:1255:- `LISTA_RTD.xlsm` — `outros` — score `6`
docs/validacoes/fase-10f-validacao-e2e-rtd-excel.md:1:# Fase 10f — Validação E2E RTD Excel
docs/validacoes/fase-10f-validacao-e2e-rtd-excel.md:10:RTD Excel -> rtd_option_quotes -> CanonicalPricingFacade -> pricing_executions
docs/validacoes/fase-10f-validacao-e2e-rtd-excel.md:33:alias_legacy_aba = E2E_RTD_PRIO3
docs/validacoes/fase-10f-validacao-e2e-rtd-excel.md:48:## Quotes RTD usadas
docs/validacoes/fase-10f-validacao-e2e-rtd-excel.md:104:Já o campo `rtd_price_source` reflete a origem interna registrada na própria quote RTD:
docs/validacoes/fase-10f-validacao-e2e-rtd-excel.md:147:E2E RTD Excel -> CanonicalPricingFacade -> pricing_executions: OK
docs/validacoes/fase-17-mapa-pastas-arquivos.md:126:LISTA_RTD.xlsx
docs/validacoes/fase-17-mapa-pastas-arquivos.md:127:LISTA_RTD.xlsm
docs/validacoes/fase-17-mapa-pastas-arquivos.md:144:- `LISTA_RTD.xlsm` está versionado.
docs/validacoes/fase-17-mapa-pastas-arquivos.md:145:- `LISTA_RTD.xlsx` está versionado.
docs/validacoes/fase-17-mapa-pastas-arquivos.md:156:| `LISTA_RTD.xlsm` | Sim | Versionado |
docs/validacoes/fase-17-mapa-pastas-arquivos.md:157:| `LISTA_RTD.xlsx` | Sim | Versionado |
docs/validacoes/fase-17-mapa-pastas-arquivos.md:262:A camada `repositories/` concentra acesso a dados de estruturas, eventos, pricing executions, snapshots, legs, status e RTD.
docs/validacoes/fase-17-mapa-pastas-arquivos.md:363:dados/RTD_LINKS.csv
docs/validacoes/fechamento-rota-mestre-2.md:1:# Fechamento da ROTA_MESTRE_2 — Automação de Opções via RTD
docs/validacoes/fechamento-rota-mestre-2.md:8:Registrar o fechamento do ciclo `ROTA_MESTRE_2`, dedicado à automação do fluxo de opções via RTD, incluindo:
docs/validacoes/fechamento-rota-mestre-2.md:11:- diagnóstico do contrato Excel/RTD;
docs/validacoes/fechamento-rota-mestre-2.md:13:- persistência de cotações RTD de opções;
docs/validacoes/fechamento-rota-mestre-2.md:18:- saneamento de versionamento das planilhas RTD.
docs/validacoes/fechamento-rota-mestre-2.md:34:Foram criados registros de auditoria, diagnóstico, checkpoints e validações relacionados ao fluxo RTD de opções, incluindo:
docs/validacoes/fechamento-rota-mestre-2.md:36:- `docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md`
docs/validacoes/fechamento-rota-mestre-2.md:42:### 2. Importação e pipeline RTD
docs/validacoes/fechamento-rota-mestre-2.md:44:Foram adicionados scripts para importação, auditoria, seed e execução de pipeline RTD de opções, incluindo:
docs/validacoes/fechamento-rota-mestre-2.md:55:Foram ajustadas camadas de banco, repositórios e serviços para suportar o fluxo RTD de opções e sua rastreabilidade, incluindo alterações em:
docs/validacoes/fechamento-rota-mestre-2.md:69:- cotação RTD persistida;
docs/validacoes/fechamento-rota-mestre-2.md:72:- guardrails para ausência, inconsistência ou invalidez da cotação RTD.
docs/validacoes/fechamento-rota-mestre-2.md:78:- importação de links RTD;
docs/validacoes/fechamento-rota-mestre-2.md:80:- execução do pipeline RTD;
docs/validacoes/fechamento-rota-mestre-2.md:81:- resolução do caminho correto do banco RTD;
docs/validacoes/fechamento-rota-mestre-2.md:82:- resolução de preço RTD;
docs/validacoes/fechamento-rota-mestre-2.md:92:Foi corrigido o tratamento das planilhas RTD:
docs/validacoes/fechamento-rota-mestre-2.md:94:- `LISTA_RTD.xlsm` foi removida do versionamento e protegida no `.gitignore`;
docs/validacoes/fechamento-rota-mestre-2.md:95:- `LISTA_RTD.xlsx` foi restaurada como arquivo versionado conforme referência de `origin/main`;
docs/validacoes/fechamento-rota-mestre-2.md:100:- `git diff --name-status origin/main..HEAD -- LISTA_RTD.xlsx LISTA_RTD.xlsm .gitignore`
docs/validacoes/fechamento-rota-mestre-2.md:107:- `9ea0240 chore: restaura planilha RTD versionada`
docs/validacoes/fechamento-rota-mestre-2.md:108:- `afa69cc chore: preserva planilha RTD fora do versionamento`
docs/validacoes/fechamento-rota-mestre-2.md:110:- `9009a40 test: adiciona fluxo integrado RTD ponta a ponta`
docs/validacoes/fechamento-rota-mestre-2.md:116:O ciclo entregou um fluxo RTD de opções documentado, testado e integrado ao pricing canônico, com rastreabilidade operacional e cobertura automatizada.
docs/validacoes/fechamento-rota-mestre-v1.md:49:Fase 5  - Definição do Contrato RTD
docs/validacoes/fechamento-rota-mestre-v1.md:50:Fase 6  - Consolidação da Camada BRIDGE RTD
docs/validacoes/fechamento-rota-mestre-v1.md:51:Fase 7  - Ingestão Bruta do RTD
```

## Artefatos documentais gerados ou auxiliares

```text
docs/fase_2_diagnostico_csvs_rtd_excel.json
docs/fase_3_diagnostico_persistencia_rtd_opcoes.json
docs/mapeamento_automacao_opcoes_rtd.json
```

## Classificação preliminar

| Arquivo/Grupo | Classe | Observação |
|---|---|---|
| `docs/ROTA_MESTRE_3_RECONCILIACAO_POS_BACKUP.md` | Documento vivo | Rota atual de reconciliação pós-backup |
| `docs/decisions/` | Decisões vivas | Fonte de interpretação atual |
| `docs/checkpoints/` | Histórico/auditoria | Não reescrever salvo correção explícita e documentada |
| `docs/mapeamento_automacao_opcoes_rtd.json` | Artefato documental gerado | Não confundir com contrato operacional |
| Documentos antigos da Rota Mestre 2 | Histórico orientativo | Podem conter referências legadas |

## Resultado

Inventário documental inicial registrado. Nenhuma alteração funcional realizada.

## Próxima ação recomendada

Classificar quais documentos vivos precisam receber nota de supersessão e quais devem permanecer históricos sem edição.
