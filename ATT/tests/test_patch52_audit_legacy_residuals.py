# tests/test_patch52_audit_legacy_residuals.py
"""
Testes do patch_52 — cobertura de classificacao, varredura e geracao de relatorio.
Nenhum arquivo de producao e modificado; todos os fixtures sao temporarios.
"""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

import pytest

from scripts.audit_legacy_residuals_patch52 import (
    BRIDGE_FILES,
    Ocorrencia,
    Relatorio,
    RelatorioArquivo,
    _classificar,
    _linha_tem_alias_ok,
    _varrer_arquivo,
    construir_relatorio,
    gerar_json,
    gerar_markdown,
    varrer_projeto,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def raiz_tmp(tmp_path: Path) -> Path:
    """Cria estrutura minima de diretorios para testes de varredura."""
    for d in ("services", "repositories", "domain", "db", "api", "UI"):
        (tmp_path / d).mkdir()
    return tmp_path


def _escrever(raiz: Path, rel: str, codigo: str) -> Path:
    caminho = raiz / rel
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(textwrap.dedent(codigo), encoding="utf-8")
    return caminho


# ---------------------------------------------------------------------------
# _linha_tem_alias_ok
# ---------------------------------------------------------------------------

class TestLinhaTemAliasOk:

    def test_alias_legacy_aba_e_ok(self):
        assert _linha_tem_alias_ok("x = alias_legacy_aba") is True

    def test_get_abas_readonly_e_ok(self):
        assert _linha_tem_alias_ok("resultado = get_abas()") is True

    def test_alias_readonly_terms_e_ok(self):
        assert _linha_tem_alias_ok("for t in ALIAS_READONLY_TERMS:") is True

    def test_comentario_bridge_legado_e_ok(self):
        assert _linha_tem_alias_ok("x = foo  # BRIDGE LEGADO") is True

    def test_linha_sem_marcador_nao_e_ok(self):
        assert _linha_tem_alias_ok("    WHERE aba = 'foo'") is False

    def test_linha_vazia_nao_e_ok(self):
        assert _linha_tem_alias_ok("") is False


# ---------------------------------------------------------------------------
# _classificar
# ---------------------------------------------------------------------------

class TestClassificar:

    def test_arquivo_bridge_retorna_bridge_controlado(self):
        arq = "services/canonical_input_service.py"
        assert arq in BRIDGE_FILES
        resultado = _classificar(arq, "    aba = self._get_aba()", "kwarg_aba")
        assert resultado == "bridge_controlado"

    def test_linha_com_alias_ok_retorna_alias_ok(self):
        resultado = _classificar(
            "services/qualquer.py",
            "x = alias_legacy_aba",
            "comparacao_aba",
        )
        assert resultado == "alias_ok"

    def test_arquivo_nao_bridge_linha_sem_marcador_retorna_residuo(self):
        resultado = _classificar(
            "services/novo_servico.py",
            "    if aba == 'xpto':",
            "comparacao_aba",
        )
        assert resultado == "residuo_ativo"

    def test_bridge_controlado_prevalece_sobre_alias_ok_quando_bridge_file(self):
        # arquivo bridge com linha que tem alias_ok -> alias_ok vence (verificado primeiro)
        arq = "services/canonical_input_service.py"
        resultado = _classificar(arq, "x = alias_legacy_aba", "comparacao_aba")
        assert resultado == "alias_ok"


# ---------------------------------------------------------------------------
# _varrer_arquivo
# ---------------------------------------------------------------------------

class TestVarrerArquivo:

    def test_detecta_param_aba_em_assinatura(self, raiz_tmp: Path):
        caminho = _escrever(
            raiz_tmp,
            "services/svc_x.py",
            """\
            def processar(aba, dados):
                return dados
            """,
        )
        ocs = _varrer_arquivo(caminho, raiz_tmp)
        assert len(ocs) == 1
        assert ocs[0].padrao == "param_aba_em_assinatura"
        assert ocs[0].classificacao == "residuo_ativo"

    def test_detecta_sql_where_aba(self, raiz_tmp: Path):
        caminho = _escrever(
            raiz_tmp,
            "repositories/rep_y.py",
            """\
            SQL = "SELECT * FROM tabela WHERE aba = :val"
            """,
        )
        ocs = _varrer_arquivo(caminho, raiz_tmp)
        assert any(o.padrao == "sql_where_aba" for o in ocs)

    def test_ignora_comentario_puro(self, raiz_tmp: Path):
        caminho = _escrever(
            raiz_tmp,
            "services/svc_z.py",
            """\
            # def processar(aba, dados):
            #     WHERE aba = 'x'
            """,
        )
        ocs = _varrer_arquivo(caminho, raiz_tmp)
        assert ocs == []

    def test_arquivo_bridge_classificado_bridge_controlado(self, raiz_tmp: Path):
        caminho = _escrever(
            raiz_tmp,
            "services/canonical_input_service.py",
            """\
            def get(aba, tipo):
                return _fetch(aba=aba)
            """,
        )
        ocs = _varrer_arquivo(caminho, raiz_tmp)
        for oc in ocs:
            assert oc.classificacao == "bridge_controlado"

    def test_linha_com_alias_legacy_aba_nao_e_residuo(self, raiz_tmp: Path):
        caminho = _escrever(
            raiz_tmp,
            "domain/entidade.py",
            """\
            campo = alias_legacy_aba
            """,
        )
        ocs = _varrer_arquivo(caminho, raiz_tmp)
        for oc in ocs:
            assert oc.classificacao != "residuo_ativo"

    def test_arquivo_inexistente_retorna_lista_vazia(self, raiz_tmp: Path):
        caminho = raiz_tmp / "services" / "nao_existe.py"
        ocs = _varrer_arquivo(caminho, raiz_tmp)
        assert ocs == []

    def test_detecta_kwarg_aba(self, raiz_tmp: Path):
        caminho = _escrever(
            raiz_tmp,
            "domain/calc.py",
            """\
            resultado = calcular(aba='principal', valor=10)
            """,
        )
        ocs = _varrer_arquivo(caminho, raiz_tmp)
        assert any(o.padrao == "kwarg_aba" for o in ocs)
        assert all(o.classificacao == "residuo_ativo" for o in ocs)

    def test_detecta_get_legs_com_aba(self, raiz_tmp: Path):
        caminho = _escrever(
            raiz_tmp,
            "services/svc_legs.py",
            """\
            dados = get_legs(aba, periodo)
            """,
        )
        ocs = _varrer_arquivo(caminho, raiz_tmp)
        assert any(o.padrao == "get_legs_com_aba" for o in ocs)

    def test_arquivo_fora_dos_scan_dirs_nao_e_varrido(self, raiz_tmp: Path):
        caminho = _escrever(
            raiz_tmp,
            "scripts/helper.py",
            """\
            def foo(aba):
                WHERE aba = 'x'
            """,
        )
        # varrer_projeto nao inclui scripts/
        todas = varrer_projeto(raiz_tmp)
        arquivos = [o.arquivo for o in todas]
        assert not any("scripts/helper" in a for a in arquivos)


# ---------------------------------------------------------------------------
# construir_relatorio
# ---------------------------------------------------------------------------

class TestConstruirRelatorio:

    def _ocs_fixture(self) -> list[Ocorrencia]:
        return [
            Ocorrencia("services/a.py", 10, "def f(aba):", "param_aba_em_assinatura", "residuo_ativo"),
            Ocorrencia("services/a.py", 20, "x = alias_legacy_aba", "comparacao_aba", "alias_ok"),
            Ocorrencia("services/canonical_input_service.py", 5, "aba=self._v", "kwarg_aba", "bridge_controlado"),
        ]

    def test_totais_corretos(self, tmp_path: Path):
        ocs = self._ocs_fixture()
        rel = construir_relatorio(ocs, tmp_path)
        assert rel.total_ocorrencias == 3
        assert rel.total_residuos_ativos == 1
        assert rel.total_bridge_controlado == 1
        assert rel.total_alias_ok == 1

    def test_residuos_por_arquivo_so_contem_residuos_ativos(self, tmp_path: Path):
        ocs = self._ocs_fixture()
        rel = construir_relatorio(ocs, tmp_path)
        assert "services/a.py" in rel.residuos_por_arquivo
        assert rel.residuos_por_arquivo["services/a.py"] == 1
        # canonical nao tem residuo_ativo
        assert "services/canonical_input_service.py" not in rel.residuos_por_arquivo

    def test_relatorio_vazio_quando_sem_ocorrencias(self, tmp_path: Path):
        rel = construir_relatorio([], tmp_path)
        assert rel.total_ocorrencias == 0
        assert rel.total_residuos_ativos == 0
        assert rel.residuos_por_arquivo == {}

    def test_arquivos_listados_no_relatorio(self, tmp_path: Path):
        ocs = self._ocs_fixture()
        rel = construir_relatorio(ocs, tmp_path)
        nomes = [b["arquivo"] for b in rel.arquivos]
        assert "services/a.py" in nomes
        assert "services/canonical_input_service.py" in nomes


# ---------------------------------------------------------------------------
# gerar_markdown
# ---------------------------------------------------------------------------

class TestGerarMarkdown:

    def _rel_simples(self, tmp_path: Path) -> Relatorio:
        ocs = [
            Ocorrencia("services/svc.py", 7, "def f(aba):", "param_aba_em_assinatura", "residuo_ativo"),
        ]
        return construir_relatorio(ocs, tmp_path)

    def test_arquivo_md_criado(self, tmp_path: Path):
        rel = self._rel_simples(tmp_path)
        destino = tmp_path / "relatorio.md"
        gerar_markdown(rel, destino)
        assert destino.exists()

    def test_md_contem_cabecalho(self, tmp_path: Path):
        rel = self._rel_simples(tmp_path)
        destino = tmp_path / "relatorio.md"
        gerar_markdown(rel, destino)
        conteudo = destino.read_text(encoding="utf-8")
        assert "patch_52" in conteudo
        assert "Residuos Ativos" in conteudo

    def test_md_contem_arquivo_com_residuo(self, tmp_path: Path):
        rel = self._rel_simples(tmp_path)
        destino = tmp_path / "relatorio.md"
        gerar_markdown(rel, destino)
        conteudo = destino.read_text(encoding="utf-8")
        assert "services/svc.py" in conteudo
        assert "residuo_ativo" in conteudo

    def test_md_sem_residuos_exibe_mensagem_vazia(self, tmp_path: Path):
        rel = construir_relatorio([], tmp_path)
        destino = tmp_path / "relatorio.md"
        gerar_markdown(rel, destino)
        conteudo = destino.read_text(encoding="utf-8")
        assert "Nenhum residuo ativo encontrado" in conteudo

    def test_md_contem_proximos_passos(self, tmp_path: Path):
        rel = self._rel_simples(tmp_path)
        destino = tmp_path / "relatorio.md"
        gerar_markdown(rel, destino)
        conteudo = destino.read_text(encoding="utf-8")
        assert "patch_53" in conteudo


# ---------------------------------------------------------------------------
# gerar_json
# ---------------------------------------------------------------------------

class TestGerarJson:

    def test_json_valido_e_deserializavel(self, tmp_path: Path):
        ocs = [
            Ocorrencia("domain/ent.py", 3, "aba='x'", "kwarg_aba", "residuo_ativo"),
        ]
        rel = construir_relatorio(ocs, tmp_path)
        destino = tmp_path / "relatorio.json"
        gerar_json(rel, destino)
        dados = json.loads(destino.read_text(encoding="utf-8"))
        assert dados["total_residuos_ativos"] == 1
        assert isinstance(dados["arquivos"], list)

    def test_json_contem_campo_gerado_em(self, tmp_path: Path):
        rel = construir_relatorio([], tmp_path)
        destino = tmp_path / "relatorio.json"
        gerar_json(rel, destino)
        dados = json.loads(destino.read_text(encoding="utf-8"))
        assert "gerado_em" in dados
        assert dados["gerado_em"] != ""

    def test_json_sem_ocorrencias_estrutura_minima(self, tmp_path: Path):
        rel = construir_relatorio([], tmp_path)
        destino = tmp_path / "relatorio.json"
        gerar_json(rel, destino)
        dados = json.loads(destino.read_text(encoding="utf-8"))
        assert dados["total_ocorrencias"] == 0
        assert dados["residuos_por_arquivo"] == {}


# ---------------------------------------------------------------------------
# varrer_projeto (integracao leve)
# ---------------------------------------------------------------------------

class TestVarrerProjeto:

    def test_diretorio_inexistente_nao_levanta_excecao(self, tmp_path: Path):
        # nenhum subdir criado, varrer_projeto deve retornar lista vazia sem erro
        resultado = varrer_projeto(tmp_path)
        assert isinstance(resultado, list)

    def test_varredura_completa_detecta_residuos_em_multiplos_dirs(self, raiz_tmp: Path):
        _escrever(raiz_tmp, "services/svc_a.py", "def f(aba): pass\n")
        _escrever(raiz_tmp, "repositories/rep_b.py", 'SQL = "WHERE aba = :v"\n')
        _escrever(raiz_tmp, "domain/ent_c.py", "x = calcular(aba='x')\n")

        ocs = varrer_projeto(raiz_tmp)
        arquivos_com_residuo = {o.arquivo for o in ocs if o.classificacao == "residuo_ativo"}

        assert "services/svc_a.py" in arquivos_com_residuo
        assert "repositories/rep_b.py" in arquivos_com_residuo
        assert "domain/ent_c.py" in arquivos_com_residuo

    def test_varredura_nao_inclui_extensoes_nao_py(self, raiz_tmp: Path):
        caminho = raiz_tmp / "services" / "config.yaml"
        caminho.write_text("aba: principal\n", encoding="utf-8")
        ocs = varrer_projeto(raiz_tmp)
        assert not any(".yaml" in o.arquivo for o in ocs)
