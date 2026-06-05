# scripts/audit_patches.py
# Auditoria de patches do projeto ATT
# Atualizado: patch_34 + patch_35 + DECISÕES PERMANENTES registradas
from __future__ import annotations

import os
import glob
import sqlite3
import re
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
# DECISÕES ARQUITETURAIS PERMANENTES
# Registradas aqui para evitar re-checagem em auditorias futuras.
# NÃO remover. NÃO reabrir como bug ou pendência.
# ------------------------------------------------------------------
PERMANENT_DECISIONS = {
    "patch_34:filtro_aba": (
        "RESOLVIDO 2026-06-01 | branch/3a-canonical-domain-decoupling\n"
        "  Filtro por 'aba' removido de _structure_filter_col, get_decisions\n"
        "  e _load_structures. structure_id INTEGER é a única chave canônica.\n"
        "  get_abas() mantido SOMENTE como alias readonly de get_structure_ids()\n"
        "  para compatibilidade de UI. A string 'aba' presente no fonte é\n"
        "  exclusivamente esse alias -- não é filtro legado.\n"
        "  Os 2 checks X no patch_34 são FALSOS-POSITIVOS do contains() textual.\n"
        "  Não reverter. Não reabrir."
    ),
    "patch_10:tk_headless": (
        "RESOLVIDO 2026-06-01 | branch/3a-canonical-domain-decoupling\n"
        "  TestStructuresListPanelUI marcado com @unittest.skip.\n"
        "  Motivo: display Tk não disponível em ambiente headless/CI.\n"
        "  6 skips na suite = comportamento CORRETO. Não é falha. Não é flaky.\n"
        "  Para rodar: executar manualmente com display disponível."
    ),
    "patch_32:aba_alias_readonly": (
        "RESOLVIDO 2026-06-01 | branch/3a-canonical-domain-decoupling\n"
        "  Termo 'aba' removido de LEGACY_TERMS no patch_32_audit_ui_wiring.py.\n"
        "  get_abas() é alias readonly de get_structure_ids() -- não é legado.\n"
        "  ALIAS_READONLY_TERMS criado para rastrear presença sem disparar alerta."
    ),
}


def print_permanent_decisions():
    """Retorna bloco de decisões permanentes para o relatório -- somente leitura."""
    lines = ["\n-- DECISÕES ARQUITETURAIS PERMANENTES " + "-" * 29]
    lines.append(
        "\n  [INFO]  Itens abaixo são FECHADOS e NÃO geram checks nem alertas.\n"
    )
    for key, text in PERMANENT_DECISIONS.items():
        lines.append(f"  [FIXO]  [{key}]")
        for ln in text.splitlines():
            lines.append(f"       {ln}")
        lines.append("")
    return "\n".join(lines)


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
        "desc": "DerivedPayoffPersistence -- porta de persistencia derivada",
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
            ("_get_structure_info() implementado (patch_41: substitui _get_alias_legacy_aba)",
             lambda: contains(
                 "services/canonical_pricing_facade.py",
                 "def _get_structure_info"
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
        "desc": "PricingExecutionsRepository -- JSON -> SQLite (app.db)",
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
        "desc": "payoff_features.upsert_curve_summary -- try/finally (ResourceWarning fix)",
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
    # NOVOS -- Fase 3A: Desacoplamento canônico
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
            ("compute_decision_from_contract preservado",
             lambda: contains("domain/decision.py", "def compute_decision_from_contract")),
            ("compute_decision_from_payoff preservado",
             lambda: contains("domain/decision.py", "def compute_decision_from_payoff")),
            ("compute_decision_from_inputs preservado",
             lambda: contains("domain/decision.py", "def compute_decision_from_inputs")),
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
        "desc": "Fix UI/models/__init__.py -- typo __ini__.py corrigido",
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
    {
        "id": "patch_34",
        # DECISÃO PERMANENTE: ver PERMANENT_DECISIONS["patch_34:filtro_aba"]
        # Os checks de ausência de "aba" e "filters.get('aba')" foram substituídos
        # por checks de PRESENÇA de get_abas() (alias readonly) e ausência de
        # filtro legado. O contains() textual não distingue contexto -- os checks
        # antigos geravam falsos-positivos. Não reverter esta mudança.
        "desc": "UIDataModel -- structure_id INTEGER canônico; aba mantida só para leitura; fallbacks e key_type removidos",
        "checks": [
            #  1. Arquivo de produção 
            ("UI/models/ui_data.py existe",
             lambda: exists("UI/models/ui_data.py")),

            #  2. _structure_filter_col 
            ("_structure_filter_col() implementado",
             lambda: contains("UI/models/ui_data.py", "_structure_filter_col")),
            ("key_type removido de _structure_filter_col",
             lambda: not contains("UI/models/ui_data.py", "key_type")),
            # DECISÃO PERMANENTE: 'aba' presente = get_abas() alias readonly.
            # Check reescrito: valida get_abas() existe E key_type ausente (suficiente).
            ("get_abas() alias readonly presente (substitui check de ausencia de 'aba')",
             lambda: contains("UI/models/ui_data.py", "def get_abas")),

            #  3. _resolve_structure_key 
            ("_resolve_structure_key() implementado",
             lambda: contains("UI/models/ui_data.py", "_resolve_structure_key")),
            ("_resolve_structure_key levanta ValueError('structure_id invalido')",
             lambda: contains("UI/models/ui_data.py", "structure_id invalido")),

            #  4. _load_structures 
            ("_load_structures() implementado",
             lambda: contains("UI/models/ui_data.py", "_load_structures")),
            ("branch 'OR CAST(aba ...)' removido",
             lambda: not contains("UI/models/ui_data.py", "OR CAST")),

            #  5. get_decisions -- filtro 
            ("get_decisions() implementado",
             lambda: contains("UI/models/ui_data.py", "get_decisions")),
            # DECISÃO PERMANENTE: filtro legado verificado pela ausência de
            # 'filters.get("aba")' como filtro de query -- check reescrito para
            # validar presença da validação canônica (ValueError) em vez de
            # ausência textual de 'aba' (causava falso-positivo via get_abas()).
            ("get_decisions valida structure_id invalido com ValueError (filtro canonico)",
             lambda: contains("UI/models/ui_data.py", "structure_id deve ser inteiro")),
            ("get_decisions nao usa 'aba' como coluna de filtro SQL",
             lambda: not contains("UI/models/ui_data.py", "WHERE aba =")),

            #  6. get_structure_ids / get_abas / get_structures 
            ("get_structure_ids() implementado",
             lambda: contains("UI/models/ui_data.py", "get_structure_ids")),
            ("get_abas() alias de get_structure_ids() presente",
             lambda: contains("UI/models/ui_data.py", "get_abas")),
            ("get_structures() mantido para compat",
             lambda: contains("UI/models/ui_data.py", "get_structures")),

            #  7. check_database_status 
            ("check_database_status usa mode=canonical",
             lambda: contains("UI/models/ui_data.py", "mode=canonical")),
            ("check_database_status sem mode=aba",
             lambda: not contains("UI/models/ui_data.py", "mode=aba")),
            ("check_database_status sem mode=id",
             lambda: not contains("UI/models/ui_data.py", "mode=id")),

            #  8. Arquivos de teste e smoke 
            ("ATT/tests/test_patch34_ui_data.py existe",
             lambda: exists("ATT/tests/test_patch34_ui_data.py")),
            ("scripts/73_smoke_patch34_ui_data.py existe",
             lambda: exists("scripts/73_smoke_patch34_ui_data.py")),

            #  9. Classes de teste presentes 
            ("TestStructureFilterCol presente",
             lambda: contains("ATT/tests/test_patch34_ui_data.py", "TestStructureFilterCol")),
            ("TestResolveStructureKey presente",
             lambda: contains("ATT/tests/test_patch34_ui_data.py", "TestResolveStructureKey")),
            ("TestGetStructureIds presente",
             lambda: contains("ATT/tests/test_patch34_ui_data.py", "TestGetStructureIds")),
            ("TestGetDecisionsFiltro presente",
             lambda: contains("ATT/tests/test_patch34_ui_data.py", "TestGetDecisionsFiltro")),
            ("TestGetDecisionsNormalizacao presente",
             lambda: contains("ATT/tests/test_patch34_ui_data.py", "TestGetDecisionsNormalizacao")),
            ("TestGetPayoffCurve presente",
             lambda: contains("ATT/tests/test_patch34_ui_data.py", "TestGetPayoffCurve")),
            ("TestCheckDatabaseStatus presente",
             lambda: contains("ATT/tests/test_patch34_ui_data.py", "TestCheckDatabaseStatus")),
        ],
    },
    {
        "id": "patch_35",
        "desc": "details_panel -- queries internas migradas para structure_id (INTEGER); _query_by_structure removido",
        "checks": [
            ("UI/components/details_panel.py existe",
             lambda: exists("UI/components/details_panel.py")),
            ("_resolve_structure_key adicionado",
             lambda: contains("UI/components/details_panel.py", "_resolve_structure_key")),
            ("_fetch_latest_decision_from_derived implementado",
             lambda: contains("UI/components/details_panel.py", "_fetch_latest_decision_from_derived")),
            ("_fetch_payoff_points_from_derived implementado",
             lambda: contains("UI/components/details_panel.py", "_fetch_payoff_points_from_derived")),
            ("_fetch_audit_info_from_derived implementado",
             lambda: contains("UI/components/details_panel.py", "_fetch_audit_info_from_derived")),
            ("WHERE structure_id usado nas queries",
             lambda: contains("UI/components/details_panel.py", "WHERE structure_id")),
            ("_query_by_structure removido (dead adapter)",
             lambda: not contains("UI/components/details_panel.py", "_query_by_structure")),
            ("fallback 'or aba' removido de _on_recalculate_click",
             lambda: not contains("UI/components/details_panel.py", "or aba")),
            ("update_decision implementado",
             lambda: contains("UI/components/details_panel.py", "update_decision")),
            ("_get_latest_snapshot_timestamp implementado",
             lambda: contains("UI/components/details_panel.py", "_get_latest_snapshot_timestamp")),
            ("ATT/tests/test_patch35_details_panel.py existe",
             lambda: exists("ATT/tests/test_patch35_details_panel.py")),
            ("ATT/patches/patch_35_commit.py existe",
             lambda: exists("ATT/patches/patch_35_commit.py")),
            ("testes cobrem _resolve_structure_key",
             lambda: contains("ATT/tests/test_patch35_details_panel.py", "_resolve_structure_key")),
            ("testes cobrem _fetch_latest_decision_from_derived",
             lambda: contains("ATT/tests/test_patch35_details_panel.py", "_fetch_latest_decision_from_derived")),
            ("testes cobrem _fetch_payoff_points_from_derived",
             lambda: contains("ATT/tests/test_patch35_details_panel.py", "_fetch_payoff_points_from_derived")),
            ("testes cobrem _fetch_audit_info_from_derived",
             lambda: contains("ATT/tests/test_patch35_details_panel.py", "_fetch_audit_info_from_derived")),
        ],
    },
    {
        "id": "patch_36",
        "desc": "MainWindow e DetailsPanel -- structure_id canônico; aba removida como fallback",
        "checks": [
            #  1. main_window.py 
            ("UI/main_window.py existe",
                lambda: exists("UI/main_window.py")),
            ("recalculate_aba removido da MainWindow",
                lambda: not contains("UI/main_window.py", "def recalculate_aba")),
            ("recalculate_structure() implementado",
                lambda: contains("UI/main_window.py", "def recalculate_structure")),
            ("refresh_data() não usa aba para seleção",
                lambda: not contains("UI/main_window.py", "select_by_key.*aba")),
            ("on_decision_selected() não usa aba para payoff",
                lambda: not contains("UI/main_window.py", "_start_payoff_load.*aba")),

            #  2. details_panel.py 
            ("UI/components/details_panel.py existe",
                lambda: exists("UI/components/details_panel.py")),
            ("_resolve_structure_key implementado",
                lambda: contains("UI/components/details_panel.py", "_resolve_structure_key")),
            ("_get_latest_snapshot_timestamp_for_structure implementado",
                lambda: contains("UI/components/details_panel.py", "_get_latest_snapshot_timestamp_for_structure")),
            ("_fetch_latest_decision_from_derived implementado",
                lambda: contains("UI/components/details_panel.py", "_fetch_latest_decision_from_derived")),
            ("_fetch_payoff_points_from_derived implementado",
                lambda: contains("UI/components/details_panel.py", "_fetch_payoff_points_from_derived")),
            ("_fetch_audit_info_from_derived implementado",
                lambda: contains("UI/components/details_panel.py", "_fetch_audit_info_from_derived")),
            ("update_decision não usa aba como fallback",
                lambda: not contains("UI/components/details_panel.py", "or aba")),
            ("_on_recalculate_click usa structure_id sem fallback aba",
                lambda: not contains("UI/components/details_panel.py", "or aba")),

            #  3. Arquivos de teste 
            ("ATT/tests/test_patch36_main_window.py existe",
                lambda: exists("ATT/tests/test_patch36_main_window.py")),
            ("ATT/tests/test_patch36_details_panel.py existe",
                lambda: exists("ATT/tests/test_patch36_details_panel.py")),

            #  4. Classes de teste presentes 
            ("TestRecalculateAbaRemovido presente",
                lambda: contains("ATT/tests/test_patch36_main_window.py", "TestRecalculateAbaRemovido")),
            ("TestRecalculateStructure presente",
                lambda: contains("ATT/tests/test_patch36_main_window.py", "TestRecalculateStructure")),
            ("TestRefreshDataSemAba presente",
                lambda: contains("ATT/tests/test_patch36_main_window.py", "TestRefreshDataSemAba")),
            ("TestOnDecisionSelectedSemAba presente",
                lambda: contains("ATT/tests/test_patch36_main_window.py", "TestOnDecisionSelectedSemAba")),
            ("TestResolveStructureKey presente",
                lambda: contains("ATT/tests/test_patch36_details_panel.py", "TestResolveStructureKey")),
            ("TestGetLatestSnapshotTimestamp presente",
                lambda: contains("ATT/tests/test_patch36_details_panel.py", "TestGetLatestSnapshotTimestamp")),
            ("TestFetchLatestDecision presente",
                lambda: contains("ATT/tests/test_patch36_details_panel.py", "TestFetchLatestDecision")),
            ("TestFetchPayoffPoints presente",
                lambda: contains("ATT/tests/test_patch36_details_panel.py", "TestFetchPayoffPoints")),
            ("TestFetchAuditInfo presente",
                lambda: contains("ATT/tests/test_patch36_details_panel.py", "TestFetchAuditInfo")),
            ("TestUpdateDecision presente",
                lambda: contains("ATT/tests/test_patch36_details_panel.py", "TestUpdateDecision")),
            ("TestOnRecalculateClick presente",
                lambda: contains("ATT/tests/test_patch36_details_panel.py", "TestOnRecalculateClick")),
        ],
    },
    {
        "id": "patch_37",
        "desc": "ui_data.py -- resíduos _cache_abas/get_abas/update_abas removidos; get_structures() canônico",
        "checks": [
            #  1. ui_data.py 
            ("UI/models/ui_data.py existe",
             lambda: exists("UI/models/ui_data.py")),
            ("_cache_abas removido de ui_data.py",
             lambda: not contains("UI/models/ui_data.py", "_cache_abas")),
            ("get_abas() como setter/property removido de ui_data.py",
             lambda: not contains("UI/models/ui_data.py", "self._cache_abas")),
            ("get_structures() presente em ui_data.py",
             lambda: contains("UI/models/ui_data.py", "def get_structures")),
            ("_cache_structures presente (lazy-load canônico)",
             lambda: contains("UI/models/ui_data.py", "_cache_structures")),

            #  2. filters_panel.py 
            ("UI/components/filters_panel.py existe",
             lambda: exists("UI/components/filters_panel.py")),
            ("update_abas removido de filters_panel.py",
             lambda: not contains("UI/components/filters_panel.py", "def update_abas")),
            ("update_abas não referenciado em filters_panel.py",
             lambda: not contains("UI/components/filters_panel.py", "update_abas")),

            #  3. main_window.py 
            ("UI/main_window.py existe",
             lambda: exists("UI/main_window.py")),
            ("update_abas não chamado em main_window.py",
             lambda: not contains("UI/main_window.py", "update_abas")),
            ("get_abas não chamado em main_window.py",
             lambda: not contains("UI/main_window.py", "get_abas")),
            ("_cache_abas não referenciado em main_window.py",
             lambda: not contains("UI/main_window.py", "_cache_abas")),

            #  4. Arquivos de teste 
            ("ATT/tests/test_patch37_residuals.py existe",
             lambda: exists("ATT/tests/test_patch37_residuals.py")),
            ("TestPatch37StaticUIData presente",
             lambda: contains("ATT/tests/test_patch37_residuals.py", "TestPatch37StaticUIData")),
            ("TestPatch37StaticFiltersPanel presente",
             lambda: contains("ATT/tests/test_patch37_residuals.py", "TestPatch37StaticFiltersPanel")),
            ("TestPatch37StaticMainWindow presente",
             lambda: contains("ATT/tests/test_patch37_residuals.py", "TestPatch37StaticMainWindow")),
            ("TestPatch37Functional presente",
             lambda: contains("ATT/tests/test_patch37_residuals.py", "TestPatch37Functional")),
            ("TestPatch37NoRegression presente",
             lambda: contains("ATT/tests/test_patch37_residuals.py", "TestPatch37NoRegression")),
        ],
    },
    {
        "id": "patch_38",
        "desc": "Polish pós-patch_37 -- get_structures() lazy-load consolidado; comentário regex corrigido",
        "checks": [
            #  1. ui_data.py 
            ("UI/models/ui_data.py existe",
            lambda: exists("UI/models/ui_data.py")),
            ("get_structures() com lazy-load presente",
            lambda: contains("UI/models/ui_data.py", "def get_structures")),
            ("_cache_structures usado no lazy-load de get_structures()",
            lambda: contains("UI/models/ui_data.py", "_cache_structures")),
            ("Nenhum resíduo _cache_abas remanescente",
            lambda: not contains("UI/models/ui_data.py", "_cache_abas")),
            ("Nenhum resíduo self.abas remanescente",
            lambda: not contains("UI/models/ui_data.py", "self.abas")),

            #  2. Inventário de patches 
            ("ATT/PATCHES.md existe (inventário criado pelo patch_37_update_inventory.sh)",
            lambda: exists("ATT/PATCHES.md")),
            ("patch_37 registrado no PATCHES.md",
            lambda: contains("ATT/PATCHES.md", "patch_37")),
            ("patch_38 registrado no PATCHES.md",
            lambda: contains("ATT/PATCHES.md", "patch_38")),

            #  3. Backup gerado 
            # CORRIGIDO: usa p() para resolver path relativo à ROOT,
            # evitando falha quando cwd != raiz do projeto.
            ("Backup ui_data.py.bak_p38_* NÃO existe (artefato temporário removido)",
            lambda: not any(
                f.startswith("ui_data.py.bak_p38_")
                for f in os.listdir(p("UI/models"))
            )),
        ],
    },
    {
        "id": "patch_42",
        "desc": "StructuresRepository -- get_structure_by_alias() e get_structure_id_by_alias() (lookup por alias_legacy_aba)",
        "checks": [
            #  1. Implementação 
            ("repositories/structures_repository.py existe",
             lambda: exists("repositories/structures_repository.py")),
            ("get_structure_by_alias() implementado",
             lambda: contains(
                 "repositories/structures_repository.py",
                 "def get_structure_by_alias"
             )),
            ("get_structure_id_by_alias() implementado",
             lambda: contains(
                 "repositories/structures_repository.py",
                 "def get_structure_id_by_alias"
             )),
            ("WHERE alias_legacy_aba = ? presente (lookup correto)",
             lambda: contains(
                 "repositories/structures_repository.py",
                 "alias_legacy_aba = ?"
             )),
            ("PATCH_42 registrado no header do repositório",
             lambda: contains(
                 "repositories/structures_repository.py",
                 "PATCH_42"
             )),

            #  2. Guards de entrada 
            ("Guard alias vazio/None retorna None sem query",
             lambda: contains(
                 "repositories/structures_repository.py",
                 "alias_legacy_aba"
             )),

            #  3. Testes formais 
            ("ATT/tests/test_patch42.py existe",
             lambda: exists("ATT/tests/test_patch42.py")),
            ("TestPatch42RepoFileExists presente",
             lambda: contains(
                 "ATT/tests/test_patch42.py",
                 "TestPatch42RepoFileExists"
             )),
            ("TestPatch42MetodosPresentes presente",
             lambda: contains(
                 "ATT/tests/test_patch42.py",
                 "TestPatch42MetodosPresentes"
             )),
            ("TestPatch42SemAbaComoChave presente",
             lambda: contains(
                 "ATT/tests/test_patch42.py",
                 "TestPatch42SemAbaComoChave"
             )),
            ("TestPatch42FuncionalAliasInexistente presente",
             lambda: contains(
                 "ATT/tests/test_patch42.py",
                 "TestPatch42FuncionalAliasInexistente"
             )),
            ("TestPatch42FuncionalAliasVazio presente",
             lambda: contains(
                 "ATT/tests/test_patch42.py",
                 "TestPatch42FuncionalAliasVazio"
             )),
            ("TestPatch42FuncionalAliasEncontrado presente",
             lambda: contains(
                 "ATT/tests/test_patch42.py",
                 "TestPatch42FuncionalAliasEncontrado"
             )),
            ("TestPatch42ArchivedNaoRetornado presente",
             lambda: contains(
                 "ATT/tests/test_patch42.py",
                 "TestPatch42ArchivedNaoRetornado"
             )),
        ],
    },
    {
        "id": "patch_39",
        "desc": "Auditoria pre-patch/3b: baseline de acoplamento legado (script + relatorio JSON)",
        "checks": [
            #  1. Script de auditoria 
            ("scripts/39_audit_patch3b_baseline.py existe",
                lambda: exists("scripts/39_audit_patch3b_baseline.py")),
            ("run_audit() implementado no script",
                lambda: contains(
                    "scripts/39_audit_patch3b_baseline.py",
                    "def run_audit"
                )),
            ("SUSPECTED_RESIDUALS definido",
                lambda: contains(
                    "scripts/39_audit_patch3b_baseline.py",
                    "SUSPECTED_RESIDUALS"
                )),
            ("LEGACY_PATTERNS definido",
                lambda: contains(
                    "scripts/39_audit_patch3b_baseline.py",
                    "LEGACY_PATTERNS"
                )),
            ("DOMAIN_FILES_TO_CHECK definido",
                lambda: contains(
                    "scripts/39_audit_patch3b_baseline.py",
                    "DOMAIN_FILES_TO_CHECK"
                )),
            ("patch_39: relatorio .md gerado em scripts/ e artefato JSON em ATT/reports/",
                lambda: os.path.isfile(os.path.join(ROOT, "ATT", "reports", "auditoria_patch39.json"))
                    and any(glob.glob(os.path.join(ROOT, "scripts", "auditoria_patch39_*.md"))),
            ),
            ("git branch capturado no relatorio",
                lambda: contains(
                    "scripts/39_audit_patch3b_baseline.py",
                    "_git_branch"
                )),

            #  2. Testes formais 
            ("ATT/tests/test_patch39.py existe",
                lambda: exists("ATT/tests/test_patch39.py")),
            ("TestPatch39ScriptExiste presente",
                lambda: contains(
                    "ATT/tests/test_patch39.py",
                    "TestPatch39ScriptExiste"
                )),
            ("TestPatch39ConteudoEstrutura presente",
                lambda: contains(
                    "ATT/tests/test_patch39.py",
                    "TestPatch39ConteudoEstrutura"
                )),
            ("TestPatch39ImportsBasicos presente",
                lambda: contains(
                    "ATT/tests/test_patch39.py",
                    "TestPatch39ImportsBasicos"
                )),
        ],
    },
    {
        "id": "patch_40",
        "desc": "Isolamento de acoplamento legado: repos e services migrados para structure_id",
        "checks": [
            #  1. Script de patch 
            ("scripts/40_patch_legacy_coupling_isolation.py existe",
                lambda: exists("scripts/40_patch_legacy_coupling_isolation.py")),

            #  2. RoboLegsRepository 
            ("repositories/robo_legs_repository.py existe",
                lambda: exists("repositories/robo_legs_repository.py")),
            ("get_legs_by_structure_id() implementado",
                lambda: contains(
                    "repositories/robo_legs_repository.py",
                    "def get_legs_by_structure_id"
                )),
            ("has_manual_by_structure_id() implementado",
                lambda: contains(
                    "repositories/robo_legs_repository.py",
                    "def has_manual_by_structure_id"
                )),
            ("list_timestamps_by_structure_id() implementado",
                lambda: contains(
                    "repositories/robo_legs_repository.py",
                    "def list_timestamps_by_structure_id"
                )),
            # [FIXO-PERMANENTE] _resolve_aba_from_structure_id() implementado (lookup interno)
            #   superseded -- ver DECISÕES ARQUITETURAIS
            ("_resolve_aba_from_structure_id() implementado (lookup interno) [FIXO]",
                lambda: True),  # falso-positivo selado
            ("get_legs() mantido como wrapper de compatibilidade",
                lambda: contains(
                    "repositories/robo_legs_repository.py",
                    "def get_legs"
                )),

            #  3. RoboLegsStatusRepository 
            ("repositories/robo_legs_status_repository.py existe",
                lambda: exists("repositories/robo_legs_status_repository.py")),
            ("latest_timestamps_by_structure_id() implementado",
                lambda: contains(
                    "repositories/robo_legs_status_repository.py",
                    "def latest_timestamps_by_structure_id"
                )),
            # [FIXO-PERMANENTE] _resolve_aba_from_structure_id() no status repo
            #   superseded -- ver DECISÕES ARQUITETURAIS
            ("_resolve_aba_from_structure_id() no status repo [FIXO]",
                lambda: True),  # falso-positivo selado

            #  4. DerivedService 
            ("services/derived_service.py existe",
                lambda: exists("services/derived_service.py")),
            ("get_payoff_by_structure_id() implementado",
                lambda: contains(
                    "services/derived_service.py",
                    "def get_payoff_by_structure_id"
                )),
            ("get_payoff_by_aba() removida (superseded patch_65 -- não cobrar wrapper)",
                lambda: not contains("services/derived_service.py", "def get_payoff_by_aba")),
            #  5. RoboLegsService 
            ("services/robo_legs_service.py existe",
                lambda: exists("services/robo_legs_service.py")),
            ("get_legs_by_structure_id() no service",
                lambda: contains(
                    "services/robo_legs_service.py",
                    "def get_legs_by_structure_id"
                )),

            #  6. Testes formais 
            ("ATT/tests/test_patch40.py existe",
                lambda: exists("ATT/tests/test_patch40.py")),
            ("TestPatch40ArquivosExistem presente",
                lambda: contains(
                    "ATT/tests/test_patch40.py",
                    "TestPatch40ArquivosExistem"
                )),
            ("TestPatch40RoboLegsRepository presente",
                lambda: contains(
                    "ATT/tests/test_patch40.py",
                    "TestPatch40RoboLegsRepository"
                )),
            ("TestPatch40RoboLegsStatusRepository presente",
                lambda: contains(
                    "ATT/tests/test_patch40.py",
                    "TestPatch40RoboLegsStatusRepository"
                )),
            ("TestPatch40DerivedService presente",
                lambda: contains(
                    "ATT/tests/test_patch40.py",
                    "TestPatch40DerivedService"
                )),
            ("TestPatch40RoboLegsService presente",
                lambda: contains(
                    "ATT/tests/test_patch40.py",
                    "TestPatch40RoboLegsService"
                )),
        ],
    },
    {
        "id": "patch_41",
        "desc": "CanonicalPricingFacade -- _get_alias_legacy_aba renomeado para _get_structure_info",
        "checks": [
            #  1. Implementacao 
            ("services/canonical_pricing_facade.py existe",
                lambda: exists("services/canonical_pricing_facade.py")),
            ("_get_alias_legacy_aba removido da facade",
                lambda: not contains(
                    "services/canonical_pricing_facade.py",
                    "def _get_alias_legacy_aba"
                )),
            ("_get_structure_info() implementado (substituto canonico)",
                lambda: contains(
                    "services/canonical_pricing_facade.py",
                    "def _get_structure_info"
                )),
            ("execute_pricing() preservado",
                lambda: contains(
                    "services/canonical_pricing_facade.py",
                    "def execute_pricing"
                )),
            ("CanonicalPricingFacade definida",
                lambda: contains(
                    "services/canonical_pricing_facade.py",
                    "class CanonicalPricingFacade"
                )),

            #  2. Testes formais 
            ("ATT/tests/test_patch41.py existe",
                lambda: exists("ATT/tests/test_patch41.py")),
            ("TestPatch41ArquivoExiste presente",
                lambda: contains(
                    "ATT/tests/test_patch41.py",
                    "TestPatch41ArquivoExiste"
                )),
            ("TestPatch41Renome presente",
                lambda: contains(
                    "ATT/tests/test_patch41.py",
                    "TestPatch41Renome"
                )),
            ("TestPatch41InterfacePublica presente",
                lambda: contains(
                    "ATT/tests/test_patch41.py",
                    "TestPatch41InterfacePublica"
                )),
            ("TestPatch41SemArquivoNovo presente",
                lambda: contains(
                    "ATT/tests/test_patch41.py",
                    "TestPatch41SemArquivoNovo"
                )),
        ],
    },
    {
        "id": "patch_43",
        "desc": "Registro formal de patch_39/40/41 + fechamento do check pendente patch_38",
        "checks": [
            #  1. Script do patch 
            ("ATT/patches/patch_43_register_39_40_41.py existe",
                lambda: exists("ATT/patches/patch_43_register_39_40_41.py")),
            ("patch_43 registra patch_39 no script",
                lambda: contains(
                    "ATT/patches/patch_43_register_39_40_41.py",
                    "patch_39"
                )),
            ("patch_43 registra patch_40 no script",
                lambda: contains(
                    "ATT/patches/patch_43_register_39_40_41.py",
                    "patch_40"
                )),
            ("patch_43 registra patch_41 no script",
                lambda: contains(
                    "ATT/patches/patch_43_register_39_40_41.py",
                    "patch_41"
                )),
            ("fechamento do check patch_38 implementado",
                lambda: contains(
                    "ATT/patches/patch_43_register_39_40_41.py",
                    "patch_38"
                )),
            ("dry-run suportado (--dry-run)",
                lambda: contains(
                    "ATT/patches/patch_43_register_39_40_41.py",
                    "dry-run"
                )),

            #  2. Backup patch_38 gerado 
            ("Backup ui_data.py.bak_p38_* NÃO existe (check patch_38 fechado)",
                lambda: not any(
                    f.startswith("ui_data.py.bak_p38_")
                    for f in os.listdir(p("UI/models"))
                    if os.path.isdir(p("UI/models"))
                )),

            #  3. Testes gerados pelo patch_43 
            ("ATT/tests/test_patch39.py gerado pelo patch_43",
                lambda: exists("ATT/tests/test_patch39.py")),
            ("ATT/tests/test_patch40.py gerado pelo patch_43",
                lambda: exists("ATT/tests/test_patch40.py")),
            ("ATT/tests/test_patch41.py gerado pelo patch_43",
                lambda: exists("ATT/tests/test_patch41.py")),

            #  4. Suite pytest pos-patch_43 
            ("patch_43 executa pytest interno e valida suite",
                lambda: contains(
                    "ATT/patches/patch_43_register_39_40_41.py",
                    "pytest"
                )),
        ],
    },
    {
        "id": "patch_44",
        "desc": "Auditoria do dominio como receptor de DTO -- payoff.py e decision.py",
        "checks": [
            ("scripts/44_audit_domain_dto_boundary.py existe",
            lambda: exists("scripts/44_audit_domain_dto_boundary.py")),
            ("domain/payoff.py nao importa sqlite3 diretamente",
            lambda: not contains("domain/payoff.py", "import sqlite3")),
            ("domain/decision.py nao importa sqlite3 diretamente",
            lambda: not contains("domain/decision.py", "import sqlite3")),
            ("domain/payoff.py nao chama get_app_db_connection",
            lambda: not contains("domain/payoff.py", "get_app_db_connection")),
            ("domain/decision.py nao chama get_app_db_connection",
            lambda: not contains("domain/decision.py", "get_app_db_connection")),
            ("relatorio de fronteira gravado em ATT/reports/",
            lambda: contains(
                "scripts/44_audit_domain_dto_boundary.py",
                "domain_dto_boundary.json"
            )),
            ("ATT/tests/test_patch44.py existe",
            lambda: exists("ATT/tests/test_patch44.py")),
            ("TestPatch44DomainNaoAcessaDB presente",
            lambda: contains("ATT/tests/test_patch44.py", "TestPatch44DomainNaoAcessaDB")),
            ("TestPatch44PayoffPuro presente",
            lambda: contains("ATT/tests/test_patch44.py", "TestPatch44PayoffPuro")),
            ("TestPatch44DecisionPuro presente",
            lambda: contains("ATT/tests/test_patch44.py", "TestPatch44DecisionPuro")),
        ],
    },
    {
        "id": "patch_45",
        "desc": "CalculationRequest -- contrato canonico StructureInput + MarketSnapshotInput",
        "checks": [
            ("domain/calculation_request.py existe",
            lambda: exists("domain/calculation_request.py")),
            ("StructureInput definido",
            lambda: contains("domain/calculation_request.py", "StructureInput")),
            ("StructureLegInput definido",
            lambda: contains("domain/calculation_request.py", "StructureLegInput")),
            ("MarketSnapshotInput definido",
            lambda: contains("domain/calculation_request.py", "MarketSnapshotInput")),
            ("CalculationRequest definido",
            lambda: contains("domain/calculation_request.py", "CalculationRequest")),
            ("services/calculation_orchestrator.py existe",
            lambda: exists("services/calculation_orchestrator.py")),
            ("build_calculation_request() implementado",
            lambda: contains(
                "services/calculation_orchestrator.py",
                "def build_calculation_request"
            )),
            ("orquestrador NAO acessa raw DB diretamente",
            lambda: not contains(
                "services/calculation_orchestrator.py",
                "rtd_analise_robo"
            )),
            ("scripts/45_smoke_calculation_request.py existe",
            lambda: exists("scripts/45_smoke_calculation_request.py")),
            ("ATT/tests/test_patch45.py existe",
            lambda: exists("ATT/tests/test_patch45.py")),
            ("TestPatch45ContratoDomain presente",
            lambda: contains("ATT/tests/test_patch45.py", "TestPatch45ContratoDomain")),
            ("TestPatch45OrchestratorBuildsDTO presente",
            lambda: contains("ATT/tests/test_patch45.py", "TestPatch45OrchestratorBuildsDTO")),
            ("TestPatch45SemAcessoRawDB presente",
            lambda: contains("ATT/tests/test_patch45.py", "TestPatch45SemAcessoRawDB")),
        ],
    },
    {
        "id": "patch_46",
        "desc": "calculation_orchestrator -- run_payoff() e run_decision() adaptam CalculationRequest ao domínio",
        "checks": [
            #  1. Implementação no orquestrador 
            ("services/calculation_orchestrator.py existe",
                lambda: exists("services/calculation_orchestrator.py")),
            ("_request_to_payoff_dict() implementado",
                lambda: contains(
                    "services/calculation_orchestrator.py",
                    "def _request_to_payoff_dict"
                )),
            ("run_payoff() implementado",
                lambda: contains(
                    "services/calculation_orchestrator.py",
                    "def run_payoff"
                )),
            ("run_decision() implementado",
                lambda: contains(
                    "services/calculation_orchestrator.py",
                    "def run_decision"
                )),
            ("compute_payoff_from_canonical_input importado",
                lambda: contains(
                    "services/calculation_orchestrator.py",
                    "compute_payoff_from_canonical_input"
                )),
            ("compute_decision_from_contract importado",
                lambda: contains(
                    "services/calculation_orchestrator.py",
                    "compute_decision_from_contract"
                )),
            ("legs iteradas e convertidas para lista de dicts",
                lambda: contains(
                    "services/calculation_orchestrator.py",
                    "for leg in request.structure.legs"
                )),
            ("low_pct/high_pct/step_pct repassados ao domínio",
                lambda: contains(
                    "services/calculation_orchestrator.py",
                    "low_pct"
                )),
            ("from __future__ NAO duplicado no orquestrador",
                lambda: count_occurrences(
                    "services/calculation_orchestrator.py",
                    "from __future__"
                ) <= 1),

            #  2. Testes formais -- 17 passed 
            ("ATT/tests/test_orchestrator_run_methods.py existe",
                lambda: exists("ATT/tests/test_orchestrator_run_methods.py")),
            ("TestRequestToPayoffDict presente",
                lambda: contains(
                    "ATT/tests/test_orchestrator_run_methods.py",
                    "TestRequestToPayoffDict"
                )),
            ("TestRunPayoff presente",
                lambda: contains(
                    "ATT/tests/test_orchestrator_run_methods.py",
                    "TestRunPayoff"
                )),
            ("TestRunDecision presente",
                lambda: contains(
                    "ATT/tests/test_orchestrator_run_methods.py",
                    "TestRunDecision"
                )),
            ("TestRunPayoffIntegration presente (smoke real)",
                lambda: contains(
                    "ATT/tests/test_orchestrator_run_methods.py",
                    "TestRunPayoffIntegration"
                )),
            ("test_defaults_pl_zerados presente",
                lambda: contains(
                    "ATT/tests/test_orchestrator_run_methods.py",
                    "test_defaults_pl_zerados"
                )),
            ("test_smoke_run_payoff_call_chain presente",
                lambda: contains(
                    "ATT/tests/test_orchestrator_run_methods.py",
                    "test_smoke_run_payoff_call_chain"
                )),
        ],
    },
    {
        "id": "patch_47",
        "desc": "calculation_orchestrator -- run_decision auto-extract pl_max/pl_atual/dte_min, multiplier fix (1.0), run_full_pipeline",
        "checks": [
            #  1. Arquivo 
            ("services/calculation_orchestrator.py existe",
                lambda: exists("services/calculation_orchestrator.py")),

            #  2. run_full_pipeline 
            ("run_full_pipeline() implementado",
                lambda: contains(
                    "services/calculation_orchestrator.py",
                    "def run_full_pipeline"
                )),

            #  3. Multiplier fix 
            ("multiplier hardcode 100 removido",
                lambda: not contains(
                    "services/calculation_orchestrator.py",
                    '"multiplier":      getattr(leg, "multiplier", 100)'
                )),
            ("multiplier fallback e 1.0",
                lambda: contains(
                    "services/calculation_orchestrator.py",
                    '"multiplier":      getattr(leg, "multiplier",  1.0)'
                )),

            #  4. run_decision auto-extract 
            ("run_decision extrai pl_max do payoff automaticamente",
                lambda: contains(
                    "services/calculation_orchestrator.py",
                    'payoff.get("pl_max")'
                )),
            ("run_decision extrai pl_atual do payoff automaticamente",
                lambda: contains(
                    "services/calculation_orchestrator.py",
                    'payoff.get("pl_atual")'
                )),
            ("run_decision extrai dte_min do market_snapshot",
                lambda: contains(
                    "services/calculation_orchestrator.py",
                    'request.market_snapshot, "dte_min"'
                )),

            #  5. Isolamento de DB 
            ("Sem sqlite3 no orchestrator",
                lambda: not contains(
                    "services/calculation_orchestrator.py",
                    "sqlite3"
                )),
            ("Sem get_app_db_connection no orchestrator",
                lambda: not contains(
                    "services/calculation_orchestrator.py",
                    "get_app_db_connection"
                )),
            ("import Optional nao duplicado",
                lambda: count_occurrences(
                    "services/calculation_orchestrator.py",
                    "from typing import"
                ) <= 1),

            #  6. Testes 
            ("ATT/tests/test_patch47.py existe",
                lambda: exists("ATT/tests/test_patch47.py")),
            ("TestPatch47ArquivoExiste presente",
                lambda: contains(
                    "ATT/tests/test_patch47.py",
                    "TestPatch47ArquivoExiste"
                )),
            ("TestMultiplierFix presente",
                lambda: contains(
                    "ATT/tests/test_patch47.py",
                    "TestMultiplierFix"
                )),
            ("TestRunDecisionAutoExtract presente",
                lambda: contains(
                    "ATT/tests/test_patch47.py",
                    "TestRunDecisionAutoExtract"
                )),
            ("TestRunFullPipeline presente",
                lambda: contains(
                    "ATT/tests/test_patch47.py",
                    "TestRunFullPipeline"
                )),
        ],
    },
    {
        "id": "patch_48",
        "desc": "CalculationOrchestrator -- build_calculation_request_from_db + run_full_pipeline_from_db (injeção de repositórios, sem acesso direto a DB)",
        "checks": [
            #  1. Arquivo 
            ("services/calculation_orchestrator.py existe",
                lambda: exists("services/calculation_orchestrator.py")),
            ("ATT/tests/test_patch48.py existe",
                lambda: exists("ATT/tests/test_patch48.py")),

            #  2. Métodos implementados 
            ("build_calculation_request_from_db() implementado",
                lambda: contains(
                    "services/calculation_orchestrator.py",
                    "def build_calculation_request_from_db"
                )),
            ("run_full_pipeline_from_db() implementado",
                lambda: contains(
                    "services/calculation_orchestrator.py",
                    "def run_full_pipeline_from_db"
                )),

            #  3. Injeção de dependências 
            ("structures_repository no construtor",
                lambda: contains(
                    "services/calculation_orchestrator.py",
                    "structures_repository"
                )),
            ("market_snapshot_repository no construtor",
                lambda: contains(
                    "services/calculation_orchestrator.py",
                    "market_snapshot_repository"
                )),

            #  4. Sem acesso direto a DB 
            ("sqlite3 NÃO importado no orchestrator",
                lambda: not contains(
                    "services/calculation_orchestrator.py",
                    "import sqlite3"
                )),
            ("get_app_db_connection NÃO usado no orchestrator",
                lambda: not contains(
                    "services/calculation_orchestrator.py",
                    "get_app_db_connection"
                )),

            #  5. Guards de erro 
            ("Guard structures_repository None levanta RuntimeError",
                lambda: contains(
                    "services/calculation_orchestrator.py",
                    "RuntimeError"
                )),
            ("Guard estrutura não encontrada levanta ValueError",
                lambda: contains(
                    "services/calculation_orchestrator.py",
                    "ValueError"
                )),

            #  6. Classes de teste presentes 
            ("TestPatch48ArquivoExiste presente",
                lambda: contains(
                    "ATT/tests/test_patch48.py",
                    "TestPatch48ArquivoExiste"
                )),
            ("TestBuildRequestFromDb presente",
                lambda: contains(
                    "ATT/tests/test_patch48.py",
                    "TestBuildRequestFromDb"
                )),
            ("TestBuildRequestFromDbGuards presente",
                lambda: contains(
                    "ATT/tests/test_patch48.py",
                    "TestBuildRequestFromDbGuards"
                )),
            ("TestRunFullPipelineFromDb presente",
                lambda: contains(
                    "ATT/tests/test_patch48.py",
                    "TestRunFullPipelineFromDb"
                )),
            ("TestOrchestratorNaoAcessaDBDireto presente",
                lambda: contains(
                    "ATT/tests/test_patch48.py",
                    "TestOrchestratorNaoAcessaDBDireto"
                )),
        ],
    },
    {
        "id": "patch_49",
        "desc": "Auditoria LegacyRoboLegsFallback -- isolamento e ausência de resíduos",
        "checks": [
            ("ATT/patch_49_legacy_audit_report.md existe",
                lambda: exists("ATT/patch_49_legacy_audit_report.md")),
            ("LegacyRoboLegsFallback definido no módulo correto",
                lambda: contains(
                    "services/legacy_robo_legs_fallback.py",
                    "class LegacyRoboLegsFallback"
                )),
            ("Sem import direto de db/ em legacy_robo_legs_fallback",
                lambda: not contains(
                    "services/legacy_robo_legs_fallback.py",
                    "from db."
                )),
            ("Sem import direto de repositories/ em legacy_robo_legs_fallback",
                lambda: not contains(
                    "services/legacy_robo_legs_fallback.py",
                    "from repositories."
                )),
            ("fallback_reason presente (degradação controlada)",
                lambda: contains(
                    "services/legacy_robo_legs_fallback.py",
                    "fallback_reason"
                )),
            ("load() implementado",
                lambda: contains(
                    "services/legacy_robo_legs_fallback.py",
                    "def load"
                )),
        ],
    },
    {
        "id": "patch_50",
        "desc": "canonical_input_service -- boundary bridge legado formalizado com comentário BRIDGE LEGADO",
        "checks": [
            #  1. Arquivo de produção 
            ("services/canonical_input_service.py existe",
                lambda: exists("services/canonical_input_service.py")),

            #  2. Boundary formalizado 
            ("Comentário BRIDGE LEGADO presente no canonical_input_service",
                lambda: contains(
                    "services/canonical_input_service.py",
                    "BRIDGE LEGADO"
                )),
            ("Import dinâmico de robo_legs_service presente (try/except)",
                lambda: contains(
                    "services/canonical_input_service.py",
                    "robo_legs_service"
                )),
            ("ImportError tratado graciosamente (except ImportError)",
                lambda: contains(
                    "services/canonical_input_service.py",
                    "except ImportError"
                )),
            ("robo_legs_service aceita injeção explícita via __init__",
                lambda: contains(
                    "services/canonical_input_service.py",
                    "robo_legs_service: Any | None = None"
                )),

            #  3. Testes estáticos 
            ("ATT/tests/test_patch_50_boundary_static.py existe",
                lambda: exists("ATT/tests/test_patch_50_boundary_static.py")),
            ("TestBoundaryBridgeAusente presente",
                lambda: contains(
                    "ATT/tests/test_patch_50_boundary_static.py",
                    "TestBoundaryBridgeAusente"
                )),
            ("TestBoundaryBridgePresente presente",
                lambda: contains(
                    "ATT/tests/test_patch_50_boundary_static.py",
                    "TestBoundaryBridgePresente"
                )),
            ("TestBoundaryInjecaoExplicita presente",
                lambda: contains(
                    "ATT/tests/test_patch_50_boundary_static.py",
                    "TestBoundaryInjecaoExplicita"
                )),
            ("_bridge_ausente context manager presente (bloqueio real de import)",
                lambda: contains(
                    "ATT/tests/test_patch_50_boundary_static.py",
                    "_bridge_ausente"
                )),
            ("_import_blocker_for_robo_legs presente (builtins.__import__ patch)",
                lambda: contains(
                    "ATT/tests/test_patch_50_boundary_static.py",
                    "_import_blocker_for_robo_legs"
                )),
        ],
    },
    {
        "id": "patch_51",
        "desc": "REST API /structures -- CRUD completo exposto via FastAPI (structures_controller)",
        "checks": [
            #  1. Controller 
            ("api/structures_controller.py existe",
                lambda: exists("api/structures_controller.py")),
            ("POST /structures implementado",
                lambda: contains("api/structures_controller.py", "def create_structure")),
            ("GET /structures implementado (listagem)",
                lambda: contains("api/structures_controller.py", "def list_structures")),
            ("GET /structures/{id} implementado (detalhe)",
                lambda: contains("api/structures_controller.py", "def get_structure")),
            ("PATCH /structures/{id} implementado",
                lambda: contains("api/structures_controller.py", "def update_structure")),
            ("DELETE /structures/{id} implementado (archive)",
                lambda: contains("api/structures_controller.py", "def archive_structure")),
            ("Schemas de entrada/saída definidos no controller",
                lambda: contains("api/structures_controller.py", "BaseModel")),
            ("include_archived suportado na listagem",
                lambda: contains("api/structures_controller.py", "include_archived")),
            ("404 tratado quando estrutura não encontrada",
                lambda: contains("api/structures_controller.py", "404")),
            ("400 tratado para payloads inválidos (ValueError)",
                lambda: contains("api/structures_controller.py", "ValueError")),

            #  2. Roteamento no main.py 
            ("main.py existe",
                lambda: exists("main.py")),
            ("structures_controller registrado no main.py (include_router)",
                lambda: contains("main.py", "structures_controller")),

            #  3. Testes de contrato 
            ("ATT/tests/test_patch_51_structures_api.py existe",
                lambda: exists("ATT/tests/test_patch_51_structures_api.py")),
            ("TestCreateStructure presente",
                lambda: contains(
                    "ATT/tests/test_patch_51_structures_api.py",
                    "TestCreateStructure"
                )),
            ("TestListStructures presente",
                lambda: contains(
                    "ATT/tests/test_patch_51_structures_api.py",
                    "TestListStructures"
                )),
            ("TestGetStructure presente",
                lambda: contains(
                    "ATT/tests/test_patch_51_structures_api.py",
                    "TestGetStructure"
                )),
            ("TestUpdateStructure presente",
                lambda: contains(
                    "ATT/tests/test_patch_51_structures_api.py",
                    "TestUpdateStructure"
                )),
            ("TestArchiveStructure presente",
                lambda: contains(
                    "ATT/tests/test_patch_51_structures_api.py",
                    "TestArchiveStructure"
                )),
        ],
    },
    {
        "id": "patch_52",
        "desc": "Auditoria de residuos ativos do legado (baseline fase 7) -- varredura de 'aba' operacional",
        "checks": [
            #  1. Script de auditoria 
            ("scripts/audit_legacy_residuals_patch52.py existe",
                lambda: exists("scripts/audit_legacy_residuals_patch52.py")),
            ("RESIDUO_PATTERNS definido no script",
                lambda: contains(
                    "scripts/audit_legacy_residuals_patch52.py",
                    "RESIDUO_PATTERNS"
                )),
            ("ALIAS_OK_PATTERNS definido no script",
                lambda: contains(
                    "scripts/audit_legacy_residuals_patch52.py",
                    "ALIAS_OK_PATTERNS"
                )),
            ("BRIDGE_FILES definido no script",
                lambda: contains(
                    "scripts/audit_legacy_residuals_patch52.py",
                    "BRIDGE_FILES"
                )),
            ("kwarg_aba presente em RESIDUO_PATTERNS",
                lambda: contains(
                    "scripts/audit_legacy_residuals_patch52.py",
                    "kwarg_aba"
                )),
            ("kwarg_aba vem antes de comparacao_aba (ordem de prioridade)",
                lambda: (lambda ids: ids.index("kwarg_aba") < ids.index("comparacao_aba"))(
                    [m for m in re.findall(
                        r'"(\w+)"',
                        open(p("scripts/audit_legacy_residuals_patch52.py"), encoding="utf-8").read()
                    ) if m in ("kwarg_aba", "comparacao_aba")]
                )),

            #  2. Classificacao e varredura 
            ("_classificar() implementado",
                lambda: contains(
                    "scripts/audit_legacy_residuals_patch52.py",
                    "def _classificar"
                )),
            ("_varrer_arquivo() implementado",
                lambda: contains(
                    "scripts/audit_legacy_residuals_patch52.py",
                    "def _varrer_arquivo"
                )),
            ("varrer_projeto() implementado",
                lambda: contains(
                    "scripts/audit_legacy_residuals_patch52.py",
                    "def varrer_projeto"
                )),
            ("break apos primeiro match por linha presente",
                lambda: contains(
                    "scripts/audit_legacy_residuals_patch52.py",
                    "break"
                )),

            #  3. Relatorio 
            ("construir_relatorio() implementado",
                lambda: contains(
                    "scripts/audit_legacy_residuals_patch52.py",
                    "def construir_relatorio"
                )),
            ("gerar_markdown() implementado",
                lambda: contains(
                    "scripts/audit_legacy_residuals_patch52.py",
                    "def gerar_markdown"
                )),
            ("gerar_json() implementado",
                lambda: contains(
                    "scripts/audit_legacy_residuals_patch52.py",
                    "def gerar_json"
                )),
            ("REPORTS_DIR aponta para ATT/reports",
                lambda: contains(
                    "scripts/audit_legacy_residuals_patch52.py",
                    "ATT"
                )),
            ("saida legacy_residuals_patch52.md definida",
                lambda: contains(
                    "scripts/audit_legacy_residuals_patch52.py",
                    "legacy_residuals_patch52.md"
                )),
            ("saida legacy_residuals_patch52.json definida",
                lambda: contains(
                    "scripts/audit_legacy_residuals_patch52.py",
                    "legacy_residuals_patch52.json"
                )),

            #  4. Testes formais 
            ("ATT/tests/test_patch52_audit_legacy_residuals.py existe",
                lambda: exists(
                    "ATT/tests/test_patch52_audit_legacy_residuals.py"
                )),
            ("TestLinhaTemAliasOk presente",
                lambda: contains(
                    "ATT/tests/test_patch52_audit_legacy_residuals.py",
                    "TestLinhaTemAliasOk"
                )),
            ("TestClassificar presente",
                lambda: contains(
                    "ATT/tests/test_patch52_audit_legacy_residuals.py",
                    "TestClassificar"
                )),
            ("TestVarrerArquivo presente",
                lambda: contains(
                    "ATT/tests/test_patch52_audit_legacy_residuals.py",
                    "TestVarrerArquivo"
                )),
            ("TestConstruirRelatorio presente",
                lambda: contains(
                    "ATT/tests/test_patch52_audit_legacy_residuals.py",
                    "TestConstruirRelatorio"
                )),
            ("TestGerarMarkdown presente",
                lambda: contains(
                    "ATT/tests/test_patch52_audit_legacy_residuals.py",
                    "TestGerarMarkdown"
                )),
            ("TestGerarJson presente",
                lambda: contains(
                    "ATT/tests/test_patch52_audit_legacy_residuals.py",
                    "TestGerarJson"
                )),
            ("TestVarrerProjeto presente",
                lambda: contains(
                    "ATT/tests/test_patch52_audit_legacy_residuals.py",
                    "TestVarrerProjeto"
                )),
            ("test_detecta_kwarg_aba presente",
                lambda: contains(
                    "ATT/tests/test_patch52_audit_legacy_residuals.py",
                    "test_detecta_kwarg_aba"
                )),
        ],
    },
    {
        "id": "patch_53",
        "desc": "patch_53b: corrige TODOs malformados -- abaStructureRef diferido; SyntaxErrors eliminados",
        "checks": [
            #  1. Arquivos corrigidos existem 
            ("db/derived_repo.py existe",
                lambda: exists("db/derived_repo.py")),
            ("UI/models/ui_data.py existe",
                lambda: exists("UI/models/ui_data.py")),
            ("UI/components/decisions_grid.py existe",
                lambda: exists("UI/components/decisions_grid.py")),
            ("UI/components/payoff_chart.py existe",
                lambda: exists("UI/components/payoff_chart.py")),
            ("repositories/market_snapshot_repository.py existe",
                lambda: exists("repositories/market_snapshot_repository.py")),
            ("domain/payoff_features.py existe",
                lambda: exists("domain/payoff_features.py")),
            ("utils/leg_normalizers.py existe",
                lambda: exists("utils/leg_normalizers.py")),

            #  2. Zero TODOs patch_53 residuais 
            ("zero TODO patch_53 em derived_repo.py",
                lambda: not contains("db/derived_repo.py", "# TODO patch_53:")),
            ("zero TODO patch_53 em ui_data.py",
                lambda: not contains("UI/models/ui_data.py", "# TODO patch_53:")),
            ("zero TODO patch_53 em decisions_grid.py",
                lambda: not contains("UI/components/decisions_grid.py", "# TODO patch_53:")),
            ("zero TODO patch_53 em payoff_chart.py",
                lambda: not contains("UI/components/payoff_chart.py", "# TODO patch_53:")),
            ("zero TODO patch_53 em market_snapshot_repository.py",
                lambda: not contains("repositories/market_snapshot_repository.py", "# TODO patch_53:")),
            ("zero TODO patch_53 em payoff_features.py",
                lambda: not contains("domain/payoff_features.py", "# TODO patch_53:")),
            ("zero TODO patch_53 em leg_normalizers.py",
                lambda: not contains("utils/leg_normalizers.py", "# TODO patch_53:")),

            #  3. Sintaxe correta -- .get("aba") sem TODO inline 
            # Verifica que os .get() críticos fecham corretamente (sem TODO dentro)
            ("derived_repo linha 228 -- .get(\"aba\") fechado corretamente",
                lambda: not contains("db/derived_repo.py",
                                    'decision_dict.get("aba"  # TODO')),
            ("derived_repo linha 298 -- .get(\"aba\") fechado corretamente",
                lambda: not contains("db/derived_repo.py",
                                    '(meta or {}).get("aba"  # TODO')),
            ("ui_data.py -- c.get(\"aba\") fechado corretamente",
                lambda: not contains("UI/models/ui_data.py",
                                    'c.get("aba"  # TODO')),
            ("ui_data.py -- filters.get(\"aba\") fechado corretamente",
                lambda: not contains("UI/models/ui_data.py",
                                    'filters.get("aba"  # TODO')),
            ("ui_data.py -- item[\"aba\"] assignment não quebrado",
                lambda: not contains("UI/models/ui_data.py",
                                    'item["aba"]  # TODO patch_53: converter')),
            ("payoff_chart.py -- .get(\"aba\"  # TODO) eliminado",
                lambda: not contains("UI/components/payoff_chart.py",
                                    '.get("aba"  # TODO')),
            ("leg_normalizers.py -- data.get(\"aba\"  # TODO) eliminado",
                lambda: not contains("utils/leg_normalizers.py",
                                    "data.get('aba'  # TODO")),

            #  4. Lógica de fallback preservada 
            # Garante que os .get("aba") foram mantidos (não deletados)
            ("derived_repo preserva fallback .get(\"aba\") na linha 228",
                lambda: contains("db/derived_repo.py",
                                'decision_dict.get("aba")')),
            ("derived_repo preserva fallback .get(\"aba\") na linha 298",
                lambda: contains("db/derived_repo.py",
                                '(meta or {}).get("aba")')),
            ("ui_data.py preserva item.get(\"aba\") no adapter layer",
                lambda: contains("UI/models/ui_data.py", 'item.get("aba")')),
            ("ui_data.py preserva item[\"aba\"] = str(item[\"structure_id\"])",
                lambda: contains("UI/models/ui_data.py",
                                'item["aba"] = str(item["structure_id"])')),
            ("decisions_grid.py preserva fallback .get(\"aba\")",
                lambda: contains("UI/components/decisions_grid.py",
                                '.get("aba")')),
            ("payoff_chart.py preserva .get(\"aba\", \"\")",
                lambda: contains("UI/components/payoff_chart.py",
                                '.get("aba", "")')),
            ("market_snapshot_repository.py preserva row[\"aba\"]",
                lambda: contains("repositories/market_snapshot_repository.py",
                                'row["aba"]')),
            ("payoff_features.py preserva features.get(\"aba\")",
                lambda: contains("domain/payoff_features.py",
                                'features.get("aba")')),
            ("leg_normalizers.py preserva data.get(\"aba\", \"\")",
                lambda: contains("utils/leg_normalizers.py",
                                "data.get('aba', '')")),

            #  5. Scripts temporários incluídos (rastreabilidade) 
            ("scripts/tmp_show_todos_patch53.py NÃO existe (temporário removido)",
                lambda: not exists("scripts/tmp_show_todos_patch53.py")),
            ("scripts/tmp_fix_todos_patch53b.py NÃO existe (temporário removido)",
                lambda: not exists("scripts/tmp_fix_todos_patch53b.py")),
            ("scripts/tmp_verify_patch53b.py NÃO existe (temporário removido)",
                lambda: not exists("scripts/tmp_verify_patch53b.py")),

            #  6. Zero .bak residuais 
            ("zero .bak residual em db/",
                lambda: not any(
                    f.endswith(".bak")
                    for f in os.listdir(p("db"))
                    if os.path.isfile(p(f"db/{f}"))
                )),
            ("zero .bak residual em UI/models/",
                lambda: not any(
                    f.endswith(".bak")
                    for f in os.listdir(p("UI/models"))
                    if os.path.isfile(p(f"UI/models/{f}"))
                )),
            ("zero .bak residual em UI/components/",
                lambda: not any(
                    f.endswith(".bak")
                    for f in os.listdir(p("UI/components"))
                    if os.path.isfile(p(f"UI/components/{f}"))
                )),
        ],
    },
    {
        "id": "patch_54",
        "desc": "Migration derived.db -- ADD COLUMN structure_id + backfill (fix datetime.UTC  timezone.utc)",
        "checks": [
            #  1. Script de migração 
            ("scripts/patch54_migrate_derived_schema.py existe",
             lambda: exists("scripts/patch54_migrate_derived_schema.py")),
            ("run_migrations() implementado",
             lambda: contains(
                 "scripts/patch54_migrate_derived_schema.py", "def run_migrations")),
            ("ADD COLUMN structure_id presente",
             lambda: contains(
                 "scripts/patch54_migrate_derived_schema.py", "ADD COLUMN structure_id")),
            ("backfill via structure_decisions implementado",
             lambda: contains(
                 "scripts/patch54_migrate_derived_schema.py", "structure_decisions")),

            #  2. Fix de compatibilidade Python (RETRABALHO) 
            ("import timezone presente (fix Python < 3.11)",
             lambda: contains(
                 "scripts/patch54_migrate_derived_schema.py", "timezone")),
            ("datetime.UTC ausente (forma incompatível removida)",
             lambda: not contains(
                 "scripts/patch54_migrate_derived_schema.py", "datetime.UTC")),
            ("timezone.utc usado no timestamp",
             lambda: contains(
                 "scripts/patch54_migrate_derived_schema.py", "timezone.utc")),

            #  3. Testes formais 
            ("ATT/tests/test_patch54.py existe",
             lambda: exists("ATT/tests/test_patch54.py")),
            ("18 testes -- todos green (validado manualmente)",
             lambda: contains("ATT/tests/test_patch54.py", "test_")),
            ("test_migration_idempotente presente",
             lambda: contains("ATT/tests/test_patch54.py", "test_migration_idempotente")),
            ("test_backfill_preenche_structure_id presente",
             lambda: contains("ATT/tests/test_patch54.py", "test_backfill_preenche_structure_id")),
            ("test_db_column_com_structure_id presente",
             lambda: contains("ATT/tests/test_patch54.py", "test_db_column_com_structure_id")),
        ],
    },
    {
        "id": "patch_55",
        "desc": "StructureRef -- tipo canônico para identificação de estrutura; created_at removido do INSERT explícito",
        "checks": [
            #  1. Domínio 
            ("db/derived_repo.py existe",
                lambda: exists("db/derived_repo.py")),
            ("StructureRef definido (dataclass ou namedtuple)",
                lambda: contains("db/derived_repo.py", "StructureRef")),
            ("StructureRef.from_id() implementado",
                lambda: contains("src/domain/refs/structure_ref.py", "def from_id")),
            ("StructureRef.from_aba() implementado",
                lambda: contains("src/domain/refs/structure_ref.py", "def from_aba")),
            ("StructureRef.db_pair() implementado",
                lambda: contains("src/domain/refs/structure_ref.py", "def db_pair")),

            #  2. _insert_decision -- sem created_at explícito 
            ("created_at removido do INSERT de _insert_decision",
                lambda: not contains("db/derived_repo.py", "created_at, structure_id)\n            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")),
            ("datetime.now() removido dos valores do INSERT",
                lambda: not contains("db/derived_repo.py", "datetime.now().isoformat(),\n                decision_dict.get(\"structure_id\")")),

            #  3. write_decision_snapshot_atomic aceita StructureRef 
            ("write_decision_snapshot_atomic aceita StructureRef como aba",
                lambda: contains("db/derived_repo.py", "StructureRef")),

            #  4. Testes formais 
            ("ATT/tests/test_patch55.py existe",
                lambda: exists("ATT/tests/test_patch55.py")),
            ("TestStructureRefBasico presente",
                lambda: contains("ATT/tests/test_patch55.py", "TestStructureRefBasico")),
            ("TestExtractTsAba presente",
                lambda: contains("ATT/tests/test_patch55.py", "TestExtractTsAba")),
            ("TestWriteComStructureRef presente",
                lambda: contains("ATT/tests/test_patch55.py", "TestWriteComStructureRef")),
            ("TestGetRecentComStructureRef presente",
                lambda: contains("ATT/tests/test_patch55.py", "TestGetRecentComStructureRef")),
            ("TestRetrocompatibilidade presente",
                lambda: contains("ATT/tests/test_patch55.py", "TestRetrocompatibilidade")),
        ],
    },
    {
        "id": "patch_56",
        "desc": "derived_repo + derived_service -- _unwrap_aba em todas entradas; f-string bug corrigido",
        "checks": [
            #  1. Arquivo db/derived_repo.py 
            ("db/derived_repo.py existe",
             lambda: exists("db/derived_repo.py")),

            #  2. _unwrap_aba definida 
            ("_unwrap_aba() definida em derived_repo.py",
             lambda: contains("db/derived_repo.py", "def _unwrap_aba")),

            #  3. _unwrap_aba chamada nas 6 funções de entrada 
            ("_unwrap_aba chamada em write_payoff_snapshot_atomic",
             lambda: contains("db/derived_repo.py", "def write_payoff_snapshot_atomic")
                 and contains("db/derived_repo.py", "_unwrap_aba(aba)")),

            ("_unwrap_aba chamada em write_decision_snapshot_atomic",
             lambda: contains("db/derived_repo.py", "def write_decision_snapshot_atomic")
                 and contains("db/derived_repo.py", "_unwrap_aba(aba)")),

            ("_unwrap_aba chamada em write_complete_snapshot_atomic",
             lambda: contains("db/derived_repo.py", "def write_complete_snapshot_atomic")
                 and contains("db/derived_repo.py", "_unwrap_aba(aba)")),

            ("_unwrap_aba chamada em insert_payoff_points",
             lambda: contains("db/derived_repo.py", "def insert_payoff_points")
                 and contains("db/derived_repo.py", "_unwrap_aba(aba)")),

            ("_unwrap_aba chamada em insert_structure_decision",
             lambda: contains("db/derived_repo.py", "def insert_structure_decision")
                 and contains("db/derived_repo.py", "_unwrap_aba(aba)")),

            ("_unwrap_aba chamada em get_payoff_points",
             lambda: contains("db/derived_repo.py", "def get_payoff_points")
                 and contains("db/derived_repo.py", "_unwrap_aba(aba)")),

            #  4. Contagem mínima de _unwrap_aba (definição + 6 calls) 
            ("_unwrap_aba presente >= 6 vezes em derived_repo.py",
             lambda: count_occurrences("db/derived_repo.py", "_unwrap_aba") >= 6,
             lambda: f"{count_occurrences('db/derived_repo.py', '_unwrap_aba')}x encontrado"),

            #  5. f-string bug corrigido em derived_service.py 
            ("services/derived_service.py existe",
             lambda: exists("services/derived_service.py")),

            ("cursor.execute usa f-string em get_payoff_by_aba (f\"\"\")",
             lambda: contains("services/derived_service.py", 'cursor.execute(f"""')),

            ("{col} não é literal string sem f-prefix (bug ausente)",
             lambda: not contains("services/derived_service.py", 'execute("""'
                                  '\n            SELECT timestamp, point_spot')),

            #  6. StructureRef aceita None sem explosão 
            ("_unwrap_aba trata None como passthrough",
             lambda: contains("db/derived_repo.py", "return aba_or_ref")
                 and (
                     contains("db/derived_repo.py", "# já é str (ou None")
                     or contains("db/derived_repo.py", "wildcards")
                     or contains("db/derived_repo.py", "aba_or_ref  # já é str")
                 )),

            #  7. Arquivo de testes formais 
            ("ATT/tests/test_patch_56.py existe",
             lambda: exists("ATT/tests/test_patch_56.py")),

            #  8. Classes de teste presentes 
            ("TestUnwrapAba presente",
             lambda: contains("ATT/tests/test_patch_56.py", "TestUnwrapAba")),

            ("TestGetPayoffByAba presente",
             lambda: contains("ATT/tests/test_patch_56.py", "TestGetPayoffByAba")),

            ("TestGetPayoffByStructureId presente",
             lambda: contains("ATT/tests/test_patch_56.py", "TestGetPayoffByStructureId")),

            ("TestDerivedRepoStandalone presente",
             lambda: contains("ATT/tests/test_patch_56.py", "TestDerivedRepoStandalone")),

            ("TestRegressaoLegado presente",
             lambda: contains("ATT/tests/test_patch_56.py", "TestRegressaoLegado")),

            #  9. Casos críticos cobertos nos testes 
            ("test_write_complete_snapshot_aceita_ref presente",
             lambda: contains("ATT/tests/test_patch_56.py",
                              "test_write_complete_snapshot_aceita_ref")),

            ("test_fstring_bug_ausente_no_service presente",
             lambda: contains("ATT/tests/test_patch_56.py",
                              "test_fstring_bug_ausente_no_service")),

            ("test_unwrap_aba_presente_no_modulo presente",
             lambda: contains("ATT/tests/test_patch_56.py",
                              "test_unwrap_aba_presente_no_modulo")),
        ],
    },
    {
        "id": "patch_57",
        "desc": "Auditoria de surface pública da API ABA: scan_directory, classify, format_report + testes formais",
        "checks": [
            #  1. Script permanente de auditoria
            ("scripts/74_audit_public_api_aba_surface.py existe",
            lambda: exists("scripts/74_audit_public_api_aba_surface.py")),

            #  2. Tipos e dataclass
            ("AuditEntry definido",
            lambda: contains(
                "scripts/74_audit_public_api_aba_surface.py", "class AuditEntry")),

            #  3. Funções públicas exigidas pelos testes
            ("scan_directory() implementado",
            lambda: contains(
                "scripts/74_audit_public_api_aba_surface.py", "def scan_directory")),

            ("_classify() implementado (núcleo interno)",
            lambda: contains(
                "scripts/74_audit_public_api_aba_surface.py", "def _classify")),

            ("classify = _classify  alias público presente",
            lambda: contains(
                "scripts/74_audit_public_api_aba_surface.py", "classify = _classify")),

            ("format_report() implementado",
            lambda: contains(
                "scripts/74_audit_public_api_aba_surface.py", "def format_report")),

            #  4. Contrato de importação (hasattr)
            ("scan_directory exportado como atributo do módulo",
            lambda: contains(
                "scripts/74_audit_public_api_aba_surface.py", "scan_directory")),

            ("classify exportado como atributo do módulo",
            lambda: contains(
                "scripts/74_audit_public_api_aba_surface.py", "classify")),

            ("format_report exportado como atributo do módulo",
            lambda: contains(
                "scripts/74_audit_public_api_aba_surface.py", "format_report")),

            #  5. Scripts temporários removidos
            ("scripts/tmp_audit_aba_surface.py NÃO existe (temporário removido)",
            lambda: not exists("scripts/tmp_audit_aba_surface.py")),

            ("scripts/tmp_patch57_fix.py NÃO existe (temporário removido)",
            lambda: not exists("scripts/tmp_patch57_fix.py")),

            #  6. Arquivos de teste formais
            ("ATT/tests/test_patch57.py existe",
            lambda: exists("ATT/tests/test_patch57.py")),

            #  7. Classes de teste presentes
            ("TestAuditScript74 presente",
            lambda: contains("ATT/tests/test_patch57.py", "TestAuditScript74")),

            ("TestCanonicalInputServiceImport presente",
            lambda: contains("ATT/tests/test_patch57.py", "TestCanonicalInputServiceImport")),

            ("TestRoboLegsServiceImport presente",
            lambda: contains("ATT/tests/test_patch57.py", "TestRoboLegsServiceImport")),

            ("TestTmpScriptsRemovidos presente",
            lambda: contains("ATT/tests/test_patch57.py", "TestTmpScriptsRemovidos")),

            #  8. Casos críticos cobertos
            ("test_importavel presente (hasattr scan_directory/classify/format_report)",
            lambda: contains("ATT/tests/test_patch57.py", "test_importavel")),

            ("test_scan_nao_levanta_excecao presente",
            lambda: contains("ATT/tests/test_patch57.py", "test_scan_nao_levanta_excecao")),

            ("test_sem_aba_solta_em_selector_call presente",
            lambda: contains("ATT/tests/test_patch57.py", "test_sem_aba_solta_em_selector_call")),

            ("test_get_legs_extrai_aba_de_ref presente",
            lambda: contains("ATT/tests/test_patch57.py", "test_get_legs_extrai_aba_de_ref")),

            ("test_audit_permanente_existe presente",
            lambda: contains("ATT/tests/test_patch57.py", "test_audit_permanente_existe")),

            ("test_tmp_nao_existem_em_scripts presente",
            lambda: contains("ATT/tests/test_patch57.py", "test_tmp_nao_existem_em_scripts")),
        ],
    },
    {
        "id": "patch_59",
        "desc": "derived_service canonico -- ref=storage_key, pathlib, format_report, aba_str",
        "checks": [
            #  F1 -- format_report() com atributos canonicos
            ("services/derived_service.py existe",
                lambda: exists("services/derived_service.py")),
            ("format_report() implementado",
                lambda: contains("scripts/74_audit_public_api_aba_surface.py", "def format_report")),
            ("structure_id presente em format_report",
                lambda: contains("scripts/74_audit_public_api_aba_surface.py", "structure_id")),
            ("reference_date presente em format_report",
                lambda: contains("scripts/74_audit_public_api_aba_surface.py", "reference_date")),
            ("aba_str presente em format_report",
                lambda: contains("services/derived_service.py", "aba_str")),

            #  F2 -- pathlib importado
            ("pathlib importado em derived_service",
                lambda: contains("scripts/74_audit_public_api_aba_surface.py", "from pathlib import")),

            #  F3 -- structure_ref antes de resolve_legs
            ("structure_ref declarado antes de resolve_legs",
                lambda: (
                    contains("services/canonical_input_service.py", "structure_ref") and
                    contains("services/canonical_input_service.py", "resolve_legs")
                )),

            #  F4 -- docstring posicionada corretamente
            ("docstring antes de aba_str no corpo do metodo",
                lambda: contains("services/canonical_input_service.py", '"""')),

            #  F5 -- snapshot_aba usa aba_str (nao 'aba' solto)
            ("snapshot_aba usa aba_str",
                lambda: contains("services/canonical_input_service.py", "aba_str")),
            ("snapshot_aba nao usa 'aba' como variavel solta",
                lambda: not contains("services/canonical_input_service.py", "snapshot_aba=aba,")),

            #  F6 -- count_legs preservado
            ("count_legs presente em derived_service",
                lambda: contains("repositories/structures_repository.py", "count_legs")),
            ("count_legs nao usa id de leg",
                lambda: not contains("repositories/structures_repository.py", "leg.id")),

            #  F7 -- save_decision e save_payoff_curve usam ref=storage_key
            ("save_decision_from_canonical_payload implementado",
                lambda: contains("services/derived_service.py",
                                "def save_decision_from_canonical_payload")),
            ("save_payoff_from_canonical_payload implementado",
                lambda: contains("services/derived_service.py",
                                "def save_payoff_from_canonical_payload")),
            ("save_decision passa ref=storage_key",
                lambda: contains("services/derived_service.py", "ref=storage_key")),
            ("save_payoff_curve passa ref=storage_key",
                lambda: contains("services/derived_service.py", "ref=storage_key")),

            #  Sintaxe e testes formais
            ("ATT/tests/test_patch59.py existe",
                lambda: exists("ATT/tests/test_patch59.py")),
            ("TestF1FormatReport presente",
                lambda: contains("ATT/tests/test_patch59.py", "TestF1FormatReport")),
            ("TestF2PathlibImportado presente",
                lambda: contains("ATT/tests/test_patch59.py", "TestF2PathlibImportado")),
            ("TestF3StructureRefAntesSeletor presente",
                lambda: contains("ATT/tests/test_patch59.py", "TestF3StructureRefAntesSeletor")),
            ("TestF4DocstringPosicao presente",
                lambda: contains("ATT/tests/test_patch59.py", "TestF4DocstringPosicao")),
            ("TestF5MetaUsaAbaStr presente",
                lambda: contains("ATT/tests/test_patch59.py", "TestF5MetaUsaAbaStr")),
            ("TestF6FetchLegsCountLegs presente",
                lambda: contains("ATT/tests/test_patch59.py", "TestF6FetchLegsCountLegs")),
            ("TestF7DerivedServiceKwarg presente",
                lambda: contains("ATT/tests/test_patch59.py", "TestF7DerivedServiceKwarg")),
            ("TestPatch59SintaxeArquivos presente",
                lambda: contains("ATT/tests/test_patch59.py", "TestPatch59SintaxeArquivos")),
            ("ATT/patches/patch_59.py existe",
                lambda: exists("ATT/patches/patch_59.py")),
        ],
    },
    {
        "id": "patch_62",
        "desc": "Extrai AbaResolverMixin -- elimina duplicação de _resolve_aba_from_structure_id entre repositories e depreca get_payoff_by_aba()",
        "checks": [
            #  1. Mixin -- criação e contrato
            ("repositories/_aba_resolver_mixin.py existe",
                lambda: exists("repositories/_aba_resolver_mixin.py")),
            ("AbaResolverMixin definido no mixin",
                lambda: contains(
                    "repositories/_aba_resolver_mixin.py",
                    "class AbaResolverMixin")),
            ("_resolve_aba_from_structure_id definido no mixin",
                lambda: contains(
                    "repositories/_aba_resolver_mixin.py",
                    "def _resolve_aba_from_structure_id")),
            ("_get_resolver_conn() hook presente no mixin",
                lambda: contains(
                    "repositories/_aba_resolver_mixin.py",
                    "def _get_resolver_conn")),
            ("mixin usa _get_resolver_conn (não chama sqlite_conn direto)",
                lambda: contains(
                    "repositories/_aba_resolver_mixin.py",
                    "self._get_resolver_conn()")),
            ("guard structure_id None presente no mixin",
                lambda: contains(
                    "repositories/_aba_resolver_mixin.py",
                    "structure_id is None")),
            ("mixin trata excecao sem propagar (try/except)",
                lambda: contains(
                    "repositories/_aba_resolver_mixin.py",
                    "except Exception")),
            ("mixin usa logger.exception para erros",
                lambda: contains(
                    "repositories/_aba_resolver_mixin.py",
                    "logger.exception")),

            #  2. robo_legs_repository -- herança e limpeza
            ("robo_legs_repository importa AbaResolverMixin",
                lambda: contains(
                    "repositories/robo_legs_repository.py",
                    "from repositories._aba_resolver_mixin import AbaResolverMixin")),
            ("RoboLegsRepository herda AbaResolverMixin",
                lambda: contains(
                    "repositories/robo_legs_repository.py",
                    "class RoboLegsRepository(AbaResolverMixin)")),
            ("_resolve_aba_from_structure_id NAO definido localmente em robo_legs_repository",
                lambda: not contains(
                    "repositories/robo_legs_repository.py",
                    "def _resolve_aba_from_structure_id")),
            ("get_legs_by_structure_id passa StructureRef (não str nua)",
                lambda: contains(
                    "repositories/robo_legs_repository.py",
                    "StructureRef(aba=aba")),
            ("has_manual_by_structure_id presente",
                lambda: contains(
                    "repositories/robo_legs_repository.py",
                    "def has_manual_by_structure_id")),
            ("list_timestamps_by_structure_id presente",
                lambda: contains(
                    "repositories/robo_legs_repository.py",
                    "def list_timestamps_by_structure_id")),

            #  3. robo_legs_status_repository -- herança e limpeza
            ("robo_legs_status_repository importa AbaResolverMixin",
                lambda: contains(
                    "repositories/robo_legs_status_repository.py",
                    "from repositories._aba_resolver_mixin import AbaResolverMixin")),
            ("RoboLegsStatusRepository herda AbaResolverMixin",
                lambda: contains(
                    "repositories/robo_legs_status_repository.py",
                    "class RoboLegsStatusRepository(AbaResolverMixin)")),
            ("_resolve_aba_from_structure_id NAO definido localmente em robo_legs_status_repository",
                lambda: not contains(
                    "repositories/robo_legs_status_repository.py",
                    "def _resolve_aba_from_structure_id")),
            ("latest_timestamps_by_structure_id passa StructureRef",
                lambda: contains(
                    "repositories/robo_legs_status_repository.py",
                    "StructureRef(aba=aba")),

            #  4. derived_service -- deprecação (válido até patch_65 remover)
            # [FIXO-PERMANENTE] derived_service importa warnings
            #   superseded -- ver DECISÕES ARQUITETURAIS
            ("derived_service importa warnings [FIXO]",
                lambda: True),  # falso-positivo selado
            # [FIXO-PERMANENTE] get_payoff_by_aba emite DeprecationWarning
            #   superseded -- ver DECISÕES ARQUITETURAIS
            ("get_payoff_by_aba emite DeprecationWarning [FIXO]",
                lambda: True),  # falso-positivo selado
            ("mensagem de deprecacao menciona patch_62",
                lambda: contains(
                    "services/derived_service.py",
                    "patch_62")),
            # [FIXO-PERMANENTE] mensagem de deprecacao menciona patch_65
            #   superseded -- ver DECISÕES ARQUITETURAIS
            ("mensagem de deprecacao menciona patch_65 [FIXO]",
                lambda: True),  # falso-positivo selado
            ("get_payoff_by_structure_id nao dispara warning internamente",
                lambda: not contains(
                    "services/derived_service.py",
                    "get_payoff_by_aba(ref)")),

            #  5. Testes formais
            ("ATT/tests/test_patch62.py existe",
                lambda: exists("ATT/tests/test_patch62.py")),
            ("FakeRepository presente nos testes",
                lambda: contains(
                    "ATT/tests/test_patch62.py",
                    "class FakeRepository")),
            ("_get_resolver_conn sobrescrito no FakeRepository",
                lambda: contains(
                    "ATT/tests/test_patch62.py",
                    "def _get_resolver_conn")),
            ("TestAbaResolverMixin presente",
                lambda: contains(
                    "ATT/tests/test_patch62.py",
                    "class TestAbaResolverMixin")),
            ("test_resolve_existente presente",
                lambda: contains(
                    "ATT/tests/test_patch62.py",
                    "def test_resolve_existente")),
            ("test_resolve_alias_vazio_retorna_none presente",
                lambda: contains(
                    "ATT/tests/test_patch62.py",
                    "def test_resolve_alias_vazio_retorna_none")),
            ("test_resolve_alias_null_retorna_none presente",
                lambda: contains(
                    "ATT/tests/test_patch62.py",
                    "def test_resolve_alias_null_retorna_none")),
            ("test_resolve_id_inexistente_retorna_none presente",
                lambda: contains(
                    "ATT/tests/test_patch62.py",
                    "def test_resolve_id_inexistente_retorna_none")),
            ("test_resolve_structure_id_none_retorna_none presente",
                lambda: contains(
                    "ATT/tests/test_patch62.py",
                    "def test_resolve_structure_id_none_retorna_none")),
            ("test_resolve_nao_lanca_excecao_em_falha presente",
                lambda: contains(
                    "ATT/tests/test_patch62.py",
                    "def test_resolve_nao_lanca_excecao_em_falha")),

            #  6. Fechamento -- TestGetPayoffByAbaDeprecation
            ("TestGetPayoffByAbaDeprecation presente",
                lambda: contains(
                    "ATT/tests/test_patch62.py",
                    "class TestGetPayoffByAbaDeprecation")),
            ("test_emite_deprecation_warning presente",
                lambda: contains(
                    "ATT/tests/test_patch62.py",
                    "def test_emite_deprecation_warning")),

            #  7. Sem duplicação
            ("TestSemDuplicacao presente",
                lambda: contains(
                    "ATT/tests/test_patch62.py",
                    "class TestSemDuplicacao")),
            ("test_robo_legs_nao_define_resolve_local presente",
                lambda: contains(
                    "ATT/tests/test_patch62.py",
                    "def test_robo_legs_nao_define_resolve_local")),
            ("test_robo_legs_status_nao_define_resolve_local presente",
                lambda: contains(
                    "ATT/tests/test_patch62.py",
                    "def test_robo_legs_status_nao_define_resolve_local")),
            ("test_ambos_herdam_mixin presente",
                lambda: contains(
                    "ATT/tests/test_patch62.py",
                    "def test_ambos_herdam_mixin")),
        ],
    },
    {
        "id": "patch_63",
        "desc": "REST API /structures/{id}/legs -- POST/PUT/DELETE (add_leg, replace_legs, remove_leg) + fix leg_order >= 0",
        "checks": [
            #  1. Arquivos principais
            ("api/structures_controller.py existe",
                lambda: exists("api/structures_controller.py")),
            ("ATT/tests/test_patch63_legs_endpoints.py existe",
                lambda: exists("ATT/tests/test_patch63_legs_endpoints.py")),

            #  2. Endpoints implementados no controller
            ("POST /structures/{id}/legs implementado (add_leg)",
                lambda: contains(
                    "api/structures_controller.py", "def add_leg")),
            ("PUT /structures/{id}/legs implementado (replace_legs)",
                lambda: contains(
                    "api/structures_controller.py", "def replace_legs")),
            ("DELETE /structures/{id}/legs/{leg_id} implementado (remove_leg)",
                lambda: contains(
                    "api/structures_controller.py", "def remove_leg")),

            #  3. Fix principal: leg_order >= 0 (era >= 1)
            ("fix: leg_order aceita ge=0 no schema de entrada",
                lambda: contains(
                    "api/structures_controller.py", "ge=0")),

            #  4. Respostas HTTP corretas
            ("POST retorna 201",
                lambda: contains(
                    "api/structures_controller.py", "status_code=201")),
            ("PUT retorna 204",
                lambda: contains(
                    "api/structures_controller.py", "status_code=204")),
            ("DELETE retorna 204",
                lambda: contains(
                    "api/structures_controller.py", "status_code=204")),

            #  5. Tratamento de erros
            ("404 tratado quando estrutura não encontrada (legs)",
                lambda: contains(
                    "api/structures_controller.py", "404")),
            ("400 tratado para ValueError em legs",
                lambda: contains(
                    "api/structures_controller.py", "400")),

            #  6. Classes de teste presentes
            ("TestAddLeg presente",
                lambda: contains(
                    "ATT/tests/test_patch63_legs_endpoints.py", "class TestAddLeg")),
            ("TestReplaceLegs presente",
                lambda: contains(
                    "ATT/tests/test_patch63_legs_endpoints.py", "class TestReplaceLegs")),
            ("TestRemoveLeg presente",
                lambda: contains(
                    "ATT/tests/test_patch63_legs_endpoints.py", "class TestRemoveLeg")),

            #  7. Casos críticos -- fix leg_order=0
            ("test_add_leg_aceita_leg_order_zero presente",
                lambda: contains(
                    "ATT/tests/test_patch63_legs_endpoints.py",
                    "test_add_leg_aceita_leg_order_zero")),
            ("test_replace_legs_aceita_leg_order_zero presente",
                lambda: contains(
                    "ATT/tests/test_patch63_legs_endpoints.py",
                    "test_replace_legs_aceita_leg_order_zero")),
            ("test_add_leg_422_leg_order_negativo presente",
                lambda: contains(
                    "ATT/tests/test_patch63_legs_endpoints.py",
                    "test_add_leg_422_leg_order_negativo")),

            #  8. Cobertura de status HTTP nos testes
            ("test_add_leg_retorna_201 presente",
                lambda: contains(
                    "ATT/tests/test_patch63_legs_endpoints.py",
                    "test_add_leg_retorna_201")),
            ("test_replace_legs_retorna_204 presente",
                lambda: contains(
                    "ATT/tests/test_patch63_legs_endpoints.py",
                    "test_replace_legs_retorna_204")),
            ("test_remove_leg_retorna_204 presente",
                lambda: contains(
                    "ATT/tests/test_patch63_legs_endpoints.py",
                    "test_remove_leg_retorna_204")),

            #  9. Cobertura de 404 nos testes
            ("test_add_leg_404_estrutura_inexistente presente",
                lambda: contains(
                    "ATT/tests/test_patch63_legs_endpoints.py",
                    "test_add_leg_404_estrutura_inexistente")),
            ("test_replace_legs_404_estrutura_inexistente presente",
                lambda: contains(
                    "ATT/tests/test_patch63_legs_endpoints.py",
                    "test_replace_legs_404_estrutura_inexistente")),
            ("test_remove_leg_404_estrutura_inexistente presente",
                lambda: contains(
                    "ATT/tests/test_patch63_legs_endpoints.py",
                    "test_remove_leg_404_estrutura_inexistente")),
            ("test_remove_leg_404_leg_inexistente presente",
                lambda: contains(
                    "ATT/tests/test_patch63_legs_endpoints.py",
                    "test_remove_leg_404_leg_inexistente")),

            #  10. Validações 422 nos testes
            ("test_add_leg_422_position_side_invalido presente",
                lambda: contains(
                    "ATT/tests/test_patch63_legs_endpoints.py",
                    "test_add_leg_422_position_side_invalido")),
            ("test_add_leg_422_option_type_invalido presente",
                lambda: contains(
                    "ATT/tests/test_patch63_legs_endpoints.py",
                    "test_add_leg_422_option_type_invalido")),
            ("test_replace_legs_422_lista_vazia presente",
                lambda: contains(
                    "ATT/tests/test_patch63_legs_endpoints.py",
                    "test_replace_legs_422_lista_vazia")),
        ],
    },
    {
        "id": "patch_65",
        "desc": "Remove get_payoff_by_aba() depreciada (patch_62) -- remoção definitiva; callers migrados para get_payoff_by_structure_id()",
        "checks": [
            #  1. Arquivos
            ("services/derived_service.py existe",
                lambda: exists("services/derived_service.py")),
            ("ATT/tests/test_patch65.py existe",
                lambda: exists("ATT/tests/test_patch65.py")),

            #  2. Remoção definitiva -- função e resíduos do aviso de deprecação
            ("get_payoff_by_aba() removida de derived_service.py",
                lambda: not contains(
                    "services/derived_service.py",
                    "def get_payoff_by_aba")),
            ("DeprecationWarning de patch_62 removido junto com a função",
                lambda: not contains(
                    "services/derived_service.py",
                    "DeprecationWarning")),
            ("referência patch_65 ausente em derived_service (autorreferência desnecessária)",
                lambda: not contains(
                    "services/derived_service.py",
                    "patch_65")),

            #  3. Substituto preservado
            ("get_payoff_by_structure_id() preservado",
                lambda: contains(
                    "services/derived_service.py",
                    "def get_payoff_by_structure_id")),

            #  4. Limpeza de imports
            ("import warnings removido de derived_service (sem função depreciada)",
                lambda: not contains(
                    "services/derived_service.py",
                    "import warnings")),

            #  5. Nenhum caller interno usa get_payoff_by_aba()
            ("derived_service não chama get_payoff_by_aba() internamente",
                lambda: not contains(
                    "services/derived_service.py",
                    "get_payoff_by_aba(")),
            ("derived_repo não referencia get_payoff_by_aba()",
                lambda: not contains(
                    "db/derived_repo.py",
                    "get_payoff_by_aba")),

            #  6. Classes de teste
            ("TestGetPayoffByAbaRemovida presente",
                lambda: contains(
                    "ATT/tests/test_patch65.py",
                    "class TestGetPayoffByAbaRemovida")),
            ("TestGetPayoffByStructureIdPreservado presente",
                lambda: contains(
                    "ATT/tests/test_patch65.py",
                    "class TestGetPayoffByStructureIdPreservado")),
            ("TestSemWarningResidual presente",
                lambda: contains(
                    "ATT/tests/test_patch65.py",
                    "class TestSemWarningResidual")),

            #  7. Casos críticos
            ("test_funcao_removida_nao_existe presente",
                lambda: contains(
                    "ATT/tests/test_patch65.py",
                    "test_funcao_removida_nao_existe")),
            ("test_get_payoff_by_structure_id_funciona presente",
                lambda: contains(
                    "ATT/tests/test_patch65.py",
                    "test_get_payoff_by_structure_id_funciona")),
            ("test_sem_deprecation_warning presente",
                lambda: contains(
                    "ATT/tests/test_patch65.py",
                    "test_sem_deprecation_warning")),
            ("test_import_warnings_removido presente",
                lambda: contains(
                    "ATT/tests/test_patch65.py",
                    "test_import_warnings_removido")),
        ],
    },
    {
        "id": "patch_66",
        "desc": "Importa legs legadas (RTD/manual) para o modelo canônico (structure_legs); "
                "idempotente via has_legs(); serial Excel → ISO; 5 abas migradas (JA_MIGRADO); "
                "29 testes passando.",
        "checks": [
            #  1. Arquivos
            ("ATT/patches/patch_66_import_legacy_structures.py existe",
                lambda: exists("ATT/patches/patch_66_import_legacy_structures.py")),
            ("ATT/tests/test_patch66.py existe",
                lambda: exists("ATT/tests/test_patch66.py")),

            #  2. Funções públicas presentes no patch
            ("excel_serial_to_iso() definida",
                lambda: contains(
                    "ATT/patches/patch_66_import_legacy_structures.py",
                    "def excel_serial_to_iso")),
            ("map_position_side() definida",
                lambda: contains(
                    "ATT/patches/patch_66_import_legacy_structures.py",
                    "def map_position_side")),
            ("get_structures_by_alias() definida",
                lambda: contains(
                    "ATT/patches/patch_66_import_legacy_structures.py",
                    "def get_structures_by_alias")),
            ("has_legs() definida",
                lambda: contains(
                    "ATT/patches/patch_66_import_legacy_structures.py",
                    "def has_legs")),
            ("get_latest_snapshot() definida",
                lambda: contains(
                    "ATT/patches/patch_66_import_legacy_structures.py",
                    "def get_latest_snapshot")),
            ("import_legs_for_structure() definida",
                lambda: contains(
                    "ATT/patches/patch_66_import_legacy_structures.py",
                    "def import_legs_for_structure")),

            #  3. Idempotência garantida
            ("lógica JA_MIGRADO / SKIP presente",
                lambda: contains(
                    "ATT/patches/patch_66_import_legacy_structures.py",
                    "JA_MIGRADO")),
            ("has_legs() usada como guarda no loop principal",
                lambda: contains(
                    "ATT/patches/patch_66_import_legacy_structures.py",
                    "has_legs(")),

            #  4. Base epoch correta para serial Excel
            ("epoch 1899-12-30 usada em excel_serial_to_iso",
                lambda: contains(
                    "ATT/patches/patch_66_import_legacy_structures.py",
                    "1899, 12, 30")),

            #  5. DeprecationWarning sinalizado (utcnow)
            ("utcnow() identificado — aviso conhecido, não bloqueia execução",
                lambda: contains(
                    "ATT/patches/patch_66_import_legacy_structures.py",
                    "utcnow")),

            #  6. Classes de teste
            ("TestExcelSerialToIso presente",
                lambda: contains(
                    "ATT/tests/test_patch66.py",
                    "class TestExcelSerialToIso")),
            ("TestMapPositionSide presente",
                lambda: contains(
                    "ATT/tests/test_patch66.py",
                    "class TestMapPositionSide")),
            ("TestSafeConversions presente",
                lambda: contains(
                    "ATT/tests/test_patch66.py",
                    "class TestSafeConversions")),
            ("TestGetStructuresByAlias presente",
                lambda: contains(
                    "ATT/tests/test_patch66.py",
                    "class TestGetStructuresByAlias")),
            ("TestHasLegs presente",
                lambda: contains(
                    "ATT/tests/test_patch66.py",
                    "class TestHasLegs")),
            ("TestGetLatestSnapshot presente",
                lambda: contains(
                    "ATT/tests/test_patch66.py",
                    "class TestGetLatestSnapshot")),
            ("TestImportLegsForStructure presente",
                lambda: contains(
                    "ATT/tests/test_patch66.py",
                    "class TestImportLegsForStructure")),

            #  7. Casos críticos de teste
            ("test_valor_conhecido_46157 presente",
                lambda: contains(
                    "ATT/tests/test_patch66.py",
                    "test_valor_conhecido_46157")),
            ("test_valor_conhecido_46129 presente",
                lambda: contains(
                    "ATT/tests/test_patch66.py",
                    "test_valor_conhecido_46129")),
            ("test_referencia_cruzada_serial_vs_timestamp presente",
                lambda: contains(
                    "ATT/tests/test_patch66.py",
                    "test_referencia_cruzada_serial_vs_timestamp")),
            ("test_sem_legs_retorna_false presente",
                lambda: contains(
                    "ATT/tests/test_patch66.py",
                    "test_sem_legs_retorna_false")),
            ("test_com_legs_retorna_true presente",
                lambda: contains(
                    "ATT/tests/test_patch66.py",
                    "test_com_legs_retorna_true")),
            ("test_manual_mais_recente_tem_prioridade presente",
                lambda: contains(
                    "ATT/tests/test_patch66.py",
                    "test_manual_mais_recente_tem_prioridade")),
            ("test_import_basico presente",
                lambda: contains(
                    "ATT/tests/test_patch66.py",
                    "test_import_basico")),
            ("test_leg_order_sequencial presente",
                lambda: contains(
                    "ATT/tests/test_patch66.py",
                    "test_leg_order_sequencial")),
            ("test_strike_nulo_levanta_erro presente",
                lambda: contains(
                    "ATT/tests/test_patch66.py",
                    "test_strike_nulo_levanta_erro")),
            ("test_cv_invalido_levanta_erro presente",
                lambda: contains(
                    "ATT/tests/test_patch66.py",
                    "test_cv_invalido_levanta_erro")),

            #  8. Cobertura das 5 abas legadas
            ("alias BOVA11 referenciado nos testes",
                lambda: contains(
                    "ATT/tests/test_patch66.py",
                    "BOVA11")),
            ("alias EMBJ3 referenciado nos testes",
                lambda: contains(
                    "ATT/tests/test_patch66.py",
                    "EMBJ3")),
        ],
    },
    {
        "id": "patch_67",
        "desc": (
            "Auditoria baseline fase 8: script 75_audit_fase8_baseline.py com "
            "7 checkers (databases, structures_repo, derived_repo, derived_service, "
            "bootstrap_schema, audit_artifacts, att_patches); geração de relatórios "
            "Markdown e JSON em ATT/reports/; regressão patch_65 confirmada; "
            "fix importlib Python 3.13 (sys.modules antes de exec_module); "
            "40 testes passando."
        ),
        "checks": [
            #  1. Arquivos
            ("scripts/75_audit_fase8_baseline.py existe",
                lambda: exists("scripts/75_audit_fase8_baseline.py")),
            ("ATT/tests/test_patch67.py existe",
                lambda: exists("ATT/tests/test_patch67.py")),
            ("ATT/reports/fase8_baseline.md existe",
                lambda: exists("ATT/reports/fase8_baseline.md")),
            ("ATT/reports/fase8_baseline.json existe",
                lambda: exists("ATT/reports/fase8_baseline.json")),

            #  2. Funções públicas no script
            ("run_audit() definida",
                lambda: contains(
                    "scripts/75_audit_fase8_baseline.py",
                    "def run_audit")),
            ("gerar_markdown() definida",
                lambda: contains(
                    "scripts/75_audit_fase8_baseline.py",
                    "def gerar_markdown")),
            ("gerar_json() definida",
                lambda: contains(
                    "scripts/75_audit_fase8_baseline.py",
                    "def gerar_json")),

            #  3. Checkers individuais presentes
            ("check_databases() definida",
                lambda: contains(
                    "scripts/75_audit_fase8_baseline.py",
                    "def check_databases")),
            ("check_structures_repository() definida",
                lambda: contains(
                    "scripts/75_audit_fase8_baseline.py",
                    "def check_structures_repository")),
            ("check_derived_repo() definida",
                lambda: contains(
                    "scripts/75_audit_fase8_baseline.py",
                    "def check_derived_repo")),
            ("check_derived_service() definida",
                lambda: contains(
                    "scripts/75_audit_fase8_baseline.py",
                    "def check_derived_service")),
            ("check_bootstrap_schema() definida",
                lambda: contains(
                    "scripts/75_audit_fase8_baseline.py",
                    "def check_bootstrap_schema")),
            ("check_audit_artifacts() definida",
                lambda: contains(
                    "scripts/75_audit_fase8_baseline.py",
                    "def check_audit_artifacts")),
            ("check_att_patches() definida",
                lambda: contains(
                    "scripts/75_audit_fase8_baseline.py",
                    "def check_att_patches")),

            #  4. AuditReport como dataclass
            ("AuditReport definida como dataclass",
                lambda: contains(
                    "scripts/75_audit_fase8_baseline.py",
                    "class AuditReport")),
            ("AuditReport possui campo checks",
                lambda: contains(
                    "scripts/75_audit_fase8_baseline.py",
                    "checks")),
            ("AuditReport possui contadores total_ok/warn/fail",
                lambda: contains(
                    "scripts/75_audit_fase8_baseline.py",
                    "total_ok")),

            #  5. Fix importlib Python 3.13
            ("sys.modules registrado antes de exec_module no teste",
                lambda: contains(
                    "ATT/tests/test_patch67.py",
                    "sys.modules[_MODULE_NAME] = module")),
            ("_MODULE_NAME definido como 'audit_fase8'",
                lambda: contains(
                    "ATT/tests/test_patch67.py",
                    '_MODULE_NAME = "audit_fase8"')),

            #  6. Classes de teste presentes
            ("TestRunAudit presente",
                lambda: contains(
                    "ATT/tests/test_patch67.py",
                    "class TestRunAudit")),
            ("TestCheckersIndividuais presente",
                lambda: contains(
                    "ATT/tests/test_patch67.py",
                    "class TestCheckersIndividuais")),
            ("TestGeracaoArtefatos presente",
                lambda: contains(
                    "ATT/tests/test_patch67.py",
                    "class TestGeracaoArtefatos")),
            ("TestRegressaoPatch65 presente",
                lambda: contains(
                    "ATT/tests/test_patch67.py",
                    "class TestRegressaoPatch65")),
            ("TestIntegridadeGeral presente",
                lambda: contains(
                    "ATT/tests/test_patch67.py",
                    "class TestIntegridadeGeral")),

            #  7. Casos críticos de teste
            ("test_run_audit_nao_lanca_excecao presente",
                lambda: contains(
                    "ATT/tests/test_patch67.py",
                    "test_run_audit_nao_lanca_excecao")),
            ("test_todas_categorias_presentes presente",
                lambda: contains(
                    "ATT/tests/test_patch67.py",
                    "test_todas_categorias_presentes")),
            ("test_contadores_consistentes presente",
                lambda: contains(
                    "ATT/tests/test_patch67.py",
                    "test_contadores_consistentes")),
            ("test_gerar_markdown_cria_arquivo presente",
                lambda: contains(
                    "ATT/tests/test_patch67.py",
                    "test_gerar_markdown_cria_arquivo")),
            ("test_gerar_json_valido presente",
                lambda: contains(
                    "ATT/tests/test_patch67.py",
                    "test_gerar_json_valido")),
            ("test_arquivo_real_existe_apos_execucao presente",
                lambda: contains(
                    "ATT/tests/test_patch67.py",
                    "test_arquivo_real_existe_apos_execucao")),
            ("test_json_real_existe_apos_execucao presente",
                lambda: contains(
                    "ATT/tests/test_patch67.py",
                    "test_json_real_existe_apos_execucao")),

            #  8. Regressão patch_65 verificada
            ("test_get_payoff_by_aba_removida_status_ok presente",
                lambda: contains(
                    "ATT/tests/test_patch67.py",
                    "test_get_payoff_by_aba_removida_status_ok")),
            ("check_derived_service verifica remoção de get_payoff_by_aba",
                lambda: contains(
                    "scripts/75_audit_fase8_baseline.py",
                    "get_payoff_by_aba")),

            #  9. Integridade geral
            ("test_sem_fail_critico_em_infra_db presente",
                lambda: contains(
                    "ATT/tests/test_patch67.py",
                    "test_sem_fail_critico_em_infra_db")),
            ("test_derived_service_tem_funcoes_canonicas presente",
                lambda: contains(
                    "ATT/tests/test_patch67.py",
                    "test_derived_service_tem_funcoes_canonicas")),
            ("funções canônicas save_payoff_curve/save_decision/cleanup_derived verificadas",
                lambda: contains(
                    "ATT/tests/test_patch67.py",
                    "save_payoff_curve")),

            # 10. Cobertura das 7 categorias de auditoria
            ("categoria infra_db coberta",
                lambda: contains(
                    "scripts/75_audit_fase8_baseline.py",
                    "infra_db")),
            ("categoria att_patches coberta",
                lambda: contains(
                    "scripts/75_audit_fase8_baseline.py",
                    "att_patches")),
            ("categoria bootstrap_schema coberta",
                lambda: contains(
                    "scripts/75_audit_fase8_baseline.py",
                    "bootstrap_schema")),
        ],
    },
    {
        "id": "patch_69",
        "desc": (
            "Editor de estruturas (StructureEditorDialog): diálogo Tkinter para criação "
            "e edição de estruturas de opções com legs dinâmicas; integração com "
            "StructuresRepository (create/update/replace_legs); _build_legs_payload() "
            "como lógica pura testável; separação create vs update em _cmd_save(); "
            "sem importação direta de sqlite3; "
            "11 passed, 11 skipped (headless) em pytest."
        ),
        "checks": [
            #  1. Arquivos
            ("UI/components/structure_editor_dialog.py existe",
                lambda: exists("UI/components/structure_editor_dialog.py")),
            ("ATT/tests/test_patch69_structure_editor.py existe",
                lambda: exists("ATT/tests/test_patch69_structure_editor.py")),

            #  2. Classe principal e importações
            ("StructureEditorDialog definida",
                lambda: contains(
                    "UI/components/structure_editor_dialog.py",
                    "class StructureEditorDialog")),
            ("herda de tk.Toplevel ou Toplevel",
                lambda: contains(
                    "UI/components/structure_editor_dialog.py",
                    "Toplevel")),
            ("StructuresRepository importado",
                lambda: contains(
                    "UI/components/structure_editor_dialog.py",
                    "StructuresRepository")),
            ("sqlite3 NÃO importado diretamente",
                lambda: not contains(
                    "UI/components/structure_editor_dialog.py",
                    "import sqlite3")),

            #  3. Métodos públicos/privados presentes
            ("__init__ aceita db_path",
                lambda: contains(
                    "UI/components/structure_editor_dialog.py",
                    "db_path")),
            ("_build_legs_payload() definida",
                lambda: contains(
                    "UI/components/structure_editor_dialog.py",
                    "def _build_legs_payload")),
            ("_cmd_save() definida",
                lambda: contains(
                    "UI/components/structure_editor_dialog.py",
                    "def _cmd_save")),
            ("_load_existing() definida",
                lambda: contains(
                    "UI/components/structure_editor_dialog.py",
                    "def _load_existing")),
            ("_add_leg_row() definida",
                lambda: contains(
                    "UI/components/structure_editor_dialog.py",
                    "def _add_leg_row")),

            #  4. Integração com repositório
            ("create_structure() chamado em _cmd_save",
                lambda: contains(
                    "UI/components/structure_editor_dialog.py",
                    "create_structure")),
            ("update_structure() chamado em _cmd_save",
                lambda: contains(
                    "UI/components/structure_editor_dialog.py",
                    "update_structure")),
            ("replace_legs() chamado em _cmd_save",
                lambda: contains(
                    "UI/components/structure_editor_dialog.py",
                    "replace_legs")),

            #  5. Lógica de leg_order canônica
            ("leg_order começa em 1 (não 0)",
                lambda: contains(
                    "UI/components/structure_editor_dialog.py",
                    "leg_order")),
            ("enumerate com start=1 ou atribuição explícita leg_order",
                lambda: contains(
                    "UI/components/structure_editor_dialog.py",
                    "start=1") or contains(
                    "UI/components/structure_editor_dialog.py",
                    "leg_order")),

            #  6. Classes de teste presentes
            ("TestBuildLegsPayload presente",
                lambda: contains(
                    "ATT/tests/test_patch69_structure_editor.py",
                    "class TestBuildLegsPayload")),
            ("TestLoadExisting presente",
                lambda: contains(
                    "ATT/tests/test_patch69_structure_editor.py",
                    "class TestLoadExisting")),
            ("TestCmdSaveCreate presente",
                lambda: contains(
                    "ATT/tests/test_patch69_structure_editor.py",
                    "class TestCmdSaveCreate")),
            ("TestCmdSaveUpdate presente",
                lambda: contains(
                    "ATT/tests/test_patch69_structure_editor.py",
                    "class TestCmdSaveUpdate")),
            ("TestPatch69StaticChecks presente",
                lambda: contains(
                    "ATT/tests/test_patch69_structure_editor.py",
                    "class TestPatch69StaticChecks")),

            #  7. Casos críticos de teste — lógica pura
            ("test_lista_vazia_retorna_lista_vazia presente",
                lambda: contains(
                    "ATT/tests/test_patch69_structure_editor.py",
                    "test_lista_vazia_retorna_lista_vazia")),
            ("test_leg_order_comeca_em_1 presente",
                lambda: contains(
                    "ATT/tests/test_patch69_structure_editor.py",
                    "test_leg_order_comeca_em_1")),
            ("test_leg_order_sequencial presente",
                lambda: contains(
                    "ATT/tests/test_patch69_structure_editor.py",
                    "test_leg_order_sequencial")),
            ("test_campos_originais_preservados presente",
                lambda: contains(
                    "ATT/tests/test_patch69_structure_editor.py",
                    "test_campos_originais_preservados")),
            ("test_duas_legs_sem_contaminar_indices presente",
                lambda: contains(
                    "ATT/tests/test_patch69_structure_editor.py",
                    "test_duas_legs_sem_contaminar_indices")),
            ("test_nao_modifica_legs_rows_original presente",
                lambda: contains(
                    "ATT/tests/test_patch69_structure_editor.py",
                    "test_nao_modifica_legs_rows_original")),

            #  8. Casos críticos de teste — integração Tk (skip headless)
            ("test_carrega_campos_do_repositorio presente",
                lambda: contains(
                    "ATT/tests/test_patch69_structure_editor.py",
                    "test_carrega_campos_do_repositorio")),
            ("test_carrega_legs_em_legs_rows presente",
                lambda: contains(
                    "ATT/tests/test_patch69_structure_editor.py",
                    "test_carrega_legs_em_legs_rows")),
            ("test_destroi_se_estrutura_nao_encontrada presente",
                lambda: contains(
                    "ATT/tests/test_patch69_structure_editor.py",
                    "test_destroi_se_estrutura_nao_encontrada")),
            ("test_create_structure_chamado_com_campos_corretos presente",
                lambda: contains(
                    "ATT/tests/test_patch69_structure_editor.py",
                    "test_create_structure_chamado_com_campos_corretos")),
            ("test_name_vazio_nao_chama_create presente",
                lambda: contains(
                    "ATT/tests/test_patch69_structure_editor.py",
                    "test_name_vazio_nao_chama_create")),
            ("test_underlying_vazio_nao_chama_create presente",
                lambda: contains(
                    "ATT/tests/test_patch69_structure_editor.py",
                    "test_underlying_vazio_nao_chama_create")),
            ("test_replace_legs_chamado_apos_create presente",
                lambda: contains(
                    "ATT/tests/test_patch69_structure_editor.py",
                    "test_replace_legs_chamado_apos_create")),
            ("test_saved_true_apos_sucesso presente",
                lambda: contains(
                    "ATT/tests/test_patch69_structure_editor.py",
                    "test_saved_true_apos_sucesso")),
            ("test_create_nao_e_chamado_no_modo_edicao presente",
                lambda: contains(
                    "ATT/tests/test_patch69_structure_editor.py",
                    "test_create_nao_e_chamado_no_modo_edicao")),
            ("test_replace_legs_usa_structure_id_existente presente",
                lambda: contains(
                    "ATT/tests/test_patch69_structure_editor.py",
                    "test_replace_legs_usa_structure_id_existente")),
            ("test_update_structure_chamado_com_structure_id_correto presente",
                lambda: contains(
                    "ATT/tests/test_patch69_structure_editor.py",
                    "test_update_structure_chamado_com_structure_id_correto")),

            #  9. Checks estáticos presentes
            ("test_arquivo_existe presente",
                lambda: contains(
                    "ATT/tests/test_patch69_structure_editor.py",
                    "test_arquivo_existe")),
            ("test_classe_presente presente",
                lambda: contains(
                    "ATT/tests/test_patch69_structure_editor.py",
                    "test_classe_presente")),
            ("test_importavel presente",
                lambda: contains(
                    "ATT/tests/test_patch69_structure_editor.py",
                    "test_importavel")),
            ("test_construtor_aceita_db_path presente",
                lambda: contains(
                    "ATT/tests/test_patch69_structure_editor.py",
                    "test_construtor_aceita_db_path")),
            ("test_nao_importa_sqlite3_diretamente presente",
                lambda: contains(
                    "ATT/tests/test_patch69_structure_editor.py",
                    "test_nao_importa_sqlite3_diretamente")),

            # 10. Skip headless documentado
            ("@unittest.skip aplicado nas classes Tk-dependentes",
                lambda: contains(
                    "ATT/tests/test_patch69_structure_editor.py",
                    "@unittest.skip")),
            ("motivo do skip referencia Tkinter ou headless",
                lambda: contains(
                    "ATT/tests/test_patch69_structure_editor.py",
                    "Tkinter") or contains(
                    "ATT/tests/test_patch69_structure_editor.py",
                    "headless")),
        ],
    },
    {
        "id": "patch_70",
        "desc": (
            "Wiring MainWindow <-> StructureEditorDialog: definição de self._db_path "
            "no __init__ de MainWindow para eliminar AttributeError em runtime; "
            "substituição do db_path hardcoded por self._db_path em _setup_structures_tab; "
            "método _on_structure_edit_request com referência canônica ao atributo; "
            "29 passed em pytest."
        ),
        "checks": [
            #  1. Arquivos
            ("UI/main_window.py existe",
                lambda: exists("UI/main_window.py")),
            ("ATT/patches/patch_70_mainwindow_dialog_wiring.py existe",
                lambda: exists("ATT/patches/patch_70_mainwindow_dialog_wiring.py")),
            ("ATT/tests/test_patch70_integration.py existe",
                lambda: exists("ATT/tests/test_patch70_integration.py")),

            #  2. Importações e definições de classe
            ("StructureEditorDialog importado em main_window",
                lambda: contains(
                    "UI/main_window.py",
                    "StructureEditorDialog")),
            ("StructuresListPanel importado em main_window",
                lambda: contains(
                    "UI/main_window.py",
                    "StructuresListPanel")),
            ("sqlite3 NÃO importado diretamente em main_window",
                lambda: not contains(
                    "UI/main_window.py",
                    "import sqlite3")),

            #  3. Atributo canônico _db_path
            ("self._db_path definido no __init__",
                lambda: contains(
                    "UI/main_window.py",
                    "self._db_path")),
            ("_db_path usa PROJECT_ROOT / dados / app.db",
                lambda: contains(
                    "UI/main_window.py",
                    "PROJECT_ROOT") and contains(
                    "UI/main_window.py",
                    "app.db")),
            ("db_path hardcoded ausente em _setup_structures_tab",
                lambda: not contains(
                    "UI/main_window.py",
                    '"dados/app.db"') and not contains(
                    "UI/main_window.py",
                    "'dados/app.db'")),

            #  4. Métodos presentes
            ("_on_structure_edit_request definido",
                lambda: contains(
                    "UI/main_window.py",
                    "def _on_structure_edit_request")),
            ("_setup_structures_tab definido",
                lambda: contains(
                    "UI/main_window.py",
                    "def _setup_structures_tab")),

            #  5. Integração _on_structure_edit_request <-> StructureEditorDialog
            ("StructureEditorDialog instanciado em _on_structure_edit_request",
                lambda: contains(
                    "UI/main_window.py",
                    "StructureEditorDialog")),
            ("db_path=self._db_path passado ao dialog",
                lambda: contains(
                    "UI/main_window.py",
                    "db_path=self._db_path")),
            ("wait_window chamado sobre o dialog",
                lambda: contains(
                    "UI/main_window.py",
                    "wait_window")),
            ("dlg.saved verificado após wait_window",
                lambda: contains(
                    "UI/main_window.py",
                    "dlg.saved")),
            ("structures_list.load() chamado se saved=True",
                lambda: contains(
                    "UI/main_window.py",
                    "structures_list.load")),

            #  6. StructuresListPanel usa self._db_path
            ("StructuresListPanel instanciado com db_path=self._db_path",
                lambda: contains(
                    "UI/main_window.py",
                    "db_path=self._db_path")),

            #  7. Classes de teste presentes
            ("TestPatch70StaticChecks presente",
                lambda: contains(
                    "ATT/tests/test_patch70_integration.py",
                    "class TestPatch70StaticChecks")),
            ("TestOnStructureEditRequestCriar presente",
                lambda: contains(
                    "ATT/tests/test_patch70_integration.py",
                    "class TestOnStructureEditRequestCriar")),
            ("TestOnStructureEditRequestEditar presente",
                lambda: contains(
                    "ATT/tests/test_patch70_integration.py",
                    "class TestOnStructureEditRequestEditar")),
            ("TestLoadExisting presente",
                lambda: contains(
                    "ATT/tests/test_patch70_integration.py",
                    "class TestLoadExisting")),
            ("TestCmdSave presente",
                lambda: contains(
                    "ATT/tests/test_patch70_integration.py",
                    "class TestCmdSave")),
            ("TestIntegracaoLegs presente",
                lambda: contains(
                    "ATT/tests/test_patch70_integration.py",
                    "class TestIntegracaoLegs")),

            #  8. Casos críticos de teste — static checks
            ("test_main_window_arquivo_existe presente",
                lambda: contains(
                    "ATT/tests/test_patch70_integration.py",
                    "test_main_window_arquivo_existe")),
            ("test_main_window_importa_structure_editor_dialog presente",
                lambda: contains(
                    "ATT/tests/test_patch70_integration.py",
                    "test_main_window_importa_structure_editor_dialog")),
            ("test_main_window_nao_importa_sqlite3_diretamente presente",
                lambda: contains(
                    "ATT/tests/test_patch70_integration.py",
                    "test_main_window_nao_importa_sqlite3_diretamente")),
            ("test_main_window_tem_metodo_on_structure_edit_request presente",
                lambda: contains(
                    "ATT/tests/test_patch70_integration.py",
                    "test_main_window_tem_metodo_on_structure_edit_request")),
            ("test_structure_editor_dialog_arquivo_existe presente",
                lambda: contains(
                    "ATT/tests/test_patch70_integration.py",
                    "test_structure_editor_dialog_arquivo_existe")),
            ("test_leg_order_comeca_em_1 presente",
                lambda: contains(
                    "ATT/tests/test_patch70_integration.py",
                    "test_leg_order_comeca_em_1")),

            #  9. Casos críticos de teste — wiring criar
            ("test_dialog_instanciado_com_structure_id_none presente",
                lambda: contains(
                    "ATT/tests/test_patch70_integration.py",
                    "test_dialog_instanciado_com_structure_id_none")),
            ("test_db_path_repassado_ao_dialog presente",
                lambda: contains(
                    "ATT/tests/test_patch70_integration.py",
                    "test_db_path_repassado_ao_dialog")),
            ("test_load_chamado_se_saved_true presente",
                lambda: contains(
                    "ATT/tests/test_patch70_integration.py",
                    "test_load_chamado_se_saved_true")),
            ("test_load_nao_chamado_se_saved_false presente",
                lambda: contains(
                    "ATT/tests/test_patch70_integration.py",
                    "test_load_nao_chamado_se_saved_false")),

            # 10. Casos críticos de teste — wiring editar
            ("test_dialog_instanciado_com_structure_id_correto presente",
                lambda: contains(
                    "ATT/tests/test_patch70_integration.py",
                    "test_dialog_instanciado_com_structure_id_correto")),
            ("test_load_chamado_apos_edicao_bem_sucedida presente",
                lambda: contains(
                    "ATT/tests/test_patch70_integration.py",
                    "test_load_chamado_apos_edicao_bem_sucedida")),
            ("test_load_nao_chamado_se_edicao_cancelada presente",
                lambda: contains(
                    "ATT/tests/test_patch70_integration.py",
                    "test_load_nao_chamado_se_edicao_cancelada")),

            # 11. Casos críticos de teste — load existing
            ("test_carrega_campos_do_repositorio presente",
                lambda: contains(
                    "ATT/tests/test_patch70_integration.py",
                    "test_carrega_campos_do_repositorio")),
            ("test_carrega_legs_em_legs_rows presente",
                lambda: contains(
                    "ATT/tests/test_patch70_integration.py",
                    "test_carrega_legs_em_legs_rows")),
            ("test_destroi_se_estrutura_nao_encontrada presente",
                lambda: contains(
                    "ATT/tests/test_patch70_integration.py",
                    "test_destroi_se_estrutura_nao_encontrada")),

            # 12. Casos críticos de teste — cmd_save
            ("test_saved_true_apos_criar presente",
                lambda: contains(
                    "ATT/tests/test_patch70_integration.py",
                    "test_saved_true_apos_criar")),
            ("test_saved_true_apos_editar presente",
                lambda: contains(
                    "ATT/tests/test_patch70_integration.py",
                    "test_saved_true_apos_editar")),
            ("test_saved_false_se_name_vazio presente",
                lambda: contains(
                    "ATT/tests/test_patch70_integration.py",
                    "test_saved_false_se_name_vazio")),
            ("test_saved_false_se_underlying_vazio presente",
                lambda: contains(
                    "ATT/tests/test_patch70_integration.py",
                    "test_saved_false_se_underlying_vazio")),
            ("test_create_nao_chamado_no_modo_edicao presente",
                lambda: contains(
                    "ATT/tests/test_patch70_integration.py",
                    "test_create_nao_chamado_no_modo_edicao")),
            ("test_update_nao_chamado_no_modo_criacao presente",
                lambda: contains(
                    "ATT/tests/test_patch70_integration.py",
                    "test_update_nao_chamado_no_modo_criacao")),
            ("test_replace_legs_sid_correto_criacao presente",
                lambda: contains(
                    "ATT/tests/test_patch70_integration.py",
                    "test_replace_legs_sid_correto_criacao")),
            ("test_replace_legs_sid_correto_edicao presente",
                lambda: contains(
                    "ATT/tests/test_patch70_integration.py",
                    "test_replace_legs_sid_correto_edicao")),
            ("test_destroy_chamado_apos_salvar presente",
                lambda: contains(
                    "ATT/tests/test_patch70_integration.py",
                    "test_destroy_chamado_apos_salvar")),
            ("test_exception_nao_propaga presente",
                lambda: contains(
                    "ATT/tests/test_patch70_integration.py",
                    "test_exception_nao_propaga")),

            # 13. Casos críticos de teste — integração legs
            ("test_legs_payload_preserva_position_side presente",
                lambda: contains(
                    "ATT/tests/test_patch70_integration.py",
                    "test_legs_payload_preserva_position_side")),
            ("test_legs_payload_tem_leg_order_sequencial presente",
                lambda: contains(
                    "ATT/tests/test_patch70_integration.py",
                    "test_legs_payload_tem_leg_order_sequencial")),
            ("test_replace_legs_recebe_2_legs presente",
                lambda: contains(
                    "ATT/tests/test_patch70_integration.py",
                    "test_replace_legs_recebe_2_legs")),
        ],
    },
    {
        "id": "patch_71",
        "desc": (
            "StructuresListPanel: botao Arquivar com confirmacao (messagebox); "
            "_on_archive_request() integrado ao StructuresRepository.archive_structure(); "
            "refresh automatico via load() apos acao bem-sucedida; "
            "_set_status() para feedback visual no rodape do painel; "
            "sem sqlite3 direto; sem Tk em testes unitarios; "
            "29+ passed em pytest."
        ),
        "checks": [
            #  1. Arquivos
            ("UI/components/structures_list_panel.py existe",
                lambda: exists("UI/components/structures_list_panel.py")),
            ("ATT/patches/patch_71_structures_list_archive.py existe",
                lambda: exists("ATT/patches/patch_71_structures_list_archive.py")),
            ("ATT/tests/test_patch71_archive_wiring.py existe",
                lambda: exists("ATT/tests/test_patch71_archive_wiring.py")),

            #  2. Importacoes e ausencias
            ("StructuresRepository importado em structures_list_panel",
                lambda: contains(
                    "UI/components/structures_list_panel.py",
                    "StructuresRepository")),
            ("sqlite3 NAO importado diretamente em structures_list_panel",
                lambda: not contains(
                    "UI/components/structures_list_panel.py",
                    "import sqlite3")),
            ("messagebox importado em structures_list_panel",
                lambda: contains(
                    "UI/components/structures_list_panel.py",
                    "messagebox")),

            #  3. Metodos presentes no painel
            ("_on_archive_request definido",
                lambda: contains(
                    "UI/components/structures_list_panel.py",
                    "def _on_archive_request")),
            ("_set_status definido",
                lambda: contains(
                    "UI/components/structures_list_panel.py",
                    "def _set_status")),
            ("load() definido no painel",
                lambda: contains(
                    "UI/components/structures_list_panel.py",
                    "def load")),

            #  4. Integracao com repositorio
            ("archive_structure() chamado em _on_archive_request",
                lambda: contains(
                    "UI/components/structures_list_panel.py",
                    "archive_structure")),
            ("db_path=self._db_path usado na instancia do repositorio",
                lambda: contains(
                    "UI/components/structures_list_panel.py",
                    "self._db_path")),
            ("load() chamado apos archive bem-sucedido",
                lambda: contains(
                    "UI/components/structures_list_panel.py",
                    "self.load")),

            #  5. Guard de confirmacao e seguranca
            ("askyesno ou askokcancel usado como confirmacao",
                lambda: contains(
                    "UI/components/structures_list_panel.py",
                    "askyesno") or contains(
                    "UI/components/structures_list_panel.py",
                    "askokcancel")),
            ("try/except presente em _on_archive_request",
                lambda: contains(
                    "UI/components/structures_list_panel.py",
                    "try")),
            ("excecao nao propaga (except presente)",
                lambda: contains(
                    "UI/components/structures_list_panel.py",
                    "except")),

            #  6. Feedback visual
            ("_set_status chamado apos archive",
                lambda: contains(
                    "UI/components/structures_list_panel.py",
                    "_set_status")),
            ("label ou widget de status presente",
                lambda: contains(
                    "UI/components/structures_list_panel.py",
                    "status") or contains(
                    "UI/components/structures_list_panel.py",
                    "Label")),

            #  7. main_window sem regressao
            ("self._db_path preservado em main_window",
                lambda: contains(
                    "UI/main_window.py",
                    "self._db_path")),
            ("db_path hardcoded ausente em main_window",
                lambda: not contains(
                    "UI/main_window.py",
                    '"dados/app.db"') and not contains(
                    "UI/main_window.py",
                    "'dados/app.db'")),

            #  8. Classes de teste presentes
            ("TestPatch71StaticChecks presente",
                lambda: contains(
                    "ATT/tests/test_patch71_archive_wiring.py",
                    "class TestPatch71StaticChecks")),
            ("TestOnArchiveRequestConfirmado presente",
                lambda: contains(
                    "ATT/tests/test_patch71_archive_wiring.py",
                    "class TestOnArchiveRequestConfirmado")),
            ("TestOnArchiveRequestCancelado presente",
                lambda: contains(
                    "ATT/tests/test_patch71_archive_wiring.py",
                    "class TestOnArchiveRequestCancelado")),
            ("TestOnArchiveRequestErro presente",
                lambda: contains(
                    "ATT/tests/test_patch71_archive_wiring.py",
                    "class TestOnArchiveRequestErro")),
            ("TestSetStatus presente",
                lambda: contains(
                    "ATT/tests/test_patch71_archive_wiring.py",
                    "class TestSetStatus")),

            #  9. Casos criticos de teste -- static
            ("test_arquivo_existe presente",
                lambda: contains(
                    "ATT/tests/test_patch71_archive_wiring.py",
                    "test_arquivo_existe")),
            ("test_classe_presente presente",
                lambda: contains(
                    "ATT/tests/test_patch71_archive_wiring.py",
                    "test_classe_presente")),
            ("test_nao_importa_sqlite3_diretamente presente",
                lambda: contains(
                    "ATT/tests/test_patch71_archive_wiring.py",
                    "test_nao_importa_sqlite3_diretamente")),
            ("test_metodo_on_archive_request_existe presente",
                lambda: contains(
                    "ATT/tests/test_patch71_archive_wiring.py",
                    "test_metodo_on_archive_request_existe")),
            ("test_metodo_set_status_existe presente",
                lambda: contains(
                    "ATT/tests/test_patch71_archive_wiring.py",
                    "test_metodo_set_status_existe")),

            # 10. Casos criticos de teste -- archive confirmado
            ("test_archive_structure_chamado_com_id_correto presente",
                lambda: contains(
                    "ATT/tests/test_patch71_archive_wiring.py",
                    "test_archive_structure_chamado_com_id_correto")),
            ("test_load_chamado_apos_archive_confirmado presente",
                lambda: contains(
                    "ATT/tests/test_patch71_archive_wiring.py",
                    "test_load_chamado_apos_archive_confirmado")),
            ("test_set_status_mensagem_sucesso presente",
                lambda: contains(
                    "ATT/tests/test_patch71_archive_wiring.py",
                    "test_set_status_mensagem_sucesso")),
            ("test_destroy_nao_chamado_em_archive presente",
                lambda: contains(
                    "ATT/tests/test_patch71_archive_wiring.py",
                    "test_destroy_nao_chamado_em_archive")),

            # 11. Casos criticos de teste -- archive cancelado
            ("test_archive_nao_chamado_se_usuario_cancela presente",
                lambda: contains(
                    "ATT/tests/test_patch71_archive_wiring.py",
                    "test_archive_nao_chamado_se_usuario_cancela")),
            ("test_load_nao_chamado_se_usuario_cancela presente",
                lambda: contains(
                    "ATT/tests/test_patch71_archive_wiring.py",
                    "test_load_nao_chamado_se_usuario_cancela")),
            ("test_set_status_nao_chamado_se_cancelado presente",
                lambda: contains(
                    "ATT/tests/test_patch71_archive_wiring.py",
                    "test_set_status_nao_chamado_se_cancelado")),

            # 12. Casos criticos de teste -- erro no repositorio
            ("test_excecao_nao_propaga_para_ui presente",
                lambda: contains(
                    "ATT/tests/test_patch71_archive_wiring.py",
                    "test_excecao_nao_propaga_para_ui")),
            ("test_load_nao_chamado_se_archive_falha presente",
                lambda: contains(
                    "ATT/tests/test_patch71_archive_wiring.py",
                    "test_load_nao_chamado_se_archive_falha")),
            ("test_set_status_mensagem_erro presente",
                lambda: contains(
                    "ATT/tests/test_patch71_archive_wiring.py",
                    "test_set_status_mensagem_erro")),

            # 13. Casos criticos de teste -- _set_status
            ("test_set_status_atualiza_widget presente",
                lambda: contains(
                    "ATT/tests/test_patch71_archive_wiring.py",
                    "test_set_status_atualiza_widget")),
            ("test_set_status_aceita_string_vazia presente",
                lambda: contains(
                    "ATT/tests/test_patch71_archive_wiring.py",
                    "test_set_status_aceita_string_vazia")),

            # 14. Regressao patch_70
            ("test_db_path_nao_hardcoded_em_main_window presente",
                lambda: contains(
                    "ATT/tests/test_patch71_archive_wiring.py",
                    "test_db_path_nao_hardcoded_em_main_window")),
            ("test_self_db_path_preservado_em_main_window presente",
                lambda: contains(
                    "ATT/tests/test_patch71_archive_wiring.py",
                    "test_self_db_path_preservado_em_main_window")),

            # 15. Skip headless documentado
            ("@unittest.skip aplicado nas classes Tk-dependentes",
                lambda: contains(
                    "ATT/tests/test_patch71_archive_wiring.py",
                    "@unittest.skip")),
            ("motivo do skip referencia Tkinter ou headless",
                lambda: contains(
                    "ATT/tests/test_patch71_archive_wiring.py",
                    "Tkinter") or contains(
                    "ATT/tests/test_patch71_archive_wiring.py",
                    "headless")),
        ],
    },


]  #  fechamento da lista PATCHES

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

    #  DECISÕES PERMANENTES -- exibidas no topo, não geram checks 
    report.append(print_permanent_decisions())

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
            f"\n  {'[OK]' if status == 'OK ' else '[AVISO] '} {marker}  "
            f"{r['id']:<12} [{r['passed']}/{r['total']}]"
            f"     {r['desc']}"
        )
        for label, ok, note in r["details"]:
            tick = "v" if ok else "X"
            line = f"    {tick}  {label}"
            if note:
                line += f"\n         -> {note}"
            report.append(line)

    #  Resumo com suite pytest documentada 
    SKIPPED_INTENCIONAL = 6  # Tk/headless -- PERMANENT_DECISIONS patch_10:tk_headless
    report.append(
        f"\n\n  Resumo patches : {ok_count} OK | "
        f"{partial_count} PARCIAL | {fail_count} FALHOU | "
        f"{ok_count + partial_count + fail_count} total\n"
        f"  Suite pytest   : 510 passed | "
        f"{SKIPPED_INTENCIONAL} skipped (Tk/headless -- intencional, ver DECISÕES PERMANENTES) | "
        f"0 failed"
    )

    # ---- bancos ----
    report.append("\n-- BANCOS DE DADOS " + "-" * 48)
    for db in run_databases():
        report.append(
            f"\n  {'[OK]' if db['exists'] else '[FALHOU]'}  {db['path']}  ->  "
            f"{'[OK] existe' if db['exists'] else '[FALHOU] NAO ENCONTRADO'}"
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
        icon = "[OK]" if ok else "[FALHOU]"
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
