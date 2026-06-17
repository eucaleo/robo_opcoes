# Fase 4.4 — Plano de normalização dos consumidores de caminhos de banco

## Status

Concluída.

## Tipo

Planejamento técnico/documental.

Sem alteração funcional.

## Objetivo

Definir uma ordem segura para normalizar consumidores funcionais de caminhos de banco SQLite, com base no inventário da Fase 4.3.

## Premissas

- `db/config.py` permanece como fonte técnica atual para caminhos oficiais.
- `dados/app.db` continua sendo o banco operacional/raw padrão.
- `dados/derived.db` continua sendo o banco derivado/recalculável padrão.
- Scripts com argumento `--db` devem preservar compatibilidade de CLI.
- Nenhuma alteração de schema ou conteúdo de banco deve ocorrer nesta fase.
- Chamadas diretas a `sqlite3.connect()` não são problema por si só quando recebem caminho já resolvido.

## Estratégia de normalização

A normalização deve priorizar consumidores de runtime antes de scripts auxiliares ou históricos.

## Ordem recomendada

### 1. Repositórios de runtime ligados ao banco operacional

Prioridade alta.

Arquivos candidatos:

- `repositories/rtd_option_quotes_repository.py`
- `repositories/structures_repository.py`
- `repositories/structure_events_repository.py`
- `repositories/pricing_executions_repository.py`
- `repositories/robo_legs_repository.py`
- `repositories/robo_legs_status_repository.py`

Motivo:

- são consumidores funcionais do domínio;
- participam de fluxos de operação;
- concentram defaults literais para `dados/app.db` ou `./dados/app.db`.

Diretriz:

- substituir defaults literais por valores derivados de `db.config.APP_DB_PATH`;
- preservar possibilidade de receber `db_path` explicitamente;
- não remover parâmetros públicos existentes.

### 2. Serviços de runtime

Prioridade alta.

Arquivos candidatos:

- `services/canonical_pricing_facade.py`
- `services/pricing_execution_app_service.py`

Motivo:

- participam de fluxo de precificação e execução;
- têm lógica sensível de escolha entre `app.db` e `derived.db`;
- qualquer alteração deve ser conservadora.

Diretriz:

- manter fallback explícito quando houver regra funcional documentada;
- centralizar somente caminhos padrão;
- não alterar regra de busca de dados sem teste específico.

### 3. UI e camada de leitura

Prioridade média.

Arquivos candidatos:

- `UI/models/ui_data.py`
- `UI/components/structure_editor_dialog.py`
- `UI/components/details_panel.py`

Motivo:

- consomem dados derivados e operacionais;
- possuem conexões diretas;
- podem depender de caminhos injetados pela aplicação.

Diretriz:

- preservar injeção de caminho quando existente;
- evitar troca ampla de comportamento de leitura;
- revisar caso a caso.

### 4. Módulos internos de DB derivado

Prioridade média.

Arquivos candidatos:

- `db/derived_repo.py`
- `db/reader.py`
- `db/writer.py`
- `domain/payoff_features.py`
- `create_payoff_summary_table.py`

Motivo:

- concentram uso de `dados/derived.db`;
- são candidatos naturais a usar `DERIVED_DB_PATH`.

Diretriz:

- migrar defaults para `db.config.DERIVED_DB_PATH`;
- manter compatibilidade com `db_path` explícito.

### 5. Infraestrutura e bootstrap

Prioridade média/baixa.

Arquivos candidatos:

- `infra/bootstrap_structures_schema.py`
- `db/init_db.py`
- `validate_db.py`

Motivo:

- scripts ou módulos de inicialização/validação;
- menor risco operacional se tratados depois do runtime.

Diretriz:

- centralizar caminho padrão;
- preservar comandos manuais existentes quando possível.

### 6. Scripts operacionais com `--db`

Prioridade baixa, porém importante para consistência.

Arquivos candidatos:

- `scripts/audit_rtd_option_quotes.py`
- `scripts/import_legacy_structure_legs.py`
- `scripts/import_lista_rtd_excel_to_option_quotes.py`
- `scripts/import_rtd_links_to_option_quotes.py`
- `scripts/purge_derived_snapshots.py`
- `scripts/repair_derived_db_consistency.py`
- `scripts/run_lista_rtd_option_quotes_pipeline.py`
- `scripts/run_rtd_option_quotes_pipeline.py`
- `scripts/seed_current_rtd_option_quotes.py`
- `scripts/validate_app_db.py`
- `scripts/validate_derived_db.py`

Diretriz:

- manter `--db`;
- alterar apenas o default interno para usar `APP_DB_PATH` ou `DERIVED_DB_PATH`;
- não alterar exemplos de documentação na mesma etapa, salvo quando necessário.

## Regras de segurança para futuras alterações

Toda alteração funcional futura deve obedecer às seguintes regras:

1. alterar poucos arquivos por commit;
2. preservar assinaturas públicas;
3. preservar parâmetros `db_path` e `--db`;
4. não trocar `app.db` por `derived.db` nem o inverso sem justificativa explícita;
5. executar validação mínima após cada grupo;
6. registrar checkpoint quando houver mudança de comportamento potencial.

## Critério de pronto para iniciar refatoração

A refatoração pode começar quando houver consenso sobre:

- priorizar repositórios de runtime;
- usar `db/config.py` como fonte central;
- manter compatibilidade dos parâmetros existentes;
- validar cada lote separadamente.

## Conclusão

A normalização deve ser incremental e conservadora.

A recomendação é iniciar pelos repositórios de runtime ligados a `dados/app.db`, pois concentram consumidores funcionais relevantes e defaults literais recorrentes.
