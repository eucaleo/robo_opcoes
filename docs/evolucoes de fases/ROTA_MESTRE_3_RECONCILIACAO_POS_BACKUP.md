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

Fase 6.2 — Validação pós-correção do pipeline RTD wide/autobootstrap concluída.

A validação pós-correção foi executada e registrada em checkpoint próprio:

- `docs/checkpoints/fase-6-2-validacao-pos-correcao-pipeline-rtd-wide.md`

Resultados registrados:

- `python -m pytest ATT/tests/test_run_rtd_option_quotes_pipeline.py ATT/tests/test_audit_rtd_option_quotes.py`
  - `16 passed in 0.43s`
- `python -m pytest ATT/tests -k "rtd_option_quotes"`
  - `19 passed, 630 deselected in 3.10s`

Commits principais da transição:

- `b50137a docs: atualiza status da rota mestre apos fase 5 rtd`
- `7bf3b71 docs: registra plano da fase 6 retomada funcional controlada`
- `a39a670 docs: registra checkpoint pre-fase 6 validacao RTD`
- `0788ede feat: preserva snapshot quando quote RTD estiver vencida`
- `229103c feat: adiciona pipeline operacional de refresh RTD`
- `9d78fed docs: registra validacao operacional inicial do pipeline RTD`
- `700a716 Corrige pipeline RTD wide com autobootstrap de schema`
- `bc5ab65 docs: registra fase 6.2 validacao pos-correcao RTD wide`
- `f1986af docs: fecha fase 6.2 validacao RTD wide`

Estado consolidado após a Fase 6.2:

1. o pipeline RTD usa o importador wide oficial;
2. o schema `rtd_option_quotes` é validado/criado de forma controlada;
3. o Excel permanece apenas como gateway RTD;
4. os testes RTD específicos permanecem verdes;
5. a branch `fase-12-fechamento-ciclo` está alinhada com `origin/fase-12-fechamento-ciclo`;
6. o fechamento foi registrado documentalmente.

Fase 6.3 — Mapa de impacto e retomada funcional incremental pós-pipeline RTD concluída documentalmente.

Checkpoint da fase:

- `docs/checkpoints/fase-6-3-mapa-impacto-retomada-funcional-rtd.md`

Commit de inventário:

- `74d1858 docs: registra inventario fase 6.3 RTD`

Resultado consolidado da Fase 6.3:

1. consumidor funcional principal identificado em `services/canonical_pricing_facade.py`;
2. camada de leitura identificada em `repositories/rtd_option_quotes_repository.py`;
3. pipeline/importação/auditoria RTD mantidos como área operacional controlada;
4. scripts legados ou auxiliares congelados até decisão explícita;
5. evidências de testes registradas em `docs/checkpoints/evidencias/`;
6. próxima fase definida.

Fase 6.4 — Proteção do contrato de leitura RTD para canonical pricing concluída.

A Fase 6.4 foi integrada à branch `fase-12-fechamento-ciclo` após validação pós-merge.

Checkpoint da fase:

- `docs/checkpoints/fase-6-4-contrato-leitura-rtd-canonical-pricing.md`

Commits principais da fase:

- `95d9a56 docs: inicia fase 6.4 contrato RTD canonical pricing`
- `7c5d54d test: protege contrato publico RtdOptionQuotesRepository`
- `c98d6d2 merge: integra fase 6.4 contrato RTD canonical pricing`

Evidências pós-merge registradas:

- `docs/checkpoints/evidencias/fase-6-4-pytest-rtd-option-quotes-pos-merge.txt`

Validações pós-merge executadas:

- `python -m pytest ATT/tests/test_rtd_option_quotes_repository_contract.py`
  - `6 passed in 0.36s`
- `python -m pytest ATT/tests -k "rtd_option_quotes"`
  - `25 passed, 630 deselected in 3.19s`
- `python -m pytest ATT/tests/test_canonical_pricing_facade_rtd_price_resolution.py ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py`
  - `22 passed in 1.24s`
- `python -m pytest ATT/tests -k "rtd_option_quotes" | tee docs/checkpoints/evidencias/fase-6-4-pytest-rtd-option-quotes-pos-merge.txt`
  - `25 passed, 630 deselected in 3.06s`

Resultado consolidado da Fase 6.4:

1. contrato público de `repositories/rtd_option_quotes_repository.py` protegido por testes diretos;
2. leitura por código, listagem e consulta por ativo-base validada;
3. comportamento em ausência da tabela `rtd_option_quotes` coberto por teste;
4. suíte RTD específica permaneceu verde após o merge;
5. testes de canonical pricing relacionados à resolução de preço RTD permaneceram verdes;
6. evidência pós-merge foi registrada em `docs/checkpoints/evidencias/`;
7. nenhuma alteração em UI/API foi realizada;
8. Excel permanece apenas como gateway RTD.

Fase 6.5 — Retomada funcional incremental pós-proteção do contrato RTD concluída documentalmente.

Checkpoint da fase:

- `docs/checkpoints/fase-6-5-retomada-funcional-incremental-rtd.md`

Evidência complementar:

- `EVIDENCIAS_FASE_6_5_RTD.md`

Commits principais da fase:

- `3886870 docs: registra checkpoint fase 6.5 fallback rtd invalido`
- `1105e61 docs: registra baseline matriz rtd canonical fase 6.5`
- `afbce51 test: cobre fallback integrado quando quote rtd esta stale`
- `82c75c7 test: cover RTD asset mismatch fallback in pricing execution`
- `58889f1 docs: add RTD asset mismatch fallback evidence`
- `fe570fc docs: organize RTD evidence heading`
- `c5a65f8 docs: registra checkpoint fase 6.5 RTD`
- `ff9e6e2 docs: consolida checkpoint fase 6.5 RTD`

Resultado consolidado da Fase 6.5:

1. cobertura integrada ampliada em `CanonicalPricingFacade.execute_pricing`;
2. fallback para snapshot protegido quando a quote RTD possui preço inválido;
3. fallback para snapshot protegido quando a quote RTD está stale;
4. fallback para snapshot protegido quando a quote RTD possui ativo-base divergente do underlying esperado;
5. metadados RTD preservados no payload do engine e no payload persistido;
6. testes RTD/canonical pricing relacionados permaneceram verdes;
7. nenhuma alteração em UI/API foi realizada;
8. Excel permanece apenas como gateway RTD.

Etapa corrente:

- Próxima microfatia da Fase 6 — retomada funcional controlada após consolidação dos fallbacks RTD no canonical pricing.

## Nota de supersessão — LISTA_RTD.xlsx

A partir da reconciliação registrada em `docs/checkpoints/fase-2-rota-mestre-3-reconciliacao-ponte-rtd.md` e `docs/checkpoints/fase-2-1-classificacao-referencias-lista-rtd.md`, a ponte RTD operacional oficial é `LISTA_RTD.xlsm`.

Referências anteriores a `LISTA_RTD.xlsx` devem ser interpretadas como histórico/legado, salvo evidência funcional ativa em sentido contrário.

A decisão formal está registrada em:

- `docs/decisions/2026-06-17-supersessao-lista-rtd-xlsx.md`

## Microfatia — Diagnóstico neutro para preço manual

Commit:

- `852d9be test: valida diagnostico neutro em preco manual`

Objetivo:

- Garantir que preço manual explícito seja preservado no canonical pricing sem consulta ao RTD.

Contrato validado:

1. `price` e `premium` preservam o valor manual.
2. `price_source` permanece como `manual`.
3. `price_resolution_status` permanece `ok`.
4. `rtd_quote_found` permanece `None`.
5. `rtd_validation_status` permanece `not_applicable`.
6. `rtd_validation_message` informa que o RTD não foi consultado.
7. Metadados concretos da quote RTD não vazam para a perna manual.
8. O repositório RTD não é chamado.

Evidência:

- `docs/checkpoints/evidencias/fase-6-6-pytest-metadados-rtd-canonical-manual-price.txt`

---

## Atualização pós-restauração documental — Fases 6.7 a 6.10

Esta seção foi adicionada na Fase 6.10 para sincronizar a ROTA_MESTRE_3 restaurada com o estado real da linha principal após as Fases 6.7, 6.8 e 6.9.

A restauração documental foi necessária porque os arquivos principais da rota não estavam presentes no working tree atual da main, embora existissem no histórico Git.

Arquivos restaurados:

- docs/ROTA_MESTRE_3_RECONCILIACAO_POS_BACKUP.md
- docs/AUDITORIA_ROTA_MESTRE_3.md

Commit de restauração:

- 1a20cea docs: restaura rota mestre 3 e auditoria

Base atual da main antes da restauração:

- dddbec8 merge: integra fase 6.9 ajuste rtd canonical pricing

---

### Fase 6.7 — Consolidação de diagnóstico RTD/canonical pricing

Status: concluída documentalmente.

Checkpoint:

- docs/checkpoints/fase-6-7-consolidacao-diagnostico-rtd-canonical.md

Evidências:

- docs/checkpoints/evidencias/fase-6-7-inventario-diagnostico-rtd-canonical.txt
- docs/checkpoints/evidencias/fase-6-7-pytest-baseline-canonical-rtd.txt
- docs/checkpoints/evidencias/fase-6-7-pytest-baseline-rtd-option-quotes.txt
- docs/checkpoints/evidencias/fase-6-7-recorte-funcional-rtd-canonical.txt

Commit principal:

- 4960ca0 docs: consolidate fase 6.7 rtd canonical diagnostics

Resultado consolidado:

1. foi registrado inventário de diagnóstico do caminho RTD/canonical pricing;
2. foi preservado recorte funcional controlado para retomada incremental;
3. foram registradas evidências de baseline dos testes RTD e canonical;
4. nenhuma alteração funcional destrutiva foi executada;
5. a fase serviu como consolidação documental para orientar os guardrails posteriores.

---

### Fase 6.8 — Guardrail da matriz de diagnóstico RTD/canonical pricing

Status: concluída e integrada.

Checkpoint:

- docs/checkpoints/fase-6-8-guardrail-matriz-diagnostico-rtd.md

Evidência:

- docs/checkpoints/evidencias/fase-6-8-pytest-guardrail-matriz-diagnostico-rtd.txt

Commits relacionados:

- b2ad0b3 test: add guardrail matriz diagnostico rtd canonical
- 4cb1b7b merge: integra fase 6.8 guardrail matriz diagnostico rtd canonical

Resultado consolidado:

1. foi adicionado guardrail automatizado para a matriz de diagnóstico RTD/canonical;
2. a cobertura de ATT/tests/test_canonical_pricing_facade.py foi ampliada;
3. o comportamento esperado do diagnóstico RTD foi protegido por teste;
4. a fase foi integrada à linha principal por merge controlado;
5. não houve alteração de UI/API;
6. o Excel permaneceu apenas como gateway RTD.

---

### Fase 6.9 — Ajuste de parsing numérico RTD no canonical pricing

Status: concluída, integrada e etiquetada.

Checkpoint:

- docs/checkpoints/fase-6-9-ajuste-rtd-canonical-pricing.md

Evidências:

- docs/checkpoints/evidencias/fase-6-9-pytest-canonical-pricing-rtd-number-formats.txt
- docs/checkpoints/evidencias/fase-6-9-pytest-pricing-execution-services.txt

Commits relacionados:

- beba13f fix: robust rtd canonical pricing number parsing
- dddbec8 merge: integra fase 6.9 ajuste rtd canonical pricing

Tag relacionada:

- fase-6-9-rtd-canonical-pricing

Arquivos principais alterados na fase:

- services/canonical_pricing_facade.py
- ATT/tests/test_canonical_pricing_facade.py
- docs/checkpoints/fase-6-9-ajuste-rtd-canonical-pricing.md
- docs/checkpoints/evidencias/fase-6-9-pytest-canonical-pricing-rtd-number-formats.txt
- docs/checkpoints/evidencias/fase-6-9-pytest-pricing-execution-services.txt

Resultado consolidado:

1. o parsing numérico de preços RTD no canonical pricing foi tornado mais robusto;
2. formatos numéricos adicionais foram cobertos por testes;
3. os serviços de execução de pricing permaneceram validados;
4. a fase foi integrada à main;
5. a tag fase-6-9-rtd-canonical-pricing foi registrada no ponto de integração;
6. não houve alteração de UI/API;
7. o Excel permaneceu apenas como gateway RTD.

---

### Fase 6.10 — Restauração e sincronização documental da ROTA_MESTRE_3

Status: em encerramento documental.

Objetivo:

- restaurar os documentos principais da ROTA_MESTRE_3 a partir do histórico Git;
- confirmar que os arquivos restaurados existem e possuem conteúdo válido;
- sincronizar o estado documental com as Fases 6.7, 6.8 e 6.9 já integradas à main;
- registrar a própria restauração como fase rastreável.

Branch de trabalho:

- fase-6-10-restaura-documentacao-rota-mestre-3

Commit de restauração:

- 1a20cea docs: restaura rota mestre 3 e auditoria

Comandos principais executados:

    git checkout main
    git pull --ff-only origin main
    git checkout -b fase-6-10-restaura-documentacao-rota-mestre-3
    git ls-tree -r --name-only 8a56969 docs | grep -E "ROTA_MESTRE_3|AUDITORIA_ROTA_MESTRE_3"
    git show 8a56969:docs/ROTA_MESTRE_3_RECONCILIACAO_POS_BACKUP.md | sed -n '1,120p'
    git show 8a56969:docs/AUDITORIA_ROTA_MESTRE_3.md | sed -n '1,160p'
    git checkout 8a56969 -- docs/ROTA_MESTRE_3_RECONCILIACAO_POS_BACKUP.md docs/AUDITORIA_ROTA_MESTRE_3.md
    git status --short
    git diff --check
    git add docs/ROTA_MESTRE_3_RECONCILIACAO_POS_BACKUP.md docs/AUDITORIA_ROTA_MESTRE_3.md
    git commit -m "docs: restaura rota mestre 3 e auditoria"

Resultado observado:

1. os documentos foram encontrados no commit histórico 8a56969;
2. ambos foram restaurados no working tree atual;
3. git diff --check não reportou problemas;
4. a restauração foi registrada no commit 1a20cea;
5. após o commit, o working tree ficou limpo;
6. erros posteriores no terminal foram causados por colagem acidental de prompt e saída como comando e não alteraram o estado Git.

Estado consolidado após a Fase 6.10:

1. a documentação mestre voltou a existir na linha atual de trabalho;
2. a rota foi sincronizada com as Fases 6.7, 6.8 e 6.9;
3. a continuidade documental foi restabelecida;
4. nenhuma alteração funcional foi realizada nesta fase;
5. nenhuma alteração de banco foi realizada;
6. nenhuma alteração de UI/API foi realizada;
7. a próxima etapa somente deve avançar após validação e integração desta sincronização documental.
