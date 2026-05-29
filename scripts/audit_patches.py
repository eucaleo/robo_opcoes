# scripts/audit_patches.py
# Auditoria de patches do projeto ATT
# Atualizado: patch_23 e patch_24 adicionados

import os
import sqlite3
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def p(path):
    return os.path.join(ROOT, path)


def exists(path):
    return os.path.isfile(p(path))


def contains(path, text):
    try:
        with open(p(path), encoding="utf-8", errors="ignore") as f:
            return text in f.read()
    except FileNotFoundError:
        return False


def count_occurrences(path, text):
    try:
        with open(p(path), encoding="utf-8", errors="ignore") as f:
            return f.read().count(text)
    except FileNotFoundError:
        return 0


# ------------------------------------------------------------------
# Definicao dos patches
# ------------------------------------------------------------------

PATCHES = [
    {
        "id": "patch_01",
        "desc": "Auditoria baseline_v2 - documentacao e inventario",
        "checks": [
            ("docs/baseline_v2_audit.md existe",
             lambda: exists("docs/baseline_v2_audit.md")),
        ],
    },
    {
        "id": "patch_02",
        "desc": "Contratos canonicos de structures definidos",
        "checks": [
            ("infra/bootstrap_structures_schema.py existe",
             lambda: exists("infra/bootstrap_structures_schema.py")),
            ("Schema 'structures' definido no bootstrap",
             lambda: contains("infra/bootstrap_structures_schema.py", "structures")),
            ("Schema 'structure_legs' definido no bootstrap",
             lambda: contains("infra/bootstrap_structures_schema.py", "structure_legs")),
        ],
    },
    {
        "id": "patch_03",
        "desc": "Camada de compatibilidade com legado isolada",
        "checks": [
            ("repositories/structures_repository.py existe",
             lambda: exists("repositories/structures_repository.py")),
            ("alias_legacy_aba presente no repositorio",
             lambda: contains("repositories/structures_repository.py", "alias_legacy_aba")),
        ],
    },
    {
        "id": "patch_04",
        "desc": "CRUD canonico completo do StructuresRepository",
        "checks": [
            ("create_structure() implementado",
             lambda: contains("repositories/structures_repository.py", "def create_structure")),
            ("get_structure() implementado",
             lambda: contains("repositories/structures_repository.py", "def get_structure")),
            ("list_structures() implementado",
             lambda: contains("repositories/structures_repository.py", "def list_structures")),
            ("update_structure() implementado",
             lambda: contains("repositories/structures_repository.py", "def update_structure")),
            ("archive_structure() implementado",
             lambda: contains("repositories/structures_repository.py", "def archive_structure")),
            ("add_leg() implementado",
             lambda: contains("repositories/structures_repository.py", "def add_leg")),
            ("replace_legs() implementado",
             lambda: contains("repositories/structures_repository.py", "def replace_legs")),
        ],
    },
    {
        "id": "patch_05",
        "desc": "Testes smoke/contrato do StructuresRepository",
        "checks": [
            ("scripts/10_smoke_structures_repository.py existe",
             lambda: exists("scripts/10_smoke_structures_repository.py")),
            ("ATT/tests/test_patch10_smoke.py existe",
             lambda: exists("ATT/tests/test_patch10_smoke.py")),
            ("ATT/tests/test_patch10_ui_integration.py existe",
             lambda: exists("ATT/tests/test_patch10_ui_integration.py")),
        ],
    },
    {
        "id": "patch_06",
        "desc": "Normalizacao de repositories - queries e persistencia",
        "checks": [
            ("VALID_POSITION_SIDES definido",
             lambda: contains("repositories/structures_repository.py", "VALID_POSITION_SIDES")),
            ("VALID_OPTION_TYPES definido",
             lambda: contains("repositories/structures_repository.py", "VALID_OPTION_TYPES")),
            ("Validacao de expiration_date presente",
             lambda: contains("repositories/structures_repository.py", "expiration_date")),
        ],
    },
    {
        "id": "patch_10",
        "desc": "Smoke tests pytest para StructuresRepository (19 testes)",
        "checks": [
            ("ATT/tests/test_patch10_smoke.py existe",
             lambda: exists("ATT/tests/test_patch10_smoke.py")),
            ("TestStructuresRepository presente",
             lambda: contains("ATT/tests/test_patch10_smoke.py", "TestStructuresRepository")),
            ("TestRepositoryValidation presente",
             lambda: contains("ATT/tests/test_patch10_smoke.py", "TestRepositoryValidation")),
            ("TestImports presente",
             lambda: contains("ATT/tests/test_patch10_smoke.py", "TestImports")),
        ],
    },
    {
        "id": "patch_11",
        "desc": "Conexoes SQLite fechadas via try/finally (ResourceWarning fix)",
        "checks": [
            ("try/finally presente no repositorio",
             lambda: contains("repositories/structures_repository.py", "try")),
            ("conn.close() explicito presente",
             lambda: contains("repositories/structures_repository.py", "conn.close()")),
            ("Sem 'with self._connect() as conn' (padrao antigo)",
             lambda: not contains("repositories/structures_repository.py",
                                  "with self._connect() as conn")),
            ("conn.close() aparece >= 6 vezes (1 por metodo publico)",
             lambda: count_occurrences(
                 "repositories/structures_repository.py", "conn.close()") >= 6,
             lambda: f"{count_occurrences('repositories/structures_repository.py', 'conn.close()')}x encontrado"),
        ],
    },
    {
        "id": "patch_12",
        "desc": "MarketSnapshot - dominio e repositorio canonicos",
        "checks": [
            ("repositories/market_snapshot_repository.py existe",
             lambda: exists("repositories/market_snapshot_repository.py")),
            ("domain/market_snapshot.py existe",
             lambda: exists("domain/market_snapshot.py")),
            ("LegMarketSnapshot definido no dominio",
             lambda: contains("domain/market_snapshot.py", "LegMarketSnapshot")),
            ("StructureMarketSnapshot definido no dominio",
             lambda: contains("domain/market_snapshot.py", "StructureMarketSnapshot")),
            ("_parse_br_float implementado no repositorio",
             lambda: contains("repositories/market_snapshot_repository.py", "_parse_br_float")),
            ("_mid_price implementado no repositorio",
             lambda: contains("repositories/market_snapshot_repository.py", "_mid_price")),
        ],
    },
    {
        "id": "patch_13",
        "desc": "Politica de selecao manual > rtd (MarketSnapshotSelector)",
        "checks": [
            ("services/market_snapshot_selector.py existe",
             lambda: exists("services/market_snapshot_selector.py")),
            ("Politica manual > rtd implementada",
             lambda: contains("services/market_snapshot_selector.py", "manual")),
            ("scripts/61_smoke_market_snapshot.py existe",
             lambda: exists("scripts/61_smoke_market_snapshot.py")),
            ("SnapshotSelectionResult presente",
             lambda: contains("services/market_snapshot_selector.py",
                              "SnapshotSelectionResult")),
        ],
    },
    {
        "id": "patch_14",
        "desc": "canonical_input_service consome MarketSnapshotSelector [PENDENTE]",
        "checks": [
            ("services/canonical_input_service.py existe",
             lambda: exists("services/canonical_input_service.py")),
            ("MarketSnapshotSelector importado no canonical_input_service",
             lambda: contains("services/canonical_input_service.py",
                              "MarketSnapshotSelector")),
            ("scripts/63_smoke_canonical_with_snapshot.py existe",
             lambda: exists("scripts/63_smoke_canonical_with_snapshot.py")),
        ],
    },
    {
        "id": "patch_15",
        "desc": "Smoke integracao pipeline completo structure+snapshot->pricing [PENDENTE]",
        "checks": [
            ("scripts/64_smoke_pipeline_integration.py existe",
             lambda: exists("scripts/64_smoke_pipeline_integration.py")),
            ("PricingExecutionAppService importavel",
             lambda: exists("services/pricing_execution_app_service.py")),
        ],
    },
    {
        "id": "patch_16",
        "desc": "PricingExecutionPersistenceService criado",
        "checks": [
            ("services/pricing_execution_persistence_service.py existe",
             lambda: exists("services/pricing_execution_persistence_service.py")),
            ("PricingExecutionPersistenceService definido",
             lambda: contains(
                 "services/pricing_execution_persistence_service.py",
                 "class PricingExecutionPersistenceService"
             )),
            ("persist_execution() implementado",
             lambda: contains(
                 "services/pricing_execution_persistence_service.py",
                 "def persist_execution"
             )),
            ("services/payoff_persistence_port.py existe",
             lambda: exists("services/payoff_persistence_port.py")),
        ],
    },
    {
        "id": "patch_17",
        "desc": "DerivedPayoffPersistence — porta de persistencia derivada",
        "checks": [
            ("services/derived_payoff_persistence.py existe",
             lambda: exists("services/derived_payoff_persistence.py")),
            ("DerivedPayoffPersistence definido",
             lambda: contains(
                 "services/derived_payoff_persistence.py",
                 "class DerivedPayoffPersistence"
             )),
            ("persist() implementado",
             lambda: contains(
                 "services/derived_payoff_persistence.py",
                 "def persist"
             )),
            ("_persist_payoff() implementado",
             lambda: contains(
                 "services/derived_payoff_persistence.py",
                 "def _persist_payoff"
             )),
            ("_persist_decision() implementado",
             lambda: contains(
                 "services/derived_payoff_persistence.py",
                 "def _persist_decision"
             )),
            ("_build_canonical_input() implementado",
             lambda: contains(
                 "services/derived_payoff_persistence.py",
                 "def _build_canonical_input"
             )),
        ],
    },
    {
        "id": "patch_18",
        "desc": "CanonicalPricingFacade corrigida (C1-C4)",
        "checks": [
            ("services/canonical_pricing_facade.py existe",
             lambda: exists("services/canonical_pricing_facade.py")),
            ("CanonicalPricingFacade definida",
             lambda: contains(
                 "services/canonical_pricing_facade.py",
                 "class CanonicalPricingFacade"
             )),
            ("execute_pricing() implementado",
             lambda: contains(
                 "services/canonical_pricing_facade.py",
                 "def execute_pricing"
             )),
            ("_get_alias_legacy_aba() implementado",
             lambda: contains(
                 "services/canonical_pricing_facade.py",
                 "def _get_alias_legacy_aba"
             )),
            ("engine_result extraido do wrapper (C4)",
             lambda: contains(
                 "services/canonical_pricing_facade.py",
                 'execution_result.get("result", execution_result)'
             )),
        ],
    },
    {
        "id": "patch_19",
        "desc": "PricingExecutionsRepository — JSON -> SQLite (app.db)",
        "checks": [
            ("repositories/pricing_executions_repository.py existe",
             lambda: exists("repositories/pricing_executions_repository.py")),
            ("PricingExecutionsRepository definido",
             lambda: contains(
                 "repositories/pricing_executions_repository.py",
                 "class PricingExecutionsRepository"
             )),
            ("save_execution() implementado",
             lambda: contains(
                 "repositories/pricing_executions_repository.py",
                 "def save_execution"
             )),
            ("get_execution() implementado",
             lambda: contains(
                 "repositories/pricing_executions_repository.py",
                 "def get_execution"
             )),
            ("list_executions() implementado",
             lambda: contains(
                 "repositories/pricing_executions_repository.py",
                 "def list_executions"
             )),
            ("count_executions() implementado",
             lambda: contains(
                 "repositories/pricing_executions_repository.py",
                 "def count_executions"
             )),
            ("get_latest_by_structure() implementado",
             lambda: contains(
                 "repositories/pricing_executions_repository.py",
                 "def get_latest_by_structure"
             )),
            ("_deserialize() implementado (JSON -> dict)",
             lambda: contains(
                 "repositories/pricing_executions_repository.py",
                 "def _deserialize"
             )),
        ],
    },
    {
        "id": "patch_20",
        "desc": "payoff_features.upsert_curve_summary — try/finally (ResourceWarning fix)",
        "checks": [
            ("domain/payoff_features.py existe",
             lambda: exists("domain/payoff_features.py")),
            ("upsert_curve_summary() implementado",
             lambda: contains(
                 "domain/payoff_features.py",
                 "def upsert_curve_summary"
             )),
            ("try/finally presente no upsert",
             lambda: contains("domain/payoff_features.py", "finally")),
            ("conn.close() explicito presente",
             lambda: contains("domain/payoff_features.py", "conn.close()")),
        ],
    },
    {
        "id": "patch_21",
        "desc": "Pipeline conectado: payoff + decisao gravados no derived.db",
        "checks": [
            ("DerivedPayoffPersistence injetado na facade (C5)",
             lambda: contains(
                 "services/canonical_pricing_facade.py",
                 "DerivedPayoffPersistence"
             )),
            ("fire-and-forget: port falha nao derruba execucao",
             lambda: contains(
                 "services/pricing_execution_persistence_service.py",
                 "logger.exception"
             )),
            ("ATT/tests/test_patches_19_20_21.py existe",
             lambda: exists("ATT/tests/test_patches_19_20_21.py")),
            ("test_patch21_port_called_on_success presente",
             lambda: contains(
                 "ATT/tests/test_patches_19_20_21.py",
                 "test_patch21_port_called_on_success"
             )),
            ("test_patch21_facade_wiring presente",
             lambda: contains(
                 "ATT/tests/test_patches_19_20_21.py",
                 "test_patch21_facade_wiring"
             )),
        ],
    },
    {
        "id": "patch_22",
        "desc": "Auditoria e validacao do bootstrap completo (pricing_executions + wiring)",
        "checks": [
            ("ATT/tests/test_patch22.py existe",
             lambda: exists("ATT/tests/test_patch22.py")),
            ("test_patch22_schema_tables_and_indexes presente",
             lambda: contains(
                 "ATT/tests/test_patch22.py",
                 "test_patch22_schema_tables_and_indexes"
             )),
            ("test_patch22_pricing_executions_columns presente",
             lambda: contains(
                 "ATT/tests/test_patch22.py",
                 "test_patch22_pricing_executions_columns"
             )),
            ("test_patch22_facade_injects_derived_payoff_persistence presente",
             lambda: contains(
                 "ATT/tests/test_patch22.py",
                 "test_patch22_facade_injects_derived_payoff_persistence"
             )),
            ("test_patch22_bootstrap_is_idempotent presente",
             lambda: contains(
                 "ATT/tests/test_patch22.py",
                 "test_patch22_bootstrap_is_idempotent"
             )),
            ("pricing_executions no DATABASES do audit",
             lambda: contains(
                 "scripts/audit_patches.py",
                 "pricing_executions"
             )),
        ],
    },
    # ------------------------------------------------------------------
    # NOVOS — Fase 3A: Desacoplamento canônico
    # ------------------------------------------------------------------
    {
        "id": "patch_23",
        "desc": "Script de auditoria de acoplamento legado criado",
        "checks": [
            ("scripts/69_audit_legacy_domain_coupling.py existe",
             lambda: exists("scripts/69_audit_legacy_domain_coupling.py")),
            ("docs/audit_domain_coupling_patch24.md existe",
             lambda: exists("docs/audit_domain_coupling_patch24.md")),
            ("CouplingOccurrence definido no script",
             lambda: contains(
                 "scripts/69_audit_legacy_domain_coupling.py",
                 "CouplingOccurrence"
             )),
            ("AuditReport definido no script",
             lambda: contains(
                 "scripts/69_audit_legacy_domain_coupling.py",
                 "AuditReport"
             )),
            ("LEGACY_TERMS definido no script",
             lambda: contains(
                 "scripts/69_audit_legacy_domain_coupling.py",
                 "LEGACY_TERMS"
             )),
            ("Exit code CI implementado (sys.exit)",
             lambda: contains(
                 "scripts/69_audit_legacy_domain_coupling.py",
                 "sys.exit"
             )),
        ],
    },
    {
        "id": "patch_24",
        "desc": "Desacoplamento legado: decision.py limpo + payoff_features chave canonica",
        "checks": [
            # decision.py — remoção do legado
            ("compute_decision_for_aba removida de decision.py",
             lambda: not contains("domain/decision.py", "compute_decision_for_aba")),
            ("get_app_db_connection removido de decision.py",
             lambda: not contains("domain/decision.py", "get_app_db_connection")),
            ("rtd_analise_robo removido de decision.py",
             lambda: not contains("domain/decision.py", "rtd_analise_robo")),
            ("compute_payoff_for_aba removido de decision.py",
             lambda: not contains("domain/decision.py", "compute_payoff_for_aba")),
            ("read_structure_summary removido de decision.py",
             lambda: not contains("domain/decision.py", "read_structure_summary")),
            # decision.py — interfaces canônicas intactas
            ("compute_decision_from_contract preservado",
             lambda: contains("domain/decision.py", "def compute_decision_from_contract")),
            ("compute_decision_from_payoff preservado",
             lambda: contains("domain/decision.py", "def compute_decision_from_payoff")),
            ("compute_decision_from_inputs preservado",
             lambda: contains("domain/decision.py", "def compute_decision_from_inputs")),
            # payoff_features.py — chave canônica
            ("ON CONFLICT(structure_id, reference_date) em payoff_features",
             lambda: contains(
                 "domain/payoff_features.py",
                 "ON CONFLICT(structure_id, reference_date)"
             )),
            ("ON CONFLICT(timestamp, aba) removido de payoff_features",
             lambda: not contains(
                 "domain/payoff_features.py",
                 "ON CONFLICT(timestamp, aba)"
             )),
            ("structure_id em compute_curve_features",
             lambda: contains("domain/payoff_features.py", "structure_id")),
            ("reference_date em compute_curve_features",
             lambda: contains("domain/payoff_features.py", "reference_date")),
            # testes
            ("ATT/tests/test_patch24.py existe",
             lambda: exists("ATT/tests/test_patch24.py")),
            ("TestDecisionLegacyRemoval presente",
             lambda: contains(
                 "ATT/tests/test_patch24.py",
                 "TestDecisionLegacyRemoval"
             )),
            ("TestPayoffFeaturesCanonicalKey presente",
             lambda: contains(
                 "ATT/tests/test_patch24.py",
                 "TestPayoffFeaturesCanonicalKey"
             )),
            ("test_patch24_upsert_executes_with_in_memory_db presente",
             lambda: contains(
                 "ATT/tests/test_patch24.py",
                 "test_patch24_upsert_executes_with_in_memory_db"
             )),
        ],
    },
    {
        "id": "patch_25",
        "desc": "Smoke de regressao pos-patch_24 (decision + payoff canonicos)",
        "checks": [
            ("ATT/tests/teste_rapido_smoke_patch2_25.py existe",
                lambda: exists("ATT/tests/teste_rapido_smoke_patch2_25.py")),
            ("compute_decision_from_inputs presente em decision.py",
                lambda: contains("domain/decision.py", "def compute_decision_from_inputs")),
            ("compute_curve_features presente em payoff_features.py",
                lambda: contains("domain/payoff_features.py", "def compute_curve_features")),
            ("structure_id usado em compute_curve_features",
                lambda: contains("domain/payoff_features.py", "structure_id")),
        ],
    },
    {
        "id": "patch_26",
        "desc": "db/derived_repo.py - DerivedRepo canonico (write_decision_snapshot_atomic)",
        "checks": [
            ("db/derived_repo.py existe",
                lambda: exists("db/derived_repo.py")),
            ("class DerivedRepo definida",
                lambda: contains("db/derived_repo.py", "class DerivedRepo")),
            ("write_decision_snapshot_atomic implementado",
                lambda: contains("db/derived_repo.py", "def write_decision_snapshot_atomic")),
            ("insert_structure_decision implementado",
                lambda: contains("db/derived_repo.py", "def insert_structure_decision")),
            ("get_recent_decisions implementado",
                lambda: contains("db/derived_repo.py", "def get_recent_decisions")),
        ],
    },
    {
        "id": "patch_27",
        "desc": "db/derived_repo.py - migracao e guards de schema (_migrations)",
        "checks": [
            ("_migrations dict presente",
                lambda: contains("db/derived_repo.py", "_migrations")),
            ("guard ALTER TABLE para 'why'",
                lambda: contains("db/derived_repo.py", "why")),
            ("guard ALTER TABLE para 'spot_ref'",
                lambda: contains("db/derived_repo.py", "spot_ref")),
            ("guard ALTER TABLE para 'meta_json'",
                lambda: contains("db/derived_repo.py", "meta_json")),
            ("guard ALTER TABLE para 'structure_id'",
                lambda: contains("db/derived_repo.py", "structure_id")),
            ("_table_columns implementado",
                lambda: contains("db/derived_repo.py", "def _table_columns")),
        ],
    },
    {
        "id": "patch_28",
        "desc": "Migracao de structures legado para modelo canonico",
        "checks": [
            ("ATT/patches/patch_28_migrate_structures.py existe",
                lambda: exists("ATT/patches/patch_28_migrate_structures.py")),
            ("migrate() ou run() implementado no patch_28",
                lambda: (
                    contains("ATT/patches/patch_28_migrate_structures.py", "def migrate") or
                    contains("ATT/patches/patch_28_migrate_structures.py", "def run")
                )),
            ("tabela structures referenciada no patch_28",
                lambda: contains("ATT/patches/patch_28_migrate_structures.py", "structures")),
            ("tabela structure_legs referenciada no patch_28",
                lambda: contains("ATT/patches/patch_28_migrate_structures.py", "structure_legs")),
        ],
    },
    {
        "id": "patch_29",
        "desc": "Adicao de structure_id em structure_decisions (migration + backfill)",
        "checks": [
            ("ATT/patches/patch_29_add_structure_id_to_decisions.py existe",
                lambda: exists("ATT/patches/patch_29_add_structure_id_to_decisions.py")),
            ("ALTER TABLE structure_decisions no patch_29",
                lambda: contains(
                    "ATT/patches/patch_29_add_structure_id_to_decisions.py",
                    "structure_decisions"
                )),
            ("structure_id referenciado no patch_29",
                lambda: contains(
                    "ATT/patches/patch_29_add_structure_id_to_decisions.py",
                    "structure_id"
                )),
            ("backup criado antes da migracao (BAK)",
                lambda: (
                    contains("ATT/patches/patch_29_add_structure_id_to_decisions.py", "BAK") or
                    contains("ATT/patches/patch_29_add_structure_id_to_decisions.py", "backup") or
                    contains("ATT/patches/patch_29_add_structure_id_to_decisions.py", "shutil")
                )),
        ],
    },
    {
        "id": "patch_30",
        "desc": "derived_repo.py - corrige DDL e propaga structure_id em todos os INSERTs",
        "checks": [
            ("db/derived_repo.py existe",
                lambda: exists("db/derived_repo.py")),
            ("structure_id no INSERT de write_decision_snapshot_atomic",
                lambda: contains("db/derived_repo.py", "structure_id")),
            ("_migrations unifica guards ALTER TABLE",
                lambda: contains("db/derived_repo.py", "_migrations")),
            ("try/finally em write_decision_snapshot_atomic",
                lambda: contains("db/derived_repo.py", "finally")),
            ("conn.close() explicito em derived_repo",
                lambda: contains("db/derived_repo.py", "conn.close()")),
            ("_table_columns valida colunas presentes",
                lambda: contains("db/derived_repo.py", "_table_columns")),
        ],
    },
    {
        "id": "patch_31",
        "desc": "Fix UI/models/__init__.py — typo __ini__.py corrigido",
        "checks": [
            ("UI/models/__init__.py existe",
                lambda: exists("UI/models/__init__.py")),
            ("UI/models/__ini__.py (typo) NÃO existe",
                lambda: not exists("UI/models/__ini__.py")),
            ("ATT/tests/test_patch31.py existe",
                lambda: exists("ATT/tests/test_patch31.py")),
            ("test_init_existe presente",
                lambda: contains("ATT/tests/test_patch31.py", "test_init_existe")),
            ("test_typo_removido presente",
                lambda: contains("ATT/tests/test_patch31.py", "test_typo_removido")),
            ("test_import_ui_models presente",
                lambda: contains("ATT/tests/test_patch31.py", "test_import_ui_models")),
        ],
    },
    {
        "id": "patch_32",
        "desc": "Auditoria de wiring da UI (legado vs canonico)",
        "checks": [
            ("ATT/patches/patch_32_audit_ui_wiring.py existe",
                lambda: exists("ATT/patches/patch_32_audit_ui_wiring.py")),
            ("LEGACY_TERMS definido no script",
                lambda: contains(
                    "ATT/patches/patch_32_audit_ui_wiring.py", "LEGACY_TERMS")),
            ("CANONICAL_TERMS definido no script",
                lambda: contains(
                    "ATT/patches/patch_32_audit_ui_wiring.py", "CANONICAL_TERMS")),
            ("classificar() implementado",
                lambda: contains(
                    "ATT/patches/patch_32_audit_ui_wiring.py", "def classificar")),
            ("gerar_markdown() implementado",
                lambda: contains(
                    "ATT/patches/patch_32_audit_ui_wiring.py", "def gerar_markdown")),
            ("scripts/72_smoke_patch32_ui_audit.py existe",
                lambda: exists("scripts/72_smoke_patch32_ui_audit.py")),
        ],
    },
    {
        "id": "patch_33",
        "desc": "Migration: structure_id em payoff_curve_points e payoff_curve_summary",
        "checks": [
            ("db/migrations/run_patch_33.py existe",
                lambda: exists("db/migrations/run_patch_33.py")),
            ("col_exists() implementado",
                lambda: contains("db/migrations/run_patch_33.py", "def col_exists")),
            ("ADD COLUMN structure_id em payoff_curve_points",
                lambda: contains(
                    "db/migrations/run_patch_33.py",
                    "payoff_curve_points ADD COLUMN structure_id")),
            ("ADD COLUMN structure_id em payoff_curve_summary",
                lambda: contains(
                    "db/migrations/run_patch_33.py",
                    "payoff_curve_summary ADD COLUMN structure_id")),
            ("BACKFILL via structure_decisions implementado",
                lambda: contains(
                    "db/migrations/run_patch_33.py", "structure_decisions")),
            ("Índice idx_payoff_points_sid_ts definido",
                lambda: contains(
                    "db/migrations/run_patch_33.py", "idx_payoff_points_sid_ts")),
            ("Índice idx_payoff_summary_sid_ts definido",
                lambda: contains(
                    "db/migrations/run_patch_33.py", "idx_payoff_summary_sid_ts")),
            ("ATT/tests/test_patch33.py existe",
                lambda: exists("ATT/tests/test_patch33.py")),
        ],
    },


]  # ← fechamento da lista PATCHES


# ------------------------------------------------------------------
# Definicao dos bancos esperados
# ------------------------------------------------------------------

DATABASES = [
    {
        "path": "dados/app.db",
        "tables": [
            "structures",
            "structure_legs",
            "pricing_executions",
            "rtd_analise_robo",
            "rtd_analise_robo_legs",
            "manual_analise_robo_legs",
            "rtd_configuracoes",
            "rtd_consolidacoes",
        ],
    },
    {
        "path": "dados/derived.db",
        "tables": [
            "payoff_curve_points",
            "payoff_curve_summary",
            "structure_decisions",
        ],
    },
]

# ------------------------------------------------------------------
# Servicos fase 3A
# ------------------------------------------------------------------

FASE_3A_SERVICES = [
    "services/structure_input_mapper.py",
    "services/market_snapshot_provider.py",
    "services/market_snapshot_selector.py",
    "services/canonical_input_service.py",
    "services/pricing_execution_service.py",
    "services/pricing_execution_app_service.py",
    "domain/market_snapshot.py",
    "repositories/market_snapshot_repository.py",
]


# ------------------------------------------------------------------
# Runners
# ------------------------------------------------------------------

def run_patches():
    results = []
    for patch in PATCHES:
        checks = patch["checks"]
        passed = 0
        details = []
        for check in checks:
            label = check[0]
            fn    = check[1]
            extra = check[2] if len(check) > 2 else None
            ok    = fn()
            if ok:
                passed += 1
            note = ""
            if extra:
                try:
                    note = extra()
                except Exception:
                    note = ""
            details.append((label, ok, note))
        results.append({
            "id":      patch["id"],
            "desc":    patch["desc"],
            "passed":  passed,
            "total":   len(checks),
            "details": details,
        })
    return results


def run_databases():
    results = []
    for db in DATABASES:
        db_path = p(db["path"])
        if not os.path.isfile(db_path):
            results.append({"path": db["path"], "exists": False, "tables": []})
            continue
        try:
            conn = sqlite3.connect(db_path)
            cur  = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            found  = {r[0] for r in cur.fetchall()}
            conn.close()
        except Exception:
            found = set()
        table_results = []
        for t in db["tables"]:
            table_results.append((t, t in found))
        results.append({
            "path":   db["path"],
            "exists": True,
            "tables": table_results,
            "found":  sorted(found),
        })
    return results


def run_fase3a():
    return [(f, exists(f)) for f in FASE_3A_SERVICES]


def find_bak_files():
    bak = []
    for root, _, files in os.walk(ROOT):
        for f in files:
            if f.endswith(".bak"):
                full = os.path.join(root, f)
                bak.append(os.path.relpath(full, ROOT))
    return sorted(bak)


def find_loose_dbs():
    loose = []
    dados = os.path.join(ROOT, "dados")
    for root, _, files in os.walk(ROOT):
        if root.startswith(dados):
            continue
        for f in files:
            if f.endswith(".db") or f.endswith(".sqlite3"):
                full = os.path.join(root, f)
                loose.append(os.path.relpath(full, ROOT))
    return sorted(loose)


def find_py_files():
    py = []
    for root, _, files in os.walk(ROOT):
        for f in files:
            if f.endswith(".py"):
                full = os.path.join(root, f)
                py.append(os.path.relpath(full, ROOT))
    return sorted(py)


# ------------------------------------------------------------------
# Relatorio
# ------------------------------------------------------------------

def generate_report():
    ts     = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = []
    SEP    = "=" * 70

    report.append(SEP)
    report.append("  AUDITORIA DE PATCHES - PROJETO ATT")
    report.append(f"  Gerado em : {ts}")
    report.append(f"  Raiz      : {ROOT}")
    report.append(SEP)

    # ---- patches ----
    report.append("\n-- PATCHES " + "-" * 56)
    patch_results = run_patches()
    ok_count      = 0
    partial_count = 0
    fail_count    = 0

    for r in patch_results:
        if r["passed"] == r["total"]:
            status = "OK "
            ok_count += 1
        elif r["passed"] > 0:
            status = "PARCIAL"
            partial_count += 1
        else:
            status = "FALHOU"
            fail_count += 1

        marker = "OK" if status == "OK " else "!!"
        report.append(
            f"\n  {'✅' if status == 'OK ' else '⚠️ '} {marker}  "
            f"{r['id']:<12} [{r['passed']}/{r['total']}]"
            f"     {r['desc']}"
        )
        for label, ok, note in r["details"]:
            tick = "v" if ok else "X"
            line = f"    {tick}  {label}"
            if note:
                line += f"\n         -> {note}"
            report.append(line)

    report.append(
        f"\n\n  Resumo patches: {ok_count} OK | "
        f"{partial_count} PARCIAL | {fail_count} FALHOU | "
        f"{ok_count + partial_count + fail_count} total"
    )

    # ---- bancos ----
    report.append("\n-- BANCOS DE DADOS " + "-" * 48)
    for db in run_databases():
        report.append(
            f"\n  {'✅' if db['exists'] else '❌'}  {db['path']}  ->  "
            f"{'✅ existe' if db['exists'] else '❌ NAO ENCONTRADO'}"
        )
        if db["exists"]:
            found_str = ", ".join(db["found"])
            report.append(f"    Tabelas encontradas : {found_str}")
            all_ok = all(ok for _, ok in db["tables"])
            if all_ok:
                report.append("    v  Todas as tabelas esperadas presentes")
            else:
                for t, ok in db["tables"]:
                    if not ok:
                        report.append(f"    X  FALTANDO: {t}")

    # ---- servicos fase 3a ----
    report.append("\n-- SERVICOS FASE 3A " + "-" * 47)
    for path, ok in run_fase3a():
        icon = "✅" if ok else "❌"
        report.append(f"\n  {icon}  {path}")

    # ---- bak ----
    report.append("\n-- ARQUIVOS .BAK (divida tecnica) " + "-" * 33)
    for f in find_bak_files():
        report.append(f"\n  !!  {f}")

    # ---- dbs soltos ----
    report.append("\n-- BANCOS SOLTOS FORA DE dados/ " + "-" * 35)
    for f in find_loose_dbs():
        report.append(f"\n  !!  {f}")

    # ---- inventario py ----
    report.append("\n-- INVENTARIO DE ARQUIVOS .PY NO PROJETO " + "-" * 26)
    for f in find_py_files():
        report.append(f"\n  PY  {f}")

    report.append("\n" + SEP)
    return "\n".join(report)


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Auditoria de patches ATT")
    parser.add_argument("-v", "--verbose", action="store_true", help="Saida detalhada")
    parser.add_argument("--output", default=None, help="Caminho do arquivo de saida (.md)")
    args = parser.parse_args()

    text = generate_report()
    print(text)

    if args.output:
        output_path = args.output
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    else:
        output_dir  = p("scripts")
        ts_file     = datetime.now().strftime("%Y%m%d_%H%M")
        output_path = os.path.join(output_dir, f"auditoria_{ts_file}.md")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"\nRelatorio salvo em: {output_path}")
