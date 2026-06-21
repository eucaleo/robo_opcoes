# EVOLUCAO_REVISAO_FUNCIONAL_POS_USO_REAL

## Objetivo

Registrar a evolução da revisão funcional pós uso real, acompanhando fases, testes, evidências, arquivos alterados, commits realizados e pendências identificadas.

## Documento base

| Item | Informação |
|---|---|
| Rota de controle | docs/ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md |
| Branch base | main |
| Último marco conhecido | ROTA_MESTRE_3 encerrada |
| Commit de fechamento informado | f95bcb8 |
| Commit de organização documental | 751fe22 |
| Status | Revisão funcional aberta |

## Regras principais

1. Não migrar para web.
2. Não utilizar emojis.
3. Manter-se ao escopo da revisão.
4. Efetuar buscas de dados e arquivos antes de alterações.
5. Toda mudança deve ser testada após concluída.
6. Após encerramento de fase, testar também as fases já encerradas.
7. Em alterações sempre gerar código inteiro do arquivo.
8. A cada alteração concluída e testada, commitar.
9. Não codar sem rumo.
10. Criar arquivo de auditoria para ser atualizado com os testes.
11. Não gerar código com crase, sempre usar indentação.

## Fases

| Fase | Descrição | Status |
|---|---|---|
| Marco 0 | Controle e congelamento da rota | Concluído |
| Fase 1 | Reprodução controlada dos problemas | Pendente |
| Fase 2 | Correção da normalização numérica | Pendente |
| Fase 3 | Cadastro manual, payoff e decisões | Pendente |
| Fase 4 | Botão atualizar dados | Pendente |
| Fase 5 | Execução RTD | Pendente |
| Fase 6 | Validação integrada | Pendente |

## Problemas acompanhados

| ID | Problema | Status |
|---|---|---|
| P-001 | Erro com vírgula decimal em strike/preço | Pendente |
| P-002 | Inclusão assistida por símbolo da opção | Pendente |
| P-003 | Estrutura manual aparece, mas não gera payoff | Pendente |
| P-004 | Estrutura manual não gera decisões | Pendente |
| P-005 | Botão atualizar dados com feedback genérico ou insuficiente | Pendente |
| P-006 | Atualização RTD não refletida no sistema | Pendente |
| P-007 | Possível divergência de horário | Pendente |

## Registro de evolução

### Registro 001

| Campo | Informação |
|---|---|
| Data | 2026-06-21 |
| Fase | Marco 0 |
| Ação | Organização dos documentos anteriores em docs/evolucoes de fases/ |
| Commit | 751fe22 |
| Resultado | Fases anteriores separadas da revisão funcional atual |
| Status | Concluído |

### Registro 002

| Campo | Informação |
|---|---|
| Data | 2026-06-21 |
| Fase | Marco 0 |
| Ação | Criação da rota de controle da revisão funcional |
| Arquivo | docs/ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md |
| Resultado | Documento base disponível para condução das próximas fases |
| Status | Pendente de commit |

## Evidências iniciais

| ID | Tipo | Descrição | Status |
|---|---|---|---|
| EV-001 | Documento | Rota de revisão funcional consolidada | Registrado |
| EV-002 | Teste/print | Erro strike must be numeric com vírgula decimal | Registrado |
| EV-003 | Teste/print | Estrutura manual aparece, mas não gera payoff/decisões | Registrado |
| EV-004 | Teste/print | Pipeline com mensagem genérica de sucesso | Registrado |

## Comandos de validação previstos

    python -m pytest ATT/tests -q
    python -m compileall repositories services domain ATT/tests

## Pendências abertas

| ID | Pendência | Prioridade | Status |
|---|---|---|---|
| PE-001 | Iniciar reprodução controlada da Fase 1 | Alta | Pendente |
| PE-002 | Corrigir normalização numérica antes da validação | Alta | Pendente |
| PE-003 | Garantir cadastro manual funcional | Alta | Pendente |
| PE-004 | Garantir geração de payoff | Alta | Pendente |
| PE-005 | Garantir geração de decisões | Alta | Pendente |
| PE-006 | Melhorar feedback do pipeline | Média | Pendente |
| PE-007 | Validar e estabilizar RTD | Média | Pendente |
| PE-008 | Padronizar horário exibido | Baixa | Pendente |
