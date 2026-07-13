import inspect
import unittest

from rtd_excel_online import fase7_alertas_decisao as modulo
from rtd_excel_online.fase7_alertas_decisao import (
    ParametrosAlerta,
    SnapshotMercado,
    avaliar_snapshot,
)


class TestFase7AlertasDecisao(unittest.TestCase):
    def test_preco_acima_do_vwap_gera_alerta_somente_leitura(self):
        resultado = avaliar_snapshot(
            SnapshotMercado(
                simbolo="TESTE1",
                ultimo_preco=10.50,
                vwap=10.00,
            ),
            timestamp="2026-07-10T20:00:00+00:00",
        )

        regras = {alerta.regra for alerta in resultado.alertas}

        self.assertIn("PRECO_ACIMA_VWAP", regras)
        self.assertEqual(resultado.decisao.classificacao, "ACIMA_DO_VWAP")
        self.assertFalse(resultado.decisao.permite_execucao)

    def test_cruzamento_de_alta_do_vwap_gera_decisao_explicavel(self):
        resultado = avaliar_snapshot(
            SnapshotMercado(
                simbolo="TESTE2",
                preco_anterior=9.90,
                vwap_anterior=10.00,
                ultimo_preco=10.20,
                vwap=10.05,
            ),
            timestamp="2026-07-10T20:01:00+00:00",
        )

        regras = {alerta.regra for alerta in resultado.alertas}

        self.assertIn("CRUZAMENTO_ALTA_VWAP", regras)
        self.assertEqual(resultado.decisao.classificacao, "ACOMPANHAR_ALTA")
        self.assertFalse(resultado.decisao.permite_execucao)

    def test_spread_anormal_bloqueia_operacao(self):
        resultado = avaliar_snapshot(
            SnapshotMercado(
                simbolo="TESTE3",
                bid=10.00,
                ask=11.00,
                ultimo_preco=10.50,
                vwap=10.20,
            ),
            ParametrosAlerta(max_spread_pct=0.02),
            timestamp="2026-07-10T20:02:00+00:00",
        )

        regras = {alerta.regra for alerta in resultado.alertas}

        self.assertIn("SPREAD_ANORMAL", regras)
        self.assertEqual(resultado.decisao.classificacao, "EVITAR_OPERACAO")
        self.assertFalse(resultado.decisao.permite_execucao)

    def test_liquidez_baixa_bloqueia_operacao(self):
        resultado = avaliar_snapshot(
            SnapshotMercado(
                simbolo="TESTE4",
                volume=0,
                ultimo_preco=8.50,
                vwap=8.40,
            ),
            ParametrosAlerta(min_volume=1),
            timestamp="2026-07-10T20:03:00+00:00",
        )

        regras = {alerta.regra for alerta in resultado.alertas}

        self.assertIn("LIQUIDEZ_BAIXA", regras)
        self.assertEqual(resultado.decisao.classificacao, "EVITAR_OPERACAO")
        self.assertFalse(resultado.decisao.permite_execucao)

    def test_payoff_e_estrutura_favoravel_sao_sinais_somente_leitura(self):
        resultado = avaliar_snapshot(
            SnapshotMercado(
                simbolo="TESTE5",
                payoff_anterior=100.00,
                payoff_atual=101.00,
                estrutura_favoravel=True,
            ),
            ParametrosAlerta(payoff_delta_relevante=0.50),
            timestamp="2026-07-10T20:04:00+00:00",
        )

        regras = {alerta.regra for alerta in resultado.alertas}

        self.assertIn("PAYOFF_ALTERADO", regras)
        self.assertIn("ESTRUTURA_FAVORAVEL", regras)
        self.assertFalse(resultado.decisao.permite_execucao)

    def test_simbolo_obrigatorio(self):
        with self.assertRaises(ValueError):
            avaliar_snapshot(SnapshotMercado(simbolo=""))

    def test_modulo_nao_importa_dependencias_operacionais(self):
        fonte = inspect.getsource(modulo).lower()

        proibidos = [
            "win32com",
            "openpyxl",
            "xlwings",
            "sqlite3",
            "subprocess",
            "pyautogui",
            "socket",
        ]

        for termo in proibidos:
            self.assertNotIn(termo, fonte)


if __name__ == "__main__":
    unittest.main()
