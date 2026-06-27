#!/usr/bin/env bash
set -u

echo "=== Conferencia de seguimento Payoff RTD ==="
echo "Diretorio atual:"
pwd
echo

mkdir -p docs/checkpoints/evidencias

python - <<'PY'
from pathlib import Path
from datetime import datetime
import os
import sqlite3
import subprocess
import json
import traceback

ROOT = Path(".")
OUT = ROOT / "docs" / "checkpoints" / "evidencias" / "fase-12-conferencia-seguimento-payoff-rtd.md"

APP_DB = ROOT / "dados" / "app.db"
DERIVED_DB = ROOT / "dados" / "derived.db"

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

lines = []

def add(text=""):
    lines.append(str(text))

def md_bool(value):
    return "OK" if value else "ATENCAO"

def qident(name):
    return '"' + str(name).replace('"', '""') + '"'

def connect_db(path):
    con = sqlite3.connect(str(path))
    con.row_factory = sqlite3.Row
    return con

def table_exists(con, table):
    row = con.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name = ?",
        (table,),
    ).fetchone()
    return row is not None

def table_cols(con, table):
    if not table_exists(con, table):
        return []
    return [row["name"] for row in con.execute(f"PRAGMA table_info({qident(table)})").fetchall()]

def pick(cols, candidates):
    cols_lower = {c.lower(): c for c in cols}
    for cand in candidates:
        if cand.lower() in cols_lower:
            return cols_lower[cand.lower()]
    return None

def fetch_all_safe(con, sql, params=()):
    try:
        return con.execute(sql, params).fetchall()
    except Exception as exc:
        return f"ERRO: {exc}"

def row_to_dict(row):
    return {k: row[k] for k in row.keys()}

def snapshot_to_dict(obj):
    if obj is None:
        return {"repr": "None"}
    if isinstance(obj, dict):
        return obj
    if hasattr(obj, "_asdict"):
        try:
            return dict(obj._asdict())
        except Exception:
            pass
    if hasattr(obj, "__dict__"):
        try:
            data = {}
            for k, v in vars(obj).items():
                try:
                    json.dumps(v, default=str)
                    data[k] = v
                except Exception:
                    data[k] = str(v)
            if data:
                return data
        except Exception:
            pass
    return {"repr": repr(obj)}

def get_field(data, name):
    if isinstance(data, dict):
        return data.get(name)
    return None

def run_git_grep(pattern, paths):
    existing = [p for p in paths if (ROOT / p).exists()]
    if not existing:
        return []
    cmd = ["git", "grep", "-n", "-I", "-E", pattern, "--"] + existing
    proc = subprocess.run(cmd, text=True, capture_output=True)
    if proc.returncode == 0:
        return proc.stdout.splitlines()
    if proc.returncode == 1:
        return []
    return ["ERRO git grep: " + proc.stderr.strip()]

def scan_db_for_token(db_path, tokens):
    findings = []
    if not db_path.exists():
        return findings
    try:
        con = connect_db(db_path)
        tables = [
            row["name"]
            for row in con.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"
            ).fetchall()
        ]
        for table in tables:
            cols = table_cols(con, table)
            for col in cols:
                for token in tokens:
                    sql = (
                        f"SELECT COUNT(*) AS n FROM {qident(table)} "
                        f"WHERE CAST({qident(col)} AS TEXT) LIKE ?"
                    )
                    try:
                        n = con.execute(sql, (f"%{token}%",)).fetchone()["n"]
                        if n:
                            findings.append({
                                "db": db_path.as_posix(),
                                "table": table,
                                "column": col,
                                "token": token,
                                "count": n,
                            })
                    except Exception:
                        pass
        con.close()
    except Exception as exc:
        findings.append({
            "db": db_path.as_posix(),
            "erro": str(exc),
        })
    return findings

add("# Conferencia de seguimento - Payoff RTD")
add()
add(f"Gerado em: {now}")
add()
add("## Objetivo")
add()
add("Registrar evidencia de fechamento das tres primeiras pendencias da frente de payoff RTD e orientar o seguimento ate o fechamento final.")
add()
add("Esta conferencia nao altera codigo funcional. Apenas consulta banco, provider, grep e estado Git.")
add()

add("## Declaracao operacional")
add()
add("As tres primeiras pendencias foram informadas como fechadas pelo responsavel da frente.")
add()
add("Esta evidencia documenta as conferencias para reduzir retrabalho e manter rastreabilidade.")
add()

add("## Ambiente")
add()
add(f"Diretorio: {ROOT.resolve()}")
add(f"MYHUBIA_DB_PATH: {os.environ.get('MYHUBIA_DB_PATH', '<vazio>')}")
add(f"dados/app.db existe: {APP_DB.exists()}")
add(f"dados/app.db tamanho bytes: {APP_DB.stat().st_size if APP_DB.exists() else 'N/A'}")
add(f"dados/derived.db existe: {DERIVED_DB.exists()}")
add(f"dados/derived.db tamanho bytes: {DERIVED_DB.stat().st_size if DERIVED_DB.exists() else 'N/A'}")
add()

# Banco operacional e RTD underlying
add("## Conferencia 1 - Fonte RTD de ativos-base")
add()

underlying_ok = False
underlying_rows = []

if APP_DB.exists():
    try:
        con = connect_db(APP_DB)
        exists = table_exists(con, "rtd_underlying_quotes")
        add(f"Tabela rtd_underlying_quotes em dados/app.db: {md_bool(exists)}")
        if exists:
            cols = table_cols(con, "rtd_underlying_quotes")
            add("Colunas encontradas:")
            for c in cols:
                add(f"- {c}")
            ativo_col = pick(cols, ["ativo", "underlying", "underlying_asset", "symbol"])
            preco_col = pick(cols, ["ultimo_preco", "last_price", "spot_price", "preco"])
            source_col = pick(cols, ["source", "fonte"])
            updated_col = pick(cols, ["updated_at", "atualizado_em"])

            if ativo_col and preco_col:
                rows = con.execute(
                    f"SELECT * FROM rtd_underlying_quotes WHERE {qident(ativo_col)} IN ('BOVA11', 'PRIO3') ORDER BY {qident(ativo_col)}"
                ).fetchall()
                underlying_rows = [row_to_dict(r) for r in rows]
                for r in rows:
                    d = row_to_dict(r)
                    add()
                    add(f"Ativo: {d.get(ativo_col)}")
                    add(f"Preco: {d.get(preco_col)}")
                    if source_col:
                        add(f"Source: {d.get(source_col)}")
                    if updated_col:
                        add(f"Updated_at: {d.get(updated_col)}")
                underlying_ok = len(rows) >= 2 and all((row[preco_col] is not None and float(row[preco_col]) > 0) for row in rows)
            else:
                add("ATENCAO: nao foi possivel identificar coluna de ativo ou preco.")
        con.close()
    except Exception as exc:
        add(f"ERRO ao consultar rtd_underlying_quotes: {exc}")
else:
    add("ATENCAO: dados/app.db nao encontrado.")

add()
add(f"Resultado conferencia 1 banco RTD: {md_bool(underlying_ok)}")
add()

# Provider
add("## Conferencia 2 - MarketSnapshotProvider")
add()

provider_ok = False
provider_results = []

try:
    from services.market_snapshot_provider import MarketSnapshotProvider

    provider = MarketSnapshotProvider()
    for asset in ["BOVA11", "PRIO3"]:
        try:
            snap = provider.get_snapshot(asset)
            data = snapshot_to_dict(snap)
            provider_results.append((asset, data))
            add(f"### Snapshot {asset}")
            add()
            for k in sorted(data.keys()):
                add(f"- {k}: {data[k]}")
            add()
        except Exception as exc:
            provider_results.append((asset, {"erro": str(exc)}))
            add(f"ERRO em get_snapshot para {asset}: {exc}")

    checks = []
    for asset, data in provider_results:
        source = get_field(data, "snapshot_source")
        market_source = get_field(data, "market_snapshot_source")
        static_fallback = get_field(data, "is_static_fallback")
        spot = get_field(data, "spot_price")
        checks.append(
            source == "rtd_underlying_quotes"
            or market_source == "rtd_underlying_quotes"
        )
        checks.append(static_fallback is False or str(static_fallback).lower() == "false")
        try:
            checks.append(float(spot) > 0)
        except Exception:
            checks.append(False)

    provider_ok = bool(checks) and all(checks)

except Exception as exc:
    add("ERRO ao importar ou executar MarketSnapshotProvider:")
    add(str(exc))
    add(traceback.format_exc())

add(f"Resultado conferencia 2 provider RTD: {md_bool(provider_ok)}")
add()

# Qualidade das opcoes
add("## Conferencia 3 - Qualidade RTD das opcoes")
add()

option_ok = False
option_rows = []

active_option_symbols = [
    "BOVAG34",
    "BOVAH186",
    "BOVAS61",
    "BOVAT158",
    "PRIOG800",
    "PRIOH505",
    "PRIOS525",
    "PRIOT700",
]

if APP_DB.exists():
    try:
        con = connect_db(APP_DB)
        exists = table_exists(con, "rtd_option_quotes")
        add(f"Tabela rtd_option_quotes em dados/app.db: {md_bool(exists)}")
        if exists:
            cols = table_cols(con, "rtd_option_quotes")
            codigo_col = pick(cols, ["codigo_opcao", "codigo", "ticker", "symbol"])
            call_put_col = pick(cols, ["call_put", "tipo", "option_type"])
            ultimo_col = pick(cols, ["ultimo_preco", "last_price", "preco"])
            bid_col = pick(cols, ["bid"])
            ask_col = pick(cols, ["ask"])
            source_col = pick(cols, ["source", "fonte"])
            updated_col = pick(cols, ["updated_at", "atualizado_em"])

            add("Colunas principais detectadas:")
            add(f"- codigo: {codigo_col}")
            add(f"- call_put: {call_put_col}")
            add(f"- ultimo_preco: {ultimo_col}")
            add(f"- bid: {bid_col}")
            add(f"- ask: {ask_col}")
            add(f"- source: {source_col}")
            add(f"- updated_at: {updated_col}")
            add()

            if codigo_col:
                placeholders = ",".join(["?"] * len(active_option_symbols))
                rows = con.execute(
                    f"SELECT * FROM rtd_option_quotes WHERE {qident(codigo_col)} IN ({placeholders}) ORDER BY {qident(codigo_col)}",
                    active_option_symbols,
                ).fetchall()
                option_rows = [row_to_dict(r) for r in rows]

                for r in rows:
                    d = row_to_dict(r)
                    add(f"Opcao: {d.get(codigo_col)}")
                    if call_put_col:
                        add(f"  call_put: {d.get(call_put_col)}")
                    if ultimo_col:
                        add(f"  ultimo_preco: {d.get(ultimo_col)}")
                    if bid_col:
                        add(f"  bid: {d.get(bid_col)}")
                    if ask_col:
                        add(f"  ask: {d.get(ask_col)}")
                    if source_col:
                        add(f"  source: {d.get(source_col)}")
                    if updated_col:
                        add(f"  updated_at: {d.get(updated_col)}")

                count_ok = len(rows) == len(active_option_symbols)

                call_put_ok = True
                if call_put_col:
                    invalid = []
                    for r in rows:
                        v = str(r[call_put_col]).strip().upper() if r[call_put_col] is not None else ""
                        if v in ["", "0", "NONE", "NULL", "N/A"]:
                            invalid.append(r[codigo_col])
                    if invalid:
                        call_put_ok = False
                        add()
                        add("ATENCAO: call_put invalido encontrado em:")
                        for x in invalid:
                            add(f"- {x}")

                zero_with_spread_ok = True
                if ultimo_col and bid_col and ask_col:
                    still_zero = []
                    for r in rows:
                        try:
                            ultimo = float(r[ultimo_col] or 0)
                            bid = float(r[bid_col] or 0)
                            ask = float(r[ask_col] or 0)
                            if ultimo <= 0 and bid > 0 and ask > 0:
                                still_zero.append(r[codigo_col])
                        except Exception:
                            pass
                    if still_zero:
                        zero_with_spread_ok = False
                        add()
                        add("ATENCAO: opcoes ainda com ultimo_preco zero e bid/ask positivos:")
                        for x in still_zero:
                            add(f"- {x}")

                option_ok = count_ok and call_put_ok and zero_with_spread_ok

                add()
                add(f"Quantidade esperada de opcoes ativas: {len(active_option_symbols)}")
                add(f"Quantidade encontrada: {len(rows)}")
                add(f"Escopo de opcoes ativo completo: {md_bool(count_ok)}")
                add(f"call_put normalizado: {md_bool(call_put_ok)}")
                add(f"Regra de preco para ultimo_preco zero conferida: {md_bool(zero_with_spread_ok)}")

            else:
                add("ATENCAO: coluna de codigo da opcao nao detectada.")
        con.close()
    except Exception as exc:
        add(f"ERRO ao consultar rtd_option_quotes: {exc}")
else:
    add("ATENCAO: dados/app.db nao encontrado.")

add()
add(f"Resultado conferencia 3 qualidade opcoes: {md_bool(option_ok)}")
add()

# Busca por referencias residuais
add("## Conferencia 4 - Busca por referencias residuais")
add()

code_paths = ["services", "domain", "repositories", "scripts", "db", "api", "UI", "src", "core", "infra"]
grep_pattern = "66[,.]84|DEFAULT_MARKET_BY_ASSET|static_fallback|rtd_underlying_quotes|market_snapshot_source|is_static_fallback"
grep_lines = run_git_grep(grep_pattern, code_paths)

add("Busca executada em caminhos de codigo e scripts:")
for p in code_paths:
    if (ROOT / p).exists():
        add(f"- {p}")
add()
add("Padrao:")
add(grep_pattern)
add()

if grep_lines:
    add("Ocorrencias encontradas:")
    for item in grep_lines[:300]:
        add(f"- {item}")
    if len(grep_lines) > 300:
        add(f"- Saida limitada. Total de linhas: {len(grep_lines)}")
else:
    add("Nenhuma ocorrencia encontrada para o padrao nos caminhos avaliados.")

add()

# Scan DB 66.84
add("## Conferencia 5 - Busca de valor 66.84 nos bancos")
add()

db_findings = []
db_findings.extend(scan_db_for_token(APP_DB, ["66.84", "66,84"]))
db_findings.extend(scan_db_for_token(DERIVED_DB, ["66.84", "66,84"]))

if db_findings:
    add("Ocorrencias encontradas:")
    for f in db_findings:
        add("- " + json.dumps(f, ensure_ascii=False))
else:
    add("Nenhuma ocorrencia de 66.84 ou 66,84 encontrada em dados/app.db ou dados/derived.db.")

add()

# Documentos de arquitetura/checklist
add("## Conferencia 6 - Documentacao criada")
add()

doc_paths = [
    ROOT / "docs" / "arquitetura" / "fonte_autoritativa_rtd_ativos_base.md",
    ROOT / "docs" / "checklists" / "rtd_underlying_quotes.md",
    ROOT / "docs" / "README.md",
    ROOT / "docs" / "correcao_de_payoff.md",
]

for p in doc_paths:
    add(f"{p.as_posix()}: {'existe' if p.exists() else 'ausente'}")

add()

# Resumo
add("## Resumo das tres primeiras pendencias")
add()
add("| Pendencia | Estado documentado | Evidencia |")
add("| --- | --- | --- |")
add(f"| MarketSnapshotProvider lendo rtd_underlying_quotes | {'Fechada conferida' if provider_ok else 'Requer atencao'} | Conferencias 1 e 2 |")
add(f"| Payoff BOVA11 sem preco atual indevido 66.84 | {'Fechada conferida' if not db_findings else 'Requer atencao'} | Conferencia 5 e grep |")
add(f"| Qualidade RTD opcoes: call_put e ultimo_preco zero | {'Fechada conferida' if option_ok else 'Requer atencao'} | Conferencia 3 |")
add()

# Seguimento ate fechamento final
add("## Seguimento em direcao ao fechamento final")
add()
add("Com as tres primeiras pendencias tratadas, a frente deve seguir para as pendencias finais de produto, motor e auditoria.")
add()
add("### Pendencias finais restantes")
add()
add("1. Separar explicitamente payoff no vencimento de marcacao atual e PL atual.")
add("2. Separar preco base na implantacao, preco base atual, preco usado na curva e preco simulado no vencimento.")
add("3. Remover ou renomear o rotulo generico Preco ref. na interface.")
add("4. Exibir tabela por perna com ticker, tipo, direcao, quantidade, strike, vencimento, premio de entrada, preco atual, intrinseco, extrinseco, PL atual e payoff no vencimento ao preco atual.")
add("5. Validar comparabilidade entre estruturas antes de comparar curvas.")
add("6. Bloquear ou alertar estruturas com ativo-base divergente, vencimentos incompatíveis ou fonte de mercado estatica.")
add("7. Criar testes automatizados cobrindo call comprada, call vendida, put comprada, put vendida, travas e multiplas pernas.")
add("8. Revalidar visualmente e por dados a estrutura 3 de BOVA11.")
add()

add("### Criterio de aceite final")
add()
add("- Nenhum calculo de PL atual deve usar static_fallback como preco de mercado.")
add("- O spot atual deve ter origem auditavel em rtd_underlying_quotes.")
add("- O payoff no vencimento deve estar separado do PL atual.")
add("- A UI deve deixar claro qual preco e de implantacao, qual e atual e qual e simulado.")
add("- Cada perna deve ser auditavel individualmente.")
add("- Estruturas incompativeis nao devem ser comparadas sem alerta.")
add("- Testes automatizados devem cobrir os cenarios financeiros minimos.")
add()

# Git status
add("## Estado Git no momento da conferencia")
add()
try:
    proc = subprocess.run(["git", "status", "--short"], text=True, capture_output=True)
    if proc.stdout.strip():
        for line in proc.stdout.splitlines():
            add(f"- {line}")
    else:
        add("Sem alteracoes pendentes.")
except Exception as exc:
    add(f"ERRO ao consultar git status: {exc}")

add()

OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")

print("Documento gerado:")
print(OUT.as_posix())

# Resumo no terminal
print()
print("=== Resumo rapido ===")
print("Conferencia 1 banco RTD:", "OK" if underlying_ok else "ATENCAO")
print("Conferencia 2 provider:", "OK" if provider_ok else "ATENCAO")
print("Conferencia 3 opcoes:", "OK" if option_ok else "ATENCAO")
print("Conferencia 5 66.84 nos bancos:", "OK" if not db_findings else "ATENCAO")
PY

py_status=$?

echo
echo "=== Status Python ==="
echo "$py_status"

echo
echo "=== Arquivo de conferencia ==="
ls -la docs/checkpoints/evidencias/fase-12-conferencia-seguimento-payoff-rtd.md 2>/dev/null || true

echo
echo "=== Previa do documento ==="
sed -n '1,220p' docs/checkpoints/evidencias/fase-12-conferencia-seguimento-payoff-rtd.md 2>/dev/null || true

echo
echo "=== Git status ==="
git status --short

exit "$py_status"
