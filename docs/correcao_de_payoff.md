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
- comparação entre estruturas incompatíveis;
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
- opções de vencimentos diferentes forem comparadas sem aviso;
- estruturas de ativos-base diferentes forem comparadas;
- preço usado na curva estiver muito distante do preço atual sem justificativa;
- curva fixada e curva atual usarem escalas incompatíveis.
Mensagem sugerida:

text


Não é possível comparar estruturas com ativos-base diferentes ou preços de referência incompatíveis.
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
validateComparableStructures()
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
- Estruturas de ativos diferentes não puderem ser comparadas sem alerta.
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
- comparação entre duas estruturas incompatíveis.
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
