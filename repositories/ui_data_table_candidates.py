"""
Candidatos de tabelas para leitura de dados da UI.

Este módulo concentra aliases físicos/canônicos usados para detectar
schemas existentes no banco derivado.

A UI deve consumir estas listas sem conhecer diretamente nomes físicos
legados de staging, como tabelas rtd_*.
"""

CANDIDATE_CONSOLIDATION_TABLES = [
    "structure_decisions",
    "rtd_consolidacoes",
    "rtd_consolidations",
    "decisions",
    "rtd_decisions",
]

CANDIDATE_PAYOFF_TABLES = [
    "payoff_curve_points",
    "rtd_payoff_points",
    "rtd_payoff_curva",
    "payoff_points",
]
