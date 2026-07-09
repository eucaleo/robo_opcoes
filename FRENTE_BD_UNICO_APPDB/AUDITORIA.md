# Auditoria - Frente BD Único app.db

## Estado inicial

Frente criada para eliminar dados/app.db e absorver suas responsabilidades válidas dentro de dados/app.db.

## Decisão arquitetural

O sistema terá apenas um banco físico:

dados/app.db

O banco dados/app.db será eliminado como banco físico, referência, fallback, cache separado, origem, destino ou mecanismo auxiliar.

## Fase 0 - Inventário

Status: pendente.

## Evidências

As evidências da frente devem ser gravadas em:

FRENTE_BD_UNICO_APPDB/evidencias/

## Registro de fases

### Fase 0

Objetivo:
Mapear todas as referências a app.db, app.db, RTD, repositórios, serviços, schemas, conexões SQLite, payoff, simulações, caches e testes.

Buscas executadas:
Pendente.

Arquivos afetados:
Pendente.

Testes executados:
Pendente.

Resultado:
Pendente.

Commit:
Pendente.


## Atualizacao - Fase 0 - Inventario inicial

Status:
Evidencias iniciais geradas.

Evidencias criadas:

- FRENTE_BD_UNICO_APPDB/evidencias/00_estado_git.txt
- FRENTE_BD_UNICO_APPDB/evidencias/01_bancos_e_diretorios.txt
- FRENTE_BD_UNICO_APPDB/evidencias/02_inventario_textual_geral.txt
- FRENTE_BD_UNICO_APPDB/evidencias/03_inventario_codigo_e_testes.txt
- FRENTE_BD_UNICO_APPDB/evidencias/04_schema_sqlite.txt
- FRENTE_BD_UNICO_APPDB/evidencias/05_classificacao_preliminar.txt
- FRENTE_BD_UNICO_APPDB/evidencias/06_resumo_fase_0.txt

Proxima acao:
Analisar as evidencias e classificar os arquivos em:

- migrar para app.db
- remover dependencia de app.db
- remover sync
- remover fallback
- corrigir testes
- atualizar documentacao
- sem acao


## Atualizacao - Fase 1 - Classificacao inicial

A Fase 0 foi analisada e a classificacao inicial foi registrada em:

- FRENTE_BD_UNICO_APPDB/evidencias/07_classificacao_fase_1.md

Principais conclusoes:

- dados/app.db ja possui rtd_option_quotes e rtd_underlying_quotes.
- dados/app.db ainda existe fisicamente.
- dados/app.db ainda possui rtd_option_quotes, gerando duplicidade operacional.
- dados/app.db possui payoff_curve_points, que nao apareceu no schema atual de dados/app.db.
- A remocao fisica de dados/app.db ainda nao deve ser feita antes da decisao sobre payoff_curve_points e antes da remocao das dependencias de codigo.
- A pasta docs/ aparece como untracked e sera removida na proxima rodada para concentrar a frente em FRENTE_BD_UNICO_APPDB/.

Proxima acao planejada:

- remover docs/ untracked
- gerar busca focada em app.db
- iniciar o primeiro patch de codigo por configuracao central e RTD


## Atualizacao - Fase 1 operacional iniciada

A pasta `docs/` criada anteriormente fora da frente oficial foi removida da raiz.

Evidencias geradas nesta etapa:

- `FRENTE_BD_UNICO_APPDB/evidencias/08_remocao_docs_untracked.txt`
- `FRENTE_BD_UNICO_APPDB/evidencias/09_ocorrencias_focadas_derived_db.txt`
- `FRENTE_BD_UNICO_APPDB/evidencias/10_arquivos_com_dependencia_derived.txt`
- `FRENTE_BD_UNICO_APPDB/evidencias/11_contagem_marcadores_derived.txt`

Tambem foi criado o guardrail local:

- `FRENTE_BD_UNICO_APPDB/scripts/check_no_derived_db_refs.sh`

Objetivo do guardrail:

- falhar enquanto ainda existirem referencias operacionais a `app.db`;
- excluir `dados/` e a propria frente de auditoria para evitar ruido;
- servir como validacao final antes da remocao fisica de `dados/app.db`.

Proxima etapa tecnica:

1. atacar configuracao central de banco;
2. garantir RTD exclusivamente em `dados/app.db`;
3. remover ou adaptar componentes `derived_*`;
4. decidir destino funcional de `payoff_curve_points`;
5. ajustar testes e checks.

## Atualizacao - Fase 1A

Foi iniciado o redirecionamento operacional para `dados/app.db`.

Estrategia adotada:

- manter nomes legados como `DERIVED_DB_PATH`, `derived_repo`, `derived_service` e afins por compatibilidade temporaria;
- fazer esses pontos deixarem de apontar fisicamente para `dados/app.db`;
- priorizar rotas operacionais e testes que ainda recebiam caminho literal `dados/app.db`;
- nao remover ainda arquivos legados, pois a remocao sera feita apenas depois da validacao funcional.

Evidencias desta etapa:

- `FRENTE_BD_UNICO_APPDB/evidencias/12_pre_patch_phase_1a_targets.txt`
- `FRENTE_BD_UNICO_APPDB/evidencias/13_phase1a_patch_output.txt`
- `FRENTE_BD_UNICO_APPDB/evidencias/14_phase1a_diff.txt`
- `FRENTE_BD_UNICO_APPDB/evidencias/15_phase1a_contagem_marcadores_pos_patch.txt`
- `FRENTE_BD_UNICO_APPDB/evidencias/16_phase1a_py_compile.txt`
- `FRENTE_BD_UNICO_APPDB/evidencias/17_phase1a_pytest_direcionado.txt`

Proxima etapa:

- analisar o diff real;
- reduzir referencias semanticas a `app.db`;
- decidir migração definitiva de `payoff_curve_points` para schema canonico dentro de `app.db`;
- substituir a persistencia `DerivedPayoffPersistence` por porta orientada a `app.db`.

## Atualizacao - Fase 1B

Foi executado o bootstrap/migracao das estruturas derivadas para `dados/app.db`.

Objetivo:

- tornar `app.db` funcionalmente equivalente ao antigo uso operacional de `app.db`;
- criar/validar tabelas derivadas no `app.db`;
- importar dados existentes de `dados/app.db`, quando disponivel;
- executar migration de `structure_id` em `payoff_curve_points`;
- limpar registros derivados invalidos com `timestamp` nulo ou vazio.

Evidencias desta etapa:

- `FRENTE_BD_UNICO_APPDB/evidencias/18_phase1b_schema_pre.txt`
- `FRENTE_BD_UNICO_APPDB/evidencias/19_phase1b_bootstrap_output.txt`
- `FRENTE_BD_UNICO_APPDB/evidencias/20_phase1b_schema_pos.txt`
- `FRENTE_BD_UNICO_APPDB/evidencias/21_phase1b_py_compile.txt`
- `FRENTE_BD_UNICO_APPDB/evidencias/22_phase1b_pytest_direcionado.txt`
- `FRENTE_BD_UNICO_APPDB/evidencias/23_phase1b_contagem_marcadores.txt`
- `FRENTE_BD_UNICO_APPDB/evidencias/24_phase1b_git_status.txt`

Observacao:

- antes da alteracao fisica do `app.db`, foi criado backup em `FRENTE_BD_UNICO_APPDB/backups/`.

## Atualizacao - Fase 1C

Foi completada a compatibilidade da tabela `structure_decisions` dentro de `dados/app.db`.

Motivo:

- apos a Fase 1B, `payoff_curve_points` estava consistente no `app.db`;
- porem `structure_decisions` ainda usava schema operacional simplificado;
- os testes da UI exigiam `timestamp` valido em todas as decisoes.

Acoes executadas:

- backup de `dados/app.db`;
- adicao das colunas derivadas ausentes em `structure_decisions`;
- merge de campos do antigo `dados/app.db`;
- preenchimento de fallback para `timestamp`, `aba` e `level`;
- criacao de indices por `structure_id/timestamp` e `aba/timestamp`.

Evidencias desta etapa:

- `FRENTE_BD_UNICO_APPDB/evidencias/25_phase1c_structure_decisions_migration.txt`
- `FRENTE_BD_UNICO_APPDB/evidencias/26_phase1c_appdb_diagnostico.txt`
- `FRENTE_BD_UNICO_APPDB/evidencias/27_phase1c_py_compile.txt`
- `FRENTE_BD_UNICO_APPDB/evidencias/28_phase1c_pytest_direcionado.txt`
- `FRENTE_BD_UNICO_APPDB/evidencias/29_phase1c_contagem_marcadores.txt`
- `FRENTE_BD_UNICO_APPDB/evidencias/30_phase1c_git_status.txt`

## Atualizacao - Fase 1D

Objetivo desta etapa:

- validar se `dados/app.db` ja consegue operar como fonte unica;
- testar os fluxos direcionados com `dados/app.db` temporariamente fora do caminho;
- mapear referencias remanescentes a nomes `derived*` antes de qualquer limpeza semantica ou remocao definitiva.

Evidencias desta etapa:

- `FRENTE_BD_UNICO_APPDB/evidencias/31_phase1d_appdb_single_source_guard.txt`
- `FRENTE_BD_UNICO_APPDB/evidencias/32_phase1d_mapa_referencias_derived.txt`
- `FRENTE_BD_UNICO_APPDB/evidencias/33_phase1d_py_compile_geral.txt`
- `FRENTE_BD_UNICO_APPDB/evidencias/34_phase1d_pytest_direcionado_normal.txt`
- `FRENTE_BD_UNICO_APPDB/evidencias/35_phase1d_git_status.txt`

## Atualizacao - Fase 1E

Objetivo desta etapa:

- remover de forma controlada o arquivo fisico legado `dados/app.db`;
- preservar backup do banco legado em `FRENTE_BD_UNICO_APPDB/backups`;
- validar que os testes direcionados continuam passando com `dados/app.db` como fonte unica;
- manter evidencias do estado final dos bancos e das referencias semanticas remanescentes.

Evidencias desta etapa:

- `FRENTE_BD_UNICO_APPDB/evidencias/36_phase1e_remove_legacy_derived_db.txt`
- `FRENTE_BD_UNICO_APPDB/evidencias/37_phase1e_db_files_status.txt`
- `FRENTE_BD_UNICO_APPDB/evidencias/38_phase1e_pytest_direcionado_normal.txt`
- `FRENTE_BD_UNICO_APPDB/evidencias/39_phase1e_mapa_referencias_pos_remocao.txt`
- `FRENTE_BD_UNICO_APPDB/evidencias/40_phase1e_git_status.txt`

## Atualizacao - Fase 1F-A

Objetivo desta etapa:

- limpar referencias literais ao arquivo fisico legado `derived.db`;
- substituir textos/caminhos literais para `app.db`;
- preservar nomes tecnicos de compatibilidade, como `derived_db_path`, `derived_repo` e `derived_service`;
- validar que a limpeza semantica nao quebra compilacao nem testes direcionados.

Evidencias desta etapa:

- `FRENTE_BD_UNICO_APPDB/evidencias/41_phase1f_semantic_cleanup_appdb_labels.txt`
- `FRENTE_BD_UNICO_APPDB/evidencias/42_phase1f_mapa_referencias_pos_cleanup.txt`
- `FRENTE_BD_UNICO_APPDB/evidencias/43_phase1f_pytest_direcionado.txt`
- `FRENTE_BD_UNICO_APPDB/evidencias/44_phase1f_git_status.txt`

## Atualizacao - Fase 1F-D.25

Objetivo desta etapa:

- remover residuos tecnicos proibidos derivados de derived_db_path em UI/components/details_panel.py;
- garantir que nao existam tokens tecnicos proibidos relacionados a banco derivado fisico;
- garantir que nao existam referencias a caminho fisico derived.db;
- validar compilacao e testes completos antes do commit.

Arquivos alterados:

- UI/components/details_panel.py
- FRENTE_BD_UNICO_APPDB/AUDITORIA.md

Evidencia desta etapa:

- FRENTE_BD_UNICO_APPDB/evidencias/137_phase1f_d25_remove_details_panel_derived_db_path.txt

Buscas obrigatorias:

- tokens tecnicos proibidos: derived_db, derived_db_path, DERIVED_DB_PATH, connect_derived, get_derived_connection
- nomes de arquivo proibidos: validate_derived, repair_derived, derived_db
- caminhos fisicos proibidos: derived.db, dados/derived, dados\\derived

Resultado esperado:

- buscas proibitivas sem ocorrencias
- compileall aprovado
- pytest completo aprovado

Commit:

- fase 1f-d25 remove derived_db_path do details panel

