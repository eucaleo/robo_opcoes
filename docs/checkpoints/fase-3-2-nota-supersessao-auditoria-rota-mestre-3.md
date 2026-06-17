# Fase 3.2 — Nota de supersessão na Auditoria da Rota Mestre 3

Data: 2026-06-17 10:03:00 -0300

## Objetivo

Registrar nota de supersessão em `docs/AUDITORIA_ROTA_MESTRE_3.md` para evitar ambiguidade operacional sobre `LISTA_RTD.xlsx`, sem reescrever histórico e sem alteração funcional.

## Estado Git inicial

```text
## fase-12-fechamento-ciclo...origin/fase-12-fechamento-ciclo
 M docs/AUDITORIA_ROTA_MESTRE_3.md
?? docs/checkpoints/fase-3-2-nota-supersessao-auditoria-rota-mestre-3.md
```

## Últimos commits

```text
1359c31 docs: classifica documentos vivos e historicos
3b9a132 docs: inventaria documentos vivos e historicos
0c994c4 docs: valida supersessao da ponte RTD
4cb4f50 docs: registra supersessao de LISTA_RTD xlsx
f53d74d docs: classifica referencias remanescentes LISTA_RTD
eb913ca docs: registra reconciliacao da ponte RTD oficial
6c68f37 chore: permite versionamento da ponte RTD oficial
3889e42 docs: oficializa LISTA_RTD.xlsm como ponte RTD
```

## Nota aplicada na auditoria

```text
251----
252-
253:## Nota de supersessão — LISTA_RTD.xlsx
254-
255-Esta auditoria pode conter referências históricas a `LISTA_RTD.xlsx` feitas durante a reconciliação da ponte RTD.
256-
257-A interpretação atual consolidada está definida em `docs/decisions/2026-06-17-supersessao-lista-rtd-xlsx.md`:
258-
259-- `LISTA_RTD.xlsm` é a ponte RTD operacional oficial.
260-- `LISTA_RTD.xlsx` é referência legada/histórica.
261-- Referências anteriores a `LISTA_RTD.xlsx` nesta auditoria devem ser lidas como evidência do processo de reconciliação, não como contrato operacional vigente.
```

## Diff documental

```diff
diff --git a/docs/AUDITORIA_ROTA_MESTRE_3.md b/docs/AUDITORIA_ROTA_MESTRE_3.md
index 1976f1f..996254c 100644
--- a/docs/AUDITORIA_ROTA_MESTRE_3.md
+++ b/docs/AUDITORIA_ROTA_MESTRE_3.md
@@ -247,3 +247,15 @@ Nenhuma alteração funcional foi executada.
 Nenhuma tabela foi criada.
 
 Nenhuma limpeza destrutiva adicional foi executada.
+
+---
+
+## Nota de supersessão — LISTA_RTD.xlsx
+
+Esta auditoria pode conter referências históricas a `LISTA_RTD.xlsx` feitas durante a reconciliação da ponte RTD.
+
+A interpretação atual consolidada está definida em `docs/decisions/2026-06-17-supersessao-lista-rtd-xlsx.md`:
+
+- `LISTA_RTD.xlsm` é a ponte RTD operacional oficial.
+- `LISTA_RTD.xlsx` é referência legada/histórica.
+- Referências anteriores a `LISTA_RTD.xlsx` nesta auditoria devem ser lidas como evidência do processo de reconciliação, não como contrato operacional vigente.
```

## Resultado

- `docs/AUDITORIA_ROTA_MESTRE_3.md` recebeu nota curta de supersessão.
- `LISTA_RTD.xlsm` permanece como ponte RTD operacional oficial.
- `LISTA_RTD.xlsx` permanece como referência legada/histórica.
- O histórico da auditoria não foi reescrito.
- Nenhuma alteração funcional foi realizada.

## Próxima ação recomendada

Avaliar se `docs/mapeamento_automacao_opcoes_rtd.md` deve receber nota interpretativa ou se deve permanecer apenas como artefato documental histórico.
