# Ciclo 2 — Fase 7A — Auditoria estática RTD/opções

## Objetivo

Mapear, sem alteração funcional, o estado atual da frente RTD/opções, com foco em:

- `rtd_option_quotes`
- `dados/RTD_LINKS.csv`
- persistência/importação de cotações RTD de opções
- pontos de leitura existentes
- ausência ou presença de rotina de escrita/importação

## Estado inicial

Branch:

```text
ciclo-2-testes-evolucao
```

Checkpoint criado após auditoria estática por nomes e referências relacionadas a RTD, opções, cotações e importação.

## Arquivos/localizações relevantes encontrados

Busca por nomes de arquivos relacionados retornou os principais pontos abaixo:

```text
./LISTA_RTD.xlsx
./OPERACOES_E_OPCOES.xlsm
./dados/RTD_LINKS.csv
./docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md
./docs/fase_2_auditoria_contrato_rtd_excel.md
./docs/fase_2_diagnostico_csvs_rtd_excel.json
./docs/fase_2_diagnostico_csvs_rtd_excel.md
./docs/fase_2_mapa_contrato_rtd_excel.md
./docs/fase_3_diagnostico_persistencia_rtd_opcoes.json
./docs/fase_3_diagnostico_persistencia_rtd_opcoes.md
./docs/lista_priorizada_automacao_opcoes_rtd.md
./docs/mapeamento_automacao_opcoes_rtd.json
./docs/mapeamento_automacao_opcoes_rtd.md
./repositories/rtd_option_quotes_repository.py
./scripts/mapear_automacao_opcoes_rtd.py
```

## Achados principais

### 1. `dados/RTD_LINKS.csv`

O arquivo existe e já foi classificado em documentação anterior como fonte local/exportação da aba `RTD_LINKS`.

Contrato documentado anteriormente:

```text
codigo_opcao
ativo_base
campo
valor
atualizado_em
```

Papel provável:

- entrada bruta operacional;
- origem de atributos/cotações de opções vindos de Excel/RTD;
- fonte candidata para alimentar `rtd_option_quotes`.

### 2. `rtd_option_quotes`

A tabela já aparece documentada em auditorias anteriores como staging/persistência de cotações RTD/opções.

Schema documentado anteriormente inclui:

```text
codigo_opcao
ativo_base
call_put
strike
vencimento
ultimo_preco
ultima_quantidade
bid
ask
volume
iv
delta
gamma
theta
vega
source
raw_json
updated_at
created_at
```

Com restrição lógica importante:

```text
UNIQUE(codigo_opcao)
```

### 3. `repositories/rtd_option_quotes_repository.py`

O arquivo existe e aparece como ponto de leitura da tabela `rtd_option_quotes`.

Papel identificado:

- repositório de leitura;
- não foi identificado, nesta auditoria estática, como importador ou escritor principal;
- deve permanecer como fronteira aceitável de acesso à tabela staging.

### 4. Rotina de escrita/importação

A auditoria estática ampla encontrou muitas referências documentais e históricas, mas não evidenciou rotina ativa versionada atual, em código Python ou SQL, responsável por:

- ler `dados/RTD_LINKS.csv`;
- normalizar formato atributo/valor;
- fazer `INSERT`, `UPDATE` ou `UPSERT` em `rtd_option_quotes`.

Há menções históricas a `scripts/patch_73_rtd_option_quotes.py`, porém o arquivo não apareceu como arquivo ativo no resultado de busca por nomes.

## Observações sobre o grep amplo

Foi executada busca ampla por termos relacionados a:

```text
RTD
rtd
opção/opções
option/options
quote/quotes
cotação/cotações
```

O resultado foi muito extenso porque incluiu:

- documentação histórica em `docs/`;
- caches de teste;
- JSONs de auditoria;
- checkpoints anteriores;
- backups em `_repo_audit/`;
- dados operacionais em `dados/`.

Conclusão operacional: a busca ampla serviu para confirmar histórico e contexto, mas não deve ser repetida como base da próxima fase. A próxima etapa deve usar buscas focadas por escrita/importação.

## Conclusão da Fase 7A

A frente RTD/opções possui:

- contrato CSV documentado em `dados/RTD_LINKS.csv`;
- tabela staging/persistência `rtd_option_quotes`;
- repositório de leitura `repositories/rtd_option_quotes_repository.py`;
- documentação anterior consistente sobre o papel operacional dessas peças.

Porém, no estado auditado, não foi localizada rotina ativa versionada que faça a importação/sincronização de `RTD_LINKS.csv` para `rtd_option_quotes`.

## Próxima fase sugerida

Fase 7B — auditoria focada de escrita/importação RTD/opções.

Objetivo:

- localizar com precisão qualquer `INSERT`, `UPDATE`, `UPSERT`, `to_sql`, `executemany`, `pandas.read_csv` ou rotina equivalente envolvendo:
  - `rtd_option_quotes`
  - `RTD_LINKS.csv`
  - `codigo_opcao`
  - `ultimo_preco`
  - `bid`
  - `ask`

Caso nenhuma rotina seja encontrada, a próxima decisão técnica será criar importador somente-leitura/idempotente para `RTD_LINKS.csv`, sem alterar UI ou cálculo.
