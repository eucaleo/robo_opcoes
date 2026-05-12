# STATUS_MIGRACAO_ATUAL

## Estado atual

**Status:** em progresso controlado  
**Situação geral:** base documental consolidada para retomada segura  
**Decisão estrutural vigente:** diretório principal de dados padronizado como `dados/`

---

## Escopo atualmente estabilizado

Os documentos-base de continuidade e retomada consideram como definição já estabelecida que:

- o projeto deve usar `dados/` como diretório principal de dados;
- `data/` passa a ser tratado como nomenclatura legada;
- a mudança ocorreu para reduzir ambiguidades semânticas entre:
  - dados persistidos do sistema;
  - valores temporais como data, datetime e timestamp.

---

## O que já está definido

- A convenção oficial de armazenamento em disco foi consolidada em `dados/`;
- A documentação futura deve refletir essa convenção;
- Novas rotinas não devem nascer apontando para `data/`;
- Referências antigas em código, scripts e documentação devem ser identificadas e ajustadas de forma incremental.

---

## Impacto esperado

A adoção de `dados/` como padrão reduz:

- confusão em buscas por texto;
- interpretações ambíguas em discussões técnicas;
- colisões semânticas entre domínio de dados e domínio temporal;
- risco de erro em manutenção e onboarding.

---

## Limites do estado atual

Ainda pode haver:

- scripts legados usando `data/`;
- documentação antiga com nomenclatura anterior;
- automações ou configurações que dependam do caminho antigo.

Esses pontos não invalidam a decisão consolidada: apenas indicam necessidade de migração e saneamento gradual.

---

## Foco atual

Garantir que todos os documentos centrais da retomada e da arquitetura passem a refletir explicitamente a convenção `dados/` como fonte oficial.

---

## Critério de consistência

Considera-se consistente o estado em que:

- a documentação central usa `dados/`;
- `data/` aparece apenas como legado ou referência histórica;
- o próximo passo operacional esteja claramente documentado para eliminar resíduos da convenção antiga.
