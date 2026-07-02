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
    [ModernDarkUI] 2 estruturas carregadas
    [ModernDarkUI] Estrutura carregada: ID 3

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
| Filtros de decisões | NÃO TESTADO |PARCIAL|  |
| Seleção de decisões | NÃO TESTADO |PARCIAL|  |
| Detalhamento de decisão | NÃO TESTADO |PARCIAL|  |
| Rationale/why JSON | NÃO TESTADO |AUSENTE|  |
| Recalcular estrutura | NÃO TESTADO | PARCIAL |  |
| Curva de Payoff | NÃO TESTADO | PARCIAL |  |
| Comparação Curva A | NÃO TESTADO | PARCIAL |  |
| Exportação PNG | NÃO TESTADO | AUSENTE |  |
| CRUD de estruturas | NÃO TESTADO | PARCIAL |  |
| Terminal VWAP Payoff | NÃO TESTADO | PARCIAL |  |
| Legs/pernas da estrutura | NÃO TESTADO | VALIDADO |  |
| Mensagens de status | NÃO TESTADO | PARCIAL |  |
| Banco e contratos canônicos | NÃO TESTADO | NÃO TESTADO |  |
| Conexao com RTD | AUSENTE|  |  |
| Validação nova perna| PARCIAL |  |  |

## Observações por área

### Estruturas

- Observação:
- Pendência:

### Payoff

- Observação:
- Pendência:

### Terminal VWAP Payoff

- Observação:
- Pendência:

### Decisões

- Observação:
- Pendência:

### Exportação

- Observação:
- Pendência:

### Status e mensagens

- Observação:
- Pendência:

## Conclusão manual

Conclusão desta rodada:

- [ ] O modo dark ainda NÃO possui equivalência funcional suficiente para substituir a UI atual.
- [ ] O modo dark possui equivalência parcial e pode continuar evoluindo em paralelo.
- [ ] A UI atual deve permanecer como caminho principal.
- [ ] Próximos patches devem ser pequenos e por função faltante.

## Próxima decisão recomendada

Após preencher esta validação, escolher apenas uma função pendente para implementação ou realocação no modo dark.

Ordem sugerida:

1. seleção/detalhamento de decisões;
2. filtros de decisões;
3. exportação PNG;
4. comparação Curva A;
5. rationale/why JSON.
