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

Fase 4 em andamento.

As Fases 0, 1, 2 e 3 possuem registros documentais relacionados no histórico do projeto.

A reconciliação avançou de forma controlada por meio de checkpoints documentais, incluindo:

- inventário e classificação de documentos vivos e históricos;
- classificação da ponte RTD operacional;
- supersessão de referências legadas a `LISTA_RTD.xlsx`;
- inventário de caminhos de banco;
- reconciliação conceitual entre `dados/app.db` e `dados/derived.db`;
- inventário funcional de consumidores de caminhos de banco;
- plano de normalização dos consumidores de caminhos de banco.

A rota ainda não autoriza alteração funcional ampla, criação de tabela, limpeza destrutiva ou alteração em UI, API, repository ou serviço sem fase específica, mapa de impacto e validação registrada.

A próxima decisão controlada deve definir se o projeto seguirá para:

- fechamento documental da Fase 4;
- Fase 5 — Reconciliação RTD/Excel;
- ou preparação explícita de uma refatoração incremental e validada dos consumidores de caminhos de banco.

## Nota de supersessão — LISTA_RTD.xlsx

A partir da reconciliação registrada em `docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md` e `docs/checkpoints/fase-2-1-classificacao-referencias-lista-rtd.md`, a ponte RTD operacional oficial é `LISTA_RTD.xlsm`.

Referências anteriores a `LISTA_RTD.xlsx` devem ser interpretadas como histórico/legado, salvo evidência funcional ativa em sentido contrário.

A decisão formal está registrada em:

- `docs/decisions/2026-06-17-supersessao-lista-rtd-xlsx.md`
