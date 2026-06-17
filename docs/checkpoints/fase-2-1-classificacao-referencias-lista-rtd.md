# Fase 2.1 — Classificação das referências remanescentes LISTA_RTD

Data: 2026-06-17 09:33:49 -0300

Branch:

```text
fase-12-fechamento-ciclo
```

## Estado Git inicial

```text
## fase-12-fechamento-ciclo...origin/fase-12-fechamento-ciclo
?? docs/checkpoints/fase-2-1-classificacao-referencias-lista-rtd.md
```

## Objetivo

Classificar referências restantes a `LISTA_RTD.xlsx` e `LISTA_RTD.xlsm` sem alterar fluxo funcional.

## Regra vigente

- `LISTA_RTD.xlsm` é a ponte RTD operacional oficial.
- `LISTA_RTD.xlsx` é legado/obsoleto para operação atual.
- Referências antigas a `LISTA_RTD.xlsx` devem ser tratadas como históricas, salvo evidência de consumo funcional ativo.

## Referências a LISTA_RTD.xlsx

```text
.gitignore:12:LISTA_RTD.xlsx
docs/AUDITORIA_ROTA_MESTRE_3.md:92:O dry-run com LISTA_RTD.xlsx falhou porque a aba disponível é diferente das esperadas pelos scripts:
docs/AUDITORIA_ROTA_MESTRE_3.md:241:A planilha RTD legada abolida foi removida do versionamento. A entrada `LISTA_RTD.xlsx` deixou de ser tratada como ponte RTD oficial.
docs/checkpoints/ciclo-2-fase-7a-auditoria-rtd-opcoes.md:28:./LISTA_RTD.xlsx
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:13:Confirmar que a ponte RTD operacional oficial é `LISTA_RTD.xlsm`, identificar referências remanescentes a `LISTA_RTD.xlsx` e separar documentação histórica de dependências operacionais.
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:40:## Referências gerais a LISTA_RTD.xlsx ou LISTA_RTD.xlsm
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:43:.gitignore:12:LISTA_RTD.xlsx
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:45:docs/AUDITORIA_ROTA_MESTRE_3.md:92:O dry-run com LISTA_RTD.xlsx falhou porque a aba disponível é diferente das esperadas pelos scripts:
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:49:docs/AUDITORIA_ROTA_MESTRE_3.md:241:A planilha RTD legada abolida foi removida do versionamento. A entrada `LISTA_RTD.xlsx` deixou de ser tratada como ponte RTD oficial.
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:60:docs/checkpoints/ciclo-2-fase-7a-auditoria-rtd-opcoes.md:28:./LISTA_RTD.xlsx
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:94:docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:73:## Decisão sobre fontes legadas e LISTA_RTD.xlsx
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:95:docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:82:- `LISTA_RTD.xlsx` passa a ser considerada candidata a fonte/gateway para o universo bruto RTD.
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:96:docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:88:O fluxo novo não deve reconstruir o sistema em torno dos dados obsoletos. A Fase 2 deve mapear o legado existente e preparar a transição para um modelo onde a `LISTA_RTD.xlsx` alimenta dados RTD brutos, enquanto as estruturas operacionais nascem e vivem no banco do sistema.
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:97:docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:113:- `db/import_excel.py` não consome `LISTA_RTD.xlsx`.
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:98:docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:128:- criar posteriormente um gateway específico para `LISTA_RTD.xlsx`;
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:100:docs/mapeamento_automacao_opcoes_rtd.json:2539:      "path": "LISTA_RTD.xlsx",
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:101:docs/mapeamento_automacao_opcoes_rtd.md:1254:- `LISTA_RTD.xlsx` — `outros` — score `6`
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:103:docs/validacoes/fase-17-mapa-pastas-arquivos.md:126:LISTA_RTD.xlsx
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:106:docs/validacoes/fase-17-mapa-pastas-arquivos.md:145:- `LISTA_RTD.xlsx` está versionado.
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:108:docs/validacoes/fase-17-mapa-pastas-arquivos.md:157:| `LISTA_RTD.xlsx` | Sim | Versionado |
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:110:docs/validacoes/fechamento-rota-mestre-2.md:95:- `LISTA_RTD.xlsx` foi restaurada como arquivo versionado conforme referência de `origin/main`;
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:111:docs/validacoes/fechamento-rota-mestre-2.md:100:- `git diff --name-status origin/main..HEAD -- LISTA_RTD.xlsx LISTA_RTD.xlsm .gitignore`
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:130:docs/mapeamento_automacao_opcoes_rtd.json:2539:      "path": "LISTA_RTD.xlsx",
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:149:- `LISTA_RTD.xlsx` não deve ser tratada como ponte operacional atual.
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:150:- Referências a `LISTA_RTD.xlsx` em documentos antigos devem ser classificadas como históricas, salvo se indicarem dependência operacional ativa.
docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:73:## Decisão sobre fontes legadas e LISTA_RTD.xlsx
docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:82:- `LISTA_RTD.xlsx` passa a ser considerada candidata a fonte/gateway para o universo bruto RTD.
docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:88:O fluxo novo não deve reconstruir o sistema em torno dos dados obsoletos. A Fase 2 deve mapear o legado existente e preparar a transição para um modelo onde a `LISTA_RTD.xlsx` alimenta dados RTD brutos, enquanto as estruturas operacionais nascem e vivem no banco do sistema.
docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:113:- `db/import_excel.py` não consome `LISTA_RTD.xlsx`.
docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:128:- criar posteriormente um gateway específico para `LISTA_RTD.xlsx`;
docs/mapeamento_automacao_opcoes_rtd.json:2539:      "path": "LISTA_RTD.xlsx",
docs/mapeamento_automacao_opcoes_rtd.md:1254:- `LISTA_RTD.xlsx` — `outros` — score `6`
docs/validacoes/fase-17-mapa-pastas-arquivos.md:126:LISTA_RTD.xlsx
docs/validacoes/fase-17-mapa-pastas-arquivos.md:145:- `LISTA_RTD.xlsx` está versionado.
docs/validacoes/fase-17-mapa-pastas-arquivos.md:157:| `LISTA_RTD.xlsx` | Sim | Versionado |
docs/validacoes/fechamento-rota-mestre-2.md:95:- `LISTA_RTD.xlsx` foi restaurada como arquivo versionado conforme referência de `origin/main`;
docs/validacoes/fechamento-rota-mestre-2.md:100:- `git diff --name-status origin/main..HEAD -- LISTA_RTD.xlsx LISTA_RTD.xlsm .gitignore`
```

## Referências a LISTA_RTD.xlsm

```text
docs/AUDITORIA_ROTA_MESTRE_2.md:278:- `LISTA_RTD.xlsm`
docs/AUDITORIA_ROTA_MESTRE_3.md:166:LISTA_RTD.xlsm
docs/AUDITORIA_ROTA_MESTRE_3.md:178:LISTA_RTD.xlsm
docs/AUDITORIA_ROTA_MESTRE_3.md:239:A planilha `LISTA_RTD.xlsm` foi preservada como ponte RTD oficial e testada.
docs/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:476:LISTA_RTD.xlsm
docs/FASE_3_CLASSIFICACAO_FONTES_DADOS.md:52:LISTA_RTD.xlsm
docs/FASE_3_CLASSIFICACAO_FONTES_DADOS.md:286:| `LISTA_RTD.xlsm` | entrada bruta/configuração | separar dados de mercado, operação e parâmetros |
docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:133:ATT/checks/check_api_routes.py:13:    ROOT_DIR / "LISTA_RTD.xlsm",
docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:135:ATT/checks/check_api_routes.py:27:        "Nenhum workbook principal encontrado: LISTA_RTD.xlsm/xlsx"
docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:145:ATT/checks/check_end_to_end.py:10:    ROOT_DIR / "LISTA_RTD.xlsm",
docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:147:ATT/checks/check_structures.py:10:    ROOT_DIR / "LISTA_RTD.xlsm",
docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:203:- Os arquivos em `ATT/checks/` fazem validações locais envolvendo workbook Excel, `win32com` ou presença de `LISTA_RTD.xlsm/xlsx`.
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:170:•	LISTA_RTD.xlsm
docs/ROTA_MESTRE_3_RECONCILIACAO_POS_BACKUP.md:47:Classificar LISTA_RTD.xlsm e _usage_audit/ antes de qualquer limpeza.
docs/checkpoints/ciclo-2-fase-7a-auditoria-rtd-opcoes.md:29:./LISTA_RTD.xlsm
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:13:Confirmar que a ponte RTD operacional oficial é `LISTA_RTD.xlsm`, identificar referências remanescentes a `LISTA_RTD.xlsx` e separar documentação histórica de dependências operacionais.
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:25:100644 88b432a9355a4ad2e8bf0ef60d32e3be3d8fbbeb 0	LISTA_RTD.xlsm
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:31:-rw-r--r-- 1 eucal 197609 14156 Jun 16 21:09 LISTA_RTD.xlsm
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:34:## Verificação de .gitignore para LISTA_RTD.xlsm
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:37:OK: LISTA_RTD.xlsm não está ignorado pelo .gitignore.
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:40:## Referências gerais a LISTA_RTD.xlsx ou LISTA_RTD.xlsm
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:44:docs/AUDITORIA_ROTA_MESTRE_2.md:278:- `LISTA_RTD.xlsm`
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:46:docs/AUDITORIA_ROTA_MESTRE_3.md:166:LISTA_RTD.xlsm
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:47:docs/AUDITORIA_ROTA_MESTRE_3.md:178:LISTA_RTD.xlsm
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:48:docs/AUDITORIA_ROTA_MESTRE_3.md:239:A planilha `LISTA_RTD.xlsm` foi preservada como ponte RTD oficial e testada.
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:50:docs/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:476:LISTA_RTD.xlsm
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:51:docs/FASE_3_CLASSIFICACAO_FONTES_DADOS.md:52:LISTA_RTD.xlsm
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:52:docs/FASE_3_CLASSIFICACAO_FONTES_DADOS.md:286:| `LISTA_RTD.xlsm` | entrada bruta/configuração | separar dados de mercado, operação e parâmetros |
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:53:docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:133:ATT/checks/check_api_routes.py:13:    ROOT_DIR / "LISTA_RTD.xlsm",
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:54:docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:135:ATT/checks/check_api_routes.py:27:        "Nenhum workbook principal encontrado: LISTA_RTD.xlsm/xlsx"
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:55:docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:145:ATT/checks/check_end_to_end.py:10:    ROOT_DIR / "LISTA_RTD.xlsm",
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:56:docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:147:ATT/checks/check_structures.py:10:    ROOT_DIR / "LISTA_RTD.xlsm",
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:57:docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md:203:- Os arquivos em `ATT/checks/` fazem validações locais envolvendo workbook Excel, `win32com` ou presença de `LISTA_RTD.xlsm/xlsx`.
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:58:docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:170:•	LISTA_RTD.xlsm
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:59:docs/ROTA_MESTRE_3_RECONCILIACAO_POS_BACKUP.md:47:Classificar LISTA_RTD.xlsm e _usage_audit/ antes de qualquer limpeza.
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:61:docs/checkpoints/ciclo-2-fase-7a-auditoria-rtd-opcoes.md:29:./LISTA_RTD.xlsm
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:62:docs/checkpoints/fase-7h-pipeline-lista-rtd-option-quotes.md:9:Oficializar o fluxo de atualização de cotações de opções via Excel RTD, usando `LISTA_RTD.xlsm` como gateway para a tabela `rtd_option_quotes`.
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:63:docs/checkpoints/fase-7h-pipeline-lista-rtd-option-quotes.md:14:LISTA_RTD.xlsm
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:64:docs/checkpoints/fase-8a-auditoria-integracao-rtd-option-quotes-snapshot.md:202:4. Verificar se o Excel `LISTA_RTD.xlsm` contém as legs atuais que ainda não foram persistidas em `structure_legs`.
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:65:docs/checkpoints/fase-8a-auditoria-integracao-rtd-option-quotes-snapshot.md:206:   - uma aba do `LISTA_RTD.xlsm`;
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:66:docs/checkpoints/fase-8b-reconciliacao-estruturas-legs-rtd-option-quotes.md:65:A tabela `rtd_option_quotes` contém 8 cotações atuais importadas de `LISTA_RTD.xlsm`.
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:67:docs/checkpoints/fase-8b-reconciliacao-estruturas-legs-rtd-option-quotes.md:163:enquanto rtd_option_quotes representa códigos atuais vindos do LISTA_RTD.xlsm.
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:68:docs/checkpoints/fase-8b-reconciliacao-estruturas-legs-rtd-option-quotes.md:179:4. Confirmar se `LISTA_RTD.xlsm` contém apenas cotações ou também contém composição atual das estruturas.
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:69:docs/checkpoints/fase-8d-auditoria-codigo-funcional-rtd.txt:222:scripts/import_lista_rtd_excel_to_option_quotes.py:2:Importa cotações RTD de opções do LISTA_RTD.xlsm para rtd_option_quotes.
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:70:docs/checkpoints/fase-8d-auditoria-codigo-funcional-rtd.txt:249:scripts/import_lista_rtd_excel_to_option_quotes.py:525:        description="Importa LISTA_RTD.xlsm para rtd_option_quotes"
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:71:docs/checkpoints/fase-8d-auditoria-codigo-funcional-rtd.txt:250:scripts/import_lista_rtd_excel_to_option_quotes.py:631:            print("Importação LISTA_RTD.xlsm -> rtd_option_quotes")
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:72:docs/checkpoints/fase-8d-auditoria-codigo-funcional-rtd.txt:251:scripts/import_lista_rtd_excel_to_option_quotes.py:641:        print("Importação LISTA_RTD.xlsm -> rtd_option_quotes")
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:73:docs/checkpoints/fase-8d-auditoria-codigo-funcional-rtd.txt:344:scripts/run_lista_rtd_option_quotes_pipeline.py:3:Pipeline LISTA_RTD.xlsm -> rtd_option_quotes.
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:74:docs/checkpoints/fase-8d-auditoria-codigo-funcional-rtd.txt:352:scripts/run_lista_rtd_option_quotes_pipeline.py:60:        description="Executa pipeline LISTA_RTD.xlsm -> rtd_option_quotes."
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:75:docs/checkpoints/fase-8d-auditoria-codigo-funcional-rtd.txt:353:scripts/run_lista_rtd_option_quotes_pipeline.py:148:            print("Pipeline LISTA_RTD.xlsm -> rtd_option_quotes")
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:76:docs/checkpoints/fase-8d-auditoria-codigo-funcional-rtd.txt:354:scripts/run_lista_rtd_option_quotes_pipeline.py:210:        print("Pipeline LISTA_RTD.xlsm -> rtd_option_quotes")
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:77:docs/checkpoints/fase-8d-auditoria-pontos-integracao-rtd.txt:1044:scripts/import_lista_rtd_excel_to_option_quotes.py:2:Importa cotações RTD de opções do LISTA_RTD.xlsm para rtd_option_quotes.
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:78:docs/checkpoints/fase-8d-auditoria-pontos-integracao-rtd.txt:1071:scripts/import_lista_rtd_excel_to_option_quotes.py:525:        description="Importa LISTA_RTD.xlsm para rtd_option_quotes"
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:79:docs/checkpoints/fase-8d-auditoria-pontos-integracao-rtd.txt:1072:scripts/import_lista_rtd_excel_to_option_quotes.py:631:            print("Importação LISTA_RTD.xlsm -> rtd_option_quotes")
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:80:docs/checkpoints/fase-8d-auditoria-pontos-integracao-rtd.txt:1073:scripts/import_lista_rtd_excel_to_option_quotes.py:641:        print("Importação LISTA_RTD.xlsm -> rtd_option_quotes")
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:81:docs/checkpoints/fase-8d-auditoria-pontos-integracao-rtd.txt:1140:scripts/run_lista_rtd_option_quotes_pipeline.py:3:Pipeline LISTA_RTD.xlsm -> rtd_option_quotes.
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:82:docs/checkpoints/fase-8d-auditoria-pontos-integracao-rtd.txt:1148:scripts/run_lista_rtd_option_quotes_pipeline.py:60:        description="Executa pipeline LISTA_RTD.xlsm -> rtd_option_quotes."
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:83:docs/checkpoints/fase-8d-auditoria-pontos-integracao-rtd.txt:1149:scripts/run_lista_rtd_option_quotes_pipeline.py:148:            print("Pipeline LISTA_RTD.xlsm -> rtd_option_quotes")
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:84:docs/checkpoints/fase-8d-auditoria-pontos-integracao-rtd.txt:1150:scripts/run_lista_rtd_option_quotes_pipeline.py:210:        print("Pipeline LISTA_RTD.xlsm -> rtd_option_quotes")
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:85:docs/checkpoints/fase-8d-grep-fluxo-preco-rtd.txt:83:scripts/import_lista_rtd_excel_to_option_quotes.py:2:Importa cotações RTD de opções do LISTA_RTD.xlsm para rtd_option_quotes.
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:86:docs/checkpoints/fase-8d-grep-fluxo-preco-rtd.txt:132:scripts/import_lista_rtd_excel_to_option_quotes.py:525:        description="Importa LISTA_RTD.xlsm para rtd_option_quotes"
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:87:docs/checkpoints/fase-8d-grep-fluxo-preco-rtd.txt:133:scripts/import_lista_rtd_excel_to_option_quotes.py:631:            print("Importação LISTA_RTD.xlsm -> rtd_option_quotes")
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:88:docs/checkpoints/fase-8d-grep-fluxo-preco-rtd.txt:134:scripts/import_lista_rtd_excel_to_option_quotes.py:641:        print("Importação LISTA_RTD.xlsm -> rtd_option_quotes")
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:89:docs/checkpoints/fase-8d-grep-fluxo-preco-rtd.txt:175:scripts/run_lista_rtd_option_quotes_pipeline.py:3:Pipeline LISTA_RTD.xlsm -> rtd_option_quotes.
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:90:docs/checkpoints/fase-8d-grep-fluxo-preco-rtd.txt:181:scripts/run_lista_rtd_option_quotes_pipeline.py:60:        description="Executa pipeline LISTA_RTD.xlsm -> rtd_option_quotes."
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:91:docs/checkpoints/fase-8d-grep-fluxo-preco-rtd.txt:182:scripts/run_lista_rtd_option_quotes_pipeline.py:148:            print("Pipeline LISTA_RTD.xlsm -> rtd_option_quotes")
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:92:docs/checkpoints/fase-8d-grep-fluxo-preco-rtd.txt:183:scripts/run_lista_rtd_option_quotes_pipeline.py:210:        print("Pipeline LISTA_RTD.xlsm -> rtd_option_quotes")
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:93:docs/checkpoints/fase-8e-before-auditoria-rota-mestre-2.md:278:- `LISTA_RTD.xlsm`
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:99:docs/fase_2_auditoria_contrato_rtd_excel.md:20:- `LISTA_RTD.xlsm`
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:102:docs/mapeamento_automacao_opcoes_rtd.md:1255:- `LISTA_RTD.xlsm` — `outros` — score `6`
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:104:docs/validacoes/fase-17-mapa-pastas-arquivos.md:127:LISTA_RTD.xlsm
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:105:docs/validacoes/fase-17-mapa-pastas-arquivos.md:144:- `LISTA_RTD.xlsm` está versionado.
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:107:docs/validacoes/fase-17-mapa-pastas-arquivos.md:156:| `LISTA_RTD.xlsm` | Sim | Versionado |
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:109:docs/validacoes/fechamento-rota-mestre-2.md:94:- `LISTA_RTD.xlsm` foi removida do versionamento e protegida no `.gitignore`;
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:111:docs/validacoes/fechamento-rota-mestre-2.md:100:- `git diff --name-status origin/main..HEAD -- LISTA_RTD.xlsx LISTA_RTD.xlsm .gitignore`
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:112:scripts/import_lista_rtd_excel_to_option_quotes.py:2:Importa cotações RTD de opções do LISTA_RTD.xlsm para rtd_option_quotes.
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:113:scripts/import_lista_rtd_excel_to_option_quotes.py:5:    LISTA_RTD.xlsm aberto no Excel
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:114:scripts/import_lista_rtd_excel_to_option_quotes.py:27:DEFAULT_WORKBOOK = "LISTA_RTD.xlsm"
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:115:scripts/import_lista_rtd_excel_to_option_quotes.py:525:        description="Importa LISTA_RTD.xlsm para rtd_option_quotes"
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:116:scripts/import_lista_rtd_excel_to_option_quotes.py:537:        help="Caminho do workbook RTD. Padrão: LISTA_RTD.xlsm",
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:117:scripts/import_lista_rtd_excel_to_option_quotes.py:631:            print("Importação LISTA_RTD.xlsm -> rtd_option_quotes")
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:118:scripts/import_lista_rtd_excel_to_option_quotes.py:641:        print("Importação LISTA_RTD.xlsm -> rtd_option_quotes")
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:119:scripts/run_lista_rtd_option_quotes_pipeline.py:3:Pipeline LISTA_RTD.xlsm -> rtd_option_quotes.
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:120:scripts/run_lista_rtd_option_quotes_pipeline.py:60:        description="Executa pipeline LISTA_RTD.xlsm -> rtd_option_quotes."
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:121:scripts/run_lista_rtd_option_quotes_pipeline.py:71:        default="LISTA_RTD.xlsm",
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:122:scripts/run_lista_rtd_option_quotes_pipeline.py:72:        help="Caminho do workbook RTD. Padrão: LISTA_RTD.xlsm",
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:123:scripts/run_lista_rtd_option_quotes_pipeline.py:148:            print("Pipeline LISTA_RTD.xlsm -> rtd_option_quotes")
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:124:scripts/run_lista_rtd_option_quotes_pipeline.py:210:        print("Pipeline LISTA_RTD.xlsm -> rtd_option_quotes")
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:131:scripts/import_lista_rtd_excel_to_option_quotes.py:2:Importa cotações RTD de opções do LISTA_RTD.xlsm para rtd_option_quotes.
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:132:scripts/import_lista_rtd_excel_to_option_quotes.py:5:    LISTA_RTD.xlsm aberto no Excel
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:133:scripts/import_lista_rtd_excel_to_option_quotes.py:27:DEFAULT_WORKBOOK = "LISTA_RTD.xlsm"
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:134:scripts/import_lista_rtd_excel_to_option_quotes.py:525:        description="Importa LISTA_RTD.xlsm para rtd_option_quotes"
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:135:scripts/import_lista_rtd_excel_to_option_quotes.py:537:        help="Caminho do workbook RTD. Padrão: LISTA_RTD.xlsm",
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:136:scripts/import_lista_rtd_excel_to_option_quotes.py:631:            print("Importação LISTA_RTD.xlsm -> rtd_option_quotes")
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:137:scripts/import_lista_rtd_excel_to_option_quotes.py:641:        print("Importação LISTA_RTD.xlsm -> rtd_option_quotes")
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:138:scripts/run_lista_rtd_option_quotes_pipeline.py:3:Pipeline LISTA_RTD.xlsm -> rtd_option_quotes.
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:139:scripts/run_lista_rtd_option_quotes_pipeline.py:60:        description="Executa pipeline LISTA_RTD.xlsm -> rtd_option_quotes."
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:140:scripts/run_lista_rtd_option_quotes_pipeline.py:71:        default="LISTA_RTD.xlsm",
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:141:scripts/run_lista_rtd_option_quotes_pipeline.py:72:        help="Caminho do workbook RTD. Padrão: LISTA_RTD.xlsm",
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:142:scripts/run_lista_rtd_option_quotes_pipeline.py:148:            print("Pipeline LISTA_RTD.xlsm -> rtd_option_quotes")
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:143:scripts/run_lista_rtd_option_quotes_pipeline.py:210:        print("Pipeline LISTA_RTD.xlsm -> rtd_option_quotes")
docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md:148:- `LISTA_RTD.xlsm` é a ponte RTD oficial e testada.
docs/checkpoints/fase-7h-pipeline-lista-rtd-option-quotes.md:9:Oficializar o fluxo de atualização de cotações de opções via Excel RTD, usando `LISTA_RTD.xlsm` como gateway para a tabela `rtd_option_quotes`.
docs/checkpoints/fase-7h-pipeline-lista-rtd-option-quotes.md:14:LISTA_RTD.xlsm
docs/checkpoints/fase-8a-auditoria-integracao-rtd-option-quotes-snapshot.md:202:4. Verificar se o Excel `LISTA_RTD.xlsm` contém as legs atuais que ainda não foram persistidas em `structure_legs`.
docs/checkpoints/fase-8a-auditoria-integracao-rtd-option-quotes-snapshot.md:206:   - uma aba do `LISTA_RTD.xlsm`;
docs/checkpoints/fase-8b-reconciliacao-estruturas-legs-rtd-option-quotes.md:65:A tabela `rtd_option_quotes` contém 8 cotações atuais importadas de `LISTA_RTD.xlsm`.
docs/checkpoints/fase-8b-reconciliacao-estruturas-legs-rtd-option-quotes.md:163:enquanto rtd_option_quotes representa códigos atuais vindos do LISTA_RTD.xlsm.
docs/checkpoints/fase-8b-reconciliacao-estruturas-legs-rtd-option-quotes.md:179:4. Confirmar se `LISTA_RTD.xlsm` contém apenas cotações ou também contém composição atual das estruturas.
docs/checkpoints/fase-8d-auditoria-codigo-funcional-rtd.txt:222:scripts/import_lista_rtd_excel_to_option_quotes.py:2:Importa cotações RTD de opções do LISTA_RTD.xlsm para rtd_option_quotes.
docs/checkpoints/fase-8d-auditoria-codigo-funcional-rtd.txt:249:scripts/import_lista_rtd_excel_to_option_quotes.py:525:        description="Importa LISTA_RTD.xlsm para rtd_option_quotes"
docs/checkpoints/fase-8d-auditoria-codigo-funcional-rtd.txt:250:scripts/import_lista_rtd_excel_to_option_quotes.py:631:            print("Importação LISTA_RTD.xlsm -> rtd_option_quotes")
docs/checkpoints/fase-8d-auditoria-codigo-funcional-rtd.txt:251:scripts/import_lista_rtd_excel_to_option_quotes.py:641:        print("Importação LISTA_RTD.xlsm -> rtd_option_quotes")
docs/checkpoints/fase-8d-auditoria-codigo-funcional-rtd.txt:344:scripts/run_lista_rtd_option_quotes_pipeline.py:3:Pipeline LISTA_RTD.xlsm -> rtd_option_quotes.
docs/checkpoints/fase-8d-auditoria-codigo-funcional-rtd.txt:352:scripts/run_lista_rtd_option_quotes_pipeline.py:60:        description="Executa pipeline LISTA_RTD.xlsm -> rtd_option_quotes."
docs/checkpoints/fase-8d-auditoria-codigo-funcional-rtd.txt:353:scripts/run_lista_rtd_option_quotes_pipeline.py:148:            print("Pipeline LISTA_RTD.xlsm -> rtd_option_quotes")
docs/checkpoints/fase-8d-auditoria-codigo-funcional-rtd.txt:354:scripts/run_lista_rtd_option_quotes_pipeline.py:210:        print("Pipeline LISTA_RTD.xlsm -> rtd_option_quotes")
docs/checkpoints/fase-8d-auditoria-pontos-integracao-rtd.txt:1044:scripts/import_lista_rtd_excel_to_option_quotes.py:2:Importa cotações RTD de opções do LISTA_RTD.xlsm para rtd_option_quotes.
docs/checkpoints/fase-8d-auditoria-pontos-integracao-rtd.txt:1071:scripts/import_lista_rtd_excel_to_option_quotes.py:525:        description="Importa LISTA_RTD.xlsm para rtd_option_quotes"
docs/checkpoints/fase-8d-auditoria-pontos-integracao-rtd.txt:1072:scripts/import_lista_rtd_excel_to_option_quotes.py:631:            print("Importação LISTA_RTD.xlsm -> rtd_option_quotes")
docs/checkpoints/fase-8d-auditoria-pontos-integracao-rtd.txt:1073:scripts/import_lista_rtd_excel_to_option_quotes.py:641:        print("Importação LISTA_RTD.xlsm -> rtd_option_quotes")
docs/checkpoints/fase-8d-auditoria-pontos-integracao-rtd.txt:1140:scripts/run_lista_rtd_option_quotes_pipeline.py:3:Pipeline LISTA_RTD.xlsm -> rtd_option_quotes.
docs/checkpoints/fase-8d-auditoria-pontos-integracao-rtd.txt:1148:scripts/run_lista_rtd_option_quotes_pipeline.py:60:        description="Executa pipeline LISTA_RTD.xlsm -> rtd_option_quotes."
docs/checkpoints/fase-8d-auditoria-pontos-integracao-rtd.txt:1149:scripts/run_lista_rtd_option_quotes_pipeline.py:148:            print("Pipeline LISTA_RTD.xlsm -> rtd_option_quotes")
docs/checkpoints/fase-8d-auditoria-pontos-integracao-rtd.txt:1150:scripts/run_lista_rtd_option_quotes_pipeline.py:210:        print("Pipeline LISTA_RTD.xlsm -> rtd_option_quotes")
docs/checkpoints/fase-8d-grep-fluxo-preco-rtd.txt:83:scripts/import_lista_rtd_excel_to_option_quotes.py:2:Importa cotações RTD de opções do LISTA_RTD.xlsm para rtd_option_quotes.
docs/checkpoints/fase-8d-grep-fluxo-preco-rtd.txt:132:scripts/import_lista_rtd_excel_to_option_quotes.py:525:        description="Importa LISTA_RTD.xlsm para rtd_option_quotes"
docs/checkpoints/fase-8d-grep-fluxo-preco-rtd.txt:133:scripts/import_lista_rtd_excel_to_option_quotes.py:631:            print("Importação LISTA_RTD.xlsm -> rtd_option_quotes")
docs/checkpoints/fase-8d-grep-fluxo-preco-rtd.txt:134:scripts/import_lista_rtd_excel_to_option_quotes.py:641:        print("Importação LISTA_RTD.xlsm -> rtd_option_quotes")
docs/checkpoints/fase-8d-grep-fluxo-preco-rtd.txt:175:scripts/run_lista_rtd_option_quotes_pipeline.py:3:Pipeline LISTA_RTD.xlsm -> rtd_option_quotes.
docs/checkpoints/fase-8d-grep-fluxo-preco-rtd.txt:181:scripts/run_lista_rtd_option_quotes_pipeline.py:60:        description="Executa pipeline LISTA_RTD.xlsm -> rtd_option_quotes."
docs/checkpoints/fase-8d-grep-fluxo-preco-rtd.txt:182:scripts/run_lista_rtd_option_quotes_pipeline.py:148:            print("Pipeline LISTA_RTD.xlsm -> rtd_option_quotes")
docs/checkpoints/fase-8d-grep-fluxo-preco-rtd.txt:183:scripts/run_lista_rtd_option_quotes_pipeline.py:210:        print("Pipeline LISTA_RTD.xlsm -> rtd_option_quotes")
docs/checkpoints/fase-8e-before-auditoria-rota-mestre-2.md:278:- `LISTA_RTD.xlsm`
docs/fase_2_auditoria_contrato_rtd_excel.md:20:- `LISTA_RTD.xlsm`
docs/mapeamento_automacao_opcoes_rtd.md:1255:- `LISTA_RTD.xlsm` — `outros` — score `6`
docs/validacoes/fase-17-mapa-pastas-arquivos.md:127:LISTA_RTD.xlsm
docs/validacoes/fase-17-mapa-pastas-arquivos.md:144:- `LISTA_RTD.xlsm` está versionado.
docs/validacoes/fase-17-mapa-pastas-arquivos.md:156:| `LISTA_RTD.xlsm` | Sim | Versionado |
docs/validacoes/fechamento-rota-mestre-2.md:94:- `LISTA_RTD.xlsm` foi removida do versionamento e protegida no `.gitignore`;
docs/validacoes/fechamento-rota-mestre-2.md:100:- `git diff --name-status origin/main..HEAD -- LISTA_RTD.xlsx LISTA_RTD.xlsm .gitignore`
scripts/import_lista_rtd_excel_to_option_quotes.py:2:Importa cotações RTD de opções do LISTA_RTD.xlsm para rtd_option_quotes.
scripts/import_lista_rtd_excel_to_option_quotes.py:5:    LISTA_RTD.xlsm aberto no Excel
scripts/import_lista_rtd_excel_to_option_quotes.py:27:DEFAULT_WORKBOOK = "LISTA_RTD.xlsm"
scripts/import_lista_rtd_excel_to_option_quotes.py:525:        description="Importa LISTA_RTD.xlsm para rtd_option_quotes"
scripts/import_lista_rtd_excel_to_option_quotes.py:537:        help="Caminho do workbook RTD. Padrão: LISTA_RTD.xlsm",
scripts/import_lista_rtd_excel_to_option_quotes.py:631:            print("Importação LISTA_RTD.xlsm -> rtd_option_quotes")
scripts/import_lista_rtd_excel_to_option_quotes.py:641:        print("Importação LISTA_RTD.xlsm -> rtd_option_quotes")
scripts/run_lista_rtd_option_quotes_pipeline.py:3:Pipeline LISTA_RTD.xlsm -> rtd_option_quotes.
scripts/run_lista_rtd_option_quotes_pipeline.py:60:        description="Executa pipeline LISTA_RTD.xlsm -> rtd_option_quotes."
scripts/run_lista_rtd_option_quotes_pipeline.py:71:        default="LISTA_RTD.xlsm",
scripts/run_lista_rtd_option_quotes_pipeline.py:72:        help="Caminho do workbook RTD. Padrão: LISTA_RTD.xlsm",
scripts/run_lista_rtd_option_quotes_pipeline.py:148:            print("Pipeline LISTA_RTD.xlsm -> rtd_option_quotes")
scripts/run_lista_rtd_option_quotes_pipeline.py:210:        print("Pipeline LISTA_RTD.xlsm -> rtd_option_quotes")
```

## Verificação específica do JSON de mapeamento

```text
    {
      "path": "scripts/validate_derived_db.py",
      "role": "scripts",
      "level": "medio",
      "score": 7,
      "path_hits": {},
      "content_hits": {
        "persistencia": 3,
        "ui": 2,
        "calculo": 2
      },
      "note": ""
    },
    {
      "path": "LISTA_RTD.xlsx",
      "role": "outros",
      "level": "medio",
      "score": 6,
      "path_hits": {
        "rtd": 1,
        "excel": 1
      },
      "content_hits": {},
      "note": ""
    },
    {
```

## Quem referencia o JSON de mapeamento

```text
_usage_audit/uso_scripts_2026-06-16_13-40-00/RESUMO.md:37:./docs/mapeamento_automacao_opcoes_rtd.json:2071:      "path": "limpar_repositorio_seguro.sh",
_usage_audit/uso_scripts_2026-06-16_13-40-00/RESUMO.md:65:./docs/mapeamento_automacao_opcoes_rtd.json:2364:      "path": "find_structure.sh",
_usage_audit/uso_scripts_2026-06-16_13-40-00/RESUMO.md:92:./docs/mapeamento_automacao_opcoes_rtd.json:740:      "path": "mapear_repositorio.sh",
_usage_audit/uso_scripts_2026-06-16_13-40-00/find_structure.sh_referencias.txt:1:./docs/mapeamento_automacao_opcoes_rtd.json:2364:      "path": "find_structure.sh",
_usage_audit/uso_scripts_2026-06-16_13-40-00/find_structure.sh_referencias_testes.txt:1:./docs/mapeamento_automacao_opcoes_rtd.json:2364:      "path": "find_structure.sh",
_usage_audit/uso_scripts_2026-06-16_13-40-00/limpar_repositorio_seguro.sh_referencias.txt:1:./docs/mapeamento_automacao_opcoes_rtd.json:2071:      "path": "limpar_repositorio_seguro.sh",
_usage_audit/uso_scripts_2026-06-16_13-40-00/limpar_repositorio_seguro.sh_referencias_testes.txt:1:./docs/mapeamento_automacao_opcoes_rtd.json:2071:      "path": "limpar_repositorio_seguro.sh",
_usage_audit/uso_scripts_2026-06-16_13-40-00/mapear_repositorio.sh_referencias.txt:1:./docs/mapeamento_automacao_opcoes_rtd.json:740:      "path": "mapear_repositorio.sh",
_usage_audit/uso_scripts_2026-06-16_13-40-00/mapear_repositorio.sh_referencias_testes.txt:1:./docs/mapeamento_automacao_opcoes_rtd.json:740:      "path": "mapear_repositorio.sh",
docs/AUDITORIA_ROTA_MESTRE_2.md:126:- `docs/mapeamento_automacao_opcoes_rtd.json`
docs/AUDITORIA_ROTA_MESTRE_2.md:139:test -f docs/mapeamento_automacao_opcoes_rtd.json
docs/AUDITORIA_ROTA_MESTRE_2.md:154:- `docs/mapeamento_automacao_opcoes_rtd.json`
docs/AUDITORIA_ROTA_MESTRE_2.md:210:- `docs/mapeamento_automacao_opcoes_rtd.json`
docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:944:•	mapeamento_automacao_opcoes_rtd.json
docs/checkpoints/ciclo-2-fase-7a-auditoria-rtd-opcoes.md:39:./docs/mapeamento_automacao_opcoes_rtd.json
docs/checkpoints/fase-8d-auditoria-pontos-integracao-rtd.txt:802:docs/mapeamento_automacao_opcoes_rtd.json:660:      "path": "repositories/rtd_option_quotes_repository.py",
docs/checkpoints/fase-8d-auditoria-pontos-integracao-rtd.txt:803:docs/mapeamento_automacao_opcoes_rtd.json:708:      "path": "repositories/market_snapshot_repository.py",
docs/checkpoints/fase-8d-auditoria-pontos-integracao-rtd.txt:804:docs/mapeamento_automacao_opcoes_rtd.json:721:      "note": "Prioritário para auditoria de persistência de snapshot."
docs/checkpoints/fase-8d-auditoria-pontos-integracao-rtd.txt:805:docs/mapeamento_automacao_opcoes_rtd.json:756:      "path": "ATT/tests/test_legacy_structure_legs_importer_integration.py",
docs/checkpoints/fase-8d-auditoria-pontos-integracao-rtd.txt:806:docs/mapeamento_automacao_opcoes_rtd.json:909:      "path": "ATT/tests/test_system_snapshots_repository.py",
docs/checkpoints/fase-8d-auditoria-pontos-integracao-rtd.txt:807:docs/mapeamento_automacao_opcoes_rtd.json:925:      "path": "services/market_snapshot_selector.py",
docs/checkpoints/fase-8d-auditoria-pontos-integracao-rtd.txt:808:docs/mapeamento_automacao_opcoes_rtd.json:937:      "note": "Prioritário para auditoria de seleção de snapshot."
docs/checkpoints/fase-8d-auditoria-pontos-integracao-rtd.txt:809:docs/mapeamento_automacao_opcoes_rtd.json:940:      "path": "ATT/tests/test_legacy_structure_legs_reader.py",
docs/checkpoints/fase-8d-auditoria-pontos-integracao-rtd.txt:810:docs/mapeamento_automacao_opcoes_rtd.json:1063:      "path": "repositories/system_snapshots_repository.py",
docs/checkpoints/fase-8d-auditoria-pontos-integracao-rtd.txt:811:docs/mapeamento_automacao_opcoes_rtd.json:1184:      "path": "domain/market_snapshot.py",
docs/checkpoints/fase-8d-auditoria-pontos-integracao-rtd.txt:812:docs/mapeamento_automacao_opcoes_rtd.json:1197:      "path": "ATT/tests/test_legacy_structure_legs_importer.py",
docs/checkpoints/fase-8d-auditoria-pontos-integracao-rtd.txt:813:docs/mapeamento_automacao_opcoes_rtd.json:1286:      "path": "services/market_snapshot_provider.py",
docs/checkpoints/fase-8d-auditoria-pontos-integracao-rtd.txt:814:docs/mapeamento_automacao_opcoes_rtd.json:1297:      "note": "Prioritário para auditoria de snapshot."
docs/checkpoints/fase-8d-auditoria-pontos-integracao-rtd.txt:815:docs/mapeamento_automacao_opcoes_rtd.json:1432:      "path": "ATT/tests/test_system_snapshots_schema.py",
docs/checkpoints/fase-8d-auditoria-pontos-integracao-rtd.txt:816:docs/mapeamento_automacao_opcoes_rtd.json:1608:      "path": "ATT/tests/test_market_snapshot_provider.py",
docs/checkpoints/fase-8d-auditoria-pontos-integracao-rtd.txt:817:docs/mapeamento_automacao_opcoes_rtd.json:1636:      "path": "scripts/import_legacy_structure_legs.py",
docs/checkpoints/fase-8d-auditoria-pontos-integracao-rtd.txt:818:docs/mapeamento_automacao_opcoes_rtd.json:1876:      "path": "services/legacy_structure_legs_importer.py",
docs/checkpoints/fase-8d-auditoria-pontos-integracao-rtd.txt:819:docs/mapeamento_automacao_opcoes_rtd.json:1890:      "path": "services/legacy_structure_legs_reader.py",
docs/checkpoints/fase-8d-auditoria-pontos-integracao-rtd.txt:820:docs/mapeamento_automacao_opcoes_rtd.json:2514:      "path": "scripts/purge_derived_snapshots.py",
docs/checkpoints/fase-8e-before-auditoria-rota-mestre-2.md:126:- `docs/mapeamento_automacao_opcoes_rtd.json`
docs/checkpoints/fase-8e-before-auditoria-rota-mestre-2.md:139:test -f docs/mapeamento_automacao_opcoes_rtd.json
docs/checkpoints/fase-8e-before-auditoria-rota-mestre-2.md:154:- `docs/mapeamento_automacao_opcoes_rtd.json`
docs/checkpoints/fase-8e-before-auditoria-rota-mestre-2.md:210:- `docs/mapeamento_automacao_opcoes_rtd.json`
docs/lista_priorizada_automacao_opcoes_rtd.md:8:- `docs/mapeamento_automacao_opcoes_rtd.json`
scripts/mapear_automacao_opcoes_rtd.py:12:OUT_JSON = ROOT / "docs" / "mapeamento_automacao_opcoes_rtd.json"
```

## Classificação preliminar

| Arquivo/padrão | Classificação | Ação recomendada |
|---|---|---|
| `.gitignore: LISTA_RTD.xlsx` | Proteção contra retorno do legado | Manter |
| `scripts/*LISTA_RTD.xlsm*` | Operacional atual | Manter |
| `docs/checkpoints/*` | Evidência histórica | Manter, salvo nota explicativa futura |
| `docs/decisions/*LISTA_RTD.xlsx*` | Decisão histórica possivelmente superada | Atualizar com nota de supersessão, sem apagar histórico |
| `docs/validacoes/*LISTA_RTD.xlsx*` | Validação histórica possivelmente superada | Atualizar com nota de supersessão |
| `docs/mapeamento_automacao_opcoes_rtd.json` | Mapeamento documental, precisa confirmar se é consumido por código | Não alterar até confirmar consumo |

## Decisão desta etapa

Nenhuma dependência funcional ativa de `LISTA_RTD.xlsx` foi confirmada nesta etapa.

A próxima ação segura é atualizar documentação viva para declarar que referências anteriores a `LISTA_RTD.xlsx` foram supersedidas por `LISTA_RTD.xlsm` como ponte RTD oficial.
