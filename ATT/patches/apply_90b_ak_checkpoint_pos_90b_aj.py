from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT / "ATT" / "reports"
DOCS_DIR = ROOT / "docs"

REPORT_JSON = REPORTS_DIR / "frente_90b_ak_checkpoint_pos_90b_aj.json"
REPORT_MD = REPORTS_DIR / "frente_90b_ak_checkpoint_pos_90b_aj.md"
DOCUMENT_MD = DOCS_DIR / "FRENTE_90B_AK_CHECKPOINT_POS_90B_AJ.md"

TARGETS = (
    "ATT/patches/audit_90b_ae_bootstrap_migrations_connection_inventory.py",
    "ATT/tests/test_frente_90b_ae_bootstrap_migrations_connection_inventory.py",
    "ATT/run_frente_90b_af_migrations_remanescentes_normalizadas.sh",
    "ATT/run_frente_90b_ai_repair_idempotencia_90b_af.sh",
)


def build_payload() -> dict[str, object]:
    target_status = [
        {
            "path": relative_path,
            "exists": (ROOT / relative_path).is_file(),
        }
        for relative_path in TARGETS
    ]
    missing_paths = [
        item["path"]
        for item in target_status
        if not item["exists"]
    ]

    return {
        "frente": "90B-AK",
        "status": (
            "CHECKPOINT_ONLY_PENDING_RUNNER_VALIDATION"
            if not missing_paths
            else "CHECKPOINT_BLOCKED_MISSING_ATT_ARTIFACTS"
        ),
        "objective": (
            "Registrar o checkpoint posterior ao repair 90B-AJ e preparar "
            "a revalidacao controlada da cadeia 90B-AI, 90B-AF e 90B-AE."
        ),
        "targets": target_status,
        "missing_paths": missing_paths,
        "scope": {
            "production_files_modified": False,
            "sqlite_connections_opened": False,
            "sqlite_schema_modified": False,
            "sqlite_data_modified": False,
            "ui_modified": False,
            "git_used": False,
        },
        "acceptance": {
            "attifacts_required_present": not missing_paths,
            "checkpoint_generated": True,
            "requires_90b_ai_runner": True,
            "requires_90b_af_runner": True,
            "requires_90b_ae_documentation_assertion": True,
        },
    }


def build_markdown(payload: dict[str, object]) -> str:
    target_lines = "\n".join(
        (
            f"| `{item['path']}` | "
            f"`{'sim' if item['exists'] else 'nao'}` |"
        )
        for item in payload["targets"]
    )
    missing_paths = payload["missing_paths"]
    missing_text = ", ".join(missing_paths) if missing_paths else "nenhum"

    return f"""# Frente 90B-AK - Checkpoint posterior ao repair 90B-AJ

## Objetivo

Registrar uma evidencia auditavel posterior ao repair 90B-AJ e preparar a
revalidacao encadeada das frentes 90B-AI, 90B-AF e 90B-AE.

## Escopo

- Nenhuma alteracao de schema SQLite.
- Nenhuma alteracao de dados SQLite.
- Nenhuma alteracao de arquivo produtivo.
- Nenhuma alteracao de UI.
- Nenhum uso de Git.
- O checkpoint apenas verifica a presenca dos artefatos ATT necessarios e
  delega a validacao funcional aos runners ja existentes.

## Artefatos requeridos

| Caminho | Existe |
|---|---:|
{target_lines}

## Resultado do inventario do checkpoint

- Status: `{payload["status"]}`
- Artefatos ausentes: `{missing_text}`
- Schema SQLite alterado: `nao`
- Dados SQLite alterados: `nao`
- Arquivos produtivos alterados: `nao`
- UI alterada: `nao`
- Git utilizado: `nao`

## Revalidacao operacional exigida

A validacao funcional deve executar, nesta ordem:

1. `ATT/run_frente_90b_ai_repair_idempotencia_90b_af.sh`;
2. `ATT/run_frente_90b_af_migrations_remanescentes_normalizadas.sh`;
3. o teste 90B-AE que exige a frase literal
   `Nenhuma alteracao de schema` na documentacao gerada.

O checkpoint nao mascara falhas preexistentes. Caso qualquer runner falhe, o
resultado final deve permanecer nao aprovado.
"""


def main() -> int:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    payload = build_payload()
    markdown = build_markdown(payload)

    REPORT_JSON.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    REPORT_MD.write_text(markdown, encoding="utf-8")
    DOCUMENT_MD.write_text(markdown, encoding="utf-8")

    print(f"STATUS={payload['status']}")
    print(f"REPORT_JSON={REPORT_JSON}")
    print(f"REPORT_MD={REPORT_MD}")
    print(f"DOCUMENT={DOCUMENT_MD}")
    print(f"ATT_ARTIFACTS_MISSING={len(payload['missing_paths'])}")
    print("PRODUCTION_TARGETS_CHANGED=0")
    print("SQLITE_CONNECTIONS_OPENED=0")
    print("SCHEMA_SQLITE_ALTERADO=0")
    print("DADOS_SQLITE_ALTERADOS=0")
    print("UI_ALTERADA=0")
    print("GIT_UTILIZADO=0")

    return 0 if not payload["missing_paths"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
