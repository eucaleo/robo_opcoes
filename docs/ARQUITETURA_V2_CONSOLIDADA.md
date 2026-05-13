# ARQUITETURA_V2_CONSOLIDADA

## Consolidação arquitetural

A arquitetura vigente adota `dados/` como diretório raiz para persistência em disco relacionada ao domínio de dados do projeto.

Essa convenção substitui a nomenclatura anterior `data/`, mantida apenas como referência legada em componentes ainda não saneados.

---

## Diretriz estrutural

A separação semântica oficial passa a ser:

- **`dados/`** para arquivos, insumos, saídas, derivados e persistência;
- **data / datetime / timestamp** para informação temporal de domínio.

Essa distinção melhora a clareza arquitetural e reduz ambiguidades em código, documentação e operação.

---

## Organização esperada

Exemplo de organização consolidada:

- `dados/raw/`
- `dados/derived/`
- `dados/tmp/`
- `dados/exports/`

A existência exata de cada subdiretório depende do projeto, mas a raiz oficial deve ser `dados/`.

---

## Efeito sobre componentes

Todos os componentes novos devem:

- ler e escrever sob `dados/`, quando aplicável;
- evitar criar novas dependências estruturais com `data/`;
- explicitar quando um campo representa tempo, usando nomes como:
  - `data_referencia`
  - `data_evento`
  - `timestamp_processamento`
  - `datetime_execucao`

---

## Diretriz de migração

Componentes legados com referência a `data/` devem ser ajustados progressivamente, priorizando:

1. documentação central;
2. configurações de caminho;
3. scripts de ingestão e exportação;
4. utilitários de suporte;
5. código residual de baixo risco.

---

## Estado consolidado

A arquitetura documental já considera `dados/` como convenção oficial.
