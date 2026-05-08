#bridge_ingest_csv.py

import os
import sys
import argparse
import subprocess
import time
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from db.config import APP_DB_PATH
import pandas as pd

from db.sqlite import connect  # <-- CORRIGIDO (db, não Db)

PROJECT_DIR = Path(r"C:\Users\eucal\projeto")
BRIDGE_DIR = PROJECT_DIR / "bridge"
RAW_DB = APP_DB_PATH
DERIVED_PIPELINE = PROJECT_DIR / "Scripts" / "run_derived_pipeline.py"
RUN_DERIVED_AFTER_INGEST = os.getenv("RUN_DERIVED_AFTER_INGEST", "1") == "1"
DERIVED_DEBOUNCE_SEC = float(os.getenv("DERIVED_DEBOUNCE_SEC", "3"))


@dataclass(frozen=True)
class CsvSpec:
    filename: str
    table: str
    mode: str  # "replace" | "append"

SPECS = [
    CsvSpec("analise_raiox.csv", "rtd_analise_raiox", "replace"),
    CsvSpec("consolidacoes.csv", "rtd_consolidacoes", "replace"),
    CsvSpec("analise_robo.csv", "rtd_analise_robo", "replace"),
    CsvSpec("analise_robo_legs.csv", "rtd_analise_robo_legs", "replace"),
    CsvSpec("configuracoes.csv", "rtd_configuracoes", "replace"),

    CsvSpec("rolls_detectados.csv", "rtd_rolls_detectados", "append"),
    CsvSpec("hist_robo.csv", "rtd_hist_robo", "append"),
    CsvSpec("encerramentos_manuais.csv", "rtd_encerramentos_manuais", "append"),
]

def normalize_col(col: str) -> str:
    s = str(col).strip()
    s = s.replace("\n", " ").replace("\r", " ")
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = s.lower()
    s = re.sub(r"[^\w]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    aliases = {
        "c_v": "cv",
        "call_put": "call_put",
        "lucro_prejuizo": "lucro_prejuizo",
        "pl_real": "pl_real",
        "pl_estimado": "pl_estimado",
        "dif": "dif",
        "dif_pct": "dif_pct",
        "observacao": "observacao",
        "obs": "obs",
    }
    return aliases.get(s, s)

def run_derived_pipeline() -> int:
    """
    Roda o pipeline de derivadas em processo separado.
    Não levanta exceção; retorna returncode.
    """
    if not DERIVED_PIPELINE.exists():
        print(f"[DERIVED] pipeline não encontrado: {DERIVED_PIPELINE}")
        return 2

    cmd = [sys.executable, str(DERIVED_PIPELINE)]
    print(f"[DERIVED] executando: {' '.join(cmd)}")

    p = subprocess.run(cmd, cwd=str(PROJECT_DIR), capture_output=True, text=True)

    if p.stdout:
        print(p.stdout.rstrip())
    if p.returncode != 0 and p.stderr:
        print(p.stderr.rstrip())

    print(f"[DERIVED] returncode={p.returncode}")
    return p.returncode


def read_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(
        path,
        sep=";",
        dtype=str,
        keep_default_na=False,
        encoding="utf-8",
    )
    df.columns = [normalize_col(c) for c in df.columns]
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
    df = df.loc[~(df == "").all(axis=1)]
    return df

def ensure_table_text(conn, table: str, cols: list[str]):
    cols_sql = ", ".join([f'"{c}" TEXT' for c in cols]) if cols else '"_empty" TEXT'
    conn.execute(f'CREATE TABLE IF NOT EXISTS "{table}" ({cols_sql})')
    existing = {r[1] for r in conn.execute(f'PRAGMA table_info("{table}")').fetchall()}
    for c in cols:
        if c not in existing:
            conn.execute(f'ALTER TABLE "{table}" ADD COLUMN "{c}" TEXT')

def replace_table(conn, table: str, df: pd.DataFrame):
    ensure_table_text(conn, table, list(df.columns))
    conn.execute(f'DELETE FROM "{table}"')
    if not df.empty:
        df.to_sql(table, conn, if_exists="append", index=False)

def append_table(conn, table: str, df: pd.DataFrame):
    ensure_table_text(conn, table, list(df.columns))
    if not df.empty:
        df.to_sql(table, conn, if_exists="append", index=False)

def ingest_once():
    conn = connect(RAW_DB)  # Path ok no seu helper
    try:
        total = 0
        for spec in SPECS:
            path = BRIDGE_DIR / spec.filename
            if not path.exists():
                continue

            df = read_csv(path)

            if spec.mode == "replace":
                replace_table(conn, spec.table, df)
            else:
                append_table(conn, spec.table, df)

            total += len(df)

        conn.commit()
        return total
    finally:
        conn.close()

def main(argv=None):
    parser = argparse.ArgumentParser(description="Ingest CSVs do bridge/ para data/app.db")
    parser.add_argument(
        "--once",
        action="store_true",
        help="Processa um único evento (uma atualização do last_export.txt) e sai.",
    )
    parser.add_argument(
        "--run-now",
        action="store_true",
        help="Roda ingest imediatamente (sem esperar last_export.txt mudar) e sai.",
    )
    args = parser.parse_args(argv)

    BRIDGE_DIR.mkdir(parents=True, exist_ok=True)
    control = BRIDGE_DIR / "last_export.txt"
    last_mtime = 0.0
    last_derived_run = 0.0

    print(f"[INGEST] Bridge dir: {BRIDGE_DIR}")
    print(f"[INGEST] Raw DB:     {RAW_DB}")

    def maybe_run_derived():
        nonlocal last_derived_run
        if not RUN_DERIVED_AFTER_INGEST:
            return
        now = time.time()
        if (now - last_derived_run) >= DERIVED_DEBOUNCE_SEC:
            last_derived_run = now
            rc = run_derived_pipeline()
            if rc != 0:
                print("[DERIVED] WARNING: pipeline falhou (ingest ok).")
        else:
            print("[DERIVED] debounce: ignorando disparo muito próximo do anterior.")

    # Modo: rodar agora e sair
    if args.run_now:
        rows = ingest_once()
        print(f"[INGEST] import concluído, linhas processadas: {rows}")
        maybe_run_derived()
        return

    print("[INGEST] aguardando last_export.txt ...")

    while True:
        if control.exists():
            mtime = control.stat().st_mtime
            if mtime > last_mtime:
                last_mtime = mtime
                rows = ingest_once()
                print(f"[INGEST] import concluído, linhas processadas: {rows}")
                maybe_run_derived()

                if args.once:
                    print("[INGEST] --once: finalizando.")
                    return

        time.sleep(1.0)


if __name__ == "__main__":
    main()

