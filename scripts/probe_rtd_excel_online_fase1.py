"""Diagnóstico manual da Fase 1 do Excel RTD BTG Online.

Este script executa um probe controlado contra o Excel já aberto.

Garantias:
- não abre Excel automaticamente;
- não grava banco;
- não cria snapshot;
- não inicia subprocesso;
- não altera workbook;
- apenas lê metadados, workbook, aba e cabeçalhos.
"""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import sys
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[1]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from services.rtd_excel_probe_service import (  # noqa: E402
    DEFAULT_REQUIRED_HEADERS,
    DEFAULT_WORKBOOK_NAME,
    DEFAULT_WORKSHEET_NAME,
    ExcelRtdProbeService,
)


DEFAULT_OUTPUT_DIR = (
    ROOT_DIR / "FRENTE_RTD_EXCEL_BTG_ONLINE" / "output"
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Executa diagnóstico manual controlado do Excel RTD Online."
    )
    parser.add_argument(
        "--workbook",
        default=DEFAULT_WORKBOOK_NAME,
        help=f"Nome do workbook esperado. Default: {DEFAULT_WORKBOOK_NAME}",
    )
    parser.add_argument(
        "--worksheet",
        default=DEFAULT_WORKSHEET_NAME,
        help=f"Nome da aba esperada. Default: {DEFAULT_WORKSHEET_NAME}",
    )
    parser.add_argument(
        "--required-header",
        action="append",
        dest="required_headers",
        help=(
            "Cabeçalho obrigatório. Pode ser repetido. "
            "Se omitido, usa ticker/bid/ask com aliases."
        ),
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help=f"Diretório para relatórios. Default: {DEFAULT_OUTPUT_DIR}",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Retorna exit code 1 se o probe não for OK.",
    )

    args = parser.parse_args()

    required_headers = tuple(args.required_headers or DEFAULT_REQUIRED_HEADERS)

    service = ExcelRtdProbeService()
    result = service.probe(
        workbook_name=args.workbook,
        worksheet_name=args.worksheet,
        required_headers=required_headers,
    )

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = output_dir / f"probe_rtd_excel_online_fase1_{timestamp}.json"
    md_path = output_dir / f"probe_rtd_excel_online_fase1_{timestamp}.md"

    payload = result.to_dict()
    payload["generated_at"] = datetime.now().isoformat(timespec="seconds")
    payload["script"] = "scripts/probe_rtd_excel_online_fase1.py"

    json_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    md_path.write_text(
        _render_markdown(payload),
        encoding="utf-8",
    )

    print()
    print("============================================================")
    print("Diagnóstico manual Excel RTD Online - Fase 1")
    print("============================================================")
    print(f"OK: {payload.get('ok')}")
    print(f"Excel aberto: {payload.get('excel_running')}")
    print(f"Workbook encontrado: {payload.get('workbook_found')}")
    print(f"Aba encontrada: {payload.get('worksheet_found')}")
    print(f"Workbook: {payload.get('workbook_name')}")
    print(f"Caminho: {payload.get('workbook_path')}")
    print(f"Aba: {payload.get('worksheet_name')}")
    print(f"Mensagem: {payload.get('message')}")
    print(f"Erro: {payload.get('error')}")
    print(f"Cabeçalhos obrigatórios: {payload.get('required_headers')}")
    print(f"Cabeçalhos ausentes: {payload.get('missing_headers')}")
    print()
    print("Relatórios gerados:")
    print(json_path)
    print(md_path)
    print("============================================================")
    print()

    if args.strict and not result.ok:
        return 1

    return 0


def _render_markdown(payload: dict[str, Any]) -> str:
    headers = payload.get("headers") or {}
    raw_headers = payload.get("raw_headers") or {}

    lines = [
        "# Diagnóstico manual Excel RTD Online - Fase 1",
        "",
        f"- Gerado em: `{payload.get('generated_at')}`",
        f"- Script: `{payload.get('script')}`",
        "",
        "## Resultado",
        "",
        f"- OK: `{payload.get('ok')}`",
        f"- Excel aberto: `{payload.get('excel_running')}`",
        f"- Workbook encontrado: `{payload.get('workbook_found')}`",
        f"- Aba encontrada: `{payload.get('worksheet_found')}`",
        f"- Workbook: `{payload.get('workbook_name')}`",
        f"- Caminho: `{payload.get('workbook_path')}`",
        f"- Aba: `{payload.get('worksheet_name')}`",
        f"- Mensagem: `{payload.get('message')}`",
        f"- Erro: `{payload.get('error')}`",
        "",
        "## Cabeçalhos obrigatórios",
        "",
    ]

    for item in payload.get("required_headers") or []:
        lines.append(f"- `{item}`")

    lines.extend(
        [
            "",
            "## Cabeçalhos ausentes",
            "",
        ]
    )

    missing = payload.get("missing_headers") or []

    if missing:
        for item in missing:
            lines.append(f"- `{item}`")
    else:
        lines.append("- Nenhum.")

    lines.extend(
        [
            "",
            "## Cabeçalhos normalizados encontrados",
            "",
        ]
    )

    if headers:
        for name, col in sorted(headers.items(), key=lambda item: item[1]):
            lines.append(f"- Coluna `{col}`: `{name}`")
    else:
        lines.append("- Nenhum cabeçalho normalizado encontrado.")

    lines.extend(
        [
            "",
            "## Cabeçalhos originais encontrados",
            "",
        ]
    )

    if raw_headers:
        for name, col in sorted(raw_headers.items(), key=lambda item: item[1]):
            lines.append(f"- Coluna `{col}`: `{name}`")
    else:
        lines.append("- Nenhum cabeçalho original encontrado.")

    lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
