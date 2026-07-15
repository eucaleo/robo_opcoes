from __future__ import annotations

import argparse
import os
import shlex
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


def log(msg: str) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[auto-refresh {now}] {msg}", flush=True)


def run_cmd(cmd: list[str], cwd: Path | None = None) -> int:
    log("executando: " + " ".join(shlex.quote(part) for part in cmd))
    proc = subprocess.run(cmd, cwd=str(cwd) if cwd else None)
    return proc.returncode


def build_payoff_command(template: str, db: str) -> list[str]:
    rendered = template.format(db=Path(db).as_posix())  # PAYOFF_DB_POSIX_FIX
    return shlex.split(rendered)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Loop automático: Excel RTD -> SQLite -> cálculo externo de payoff."
    )
    parser.add_argument("--db", default="dados/app.db")
    parser.add_argument("--interval", type=float, default=10.0)
    parser.add_argument("--wait", type=float, default=None)
    parser.add_argument("--iterations", type=int, default=0)
    parser.add_argument(
        "--rtd-script",
        default="scripts/run_excel_rtd_option_quotes_snapshot_loop.py",
    )
    parser.add_argument(
        "--payoff-command",
        default=os.getenv("PAYOFF_REFRESH_COMMAND", "").strip(),
        help=(
            "Comando externo que recalcula payoff e grava payoff_curve_points. "
            "Pode usar {db}. Exemplo: "
            "'python scripts/seu_calculo_payoff.py --db {db}'"
        ),
    )
    parser.add_argument("--continue-on-payoff-error", action="store_true")
    args = parser.parse_args()

    db_path = Path(args.db)
    rtd_script = Path(args.rtd_script)

    if not rtd_script.exists():
        log(f"ERRO: script RTD não encontrado: {rtd_script}")
        return 1

    if not args.payoff_command:
        log("ERRO: nenhum comando de payoff informado.")
        log("Defina assim no Git Bash:")
        log("  export PAYOFF_REFRESH_COMMAND='python scripts/SEU_SCRIPT_PAYOFF.py --db {db}'")
        log("Ou passe:")
        log("  --payoff-command 'python scripts/SEU_SCRIPT_PAYOFF.py --db {db}'")
        return 1

    wait = args.wait if args.wait is not None else args.interval
    iteration = 0

    log("loop iniciado")
    log(f"db={db_path}")
    log(f"interval={args.interval}s")
    log(f"wait={wait}s")
    log(f"iterations={args.iterations or 'infinito'}")
    log(f"payoff_command={args.payoff_command}")

    try:
        while True:
            iteration += 1
            log(f"ciclo {iteration} iniciado")

            rtd_cmd = [
                sys.executable,
                str(rtd_script),
                "--db",
                str(db_path),
                "--interval",
                str(args.interval),
                "--iterations",
                "1",
            ]

            rtd_rc = run_cmd(rtd_cmd)
            if rtd_rc != 0:
                log(f"ERRO: snapshot RTD falhou com exit code {rtd_rc}")
                return rtd_rc

            payoff_cmd = build_payoff_command(args.payoff_command, str(db_path))
            payoff_rc = run_cmd(payoff_cmd)

            if payoff_rc != 0:
                log(f"ERRO: cálculo de payoff falhou com exit code {payoff_rc}")
                if not args.continue_on_payoff_error:
                    return payoff_rc

            log(f"ciclo {iteration} concluído")

            if args.iterations > 0 and iteration >= args.iterations:
                log("limite de iterações atingido")
                return 0

            time.sleep(max(0.0, wait))

    except KeyboardInterrupt:
        log("interrompido pelo usuário")
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
