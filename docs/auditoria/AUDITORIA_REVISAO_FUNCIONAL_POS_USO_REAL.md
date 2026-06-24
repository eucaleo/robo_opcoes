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
