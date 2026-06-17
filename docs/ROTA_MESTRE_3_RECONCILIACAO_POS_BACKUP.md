# ROTA_MESTRE_3 — Reconciliação pós-backup e retomada controlada

## Objetivo

Conduzir a retomada do projeto após backup/restauração com controle documental, auditoria de banco, inventário de arquivos e retomada funcional progressiva.

Esta rota existe para evitar alterações funcionais sem rastreabilidade e impedir perda acidental de arquivos críticos.

---

## Estado inicial conhecido

```text
branch: fase-12-fechamento-ciclo
commit HEAD inicial conhecido: 17a173c
estado informado: banco limpo
rtd_option_quotes: ausente em dados/app.db
structures: vazia
structure_legs: vazia
```

---

## Regras de condução

1. Nenhuma alteração funcional deve ocorrer sem fase definida.
2. Nenhuma limpeza destrutiva deve ocorrer antes do inventário.
3. Nenhuma tabela deve ser criada antes da auditoria de schema.
4. Nenhuma alteração em UI, API, repository ou serviço deve ocorrer antes do mapa de impacto.
5. Cada fase deve ter comandos, testes e resultados registrados.
6. Cada fase encerrada deve ter commit relacionado.
7. Se houver dúvida sobre histórico, consultar Git e documentação antes de alterar.
8. Bancos locais não devem ser versionados.
9. Arquivos operacionais devem ser classificados antes de exclusão.
10. O Excel permanece apenas como gateway RTD.

---

## Fases planejadas

### Fase 0 — Marco documental e congelamento da rota

Criar e versionar os documentos de controle da ROTA_MESTRE_3.

### Fase 1 — Higiene controlada do estado Git

Classificar LISTA_RTD.xlsm e _usage_audit/ antes de qualquer limpeza.

### Fase 2 — Inventário de arquivos operacionais e evidências

Mapear bancos, planilhas, CSVs, docs, diretórios ignorados e arquivos não versionados.

### Fase 3 — Auditoria da ausência de rtd_option_quotes

Confirmar schema histórico, dependências, testes e forma correta de recriação.

### Fase 4 — Reconciliação de schema

Definir se rtd_option_quotes será recriada por migração, bootstrap, script controlado ou restauração validada.

### Fase 5 — Reconciliação RTD/Excel

Validar workbook, abas disponíveis e contrato de leitura.

### Fase 6 — Retomada funcional controlada

Somente após banco, arquivos e contratos estarem reconciliados.

---

## Status atual

Fase 5 — Reconciliação RTD/Excel concluída documentalmente.

As Fases 0, 1, 2, 3, 4 e 5 possuem registros documentais relacionados no histórico do projeto.

A reconciliação avançou de forma controlada por meio de checkpoints documentais, incluindo:

- inventário e classificação de documentos vivos e históricos;
- classificação da ponte RTD operacional;
- supersessão de referências legadas a `LISTA_RTD.xlsx`;
- inventário de caminhos de banco;
- reconciliação conceitual entre `dados/app.db` e `dados/derived.db`;
- inventário funcional de consumidores de caminhos de banco;
- plano de normalização dos consumidores de caminhos de banco;
- inventário da `LISTA_RTD.xlsm`;
- mapa somente leitura das fórmulas RTD;
- consolidação da ponte RTD Excel;
- reconciliação documental entre a aba `RTD_OPTION_QUOTES` e a tabela `rtd_option_quotes`.

Último checkpoint publicado:

- `2bd5fad docs: registra reconciliacao documental RTD option quotes`

A rota ainda não autoriza alteração funcional ampla, limpeza destrutiva, alteração em UI, API, repository ou serviço sem fase específica, mapa de impacto e validação registrada.

A próxima decisão controlada deve preparar explicitamente a:

- Fase 6 — Retomada funcional controlada.

Antes da Fase 6, deve haver um plano objetivo indicando:

1. quais comandos serão executados;
2. quais arquivos poderão ser alterados;
3. se haverá ou não criação/validação de tabela;
4. quais testes serão rodados;
5. qual critério encerra a fase;
6. qual commit registrará o fechamento.

## Nota de supersessão — LISTA_RTD.xlsx

A partir da reconciliação registrada em `docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md` e `docs/checkpoints/fase-2-1-classificacao-referencias-lista-rtd.md`, a ponte RTD operacional oficial é `LISTA_RTD.xlsm`.

Referências anteriores a `LISTA_RTD.xlsx` devem ser interpretadas como histórico/legado, salvo evidência funcional ativa em sentido contrário.

A decisão formal está registrada em:

- `docs/decisions/2026-06-17-supersessao-lista-rtd-xlsx.md`
