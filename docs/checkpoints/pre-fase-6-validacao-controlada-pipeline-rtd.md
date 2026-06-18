# Checkpoint - Pre-Fase 6: validacao controlada do pipeline RTD

## Contexto

Este checkpoint registra evolucao tecnica apos a conclusao documental da Fase 5 da ROTA_MESTRE_3.
O registro nao inicia formalmente a Fase 6 e nao autoriza alteracao funcional ampla.
O objetivo e evitar refazimentos e preservar rastreabilidade antes da retomada funcional controlada.

## Referencia

- Documento-base: ROTA_MESTRE_3_RECONCILIACAO_POS_BACKUP.md
- Status anterior: Fase 5 concluida documentalmente.
- Ultimo checkpoint conhecido: 2bd5fad docs: registra reconciliacao documental RTD option quotes

## Evolucao registrada

Foi validado de forma controlada o pipeline:

```text
rtd_option_quotes -> rtd_symbols.txt -> LISTA_RTD.xlsm -> RTD_LINKS.csv -> rtd_option_quotes
```

Resultados observados:

- modo strict bloqueou corretamente sem structure_legs;
- modo fallback usou rtd_option_quotes como fonte de simbolos;
- Excel/RTD gerou dados/RTD_LINKS.csv;
- importador atualizou 4 registros em rtd_option_quotes;
- updated_at avancou para 2026-06-17 22:11:23;
- structures e structure_legs permaneceram vazias;
- falha do Excel ao alterar Calculation foi tratada como aviso nao bloqueante;
- bloco param(...) foi preservado como primeiro bloco real do PowerShell.

## Arquivos envolvidos

Arquivos operacionais usados:

- LISTA_RTD.xlsm
- dados/rtd_symbols.txt
- dados/RTD_LINKS.csv
- dados/app.db

Scripts envolvidos:

- scripts/run_rtd_refresh_full.py
- scripts/build_rtd_symbols.py
- scripts/refresh_rtd_option_quotes_excel.ps1
- scripts/import_rtd_option_quotes_wide_csv.py

Arquivo alterado:

- scripts/refresh_rtd_option_quotes_excel.ps1

Backups locais observados:

- scripts/refresh_rtd_option_quotes_excel.ps1.bak
- scripts/refresh_rtd_option_quotes_excel.ps1.fix-param.bak

Esses backups locais nao devem ser removidos por limpeza destrutiva automatica.

## Limites

Este checkpoint nao autoriza:

- alteracao funcional ampla;
- limpeza destrutiva;
- alteracao em UI;
- alteracao em API;
- alteracao em repository;
- alteracao em servico;
- uso de strict como fluxo produtivo enquanto structure_legs estiver vazia.

## Proxima decisao controlada

Antes da Fase 6 deve haver plano objetivo indicando:

1. quais comandos serao executados;
2. quais arquivos poderao ser alterados;
3. se havera ou nao criacao ou validacao de tabela;
4. quais testes serao rodados;
5. qual criterio encerra a fase;
6. qual commit registrara o fechamento.

## Conclusao

A validacao controlada demonstrou que a ponte RTD operacional esta funcional em modo fallback.
O modo strict tambem foi validado negativamente, bloqueando com seguranca sem structure_legs.
Este checkpoint deve ser usado como base documental para evitar refazimentos na preparacao da Fase 6.

<!-- CHECKPOINT_COMPLETO_VALIDACAO_RTD_PRE_FASE_6 -->
