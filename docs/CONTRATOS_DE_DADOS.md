# CONTRATOS_DE_DADOS

## Premissa estrutural

Este documento assume como convenção oficial que os contratos de arquivos e diretórios do projeto se organizam sob a raiz `dados/`.

A nomenclatura `data/` não deve ser usada como referência principal em novos contratos, por ter sido substituída documentalmente por `dados/`.

---

## Raízes contratuais

### Dados brutos
- `dados/raw/`

Contém arquivos de entrada, extrações originais, dumps, imports e insumos ainda não transformados.

### Dados derivados
- `dados/derived/`

Contém saídas transformadas, tabelas intermediárias materializadas, agregações, enriquecimentos e datasets prontos para consumo interno.

### Temporários
- `dados/tmp/`

Contém artefatos transitórios de processamento, passíveis de recriação.

### Exportações
- `dados/exports/`

Contém arquivos finais de saída para consumo externo, integração ou entrega.

---

## Regra de nomenclatura

Para evitar ambiguidade:

- usar `dados` para diretórios e contratos de armazenamento;
- usar `data`, `datetime`, `timestamp` e derivados apenas para campos temporais.

Exemplos de campos temporais adequados:
- `data_referencia`
- `data_processamento`
- `timestamp_ingestao`
- `datetime_atualizacao`

---

## Compatibilidade legada

Se algum processo ainda consumir `data/`, isso deve ser tratado como compatibilidade temporária e não como convenção oficial.

Toda evolução contratual nova deve nascer em conformidade com `dados/`.
