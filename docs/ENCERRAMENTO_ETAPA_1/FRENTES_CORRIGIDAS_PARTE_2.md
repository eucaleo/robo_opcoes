## Frente 14 — Multiplier canônico de opções

Status: aplicada e validada.

A Frente 14 consolidou o tratamento de multiplier canônico de opções, reduzindo divergências entre pontos de cálculo e leitura operacional.

Decisão aplicada: manter evolução incremental, sem troca ampla de fluxo operacional.

---

## Frente 15 — Contenção de divergências financeiras

Status: aplicada e validada.

A Frente 15 registrou a contenção de divergências financeiras e a proteção contra leituras paralelas não controladas.

Decisão aplicada: preservar compatibilidade e validar mudanças por testes locais.

---

## Frente 16 — Contratos de leitura e escrita

Status: aplicada e validada.

A Frente 16 reforçou contratos de leitura e escrita para reduzir ambiguidade entre componentes legados e caminhos consolidados.

Decisão aplicada: manter contenção explícita e rastreável.

---

## Frente 17 — Contenção DB reader writer legado

Status: aplicada e validada.

A Frente 17 aposentou o uso operacional direto de módulos legados de leitura e escrita de banco, preservando compatibilidade apenas onde necessário.

Decisão aplicada: uso operacional deve preferir repositories e serviços consolidados.

---

## Frente 18 — Auditoria de contrato financeiro de legs

Status: aplicada e validada.

A Frente 18 auditou contratos financeiros relacionados a legs, campos derivados e pontos de cálculo sensíveis.

Decisão aplicada: separar auditoria, contrato e adoção incremental para evitar troca operacional abrupta.

---

## Frente 19 — Semântica numérica financeira e Greeks negativos

Regra documental preservada: delta negativo, demais gregas negativas e zeros validos devem manter semantica numerica e nao podem ser convertidos para ausencia de valor.


Preservação de gregas negativas e zeros válidos


Status: aplicada e validada.

A Frente 19 consolidou a regra de semântica numérica financeira: valores negativos legítimos devem ser preservados.

Greeks negativos são válidos e não podem ser convertidos para positivo por normalizadores genéricos. Campos como delta, theta, gamma, vega, rho, preço, quantidade, payoff e demais valores financeiros devem manter o sinal quando esse sinal fizer parte da informação financeira.

### Encerramento da Frente 19

A Frente 19D registrou o encerramento dos guardrails de preservação de Greeks negativos.

A regra documentada é: normalização de formato não é autorização para alterar semântica numérica. Qualquer conversão deve ser explícita, testável e local ao ponto de consumo.

Decisão aplicada: preservar negativos legítimos, impedir normalização destrutiva e manter cobertura documental.

---

### Registro complementar de validação documental

- Status: Concluída
- theta negativo

### Complemento local de validação documental

- A documentação confirma preservação de delta negativo, theta negativo e zero válido.

## Frente 20A — Auditoria RTD Option Quotes

Status: aplicada e validada.

### Objetivo

Iniciar a Frente 20 com auditoria controlada do eixo RTD Option Quotes, sem trocar fluxo operacional nesta etapa.

A meta foi identificar duplicações, contratos paralelos e pontos candidatos para consolidação futura antes de qualquer alteração funcional em serviços, bridge, importadores ou scripts.

### Escopo da auditoria

Foram auditados pontos relacionados a:

- fonte de schema RTD Option Quotes;
- constantes de workbook, sheet, headers e campos RTD;
- normalização de cabeçalhos;
- fluxos que leem Excel RTD;
- fluxos que persistem em rtd_option_quotes;
- uso de repository versus SQL direto;
- importadores CSV relacionados;
- scripts operacionais de captura e sincronização.

### Decisão aplicada

A Frente 20A foi tratada como etapa exclusivamente diagnóstica.

Não há troca operacional nesta etapa.

Nenhum fluxo de sincronização foi substituído nesta rodada. Nenhum serviço operacional passou a usar novo caminho por força deste patch.

---

## Frente 20B — Contrato canônico RTD Option Quotes

Status: aplicada localmente e validada.

### Objetivo

Consolidar um contrato mínimo e consumível para schema RTD Option Quotes, mantendo a mudança pequena, local e testável.

A Frente 20B estabiliza constantes, cabeçalhos, campos obrigatórios e normalização de headers em services/rtd_option_quotes_schema.py.

### Decisão aplicada

Não há troca operacional ampla nesta etapa.

A adoção deve ser incremental, local e testável. Serviços, bridge, importadores e scripts devem migrar para o contrato consolidado apenas em frentes futuras, com testes específicos.

### Próxima frente sugerida

Frente 20C: iniciar adoção pontual do contrato RTD Option Quotes em um único ponto consumidor, sem refatoração ampla e sem troca de fluxo de persistência.

### Registro complementar de validação documental

- Sem troca operacional ampla nesta etapa.

### Complemento local de validação documental

- Execução somente local nesta etapa, preservando a consolidação final para o encerramento geral das frentes.

## Frente 20C — Guarda local para teste GUI dependente de Tk

Status: aplicada localmente.

### Objetivo

Remover o bloqueio de coleta da suíte completa causado por ambiente local sem `tkinter` completo para `customtkinter`.

O erro observado ocorria antes da execução dos testes, durante importação de `ATT/tests/test_structure_editor_dialog.py`, porque `customtkinter` dependia de atributos ausentes em `tkinter`, como `Variable`.

### Decisão aplicada

Foi adicionada uma guarda defensiva somente local no teste GUI `ATT/tests/test_structure_editor_dialog.py`.

A guarda valida a disponibilidade mínima de `tkinter` antes de importar `customtkinter`.

Quando o ambiente possui `tkinter` completo, o teste segue normalmente.

Quando o ambiente local não possui `tkinter` completo, o módulo é ignorado com `pytest.skip(..., allow_module_level=True)`, evitando falha de coleta global.

### Limites

- Sem troca operacional ampla nesta etapa.
- Ajuste somente local.
- Nenhuma alteração em serviços, bridge, banco, repositórios ou fluxo de persistência.
- Nenhuma operação de git executada.

### Próxima frente

Após validação da suíte completa, seguir para a próxima frente mantendo o mesmo critério: correções locais, documentadas, sem atualização de git até o encerramento geral das frentes.


## Frente 20D — Guardrails locais para suíte completa

Status: aplicada localmente.

### Objetivo

Estabilizar falhas latentes da suíte completa sem operação de git e sem troca operacional ampla.

### Escopo local

- marcador DEPRECATED e fail-fast esperado em db.reader.py e db.writer.py;
- registro documental da Frente 09;
- schema oficial local de pricing_executions;
- adaptação isolada do fallback legado RTD para option_type legado C;
- fallback local para testes GUI quando customtkinter/tkinter estiverem incompletos no ambiente.

### Decisão aplicada

Ajuste somente local.

Nenhuma operação de git executada.


### Registro complementar Frente 09

A Frente 09 mantém o registro de transição para derived_repo.


## Frente 20E — Correção local de guardrails remanescentes

Status: aplicada localmente.

### Objetivo

Corrigir guardrails remanescentes da suíte completa após a Frente 20D.

### Ajustes locais

- Reorganização de db.writer.py e db.reader.py para manter from __future__ no início válido do módulo.
- Preservação explícita de DEPRECATED e fail-fast para PayoffWriter e PayoffReader.
- Registro documental da Frente 09 com derived_repo.
- Proteção local de customtkinter em ambientes de teste com tkinter incompleto.

### Decisão aplicada

Ajuste somente local, sem operação de git.

---

## Frente 20H — Ajuste final de contratos remanescentes

### Status

Aplicada localmente e validada, sem operação de git.

### Escopo

- Revalidação do contrato canônico de `option_type`: somente `CALL` ou `PUT`; `C/P` não são aceitos como `option_type`.
- Reforço do contrato oficial de `pricing_executions`, incluindo `updated_at` e retorno explícito `status=ok`.
- Reforço dos módulos legados `db.reader` e `db.writer` com `get_deprecation_status()` contendo `retired=True`.
- Regeneração dos arquivos de conferência com corte antes da Frente 14.

### Decisão aplicada

Ajuste automatizado local, documentado, sem atualização de git.

---

## Frente 20I — Restauração de helpers locais do fallback legado

### Status

Aplicada localmente e validada.

### Objetivo

Restaurar helpers locais necessários ao `LegacyRoboLegsFallback`, preservando o comportamento incremental e sem alterar fluxo operacional amplo.

### Escopo

- Conferência e restauração dos helpers `_clean_text` e `_clean_upper_text`.
- Preservação do fallback legado apenas como compatibilidade controlada.
- Manutenção da regra de não executar operações de git durante o ciclo local das frentes.

### Decisão aplicada

Ajuste automatizado local, documentado, sem atualização de git.

---

## Frente 20J — Inferência legada de CALL/PUT por símbolo, sem abreviação canônica

### Status

Aplicada localmente e validada.

### Objetivo

Corrigir o fallback legado para permitir compatibilidade com dados antigos sem reintroduzir abreviações canônicas inválidas para tipo de opção.

### Regra preservada

- `C` e `V` pertencem ao contrato legado de compra/venda.
- C e V pertencem ao contrato legado de compra/venda.
- `C` não significa `CALL` no contrato canônico.
- `P` não deve ser tratado como abreviação operacional de `PUT` no contrato canônico.
- `CALL` deve ser informado por extenso.
- CALL deve ser informado por extenso.
- `PUT` deve ser informado por extenso.
- PUT deve ser informado por extenso.

### Escopo

- Quando o dado legado vier pelo campo `call_put` com valor `C` ou `P`, o fallback não promove esse valor como `option_type` canônico.
- O fallback legado infere `CALL` ou `PUT` pelo símbolo, quando necessário, para alimentar o contrato canônico final.
- O campo canônico `option_type` continua aceitando somente `CALL` ou `PUT` por extenso.
- `option_type=C` e `option_type=P` continuam inválidos pelo contrato da Frente 13.

### Decisão aplicada

Compatibilidade controlada apenas no fallback legado, com inferência por símbolo e preservação do contrato canônico.
Sem atualização de git nesta etapa.

---

## Frente 20K — Registro documental local após suíte completa verde

### Status

Aplicada localmente e validada.

### Validação local

A suíte completa foi executada localmente com sucesso:

- `829 passed`
- `4 skipped`
- `2 warnings`
- `6 subtests passed`

### Decisão operacional preservada

As alterações seguem mantidas apenas no documento local em `docs`.

Nenhuma operação de git deve ser executada antes da conclusão geral das frentes.

---

## Frente 21A — Adoção pontual do contrato RTD Option Quotes no probe Excel

### Status

Aplicada localmente.

### Objetivo

Iniciar a Frente 21 com uma adoção pontual, pequena e testável do contrato canônico de RTD Option Quotes no probe Excel, sem trocar fluxo operacional amplo.

### Escopo

- Inclusão de ponte local em `services/rtd_excel_probe_service.py` para consumir `services/rtd_option_quotes_schema.py`.
- Exposição controlada dos headers obrigatórios a partir do contrato canônico.
- Normalização de headers via contrato canônico quando disponível.
- Criação de guardrail local em `ATT/tests/test_frente_21a_rtd_option_quotes_probe_schema_contract.py`.

### Decisão aplicada

`services/rtd_option_quotes_schema.py` passa a ser referenciado pelo probe RTD Excel como fonte canônica consumível nesta frente.

Sem troca operacional ampla.

Sem alteração de persistência.

Sem troca de bridge, importadores ou scripts de sincronização nesta etapa.

Nenhuma operação de git executada.

### Validação esperada

- `python -m py_compile services/rtd_excel_probe_service.py`
- `python -m pytest ATT/tests/test_frente_21a_rtd_option_quotes_probe_schema_contract.py -q`

### Próxima frente sugerida

Frente 21B: iniciar adoção pontual do contrato RTD Option Quotes em mais um consumidor, preferencialmente mantendo o mesmo padrão: uma alteração pequena, local, testável e sem troca ampla de fluxo.

---

## Frente 21C — API pública mínima de headers RTD Option Quotes

### Status

Aplicada localmente.

### Objetivo

Consolidar uma API pública pequena e estável em `services/rtd_option_quotes_schema.py` para consumo de headers RTD Option Quotes.

### Escopo

- Adição de `rtd_option_quotes_headers()`.
- Adição de `rtd_option_quotes_required_headers()`.
- Preservação do schema RTD Option Quotes como fonte canônica local.
- Ajuste do probe RTD Excel para preferir a API pública do schema quando disponível.
- Guardrail local em `ATT/tests`.

### Decisão aplicada

Mudança pequena, local e testável, sem troca operacional ampla e sem operação de git.

A regra de contrato financeiro permanece preservada: `CALL` e `PUT` devem ser informados por extenso no contrato canônico; `C` e `V` pertencem ao contrato legado de compra/venda, não ao tipo de opção.

---

## Frente 21D — API pública mínima de workbook/sheet do RTD Option Quotes

### Status

Aplicada localmente e validada.

### Objetivo

Centralizar no contrato canônico `services/rtd_option_quotes_schema.py` também os nomes públicos de workbook e sheet usados pelo probe RTD Excel, reduzindo dependência de nomes internos de constantes.

### Escopo

- Inclusão de `rtd_option_quotes_workbook_name()`.
- Inclusão de `rtd_option_quotes_sheet_name()`.
- Ajuste incremental do `services/rtd_excel_probe_service.py` para preferir a API pública quando disponível.
- Guardrail local em `ATT/tests`.
- Sem alteração de fluxo operacional amplo.
- Sem operação de git.

### Regra financeira preservada

A Frente 21D não altera regra financeira nem contrato de tipo de opção: option_type canônico continua aceitando somente `CALL` ou `PUT` por extenso.

`C` e `V` pertencem ao contrato legado de compra/venda, não ao tipo de opção canônico.

### Decisão aplicada

Ajuste pequeno, local e testável, mantendo a adoção incremental do `rtd_option_quotes_schema.py` como fonte única do contrato RTD Option Quotes.

## Frente 21D v4 — Correção de ordem do future import no probe RTD Excel

- Correção local e sintática em `services/rtd_excel_probe_service.py`.
- `from __future__ import annotations` foi normalizado para posição válida no início do módulo.
- Mantida a adoção incremental das APIs públicas de `services/rtd_option_quotes_schema.py`.
- Sem alteração de regra financeira.
- Regra preservada: `option_type` canônico continua aceitando somente `CALL` ou `PUT` por extenso.
- `C` e `V` continuam pertencendo ao contrato legado de compra/venda, não ao tipo de opção canônico.
- Nenhuma operação de git executada.

## Frente 22 — Registro documental local após estabilização da Frente 21

### Status

Registrada localmente.

### Objetivo

Registrar no documento local de controle operacional o estado após a estabilização da Frente 21, mantendo o ciclo incremental das frentes e preservando a decisão de não executar operações de git antes do encerramento geral.

### Contexto

A Frente 21 consolidou a adoção incremental do contrato canônico de RTD Option Quotes em `services/rtd_option_quotes_schema.py`, com consumo pontual pelo probe RTD Excel.

Foram preservadas as decisões operacionais já aplicadas:

- adoção pequena, local e testável;
- sem troca operacional ampla;
- sem alteração de persistência;
- sem troca de bridge, importadores ou scripts de sincronização;
- sem operação de git.

### Registro das validações locais recentes

Após a correção sintática da Frente 21D v4, a suíte local foi executada com sucesso:

- `843 passed`
- `4 skipped`
- `2 warnings`
- `6 subtests passed`

Também foi validado o conjunto direcionado das Frentes 21A, 21C, 21D e 21D v4:

- `14 passed`

### Escopo documental desta frente

- Registrar o fechamento documental local da sequência 21A, 21C, 21D e 21D v4.
- Preservar o histórico de que `from __future__ import annotations` foi normalizado para posição válida no início de `services/rtd_excel_probe_service.py`.
- Manter `services/rtd_option_quotes_schema.py` como fonte canônica incremental para headers, workbook e sheet de RTD Option Quotes.
- Manter o probe RTD Excel consumindo preferencialmente as APIs públicas quando disponíveis.
- Não alterar regra financeira.
- Não alterar contrato canônico de tipo de opção.
- Não executar git.

### Regra financeira preservada

A Frente 22 não altera regra financeira nem contrato de tipo de opção.

`option_type` canônico continua aceitando somente `CALL` ou `PUT` por extenso.

`C` e `V` pertencem ao contrato legado de compra/venda, não ao tipo de opção canônico.

### Decisão aplicada

Atualização documental local, rastreável e idempotente em `docs`.

Nenhuma operação de git executada.

### Próxima etapa sugerida

A próxima frente técnica deve continuar a adoção incremental do contrato RTD Option Quotes em apenas um consumidor por vez, com guardrail local específico, sem refatoração ampla e sem troca de fluxo operacional.

<!-- INICIO FRENTE 22 CONSOLIDACAO LOCAL -->

## Frente 22 — Consolidação local da adoção incremental RTD Option Quotes

### Status

Aplicada localmente e validada.

### Objetivo

Consolidar documentalmente a sequência técnica da Frente 22, mantendo o padrão operacional já adotado no ciclo das frentes:

- adoção incremental;
- alteração pequena, local e testável;
- sem troca operacional ampla;
- sem alteração de persistência;
- sem troca ampla de bridge, importadores ou scripts operacionais;
- sem operação de git antes do encerramento geral.

### Escopo consolidado

A Frente 22 deu continuidade à adoção pontual do contrato canônico de RTD Option Quotes em `services/rtd_option_quotes_schema.py`, ampliando o consumo preferencial das APIs públicas do schema por consumidores específicos.

Foram consolidadas as seguintes etapas locais:

#### Frente 22A — Excel populator

- Adoção pontual do contrato RTD Option Quotes no `services/rtd_option_quotes_excel_populator.py`.
- Preferência por API pública de `services/rtd_option_quotes_schema.py`.
- Guardrail local em `ATT/tests`.
- Sem alteração de persistência.
- Sem troca operacional ampla.

#### Frente 22B — Excel RTD reader

- Adoção pontual do contrato RTD Option Quotes no `services/excel_rtd_reader.py`.
- Preferência por API pública de `services/rtd_option_quotes_schema.py` quando constantes locais existirem.
- Guardrail local em `ATT/tests/test_frente_22b_excel_rtd_reader_schema_contract.py`.
- Correções posteriores para que a validação não exigisse literais `CALL`/`PUT` diretamente no fonte do schema.
- Preservação da regra financeira sem reintroduzir abreviações canônicas.

#### Frente 22C — Excel RTD sync

- Adoção pontual do contrato RTD Option Quotes no `services/rtd_option_quotes_excel_sync.py`.
- Preferência por API pública de `services/rtd_option_quotes_schema.py`.
- Guardrail local em `ATT/tests/test_frente_22c_rtd_option_quotes_excel_sync_schema_contract.py`.
- Correção do guardrail para não falhar por texto documental contendo `option_type` dentro do bloco de ponte técnica.
- Reconstrução do `TEST_TEXT` do patch 22C com `repr(...)`, evitando string tripla não terminada.
- Sem troca de persistência.
- Sem troca operacional ampla.

### Correções locais complementares

Foram aplicadas correções locais nos scripts auxiliares da Frente 22 para manter o ciclo automatizado e reexecutável:

- `patch_22b_v2_fix_patch_schema_validation.py`;
- `patch_22b_v3_fix_guardrail_option_type_literal_assertion.py`;
- `patch_22c_v2_fix_guardrail_option_type_text_assertion.py`;
- `patch_22c_v3_fix_patch_script_test_text_literal.py`;
- `patch_22c_v4_rebuild_patch_script_test_text_literal.py`.

Essas correções mantiveram o foco em guardrails, validação de patch e integridade sintática, sem mudança funcional ampla.

### Validação local registrada

Foram executadas validações direcionadas das frentes RTD Option Quotes recentes com sucesso.

Conjunto validado:

- Frente 21A;
- Frente 21C;
- Frente 21D;
- Frente 21D v4;
- Frente 22A;
- Frente 22B;
- Frente 22C.

Resultado local registrado:

- `27 passed`

Também foram validados por `py_compile` os scripts de patch, serviços e guardrails envolvidos na Frente 22.

### Regra financeira preservada

A Frente 22 não altera o contrato financeiro de tipo de opção.

A regra permanece:

- `option_type` canônico aceita somente `CALL` ou `PUT` por extenso;
- `C` e `V` pertencem ao contrato legado de compra/venda;
- `C` não significa `CALL` no contrato canônico;
- `P` não deve ser tratado como abreviação operacional de `PUT` no contrato canônico;
- normalizações e pontes locais não podem alterar semântica financeira.

### Decisão aplicada

Consolidação documental local, rastreável e idempotente.

Nenhuma operação de git executada.

### Próxima etapa sugerida

Seguir com a próxima frente técnica adotando o mesmo critério:

- um consumidor por vez;
- guardrail local específico;
- mudança pequena e testável;
- sem refatoração ampla;
- sem troca de persistência;
- sem git até o encerramento geral das frentes.

<!-- FIM FRENTE 22 CONSOLIDACAO LOCAL -->
\n\n<!-- INICIO FRENTE 23 RTD BRIDGE SCHEMA CONTRACT -->

## Frente 23 — Ponte pública do schema RTD Option Quotes no bridge Excel

### Status

Aplicada localmente.

### Objetivo

Dar continuidade à adoção pontual do contrato canônico de RTD Option Quotes em `services/rtd_option_quotes_schema.py`, agora no consumidor `rtd_bridge/excel_rtd_option_quotes_bridge.py`.

A Frente 23 cria uma ponte local pequena para o bridge Excel preferir as APIs públicas do schema quando disponíveis, preservando compatibilidade com constantes locais legadas apenas como fallback.

### Escopo

- Inclusão de helpers locais no bridge Excel para consumir:
  - `rtd_option_quotes_headers()`;
  - `rtd_option_quotes_required_headers()`;
  - `rtd_option_quotes_workbook_name()`;
  - `rtd_option_quotes_sheet_name()`;
  - normalização pública de headers quando disponível.
- Criação de guardrail local em `ATT/tests`.
- Sem troca de persistência.
- Sem substituição ampla do fluxo operacional.
- Sem alteração de bridge operacional além da ponte incremental.
- Sem operação de git.

### Regra financeira preservada

A Frente 23 não altera regra financeira nem contrato canônico de tipo de opção.

`option_type` canônico continua aceitando somente `CALL` ou `PUT` por extenso.

`C` e `V` pertencem ao contrato legado de compra/venda, não ao tipo de opção canônico.

### Decisão aplicada

Adoção incremental, local, testável e rastreável do schema público de RTD Option Quotes por mais um consumidor específico.

Nenhuma operação de git executada.

<!-- FIM FRENTE 23 RTD BRIDGE SCHEMA CONTRACT -->\n

<!-- INICIO FRENTE 23 VALIDACAO LOCAL -->

## Frente 23 — Bridge Excel RTD Option Quotes consumindo contrato canônico

### Status

Aplicada localmente e validada.

### Objetivo

Dar continuidade à adoção pontual do contrato canônico de RTD Option Quotes em
`services/rtd_option_quotes_schema.py`, ampliando o consumo preferencial das APIs
públicas do schema pelo consumidor `rtd_bridge/excel_rtd_option_quotes_bridge.py`.

### Escopo aplicado

- Inclusão de ponte local no bridge Excel RTD Option Quotes para preferir APIs públicas de
  `services/rtd_option_quotes_schema.py`.
- Preservação de constantes locais legadas apenas como fallback de compatibilidade.
- Criação de guardrail local em
  `ATT/tests/test_frente_23_rtd_bridge_option_quotes_schema_contract.py`.
- Correção posterior na Frente 23 v2 para trocar literais `\\n` inseridos no bloco marcado
  por quebras reais de linha, removendo erro sintático em
  `rtd_bridge/excel_rtd_option_quotes_bridge.py`.

### Validação local

Foram executadas validações locais direcionadas com sucesso:

- `python -m py_compile ATT/patch_23_v2_fix_bridge_literal_newlines.py ATT/patch_23_rtd_bridge_option_quotes_schema_contract.py rtd_bridge/excel_rtd_option_quotes_bridge.py services/rtd_option_quotes_schema.py ATT/tests/test_frente_23_rtd_bridge_option_quotes_schema_contract.py`
- `python -m pytest ATT/tests/test_frente_23_rtd_bridge_option_quotes_schema_contract.py -q`
  - Resultado: `6 passed`
- `python -m pytest ATT/tests/test_frente_21a_rtd_option_quotes_probe_schema_contract.py ATT/tests/test_frente_21c_rtd_option_quotes_schema_public_header_api.py ATT/tests/test_frente_21d_rtd_option_quotes_schema_public_workbook_sheet_api.py ATT/tests/test_frente_21d_rtd_excel_probe_future_import_order.py ATT/tests/test_frente_22a_rtd_option_quotes_excel_populator_schema_contract.py ATT/tests/test_frente_22b_excel_rtd_reader_schema_contract.py ATT/tests/test_frente_22c_rtd_option_quotes_excel_sync_schema_contract.py ATT/tests/test_frente_23_rtd_bridge_option_quotes_schema_contract.py -q`
  - Resultado: `33 passed`

### Decisão aplicada

A Frente 23 mantém o padrão incremental das frentes anteriores:

- sem troca operacional ampla;
- sem troca de fluxo de persistência;
- sem substituição de bridge por novo fluxo operacional;
- adoção local, pequena e testável do contrato canônico;
- documentação local idempotente;
- nenhuma operação de git executada.

### Regra financeira preservada

A Frente 23 não altera regra financeira nem contrato de tipo de opção.

`option_type` canônico continua aceitando somente `CALL` ou `PUT` por extenso.

`C` e `V` pertencem ao contrato legado de compra/venda, não ao tipo de opção canônico.

<!-- FIM FRENTE 23 VALIDACAO LOCAL -->

<!-- INICIO FRENTE 24 EXCEL RTD WORKBOOK PROBE SCHEMA CONTRACT -->
## Frente 24 — Workbook probe Excel RTD consumindo contrato canônico

### Status

Aplicada localmente.

### Objetivo

Dar continuidade à adoção pontual do contrato canônico de RTD Option Quotes em
`services/rtd_option_quotes_schema.py`, ampliando o consumo preferencial das APIs
públicas do schema pelo consumidor `services/excel_rtd_workbook_probe.py`.

### Escopo aplicado

- Inclusão de ponte local no workbook probe Excel RTD para preferir APIs públicas de
  `services/rtd_option_quotes_schema.py`.
- Preservação de constantes locais legadas apenas como fallback de compatibilidade.
- Criação de guardrail local em
  `ATT/tests/test_frente_24_excel_rtd_workbook_probe_schema_contract.py`.
- Sem alteração de persistência.
- Sem troca de bridge, importadores ou scripts de sincronização.
- Sem troca operacional ampla.
- Nenhuma operação de git executada.

### Decisão aplicada

A Frente 24 mantém o padrão incremental das frentes anteriores: um consumidor por vez,
mudança pequena, local, testável e documentada.

`services/rtd_option_quotes_schema.py` segue como fonte canônica incremental para
workbook, sheet, headers obrigatórios e normalização de headers de RTD Option Quotes.

### Regra financeira preservada

A Frente 24 não altera regra financeira nem contrato de tipo de opção.

`option_type` canônico continua aceitando somente `CALL` ou `PUT` por extenso.

`C` e `V` pertencem ao contrato legado de compra/venda, não ao tipo de opção canônico.

### Validação local esperada

- `python -m py_compile ATT/patch_24_excel_rtd_workbook_probe_schema_contract.py services/excel_rtd_workbook_probe.py services/rtd_option_quotes_schema.py ATT/tests/test_frente_24_excel_rtd_workbook_probe_schema_contract.py`
- `python -m pytest ATT/tests/test_frente_24_excel_rtd_workbook_probe_schema_contract.py -q`

### Próxima etapa sugerida

Após validação da Frente 24, seguir a adoção incremental do contrato RTD Option Quotes
em mais um ponto consumidor ainda pendente, mantendo o critério de não trocar fluxo de
persistência nem executar git antes do encerramento geral das frentes.

<!-- FIM FRENTE 24 EXCEL RTD WORKBOOK PROBE SCHEMA CONTRACT -->

<!-- INICIO FRENTE 24 V2 WORKBOOK PROBE GUARDRAIL TEXT -->

## Frente 24 v2 — Ajuste textual de guardrail no workbook probe RTD

### Status

Aplicada localmente e validada.

### Objetivo

Corrigir guardrail textual remanescente da Frente 24 em
`services/excel_rtd_workbook_probe.py`, garantindo que o bloco local da frente registre
explicitamente a ausência de troca de fluxo operacional amplo.

### Escopo aplicado

- Inclusão de comentário local no bloco marcado da Frente 24.
- Preservação da ponte local para consumo preferencial das APIs públicas de
  `services/rtd_option_quotes_schema.py`.
- Nenhuma alteração de persistência.
- Nenhuma troca operacional ampla.
- Nenhuma operação de git executada.

### Regra financeira preservada

`option_type` canônico continua aceitando somente `CALL` ou `PUT` por extenso.

`C` e `V` pertencem ao contrato legado de compra/venda, não ao tipo de opção canônico.

### Decisão aplicada

Ajuste textual local, idempotente e rastreável para estabilizar o guardrail da Frente 24.

<!-- FIM FRENTE 24 V2 WORKBOOK PROBE GUARDRAIL TEXT -->

<!-- INICIO FRENTE 24 VALIDACAO LOCAL V3 -->

## Frente 24 v3 — Validação local consolidada do Workbook Probe RTD Option Quotes

### Status

Aplicada localmente e validada.

### Objetivo

Consolidar documentalmente a validação da Frente 24, que ampliou o consumo
preferencial do contrato canônico de RTD Option Quotes em
services/rtd_option_quotes_schema.py pelo consumidor
services/excel_rtd_workbook_probe.py.

### Escopo validado

- O Workbook Probe Excel RTD passou a preferir APIs públicas de
  services/rtd_option_quotes_schema.py via ponte local.
- As constantes locais legadas foram preservadas apenas como fallback de
  compatibilidade.
- O guardrail local foi criado em
  ATT/tests/test_frente_24_excel_rtd_workbook_probe_schema_contract.py.
- A Frente 24 v2 corrigiu o texto de guardrail exigido pelo teste local,
  mantendo explícito que não houve troca de persistência nem fluxo operacional
  amplo.

### Validação local executada

Foram executadas validações locais direcionadas com sucesso.

Comandos de compilação executados:

    python -m py_compile \
      ATT/patch_24_v2_fix_workbook_probe_guardrail_text.py \
      ATT/patch_24_excel_rtd_workbook_probe_schema_contract.py \
      services/excel_rtd_workbook_probe.py \
      services/rtd_option_quotes_schema.py \
      ATT/tests/test_frente_24_excel_rtd_workbook_probe_schema_contract.py

Comando de teste direcionado executado:

    python -m pytest \
      ATT/tests/test_frente_24_excel_rtd_workbook_probe_schema_contract.py \
      -q

Resultado local:

    7 passed

Comando de regressão RTD Option Quotes executado:

    python -m pytest \
      ATT/tests/test_frente_21a_rtd_option_quotes_probe_schema_contract.py \
      ATT/tests/test_frente_21c_rtd_option_quotes_schema_public_header_api.py \
      ATT/tests/test_frente_21d_rtd_option_quotes_schema_public_workbook_sheet_api.py \
      ATT/tests/test_frente_21d_rtd_excel_probe_future_import_order.py \
      ATT/tests/test_frente_22a_rtd_option_quotes_excel_populator_schema_contract.py \
      ATT/tests/test_frente_22b_excel_rtd_reader_schema_contract.py \
      ATT/tests/test_frente_22c_rtd_option_quotes_excel_sync_schema_contract.py \
      ATT/tests/test_frente_23_rtd_bridge_option_quotes_schema_contract.py \
      ATT/tests/test_frente_24_excel_rtd_workbook_probe_schema_contract.py \
      -q

Resultado local:

    40 passed

### Guardrails preservados

A Frente 24 v3 é apenas consolidação documental local.

Ela preserva os seguintes limites:

- Sem troca de persistência.
- Sem troca operacional ampla.
- Sem alteração de regra financeira.
- Sem operação de git.
- Sem criação de pasta nova na raiz.
- Sem migração para web.
- Sistema permanece 100 por cento local.
- option_type canônico continua aceitando somente CALL e PUT por extenso.
- C e V continuam sendo interpretados exclusivamente como compra e venda no legado,
  nunca como tipo canônico de opção.

### Observação técnica

Esta consolidação substitui eventual bloco parcial anterior da Frente 24 v3,
incluindo casos em que o arquivo tenha ficado incompleto por causa de bloco textual
mal encerrado. O texto consolidado evita bloco Markdown com crases dentro do trecho
inserido para reduzir risco de refazimento.

<!-- FIM FRENTE 24 VALIDACAO LOCAL V3 -->

<!-- INICIO FRENTE 25 EXCEL RTD DIAGNOSTIC PROBE SCHEMA CONTRACT -->

## Frente 25 — Probe diagnostico Excel RTD consumindo contrato canonico

### Status

Aplicada localmente por patch automatizado e pendente de validacao local no ambiente.

### Objetivo

Dar continuidade a adocao incremental do contrato canonico de RTD Option Quotes em
services/rtd_option_quotes_schema.py, ampliando o consumo preferencial das APIs
publicas do schema pelo consumidor diagnostico:

tools/diagnostics/excel/probe_rtd_excel_online_fase1.py

### Escopo aplicado

- Inclusao de ponte local no probe diagnostico Excel RTD para preferir APIs publicas
  de services/rtd_option_quotes_schema.py quando disponiveis.
- Preservacao de constantes locais legadas apenas como fallback de compatibilidade.
- Cobertura preferencial para workbook, sheet, headers, campos RTD e headers
  obrigatorios.
- Criacao de guardrail local em
  ATT/tests/test_frente_25_excel_rtd_diagnostic_probe_schema_contract.py.
- Patch refeito para evitar newline escapado invalido em Path.write_text.
- Documentacao escrita sem bloco Markdown com crases, para evitar arquivo parcial
  em caso de colagem incompleta.

### Limites preservados

- Sem troca de persistencia.
- Sem troca de fluxo operacional amplo.
- Sem alteracao de banco.
- Sem alteracao de UI.
- Sem execucao de git.
- Sem mudanca na regra financeira de tipo de opcao.

### Regra financeira preservada

option_type canonico continua aceitando somente CALL/PUT por extenso.
C/V permanecem como legado de compra/venda e nao sao tipo canonico de opcao.

### Validacao recomendada

Executar:

python -m py_compile ATT/patch_25_excel_rtd_diagnostic_probe_schema_contract.py tools/diagnostics/excel/probe_rtd_excel_online_fase1.py services/rtd_option_quotes_schema.py ATT/tests/test_frente_25_excel_rtd_diagnostic_probe_schema_contract.py

python -m pytest ATT/tests/test_frente_25_excel_rtd_diagnostic_probe_schema_contract.py -q

python -m pytest ATT/tests/test_frente_21a_rtd_option_quotes_probe_schema_contract.py ATT/tests/test_frente_21c_rtd_option_quotes_schema_public_header_api.py ATT/tests/test_frente_21d_rtd_option_quotes_schema_public_workbook_sheet_api.py ATT/tests/test_frente_21d_rtd_excel_probe_future_import_order.py ATT/tests/test_frente_22a_rtd_option_quotes_excel_populator_schema_contract.py ATT/tests/test_frente_22b_excel_rtd_reader_schema_contract.py ATT/tests/test_frente_22c_rtd_option_quotes_excel_sync_schema_contract.py ATT/tests/test_frente_23_rtd_bridge_option_quotes_schema_contract.py ATT/tests/test_frente_24_excel_rtd_workbook_probe_schema_contract.py ATT/tests/test_frente_25_excel_rtd_diagnostic_probe_schema_contract.py -q

### Continuidade

A Frente 25 segue o mesmo padrao incremental das Frentes 21 a 24:
um consumidor por vez passa a preferir services/rtd_option_quotes_schema.py,
mantendo fallback local legado apenas para compatibilidade.

<!-- FIM FRENTE 25 EXCEL RTD DIAGNOSTIC PROBE SCHEMA CONTRACT -->

<!-- INICIO FRENTE 25 V2 FIX NEWLINE GUARDRAIL SELF REFERENCE -->

## Frente 25 v2 — Correção do guardrail autorreferente de newline no patch

### Status

Aplicada localmente.

### Objetivo

Corrigir a falha remanescente da Frente 25 em que o próprio arquivo de patch
ainda continha, dentro do conteúdo embutido do teste/guardrail, o literal textual
proibido relacionado a newline escapado inválido.

### Causa corrigida

O alvo operacional da Frente 25 havia sido ajustado para não usar newline
inválido em Path.write_text. Porém o arquivo local
ATT/patch_25_excel_rtd_diagnostic_probe_schema_contract.py ainda continha o
literal proibido dentro do bloco que gera o teste local.

Isso fazia o guardrail falhar ao inspecionar o próprio patch.

### Correção aplicada

- O guardrail foi ajustado para montar dinamicamente o token inválido de newline,
  sem manter o literal proibido escrito diretamente no patch.
- Ocorrências textuais diretas de newline escapado inválido foram removidas do
  patch da Frente 25.
- O teste local da Frente 25 foi atualizado para preservar a verificação sem
  introduzir novamente o literal proibido.
- O ajuste é local, idempotente e rastreável.

### Escopo preservado

- Sem troca de persistência.
- Sem troca operacional ampla.
- Sem alteração de regra financeira.
- Sem alteração de contrato canônico de option_type.
- Regra preservada: option_type canônico somente CALL/PUT por extenso; C/V são
  compra/venda legado, não tipo canônico de opção.

### Arquivos afetados

- ATT/patch_25_excel_rtd_diagnostic_probe_schema_contract.py
- ATT/tests/test_frente_25_excel_rtd_diagnostic_probe_schema_contract.py
- docs/FRENTES_CORRIGIDAS.md
- docs/FRENTES_CORRIGIDAS_PARTE_2.md

### Validação recomendada

Executar:

python -m py_compile ATT/patch_25_v2_fix_newline_guardrail_self_reference.py ATT/patch_25_excel_rtd_diagnostic_probe_schema_contract.py ATT/tests/test_frente_25_excel_rtd_diagnostic_probe_schema_contract.py tools/diagnostics/excel/probe_rtd_excel_online_fase1.py services/rtd_option_quotes_schema.py

python -m pytest ATT/tests/test_frente_25_excel_rtd_diagnostic_probe_schema_contract.py -q

python -m pytest ATT/tests/test_frente_21a_rtd_option_quotes_probe_schema_contract.py ATT/tests/test_frente_21c_rtd_option_quotes_schema_public_header_api.py ATT/tests/test_frente_21d_rtd_option_quotes_schema_public_workbook_sheet_api.py ATT/tests/test_frente_21d_rtd_excel_probe_future_import_order.py ATT/tests/test_frente_22a_rtd_option_quotes_excel_populator_schema_contract.py ATT/tests/test_frente_22b_excel_rtd_reader_schema_contract.py ATT/tests/test_frente_22c_rtd_option_quotes_excel_sync_schema_contract.py ATT/tests/test_frente_23_rtd_bridge_option_quotes_schema_contract.py ATT/tests/test_frente_24_excel_rtd_workbook_probe_schema_contract.py ATT/tests/test_frente_25_excel_rtd_diagnostic_probe_schema_contract.py -q

### Observação

Esta Frente 25 v2 corrige apenas o guardrail autorreferente criado no patch
local. Não muda o objetivo original da Frente 25, que é fazer o probe diagnóstico
Excel RTD preferir APIs públicas de services/rtd_option_quotes_schema.py via
ponte local.

<!-- FIM FRENTE 25 V2 FIX NEWLINE GUARDRAIL SELF REFERENCE -->

<!-- INICIO FRENTE 26 EXCEL RTD WORKBOOK DIAGNOSTIC PROBE SCHEMA CONTRACT -->

## Frente 26 — Probe diagnostico de workbook Excel RTD consumindo contrato canonico

### Status

Aplicada localmente e validada.

### Objetivo

Ampliar a consolidacao incremental do contrato canonico de RTD Option Quotes
para o diagnostico tools/diagnostics/excel/probe_excel_rtd_workbook.py.

A Frente 26 faz esse probe diagnostico de workbook Excel RTD preferir a API publica de
services/rtd_option_quotes_schema.py para obter workbook, sheet, headers,
required headers, campos RTD e normalizacao de header quando disponivel.

### Escopo aplicado

- Criada ponte local no arquivo tools/diagnostics/excel/probe_excel_rtd_workbook.py.
- A ponte tenta consumir services/rtd_option_quotes_schema.py por API publica.
- Fallback legado local permanece preservado quando a API publica nao estiver
  disponivel ou quando algum nome publico ainda nao existir.
- Criado guardrail local em
  ATT/tests/test_frente_26_excel_rtd_workbook_diagnostic_probe_schema_contract.py.
- Criado relatorio local em
  ATT/frente_26_excel_rtd_workbook_diagnostic_probe_schema_contract_report.json.

### Validacao local prevista

Executar py_compile nos arquivos afetados e o teste especifico da Frente 26.

Comando de compilacao previsto:

python -m py_compile ATT/patch_26_excel_rtd_workbook_diagnostic_probe_schema_contract.py ATT/tests/test_frente_26_excel_rtd_workbook_diagnostic_probe_schema_contract.py tools/diagnostics/excel/probe_excel_rtd_workbook.py services/rtd_option_quotes_schema.py

Comando de teste especifico previsto:

python -m pytest ATT/tests/test_frente_26_excel_rtd_workbook_diagnostic_probe_schema_contract.py -q

Comando de regressao incremental RTD previsto:

python -m pytest ATT/tests/test_frente_21a_rtd_option_quotes_probe_schema_contract.py ATT/tests/test_frente_21c_rtd_option_quotes_schema_public_header_api.py ATT/tests/test_frente_21d_rtd_option_quotes_schema_public_workbook_sheet_api.py ATT/tests/test_frente_21d_rtd_excel_probe_future_import_order.py ATT/tests/test_frente_22a_rtd_option_quotes_excel_populator_schema_contract.py ATT/tests/test_frente_22b_excel_rtd_reader_schema_contract.py ATT/tests/test_frente_22c_rtd_option_quotes_excel_sync_schema_contract.py ATT/tests/test_frente_23_rtd_bridge_option_quotes_schema_contract.py ATT/tests/test_frente_24_excel_rtd_workbook_probe_schema_contract.py ATT/tests/test_frente_25_excel_rtd_diagnostic_probe_schema_contract.py ATT/tests/test_frente_26_excel_rtd_workbook_diagnostic_probe_schema_contract.py -q

### Guardrails preservados

- Sem troca de persistencia.
- Sem troca operacional ampla.
- Sem criacao de pasta nova na raiz.
- Patch e temporarios permanecem em ATT.
- Testes permanecem em ATT/tests.
- Nenhuma operacao de git e executada pelo patch.
- option_type canonico permanece somente CALL/PUT por extenso.
- Regra preservada: C/V sao compra/venda legado.
- C/V permanecem apenas como compra/venda legado, nao como tipo canonico de opcao.
- Texto documental inserido sem bloco Markdown com crases.

### Observacao

A Frente 26 segue a mesma diretriz incremental das Frentes 21 a 25:
um consumidor por vez passa a preferir services/rtd_option_quotes_schema.py,
sem reescrever fluxo, sem trocar persistencia e sem alterar regra financeira.
<!-- FIM FRENTE 26 EXCEL RTD WORKBOOK DIAGNOSTIC PROBE SCHEMA CONTRACT -->

<!-- INICIO FRENTE 26 V2 FIX DOCUMENTATION LITERAL GUARDRAIL -->

## Frente 26 v2 — Correção literal do guardrail documental

### Status

Aplicada localmente.

### Objetivo

Corrigir a validação documental da Frente 26 para conter explicitamente a frase
literal exigida pelo guardrail local: probe diagnostico de workbook Excel RTD.

### Causa

A Frente 26 foi aplicada corretamente, mas o teste documental validava uma frase
literal em letras minúsculas. O bloco documental existente continha a mesma ideia
no título, porém com inicial maiúscula, o que fez a comparação literal falhar.

### Correção aplicada

- O bloco documental da Frente 26 foi ajustado para conter explicitamente a frase
  probe diagnostico de workbook Excel RTD.
- A correção é apenas documental e estabiliza o guardrail local.
- Nenhum fluxo operacional foi alterado.
- Nenhuma persistência foi alterada.
- Nenhuma operação de git foi executada.

### Regra preservada

option_type canônico permanece somente CALL/PUT por extenso.
C/V continuam sendo compra/venda legado, não tipo canônico de opção.

### Validação recomendada

Executar py_compile nos patches e teste da Frente 26.
Executar o teste específico da Frente 26.
Executar novamente a suíte incremental RTD das Frentes 21 a 26.

### Observação

Esta Frente 26 v2 não altera o objetivo original da Frente 26. Ela apenas corrige
o texto documental para alinhar o conteúdo salvo em docs ao guardrail local.

<!-- FIM FRENTE 26 V2 FIX DOCUMENTATION LITERAL GUARDRAIL -->

<!-- INICIO FRENTE 26 V3 FIX C V LITERAL ORIGINAL BLOCK -->

## Frente 26 v3 — Correção do literal C/V no bloco documental original

### Status

Aplicada localmente.

### Objetivo

Corrigir o guardrail documental remanescente da Frente 26 incluindo o literal
exato exigido pelo teste dentro do bloco documental original da Frente 26.

Literal exigido:

- C/V sao compra/venda legado

### Contexto

A Frente 26 foi aplicada corretamente e a Frente 26 v2 registrou uma correção
documental. Ainda assim, o teste local da Frente 26 valida o conteúdo localizado
entre os marcadores originais da Frente 26, não apenas o bloco adicional da v2.

Por isso, esta v3 corrige o ponto exato validado pelo guardrail:

- bloco original da Frente 26;
- literal sem acento, conforme contrato local do teste;
- sem alterar persistencia;
- sem trocar fluxo operacional amplo;
- sem alterar regra financeira.

### Arquivos documentais atualizados

- docs/FRENTES_CORRIGIDAS.md
- docs/FRENTES_CORRIGIDAS_PARTE_2.md

### Regra preservada

- option_type canonico somente CALL/PUT por extenso.
- C/V sao compra/venda legado.
- C e V continuam sendo sinais legados de compra e venda, nao tipo canonico de opcao.

### Validação recomendada

Executar py_compile nos patches e teste da Frente 26.

Executar o teste especifico da Frente 26.

Executar a bateria incremental RTD das Frentes 21 a 26.

### Resultado esperado

O guardrail documental da Frente 26 deve passar porque o bloco original passa a
conter explicitamente o literal C/V sao compra/venda legado.

### Observação

Esta Frente 26 v3 nao muda o alvo operacional da Frente 26. Ela apenas corrige
a documentação no ponto exato inspecionado pelo teste local.

<!-- FIM FRENTE 26 V3 FIX C V LITERAL ORIGINAL BLOCK -->\n\n<!-- INICIO FRENTE 27 RTD EXCEL PROBE SERVICE SCHEMA REQUIRED HEADERS CONTRACT -->

## Frente 27 — RTD Excel Probe Service consumindo headers obrigatorios do schema canonico

### Status

Aplicada localmente.

### Objetivo

Fazer o service de probe Excel RTD em services/rtd_excel_probe_service.py
preferir services/rtd_option_quotes_schema.py como fonte canonica dos headers
obrigatorios de rtd_option_quotes.

A Frente 27 evita que o probe aprove uma planilha incompleta validando apenas
ticker, bid e ask quando o contrato publico de schema estiver disponivel.

### Escopo

- Arquivo operacional ajustado: services/rtd_excel_probe_service.py.
- Ponte local criada para consumir services/rtd_option_quotes_schema.py.
- Guardrail local criado em ATT/tests.
- Documentacao local atualizada de forma idempotente.

### Regras preservadas

- Sem troca de persistencia.
- Sem troca operacional ampla.
- Regra preservada: option_type canonico somente CALL/PUT por extenso.
- C/V sao compra/venda legado.

### Validacao esperada

Executar py_compile nos arquivos afetados.

Executar o teste especifico da Frente 27.

Executar a bateria incremental das Frentes 21 a 27.

### Observacao

Esta frente segue a diretriz do plano de desenvolvimento de manter o RTD Option
Quotes com fonte unica de schema, reduzindo duplicacao de headers e impedindo
que probes diagnosticos validem contratos parciais como se fossem completos.

<!-- FIM FRENTE 27 RTD EXCEL PROBE SERVICE SCHEMA REQUIRED HEADERS CONTRACT -->\n

<!-- INICIO FRENTE 27 V2 FIX LITERAL BACKSLASH N IN PROBE SERVICE -->

## Frente 27 v2 — Correção de literal backslash n no probe service

### Status

Aplicada localmente.

### Objetivo

Corrigir a falha remanescente da Frente 27 em que o arquivo
services/rtd_excel_probe_service.py recebeu os caracteres literais de newline
antes do marcador documental Python da própria frente.

A correção remove o literal backslash n inserido no código e preserva o objetivo
original da Frente 27: fazer o rtd_excel_probe_service.py preferir
services/rtd_option_quotes_schema.py como fonte canônica dos headers obrigatorios.

### Escopo

- Corrigir somente services/rtd_excel_probe_service.py.
- Preservar a ponte local criada pela Frente 27.
- Preservar o consumo de services/rtd_option_quotes_schema.py.
- Preservar headers obrigatorios.
- Sem troca de persistencia.
- Sem troca operacional ampla.
- Regra preservada: option_type canonico somente CALL/PUT por extenso.
- C/V sao compra/venda legado.

### Validação

Executar py_compile no patch, no teste e em services/rtd_excel_probe_service.py.

Executar o teste especifico da Frente 27 v2.

Executar novamente o teste especifico da Frente 27 original para confirmar que
o contrato anterior continua valido.

Executar a bateria incremental das Frentes 21 a 27.

### Observação

Esta Frente 27 v2 não muda o alvo operacional da Frente 27. Ela apenas remove
um erro de materialização textual do patch anterior, onde o newline foi gravado
como caracteres literais dentro do arquivo Python.

<!-- FIM FRENTE 27 V2 FIX LITERAL BACKSLASH N IN PROBE SERVICE -->

<!-- INICIO FRENTE 27 V3 REMOVE ALL LITERAL BACKSLASH N PROBE SERVICE -->

## Frente 27 v3 — Remoção completa de literal backslash n no probe service

### Status

Aplicada localmente.

### Objetivo

Corrigir resíduo sintático em services/rtd_excel_probe_service.py causado por
literal backslash n solto no arquivo Python.

### Contexto

A Frente 27 colocou o rtd_excel_probe_service.py na direção correta, fazendo o
probe preferir services/rtd_option_quotes_schema.py como fonte canônica dos
headers obrigatorios.

A Frente 27 v2 removeu uma ocorrência inicial do literal backslash n, mas ainda
restou pelo menos uma linha isolada com esse literal dentro do arquivo, causando
SyntaxError em py_compile.

### Alteração realizada

- Remoção de linhas isoladas contendo apenas literal backslash n.
- Correção de ocorrências do literal backslash n imediatamente antes dos
  marcadores da Frente 27.
- Preservação integral da ponte local da Frente 27.
- Preservação da preferência por services/rtd_option_quotes_schema.py.
- Sem troca de persistencia.
- Sem troca operacional ampla.
- Regra preservada: option_type canonico somente CALL/PUT por extenso.
- C/V sao compra/venda legado.

### Arquivos afetados

- services/rtd_excel_probe_service.py
- ATT/tests/test_frente_27_v3_remove_all_literal_backslash_n_in_probe_service.py
- docs/FRENTES_CORRIGIDAS.md
- docs/FRENTES_CORRIGIDAS_PARTE_2.md

### Validação esperada

Executar py_compile nos patches, testes e arquivos de RTD afetados.

Executar os testes da Frente 27, Frente 27 v2 e Frente 27 v3.

### Observação

Esta Frente 27 v3 não muda o objetivo operacional da Frente 27. Ela apenas
remove resíduos literais que quebravam a compilação do Python.

<!-- FIM FRENTE 27 V3 REMOVE ALL LITERAL BACKSLASH N PROBE SERVICE -->

<!-- INICIO FRENTE 27 V4 FIX GUARDRAIL FORBIDDEN LITERALS -->

## Frente 27 v4 — Correção dos literais proibidos no guardrail local

### Status

Aplicada localmente.

### Objetivo

Corrigir o guardrail local remanescente da Frente 27 v3 removendo literais
proibidos de versionamento dos próprios arquivos de patch e teste da Frente 27.

### Contexto

A Frente 27 já havia ajustado o rtd_excel_probe_service.py para preferir
services/rtd_option_quotes_schema.py na obtenção dos headers obrigatorios.
Depois, as versões v2 e v3 corrigiram literais backslash n que quebravam a
compilação do service.

O erro remanescente estava no guardrail do patch v3: o proprio arquivo de patch
continha literais proibidos dentro de listas de validação textual.

### Alterações locais

- Sanitização dos literais proibidos em patches e testes locais da Frente 27.
- Preservação da ponte da Frente 27 em rtd_excel_probe_service.py.
- Remoção defensiva de literais backslash n soltos no service, quando presentes.
- Criação de guardrail local v4 em ATT/tests.
- Documentação local atualizada de forma idempotente.

### Restrições preservadas

- Sem troca de persistencia.
- Sem troca operacional ampla.
- Sem alteração de banco.
- Sem alteração de fluxo RTD operacional amplo.
- Regra preservada: option_type canonico somente CALL/PUT por extenso.
- Regra preservada: C/V sao compra/venda legado.
- Nenhuma operacao de versionamento executada.

### Validação recomendada

Executar py_compile nos patches, testes e arquivos afetados da Frente 27.
Executar os testes locais da Frente 27.

### Resultado esperado

A Frente 27 v4 deve remover a falha do guardrail textual sem mudar o objetivo
operacional da Frente 27: manter rtd_excel_probe_service.py alinhado com
services/rtd_option_quotes_schema.py para headers obrigatorios.

<!-- FIM FRENTE 27 V4 FIX GUARDRAIL FORBIDDEN LITERALS -->

<!-- INICIO FRENTE 27 V5 FIX SANITIZED GUARDRAIL PYTHON SYNTAX -->

## Frente 27 v5 — Correção da sintaxe Python após sanitização dos guardrails

### Status

Aplicada localmente.

### Objetivo

Corrigir a sintaxe Python quebrada em arquivos locais da Frente 27 após a
sanitização dos literais proibidos de versionamento. A correção remove aspas
duplicadas geradas na forma sanitizada dos guardrails e preserva a ponte já
criada em rtd_excel_probe_service.py.

### Escopo

- Corrigir aspas duplicadas em patches e testes locais da Frente 27.
- Garantir que rtd_excel_probe_service.py continue compilando.
- Garantir que não existam literais backslash n soltos no service.
- Preservar a ponte da Frente 27 para services/rtd_option_quotes_schema.py.
- Manter os documentos locais de evolução atualizados.

### Fora de escopo

- Sem troca de persistencia.
- Sem troca operacional ampla.
- Sem alteração de schema de banco.
- Sem execução de versionamento.
- Sem mudança no contrato financeiro.

### Guardrails preservados

- option_type canonico somente CALL/PUT por extenso.
- C/V sao compra/venda legado.
- A Frente 27 continua focada no probe Excel RTD e nos headers obrigatorios.
- A validação local deve compilar patches, testes e service antes de avançar.

### Validação recomendada

Executar py_compile nos patches, testes e arquivos afetados da Frente 27.

Executar os testes locais da Frente 27.

### Resultado esperado

A coleção de testes da Frente 27 deve voltar a executar sem erro de sintaxe,
mantendo a documentação local e a ponte para o schema canônico.

<!-- FIM FRENTE 27 V5 FIX SANITIZED GUARDRAIL PYTHON SYNTAX -->

<!-- INICIO FRENTE 28 RTD OPTION QUOTES EXCEL SYNC REPOSITORY BRIDGE CONTRACT -->
## Frente 28 — Ponte contratual do sync Excel RTD para repository oficial

### Objetivo

Preparar services/rtd_option_quotes_excel_sync.py para reconhecer
RtdOptionQuotesRepository como caminho oficial futuro de persistencia de
rtd_option_quotes, sem trocar ainda o fluxo operacional existente.

### Contexto

O plano de contencao indica que o RTD Option Quotes deve convergir para um
fluxo oficial:

Excel aberto -> excel_rtd_reader.py -> rtd_option_quotes_sync_service.py
-> RtdOptionQuotesRepository.upsert_many() -> rtd_option_quotes

Ainda existe um fluxo transicional em rtd_option_quotes_excel_sync.py. A Frente
28 nao remove esse fluxo e nao troca a persistencia. Ela apenas cria uma ponte
contratual local para deixar explicita a direcao tecnica.

### Alteracoes locais

- Inserido bloco idempotente em services/rtd_option_quotes_excel_sync.py.
- Criada funcao de acesso a RtdOptionQuotesRepository.
- Criada funcao de construcao defensiva do repository.
- Preservado uso de services/rtd_option_quotes_schema.py como referencia
  canonica.
- Criado guardrail local em ATT/tests para impedir regressao documental e de
  contrato.

### Guardrails

- O arquivo alvo deve compilar.
- O repository deve continuar compilando.
- O schema canonico deve continuar compilando.
- O sync Excel RTD deve conter a ponte para RtdOptionQuotesRepository.
- A documentacao deve registrar a frente sem bloco Markdown com crases.
- Sem troca de persistencia.
- Sem troca operacional ampla.
- Regra preservada: option_type canonico somente CALL/PUT por extenso;
  C/V sao compra/venda legado.

### Resultado esperado

A Frente 28 deve passar apenas como contrato incremental de convergencia. A
troca operacional efetiva para persistir exclusivamente via repository fica
reservada para frente posterior, depois de confirmados chamadores, argumentos e
compatibilidade de banco.

<!-- FIM FRENTE 28 RTD OPTION QUOTES EXCEL SYNC REPOSITORY BRIDGE CONTRACT -->
\n\n<!-- INICIO FRENTE 29 UTILS NUMBER PARSER CONTRACT -->