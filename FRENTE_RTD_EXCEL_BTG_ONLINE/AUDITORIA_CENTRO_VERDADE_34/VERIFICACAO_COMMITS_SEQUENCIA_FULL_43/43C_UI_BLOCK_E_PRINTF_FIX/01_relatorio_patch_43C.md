# Rodada 43C - Relatorio de patch

- Corrigido `scripts/verify_commits_sequence_full_43B.sh`: `printf '- ...'` -> `printf -- '- ...'`.
- Alterado `UI/main_window.py`: `recalculate_structure()` agora bloqueia recálculo via UI.
- Alterado `UI/main_window.py`: `run_pipeline()` agora bloqueia execução de pipeline via UI.
