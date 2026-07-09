from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from io import StringIO
from pathlib import Path
import tokenize


ROOT = Path(__file__).resolve().parents[2]
EVID = ROOT / "FRENTE_BD_UNICO_APPDB" / "evidencias"

OPERATIONAL_DIRS = [
    "ATT",
    "UI",
    "db",
    "domain",
    "repositories",
    "scripts",
    "services",
]

CONFIG_REL = "db/config.py"


@dataclass(frozen=True)
class Hit:
    rel: str
    line: int
    token: str
    category: str
    text: str


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def iter_py_files() -> list[Path]:
    files: list[Path] = []
    for rel in OPERATIONAL_DIRS:
        base = ROOT / rel
        if not base.exists():
            continue
        files.extend(
            p for p in base.rglob("*.py")
            if "__pycache__" not in p.parts
        )
    return sorted(set(files))


def categorize(rel: str, token: str) -> str:
    lower = token.lower()

    if rel == CONFIG_REL and token == "DERIVED_DB_PATH":
        return "OK_ALIAS_LEGADO_CONFIG"

    if token == "DERIVED_DB_PATH":
        return "BLOQUEIO_DERIVED_DB_PATH_FORA_CONFIG"

    if rel.startswith("ATT/tests/"):
        return "TESTE_COMPATIBILIDADE"

    if lower.startswith("test_") or "_test" in lower:
        return "TESTE_COMPATIBILIDADE"

    if token.isupper():
        return "REVISAR_CONSTANTE_COMPATIBILIDADE"

    if token.startswith("Derived") or token.endswith("Derived"):
        return "REVISAR_PASCAL_CAMEL_PUBLICO"

    if lower.startswith("derived_") or "_derived" in lower or lower.endswith("_derived"):
        return "CANDIDATO_INTERNO_SNAKE_CASE"

    return "REVISAR_IDENTIFICADOR_TECNICO"


def scan_file(path: Path) -> list[Hit]:
    rel = path.relative_to(ROOT).as_posix()
    text = read(path)
    lines = text.splitlines()
    hits: list[Hit] = []

    try:
        tokens = tokenize.generate_tokens(StringIO(text).readline)
        for tok in tokens:
            if tok.type != tokenize.NAME:
                continue

            token = tok.string
            if "derived" not in token.lower():
                continue

            line_no = tok.start[0]
            line_text = lines[line_no - 1].strip() if 0 <= line_no - 1 < len(lines) else ""
            category = categorize(rel, token)

            hits.append(
                Hit(
                    rel=rel,
                    line=line_no,
                    token=token,
                    category=category,
                    text=line_text,
                )
            )
    except tokenize.TokenError as exc:
        hits.append(
            Hit(
                rel=rel,
                line=0,
                token="<TOKENIZE_ERROR>",
                category="ERRO_TOKENIZE",
                text=str(exc),
            )
        )

    return hits


def main() -> None:
    EVID.mkdir(parents=True, exist_ok=True)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    files = iter_py_files()

    all_hits: list[Hit] = []
    for path in files:
        all_hits.extend(scan_file(path))

    by_category = Counter(hit.category for hit in all_hits)
    by_token = Counter(hit.token for hit in all_hits)
    files_by_token: dict[str, set[str]] = defaultdict(set)

    for hit in all_hits:
        files_by_token[hit.token].add(hit.rel)

    blocking_hits = [
        hit for hit in all_hits
        if hit.category in {
            "BLOQUEIO_DERIVED_DB_PATH_FORA_CONFIG",
            "ERRO_TOKENIZE",
        }
    ]

    candidate_hits = [
        hit for hit in all_hits
        if hit.category in {
            "CANDIDATO_INTERNO_SNAKE_CASE",
            "REVISAR_CONSTANTE_COMPATIBILIDADE",
            "REVISAR_PASCAL_CAMEL_PUBLICO",
            "REVISAR_IDENTIFICADOR_TECNICO",
        }
    ]

    detail_lines: list[str] = []
    detail_lines.append("===== DATA =====")
    detail_lines.append(now)
    detail_lines.append("")
    detail_lines.append("===== OBJETIVO =====")
    detail_lines.append("Auditar identificadores Python contendo derived, Derived ou DERIVED.")
    detail_lines.append("Esta fase e apenas classificatoria; nao altera codigo operacional.")
    detail_lines.append("Separar alias legado permitido, testes/compatibilidade e candidatos a migracao futura.")
    detail_lines.append("")
    detail_lines.append("===== ESCOPO OPERACIONAL =====")
    for rel in OPERATIONAL_DIRS:
        detail_lines.append(rel)
    detail_lines.append("")
    detail_lines.append("===== TOTAL PY VARREDOS =====")
    detail_lines.append(str(len(files)))
    detail_lines.append("")
    detail_lines.append("===== TOTAL DE OCORRENCIAS TOKEN NAME COM derived =====")
    detail_lines.append(str(len(all_hits)))
    detail_lines.append("")
    detail_lines.append("===== CONTAGEM POR CATEGORIA =====")
    if by_category:
        for category, count in sorted(by_category.items()):
            detail_lines.append(f"{category}: {count}")
    else:
        detail_lines.append("Nenhuma ocorrencia encontrada.")
    detail_lines.append("")
    detail_lines.append("===== OCORRENCIAS DETALHADAS =====")
    if all_hits:
        for hit in sorted(all_hits, key=lambda h: (h.rel, h.line, h.token)):
            detail_lines.append(
                f"{hit.category} | {hit.rel}:{hit.line}: {hit.token} | {hit.text}"
            )
    else:
        detail_lines.append("Nenhuma ocorrencia encontrada.")
    detail_lines.append("")
    detail_lines.append("===== BLOQUEIOS =====")
    if blocking_hits:
        for hit in blocking_hits:
            detail_lines.append(
                f"{hit.category} | {hit.rel}:{hit.line}: {hit.token} | {hit.text}"
            )
    else:
        detail_lines.append("Nenhum bloqueio encontrado.")
    detail_lines.append("")
    detail_lines.append("===== DECISAO =====")
    if blocking_hits:
        detail_lines.append("[BLOQUEIO] Existem ocorrencias bloqueantes. Revisar antes de prosseguir.")
    else:
        detail_lines.append("[OK] Nenhum DERIVED_DB_PATH fora de db/config.py.")
        detail_lines.append("[OK] Auditoria classificatoria concluida.")
        detail_lines.append("[OK] Proxima fase pode escolher candidatos internos seguros para renomeacao controlada.")
    detail_lines.append("")

    detail_out = EVID / "66_phase1f_d_auditoria_identificadores_derived.txt"
    detail_out.write_text("\n".join(detail_lines), encoding="utf-8")

    summary_lines: list[str] = []
    summary_lines.append("===== DATA =====")
    summary_lines.append(now)
    summary_lines.append("")
    summary_lines.append("===== OBJETIVO =====")
    summary_lines.append("Resumo agrupado dos identificadores Python contendo derived.")
    summary_lines.append("")
    summary_lines.append("===== RESUMO POR TOKEN =====")
    if by_token:
        summary_lines.append("categoria\tocorrencias\tarquivos\ttoken")
        for token, count in sorted(by_token.items(), key=lambda item: (-item[1], item[0].lower())):
            categories = sorted({hit.category for hit in all_hits if hit.token == token})
            category = ",".join(categories)
            file_count = len(files_by_token[token])
            summary_lines.append(f"{category}\t{count}\t{file_count}\t{token}")
    else:
        summary_lines.append("Nenhum token encontrado.")
    summary_lines.append("")
    summary_lines.append("===== CANDIDATOS A REVISAO FUTURA =====")
    if candidate_hits:
        seen: set[tuple[str, str]] = set()
        for hit in sorted(candidate_hits, key=lambda h: (h.category, h.token.lower(), h.rel, h.line)):
            key = (hit.category, hit.token)
            if key in seen:
                continue
            seen.add(key)
            locations = sorted(
                f"{h.rel}:{h.line}"
                for h in candidate_hits
                if h.category == hit.category and h.token == hit.token
            )
            summary_lines.append(f"{hit.category} | {hit.token} | {', '.join(locations)}")
    else:
        summary_lines.append("Nenhum candidato encontrado.")
    summary_lines.append("")
    summary_lines.append("===== DECISAO =====")
    if blocking_hits:
        summary_lines.append("[BLOQUEIO] Ha bloqueios na auditoria detalhada.")
    else:
        summary_lines.append("[OK] Sem bloqueio automatico.")
        summary_lines.append("[OK] Usar este resumo para planejar renomeacoes pequenas e isoladas.")
    summary_lines.append("")

    summary_out = EVID / "67_phase1f_d_resumo_identificadores_derived.txt"
    summary_out.write_text("\n".join(summary_lines), encoding="utf-8")

    print("[OK] Fase 1F-D auditoria de identificadores derived concluida.")
    print(f"Gerado: {detail_out.relative_to(ROOT).as_posix()}")
    print(f"Gerado: {summary_out.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
