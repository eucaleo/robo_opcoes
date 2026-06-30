# Índice de Documentação

Atualizado em: 2026-06-30 18:42:54

## Documentos principais

### Plano RTD Excel Vivo

Arquivo:

    docs/PLANO_RTD_EXCEL_VIVO.md

Uso:

    descreve a arquitetura alvo com Excel LISTA_RTD.xlsm aberto, coletor Python online, snapshot em app.db, histórico intraday, candles, VWAP e UI operacional viva

### Arquitetura de Bancos

Arquivo:

    docs/ARQUITETURA_BANCOS.md

Uso:

    define dados/app.db como banco canônico operacional e dados/derived.db como banco de derivados

### Rota de Desenvolvimento

Arquivo:

    docs/ROTA_DESENVOLVIMENTO.md

Uso:

    organiza os marcos de evolução do projeto e os critérios de conclusão de cada fase

### Auditoria de Desenvolvimento

Arquivo:

    docs/AUDITORIA_DESENVOLVIMENTO.md

Uso:

    registra decisões, testes, fases concluídas, pendências e commits

## Decisão central

Fonte oficial de mercado vivo:

    dados/app.db

Banco de derivados:

    dados/derived.db

Excel RTD vivo:

    LISTA_RTD.xlsm

## Regra crítica

Não manter sincronização contínua entre app.db e derived.db para cotação viva.

## Próximo passo técnico

Depois da documentação, a próxima etapa é implementar o contrato técnico:

    defaults de RTD para dados/app.db
    constantes centrais de banco
    teste de regressão
    desativação segura de RTD ativo em derived.db
