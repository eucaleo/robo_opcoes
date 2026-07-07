## Objetivo

Adiciona smoke opt-in da Payoff UI moderna para validar o entrypoint moderno e o modo smoke sem abrir a UI completa.

## Arquivos principais

- ATT/tests/test_modern_ui_entrypoint_smoke.py
- ATT/tests/test_modern_ui_smoke_mode.py
- UI/modern/smoke_mode.py
- pytest.ini

## Validação local

Executado em Windows/Git Bash:

    pytest ATT/tests/test_modern_ui_smoke_mode.py -q
    pytest ATT/tests/test_modern_ui_entrypoint_smoke.py -q
    python -m UI.modern --info

Resultado local:

    10 passed
    1 passed, 1 skipped
    python -m UI.modern --info OK

## Commit

    72c12b7 test: adiciona smoke opt-in da Payoff UI moderna

## Status

    SMOKE_OPT_IN_PAYOFF_UI_MODERNA:
    VALIDADO_NA_BRANCH_FIX
    PENDENTE_DE_MERGE_NA_MAIN
