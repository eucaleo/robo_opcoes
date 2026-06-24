import json
import os
import shutil
import sqlite3
import sys
from datetime import datetime

db_path = sys.argv[1] if len(sys.argv) >= 2 else "dados/app.db"
symbol = sys.argv[2] if len(sys.argv) >= 3 else "PETRS424"

print("=== Inserir quote de teste ===")
print("DB:", db_path)
print("DB absoluto:", os.path.abspath(db_path))
print("Symbol:", symbol)

if not os.path.exists(db_path):
    print("ERRO: banco nao encontrado")
    raise SystemExit(1)

stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_path = db_path + ".bak_inserir_" + symbol + "_" + stamp

shutil.copy2(db_path, backup_path)

print("Backup criado:", backup_path)

payload = {
    "codigo_opcao": symbol,
    "ativo_base": "PETR4",
    "call_put": "Put",
    "strike": "42,4",
    "vencimento": "2026-07-17",
    "ultimo_preco": "0,50",
    "ultima_quantidade": "0",
    "bid": "0,45",
    "ask": "0,55",
    "volume": "0",
    "iv": "0",
    "delta": "-0,5000",
    "gamma": "0,0000",
    "theta": "0,0000",
    "vega": "0,0000",
    "observacao": "REGISTRO DE TESTE LOCAL PARA VALIDAR AUTOPREENCHIMENTO",
}

con = sqlite3.connect(db_path)
con.row_factory = sqlite3.Row

try:
    tables = con.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"
    ).fetchall()

    table_names = [row["name"] for row in tables]

    if "rtd_option_quotes" not in table_names:
        print("ERRO: tabela rtd_option_quotes nao existe")
        raise SystemExit(1)

    antes = con.execute(
        "SELECT COUNT(*) AS total FROM rtd_option_quotes WHERE codigo_opcao = ?",
        (symbol,),
    ).fetchone()["total"]

    print("Registros existentes antes:", antes)

    con.execute(
        "DELETE FROM rtd_option_quotes WHERE codigo_opcao = ?",
        (symbol,),
    )

    con.execute(
        """
        INSERT INTO rtd_option_quotes (
            codigo_opcao,
            ativo_base,
            call_put,
            strike,
            vencimento,
            ultimo_preco,
            ultima_quantidade,
            bid,
            ask,
            volume,
            iv,
            delta,
            gamma,
            theta,
            vega,
            source,
            raw_json,
            updated_at,
            created_at
        )
        VALUES (
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            CURRENT_TIMESTAMP,
            CURRENT_TIMESTAMP
        )
        """,
        (
            symbol,
            "PETR4",
            "PUT",
            42.4,
            "2026-07-17",
            0.50,
            0.0,
            0.45,
            0.55,
            0.0,
            0.0,
            -0.5,
            0.0,
            0.0,
            0.0,
            "TESTE_LOCAL_AUTOPREENCHIMENTO",
            json.dumps(payload, ensure_ascii=False),
        ),
    )

    con.commit()

    depois = con.execute(
        "SELECT rowid, * FROM rtd_option_quotes WHERE codigo_opcao = ?",
        (symbol,),
    ).fetchall()

    print("")
    print("Registros depois:", len(depois))

    for row in depois:
        print(dict(row))

    print("")
    print("OK: quote de teste inserida.")
    print("Agora abra o sistema e teste o botao de autopreenchimento com:", symbol)

finally:
    con.close()
