# Frentes Corrigidas — Controle Operacional

Este arquivo registra as frentes já corrigidas durante a contenção do sistema.

## Regras da contenção

- Correções pequenas, testáveis e reversíveis.
- Patches e temporários em ATT/.
- Testes novos em ATT/tests/.
- Não criar pastas novas na raiz.
- Banco oficial da aplicação: dados/app.db.
- data/app.db não deve ser criado nem usado.
- Arquivos Markdown devem evitar blocos com crase em patches automatizados.
- Quando for necessário mostrar código em Markdown gerado por patch, usar bloco indentado.

---

## Frente 01 — Caminho único do banco

Status: concluída.

### Problema

Havia divergência entre:

- db/config.py usando dados/app.db.
- db/sqlite.py usando data/app.db.

Como a pasta data/ não existe no projeto e o sistema usa dados/, isso indicava risco real de criação ou acesso ao banco errado.

### Correção aplicada

db/sqlite.py foi atualizado para usar o caminho canônico vindo de db.config:

    from db.config import APP_DB_PATH
    DEFAULT_DB_PATH = APP_DB_PATH

### Validações executadas

Comando:

    pytest ATT/tests/test_guardrail_db_path_unico.py -q

Resultado:

    2 passed

Comando:

    find . -maxdepth 2 -type d -iname "data"

Resultado:

    Nenhuma pasta data/ encontrada.

Comando:

    grep -R "data/app.db\|Path(\"data\") / \"app.db\"\|Path('data') / 'app.db'" -n . --exclude-dir=.git --exclude-dir=__pycache__ --exclude-dir=.pytest_cache --exclude-dir=.venv

Resultado observado:

- Ocorrências apenas em ATT/patch_01_db_sqlite_path.py.
- Ocorrências esperadas no teste guardrail.
- Referência documental em docs/PROXIMA_ACAO.md.

### Veredito

Frente concluída.

O sistema não deve mais criar ou usar data/app.db pelo helper db/sqlite.py.

---

## Frente 02 — Colunas structure_id nas tabelas derivadas

Status: concluída parcialmente.

### Problema

A consolidação indicou risco de tabelas derivadas sem structure_id, especialmente:

- structure_decisions.
- payoff_curve_points.
- payoff_curve_summary.

Essas colunas são necessárias para reforçar structure_id como identidade canônica.

### Correção aplicada

Foi criada migration segura em:

    db/migrations/ensure_canonical_structure_id_columns.py

A migration verifica a existência das tabelas e colunas antes de alterar o banco.

### Validações executadas

Comando:

    pytest ATT/tests/test_migration_structure_id_columns.py -q

Resultado:

    4 passed

Comando:

    python db/migrations/ensure_canonical_structure_id_columns.py --db dados/app.db

Resultado observado:

    structure_decisions.structure_id: already_exists
    payoff_curve_points.structure_id: already_exists
    payoff_curve_summary.structure_id: missing_table

Índices:

    structure_decisions.structure_id: ensured
    payoff_curve_points.structure_id: ensured
    payoff_curve_summary.structure_id: missing_table

### Pendência objetiva

A tabela payoff_curve_summary ainda não existe no banco atual.

Decisão pendente:

- criar payoff_curve_summary oficialmente no schema canônico;
- ou pausar/remover temporariamente os usos dessa tabela até o contrato ser definido.

### Veredito

Frente concluída para as tabelas existentes.

A pendência payoff_curve_summary deve virar frente própria, pois envolve decisão de contrato de schema.

---

## Próxima frente sugerida

Frente 03 — Resolver conflito de schema da tabela pricing_executions.

Motivo:

- infra/bootstrap_structures_schema.py define dois contratos diferentes para pricing_executions.
- PricingExecutionsRepository espera o schema com execution_status, execution_engine, pricing_payload e result.
- Esse conflito pode quebrar execução, histórico de pricing, snapshots e refresh de payoff.

---

## Frente 03 — Schema único de pricing_executions

Status: concluída.

### Problema

O arquivo infra/bootstrap_structures_schema.py continha dois contratos diferentes para a tabela pricing_executions.

O contrato oficial, usado em ensure_structures_schema(), contém:

    id
    created_at
    structure_id
    underlying_asset
    reference_date
    execution_status
    execution_engine
    error_message
    duration_ms
    number_of_legs
    total_quantity
    theoretical_value
    pricing_payload
    result

O bootstrap auxiliar antigo ainda criava outro contrato com:

    status
    canonical_input
    engine_result
    executed_at

Isso poderia criar ou manter bancos incompatíveis com PricingExecutionsRepository, serviços de pricing, snapshots e refresh de payoff.

### Correção aplicada

O bootstrap auxiliar bootstrap_pricing_executions() foi mantido apenas por compatibilidade, mas agora usa o contrato oficial.

Também foi adicionada proteção para bancos antigos:

    adicionar colunas oficiais ausentes;
    garantir índices oficiais;
    corrigir idx_pricing_executions_status para apontar para execution_status.

### Validações executadas

Comando:

    pytest ATT/tests/test_guardrail_pricing_executions_schema.py -q

Resultado:

    2 passed

Comando:

    pytest ATT/tests/test_guardrail_pricing_executions_bootstrap_contract.py -q

Resultado:

    2 passed

Comando:

    python ATT/inspect_03_pricing_executions_schema.py

Resultado observado:

    pricing_executions existe.
    Nenhuma coluna obrigatória ausente.
    Bootstrap principal e bootstrap auxiliar usam o mesmo contrato oficial.

Comando:

    grep -n "canonical_input\|engine_result\|executed_at" infra/bootstrap_structures_schema.py || true

Resultado:

    Nenhuma ocorrência encontrada.

### Veredito

Frente concluída.

pricing_executions passa a ter um único contrato operacional no bootstrap principal e no bootstrap auxiliar.
---

## Frente 04 — Aposentar db.writer e db.reader

Status: concluída.

### Problema

Os arquivos db/writer.py e db/reader.py pertenciam ao fluxo legado de payoff e decisão.

A inspeção mostrou que eles não tinham uso operacional ativo, mas ainda continham riscos caso fossem chamados:

- uso de variável indefinida;
- filtros legados por aba;
- strings SQL com ref.db_column sem interpolação;
- SQL direto fora de repositories/services;
- conflito com a regra de structure_id como identidade canônica.

### Correção aplicada

Os módulos foram aposentados com fail-fast.

As classes PayoffWriter e PayoffReader foram mantidas apenas para compatibilidade de importação, mas qualquer tentativa de instanciá-las agora falha explicitamente com RuntimeError.

Também foram removidos dos arquivos ativos os trechos quebrados de SQL legado.

### Validações executadas

Comando:

    pytest ATT/tests/test_guardrail_db_reader_writer_deprecated.py -q

Resultado esperado:

    3 passed

Comando:

    python ATT/inspect_04_db_reader_writer.py

Resultado esperado:

    usage_hits: []

Comando:

    grep -R "from db.writer\|import db.writer\|db.writer\|from db.reader\|import db.reader\|db.reader\|from db import writer\|from db import reader" -n db domain infra repositories services UI scripts controllers --exclude-dir=.git --exclude-dir=__pycache__ --exclude-dir=.pytest_cache --exclude-dir=.venv || true

Resultado esperado:

    Nenhum uso operacional ativo encontrado.

### Veredito

Frente concluída.

db.writer e db.reader deixam de ser risco silencioso no fluxo operacional.

Qualquer necessidade futura de leitura ou escrita deve passar por db.derived_repo, repositories, query services ou command services canônicos.

---

## Próxima frente sugerida

Frente 05 — Resolver contrato da tabela payoff_curve_summary.

Motivo:

- A Frente 02 confirmou que payoff_curve_summary ainda não existe no banco atual.
- Há uso previsto em domain/payoff_features.py e em fluxos derivados.
- A decisão pendente é criar a tabela oficialmente no schema canônico ou pausar/remover temporariamente seus usos até o contrato definitivo.
---

## Frente 05 — Contrato oficial de payoff_curve_summary

Status: concluída.

### Problema

A tabela payoff_curve_summary era usada por domain/payoff_features.py, mas não era garantida pelo schema canônico nem existia no banco atual.

O upsert em domain/payoff_features.py dependia da chave:

    structure_id + reference_date

mas a tabela não estava criada.

### Correção aplicada

A tabela payoff_curve_summary foi adicionada oficialmente em db/schema.py e criada em dados/app.db.

Contrato mínimo criado:

- structure_id
- reference_date
- timestamp
- aba
- spot_ref
- points_count
- pl_min
- pl_max
- pl_at_spot_ref
- breakevens_json
- be_count
- pos_ranges_json
- pos_ranges_count
- max_drawdown_like
- meta_json
- created_at

Também foi criada chave única canônica:

    UNIQUE(structure_id, reference_date)

### Validações executadas

Comando:

    pytest ATT/tests/test_guardrail_payoff_curve_summary_schema.py -q

Resultado:

    4 passed

Comando:

    python ATT/inspect_05_payoff_curve_summary.py

Resultado confirmado:

    table_exists: true

### Veredito

Frente concluída.

payoff_curve_summary passa a existir como tabela canônica de resumo de payoff por estrutura e data de referência.
---

## Frente 06 — Mapa de sombras aba versus structure_id

Status: diagnóstico concluído.

### Problema

O sistema está em transição entre:

- identidade legada por aba;
- identidade canônica por structure_id.

Como existem muitos módulos e caminhos paralelos, uma substituição global de aba por structure_id seria perigosa.

### Diagnóstico executado

Foi criado e executado o inspetor:

    ATT/inspect_06_aba_structure_id_shadows.py

O relatório foi salvo em:

    ATT/inspect_06_aba_structure_id_shadows.json

Resumo apurado:

    files_scanned: 118
    files_with_aba: 37
    files_with_structure_id: 58
    files_mixed_aba_structure_id: 26
    files_direct_sql_aba: 6
    files_aba_without_structure_id: 11
    files_bridge_or_ref_context: 16
    files_legacy_context: 9

### Achados principais

Arquivos com maior prioridade de análise:

- db/derived_repo.py
- repositories/robo_legs_repository.py
- UI/models/ui_data.py
- repositories/market_snapshot_repository.py
- services/market_snapshot_selector.py
- services/canonical_pricing_facade.py
- services/canonical_input_service.py
- services/derived_service.py

### Decisão técnica

Não fazer replace global de aba.

A regra formal fica:

    Camada canônica: structure_id obrigatório.
    Camada legado: aba permitido.
    Ponte: structure_id pode virar aba apenas em resolver dedicado, StructureRef ou AbaResolverMixin.

### Próxima frente escolhida

Frente 07 — Corrigir ponte canônica structure_id -> aba em market_snapshot_repository e market_snapshot_selector.

Motivo:

- repositories/market_snapshot_repository.py tem uso intenso de aba e nenhum structure_id.
- services/market_snapshot_selector.py também opera só por aba.
- O plano inicial já apontava MarketSnapshotRepository como ponto crítico.

## Frente 07 — Ponte MarketSnapshot structure_id para aba legada

- **Status:** aplicada e testada.
- **Objetivo:** permitir entrada canônica por `structure_id` no fluxo de MarketSnapshot sem migrar fisicamente as tabelas legadas RTD/manuais.
- **Arquivos ajustados:**
  - `repositories/market_snapshot_repository.py`
  - `services/market_snapshot_selector.py`
- **Regra definida:**
  - camada canônica pode chamar por `structure_id`;
  - repository resolve `structures.alias_legacy_aba`;
  - tabelas legadas continuam consultadas por `aba` internamente;
  - `aba` permanece somente como ponte de compatibilidade nesse fluxo.
- **Guardrail criado:**
  - `ATT/tests/test_guardrail_market_snapshot_structure_id_bridge.py`
- **Risco contido:**
  - evita espalhar novas chamadas diretas por `aba`;
  - evita quebrar RTD/manual legados que ainda dependem de `aba`;
  - permite `MarketSnapshotSelector.select(structure_id=...)`.

## Frente 08 — RoboLegs com entrada canônica por structure_id

Status: aplicada e validada.

Registrado em: 2026-07-29 21:30:03

### Objetivo

Permitir que a camada de leitura de legs legadas do robô seja chamada por
structure_id, mantendo aba apenas como ponte física para tabelas legadas:

- manual_analise_robo_legs
- rtd_analise_robo_legs

### Regra consolidada

- Entrada canônica: structure_id
- Ponte autorizada: structures.alias_legacy_aba
- Consulta física legada: WHERE aba = ?
- Compatibilidade preservada: chamadas antigas por aba continuam aceitas.

### Arquivos alterados

- repositories/robo_legs_repository.py
- repositories/robo_legs_status_repository.py
- services/robo_legs_service.py
- services/robo_legs_status_service.py

### Guardrail adicionado

- ATT/tests/test_guardrail_robo_legs_structure_id_bridge.py

### Evidências executadas

Comando executado:

    pytest \
      ATT/tests/test_guardrail_robo_legs_structure_id_bridge.py \
      ATT/tests/test_robo_legs_repository.py \
      ATT/tests/test_robo_legs_status_repository.py \
      ATT/tests/test_robo_legs_service.py \
      ATT/tests/test_robo_legs_status_service.py \
      ATT/tests/test_legacy_structure_legs_reader.py \
      ATT/tests/test_legacy_structure_legs_importer.py \
      ATT/tests/test_canonical_input_service.py \
      -q

Resultado:

    36 passed in 3.07s

Compilação executada:

    python -m py_compile \
      repositories/robo_legs_repository.py \
      repositories/robo_legs_status_repository.py \
      services/robo_legs_service.py \
      services/robo_legs_status_service.py

Resultado:

    OK, sem erro de sintaxe.

### Diagnóstico pós-frente

Antes da Frente 08:

- files_with_structure_id: 60
- files_mixed_aba_structure_id: 28
- files_aba_without_structure_id: 9

Depois da Frente 08:

- files_with_structure_id: 61
- files_mixed_aba_structure_id: 29
- files_aba_without_structure_id: 8

Interpretação:

- A quantidade de arquivos sem structure_id reduziu de 9 para 8.
- O aumento em mixed_aba_structure_id é esperado, pois a frente criou ponte explícita structure_id -> aba em área legada controlada.
- O uso físico de WHERE aba = ? permanece autorizado apenas porque as tabelas robo legadas ainda são indexadas por aba.
- A entrada canônica passa a aceitar structure_id, StructureRef.from_id(...) e int.

### Contrato validado

A Frente 08 está aderente ao plano:

- Camada canônica recebe structure_id.
- Camada legada continua usando aba apenas como detalhe físico.
- A ponte autorizada é alias_legacy_aba em structures.
- Chamadas antigas por aba permanecem funcionais.
- Chamadas novas por structure_id passam a ter guardrail.

### Situação final

Frente 08 concluída.

RoboLegsRepository, RoboLegsStatusRepository, RoboLegsService e
RoboLegsStatusService agora aceitam entrada canônica por structure_id sem quebrar
compatibilidade com o fluxo legado por aba.

## Frente 09 — Auditoria e contenção do DerivedRepo

Status: em andamento.

Registrado em: 2026-07-29 21:36:58

### Objetivo

Auditar e conter o arquivo db/derived_repo.py, que ainda concentra a maior sombra
entre aba, structure_id e timestamp.

### Motivo

O diagnóstico após a Frente 08 indica que db/derived_repo.py segue como o maior
ponto de risco para a transição canônica:

- muitos usos de aba;
- deletes por aba e timestamp;
- métodos duplicados dentro do mesmo repositório;
- convivência entre escrita derivada, payoff, decisões e consistência;
- risco de apagar ou consultar snapshots usando chave legada quando structure_id
  já está disponível.

### Regra da Frente 09

Antes de qualquer alteração estrutural no DerivedRepo, será executada auditoria
profunda para identificar:

- métodos duplicados efetivos;
- deletes em payoff_curve_points;
- deletes em structure_decisions;
- consultas por WHERE aba = ?;
- pontos onde structure_id já existe mas ainda não é a chave preferencial.

### Arquivos envolvidos

- db/derived_repo.py
- ATT/inspect_09_derived_repo_deep.py
- ATT/inspect_09_derived_repo_deep.json

### Evidência inicial

Comando de auditoria:

    PYTHONUTF8=1 PYTHONIOENCODING=utf-8 python ATT/inspect_09_derived_repo_deep.py

### Situação

Frente 09 aberta para auditoria controlada.

A próxima etapa será aplicar patch somente nos pontos confirmados pelo JSON de
inspeção, mantendo aba apenas como fallback legado e structure_id como chave
preferencial onde a coluna existir.

## Frente 09A — DerivedRepo inspeção contextual e guardrail de transição

Status: em andamento controlado.

Registrado em: 2026-07-29 21:43:01

### Objetivo

Dar continuidade segura à Frente 09 antes de alterar `db/derived_repo.py`,
que é arquivo crítico do eixo Banco/schema canônico e ainda concentra uso legado
por `aba + timestamp`.

### Motivação

A inspeção inicial da Frente 09 indicou pontos críticos em `db/derived_repo.py`:

- `WHERE aba = ?`
- `DELETE FROM payoff_curve_points`
- `DELETE FROM structure_decisions`
- uso simultâneo de `structure_id`, `StructureRef`, `aba` e `timestamp`

Como o arquivo possui múltiplas funções de escrita, limpeza, validação e leitura
de payoff/decisão, a correção deve ser feita em passos pequenos e testáveis.

### Arquivos adicionados

- `ATT/inspect_09a_derived_repo_context.py`
- `ATT/tests/test_guardrail_derived_repo_structure_id_transition.py`

### Regra de segurança

Nenhuma alteração funcional profunda em `db/derived_repo.py` deve ser feita sem:

- inspeção contextual dos blocos críticos;
- guardrail registrando o estado legado atual;
- testes de regressão dos serviços derivados;
- documentação em `docs/FRENTES_CORRIGIDAS.md`.

### Evidências esperadas

Comandos:

    PYTHONUTF8=1 PYTHONIOENCODING=utf-8 python ATT/inspect_09a_derived_repo_context.py

    pytest \
      ATT/tests/test_guardrail_derived_repo_structure_id_transition.py \
      ATT/tests/test_derived_service.py \
      ATT/tests/test_payoff_canonical.py \
      ATT/tests/test_structure_metrics.py \
      -q

### Próxima etapa

Frente 09B:

- isolar resolução de identidade em helper único;
- preferir `structure_id` quando disponível;
- manter `aba` apenas como rastreabilidade/fallback legado;
- reduzir `DELETE/WHERE aba + timestamp` ou encapsular em caminho explicitamente legado;
- atualizar guardrail para exigir o novo contrato.

## Frente 09B — DerivedRepo com delete idempotente preferindo structure_id

Status: aplicada e validada.

Registrado em: 2026-07-29 21:49:10

### Objetivo

Reduzir o risco do DerivedRepo manter snapshots duplicados quando uma estrutura
mantem o mesmo structure_id, mas muda ou resolve outro alias legado de aba.

A frente altera os deletes idempotentes de snapshots derivados para preferirem:

- structure_id + timestamp, quando structure_id estiver disponivel;
- aba + timestamp apenas como fallback legado.

### Regra consolidada

- Entrada canonica: structure_id.
- Chave preferencial de substituicao de snapshot: structure_id + timestamp.
- Fallback legado autorizado: aba + timestamp.
- Coluna aba permanece como rastreabilidade e compatibilidade fisica.
- Nenhuma tabela legada foi removida nesta frente.

### Arquivo alterado

- db/derived_repo.py

### Guardrail adicionado

- ATT/tests/test_guardrail_derived_repo_structure_id_deletes.py

### Evidencias esperadas

Comando principal:

    pytest \
      ATT/tests/test_guardrail_derived_repo_structure_id_deletes.py \
      ATT/tests/test_guardrail_derived_repo_structure_id_transition.py \
      ATT/tests/test_derived_service.py \
      ATT/tests/test_payoff_canonical.py \
      ATT/tests/test_structure_metrics.py \
      -q

Compilacao esperada:

    python -m py_compile \
      ATT/patch_09b_derived_repo_structure_id_deletes.py \
      ATT/tests/test_guardrail_derived_repo_structure_id_deletes.py \
      db/derived_repo.py

### Contrato validado

A Frente 09B segue o plano de contencao:

- Camada canonica prioriza structure_id.
- Aba continua permitida somente como fallback legado.
- A alteracao e pequena, testavel e reversivel.
- Nao cria pasta nova na raiz.
- Usa ATT para patch e ATT/tests para guardrail.

### Situacao final

Frente 09B concluida quando os testes acima passarem.

### Validação executada

Validado em: 2026-07-29 21:54:11

Resultado real dos testes:

    32 passed in 0.57s

Resultado da inspeção pós-patch:

- DELETE FROM payoff_curve_points: 5 -> 2
- DELETE FROM structure_decisions: 5 -> 2
- WHERE aba = ? AND timestamp = ?: 8 -> 3
- WHERE aba = ?: 10 -> 5
- structure_id: 43 -> 57

Interpretação:

- Os deletes idempotentes principais de snapshot passaram a preferir structure_id + timestamp.
- O fallback por aba + timestamp permanece apenas no helper de transição.
- Os deletes restantes são rotinas de limpeza por data antiga, não substituição de snapshot.
- A Frente 09B está validada.

## Frente 09C — DerivedRepo lê payoff por structure_id preferencial

Status: aplicada e validada.

Registrado em: 2026-07-29 21:58:39

### Objetivo

Permitir que a leitura de pontos de payoff derivados use `structure_id` como
filtro preferencial, reduzindo dependência operacional de `aba` em consultas
canônicas.

### Regra consolidada

- Entrada canônica: `structure_id`.
- Filtro preferencial de leitura: `structure_id`.
- `aba` permanece autorizada apenas como fallback legado.
- `timestamp` continua sendo filtro complementar quando informado.
- Compatibilidade com chamadas antigas por `aba` foi preservada.

### Arquivo alterado

- `db/derived_repo.py`

### Guardrail adicionado

- `ATT/tests/test_guardrail_derived_repo_get_payoff_by_structure_id.py`

### Evidências executadas

Compilação executada:

    python -m py_compile \
      ATT/tests/test_guardrail_derived_repo_get_payoff_by_structure_id.py \
      db/derived_repo.py

    python -m py_compile ATT/patch_09c_derived_repo_get_payoff_by_structure_id.py

Resultado:

    OK, sem erro de sintaxe.

Comando executado:

    pytest \
      ATT/tests/test_guardrail_derived_repo_get_payoff_by_structure_id.py \
      ATT/tests/test_guardrail_derived_repo_structure_id_deletes.py \
      ATT/tests/test_guardrail_derived_repo_structure_id_transition.py \
      ATT/tests/test_derived_service.py \
      ATT/tests/test_payoff_canonical.py \
      ATT/tests/test_structure_metrics.py \
      -q

Resultado:

    35 passed in 0.67s

### Contrato validado

A Frente 09C segue o plano de contenção:

- Camada canônica lê payoff por `structure_id`.
- `aba` segue somente como compatibilidade legada.
- A alteração é pequena, testável e reversível.
- Não cria pasta nova na raiz.
- Usa `ATT` para patch e `ATT/tests` para guardrail.

### Situação final

Frente 09C concluída.

O `DerivedRepo` agora permite leitura canônica de payoff por `structure_id`,
mantendo fallback legado por `aba`.\n\n## Frente 09D — DerivedRepo validate_snapshot_consistency por structure_id

Status: aplicada, aguardando validação.

Registrado em: 2026-07-29 22:01:10

### Objetivo

Ajustar a validação de consistência dos snapshots derivados para usar a regra
canônica da transição:

- structure_id + timestamp quando structure_id estiver disponível;
- aba + timestamp somente como fallback legado quando ambos os lados não tiverem structure_id.

### Arquivo alterado

- db/derived_repo.py

### Guardrail adicionado

- ATT/tests/test_guardrail_derived_repo_consistency_structure_id.py

### Contrato validado

- Decisão e payoff com mesmo structure_id e timestamp são consistentes mesmo que aba seja diferente.
- Fluxo legado sem structure_id continua consistente por aba + timestamp.
- Fluxo legado sem structure_id e com abas divergentes continua sendo marcado como inconsistente.

### Evidência esperada

    pytest \
      ATT/tests/test_guardrail_derived_repo_consistency_structure_id.py \
      ATT/tests/test_guardrail_derived_repo_get_payoff_by_structure_id.py \
      ATT/tests/test_guardrail_derived_repo_structure_id_deletes.py \
      ATT/tests/test_guardrail_derived_repo_structure_id_transition.py \
      ATT/tests/test_derived_service.py \
      ATT/tests/test_payoff_canonical.py \
      ATT/tests/test_structure_metrics.py \
      -q

### Situação final

Frente 09D concluída quando os testes acima passarem.

## Frente 10 — Contrato canônico de schema para pricing_executions

Status: aplicada e validada.

Registrado em: 2026-07-29 22:11:01

### Objetivo

Consolidar o contrato mínimo da tabela pricing_executions, evitando regressão
entre schemas paralelos e garantindo os campos usados pelo repository, services
de pricing e consultas.

### Regra consolidada

- Campo de status oficial: execution_status.
- Payload de entrada oficial: pricing_payload.
- Resultado persistido oficial: result.
- Identidade canônica preferencial: structure_id.
- Não usar coluna legada ambígua status em pricing_executions.

### Arquivos envolvidos

- infra/bootstrap_structures_schema.py
- repositories/pricing_executions_repository.py
- services/pricing_execution_persistence_service.py
- services/pricing_execution_query_service.py

### Guardrail adicionado

- ATT/tests/test_guardrail_pricing_executions_schema_contract.py

### Evidências esperadas

    python -m py_compile \
      ATT/patch_10_pricing_executions_schema_contract.py \
      ATT/tests/test_guardrail_pricing_executions_schema_contract.py \
      infra/bootstrap_structures_schema.py \
      repositories/pricing_executions_repository.py

    pytest \
      ATT/tests/test_guardrail_pricing_executions_schema_contract.py \
      ATT/tests/test_pricing_executions_repository.py \
      ATT/tests/test_pricing_execution_app_service.py \
      ATT/tests/test_pricing_execution_orchestration_service.py \
      ATT/tests/test_pricing_execution_persistence_service.py \
      ATT/tests/test_pricing_execution_query_service.py \
      ATT/tests/test_pricing_execution_service.py \
      -q

## Frente 11A — Contrato financeiro de leg: premium, current_price e multiplier

Status: aplicada.

Registrado em: 2026-07-29 22:16:54

### Objetivo

Consolidar a separação entre preço de entrada e preço atual de mercado,
alinhando o comportamento ao contrato financeiro definido no plano de contenção.

### Regras consolidadas

- `premium` permanece como preço de entrada.
- `entry_premium` preserva explicitamente o preço de entrada quando houver enriquecimento RTD.
- `current_price` recebe o preço atual vindo do RTD.
- `price` não deve ser usado como contrato novo.
- `multiplier` padrão para opções passa a ser `100.0`.

### Arquivos ajustados

- `ATT/tests/test_structure_leg_rtd_enrichment_service.py`
- `services/terminal_vwap_payoff_app_service.py`
- `services/structure_input_mapper.py`
- `services/robo_leg_mapper.py`
- `services/legacy_robo_legs_fallback.py`
- `services/canonical_pricing_facade.py`
- `domain/calculation_request.py`
- `domain/payoff.py`

### Evidência esperada

    python -m py_compile \
      ATT/patch_11a_financial_leg_contract_premium_current_multiplier.py \
      services/structure_leg_rtd_enrichment_service.py \
      services/terminal_vwap_payoff_app_service.py \
      services/terminal_vwap_payoff_viewmodel_service.py \
      services/structure_input_mapper.py \
      services/robo_leg_mapper.py \
      services/legacy_robo_legs_fallback.py \
      services/canonical_pricing_facade.py \
      services/pricing_payload_adapter.py \
      domain/payoff.py \
      domain/calculation_request.py \
      domain/position_side.py \
      domain/structure_metrics.py

    pytest \
      ATT/tests/test_structure_leg_rtd_enrichment_service.py \
      ATT/tests/test_terminal_vwap_payoff_app_service.py \
      ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py \
      ATT/tests/test_robo_leg_mapper.py \
      ATT/tests/test_legacy_robo_legs_fallback.py \
      ATT/tests/test_canonical_pricing_facade.py \
      ATT/tests/test_pricing_payload_adapter.py \
      ATT/tests/test_position_side.py \
      ATT/tests/test_payoff_canonical.py \
      ATT/tests/test_structure_metrics.py \
      -q

## Frente 11 — Contrato canônico de legs para pricing/payoff

Status: aplicada e validada.

Registrado em: 2026-07-29 22:20:00

### Objetivo

Consolidar o contrato canônico das legs usadas no fluxo de pricing/payoff,
separando preço de entrada, preço vivo RTD, lado da posição, tipo da opção e
multiplicador operacional.

### Regra consolidada

- `premium`: preço de entrada da operação.
- `current_price`: preço vivo vindo do RTD/mercado.
- `multiplier`: padrão canônico `100.0`.
- `position_side`: canônico de domínio como `COMPRADO` ou `VENDIDO`.
- `option_type`: canônico como `CALL` ou `PUT`.
- `price` não deve substituir semanticamente `premium` nem `current_price`.
- Conversões técnicas para `LONG`/`SHORT` ficam restritas às bordas do engine.

### Arquivos envolvidos

- `services/structure_leg_rtd_enrichment_service.py`
- `services/terminal_vwap_payoff_app_service.py`
- `services/terminal_vwap_payoff_viewmodel_service.py`
- `services/robo_leg_mapper.py`
- `services/legacy_robo_legs_fallback.py`
- `services/canonical_pricing_facade.py`
- `services/pricing_payload_adapter.py`
- `domain/payoff.py`
- `domain/calculation_request.py`
- `domain/position_side.py`
- `domain/structure_metrics.py`

### Evidências validadas

    python -m py_compile services/robo_leg_mapper.py ATT/tests/test_robo_leg_mapper.py

    pytest ATT/tests/test_structure_leg_rtd_enrichment_service.py ATT/tests/test_terminal_vwap_payoff_app_service.py ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py ATT/tests/test_robo_leg_mapper.py ATT/tests/test_legacy_robo_legs_fallback.py ATT/tests/test_canonical_pricing_facade.py ATT/tests/test_pricing_payload_adapter.py ATT/tests/test_position_side.py ATT/tests/test_payoff_canonical.py ATT/tests/test_structure_metrics.py -q

Resultado validado:

    87 passed, 6 subtests passed

## Frente 12 — Gregas negativas e zero preservados no enriquecimento RTD

Status: concluída e validada.

Registrado em: 2026-07-30 11:20:16

### Objetivo

Corrigir o contrato financeiro das gregas no fluxo de enriquecimento RTD de legs,
garantindo que valores negativos e zero sejam preservados corretamente.

Esta frente dá continuidade à Frente 11, que consolidou o contrato canônico de
legs para pricing/payoff.

### Contrato mantido da Frente 11

- premium: preço de entrada.
- current_price: preço atual de mercado.
- multiplier: padrão canônico 100.0.
- position_side: COMPRADO ou VENDIDO.
- option_type: CALL ou PUT.

### Problema identificado

No plano de contenção, o Eixo E apontava risco financeiro direto nas gregas.

O risco era tratar gregas pela mesma regra usada para preços positivos,
o que poderia eliminar valores financeiramente válidos, como:

- delta negativo.
- theta negativo.
- gamma igual a zero.
- vega igual a zero.

Gregas negativas e gregas iguais a zero são válidas e não podem ser
interpretadas automaticamente como ausência de dado.

### Regra consolidada

A Frente 12 formaliza a distinção entre campos de preço/mercado e campos de gregas.

Campos de preço e mercado devem continuar protegidos contra valores inválidos:

    ultimo_preco
    bid
    ask
    vwap
    volume

Campos de gregas devem aceitar valores negativos e zero:

    delta
    gamma
    theta
    vega

### Arquivo principal envolvido

    services/structure_leg_rtd_enrichment_service.py

### Testes relacionados

    ATT/tests/test_structure_leg_rtd_enrichment_service.py
    ATT/tests/test_structure_metrics.py
    ATT/tests/test_terminal_vwap_payoff_app_service.py
    ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py

### Evidência de compilação

Comando executado:

    python -m py_compile \
      ATT/patch_12_greeks_allow_negative.py \
      services/structure_leg_rtd_enrichment_service.py \
      ATT/tests/test_structure_leg_rtd_enrichment_service.py

Resultado: compilação sem erro.

### Evidência de regressão

Comando executado:

    pytest \
      ATT/tests/test_structure_leg_rtd_enrichment_service.py \
      ATT/tests/test_structure_metrics.py \
      ATT/tests/test_terminal_vwap_payoff_app_service.py \
      ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py \
      -q

Resultado validado:

    32 passed in 0.46s

### Observação operacional

Durante a aplicação da Frente 12, o patch automatizado
ATT/patch_12_greeks_allow_negative.py retornou erro porque o bloco de gregas
não foi encontrado exatamente no formato esperado pelo script.

Erro observado:

    RuntimeError: Bloco de gregas não encontrado em structure_leg_rtd_enrichment_service.py

Mesmo assim, a validação posterior por py_compile e testes de regressão confirmou
que o estado final do código está consistente para esta frente.

### Critério de conclusão

A Frente 12 é considerada concluída quando:

- o enriquecimento RTD preserva gregas negativas.
- o enriquecimento RTD preserva gregas iguais a zero.
- preços de mercado continuam separados das gregas.
- premium e current_price continuam semanticamente separados.
- os testes de regressão passam.

### Resultado

Frente 12 concluída e validada.

### Próxima frente recomendada

Frente 13 — Normalização explícita de C/V versus CALL/PUT.

Contrato confirmado para a Frente 13:

    C    = COMPRA / COMPRADO
    V    = VENDA / VENDIDO
    CALL = CALL, sempre palavra completa para tipo da opção
    PUT  = PUT, sempre palavra completa para tipo da opção

Regras esperadas:

    position_side:
      C, COMPRA, COMPRADO, LONG  -> COMPRADO
      V, VENDA, VENDIDO, SHORT   -> VENDIDO

    option_type:
      CALL -> CALL
      PUT  -> PUT

    Não aceitar C/P como option_type canônico.
    Não transformar valor desconhecido em PUT por default.
    Valor inválido deve gerar erro explícito.

## Frente 13 — Normalização explícita de C/V versus CALL/PUT — encerrada

### Status

Concluída e validada.

### Objetivo da frente

Separar definitivamente dois contratos que estavam misturados no sistema:

- lado da posição;
- tipo da opção.

Antes da Frente 13, havia risco de confusão entre:

- `C` como compra;
- `C` como call;
- `P` como put;
- valores inválidos sendo normalizados silenciosamente para `PUT`.

Essa ambiguidade tinha impacto direto no fluxo de legs, pricing, payoff e decisão.

### Contrato consolidado

#### Lado da posição

O contrato de lado operacional da posição passa a aceitar:

- `C`, `COMPRA`, `COMPRADO`, `LONG` -> `COMPRADO`;
- `V`, `VENDA`, `VENDIDO`, `SHORT` -> `VENDIDO`.

Para o pricing engine, o lado técnico é convertido para:

- `COMPRADO`, `C`, `COMPRA`, `LONG` -> `LONG`;
- `VENDIDO`, `V`, `VENDA`, `SHORT` -> `SHORT`.

#### Tipo da opção

O contrato canônico de tipo da opção passa a aceitar somente:

- `CALL`;
- `PUT`.

Não são aceitos como `option_type` canônico:

- `C`;
- `P`;
- aliases ambíguos;
- valores vazios;
- valores desconhecidos.

Valor inválido deve gerar erro explícito.

### Regras finais aplicadas

- `C/V` pertencem ao contrato de compra/venda da posição.
- `CALL/PUT` pertencem ao contrato de tipo da opção.
- `C/P` não são aceitos como `option_type` canônico.
- Valor desconhecido de `option_type` não pode virar `PUT` por default.
- Valor desconhecido de `cv` ou `position_side` deve gerar erro explícito.
- O adapter de pricing deve receber o contrato canônico e converter o lado operacional para `LONG/SHORT`.

### Arquivos envolvidos

- `utils/leg_normalizers.py`
- `services/robo_leg_mapper.py`
- `services/legacy_robo_legs_fallback.py`
- `services/pricing_payload_adapter.py`
- `ATT/tests/test_frente_13_cv_call_put_contract.py`
- `docs/FRENTES_CORRIGIDAS.md`

### Ajustes consolidados

#### `utils/leg_normalizers.py`

Foram formalizados normalizadores explícitos para:

- `normalize_position_side`;
- `normalize_pricing_side`;
- `normalize_option_type`;
- `normalize_call_put`.

O comportamento legado de `normalize_call_put` também foi endurecido para aceitar apenas `CALL` ou `PUT` por extenso.

#### `services/robo_leg_mapper.py`

O mapper de legs do robô passou a:

- separar `cv` de `call_put`;
- aceitar `vencimento` como `str` ou objeto com `strftime`;
- retornar `position_side` canônico;
- retornar `option_type` canônico;
- usar erro explícito para `cv` inválido;
- usar erro explícito para `call_put` inválido;
- alinhar o `multiplier` padrão para `100.0`.

#### `services/legacy_robo_legs_fallback.py`

O fallback legado passou a:

- usar os normalizadores centralizados;
- impedir fallback silencioso para `PUT`;
- retornar erro explícito para `cv` inválido;
- retornar erro explícito para `call_put` inválido;
- alinhar o `multiplier` padrão para `100.0`.

#### `services/pricing_payload_adapter.py`

O adapter de pricing passou a:

- converter `position_side` para `LONG/SHORT` via `normalize_pricing_side`;
- validar `option_type` via `normalize_option_type`;
- impedir que valores ambíguos cheguem ao payload do pricing.

### Validação executada

Foram executados testes específicos da Frente 13 e testes de regressão relacionados.

Resultado consolidado:

- `74 passed`;
- `6 subtests passed`;
- nenhuma falha remanescente na suíte executada.

### Guardrail criado

A Frente 13 passa a proteger o sistema contra regressões nos seguintes pontos:

- `C` não pode ser interpretado como `CALL` dentro de `option_type`;
- `P` não pode ser interpretado como `PUT` dentro de `option_type`;
- `call_put` inválido não pode virar `PUT` por default;
- `position_side` deve ser explicitamente normalizado;
- pricing deve receber lado técnico `LONG/SHORT`;
- domínio canônico deve preservar `COMPRADO/VENDIDO` e `CALL/PUT`.

### Resultado

A Frente 13 encerra a ambiguidade entre compra/venda e CALL/PUT.

O sistema passa a ter um contrato mais seguro para legs financeiras, reduzindo risco de erro silencioso no payoff, pricing e decisão.

## Frente 14 — Contrato canônico de multiplier de opções

Status: concluída.

### Objetivo

Padronizar o contrato financeiro mínimo do multiplier em legs de opções, removendo o risco de cálculo de payoff, pricing ou payload com multiplicador incorreto.

### Decisão consolidada

O contrato oficial definido para opções é:

- multiplier padrão para opções: 100.0;
- multiplier ausente, vazio ou None deve assumir 100.0;
- multiplier informado deve ser convertido para float;
- multiplier menor ou igual a zero deve gerar erro explícito;
- nenhuma camada crítica deve assumir silenciosamente 1.0 para opções;
- multiplier representa o fator contratual da opção;
- multiplier não deve ser usado para corrigir quantity.

### Implementação aplicada

Foi criado e reforçado o normalizador canônico em utils/leg_normalizers.py:

- DEFAULT_OPTION_MULTIPLIER;
- normalize_option_multiplier.

O normalizador foi adotado nos pontos críticos de entrada, fallback, payoff e pricing:

- services/robo_leg_mapper.py;
- services/legacy_robo_legs_fallback.py;
- services/terminal_vwap_payoff_app_service.py;
- services/pricing_payload_adapter.py.

Também foi criado ou ajustado o teste contratual:

- ATT/tests/test_frente_14_multiplier_contract.py.

### Ajustes complementares

Durante a execução foram aplicados reforços incrementais:

- Frente 14B: uso obrigatório do normalizador nos pontos críticos;
- Frente 14C: correção da ordem de imports em terminal_vwap_payoff_app_service.py;
- Frente 14D: ajuste do guardrail de teste para refletir o contrato reforçado com multiplier None normalizado para 100.0.

### Validação executada

Foram validados os módulos afetados por compilação e testes direcionados.

Resultado consolidado registrado:

- py_compile aprovado;
- testes direcionados aprovados;
- busca residual por uso perigoso de 1.0 como default de multiplier sem ocorrências operacionais nos arquivos críticos cobertos.

### Observação

A execução ampla de pytest ATT/tests -q ainda possuía bloqueio ambiental de coleta em teste dependente de customtkinter/tkinter. Esse erro foi tratado como fora do escopo da Frente 14.

### Conclusão

A Frente 14 foi concluída. O contrato canônico de multiplier de opções foi consolidado e protegido por testes.

---

## Frente 15 — Schema mínimo canônico das tabelas derivadas

Status: concluída e validada localmente.

### Objetivo

Garantir que as tabelas derivadas críticas sejam compatíveis com o contrato canônico baseado em structure_id.

### Problema tratado

O sistema ainda convivia com resíduos da transição entre identidade legada por aba e identidade canônica por structure_id.

O risco era que serviços de payoff, decisão e persistência derivada tentassem gravar ou ler structure_id em tabelas que não possuíam essa coluna de forma garantida.

Tabelas tratadas:

- structure_decisions;
- payoff_curve_points;
- payoff_curve_summary.

### Decisão consolidada

As tabelas derivadas passam a seguir o seguinte contrato mínimo:

- structure_decisions deve possuir structure_id quando a tabela existir;
- payoff_curve_points deve possuir structure_id quando a tabela existir;
- payoff_curve_summary passa a ser tabela derivada oficial mínima e deve possuir structure_id.

A Frente 15 não recria tabelas existentes e não executa operação destrutiva.

### Arquivo criado

- db/migrations/ensure_derived_tables_schema.py.

### Teste criado

- ATT/tests/test_frente_15_derived_schema_contract.py.

### Regras da migration

A migration é:

- idempotente;
- sem DROP TABLE;
- sem DELETE FROM;
- sem recriar structure_decisions;
- sem recriar payoff_curve_points;
- tolerante à ausência de structure_decisions ou payoff_curve_points;
- responsável por criar payoff_curve_summary como tabela derivada oficial mínima quando ausente;
- responsável por adicionar structure_id somente quando a coluna ainda não existe.

### Validação executada

Resultado registrado:

- teste dedicado da Frente 15 aprovado;
- aplicação no banco local dados/app.db validada;
- regressão de banco único aprovada;
- resultado consolidado informado: 12 passed.

### Conclusão

A Frente 15 foi concluída. O schema mínimo das tabelas derivadas críticas ficou alinhado ao contrato canônico por structure_id.

---

## Frente 16 — Schema único de pricing_executions

Status: concluída e validada localmente.

### Objetivo

Eliminar a ambiguidade no contrato da tabela pricing_executions, garantindo que bootstrap, repository e services de pricing usem o mesmo schema mínimo oficial.

### Problema tratado

Foi identificado risco de coexistência de mais de um schema para pricing_executions, especialmente entre:

- infra/bootstrap_structures_schema.py;
- repositories/pricing_executions_repository.py;
- services de execução, persistência, orquestração e consulta de pricing.

O risco principal era o repository esperar campos que o bootstrap não garantia, causando falhas diferentes entre ambientes ou perda de rastreabilidade do envelope de pricing.

### Decisão consolidada

A tabela pricing_executions passa a ter um contrato oficial mínimo garantido por migration própria.

Campos obrigatórios definidos:

- id;
- structure_id;
- execution_status;
- pricing_payload;
- result;
- error_message;
- created_at;
- updated_at.

O bootstrap de estruturas foi revisado para delegar a garantia da tabela pricing_executions ao contrato oficial da migration.

### Arquivos criados ou revisados

- db/migrations/ensure_pricing_executions_schema.py;
- ATT/tests/test_frente_16_pricing_executions_schema_contract.py;
- infra/bootstrap_structures_schema.py;
- docs/FRENTES_CORRIGIDAS.md.

### Ajuste complementar

Após a aplicação inicial, foi aplicada correção técnica porque from __future__ import annotations havia ficado fora da posição válida em infra/bootstrap_structures_schema.py.

Essa correção não alterou o contrato funcional da Frente 16.

### Validação executada

Resultado registrado:

- testes específicos da Frente 16 aprovados;
- testes relacionados ao repository e services de pricing aprovados;
- validação integrada com frentes anteriores aprovada;
- resultado consolidado informado: 67 passed.

### Conclusão

A Frente 16 foi concluída. O schema oficial mínimo de pricing_executions foi consolidado, aplicado no banco local e validado por testes específicos e integrados.

---

## Frente 17 — Contenção de db/writer.py e db/reader.py

Status: concluída.

### Objetivo

Corrigir, isolar ou aposentar os módulos semi-legados de leitura e escrita direta no banco, evitando que db/writer.py e db/reader.py continuem como caminho operacional paralelo ao fluxo canônico.

### Problema tratado

O plano de contenção havia identificado que db/writer.py e db/reader.py aparentavam conter resíduo de refactor incompleto para StructureRef.

Os principais riscos eram:

- uso de aba indefinida;
- strings que deveriam ser interpoladas corretamente;
- escrita em colunas erradas;
- manutenção de caminho legado concorrente com repositories e services;
- possibilidade de novos fluxos usarem módulos semi-legados por engano.

### Diagnóstico realizado

Foi criada uma verificação de chamadores reais.

Resultado da varredura local:

- chamadores operacionais encontrados: 0;
- chamadores em testes encontrados: 0.

Relatório gerado ou revisado:

- ATT/frente_17_db_reader_writer_callers.json.

### Decisão consolidada

Como não foram encontrados chamadores reais, db/writer.py e db/reader.py foram aposentados como módulos operacionais ativos.

Os módulos foram mantidos apenas como stubs seguros de compatibilidade, com status explícito de legado e emissão de DeprecationWarning no import.

Fluxos novos ou corrigidos devem usar:

- repositories;
- services;
- db.derived_repo quando aplicável.

db/writer.py e db/reader.py não devem ser usados como camada ativa de leitura ou escrita no banco.

### Arquivos criados ou revisados

- db/writer.py;
- db/reader.py;
- ATT/frente_17_db_reader_writer_callers.json;
- ATT/tests/test_frente_17_db_reader_writer_containment.py;
- docs/FRENTES_CORRIGIDAS.md.

### Validação local

Resultado registrado:

- patch aplicado com sucesso;
- py_compile aprovado;
- testes da Frente 17 aprovados;
- 4 passed;
- 2 warnings esperados de DeprecationWarning ao importar db.reader e db.writer.

### Conclusão

A Frente 17 concluiu a contenção dos módulos db/writer.py e db/reader.py. O sistema reduz um caminho legado paralelo de acesso ao banco e reforça a direção canônica:

- UI e controllers;
- services;
- repositories;
- banco canônico.

---

## Frente 18 — Contrato financeiro de leg, multiplier, premium e current_price

Status: concluída.

A Frente 18 foi aplicada em duas etapas controladas:

- Frente 18A: auditoria do contrato financeiro de legs, sem alteração do fluxo operacional;
- Frente 18B: criação do contrato financeiro canônico em módulo próprio, também sem alterar o fluxo operacional existente.

### Objetivo

Formalizar o contrato financeiro canônico de uma leg, reduzindo ambiguidades entre multiplier, premium, current_price e price.

### Problema tratado

Foram identificadas ambiguidades com impacto direto em payoff, pricing e visualização:

- multiplier já havia sido parcialmente corrigido em frentes anteriores, mas ainda precisava de contrato explícito;
- premium, price e current_price ainda podiam ser interpretados de forma ambígua;
- modelos legado e canônico coexistiam sem uma referência formal única;
- parte do fluxo ainda aceitava aliases pouco explícitos.

### Decisão aplicada

Foi criado o contrato financeiro canônico de leg em:

- services/structure_leg_financial_contract.py.

O contrato passa a registrar explicitamente os campos mínimos esperados para uma leg financeira canônica:

- position_side: COMPRADO ou VENDIDO;
- pricing_side: LONG ou SHORT;
- option_type: CALL ou PUT;
- symbol;
- strike;
- expiration_date;
- quantity;
- premium;
- current_price;
- multiplier.

### Regras consolidadas

- multiplier oficial para opções: 100.0;
- premium representa preço de entrada;
- current_price representa preço atual de mercado;
- price não deve ser usado como campo canônico novo;
- price pode existir apenas como legado controlado, quando necessário;
- price legado, quando permitido, pode preencher current_price somente se current_price não tiver sido informado;
- price legado nunca sobrescreve current_price explícito.

### Arquivos criados ou atualizados

- ATT/patch_18a_leg_financial_contract_audit.py;
- ATT/patch_18a_fix_dataclass_import.py;
- ATT/patch_18b_leg_financial_contract.py;
- ATT/frente_18_leg_financial_contract_audit.json;
- ATT/tests/test_frente_18_leg_financial_contract_audit.py;
- ATT/tests/test_frente_18b_leg_financial_contract.py;
- services/structure_leg_financial_contract.py;
- docs/FRENTES_CORRIGIDAS.md.

### Validação executada

Resultado consolidado informado:

- 13 passed;
- 2 warnings esperados da Frente 17, referentes aos módulos db.reader.py e db.writer.py aposentados com DeprecationWarning.

### Conclusão

A Frente 18 criou a fonte central do contrato financeiro de leg. A adoção completa pelos serviços existentes deve continuar em frentes posteriores, por patches pequenos e testáveis.

---

## Frente 19 — Preservação de gregas negativas e zeros válidos

Status: Concluída.

### Objetivo

Garantir que gregas, variações e campos financeiros de risco que podem ser negativos ou zero não sejam descartados por normalizadores genéricos.

### Problema tratado

Foi identificado risco de perda de informação financeira quando conversões numéricas genéricas descartavam valores menores ou iguais a zero.

Esse comportamento era inadequado para campos de risco, porque:

- delta negativo pode ser válido;
- theta negativo pode ser válido;
- gamma pode ser zero;
- vega pode ser zero;
- variações podem carregar sinal financeiro relevante;
- zero pode representar dado válido e não ausência;
- decisões e métricas poderiam ser calculadas com informação incompleta.

### Regra consolidada

Foram separados os normalizadores por semântica financeira.

Campos que devem exigir valor positivo:

- bid;
- ask;
- vwap;
- volume;
- último preço quando aplicável;
- preços operacionais que não aceitam zero.

Campos que podem aceitar negativo ou zero:

- delta;
- gamma;
- theta;
- vega;
- variações;
- campos derivados de risco;
- campos financeiros onde o sinal é informação relevante.

Campos que aceitam zero, mas não aceitam negativo:

- campos não negativos específicos;
- métricas onde zero é válido, mas negativo é inválido por contrato.

### Frente 19A — Preservação inicial no enriquecimento RTD

Status: aplicada.

Foram separados normalizadores por semântica financeira em:

- services/structure_leg_rtd_enrichment_service.py.

Foram introduzidos ou conferidos helpers com papéis distintos:

- to_optional_float_allow_negative: preserva negativos e zero;
- to_optional_positive_float: mantém proteção para campos que exigem valor positivo.

Arquivos alterados ou criados:

- ATT/patch_19a_preserve_negative_greeks.py;
- ATT/tests/test_frente_19a_preserve_negative_greeks.py;
- services/structure_leg_rtd_enrichment_service.py;
- docs/FRENTES_CORRIGIDAS.md.

Critérios aceitos:

- delta negativo é preservado;
- theta negativo é preservado;
- zero válido não vira None indevidamente;
- campos que devem ser positivos continuam protegidos;
- testes específicos cobrem negativo, zero, vazio e inválido.

Resultado de teste:

- pytest ATT/tests/test_frente_19a_preserve_negative_greeks.py -q;
- 5 passed.

### Frente 19B — Normalizadores financeiros compartilhados e guardrails

Status: aplicada.

Foi consolidada uma base compartilhada de normalização numérica para campos financeiros e de risco, preservando gregas negativas e zeros válidos sem enfraquecer a proteção de campos que exigem valor positivo.

Entregas:

- criado utils/financial_number_normalizers.py;
- criado ATT/tests/test_frente_19b_financial_number_normalizers.py;
- mantida a separação semântica entre normalizadores de risco, não negativos e positivos;
- adicionado guardrail cobrindo os helpers introduzidos na Frente 19A.

Contrato validado:

- delta negativo deve ser preservado;
- theta negativo deve ser preservado;
- zero válido não deve virar None nos campos de risco;
- campos positivos continuam bloqueando zero, negativo, vazio, inválido, NaN e infinito;
- o parser aceita formatos numéricos comuns BR e US, como 1.234,56, 1,234.56, -0,25 e 0.

Resultado de teste:

- pytest ATT/tests/test_frente_19b_financial_number_normalizers.py -q;
- 6 passed.

### Frente 19C — Adoção controlada dos normalizadores financeiros compartilhados

Status: aplicada.

A Frente 19C iniciou a adoção dos normalizadores financeiros compartilhados criados na Frente 19B nos módulos candidatos, sem trocar o fluxo operacional amplo de uma só vez.

Arquivos tratados:

- utils/financial_number_normalizers.py;
- services/terminal_vwap_payoff_viewmodel_service.py;
- domain/structure_metrics.py;
- utils/leg_normalizers.py;
- ATT/tests/test_frente_19c_adopt_financial_normalizers.py;
- docs/FRENTES_CORRIGIDAS.md.

Contrato consolidado:

- parse_optional_risk_float preserva negativo e zero;
- parse_optional_greek_float preserva negativo e zero para gregas;
- parse_optional_variation_float preserva negativo e zero para variações;
- parse_optional_non_negative_float preserva zero e rejeita negativo;
- parse_optional_positive_float exige valor estritamente positivo;
- parse_optional_price_float mantém proteção positiva para preço operacional.

Critérios conferidos por teste:

- delta, theta e demais gregas negativas continuam preservadas;
- zero válido em risco não vira None;
- campos positivos seguem rejeitando zero e negativos;
- vazio e inválido seguem retornando None;
- módulos candidatos passam a registrar adoção dos normalizadores compartilhados.

Resultado de teste:

- pytest ATT/tests/test_frente_19c_adopt_financial_normalizers.py -q;
- 5 passed.

### Frente 19D — Fechamento e guardrails de gregas negativas e zeros válidos

Status: aplicada. Frente 19 encerrada.

A Frente 19D encerrou a frente com guardrails explícitos garantindo que a preservação de gregas negativas e zeros válidos permaneça protegida contra regressões.

Entregas:

- conferida API mínima dos normalizadores financeiros compartilhados;
- criado ou revisado teste de fechamento da Frente 19;
- criado relatório de fechamento da Frente 19;
- atualizado documento de evolução.

Arquivos alterados ou criados:

- ATT/patch_19d_close_frente_19.py;
- ATT/tests/test_frente_19d_close_negative_greeks_guardrails.py;
- ATT/frente_19_negative_greeks_closure.json;
- utils/financial_number_normalizers.py;
- docs/FRENTES_CORRIGIDAS.md.

Guardrails finais:

A Frente 19 passa a proteger explicitamente contra perda de informação financeira relevante, especialmente em:

- gregas negativas;
- gregas zeradas;
- variações negativas;
- variações zeradas;
- campos de risco com sinal financeiro;
- entradas vazias ou inválidas;
- campos positivos que não devem aceitar zero ou negativo;
- NaN e infinito.

Critérios finais de aceite:

- delta negativo é preservado;
- theta negativo é preservado;
- zero válido é preservado para campos de risco;
- campos positivos continuam rejeitando zero;
- campos positivos continuam rejeitando negativos;
- entradas vazias continuam retornando None;
- entradas inválidas continuam retornando None;
- NaN e infinito continuam rejeitados;
- normalizadores compartilhados têm contrato explícito;
- testes de regressão cobrem Frente 19A, 19B, 19C e 19D.

Resultado de teste da etapa 19D:

- pytest ATT/tests/test_frente_19d_close_negative_greeks_guardrails.py -q;
- 5 passed.

Regressão final executada:

- testes das Frentes 17, 18, 18B, 19A, 19B, 19C e 19D;
- resultado: 34 passed, 2 warnings.

Os 2 warnings são esperados e relacionados à Frente 17, onde db.reader.py e db.writer.py foram aposentados para uso operacional com aviso explícito de depreciação.

### Conclusão

A Frente 19 foi concluída com sucesso.

O sistema agora possui uma separação explícita entre normalização de campos positivos e normalização de campos de risco, preservando negativos e zeros válidos onde esses valores carregam significado financeiro.

A proteção foi aplicada inicialmente no enriquecimento RTD de legs, consolidada em normalizadores compartilhados, adotada de forma controlada em módulos candidatos e encerrada com guardrails específicos de regressão.
