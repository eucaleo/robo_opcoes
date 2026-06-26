# Revisão funcional pós uso real — Fase 8 — Duplicidade de estrutura

## Status

Concluída por reconciliação.

## Objetivo original

Investigar a ocorrência relatada em que a estrutura número 2 aparecia duplicada na listagem, mas a duplicidade não aparecia no filtro de decisão.

## Resultado da investigação

A investigação do estado atual indicou que o problema não está mais presente no banco operacional atual.

No banco oficial atual dados/app.db:

- A tabela structures possui 2 registros.
- A estrutura id = 2 aparece uma única vez.
- Não há nomes duplicados em structures.
- Não há duplicidade de legs por structure_id + símbolo normalizado em structure_legs.

Resultado observado:

    === DB: dados\app.db ===

    [structures] total:
    2

    [structures] id = 2:
    linhas com id=2: 1

    [structures] possíveis nomes duplicados:
    sem nomes duplicados

    [structure_legs] duplicidade por structure_id + símbolo normalizado:
    sem duplicidade de legs por estrutura

O script de andamento da rota também confirmou:

    Possíveis duplicidades em structures
    total_structures=2
    (sem duplicidade física por id em structures)

## Reconciliação histórica

Durante a validação foram encontrados bancos antigos e evidências históricas indicando duplicidade em backup anterior.

Exemplo observado em dados/app.backup_antes_corrigir_bovas61.db:

    structure_id=2, symbol_norm=BOVAG34, qtd=2

Esse achado confirma que havia um problema histórico relacionado à estrutura 2, mas ele não está presente no banco operacional atual.

A correção foi antecipada durante a Fase 6, especialmente no commit:

    f67d408 Corrige edição e duplicidade de legs em estruturas

A Fase 6 também registrou correções preventivas:

- validação de símbolo duplicado no formulário;
- validação de duplicidade no payload antes de salvar;
- bloqueio de duplicidade por estrutura no repositório;
- integridade reforçada para evitar legs duplicadas.

## Decisão

Não será feita alteração adicional de código nesta fase.

A Fase 8 fica encerrada como resolvida por antecipação e validada no estado atual.

## Evidências técnicas

- python scripts/verificar_andamento_rota.py
- diagnóstico direto dos bancos SQLite
- grep focado em duplicidade no código ativo
- python -m compileall executado com retorno 0

## Conclusão

A duplicidade da estrutura número 2 não é mais reproduzível no estado atual do projeto.

A Fase 8 está concluída documentalmente.
