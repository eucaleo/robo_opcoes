# Fase 7.3 - Regressao de contratos somente leitura

Data: 13/07/2026

Branch:

    feature/rtd-excel-online-fase6-retencao-limpeza

Base documental anterior:

    Fase 7.1 - Auditoria e rebaseline
    Fase 7.2 - Contrato minimo de decisao e alertas

Commits recentes de referencia:

    32c84ea docs: fecha fase 7.2 de contratos minimos
    e9433a4 docs: classifica contratos minimos da fase 7.2
    1b2b815 docs: ajusta documentos da fase 7 para blocos indentados
    93be050 docs: abre contrato minimo de decisao e alertas da fase 7.2
    9678c2b docs: adiciona auditoria de rebaseline da fase 7.1

## Objetivo da Fase 7.3

A Fase 7.3 tem como objetivo criar uma camada de regressao para proteger os contratos somente leitura identificados na Fase 7.2.

O foco e garantir estabilidade dos seguintes pontos:

    Decisao explicavel.
    Alertas locais.
    Adapter de snapshot.
    Ausencia de execucao real.
    Ausencia de broker.
    Ausencia de roteamento operacional.
    Ausencia de alteracao de banco.

## Escopo permitido

Durante a Fase 7.3, estao permitidas as seguintes atividades:

    Criar testes de regressao.
    Criar testes de contrato.
    Criar documentacao tecnica.
    Consolidar evidencias de comportamento atual.
    Fazer ajustes minimos somente se forem necessarios para preservar contrato existente.

## Escopo bloqueado

Durante a Fase 7.3, continuam bloqueadas as seguintes atividades:

    Implementar envio de ordem real.
    Integrar broker.
    Criar robo executor.
    Criar roteamento operacional.
    Automatizar operacao real.
    Alterar banco de dados.
    Criar dependencia obrigatoria de Excel COM nos testes de contrato.
    Criar dependencia obrigatoria de subprocesso nos testes de contrato.

## Contratos protegidos

### Contrato de decisao

Itens protegidos:

    compute_decision_from_inputs
    compute_decision_from_payoff
    compute_decision_from_contract

Expectativa geral:

    As funcoes devem retornar decisoes explicaveis.
    As funcoes devem preservar justificativas em formato estruturado.
    As funcoes nao devem executar ordens.
    As funcoes nao devem depender de broker.
    As funcoes nao devem alterar banco.

### Contrato de alertas

Itens protegidos:

    SnapshotMercado
    ParametrosAlerta
    avaliar_snapshot

Expectativa geral:

    A avaliacao deve ser local.
    A avaliacao deve ser somente leitura.
    A avaliacao deve produzir alertas explicaveis.
    A avaliacao nao deve enviar ordens.
    A avaliacao nao deve depender de broker.

### Contrato de adapter

Itens protegidos:

    snapshot_mercado_from_rtd_option_quote
    avaliar_rtd_option_quote
    snapshot_mercado_from_leg_market_snapshot

Expectativa geral:

    O adapter deve converter entradas de mercado para snapshot local.
    O adapter deve preservar dados relevantes de timestamp e cotacao.
    O adapter nao deve executar operacao real.
    O adapter nao deve exigir Excel COM para testes de contrato.
    O adapter nao deve alterar banco.

## Plano inicial de regressao

A regressao inicial deve cobrir:

    Testes existentes de decisao.
    Testes existentes de alertas.
    Testes existentes de adapter.
    Teste de ausencia de termos operacionais proibidos nos arquivos focados.
    Teste de estabilidade minima dos campos retornados pelas funcoes de decisao.
    Teste de estabilidade minima da estrutura dos alertas.
    Teste de conversao de snapshot sem dependencia operacional externa.

## Arquivos candidatos para auditoria inicial

Arquivos de dominio e contrato:

    domain/decision.py

Arquivos de testes ja existentes:

    ATT/tests/test_decision.py
    ATT/tests/test_fase7_alertas_decisao.py
    ATT/tests/test_fase7_snapshot_adapter.py

Arquivos de documentacao relacionados:

    docs/fase7_01_auditoria_rebaseline_20260713.md
    docs/fase7_02_contrato_minimo_decisao_alertas_20260713.md
    docs/fase7_03_regressao_contratos_somente_leitura_20260713.md

## Criterios de aceite da Fase 7.3

A Fase 7.3 podera ser considerada concluida quando:

    Houver documento de abertura versionado.
    Houver execucao registrada dos testes existentes relevantes.
    Houver pelo menos uma evidencia de regressao somente leitura.
    Houver confirmacao documental de que nao foi introduzida execucao real.
    Houver confirmacao documental de que nao foi introduzido broker.
    Houver confirmacao documental de que nao foi introduzido roteamento operacional.
    Houver confirmacao documental de que nao foi introduzida alteracao de banco.

## Estado inicial

A Fase 7.3 foi aberta a partir de base limpa apos fechamento formal da Fase 7.2.

Marcador inicial:

    INICIO_FASE7_03_REGRESSAO_CONTRATOS_SOMENTE_LEITURA_20260713


## Evidencia inicial de regressao

Data: 13/07/2026

Comandos executados:

    python -m pytest ATT/tests/test_decision.py ATT/tests/test_fase7_alertas_decisao.py ATT/tests/test_fase7_snapshot_adapter.py -q

    py -m pytest ATT/tests/test_decision.py ATT/tests/test_fase7_alertas_decisao.py ATT/tests/test_fase7_snapshot_adapter.py -q

Resultados observados:

    12 passed in 0.43s
    12 passed in 0.38s

Interpretacao:

    A regressao inicial confirmou estabilidade dos testes existentes de decisao, alertas e adapter.
    A execucao confirmou que os contratos somente leitura seguem consistentes.
    Nao houve indicio de execucao real.
    Nao houve indicio de broker.
    Nao houve indicio de roteamento operacional.
    Nao houve indicio de alteracao de banco.

Conclusao parcial:

    A Fase 7.3 possui evidencia inicial valida de regressao somente leitura.

Marcador:

    EVIDENCIA_INICIAL_REGRESSAO_FASE7_03_20260713


## Evidencia de auditoria textual somente leitura

Data: 13/07/2026

Comando executado:

    grep -RInE "broker|corretora|ordem real|ordem_real|send_order|place_order|execute_order|route_order|roteamento|executor|subprocess|win32com|xlwings|Dispatch|sqlite|postgres|mysql|sqlalchemy|INSERT|UPDATE|DELETE" \
      domain/decision.py \
      ATT/tests/test_decision.py \
      ATT/tests/test_fase7_alertas_decisao.py \
      ATT/tests/test_fase7_snapshot_adapter.py || true

Resultado observado:

    ATT/tests/test_fase7_alertas_decisao.py:110:            "win32com",
    ATT/tests/test_fase7_alertas_decisao.py:112:            "xlwings",
    ATT/tests/test_fase7_alertas_decisao.py:113:            "sqlite3",
    ATT/tests/test_fase7_alertas_decisao.py:114:            "subprocess",
    ATT/tests/test_fase7_snapshot_adapter.py:87:def test_adapter_nao_importa_dependencias_de_excel_com_ou_subprocesso():
    ATT/tests/test_fase7_snapshot_adapter.py:91:        "win32com",
    ATT/tests/test_fase7_snapshot_adapter.py:92:        "xlwings",
    ATT/tests/test_fase7_snapshot_adapter.py:94:        "subprocess",

Classificacao dos achados:

    Achado operacional real: nao
    Falso positivo documental/teste: sim
    Necessita ajuste: nao

Interpretacao:

    As ocorrencias encontradas pertencem aos testes que validam ausencia de dependencias proibidas.
    Nao foi identificado uso operacional real de broker, corretora, envio de ordem, roteamento, subprocesso, Excel COM obrigatorio ou banco de dados.
    A auditoria textual reforca que os contratos avaliados permanecem em modo somente leitura.

Conclusao parcial:

    A Fase 7.3 possui evidencia textual valida de ausencia de integracao operacional real nos arquivos focados.

Marcador:

    EVIDENCIA_AUDITORIA_TEXTUAL_FASE7_03_20260713


## Evidencia de regressao focada da Fase 7.3

Data: 13/07/2026

Comandos executados:

    py -m pytest \
      ATT/tests/test_decision.py \
      ATT/tests/test_fase7_alertas_decisao.py \
      ATT/tests/test_fase7_snapshot_adapter.py \
      -q

    python -m pytest \
      ATT/tests/test_decision.py \
      ATT/tests/test_fase7_alertas_decisao.py \
      ATT/tests/test_fase7_snapshot_adapter.py \
      -q

Resultado observado:

    12 passed in 0.38s
    12 passed in 0.38s

Arquivos cobertos diretamente:

    ATT/tests/test_decision.py
    ATT/tests/test_fase7_alertas_decisao.py
    ATT/tests/test_fase7_snapshot_adapter.py

Classificacao:

    Regressao focada Fase 7.3: aprovada
    Ambientes Python testados: py e python
    Falhas observadas: nenhuma
    Working tree apos execucao: limpo

Interpretacao:

    A regressao focada dos contratos de decisao, alertas e adaptador de snapshot passou integralmente.
    Os testes confirmam que a Fase 7.3 permanece restrita a comportamento de leitura, classificacao, alerta e decisao simulada.
    Nao houve evidencia de envio de ordem real, integracao com broker, persistencia operacional ou dependencia obrigatoria de Excel COM nos contratos focados.

Conclusao parcial:

    A Fase 7.3 possui regressao focada aprovada em ambos os comandos Python utilizados no ambiente local.

Marcador:

    EVIDENCIA_REGRESSAO_FOCADA_FASE7_03_20260713

## Observacao sobre regressao ampliada da pasta ATT/tests

Data: 13/07/2026

Comandos executados:

    py -m pytest ATT/tests -q
    python -m pytest ATT/tests -q

Resultado observado:

    2 failed, 899 passed, 2 skipped, 6 subtests passed
    2 failed, 899 passed, 2 skipped, 6 subtests passed

Falhas observadas:

    ATT/tests/test_repository_generated_artifacts_guardrail.py::test_generated_rtd_output_artifacts_are_not_tracked
    ATT/tests/test_ui_modern_dark_window_excel_rtd_status_menu.py::test_operational_dark_window_help_menu_and_live_excel_rtd_status

Classificacao das falhas:

    Falha 1:
        Tipo: higiene de repositorio / artefatos gerados rastreados
        Relacao direta com contrato Fase 7.3: nao evidenciada
        Primeiro item observado: FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_10_manifesto_ids_elegiveis_20260713.json

    Falha 2:
        Tipo: dependencia ambiental operacional Excel COM / RTD
        Relacao direta com contrato Fase 7.3: nao evidenciada
        Mensagem observada: Excel nao encontrado
        Condicao necessaria: Excel aberto com workbook LISTA_RTD.xlsm e aba RTD_OPTION_QUOTES

Interpretacao:

    A regressao ampliada da pasta ATT/tests nao ficou verde globalmente.
    As duas falhas observadas nao indicam regressao direta nos contratos focados da Fase 7.3.
    Uma falha aponta para artefatos gerados rastreados no repositorio.
    A outra falha depende de ambiente operacional real com Excel COM e RTD ativos.

Conclusao parcial:

    A regressao ampliada foi executada e documentada com falhas externas ao escopo direto da Fase 7.3.
    O sucesso da regressao focada permanece valido para os contratos de decisao, alertas e snapshot adapter.

Marcador:

    EVIDENCIA_REGRESSAO_AMPLIADA_COM_FALHAS_EXTERNAS_FASE7_03_20260713

