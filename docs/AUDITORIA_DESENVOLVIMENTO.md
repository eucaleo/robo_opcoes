# Auditoria de Desenvolvimento

Atualizado em: 2026-06-30 18:42:54

## Objetivo

Registrar decisões, fases concluídas, testes executados e pendências controladas.

## Decisão congelada nesta etapa

A fonte oficial de mercado vivo é:

    dados/app.db

O banco dados/derived.db fica reservado para:

    derivados
    caches
    payoff
    simulações
    artefatos regeneráveis

Não haverá sync contínuo entre app.db e derived.db para cotação viva.

## Estado operacional informado

Foi confirmado que dados vivos existem em app.db:

    rtd_option_quotes com 11 linhas
    rtd_underlying_quotes com 2 linhas

Foi confirmado que os testes específicos passaram:

    ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py
    ATT/tests/test_market_snapshot_selector.py

Resultado informado:

    6 passed

## Fases

### Fase documental: alinhamento da rota RTD vivo

Status:

    em execução

Entregas esperadas:

    docs/PLANO_RTD_EXCEL_VIVO.md
    docs/ARQUITETURA_BANCOS.md
    docs/ROTA_DESENVOLVIMENTO.md
    docs/AUDITORIA_DESENVOLVIMENTO.md
    docs/INDICE_DOCUMENTACAO.md
    README.md atualizado com seção controlada

Validações esperadas:

    documentos existem
    app.db está documentado como fonte oficial de mercado vivo
    derived.db está documentado como derivados e artefatos regeneráveis
    regra contra sync contínuo está documentada
    fases RTD vivo estão documentadas

### Próxima fase: contrato técnico de bancos

Status:

    pendente

Objetivo:

    alterar defaults de RTD para dados/app.db
    criar constantes centrais de caminho
    criar teste de regressão
    impedir retorno de RTD vivo para derived.db

## Pendências controladas

    revisar pontos do código que ainda apontam RTD para derived.db
    criar contrato central de caminhos
    arquivar tabelas RTD antigas em derived.db após testes
    implementar detecção do Excel LISTA_RTD.xlsm aberto
    implementar coletor RTD online
    incluir resumo de conexão no menu ajuda

## Regra de atualização

Este arquivo deve ser atualizado ao final de cada fase testada.

Cada fase concluída deve registrar:

    data
    alteração feita
    testes executados
    resultado
    commit
    pendências restantes
