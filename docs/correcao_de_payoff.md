<!-- CHECKPOINT_RTD_ESCOPO_ATIVO_INICIO -->

# Checkpoint 2026-06-26 18:49 - RTD limitado ao escopo ativo

## Commit registrado

    eef1d5a Limita RTD ao escopo de estruturas ativas

## Objetivo da etapa

Garantir que o RTD não use caches antigos como fonte de escopo operacional.

Regra consolidada:

    structures.status = active
        define estruturas operacionais

    structure_legs das estruturas ativas
        define opções que devem ser atualizadas

    rtd_option_quotes
        é apenas cache de cotação, não define composição de estrutura

    rtd_underlying_quotes
        é cache de preço do ativo-base, não define composição de estrutura

    structure_leg_snapshots
        ficam como histórico/congelamento, não entram no refresh ativo

## Resultado validado

Opções ativas exportadas:

    BOVAG34
    BOVAH186
    BOVAS61
    BOVAT158
    PRIOG800
    PRIOH505
    PRIOS525
    PRIOT700

Total:

    8 opções

Ativos-base ativos:

    BOVA11
    PRIO3

Símbolos removidos do cache operacional:

    PETRS420
    PETRS424
    PETRS425
    PRIOH515

Auditoria final:

    Opções fora do escopo ativo: 0

## Pipeline RTD de opções

Comando executado:

    python scripts/run_rtd_refresh_full.py --db dados/app.db --visible --strict

Resultado:

    input_rows: 8
    inserted: 0
    updated: 8
    skipped: 0
    updated_at: 2026-06-26 18:41:55

Estado final:

    count: 8
    max_updated_at: 2026-06-26 18:41:55

## RTD de ativo-base validado

Tabela:

    rtd_underlying_quotes

Valores observados:

    BOVA11 = 170.78
    PRIO3  = 53.15

Fonte:

    btg_rtd_excel_underlying

Atualização:

    2026-06-26 18:36:19

## Estado atual das opções em rtd_option_quotes

    BOVAG34   BOVA11 CALL strike 157.0 ultimo_preco 14.64
    BOVAH186  BOVA11 CALL strike 186.0 ultimo_preco 1.12
    BOVAS61   BOVA11 PUT  strike 184.0 ultimo_preco 12.32
    BOVAT158  BOVA11 PUT  strike 158.0 ultimo_preco 0.63
    PRIOG800  PRIO3  CALL strike 80.0  ultimo_preco 0.02
    PRIOH505  PRIO3  CALL strike 50.5  ultimo_preco 0.0
    PRIOS525  PRIO3  0    strike 52.5  ultimo_preco 0.0
    PRIOT700  PRIO3  PUT  strike 70.0  ultimo_preco 12.03

## Atenções pendentes de qualidade dos dados

Pontos identificados antes da validação final do payoff:

    PRIOS525 está com call_put = 0
    PRIOH505 possui ultimo_preco = 0.0, mas tem bid/ask
    PRIOS525 possui ultimo_preco = 0.0, mas tem bid/ask

Hipóteses:

    1. O importador RTD pode precisar normalizar call_put pelo código da opção.
    2. O enriquecimento/pricing pode precisar usar midpoint bid/ask quando ultimo_preco vier zero ou inválido.

Não corrigido nesta etapa.

## Diagnóstico de código

O grep confirmou que o ponto central do próximo patch é:

    services/market_snapshot_provider.py

O arquivo ainda contém valores estáticos de spot em DEFAULT_MARKET_BY_ASSET ou estrutura equivalente.

Exemplos encontrados:

    spot_price: 198.35
    spot_price: 124.66
    spot_price: 168.67
    spot_price: 66.84
    spot_price: 87.37
    spot_price: 37.42
    spot_price: 61.80

## Próxima etapa

Alterar o MarketSnapshotProvider para usar fonte real:

    rtd_underlying_quotes.ultimo_preco

para o ativo-base da estrutura.

Fluxo desejado:

    CanonicalInputService
        -> MarketSnapshotProvider.get_snapshot(underlying_asset)
            -> dados/app.db:rtd_underlying_quotes
                -> spot_price = ultimo_preco
                -> market_snapshot_source = rtd_underlying_quotes
                -> is_static_fallback = false
                -> is_current_market = true ou calculado por freshness

## Regra de segurança para payoff

O payoff não deve aceitar cálculo como OK se a origem de mercado for estática.

Já existem guards em:

    domain/payoff.py
    services/payoff_pricing_engine.py

Próximo patch deve garantir:

    market_snapshot_source diferente de static_fallback
    is_static_fallback igual a false
    spot_price maior que zero

## Status da rota

    OK       RTD opções limitado a estruturas ativas
    OK       RTD ativos-base limitado a estruturas ativas
    OK       rtd_option_quotes limpo para 8 opções atuais
    OK       rtd_underlying_quotes populado com BOVA11 e PRIO3
    OK       commit do escopo RTD realizado
    pendente MarketSnapshotProvider lendo rtd_underlying_quotes
    pendente normalizar call_put inválido em PRIOS525
    pendente definir regra de prêmio quando ultimo_preco = 0 e bid/ask existem
    pendente revalidar payoff usando spot real

<!-- CHECKPOINT_RTD_ESCOPO_ATIVO_FIM -->

Correção de Payoff
Objetivo
Corrigir e validar o motor de cálculo de payoff, marcação atual e métricas financeiras das estruturas, garantindo que os gráficos e indicadores não usem preços incorretos, dados rasos ou premissas ambíguas.

O sistema deve separar claramente:

text


1. Payoff no vencimento
2. Marcação atual / PL atual
3. Métricas da implantação
4. Métricas atuais
5. Dados por perna da estrutura
Problema identificado
Foi identificado que a estrutura 3 de BOVA11 apresenta um Preço ref. de R$ 66,84, enquanto o valor atual observado do ativo-base é aproximadamente R$ 170,78.

Isso indica possível erro em uma ou mais das seguintes áreas:

text


- origem do preço de referência;
- associação incorreta do ativo-base;
- uso de preço antigo ou cacheado;
- uso de preço de outro ativo;
- cálculo equivocado no gráfico de payoff;
- uso indevido do ativo-base como chave de cálculo em vez de structure_id;
- ausência de separação entre payoff no vencimento e PL atual.
Premissa principal
O gráfico de payoff não pode ser apenas visual. Ele precisa ser sustentado por um motor financeiro auditável.

Para cada estrutura, o sistema deve manter e exibir dois blocos principais:

text


Snapshot da implantação
Snapshot atual
1. Snapshot da implantação
Dados congelados no momento em que a estrutura foi criada.

Deve conter:

text


- ID da estrutura
- Ativo-base
- Data/hora da implantação
- Preço do ativo-base na implantação
- Data de vencimento
- Dias até vencimento na implantação
- Lista de pernas da estrutura
- Ticker de cada opção
- Tipo da opção: CALL ou PUT
- Direção: comprada ou vendida
- Quantidade
- Strike
- Vencimento da opção
- Prêmio de entrada
- Custo total inicial
- Crédito/débito líquido da estrutura
- Custos operacionais, se houver
- Break-even inicial
- Ganho máximo inicial, se aplicável
- Perda máxima inicial, se aplicável
2. Snapshot atual
Dados recalculados no momento da análise.

Deve conter:

text


- Data/hora da análise
- Ativo-base
- Preço atual do ativo-base
- Dias restantes até o vencimento
- Preço atual de cada opção
- Valor atual da estrutura
- PL financeiro atual
- PL percentual atual
- Valor intrínseco de cada perna
- Valor extrínseco de cada perna
- Resultado atual por perna
- Resultado atual total
- Payoff no vencimento ao preço atual
- Distância até o break-even
- Distância até strikes relevantes
- Status: ganho, perda ou neutro
3. Separação conceitual obrigatória
O sistema deve separar estes conceitos no código e na interface:

Payoff no vencimento
Representa o resultado da estrutura considerando diferentes preços do ativo-base na data de vencimento.

Depende principalmente de:

text


- preço simulado do ativo no vencimento;
- strikes;
- tipo da opção;
- direção da posição;
- quantidade;
- prêmio de entrada;
- custos.
Marcação atual / PL atual
Representa o valor da estrutura hoje.

Depende de:

text


- preço atual do ativo-base;
- preço atual das opções;
- preço de entrada das opções;
- quantidade;
- direção;
- custos;
- tempo até vencimento;
- valor intrínseco;
- valor extrínseco.
4. Fórmulas mínimas obrigatórias
Intrínseco de call
I
n
t
r
i
n
s
e
c
o
=
max
⁡
(
S
−
K
,
0
)
Intrinseco=max(S−K,0)
Intrínseco de put
I
n
t
r
i
n
s
e
c
o
=
max
⁡
(
K
−
S
,
0
)
Intrinseco=max(K−S,0)
Extrínseco
E
x
t
r
i
n
s
e
c
o
=
P
r
e
c
o
O
p
c
a
o
−
I
n
t
r
i
n
s
e
c
o
Extrinseco=PrecoOpcao−Intrinseco
PL atual de perna comprada
P
L
=
(
P
r
e
c
o
A
t
u
a
l
−
P
r
e
c
o
E
n
t
r
a
d
a
)
×
Q
u
a
n
t
i
d
a
d
e
PL=(PrecoAtual−PrecoEntrada)×Quantidade
PL atual de perna vendida
P
L
=
(
P
r
e
c
o
E
n
t
r
a
d
a
−
P
r
e
c
o
A
t
u
a
l
)
×
Q
u
a
n
t
i
d
a
d
e
PL=(PrecoEntrada−PrecoAtual)×Quantidade
Payoff no vencimento de call comprada
P
L
=
(
max
⁡
(
S
T
−
K
,
0
)
−
P
r
e
m
i
o
)
×
Q
u
a
n
t
i
d
a
d
e
PL=(max(S 
T
​
 −K,0)−Premio)×Quantidade
Payoff no vencimento de call vendida
P
L
=
(
P
r
e
m
i
o
−
max
⁡
(
S
T
−
K
,
0
)
)
×
Q
u
a
n
t
i
d
a
d
e
PL=(Premio−max(S 
T
​
 −K,0))×Quantidade
Payoff no vencimento de put comprada
P
L
=
(
max
⁡
(
K
−
S
T
,
0
)
−
P
r
e
m
i
o
)
×
Q
u
a
n
t
i
d
a
d
e
PL=(max(K−S 
T
​
 ,0)−Premio)×Quantidade
Payoff no vencimento de put vendida
P
L
=
(
P
r
e
m
i
o
−
max
⁡
(
K
−
S
T
,
0
)
)
×
Q
u
a
n
t
i
d
a
d
e
PL=(Premio−max(K−S 
T
​
 ,0))×Quantidade
5. Ajustes necessários na interface
Evitar o rótulo genérico:

text


Preço ref.
Substituir por campos explícitos:

text


Preço base na implantação
Preço base atual
Preço usado na curva
Preço simulado no vencimento
Também separar claramente:

text


PL atual
Resultado simulado no vencimento
Payoff no vencimento ao preço atual
6. Painel mínimo recomendado no gráfico
Na tela de payoff, incluir um painel com:

text


Ativo-base
Data de implantação
Data atual
Data de vencimento
Dias até vencimento na implantação
Dias restantes
Preço base na implantação
Preço base atual
Custo inicial da estrutura
Valor atual da estrutura
PL atual financeiro
PL atual percentual
Payoff no vencimento ao preço atual
Break-even
Ganho máximo
Perda máxima
7. Tabela obrigatória por perna
Adicionar ou validar uma tabela com:

text


Ticker
Tipo
Direção
Quantidade
Strike
Vencimento
Prêmio de entrada
Preço atual
Intrínseco atual
Extrínseco atual
PL atual
Payoff no vencimento ao preço atual
Essa tabela será essencial para auditoria.

8. Validações obrigatórias
O sistema deve bloquear ou alertar quando:

text


- estrutura não tiver ativo-base definido;
- ativo-base da estrutura não bater com o ativo-base das pernas;
- preço atual do ativo-base estiver ausente;
- preço de implantação estiver ausente;
- vencimento estiver ausente;
- strike estiver ausente;
- prêmio de entrada estiver ausente;
- a estrutura possuir opções com vencimentos diferentes sem destaque explícito na análise;
- o cálculo tentar carregar pernas, snapshots ou métricas de mais de uma estrutura;
- preço usado na curva estiver muito distante do preço atual sem justificativa;
- curva de payoff no vencimento e marcação atual forem exibidas sem separação clara.
Mensagem sugerida:

text


A análise de payoff é individual por estrutura. Selecione uma única estrutura e use structure_id como chave de cálculo. O ativo-base pode se repetir em outras estruturas.
9. Auditoria inicial no código
Rodar estes comandos na raiz do projeto:

bash


git grep -n -I -E "66[,.]84|170[,.]78|pre[cç]o.?ref|preco_ref|reference.?price|spot|underlying|ativo.?base|payoff|break.?even|intr[ií]nseco|extr[ií]nseco" -- .
Também procurar por valores hardcoded:

bash


git grep -n -I -E "66\.84|66,84|198\.35|198,35|170\.78|170,78" -- .
E por campos de banco relacionados:

bash


git grep -n -I -E "implantacao|created_at|entry|entrada|premium|premio|strike|expiration|vencimento|option|opcao|legs|pernas" -- .
10. Refatoração recomendada no código
Criar ou separar serviços/funções com nomes explícitos:

text


calculateExpirationPayoff()
calculateCurrentMarkToMarket()
calculateLegIntrinsicValue()
calculateLegExtrinsicValue()
calculateStructureCurrentPL()
calculateStructureExpirationPL()
buildDeploymentSnapshot()
buildCurrentSnapshot()
validateSingleStructurePayoffScope()
Evitar função única misturando tudo, como:

text


calculatePayoff()
se ela estiver calculando várias coisas ao mesmo tempo.

11. Estrutura conceitual dos dados
Modelo mínimo sugerido:

typescript


type OptionLeg = {
  ticker: string;
  underlying: string;
  type: 'CALL' | 'PUT';
  side: 'BUY' | 'SELL';
  quantity: number;
  strike: number;
  expirationDate: string;
  entryPremium: number;
  currentPremium?: number;
};

type DeploymentSnapshot = {
  structureId: string;
  underlying: string;
  deployedAt: string;
  underlyingPriceAtDeployment: number;
  expirationDate: string;
  daysToExpirationAtDeployment: number;
  legs: OptionLeg[];
  initialNetCost: number;
};

type CurrentSnapshot = {
  structureId: string;
  calculatedAt: string;
  underlying: string;
  currentUnderlyingPrice: number;
  daysToExpiration: number;
  currentStructureValue: number;
  currentPL: number;
  currentPLPercent: number;
};

type PayoffPoint = {
  simulatedUnderlyingPrice: number;
  expirationPL: number;
};
12. Critérios de aceite
A correção só deve ser considerada concluída quando:

text


- O sistema exibir preço de implantação e preço atual separadamente.
- O campo genérico "Preço ref." for removido ou renomeado.
- O payoff no vencimento estiver separado do PL atual.
- Cada perna exibir intrínseco, extrínseco e PL atual.
- O payoff usar structure_id como chave principal e não carregar dados apenas por ativo-base.
- O caso BOVA11 não usar mais preço incompatível como R$ 66,84 sem justificativa.
- Testes automatizados cobrirem calls, puts e estratégias com múltiplas pernas.
- O gráfico deixar claro qual curva representa simulação no vencimento e qual valor representa marcação atual.
13. Testes obrigatórios
Criar testes para:

text


- call comprada;
- call vendida;
- put comprada;
- put vendida;
- trava de alta com call;
- trava de baixa com put;
- estrutura com múltiplas pernas;
- estrutura com ativo-base divergente;
- estrutura sem preço atual;
- estrutura sem preço de implantação;
- tentativa de calcular payoff com múltiplas structure_id no mesmo contexto.
14. Prioridade de execução
Eu sugiro iniciar nesta ordem:

Etapa 1 — Auditoria
text


Localizar origem do Preço ref. de R$ 66,84.
Etapa 2 — Correção de nomenclatura
text


Separar preço de implantação, preço atual e preço usado na curva.
Etapa 3 — Correção do motor
text


Separar payoff no vencimento de marcação atual.
Etapa 4 — Interface
text


Adicionar painel de métricas e tabela por perna.
Etapa 5 — Testes
text


Criar cenários automatizados e validar cálculos.
15. Primeiro comando para iniciar agora
Rode isso primeiro:

bash


git grep -n -I -E "66[,.]84|pre[cç]o.?ref|preco_ref|reference.?price|spot|underlying|ativo.?base|payoff" -- .
Depois, se encontrar o arquivo responsável pelo gráfico, rode:

bash


git grep -n -I -E "PL estimado|break.?even|regi[aã]o|ganho|perda|curva|fixada|simulado|vencimento" -- .
Nome da frente
Eu documentaria assim:

text


Fase 12 — Correção do motor de payoff, PL atual e métricas financeiras
Status inicial:

text


Status: Em andamento
Prioridade: Crítica
Motivo: Risco de cálculo financeiro incorreto

## Achado corrigido: bloqueio de snapshot estático como preço atual

Data: 2026-06-26

Foi confirmado que o fluxo de payoff usava MarketSnapshotProvider como fonte autoritativa de spot, taxa e volatilidade.

O MarketSnapshotProvider possuía valores estáticos em DEFAULT_MARKET_BY_ASSET para ativos como BOVA11 e PRIO3.

Impacto identificado:

    1. O preço hardcoded entrava no canonical_input_service.
    2. O campo spot_price era propagado para o payload de precificação.
    3. domain/payoff.py usava spot_price como spot_ref.
    4. PayoffPricingEngine calculava PL atual com esse preço.
    5. derived_payoff_persistence.py gravava spot_ref.
    6. A UI exibia esse número como Preço ref.

Correção aplicada:

    1. MarketSnapshotProvider não usa mais DEFAULT_MARKET_BY_ASSET implicitamente.
    2. O fallback estático só pode ser habilitado explicitamente por configuração.
    3. O snapshot passa a carregar market_snapshot_source, is_static_fallback e is_current_market.
    4. O payload propaga a origem do preço.
    5. PayoffPricingEngine bloqueia cálculo quando o preço veio de static_fallback.

Decisão:

    Preço hardcoded não pode ser tratado como preço atual.
    Preço sem origem auditável não deve alimentar PL atual.
    A UI pode exibir referência, mas não deve sugerir mercado atual quando a fonte for fallback estático.

<!-- PAYOFF_MARKET_DATA_ROUTE_START -->

# Rota atualizada - correção do payoff via Market Snapshot real

Atualizado em: 2026-06-26 17:09:55

## Diagnóstico consolidado

O problema não é apenas ausência de spot_price do ativo-base.

O problema estrutural é que o cálculo final de payoff ainda não está recebendo um Market Snapshot real e canônico.
O sistema possuía dados RTD parciais, mas a ligação com o cálculo final estava incompleta.

## Estado confirmado

### 1. Cotações de opções

O pipeline RTD de opções foi validado em dados/app.db.

Comando executado:

    python scripts/run_rtd_refresh_full.py --db dados/app.db

Resultado validado:

    rtd_option_quotes:
    - row_count: 12
    - duplicate_codigo_count: 0
    - stale_rows: 0
    - max_updated_at atualizado

Portanto, as opções agora estão no banco correto:

    dados/app.db

### 2. Problema restante

Ainda faltam fontes dinâmicas ligadas ao payoff para:

- ativo-base;
- spot price;
- parâmetros de mercado;
- eventual volatilidade, risk-free e dividend yield;
- montagem final do payload de precificação.

### 3. Causa técnica principal

O pipeline atual gera símbolos RTD principalmente a partir de opções:

    structure_legs
    structure_leg_snapshots
    rtd_option_quotes.codigo_opcao

Mas ainda não há pipeline dedicado para ativos-base como:

    BOVA11
    PRIO3
    PETR4

A aba RTD-BTG LISTA do Excel possui exemplo de ativo, mas fixo em BPAC11.
Ela não está parametrizada nem ligada ao fluxo final do payoff.

## Nova rota oficial

A correção passa a seguir esta ordem:

    1. Manter RTD de opções em dados/app.db
    2. Criar pipeline RTD separado para ativos-base
    3. Persistir ativos-base em rtd_underlying_quotes
    4. Alterar MarketSnapshotProvider para buscar spot real no banco
    5. Montar pricing payload com dados reais
    6. Revalidar payoff

## Nova tabela canônica inicial

A primeira tabela para corrigir o snapshot de mercado será:

    CREATE TABLE IF NOT EXISTS rtd_underlying_quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ativo TEXT NOT NULL UNIQUE,
        ultimo_preco REAL,
        bid REAL,
        ask REAL,
        close_price REAL,
        prev_close REAL,
        open_price REAL,
        high_price REAL,
        low_price REAL,
        volume REAL,
        change_percent REAL,
        source TEXT,
        updated_at TEXT,
        created_at TEXT
    );

## Scripts desta etapa

Os scripts previstos para esta etapa são:

    scripts/build_rtd_underlying_symbols.py
    scripts/refresh_rtd_underlying_quotes_excel.ps1
    scripts/import_rtd_underlying_quotes_csv.py
    scripts/run_rtd_underlying_refresh_full.py
    scripts/update_correcao_payoff_doc.py

## Próxima validação esperada

Após executar:

    python scripts/run_rtd_underlying_refresh_full.py --db dados/app.db

Esperamos encontrar em rtd_underlying_quotes linhas como:

    BOVA11
    PRIO3
    PETR4

com ultimo_preco, bid, ask, close_price e updated_at preenchidos.

## Ponto de decisão seguinte

Depois que rtd_underlying_quotes estiver populada, o próximo patch será no MarketSnapshotProvider.

Ele deverá montar o snapshot buscando:

    structures.underlying_asset
    rtd_underlying_quotes.ultimo_preco
    rtd_option_quotes por perna

E eliminar fallback estático como fonte primária de payoff.

<!-- PAYOFF_MARKET_DATA_ROUTE_END -->
## Conferência de seguimento RTD, snapshot e payoff

Foi executada conferência de runtime para validar a fonte de preço dos ativos-base utilizada pelo MarketSnapshotProvider.

Resultado:

- A tabela rtd_underlying_quotes existe em dados/app.db.
- BOVA11 possui preço atualizado de 170.55, fonte btg_rtd_excel_underlying.
- PRIO3 possui preço atualizado de 53.20, fonte btg_rtd_excel_underlying.
- O MarketSnapshotProvider retornou snapshot_source e market_snapshot_source iguais a rtd_underlying_quotes para BOVA11 e PRIO3.
- O campo is_static_fallback retornou False para ambos os ativos.
- O campo is_current_market retornou True para ambos os ativos.

Conclusão:

A fonte real de spot para ativos-base está validada em runtime. O provider não está usando fallback estático no cenário conferido.

Ressalvas encontradas:

- A opção PRIOS525 ainda aparece com call_put igual a 0.
- As opções PRIOH505 e PRIOS525 aparecem com ultimo_preco igual a 0.0 apesar de possuírem bid/ask positivos.
- O valor 66.84 ainda aparece como referência residual/fallback em código/documentação histórica, embora o snapshot atual de PRIO3 tenha retornado 53.20 vindo de rtd_underlying_quotes.

Decisão:

As pendências relacionadas à fonte RTD dos ativos-base e ao MarketSnapshotProvider podem ser consideradas fechadas. A qualidade RTD das opções deve permanecer como ressalva até ajuste ou justificativa formal da regra de fallback de preço e normalização de call_put.
python -m py_compile services/canonical_pricing_facade.py services/pricing_input_service.py
OK

_lookup_spot_price(Path("dados/app.db"), "PRIO3")
53.2

PricingInputService(db_path="dados/app.db")
spot_price: 53.2
market_snapshot_source: rtd_underlying_quotes
is_static_fallback: False

python -m pytest
669 passed, 2 skipped

python -m pytest ATT/tests -k "pricing or canonical or snapshot"
135 passed, 536 deselected
## Encerramento complementar - PRIOS525 como perna substituída

## Encerramento da rota RTD, Market Snapshot e Pricing Canônico

Data: 2026-06-26

Foram executadas as validações finais da rota de dados de mercado para payoff/pricing.

Validações executadas:

    python -m py_compile services/canonical_pricing_facade.py services/pricing_input_service.py
    OK

    _lookup_spot_price(Path("dados/app.db"), "PRIO3")
    53.2

    PricingInputService(db_path="dados/app.db")
    spot_price: 53.2
    market_snapshot_source: rtd_underlying_quotes
    is_static_fallback: False

    python -m pytest
    669 passed, 2 skipped

    python -m pytest ATT/tests -k "pricing or canonical or snapshot"
    135 passed, 536 deselected

RTD de ativos-base validado:

    BOVA11 = 170.55
    PRIO3  = 53.20
    source = btg_rtd_excel_underlying
    market_snapshot_source = rtd_underlying_quotes
    is_static_fallback = False
    is_current_market = True

RTD de opções validado:

    count: 8
    missing: []
    extra: []

Opções no escopo operacional:

    BOVAG34
    BOVAH186
    BOVAS61
    BOVAT158
    PRIOG800
    PRIOH505
    PRIOS525
    PRIOT700

Qualidade atual das opções conferida:

    PRIOH505  CALL  ultimo_preco 4.97
    PRIOS525  PUT   ultimo_preco 1.05

Decisão sobre PRIOS525:

Foi esclarecido que PRIOS525 corresponde a uma perna substituída da estrutura.

A validação do payoff ativo deve considerar as pernas efetivas/operacionais da estrutura, não pernas substituídas ou históricas.

No estado atual do banco, PRIOS525 também já aparece normalizada como PUT e com ultimo_preco positivo, portanto não há pendência bloqueante relacionada a call_put ou preço zerado.

Status atualizado:

    OK        RTD opções limitado ao escopo operacional esperado
    OK        RTD ativos-base limitado ao escopo ativo
    OK        rtd_underlying_quotes populado com BOVA11 e PRIO3
    OK        MarketSnapshotProvider lendo rtd_underlying_quotes
    OK        CanonicalPricingFacade priorizando rtd_underlying_quotes
    OK        PricingInputService usando db_path correto e spot real
    OK        Payoff/Pricing bloqueiam static_fallback como mercado atual
    OK        PRIO3 não retorna mais 66.84 no facade
    OK        PRIOS525 não bloqueia payoff ativo
    OK        Pendências de call_put e ultimo_preco zerado não aparecem no estado atual validado
    OK        Teste completo: 669 passed, 2 skipped
    OK        Teste pricing/canonical/snapshot: 135 passed
    OK        Push realizado até 90978f8

Conclusão:

A rota RTD + Market Snapshot real + Pricing Canônico pode ser considerada encerrada para a correção do preço incorreto usado no payoff/pricing.

## Consolidação final — regra de payoff por estrutura individual

Status: vigente.

A análise de payoff deve ser realizada sempre por estrutura individual.

A unidade principal de análise é a estrutura, identificada por structure_id e por nome próprio.

O ativo-base é apenas um atributo da estrutura.

O mesmo ativo-base pode existir em várias estruturas diferentes sem gerar conflito, mistura ou ambiguidade.

Exemplo permitido:

    Estrutura 1 - BOVA11 - Trava de Alta
    Estrutura 2 - BOVA11 - Borboleta
    Estrutura 3 - BOVA11 - Condor

Mesmo que todas usem o mesmo ativo-base, elas não se misturam porque possuem:

- ID próprio;
- nome próprio;
- conjunto próprio de pernas;
- strikes próprios;
- quantidades próprias;
- direção própria de cada perna;
- preços de entrada próprios;
- preços atuais próprios;
- vencimentos próprios;
- snapshot de implantação próprio;
- marcação atual própria;
- curva própria de payoff no vencimento.

Portanto, o sistema deve calcular e exibir o payoff usando exclusivamente os dados da estrutura selecionada.

### Regra operacional de cálculo

Para calcular payoff, marcação atual, métricas, tabela por perna e curva no vencimento, o sistema deve usar sempre uma única estrutura selecionada.

A chave principal de cálculo deve ser:

    structure_id

O ativo-base não deve ser usado como chave principal para carregar:

- pernas;
- snapshots;
- métricas;
- curva de payoff;
- marcação atual;
- resultado por perna;
- resultado consolidado.

A consulta das pernas deve ser feita por structure_id.

A consulta dos snapshots deve ser feita por structure_id.

A consulta das métricas da estrutura deve ser feita por structure_id.

As cotações atuais das opções devem ser obtidas a partir dos tickers das pernas pertencentes à própria estrutura.

A cotação atual do ativo-base deve ser obtida a partir do ativo-base vinculado à estrutura selecionada.

### O que é permitido

É permitido existir mais de uma estrutura com o mesmo ativo-base.

Isso é esperado e não representa erro.

Exemplo:

    BOVA11 pode existir em 3, 5 ou mais estruturas diferentes.

O que separa as análises não é o ativo-base.

O que separa as análises é o structure_id.

### O que é proibido no contexto de payoff

No contexto do gráfico principal de payoff, é proibido:

- carregar pernas apenas por ativo-base;
- carregar snapshots apenas por ativo-base;
- carregar métricas apenas por ativo-base;
- somar pernas de estruturas diferentes;
- montar uma curva única com dados de mais de uma structure_id;
- tratar preço hardcoded como preço atual;
- tratar fallback estático como preço atual;
- misturar payoff no vencimento com PL atual sem separação visual e conceitual.

### Estruturas com múltiplas pernas

O motor de payoff deve suportar estruturas com 2, 3, 4 ou mais pernas.

A quantidade de pernas não deve alterar a regra de cálculo.

O payoff total da estrutura é a soma dos resultados individuais das pernas pertencentes à própria estrutura.

Forma conceitual:

    PayoffTotal(ST) = soma dos Payoffs individuais das pernas da estrutura

Onde:

- ST é o preço simulado do ativo-base no vencimento;
- cada perna considerada deve pertencer à mesma structure_id;
- nenhuma perna de outra estrutura deve entrar no cálculo.

### Dados obrigatórios para análise profunda

A tela de payoff deve apresentar, no mínimo, os blocos abaixo.

#### Identificação da estrutura

- ID da estrutura;
- nome da estrutura;
- ativo-base;
- data de implantação;
- data da análise;
- vencimento principal;
- quantidade de pernas.

#### Snapshot da implantação

- preço do ativo-base na implantação;
- lista de pernas na implantação;
- ticker de cada perna;
- tipo da opção: CALL ou PUT;
- direção: compra ou venda;
- quantidade;
- strike;
- vencimento;
- prêmio de entrada;
- custo ou crédito líquido inicial;
- break-even inicial;
- ganho máximo inicial, se aplicável;
- perda máxima inicial, se aplicável.

#### Snapshot atual

- preço atual do ativo-base;
- fonte do preço atual;
- indicação de fallback estático, se houver;
- data e hora da cotação atual;
- preço atual de cada opção;
- valor atual da estrutura;
- PL financeiro atual;
- PL percentual atual;
- valor intrínseco por perna;
- valor extrínseco por perna;
- resultado atual por perna;
- resultado atual consolidado.

#### Curva de payoff no vencimento

- faixa de preços simulados do ativo-base;
- payoff individual de cada perna;
- payoff total da estrutura;
- break-even;
- regiões de ganho;
- regiões de perda;
- ganho máximo, se limitado;
- perda máxima, se limitada;
- payoff no vencimento considerando o preço atual do ativo-base.

#### Tabela obrigatória por perna

Para cada perna, exibir:

- ticker;
- tipo;
- direção;
- quantidade;
- strike;
- vencimento;
- prêmio de entrada;
- preço atual;
- valor intrínseco atual;
- valor extrínseco atual;
- PL atual;
- payoff no vencimento ao preço atual;
- contribuição da perna para o payoff total.

### Separação conceitual obrigatória

O sistema deve separar claramente:

    Payoff no vencimento
    Marcação atual / PL atual
    Snapshot da implantação
    Snapshot atual
    Dados por perna

O payoff no vencimento representa simulação em diferentes preços do ativo-base na data de vencimento.

A marcação atual representa o valor da estrutura hoje, usando as cotações atuais das opções e do ativo-base.

Esses conceitos não devem ser exibidos como se fossem a mesma coisa.

### Nomenclatura obrigatória na interface

Evitar o rótulo genérico:

    Preço ref.

Substituir por campos explícitos:

    Preço base na implantação
    Preço base atual
    Preço usado na curva
    Preço simulado no vencimento

Também separar claramente:

    PL atual
    Resultado simulado no vencimento
    Payoff no vencimento ao preço atual

### Validações obrigatórias

O sistema deve bloquear ou alertar quando:

- estrutura não tiver ativo-base definido;
- ativo-base da estrutura não bater com o ativo-base das pernas;
- preço atual do ativo-base estiver ausente;
- preço de implantação estiver ausente;
- vencimento estiver ausente;
- strike estiver ausente;
- prêmio de entrada estiver ausente;
- a estrutura possuir opções com vencimentos diferentes sem destaque explícito;
- o cálculo tentar carregar pernas, snapshots ou métricas de mais de uma estrutura;
- preço usado na curva estiver muito distante do preço atual sem justificativa;
- curva de payoff no vencimento e marcação atual forem exibidas sem separação clara;
- a fonte de mercado for fallback estático;
- spot_price estiver ausente, zerado ou sem origem auditável.

Mensagem sugerida:

    A análise de payoff é individual por estrutura.
    Selecione uma única estrutura e use structure_id como chave de cálculo.
    O ativo-base pode se repetir em outras estruturas.

### Critérios de aceite revisados

A correção só deve ser considerada concluída quando:

- o sistema exibir preço de implantação e preço atual separadamente;
- o campo genérico "Preço ref." for removido ou renomeado;
- o payoff no vencimento estiver separado do PL atual;
- cada perna exibir intrínseco, extrínseco e PL atual;
- o payoff usar structure_id como chave principal;
- nenhuma rotina de payoff carregar pernas apenas por ativo-base;
- o caso BOVA11 não usar mais preço incompatível como R$ 66,84 sem justificativa;
- preço hardcoded ou fallback estático não for aceito como mercado atual;
- testes automatizados cobrirem calls, puts e estratégias com múltiplas pernas;
- o gráfico deixar claro qual curva representa simulação no vencimento e qual valor representa marcação atual.

### Testes obrigatórios revisados

Criar ou manter testes para:

- call comprada;
- call vendida;
- put comprada;
- put vendida;
- trava de alta com call;
- trava de baixa com put;
- estrutura com múltiplas pernas;
- estrutura com ativo-base divergente entre cadastro e pernas;
- estrutura sem preço atual;
- estrutura sem preço de implantação;
- tentativa de calcular payoff com múltiplas structure_id no mesmo contexto;
- tentativa de calcular payoff usando fallback estático como mercado atual;
- estrutura cujo ativo-base também exista em outra estrutura, garantindo que não haja mistura de pernas.

### Decisão final

O ativo-base pode ser igual em várias estruturas.

Isso não é erro.

A separação correta é feita por structure_id.

O payoff deve ser profundo, auditável e completo dentro da estrutura selecionada.


<!-- CHECKPOINT_PAYOFF_EVOLUCAO_20260627_INICIO -->

## Checkpoint 2026-06-27 11:49 - Evolucao da limpeza de payoff por estrutura individual

### Contexto

Este checkpoint registra a evolucao posterior ao encerramento da rota RTD, Market Snapshot real e Pricing Canonico.

A base do projeto ja havia consolidado que:

    - o ativo-base nao e chave principal de calculo de payoff;
    - a chave principal deve ser structure_id;
    - o MarketSnapshotProvider deve usar rtd_underlying_quotes como fonte real de spot;
    - fallback estatico nao pode ser tratado como mercado atual;
    - a analise de payoff deve ser individual por estrutura;
    - pernas, snapshots, metricas e curva de payoff nao devem ser carregados apenas por ativo-base.

### Commits recentes relevantes

Estado observado na branch reinicio-normalizacao-idioma-ptbr:

    b775a1a chore: adiciona conferencia completa de payoff por estrutura
    210c6ff fix: remove spot hardcoded de fallback de mercado
    5068b60 chore: adiciona limpeza de derivados antigos de payoff
    d893de0 chore: remove CSVs legados da pasta bridge
    2c41b11 chore: remove ruido legado de comparacao entre estruturas

Commit atual remoto e local:

    2c41b11 chore: remove ruido legado de comparacao entre estruturas

### Evolucao aplicada

Foi removido o script temporario:

    scripts/atualiza_doc_payoff_estrutura_individual.py

Tambem foi ajustado o checker:

    scripts/conferir_payoff_buscas_git.sh

O checker passou a excluir caminhos que geravam ruido de auditoria:

    - docs
    - reports
    - o proprio script conferir_payoff_buscas_git.sh

Com isso, o bloco de termos antigos de comparacao incompativel deixou de acusar o proprio arquivo de conferencia.

### Validacoes executadas

Foram executados os comandos de conferencia:

    bash scripts/run_conferencia_payoff_estrutura_individual.sh
    bash scripts/conferir_payoff_runtime_focado.sh
    python scripts/scan_db_tokens_payoff.py dados/app.db dados/derived.db

Resultado observado:

    - conferencia principal concluida;
    - relatorio Git/Grep gerado;
    - conferencia DB gerada;
    - conferencia runtime focada gerada;
    - scan de tokens em bancos gerado;
    - bloco 1 do relatorio sem ocorrencias de termos antigos fora do escopo;
    - working tree limpo apos commit e push.

### Resultado da busca de termos antigos

O bloco 1 do relatorio:

    1. Termos antigos de comparacao incompativel

ficou sem ocorrencias apos a exclusao de docs, reports e do proprio checker.

Isso confirma que os termos legados abaixo nao aparecem mais no codigo operacional conferido:

    - validateComparableStructures
    - Nao e possivel comparar estruturas com ativos-base diferentes
    - comparacao entre duas estruturas incompativeis
    - Estruturas de ativos diferentes nao puderem

### Estado atual de Git

Estado final confirmado:

    HEAD local: 2c41b11
    origin/reinicio-normalizacao-idioma-ptbr: 2c41b11
    git status --short: sem pendencias

### Situacao atual da frente de payoff

Status consolidado:

    OK        RTD de opcoes limitado ao escopo operacional
    OK        RTD de ativos-base populado para BOVA11 e PRIO3
    OK        MarketSnapshotProvider usando rtd_underlying_quotes
    OK        PricingInputService usando spot real do banco correto
    OK        Payoff/Pricing bloqueiam fallback estatico como mercado atual
    OK        PRIO3 nao retorna mais 66.84 no fluxo canonico validado
    OK        regra de payoff individual por estrutura consolidada
    OK        checker de conferencia ajustado para evitar self-hit
    OK        limpeza de artefatos temporarios e CSVs legados realizada

### Ressalva de acompanhamento

O relatorio de busca ainda possui uma secao sobre campos e labels de preco de referencia.

Foram observadas ocorrencias tecnicas como:

    - spot_ref
    - pl_at_spot_ref

principalmente em testes e nomes internos.

Essas ocorrencias nao necessariamente indicam erro funcional, mas devem ser classificadas na proxima etapa como:

    - uso interno aceitavel;
    - legado a renomear;
    - label de interface a substituir;
    - campo persistido que precisa de migracao futura;
    - teste que precisa acompanhar a nova nomenclatura.

### Proxima etapa recomendada

A proxima etapa deve ser uma auditoria focada de nomenclatura e interface.

Objetivo:

    garantir que o usuario final nao veja mais o rotulo generico Preco ref. quando o dado representar conceitos diferentes.

Separar explicitamente:

    - Preco base na implantacao
    - Preco base atual
    - Preco usado na curva
    - Preco simulado no vencimento
    - PL atual
    - Payoff no vencimento ao preco atual
    - Resultado simulado no vencimento

### Ordem sugerida para continuidade

1. Classificar ocorrencias restantes de spot_ref, preco_ref, reference_price e Preco ref.

2. Separar o que e campo interno tecnico do que e label exibida na interface.

3. Renomear labels visuais ambiguas.

4. Manter compatibilidade de campos internos quando houver persistencia ou testes dependentes.

5. Reexecutar a conferencia completa.

6. Registrar novo checkpoint com a decisao de nomenclatura.

### Criterio de conclusao da proxima etapa

A etapa seguinte pode ser considerada concluida quando:

    - nenhuma tela exibir Preco ref. de forma ambigua;
    - o preco atual do ativo-base estiver rotulado como Preco base atual;
    - o preco de implantacao estiver separado do preco atual;
    - o preco usado na curva estiver identificado;
    - PL atual e payoff no vencimento estiverem visualmente separados;
    - testes continuarem passando;
    - relatorio de busca estiver classificado sem pendencias bloqueantes.

<!-- CHECKPOINT_PAYOFF_EVOLUCAO_20260627_FIM -->


<!-- CHECKPOINT_PAYOFF_NOMENCLATURA_PRECO_20260627_INICIO -->

## Checkpoint 2026-06-27 - Nomenclatura de preco no payoff

### Contexto

Apos o registro da evolucao da correcao de payoff, foi iniciada a classificacao das ocorrencias relacionadas a:

    - spot_ref
    - pl_at_spot_ref
    - preco_ref
    - reference_price
    - Preco ref.

O objetivo desta etapa nao e remover campos internos de forma cega.

O objetivo e separar:

    - label exibida ao usuario;
    - campo tecnico interno;
    - coluna persistida por compatibilidade;
    - fixture de teste;
    - script diagnostico;
    - evidencia historica.

### Validacao de UI

Foi executada validacao automatizada procurando labels visiveis residuais na pasta UI com os termos:

    - Preco ref
    - Preco ref.
    - Preço ref
    - Preço ref.

Resultado esperado e validado nesta etapa:

    OK        nenhum label visivel Preco ref encontrado na UI

Isso confirma que a interface nao deve mais exibir o rotulo ambiguo como nome de campo principal.

### Script temporario de correcao de label

O script abaixo era um artefato temporario de migracao de nomenclatura:

    scripts/corrigir_labels_preco_ref_ui.py

Situacao nesta etapa:

    remocao versionada: sim

Motivo:

    - o script continha os textos antigos como padrao de substituicao;
    - isso gerava ruido nas auditorias de nomenclatura;
    - a correcao de label ja havia sido aplicada;
    - scripts temporarios de migracao nao devem permanecer como fonte de falso positivo.

### Decisao de nomenclatura

A nomenclatura de interface deve seguir a regra consolidada:

    - Preco base na implantacao
    - Preco base atual
    - Preco usado na curva
    - Preco simulado no vencimento
    - PL atual
    - Payoff no vencimento ao preco atual
    - Resultado simulado no vencimento

O termo generico Preco ref. nao deve ser usado em label de usuario.

### Ocorrencias internas ainda permitidas temporariamente

As ocorrencias restantes de spot_ref e pl_at_spot_ref podem existir temporariamente em:

    - persistencia;
    - schema de banco;
    - camada de compatibilidade;
    - testes;
    - payloads internos;
    - calculo de interpolacao do PL no preco base atual;
    - scripts diagnosticos.

Essas ocorrencias nao sao bloqueantes quando nao aparecem como label ambigua para o usuario.

### Proxima etapa

Gerar classificacao das ocorrencias restantes em codigo operacional, separando:

    - UI interna;
    - dominio e calculo;
    - persistencia;
    - servicos;
    - testes;
    - scripts diagnosticos;
    - seeds;
    - pendencias reais.

A migracao de nomes internos deve ser feita com cuidado para nao quebrar:

    - schema existente;
    - historico em dados/derived.db;
    - testes de compatibilidade;
    - persistencia de curvas ja gravadas;
    - integracao entre payoff_chart e details_panel.

<!-- CHECKPOINT_PAYOFF_NOMENCLATURA_PRECO_20260627_FIM -->

