# Fase 2 — Reconciliação da ponte RTD oficial

Data: 2026-06-17 09:26:59 -0300

Branch:

```text
fase-12-fechamento-ciclo
```

## Objetivo

Confirmar que a ponte RTD operacional oficial é `LISTA_RTD.xlsm`, identificar referências remanescentes a `LISTA_RTD.xlsx` e separar documentação histórica de dependências operacionais.

## Estado Git inicial

```text
## fase-12-fechamento-ciclo...origin/fase-12-fechamento-ciclo
?? docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md
```

## Arquivos RTD versionados

```text
100644 88b432a9355a4ad2e8bf0ef60d32e3be3d8fbbeb 0	LISTA_RTD.xlsm
```

## Arquivos RTD presentes no diretório

```text
-rw-r--r-- 1 eucal 197609 14156 Jun 16 21:09 LISTA_RTD.xlsm
```

## Verificação de .gitignore para LISTA_RTD.xlsm

```text
OK: LISTA_RTD.xlsm não está ignorado pelo .gitignore.
```

## Referências gerais a LISTA_RTD.xlsx ou LISTA_RTD.xlsm

```text
.gitignore:12:LISTA_RTD.xlsx
docs/AUDITORIA_ROTA_MESTRE_2.md:278:- `LISTA_RTD.xlsm`
docs/AUDITORIA_ROTA_MESTRE_3.md:92:O dry-run com LISTA_RTD.xlsx falhou porque a aba disponível é diferente das esperadas pelos scripts:
docs/AUDITORIA_ROTA_MESTRE_3.md:166:LISTA_RTD.xlsm
docs/AUDITORIA_ROTA_MESTRE_3.md:178:LISTA_RTD.xlsm
docs/AUDITORIA_ROTA_MESTRE_3.md:239:A planilha `LISTA_RTD.xlsm` foi preservada como ponte RTD oficial e testada.
docs/AUDITORIA_ROTA_MESTRE_3.md:241:A planilha RTD legada abolida foi removida do versionamento. A entrada `LISTA_RTD.xlsx` deixou de ser tratada como ponte RTD oficial.
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
docs/checkpoints/ciclo-2-fase-7a-auditoria-rtd-opcoes.md:28:./LISTA_RTD.xlsx
docs/checkpoints/ciclo-2-fase-7a-auditoria-rtd-opcoes.md:29:./LISTA_RTD.xlsm
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
docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:73:## Decisão sobre fontes legadas e LISTA_RTD.xlsx
docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:82:- `LISTA_RTD.xlsx` passa a ser considerada candidata a fonte/gateway para o universo bruto RTD.
docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:88:O fluxo novo não deve reconstruir o sistema em torno dos dados obsoletos. A Fase 2 deve mapear o legado existente e preparar a transição para um modelo onde a `LISTA_RTD.xlsx` alimenta dados RTD brutos, enquanto as estruturas operacionais nascem e vivem no banco do sistema.
docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:113:- `db/import_excel.py` não consome `LISTA_RTD.xlsx`.
docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md:128:- criar posteriormente um gateway específico para `LISTA_RTD.xlsx`;
docs/fase_2_auditoria_contrato_rtd_excel.md:20:- `LISTA_RTD.xlsm`
docs/mapeamento_automacao_opcoes_rtd.json:2539:      "path": "LISTA_RTD.xlsx",
docs/mapeamento_automacao_opcoes_rtd.md:1254:- `LISTA_RTD.xlsx` — `outros` — score `6`
docs/mapeamento_automacao_opcoes_rtd.md:1255:- `LISTA_RTD.xlsm` — `outros` — score `6`
docs/validacoes/fase-17-mapa-pastas-arquivos.md:126:LISTA_RTD.xlsx
docs/validacoes/fase-17-mapa-pastas-arquivos.md:127:LISTA_RTD.xlsm
docs/validacoes/fase-17-mapa-pastas-arquivos.md:144:- `LISTA_RTD.xlsm` está versionado.
docs/validacoes/fase-17-mapa-pastas-arquivos.md:145:- `LISTA_RTD.xlsx` está versionado.
docs/validacoes/fase-17-mapa-pastas-arquivos.md:156:| `LISTA_RTD.xlsm` | Sim | Versionado |
docs/validacoes/fase-17-mapa-pastas-arquivos.md:157:| `LISTA_RTD.xlsx` | Sim | Versionado |
docs/validacoes/fechamento-rota-mestre-2.md:94:- `LISTA_RTD.xlsm` foi removida do versionamento e protegida no `.gitignore`;
docs/validacoes/fechamento-rota-mestre-2.md:95:- `LISTA_RTD.xlsx` foi restaurada como arquivo versionado conforme referência de `origin/main`;
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

## Referências operacionais em código

```text
docs/mapeamento_automacao_opcoes_rtd.json:2539:      "path": "LISTA_RTD.xlsx",
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

## Decisão preliminar

- `LISTA_RTD.xlsm` é a ponte RTD oficial e testada.
- `LISTA_RTD.xlsx` não deve ser tratada como ponte operacional atual.
- Referências a `LISTA_RTD.xlsx` em documentos antigos devem ser classificadas como históricas, salvo se indicarem dependência operacional ativa.
- Nenhuma alteração funcional foi realizada nesta etapa.
