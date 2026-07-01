# Fase 1 RTD - desacoplamento de rtd_underlying_quotes no terminal VWAP/Payoff

Atualizado em: 20260630_223440

## Objetivo

Remover consulta direta da UI à tabela operacional rtd_underlying_quotes.

## Arquivos alterados

    UI/components/terminal_vwap_payoff_dark_panel.py
    repositories/rtd_underlying_quotes_repository.py

## Fluxo anterior

    TerminalVWAPPayoffDarkPanel
        -> sqlite3.connect
            -> dados/app.db
                -> rtd_underlying_quotes

## Fluxo atual

    TerminalVWAPPayoffDarkPanel
        -> RtdUnderlyingQuotesRepository.get_latest_by_asset
            -> dados/app.db.rtd_underlying_quotes

## Verificações executadas

### py_compile

    py_compile OK

### Testes RTD

...                                                                      [100%]
3 passed in 0.09s
....                                                                     [100%]
4 passed in 0.29s
.......                                                                  [100%]
7 passed in 0.36s

## Varredura de resíduo RTD no painel

    ATT/tests/test_rtd_live_db_guardrail.py:39:    A tabela rtd_option_quotes e a tabela rtd_underlying_quotes não podem voltar
    UI/components/terminal_vwap_payoff_dark_panel.py:39:    from repositories.rtd_underlying_quotes_repository import RtdUnderlyingQuotesRepository
    UI/components/terminal_vwap_payoff_dark_panel.py:140:        _rtd_underlying_quotes_repository=None,
    UI/components/terminal_vwap_payoff_dark_panel.py:146:        self._rtd_underlying_quotes_repository = _rtd_underlying_quotes_repository
    UI/components/terminal_vwap_payoff_dark_panel.py:676:    def _get_rtd_underlying_quotes_repository(self):
    UI/components/terminal_vwap_payoff_dark_panel.py:677:        if self._rtd_underlying_quotes_repository is None:
    UI/components/terminal_vwap_payoff_dark_panel.py:680:            self._rtd_underlying_quotes_repository = RtdUnderlyingQuotesRepository(
    UI/components/terminal_vwap_payoff_dark_panel.py:683:        return self._rtd_underlying_quotes_repository
    UI/components/terminal_vwap_payoff_dark_panel.py:687:            return self._get_rtd_underlying_quotes_repository().get_latest_by_asset(
    UI/components/terminal_vwap_payoff_dark_panel.py:894:            alerts.append("VWAP do ativo-base ausente em rtd_underlying_quotes")

## Conclusão

    A UI deixa de montar SQL e selecionar diretamente da tabela rtd_underlying_quotes.
    A leitura RTD do ativo-base passa a ficar centralizada em repository.
    Permanece aceitável o alerta textual da UI citando rtd_underlying_quotes.
