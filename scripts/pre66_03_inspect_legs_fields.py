"""
pre66_03_inspect_legs_fields.py
Verifica qualidade dos dados das legs legadas:
- campos nulos ou invalidos
- valores distintos de cv, call_put, position_side
- strikes nulos
- datas de vencimento presentes
Nenhuma alteracao. Somente leitura.
"""
import sqlite3
from pathlib import Path

DB_PATH = Path("dados/app.db")


def audit_legs_table(conn, table):
    cur = conn.cursor()
    print(f"\n{'='*60}")
    print(f"AUDITORIA DE CAMPOS: {table}")
    print(f"{'='*60}")

    # Verifica se existe
    cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,)
    )
    if not cur.fetchone():
        print(f"  [AVISO] Tabela nao existe: {table}")
        return

    # Colunas disponiveis
    cur.execute(f"PRAGMA table_info({table})")
    cols = [c[1] for c in cur.fetchall()]
    print(f"Colunas: {cols}")

    # cv
    if "cv" in cols:
        cur.execute(f"SELECT cv, COUNT(*) FROM {table} GROUP BY cv ORDER BY cv")
        print("\nValores de 'cv':")
        for val, cnt in cur.fetchall():
            print(f"  '{val}' -> {cnt} registros")

    # call_put
    if "call_put" in cols:
        cur.execute(
            f"SELECT call_put, COUNT(*) FROM {table} GROUP BY call_put ORDER BY call_put"
        )
        print("\nValores de 'call_put':")
        for val, cnt in cur.fetchall():
            print(f"  '{val}' -> {cnt} registros")

    # strike nulo
    if "strike" in cols:
        cur.execute(f"SELECT COUNT(*) FROM {table} WHERE strike IS NULL OR strike = ''")
        nulls = cur.fetchone()[0]
        print(f"\nStrikes nulos/vazios: {nulls}")

        cur.execute(f"SELECT MIN(strike), MAX(strike), AVG(strike) FROM {table}")
        mn, mx, avg = cur.fetchone()
        print(f"Strike min={mn}  max={mx}  avg={avg:.2f}" if avg else "Strike: sem dados")

    # vencimento
    for col in ["vencimento", "expiration_date"]:
        if col in cols:
            cur.execute(f"SELECT COUNT(*) FROM {table} WHERE {col} IS NULL OR {col} = ''")
            nulls = cur.fetchone()[0]
            cur.execute(f"SELECT DISTINCT {col} FROM {table} ORDER BY {col} LIMIT 10")
            samples = [r[0] for r in cur.fetchall()]
            print(f"\nCampo '{col}': nulos={nulls}  amostras={samples}")

    # quant / quantity
    for col in ["quant", "quantity"]:
        if col in cols:
            cur.execute(f"SELECT COUNT(*) FROM {table} WHERE {col} IS NULL OR {col} <= 0")
            invalids = cur.fetchone()[0]
            cur.execute(f"SELECT MIN({col}), MAX({col}) FROM {table}")
            mn, mx = cur.fetchone()
            print(f"\nCampo '{col}': invalidos={invalids}  min={mn}  max={mx}")

    # ativo
    if "ativo" in cols:
        cur.execute(
            f"SELECT ativo, COUNT(*) FROM {table} GROUP BY ativo ORDER BY ativo"
        )
        print("\nValores de 'ativo':")
        for val, cnt in cur.fetchall():
            print(f"  '{val}' -> {cnt} registros")


def main():
    if not DB_PATH.exists():
        print(f"[ERRO] Banco nao encontrado: {DB_PATH}")
        return

    conn = sqlite3.connect(str(DB_PATH))

    audit_legs_table(conn, "rtd_analise_robo_legs")
    audit_legs_table(conn, "manual_analise_robo_legs")

    conn.close()
    print("\n[OK] Auditoria concluida. Nenhum dado alterado.")


if __name__ == "__main__":
    main()
