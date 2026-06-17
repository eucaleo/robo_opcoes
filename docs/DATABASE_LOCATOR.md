# Database Locator & Scanner — estado reconciliado

## Status

Documento reconciliado na Fase 4.2.

Este documento substitui a orientação anterior que citava scripts de localização de banco não confirmados como vivos.

A reconciliação é documental. Não altera comportamento funcional.

## Objetivo

Registrar o estado atual da localização de bancos SQLite e apontar a fonte técnica candidata para centralização futura.

## Bancos reconhecidos no contrato atual

| Papel | Caminho padrão |
|---|---|
| Banco operacional / raw | `dados/app.db` |
| Banco derivado / recalculável | `dados/derived.db` |
| Bancos de resgate/auditoria | `_resgate_db/estado_schema_atual/*.db` |

## Artefatos auxiliares relacionados

| Papel | Caminho padrão |
|---|---|
| Bridge Excel/RTD | `bridge/*.csv` |
| Marcador de última exportação | `bridge/last_export.txt` |

## Fonte técnica candidata

O arquivo `db/config.py` é o candidato natural a fonte técnica central para resolução de caminhos de banco.

Ele define:

- `APP_DB_PATH`;
- `DERIVED_DB_PATH`;
- `connect_app()`;
- `connect_derived()`.

Contrato observado:

- `APP_DB_PATH` vem da variável de ambiente `APP_DB_PATH` ou, na ausência dela, de `dados/app.db`;
- `DERIVED_DB_PATH` vem da variável de ambiente `DERIVED_DB_PATH` ou, na ausência dela, de `dados/derived.db`.

## Sobre scripts citados anteriormente

Versões anteriores deste documento citavam comandos como:

- `python scripts/db_locator.py`;
- `bash scripts/find_dbs.sh`;
- `python scripts/db_locator.py --save-report`;
- `python scripts/db_path_doctor.py`.

Esses comandos não devem ser considerados contrato operacional enquanto os respectivos scripts não forem confirmados, recriados ou substituídos.

## Estado atual da resolução de caminhos

A auditoria documental identificou que a resolução de caminhos ainda está parcialmente distribuída por:

- `db/config.py`;
- scripts em `scripts/`;
- módulos em `db/`;
- componentes de `UI/`;
- services;
- repositories.

A centralização funcional ainda não foi feita nesta fase.

## Diretriz para próxima fase funcional

Uma fase posterior pode reconciliar código para reduzir divergências, preferencialmente usando `db/config.py` como ponto central.

Essa fase futura deve:

1. mapear consumidores;
2. definir contrato técnico;
3. alterar um grupo pequeno por vez;
4. validar comportamento;
5. evitar trocar caminhos de forma ampla sem teste.

## Regra preservada

Diagnóstico primeiro. Alteração funcional somente após contrato reconciliado.
