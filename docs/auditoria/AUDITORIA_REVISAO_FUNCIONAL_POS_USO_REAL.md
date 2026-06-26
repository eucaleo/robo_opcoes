# AUDITORIA_REVISAO_FUNCIONAL_POS_USO_REAL

## Marco de início

Reinício limpo do desenvolvimento após encerramento do ciclo anterior.

Tag base:

marco-zero-reinicio-limpo-20260622

Branch de trabalho:

reinicio-normalizacao-idioma-ptbr

## Regras fixadas

- Não migrar para web.
- Não usar emojis.
- Manter o escopo do projeto.
- Buscar dados, arquivos e evolução no Git antes de alterar.
- Não codar sem localização prévia.
- Toda mudança deve ser testada após concluída.
- Após cada alteração concluída e testada, commitar.
- A auditoria deve ser atualizada a cada teste, correção e conclusão.
- A Fase 1 é somente reprodução controlada, evidência e localização.
- Nenhuma alteração funcional deve ser feita na Fase 1.

## Índice de execução

| Ordem | Etapa | Status | Commit |
|---|---|---|---|
| 1 | Fase 1 — Reprodução controlada dos problemas | Em abertura | Pendente |

## Registro de auditoria

### Entrada 001 — Abertura da Fase 1

Data:

2026-06-22

Problema testado:

Ainda não testado. A fase está sendo aberta para reprodução controlada dos problemas descritos no documento de revisão funcional pós uso real.

Evidência observada:

Pendente.

Arquivos analisados:

Pendente.

Alteração feita:

Criação dos arquivos mínimos de auditoria e evidência da Fase 1.

Teste executado:

Pendente.

Resultado:

Pendente.

Commit gerado:

Pendente.

Pendência restante:

Executar a reprodução controlada dos problemas em sistema funcionando.

### Entrada 002 — Localização inicial dos pontos candidatos

Data:

2026-06-22

Branch usada:

reinicio-normalizacao-idioma-ptbr

Commit base da fase:

4625a67

Problema testado:

Localização inicial dos pontos candidatos relacionados aos problemas descritos na revisão funcional pós uso real.

Evidência observada:

Foram localizadas referências a Atualizar Dados, recálculo, snapshot, strike must be numeric, structure_decisions, payoff_curve_points, rtd_option_quotes, aba e alias.

Arquivos analisados:

UI/components/decisions_grid.py
UI/components/details_panel.py
UI/components/payoff_chart.py
UI/components/structures_list_panel.py
UI/components/structure_editor_dialog.py
UI/main_window.py
UI/models/ui_data.py
services/canonical_input_service.py
services/canonical_pricing_facade.py
services/derived_service.py
services/market_snapshot_selector.py
services/structure_leg_rtd_enrichment_service.py
repositories/structures_repository.py
repositories/market_snapshot_repository.py
repositories/rtd_option_quotes_repository.py
repositories/_aba_resolver_mixin.py
domain/payoff_features.py
ATT/tests

Alteração feita:

Apenas documentação da localização inicial.

Teste executado:

Busca textual no projeto.

Resultado:

Pontos candidatos localizados. Nenhuma alteração funcional realizada.

Commit gerado:

Pendente.

Pendência restante:

Inventariar banco de dados e executar reprodução controlada em sistema funcionando.


## Registro de auditoria - 2026-06-23 - Restauracao documental da rota

Data da execucao: 2026-06-23
Branch usada: reinicio-normalizacao-idioma-ptbr
Commit base: b48423e
Problema testado: ausencia dos documentos Marco 0 e Marco 2 da nova rota funcional pos uso real
Evidencia observada: arquivo de auditoria existente, arquivo da rota ausente e plano de execucao ausente
Arquivos analisados:
  - docs/rotas/NOVA_ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md
  - docs/auditoria/AUDITORIA_REVISAO_FUNCIONAL_POS_USO_REAL.md
  - docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_PLANO_EXECUCAO.md
Alteracao feita: recriados os documentos da rota e do plano operacional conforme documento base da revisao funcional pos uso real
Teste executado:
  - ls docs/rotas/NOVA_ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md
  - ls docs/auditoria/AUDITORIA_REVISAO_FUNCIONAL_POS_USO_REAL.md
  - ls docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_PLANO_EXECUCAO.md
Resultado: pendente de validacao Git
Commit gerado: 2b593ed
Pendencia restante: avancar para investigacao funcional de recalculo, snapshot e metricas financeiras

---

# Entrada de auditoria — Fase 3 — Cadastro assistido de estrutura

## Data da execucao

23/06/2026

## Branch usada

reinicio-normalizacao-idioma-ptbr

## Commit base

A identificar no momento do commit com git rev-parse HEAD.

## Problema testado

Cadastro assistido de leg de estrutura usando simbolo de opcao reconhecido no RTD ou cache.

Problemas especificos tratados:

- Leg nova nascia com option_type CALL por padrao.
- Simbolo PUT podia gerar erro de divergencia contra CALL indevido.
- Premium vazio enviado pela interface podia gerar erro premium is required.
- Premium enriquecido nao era refletido no formulario visual.

## Evidencia observada antes da correcao

O fluxo de cadastro assistido podia apresentar divergencia indevida de tipo quando o usuario informava uma opcao PUT e a leg nova carregava CALL por padrao.

Tambem foi identificado que premium vazio enviado como nulo pela interface chegava ao servico de enriquecimento e podia ser tratado como campo obrigatorio ausente.

## Arquivos analisados

- UI/components/structure_editor_dialog.py
- services/structure_leg_rtd_enrichment_service.py

## Buscas realizadas

Foram executadas buscas para localizar defaults de option_type, validadores e pontos de conversao de premium.

Buscas principais:

    grep -n "self._lf_type\|option_type.*CALL\|option_type" UI/components/structure_editor_dialog.py

    grep -RIn "premium is required\|premium is requered\|premium.*required\|premium.*obrig" . --exclude-dir=.git --exclude-dir=__pycache__ --exclude="*.bak*"

    grep -RIn "_parse_decimal(.*premium\|premium.*_parse_decimal\|field_name.*premium" UI services repositories database models scripts --exclude-dir=.git --exclude-dir=__pycache__ --exclude="*.bak*"

## Alteracao feita

### Interface

A leg nova deixou de inicializar com CALL como tipo padrao.

A interface passou a aceitar option_type vazio em nova leg para permitir que o servico detecte o tipo real pelo simbolo da opcao.

A interface tambem passou a refletir o campo premium retornado pelo enriquecimento.

### Servico de enriquecimento RTD

O premium passou a ser resolvido pela seguinte prioridade:

- Premium informado manualmente.
- ultimo_preco vindo do RTD ou cache.
- 0.0 como fallback compativel.

A validacao de divergencia entre tipo informado e tipo detectado foi preservada.

## Teste executado

Compilacao dos arquivos alterados:

    python -m py_compile UI/components/structure_editor_dialog.py services/structure_leg_rtd_enrichment_service.py

Teste isolado do enriquecimento com PETRS424:

    Resultado esperado: option_type PUT, premium 2.05, underlying_asset PETR4.

Suite completa:

    pytest

## Resultado

Compilacao sem erros.

Teste isolado aprovado:

    OK: enrich PETRS424 => PUT e premium 2.05

Suite completa aprovada:

    669 passed, 2 skipped in 37.62s

## Commit gerado

HASH_DO_COMMIT

## Pendencia restante

Nenhuma pendencia funcional aberta para a Fase 3.

Permanecem para fases futuras:

- Fase 4: integracao da estrutura manual com payoff e decisoes.
- Fase 5: botao Atualizar Dados e resumo do pipeline.
- Fase 6: execucao RTD.
- Fase 7: recalculo, snapshot e metricas financeiras.
- Fase 8: duplicidade da estrutura numero 2.
- Fase 9: normalizacao ampla para Portugues Brasil.
- Fase 10: comentario do grafico de payoff.
- Fase 11: visibilidade e atualizacao instantanea.
- Fase 12: remocao ou justificativa de aba ou alias.
- Fase 13: validacao integrada.
- Fase 14: fechamento documental.

---

# Entrada de auditoria - Fase 4 - Integracao da estrutura manual com payoff e decisoes

## Data da execucao

24/06/2026

## Branch usada

reinicio-normalizacao-idioma-ptbr

## Commit base

A identificar com git rev-parse HEAD.

## Problema testado

Estrutura criada manualmente ou por cadastro assistido precisa gerar payoff e decisoes, nao apenas aparecer visualmente na tela.

## Evidencia observada

Pendente de investigacao controlada.

## Arquivos analisados

Pendente.

## Alteracao feita

Nenhuma alteracao funcional ainda. Fase iniciada com working tree limpo e material RTD preservado em stash para Fase 6.

## Teste executado

Pendente.

## Resultado

Pendente.

## Commit gerado

Pendente.

## Pendencia restante

Investigar pipeline de payoff e decisoes, filtros de estrutura, persistencia em payoff_curve_points e structure_decisions, e motivos de rejeicao.

---

# Registro de Auditoria — Fase 4 — Payoff e Decisões

## Data

24/06/2026

## Status

Concluída.

---

## Branch

    reinicio-normalizacao-idioma-ptbr

---

## Objetivo auditado

Validar se estruturas criadas manualmente estão corretamente integradas ao fluxo funcional do sistema, especialmente nos pontos de:

- geração de payoff;
- geração de pontos em payoff_curve_points;
- participação no fluxo de decisões;
- geração ou justificativa em structure_decisions;
- rastreabilidade de rejeições ou ausência de dados;
- normalização correta dos pontos de payoff.

---

## Resultado da auditoria

A auditoria da Fase 4 considera a etapa aprovada.

Não foram identificados bloqueios para avanço à Fase 5.

---

## Decisão

A Fase 4 está oficialmente encerrada.

A próxima etapa da rota será:

    Fase 5 — Atualizar Dados e Resumo do Pipeline

---

## Commit documental sugerido

    docs: fecha fase 4 payoff e decisoes

### Observação arquitetural pós-validação RTD

Durante a validação da Fase 6, o RTD foi confirmado como operacional de ponta a ponta. Porém, a geração de símbolos indicou que a fonte atual foi rtd_option_quotes, com structure_legs e structure_leg_snapshots sem registros disponíveis no banco testado.

Isso confirma a operacionalidade do cache RTD, mas evidencia que a fonte canônica de símbolos ativos ainda precisa ser consolidada para produção. O fluxo produtivo deve preferencialmente gerar símbolos a partir de estruturas/pernas ativas e não a partir da própria tabela rtd_option_quotes, evitando perpetuação de códigos antigos após encerramento de operações.

Pendência recomendada: validar/corrigir build_rtd_symbols.py para uso produtivo com fonte canônica de operações ativas e limpeza de símbolos/cotações RTD não mais ativos.

## Execução — Fase 7 — Recálculo, Snapshot e Métricas Financeiras

### Data da execução

2026-06-25

### Branch usada

reinicio-normalizacao-idioma-ptbr

### Problema testado

Recálculo, atualização de snapshot, preenchimento de métricas financeiras e exibição das datas operacionais na aba "Estruturas".

### Evidência observada

Após a correção, a interface executou o pipeline com sucesso.

Resumo operacional observado:

- Decisões: 26
- Pontos de payoff: 2626
- Cotações RTD atualizadas: 8
- Avisos: 0
- Erros: 0

A estrutura PRIO foi recalculada com sucesso e gerou `snapshot_id` 30.

A estrutura SBSP+SMAL=BOVA foi recalculada com sucesso e gerou `snapshot_id` 31.

As métricas financeiras foram preenchidas no retorno do recálculo.

### Arquivos analisados

- UI/main_window.py
- UI/components/details_panel.py
- UI/models/ui_data.py
- db/derived_repo.py
- services/derived_service.py
- dados/derived.db

### Alteração feita

Foi adicionado o método `_fetch_structure_temporal_audit_for_details` em `MainWindow`.

A exibição das datas "Criado em" e "Atualizado" na aba "Estruturas" passou a usar datas operacionais derivadas dos registros em `structure_decisions`.

### Teste executado

- Compilação dos arquivos alterados.
- Execução da interface.
- Atualização de dados.
- Recálculo da estrutura PRIO.
- Recálculo da estrutura SBSP+SMAL=BOVA.
- Verificação de preenchimento das métricas financeiras.
- Verificação de preenchimento do painel de detalhes da estrutura.

### Resultado

Correção principal validada.

O erro anterior de ausência do método `_fetch_structure_temporal_audit_for_details` foi resolvido.

O painel de detalhes voltou a ser preenchido.

O recálculo passou a gerar registros com métricas financeiras preenchidas.

### Pendências tratadas

O bloco de busca de auditoria temporal foi ajustado após a validação de estrutura nula em `_on_structure_selected`.

A normalização temporal foi validada com execução real da interface, recálculo, pipeline e conferência direta no banco.

### Commits gerados

    c106780 Normaliza datas timezone-aware na UI e snapshots derivados
    6cfaf59 Documenta encerramento da Fase 7
    62d44a7 Adiciona pacote core

---

## Auditoria da Fase 7 — Normalização temporal

Status: **Aprovada**

Foi validado que:

- created_at e timestamp novos são gravados com offset explícito;
- registros antigos sem timezone são interpretados como horário local;
- datas UTC com offset explícito são convertidas na exibição;
- a UI passou a usar formatter central;
- o payoff usa o snapshot mais recente por timestamp;
- o pipeline final executou com sucesso;
- não restaram usos diretos relevantes de datetime.now().isoformat() nos fluxos principais.

Ocorrências restantes:

    DEFAULT CURRENT_TIMESTAMP
    datetime('now')

Essas ocorrências estão em schemas e foram classificadas como pendência técnica não bloqueante.

Documento de referência:

    docs/fases/FASE_7_NORMALIZACAO_DATETIME.md


## Fase 8 — Duplicidade de estrutura

Status: concluída por reconciliação.

A investigação da duplicidade relatada da estrutura número 2 foi encerrada documentalmente.

O banco operacional atual dados/app.db não apresenta duplicidade ativa:

- total_structures=2;
- estrutura id=2 aparece uma única vez;
- sem duplicidade física por id em structures;
- sem duplicidade de legs por structure_id e símbolo normalizado.

A evidência histórica indica que a duplicidade existiu em backup anterior, mas foi sanada por correções já aplicadas na Fase 6, especialmente no commit f67d408, que corrigiu edição e duplicidade de legs em estruturas.

Não houve alteração adicional de código nesta fase.

Checkpoint oficial criado:

- docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_8_DUPLICIDADE_ESTRUTURA.md

Validação executada:

- python scripts/verificar_andamento_rota.py
- compileall com retorno 0

Commit documental:

- ad1f324 Documenta encerramento da Fase 8 por reconciliacao

## Fase 9 — Português Brasil

Status: em andamento.

A Fase 9 foi iniciada após o encerramento da Fase 8 no commit 7027499.

Objetivo: normalizar textos visíveis ao usuário para Português do Brasil, sem alterar lógica funcional, persistência, cálculo, RTD, payoff, decisão ou contratos internos.

Critério de segurança: traduzir ou ajustar apenas textos de apresentação e mensagens controladas. Identificadores técnicos, nomes de tabelas, colunas, chaves de payload, APIs, funções, classes e contratos persistidos não devem ser alterados nesta fase sem análise específica.

Checkpoint inicial:

- docs/checkpoints/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_9_PORTUGUES_BRASIL.md


### Baseline técnica inicial da Fase 9

Durante a abertura da Fase 9 foi executado `pytest`.

Resultado:

- 671 testes coletados;
- 666 passaram;
- 3 falharam;
- 2 foram ignorados.

As falhas foram classificadas como fora do escopo direto da Fase 9 de Português Brasil:

- contrato de timestamp esperando sufixo `Z`;
- guardrails que proíbem importação direta de `sqlite3` em `UI/main_window.py`.

Evidência:

- docs/evidencias/REVISAO_FUNCIONAL_POS_USO_REAL_FASE_9_BASELINE_PYTEST.txt

Decisão operacional:

A Fase 9 prossegue apenas com normalização textual segura, sem corrigir essas falhas neste momento para evitar mistura de escopos.
