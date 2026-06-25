# EVOLUCAO_REVISAO_FUNCIONAL_POS_USO_REAL

## Objetivo

Registrar a evolução da revisão funcional pós uso real, acompanhando fases, testes, evidências, arquivos alterados, commits realizados e pendências identificadas.

## Documento base

| Item | Informação |
|---|---|
| Rota de controle | docs/ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md |
| Branch base | main |
| Branch de trabalho atual | fase-3a4-auto-pricing-manual-save |
| Último marco conhecido | ROTA_MESTRE_3 encerrada |
| Commit de fechamento informado | f95bcb8 |
| Commit de organização documental informado | 751fe22 |
| Status | Revisão funcional aberta, com Fase 3A.4 concluída tecnicamente |

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
| Fase 1 | Reprodução controlada dos problemas | Parcialmente executada por evidências reais; pendente fechamento formal |
| Fase 2 | Correção da normalização numérica | Parcialmente concluída em strike; pendente validar preço, quantidade e fluxo completo |
| Fase 3 | Cadastro manual, payoff e decisões | Concluída tecnicamente na subfase 3A.4; pendente validação manual visual em tela |
| Fase 4 | Botão atualizar dados | Pendente |
| Fase 5 | Execução RTD | Pendente |
| Fase 6 | Validação integrada | Parcialmente executada para Fase 3A.4; pendente validação final após Fases 4 e 5 |

## Problemas acompanhados

| ID | Problema | Status |
|---|---|---|
| P-001 | Erro com vírgula decimal em strike/preço | Parcialmente corrigido para strike pelo commit 5826883; pendente confirmar preço, quantidade e fluxo completo |
| P-002 | Inclusão assistida por símbolo da opção | Pendente |
| P-003 | Estrutura manual aparece, mas não gera payoff | Encaminhado tecnicamente pela Fase 3A.4; pendente validação manual visual |
| P-004 | Estrutura manual não gera decisões | Encaminhado tecnicamente pela Fase 3A.4; pendente validação manual visual |
| P-005 | Botão atualizar dados com feedback genérico ou insuficiente | Pendente |
| P-006 | Atualização RTD não refletida no sistema | Pendente |
| P-007 | Possível divergência de horário | Pendente |

## Histórico de commits relevantes

| Commit | Tipo | Descrição | Fase relacionada |
|---|---|---|---|
| f95bcb8 | Marco informado | Fechamento informado da ROTA_MESTRE_3 | Base anterior |
| 751fe22 | Documento informado | Organização documental informada | Marco 0 |
| 5826883 | Correção | fix(editor): normalize strike decimal in legs payload | Fase 2 |
| 34bc73c | Evidência | docs(checkpoints): add fase 2a strike investigation evidence | Fase 2 |
| 9f1622b | Correção | fase-3a4: recalcula pricing após salvar estrutura manual | Fase 3 |
| a79b6c1 | Evidência | docs: adiciona evidências das fases 3a a 3a3 | Fase 3 |
| 7f23b6f | Evidência | docs: registra validação integrada da fase 3a4 | Fase 3 / Validação parcial |

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
| Status | Concluído documentalmente; commit específico da criação da rota não está disponível no histórico informado deste trecho |

### Registro 003

| Campo | Informação |
|---|---|
| Data | 2026-06-21 |
| Fase | Fase 2 / Subfase 2A |
| Ação | Investigação e correção inicial da normalização de strike com vírgula decimal |
| Commit de correção | 5826883 |
| Commit de evidência | 34bc73c |
| Resultado | Normalização de strike no payload de legs foi corrigida no editor |
| Status | Parcialmente concluído; pendente validar preço, quantidade, mensagens de erro e fluxo completo de cadastro |

### Registro 004

| Campo | Informação |
|---|---|
| Data | 2026-06-21 |
| Fase | Fase 3 / Subfases 3A a 3A.3 |
| Ação | Registro documental das buscas, evidências e análises relacionadas a estrutura, payoff, decisões e persistência |
| Commit documental | a79b6c1 |
| Resultado | Evidências técnicas das fases 3A a 3A.3 foram adicionadas ao histórico do projeto |
| Arquivos | docs/checkpoints/evidencias/fase-3a-*.txt; docs/checkpoints/evidencias/fase-3a2-*.txt; docs/checkpoints/evidencias/fase-3a3-*.txt |
| Status | Concluído |

### Registro 005

| Campo | Informação |
|---|---|
| Data | 2026-06-21 |
| Fase | Fase 3 / Subfase 3A.4 |
| Ação | Recalculo de pricing, payoff e decisões após salvar estrutura manual |
| Commit funcional | 9f1622b |
| Resultado | Estrutura manual salva passou a acionar atualização funcional para pricing, payoff e decisões |
| Impacto esperado | Estrutura manual deixa de ficar apenas visual e passa a participar do fluxo funcional de cálculo |
| Status | Concluído tecnicamente; pendente validação manual visual em tela |

### Registro 006

| Campo | Informação |
|---|---|
| Data | 2026-06-21 |
| Fase | Fase 3 / Validação integrada parcial |
| Ação | Execução de suíte integrada e compileall após Fase 3A.4 |
| Commit documental | 7f23b6f |
| Evidência pytest | docs/checkpoints/evidencias/fase-3a4-pytest-suite-integrada.txt |
| Evidência compileall | docs/checkpoints/evidencias/fase-3a4-compileall-integrado.txt |
| Resultado pytest | 623 passed, 10 skipped, 6 subtests passed |
| Resultado compileall | Executado sem erro reportado em repositories, services, domain, UI e ATT/tests |
| Status | Concluído |

## Evidências registradas

| ID | Tipo | Descrição | Status |
|---|---|---|---|
| EV-001 | Documento | Rota de revisão funcional consolidada | Registrado |
| EV-002 | Teste/print | Erro strike must be numeric com vírgula decimal | Registrado |
| EV-003 | Teste/print | Estrutura manual aparece, mas não gera payoff/decisões | Registrado |
| EV-004 | Teste/print | Pipeline com mensagem genérica de sucesso | Registrado |
| EV-005 | Evidência técnica | Evidências das fases 3A a 3A.3 adicionadas em docs/checkpoints/evidencias/ | Registrado |
| EV-006 | Teste automatizado | Suíte integrada da Fase 3A.4 com 623 passed, 10 skipped, 6 subtests passed | Registrado |
| EV-007 | Compileall | Compileall executado sem erro reportado para repositories, services, domain, UI e ATT/tests | Registrado |

## Comandos de validação previstos

    python -m pytest ATT/tests -q
    python -m compileall repositories services domain UI ATT/tests

## Validações executadas nesta revisão

| Data | Fase | Comando | Resultado | Evidência |
|---|---|---|---|---|
| 2026-06-21 | Fase 3A.4 | python -m pytest ATT/tests -q | 623 passed, 10 skipped, 6 subtests passed | docs/checkpoints/evidencias/fase-3a4-pytest-suite-integrada.txt |
| 2026-06-21 | Fase 3A.4 | python -m compileall repositories services domain UI ATT/tests | Sem erro reportado | docs/checkpoints/evidencias/fase-3a4-compileall-integrado.txt |

## Pendências abertas

| ID | Pendência | Prioridade | Status |
|---|---|---|---|
| PE-001 | Iniciar reprodução controlada da Fase 1 | Alta | Parcialmente atendida por evidências reais; pendente fechamento formal da reprodução controlada |
| PE-002 | Corrigir normalização numérica antes da validação | Alta | Parcialmente concluída para strike; pendente preço, quantidade e mensagens |
| PE-003 | Garantir cadastro manual funcional | Alta | Concluído tecnicamente pela Fase 3A.4; pendente validação manual visual |
| PE-004 | Garantir geração de payoff | Alta | Concluído tecnicamente pela Fase 3A.4; pendente validação manual visual |
| PE-005 | Garantir geração de decisões | Alta | Concluído tecnicamente pela Fase 3A.4; pendente validação manual visual |
| PE-006 | Melhorar feedback do pipeline | Média | Pendente |
| PE-007 | Validar e estabilizar RTD | Média | Pendente |
| PE-008 | Padronizar horário exibido | Baixa | Pendente |

## Próxima ação recomendada

A próxima ação deve seguir a rota sem abrir nova funcionalidade fora do escopo.

Prioridade recomendada:

1. Confirmar visualmente na interface o fluxo da Fase 3A.4:
    - cadastrar estrutura manual;
    - salvar;
    - verificar geração de payoff;
    - verificar geração de decisões.
2. Retomar a Fase 2 para fechar a normalização numérica completa:
    - strike com vírgula e ponto;
    - preço/prêmio com vírgula e ponto;
    - quantidade;
    - mensagens claras para texto inválido;
    - testes unitários e de fluxo.
3. Depois seguir para Fase 4:
    - botão atualizar dados com feedback detalhado e execução rastreável.
4. Depois seguir para Fase 5:
    - execução RTD, persistência e contagem de registros atualizados.

## Critério para encerramento técnico da Fase 3

A Fase 3 pode ser considerada tecnicamente encaminhada pelos testes automatizados, mas só deve ser marcada como encerrada completamente após evidência manual ou teste funcional equivalente demonstrando que:

1. A estrutura manual aparece na listagem.
2. A estrutura manual possui legs válidas.
3. A curva de payoff é gerada sem erro.
4. A busca de decisões retorna dados ou informa claramente o motivo de rejeição.
5. O banco contém os registros esperados em payoff e decisões, quando aplicável.

## Estado consolidado atual

| Área | Estado |
|---|---|
| Auditoria documental | Atualizada até Fase 3A.4 |
| Testes automatizados | Suíte integrada aprovada na Fase 3A.4 |
| Compileall | Executado sem erro reportado |
| Cadastro manual | Concluído tecnicamente; pendente validação manual visual |
| Payoff após cadastro manual | Concluído tecnicamente; pendente validação manual visual |
| Decisões após cadastro manual | Concluído tecnicamente; pendente validação manual visual |
| Normalização numérica | Parcial; strike encaminhado, demais campos pendentes |
| Botão atualizar dados | Pendente |
| RTD | Pendente |
| Horário | Pendente |
REVISÃO FUNCIONAL PÓS-USO REAL — FASE 4 — PAYOFF E DECISÕES
Status
Concluída.

A Fase 4 está encerrada funcional e documentalmente, permitindo o avanço para a Fase 5.

Objetivo da fase
Validar se as estruturas criadas manualmente deixam de ser apenas registros visuais e passam a participar corretamente dos fluxos funcionais do sistema, principalmente:

geração de curva de payoff;
gravação de pontos em payoff_curve_points;
participação no fluxo de decisões;
gravação ou justificativa em structure_decisions;
rastreabilidade de estruturas processadas, ignoradas ou rejeitadas.
Contexto
Esta fase faz parte da rota:

NOVA_ROTA_REVISAO_FUNCIONAL_POS_USO_REAL
A revisão foi motivada por comportamento observado durante uso real do sistema, no qual uma estrutura poderia aparecer na interface, mas ainda havia risco de:

não gerar payoff;
não gerar decisão;
não ser considerada pelo pipeline;
ser rejeitada silenciosamente;
possuir legs cadastradas, mas sem dados suficientes para processamento;
apresentar inconsistência de normalização nos pontos de payoff.
Escopo validado
Foram revisados os seguintes pontos:

estrutura principal cadastrada manualmente;
legs vinculadas à estrutura;
relação entre structure_id e registros derivados;
geração de payoff;
gravação de pontos em payoff_curve_points;
integração com fluxo de decisões;
gravação ou justificativa em structure_decisions;
normalização de posição comprada e vendida;
normalização de pontos de payoff, especialmente spot e pl;
critérios para processamento, rejeição ou ignorar estruturas;
presença de diagnóstico para rastrear o comportamento do pipeline.
Diagnóstico realizado
Durante a Fase 4 foi incluído diagnóstico específico para rastrear o caminho funcional entre:

estrutura manual;
legs;
pipeline derivado;
curva de payoff;
pontos de payoff;
decisões;
registros ou justificativas finais.
Commit relacionado:



f9972c2 Adiciona diagnostico fase 4 payoff decisao
Também foi aplicada correção específica na normalização dos pontos de payoff, garantindo maior consistência entre os campos de spot e pl.

Commit relacionado:



c131cb6 Corrige normalizacao de pontos payoff spot pl
Resultado funcional
Após as validações realizadas, foi confirmado que:

estruturas manuais válidas geram curva de payoff;
estruturas manuais válidas participam do fluxo de decisões;
pontos de payoff são gravados ou o motivo de ausência fica rastreável;
decisões são gravadas ou o motivo de ausência fica rastreável;
a normalização de pontos de payoff foi corrigida;
o diagnóstico permite identificar estruturas processadas, ignoradas ou rejeitadas;
a branch permaneceu limpa e sincronizada após o ciclo;
os testes automatizados foram executados com sucesso.
Evidências de validação
Resultado informado no encerramento da fase:



669 testes aprovados
2 testes pulados
Aplicação iniciada sem erro
Working tree limpa
Branch sincronizada com o remoto
Branch utilizada:



reinicio-normalizacao-idioma-ptbr
Critérios de aceite



Critério	Resultado
Estrutura manual válida gera curva de payoff	Atendido
Estrutura manual válida participa do fluxo de decisões	Atendido
payoff_curve_points recebe pontos ou ausência fica rastreável	Atendido
structure_decisions recebe registros ou ausência fica rastreável	Atendido
Pipeline não ignora silenciosamente estruturas manuais válidas	Atendido dentro do escopo da fase
Normalização de pontos de payoff está coerente	Atendido
Diagnóstico permite entender processamento, rejeição ou ausência	Atendido
Testes automatizados permanecem aprovados	Atendido
Aplicação inicia sem erro	Atendido
Branch limpa e sincronizada	Atendido
Decisão
A Fase 4 está concluída.

A estrutura manual válida passa a ser considerada funcionalmente integrada ao fluxo de payoff e decisões.

Não há bloqueio conhecido para avanço à próxima etapa.

Pendências transferidas para a Fase 5
A próxima fase deverá tratar o botão Atualizar Dados e o resumo do pipeline.

Pontos transferidos:

identificar o handler real do botão Atualizar Dados;
verificar quais pipelines são acionados;
informar estruturas lidas;
informar estruturas processadas;
informar estruturas ignoradas;
informar decisões geradas;
informar pontos de payoff gerados;
informar cotações RTD atualizadas;
diferenciar sucesso real de execução sem dados novos;
evitar mensagem genérica de sucesso quando todos os contadores forem zero;
melhorar feedback visual ao usuário;
atualizar a tela após execução bem-sucedida;
registrar avisos e erros de forma rastreável.
Conclusão
A Fase 4 cumpriu seu objetivo.

O sistema agora possui validação funcional e rastreabilidade suficientes para confirmar que estruturas manuais válidas participam dos fluxos de payoff e decisões.

Status final:



Concluída e liberada para Fase 5.
---

## Fase 4 — Payoff e Decisões — Concluída

A Fase 4 foi encerrada funcional e documentalmente.

Foram validados:

- geração de payoff para estruturas manuais válidas;
- participação no fluxo de decisões;
- gravação ou rastreabilidade de pontos de payoff;
- gravação ou rastreabilidade de decisões;
- correção de normalização de pontos de payoff;
- diagnóstico para identificar estruturas processadas, ignoradas ou rejeitadas.

Evidências finais:

    669 testes aprovados
    2 testes pulados
    Aplicação iniciada sem erro
    Working tree limpa
    Branch sincronizada com origin

Próxima fase:

    Fase 5 — Atualizar Dados e Resumo do Pipeline
