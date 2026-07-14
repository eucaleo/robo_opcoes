# Auditoria Técnica - BD Único AppDB

Data: 2026-07-10 13:12:34  
Branch: refactor/bd-unico-appdb  
Commit auditado: eab23c8  

## Objetivo

Registrar o encerramento técnico da frente de consolidação do banco único `dados/app.db`, removendo dependências produtivas de bancos legados e preparando a base para continuidade da frente RTD Excel BTG Online.

## Escopo validado

- Uso produtivo concentrado no banco canônico `dados/app.db`.
- Ausência de referência produtiva a `app2.db`.
- Ausência de fallback físico para banco legado.
- Ausência de varredura produtiva por bancos SQLite via glob ou rglob.
- Snapshot RTD centralizado no `app.db`.
- Editor de estruturas usando `db_path` do fluxo atual.
- UI sem subprocesso RTD para preenchimento de leg.
- Limpeza textual de resíduos relacionados a bancos legados.

## Commits recentes

eab23c8 chore: limpar residuos textuais de bancos legados
a269d5a refactor: limitar snapshots do details panel ao app db canonico
96d3cf2 fix: evitar sombra de metodo app_db_path no details panel
f572091 refactor: usar db_path do dialogo no fluxo RTD
9477a1a refactor: remove sincronizacao RTD Excel da UI
4581c95 refactor: formaliza snapshot RTD centralizado
12601f8 refactor: remove subprocess RTD operacional do editor de estrutura
d3979cd docs: registra auditoria de fechamento da fase 1 RTD Excel
5af5813 docs: registra auditoria de retorno ao roteiro RTD Excel
647360d refactor: conclui centralizacao COM operacional RTD Excel

## Auditoria textual

### Busca por bancos legados físicos

Resultado:

Sem resíduos encontrados.

### Busca por app2

Resultado:

Sem referências encontradas.

## Testes executados

### Contratos BD único

.................                                                        [100%]
17 passed in 2.63s

### Fluxo RTD, editor, snapshots e enrichment

...............................................                          [100%]
47 passed in 1.63s

## Conclusão

A frente `bd-unico-appdb` está tecnicamente encerrada para fins de integração.

Estado validado:

- Banco produtivo canônico: `dados/app.db`.
- Sem dependência produtiva de `app2.db`.
- Sem fallback físico para banco legado.
- Sem busca produtiva por bancos SQLite alternativos.
- Testes contratuais e funcionais do escopo executados.

## Próxima frente recomendada

Continuar a rota RTD Excel BTG Online pela implementação controlada da Fase 1:

1. detectar Excel aberto;
2. detectar workbook `LISTA_RTD.xlsm`;
3. validar aba `RTD_OPTION_QUOTES`;
4. mapear cabeçalhos pela linha 1;
5. validar campos obrigatórios;
6. criar status claro de conexão RTD/Excel na UI;
7. somente depois iniciar coletor online contínuo.

