"""
pre66_02_inspect_timestamps_by_aba.py
Para cada 'aba' existente nas tabelas legadas:
- lista timestamps disponíveis
- identifica o mais recente
- conta legs por timestamp
- compara com o que ja existe em structures (alias_legacy_aba)
Nenhuma alteracao. Somente leitura.
"""
import sqlite3
from pathlib import Path

DB_PATH = Path("dados/app.db")


def get_timestamps_by_aba(conn, table):
    cur = conn.cursor()
    try:
        cur.execute(f"""
            SELECT aba, timestamp, COUNT(*) as n_legs
            FROM {table}
            GROUP BY aba, timestamp
            ORDER BY aba, timestamp DESC
        """)
        return cur.fetchall()
    except sqlite3.OperationalError as e:
        print(f"  [AVISO] Erro ao consultar {table}: {e}")
        return []


def get_max_timestamp_by_aba(conn, table):
    cur = conn.cursor()
    try:
        cur.execute(f"""
            SELECT aba, MAX(timestamp) as ts_max, COUNT(*) as n_legs
            FROM {table}
            GROUP BY aba
            ORDER BY aba
        """)
        return cur.fetchall()
    except sqlite3.OperationalError as e:
        print(f"  [AVISO] Erro ao consultar {table}: {e}")
        return []


def get_existing_structures(conn):
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT id, name, alias_legacy_aba, status
            FROM structures
            ORDER BY alias_legacy_aba
        """)
        return cur.fetchall()
    except sqlite3.OperationalError as e:
        print(f"  [AVISO] structures nao acessivel: {e}")
        return []


def main():
    if not DB_PATH.exists():
        print(f"[ERRO] Banco nao encontrado: {DB_PATH}")
        return

    conn = sqlite3.connect(str(DB_PATH))

    print("=" * 60)
    print("RTD_ANALISE_ROBO_LEGS -- timestamps por aba")
    print("=" * 60)
    rows_rtd = get_timestamps_by_aba(conn, "rtd_analise_robo_legs")
    for aba, ts, n in rows_rtd:
        print(f"  aba={aba:30s}  ts={ts}  legs={n}")

    print("\n" + "=" * 60)
    print("MANUAL_ANALISE_ROBO_LEGS -- timestamps por aba")
    print("=" * 60)
    rows_manual = get_timestamps_by_aba(conn, "manual_analise_robo_legs")
    for aba, ts, n in rows_manual:
        print(f"  aba={aba:30s}  ts={ts}  legs={n}")

    print("\n" + "=" * 60)
    print("SNAPSHOT MAIS RECENTE por aba (RTD)")
    print("=" * 60)
    max_rtd = get_max_timestamp_by_aba(conn, "rtd_analise_robo_legs")
    for aba, ts, n in max_rtd:
        print(f"  aba={aba:30s}  ts_max={ts}  legs={n}")

    print("\n" + "=" * 60)
    print("SNAPSHOT MAIS RECENTE por aba (MANUAL)")
    print("=" * 60)
    max_manual = get_max_timestamp_by_aba(conn, "manual_analise_robo_legs")
    for aba, ts, n in max_manual:
        print(f"  aba={aba:30s}  ts_max={ts}  legs={n}")

    print("\n" + "=" * 60)
    print("STRUCTURES JA EXISTENTES (canonico)")
    print("=" * 60)
    structs = get_existing_structures(conn)
    if structs:
        for sid, name, alias, status in structs:
            print(f"  id={sid}  alias={alias:30s}  status={status}  name={name}")
    else:
        print("  Nenhuma estrutura cadastrada ainda.")

    # Cruzamento: quais abas legadas ja tem correspondente canonico
    print("\n" + "=" * 60)
    print("CRUZAMENTO: abas legadas vs structures existentes")
    print("=" * 60)
    abas_rtd = set(r[0] for r in max_rtd)
    abas_manual = set(r[0] for r in max_manual)
    abas_legadas = abas_rtd | abas_manual
    aliases_canonicos = set(r[2] for r in structs if r[2])

    for aba in sorted(abas_legadas):
        ja_existe = "JA EXISTE" if aba in aliases_canonicos else "PENDENTE"
        print(f"  {aba:30s}  ->  {ja_existe}")

    print(f"\nTotal abas legadas : {len(abas_legadas)}")
    print(f"Total ja migradas  : {len(abas_legadas & aliases_canonicos)}")
    print(f"Total pendentes    : {len(abas_legadas - aliases_canonicos)}")

    conn.close()
    print("\n[OK] Analise concluida. Nenhum dado alterado.")


if __name__ == "__main__":
    main()
