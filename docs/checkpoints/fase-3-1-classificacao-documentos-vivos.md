# Fase 3.1 — Classificação de documentos vivos e históricos

Data: 2026-06-17 09:51:36 -0300

## Objetivo

Classificar os documentos inventariados na Fase 3 entre documentos vivos, históricos, auditorias, decisões e artefatos gerados, sem alteração funcional.

## Estado Git inicial

```text
## fase-12-fechamento-ciclo...origin/fase-12-fechamento-ciclo
?? docs/checkpoints/fase-3-1-classificacao-documentos-vivos.md
```

## Últimos commits

```text
3b9a132 docs: inventaria documentos vivos e historicos
0c994c4 docs: valida supersessao da ponte RTD
4cb4f50 docs: registra supersessao de LISTA_RTD xlsx
f53d74d docs: classifica referencias remanescentes LISTA_RTD
eb913ca docs: registra reconciliacao da ponte RTD oficial
6c68f37 chore: permite versionamento da ponte RTD oficial
3889e42 docs: oficializa LISTA_RTD.xlsm como ponte RTD
1750e0d docs: encerra fase 1 de higiene git
```

## Documentos vivos candidatos

| Documento | Classe | Justificativa | Ação recomendada |
|---|---|---|---|
| `docs/ROTA_MESTRE_3_RECONCILIACAO_POS_BACKUP.md` | Vivo | Rota atual de reconciliação pós-backup | Manter como referência principal |
| `docs/decisions/2026-06-17-supersessao-lista-rtd-xlsx.md` | Decisão viva | Formaliza supersessão de `LISTA_RTD.xlsx` por `LISTA_RTD.xlsm` | Manter como fonte de interpretação |
| `docs/DATABASE_LOCATOR.md` | Potencialmente vivo | Pode orientar localização de banco efetivo | Revisar em fase própria antes de qualquer alteração funcional |
| `docs/DB_PATHS.md` | Potencialmente vivo | Pode orientar caminhos de banco | Revisar em fase própria antes de qualquer alteração funcional |
| `docs/changelog.md` | Registro vivo/histórico | Histórico de mudanças | Não usar como contrato operacional isolado |

## Documentos históricos ou auditoriais

| Documento/Grupo | Classe | Justificativa | Ação recomendada |
|---|---|---|---|
| `docs/checkpoints/` | Histórico/auditoria | Evidências de fases anteriores | Não reescrever salvo correção documentada |
| `docs/AUDITORIA_ROTA_MESTRE_2.md` | Auditoria histórica | Registra execução da Rota Mestre 2 | Preservar como histórico |
| `docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md` | Rota anterior | Pode conter decisões e contexto legado | Não tratar como rota atual |
| `docs/AUDITORIA_ROTA_MESTRE_3.md` | Auditoria da rota atual/recente | Contém evidências e anotações de reconciliação | Pode receber nota de supersessão se houver ambiguidade ativa |
| `docs/validacoes/` | Validações históricas | Evidências de encerramentos anteriores | Preservar como histórico |

## Artefatos gerados ou auxiliares

| Arquivo | Classe | Observação |
|---|---|---|
| `docs/mapeamento_automacao_opcoes_rtd.json` | Artefato documental gerado | Não confundir com contrato operacional atual |
| `docs/mapeamento_automacao_opcoes_rtd.md` | Artefato documental/relatório | Útil para auditoria, não é contrato funcional isolado |
| `docs/fase_2_diagnostico_csvs_rtd_excel.json` | Artefato diagnóstico | Histórico de diagnóstico |
| `docs/fase_3_diagnostico_persistencia_rtd_opcoes.json` | Artefato diagnóstico | Histórico de diagnóstico |

## Referências a LISTA_RTD.xlsx em docs não-checkpoint

```text
docs/AUDITORIA_ROTA_MESTRE_3.md:92:O dry-run com LISTA_RTD.xlsx falhou porque a aba disponível é diferente das esperadas pelos scripts:
docs/AUDITORIA_ROTA_MESTRE_3.md:241:A planilha RTD legada abolida foi removida do versionamento. A entrada `LISTA_RTD.xlsx` deixou de ser tratada como ponte RTD oficial.
docs/ROTA_MESTRE_3_RECONCILIACAO_POS_BACKUP.md:77:## Nota de supersessão — LISTA_RTD.xlsx
docs/ROTA_MESTRE_3_RECONCILIACAO_POS_BACKUP.md:81:Referências anteriores a `LISTA_RTD.xlsx` devem ser interpretadas como histórico/legado, salvo evidência funcional ativa em sentido contrário.
docs/decisions/2026-06-17-supersessao-lista-rtd-xlsx.md:1:# Decisão — Supersessão de LISTA_RTD.xlsx por LISTA_RTD.xlsm
docs/decisions/2026-06-17-supersessao-lista-rtd-xlsx.md:7:Durante a reconciliação da ponte RTD, foram encontradas referências remanescentes a `LISTA_RTD.xlsx` em documentos históricos, checkpoints, validações antigas e no mapeamento documental `docs/mapeamento_automacao_opcoes_rtd.json`.
docs/decisions/2026-06-17-supersessao-lista-rtd-xlsx.md:20:A planilha `LISTA_RTD.xlsx` fica classificada como referência legada/histórica e não deve ser usada como ponte operacional atual.
docs/decisions/2026-06-17-supersessao-lista-rtd-xlsx.md:24:Referências antigas a `LISTA_RTD.xlsx` em documentos, checkpoints, auditorias ou mapeamentos anteriores devem ser lidas como histórico do processo, salvo se uma nova evidência funcional ativa demonstrar consumo real em código de produção.
docs/decisions/2026-06-17-supersessao-lista-rtd-xlsx.md:29:- Não reintroduzir `LISTA_RTD.xlsx` como dependência operacional.
docs/decisions/2026-06-17-supersessao-lista-rtd-xlsx.md:30:- Manter `LISTA_RTD.xlsx` protegido no `.gitignore`.
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

## Referências a LISTA_RTD.xlsm em docs não-checkpoint

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
docs/ROTA_MESTRE_3_RECONCILIACAO_POS_BACKUP.md:79:A partir da reconciliação registrada em `docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md` e `docs/checkpoints/fase-2-1-classificacao-referencias-lista-rtd.md`, a ponte RTD operacional oficial é `LISTA_RTD.xlsm`.
docs/decisions/2026-06-17-supersessao-lista-rtd-xlsx.md:1:# Decisão — Supersessão de LISTA_RTD.xlsx por LISTA_RTD.xlsm
docs/decisions/2026-06-17-supersessao-lista-rtd-xlsx.md:9:Também foi confirmado que os scripts funcionais atuais usam `LISTA_RTD.xlsm` como workbook padrão:
docs/decisions/2026-06-17-supersessao-lista-rtd-xlsx.md:18:`LISTA_RTD.xlsm`
docs/decisions/2026-06-17-supersessao-lista-rtd-xlsx.md:31:- Manter `LISTA_RTD.xlsm` versionável e tratado como ponte RTD oficial.
docs/fase_2_auditoria_contrato_rtd_excel.md:20:- `LISTA_RTD.xlsm`
docs/mapeamento_automacao_opcoes_rtd.md:1255:- `LISTA_RTD.xlsm` — `outros` — score `6`
docs/validacoes/fase-17-mapa-pastas-arquivos.md:127:LISTA_RTD.xlsm
docs/validacoes/fase-17-mapa-pastas-arquivos.md:144:- `LISTA_RTD.xlsm` está versionado.
docs/validacoes/fase-17-mapa-pastas-arquivos.md:156:| `LISTA_RTD.xlsm` | Sim | Versionado |
docs/validacoes/fechamento-rota-mestre-2.md:94:- `LISTA_RTD.xlsm` foi removida do versionamento e protegida no `.gitignore`;
docs/validacoes/fechamento-rota-mestre-2.md:100:- `git diff --name-status origin/main..HEAD -- LISTA_RTD.xlsx LISTA_RTD.xlsm .gitignore`
```

## Classificação interpretativa da ponte RTD

- `LISTA_RTD.xlsm` é a ponte RTD operacional oficial.
- `LISTA_RTD.xlsx` é referência legada/histórica.
- Checkpoints e auditorias antigas não devem ser reescritos apenas para trocar nomes.
- Documentos vivos podem receber nota de supersessão quando houver risco de ambiguidade operacional.

## Documentos candidatos a nota de supersessão

| Documento | Motivo | Recomendação |
|---|---|---|
| `docs/AUDITORIA_ROTA_MESTRE_3.md` | Pode conter referência explícita a `LISTA_RTD.xlsx` durante reconciliação | Avaliar nota curta, sem reescrever histórico |
| `docs/mapeamento_automacao_opcoes_rtd.json` | Artefato gerado pode conter referência legada | Não editar diretamente sem regeneração controlada |
| `docs/mapeamento_automacao_opcoes_rtd.md` | Relatório pode conter referência legada | Avaliar nota se for usado como documento vivo |

## Resultado

Classificação preliminar registrada. A Rota Mestre 3 e a decisão de supersessão permanecem como fontes vivas de interpretação. Nenhuma alteração funcional realizada.

## Próxima ação recomendada

Avaliar inclusão de nota de supersessão apenas em documentos vivos ou semi-vivos com risco de ambiguidade, começando por `docs/AUDITORIA_ROTA_MESTRE_3.md`.
