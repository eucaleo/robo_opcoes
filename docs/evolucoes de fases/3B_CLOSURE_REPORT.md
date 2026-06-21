# Encerramento 3B -- Canonical Domain Decoupling

## Status
Concluído.

## Objetivo da etapa
Consolidar o fluxo principal em torno de um contrato canônico de estrutura/mercado, reduzindo o acoplamento com formatos legados e isolando adaptações em bordas específicas.

---

## Itens executados

### 1. Contrato canônico de estrutura/mercado
Foi consolidado o uso de um shape canônico com os blocos:

- `structure`
- `market`
- `meta`

Esse contrato passou a ser a base do fluxo principal de montagem de input.

---

### 2. Priorização de legs canônicas
No fluxo principal, quando `structure["legs"]` já está disponível, a origem considerada é:

- `legs_source = "canonical"`

O fallback legado só é acionado quando não existem legs canônicas disponíveis.

---

### 3. Fallback legado isolado
O acesso às legs do legado foi encapsulado em uma camada específica de fallback/adaptação, responsável por:

- resolver alias legado quando necessário
- escolher timestamp de consulta
- buscar legs via serviço legado
- converter para shape canônico
- descartar entradas inválidas/incompletas quando necessário

Com isso, o domínio principal deixa de depender diretamente do formato legado.

---

### 4. Mapper de legs legadas para shape canônico
Foi consolidado o mapper `to_canonical_leg(...)`, com responsabilidade de converter dados legados para o contrato canônico.

#### Funções envolvidas
- `_read_attr(obj, name, default=None)`
- `_enum_value(value)`
- `_safe_upper_text(value)`
- `_to_float(value, field_name)`
- `_to_int(value, field_name)`
- `to_canonical_leg(leg, multiplier=1.0)`

#### Conversões implementadas
- `cv="C"` -> `position_side="LONG"`
- `cv="V"` -> `position_side="SHORT"`
- `call_put="CALL"` -> `option_type="CALL"`
- `call_put="PUT"` -> `option_type="PUT"`
- `ativo` -> `symbol` normalizado em uppercase/trim
- `strike` -> `float`
- `quant` -> `int`
- `vencimento` -> `expiration_date` em formato `YYYY-MM-DD`
- `preco` -> `premium`

#### Robustez adicionada
- erro explícito para `cv` inválido
- erro explícito para `call_put` inválido
- erro explícito para `strike` inválido
- erro explícito para `quant` inválido

---

### 5. Métricas de DTE sobre o shape canônico
Foi mantido o cálculo de DTE a partir do contrato canônico.

#### Funções envolvidas
- `_parse_date(value)`
- `compute_dte(reference_date, expiration_date)`
- `compute_dte_min_from_canonical_input(canonical_input)`

#### Comportamentos cobertos
- cálculo de DTE no mesmo dia
- cálculo de DTE futuro
- retorno `None` quando não há datas válidas
- extração do menor DTE entre legs canônicas
- suporte a datas em formato:
  - `YYYY-MM-DD`
  - `DD/MM/YYYY`

---

### 6. Testes adicionados/validados

#### `ATT/tests/test_robo_leg_mapper.py`
Cobertura para:
- mapeamento `LONG/CALL`
- mapeamento `SHORT/PUT`
- erro para `cv` inválido
- erro para `call_put` inválido
- erro para `strike` inválido
- erro para `quant` inválido

#### `ATT/tests/test_structure_metrics.py`
Cobertura para:
- mesmo dia
- dia futuro
- data inválida
- menor DTE em input canônico
- formato brasileiro `DD/MM/YYYY`

#### Demais evidências de validação executadas
Também passaram os testes relacionados a:
- payoff canônico
- validadores canônicos
- decisão
- derived service
- robo legs service
- structure market input assembler

---

## Resultado final do 3B

O domínio principal passou a operar orientado ao contrato canônico, com as seguintes garantias:

- legs canônicas são a fonte prioritária
- dependências legadas foram empurradas para adaptadores/fallbacks
- montagem de input estrutura+mercado foi desacoplada
- métricas de estrutura operam sobre o contrato canônico
- persistência derivada ficou preparada para evolução posterior sem bloquear esta etapa
- cobertura de testes suficiente para encerramento incremental da fase

---

## Itens explicitamente fora do escopo deste encerramento
Os itens abaixo não bloqueiam o fechamento do 3B:

- migração física completa do storage derivado de `aba` para `structure_id`
- remoção total de `alias_legacy_aba` da persistência
- reestruturação completa do histórico legado
- convergência total de identidade em todas as tabelas históricas

Esses pontos ficam aptos para uma etapa posterior de convergência de persistência/identidade.

---

## Conclusão
O 3B está concluído com sucesso.

A arquitetura resultante já apresenta:
- desacoplamento funcional do legado no fluxo principal
- shape canônico estabilizado
- testes principais passando
- base pronta para evolução incremental da camada de persistência em fase posterior
