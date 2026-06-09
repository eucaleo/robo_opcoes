# Auditoria Fase 1/2 — Estado Atual Após Limpeza Inicial

Data: 09/06/2026  
Branch: limpeza-inicial-repositorio

## Contexto

Este registro consolida o estado atual do projeto após a limpeza inicial do banco local e validações de integridade.

O objetivo é manter a evolução alinhada à ROTA MESTRE:

- Excel apenas como gateway RTD.
- Banco do sistema como fonte da verdade.
- Estruturas operacionais devem nascer no sistema.
- Abas e CSVs derivados antigos são legado, não fonte principal.
- Toda mudança concluída e testada deve ser registrada e commitada.

## Estado anterior identificado

O banco dados/app.db continha estruturas inválidas para uso operacional ou teste:

- estruturas vencidas;
- estruturas desatualizadas;
- estruturas duplicadas;
- estruturas sem legs;
- estruturas sem vínculo operacional confiável;
- registros de auditoria apontando para estruturas removidas.

Conclusão: as estruturas existentes no banco não serviam como base operacional nem como base de teste.

## Limpeza realizada

Foram removidos registros órfãos de structure_audit_log.

Antes da limpeza, PRAGMA foreign_key_check apontava inconsistências na tabela structure_audit_log.

Também foi criado/verificado índice único para evitar duplicidade de estrutura ativa por alias_legacy_aba.

## Estado atual do banco canônico

Resultado validado:

- structures: 0
- structure_legs: 0
- structure_audit_log: 0
- foreign_key_check: sem pendências

Conclusão:

- o cadastro canônico de estruturas está limpo;
- não há estruturas operacionais válidas cadastradas;
- não há legs canônicas cadastradas;
- não há logs de auditoria órfãos;
- o banco não apresenta erro de chave estrangeira após a limpeza.

## Estado atual dos dados RTD/bridge

As abas atualmente presentes na camada RTD derivada são:

- BOVA11
- EMBJ3
- PRIO3
- SBSP3
- SMAL11

Com legs em rtd_analise_robo_legs:

- BOVA11: 4 legs
- EMBJ3: 4 legs
- PRIO3: 4 legs
- SBSP3: 4 legs
- SMAL11: 4 legs

Observação: esses dados não devem ser tratados como cadastro canônico de estruturas.

## Decisão fixada

Não reconstruir automaticamente structures e structure_legs a partir de dados derivados antigos.

O cadastro canônico deverá ser reconstruído de maneira controlada, por fluxo próprio do sistema, com validações e persistência correta.

## Problema técnico identificado

O fluxo atual de cadastro/salvamento de estruturas permite inconsistências:

- criação de estrutura ativa sem legs;
- criação de cabeçalho antes de persistir legs;
- ausência de atomicidade entre estrutura e legs;
- risco de deixar estrutura órfã em caso de falha;
- necessidade de validação de alias enquanto houver vínculo legado com abas RTD.

## Próximas ações

1. Formalizar classificação das fontes da bridge.
2. Auditar dependências restantes do Excel e CSVs derivados.
3. Definir contrato RTD bruto.
4. Consolidar ingestão bruta RTD.
5. Corrigir cadastro/persistência de estruturas com validações.
6. Tornar criação de estrutura + legs uma operação atômica.
7. Garantir que a UI consuma dados do sistema, não CSV derivado antigo.

## Critério de fechamento deste marco

Este marco considera encerrado o avanço inicial quando:

- banco canônico está limpo;
- inconsistências de FK foram eliminadas;
- lixo de estruturas antigas não será reutilizado;
- estado atual foi documentado;
- documentação foi versionada em commit próprio.
