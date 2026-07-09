from __future__ import annotations

from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVID = ROOT / "FRENTE_BD_UNICO_APPDB" / "evidencias"
OUT = EVID / "113_phase1f_d7_planejamento_proximas_renomeacoes_derived.txt"


def main() -> None:
    EVID.mkdir(parents=True, exist_ok=True)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines: list[str] = []

    lines.append("===== DATA =====")
    lines.append(now)
    lines.append("")
    lines.append("===== OBJETIVO =====")
    lines.append("Planejar proximas renomeacoes de identificadores Python contendo derived.")
    lines.append("Esta fase e apenas classificatoria; nao altera codigo operacional.")
    lines.append("A base considerada e a reauditoria da Fase 1F-D.6, com 54 ocorrencias.")
    lines.append("")
    lines.append("===== ESTADO ATUAL POS D.6 =====")
    lines.append("TOTAL DE OCORRENCIAS TOKEN NAME COM derived: 54")
    lines.append("Bloqueios automaticos: nenhum")
    lines.append("Alias legado permitido: DERIVED_DB_PATH somente em db/config.py")
    lines.append("")
    lines.append("===== TOKENS RESTANTES AGRUPADOS =====")
    rows = [
        ("ensure_derived_tables", 16, 3, "alto impacto; aparece em db/derived_repo.py, db/schema.py e services/derived_service.py"),
        ("connect_derived", 11, 3, "sensivel; funcao em db/config.py usada por scripts e servicos"),
        ("cleanup_derived", 5, 2, "sensivel; funcao de servico e metodo wrapper em DerivedService"),
        ("derived_db_path", 4, 2, "compatibilidade explicita em UIDataModel e teste"),
        ("derived_repo", 4, 4, "nome de modulo/arquivo; nao renomear sem fase propria"),
        ("derived_service", 3, 3, "nome de modulo/arquivo; nao renomear sem fase propria"),
        ("DerivedPayoffPersistence", 3, 2, "classe PascalCase potencialmente publica"),
        ("derived_db", 2, 1, "parametro de construtor; requer alias/compatibilidade"),
        ("get_derived_connection", 2, 1, "uso em db/writer.py; depende de contrato exportado por db.derived_repo"),
        ("DERIVED_DB_PATH", 1, 1, "alias legado autorizado em db/config.py"),
        ("derived_payoff_persistence", 1, 1, "nome de modulo/arquivo importado"),
        ("DerivedRepo", 1, 1, "classe publica/potencialmente publica"),
        ("DerivedService", 1, 1, "classe publica/potencialmente publica"),
    ]

    for token, occ, files, note in rows:
        lines.append(f"{token}: {occ} ocorrencia(s), {files} arquivo(s) - {note}")

    lines.append("")
    lines.append("===== CLASSIFICACAO DE RISCO =====")
    lines.append("[MANTER_AGORA] DERIVED_DB_PATH")
    lines.append("Motivo: alias legado de configuracao ja permitido explicitamente.")
    lines.append("")
    lines.append("[MANTER_AGORA] derived_db_path")
    lines.append("Motivo: parametro de compatibilidade em UIDataModel e coberto por teste.")
    lines.append("")
    lines.append("[MANTER_AGORA] derived_repo, derived_service, derived_payoff_persistence")
    lines.append("Motivo: nomes de modulo/arquivo; renomear exigiria fase propria de imports, arquivos e compatibilidade.")
    lines.append("")
    lines.append("[MANTER_AGORA] DerivedRepo, DerivedService, DerivedPayoffPersistence")
    lines.append("Motivo: classes PascalCase possivelmente publicas; requer decisao arquitetural e/ou aliases.")
    lines.append("")
    lines.append("[CANDIDATO_COM_ALIAS] connect_derived")
    lines.append("Motivo: pode virar connect_app_db ou connect_app, mantendo connect_derived como alias legado temporario.")
    lines.append("")
    lines.append("[CANDIDATO_COM_ALIAS] ensure_derived_tables")
    lines.append("Motivo: pode virar ensure_app_tables ou ensure_app_db_tables, mantendo alias legado temporario.")
    lines.append("")
    lines.append("[CANDIDATO_COM_ALIAS] cleanup_derived")
    lines.append("Motivo: pode virar cleanup_app_db ou cleanup_app_snapshots, mantendo alias legado temporario.")
    lines.append("")
    lines.append("[CANDIDATO_COM_ALIAS] derived_db")
    lines.append("Motivo: parametro de construtor; renomeacao segura exige aceitar parametro legado via compatibilidade.")
    lines.append("")
    lines.append("[CANDIDATO_COM_ALIAS] get_derived_connection")
    lines.append("Motivo: pode ser migrado em consumidor db/writer.py, mas contrato exportado deve ser verificado antes.")
    lines.append("")
    lines.append("===== RECOMENDACAO PARA D.8 =====")
    lines.append("Nao mexer ainda em nomes de modulos/arquivos nem classes publicas.")
    lines.append("Proxima fase mais segura: auditar contrato de get_derived_connection e decidir se ha funcao/alias equivalente app_db.")
    lines.append("Alternativa segura: iniciar connect_derived com alias legado, se for aceitavel manter o token legado em db/config.py.")
    lines.append("")
    lines.append("===== DECISAO =====")
    lines.append("[OK] Planejamento concluido sem alteracao operacional.")
    lines.append("[OK] Proxima fase deve ser pequena e com estrategia explicita de compatibilidade.")
    lines.append("")

    OUT.write_text("\n".join(lines), encoding="utf-8")

    print("[OK] Fase 1F-D.7 planejamento concluido.")
    print(f"Gerado: {OUT.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
