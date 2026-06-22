# Auditoria - Revisao Funcional Pos Uso Real

Documento de acompanhamento da evolucao da revisao funcional pos uso real.

## Regras operacionais

- Banco de dados e fonte da verdade.
- Excel apenas como ponte RTD.
- UI nao deve depender de CSVs derivados antigos.
- Toda alteracao deve ser precedida de busca em arquivos e dados.
- Toda alteracao deve ser testada.
- Toda fase encerrada deve atualizar evidencias em docs.
- Toda alteracao concluida e testada deve ser commitada.


## Fase 3F - Diagnostico payoff estrutura manual canonica

Data: Sun Jun 21 21:55:36     2026

Branch: fase-3a4-auto-pricing-manual-save

Commit base: 8550c20

Objetivo:
Identificar por que a estrutura manual canonica structure_id=2 ainda nao gera pontos em payoff_curve_points.

Evidencia gerada:
docs/checkpoints/evidencias/fase-3f-diagnostico-payoff-manual-canonico.txt

Status:
Diagnostico executado. Aguardando analise da evidencia para definir correcao.


## Fase 3F Fix1 - Inspecao contrato payoff

Data: Sun Jun 21 21:57:17     2026

Branch: fase-3a4-auto-pricing-manual-save

Commit base: 8550c20

Objetivo:
Inspecionar schema de payoff_curve_points, codigo da CanonicalPricingFacade e referencias existentes antes de implementar geracao de payoff canonico.

Evidencia gerada:
docs/checkpoints/evidencias/fase-3f-fix1-inspecao-contrato-payoff.txt

Status:
Inspecao executada. Proxima etapa: implementar geracao e persistencia de pontos de payoff para estrutura manual canonica.


## Fase 3F Fix1 - Diagnostico compute payoff

Data: Sun Jun 21 22:01:27     2026

Branch: fase-3a4-auto-pricing-manual-save

Commit base: 8550c20

Objetivo:
Executar isoladamente PricingInputService, DerivedPayoffPersistence._build_canonical_input(),
compute_payoff_from_canonical_input() e DerivedPayoffPersistence.persist() para identificar
onde a geração/persistência do payoff falha.

Evidencia gerada:
docs/checkpoints/evidencias/fase-3f-fix1-diagnostico-compute-payoff.txt

Status:
Diagnostico executado. Proxima etapa: patch corretivo no contrato de payoff.


## Fase 3F Fix1 - Diagnostico compute payoff V2

Data: Sun Jun 21 22:04:41     2026

Branch: fase-3a4-auto-pricing-manual-save

Commit base: 8550c20

Objetivo:
Reexecutar o diagnostico isolado usando fallback de construtor do PricingInputService,
igual ao comportamento da CanonicalPricingFacade.

Evidencia gerada:
docs/checkpoints/evidencias/fase-3f-fix1-diagnostico-compute-payoff-v2.txt

Status:
Diagnostico V2 executado. Proxima etapa: patch corretivo no contrato de payoff, se necessario.


## Fase 3F Fix1 - Diagnostico compute payoff V2

Data: Sun Jun 21 22:08:20     2026

Branch: fase-3a4-auto-pricing-manual-save

Commit base: 8550c20

Objetivo:
Reexecutar o diagnostico isolado usando fallback de construtor do PricingInputService,
igual ao comportamento da CanonicalPricingFacade.

Evidencia gerada:
docs/checkpoints/evidencias/fase-3f-fix1-diagnostico-compute-payoff-v2.txt

Status:
Diagnostico V2 executado. Proxima etapa: patch corretivo no contrato de payoff, se necessario.


## Fase 3F Fix1 - Evidencia final

Data: Sun Jun 21 22:09:27     2026

Branch: fase-3a4-auto-pricing-manual-save

Commit base: 8550c20

Correção aplicada:
Normalização das legs em services/derived_payoff_persistence.py para preencher
position_side a partir de side antes de chamar domain.compute_payoff_from_canonical_input().

Motivo:
O payoff canônico validava structure.legs[n].position_side como obrigatório, enquanto
payloads manuais gerados pela UI vinham com side=LONG/SHORT.

Evidencia gerada:
docs/checkpoints/evidencias/fase-3f-fix1-evidencia-final.txt

Status:
Patch aplicado e validado por diagnóstico de geração/persistência de payoff.


## Fase 4 - Diagnostico Atualizar Dados

Data: Sun Jun 21 22:14:57     2026

Branch: fase-3a4-auto-pricing-manual-save

Commit base: a1088b3

Objetivo:
Localizar handler do botao Atualizar dados, servicos de pipeline chamados,
feedback atual exibido ao usuario e pontos onde inserir resumo rastreavel.

Evidencia gerada:
docs/checkpoints/evidencias/fase-4-diagnostico-atualizar-dados.txt

Status:
Diagnostico iniciado. Nenhuma alteracao funcional aplicada nesta etapa.


## Fase 4 Fix1 - Feedback operacional do pipeline

Foi identificado que o menu **Arquivo > Atualizar Dados** apenas recarrega os dados já persistidos na UI por meio de `refresh_data()`, sem executar o pipeline.

O menu **Ferramentas > Executar Pipeline** executa `scripts/run_derived_pipeline.py`. Antes do ajuste, o retorno visual era genérico: "Pipeline executado com sucesso!".

Ajustes realizados:

- `scripts/run_derived_pipeline.py` agora emite um resumo operacional em stdout.
- O resumo inclui contagens disponíveis no `derived.db`, como decisões e pontos de payoff.
- O script também emite uma linha parseável com o marcador `[PIPELINE_SUMMARY_JSON]`.
- `UI/main_window.py` passou a extrair esse JSON e montar uma mensagem amigável no `messagebox`.
- A status bar passou a receber um resumo curto após a execução do pipeline.
- `Atualizar Dados` permanece limitado ao refresh da UI, preservando separação de responsabilidades.

Validações:

- `python -m py_compile UI/main_window.py scripts/run_derived_pipeline.py`
- `python scripts/run_derived_pipeline.py --no-cleanup`
- `git diff --check`

Resultado esperado na UI:

- Popup com resumo operacional do pipeline.
- Status bar com decisões, pontos de payoff e erros.
