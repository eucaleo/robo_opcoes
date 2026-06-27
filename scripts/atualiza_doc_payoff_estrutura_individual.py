from pathlib import Path
import sys

path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("correcao_de_payoff.md")

if not path.exists():
    raise SystemExit(f"Arquivo não encontrado: {path}")

text = path.read_text(encoding="utf-8")

backup = path.with_suffix(path.suffix + ".bak")
backup.write_text(text, encoding="utf-8")

replacements = {
    "- comparação entre estruturas incompatíveis;":
        "- uso indevido do ativo-base como chave de cálculo em vez de structure_id;",

    "- opções de vencimentos diferentes forem comparadas sem aviso;":
        "- a estrutura possuir opções com vencimentos diferentes sem destaque explícito na análise;",

    "- estruturas de ativos-base diferentes forem comparadas;":
        "- o cálculo tentar carregar pernas, snapshots ou métricas de mais de uma estrutura;",

    "- curva fixada e curva atual usarem escalas incompatíveis.":
        "- curva de payoff no vencimento e marcação atual forem exibidas sem separação clara.",

    "Não é possível comparar estruturas com ativos-base diferentes ou preços de referência incompatíveis.":
        "A análise de payoff é individual por estrutura. Selecione uma única estrutura e use structure_id como chave de cálculo. O ativo-base pode se repetir em outras estruturas.",

    "validateComparableStructures()":
        "validateSingleStructurePayoffScope()",

    "- Estruturas de ativos diferentes não puderem ser comparadas sem alerta.":
        "- O payoff usar structure_id como chave principal e não carregar dados apenas por ativo-base.",

    "- comparação entre duas estruturas incompatíveis.":
        "- tentativa de calcular payoff com múltiplas structure_id no mesmo contexto.",

    "comparação entre duas estruturas incompatíveis":
        "tentativa de calcular payoff com múltiplas estruturas no mesmo contexto",

    "comparar estruturas incompatíveis":
        "misturar dados de estruturas diferentes no mesmo cálculo de payoff",

    "Estruturas de ativos diferentes":
        "Estruturas diferentes",

    "estruturas de ativos-base diferentes":
        "estruturas diferentes",
}

for old, new in replacements.items():
    text = text.replace(old, new)

consolidated = """## Consolidação final — regra de payoff por estrutura individual

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
"""

headings_to_replace_from = [
    "## Consolidação final — regra de payoff por estrutura individual",
    "## Regra revisada — análise de payoff por estrutura individual",
]

cut_index = None

for heading in headings_to_replace_from:
    idx = text.find(heading)
    if idx != -1:
        if cut_index is None or idx < cut_index:
            cut_index = idx

if cut_index is not None:
    text = text[:cut_index].rstrip() + "\n\n" + consolidated + "\n"
else:
    text = text.rstrip() + "\n\n" + consolidated + "\n"

path.write_text(text, encoding="utf-8")

print(f"OK: documento atualizado: {path}")
print(f"Backup criado em: {backup}")
