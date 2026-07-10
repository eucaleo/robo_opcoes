from __future__ import annotations

import argparse
import json
import sys
import traceback
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))


from rtd_bridge.excel_rtd_option_quotes_bridge import RtdOptionQuotesBridge


LOG_PATH = PROJECT_ROOT / "ATT" / "tests" / "rtd_option_quotes_bridge.log"
OUT_PATH = PROJECT_ROOT / "ATT" / "tests" / "rtd_option_quotes_bridge_result.json"


def write_log(message: str) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    with LOG_PATH.open("a", encoding="utf-8") as file:
        file.write(message)
        file.write("\n")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Teste manual do bridge RTD_OPTION_QUOTES."
    )

    parser.add_argument(
        "--workbook",
        required=True,
        help="Caminho completo para o arquivo LISTA_RTD.xlsm.",
    )

    parser.add_argument(
        "--codes",
        nargs="+",
        required=True,
        help="Lista de códigos de opções para consultar.",
    )

    parser.add_argument(
        "--visible",
        action="store_true",
        help="Abre o Excel visível para depuração.",
    )

    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="Tempo máximo de espera pelo RTD em segundos.",
    )

    args = parser.parse_args()

    started_at = datetime.now().isoformat(timespec="seconds")

    LOG_PATH.write_text("", encoding="utf-8")

    write_log("Início do teste RTD_OPTION_QUOTES")
    write_log("Horário: " + started_at)
    write_log("Projeto: " + str(PROJECT_ROOT))
    write_log("Workbook recebido: " + args.workbook)
    write_log("Códigos recebidos: " + ", ".join(args.codes))

    try:
        workbook_path = str(Path(args.workbook).resolve())

        if not Path(workbook_path).exists():
            raise FileNotFoundError("Workbook não encontrado: " + workbook_path)

        bridge = RtdOptionQuotesBridge(
            workbook_path=workbook_path,
            visible=args.visible,
            rtd_timeout_seconds=args.timeout,
        )

        result = bridge.fetch_quotes(args.codes)

        payload = {
            "ok": True,
            "elapsed_seconds": result.elapsed_seconds,
            "headers_map": result.headers_map,
            "rows": result.rows,
        }

        OUT_PATH.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        print(json.dumps(payload, ensure_ascii=False, indent=2))

        write_log("Teste concluído com sucesso.")
        write_log("Resultado salvo em: " + str(OUT_PATH))

        return 0

    except Exception as exc:
        error_payload = {
            "ok": False,
            "error": str(exc),
            "traceback": traceback.format_exc(),
        }

        OUT_PATH.write_text(
            json.dumps(error_payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        print(json.dumps(error_payload, ensure_ascii=False, indent=2))

        write_log("Erro no teste.")
        write_log(str(exc))
        write_log(traceback.format_exc())
        write_log("Resultado de erro salvo em: " + str(OUT_PATH))

        return 1


if __name__ == "__main__":
    raise SystemExit(main())
