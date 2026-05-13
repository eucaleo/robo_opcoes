# PLANO_V2

## Objetivo estratégico

Consolidar a evolução do projeto com base em uma arquitetura mais clara, menos ambígua e mais segura para manutenção incremental.

---

## Decisão estrutural já incorporada

Como parte da consolidação documental, o diretório raiz de armazenamento foi padronizado como `dados/` em substituição a `data/`.

Essa mudança já deve ser tratada como decisão tomada, motivada por clareza semântica e redução de erros operacionais.

---

## Justificativa

A nomenclatura anterior `data/` gerava ambiguidade entre:

- estrutura de dados do projeto;
- conceitos temporais como data, datetime e timestamp.

A adoção de `dados/` reduz ruído técnico e melhora:
- busca textual no repositório;
- leitura de código;
- interpretação da arquitetura;
- comunicação entre manutenção, documentação e operação.

---

## Estratégia de evolução

### Fase 1 — Consolidação documental
- refletir `dados/` nos documentos centrais;
- registrar `data/` como legado;
- alinhar fonte da verdade, arquitetura e plano operacional.

### Fase 2 — Mapeamento do legado
- localizar ocorrências remanescentes de `data/`;
- separar diretório estrutural de uso temporal legítimo;
- priorizar substituições seguras.

### Fase 3 — Migração incremental
- ajustar configs e scripts de menor risco;
- corrigir documentação residual;
- validar compatibilidade de rotinas dependentes.

### Fase 4 — Saneamento
- reduzir dependência de aliases legados;
- confirmar consistência entre documentação e implementação;
- estabilizar o uso exclusivo de `dados/` como convenção principal.

---

## Checkpoints

- Documentação central refletindo `dados/`;
- Fonte da verdade explícita;
- Próxima ação operacional definida;
- Levantamento do legado preparado;
- Primeiras substituições seguras executadas.

---

## Critério de avanço

Cada etapa deve terminar com:
- resultado verificável;
- impacto compreendido;
- próximo passo único e objetivo;
- registro no diário técnico.

---

## Estado atual do plano

O projeto encontra-se na fase de consolidação documental e preparação para mapeamento do legado associado à nomenclatura `data/`.
