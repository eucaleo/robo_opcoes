# Frente de desenvolvimento: RTD Excel BTG Online

## Objetivo da frente

Adequar o sistema para operar com o Excel `LISTA_RTD.xlsm` aberto continuamente, recebendo dados RTD da corretora, enquanto o sistema Python consome os dados vivos, atualiza snapshot, histórico, UI, estruturas e gráficos.

## Escopo inicial

Esta frente deve começar por auditoria e documentação, sem alteração funcional imediata.

Primeira meta:

- Localizar tudo que já existe no sistema relacionado a RTD, Excel, BTG, CSVs, subprocessos, preenchimento de legs, snapshot, banco e atualização de UI.
- Identificar código reutilizável.
- Identificar código morto ou ruidoso.
- Planejar alterações sem duplicar arquitetura.
- Criar testes incrementais.

## Pasta de trabalho

Todos os arquivos auxiliares desta frente devem ficar em:

`FRENTE_RTD_EXCEL_BTG_ONLINE/`

Subpastas principais:

- `output/`: relatórios automáticos de auditoria.
- Documentos `.md`: plano, auditoria, decisões e checklist.

## Regra de limpeza

Ao final da frente, os arquivos auxiliares poderão ser:

- Mantidos como documentação técnica.
- Movidos para `ATT/patches` ou documentação final.
- Removidos em bloco, se forem apenas temporários.

## Critério de início

Antes de alterar código funcional:

- Revisar `output/12_arquivos_rtd_excel_encontrados.txt`.
- Revisar `output/13_grep_rtd_excel_btg.txt`.
- Revisar `output/14_grep_subprocess_rtd_excel.txt`.
- Revisar `output/20_sqlite_schema_appdb.txt`.
- Definir quais módulos existentes serão reaproveitados.
