# FONTE_DA_VERDADE

## Decisão consolidada

Conforme definição já estabelecida em documentação anterior, o diretório oficial de dados do projeto foi alterado de `data/` para `dados/`.

Essa decisão não está em aberto e deve ser considerada a convenção definitiva adotada pelo projeto, salvo revisão futura explicitamente documentada.

---

## Motivo da padronização

A mudança de `data/` para `dados/` foi consolidada para eliminar ambiguidades recorrentes em:

- buscas textuais no código;
- leitura de documentação;
- interpretação de logs;
- prompts e instruções operacionais;
- discussões técnicas sobre schema, ingestão e persistência.

O termo `data` gerava confusão entre:

- **data como armazenamento de dados**;
- **data como referência temporal** (dia, mês, ano, timestamp, datetime).

Ao adotar `dados/`, o projeto passa a distinguir com clareza:

- **`dados/`** → conteúdo de dados, arquivos, insumos, saídas e estruturas persistidas;
- **data/datetime/timestamp** → informação temporal.

---

## Convenção oficial vigente

A partir da consolidação desta decisão:

- o diretório oficial de dados é **`dados/`**;
- referências novas não devem usar `data/` como pasta principal;
- documentação, scripts, queries, utilitários e automações devem priorizar `dados/`;
- ocorrências legadas de `data/` devem ser tratadas como herança técnica a ser migrada gradualmente.

---

## Regra prática

Sempre interpretar:

- `dados/raw/` como origem bruta;
- `dados/derived/` como derivados/processados;
- `dados/tmp/` como artefatos temporários, quando aplicável;
- `dados/exports/` como saídas exportáveis, quando aplicável.

Caso existam caminhos antigos usando `data/`, eles devem ser considerados legados e revisados progressivamente.

---

## Fonte oficial

Até segunda ordem documentada, a fonte da verdade para armazenamento em disco, contratos de arquivos e organização de diretórios é a árvore sob `dados/`.

Toda nova implementação deve partir dessa convenção.
