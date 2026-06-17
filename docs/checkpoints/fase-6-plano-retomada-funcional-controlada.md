# Fase 6 — Plano de retomada funcional controlada

## Objetivo

Preparar a retomada funcional do projeto após a conclusão documental da Fase 5 — Reconciliação RTD/Excel, mantendo controle de impacto, rastreabilidade e validação antes de qualquer alteração funcional.

Esta fase não autoriza alteração ampla em UI, API, repository, serviço ou banco sem mapa de impacto específico.

---

## Estado de entrada

Branch: fase-12-fechamento-ciclo

Último commit documental conhecido: b50137a docs: atualiza status da rota mestre apos fase 5 rtd

---

## Escopo permitido

Nesta etapa, é permitido apenas:

1. levantar o estado atual do repositório;
2. identificar bancos locais existentes;
3. verificar a existência ou ausência da tabela rtd_option_quotes;
4. mapear referências funcionais à tabela e à aba RTD_OPTION_QUOTES;
5. registrar evidências documentais;
6. preparar decisão controlada para eventual retomada funcional.

---

## Escopo proibido

Nesta etapa, não está autorizado:

- alterar UI;
- alterar API;
- alterar repositories;
- alterar services;
- criar tabela automaticamente;
- executar migração destrutiva;
- limpar arquivos operacionais;
- versionar bancos locais;
- alterar o contrato da ponte Excel/RTD.

---

## Comandos planejados de inspeção

- git status
- git log --oneline -10
- find . \( -iname "*.db" -o -iname "*.sqlite" -o -iname "*.sqlite3" \) -type f
- grep -RIn "rtd_option_quotes" . --exclude-dir=.git --exclude="*.db" --exclude="*.sqlite" --exclude="*.sqlite3"
- grep -RIn "RTD_OPTION_QUOTES" . --exclude-dir=.git --exclude="*.db" --exclude="*.sqlite" --exclude="*.sqlite3"

---

## Arquivos autorizados nesta etapa

Inicialmente, apenas este documento:

- docs/checkpoints/fase-6-plano-retomada-funcional-controlada.md

Outros arquivos somente poderão ser alterados após novo mapa de impacto.

---

## Criação ou validação de tabela

Nesta etapa, a criação de tabela ainda não está autorizada.

A Fase 6 poderá apenas validar:

- se dados/app.db existe;
- se rtd_option_quotes existe;
- se há referências funcionais à tabela;
- se há referências à aba RTD_OPTION_QUOTES;
- qual decisão será necessária antes de qualquer criação, migração ou ajuste funcional.

---

## Testes planejados

Testes inicialmente previstos:

- git status
- python -m pytest

Caso a suíte completa não esteja estável, testes específicos deverão ser definidos após o mapa de impacto.

---

## Critérios de encerramento

A Fase 6 somente poderá ser encerrada quando houver:

1. estado Git limpo;
2. bancos locais identificados;
3. existência ou ausência de rtd_option_quotes confirmada;
4. referências funcionais mapeadas;
5. decisão documentada sobre criação, validação ou postergação da tabela;
6. testes executados e resultados registrados;
7. commit documental de fechamento.

---

## Commit previsto

docs: registra plano da fase 6 retomada funcional controlada

---

## Resultado esperado

Ao final desta fase, o projeto deverá estar pronto para uma retomada funcional incremental, com escopo explícito, rastreabilidade preservada e sem alteração funcional não autorizada.
