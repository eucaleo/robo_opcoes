#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

OUT_MD = ROOT / "docs" / "mapeamento_automacao_opcoes_rtd.md"
OUT_JSON = ROOT / "docs" / "mapeamento_automacao_opcoes_rtd.json"

SKIP_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".venv",
    "venv",
    "node_modules",
    "reports",
    "_repo_audit",
}

TEXT_EXTS = {
    ".py",
    ".md",
    ".txt",
    ".json",
    ".csv",
    ".sql",
    ".yml",
    ".yaml",
    ".toml",
    ".ini",
    ".cfg",
    ".sh",
    ".bat",
    ".ps1",
}

BINARY_EXTS = {
    ".xlsm",
    ".xlsx",
    ".xls",
    ".db",
    ".sqlite",
    ".sqlite3",
    ".pyc",
    ".png",
    ".jpg",
    ".jpeg",
    ".pdf",
    ".zip",
}

KEYWORDS = {
    "rtd": ["rtd", "rtd_links", "option_quotes"],
    "excel": ["excel", "xlsm", "xlsx", "analise_robo", "hist_robo"],
    "bridge": ["bridge", "csv", "ingest", "ingestao", "ingestão"],
    "opcoes": ["opcao", "opção", "opcoes", "opções", "option", "strike", "vencimento"],
    "persistencia": ["repository", "repositories", "sqlite", "schema", "migration", "insert", "upsert"],
    "servicos": ["service", "services", "provider", "selector", "assembler"],
    "ui": ["ui", "main_window", "panel", "dialog", "component"],
    "calculo": ["calculation", "pricing", "payoff", "metric", "metrics", "grega", "gregas"],
}

IMPORTANT = {
    "repositories/rtd_option_quotes_repository.py": "Prioritário para auditoria de persistência RTD.",
    "services/market_snapshot_provider.py": "Prioritário para auditoria de snapshot.",
    "services/market_snapshot_selector.py": "Prioritário para auditoria de seleção de snapshot.",
    "repositories/market_snapshot_repository.py": "Prioritário para auditoria de persistência de snapshot.",
    "services/structure_market_input_assembler.py": "Prioritário para auditoria de input de mercado.",
    "services/canonical_input_service.py": "Prioritário para auditoria de input canônico.",
    "dados/RTD_LINKS.csv": "Prioritário para auditoria do contrato RTD/Excel.",
}


def rel(path):
    return path.relative_to(ROOT).as_posix()


def read_text(path):
    if path.suffix.lower() in BINARY_EXTS:
        return ""

    if path.suffix.lower() not in TEXT_EXTS:
        return ""

    try:
        if path.stat().st_size > 1_000_000:
            return ""

        data = path.read_bytes()

        for enc in ("utf-8", "utf-8-sig", "latin-1", "cp1252"):
            try:
                return data.decode(enc)
            except UnicodeDecodeError:
                pass

        return data.decode("utf-8", errors="replace")
    except OSError:
        return ""


def count_hits(text):
    text = text.casefold()
    hits = {}

    for group, words in KEYWORDS.items():
        total = 0

        for word in words:
            total += text.count(word.casefold())

        if total:
            hits[group] = total

    return hits


def role_for(path):
    p = path.casefold()

    if p.startswith("ui/"):
        return "ui"
    if p.startswith("services/"):
        return "services"
    if p.startswith("repositories/"):
        return "repositories"
    if p.startswith("db/") or p.startswith("infra/"):
        return "db_infra"
    if p.startswith("bridge/"):
        return "bridge"
    if p.startswith("dados/"):
        return "dados_local"
    if p.startswith("scripts/"):
        return "scripts"
    if p.startswith("docs/"):
        return "docs"

    return "outros"


def iter_files():
    for current, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for name in files:
            yield Path(current) / name


def main():
    findings = []

    for path in iter_files():
        relative = rel(path)

        path_hits = count_hits(relative)
        text_hits = count_hits(read_text(path))

        score = sum(path_hits.values()) * 3 + sum(text_hits.values())
        note = IMPORTANT.get(relative, "")

        if note:
            score += 20

        if score <= 0 and not note:
            continue

        if note or score >= 12:
            level = "forte"
        elif score >= 5:
            level = "medio"
        else:
            level = "baixo"

        findings.append({
            "path": relative,
            "role": role_for(relative),
            "level": level,
            "score": score,
            "path_hits": path_hits,
            "content_hits": text_hits,
            "note": note,
        })

    findings.sort(key=lambda x: (-x["score"], x["path"]))

    OUT_MD.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "phase": "ROTA_MESTRE_2_FASE_1",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "functional_changes": False,
        "total_findings": len(findings),
        "findings": findings,
    }

    OUT_JSON.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    fortes = [x for x in findings if x["level"] == "forte"]
    medios = [x for x in findings if x["level"] == "medio"]
    baixos = [x for x in findings if x["level"] == "baixo"]

    lines = [
        "# Mapeamento automação opções RTD — ROTA_MESTRE_2 Fase 1",
        "",
        f"Gerado em: `{payload['generated_at']}`",
        "",
        "## Escopo",
        "",
        "Mapeamento amplo de RTD, Excel, bridge, opções, persistência, serviços e UI.",
        "",
        "Nenhuma alteração funcional foi realizada.",
        "",
        "## Resumo",
        "",
        f"- Total de achados: `{len(findings)}`",
        f"- Candidatos fortes: `{len(fortes)}`",
        f"- Candidatos médios: `{len(medios)}`",
        f"- Candidatos baixos: `{len(baixos)}`",
        "",
        "## Candidatos fortes",
        "",
    ]

    for item in fortes:
        lines.extend([
            f"### `{item['path']}`",
            "",
            f"- Papel provável: `{item['role']}`",
            f"- Pontuação: `{item['score']}`",
            f"- Nota: {item['note'] or 'Classificado por frequência de referências.'}",
            f"- Hits no caminho: `{item['path_hits']}`",
            f"- Hits no conteúdo: `{item['content_hits']}`",
            "",
        ])

    lines.extend([
        "## Candidatos médios",
        "",
    ])

    for item in medios:
        lines.append(f"- `{item['path']}` — `{item['role']}` — score `{item['score']}`")

    lines.extend([
        "",
        "## Candidatos baixos",
        "",
    ])

    for item in baixos:
        lines.append(f"- `{item['path']}` — `{item['role']}` — score `{item['score']}`")

    lines.extend([
        "",
        "## Decisão",
        "",
        "Este relatório serve como base para as próximas fases da ROTA_MESTRE_2.",
        "A Fase 1 não altera UI, banco, schema, cálculo, ingestão ou dados operacionais.",
    ])

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"Relatório Markdown: {rel(OUT_MD)}")
    print(f"Relatório JSON: {rel(OUT_JSON)}")
    print(f"Arquivos encontrados: {len(findings)}")


if __name__ == "__main__":
    main()
