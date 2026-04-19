# db/import_excel.py
import pandas as pd
import re
from db.sqlite import connect

XLSX_PATH = "OPERACOES_E_OPCOES.xlsx"  # ajuste se estiver em outra pasta

SHEET_MAP = {
    "CONFIGURACOES": "robo_config",
    "ANALISE_ROBO": "robo_snapshot",
    "ANALISE_ROBO_LEGS": "robo_legs_snapshot",
    "HIST_ROBO": "robo_legs_history",
    "ENCERRAMENTOS_MANUAIS": "encerramentos_manuais",
}

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # strip básico
    df.columns = [str(c).strip() for c in df.columns]

    # mapeamento explícito (prioritário)
    explicit = {
        "Parâmetro": "parametro",
        "Valor": "valor",
        "Descrição": "descricao",

        "TIMESTAMP": "timestamp",
        "ABA": "aba",
        "ATIVO": "ativo",
        "C/V": "cv",
        "CALL_/_PUT": "call_put",
        "QUANT": "quant",
        "VALOR_EXECUTADO": "valor_executado",
        "BID": "bid",
        "ASK": "ask",
        "SPREAD": "spread",
        "SPREAD_PCT": "spread_pct",
        "IV": "iv",
        "DELTA": "delta",
        "GAMMA": "gamma",
        "THETA": "theta",
        "VEGA": "vega",
        "STRIKE": "strike",
        "VENCIMENTO": "vencimento",
        "DTE": "dte",
        "PL_REALISTA": "pl_realista",

        "Data": "data",
        "Código": "codigo",
        "Tipo": "tipo",
        "Qtd": "qtd",
        "Preço Real": "preco_real",
        "Motivo": "motivo",
        "Observação": "observacao",
    }
    df = df.rename(columns={k: v for k, v in explicit.items() if k in df.columns})

    # fallback: se sobrar coluna com espaço/char estranho, padroniza
    def slug(s: str) -> str:
        s = s.strip()
        s = s.replace("%", "pct")
        s = re.sub(r"[^\w]+", "_", s, flags=re.UNICODE)
        s = re.sub(r"_+", "_", s).strip("_")
        return s.lower()

    df.columns = [slug(c) for c in df.columns]
    return df

def write_df(conn, df: pd.DataFrame, table: str):
    # drop colunas lixo do Excel
    df = df.loc[:, ~df.columns.astype(str).str.match(r"^unnamed")]

    # descobrir colunas existentes na tabela
    table_cols = [r[1] for r in conn.execute(f"PRAGMA table_info({table})").fetchall()]

    # mantém só colunas que existem no SQLite
    df = df[[c for c in df.columns if c in table_cols]]

    # NaN -> None
    df = df.where(pd.notnull(df), None)

    df.to_sql(table, conn, if_exists="append", index=False)

def main():
    conn = connect()

    for sheet, table in SHEET_MAP.items():
        print(f"Importando {sheet} -> {table}...")
        
        df = pd.read_excel(XLSX_PATH, sheet_name=sheet)

        # em algumas abas pode ter linhas totalmente vazias
        df = df.dropna(how="all")

        df = normalize_columns(df)

        # padronizar timestamp/data como string (evita pandas gravar como datetime python)
        for col in ["timestamp", "data"]:
            if col in df.columns:
                df[col] = df[col].astype(str)

        write_df(conn, df, table)
        print(f"OK: importado {len(df)} linhas de {sheet} -> {table}")

    conn.commit()
    conn.close()
    print("OK: import finalizado")

if __name__ == "__main__":
    main()

