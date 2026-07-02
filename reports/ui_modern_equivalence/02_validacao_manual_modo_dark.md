# Validação manual de equivalência funcional do modo dark

Data de referência: 2026-07-02

Base de comparação:

- reports/ui_modern_equivalence/01_mapa_equivalencia_funcional_ui_moderna.md

Objetivo:

- validar manualmente o que está funcionalmente presente no caminho preferencial da UI moderna;
- separar presença visual de equivalência funcional;
- impedir troca de entrypoint antes de cobertura mínima validada.

## Resultado de abertura da UI moderna

Comando usado:

    python -m UI.modern

Resultado observado:

- [x] Janela abriu normalmente.
- [x] Modo dark permaneceu ativo.
- [x] Estruturas reais carregaram.
- [x] Não houve erro visível no terminal.
- [x] Não houve mudança funcional perceptível após centralização inicial de tema.

Observação registrada:

    [ModernApp] Abrindo UI moderna mode='dark' theme='dark' module='UI.modern.dark_window'
    [ModernDarkUI] 2 estruturas carregadas
    [ModernDarkUI] Estrutura carregada: ID 2
    [ModernDarkUI] Estrutura carregada: ID 3
    [ModernDarkUI] 2 estruturas carregadas
    [ModernDarkUI] 2 estruturas carregadas
    [ModernDarkUI] Estruturas recarregadas

## Critérios de classificação

Use os seguintes status:

- VALIDADO: função visível e operacional no modo dark.
- PARCIAL: função aparece, mas requer complemento, teste ou comparação adicional.
- AUSENTE: função não foi encontrada no modo dark.
- REALOCADO: função existe, mas em posição diferente da UI atual.
- NÃO TESTADO: não foi possível validar nesta rodada.

## Checklist funcional

| Função obrigatória | Status manual | Evidência/observação | Próxima ação |
|---|---|---|---|
| Filtros de decisões | PARCIAL | Presença parcial observada no modo dark. | Detalhar lacunas funcionais em rodada específica. |
| Seleção de decisões | PARCIAL | Presença parcial observada no modo dark. | Validar seleção contra UI atual. |
| Detalhamento de decisão | PARCIAL | Presença parcial observada no modo dark. | Validar campos e comportamento contra UI atual. |
| Rationale/why JSON | AUSENTE | Função não localizada no modo dark. | Implementar ou realocar em rodada futura. |
| Recalcular estrutura | PARCIAL | Presença parcial observada no modo dark. | Validar cálculo, callback e mensagens. |
| Curva de Payoff | PARCIAL | Presença parcial observada no modo dark. | Comparar comportamento com UI atual. |
| Comparação Curva A | PARCIAL | Presença parcial observada no modo dark. | Validar fluxo completo de comparação. |
| Exportação PNG | AUSENTE | Função não localizada no modo dark. | Implementar exportação em patch isolado. |
| CRUD de estruturas | PARCIAL | Presença parcial observada no modo dark. | Validar criar, editar, remover e recarregar. |
| Terminal VWAP Payoff | PARCIAL | Presença parcial observada no modo dark. | Validar equivalência funcional por bloco. |
| Legs/pernas da estrutura | VALIDADO | Pernas visíveis e utilizáveis no modo dark. | Manter contrato e evitar regressão. |
| Mensagens de status | PARCIAL | Mensagens aparecem no terminal e no fluxo observado. | Validar cobertura completa de estados. |
| Banco e contratos canônicos | NÃO TESTADO | Não validado nesta rodada. | Validar sem alterar contratos canônicos. |
| Conexão com RTD | AUSENTE | Função não localizada no modo dark. | Mapear dependência e decidir se entra no modo moderno. |
| Validação nova perna | PARCIAL | Presença parcial observada no modo dark. | Validar regras de entrada e mensagens. |

## Observações por área

### Estruturas

- Observação: estruturas reais foram carregadas e recarregadas no modo dark.
- Pendência: validar CRUD completo e regras de nova perna.

### Payoff

- Observação: recursos de payoff foram classificados como parciais.
- Pendência: comparar curva, recálculo e comparação Curva A contra a UI atual.

### Terminal VWAP Payoff

- Observação: terminal moderno abriu e carregou estruturas.
- Pendência: validar equivalência funcional por bloco.

### Decisões

- Observação: filtros, seleção e detalhamento foram classificados como parciais.
- Pendência: validar comportamento completo e verificar rationale/why JSON.

### Exportação

- Observação: exportação PNG foi classificada como ausente.
- Pendência: implementar exportação em patch isolado quando priorizado.

### Status e mensagens

- Observação: mensagens foram emitidas durante abertura, carregamento e recarregamento.
- Pendência: validar cobertura completa de erro, sucesso e ações do usuário.

## Conclusão manual

Conclusão desta rodada:

- [x] O modo dark ainda NÃO possui equivalência funcional suficiente para substituir a UI atual.
- [x] O modo dark possui equivalência parcial e pode continuar evoluindo em paralelo.
- [x] A UI atual deve permanecer como caminho principal.
- [x] Próximos patches devem ser pequenos e por função faltante.

## Próxima decisão recomendada

Após esta validação, escolher apenas uma função pendente para implementação ou realocação no modo dark.

Ordem sugerida:

1. seleção/detalhamento de decisões;
2. filtros de decisões;
3. exportação PNG;
4. comparação Curva A;
5. rationale/why JSON.
