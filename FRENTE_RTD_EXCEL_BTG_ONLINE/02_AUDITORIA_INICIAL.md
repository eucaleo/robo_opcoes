# Auditoria inicial da frente RTD Excel BTG Online

## Objetivo

Registrar o ponto de partida antes de qualquer alteração funcional.

## Status inicial esperado

A frente começa com:

- Banco único `dados/app.db`.
- Pasta `dados/` limpa de TXT de testes e backups antigos.
- Git sem alterações pendentes antes da criação desta documentação.
- Nova pasta de trabalho isolada na raiz do projeto.

## Itens a auditar

### Código relacionado a Excel e RTD

Buscar referências a:

- RTD.
- Excel.
- BTG.
- `LISTA_RTD.xlsm`.
- `RTD_LINKS.csv`.
- `RTD_UNDERLYING_QUOTES.csv`.
- `win32com`.
- `xlwings`.
- `openpyxl`.

### Código relacionado a subprocessos

Buscar chamadas que possam estar sendo usadas para consulta sob demanda:

- `subprocess`.
- `Popen`.
- `run`.
- scripts externos ligados a RTD.
- botões de preenchimento por RTD.

### Banco de dados

Auditar:

- Tabelas existentes.
- Tabelas residuais.
- Campos que já possam servir para snapshot.
- Campos que já possam servir para histórico intraday.
- Scripts de migração relacionados.

### UI

Auditar:

- Botões ligados a RTD.
- Painéis de opções.
- Preenchimento de legs.
- Atualização de estruturas.
- Tela de status ou menu Ajuda.

## Saídas geradas automaticamente

Os relatórios da auditoria ficam em:

`FRENTE_RTD_EXCEL_BTG_ONLINE/output/`

## Próximo passo após auditoria

Com base nos relatórios:

1. Montar inventário do que já existe.
2. Classificar arquivos entre:
   - manter;
   - reaproveitar;
   - adaptar;
   - remover;
   - investigar.
3. Propor Fase 1 com menor alteração possível.
