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

Fase 6 — Retomada funcional controlada iniciada documentalmente.

A Fase 5 — Reconciliação RTD/Excel foi concluída documentalmente e a rota avançou para a Fase 6 com plano, mapa de impacto e validação controlada.

Commits principais da transição:

- `b50137a docs: atualiza status da rota mestre apos fase 5 rtd`
- `7bf3b71 docs: registra plano da fase 6 retomada funcional controlada`
- `a39a670 docs: registra checkpoint pre-fase 6 validacao RTD`
- `0788ede feat: preserva snapshot quando quote RTD estiver vencida`
- `229103c feat: adiciona pipeline operacional de refresh RTD`
- `9d78fed docs: registra validacao operacional inicial do pipeline RTD`
- `700a716 Corrige pipeline RTD wide com autobootstrap de schema`

A Fase 6.1 — Validação operacional inicial do pipeline RTD foi registrada em:

- `docs/checkpoints/fase-6-1-validacao-pipeline-rtd-operacional.md`

Após a validação inicial, houve correção técnica no pipeline RTD wide com autobootstrap de schema em:

- `700a716 Corrige pipeline RTD wide com autobootstrap de schema`

Portanto, a etapa corrente passa a ser:

- Fase 6.2 — Validação pós-correção do pipeline RTD wide/autobootstrap.

A Fase 6.2 deve validar que:

1. o pipeline RTD usa o importador wide oficial;
2. o schema `rtd_option_quotes` é validado/criado de forma controlada;
3. o Excel permanece apenas como gateway RTD;
4. não houve alteração não autorizada em UI, API, repository ou serviço;
5. os testes RTD permanecem verdes;
6. o estado Git fica limpo;
7. o fechamento da fase é registrado em checkpoint próprio.

## Nota de supersessão — LISTA_RTD.xlsx

A partir da reconciliação registrada em `docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md` e `docs/checkpoints/fase-2-1-classificacao-referencias-lista-rtd.md`, a ponte RTD operacional oficial é `LISTA_RTD.xlsm`.

Referências anteriores a `LISTA_RTD.xlsx` devem ser interpretadas como histórico/legado, salvo evidência funcional ativa em sentido contrário.

A decisão formal está registrada em:

- `docs/decisions/2026-06-17-supersessao-lista-rtd-xlsx.md`
