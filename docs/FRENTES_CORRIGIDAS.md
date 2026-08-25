# Frentes Corrigidas — Controle Operacional

Este arquivo registra as frentes já corrigidas durante a contenção do projeto.

Registro mantido localmente durante a execução incremental das frentes. A atualização de controle externo deve ocorrer somente ao final do ciclo completo de frentes, conforme decisão operacional do projeto.

## Frente 1 — Contenção inicial

Status: aplicada e validada.

Registro consolidado da contenção inicial e da organização dos primeiros pontos de correção operacional.

---

## Frente 2 — Organização de fluxo

Status: aplicada e validada.

Registro consolidado da organização de fluxo e redução de ambiguidade operacional.

---

## Frente 3 — Ajustes de integração

Status: aplicada e validada.

Registro consolidado dos ajustes de integração tratados nas frentes iniciais.

---

## Frente 4 — Estabilização incremental

Status: aplicada e validada.

Registro consolidado da estabilização incremental sem troca operacional ampla.

---

## Frente 5 — Contratos locais

Status: aplicada e validada.

Registro consolidado de contratos locais e pontos de contenção já tratados.

---

## Frente 6 — Higiene de execução

Status: aplicada e validada.

Registro consolidado de higiene de execução, documentação e validações incrementais.

---

## Frente 7 — Alinhamento operacional

Status: aplicada e validada.

Registro consolidado do alinhamento operacional realizado em etapas anteriores.

---

## Frente 8 — Redução de acoplamento

Status: aplicada e validada.

Registro consolidado da redução de acoplamento e preparação de frentes seguintes.

---

## Frente 09 — Verificações locais

Status: aplicada e validada.

Registro consolidado das verificações locais e da manutenção do ciclo testável.

---

### Status operacional

- Status: Em andamento.
- Transição acompanhada para `derived_repo` sem operação de git nesta etapa.


## Frente 10 — Consolidação intermediária

Status: aplicada e validada.

Registro consolidado da etapa intermediária de evolução controlada.

---

## Frente 11 — Ajustes de consistência

Status: aplicada e validada.

Registro consolidado dos ajustes de consistência aplicados antes das frentes estruturais.

---

## Frente 12 — Preparação de governança

Status: aplicada e validada.

Registro consolidado da preparação de governança documental e operacional.

---

## Frente 13 — Marco anterior à consolidação estrutural

Status: aplicada e validada.

Registro consolidado do marco anterior à entrada nas frentes estruturais seguintes.

---

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
## Frente 29 — utils number_parser contrato local

Status: aplicada localmente.

Objetivo: criar utils/number_parser.py como ponto unico inicial para normalizacao numerica BR, Excel e CSV.

Arquivos afetados:
- utils/number_parser.py
- ATT/tests/test_frente_29_utils_number_parser_contract.py

Contrato introduzido:
- parse_float_br
- parse_optional_float
- parse_positive_float
- parse_percent

Escopo:
- Aceita formatos brasileiros como 1.234,56 e 12,5.
- Aceita formatos mistos de Excel/CSV como 1,234.56.
- Trata valores vazios, nulos textuais e simbolos monetarios simples.
- Converte percentuais para fracao decimal.

Limites preservados:
- Sem troca de persistencia.
- Sem troca operacional ampla.
- Sem alteracao de sync RTD.
- Sem alteracao de contratos financeiros.
- Sem operacao de versionamento.

Resultado esperado:
- Preparar as proximas frentes para consumir um parser numerico unico em RTD, CSV, intraday, candles e enrichment, reduzindo normalizadores duplicados.

Validação local:
- python -m py_compile ATT/patch_29_utils_number_parser_contract.py ATT/tests/test_frente_29_utils_number_parser_contract.py utils/number_parser.py
- python -m pytest ATT/tests/test_frente_29_utils_number_parser_contract.py -q
<!-- FIM FRENTE 29 UTILS NUMBER PARSER CONTRACT -->\n\n\n<!-- INICIO FRENTE 30 UTILS DATE PARSER CONTRACT -->
Frente 30 - utils/date_parser.py como contrato local de normalizacao de datas.

Objetivo:
Centralizar um ponto inicial para conversao de datas vindas de Excel, RTD, CSV e strings operacionais, preparando as proximas frentes para reduzir duplicacao de parser de datas nos fluxos RTD e intraday.

Arquivos principais:
utils/date_parser.py
ATT/tests/test_frente_30_utils_date_parser_contract.py

Funcoes publicas:
parse_excel_date_to_iso
parse_datetime_to_iso

Escopo:
Aceita serial Excel moderno usando epoch 1899-12-30.
Aceita date e datetime Python.
Aceita formatos ISO.
Aceita formatos brasileiros comuns como dd/mm/AAAA.
Retorna None para entradas vazias ou invalidas.

Garantias:
Sem troca de persistencia.
Sem troca operacional ampla.
Sem alteracao de sync RTD.
Sem operacao de versionamento.
<!-- FIM FRENTE 30 UTILS DATE PARSER CONTRACT -->\n

<!-- INICIO FRENTE 31 EXCEL RTD READER PARSER BRIDGE CONTRACT -->
## Frente 31 - Excel RTD Reader Parser Bridge Contract

Status: aplicada localmente.

Objetivo:
- registrar `utils/number_parser.py` como contrato canônico futuro para normalização numérica;
- registrar `utils/date_parser.py` como contrato canônico futuro para normalização de datas;
- preparar a redução gradual de parsers duplicados nos fluxos RTD;
- manter a operação atual intacta nesta frente.

Arquivos envolvidos:
- `services/excel_rtd_reader.py`
- `utils/number_parser.py`
- `utils/date_parser.py`
- `ATT/tests/test_frente_31_excel_rtd_reader_parser_bridge_contract.py`

Garantias:
- sem troca de persistência;
- sem troca operacional ampla;
- sem alteração de sync RTD;
- sem execução de versionamento;
- parsers canônicos preservados:
  - `parse_float_br`
  - `parse_optional_float`
  - `parse_positive_float`
  - `parse_percent`
  - `parse_excel_date_to_iso`
  - `parse_datetime_to_iso`

Validação local:
- `py_compile` nos arquivos da frente;
- teste local da Frente 31;
- regressão recomendada das Frentes 21a até 31.

<!-- FIM FRENTE 31 EXCEL RTD READER PARSER BRIDGE CONTRACT -->

<!-- INICIO FRENTE 32 RTD OPTION QUOTES EXCEL SYNC PARSER BRIDGE CONTRACT -->
Frente 32 - Ponte contratual de parsers canonicos no sync Excel RTD de opcoes.

Resumo:
- services/rtd_option_quotes_excel_sync.py passou a registrar ponte local para os parsers canonicos de numeros e datas.
- utils/number_parser.py permanece como contrato canonico numerico.
- utils/date_parser.py permanece como contrato canonico de datas.
- A frente prepara migracao incremental futura para reduzir duplicacao de parser nos fluxos RTD.

Garantias:
- Sem troca de persistencia.
- Sem troca operacional ampla.
- Sem alteracao do caminho atual de sync RTD.
- Sem operacao de versionamento.
- Regra preservada: option_type canonico somente CALL/PUT por extenso; C/V sao compra/venda legado.
<!-- FIM FRENTE 32 RTD OPTION QUOTES EXCEL SYNC PARSER BRIDGE CONTRACT -->

<!-- INICIO FRENTE 32 V2 FIX GUARDRAIL FORBIDDEN LITERALS -->
Frente 32 v2: correcao local do guardrail auto-referente da Frente 32.

Objetivo:
Sanitizar literais proibidos em patch e teste da Frente 32 para evitar que o proprio guardrail falhe ao encontrar os termos que ele mesmo verifica.

Escopo:
ATT/patch_32_rtd_option_quotes_excel_sync_parser_bridge_contract.py
ATT/tests/test_frente_32_rtd_option_quotes_excel_sync_parser_bridge_contract.py
ATT/tests/test_frente_32_v2_fix_guardrail_forbidden_literals.py

Resultado esperado:
A Frente 32 permanece como ponte contratual para parsers canonicos em rtd_option_quotes_excel_sync.py.
Nao ha troca de persistencia.
Nao ha troca operacional ampla.
Nao ha alteracao operacional do sync RTD.
utils/number_parser.py permanece como contrato canonico numerico.
utils/date_parser.py permanece como contrato canonico de datas.
Regra preservada: option_type canonico somente CALL/PUT por extenso; C/V sao compra/venda legado.
Nenhuma operacao de versionamento executada.
<!-- FIM FRENTE 32 V2 FIX GUARDRAIL FORBIDDEN LITERALS -->

<!-- INICIO FRENTE 32 V3 FIX REMAINING GUARDRAIL FORBIDDEN LITERALS -->
## Frente 32 v3 — Correção remanescente de literais proibidos no guardrail da Frente 32

Data local: 2026-07-31T19:44:21

Objetivo:
- Corrigir literais SQL DDL remanescentes no patch/guardrail local da Frente 32.
- Evitar falso positivo auto-referente nos testes da própria Frente 32.
- Preservar a ponte contratual para parsers canônicos numérico e de datas.

Escopo:
- ATT/patch_32_rtd_option_quotes_excel_sync_parser_bridge_contract.py
- ATT/tests/test_frente_32_rtd_option_quotes_excel_sync_parser_bridge_contract.py
- ATT/tests/test_frente_32_v3_fix_remaining_guardrail_forbidden_literals.py

Garantias:
- Sem troca de persistência.
- Sem troca operacional ampla.
- Sem alteração operacional do sync RTD.
- Sem comandos de versionamento.
- Regra preservada: option_type canônico somente CALL/PUT por extenso; C/V são compra/venda legado.
<!-- FIM FRENTE 32 V3 FIX REMAINING GUARDRAIL FORBIDDEN LITERALS -->

<!-- INICIO FRENTE 33 RTD OPTION QUOTES INTRADAY HISTORY PARSER BRIDGE CONTRACT -->
## Frente 33 — Ponte contratual dos parsers canonicos no historico intraday RTD

Data local: 2026-07-31T19:46:33

Arquivos tratados nesta frente:

- services/rtd_option_quotes_intraday_history_service.py
- utils/number_parser.py
- utils/date_parser.py
- ATT/tests/test_frente_33_rtd_option_quotes_intraday_history_parser_bridge_contract.py

Resumo:

- O historico intraday RTD passou a declarar uma ponte contratual para os parsers canonicos.
- Foram reconhecidos os contratos numericos parse_float_br, parse_optional_float, parse_positive_float e parse_percent.
- Foram reconhecidos os contratos de data parse_datetime_to_iso e parse_excel_date_to_iso.
- A frente prepara reducao futura de duplicacao de parser nos fluxos RTD intraday.

Garantias preservadas:

- Sem troca de persistencia.
- Sem troca de schema.
- Sem alteracao operacional da captura intraday.
- Sem troca de timezone operacional.
- Sem troca de regra de preco, bid, ask ou spread.
- Nenhuma operacao de versionamento foi executada.

Relatorio local:

- ATT/frente_33_rtd_option_quotes_intraday_history_parser_bridge_contract_report.json
<!-- FIM FRENTE 33 RTD OPTION QUOTES INTRADAY HISTORY PARSER BRIDGE CONTRACT -->
<!-- INICIO FRENTE 32 V3 FIX REMAINING GUARDRAIL FORBIDDEN LITERALS -->

## Frente 32 v3 — Correção remanescente dos literais proibidos no guardrail

### Status

Aplicada localmente e validada.

### Objetivo

Corrigir ocorrências remanescentes de literais proibidos no guardrail local da Frente 32, sem alterar o objetivo operacional original da frente.

A Frente 32 permanece focada em manter o sync RTD Option Quotes alinhado com os parsers canônicos de número e data, preservando a ponte contratual já criada para `utils/number_parser.py` e `utils/date_parser.py`.

### Correção aplicada

- Literais SQL DDL remanescentes do guardrail da Frente 32 foram sanitizados.
- Ocorrências corrigidas no patch da Frente 32: 2.
- Ocorrências corrigidas no teste da Frente 32: 2.
- Guardrail local v3 criado em `ATT/tests`.
- Documentos locais atualizados de forma idempotente.
- Ponte contratual para parsers canônicos preservada.

### Guardrails preservados

- Sem troca de persistência.
- Sem troca operacional ampla.
- Sem alteração operacional do sync RTD.
- Sem alteração de schema.
- Nenhuma operação de versionamento executada.
- Regra preservada: option_type canônico somente CALL/PUT por extenso; C/V são compra/venda legado.

### Validação local executada

Foram executados `py_compile` nos patches, testes, serviço de sync RTD e parsers canônicos envolvidos.

Teste específico da Frente 32 executado com sucesso:

- Resultado: 15 passed

Bateria incremental RTD Option Quotes das Frentes 21 a 32 executada com sucesso:

- Resultado: 121 passed

### Decisão aplicada

Correção local de guardrail, sem mudança funcional ampla e sem troca operacional.

<!-- FIM FRENTE 32 V3 FIX REMAINING GUARDRAIL FORBIDDEN LITERALS -->


<!-- INICIO FRENTE 33 RTD OPTION QUOTES INTRADAY HISTORY PARSER BRIDGE CONTRACT -->

## Frente 33 — Intraday History Service consumindo parsers canônicos

### Status

Aplicada localmente e validada.

### Objetivo

Dar continuidade à adoção incremental dos parsers canônicos em mais um consumidor específico do eixo RTD Option Quotes.

A Frente 33 registra ponte contratual no arquivo `services/rtd_option_quotes_intraday_history_service.py`, preservando `utils/number_parser.py` como contrato canônico numérico e `utils/date_parser.py` como contrato canônico de datas.

### Escopo aplicado

- Inclusão de ponte contratual local no `rtd_option_quotes_intraday_history_service.py`.
- Preservação do serviço de captura intraday sem alteração operacional ampla.
- Preservação de `utils/number_parser.py` como contrato canônico numérico.
- Preservação de `utils/date_parser.py` como contrato canônico de datas.
- Criação de guardrail local em `ATT/tests`.
- Documentos locais atualizados de forma idempotente.

### Guardrails preservados

- Sem troca de persistência.
- Sem troca de schema.
- Sem alteração operacional da captura intraday.
- Sem troca de timezone operacional.
- Nenhuma operação de versionamento executada.
- Regra preservada: option_type canônico somente CALL/PUT por extenso; C/V são compra/venda legado.

### Validação local executada

Foram executados `py_compile` no patch, teste, serviço intraday history e parsers canônicos envolvidos.

Teste específico da Frente 33 executado com sucesso:

- Resultado: 6 passed

Bateria incremental RTD Option Quotes das Frentes 21 a 33 executada com sucesso:

- Resultado: 127 passed

### Decisão aplicada

A Frente 33 mantém o padrão incremental das frentes anteriores: um consumidor por vez, ponte contratual pequena, local, testável e sem troca ampla de fluxo operacional.

<!-- FIM FRENTE 33 RTD OPTION_QUOTES_INTRADAY_HISTORY PARSER BRIDGE CONTRACT -->


<!-- INICIO FRENTE 34 RTD BRIDGE OPTION QUOTES PARSER BRIDGE CONTRACT -->

## Frente 34 — Bridge RTD Option Quotes consumindo parsers canônicos

### Status

Aplicada localmente e validada.

### Objetivo

Ampliar a adoção incremental dos parsers canônicos para o bridge RTD de Option Quotes, registrando ponte contratual no consumidor `rtd_bridge/excel_rtd_option_quotes_bridge.py`.

A Frente 34 preserva `utils/number_parser.py` como contrato canônico numérico e `utils/date_parser.py` como contrato canônico de datas, sem alterar o fluxo operacional do bridge RTD.

### Contexto da correção de alvo

A execução inicial da Frente 34 não localizou o arquivo alvo porque o patch buscava candidatos em `services`, enquanto o consumidor canônico já existente estava em:

- `rtd_bridge/excel_rtd_option_quotes_bridge.py`

A Frente 34 v3 corrigiu o patch de forma robusta, fazendo `_find_service()` reconhecer diretamente esse alvo canônico, sem depender da lista original de candidatos.

### Escopo aplicado

- Correção robusta do alvo da Frente 34 via early-return em `_find_service()`.
- Aplicação da ponte contratual no bridge RTD Option Quotes.
- Preservação dos parsers canônicos:
  - `utils/number_parser.py`;
  - `utils/date_parser.py`.
- Criação de guardrail local em `ATT/tests`.
- Documentos locais atualizados de forma idempotente.
- Relatórios locais gerados em `ATT`.

### Correção complementar v4

Após a aplicação da Frente 34, o guardrail local identificou literais proibidos autorreferentes dentro do próprio patch/teste da frente.

A Frente 34 v4 sanitizou esses literais proibidos do guardrail, preservando a validação sem manter os tokens diretos no fonte local.

Correção v4 aplicada:

- Literais proibidos autorreferentes do guardrail da Frente 34 sanitizados.
- Ocorrências sanitizadas/corrigidas: 4.
- Sem alteração operacional do bridge RTD.
- Sem alteração de persistência.
- Sem alteração de schema.
- Nenhuma operação de versionamento executada.

### Guardrails preservados

- Sem troca de persistência.
- Sem troca de schema.
- Sem alteração operacional do bridge RTD.
- Sem alteração operacional do sync RTD.
- Sem troca operacional ampla.
- Nenhuma operação de versionamento executada.
- Regra preservada: option_type canônico somente CALL/PUT por extenso; C/V são compra/venda legado.

### Validação local executada

Foram executados `py_compile` nos patches, bridge RTD e parsers canônicos envolvidos.

Teste específico da Frente 34 após correção v4 executado com sucesso:

- Resultado: 7 passed

Bateria incremental RTD Option Quotes das Frentes 21 a 34 executada com sucesso:

- Resultado: 134 passed

### Decisão aplicada

A Frente 34 conclui mais uma etapa incremental da convergência para parsers canônicos, mantendo o bridge RTD preservado operacionalmente e apenas registrando a ponte contratual necessária.

Não houve troca de persistência, schema, bridge operacional amplo, sync RTD ou regra financeira.

<!-- FIM FRENTE 34 RTD BRIDGE OPTION QUOTES PARSER BRIDGE CONTRACT -->


<!-- INICIO REGISTRO CONSOLIDADO FRENTES 32 A 34 -->

## Registro consolidado — Frentes 32 a 34

### Status

Aplicadas localmente e validadas.

### Consolidação

As Frentes 32, 33 e 34 deram continuidade à estratégia incremental de convergência do eixo RTD Option Quotes para contratos canônicos, com foco em parsers numéricos e de datas.

Foram preservados como contratos canônicos:

- `utils/number_parser.py`;
- `utils/date_parser.py`.

Consumidores alinhados nesta etapa:

- `services/rtd_option_quotes_excel_sync.py`;
- `services/rtd_option_quotes_intraday_history_service.py`;
- `rtd_bridge/excel_rtd_option_quotes_bridge.py`.

### Correções auxiliares aplicadas

- Frente 32 v3: sanitização de literais proibidos remanescentes no guardrail.
- Frente 34 v3: correção robusta do alvo canônico do bridge RTD.
- Frente 34 v4: sanitização de literais proibidos autorreferentes no guardrail.

### Resultado local consolidado

A bateria incremental RTD Option Quotes das Frentes 21 a 34 foi executada com sucesso:

- Resultado: 134 passed

### Decisão operacional preservada

- Sem troca de persistência.
- Sem troca de schema.
- Sem troca operacional ampla.
- Sem alteração operacional do sync RTD.
- Sem alteração operacional da captura intraday.
- Sem alteração operacional do bridge RTD.
- Sem troca de timezone operacional.
- Nenhuma operação de versionamento executada.
- Atualizações mantidas apenas localmente nos documentos de evolução até o encerramento geral das frentes.

### Regra financeira preservada

A regra financeira permanece inalterada:

- option_type canônico somente CALL/PUT por extenso.
- C/V são compra/venda legado.
- C e V não são tipo canônico de opção.
- Normalizações e pontes locais não podem alterar semântica financeira.

<!-- FIM REGISTRO CONSOLIDADO FRENTES 32 A 34 -->

<!-- INICIO FRENTE 35 RTD OPTION QUOTES SYNC SERVICE PARSER BRIDGE CONTRACT -->

## Frente 35 — RTD Option Quotes Sync Service consumindo contrato canonico de parsers

### Status

Aplicada localmente.

### Objetivo

Dar continuidade a centralizacao incremental dos parsers canonicos no eixo RTD Option Quotes, agora registrando ponte contratual em services/rtd_option_quotes_sync_service.py.

A Frente 35 preserva o sync service como ponto de orquestracao operacional e apenas registra dependencia preferencial dos contratos canonicos:

- utils/number_parser.py;
- utils/date_parser.py.

### Escopo aplicado

- Inclusao de ponte local declarativa em services/rtd_option_quotes_sync_service.py.
- Registro dos parsers numericos canonicos:
  - parse_float_br;
  - parse_optional_float;
  - parse_positive_float;
  - parse_percent.
- Registro dos parsers canonicos de data:
  - parse_excel_date_to_iso;
  - parse_datetime_to_iso.
- Criacao de guardrail local em ATT/tests.
- Documentacao local atualizada de forma idempotente.

### Limites preservados

- Sem troca de persistencia.
- Sem troca de schema.
- Sem alteracao operacional do sync RTD.
- Sem troca de fluxo de repository.
- Sem alteracao do bridge.
- Sem alteracao de importadores.
- Nenhuma operacao de versionamento executada.

### Regra financeira preservada

option_type canonico continua aceitando somente CALL/PUT por extenso.

C/V sao compra/venda legado.

C e V continuam sendo sinais legados de compra e venda, nao tipo canonico de opcao.

### Validacao recomendada

Executar py_compile nos arquivos afetados.

Executar o teste especifico da Frente 35.

Executar a bateria incremental RTD das Frentes 21 a 35.

### Observacao

Esta frente segue a diretriz incremental do plano: um consumidor por vez passa a reconhecer contratos canonicos compartilhados, sem refatoracao ampla e sem mudanca operacional abrupta.

<!-- FIM FRENTE 35 RTD OPTION QUOTES SYNC SERVICE PARSER BRIDGE CONTRACT -->

<!-- INICIO FRENTE 35 RTD OPTION QUOTES SYNC SERVICE PARSER BRIDGE CONTRACT -->

## Frente 35 — RTD Option Quotes Sync Service consumindo contrato canônico de parsers

### Status

Aplicada localmente e validada.

### Objetivo

Dar continuidade à consolidação incremental dos parsers canônicos de números e datas no eixo RTD Option Quotes, agora no consumidor:

services/rtd_option_quotes_sync_service.py

A Frente 35 registra uma ponte contratual local para que o sync service passe a reconhecer os contratos canônicos de parsing definidos em:

- utils/number_parser.py
- utils/date_parser.py

A alteração mantém o padrão das frentes anteriores: adoção pequena, local, testável e sem troca operacional abrupta.

### Escopo aplicado

- Inclusão de ponte contratual local em services/rtd_option_quotes_sync_service.py.
- Preservação de utils/number_parser.py como contrato canônico numérico.
- Preservação de utils/date_parser.py como contrato canônico de datas.
- Criação de guardrail local em ATT/tests/test_frente_35_rtd_option_quotes_sync_service_parser_bridge_contract.py.
- Geração de relatório local em ATT/frente_35_rtd_option_quotes_sync_service_parser_bridge_contract_report.json.
- Atualização documental local de forma idempotente.

### Limites preservados

- Sem troca de persistência.
- Sem troca de schema.
- Sem alteração operacional do sync RTD.
- Sem refatoração ampla.
- Sem mudança abrupta no fluxo de RTD Option Quotes.
- Nenhuma operação de versionamento executada.

### Regra financeira preservada

A Frente 35 não altera regra financeira nem contrato canônico de tipo de opção.

A regra permanece:

- option_type canônico somente CALL/PUT por extenso.
- C/V são compra/venda legado.
- C e V não são tipo canônico de opção.
- Pontes de parser não podem alterar semântica financeira.

### Validação local executada

Foi executada validação sintática dos arquivos afetados:

python -m py_compile ATT/patch_35_rtd_option_quotes_sync_service_parser_bridge_contract.py ATT/tests/test_frente_35_rtd_option_quotes_sync_service_parser_bridge_contract.py services/rtd_option_quotes_sync_service.py utils/number_parser.py utils/date_parser.py

Foi executado o teste específico da Frente 35:

python -m pytest ATT/tests/test_frente_35_rtd_option_quotes_sync_service_parser_bridge_contract.py -q

Resultado local:

6 passed

Também foi executada a bateria incremental RTD Option Quotes das Frentes 21 a 35:

Resultado local:

140 passed

### Decisão aplicada

A Frente 35 confirma a continuidade da estratégia de centralização incremental dos contratos compartilhados de RTD Option Quotes.

services/rtd_option_quotes_sync_service.py passa a registrar dependência contratual dos parsers canônicos, sem substituir fluxo operacional, sem trocar persistência e sem alterar schema.

A consolidação segue local até o encerramento geral das frentes, quando o documento consolidado será usado para atualização final no git.

<!-- FIM FRENTE 35 RTD OPTION QUOTES SYNC SERVICE PARSER BRIDGE CONTRACT -->

<!-- INICIO FRENTE 42 PRICING EXECUTION ENVELOPE CONTRACT -->
## Frente 42 - Pricing Execution Envelope Contract

Status: aplicada localmente.

Objetivo:
- iniciar a Fase 4 do plano efetivo;
- criar contrato canonico local para envelope de pricing;
- estabilizar as chaves status, error_message, pricing_payload, engine_result, persisted, pricing_execution_id, warnings e metadata;
- preparar a adocao gradual nos services de pricing sem alterar fluxo operacional existente.

Arquivos criados:
- services/pricing_execution_envelope.py;
- ATT/tests/test_frente_42_pricing_execution_envelope_contract.py;
- ATT/frente_42_pricing_execution_envelope_contract_report.json;
- ATT/verify_erros_frente_42.sh.

Evidencias:
- contrato com status permitido: ok, error, warning;
- persisted sempre contem record e snapshot_id;
- pricing_payload e engine_result sempre sao dicionarios;
- warnings sempre e lista;
- metadata sempre e dicionario.

Posicao no plano:
- Fase 4 iniciada;
- Fase 3 permanece avancada;
- Fase 6 segue apenas parcialmente antecipada pelas pontes de parser das Frentes 36 a 41.

Restricoes preservadas:
- Sem troca de persistencia;
- Sem troca de schema;
- Sem alteracao operacional ampla;
- Nenhuma operacao de versionamento executada.
<!-- FIM FRENTE 42 PRICING EXECUTION ENVELOPE CONTRACT -->

## Frente 42 - Pricing execution envelope contract

- Status: aplicada localmente.
- Fase: Fase 4 - Pricing e payoff.
- Objetivo: criar contrato canonico para envelope de retorno do pricing.
- Resultado: Envelope canonico de pricing criado em services/pricing_execution_envelope.py.
- Teste local: ATT/tests/test_frente_42_pricing_execution_envelope_contract.py.
- Relatorio local: ATT/frente_42_pricing_execution_envelope_contract_report.json.
- Sem troca de persistencia.
- Sem troca de schema.
- Sem alteracao operacional ampla.
- Nenhuma operacao de versionamento executada.

Observacao:
- A antecipacao parcial entre Fase 3 e Fase 6 ficou limitada a normalizacao/parser.
- A Frente 42 reposiciona a execucao na Fase 4, sem alterar banco, schema ou fluxo operacional amplo.
\n
## Frente 43 — Integracao envelope canonico fluxo pricing

- Frente 43 aplicada localmente.
- Integracao envelope canonico fluxo pricing.
- Fase 4 - Pricing e payoff.
- Objetivo: iniciar integracao controlada do envelope canonico criado na Frente 42 nos services de pricing.
- Arquivos alvo:
  - services/pricing_execution_orchestration_service.py
  - services/pricing_execution_app_service.py
- Sem troca de persistencia.
- Sem troca de schema.
- Sem alteracao operacional ampla.
- Nenhuma operacao de versionamento executada.

## Frente 43 v2 - correcao de literal backslash-n

- Frente: 43 v2.
- Ajuste: remocao de linha literal backslash-n isolada inserida nos arquivos do fluxo de pricing.
- Arquivos conferidos:
  - services/pricing_execution_orchestration_service.py
  - services/pricing_execution_app_service.py
- Objetivo: restaurar py_compile e importacao dos adaptadores da Frente 43.
- Sem troca de persistencia.
- Sem troca de schema.
- Sem alteracao operacional ampla.
- Nenhuma operacao de versionamento executada.
- Proxima frente mantida: Frente 44 - propagacao controlada envelope retorno pricing.
- Gerado em: 2026-07-31T21:51:53.

## Frente 44 - Propagacao controlada envelope retorno pricing

- Status: aplicada localmente.
- Fase: Fase 4 - Pricing e payoff.
- Objetivo: propagar retorno de pricing no envelope canonico minimo nos services de pricing.
- Escopo: controlado, local e reversivel.
- Sem troca de persistencia.
- Sem troca de schema.
- Sem alteracao operacional ampla.
- Nenhuma operacao de versionamento executada.
- Observacao: mantem a sobreposicao anterior apenas como registro documental de normalizacao/parser, sem ampliar escopo.
\n## Frente 45 - Estabilizacao envelope query retorno pricing

- Frente 45
- Estabilizacao envelope query retorno pricing
- Fase 4 - Pricing e payoff
- Objetivo: estabilizar retornos de consulta de pricing no envelope canonico minimo.
- Arquivo alvo: services/pricing_execution_query_service.py
- Contrato preservado: status, error_message, pricing_payload, engine_result, persisted e pricing_execution_id.
- Sem troca de persistencia
- Sem troca de schema
- Sem alteracao operacional ampla
- Nenhuma operacao de versionamento executada
- Observacao: esta frente apenas cria adaptador conservador de retorno para query, sem alterar banco, repository ou fluxo de gravacao.\n

## Frente 45 v2 - Fix literal backslash-n query envelope

- Frente 45 v2
- Fix literal backslash-n query envelope
- Corrigido SyntaxError causado por bloco com `\n` literal em `services/pricing_execution_query_service.py`.
- Guardrail ajustado para procurar backslash-n literal, sem bloquear quebras de linha normais.
- Sem troca de persistencia.
- Sem troca de schema.
- Sem alteracao operacional ampla.
- Nenhuma operacao de versionamento executada.

## Frente 46 - Porta PricingEngine controlada

- Frente 46 aplicada localmente.
- Porta PricingEngine controlada criada em `services/pricing_engine_port.py`.
- Contrato `PricingEnginePort` formalizado com metodo `run(pricing_payload) -> dict`.
- Helper `run_pricing_engine()` criado para chamada controlada do motor.
- `PricingEngineStub` permanece disponivel apenas para desenvolvimento/teste.
- Sem troca de engine real.
- Sem troca de persistencia.
- Sem troca de schema.
- Sem alteracao operacional ampla.
- Nenhuma operacao de versionamento executada.

## Frente 47 - Fortalecimento validacao payload pricing payoff

- Frente 47 aplicada localmente.
- Fortalecimento validacao payload pricing payoff.
- Criado modulo `services/pricing_payoff_payload_validation.py`.
- Criadas validacoes controladas para payload minimo de pricing/payoff.
- CALL/PUT nao possui default perigoso.
- Position side nao possui default perigoso.
- Campo `price` e tratado como ambiguo e gera warning, preservando separacao entre `premium`, `entry_premium` e `current_price`.
- Esta frente apenas valida e retorna diagnostico estruturado.
- Sem troca de persistencia.
- Sem troca de schema.
- Sem alteracao operacional ampla.
- Nenhuma operacao de versionamento executada.

## Frente 48 - Validacao controlada payoff calculation request

- Status: aplicada localmente.
- Fase: Fase 4 - Pricing e payoff.
- Escopo: fortalecimento controlado do contrato de entrada de payoff em `domain/calculation_request.py`.
- Tokens: Validacao controlada payoff calculation request; calculation_request; payoff validation.
- Sem troca de persistencia.
- Sem troca de schema.
- Sem alteracao operacional ampla.
- Nenhuma operacao de versionamento executada.

## Frente 49 - Correcao pontual bugs UI fluxo payoff

- Status: aplicada localmente.
- Fase: Fase 5 - UI e command services.
- Escopo: correcoes pontuais no fluxo de UI/payoff, sem refatoracao pesada.
- Alvos controlados: `decisions_dark_panel`, `decisions_grid`, `terminal_vwap_payoff_dark_panel` e `ui_data`.
- Sem troca de persistencia.
- Sem troca de schema.
- Sem alteracao operacional ampla.
- Nenhuma operacao de versionamento executada.

## Frente 50 - Reducao SQL direto UI services criticos

- Status: aplicada localmente.
- Fase: Fase 5 - UI e command services.
- Escopo: inventario controlado de SQL direto em UI/services criticos.
- Artefato criado: `services/sql_direct_usage_inventory.py`.
- Saida criada: `ATT/frente_50_sql_direto_ui_services_inventory.json`.
- Objetivo: mapear ocorrencias para reducao posterior por repositories/services.
- Sem troca de persistencia.
- Sem troca de schema.
- Sem alteracao operacional ampla.
- Nenhuma operacao de versionamento executada.
## Frente 51 - Reduzir SQL direto payoff UI services por prioridade

- Status: aplicada localmente.
- Escopo: priorizacao dos pontos de SQL direto em payoff/UI/services a partir do inventario da Frente 50.
- Artefatos:
  - services/sql_direct_usage_prioritizer.py
  - ATT/frente_51_sql_direto_payoff_ui_services_priority.json
  - ATT/tests/test_frente_51_reduzir_sql_direto_payoff_ui_services_por_prioridade.py
- Objetivo: organizar reducao incremental de SQL direto por prioridade sem alterar comportamento em runtime.
- Sem troca de persistencia.
- Sem troca de schema.
- Sem alteracao operacional ampla.
- Nenhuma operacao de versionamento executada.

<!-- INICIO FRENTE 51 VALIDACAO LOCAL HOTFIX 51D -->

## Frente 51 — Validação local consolidada da priorização de SQL direto payoff UI/services

### Status

Aplicada localmente e validada.

### Objetivo

Consolidar documentalmente a validação da Frente 51, cujo objetivo é reduzir
SQL direto em UI/services relacionados a payoff por meio de inventário técnico
priorizado, sem executar migração de schema, sem troca de persistência e sem
alteração operacional ampla.

### Escopo validado

A Frente 51 estabilizou a priorização técnica em:

- services/sql_direct_usage_prioritizer.py
- ATT/frente_51_sql_direto_payoff_ui_services_priority.json
- ATT/tests/test_frente_51_reduzir_sql_direto_payoff_ui_services_por_prioridade.py

Também foi aplicado o hotfix local 51d para evitar travamento na análise de
prefixos literais e reduzir falso positivo Python na detecção de SQL direto.

### Correção local aplicada

O hotfix 51d substituiu a lógica problemática de remoção de prefixos literais
por implementação sem loop, evitando travamento na inspeção de campos preview.

A correção preserva o objetivo da Frente 51:

- inventariar candidatos de SQL direto;
- classificar por prioridade;
- diferenciar candidatos relacionados a payoff, UI e services;
- manter a mudança como diagnóstico/priorização, sem migração funcional ampla.

### Resultado local validado

Comando de verificação executado:

    bash ATT/verify_erros_frente_51.sh

Resultado:

    Nenhum erro detectado pelo verificador da Frente 51.

Validações observadas:

- py_compile da Frente 51 concluído com sucesso.
- JSON de relatório da Frente 51 válido.
- JSON de prioridade da Frente 51 válido.
- pytest direcionado da Frente 51 concluído com sucesso.
- Resultado do pytest direcionado: 5 passed.
- Tokens documentais conferidos nos documentos locais.

Inventário priorizado após hotfix 51d:

- Total candidates: 29
- Priority counts:
  - P0: 18
  - P1: 5
  - P2: 5
  - P3: 1

### Guardrails preservados

- Sem troca de persistência.
- Sem troca de schema.
- Sem alteração operacional ampla.
- Nenhuma operação de versionamento executada.
- Sistema permanece local.
- Patches e temporários permanecem em ATT.
- Testes permanecem em ATT/tests.
- Documentação local atualizada para manter rastreabilidade até o encerramento geral das frentes.

### Próxima frente

Próxima frente mantida:

- Frente 52 — reduzir SQL direto em candidatos P0/P1 sem mudar contratos.

### Observação

A Frente 51 não remove ainda os SQLs diretos dos arquivos candidatos. Ela cria
a base priorizada para orientar a retirada incremental posterior, especialmente
nos candidatos P0 e P1, mantendo o padrão de alteração pequena, local,
testável e sem git até o encerramento geral.

<!-- FIM FRENTE 51 VALIDACAO LOCAL HOTFIX 51D -->
<!-- INICIO FRENTE 52 REFINAR PRIORIZACAO SQL DIRETO P0 P1 -->

## Frente 52 — Refinar priorização de SQL direto P0/P1 sem alterar contratos

### Status

Aplicada localmente.

### Objetivo

Refinar o inventário priorizado produzido na Frente 51 para reduzir falso-positivos
antes da retirada incremental de SQL direto em UI/services relacionados a payoff.

A Frente 52 atua somente sobre a classificação técnica dos candidatos. Ela não remove
SQL direto de arquivos operacionais, não cria schema, não troca persistência e não
altera fluxo operacional amplo.

### Escopo aplicado

- Entrada analisada: `ATT/frente_51_sql_direto_payoff_ui_services_priority.json`.
- Saída refinada: `ATT/frente_52_sql_direto_payoff_ui_services_priority_refined.json`.
- Remoção de falso-positivos evidentes:
  - `.join(...)` de Python sem SQL real;
  - `.update(...)` de dicionário/widget sem `UPDATE` SQL;
  - `.insert(...)` de UI/Python sem `INSERT INTO`;
  - `.select(...)` de métodos/selectors sem `SELECT` SQL.
- Criação de guardrail local em `ATT/tests/test_frente_52_refinar_priorizacao_sql_direto_p0_p1.py`.
- Criação de relatório local em `ATT/frente_52_refinar_priorizacao_sql_direto_p0_p1_report.json`.

### Resultado local esperado

Inventário refinado:

- Total de candidatos após refinamento: 15.
- P0: 12.
- P1: 0.
- P2: 3.
- P3: 0.
- Achados removidos como falso-positivo: 54.

### Guardrails preservados

- Sem troca de persistencia.
- Sem troca de schema.
- Sem alteracao operacional ampla.
- Nenhuma operacao de versionamento executada.
- Sem criacao de pasta nova na raiz.
- Patches e temporarios permanecem em `ATT`.
- Testes permanecem em `ATT/tests`.

### Próxima etapa sugerida

Após validar a Frente 52, a próxima frente deve atacar somente os candidatos P0/P1
remanescentes que tenham SQL direto real, um arquivo por vez, preferencialmente
começando por UI/components/details_panel.py ou UI/models/ui_data.py, sem mudar
schema, persistência ou contratos públicos.

<!-- FIM FRENTE 52 REFINAR PRIORIZACAO SQL DIRETO P0 P1 -->

## Frente 53 — Reduzir SQL direto real P0 sem alterar contratos

Status: preparada para execução técnica local.

A Frente 53 parte do inventário refinado da Frente 52:

- Fonte: `ATT/frente_52_sql_direto_payoff_ui_services_priority_refined.json`
- Relatório de pré-checagem: `ATT/frente_53_reduzir_sql_direto_p0_precheck_report.json`
- Teste de pré-checagem: `ATT/tests/test_frente_53_reduzir_sql_direto_p0_precheck.py`
- Total de candidatos refinados encontrados: 15
- Candidatos P0 encontrados: 12
- Primeiro alvo sugerido: `UI\components\terminal_vwap_payoff_dark_panel.py`

Escopo permitido:

- Reduzir SQL direto somente em candidatos reais classificados como P0.
- Preservar contratos públicos.
- Não alterar schema.
- Não alterar comportamento operacional.
- Não fazer versionamento.

Critério para a próxima etapa:

- Escolher um único candidato P0.
- Aplicar patch mínimo e reversível.
- Criar teste específico validando ausência de regressão contratual.
- Atualizar relatório da Frente 53 com antes/depois.<!-- INICIO FRENTE 53A VALIDACAO LOCAL DERIVED REPO PAYOFF PANEL -->

## Frente 53a — Terminal VWAP Payoff Dark Panel consumindo derived_repo

### Status

Aplicada localmente e validada.

### Contexto

A Frente 53a deu continuidade à Frente 53, que iniciou a redução controlada de SQL direto real P0 em UI/services relacionados a payoff.

O primeiro alvo técnico permaneceu o arquivo:

- UI/components/terminal_vwap_payoff_dark_panel.py

A alteração foi feita de forma local, incremental e reversível, preservando o contrato operacional do painel Terminal VWAP/Payoff.

### Objetivo

Reduzir SQL direto no painel Terminal VWAP/Payoff para os pontos relacionados a:

- payoff_curve_points;
- structure_decisions.

A UI passou a preferir métodos consolidados em db/derived_repo.py, evitando acesso direto da camada de interface às tabelas sensíveis de payoff e decisões.

### Escopo aplicado

- Remoção de import sqlite3 do painel Terminal VWAP/Payoff Dark Panel.
- Remoção de SQL direto contra structure_decisions no painel.
- Remoção de SQL direto contra payoff_curve_points no bloco inspecionado pelo guardrail da Frente 53a.
- Preservação da ponte local com db/derived_repo.py.
- Preservação do comportamento operacional do painel.
- Sem alteração de schema.
- Sem troca de persistência.
- Sem alteração operacional ampla.
- Nenhuma operação de versionamento executada.

### Validação local executada

Foram executadas validações locais direcionadas com sucesso.

Comando de compilação:

    python -m py_compile UI/components/terminal_vwap_payoff_dark_panel.py db/derived_repo.py

Teste específico da Frente 53a:

    python -m pytest ATT/tests/test_frente_53a_terminal_vwap_payoff_dark_panel_derived_repo_usage.py -q

Resultado:

    4 passed

Bateria direcionada do Terminal VWAP/Payoff:

    python -m pytest ATT/tests/test_frente_53a_terminal_vwap_payoff_dark_panel_derived_repo_usage.py ATT/tests/test_terminal_vwap_payoff_dark_panel_app_service_integration.py ATT/tests/test_terminal_vwap_payoff_dark_panel_operational_states.py ATT/tests/test_terminal_vwap_payoff_controller.py ATT/tests/test_terminal_vwap_payoff_app_service.py -q

Resultado:

    49 passed

### Guardrails preservados

- Sem git nesta etapa.
- Sem criação de pasta nova na raiz.
- Patches e relatórios permanecem em ATT.
- Testes permanecem em ATT/tests.
- Sistema permanece 100 por cento local.
- UI não deve acessar diretamente payoff_curve_points nem structure_decisions para os pontos cobertos pela Frente 53a.
- A continuidade da redução de SQL direto deve seguir um arquivo por vez, com teste específico.

### Posição do projeto após a Frente 53a

O projeto permanece na Fase 5 — UI e command services, dentro do eixo de redução incremental de SQL direto fora de repositories.

A Frente 53a conclui a primeira retirada validada no alvo P0 Terminal VWAP/Payoff Dark Panel. A próxima etapa técnica recomendada é continuar a Frente 53 em novo recorte pequeno, preferencialmente como Frente 53b, escolhendo apenas um próximo candidato P0 real do inventário refinado da Frente 52.

Candidatos naturais para análise seguinte, conforme o plano consolidado, são:

- UI/components/details_panel.py
- UI/models/ui_data.py

A escolha deve ser feita somente após nova pré-checagem local, preservando contratos públicos, sem alteração de schema, sem troca de persistência e sem git até o encerramento geral das frentes.

<!-- FIM FRENTE 53A VALIDACAO LOCAL DERIVED REPO PAYOFF PANEL -->

<!-- INICIO FRENTE 53B SELECT NEXT P0 SQL DIRECT TARGET -->

## Frente 53b — Seleção do próximo alvo P0 real para redução de SQL direto

### Status

Preparada localmente por patch automatizado e pendente de validação local.

### Objetivo

Dar continuidade à Frente 53 após a conclusão validada da Frente 53a, mantendo a
redução incremental de SQL direto real em UI/services relacionados a payoff.

A Frente 53b não altera código operacional. Ela seleciona o próximo alvo P0 real
com base no inventário refinado da Frente 52 e na inspeção local do fonte atual.

### Resultado da seleção local

- Inventário de origem: ATT/frente_52_sql_direto_payoff_ui_services_priority_refined.json
- Alvo já tratado e excluído da seleção: UI/components/terminal_vwap_payoff_dark_panel.py
- Próximo alvo selecionado: UI/components/details_panel.py
- Linhas com evidência de SQL direto no alvo selecionado: 23
- Total de candidatos P0 reais encontrados para continuidade: 14

### Escopo preservado

- Sem troca de persistência.
- Sem troca de schema.
- Sem alteração operacional ampla.
- Nenhuma operação de versionamento executada.
- Sem criação de pasta nova na raiz.
- Patch e relatório permanecem em ATT.
- Teste permanece em ATT/tests.
- Sistema permanece 100 por cento local.

### Próxima etapa recomendada

Após validar esta seleção, executar a retirada incremental no alvo selecionado como
um patch pequeno e reversível, preferindo repository/service já existente sempre que
possível e criando guardrail específico para impedir regressão.

<!-- FIM FRENTE 53B SELECT NEXT P0 SQL DIRECT TARGET -->

<!-- INICIO FRENTE 53B VALIDACAO LOCAL DETAILS PANEL DERIVED REPO USAGE -->

## Frente 53b — DetailsPanel consumindo derived_repo para payoff local

### Status

Aplicada localmente e validada.

### Contexto

A Frente 53b deu continuidade à Frente 53, após a Frente 53a ter removido SQL direto
do painel Terminal VWAP/Payoff Dark Panel para os pontos cobertos por payoff e decisões.

O novo recorte técnico foi o arquivo:

- UI/components/details_panel.py

A alteração seguiu a seleção local já registrada para a Frente 53b, usando como alvo
o próximo candidato P0 real do inventário refinado da Frente 52.

### Objetivo

Reduzir SQL direto no DetailsPanel para os pontos relacionados a:

- leitura da decisão mais recente da estrutura;
- leitura dos pontos de payoff por structure_id;
- leitura de auditoria mínima de payoff por structure_id.

A UI passou a delegar essas leituras para db/derived_repo.py, preservando o banco
SQLite local e evitando que a camada de interface consulte diretamente as tabelas
sensíveis de payoff e decisões nesse recorte.

### Escopo aplicado

- UI/components/details_panel.py passou a consumir db.derived_repo para:
  - get_latest_structure_decision;
  - get_payoff_curve_points_by_structure_id;
  - get_structure_payoff_audit_info.
- db/derived_repo.py recebeu funções locais de leitura para atender o DetailsPanel.
- ATT/tests/test_frente_53b_details_panel_derived_repo_usage.py foi criado como guardrail
  específico da frente.
- ATT/frente_53b_details_panel_derived_repo_usage_report.json foi gerado como relatório
  local da frente.
- Nenhuma migração Web foi feita.
- Nenhum HTTP foi introduzido.
- Nenhuma API externa foi introduzida.
- Nenhuma troca de persistência foi feita.
- Nenhuma alteração de schema foi feita.
- Nenhuma alteração operacional ampla foi feita.
- Nenhuma operação de versionamento foi executada.

### Validação local executada

Compilação executada com sucesso:

    python -m py_compile UI/components/details_panel.py db/derived_repo.py ATT/repair_53b_details_panel_no_web_local_only.py

Teste específico da Frente 53b executado com sucesso:

    python -m pytest ATT/tests/test_frente_53b_details_panel_derived_repo_usage.py -q

Resultado:

    6 passed

Bateria direcionada de regressão executada com sucesso:

    python -m pytest ATT/tests/test_frente_53a_terminal_vwap_payoff_dark_panel_derived_repo_usage.py ATT/tests/test_frente_53b_details_panel_derived_repo_usage.py ATT/tests/test_terminal_vwap_payoff_dark_panel_app_service_integration.py ATT/tests/test_terminal_vwap_payoff_dark_panel_operational_states.py ATT/tests/test_terminal_vwap_payoff_controller.py ATT/tests/test_terminal_vwap_payoff_app_service.py -q

Resultado:

    55 passed

Verificação local contra dependências Web/HTTP/API externa nos arquivos operacionais:

    grep -RInE "import requests|from requests|import httpx|from httpx|import aiohttp|from aiohttp|urllib.request|urlopen\(|socket.create_connection|websocket|fastapi|flask|django" UI/components/details_panel.py db/derived_repo.py

Resultado:

    Nenhuma ocorrência encontrada nos arquivos operacionais verificados.

### Observação sobre o guardrail

O teste da Frente 53b contém strings textuais com tokens proibidos para validar ausência
de Web/HTTP/API externa nos alvos operacionais. Por isso, buscas amplas que incluam o
arquivo de teste podem encontrar esses tokens no próprio guardrail. A verificação
operacional correta foi feita somente sobre:

- UI/components/details_panel.py
- db/derived_repo.py

E ficou limpa.

### Guardrails preservados

- Sistema permanece 100 por cento local.
- Sem Web.
- Sem HTTP.
- Sem API externa.
- Sem troca de persistência.
- Sem troca de schema.
- Sem alteração operacional ampla.
- Sem criação de pasta nova na raiz.
- Patches e relatórios permanecem em ATT.
- Testes permanecem em ATT/tests.
- Sem git nesta etapa.
- A consolidação em git fica reservada para o encerramento geral das frentes.

### Posição do projeto após a Frente 53b

A Frente 53b conclui mais um recorte incremental da redução de SQL direto real P0
em UI/services relacionados a payoff.

O projeto permanece na Fase 5 — UI e command services, seguindo a regra de avançar
um arquivo por vez, com patch pequeno, reversível e testável.

A próxima etapa técnica recomendada é continuar a Frente 53 em novo recorte pequeno,
preferencialmente avaliando outro candidato P0 real do inventário refinado da Frente 52,
como UI/models/ui_data.py, antes de qualquer refatoração ampla.

<!-- FIM FRENTE 53B VALIDACAO LOCAL DETAILS PANEL DERIVED REPO USAGE -->

<!-- INICIO FRENTE 53C VALIDACAO LOCAL PAYOFF REPO BRIDGE -->

## Frente 53c — Terminal VWAP Payoff Dark Panel com payoff persistido via derived_repo

### Status

Aplicada localmente e validada.

### Contexto

A Frente 53c deu continuidade à redução incremental de SQL direto real P0 em UI/services
relacionados a payoff, mantendo o mesmo padrão das Frentes 53a e 53b:

- um recorte pequeno por vez;
- alteração local e reversível;
- preservação de contratos públicos;
- sem troca de persistência;
- sem alteração de schema;
- sem migração para Web;
- sem execução de git.

O alvo técnico desta frente foi novamente o arquivo:

- UI/components/terminal_vwap_payoff_dark_panel.py

O recorte aplicado foi específico sobre o método:

- _load_persisted_payoff_points

### Objetivo

Remover SQL direto do carregamento de pontos persistidos de payoff no painel Terminal
VWAP/Payoff Dark Panel, fazendo o método _load_persisted_payoff_points consumir a ponte
local existente em db/derived_repo.py.

A função utilizada como ponte canônica foi:

- derived_repo.get_payoff_curve_points_by_structure_id

### Escopo aplicado

- Substituição do carregamento direto de payoff persistido por chamada ao derived_repo.
- Preservação da identificação por structure_id.
- Normalização defensiva dos pontos retornados no formato spot/pl.
- Preservação da ordenação por spot.
- Preservação do caminho canônico UI.
- Nenhuma pasta ui minúscula foi criada.
- Nenhum import operacional por ui minúsculo foi introduzido.
- Nenhuma chamada Web foi introduzida.
- Nenhum HTTP foi introduzido.
- Nenhuma API externa foi introduzida.
- Nenhuma alteração de schema foi feita.
- Nenhuma troca de persistência foi feita.
- Nenhuma alteração operacional ampla foi feita.
- Nenhuma operação de versionamento foi executada.

### Artefatos locais

- Patch: ATT/patch_53c_terminal_dark_panel_payoff_repo_bridge.py
- Teste: ATT/tests/test_frente_53c_terminal_dark_panel_payoff_repo_bridge.py
- Relatório: ATT/frente_53c_terminal_dark_panel_payoff_repo_bridge_report.json
- Backup: ATT/backup_before_53c_terminal_dark_panel_payoff_repo_bridge_20260803_203237_UI__components__terminal_vwap_payoff_dark_panel.py

### Validação local executada

Foram executadas validações locais com sucesso.

Compilação do patch, alvo operacional, repository e teste:

    python -m py_compile ATT/patch_53c_terminal_dark_panel_payoff_repo_bridge.py

    python -m py_compile UI/components/terminal_vwap_payoff_dark_panel.py db/derived_repo.py ATT/tests/test_frente_53c_terminal_dark_panel_payoff_repo_bridge.py

Execução do patch:

    python ATT/patch_53c_terminal_dark_panel_payoff_repo_bridge.py

Resultado do patch:

- OK: Frente 53c aplicada localmente.
- target: UI\components\terminal_vwap_payoff_dark_panel.py
- test: ATT\tests\test_frente_53c_terminal_dark_panel_payoff_repo_bridge.py
- relatorio: ATT\frente_53c_terminal_dark_panel_payoff_repo_bridge_report.json
- git: nao executado
- guardrail: sistema local, sem Web, sem HTTP, sem API externa

Teste específico da Frente 53c:

    python -m pytest ATT/tests/test_frente_53c_terminal_dark_panel_payoff_repo_bridge.py -q

Resultado:

    3 passed

Bateria direcionada de regressão das Frentes 53a, 53b, 53c e Terminal VWAP/Payoff:

    python -m pytest ATT/tests/test_frente_53a_terminal_vwap_payoff_dark_panel_derived_repo_usage.py ATT/tests/test_frente_53b_details_panel_derived_repo_usage.py ATT/tests/test_frente_53c_terminal_dark_panel_payoff_repo_bridge.py ATT/tests/test_terminal_vwap_payoff_dark_panel_app_service_integration.py ATT/tests/test_terminal_vwap_payoff_dark_panel_operational_states.py ATT/tests/test_terminal_vwap_payoff_controller.py ATT/tests/test_terminal_vwap_payoff_app_service.py -q

Resultado:

    58 passed

### Evidência do relatório local

O relatório local da Frente 53c registrou:

- status: aplicada_localmente;
- alvo: UI\components\terminal_vwap_payoff_dark_panel.py;
- método: _load_persisted_payoff_points;
- old_had_execute: true;
- new_uses_derived_repo: true;
- forbidden_sql_after: lista vazia;
- canonical_path: UI;
- has_exact_UI: true;
- has_exact_lower_ui: false;
- case_policy: caminho canonico UI preservado; sem criar/importar ui lowercase;
- git: nao executado.

### Observação sobre o scanner 53c

Após o encerramento da Frente 53c, o scanner local identificou 66 candidatos gerais com
possíveis ocorrências de SQL/Web direto ou tokens relacionados.

Esse scanner é amplo e inclui:

- repositories;
- migrations;
- scripts;
- diagnósticos;
- falsos positivos textuais;
- arquivos já parcialmente tratados;
- arquivos onde SQL é esperado por camada.

Portanto, o resultado do scanner não deve ser tratado como regressão automática da Frente
53c. A leitura correta é usá-lo como base para selecionar o próximo recorte pequeno e
validável, mantendo a regra de um arquivo por vez.

### Próxima frente recomendada

A próxima frente técnica recomendada é:

- Frente 53d — Pré-checagem e redução incremental de SQL direto em UI/models/ui_data.py

Justificativa:

- UI/models/ui_data.py aparece como candidato HIGH no scanner local da Frente 53c.
- O Plano de Contenção Consolidado já indicava UI/models/ui_data.py como candidato natural
  após DetailsPanel.
- O Plano Efetivo Inicial cita UIDataModel.get_payoff_curve como ponto de risco por acesso
  direto ao SQLite e possível vazamento de conexão.
- O alvo segue dentro da Fase 5 — UI e command services.
- O recorte deve ser precedido por pré-checagem local para distinguir SQL real de falso
  positivo textual.

### Guardrails preservados

- Sistema permanece 100 por cento local.
- Sem Web.
- Sem HTTP.
- Sem API externa.
- Sem troca de persistência.
- Sem alteração de schema.
- Sem alteração operacional ampla.
- Sem criação de pasta nova na raiz.
- Patches e relatórios permanecem em ATT.
- Testes permanecem em ATT/tests.
- Sem git nesta etapa.
- Caminho canônico UI preservado.

<!-- FIM FRENTE 53C VALIDACAO LOCAL PAYOFF REPO BRIDGE -->

<!-- INICIO FRENTE 37 RTD OPTION QUOTES INTRADAY CANDLE CHART PARSER BRIDGE CONTRACT -->

## Frente 37 — RTD Option Quotes Intraday Candle Chart Service Parser Bridge Contract

### Status

Aplicada localmente e validada.

### Objetivo

Consolidar ponte controlada de parser para o service de chart de candles intraday
de RTD Option Quotes, preservando o contrato local e evitando duplicacao de
normalizacao numerica e temporal.

### Escopo aplicado

- Arquivo alvo: rtd_option_quotes_intraday_candle_chart_service.py.
- Uso controlado de parser bridge para dados intraday candle chart.
- Preservacao de compatibilidade com o fluxo local existente.
- Uso de utils/number_parser.py para normalizacao numerica.
- Uso de utils/date_parser.py para normalizacao temporal.
- Sem troca de persistencia.
- Sem troca de schema.
- Sem alteracao operacional ampla.
- Nenhuma operacao de git executada.

### Guardrails preservados

- Sistema permanece local.
- Sem Web.
- Sem HTTP.
- Sem API externa.
- Sem versionamento nesta etapa.

<!-- FIM FRENTE 37 RTD OPTION QUOTES INTRADAY CANDLE CHART SERVICE PARSER BRIDGE CONTRACT -->

<!-- INICIO FRENTE 37 V3 FIX GUARDRAIL MARKER NORMALIZATION -->

## Frente 37 v3 — Fix guardrail marker normalization

### Status

Aplicada localmente.

### Objetivo

Registrar a correcao documental da Frente 37 v3 para estabilizar o guardrail de
normalizacao de marcadores.

### Correção aplicada

- Frente 37 v3 registrada nos documentos locais.
- normalizacao case-insensitive preservada para marcadores documentais.
- Guardrail documental alinhado sem alterar codigo operacional.
- Sem troca de persistencia.
- Sem troca de schema.
- Sem alteracao operacional ampla.
- Nenhuma operacao de git executada.

<!-- FIM FRENTE 37 V3 FIX GUARDRAIL MARKER NORMALIZATION -->

<!-- INICIO FRENTE 38 RTD OPTION QUOTES INTRADAY CANDLE REPOSITORY PARSER BRIDGE CONTRACT -->

## Frente 38 — RTD Option Quotes Intraday Candle Repository Parser Bridge Contract

### Status

Aplicada localmente e validada.

### Objetivo

Consolidar ponte controlada de parser para o repository de candles intraday de
RTD Option Quotes, mantendo a normalizacao local antes do consumo pelas camadas
superiores.

### Escopo aplicado

- Arquivo alvo: rtd_option_quotes_intraday_candle_repository.py.
- Ponte local com parser bridge para dados intraday candle.
- Preservacao do contrato de repository.
- Uso de utils/number_parser.py para normalizacao numerica.
- Uso de utils/date_parser.py para normalizacao temporal.
- Sem troca de persistencia.
- Sem troca de schema.
- Sem alteracao operacional ampla.
- Nenhuma operacao de git executada.

### Guardrails preservados

- Sistema permanece local.
- Sem Web.
- Sem HTTP.
- Sem API externa.
- Sem versionamento nesta etapa.

<!-- FIM FRENTE 38 RTD OPTION QUOTES INTRADAY CANDLE REPOSITORY PARSER BRIDGE CONTRACT -->

<!-- INICIO FRENTE 38 V2 FIX REPORT TARGET PATH NORMALIZATION -->

## Frente 38 v2 — Fix report target path normalization

### Status

Aplicada localmente.

### Objetivo

Registrar a correcao documental da Frente 38 v2 para estabilizar o guardrail de
normalizacao de caminho do target no relatorio local.

### Correção aplicada

- Frente 38 v2 registrada nos documentos locais.
- normalizacao posix do target preservada nos relatorios e documentos locais.
- Guardrail documental alinhado sem alterar codigo operacional.
- Sem troca de persistencia.
- Sem troca de schema.
- Sem alteracao operacional ampla.
- Nenhuma operacao de git executada.

<!-- FIM FRENTE 38 V2 FIX REPORT TARGET PATH NORMALIZATION -->

<!-- INICIO FRENTE 39 RTD OPTION QUOTES INTRADAY HISTORY REPOSITORY PARSER BRIDGE CONTRACT -->

## Frente 39 — RTD Option Quotes Intraday History Repository Parser Bridge Contract

### Status

Aplicada localmente e validada.

### Objetivo

Consolidar ponte controlada de parser para o repository de historico intraday de
RTD Option Quotes, preservando normalizacao numerica e temporal em ponto
reutilizavel.

### Escopo aplicado

- Arquivo alvo: rtd_option_quotes_intraday_history_repository.py.
- Ponte local com parser bridge para historico intraday.
- Preservacao do contrato de repository.
- Uso de utils/number_parser.py para normalizacao numerica.
- Uso de utils/date_parser.py para normalizacao temporal.
- Sem troca de persistencia.
- Sem troca de schema.
- Sem alteracao operacional ampla.
- Nenhuma operacao de git executada.

### Guardrails preservados

- Sistema permanece local.
- Sem Web.
- Sem HTTP.
- Sem API externa.
- Sem versionamento nesta etapa.

<!-- FIM FRENTE 39 RTD OPTION QUOTES INTRADAY HISTORY REPOSITORY PARSER BRIDGE CONTRACT -->

<!-- INICIO FRENTE 40 RTD OPTION QUOTES INTRADAY HISTORY SERVICE PARSER BRIDGE CONTRACT -->

## Frente 40 — RTD Option Quotes Intraday History Service Parser Bridge Contract

### Status

Aplicada localmente e validada.

### Objetivo

Consolidar a ponte controlada de parser no service de historico intraday de RTD
Option Quotes, preservando o fluxo local e evitando alteracao operacional ampla.

### Arquivos envolvidos

- services/rtd_option_quotes_intraday_history_service.py
- services/rtd_option_quotes_intraday_history_repository.py
- utils/number_parser.py
- utils/date_parser.py

### Escopo aplicado

- A Frente 40 manteve o service de historico intraday usando parser controlado.
- O contrato parser bridge foi preservado no recorte local.
- A documentacao local foi alinhada ao guardrail da frente.
- Sem troca de persistencia.
- Sem troca de schema.
- Sem alteracao operacional ampla.
- Nenhuma operacao de git executada.

### Guardrails preservados

- Sistema permanece local.
- Sem Web.
- Sem HTTP.
- Sem API externa.
- Sem versionamento nesta etapa.

- Nenhuma operacao de versionamento executada.
<!-- FIM FRENTE 40 RTD OPTION QUOTES INTRADAY HISTORY SERVICE PARSER BRIDGE CONTRACT -->

<!-- INICIO FRENTE 41 RTD OPTION QUOTES INTRADAY CANDLE SERVICE PARSER BRIDGE CONTRACT -->

## Frente 41 — RTD Option Quotes Intraday Candle Service Parser Bridge Contract

### Status

Aplicada localmente e validada.

### Objetivo

Registrar a Frente 41 como recorte local do service de candle intraday de RTD Option
Quotes consumindo parser controlado, preservando contratos e sem refatoracao ampla.

### Arquivos envolvidos

- rtd_option_quotes_intraday_candle_service.py
- utils/number_parser.py
- utils/date_parser.py

### Escopo aplicado

- Parser bridge preservado para o service de candle intraday.
- Normalizacao numerica e temporal mantida em helpers locais.
- Guardrail documental atualizado para refletir a frente encerrada.
- Sem troca de persistencia.
- Sem troca de schema.
- Sem alteracao operacional ampla.
- Nenhuma operacao de git executada.

### Guardrails preservados

- Sistema permanece local.
- Sem Web.
- Sem HTTP.
- Sem API externa.
- Sem versionamento nesta etapa.

<!-- FIM FRENTE 41 RTD OPTION QUOTES INTRADAY CANDLE SERVICE PARSER BRIDGE CONTRACT -->

<!-- INICIO RESUMO LOCAL FRENTES ENCERRADAS 37 38 39 -->

## Resumo local — Frentes encerradas 37, 38 e 39

### Status

Frentes 37, 38 e 39 encerradas localmente e documentadas.

### Escopo consolidado

- Frente 37: RTD Option Quotes Intraday Candle Chart Service Parser Bridge Contract.
- Frente 37 v3: normalizacao case-insensitive de marcadores documentais.
- Frente 38: RTD Option Quotes Intraday Candle Repository Parser Bridge Contract.
- Frente 38 v2: normalizacao posix do target no relatorio local.
- Frente 39: RTD Option Quotes Intraday History Repository Parser Bridge Contract.

### Validacao local registrada

- Bateria local direcionada das Frentes 37, 38 e 39 executada.
- Resultado registrado: 31 passed.
- Guardrails documentais das frentes encerradas preservados.

### Decisoes operacionais preservadas

- Sem troca de persistencia.
- Sem troca de schema.
- Sem alteracao operacional ampla.
- Nenhuma operacao de git executada.
- Sem Web.
- Sem HTTP.
- Sem API externa.
- Sistema permanece 100 por cento local.
- Decisoes operacionais mantidas sem ampliacao de escopo.

- Nenhuma operacao de versionamento executada.
- Resultado local: nenhum erro detectado.
- Sem operacao de git nesta etapa.
- Validacao local: relatorios JSON locais validos.
<!-- FIM RESUMO LOCAL FRENTES ENCERRADAS 37 38 39 -->

<!-- INICIO FRENTE 53D UI DATA PAYOFF REPO BRIDGE -->

## Frente 53d — UIDataModel consumindo derived_repo para payoff curve

### Status

Aplicada localmente e validada em teste direcionado.

### Contexto

A Frente 53d deu continuidade a reducao incremental de SQL direto real P0 em
UI/services relacionados a payoff, apos as Frentes 53a, 53b e 53c.

O alvo tecnico desta frente foi:

- UI/models/ui_data.py

### Objetivo

Remover SQL direto dos metodos publicos de payoff em UIDataModel para que a UI
consuma a ponte local de repository derivado ao carregar pontos de payoff.

A ponte canonica utilizada foi:

- db.derived_repo.get_payoff_curve_points_by_structure_id

### Escopo aplicado

- UI/models/ui_data.py passou a importar db.derived_repo.
- Foi criada ponte local segura por alias _PAYOFF_REPO_LOADER.
- get_payoff_curve passou a usar _PAYOFF_REPO_LOADER.
- get_payoff_curve_info passou a usar _PAYOFF_REPO_LOADER diretamente.
- Os metodos publicos de payoff nao executam SQL direto.
- Os metodos publicos de payoff nao acessam diretamente payoff_curve_points.
- Preservado o uso do banco local.
- Sem Web.
- Sem HTTP.
- Sem API externa.
- Sem troca de persistencia.
- Sem troca de schema.
- Sem alteracao operacional ampla.
- Nenhuma operacao de git executada.
- Caminho canonico UI preservado.

### Artefatos locais

- Patch: ATT/patch_53d_ui_data_payoff_repo_bridge.py
- Reparo local: ATT/repair_53d_ui_data_payoff_methods.py
- Teste: ATT/tests/test_frente_53d_ui_data_payoff_repo_bridge.py
- Relatorio: ATT/frente_53d_ui_data_payoff_repo_bridge_report.json

### Validacao local executada

Compilacao executada com sucesso:

    python -m py_compile UI/models/ui_data.py db/derived_repo.py

Teste especifico da Frente 53d executado com sucesso:

    python -m pytest ATT/tests/test_frente_53d_ui_data_payoff_repo_bridge.py -q

Resultado:

    3 passed

### Guardrails preservados

- Sistema permanece 100 por cento local.
- Sem Web.
- Sem HTTP.
- Sem API externa.
- Sem troca de persistencia.
- Sem alteracao de schema.
- Sem alteracao operacional ampla.
- Sem criacao de pasta nova na raiz.
- Patches e relatorios permanecem em ATT.
- Testes permanecem em ATT/tests.
- Sem git nesta etapa.

<!-- FIM FRENTE 53D UI DATA PAYOFF REPO BRIDGE -->

<!-- INICIO FRENTE 53D ROUND5 VALIDACAO LOCAL ABA LEGACY CONTRACT -->

## Frente 53d round5 — Validação local do contrato legado aba em UIDataModel

### Status

Aplicada localmente e validada com suíte completa.

### Contexto

Após a Frente 53d remover SQL direto dos métodos públicos de payoff em
`UI/models/ui_data.py`, restou alinhar o contrato legado retornado por
`get_payoff_curve_info()`.

Os testes de migração da UI esperavam que o campo `info["aba"]` preservasse o
valor bruto de `structure_id`, e não o texto derivado no formato `structure:<id>`.

### Ajuste aplicado

Foi aplicado patch local em:

- `UI/models/ui_data.py`

O método `get_payoff_curve_info()` passou a garantir, antes do retorno público:

- `info["aba"] = structure_id`

Com isso, o contrato legado fica compatível com os consumidores antigos que ainda
leem o campo `aba`, enquanto a identidade canônica permanece baseada em
`structure_id`.

### Escopo preservado

- Sem SQL direto reintroduzido em `get_payoff_curve`.
- Sem SQL direto reintroduzido em `get_payoff_curve_info`.
- Sem acesso direto da UI à tabela `payoff_curve_points` nos métodos públicos de payoff.
- Ponte local por `db.derived_repo` preservada.
- Alias seguro `_PAYOFF_REPO_LOADER` preservado.
- Contrato público `points, info` preservado.
- Sem troca de persistência.
- Sem alteração de schema.
- Sem alteração operacional ampla.
- Sem Web.
- Sem HTTP.
- Sem API externa.
- Sem criação de pasta nova na raiz.
- Patches, relatórios e temporários permanecem em `ATT`.
- Testes permanecem em `ATT/tests`.
- Nenhuma operação de git executada.

### Artefatos locais

- Patch round5: `ATT/patch_53d_ui_data_payoff_curve_info_round5_aba_legacy_contract.py`
- Relatório round5: `ATT/patch_53d_ui_data_payoff_curve_info_round5_aba_legacy_contract_report.json`
- Backup local: `UI/models/ui_data.py.backup_53d_round5_20260805_133919`

### Validação local executada

Compilação executada com sucesso:

    python -m py_compile UI/models/ui_data.py db/derived_repo.py ATT/patch_53d_ui_data_payoff_curve_info_round5_aba_legacy_contract.py

Bateria direcionada da Frente 53d e migração UI executada com sucesso:

    python -m pytest ATT/tests/test_frente_53d_ui_data_payoff_repo_bridge.py ATT/tests/test_ui_data_migration.py::test_payoff_curve_info_retorna_dados ATT/tests/test_ui_data_migration.py::test_payoff_curve_info_tem_structure_id ATT/tests/test_ui_data_migration.py::test_payoff_curve_info_aba_continuidade ATT/tests/test_ui_data_migration.py::test_payoff_curve_info_pontos_validos -q

Resultado local:

    7 passed

Suíte completa local executada com sucesso:

    python -m pytest ATT/tests -q

Resultado local:

    1107 passed, 4 skipped, 2 warnings, 6 subtests passed

### Observação sobre warnings

Os 2 warnings registrados são `DeprecationWarning` esperados nos testes de contenção
dos módulos legados:

- `db.reader.py`
- `db.writer.py`

Esses warnings fazem parte do contrato local de aposentadoria operacional da Frente 17
e não representam regressão da Frente 53d.

### Posição do projeto após a Frente 53d round5

A Frente 53d fica encerrada localmente com validação direcionada e suíte completa verde.

O projeto permanece na Fase 5 — UI e command services, seguindo a diretriz de reduzir
SQL direto real fora de repositories por recortes pequenos, reversíveis e testáveis.

### Próxima etapa recomendada

A próxima frente técnica deve continuar como novo recorte pequeno da Frente 53,
preferencialmente como Frente 53e, iniciando por pré-checagem local do próximo alvo
P0 real ainda remanescente no inventário refinado da Frente 52.

A escolha do próximo alvo deve preservar as regras do plano:

- um arquivo por vez;
- sem refatoração ampla;
- sem alteração de schema;
- sem troca de persistência;
- sem mudança operacional ampla;
- sem Web, HTTP ou API externa;
- sem git até o encerramento geral das frentes.

<!-- FIM FRENTE 53D ROUND5 VALIDACAO LOCAL ABA LEGACY CONTRACT -->

<!-- INICIO FRENTE 54A VALIDACAO LOCAL RTD SNAPSHOT STATUS SERVICE -->

## Frente 54a — ModernDarkWindow consumindo service local de status RTD Option Quotes

### Status

Aplicada localmente e validada em testes direcionados.

### Contexto

Após o encerramento local da Frente 53d round5, a varredura local de SQL direto em UI
indicou ocorrência remanescente em UI/modern/dark_window.py.

O ponto identificado era o watcher de snapshot RTD Option Quotes, que lia diretamente
o maior updated_at da tabela rtd_option_quotes para detectar mudança no snapshot local.

A consulta estava encapsulada na janela moderna apenas para detectar mudança do snapshot
já persistido, mas ainda representava SQL direto dentro da camada UI.

### Objetivo

Reduzir SQL direto em UI/modern/dark_window.py sem alterar comportamento operacional,
sem alterar schema, sem trocar persistência e sem introduzir Web, HTTP ou API externa.

A UI passou a delegar a leitura de MAX updated_at de rtd_option_quotes para um service
local pequeno e específico.

### Escopo aplicado

- Criado service local services/rtd_option_quotes_snapshot_status_service.py.
- O service concentra a leitura do maior updated_at de rtd_option_quotes.
- UI/modern/dark_window.py passou a consumir o service local.
- O SQL direto foi removido do watcher de snapshot RTD dentro da UI moderna.
- A consulta SQL ficou isolada em camada de service local.
- Nenhuma alteração de schema foi feita.
- Nenhuma troca de persistência foi feita.
- Nenhuma API externa foi introduzida.
- Nenhum HTTP foi introduzido.
- Nenhuma migração Web foi feita.
- Nenhuma operação de versionamento foi executada.

### Validação local registrada

Validação direcionada da Frente 54a:

- Resultado: 4 passed.

Regressão direcionada das Frentes 53c e 53d:

- Resultado: 6 passed.

Varredura local em UI/modern/dark_window.py:

- Nenhuma ocorrência operacional de execute encontrada no arquivo da UI moderna.
- A leitura de MAX updated_at de rtd_option_quotes ficou concentrada em services/rtd_option_quotes_snapshot_status_service.py.

### Artefatos locais

- Service: services/rtd_option_quotes_snapshot_status_service.py.
- Patch documental: ATT/patch_54a_docs_validacao_local.py.
- Relatório documental: ATT/frente_54a_docs_validacao_local_report.json.

### Guardrails preservados

- Sistema permanece 100 por cento local.
- Sem Web.
- Sem HTTP.
- Sem API externa.
- Sem troca de persistência.
- Sem alteração de schema.
- Sem alteração operacional ampla.
- Sem criação de pasta nova na raiz.
- Patches e temporários permanecem em ATT.
- Testes permanecem em ATT/tests.
- Nenhuma operação de git executada.
- Caminho canônico UI preservado.

### Decisão aplicada

A Frente 54a conclui um recorte pequeno da redução de SQL direto em UI, mantendo o
padrão já adotado nas Frentes 53a, 53b, 53c e 53d.

A leitura de status do snapshot RTD Option Quotes deixa de ficar dentro da UI moderna
e passa a ser responsabilidade de service local dedicado.

### Próxima etapa recomendada

A próxima frente técnica deve continuar a redução incremental de SQL direto fora de
repositories, sempre com pré-checagem local do próximo alvo real.

A recomendação é seguir como Frente 54b, selecionando apenas um novo ponto remanescente
por vez, sem refatoração ampla, sem alteração de schema, sem troca de persistência,
sem Web, sem HTTP, sem API externa e sem git até o encerramento geral das frentes.

<!-- FIM FRENTE 54A VALIDACAO LOCAL RTD SNAPSHOT STATUS SERVICE -->

