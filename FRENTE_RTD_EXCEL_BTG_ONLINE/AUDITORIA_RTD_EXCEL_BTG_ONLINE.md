# Auditoria RTD Excel BTG Online

## Objetivo

Registrar a evolução da frente RTD Excel BTG Online conforme as regras do projeto.

## Regras validadas nesta etapa

- Excel RTD tratado como ponte temporária.
- Dados permanentes devem ficar no SQLite.
- Artefatos gerados não devem ser versionados.
- Arquivos grandes não devem entrar no repositório.
- Toda alteração deve ter teste automatizado.
- Toda alteração concluída e testada deve ser commitada.

## Estado atual

- Bridge RTD_OPTION_QUOTES criado.
- Testes da frente RTD executados com sucesso.
- Suite ATT executada com sucesso.
- Push realizado para origin/refactor/bd-unico-appdb.
- Detectado alerta do GitHub para arquivos grandes em output.
- Criado guardrail para impedir versionamento de artefatos gerados e arquivos acima de 50 MB.

## Testes esperados

- ATT/tests/test_repository_generated_artifacts_guardrail.py
- Suite ATT completa

## Fase 1A - Status RTD Excel Online

### Objetivo

Criar uma camada backend para verificar o estado da conexão Excel RTD antes de integrar com a UI.

### Itens cobertos

- Verificação de disponibilidade do pywin32.
- Verificação de Excel aberto via COM.
- Verificação de workbook LISTA_RTD.xlsm aberto.
- Verificação da aba RTD_OPTION_QUOTES.
- Validação dos cabeçalhos obrigatórios por nome.
- Aceitação de colunas movidas na planilha.
- Status consolidado por objeto reutilizável.

### Regra operacional validada

O sistema não depende da posição física fixa das colunas. A validação usa os cabeçalhos da linha 1.

### Teste criado

- ATT/tests/test_excel_rtd_connection_status.py
