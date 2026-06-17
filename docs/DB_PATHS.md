# DB Paths — contrato documental

## Status

Documento reconciliado na Fase 4.2.

Este documento registra o contrato atual de caminhos de banco e artefatos auxiliares do projeto.

A reconciliação é documental. Não altera comportamento funcional.

## Contrato atual

| Papel | Caminho padrão | Observação |
|---|---|---|
| Banco operacional / raw | `dados/app.db` | Base principal de cadastro, estado operacional, RTD e estruturas |
| Banco derivado / recalculável | `dados/derived.db` | Base de resultados derivados, snapshots e dados recalculáveis |
| Bridge Excel/RTD | `bridge/*.csv` | Arquivos CSV exportados pelo bridge |
| Marcador de última exportação | `bridge/last_export.txt` | Arquivo auxiliar do bridge |
| Bancos de resgate/auditoria | `_resgate_db/estado_schema_atual/*.db` | Cópias de inspeção/resgate, não são fonte operacional |

## Fonte técnica candidata

O arquivo `db/config.py` é o candidato natural a fonte técnica central para resolução de caminhos de banco.

Ele define atualmente:

- `APP_DB_PATH`;
- `DERIVED_DB_PATH`;
- `connect_app()`;
- `connect_derived()`.

Comportamento observado em `db/config.py`:

- `APP_DB_PATH` usa a variável de ambiente `APP_DB_PATH`, se definida;
- caso contrário, usa `dados/app.db`;
- `DERIVED_DB_PATH` usa a variável de ambiente `DERIVED_DB_PATH`, se definida;
- caso contrário, usa `dados/derived.db`;
- os caminhos são resolvidos a partir da raiz do projeto;
- as funções de conexão criam a pasta de destino quando necessário.

## Regra operacional atual

Enquanto não houver alteração funcional reconciliada:

1. `dados/app.db` permanece como banco operacional/raw padrão;
2. `dados/derived.db` permanece como banco derivado/recalculável padrão;
3. scripts, UI, services e repositories que ainda usam caminhos próprios devem ser tratados como pontos a reconciliar em fase posterior;
4. nenhuma mudança funcional deve ser feita apenas por este documento.

## Pontos conhecidos de divergência

Foram identificados usos ainda descentralizados de caminhos, incluindo padrões como:

- `dados/app.db`;
- `./dados/app.db`;
- `dados/derived.db`;
- `Path("dados/app.db")`;
- constantes locais em scripts, services e repositories;
- resolução própria em componentes de UI/facade.

Esses pontos devem ser tratados em fase funcional futura, após contrato aprovado.

## Scripts de diagnóstico

Versões anteriores da documentação citavam scripts como:

- `scripts/db_locator.py`;
- `scripts/db_path_doctor.py`;
- `scripts/find_dbs.sh`.

Na reconciliação da Fase 4.2, esses scripts não foram assumidos como comandos vivos.

Se forem recriados ou substituídos futuramente, este documento deve ser atualizado com comandos existentes e validados.

## Regra preservada

Diagnóstico primeiro. Alteração funcional somente após contrato reconciliado.
